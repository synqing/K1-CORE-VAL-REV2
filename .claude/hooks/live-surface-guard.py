#!/usr/bin/env python3
"""PreToolUse gate: no live-surface actuation without proof of induction.

A law nobody enforces is a suggestion. AGENTS.md tells an agent what not to do;
this stops it. Hooks fire for subagents too and cannot be talked out of it.

Three verdicts:

  PROHIBITED   blocked for everyone, inducted or not. These have no legitimate
               use and each one has already cost us a board or a day.
  GATED        blocked unless this agent holds a valid induction token.
  ALLOW        everything else, including all reads, git, tests, and the
               induction process itself. The gate must never stop an agent from
               becoming inducted, or from diagnosing a fault.

Failure posture: if this script itself breaks, it ALLOWS and logs loudly. A
bricked project is a worse outcome than an uninducted read, and a guard that
can deadlock the tree would be removed within a day — which protects nothing.

Override: K1_INDUCTION_OVERRIDE="<reason>" permits a GATED command and appends
to .induction/override.log. It cannot lift a PROHIBITED one.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDUCT = ROOT / "tools" / "induction" / "induct.py"
LOGDIR = ROOT / ".induction"


def emit(decision: str, reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }}))


def allow() -> None:
    sys.exit(0)


def deny(reason: str) -> None:
    """Block. Any failure while composing the message must still block.

    A formatting bug in the explanation is not a reason to unlock a live board —
    that lesson cost us an allowed `doc reload` during this gate's own testing.
    """
    try:
        emit("deny", reason)
    except Exception:
        emit("deny", "BLOCKED by the K1-CORE-VAL-REV2 live-surface guard. "
                     "(The detailed reason could not be composed; run "
                     "`python3 tools/induction/induct.py --status`.)")
    sys.exit(2)


# ── what we look at ─────────────────────────────────────────────────────────

# Blocked for everyone. Each cost us something real.
PROHIBITED = [
    (r"\bopen\s+-a\s+[\"']?EasyEDA-Pro",
     "`open -a EasyEDA-Pro` strips --remote-debugging-port=9223 and the anti-throttle "
     "flags. Every CDP driver then fails with ECONNREFUSED while the CLI keeps "
     "answering normally, so the session looks healthy and silently cannot take a "
     "checkpoint.\n"
     "USE: node ~/SpectraSynq-EDA/EasyEDA-MCP/tools/easyeda_reconnect.mjs   (no --gentle)"),

    (r"easyeda-run\s+.*\bimport-test\b",
     "`easyeda-run import-test` is REFUSED (exit 3, IMPORTER_STALL_KNOWN). It paints a "
     "progress overlay at 50/67/75 percent that never advances, and --into injects "
     "Board1_1 / PCB1_1 / schematic1_1 siblings.\n"
     "Do not bypass it. Do not write a second importer. Do not ask the Captain to watch "
     "the bar. Canon: docs/SESSION-CANON-2026-09-07-IMPORTER-STALL.md"),

    (r"set[_-]?[Dd]ocument[_-]?[Ss]ource",
     "setDocumentSource / set_document_source is permanently banned in REV2 "
     "(AGENTS.md — EasyEDA only). Whole-document source pushes are not a shortcut for "
     "stackup, design-rule or padstack work; use the EasyEDA-native mechanism."),

    (r"--force[= ]true|\bforce:\s*true",
     "force:true is permanently banned in REV2 (AGENTS.md — EasyEDA only)."),
]

# Blocked unless inducted. These actuate a live surface.
GATED = [
    (r"easyeda-run\s+.*\b(mutate|txn|agent|repair|apply)\b",
     "easyeda-run actuation onto a live EasyEDA surface"),

    (r"\beasyeda\s+doc\s+reload\b",
     "`doc reload` — it SAVES before it closes. Against an unhydrated editor it writes "
     "the empty document over the board"),

    (r"\beasyeda\s+call\s+(pcb|sch|schematic)\.[a-z_.]*"
     r"(create|delete|modify|update|set|move|rip|clear|place|import)",
     "a mutating gateway verb"),

    (r"freerouting|\bfreeroute\b",
     "an external router run against board copper"),
]

# Never gated, whatever else matches: the agent must always be able to become
# inducted, to diagnose, and to read.
ALWAYS_ALLOW = [
    r"induct\.py",
    r"injection_check\.py",
    r"preflight\.sh",
    r"easyeda-run\s+(download|canary|knowledge|preflight|outline-oracle)",
    r"easyeda\s+(daemon\s+health|doc\s+ls|project\s+info|actions)",
    r"\bgit\b",
    r"python3?\s+-m\s+unittest",
]


def _sess_args(session: str | None) -> list:
    return ["--session", session] if session else []


def inducted(session: str | None) -> bool:
    try:
        return subprocess.run(
            [sys.executable, str(INDUCT), "--verify"] + _sess_args(session),
            cwd=str(ROOT), capture_output=True, timeout=25,
        ).returncode == 0
    except Exception:
        return False


def induction_reason(what: str, session: str | None) -> str:
    try:
        st = subprocess.run(
            [sys.executable, str(INDUCT), "--status"] + _sess_args(session),
            cwd=str(ROOT), capture_output=True, text=True, timeout=25,
        ).stdout.strip()
    except Exception:
        st = "(induction status unavailable)"
    sess = (" --session %s" % session) if session else ""
    return (
        "BLOCKED — not inducted. This command actuates %s.\n\n"
        "%s\n\n"
        "K1-CORE-VAL-REV2 does not allow an agent to touch a live PCB, schematic or "
        "gateway surface until it has proved it read the canon. This is not "
        "ceremony: an EasyEDA editor can hold NOTHING while answering ok=true to "
        "every read, and `doc reload` saves before it closes — an uninducted agent "
        "meeting that state destroys the board.\n\n"
        "To proceed:\n"
        "  1. python3 tools/induction/induct.py --exam\n"
        "  2. read the sources it cites — the answers exist only in the canon\n"
        "  3. python3 tools/induction/induct.py --submit answers.json%s\n\n"
        "33 questions, all must be correct. It costs one pass through the canon, "
        "which you were going to do anyway.\n\n"
        "If this is genuinely an emergency, K1_INDUCTION_OVERRIDE=\"<reason>\" permits "
        "one gated command and is written to .induction/override.log for the Captain "
        "to read." % (what, st, sess)
    )


def safe_induction_reason(what: str, session: str | None) -> str:
    try:
        return induction_reason(what, session)
    except Exception:
        return ("BLOCKED — not inducted. This command actuates %s.\n"
                "Run: python3 tools/induction/induct.py --exam" % what)


def log_override(cmd: str, reason: str) -> None:
    try:
        LOGDIR.mkdir(exist_ok=True)
        with (LOGDIR / "override.log").open("a", encoding="utf-8") as fh:
            fh.write("%s\t%s\t%s\n" % (
                time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), reason, cmd))
    except Exception:
        pass


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        allow()  # fail open, cannot parse

    tool = payload.get("tool_name", "")
    session = payload.get("session_id")
    ti = payload.get("tool_input") or {}
    # Bash carries `command`; MCP tools carry arbitrary args. Scan everything.
    blob = ti.get("command") if tool == "Bash" else json.dumps(ti)
    if not blob:
        allow()

    for pat in ALWAYS_ALLOW:
        if re.search(pat, blob, re.I):
            allow()

    for pat, why in PROHIBITED:
        if re.search(pat, blob, re.I):
            deny("PROHIBITED in K1-CORE-VAL-REV2 — this is blocked for every agent, "
                 "inducted or not.\n\n" + why)

    for pat, what in GATED:
        if re.search(pat, blob, re.I):
            if inducted(session):
                allow()
            ov = os.environ.get("K1_INDUCTION_OVERRIDE")
            if ov:
                log_override(blob[:400], ov)
                allow()
            deny(safe_induction_reason(what, session))

    allow()


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as e:  # never deadlock the tree
        try:
            LOGDIR.mkdir(exist_ok=True)
            (LOGDIR / "guard-error.log").open("a", encoding="utf-8").write(
                "%s\t%r\n" % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), e))
        except Exception:
            pass
        sys.exit(0)
