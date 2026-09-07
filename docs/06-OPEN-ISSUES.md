---
abstract: "Open REV2 issues: B0 blocked (no EasyEDA CDP), importer stall history, uncertified mutations, KH-FG A/pin missing, PAD_NET empty, HMI auto-nets, TPS62913 alias, planes_160 unreconciled."
---

# 06 — Open issues

| ID | Issue | Blocks |
|---|---|---|
| REV2-G-001 | EasyEDA canary `FAIL` / `fetch failed`. Process running **without** `--remote-debugging-port=9223`. | B0, P1, P2 |
| REV2-G-002 | Historical importer stall at “Importing 50 %” (2026-09-05 canon R6). Discriminators not all run. | B0 import-test |
| REV2-G-003 | `certified_mutating_verbs = []`. Outline verbs automation-banned. Broader product copper uncertified. | P1, P2 via gateway |
| REV2-P-001 | `KH-FG1.0-H2.0-10PIN` drawing has no A/pin. Sibling QCHF 0.5 A/PIN is a different MPN. | product power, not length |
| REV2-D-001 | PCB1 `PAD_NET` bodies empty. Connectivity ≠ padNet census. | naive ERC |
| REV2-D-002 | HMI data nets `$1N3583` / `$1N3585` unnamed. Rename in a later implementation txn, not B0. | hygiene |
| REV2-D-003 | PWR-BUCK1 identity TPS62913 vs footprint name TPS62912. Alias. | “helpful” part swaps |
| REV2-P-002 | `planes_160.json` area estimate unreconciled. REFERENCE_ONLY. | P2 polygon inject |
| REV2-M-001 | Enclosure absolute hole freeze not found; east holes treated edge-relative. | mechanical if enclosure later freezes X |

Do not “solve” these by mutating the donor.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Initial open-issue register. |
