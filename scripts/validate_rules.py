#!/usr/bin/env python3
"""Validate all seo-chief machine-readable rule packs with no dependencies."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULE_DIR = ROOT / "rules"
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
AUTO_CAPABLE = {"safe-auto", "auto-with-validation", "requires-inference"}
EVIDENCE = {"A", "B", "C", "D"}
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SOURCE_ID_RE = re.compile(r"^- \x60([a-z0-9]+(?:-[a-z0-9]+)*)\x60\s+—", re.MULTILINE)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def parse_iso_date(value: object) -> date | None:
    """Return a real ISO calendar date, not merely a shaped string."""
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def validate_not_future(value: object, label: str, today: date) -> int:
    parsed = parse_iso_date(value)
    if parsed is None:
        fail(f"{label} must be a real YYYY-MM-DD calendar date")
        return 1
    if parsed > today:
        fail(f"{label} cannot be in the future: {parsed.isoformat()}")
        return 1
    return 0


def load_source_ids() -> tuple[set[str], list[str]]:
    text = SOURCE_REGISTRY.read_text(encoding="utf-8")
    ids = SOURCE_ID_RE.findall(text)
    seen: set[str] = set()
    duplicates: list[str] = []
    for source_id in ids:
        if source_id in seen:
            duplicates.append(source_id)
        seen.add(source_id)
    return seen, duplicates


def validate_rule_pack(
    path: Path,
    payload: object,
    source_ids: set[str],
    global_rule_ids: set[str],
    today: date,
) -> tuple[int, int]:
    errors = 0
    label = path.relative_to(ROOT).as_posix()
    if not isinstance(payload, dict):
        fail(f"{label} must contain a JSON object")
        return 1, 0

    if payload.get("schema_version") != "1.0.0":
        fail(f"{label}: unexpected schema_version")
        errors += 1
    errors += validate_not_future(payload.get("research_snapshot"), f"{label}.research_snapshot", today)

    rules = payload.get("rules")
    if not isinstance(rules, list) or not rules:
        fail(f"{label}: rules must be a non-empty list")
        return errors + 1, 0

    local_rule_ids: set[str] = set()
    for index, rule in enumerate(rules):
        prefix = f"{label}:rules[{index}]"
        if not isinstance(rule, dict):
            fail(f"{prefix} is not an object")
            errors += 1
            continue

        missing = REQUIRED - rule.keys()
        if missing:
            fail(f"{prefix} missing: {sorted(missing)}")
            errors += 1

        rule_id = rule.get("id")
        if not isinstance(rule_id, str) or not ID_RE.fullmatch(rule_id):
            fail(f"{prefix}.id must be kebab-case")
            errors += 1
        elif rule_id in local_rule_ids or rule_id in global_rule_ids:
            fail(f"{prefix} duplicate rule id: {rule_id}")
            errors += 1
        else:
            local_rule_ids.add(rule_id)
            global_rule_ids.add(rule_id)

        if not isinstance(rule.get("category"), str) or not rule["category"].strip():
            fail(f"{prefix}.category must be a non-empty string")
            errors += 1
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

        evidence_level = rule.get("evidence_level")
        automation = rule.get("automation")
        if evidence_level == "C" and automation in AUTO_CAPABLE:
            fail(f"{prefix} Evidence C rules cannot be silently auto-applied")
            errors += 1
        if evidence_level == "D" and automation != "never":
            fail(f"{prefix} Evidence D rules must use automation never")
            errors += 1

        surface_flags: list[bool] = []
        for key in ("seo", "aeo", "geo"):
            value = rule.get(key)
            if not isinstance(value, bool):
                fail(f"{prefix}.{key} must be boolean")
                errors += 1
            else:
                surface_flags.append(value)
        if len(surface_flags) == 3 and not any(surface_flags):
            fail(f"{prefix} must apply to at least one of seo, aeo, or geo")
            errors += 1

        sources = rule.get("sources")
        if not isinstance(sources, list):
            fail(f"{prefix}.sources must be a list")
            errors += 1
        else:
            if evidence_level == "A" and not sources:
                fail(f"{prefix} Evidence A rules must cite a source-registry ID")
                errors += 1
            seen_sources: set[str] = set()
            for source_index, source_id in enumerate(sources):
                source_prefix = f"{prefix}.sources[{source_index}]"
                if not isinstance(source_id, str) or not source_id.strip():
                    fail(f"{source_prefix} must be a non-empty source-registry ID")
                    errors += 1
                    continue
                if source_id in seen_sources:
                    fail(f"{source_prefix} duplicates source ID: {source_id}")
                    errors += 1
                seen_sources.add(source_id)
                if source_id not in source_ids:
                    fail(f"{source_prefix} unknown source-registry ID: {source_id}")
                    errors += 1

        errors += validate_not_future(rule.get("last_verified"), f"{prefix}.last_verified", today)
        for key in ("applies_when", "check", "expected", "fix", "validation"):
            if not isinstance(rule.get(key), str) or not rule[key].strip():
                fail(f"{prefix}.{key} must be non-empty")
                errors += 1
        if "notes" in rule and (
            not isinstance(rule["notes"], str) or not rule["notes"].strip()
        ):
            fail(f"{prefix}.notes must be a non-empty string when present")
            errors += 1

    return errors, len(rules)


def main() -> int:
    errors = 0
    total_rules = 0
    today = date.today()

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

    rule_files = sorted(RULE_DIR.glob("*.json"))
    if not rule_files:
        fail(f"no rule packs found: {RULE_DIR}")
        return 1

    global_rule_ids: set[str] = set()
    for path in rule_files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(f"{path.relative_to(ROOT).as_posix()} cannot be parsed: {exc}")
            errors += 1
            continue
        pack_errors, count = validate_rule_pack(
            path, payload, source_ids, global_rule_ids, today
        )
        errors += pack_errors
        total_rules += count

    if errors:
        print(f"FAILED: {errors} rule validation error(s)")
        return 1

    print(
        f"PASS: {len(rule_files)} rule packs and {total_rules} rules validated; "
        f"ids unique; enums, dates, required fields, evidence gates, traceability, "
        f"and {len(source_ids)} source-registry IDs valid."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
