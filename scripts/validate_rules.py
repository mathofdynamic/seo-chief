#!/usr/bin/env python3
"""Validate seo-chief machine-readable rules with no third-party dependencies."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules" / "core-rules.json"
SOURCE_REGISTRY = ROOT / "references" / "source-registry.md"

REQUIRED = {
    "id", "category", "scope", "applies_when", "check", "expected", "fix",
    "validation", "severity", "automation", "seo", "aeo", "geo",
    "evidence_level", "sources", "last_verified"
}
SCOPES = {"site", "page", "template", "page-type"}
SEVERITIES = {"blocker", "critical", "high", "medium", "low", "optional"}
AUTOMATION = {
    "safe-auto", "auto-with-validation", "requires-inference",
    "requires-human-info", "requires-human-approval", "never"
}
EVIDENCE = {"A", "B", "C", "D"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_ID_RE = re.compile(r"^- `([a-z0-9]+(?:-[a-z0-9]+)*)`\s+—", re.MULTILINE)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def parse_iso_date(value: object) -> date | None:
    """Return a real ISO calendar date, not merely a YYYY-MM-DD-shaped string."""
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def load_source_ids() -> tuple[set[str], list[str]]:
    """Load source-registry IDs and report duplicate identifiers."""
    text = SOURCE_REGISTRY.read_text(encoding="utf-8")
    ids = SOURCE_ID_RE.findall(text)
    seen: set[str] = set()
    duplicates: list[str] = []
    for source_id in ids:
        if source_id in seen:
            duplicates.append(source_id)
        seen.add(source_id)
    return seen, duplicates


def main() -> int:
    errors = 0

    if not SOURCE_REGISTRY.is_file():
        fail(f"missing source registry: {SOURCE_REGISTRY}")
        return 1

    source_ids, duplicate_source_ids = load_source_ids()
    if not source_ids:
        fail("source registry contains no source IDs")
        errors += 1
    for source_id in duplicate_source_ids:
        fail(f"duplicate source registry id: {source_id}")
        errors += 1

    payload = json.loads(RULES.read_text(encoding="utf-8"))

    if payload.get("schema_version") != "1.0.0":
        fail("unexpected schema_version")
        errors += 1

    snapshot = payload.get("research_snapshot")
    if parse_iso_date(snapshot) is None:
        fail("research_snapshot must be a real YYYY-MM-DD calendar date")
        errors += 1

    rules = payload.get("rules")
    if not isinstance(rules, list) or not rules:
        fail("rules must be a non-empty list")
        return 1

    seen: set[str] = set()

    for i, rule in enumerate(rules):
        prefix = f"rules[{i}]"
        if not isinstance(rule, dict):
            fail(f"{prefix} is not an object")
            errors += 1
            continue

        missing = REQUIRED - rule.keys()
        if missing:
            fail(f"{prefix} missing: {sorted(missing)}")
            errors += 1

        rid = rule.get("id")
        if not isinstance(rid, str) or not ID_RE.fullmatch(rid):
            fail(f"{prefix}.id must be kebab-case")
            errors += 1
        elif rid in seen:
            fail(f"duplicate rule id: {rid}")
            errors += 1
        else:
            seen.add(rid)

        if rule.get("scope") not in SCOPES:
            fail(f"{prefix}.scope invalid")
            errors += 1
        if rule.get("severity") not in SEVERITIES:
            fail(f"{prefix}.severity invalid")
            errors += 1
        if rule.get("automation") not in AUTOMATION:
            fail(f"{prefix}.automation invalid")
            errors += 1
        if rule.get("evidence_level") not in EVIDENCE:
            fail(f"{prefix}.evidence_level invalid")
            errors += 1

        for key in ("seo", "aeo", "geo"):
            if not isinstance(rule.get(key), bool):
                fail(f"{prefix}.{key} must be boolean")
                errors += 1

        sources = rule.get("sources")
        if not isinstance(sources, list):
            fail(f"{prefix}.sources must be a list")
            errors += 1
        else:
            for source_index, source_id in enumerate(sources):
                source_prefix = f"{prefix}.sources[{source_index}]"
                if not isinstance(source_id, str) or not source_id.strip():
                    fail(f"{source_prefix} must be a non-empty source-registry ID")
                    errors += 1
                elif source_id not in source_ids:
                    fail(f"{source_prefix} unknown source-registry ID: {source_id}")
                    errors += 1

        verified = rule.get("last_verified")
        if parse_iso_date(verified) is None:
            fail(f"{prefix}.last_verified must be a real YYYY-MM-DD calendar date")
            errors += 1

        for key in ("applies_when", "check", "expected", "fix", "validation"):
            if not isinstance(rule.get(key), str) or not rule[key].strip():
                fail(f"{prefix}.{key} must be non-empty")
                errors += 1

    if errors:
        print(f"FAILED: {errors} rule validation error(s)")
        return 1

    print(
        f"PASS: {len(rules)} rules validated; ids unique; enums, dates, "
        f"required fields, and {len(source_ids)} source-registry IDs valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
