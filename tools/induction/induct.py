#!/usr/bin/env python3
"""K1-CORE-VAL-REV2 induction gate.

`injection_check.py` proves the CANON is present and tracked. This proves the
AGENT read it. The two are complementary and neither replaces the other.

    python3 tools/induction/induct.py --exam            # the questions
    python3 tools/induction/induct.py --submit ans.json # grade; issue a token on 100%
    python3 tools/induction/induct.py --status          # is this agent inducted?
    python3 tools/induction/induct.py --verify          # quiet; exit 0 inducted, 1 not
    python3 tools/induction/induct.py --self-test       # prove the gate goes RED

There is no answer key in this repository. Every answer is recoverable from the
canon and only from the canon: an agent that cannot answer has not read the
document the answer lives in. That is the design, not an obstacle.

A token dies when ANY of these change: AGENTS.md, CLAUDE.md, the session canons,
or the curriculum. Update a law and every prior induction lapses — which is the
only way "they confirmed they read it" can stay true over time.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
CURRICULUM = HERE / "curriculum.json"
TOKEN_DIR = ROOT / ".induction"
TTL_SECONDS = 24 * 3600

# Changing any of these invalidates every outstanding token.
CANON = [
    "AGENTS.md",
    "CLAUDE.md",
    "docs/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md",
    "docs/SESSION-CANON-2026-09-07-LIVE-EDITOR-INTEGRITY.md",
    "docs/TOOLCHAIN.md",
    "tools/induction/curriculum.json",
]


def norm(s: str) -> str:
    s = str(s).strip().lower()
    for ch in '`"\'.,;:!?()[]{}':
        s = s.replace(ch, "")
    s = s.replace("-", " ").replace("_", " ").replace("/", " ")
    return " ".join(s.split())


def h(s: str) -> str:
    return hashlib.sha256(norm(s).encode()).hexdigest()


def canon_fingerprint() -> str:
    """One hash over every document an inducted agent is certifying it has read."""
    d = hashlib.sha256()
    for rel in CANON:
        p = ROOT / rel
        d.update(rel.encode())
        d.update(p.read_bytes() if p.is_file() else b"<MISSING>")
    return d.hexdigest()


SESSION_OVERRIDE = None


def agent_id() -> str:
    """Identity a token is bound to.

    A session id is strongly preferred: it is handed to the agent by the guard,
    cannot be guessed, and dies with the session. Without one we fall back to the
    OS user, which on a single-user workstation means one induction unlocks that
    user for the TTL. That is weaker, and it is why the guard always supplies
    --session.
    """
    if SESSION_OVERRIDE:
        return "session:%s" % SESSION_OVERRIDE
    for var in ("CLAUDE_SESSION_ID", "EASYEDA_AGENT_ID", "AGENT_ID", "USER"):
        v = os.environ.get(var)
        if v:
            return "%s:%s" % (var.lower(), v)
    return "anonymous"


def token_path() -> Path:
    return TOKEN_DIR / (hashlib.sha256(agent_id().encode()).hexdigest()[:16] + ".json")


def load_curriculum() -> dict:
    if not CURRICULUM.is_file():
        sys.exit("FATAL: %s missing — induction cannot be granted." % CURRICULUM)
    return json.loads(CURRICULUM.read_text(encoding="utf-8"))


# ── commands ────────────────────────────────────────────────────────────────

def cmd_exam() -> int:
    c = load_curriculum()
    qs = c["questions"]
    print("=" * 78)
    print("K1-CORE-VAL-REV2 INDUCTION EXAM — %d questions, all must be correct" % len(qs))
    print("=" * 78)
    print()
    print("The answers are in the canon. They are nowhere else — this file stores")
    print("only hashes. Read the sources, then submit:")
    print()
    print('  python3 tools/induction/induct.py --submit answers.json')
    print()
    print('  answers.json  =  {"K1": "...", "K2": "...", ...}')
    print()
    print("Normalisation is forgiving: case, punctuation, and -/_ are ignored.")
    print("Wording is not — these are short, exact answers.")
    print()
    for mod, title in c["modules"].items():
        print("-" * 78)
        print("MODULE %s — %s" % (mod.upper(), title))
        print("-" * 78)
        for q in [x for x in qs if x["module"] == mod]:
            print()
            print("[%s] %s" % (q["id"], q["q"]))
            print("      source: %s" % q["source"])
        print()
    return 0


def grade(answers: dict, c: dict) -> tuple[list[str], list[str]]:
    ok, bad = [], []
    for q in c["questions"]:
        given = answers.get(q["id"])
        if given is None:
            bad.append("%s  (not answered)" % q["id"])
        elif h(given) == q["sha256"]:
            ok.append(q["id"])
        else:
            bad.append("%s  wrong — re-read %s" % (q["id"], q["source"]))
    return ok, bad


def cmd_submit(path: str) -> int:
    c = load_curriculum()
    try:
        answers = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        print("cannot read answers: %s" % e)
        return 2
    if not isinstance(answers, dict):
        print('answers must be a JSON object: {"K1": "...", ...}')
        return 2

    ok, bad = grade(answers, c)
    print("correct: %d / %d" % (len(ok), len(c["questions"])))
    if bad:
        print()
        print("NOT INDUCTED — every question must be correct.")
        for b in bad:
            print("  %s" % b)
        print()
        print("No token issued. Live surfaces remain blocked.")
        return 1

    TOKEN_DIR.mkdir(exist_ok=True)
    tok = {
        "agent": agent_id(),
        "issued": int(time.time()),
        "issued_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "expires": int(time.time()) + TTL_SECONDS,
        "canon_fingerprint": canon_fingerprint(),
        "curriculum_version": c.get("version"),
        "questions": len(c["questions"]),
    }
    token_path().write_text(json.dumps(tok, indent=2) + "\n", encoding="utf-8")
    print()
    print("INDUCTED.  token: %s" % token_path().relative_to(ROOT))
    print("  agent   %s" % tok["agent"])
    print("  expires %s (24 h) or sooner if any canon file changes" %
          time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(tok["expires"])))
    print()
    print("Live surfaces are now unlocked for this agent. The gate you just passed")
    print("does not make you careful — it only proves you were told. Run preflight")
    print("before the first read, and before every mutation batch.")
    return 0


def token_state() -> tuple[bool, str]:
    p = token_path()
    if not p.is_file():
        return False, "no induction token for %s" % agent_id()
    try:
        tok = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return False, "induction token unreadable (%s)" % e
    if tok.get("expires", 0) < time.time():
        return False, "induction token expired (%s)" % tok.get("issued_utc")
    if tok.get("canon_fingerprint") != canon_fingerprint():
        return False, ("the canon changed since induction — a law, a canon document "
                       "or the curriculum was edited. Re-induct.")
    return True, "inducted %s, expires %s" % (
        tok.get("issued_utc"),
        time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(tok.get("expires", 0))))


def cmd_status() -> int:
    ok, why = token_state()
    print(("INDUCTED     " if ok else "NOT INDUCTED ") + why)
    if not ok:
        print()
        print("  python3 tools/induction/induct.py --exam")
    return 0 if ok else 1


def cmd_verify() -> int:
    return 0 if token_state()[0] else 1


def cmd_self_test() -> int:
    """The gate must go RED on a wrong answer and on a changed canon."""
    c = load_curriculum()
    qs = c["questions"]
    fails = []

    # 1. a wrong answer must fail
    answers = {q["id"]: "definitely not the answer" for q in qs}
    ok, bad = grade(answers, c)
    if ok:
        fails.append("SELF-TEST: %d questions passed with junk answers" % len(ok))

    # 2. a missing answer must fail
    ok2, bad2 = grade({}, c)
    if ok2 or len(bad2) != len(qs):
        fails.append("SELF-TEST: empty submission did not fail every question")

    # 3. no plaintext answers may exist in the curriculum
    raw = CURRICULUM.read_text(encoding="utf-8")
    if '"answer"' in raw:
        fails.append("SELF-TEST: curriculum.json contains a plaintext answer key")

    # 4. the canon fingerprint must actually move when a canon file moves
    f1 = canon_fingerprint()
    target = ROOT / "CLAUDE.md"
    backup = target.read_bytes()
    try:
        target.write_bytes(backup + b"\n<!-- self-test -->\n")
        if canon_fingerprint() == f1:
            fails.append("SELF-TEST: canon fingerprint did not change when CLAUDE.md changed")
    finally:
        target.write_bytes(backup)
    if canon_fingerprint() != f1:
        fails.append("SELF-TEST: canon fingerprint did not restore")

    if fails:
        print("SELF-TEST FAIL")
        for f in fails:
            print("  - %s" % f)
        return 2
    print("SELF-TEST PASS")
    print("  junk answers rejected (%d questions)" % len(qs))
    print("  empty submission rejected")
    print("  no plaintext answer key in the repo")
    print("  canon fingerprint tracks canon edits")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--exam", action="store_true")
    g.add_argument("--submit", metavar="ANSWERS.json")
    g.add_argument("--status", action="store_true")
    g.add_argument("--verify", action="store_true")
    g.add_argument("--self-test", action="store_true")
    ap.add_argument("--session", metavar="ID",
                    help="bind/verify the token against this session id "
                         "(the guard supplies it; you cannot guess it)")
    a = ap.parse_args()
    global SESSION_OVERRIDE
    SESSION_OVERRIDE = a.session
    if a.exam:
        return cmd_exam()
    if a.submit:
        return cmd_submit(a.submit)
    if a.status:
        return cmd_status()
    if a.verify:
        return cmd_verify()
    return cmd_self_test()


if __name__ == "__main__":
    sys.exit(main())
