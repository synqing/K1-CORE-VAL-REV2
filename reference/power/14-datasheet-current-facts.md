---
abstract: "2026-09-07 manufacturer current/thermal/transient facts for live FABLE-R3 power and HMI parts. HMI is 6× WS2812E-1313 (0.220 A white max), not WS2816 strip 4 A. LED FPC/eFuse copper still 2 A/bar class. Encoder has no LED. KH-FG pin current NOT_VERIFIED."
status: VERIFIED_WITH_NAMED_GAPS
class: CLASS_C_RESEARCH
classification: load-bearing
lane: DOWNSTREAM-PCB-EVAL-2026-09-07
task: CURRENT-RATINGS-2026-09-07
---

# 14 — Datasheet current, thermal, transient facts

**Question:** manufacturer-documented current / thermal / transient numbers sufficient to size copper and decide L4 vs outer-layer 5 V.

**Live identities (FABLE-R3 PCB1, do not substitute):** GT-USB-7005A, USB2422T-I/MJ, TUSB320LAIRWBR, TPS259474LRPWR ×4 (PWR-FUSE1/2, LEDN-FUSE1, LEDS-FUSE1), TPS62913RPUR, MIMXRT1062DVJ6B, ESP32-S3-WROOM-1-N16R8, WS2812E-1313 ×6 (HMI-RGB1…6 on the HMI cell), KH-EC063T122000 ×2 (4-pad, no LED), KH-FG1.0-H2.0-10PIN ×2 (LEDN-FPC1 / LEDS-FPC1), IM69D130V01.

**Hard split (failure mode of this lane):**

| Load | What it is | What it is not |
| --- | --- | --- |
| **HMI RGB** | 6 × WS2812E-1313, 4-pin, onboard | Not WS2813, not WS2816, not the 160-LED bars |
| **LED FPC path** | North/south 10P + eFuse, 4 A-class **strip** ceiling from architecture / WS2816C | Do not add 4.000 A into the HMI 5 V budget |
| **NFC** | Retired | Do not resurrect `IVDD_LDO` 350 mA |

Tags: **[DS]** this-session PDF extract with printed page. **[DERIVED]** arithmetic on [DS] only. **[NOT_VERIFIED]** no manufacturer number found. Typical is never used as max.

---

## 0. L4 vs outer-layer 5 V (the decision this file exists for)

| Rail | Documented current that copper must survive | Layer implication |
| --- | --- | --- |
| **+5V_SYS / HMI RGB** | **0.220 A** theoretical full-white ×6 **[DERIVED]** from WS2812E p.3 | Outer 1 oz, sub-millimetre width. **Does not earn an L4 5 V corridor.** |
| **Logic 5 V into TPS62913** | Buck IOUT **3 A capability** is silicon, not the load. 3V3 peak is S3 TX **0.355 A** + RT DCDC_IN **0.110 A** + hub **0.089 A** plus GPIO/ADC (see §2). Inlet-side 5 V for that 3V3 set is **< 0.6 A** at η≥90 % **[DERIVED]** | Outer. Not 4 A-class. |
| **LEDN / LEDS 5 V (FPC)** | Architecture / WS2816C strip: **2.000 A per bar**, **4.000 A both** (LANE-PWR E1). USB 3 A cannot run that. | This is the only 4 A-class 5 V. Outer ~2 mm class at 4 A / 1 oz / 10 °C is the architecture statement; L4 is a **corridor** choice if outer is blocked — **not** a current-capability need for HMI. |
| **USB VBUS at J1** | Receptacle **5 A VBUS rating** (headroom). Source grant is CC: 0.5 / 1.5 / 3.0 A. eFuse **IMAX 5.5 A**, ILIM programmed. | Connector and eFuse outrank copper for the inlet. |

**Verdict for copper planning:** size L4 5 V only if the **LED-bar** 2 A/bar current is forced inner. Do not size inner 5 V from HMI LEDs. Do not fold WS2816 strip amperes into +5V_SYS.

---

## 1. WS2812E-1313 — onboard HMI ×6

**PDF:** `research/lanes/DOWNSTREAM-PCB-EVAL-2026-09-07/_extract/pdfs/WS2812E-1313.pdf`  
Worldsemi, 7 pages, 4-pin 1313. SHA-256 `96c12eb2eacd8af164b60aa800fa532f2c27d4ace42d8d5b7e62fdf2fd4fd7c0`. Fetched LCSC C5446700 datasheet blob 2026-09-07.  
**Not** `sources/manufacturer/WS2816C-1313-*.pdf`.

Live: HMI-RGB1…HMI-RGB6, footprint `LED-SMD_4P-L1.3-W1.3-P0.80_WS2812E-1313`.

| Fact | Number | Citation |
| --- | --- | --- |
| Pins | 1 VDD, 2 DOUT, 3 GND, 4 DIN | p.2 pin table |
| VDD abs max | +3.7 ~ +5.3 V | p.2 Absolute Maximum Ratings |
| Topt | −40 ~ +65 °C | p.2 |
| DIN/DOUT II | ±1 µA max | p.2 Electrical Characteristics, TA=25 °C, VDD=5 V |
| tTHZ (OUTR/G/B fall) | 120 µs max | p.2 Switching Characteristics |
| **Quiescent current** | **< 0.6 mA** | **p.3 LED Characteristics header** |
| **Working current (brightness/λd condition)** | **12 mA per colour** | **p.3**, columns “Condition (Working current)” for IV and λd |
| Iout min/typ/max table | **not published** on this PDF | unlike WS2816C V1.1 p.3 |
| Decoupling | “recommend 100 nF between GND and VDD” | p.4 Remarks |
| Inrush / Ipeak beyond 12 mA/ch | **not published** | — |

**Arithmetic [DERIVED] — use 12 mA as the constant-current design point; there is no higher DS max:**

```
I_IQ_max        = 0.6 mA                    (p.3 bound)
I_one_colour    = 12 mA + 0.6 mA = 12.6 mA
I_white_1LED    = 3 × 12 mA + 0.6 mA = 36.6 mA
I_dark_×6       = 6 × 0.6 mA = 3.6 mA
I_white_×6      = 6 × 36.6 mA = 219.6 mA = 0.220 A
I_step_dark→W   = 0.220 − 0.004 = 0.216 A
```

Realistic product limit: HMI indicators are not a 4 A visualiser. Copper and +5V_SYS still survive **0.220 A** coincident white. Firmware duty does not shrink the number. Six 100 nF caps → 0.6 µF; at 5 V / 10 µs that is tens of milliamps of charge current — not an ampere-class inrush. **[DERIVED]**

World-semi family web table “WS2812E … 12mA×3” agrees with the 12 mA working-current condition; it is **not** this PDF and is not used as a second max.

---

## 2. 3V3 consumers (logic, not LED copper)

### 2.1 USB2422T-I/MJ — USB-HUB1

**PDF:** `research/lanes/LANE-USB/datasheets/USB2422-DS00001726.pdf` DS00001726B. SHA-256 `4a9ad71cd6535368f9535d08924dbff9c21c0554d5fbf01cf06ae0d92a44fc0d`.

Industrial TA −40 ~ +85 °C (p.35). VDD33 3.0 ~ 3.6 V (p.35). Rise time tRT33 0 ~ 400 µs (p.35, Fig 5-1 p.36).

**Table 5-1 DC electrical characteristics (p.36–37), VDD33 = 3.3 V:**

| Symbol | Condition | Typ | Max | Unit |
| --- | --- | --- | --- | --- |
| ICCINTHS | Unconfigured Hi-Speed host | 40 | 45 | mA |
| ICCINTFS | HS host, each additional DN | 35 | 40 | mA |
| **IHCH1** | HS host, 1 DN | **47** | **58** | mA |
| **IHCH2** | HS host, **2 DN** (this board) | **70** | **89** | mA |
| IFCC2 | FS host, 2 DN | 35 | 45 | mA |
| ICSBY | Suspend | 425 | 1000 commercial / **1200 industrial** (Note 5-6) | µA |
| ICRST | Reset | 300 | 800 / **1000 industrial** (Note 5-7) | µA |

**Note 5-8 (p.37):** “Current measured during **peak USB traffic** and does not reflect the average current draw.” So **89 mA is Imax/Ipeak, 70 mA is typical peak-traffic, not a quiet average.** Use **0.089 A** on 3V3 for copper.

### 2.2 ESP32-S3-WROOM-1-N16R8

**PDF:** `research/lanes/LANE-PWR/datasheets/ESP32-S3-WROOM-1_v1.8.pdf` v1.8. SHA-256 `27d71971da07c280c6068d08c74720d1a25b8f20cf8494dc1765bdd28d40d435`.

All currents at **3.3 V, 25 °C**. “TX current consumption is rated at a **100 % duty cycle**.” (p.28)

**Table 6-4 Wi-Fi active (p.28):**

| RF | Description | Peak (mA) |
| --- | --- | --- |
| TX | 802.11b, 1 Mbps, @20.5 dBm | **355** |
| TX | 802.11g, 54 Mbps, @18 dBm | 297 |
| TX | 802.11n HT20 MCS7 @17.5 dBm | 286 |
| RX | 802.11b/g/n HT20 | 95 |

**Table 6-5 BLE active (p.28):** TX @ 20.0 dBm **344 mA**; @ 9 dBm 202 mA; RX 93 mA.

**Table 6-6 Modem-sleep (p.29), 240 MHz:** WAITI Typ1 32.9 / **Typ2 47.6 mA** (peripherals on); dual-core 32-bit Typ2 **81.3 mA**; dual-core 128-bit Typ2 **107.9 mA**.

Note on p.29: in-package **PSRAM (N16R8)** “current consumption of the module **might be higher**” than Table 6-6. TX tables are still the burst bound.

**Use: Itransient / Imax = 0.355 A (Wi-Fi 100 % TX). Itypical idle-class = 0.0476 A WAITI Typ2 @ 240 MHz, with PSRAM-upside unnamed.** Hardware must supply the TX spike even if BLE-MIDI is bursty.

### 2.3 MIMXRT1062DVJ6B

**PDF:** `research/lanes/LANE-RT/datasheets/IMXRT1060CEC.pdf` (CEC Rev 4, 04/2024) and `…/IMXRT1060IEC.pdf` (IEC Rev 4). Extracted CEC SHA-256 `d65fcf01020ccde2181a716ba6eeb5b9dc66b368b0c3066c1734f9d8e060e388`.

MPN **D**VJ6B → industrial table is IEC. Both books publish the same 110 mA DCDC_IN max (CEC @ 95 °C p.27; IEC @ 105 °C printed p.26).

**Table 12 Maximum supply currents** (CEC p.27 / IEC p.26). NXP’s own warning: this is a **max-power use case**, cores at max frequency, L1-only, “extremely low duty cycle” unless the intent is worst-case power.

| Rail | Max | Notes |
| --- | --- | --- |
| **DCDC_IN** | **110 mA** | “Max power for chip … core mark run on FlexRAM” |
| VDD_HIGH_IN | 50 mA | internal analog loading |
| VDD_SNVS_IN | 250 µA | |
| USB_OTG1/2_VBUS | 25 mA **each active** USB; table row 50 mA for both | this product is a **device** on the hub; VBUS 25 mA is host-experiment, not the 3V3 budget |
| VDDA_ADC_3P3 | 40 mA row = 750 µA max per ADC **plus 33 mA of 100 Ω touch panel**. Touch is **not fitted**. ADC-only **750 µA max**, 600 µA typ | |
| NVCC_GPIO/SD/EMC | `Imax = N·C·V·(0.5·F)` only — **no ampere number** | |

**Typical DCDC_IN 53.1 mA** is AN12245 Table 7, **not re-opened this session** → Itypical **NOT_VERIFIED** here. Do not treat 110 mA as typical.

No manufacturer transient (dI/dt) for DCDC_IN beyond “maximum supply current”.

### 2.4 TUSB320LAIRWBR — USB-CC1 (UFP)

**PDF:** `research/lanes/LANE-USB/datasheets/TUSB320LAI-SLLSEQ8.pdf` SLLSEQ8D. SHA-256 `96e1dcb810eaafa552a2839d33610e5568944065bbd8d5b2187a70de0542e09b`.

**§6.5 Electrical Characteristics (printed p.5):**

| Parameter | Typ | Max | Unit | Role on this board |
| --- | --- | --- | --- | --- |
| IUNATTACHED_UFP | 70 | — | µA | VDD current, unattached UFP |
| **IACTIVE_UFP** | **70** | — | µA | VDD current, active UFP |
| ISHUTDOWN | 0.04 | — | µA | EN_N high |
| ICC_DEFAULT/MED/HIGH_P | 80 / 180 / 330 typ | 96 / 194 / 356 | µA | **DFP Rp source current — not a UFP VDD load** |

UFP current advertisement **detection** bands (same table): default 0.25–0.61 V, 1.5 A 0.70–1.16 V, 3 A 1.31–2.04 V. These classify the **source grant**, they are not this IC’s supply current.

### 2.5 IM69D130V01 — AUD-MIC1

**PDF:** `research/lanes/LANE-AUD/datasheets/IM69D130_DS_v01_00-EN.pdf` v01.00, 2017-12-19. SHA-256 `7d6c2bebd1da22cec7376747a6cad97b2d1548825e917f51ba3b73939bd8b541`.

**Table 5 (p.7), VDD=1.8 V, TA=25 °C, no load on DATA:**

| Clock | IDD typ | IDD max |
| --- | --- | --- |
| 3.072 MHz | 980 µA | **1300 µA** |
| 2.4 MHz | 800 µA | 1050 µA |
| Standby | 25 µA | 50 µA |
| Clock off | — | 1 µA |
| Short-circuit (DATA grounded) | 1–20 **mA** | pin current, not VDD |

Startup 20–50 ms. **Imax supply 1.30 mA.** Negligible next to S3 TX.

### 2.6 TPS62913RPUR — PWR-BUCK1

**PDF:** `research/lanes/LANE-PWR/datasheets/TPS62913_SLVSFP4B.pdf` SLVSFP4B. SHA-256 `5dec6fe38b5a41a8e5325c5f27d263b80861f8f5242038c29945776da733fda0`.

| Fact | Number | Citation |
| --- | --- | --- |
| Device IOUT | **0 ~ 3 A** (TPS62913; TPS62912 is 2 A — do not swap) | p.1 Device Information; **§6.3 p.4** |
| VIN | 3.0 ~ 17 V | §6.3 p.4 |
| VOUT | 0.8 ~ 5.5 V | §6.3 p.4 |
| IQ | **5 mA typ**, EN high, no load, switching, fSW=1 MHz | §6.5 p.5 |
| ISD | 0.3 typ / 70 µA max | §6.5 p.5 |
| RθJA | 87.7 °C/W JEDEC 51-7; **56.6 °C/W** on TPS6291xEVM-077 | §6.4 p.4 |
| TJ rec | −40 ~ 150 °C (lifetime derated above 125 °C) | §6.3 note |
| Soft-start | tSS = C·0.8 / 75 µA; 470 nF → 5.01 ms | §7.3.8 (LANE-PWR extract; pin contract) |

3 A is **capability**, not the K1 3V3 load. 3V3 silicon is not the bottleneck.

---

## 3. 5 V path devices

### 3.1 TPS259474LRPWR — live eFuse on USB/bench **and** both LED edges

**PDF:** `research/lanes/LANE-PWR/datasheets/TPS25947_SLVSFC9.pdf` SLVSFC9C (Oct 2020, **Rev C May 2026**). SHA-256 `051ecddfe545b8b9f4f992148d24f385f75b1116fd36bec358f85008a7d919ec`.

Live: PWR-FUSE1, PWR-FUSE2, **LEDN-FUSE1, LEDS-FUSE1** — all **TPS259474LRPWR** (not 470L).

**Table p.4 Device Comparison:** TPS259474x = adjustable OVLO + **circuit breaker** + L = **latch-off**. TPS259470x = **active current limit**. 474 does **not** fold back to ILIM and keep conducting; after ITIMER it **opens and latches**.

| Fact | Number | Citation |
| --- | --- | --- |
| VIN rec | 2.7 ~ 23 V | §6.3 p.8 |
| **IMAX continuous** | **5.5 A**, TJ ≤ 125 °C | **§6.3 p.8 IMAX** |
| ILIM program | 0.5 ~ 6 A; RILM 549 ~ 6650 Ω | p.1; §6.3 p.8 |
| Formula | **RILM(Ω) = 3334 / IILM(A)** | §7.3.5.2 Eq. 5, p.30 |
| Accuracy | ±10 % for ILIM > 1 A | p.1 |
| Worked ILIM (p.9) | 1.65 kΩ → 1.800 / 2.028 / 2.200 A; 750 Ω → 3.96 / 4.452 / 4.84 A; 549 Ω → 5.40 / 6.068 / 6.60 A | §6.5 p.9 |
| **Transient blanking** | peaks up to **2 × ILIM** while ITIMER runs | p.1; §7.3.5.2 p.30 |
| Fast-trip scalable | ISC ≈ **2.01 × ILIM** (ISCGain 201 % typ) | §6.5 p.10 |
| Fast-trip fixed | IFT **22.2 A** typ; 500 ns | §6.5 p.10; p.1 |
| tCB (474x) | 2 µs after ITIMER expiry | §6.7 |
| RON | 28.2 mΩ typ @ 12 V 25 °C 3 A; **45 mΩ max** −40~125 °C | §6.5 p.9 |
| IQ(ON) 474x | 428 typ / **610 µA max** | §6.5 p.9 |
| IQ(OFF) | 73 / 130 µA | p.9 |
| RθJA | **41.7 °C/W** custom-board; **74.5 °C/W** JEDEC | §6.4 p.8 |
| Inrush | SR(V/ms) = IINRUSH(mA) / COUT(µF); CdVdt(pF) = 2000 / SR | §7.3.5.1 Eq. 3–4, p.29 |
| UL 2367 | RILM ≥ 750 Ω | p.1 |

USB inlet pin-contract target IILM ≈ 3.03 A → RILM = 1.10 kΩ (`architecture/pin-contracts/TPS259474L.md`). That is a **setpoint**, not a load.

**Thermal at LED-bar 2.00 A [DERIVED]:** P = I²·RON_max = 4 × 0.045 = 0.180 W. ΔT ≈ 7.5 °C (41.7) / 13.4 °C (74.5). Not the melt risk. The melt risk is **trace and FPC pins**, not the QFN.

**Transient trap for 474L on LED PWM:** a dark→full-white bar step (0.16 → 2.00 A on the **strip**, not HMI) sits under 2×ILIM only if ILIM is set above the step. If ITIMER expires, **latch-off**. Size ITIMER to the visualiser beat; do not set ILIM to average duty.

### 3.2 GT-USB-7005A — USB-C1

**PDF:** `research/lanes/LANE-USB/datasheets/GT-USB-7005A-manufacturer-drawing.pdf` G-Switch, Rev A0, 2023-02-01, sheet 1/1. SHA-256 `abe0fb3ee8c705b2c394e6f642c5268542377784c97e64785af050207d9223a0`. Drawing is vector/image; text recovered from raster of the specification block.

**G-Switch USB-C Specification (drawing, right column):**

1. **Current rated: 5 A on VBUS / 1.25 A on VCONN / 0.25 A on other**
2. Voltage rating 24 V AC; withstand 100 V AC/min
3. −40 ~ +85 °C; 10 000 cycles; up to 10 Gbit/s

VBUS contacts A4, A9, B4, B9 (pin map on the same sheet). **5 A is the total VBUS rating, not 5 A per pin.** VCONN 1.25 A is unused (R1-D-027 SuperSpeed/SBU NC). Signal pins 0.25 A.

**5 A is connector headroom, not a USB grant.** Source current is CC advertisement.

### 3.3 USB Type-C source grants (sink)

**PDF:** `research/lanes/LANE-PWR/datasheets/USB-Type-C-Spec-R2.0-August-2019.pdf` (LANE-PWR provenance SHA-256 `87d15160…9981`). Printed **p.219 Table 4-18** (quoted in `LANE-PWR/CONSUMED.md`; SuperSpeed NC → USB 2.0 Default):

| Advertisement | Sink may draw | PDP |
| --- | --- | --- |
| Default USB 2.0 | **500 mA** | 2.5 W |
| 1.5 A | **1.5 A** | 7.5 W |
| 3.0 A | **3.0 A** | 15 W |

tSinkAdj max **60 ms**. USB 3 A **cannot** run 4.000 A strip full-stress. HMI 0.220 A **can** sit inside Default **only if** radio TX is off (0.355 A on 3V3 already blows 500 mA after conversion).

---

## 4. Connectors and encoder

### 4.1 KH-FG1.0-H2.0-10PIN — LEDN-FPC1 / LEDS-FPC1

Live 10P, 1.00 mm, H2.0, north and south. Architecture contact map: 4× +5V, 4× GND, DA, DB (`contracts/led.md`).

**Manufacturer current rating for this exact MPN: NOT_VERIFIED this session.** Kinghelm product HTML for this part lists temperature −25~+85 °C, 50 V, contact ≤0.03 Ω, insulation ≥500 MΩ — **no ampere**. Sibling `KH-FPC1.0-H2.0SMT-10P-QCHF` is advertised 0.5 A/PIN on kinghelm.net; **different MPN, not a bind.**

If 0.5 A/PIN were true, 4 paralleled +5V fingers → **2.0 A per bar**, which is exactly the architecture 2.000 A/bar stress. That coincidence is **[HYPOTHESIS]** until the FG drawing states a current. **This is the highest-leverage gap for 4 A-class copper:** a 2 A bar through an unrated 1.00 mm FFC can melt the connector before L4 matters.

KiCad-era Würth 686110148922 is **not** the live part (R1-D-066 EasyEDA identities).

### 4.2 KH-EC063T122000 — HMI-ENC1 / HMI-ENC2

Live footprint `SW-SMD_KH-EC063T122000`, **4 pads**. Pull-ups on the board are `0402WGF1002TCE` (10.0 kΩ) on A/B/SW. **No LED pad, no LED current.**

**Manufacturer contact rating: NOT_VERIFIED** (Kinghelm PDF not retrieved; LCSC search did not return a datasheet this session). Closed-switch current is pull-up limited: 3.3 V / 10 kΩ ≈ **0.33 mA per closed contact [SCH]**, not a datasheet Imax. Do not budget encoder milliamps on 5 V.

---

## 5. Strip path (LED FPC) — cite, do not mix into HMI

Architecture / LANE-PWR E1 uses **WS2816C-1313-4P V1.1 p.3**: Iout 10 / 10.5 / **11.5 mA** (R+G+B), IDDdyn 0.7 typ / **1.0 mA max**, N = 160 / bar × 2 bars.

```
I_bar_white_wc = 160 × (11.5 + 1.0) mA = 2.000 A
I_both         = 4.000 A
```

That number sizes **LEDN/LEDS copper, eFuse ILIM, bench inlet**. It is **forbidden** as the 6-LED HMI load. HMI white ×6 is **18× smaller** (0.220 A vs 4.000 A).

USB policy (unchanged, still true): USB Default LED **off**; USB 1.5 A constrained envelope; USB 3 A higher-product **no full-white strip**; bench 4 A-class. Logic XOR stays off the LED trunk.

---

## 6. Gaps (named)

1. **KH-FG1.0-H2.0-10PIN pin current** — NOT_VERIFIED. Blocks a confident 2 A/bar connector verdict.
2. **KH-EC063T122000 contact mA** — NOT_VERIFIED; electrically irrelevant if 10 kΩ pull-ups hold.
3. **WS2812E Iout max** — only a 12 mA working-current condition; no min/typ/max supply row.
4. **RT typical** — AN12245 53.1 mA not re-extracted.
5. **NVCC GPIO amperes** — formula only.
6. **WROOM N16R8 PSRAM adder** on Table 6-6 — unnamed.
7. **Live RILM values** on the four 474L instances — schematic setpoint, not this datasheet extract.
8. NFC currents omitted (retired).

---

## 7. Re-run (lead)

```
pdftotext -layout research/lanes/DOWNSTREAM-PCB-EVAL-2026-09-07/_extract/pdfs/WS2812E-1313.pdf -
pdftotext -layout research/lanes/LANE-PWR/datasheets/TPS25947_SLVSFC9.pdf -
pdftotext -layout research/lanes/LANE-PWR/datasheets/TPS62913_SLVSFP4B.pdf -
pdftotext -layout research/lanes/LANE-PWR/datasheets/ESP32-S3-WROOM-1_v1.8.pdf -
pdftotext -layout research/lanes/LANE-USB/datasheets/USB2422-DS00001726.pdf -
pdftotext -layout research/lanes/LANE-USB/datasheets/TUSB320LAI-SLLSEQ8.pdf -
pdftoppm -png -r 200 research/lanes/LANE-USB/datasheets/GT-USB-7005A-manufacturer-drawing.pdf /tmp/gtusb
pdftotext -layout research/lanes/LANE-RT/datasheets/IMXRT1060CEC.pdf -
pdftotext -layout research/lanes/LANE-AUD/datasheets/IM69D130_DS_v01_00-EN.pdf -
shasum -a 256 research/lanes/DOWNSTREAM-PCB-EVAL-2026-09-07/_extract/pdfs/WS2812E-1313.pdf
```

CSV: `research/lanes/DOWNSTREAM-PCB-EVAL-2026-09-07/14-power-load-model.csv`

---

**Document Changelog**
| Date | Author | Change |
| --- | --- | --- |
| 2026-09-07 | agent:grok SSA CURRENT-RATINGS | Created from in-repo manufacturer PDFs + WS2812E LCSC blob. HMI ×6 separated from strip 4 A. |
