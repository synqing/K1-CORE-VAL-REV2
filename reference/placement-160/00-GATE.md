---
abstract: "READ-ONLY closure gate. 160_PASS. Super-macro −15 mm + 7-part west reflow fits 160×40 without cutting HMI. EasyEDA not mutated. Planes not implemented."
status: CLOSURE
authority: Captain 2026-09-07 placement-and-power closure brief
---

# GATE: `160_PASS`

Lane: **VERIFICATION**. EasyEDA was not opened, not written, not imported.

```
160_PASS
```

A genuine 160 × 40 mm placement exists. It is **not** the previous cut-line. The east super-macro (S3 + hub + RT + LED + audio + complete HMI + east mounts) translates **−15 mm**. Seven west-boundary parts are reflowed. HMI pitch is unchanged. USB hub stays between the two MCUs.

## What this is not

- Not an EasyEDA mutation.
- Not a plane implementation.
- Not a 175 mm freeze.
- Not a claim that 160 is routing-ready (L4 is still a GND pour on the live board).

## Captain numbers, re-derived

| Fact | mm | Tag |
|---|---:|---|
| S3-MCU1 body west edge | 57.780 | MEASURED |
| SVC-ADC1 body east edge | 47.700 | MEASURED |
| U34 eastmost | 172.360 | MEASURED |
| 10 mm shift S3 west vs ADC east | 0.080 | CALC |
| 15 mm shift eastmost | 157.360 | CALC |
| 160 mm east inset | 2.640 | CALC (same as 175: 175−172.36) |

## Method controls (instrument went RED)

| Case | Result |
|---|---|
| Chop outline to 160, leave parts | HMI/RGB/east mounts **off board** (RED) |
| Translate super-macro −15 mm, **no** reflow | ADS7138 overlaps incoming WROOM (RED) |
| −15 mm + 7 reflows | 0 same-side overlaps, 0 WROOM underside parts, 0 off-board (GREEN) |

10 / 10 self-tests pass. Battery: `closure/selftest.json`.

## What moved

| Class | Count | Rule |
|---|---:|---|
| MACRO | 174 | −15 mm, relative geometry frozen |
| WEST_FIXED | 62 | USB-C, buck island, shunt/INA, west mounts, west USB-CC |
| REFLOW | 7 | listed below |

### Reflow (new centres, mm)

| Part | Side | x | y | Why |
|---|---|---:|---:|---|
| SVC-ADC1 | bottom | 54.00 | 33.50 | Out of S3 body; north of S3; bottom so L1 USB wrap stays empty |
| C-SVC-DEC1 | bottom | 54.00 | 30.70 | Decap south of ADC |
| R-PWR-I2C1 | bottom | 51.50 | 33.50 | I²C west of ADC |
| R-PWR-I2C2 | bottom | 56.40 | 33.50 | I²C east of ADC |
| R-LEDN-PRS1 | bottom | 51.50 | 30.20 | Was under incoming WROOM |
| R-S3-IRQ1 | top | 44.80 | 27.20 | Blind −15 mm lands on the buck |
| SVC-TEMP1 | top | 40.97 | 29.07 | +0.80 mm Y, clears S3 west-north corner |

Buck switch-node / inductor **did not move**. Antenna remains **south** of the WROOM. East holes are **edge-relative** (no enclosure freeze found).

## Critical distances

| Pair | 175 | 160 | Δ |
|---|---:|---:|---:|
| USB-C → hub | 72.534 | 57.545 | **−14.989** |
| hub → S3 | 15.706 | 15.706 | 0 |
| hub → RT | 22.390 | 22.390 | 0 |
| S3 → RT | 36.889 | 36.889 | 0 |
| RT → flash | 10.882 | 10.882 | 0 |
| RT → crystal | 12.528 | 12.528 | 0 |
| shunt → LED-N | 91.956 | 76.957 | **−14.999** |
| audio / HMI | 17.869 | 17.869 | 0 |
| encoder C2C | 11.205 | 11.205 | 0 |
| HMI column | 11.300 | 11.300 | 0 |
| RGB column | 11.220 | 11.220 | 0 |
| inductor → S3 (C2C) | 39.444 | 24.465 | −14.979 |
| inductor body → S3 body | 27.51 | **12.51** | −15.00 |

Six WS2812E-1313, 4 pads, preserved.

## Residuals — not kills

1. **Inductor/S3 I/O-side 12.51 mm.** Antenna keepout is south (module ymin 7.045). This is west of the I/O wall, not in the RF FOV. Tightening, not an overlap, not an antenna violation.
2. **USB north wrap.** R-S3-IRQ1 sits 1.2 mm north of S3 at x≈44–45. The usable L1 alley is **x=49.5–61.8 (12.3 mm) × y=25.7–40 (14 mm)**. ADC cluster is on the **bottom**.
3. **KH-FG1.0-H2.0-10PIN current.** Official drawing does **not** state A/pin. Product-power blocker **independent of length**.

Min same-side body gap on 160 = 0.279 mm (`HMI-ENC2`–`R-HMI-ENCS2`) — **identical on 175**. Not a shrink artefact.

## Power architecture (still not implemented)

Architecture C stands for **both** lengths:

- L2 / L5 = unified solid GND. Do **not** split to “contain” LED return.
- L3 = escape, then GND fill (JLC: coverage < 25 % → pour empty areas or thickness/warpage suffer).
- L4 = +3V3 sea + local VDD_SOC island under RT.
- 4 A LED on outer 1 oz with adjacent GND copper and via banks.
- HMI +5V_SYS on outer copper (0.220 A).

Polygons: `planes_160.json`, `planes_175.json`.

## POFV (wording correction carried)

Default JLC POFV is epoxy fill + copper cap. The plated barrel/cap still conducts heat; copper-paste fill is the *better* thermal option, not the only live one. Geometry 0.20 / 0.35 mm stays on the table. 0201 VIP still NO.

## Data quality closed in this lane

1. `04-routing-census.csv` now LINE **265** + ARC **230** + VIA **218** (714 lines including header).
2. Buck: live identity `TPS62913RPUR` (3 A); footprint name still `…TPS62912RPUR` (2 A). **Alias, do not “fix” the part.**
3. RILM bound: LED-N/S 1.65 kΩ → **2.028 A typ** (DS table); USB 1.10 kΩ → **3.03 A**; bench DNP 825 Ω → **4.04 A**.
4. KH-FG drawing read; **no A/pin**.
5. Six WS2812E-1313 preserved.
6. `$1N3583` / `$1N3585` rename belongs in the **implementation** plan, not this lane.
7. Polar receipt attached: outer **5.10 / 5.00 mil → 90.003 Ω** on JLC06161H-3313E.

## Ship path (this gate does not ship copper)

1. **Already true:** coordinate candidate + self-test on disk; live board still 175 mm with L4 = GND.
2. **Remaining:** Captain accepts `160_PASS` (or keeps 175 as slack). Then a **separate implementation lane** may delete L4 GND and build Architecture C against the chosen outline.
3. **Who acts:** Captain on the gate; implementation lane only after that.
4. **Shipped means:** EasyEDA PCB1 outline + placement + L4 pour match the chosen candidate, witnessed by gateway run id — **not this file**.

Visual: `K1-Core-VAL-R1-Placement-Closure.html`

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Closure gate 160_PASS from super-macro study. |
