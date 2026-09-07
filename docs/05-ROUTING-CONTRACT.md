---
abstract: "Stop before unrestricted routing. USB stays outer Polar geometry. FlexSPI local. No inner-layer tracks on the donor today. P2 must not become a route-everything pass."
---

# 05 — Routing contract

**This bootstrap stops before unrestricted routing.**

Donor PCB1: 265 LINE + 230 ARC, **0 inner-layer tracks**, 218 vias (0 inverted), 6 pours all GND. That is a defect to fix with planes (P2), not an instruction to autoroute.

## After P2 only

- USB HS on L1 or L6 at 5.10 / 5.00 mil; do not use non-E inner pair geometry on 3313E.
- FlexSPI length-match to CLK, prefer L6, stay local to RT.
- Crystals stay local; no layer hop if avoidable.
- Kelvin shunt taps at the shunt pads, not on the force path.
- HMI `$1N3583` / `$1N3585` rename to `HMI_RGB_Dxx` is an implementation item, not a P1/P2 blocker.

Net-class proposal (reference-only): `reference/usb-impedance/20-net-class-proposal.csv`.

Next authorised lane after P2 PASS: **routing architecture** — not this bootstrap.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Routing freeze: stop before autoroute. |
