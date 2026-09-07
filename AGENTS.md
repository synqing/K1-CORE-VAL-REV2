---
abstract: "Hard operating rules for K1-CORE-VAL-REV2. EasyEDA Pro only. Donor FABLE-R3 is read-only. Gateway-only actuation. STOP if identity mismatches."
---

# AGENTS.md — K1-CORE-VAL-REV2

**Read first, every session:**
`docs/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md`
`docs/SESSION-CANON-2026-09-07-LIVE-EDITOR-INTEGRITY.md`

Cut-line is not placement. A folder is not a board. Canary needs `:9223`.

**Before the first read of a session, before every mutation batch, and after every
application restart:** run `preflight.sh <project-uuid> <doc-uuid>` (in the R1 tree at
`tools/easyeda/preflight.sh`). An EasyEDA editor can hold NOTHING while answering
`ok=true` to every read, and `doc reload` SAVES FIRST — run it in that state and it
writes the empty document over the board. A zero component count is an ABORT, never
an empty board. Never launch EasyEDA with `open -a`: it strips
`--remote-debugging-port=9223`, after which every CDP driver fails silently while the
CLI keeps answering normally.
Do not start P1/P2 until Gate B0 has a live EasyEDA project and a canonical
`easyeda/K1-CORE-VAL-REV2.epro2`. Gateway `certified_mutating_verbs` is empty.
Donor is FABLE-R3 SHA `f9f33f0f…` PCB `2aeefe7f…` — not FABLE-R1 `bbd4b0af…`,
not leftover PCB `730789ba…`.

```text
PROJECT            = K1-CORE-VAL-REV2
EDA                = EasyEDA Pro (sole authority)
OUTLINE            = 160.00 × 40.00 mm
PLACEMENT_CONTRACT = reference/placement-160/
STACK              = JLC06161H-3313E
DONOR              = K1-Core-VAL-R1-FABLE-R3 (read-only)
KICAD              = NOT SOURCE
```

## Authority

```text
Live EasyEDA Pro REV2 > REV2 contracts > REV2 references > R1 donor.
```

After Gate B0, the live EasyEDA project named **exactly** `K1-CORE-VAL-REV2` is product authority. Donor artefacts explain *why*. They do not silently override REV2.

## Donor protection

Never modify:

```text
K1-Core-VAL-R1-FABLE-R3
```

Never open, restore, import into, write, save, use as a live target, or `openProject` onto the donor while working REV2. Canonical: `docs/agent/SESSION-CANON-2026-09-07-VIA-PERSIST-AND-GATEWAY.md` in the R1 tools repo (never `openProject` over FABLE).

Retired EasyEDA identities remain tombstones (R1 `AGENTS.md`). Do not open them.

## EasyEDA only

No KiCad round-trip. No `*.kicad_*` in this tree. No Prism / k3eda / cruncher outputs as source.

Actuation is **only** `easyeda-run` from the R1 tools checkout:

```text
/Users/spectrasynq/Workspace_Management/Software/K1-CORE-VAL-R1/tools/easyeda/easyeda-run
```

No CDP, MCP, Playwright, AppleScript or computer-use attached to EasyEDA outside it. No `.epro2`/`.epru` edits except `easyeda-run repair --emergency` on a **copy**. Never `set_document_source` / `setDocumentSource` / `force:true`.

If the gateway cannot do it: **STOP and report**. Do not bypass.

## NEVER AGAIN — EasyEDA project-file import (2026-09-07)

**Trigger (measured, do not re-run to confirm):**

```text
easyeda-run import-test <large.epro2> --via gui
easyeda-run import-test <large.epro2> --via api
easyeda-run import-test <large.epro2> --via api --into <uuid>
eda.sys_FileManager.importProjectByProjectFile(...)
File → Import → JLCEDA(Professional) of a ~3 MB .epro2
```

**What happens:** EasyEDA paints a progress overlay (50% / 67% / 75%) that does **not** advance. The operator cancels with **ESC**. CDP pause-storm makes it worse; it still stalls with pause set to `uncaught`. `--into` / Existing Project additionally injects `Board1_1` / `PCB1_1` / `schematic1_1` siblings.

**Mechanical gate:** `easyeda-run import-test` and the CDP import drivers now `REFUSED` / exit 3 (`IMPORTER_STALL_KNOWN`). Do not bypass. Do not write a second importer. Do not ask Captain to watch the bar.

Canon: `docs/SESSION-CANON-2026-09-07-IMPORTER-STALL.md`

## Document-level surgery

Stackup, design-rule and padstack work must use safe EasyEDA-native mechanisms. Do not rewrite whole document source because it is easier.

Outline verbs `outline-fit` / `outline-set` / `outline-clear` are **automation bans**. Uncertified mutating verbs are **DENIED** until Captain names a certified list.

## Connectivity

Blank or missing `PAD_NET` bodies do **not** prove disconnection. Use copper `netName`, schematic wire labels, and gateway readback. Never infer connectivity from canvas colour.

## Versioning

One active name: `K1-CORE-VAL-REV2`. Canonical export: `easyeda/K1-CORE-VAL-REV2.epro2`. History lives in git, gateway receipts, `evidence/checkpoints/`. Do not mint `REV2-final2`.

## Primitive IDs

Namespace every id:

```text
K1-CORE-VAL-REV2::<document-id>::<primitive-id>
```

Do not assume EasyEDA regenerates UUIDs on import.

## Evidence

Every material live-board phase must have:

```text
precondition
operation
readback
postcondition
gateway run ID / receipt
```

Cite `evidence/easyeda-gateway/<run>/run.json`. A flag is not evidence.

## Failure posture

If the active document does not match expected project/document identity:

```text
STOP / BLOCKED
```

not best-effort mutation.

## NEVER AGAIN (injected every session — do not skip the canon file)

1. Chopping the east edge is not a 160 study. Do not freeze 175 because HMI fell off.
2. 160 = MACRO −15.000 mm X + 7 reflows. Coordinates: `reference/placement-160/`. Do not shrink HMI pitch.
3. Antenna is SOUTH of the WROOM. Inductor gap 12.51 mm is I/O-side (PWR-S3-001). Do not move the buck.
4. L2/L5 stay unified GND. 4 A LED is outer 1 oz. L4 is +3V3 + VDD_SOC.
5. A folder is not a board. No `easyeda/K1-CORE-VAL-REV2.epro2` → you are at Gate B0, not P1.
6. `cp` donor `.epro2` is not a new EasyEDA project. `openProject` over FABLE is forbidden.
7. Canary `fetch failed` = no CDP `:9223`. Never `open -a EasyEDA-Pro` (strips the debug port).
8. `certified_mutating_verbs=[]`. Outline CLI banned. `setDocumentSource` banned. Gateway cannot → STOP.
9. Cut-line and naive-translate self-tests must still go RED.
10. Empty PAD_NET ≠ disconnected. TPS62913 is the die; TPS62912 in the footprint name is an alias.
11. Donor is FABLE-R3 `f9f33f0f…` / PCB `2aeefe7f…`. Not FABLE-R1 `bbd4b0af…`. Not leftover PCB `730789ba…`.
12. A 0402 overlapping the ADS7138 bbox is packing, not a 175 freeze. −10 mm is not 160_PASS.
13. Host never throws (`undefined`/`false`). Default Gerber drops inner copper. Via CREATE persists; modify does not.
14. `easyeda-run` receipts land in the **R1** `evidence/easyeda-gateway/` tree. Copy them here.
15. Zero component count from a live read is ABORT (empty editor), never “blank board.” `doc reload` saves first — do not reload an empty editor.
16. Namespace ids `K1-CORE-VAL-REV2::<doc>::<id>`.

Story and EasyEDA surface table: `docs/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md`.
Live-editor empty-document scar: `docs/SESSION-CANON-2026-09-07-LIVE-EDITOR-INTEGRITY.md`.

## What is injected vs what you must open

A file nobody is forced to load is theatre. On session start in **this** tree:

| Auto-loaded | Not auto-loaded |
|---|---|
| this `AGENTS.md` (including NEVER AGAIN 1–16) | the long canons under `docs/SESSION-CANON-*` |
| `CLAUDE.md` | skill **bodies** (catalog shows the name only) |
| `.cursor/rules/k1-core-val-rev2.mdc` (`alwaysApply`) | anything under `.grok/` (gitignored) |

Skill `k1-core-val-rev2` is tracked at `.agents/skills/k1-core-val-rev2/SKILL.md`. Load it on hardware work. Open a canon when the task hits that scar.

If this session is **not** this tree (you are in `K1-CORE-VAL-R1` or elsewhere): you did **not** get the 16 laws. Stop implementing. Open REV2, or you are flying blind.

Injection proof (must be able to go red): `python3 tools/injection_check.py` and `python3 tools/injection_check.py --self-test`.

## Frozen product facts

- WIDTH 40.0 mm. LED interface = FPC 10P. Dual VH retired.
- Six 4-pin **WS2812E-1313** HMI LEDs. Not WS2813.
- No NFC.
- Buck device = **TPS62913RPUR** (3 A). Footprint title may still say TPS62912. Do not “fix” the part.
- USB hub stays between S3 and RT.
- L2 and L5 = unified solid GND. Do not split grounds for LED return.
- 4 A LED on outer 1 oz. L4 = +3V3 + local VDD_SOC.
- Constraint **PWR-S3-001**: inductor body ↔ S3 body ≥ 12.51 mm.

## Anti-goals

Not a zone redesign, MCU rethink, KiCad migration, autorouter experiment, HMI redesign, USB topology redesign, NFC discussion, or component-swap exercise.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | REV2 operating constitution. |
| 2026-09-07 | agent:grok | NEVER AGAIN block inlined so session injection carries the gold, not a filename. |
| 2026-09-07 | agent:grok | What-is-injected table; skill tracked under `.agents/skills/`; injection_check.py. |
