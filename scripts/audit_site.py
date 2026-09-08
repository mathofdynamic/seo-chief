#!/usr/bin/env python3
"""Dependency-free static same-origin SEO audit fallback for SEO Chief.

This intentionally does NOT execute JavaScript and does NOT predict rankings.
Use browser/rendering tools when available for rendered DOM/schema/performance.
"""
from __future__ import annotations

import argparse, json, time
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

UA = "seo-chief-audit/2.0 (+https://github.com/mathofdynamic/seo-chief)"
HTML_TYPES = ("text/html", "application/xhtml+xml")
MAX_BYTES = 4_000_000
SITEMAP_BYTES = 8_000_000
MAX_SITEMAPS = 50


def normalize(url: str, keep_query: bool = False) -> str | None:
    try:
        p = urlparse(url.strip())
    except Exception:
        return None
    if p.scheme not in {"http", "https"} or not p.netloc:
        return None
    path = p.path or "/"
    return urlunparse((p.scheme.lower(), p.netloc.lower(), path, "", p.query if keep_query else "", ""))


def same_origin(a: str, b: str) -> bool:
    pa, pb = urlparse(a), urlparse(b)
    return (pa.scheme.lower(), pa.netloc.lower()) == (pb.scheme.lower(), pb.netloc.lower())


def decode(body: bytes, content_type: str | None) -> str:
    charset = "utf-8"
    if content_type and "charset=" in content_type.lower():
        charset = content_type.lower().split("charset=", 1)[1].split(";", 1)[0].strip()
    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


@dataclass
class Fetch:
    requested: str
    final: str | None = None
    status: int | None = None
    content_type: str | None = None
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    error: str | None = None


def fetch(url: str, timeout: float, max_bytes: int = MAX_BYTES) -> Fetch:
    req = Request(url, headers={"User-Agent": UA, "Accept": "text/html,application/xml,text/xml,*/*;q=0.1"})
    try:
        with urlopen(req, timeout=timeout) as r:
            headers = {k.lower(): v for k, v in r.headers.items()}
            ctype = headers.get("content-type", "").split(";", 1)[0].lower() or None
            return Fetch(url, r.geturl(), r.status, ctype, headers, r.read(max_bytes + 1)[:max_bytes])
    except HTTPError as e:
        headers = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
        ctype = headers.get("content-type", "").split(";", 1)[0].lower() or None
        body = e.read(max_bytes) if hasattr(e, "read") else b""
        return Fetch(url, e.geturl(), e.code, ctype, headers, body, f"HTTP {e.code}")
    except (URLError, TimeoutError, OSError) as e:
        return Fetch(url, error=str(e))


class Parser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title_parts: list[str] = []; self.in_title = False
        self.title: str | None = None; self.meta: dict[str, str] = {}
        self.canonical: str | None = None; self.lang: str | None = None
        self.h1: list[str] = []; self.h2_count = 0; self.heading: str | None = None; self.heading_parts: list[str] = []
        self.links: list[str] = []; self.hreflang: list[dict[str, str]] = []
        self.images = 0; self.images_missing_alt = 0
        self.jsonld_count = 0; self.jsonld_types: set[str] = set(); self.jsonld_errors = 0
        self.in_jsonld = False; self.jsonld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower(); a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html": self.lang = a.get("lang") or self.lang
        elif tag == "title": self.in_title = True; self.title_parts = []
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name: self.meta[name] = a.get("content", "")
        elif tag == "link":
            rel = {x.lower() for x in a.get("rel", "").split()}
            if "canonical" in rel and a.get("href"): self.canonical = a["href"]
            if "alternate" in rel and a.get("hreflang") and a.get("href"):
                self.hreflang.append({"lang": a["hreflang"], "href": a["href"]})
        elif tag in {"h1", "h2"}:
            if tag == "h2": self.h2_count += 1
            self.heading = tag; self.heading_parts = []
        elif tag == "a" and a.get("href"): self.links.append(a["href"])
        elif tag == "img":
            self.images += 1
            if "alt" not in a: self.images_missing_alt += 1
        elif tag == "script" and a.get("type", "").lower() == "application/ld+json":
            self.in_jsonld = True; self.jsonld_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self.in_title:
            self.title = " ".join("".join(self.title_parts).split()) or None; self.in_title = False
        elif tag in {"h1", "h2"} and self.heading == tag:
            text = " ".join("".join(self.heading_parts).split())
            if tag == "h1" and text: self.h1.append(text)
            self.heading = None; self.heading_parts = []
        elif tag == "script" and self.in_jsonld:
            raw = "".join(self.jsonld_parts).strip(); self.jsonld_count += 1
            if raw:
                try: self._collect_types(json.loads(raw))
                except json.JSONDecodeError: self.jsonld_errors += 1
            self.in_jsonld = False; self.jsonld_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_title: self.title_parts.append(data)
        if self.heading: self.heading_parts.append(data)
        if self.in_jsonld: self.jsonld_parts.append(data)

    def _collect_types(self, value: object) -> None:
        if isinstance(value, dict):
            t = value.get("@type")
            if isinstance(t, str): self.jsonld_types.add(t)
            elif isinstance(t, list): self.jsonld_types.update(x for x in t if isinstance(x, str))
            for v in value.values(): self._collect_types(v)
        elif isinstance(value, list):
            for v in value: self._collect_types(v)


@dataclass
class Page:
    url: str; final_url: str | None; status: int | None; content_type: str | None
    redirected: bool = False; title: str | None = None; meta_description: str | None = None
    meta_robots: str | None = None; x_robots_tag: str | None = None; canonical: str | None = None
    html_lang: str | None = None; viewport: str | None = None; h1: list[str] = field(default_factory=list)
    h2_count: int = 0; static_jsonld_count: int = 0; static_jsonld_types: list[str] = field(default_factory=list)
    static_jsonld_parse_errors: int = 0; hreflang: list[dict[str, str]] = field(default_factory=list)
    image_count: int = 0; images_missing_alt_attribute: int = 0; internal_outlinks: list[str] = field(default_factory=list)
    inlinks: int = 0; discovered_from: list[str] = field(default_factory=list); error: str | None = None


def parse_page(requested: str, r: Fetch, base: str, include_query: bool) -> tuple[Page, list[str]]:
    final_norm = normalize(r.final, True) if r.final else None
    requested_norm = normalize(requested, True)
    page = Page(requested, r.final, r.status, r.content_type, redirected=bool(final_norm and final_norm != requested_norm),
                x_robots_tag=r.headers.get("x-robots-tag"), error=r.error)
    if not r.body or not r.content_type or not any(r.content_type.startswith(x) for x in HTML_TYPES): return page, []
    p = Parser()
    try: p.feed(decode(r.body, r.headers.get("content-type")))
    except Exception as e: page.error = f"HTML parse error: {e}"; return page, []
    current = r.final or requested
    page.title = p.title; page.meta_description = p.meta.get("description") or None; page.meta_robots = p.meta.get("robots") or None
    page.canonical = urljoin(current, p.canonical) if p.canonical else None; page.html_lang = p.lang; page.viewport = p.meta.get("viewport") or None
    page.h1 = p.h1; page.h2_count = p.h2_count; page.static_jsonld_count = p.jsonld_count
    page.static_jsonld_types = sorted(p.jsonld_types); page.static_jsonld_parse_errors = p.jsonld_errors
    page.hreflang = [{"lang": x["lang"], "href": urljoin(current, x["href"])} for x in p.hreflang]
    page.image_count = p.images; page.images_missing_alt_attribute = p.images_missing_alt
    seen: set[str] = set(); out: list[str] = []
    for href in p.links:
        u = normalize(urljoin(current, href), include_query)
        if u and same_origin(base, u) and u not in seen: seen.add(u); out.append(u)
    page.internal_outlinks = out
    return page, out


def robots(base: str, timeout: float) -> tuple[str, Fetch, RobotFileParser, list[str]]:
    p = urlparse(base); url = urlunparse((p.scheme, p.netloc, "/robots.txt", "", "", "")); r = fetch(url, timeout, 512_000)
    rp = RobotFileParser(); rp.set_url(url); maps: list[str] = []
    lines = decode(r.body, r.headers.get("content-type")).splitlines() if r.status == 200 and r.body else []
    rp.parse(lines)
    for line in lines:
        if line.lower().startswith("sitemap:"):
            x = line.split(":", 1)[1].strip()
            if x: maps.append(x)
    return url, r, rp, maps


def sitemap_pages(base: str, initial: list[str], timeout: float) -> tuple[list[str], list[dict[str, object]]]:
    p = urlparse(base); fallback = urlunparse((p.scheme, p.netloc, "/sitemap.xml", "", "", ""))
    q = deque(dict.fromkeys([*initial, fallback])); seen: set[str] = set(); pages: set[str] = set(); reports = []
    while q and len(seen) < MAX_SITEMAPS:
        u = normalize(q.popleft(), True)
        if not u or u in seen: continue
        seen.add(u); r = fetch(u, timeout, SITEMAP_BYTES); rep: dict[str, object] = {"url": u, "status": r.status, "kind": None, "entries": 0, "error": r.error}
        if r.status == 200 and r.body:
            try:
                root = ET.fromstring(decode(r.body, r.headers.get("content-type"))); kind = root.tag.rsplit("}", 1)[-1].lower(); rep["kind"] = kind
                locs = [x.text.strip() for x in root.findall(".//{*}loc") if x.text and x.text.strip()]; rep["entries"] = len(locs)
                if kind == "sitemapindex": q.extend(x for x in locs if same_origin(base, x))
                elif kind == "urlset":
                    for x in locs:
                        n = normalize(x)
                        if n and same_origin(base, n): pages.add(n)
            except ET.ParseError as e: rep["error"] = f"XML parse error: {e}"
        reports.append(rep)
    return sorted(pages), reports


def finding(items: list[dict[str, object]], severity: str, code: str, message: str, **extra: object) -> None:
    items.append({"severity": severity, "code": code, "message": message, **extra})


def findings_for(pages: list[Page], sitemap: set[str]) -> tuple[list[dict[str, object]], dict[str, list[list[str]]]]:
    out: list[dict[str, object]] = []; titles: defaultdict[str, list[str]] = defaultdict(list); descs: defaultdict[str, list[str]] = defaultdict(list)
    for p in pages:
        if p.title: titles[p.title].append(p.url)
        if p.meta_description: descs[p.meta_description].append(p.url)
        if p.status is None: finding(out, "high", "fetch-failed", "Page could not be fetched.", url=p.url, error=p.error); continue
        if p.status >= 500: finding(out, "critical", "server-error", f"HTTP {p.status}.", url=p.url)
        elif p.status >= 400: finding(out, "high", "client-error", f"HTTP {p.status}.", url=p.url)
        if p.redirected: finding(out, "medium", "redirected-url", "Requested URL redirected to a different final URL.", url=p.url, final_url=p.final_url)
        if p.status != 200 or not p.content_type or not any(p.content_type.startswith(x) for x in HTML_TYPES): continue
        robots_text = " ".join(x for x in (p.meta_robots, p.x_robots_tag) if x).lower()
        if p.url in sitemap and "noindex" in robots_text: finding(out, "high", "sitemap-noindex-conflict", "Sitemap URL is marked noindex.", url=p.url)
        if not p.title: finding(out, "medium", "missing-title", "No static <title> observed.", url=p.url)
        if not p.meta_description: finding(out, "low", "missing-meta-description", "No static meta description observed.", url=p.url)
        if not p.canonical: finding(out, "low", "missing-canonical", "No static canonical observed.", url=p.url)
        if not p.html_lang: finding(out, "medium", "missing-html-lang", "No html lang attribute observed.", url=p.url)
        if not p.viewport: finding(out, "medium", "missing-viewport", "No viewport meta tag observed.", url=p.url)
        if p.images_missing_alt_attribute: finding(out, "medium", "images-missing-alt-attribute", "Image elements omit the alt attribute.", url=p.url, count=p.images_missing_alt_attribute)
        if p.static_jsonld_parse_errors: finding(out, "medium", "invalid-static-jsonld", "Static JSON-LD block could not be parsed.", url=p.url, count=p.static_jsonld_parse_errors)
    duplicate_titles = [v for v in titles.values() if len(v) > 1]; duplicate_descs = [v for v in descs.values() if len(v) > 1]
    for urls in duplicate_titles: finding(out, "medium", "duplicate-title", "Same static title observed on multiple crawled URLs.", urls=urls)
    for urls in duplicate_descs: finding(out, "low", "duplicate-meta-description", "Same static meta description observed on multiple crawled URLs.", urls=urls)
    return out, {"titles": duplicate_titles, "meta_descriptions": duplicate_descs}


def main() -> int:
    ap = argparse.ArgumentParser(description="Static same-origin site audit fallback for SEO Chief (no JavaScript execution).")
    ap.add_argument("url"); ap.add_argument("--max-pages", type=int, default=50); ap.add_argument("--timeout", type=float, default=10)
    ap.add_argument("--delay", type=float, default=0.1); ap.add_argument("--include-query", action="store_true"); ap.add_argument("--output")
    ap.add_argument("--check-agent", action="append", default=[], help="Report robots.txt permission for this user-agent; repeatable. Verify agent names before use.")
    args = ap.parse_args(); base = normalize(args.url if "://" in args.url else "https://" + args.url)
    if not base: ap.error("url must be an http(s) URL")
    started = datetime.now(timezone.utc); robots_url, rr, rp, declared = robots(base, args.timeout); spages, sreports = sitemap_pages(base, declared, args.timeout)
    discovered: defaultdict[str, set[str]] = defaultdict(set); q = deque([base, *spages]); discovered[base].add("seed")
    for u in spages: discovered[u].add("sitemap")
    crawled: dict[str, Page] = {}; skipped: list[str] = []
    while q and len(crawled) < max(1, args.max_pages):
        u = normalize(q.popleft(), args.include_query)
        if not u or u in crawled or not same_origin(base, u): continue
        if not rp.can_fetch(UA, u): skipped.append(u); continue
        if args.delay: time.sleep(max(0, args.delay))
        r = fetch(u, args.timeout); page, links = parse_page(u, r, base, args.include_query); page.discovered_from = sorted(discovered[u]); crawled[u] = page
        for link in links:
            discovered[link].add(u)
            if link not in crawled: q.append(link)
    for src, p in crawled.items():
        for dst in p.internal_outlinks:
            if dst in crawled: crawled[dst].inlinks += 1
    pages = list(crawled.values()); f, dup = findings_for(pages, set(spages))
    sampled_orphans = [u for u in spages if u in crawled and crawled[u].inlinks == 0 and u != base]
    for u in sampled_orphans: finding(f, "medium", "sampled-orphan", "Sitemap URL has no inlink in the sampled crawl graph.", url=u)
    agent_checks = {a: rp.can_fetch(a, base) for a in args.check_agent}
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    report = {
        "meta": {"target": base, "started_at": started.isoformat(), "finished_at": datetime.now(timezone.utc).isoformat(), "user_agent": UA,
                 "mode": "static-html-fallback", "max_pages": args.max_pages, "include_query": args.include_query,
                 "limitations": ["JavaScript is not executed.", "Absence of JSON-LD here does not prove rendered schema is absent.",
                                 "robots.txt permission does not prove CDN/WAF/network access for a real crawler.",
                                 "Crawl-depth/orphan findings are sample-based when max-pages truncates discovery.",
                                 "This report is diagnostic evidence, not a ranking prediction."]},
        "robots": {"url": robots_url, "status": rr.status, "error": rr.error, "declared_sitemaps": declared, "checked_user_agents": agent_checks},
        "sitemaps": {"reports": sreports, "same_origin_page_urls": spages},
        "crawl": {"pages_fetched": len(pages), "queue_remaining": len(q), "skipped_by_robots": sorted(set(skipped)), "sampled_sitemap_pages_without_crawled_inlinks": sampled_orphans},
        "pages": [asdict(x) for x in pages], "duplicates": dup,
        "findings": sorted(f, key=lambda x: (severity_order.get(str(x["severity"]), 9), str(x["code"])))
    }
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output: Path(args.output).write_text(text + "\n", encoding="utf-8")
    else: print(text)
    counts = Counter(x["severity"] for x in f)
    print(f"audited {len(pages)} page(s); findings: " + ", ".join(f"{k}={counts[k]}" for k in ("critical","high","medium","low") if counts[k]), file=__import__('sys').stderr)
    return 0

if __name__ == "__main__": raise SystemExit(main())
