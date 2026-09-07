# K1-CORE-VAL-REV2

## You are not permitted to touch a live surface until you are inducted.

```bash
python3 tools/induction/induct.py --status     # am I inducted?
python3 tools/induction/induct.py --exam       # 33 questions
python3 tools/induction/induct.py --submit answers.json
```

A `PreToolUse` hook blocks every mutating EasyEDA command — `doc reload`, gateway
actuation, mutating verbs, Freerouting — until this agent holds a valid token.
Reads, git, tests, diagnostics and the induction itself are never blocked, so
nothing stops you getting inducted or diagnosing a fault.

The answers are not in this repository. They are in the canon and only in the
canon; the exam stores hashes. If you cannot answer, you have not read the file
the answer lives in. That is the design.

A token dies after 24 h, **and the moment any canon file changes.** Update a law
and every prior induction lapses.

Follow `AGENTS.md`. That file carries the NEVER AGAIN laws in-session.

Canons:

- `docs/TOOLCHAIN.md` — every tool that can reach EasyEDA, its faults, its recovery
- `docs/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md`
- `docs/SESSION-CANON-2026-09-07-LIVE-EDITOR-INTEGRITY.md`

Two facts that have each nearly cost a board, so that you have them before you
read anything else:

1. An EasyEDA editor can hold **nothing** while answering `ok=true` to every read.
   A zero component count is an ABORT, never an empty board.
2. `doc reload` **saves before it closes**. Run it against that editor and it
   writes the empty document over the board.

Load skill `k1-core-val-rev2` (tracked at `.agents/skills/k1-core-val-rev2/`).
Do not implement in K1-CORE-VAL-R1.

If this session opened the R1 tree, you did not get REV2 `AGENTS.md`. Stop and open REV2.
