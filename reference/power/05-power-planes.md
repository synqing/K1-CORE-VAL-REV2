---
abstract: "Architecture C polygons for 175 and 160. L2/L5 stay one GND. 4 A LED on outer 1 oz. L3 post-route GND fill. Not implemented."
---

# Architecture C — both lengths, not built yet

Captain correction carried: LED return is **not** kept out of the shared GND plane. L2 and L5 stay unified. Contain the 4 A loop with forward copper, adjacent GND copper, short connector returns, dense stitching.

## Layer roles

| Layer | Role |
|---|---|
| L1 | signals + +5V_LED north + +5V_SYS HMI |
| L2 | solid GND |
| L3 | service/escape; **then** GND fill unused area (JLC <25 % coverage rule) |
| L4 | +3V3-dominant + VDD_SOC island under RT |
| L5 | solid GND |
| L6 | signals + +5V_LED south |

## L4 +3V3

Inset 16 mm from west (USB-C cavity) and 4 mm from other edges. Keep out south of S3 (antenna). Min neck 8 mm.

| Outline | 3V3 area est. | VDD_SOC island |
|---|---:|---|
| 175 | ~4722 mm² | RT 98.6–110.9 × 13.1–26.9 |
| 160 | ~4272 mm² | RT follows −15 mm |

Existing VDD_SOC: 10 vias, 0 tracks — the island is what those vias are waiting for.

## Outer 5 V LED

3 mm min neck, 1 oz. Via banks: 8 at shunt, 6 at each FPC. Length 175: ~92 mm north; 160: ~77 mm. Return: adjacent outer GND + stitch to L2/L5. **No GND split.**

## +5V_SYS HMI

0.220 A ×6 white. L1 pour along HMI. Does not earn L4.

Exact polygons: `planes_175.json`, `planes_160.json`.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Architecture C for both candidates; no GND split. |
