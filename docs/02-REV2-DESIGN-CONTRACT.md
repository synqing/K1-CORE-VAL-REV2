---
abstract: "Locked REV2 product facts: 160×40, FPC 10P, six WS2812E-1313, no NFC, USB hub between MCUs, TPS62913 alias, JLC06161H-3313E."
---

# 02 — REV2 design contract

Frozen unless a new Captain ruling + `docs/DECISIONS.md` entry.

| Item | Contract |
|---|---|
| Outline | 160.00 × 40.00 mm |
| LED interconnect | FPC 10P (dual VH retired) |
| HMI | 6 tactile + 2 encoders + 6 × WS2812E-1313 (4-pad) |
| NFC | absent — do not reintroduce |
| USB | GT-USB-7005A → USB2422 between S3 and RT |
| S3 | ESP32-S3-WROOM-1-N16R8, antenna **south** |
| RT | MIMXRT1062DVJ6B |
| Buck | TPS62913RPUR (3 A). Footprint name may contain TPS62912. Do not swap the die. |
| Stack | JLC06161H-3313E, 6 layer |
| Layer roles | L1 sig+5V · L2 GND · L3 escape then GND fill · L4 3V3+VDD_SOC · L5 GND · L6 sig+5V |
| USB HS | outer 5.10 / 5.00 mil → 90.003 Ω (Polar receipt) |
| PWR-S3-001 | inductor body ↔ S3 body ≥ 12.51 mm |
| East mounts | edge-relative; ~2.64 mm inset after −15 mm |

Do not “correct” HMI LEDs to WS2813. Do not delete an HMI column to make 160 fit.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Design contract from 160_PASS + donor census. |
