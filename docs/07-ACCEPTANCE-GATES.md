---
abstract: "B0 donor-parity, P1 160 placement, P2 Architecture C. Each needs gateway receipt. P1/P2 must not share a transaction."
---

# 07 — Acceptance gates

## B0 — bootstrap / donor parity

PASS only when all are true:

- new EasyEDA project exists, title **exactly** `K1-CORE-VAL-REV2`
- canonical `easyeda/K1-CORE-VAL-REV2.epro2` exported + SHA in `bootstrap/source-integrity.json`
- project / PCB / schematic / page IDs recorded (namespaced)
- donor FABLE-R3 **untouched**
- 243 components; S3 / hub / RT / USB-C identities match donor
- schematic renders, PCB renders
- `JLC06161H-3313E` preserved
- no corruption signature, no blank Pages tree, no unexpected second PCB
- reference manifest complete, REV2 docs present

FAIL → **STOP**. Do not pair 160 placement with a broken import.

## P1 — 160 placement

Only after B0. Separate transaction from planes.

Live readback must prove: 160×40 · 174 MACRO at −15.000 mm X · 62 west-fixed · 7 reflows at contract XY · HMI pitch unchanged · six WS2812E · hub between S3 and RT · RT↔flash/xtal unchanged · east mounts on board · no new same-side collision · no WROOM underside · antenna south keepout intact · PWR-S3-001 ≥ 12.51 mm.

Red controls A/B must still go red.

## P2 — Architecture C

Only after P1. Remove donor L4 GND pour. Pour L4 +3V3 + VDD_SOC island. Keep L2/L5 unified GND. Outer 5 V LED corridors + via banks. L3 GND fill strategy after escape (do not leave inner copper-empty). Verify export / DRC / inner layers. **Stop before unrestricted routing.**

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | B0 / P1 / P2 gates. |
