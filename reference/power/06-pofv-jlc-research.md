---
abstract: "JLCPCB 6-layer POFV is epoxy-filled then copper-capped, free on 6–20 L. Hole 0.20–0.50 mm, annular ring 0.05 min / 0.075 preferred. Copper-paste fill is a paid thermal option. Current RT 0.20/0.35 mm vias sit on the published table."
---

# 06 — JLCPCB POFV research (current pages)

Retrieved 2026-09-07. Official pages, not PCBWay, not 2022 blogs as sole source (the 2022 POFV announcement is still linked from JLC and is consistent with the 2026-08-18 via-covering article).

## Process

| Name | Fill | Cap | 6-layer price | Use |
|---|---|---|---|---|
| POFV / epoxy-filled & capped | **non-conductive epoxy** | copper plate-over | **free default** on 6–20 L | BGA / SMT via-in-pad |
| Copper-paste-filled & capped | conductive copper paste | copper plate-over | charged; k=8 W/m·K | thermal vias, power pads |
| Ink plugged | solder-mask ink | none | standard | not for via-in-pad |
| Tented / untented | none | none | standard | ordinary vias |

Sources:

- https://jlcpcb.com/help/article/pcb-via-covering (updated **2026-08-18**)
- https://jlcpcb.com/news/free-via-in-pad-6-20-layer-pcbs-pofv (policy still cited 2026)
- https://jlcpcb.com/help/article/bga-design-guidelines---pcb-layout-recommendations-for-bga-packages
- https://jlcpcb.com/events/6-layer-pcb (Via In Pad: yes, free)
- https://jlcpcb.com/blog/via-in-pad-design-deep-dive (2026-07-16)

POFV construction: drill → plate → epoxy fill → planarize → second copper cap (surface ≥5 µm, up to 25 µm in the POFV write-up). Hole must be **≤ 0.5 mm** or fill is not guaranteed; JLC will not take complaints on larger holes.

Ink plugging is **forbidden** for via-in-pad and for vias <0.35 mm from a pad. Those must be epoxy or copper-paste.

## Geometry (mechanical POFV)

From the POFV announcement table + 2026-07 deep-dive:

| Parameter | Published |
|---|---|
| Hole | 0.20–0.50 mm (recommended 0.25–0.35) |
| Land at 0.20 hole | 0.30 or **0.35** mm |
| Annular ring | 0.05 mm min, 0.075 mm preferred |
| Aspect ratio | prefer ≤8:1, max 10:1 |
| Distance to PTH/NPTH | > 0.45 mm |
| Planarization | depression/protrusion ≤ 50 µm; 127 µm class mentioned as the pad-level spec |

This export’s vias: hole **0.200 mm**, land **0.350 mm**, type NORMAL, **0 inverted**. That is the 0.20/0.35 row of JLC’s table. Board 1.65 mm / 0.20 mm hole = aspect **8.25:1** — inside the 10:1 cap, slightly over the 8:1 comfort line. Acceptable; do not shrink the drill further.

BGA pad min published 0.25 mm. RT is 0.8 mm pitch / 12 mm VJ — VIP is the intended escape, not a sneak.

## Where it is a good idea

**A — strong:** RT signal/power/GND balls that actually need a layer change; RT/S3/hub HF decap to the adjacent plane; USB2422 EP if paste is windowed.

**B — useful:** eFuse / ADC EP thermal (prefer copper-paste fill here if paying); LED FPC return via banks.

**C — neutral:** random 0402 that already has a dogbone.

**D — avoid:** 0201 VIP; 4 A LED connector pads as the only current path (use a via **bank beside** the pad); VIP on a pad that must stay probing-friendly.

## Assembly

Capped epoxy vias are solderable (HASL or ENIG). Window the paste so it does not dump into a depression. Copper-paste fill is the thermal option (8 W/m·K); default POFV epoxy does **not** conduct heat through the barrel.

Tenting/mask: VIP pads are **not** tented; they take the board surface finish. Ordinary stitching vias should stay tented, hole ≤0.4 mm preferred.

## Pricing / order

6–20 layer: POFV via-in-pad is the **free default**. 4-layer still charged. Specify in Gerber notes which diameters are filled, or “all 0.20 mm vias”. Use “confirm production files”. Copper-paste fill is a separate, paid choice — do not assume it.

UNCONFIRMED this session: exact 2026 quote-page checkbox labels (interactive cart not driven). The help-centre and 6-layer capability page agree on free VIP for 6 L.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Official JLC via-covering (2026-08-18) + POFV + BGA pages. |
