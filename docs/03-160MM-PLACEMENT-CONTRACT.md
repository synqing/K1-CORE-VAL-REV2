---
abstract: "Machine placement contract. Authority is placement_160.json then coordinate_map_160.csv. MACRO −15 mm X, 62 west-fixed, 7 exact reflows. Not a cut-line."
---

# 03 — 160 mm placement contract

This is **not** “cut the 175 mm board at x=160”. That method was falsified.

## Authority order

1. `reference/placement-160/placement_160.json`
2. `reference/placement-160/coordinate_map_160.csv`
3. This file
4. Prose

## Classes

| Class | N | Rule |
|---|---:|---|
| MACRO | 174 | Δx = **−15.000 mm**, Δy = 0 |
| WEST_FIXED | 62 | USB-C, buck island, shunt/INA, west mounts, west USB-CC — do not move |
| REFLOW | 7 | exact centres below |

Do not individually “improve” MACRO members during translation.

## Distances that must remain

| Pair | mm |
|---|---:|
| hub → S3 | 15.706 |
| hub → RT | 22.390 |
| S3 → RT | 36.889 |
| RT → flash | 10.882 |
| RT → crystal | 12.528 |
| audio / HMI | 17.869 |
| encoder C2C | 11.205 |
| HMI column | 11.300 |
| RGB column | 11.220 |

## Distances that should shorten

| Pair | 175 | 160 |
|---|---:|---:|
| USB-C → hub | 72.534 | 57.545 |
| shunt → LED-N | 91.956 | 76.957 |

## Exact reflow (mm)

| Part | Side | x | y |
|---|---|---:|---:|
| SVC-ADC1 | bottom | 54.00 | 33.50 |
| C-SVC-DEC1 | bottom | 54.00 | 30.70 |
| R-PWR-I2C1 | bottom | 51.50 | 33.50 |
| R-PWR-I2C2 | bottom | 56.40 | 33.50 |
| R-LEDN-PRS1 | bottom | 51.50 | 30.20 |
| R-S3-IRQ1 | top | 44.80 | 27.20 |
| SVC-TEMP1 | top | 40.97 | 29.07 |

ADC cluster is **bottom** so the L1 USB north wrap stays open. Do not put parts under the WROOM. Antenna keepout stays south of S3.

## Red controls (verifier must go red)

- A: cut outline to 160, leave parts → HMI off-board
- B: −15 mm macro, skip seven reflows → ADS7138 overlaps S3
- C: −15 mm + seven reflows → GREEN

Battery: `reference/placement-160/selftest.json`.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Placement contract from closure 160_PASS. |
