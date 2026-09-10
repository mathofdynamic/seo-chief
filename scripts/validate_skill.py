#!/usr/bin/env python3
"""Validate the seo-chief package contract and referenced resources."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = SCRIPT_DIR.parent
SKILL = ROOT / "SKILL.md"
SCENARIOS = ROOT / "tests" / "evaluation-scenarios.json"

REQUIRED_PATHS = {
    "SKILL.md",
    "README.md",
    "agents/openai.yaml",
    "references/aeo-geo.md",
    "references/agent-readiness.md",
    "references/deployment-adapters.md",
    "references/evidence-policy.md",
    "references/evaluation-scenarios.md",
    "references/execution-protocol.md",
    "references/keyword-content.md",
    "references/page-types.md",
    "references/response-validation.md",
    "references/rule-schema.md",
    "references/safety-validation.md",
    "references/site-audit.md",
    "references/source-registry.md",
    "rules/core-rules.json",
    "scripts/validate_response_matrix.py",
    "scripts/validate_rules.py",
    "scripts/validate_skill.py",
    "templates/change-manifest.json",
    "templates/consolidated-decision-table.md",
    "templates/production-response-matrix.json",
    "tests/evaluation-scenarios.json",
    "tests/test_response_matrix.py",
    "tests/test_skill_contract.py",
}

PATH_RE = re.compile(r"(?<![A-Za-z0-9])((?:agents|references|rules|scripts|templates|tests)/[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*)")
REQUIRED_MODES = {"autopilot", "audit-only", "plan-only", "no-deploy", "no-merge", "no-push"}
REQUIRED_SCENARIOS = {
    "one-call-autopilot",
    "nested-dirty-repositories",
    "vps-nginx-deployment",
    "markdown-404-negotiation",
    "cache-vary-behavior",
    "missing-business-facts",
    "brand-external-authority-blocker",
    "no-deploy-mode",
    "no-push-mode",
}


def error(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate_frontmatter(text: str, errors: list[str]) -> None:
    if not text.startswith("---\n"):
        error("SKILL.md must start with YAML frontmatter", errors)
        return
    end = text.find("\n---", 4)
    if end == -1:
        error("SKILL.md frontmatter is not closed", errors)
        return
    frontmatter = text[4:end].splitlines()
    values: dict[str, str] = {}
    for line in frontmatter:
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    for key in ("name", "description"):
        if not values.get(key):
            error(f"SKILL.md frontmatter missing {key}", errors)
    if values.get("name") != "seo-chief":
        error("SKILL.md frontmatter name must be seo-chief", errors)


def validate_references(errors: list[str]) -> None:
    markdown_files = sorted(ROOT.rglob("*.md"))
    for path in markdown_files:
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        discovered = set(PATH_RE.findall(text))
        source_label = path.relative_to(ROOT).as_posix()
        for relative in sorted(discovered):
            if not (ROOT / relative).is_file():
                error(f"{source_label} references missing file: {relative}", errors)


def validate_markers(text: str, errors: list[str]) -> None:
    lower = text.lower()
    for mode in REQUIRED_MODES:
        if mode.lower() not in lower:
            error(f"SKILL.md is missing execution mode marker: {mode}", errors)
    markers = (
        "does not stop after producing a plan",
        "17.",
        "safe-auto",
        "auto-with-validation",
        "requires-human-info",
        "requires-human-approval",
        "never fabricate",
        "never push git",
        "vps/nginx/pm2",
        "cloudflare pages/workers",
        "vercel",
        "netlify",
        "static hosting",
        "docker/reverse proxy",
        "github pages",
        "browser-only control-panel",
        "nginx -t",
        "text/markdown",
        "vary",
        "external authority",
        "machine-readable",
        "### changed",
        "### verified",
        "### blockers",
    )
    for marker in markers:
        if marker.lower() not in lower:
            error(f"SKILL.md is missing required operational marker: {marker}", errors)


def validate_scenarios(errors: list[str]) -> None:
    try:
        payload = json.loads(SCENARIOS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        error(f"cannot load evaluation scenarios: {exc}", errors)
        return
    scenarios = payload.get("scenarios") if isinstance(payload, dict) else None
    if not isinstance(scenarios, list) or not scenarios:
        error("evaluation-scenarios.json must contain a non-empty scenarios list", errors)
        return
    seen: set[str] = set()
    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            error(f"scenario {index} is not an object", errors)
            continue
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str) or not scenario_id:
            error(f"scenario {index} has no id", errors)
            continue
        if scenario_id in seen:
            error(f"duplicate scenario id: {scenario_id}", errors)
        seen.add(scenario_id)
        for field in ("prompt", "assertions", "required_markers"):
            if field not in scenario:
                error(f"scenario {scenario_id} missing {field}", errors)
        markers = scenario.get("required_markers", {})
        if not isinstance(markers, dict):
            error(f"scenario {scenario_id}.required_markers must be an object", errors)
            continue
        for relative, required in markers.items():
            path = ROOT / relative
            if not path.is_file():
                error(f"scenario {scenario_id} references missing file: {relative}", errors)
                continue
            content = path.read_text(encoding="utf-8").lower()
            for marker in required if isinstance(required, list) else []:
                if str(marker).lower() not in content:
                    error(f"scenario {scenario_id} marker missing from {relative}: {marker}", errors)
    missing = sorted(REQUIRED_SCENARIOS - seen)
    if missing:
        error(f"required regression scenarios missing: {', '.join(missing)}", errors)


def validate_rules(errors: list[str]) -> None:
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import validate_rules as rules_validator

        if rules_validator.main() != 0:
            error("rules validator failed", errors)
    except Exception as exc:  # pragma: no cover - defensive package-level reporting
        error(f"could not run rules validator: {exc}", errors)


def main() -> int:
    errors: list[str] = []
    for relative in sorted(REQUIRED_PATHS):
        if not (ROOT / relative).is_file():
            error(f"required package file missing: {relative}", errors)

    try:
        skill_text = SKILL.read_text(encoding="utf-8")
    except OSError as exc:
        error(f"cannot read SKILL.md: {exc}", errors)
        skill_text = ""

    if skill_text:
        validate_frontmatter(skill_text, errors)
        validate_references(errors)
        validate_markers(skill_text, errors)

    validate_scenarios(errors)
    validate_rules(errors)

    if errors:
        for item in errors:
            print(f"ERROR: {item}", file=sys.stderr)
        print(f"FAILED: {len(errors)} skill contract error(s)")
        return 1

    print(f"PASS: seo-chief package structure, references, modes, scenarios, and rule schema validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
