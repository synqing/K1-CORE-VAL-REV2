---
abstract: "Recommend Architecture C: L4 is a 3V3 plane plus a VDD_SOC patch. 4 A LED and long +5V_SYS run on outer 1 oz. Inner 0.5 oz is the wrong metal for 4 A. Today L4 is a GND pour — that is the defect to fix, not the role map."
---

# 15 — L4 power-plane study

Inner copper is 15.2 µm (0.5 oz). Outer is 35 µm (1 oz). Resistivity used: 1.72×10⁻⁸ Ω·m (CALC).

## Rails that exist (P0 net table + copper)

| Rail | Span x mm | Vias | Tracks | What it is |
|---|---:|---:|---:|---|
| +3V3 | 151 | 14 | 9 | logic, 91 components on explicit pads |
| +5V_SYS | 149 | 4 | 15 | includes **east HMI six WS2812E** |
| +5V_LED | 84 | 7 | 11 | post-shunt LED trunk |
| +5V_LED_N / _S | ~14–17 | 3 / 3 | 13 / 14 | branch after eFuse |
| VDD_SOC | 19 | 10 | **0** | RT core, via-only, no plane |
| GND | whole board | 90 | 3 | pours on every layer |

## Why 5 V should not “live on L4”

4 A × 92 mm on L4, 5 mm neck, 0.5 oz: R ≈ 18 mΩ, drop ≈ 72 mV, I²R ≈ 0.29 W in the neck (CALC). Same current on L1 1 oz, 3 mm: R ≈ 15 mΩ. Two outer layers in parallel beat a skinny inner plane and do not punch antipads through both GND planes for every LED via.

+5V_SYS to HMI at **0.220 A** theoretical full-white ×6 (WS2812E-1313 p.3, 12 mA/colour) over 150 mm needs a pour or ≥1 mm of 1 oz, not four vias. It does **not** earn an L4 5 V corridor.

3V3 at 2 A peak on a 30 mm-wide L4 plane, 100 mm: drop ≈ 8 mV. That **is** what L4 is for.

## Architectures

**A — 3V3 sea with embedded 5 V islands.** 5 V patches cut the 3V3 field under RT and under HMI. LED current still on 0.5 oz if you take the island seriously. Reject as the *primary* 5 V path.

**B — longitudinal 3V3 west / 5 V east.** Splits 3V3 under RT. The RT ball field wants 3V3 and VDD_SOC, not 5 V. Reject.

**C — 3V3-dominant L4, 5 V on L1/L6 (recommended).** L4: solid 3V3 from power entry through RT, with a **VDD_SOC** island under the BGA (already 10 vias, 0 tracks — they are waiting for a plane). Optional tiny +5V_SYS stitch near the hub only. LED 5 V: L1/L6 polygons ≥3 mm 1 oz, via banks at shunt, eFuses, FPCs. HMI +5V_SYS: L1 pour along the north or south of the HMI columns plus local 10–22 µF.

**D — 5 V on L4, 3V3 on outer.** Inverts the copper weights relative to current. Worse PI for RT. Reject.

## Plane capacitance

L4↔L5, 0.10 mm, Er 4.36, say 80 mm × 30 mm of 3V3: C ≈ εA/d ≈ 4.36×8.85e-12×0.080×0.030/0.00010 ≈ **920 pF** (CALC). Useful HF, not a substitute for bulk.

## HMI 5 V choice

Dedicated L4 corridor: possible, wastes 3V3, 0.5 oz. **Reject as primary.**  
L1/L6 heavy copper: **yes**.  
Combined: L1 pour + a few POFV to L4 only if a 3V3-free alley already exists. Not required if the L1 pour is ≥1 mm.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Four L4 options from live rail geography. |
