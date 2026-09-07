---
abstract: "What is live vs reference vs forbidden. After B0, live EasyEDA REV2 wins. Donor UUIDs are fingerprints, not REV2 identity."
---

# 01 — Authority map

## After Gate B0 (target)

| Rank | Surface |
|---|---|
| 1 | Live EasyEDA Pro project titled `K1-CORE-VAL-REV2` |
| 2 | `docs/` locked contracts + `docs/DECISIONS.md` |
| 3 | `reference/` artefacts marked `machine-contract` |
| 4 | REV2 gateway receipts under `evidence/` |
| 5 | R1/FABLE donor references |
| 6 | Historical evaluations |

## Before B0 (now)

| Rank | Surface |
|---|---|
| 1 | Donor export SHA `f9f33f0f7cbfc184ccb7b78e87e0840aae9ab5f74d672bbd09df8a3249dd9ebe` |
| 2 | `reference/placement-160/` (`160_PASS`) |
| 3 | This folder's contracts |
| 4 | Historical R1 eval (cut-line 160 REJECT is **withdrawn**) |

## Donor fingerprints (not REV2 identity)

| Field | Value |
|---|---|
| Title | `K1-Core-VAL-R1-FABLE-R3` |
| PCB UUID | `2aeefe7f7971144f` |
| Schematic UUID | `0a76d84abf763109` |
| Stack | `JLC06161H-3313E` |
| Components | 243 |
| Archive | `reference/donor-r1/ProPrj_K1-Core-VAL-R1-FABLE-R3_2026-09-07.epro2` |

Namespace live ids as `K1-CORE-VAL-REV2::<doc>::<primitive>`. Import may **preserve** donor primitive ids; that is not automatically a failure.

## Not imported as authority

Cut-line 165/160/155 REJECT · NFC-era docs · WS2813 · KiCad placement copies · stale zoning · screenshots · FABLE intermediate recoveries · corrupt `.epro2` · old routing as a plan · plane claims that contradict Architecture C.

Those may be cited from the R1 tree for provenance. They are not copied here.

## Tombstones (never open)

`96cb427938304a4b80f2e2ff0e16f2a4` · `e5d41aff545b47d4a2b33f5658f10d4c` · `f0e510c3af694db49d1c0b1634c28a30` and descendants listed in R1 `AGENTS.md`.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Authority map. |
