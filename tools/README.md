---
abstract: "REV2 does not fork the EasyEDA gateway. Actuation is the R1 tools/easyeda/easyeda-run binary. Evidence for REV2 work is copied into this repo's evidence/."
---

# tools/

This project does **not** carry a second EasyEDA automation stack.

Use:

```text
/Users/spectrasynq/Workspace_Management/Software/K1-CORE-VAL-R1/tools/easyeda/easyeda-run
```

Policy: R1 `docs/easyeda/EASYEDA-AGENT-POLICY.md`.

After each REV2 gateway run, copy `run.json` (and screenshots) into:

```text
evidence/easyeda-gateway/<run-id>/
```

Do not attach CDP/MCP/Playwright to EasyEDA except through that binary.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Point at R1 gateway; no fork. |
