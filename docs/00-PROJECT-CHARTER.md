---
abstract: "Why REV2 exists: a new product-generation boundary, not FABLE-R4. 160×40 mm EasyEDA-native. Donor FABLE-R3 is reference only."
---

# 00 — Project charter

`K1-CORE-VAL-REV2` is a **new product-generation boundary**. It is not `R1-FABLE-R4`.

The R1/FABLE tree accumulated recovery identities, KiCad insurance, cut-line 160 studies (later withdrawn), stale NFC-era assumptions, and many `.epro2` snapshots. Encoding that history into another active name would reduce confidence in what is authoritative.

```text
K1-Core-VAL-R1-FABLE-R3     donor / reference only
        │  controlled EasyEDA import
        ▼
K1-CORE-VAL-REV2            live EasyEDA authority after Gate B0
```

## Mission

1. Self-contained EasyEDA-native project folder (this tree).
2. A **new** EasyEDA Pro project named exactly `K1-CORE-VAL-REV2`.
3. Prove donor-parity (Gate B0) before any geometry change.
4. Instantiate the accepted `160_PASS` placement (Gate P1).
5. Implement Architecture C power planes (Gate P2).
6. **Stop before unrestricted routing.**

Do not recreate the design from scratch. Do not convert through KiCad. Do not mutate the donor.

## Success test

An agent opening this folder six months later can answer, without R1 archaeology:

what is authoritative · which EasyEDA project to modify · board size · where 160 coordinates came from · stack · what L4 contains · locked decisions · open issues · receipts.

---
**Document Changelog**
| Date | Author | Change |
|---|---|---|
| 2026-09-07 | agent:grok | Charter. |
