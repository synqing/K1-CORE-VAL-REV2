---
abstract: "JLC06161H-3313E confirmed. Layer Manager sums to 1.650 mm. L1 refs L2, L3 refs L2 not L4, L4 refs L5, L6 refs L5. Freeze the stack. Do not use JLC06161H-3313 (non-E) widths."
---

# 05 — Current stack

## Verdict

**Freeze `JLC06161H-3313E`.** Do not normalise to 1.6 mm. Do not open EasyEDA Layer Stack Manager and click OK — that regenerates from the non-E preset (known split-state hazard in `harness/r1_apply_3313e_stack.py`, P4 rationale).

## Layer Manager construction (P1, MEASURED)

| z | Layer | Type | Thickness mm | Er |
|---|---|---|---:|---:|
| L1 | Top | Cu 1 oz | 0.035001 | — |
| | Dielectric1 | 3313 RC57% 4.2 mil | 0.099390 | 4.1 |
| L2 | Inner1 | Cu inner | 0.015189 | — |
| | CORE1 | 0.1 mm internal core | 0.100000 | **4.36** |
| L3 | Inner2 | Cu inner | 0.015189 | — |
| | CORE2 | 7628 prepreg | 0.210400 | 4.4 |
| | Substrate | 0.7 mm core | 0.700000 | 4.53 |
| | CORE3 | 7628 prepreg | 0.210400 | 4.4 |
| L4 | Inner3 | Cu inner | 0.015200 | — |
| | Dielectric4 | 0.1 mm core | 0.100000 | 4.36 |
| L5 | Inner4 | Cu inner | 0.015189 | — |
| | CORE4 | 3313 prepreg | 0.099400 | 4.1 |
| L6 | Bottom | Cu 1 oz | 0.035000 | — |

**Sum = 1.65036 mm.**

Official JLC table “10) JLC06161H-3313E” at https://jlcpcb.com/impedance (retrieved 2026-09-07): 0.035 / 0.0994 / 0.0152 / 0.10 / 0.0152 / 0.2104 / 0.70 / 0.2104 / 0.0152 / 0.10 / 0.0152 / 0.0994 / 0.035. **Match.**

Non-E `JLC06161H-3313` uses 0.55 mm cores and finishes ~1.54 mm. **Different board. Do not copy its trace widths.**

## Adjacency (the point)

| Signal layer | Primary reference | Dielectric | Why |
|---|---|---|---|
| L1 | L2 | 0.0994 mm, Er 4.1 | coated microstrip |
| L3 | **L2** | 0.100 mm, Er 4.36 | L4 is 1.12 mm below through 7628+0.7+7628. L3 is **not** a symmetric stripline to L4. |
| L4 | L5 | 0.100 mm, Er 4.36 | power plane capacitance is L4↔L5 |
| L6 | L5 | 0.0994 mm, Er 4.1 | same as L1 |

## Functional roles

Intended (keep):

```
L1 signal + local 5V
L2 GND
L3 signal / RT escape
L4 power (3V3 + VDD_SOC)   ← today this pour is GND
L5 GND
L6 signal + local 5V
```

Actual P0: L2–L5 and L6 and L1 are GND pours; **zero inner tracks**. That is a pour defect, not a reason to change the role map.

## USB 90 Ω

Orchestrator re-ran the cart template API (2026-09-07): `JLC06161H-3313E` is live, `compressionThickness` **1.6504 mm**, template `202601260616524415`, special/not default. Full Polar write-up: `05-jlc-official-stack.md`.

JLC does not publish a static 3313E width table. Polar SI9000 via JLC’s calculator (`DiffEdgeCoupledCoatedMicrostrip1B`, H1=0.09940 mm Er 4.1):

| | W | S | Zdiff |
|---|---:|---:|---:|
| **Use this** | **5.10 mil (0.1295 mm)** | **5.00 mil (0.1270 mm)** | **90.00 Ω** |
| Also ~90 Ω, tighter | 3.94 mil (0.100 mm) | 3.54 mil (0.090 mm) | 90.28 Ω (on JLC 3.5 mil floor — do not prefer) |

Non-E inner 4.67 / 5.5 mil on this stack Polar-solves to **88 Ω**. Do not copy it.

Polar hop itself is websocket (`wss://tools.jlc.com/...`); this orchestrator re-ran the template API, not the Polar socket. Receipt: `evidence-jlc/jlc06161h-3313e-polar-2026-09-07.json`.

JLC impedance tolerance **±10 %**. USB 2.0 **90 Ω ±15 %**.

**Do not route USB on L3.**

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Re-parsed P1 JSON; matched official JLC 3313E table. |
