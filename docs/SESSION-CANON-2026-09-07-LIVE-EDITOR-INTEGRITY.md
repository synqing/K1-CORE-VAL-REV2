---
abstract: "Live-editor integrity canon. An EasyEDA editor can hold NOTHING while answering ok=true to every read, and the documented cure for a stale read (doc reload) SAVES FIRST — so running it in that state writes the empty document over the board. Run tools/easyeda/preflight.sh before the first read of a session and before every mutation batch."
---

# Live-editor integrity — read before touching a live board

Earned 2026-09-07 on `K1-Core-VAL-R1-FABLE-R3` (`INC-2026-09-07-EMPTY-EDITOR-001`).
Machine-readable form: `tools/easyeda/knowledge/` in the R1 tree — failure classes
`FC-EDA-*`, `FC-HOST-*`, `FC-GW-*`, invariants `INV-EDA-*`, `INV-HOST-*`,
recovery `REC-EMPTY-EDITOR-001`.

---

## The one that can destroy a board

**An EasyEDA editor can hold an empty document while every read succeeds.**

`pcb.components.list` returns `ok:true` and `"components": []`. No error field.
A board with 243 components is byte-identical, at the read layer, to no board at all.

Every liveness probe passes in this state:

| probe | what it says | is it true |
|---|---|---|
| `doc ls` | document is ★ active | yes, and irrelevant |
| `document.current` | correct project, document, tab | yes, and irrelevant |
| `doc open <uuid>` | `✓ opened pcb "PCB1"` | returns success against an unhydrated document |
| `--force-stale-read` | `{"components": [], "count": 0}` | identical output — it does **not** discriminate |

**And the documented cure is the thing that kills you.** `doc reload` is
save → close → reopen. The save is unconditional and happens *before* anything
verifies that the in-memory document is the real one. Run it against an unhydrated
editor and it writes the empty document over the server copy.

The state is self-arming: a `doc reload` whose *reopen* leg fails
(`document.open failed: connector did not respond`) leaves the editor unhydrated —
which is exactly the state in which the next `doc reload` destroys the board.
Observed duration before anyone noticed: **3 h 43 m**.

### Rules

1. **Never `doc reload` without a hydration probe passing immediately before it.**
2. **A zero or short component count is an ABORT. It is never evidence of an empty board.**
3. **If the editor is not hydrated after a reload, do not reload again.** Restart the
   application (`REC-EMPTY-EDITOR-001`).
4. **Do not quit the application gracefully to recover** — a quit can flush the same
   save. `SIGKILL` cannot flush a save, which is precisely why it is the safe choice here.

---

## The one that silently halves your tooling

**A plain launch strips the CDP flags.** `open -a EasyEDA-Pro`, the Dock, and
Spotlight all start EasyEDA Pro without `--remote-debugging-port=9223` and without
the anti-throttle flags.

The failure is *partial*, which is why it is dangerous:

- the `easyeda` CLI / daemon / connector path (port 60832) is **unaffected** and keeps answering
- every CDP driver under `tools/easyeda/drivers/cdp/` fails with `ECONNREFUSED 127.0.0.1:9223`
- so DSN export succeeds while the project-archive checkpoint silently does not

`easyeda-run download` in that state prints the literal `null`, **exits 0**, and writes
no file. Exit status is not a success signal for that command.

An agent that restarts the application to recover from any *other* fault creates this one.

**Always launch via** `node ~/SpectraSynq-EDA/EasyEDA-MCP/tools/easyeda_reconnect.mjs`
(no `--gentle`) **or the "EasyEDA (Bridge)" launcher.** The bridge watchdog names this
fault every 30 s in `~/Library/Logs/easyeda-bridge-watchdog.log` — read it first when
anything CDP-shaped misbehaves.

---

## The gate

```bash
tools/easyeda/preflight.sh <project-uuid> [doc-uuid] \
    [--min-components N] [--expect-pours N]
```

| exit | meaning |
|---|---|
| 0 | FIT — read and write |
| 10 | UNHYDRATED — editor holds no board; **do not `doc reload`** |
| 11 | NO-CDP — archive download and every CDP driver will fail silently |
| 12 | NO-WINDOW — no window, or more than one (two windows = two autosave writers) |
| 13 | WRONG-DOC — connector bound to a different document |
| 14 | POUR-DRIFT — a plane has appeared or vanished |
| 15 | DRC-FAIL — the DRC call did not answer; **a failed check is not a clean board** |

Run it before the first read of a session, before every mutation batch, and after
every application restart. Red fixtures for all seven outcomes:
`tools/easyeda/tests/efis/test_preflight_gate.py`.

---

## Measurement discipline

**Quote the TOTAL, never the group count.** `pcb.drc.check` reports a top-level count
that is the number of rule *groups*. The true total is the sum of each group's `count`.
On 2026-09-07 the headline said `4`; the board had **362**.

**Every metric is a fresh readback.** A number computed from a planned diff is not a
measurement and may not be stated as one. This produced a reported DRC of 280 against
an actual 362 — an 82-error gap in the connection class alone, invisible in the
transcript because every intermediate number *looked* like a measurement. The error
compounds silently across a batch, because each step is measured against the previous
step's estimate, and it poisons the record the next agent inherits.

**A checker's docstring is not coverage.** `check_plan.py` documented plan-vs-plan
clearance checking that was never written; four generated links shorted and the gate
passed all four. `check_stitch.py` modelled copper but not same-net *drill* spacing;
six vias landed at 0.000 mm separation. A gate's PASS is worse than no gate, because
it converts an unchecked action into an authorised one. Back every claimed check with
an executing test.

**A pour that vanishes invalidates every routing metric taken afterwards.** The `+3V3`
Inner3 flood has gone missing three times on FABLE-R3. Mechanism not established —
do not record a cause until one is measured. Capture the pour inventory before and
after every save; `--expect-pours` makes the gate enforce it.

---

## Router ceiling (FABLE-R3, but general to EasyEDA DSN)

EasyEDA's DSN export marks **every** wire and via `(type protect)`. Freerouting treats
protected copper as user-fixed and will neither rip it up nor shove it. Measured on
FABLE-R9: 1248 of 1248 objects protected, `(type route)` 0, `(type fix)` 0.

The router therefore plateaus after a few nets, and the plateau is easily misread as
router weakness or a resource limit. It is neither:

- `-mt` sizes the **optimisation** pool only; autorouting is single-threaded
  (measured 100.1 % CPU at `-mt 6`), so more cores cannot help
- disabling fanout (`FREEROUTING__ROUTER__FANOUT__ENABLED=false`) took one pass from
  27 minutes to 5 seconds — a settings win, not a throughput win

The real control is **selective unprotection**: strip `(type protect)` from the
authorised target nets only and leave every other object protected.

---

## Two operational rules that cost time to learn

- **Open the project before the document.** `project open --uuid <doc>` fails with
  `EDA_CALL_FAILED` while the application is on its start page. The project must be
  loaded first — that step is UI-only.
- **No blocking waits over the host bridge.** `sleep` inside a bridged command blocks
  the connection and presents to the Captain as a stall. Launch detached and poll with
  separate instant calls.
