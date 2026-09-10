#!/usr/bin/env python3
"""Capture and validate project-neutral production HTTP response matrices.

The helper deliberately uses only the Python standard library. It validates
observed response contracts; it does not infer rankings, indexing, or citation
outcomes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_VERSION = "1.0.0"
SENSITIVE_HEADERS = {
    "authorization",
    "cookie",
    "proxy-authorization",
    "set-cookie",
}


def _text(value: str) -> str:
    return re.sub(r"\s+", " ", unescape(value)).strip()


def _header_map(headers: Any) -> dict[str, str]:
    if not isinstance(headers, dict):
        return {}
    return {str(key).lower(): str(value) for key, value in headers.items()}


def _media_type(value: str | None) -> str:
    return (value or "").split(";", 1)[0].strip().lower()


def _tokens(value: str | None) -> set[str]:
    return {token.strip().lower() for token in (value or "").split(",") if token.strip()}


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


class HTMLProbe(HTMLParser):
    """Collect only the HTML fields needed by the response contract."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.json_ld_parts: list[str] = []
        self.meta: dict[str, str] = {}
        self.canonical: str | None = None
        self._in_title = False
        self._in_h1 = False
        self._in_json_ld = False
        self._json_ld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag == "meta":
            name = attributes.get("name", "").lower()
            if name:
                self.meta[name] = attributes.get("content", "")
        elif tag == "link" and "canonical" in attributes.get("rel", "").lower().split():
            self.canonical = attributes.get("href") or None
        elif tag == "script" and "ld+json" in attributes.get("type", "").lower():
            self._in_json_ld = True
            self._json_ld_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False
        elif tag == "script" and self._in_json_ld:
            self._in_json_ld = False
            self.json_ld_parts.append("".join(self._json_ld_parts).strip())
            self._json_ld_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._in_h1:
            self.h1_parts.append(data)
        if self._in_json_ld:
            self._json_ld_parts.append(data)

    @property
    def title(self) -> str:
        return _text(" ".join(self.title_parts))

    @property
    def h1(self) -> str:
        return _text(" ".join(self.h1_parts))


def inspect_html(body: str) -> tuple[HTMLProbe, list[str]]:
    probe = HTMLProbe()
    try:
        probe.feed(body)
        probe.close()
    except Exception as exc:  # HTMLParser is permissive, but malformed input is evidence.
        return probe, [f"HTML parser error: {exc}"]
    return probe, []


def _json_ld_types(probe: HTMLProbe) -> set[str]:
    types: set[str] = set()
    for raw in probe.json_ld_parts:
        try:
            value = json.loads(raw)
        except json.JSONDecodeError:
            continue
        values = value if isinstance(value, list) else [value]
        for item in values:
            if not isinstance(item, dict):
                continue
            candidates = item.get("@type", [])
            if isinstance(candidates, str):
                candidates = [candidates]
            if isinstance(candidates, list):
                types.update(str(candidate) for candidate in candidates)
            graph = item.get("@graph")
            if isinstance(graph, list):
                for node in graph:
                    if isinstance(node, dict):
                        node_types = node.get("@type", [])
                        if isinstance(node_types, str):
                            node_types = [node_types]
                        if isinstance(node_types, list):
                            types.update(str(candidate) for candidate in node_types)
    return types


def _check_contains(errors: list[str], actual: str, expected: Any, label: str) -> None:
    for value in _as_list(expected):
        if str(value) not in actual:
            errors.append(f"{label} missing {value!r}")


def _check_not_contains(errors: list[str], actual: str, expected: Any, label: str) -> None:
    for value in _as_list(expected):
        if str(value) in actual:
            errors.append(f"{label} contains forbidden {value!r}")


def _validate_headers(response: dict[str, Any], expected: dict[str, Any], errors: list[str]) -> None:
    headers = _header_map(response.get("headers"))
    expected_headers = expected.get("headers", {})
    if isinstance(expected_headers, dict):
        for name, requirement in expected_headers.items():
            key = str(name).lower()
            if key not in headers:
                errors.append(f"missing header {name}")
                continue
            actual = headers[key]
            if isinstance(requirement, str):
                if actual != requirement:
                    errors.append(f"header {name} expected {requirement!r}, got {actual!r}")
            elif isinstance(requirement, dict):
                if "equals" in requirement and actual != str(requirement["equals"]):
                    errors.append(f"header {name} expected exact value {requirement['equals']!r}")
                _check_contains(errors, actual, requirement.get("contains"), f"header {name}")
                if "contains_tokens" in requirement:
                    actual_tokens = _tokens(actual)
                    for token in _as_list(requirement["contains_tokens"]):
                        if str(token).lower() not in actual_tokens:
                            errors.append(f"header {name} missing token {token!r}")

    vary_required = expected.get("vary_contains")
    if vary_required is not None:
        vary = _tokens(headers.get("vary"))
        for token in _as_list(vary_required):
            if str(token).lower() not in vary:
                errors.append(f"Vary missing token {token!r}")

    xrobots_required = expected.get("x_robots_contains")
    if xrobots_required is not None:
        _check_contains(errors, headers.get("x-robots-tag", "").lower(), [str(v).lower() for v in _as_list(xrobots_required)], "X-Robots-Tag")

    if expected.get("location_contains") is not None:
        _check_contains(errors, headers.get("location", ""), expected["location_contains"], "Location")


def _validate_html(body: str, expected: dict[str, Any], errors: list[str]) -> None:
    probe, parser_errors = inspect_html(body)
    errors.extend(parser_errors)
    html_expected = expected.get("html", {})
    if not isinstance(html_expected, dict):
        html_expected = {}

    if html_expected.get("title_required") and not probe.title:
        errors.append("HTML title is missing")
    if html_expected.get("description_required") and not probe.meta.get("description", "").strip():
        errors.append("meta description is missing")
    if html_expected.get("canonical_required") and not probe.canonical:
        errors.append("canonical link is missing")
    if html_expected.get("h1_required") and not probe.h1:
        errors.append("H1 is missing")
    _check_contains(errors, probe.title, html_expected.get("title_contains"), "title")
    _check_contains(errors, probe.meta.get("description", ""), html_expected.get("description_contains"), "meta description")
    _check_contains(errors, probe.h1, html_expected.get("h1_contains"), "H1")
    if html_expected.get("canonical_equals") is not None and probe.canonical != html_expected["canonical_equals"]:
        errors.append(f"canonical expected {html_expected['canonical_equals']!r}, got {probe.canonical!r}")
    robots = probe.meta.get("robots", "").lower()
    _check_contains(errors, robots, html_expected.get("robots_contains"), "robots meta")
    _check_not_contains(errors, robots, html_expected.get("robots_not_contains"), "robots meta")
    required_types = {str(value) for value in _as_list(html_expected.get("json_ld_types"))}
    if required_types:
        actual_types = _json_ld_types(probe)
        missing = sorted(required_types - actual_types)
        if missing:
            errors.append(f"JSON-LD missing @type values: {', '.join(missing)}")


def _validate_format(response: dict[str, Any], expected: dict[str, Any], errors: list[str]) -> None:
    body = str(response.get("body", ""))
    kind = expected.get("format")
    if kind == "html":
        _validate_html(body, expected, errors)
    elif kind == "markdown":
        try:
            body.encode("utf-8")
        except UnicodeEncodeError:
            errors.append("Markdown body is not valid UTF-8")
        if expected.get("markdown_links_any"):
            links = set(re.findall(r"\[[^\]]+\]\(([^)]+)\)", body))
            if not any(
                any(str(candidate) in link for link in links)
                for candidate in _as_list(expected["markdown_links_any"])
            ):
                errors.append("Markdown body has no required public recovery link")
    elif kind == "robots":
        directives = [line.strip() for line in body.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        if expected.get("robots_must_contain"):
            joined = "\n".join(directives).lower()
            _check_contains(errors, joined, [str(value).lower() for value in _as_list(expected["robots_must_contain"])], "robots.txt")
    elif kind == "sitemap":
        try:
            root = ET.fromstring(body)
            locations = [node.text or "" for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "loc"]
            minimum = int(expected.get("sitemap_min_urls", 0))
            if len(locations) < minimum:
                errors.append(f"sitemap has {len(locations)} URLs; expected at least {minimum}")
        except (ET.ParseError, ValueError) as exc:
            errors.append(f"invalid sitemap XML: {exc}")
    elif kind == "json":
        try:
            value = json.loads(body)
            if expected.get("json_object") and not isinstance(value, dict):
                errors.append("JSON response is not an object")
            for key in _as_list(expected.get("json_required_keys")):
                if not isinstance(value, dict) or key not in value:
                    errors.append(f"JSON response missing key {key!r}")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid JSON response: {exc.msg}")
    elif kind == "api":
        try:
            value = json.loads(body)
            if not isinstance(value, dict):
                errors.append("API health response is not a JSON object")
            for key in _as_list(expected.get("api_required_keys")):
                if not isinstance(value, dict) or key not in value:
                    errors.append(f"API health response missing key {key!r}")
        except json.JSONDecodeError as exc:
            errors.append(f"API health response is not valid JSON: {exc.msg}")
    elif kind == "asset":
        if not body and not response.get("body_bytes"):
            errors.append("asset response is empty")


def validate_response(response: dict[str, Any]) -> list[str]:
    """Return human-readable failures for one response record."""
    errors: list[str] = []
    expected = response.get("expect", {})
    if not isinstance(expected, dict):
        return ["expect must be an object"]

    response_id = response.get("id", "unknown")
    if response.get("error"):
        return [f"{response_id}: capture error: {response['error']}"]

    status = response.get("status")
    allowed_statuses = {int(value) for value in _as_list(expected.get("status"))}
    if allowed_statuses and status not in allowed_statuses:
        errors.append(f"{response_id}: status expected {sorted(allowed_statuses)}, got {status}")

    headers = _header_map(response.get("headers"))
    if expected.get("content_type") is not None:
        actual_type = _media_type(headers.get("content-type"))
        if actual_type != str(expected["content_type"]).lower():
            errors.append(f"{response_id}: content type expected {expected['content_type']!r}, got {actual_type!r}")
    if expected.get("content_type_prefix") is not None:
        actual_type = _media_type(headers.get("content-type"))
        if not actual_type.startswith(str(expected["content_type_prefix"]).lower()):
            errors.append(f"{response_id}: content type does not start with {expected['content_type_prefix']!r}")

    body = str(response.get("body", ""))
    _check_contains(errors, body, expected.get("body_contains"), f"{response_id} body")
    _check_not_contains(errors, body, expected.get("body_not_contains"), f"{response_id} body")
    _validate_headers(response, expected, errors)
    _validate_format(response, expected, errors)

    if expected.get("final_url_host") is not None:
        host = urllib.parse.urlsplit(str(response.get("url", ""))).netloc.lower()
        if host != str(expected["final_url_host"]).lower():
            errors.append(f"{response_id}: final host expected {expected['final_url_host']!r}, got {host!r}")

    return errors


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")
    responses = payload.get("responses")
    if not isinstance(responses, list) or not responses:
        return errors + ["responses must be a non-empty list"]

    by_id: dict[str, dict[str, Any]] = {}
    for response in responses:
        if not isinstance(response, dict):
            errors.append("response entry is not an object")
            continue
        response_id = str(response.get("id", ""))
        if not response_id or response_id in by_id:
            errors.append(f"duplicate or missing response id: {response_id!r}")
            continue
        by_id[response_id] = response
        errors.extend(validate_response(response))

    for group in payload.get("variant_groups", []):
        if not isinstance(group, dict):
            errors.append("variant group is not an object")
            continue
        group_id = str(group.get("id", "unknown"))
        ids = [str(value) for value in _as_list(group.get("response_ids"))]
        missing = [value for value in ids if value not in by_id]
        if missing:
            errors.append(f"variant group {group_id}: missing response IDs {missing}")
            continue
        selected = [by_id[value] for value in ids]
        if group.get("same_status") and len({item.get("status") for item in selected}) != 1:
            errors.append(f"variant group {group_id}: statuses differ")
        if group.get("different_content_type"):
            types = {_media_type(_header_map(item.get("headers")).get("content-type")) for item in selected}
            if len(types) < 2:
                errors.append(f"variant group {group_id}: content types are not separated")
        for token in _as_list(group.get("vary_contains")):
            for item in selected:
                if str(token).lower() not in _tokens(_header_map(item.get("headers")).get("vary")):
                    errors.append(f"variant group {group_id}: Vary missing {token!r} for {item.get('id')}")

    return errors


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_args: Any, **_kwargs: Any) -> None:
        return None


def _safe_request_headers(headers: Any) -> dict[str, str]:
    if not isinstance(headers, dict):
        return {}
    result: dict[str, str] = {}
    for name, value in headers.items():
        if str(name).lower() in SENSITIVE_HEADERS:
            raise ValueError(f"sensitive request header is not allowed in a matrix: {name}")
        result[str(name)] = str(value)
    return result


def capture_request(base_url: str, request_spec: dict[str, Any], timeout: float) -> dict[str, Any]:
    response: dict[str, Any] = {
        "id": request_spec.get("id"),
        "path": request_spec.get("path", "/"),
        "expect": request_spec.get("expect", {}),
    }
    url = urllib.parse.urljoin(base_url.rstrip("/") + "/", str(request_spec.get("path", "/")).lstrip("/"))
    try:
        headers = _safe_request_headers(request_spec.get("headers", {}))
        request = urllib.request.Request(
            url,
            headers=headers,
            method=str(request_spec.get("method", "GET")).upper(),
        )
        follow = bool(request_spec.get("follow_redirects", False))
        opener = urllib.request.build_opener() if follow else urllib.request.build_opener(_NoRedirectHandler)
        with opener.open(request, timeout=timeout) as result:
            raw = result.read()
            response.update(
                status=result.status,
                url=result.geturl(),
                headers=dict(result.headers.items()),
                body_bytes=len(raw),
                body=raw.decode(result.headers.get_content_charset() or "utf-8", errors="replace"),
            )
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        response.update(
            status=exc.code,
            url=exc.geturl(),
            headers=dict(exc.headers.items()),
            body_bytes=len(raw),
            body=raw.decode(exc.headers.get_content_charset() or "utf-8", errors="replace"),
        )
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        response["error"] = str(exc)
        response["url"] = url
    return response


def capture_spec(spec: dict[str, Any]) -> dict[str, Any]:
    base_url = str(spec.get("base_url", ""))
    if not urllib.parse.urlsplit(base_url).scheme:
        raise ValueError("spec.base_url must be an absolute HTTP(S) URL")
    timeout = float(spec.get("timeout_seconds", 20))
    requests = spec.get("requests")
    if not isinstance(requests, list) or not requests:
        raise ValueError("spec.requests must be a non-empty list")
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "base_url": base_url,
        "responses": [capture_request(base_url, item, timeout) for item in requests],
        "variant_groups": spec.get("variant_groups", []),
    }
    return payload


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--spec", type=Path, help="JSON request specification to capture and validate")
    source.add_argument("--captured", type=Path, help="JSON captured response matrix to validate")
    parser.add_argument("--output", type=Path, help="write captured matrix to this path")
    args = parser.parse_args(argv)

    try:
        payload = capture_spec(_load(args.spec)) if args.spec else _load(args.captured)
        if args.output and args.spec:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        errors = validate_payload(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAILED: {len(errors)} response validation error(s)")
        return 1

    print(f"PASS: {len(payload['responses'])} response(s) and {len(payload.get('variant_groups', []))} variant group(s) validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
