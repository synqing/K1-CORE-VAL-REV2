---
abstract: "K1-CORE-VAL-REV2 is the active EasyEDA-native successor to FABLE-R3. 160×40 mm. Read AGENTS.md and docs/DECISIONS.md first. KiCad is not source."
---

# K1-CORE-VAL-REV2

THIS IS **K1-CORE-VAL-REV2**.

- **EDA authority** = EasyEDA Pro.
- This is the active successor to `K1-Core-VAL-R1-FABLE-R3`.
- **Target outline** = **160 × 40 mm**.
- **160_PASS placement contract** = `reference/placement-160/`.
- KiCad files are **not** active source.
- Old R1/FABLE material is **reference-only**.
- Do not create ad-hoc active project versions (`…-final`, `…-FABLE-R1`, …).
- Do not mutate the donor.
- Read `AGENTS.md` and `docs/DECISIONS.md` first.

## What is real right now

| Item | State |
|---|---|
| Folder + contracts + hashed references | **YES** |
| Live EasyEDA project named `K1-CORE-VAL-REV2` | **NO** — Gate B0 blocked (gateway canary cannot reach EasyEDA; no CDP `:9223`) |
| Canonical `easyeda/K1-CORE-VAL-REV2.epro2` | **NOT YET** |
| 160 mm placement on a live board | **NOT STARTED** |
| Architecture C pours | **NOT STARTED** |

Copying the donor `.epro2` into `easyeda/` does **not** create REV2. EasyEDA itself must recognise a new project.

## Authority (after B0)

```text
Live EasyEDA Pro REV2
  > REV2 contracts (docs/)
  > REV2 machine-contracts (reference/placement-160, Polar, RILM)
  > R1/FABLE donor references
  > historical evaluations
```

## Do not

- Round-trip through KiCad.
- Rename FABLE-R3 in place.
- Encode history into the active project name.
- Implement from `reference/power/planes_160.json` until reconciled (REFERENCE_ONLY).
- Split L2/L5 GND to “contain” LED return.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Bootstrap README. |
