---
name: k1-core-val-rev2
description: >
  Use when the working tree is K1-CORE-VAL-REV2, or the task is K1 Core VAL
  hardware, EasyEDA K1 board, 160 mm placement, Architecture C, FABLE donor,
  REV2 bootstrap, Gate B0/P1/P2, WS2812E HMI, cut-line 160 reject, empty
  EasyEDA editor, doc reload, canary fetch failed, or open -a EasyEDA-Pro
  on this board. ALWAYS FIRST on REV2. Do not implement the board in K1-CORE-VAL-R1 (deprecated).
---

# K1-CORE-VAL-REV2

Live product. EasyEDA Pro is sole schematic+PCB authority. KiCad is not source.

This skill is tracked at `.agents/skills/k1-core-val-rev2/` so GitHub clones
see it. `.grok/` is gitignored — do not keep the only copy there.

## Boot (every turn)

1. Repo `AGENTS.md` is session-injected. The NEVER AGAIN block in that file is the gold.
2. Open `docs/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md` when doing placement.
3. Open `docs/SESSION-CANON-2026-09-07-LIVE-EDITOR-INTEGRITY.md` before any EasyEDA read/write.
4. If `easyeda/K1-CORE-VAL-REV2.epro2` is missing → **Gate B0**. Do not start P1/P2.
5. EasyEDA only through
   `/Users/spectrasynq/Workspace_Management/Software/K1-CORE-VAL-R1/tools/easyeda/easyeda-run`.
   Need CDP `:9223`. Never `open -a EasyEDA-Pro`.
6. Placement numbers from `reference/placement-160/placement_160.json` only.

## Hard stops

- Cut-line 160 reject / freeze 175 because HMI fell off
- `cp` donor to `easyeda/K1-CORE-VAL-REV2.epro2` and call it a new project
- `openProject` or import onto FABLE
- `setDocumentSource` / whole-document push
- Outline CLI (`outline-fit/set/clear`)
- Implement in K1-CORE-VAL-R1
- Treat FABLE-R1 uuid `bbd4b0af…` or PCB2 `730789ba…` as donor
- Split L2/L5 GND; shrink HMI pitch; swap TPS62913 → 62912; revive NFC; WS2813
- Zero live component count = empty editor (ABORT), not a blank board
- `doc reload` on an empty editor (it saves first and can wipe the board)
- `easyeda-run import-test`, `importProjectByProjectFile`, or File→Import of a large `.epro2` (stalls at 50/67/75%; ESC cancels; Existing Project injects `PCB1_1`)

## Then

`physics-before-geometry` · `easyeda-verification-contract` · `hardware-truth-gate`.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Created so REV2 is discoverable on every skill path. |
| 2026-09-07 | agent:grok | IMPORTER_STALL_KNOWN hard stop. |
| 2026-09-07 | agent:grok | Tracked under `.agents/skills/` (`.grok/` is gitignored). |
