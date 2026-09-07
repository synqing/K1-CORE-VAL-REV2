---
abstract: "Hard operating rules for K1-CORE-VAL-REV2. EasyEDA Pro only. Donor FABLE-R3 is read-only. Gateway-only actuation. STOP if identity mismatches."
---

# AGENTS.md — K1-CORE-VAL-REV2

**Read first, every session:**
`docs/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md`

Cut-line is not placement. A folder is not a board. Canary needs `:9223`.
Do not start P1/P2 until Gate B0 has a live EasyEDA project and a canonical
`easyeda/K1-CORE-VAL-REV2.epro2`. Gateway `certified_mutating_verbs` is empty.

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
