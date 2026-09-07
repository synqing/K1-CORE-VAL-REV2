---
abstract: "JLC06161H-3313E frozen. Architecture C: L2/L5 unified GND, L4 3V3+VDD_SOC, 4 A LED on 1 oz outer. Polar USB 5.10/5.00 mil. planes_160.json is REFERENCE_ONLY until reconciled."
---

# 04 — Stackup and power contract

## Stack

`JLC06161H-3313E` (special ~1.6504 mm). Do not substitute non-E 3313.

Physical map: layerId 1=Top, 15=L2, 16=L3, 17=L4, 18=L5, 2=Bottom.

## Architecture C (locked topology, not yet poured)

| Layer | Role |
|---|---|
| L1 | signals + +5V_LED north + +5V_SYS HMI |
| L2 | **solid GND** — do not split |
| L3 | service/escape, then GND fill unused area (JLC: coverage < 25 % → pour or thickness/warpage) |
| L4 | **+3V3 sea** + **VDD_SOC island** under RT |
| L5 | **solid GND** — do not split |
| L6 | signals + +5V_LED south |

LED 4 A lives on **outer 1 oz**, not 0.5 oz L4. Contain the loop with forward copper, adjacent GND copper, short connector returns, dense stitching to L2/L5. **Wrong model:** “keep 4 A return out of the shared GND plane.”

HMI +5V_SYS is ~0.220 A ×6 white. It does not earn an L4 5 V corridor.

`reference/power/planes_160.json` is **REFERENCE_ONLY UNTIL RECONCILED**. Do not inject those polygons blindly. Rebuild from live 160 geometry after P1.

## USB impedance

Polar receipt: `reference/usb-impedance/jlc06161h-3313e-polar-2026-09-07.json`

Outer **W 5.10 mil / S 5.00 mil → 90.003 Ω** (DiffEdgeCoupledCoatedMicrostrip1B, H1 0.09940 mm, Er 4.1).

## RILM (TPS259474)

| Resistor | R | IILM |
|---|---|---|
| LED-N / LED-S | 1.65 kΩ | 2.028 A typ (DS table) |
| USB ingress | 1.10 kΩ | 3.03 A derived |
| bench DNP | 825 Ω | 4.04 A derived |

## POFV

Epoxy fill + copper cap is default on 6L. Plated barrel/cap still conducts heat; copper-paste is the *better* thermal option. Existing 0.20 / 0.35 mm stays. RT BGA VIP GO. 0201 VIP NO.

## Open power fact

`KH-FG1.0-H2.0-10PIN` drawing lists 50 V and contact resistance. **No A/pin.** Product-power blocker independent of board length.

Do not mix L4 pours into the P1 placement transaction.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Stack + Architecture C + Polar + RILM. |
