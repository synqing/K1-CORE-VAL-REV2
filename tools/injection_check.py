#!/usr/bin/env python3
"""Prove session-start injection for K1-CORE-VAL-REV2 can go RED.

A canon file nobody is forced to load is theatre. This gate checks the
surfaces that actually land in a future agent's first turn:

  AGENTS.md / CLAUDE.md          Grok, Claude Code, Codex
  .cursor/rules/*.mdc            Cursor (alwaysApply)
  .agents/skills/.../SKILL.md    skill catalog (must be a real git-tracked file)
  .pcb-lane / .schematic-lane    pcb-design-router Hop 0

Exit 0 only when every surface is present, content-correct, and git-tracked.
`--self-test` plants a missing law and requires this script to FAIL.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".agents/skills/k1-core-val-rev2/SKILL.md"
CURSOR = ROOT / ".cursor/rules/k1-core-val-rev2.mdc"
REQUIRED_TRACKED = [
    "AGENTS.md",
    "CLAUDE.md",
    ".cursor/rules/k1-core-val-rev2.mdc",
    ".agents/skills/k1-core-val-rev2/SKILL.md",
    ".pcb-lane",
    ".schematic-lane",
    "docs/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md",
    "docs/SESSION-CANON-2026-09-07-LIVE-EDITOR-INTEGRITY.md",
    "tools/injection_check.py",
]


def git_tracked(root: Path) -> set[str]:
    out = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=root, text=True
    )
    return {p for p in out.split("\0") if p}


def check(root: Path, tracked: set[str] | None = None) -> list[str]:
    fails: list[str] = []
    tracked = git_tracked(root) if tracked is None else tracked

    agents_path = root / "AGENTS.md"
    if not agents_path.is_file():
        fails.append("AGENTS.md missing")
        agents = ""
    else:
        agents = agents_path.read_text(encoding="utf-8")

    if "NEVER AGAIN" not in agents:
        fails.append("AGENTS.md has no NEVER AGAIN block (the injected gold)")
    for i in range(1, 17):
        if not re.search(rf"^{i}\. ", agents, re.M):
            fails.append(f"AGENTS.md missing NEVER AGAIN law {i}")
    if "What is injected" not in agents:
        fails.append("AGENTS.md missing 'What is injected' (map vs opt-in)")

    if not (root / "CLAUDE.md").is_file():
        fails.append("CLAUDE.md missing")

    if not CURSOR.is_file():
        fails.append(f"{CURSOR.relative_to(root)} missing")
    else:
        mdc = CURSOR.read_text(encoding="utf-8")
        if "alwaysApply: true" not in mdc:
            fails.append("cursor rule is not alwaysApply: true")

    if not SKILL.is_file():
        fails.append(f"{SKILL.relative_to(root)} missing")
    elif SKILL.is_symlink() or SKILL.parent.is_symlink():
        fails.append(
            "skill is a symlink (GitHub clones get a dangling pointer; "
            ".grok/ is gitignored)"
        )
    else:
        body = SKILL.read_text(encoding="utf-8")
        if "name: k1-core-val-rev2" not in body:
            fails.append("skill frontmatter name mismatch")
        if "Do not implement the board in K1-CORE-VAL-R1" not in body:
            fails.append("skill description missing R1 stop")

    for lane_name, expect in ((".pcb-lane", "easyeda"), (".schematic-lane", "easyeda")):
        p = root / lane_name
        if not p.is_file():
            fails.append(f"{lane_name} missing")
            continue
        first = next(
            (ln.strip() for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip() and not ln.strip().startswith("#")),
            "",
        )
        if first != expect:
            fails.append(f"{lane_name} first word is {first!r}, want {expect!r}")

    for rel in REQUIRED_TRACKED:
        if rel not in tracked:
            fails.append(f"not git-tracked (GitHub clones will not see it): {rel}")

    grok_skill = root / ".grok/skills/k1-core-val-rev2"
    if grok_skill.exists() and not grok_skill.is_symlink():
        # Local grok path may exist; it must not be the only copy.
        if grok_skill.resolve() != SKILL.parent.resolve():
            fails.append(
                ".grok/skills/k1-core-val-rev2 is a real dir; it is gitignored. "
                "Canonical tracked skill must live under .agents/skills/"
            )

    return fails


def self_test() -> int:
    """Plant a missing law. The checker MUST go red."""
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    stripped = re.sub(r"^15\. .*\n", "", agents, count=1, flags=re.M)
    if stripped == agents:
        print("SELF-TEST FAIL: could not strip law 15 from AGENTS.md fixture")
        return 2
    tmp = ROOT / ".injection-check-tmp-AGENTS.md"
    orig = ROOT / "AGENTS.md"
    backup = orig.read_bytes()
    try:
        orig.write_text(stripped, encoding="utf-8")
        fails = check(ROOT)
    finally:
        orig.write_bytes(backup)
        if tmp.exists():
            tmp.unlink()
    if not any("law 15" in f for f in fails):
        print("SELF-TEST FAIL: checker stayed green after deleting law 15")
        print("fails:", fails)
        return 2
    print("SELF-TEST PASS: deleting law 15 went RED")
    return 0


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    fails = check(ROOT)
    if fails:
        print("INJECTION CHECK FAIL")
        for f in fails:
            print(f"  - {f}")
        return 1
    print("INJECTION CHECK PASS")
    print("  AGENTS.md NEVER AGAIN 1-16")
    print("  CLAUDE.md")
    print("  Cursor alwaysApply")
    print("  tracked .agents/skills/k1-core-val-rev2/SKILL.md (real file)")
    print("  .pcb-lane / .schematic-lane = easyeda")
    print("  both session canons git-tracked")
    return 0


if __name__ == "__main__":
    sys.exit(main())
