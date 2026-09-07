---
abstract: "Every tool that can touch EasyEDA in REV2: what it is, when to use it, when NOT to, its known faults, and how to recover. Read before induction — the exam draws on this file and on the canons it points to."
---

# TOOLCHAIN — what may touch EasyEDA, and how

Abbreviations, once: **CDP** = Chrome DevTools Protocol (the debug channel an
Electron app exposes on a TCP port). **DRC** = Design Rule Check. **DSN** = the
Specctra design file EasyEDA exports for external routers. **SES** = the Specctra
session file a router returns. **MCP** = Model Context Protocol.

There are five things that can reach EasyEDA. Only one of them may write.

| | may write? | reaches EasyEDA via |
|---|---|---|
| `easyeda-run` (the gateway) | **YES — the only one** | CDP drivers + the agent daemon |
| `easyeda` CLI / daemon / connector | reads, and gateway-mediated writes | TCP 60832 → connector extension |
| EasyEDA MCP Bridge | **no** | WebSocket 19732 / HTTP 19733 |
| EasyEDA Pro API (in-page) | **no** | CDP 9223, in-page `eda.*` |
| Freerouting | **no** — files only | reads a `.dsn`, writes a `.ses` |

---

## 1. `easyeda-run` — the gateway. The only actuation path.

```
/Users/spectrasynq/Workspace_Management/Software/K1-CORE-VAL-R1/tools/easyeda/easyeda-run
```

Everything that mutates a live board goes through it, because it is the only path
that produces a receipt: `evidence/easyeda-gateway/<run>/run.json`. A flag is not
evidence; a receipt is.

**Use it for:** `download` (server archive checkpoint), `canary` (liveness),
`knowledge` (query the failure corpus), `txn` (controlled-write transaction),
`agent` (typed action), `outline-oracle`.

**Do not:** attach CDP, MCP, Playwright, AppleScript or computer-use to EasyEDA
outside it. Do not edit `.epro2` / `.epru` directly, except
`repair --emergency` **on a copy**.

**If the gateway cannot do what you need: STOP and report.** Do not build a second
path. Every second path in this project's history became an incident.

**Known faults:**
- `download` prints `null`, exits **0**, and writes nothing when CDP is down.
  Exit status is not a success signal for this command — check the file exists.
  (`FC-GW-DOWNLOAD-NULL-RC0-001`)
- `import-test` is permanently REFUSED, exit 3 `IMPORTER_STALL_KNOWN`. It stalls at
  50/67/75 % forever and `--into` injects `Board1_1` / `PCB1_1` siblings.
- Uncertified mutating verbs are DENIED. `certified_mutating_verbs` is currently
  **empty** — that is deliberate, not a bug to route around.
- `txn close` takes **no** `--session` flag. The flag form leaves the writer lease
  held and the next batch aborts with "no session".

---

## 2. `easyeda` CLI / daemon / connector — reads and typed actions

Local daemon on **TCP 60832**, talking to the connector extension inside EasyEDA
Pro. Independent of CDP: it keeps working when CDP is dead, which is exactly what
makes a half-broken session look healthy.

**Use it for:** `daemon health`, `doc ls`, `project info`, `call pcb.*.list`,
`call pcb.drc.check`, `call document.current`.

**Verb names that have cost time:**

| wrong | right |
|---|---|
| `pcb.component.list` | `pcb.components.list` |
| `kind=line` (track deletion) | `kind=track` |

**`doc reload` is the single most dangerous command in this toolchain.** It is
save → close → reopen, and the save is unconditional. Against an unhydrated editor
it writes the empty document over the board. Its reopen leg can fail on its own,
which *leaves* the editor unhydrated and arms the trap for the next reload.
The live-surface guard gates it. Do not talk your way past it.

**Reads can lie by omission.** An unhydrated editor answers `ok=true` with an empty
array and no error. `doc ls`, `document.current`, `doc open` and
`--force-stale-read` all fail to discriminate. Only an object count does.

---

## 3. EasyEDA MCP Bridge — read/diagnose, never the write path in REV2

HTTP **19733**, WebSocket **19732**, watchdog log
`~/Library/Logs/easyeda-bridge-watchdog.log`.

**Its most valuable output is that log.** It states the correct fix every 30 s. Read
it *first* whenever anything CDP-shaped misbehaves, before forming any theory.

**Recovery tool:**

```bash
node ~/SpectraSynq-EDA/EasyEDA-MCP/tools/easyeda_reconnect.mjs      # NO --gentle
```

`--gentle` refuses to relaunch and only reports. When the GUI is dead, frozen, or
running without CDP, the no-`--gentle` form is the correct call. The first heal
often reports `sandbox-missing` — **wait and retry; do not kill the new app.**

**Never** `open -a EasyEDA-Pro`. It strips `--remote-debugging-port=9223` and the
anti-throttle flags, after which every CDP driver dies with `ECONNREFUSED` while
the CLI keeps answering normally. The guard blocks this for every agent.

---

## 4. EasyEDA Pro API (`eda.*`) — understanding, not actuation

Reached in-page over CDP 9223. Skill `easyeda-api` carries the reference.

**Read it to understand what the gateway is doing. Do not drive the board with it.**

**The property that makes it dangerous:** *the host never throws.* Rejection is
`undefined` (create / modify) or `false` (delete / rename / save / import). A
handler that returns instead of raising reports a phantom write as a success. So an
API "success" is never evidence — only a readback is.

Two more, measured:
- Default `getGerberFile()` layer set **omits inner copper**. Always pass an
  explicit layers array or the fab package is silently 2-layer.
- Via **create** persists; via **modify** does not.

---

## 5. Freerouting — a file-in, file-out router. It never touches the board.

Reads a `.dsn`, writes a `.ses`. Nothing it does reaches EasyEDA until a human or
the gateway imports the result — and **SES import MERGES rather than replaces**,
which is its own trap.

**The ceiling you will hit, and the reason:** EasyEDA's DSN export marks *every*
wire and via `(type protect)`. Freerouting treats protected copper as user-fixed
and will neither rip it up nor shove it. Measured on FABLE-R9: **1248 of 1248**
objects protected, `(type route)` 0, `(type fix)` 0.

So the router stops improving after a few nets. That plateau is **not** a resource
limit, and throwing cores at it cannot help:
- `-mt` sizes the **optimisation** pool only; autorouting is single-threaded
  (measured 100.1 % CPU at `-mt 6`)
- disabling fanout (`FREEROUTING__ROUTER__FANOUT__ENABLED=false`) took one pass from
  27 minutes to 5 seconds — a settings win, not a throughput win

**The control is selective unprotection:** strip `(type protect)` from the
authorised target nets only, leave every other object protected, and audit that the
count of unprotected non-target objects is exactly zero before routing.

**Log every byte.** All router output is archived per run — command, console log,
inputs, artefact, manifest, stages. A zero-byte artefact must fail loudly rather
than pass quietly. Captain's standing mandate: *this is to prevent any loss of any
work, ever.*

**Two DSN dialects** exist and any parser must handle both:
EasyEDA writes `(wire(path L W x y …))`;
Freerouting writes `(wire (polyline_path L W x1 y1 x2 y2 …))` — segment pairs, not
a continuous polyline.

---

## 6. Schematic work

Skill `create-schematic` carries the netlist-first, measure-first, batch-first
method. The trap it exists to prevent: EasyEDA **collinear-merges** wire stubs, and
a merge silently absorbs one net into another — GND pin count has gone 100 → 0 with
364 pins landing on `+3V3`, reported by the tool as success
(`OBS-GND-3V3-COLLAPSE-001`).

Verify connectivity against the EDA's own netlist export, never against a counter
returned by the tool that did the writing, and never against canvas colour.

---

## 7. The preflight gate — run it, always

```bash
tools/easyeda/preflight.sh <project-uuid> [doc-uuid] [--min-components N] [--expect-pours N]
```

Before the first read of a session, before every mutation batch, and after every
application restart.

| exit | meaning |
|---|---|
| 0 | FIT — read and write |
| 10 | UNHYDRATED — editor holds no board; **do not `doc reload`** |
| 11 | NO-CDP — the archive download and every CDP driver will fail silently |
| 12 | NO-WINDOW — none, or more than one (two windows = two autosave writers) |
| 13 | WRONG-DOC — connector bound to a different document |
| 14 | POUR-DRIFT — a plane has appeared or vanished |
| 15 | DRC-FAIL — the check did not answer; **a failed check is not a clean board** |

---

## 8. Recovery — the one procedure worth memorising

An editor that reads zero objects:

1. **Do not `doc reload`. Do not quit gracefully.** Both can flush a save.
2. `easyeda-run download` — prove the server copy is intact, and census it.
3. `pkill -9 -f EasyEDA-Pro` — SIGKILL cannot flush a save. That is why it is safer.
4. `node ~/SpectraSynq-EDA/EasyEDA-MCP/tools/easyeda_reconnect.mjs` (no `--gentle`).
5. Reopen the **project** from the start page — a document cannot open until its
   project is loaded — then `easyeda doc open <doc-uuid> --project <project-uuid>`.
6. Verify hydration by object count before anything else.
7. Re-check CDP. Steps 3–4 are where this goes wrong.

---

## 9. Measurement — what counts as evidence

- **Quote the DRC TOTAL, never the group count.** The headline is a number of rule
  *groups*; the total is the sum of their `count` fields. A board reading "4" had 362.
- **Every metric is a fresh readback.** A number derived from a planned diff is not a
  measurement. This produced a reported 280 against an actual 362.
- **A fresh readback beats any status document, including one you wrote.**
- **A checker's docstring is not coverage.** A gate that claims a check it does not
  implement is worse than no gate: it converts an unchecked action into an
  authorised one.
- **Never infer connectivity from canvas colour**, and blank `PAD_NET` bodies do not
  prove disconnection.
