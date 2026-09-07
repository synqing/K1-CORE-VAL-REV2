---
abstract: "REV2 changelog. B0 still blocked: CDP now healthy; one GUI import-test stalled (IMPORTER_STALL). No live REV2 project."
---

# 08 — Changelog

| Date | Change |
|---|---|
| 2026-09-07 | Folder created. Curated 22 hashed references. Contracts written. Donor archive copied read-only. |
| 2026-09-07 | Gate B0 **BLOCKED**: EasyEDA Pro running without CDP `:9223`; `easyeda-run canary` → `FAIL fetch failed`. Donor not mutated. |
| 2026-09-07 | Canon: `docs/SESSION-CANON-2026-09-07-CUTLINE-IS-NOT-PLACEMENT.md`. Wired from AGENTS.md / README. |
| 2026-09-07 | Canon extended: EasyEDA surface pitfalls, lying maps, FABLE-R1≠R3, leftover PCB2. |
| 2026-09-07 | CDP/canary recovered (`:9223` PASS, CLI/daemon/connector v1.3.0). One GUI `import-test --via gui` of the immutable donor as **NEW PROJECT** `K1-CORE-VAL-REV2`. Gate A `PASS_WITH_WARNINGS`. Gate B **FAIL**: dialog 1 stuck on **Importing**, bar **75 %**, 90 s, no dialog 2, `project_uuid=null`. Trap `FC-CDP-PAUSE-STORM-001` + `Cannot close a CLOSED writable stream`. Modal dismissed. FABLE UUID unchanged. Donor SHA unchanged. No second import. Evidence: `evidence/bootstrap/import-stall-20260907T141043Z/`. |
| — | Live project, canonical epro2, P1, P2: not started. |

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Bootstrap log. |
| 2026-09-07 | agent:grok | B0 IMPORTER_STALL after one GUI import-test. |
