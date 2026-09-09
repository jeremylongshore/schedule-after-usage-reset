#!/usr/bin/env python3
"""Fail-closed consistency checks for the data-only plugin repository."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = ROOT / "skills" / "schedule-after-usage-reset" / "SKILL.md"
PLUGIN_PATH = ROOT / ".claude-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".claude-plugin" / "marketplace.json"
EXPECTED_NAME = "schedule-after-usage-reset"
EXPECTED_REPOSITORY = (
    "https://github.com/jeremylongshore/schedule-after-usage-reset"
)


def frontmatter_scalar(document: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", document, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def main() -> int:
    failures: list[str] = []

    def require(condition: bool, message: str) -> None:
        if not condition:
            failures.append(message)

    skill = SKILL_PATH.read_text(encoding="utf-8")
    plugin = json.loads(PLUGIN_PATH.read_text(encoding="utf-8"))
    marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
    entry = marketplace["plugins"][0]

    require(plugin["name"] == EXPECTED_NAME, "plugin name drifted")
    require(entry["name"] == EXPECTED_NAME, "marketplace plugin name drifted")
    require(entry["source"] == "./", "marketplace source must remain local")
    require(plugin["version"] == entry["version"], "manifest versions differ")
    require(
        frontmatter_scalar(skill, "version") == plugin["version"],
        "skill and manifest versions differ",
    )
    require(
        frontmatter_scalar(skill, "name") == EXPECTED_NAME,
        "skill name drifted",
    )
    require(plugin["repository"] == EXPECTED_REPOSITORY, "repository URL drifted")
    require(plugin["homepage"] == EXPECTED_REPOSITORY, "homepage URL drifted")
    require(plugin["skills"] == "./skills/", "plugin skills path drifted")
    require(
        (SKILL_PATH.parent / "references" / "scheduling-options.md").is_file(),
        "scheduler reference is missing",
    )

    for forbidden in ("find-generic-password", "/api/oauth/usage", "accessToken"):
        require(forbidden not in skill, f"unsafe legacy pattern returned: {forbidden}")

    for required in (
        'allowed-tools: "CronCreate,CronList"',
        "## Safety boundary",
        "## Error handling",
        "CronList",
        "Never call undocumented Anthropic usage endpoints.",
    ):
        require(required in skill, f"required safety contract missing: {required}")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print("Repository consistency: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
