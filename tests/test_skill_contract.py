from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_package_validator_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_skill.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_required_regression_scenarios_are_present(self) -> None:
        payload = json.loads((ROOT / "tests" / "evaluation-scenarios.json").read_text(encoding="utf-8"))
        ids = {scenario["id"] for scenario in payload["scenarios"]}
        required = {
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
        self.assertTrue(required.issubset(ids))

    def test_skill_has_the_report_contract(self) -> None:
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        for marker in ("### changed", "### verified", "### blockers", "17.", "no-deploy", "no-push"):
            self.assertIn(marker, skill)


if __name__ == "__main__":
    unittest.main()
