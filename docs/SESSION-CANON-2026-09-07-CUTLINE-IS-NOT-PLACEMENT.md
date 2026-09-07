---
abstract: "Never-again canon 2026-09-07. Cut-line is not placement. 160_PASS is a −15 mm super-macro + 7 reflows. Folder bootstrap is not a live EasyEDA project. Canary needs :9223. Do not freeze 175 because chopping the east edge deletes the HMI."
status: CANON
authority: Captain 2026-09-07 (placement close-out + REV2 bootstrap)
identical_copy: "K1-CORE-VAL-R1 docs/agent/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md"
---

# SESSION CANON — 2026-09-07 — CUT-LINE IS NOT PLACEMENT

Read §1 before any board-length, placement, EasyEDA import, or “REV2 is ready” claim.

This session spent a full evaluation close-out, a Captain rejection, a real 160 mm coordinate study, and a REV2 bootstrap that **did not create a live EasyEDA project**. The cost was repeating a false 160 REJECT, then almost shipping a folder as if it were a board.

---

## 1 — The rules (bind every future agent)

1. **A cut-line is not a placement study.** Shortening the outline and reporting “HMI fell off” does **not** falsify a shorter board. Do not freeze 175 mm on that basis. Do not “reject 160” by deleting the east column.

2. **The 160 mm candidate is a super-macro translation.** Move the east chain as one piece: S3 + RF + hub + RT + LED/audio + **complete HMI** + east mounts, **Δx = −15.000 mm, Δy = 0**. Preserve relative electrical geometry. East holes are **edge-relative** unless enclosure authority freezes absolute X.

3. **Do not solve length by shrinking HMI pitch.** Six buttons, two encoders, six 4-pin WS2812E-1313 stay. Encoder C2C 11.205 mm, column 11.300 mm.

4. **The real 160 collision is the west doorway, not the HMI.** After −15 mm, S3 xmin = 42.78 mm into the ADS7138/service neighbourhood (SVC-ADC1 xmax was 47.70). Reflow **seven** parts at the contracted centres. Blind-translate of `R-S3-IRQ1` lands on the buck — that part is a reflow, not MACRO.

5. **Antenna is SOUTH of the WROOM, not west.** Inductor→S3 body 12.51 mm is I/O-side slack (PWR-S3-001 ≥ 12.51 mm), not an RF keepout violation. Do not move the buck island. Do not put parts under the WROOM. Put the ADS7138 cluster on the **bottom** so the L1 USB north wrap stays open.

6. **L2 and L5 stay one boring GND.** Do not split grounds to “contain” 4 A LED return. Contain the loop with forward/return copper geometry and stitching. 4 A LED is outer 1 oz. L4 is +3V3 + local VDD_SOC. L3 gets GND fill after escape (JLC: inner coverage < 25 % → thickness/warpage).

7. **A folder is not a board.** `cp donor.epro2 REV2.epro2` is not a new EasyEDA project. Gate B0 requires a **new** EasyEDA project object, title exactly `K1-CORE-VAL-REV2`, canonical export, SHA, donor-parity of 243 parts. Until then P1/P2 are **NOT STARTED**, not “ready for implementation.”

8. **EasyEDA actuation is `easyeda-run` only, and it needs CDP `:9223`.** Canary `FAIL` / `fetch failed` means the app was launched **without** the Bridge launcher. Do not attach CDP/MCP/Playwright to an already-open FABLE window. Never `openProject` onto FABLE. Never kill Captain’s unsaved session to get a port.

9. **The gateway still cannot certify P1/P2 writes.** `certified_mutating_verbs = []`. `outline-fit` / `outline-set` / `outline-clear` are automation bans. Product copper is uncertified. If the gateway cannot do it: **STOP**. Do not whole-document `setDocumentSource`. Do not invent a second automation stack.

10. **Prove the instrument can go red.** Cut-outline-in-place must RED (HMI off-board). Naive −15 mm without the seven reflows must RED (ADS7138 overlaps S3). Candidate GREEN is worthless if those two never fail.

11. **Measure the property, not the annotation.** Empty `PAD_NET` bodies are not “disconnected.” NFC substring hits on `C0402T104…` are not NFC hardware. A routing census of LINE+VIA that omits 230 ARCs is not a route census. Footprint title `TPS62912RPUR` is not a 2 A part — live identity is **TPS62913RPUR**.

12. **Namespace EasyEDA ids by project.** `K1-CORE-VAL-REV2::<document-id>::<primitive-id>`. Import may preserve donor UUIDs. That is not automatically corruption.

---

## 2 — What this session was asked to do

1. Read-only evaluation of live FABLE-R3 PCB1 (placement, 175 vs shrink, L4, POFV, routing architecture).
2. Captain rejected the 175 freeze: the 165/160/155 “candidates” were cut-lines.
3. Closure lane: genuine 160 super-macro study → exactly `160_PASS` or `175_FREEZE`.
4. REV2 bootstrap: new generation boundary, new EasyEDA project, then P1 then P2.
5. Git init, first commit, push to `https://github.com/synqing/K1-CORE-VAL-REV2.git`.

EasyEDA was **not** mutated in the evaluation or closure lanes. The donor FABLE-R3 archive SHA stayed `f9f33f0f7cbfc184ccb7b78e87e0840aae9ab5f74d672bbd09df8a3249dd9ebe`.

---

## 3 — Methodological failure (the expensive one)

### What Opus shipped

| Candidate | What it actually did | Verdict it claimed |
|---|---|---|
| 165 mm | `HMI-* → SHIFT_WEST -10` | blocked by HMI/mounts |
| 160 mm | chop outline; `HMI-BTNENC2 + RGB4/5/6 → OFF_BOARD` | REJECT |
| 155 mm | more chopping | REJECT |
| 175 mm | keep current XY | FREEZE |

That comparison table **assumed** shortening the board means crushing the HMI while leaving S3/hub/RT where they are.

### Captain’s ruling (bind)

- 175 freeze: **HOLD — not proven**
- 160 rejection: **REJECT THE REJECTION**
- Begin EasyEDA implementation: **NO-GO** until the super-macro experiment exists

### The experiment that was missing

Captain’s arithmetic, re-derived from PCB1 census (document origin, mm = mil × 0.0254):

| Fact | mm |
|---|---:|
| S3-MCU1 body west | 57.780 |
| SVC-ADC1 body east | 47.700 |
| U34 eastmost | 172.360 |
| 10 mm shift: S3 west vs ADC east | **0.080** |
| 15 mm shift: U34 eastmost | 157.360 (fits 160 with 2.64 mm inset, same as 175) |

A 10 mm slide almost clears the doorway. A 15 mm slide **does** collide with the service cluster. That collision is a **local reflow**, not a board-length kill.

### What the real 160 candidate is

| Class | N | Rule |
|---|---:|---|
| MACRO | 174 | −15.000 mm X |
| WEST_FIXED | 62 | USB-C, buck island, shunt/INA, west mounts, west USB-CC |
| REFLOW | 7 | exact centres in `docs/03-160MM-PLACEMENT-CONTRACT.md` |

Preserved: hub↔S3 15.706, hub↔RT 22.390, S3↔RT 36.889, RT↔flash 10.882, RT↔crystal 12.528, audio/HMI 17.869, encoder 11.205, HMI column 11.300, RGB column 11.220.

Shortened: USB-C→hub 72.534→57.545, shunt→LED-N 91.956→76.957.

Self-test (must still go red): `reference/placement-160/selftest.json`.

Gate token: **`160_PASS`**. Residual, not a kill: inductor body→S3 **12.51 mm** (was 27.51), I/O side, antenna south. Constraint **PWR-S3-001**.

Machine authority (do not reconstruct from prose):

```text
reference/placement-160/placement_160.json
reference/placement-160/coordinate_map_160.csv
```

---

## 4 — Classification traps (will re-break 160 if ignored)

- **Prefix is not class.** `C-PWR-DEC2` and south `LOGC-*` sit in the LED neighbourhood (~x=110–122). They **MACRO**. A `PWR-`/`LOGC-` WEST_FIXED rule would leave them behind the sliding LED FPC.
- **Not every S3 passive is MACRO.** `R-S3-IRQ2` stays west. `R-S3-IRQ1` cannot take −15 mm (lands in the buck). Park it north of the new S3 west corner.
- **HMI column pair is BTN1↔BTN6, not BTN1↔BTN4.** BTN4 is the other column’s far row; hypot() looks like ~24.7 mm. That is a diagonal, not pitch.
- **“North of S3 corridor” is not the first 0402.** `R-S3-IRQ1` sits 1.2 mm north of S3 at x≈44–45. The USB alley is x≈49.5–61.8 × y≈25.7–40. A metric that treats any overlapping-X body as a full-width wall is lying.
- **Min same-side gap 0.279 mm** (`HMI-ENC2`–`R-HMI-ENCS2`) already exists on 175. Do not blame 160 for it.

---

## 5 — Power / POFV language that must not come back

Captain corrections (keep):

| Wrong | Right |
|---|---|
| “4 A LED return must stay out of the shared GND plane” | L2/L5 stay unified GND. Contain the loop in copper geometry. |
| “POFV epoxy is thermally dead” | Plated barrel/cap still conducts. Copper-paste is *better*, not the only live path. |
| “HMI 0.220 A earns L4 5 V” | No. Six WS2812E full-white. Outer 1 oz. |
| “Force 4 A through 0.5 oz L4” | Outer 1 oz + via banks. |

Architecture C is locked topology, **not poured**. `reference/power/planes_160.json` is **REFERENCE_ONLY UNTIL RECONCILED** (generator area vs prose disagreed). Do not inject those polygons blindly.

RILM (TPS259474, DS table / 3334/I):

| Resistor | R | IILM |
|---|---|---|
| LED-N / LED-S | 1.65 kΩ | 2.028 A typ |
| USB | 1.10 kΩ | 3.03 A derived |
| bench DNP | 825 Ω | 4.04 A derived |

`KH-FG1.0-H2.0-10PIN` Kinghelm drawing (LCSC C2797226, 2015-01-28 raster): 50 V, ≤0.03 Ω, ≥500 MΩ, −25–85 °C. **No A/pin.** Sibling `KH-FPC1.0-H2.0SMT-10P-QCHF` is 0.5 A/PIN — **different MPN**. Product-power blocker independent of 160 vs 175.

USB Polar (JLC06161H-3313E): outer **5.10 / 5.00 mil → 90.003 Ω**. Do not use non-E inner 4.67/5.5 on this stack.

---

## 6 — Data-quality scars

| Scar | What happened | Rule |
|---|---|---|
| Routing census | File had 265 LINE + 218 VIA. PCB1 has **230 ARC**. Agents used it for congestion. | Census LINE+ARC+VIA or do not quote it. |
| Buck alias | Identity `TPS62913RPUR` (3 A), footprint title `…TPS62912RPUR` (2 A). | Do not “correct” the die to 62912. |
| RILM “unresolved” | Values were already in the component census (1.65k / 1.10k / 825). | Read the census before declaring a gap. |
| NFC false positive | `C0402T104K4RACTU` matched `C0402`/`NFC` token search. **Zero placed NFC.** | Inspect hits. Do not revive NFC. |
| PAD_NET empty | PCB1 padNet bodies blank. | Copper `netName` + schematic wire labels. Colour is not connectivity. |
| HMI auto-nets | `$1N3583` / `$1N3585`. | Rename in an implementation txn, not a verification lane. |
| Baseline manifest | FABLE-R1 SHA `b6cabdc3…` ≠ FABLE-R3 `f9f33f0f…`. | Manifest mismatch → do not use manifest geometry. |
| Polar vs live coverlay | Help-table 5.10/5.00 is the contract. Old 0.100/0.090 mm is Polar-valid ~90 Ω but **below** JLC 3.5 mil floor preference. | |

---

## 7 — Visual / oracle scars

- PCB y=0 is the **south** edge. SVG y increases down. Draw north-up (`svg_y = (40 − ymax) × scale`) or Captain sees USB-C with the antenna at the top.
- A file path is not a visual. Open/publish the HTML. Headless Chrome `--screenshot` is viewport-height; 2200 px cropped the self-test.
- Dark `prefers-color-scheme` made FR4 overlay unreadable. Keep the **board canvas light** even if chrome is dark.
- Bar length must encode **goodness** (shorter USB = longer bar). Preserved distances are goodness too.

---

## 8 — REV2 bootstrap scars (this is why “ready for implementation” was false)

| Claim that felt like progress | Reality |
|---|---|
| Folder exists, docs written, 22 hashed refs | Necessary, not B0 |
| Donor `.epro2` copied into `reference/donor-r1/` chmod 444 | Reference. **Not** `easyeda/K1-CORE-VAL-REV2.epro2` |
| Git init + push to GitHub | Versioning. Not a live EDA project |
| “Next agent can begin implementation” | **No.** Next agent starts at **Gate B0** (import-test), not P1 |

**B0 blocker (2026-09-07):** EasyEDA Pro was running **without** `--remote-debugging-port=9223`. `easyeda-run canary` → `FAIL` / `fetch failed`. Attaching to that window, or `openProject` over FABLE, is forbidden. Killing it risks unsaved donor work.

Later the same host **did** listen on `:9223`. That does **not** retroactively create a REV2 project. Check `lsof -nP -iTCP:9223` **this session**. Yesterday’s canary is not today’s.

**Even after B0 is green:** P1 (outline + 174 moves + 7 reflows) and P2 (delete L4 GND, pour 3V3) are still **capability-blocked** unless Captain certifies verbs or a human does them in EasyEDA. Empty `certified_mutating_verbs` + “finish placement” = STOP, not a 10-call tour.

Importer stall at “Importing 50 %” (2026-09-05 R6) is **still unresolved**. `import-test` may fail even with a green canary. Same failure twice → stop, change approach. Lengthening a timeout is not a change of approach. Recovery: `easyeda-run canary --dismiss-dialog`.

---

## 9 — Git / GitHub scars

- First commit used a fake `agent:grok <rev2-bootstrap@local>` author. Amend `--reset-author` **before** anyone pulls. After push, do not rewrite.
- Captain-named path `/Users/spectrasynq/Workspace_Management/Software/K1-CORE-VAL-REV2` is the allowed sibling. Do not invent `…-g1` worktrees.
- GitHub repo was created **PUBLIC** (same as other VAL repos; KiCad hardware repos are PRIVATE). The 3 MB donor `.epro2` is on the internet. Do not silently flip visibility; do not pretend it is private.
- Canonical export must stay `easyeda/K1-CORE-VAL-REV2.epro2` — one name. Checkpoints go in `evidence/checkpoints/`, not `REV2-final2.epro2`.

---

## 10 — What we already knew (do not re-discover)

These were prior canons. This session re-confirmed them; it did not invent them.

- EasyEDA Pro is sole schematic+PCB authority (R1-D-066). KiCad is historical.
- Gateway-only actuation; `setDocumentSource` is lossy/destructive.
- Via CREATE persists, modify does not (SESSION-CANON-2026-09-07-VIA-PERSIST).
- Never `openProject` onto FABLE.
- NFC does not exist on this board.
- Six 4-pin WS2812E-1313 are intentional.
- WIDTH 40.0 mm, FPC 10P, dual VH retired.
- USB hub belongs **between** S3 and RT.

---

## 11 — Session-start checklist (fail closed)

```text
[ ] Which tree? R1 = evidence. REV2 = live product (after B0).
[ ] Read this file, then REV2 AGENTS.md + docs/DECISIONS.md.
[ ] Placement numbers come from placement_160.json, not from a 175 cut line.
[ ] lsof TCP:9223 LISTEN? If no → canary will FAIL. Do not attach to a non-bridge EasyEDA.
[ ] Current EasyEDA title? If FABLE → do not openProject, do not import over it.
[ ] txn status open? If yes → you are the second writer. STOP.
[ ] certified_mutating_verbs empty? Then P1/P2 are not a CLI job.
[ ] Is easyeda/K1-CORE-VAL-REV2.epro2 present with a SHA in bootstrap/source-integrity.json?
    NO → you are at B0, not P1.
[ ] Self-test battery: can it still go RED on cut-line and naive-translate?
```

---

## 12 — Evidence index (do not re-derive)

| What | Path |
|---|---|
| 160_PASS gate | `reference/placement-160/00-GATE.md` (this repo) |
| Coordinate map | `reference/placement-160/placement_160.json` |
| Self-test | `reference/placement-160/selftest.json` |
| Polar USB | `reference/usb-impedance/jlc06161h-3313e-polar-2026-09-07.json` |
| B0 blocked receipt | `evidence/checkpoints/2026-09-07-B0-BLOCKED/README.md` |
| Donor SHA | `f9f33f0f7cbfc184ccb7b78e87e0840aae9ab5f74d672bbd09df8a3249dd9ebe` |
| Evaluation lane (R1, historical) | `K1-CORE-VAL-R1/research/lanes/DOWNSTREAM-PCB-EVAL-2026-09-07/` |
| Cut-line files (withdrawn) | R1 `10–12-placement-candidate-16x.json`, `13-placement-comparison.md` |
| Gateway capability | R1 `tools/easyeda/policies/capability-status.json` |
| Importer stall | R1 `docs/agent/SESSION-CANON-2026-09-05-GATEWAY-CONCURRENCY-AND-IMPORTER.md` |
| Via persist | R1 `docs/agent/SESSION-CANON-2026-09-07-VIA-PERSIST-AND-GATEWAY.md` |

---

## 13 — Cost we are not paying again

| Waste | How it will try to return | Refuse with |
|---|---|---|
| Freeze 175 because HMI falls off a chopped outline | “160 doesn’t fit” screenshot of east edge | Rule 1 |
| Delete RGB4/5/6 to make 160 | “HMI too wide” | Rule 3 |
| Translate IRQ1 with S3 | “all S3-* are MACRO” | Rule 4 |
| Move the buck west of the antenna | “need RF clearance” | Rule 5 |
| Split L2/L5 for LED | “keep 4 A out of GND” | Rule 6 |
| `cp` donor to `easyeda/K1-CORE-VAL-REV2.epro2` and start P1 | “folder is ready” | Rule 7 |
| Playwright/CDP on Captain’s EasyEDA | “canary failed, I’ll attach anyway” | Rule 8 |
| `setDocumentSource` to move 174 parts | “gateway has no move verb” | Rule 9 |
| All-green placement score with no red controls | “self-test passed” | Rule 10 |
| Swap TPS62913 → 62912 | “footprint name mismatch” | Rule 11 |

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Canon from placement close-out + REV2 bootstrap session. |
