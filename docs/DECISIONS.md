---
abstract: "REV2 locked decisions: new generation boundary, 160_PASS, Architecture C, no GND split, EasyEDA-only, donor read-only, Polar USB geometry."
---

# DECISIONS

| ID | Decision | Status |
|---|---|---|
| REV2-D-001 | `K1-CORE-VAL-REV2` is a new generation boundary, not FABLE-R4 | LOCKED |
| REV2-D-002 | EasyEDA Pro is sole schematic+PCB authority. KiCad is not in this project | LOCKED |
| REV2-D-003 | Donor `K1-Core-VAL-R1-FABLE-R3` is read-only | LOCKED |
| REV2-D-004 | Outline **160.00 × 40.00 mm** from closure `160_PASS` | LOCKED |
| REV2-D-005 | Placement = MACRO −15 mm + 7 reflows; not a cut-line | LOCKED |
| REV2-D-006 | USB hub remains between S3 and RT | LOCKED |
| REV2-D-007 | Architecture C: L4 3V3 + VDD_SOC; 4 A LED on outer 1 oz | LOCKED |
| REV2-D-008 | L2/L5 remain unified GND | LOCKED |
| REV2-D-009 | Stack JLC06161H-3313E | LOCKED |
| REV2-D-010 | USB outer 5.10/5.00 mil (Polar 90.003 Ω) | LOCKED |
| REV2-D-011 | Six 4-pin WS2812E-1313; no NFC; no WS2813 | LOCKED |
| REV2-D-012 | PWR-S3-001 inductor↔S3 ≥ 12.51 mm | LOCKED |
| REV2-D-013 | Active name does not encode history | LOCKED |
| REV2-D-014 | Stop this bootstrap before unrestricted routing | LOCKED |

Cut-line 160 REJECT in R1 `13-placement-comparison.md` is **superseded** and was not imported as authority.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Initial REV2 decision register. |
