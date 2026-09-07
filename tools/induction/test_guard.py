#!/usr/bin/env python3
"""RED fixtures for the live-surface guard and the induction gate.

A guard nobody tested is a guard that fails open on the day it matters.
Every claim the guard makes is planted here and asserted.

    python3 tools/induction/test_guard.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GUARD = ROOT / ".claude" / "hooks" / "live-surface-guard.py"
INDUCT = ROOT / "tools" / "induction" / "induct.py"


def run_guard(command: str, tool: str = "Bash", env_extra: dict | None = None):
    """Returns (returncode, reason_text). rc 2 == blocked."""
    payload = {"hook_event_name": "PreToolUse", "tool_name": tool,
               "tool_input": {"command": command} if tool == "Bash"
               else {"arg": command}}
    env = dict(os.environ)
    env.pop("K1_INDUCTION_OVERRIDE", None)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload),
                       capture_output=True, text=True, timeout=90, env=env,
                       cwd=str(ROOT))
    reason = ""
    if p.stdout.strip():
        try:
            reason = json.loads(p.stdout)["hookSpecificOutput"]["permissionDecisionReason"]
        except Exception:
            reason = p.stdout
    return p.returncode, reason


class TestProhibited(unittest.TestCase):
    """Blocked for everyone, induction irrelevant."""

    def test_open_dash_a_is_blocked(self):
        rc, why = run_guard('open -a "EasyEDA-Pro"')
        self.assertEqual(rc, 2, why)
        self.assertIn("9223", why)
        self.assertIn("easyeda_reconnect.mjs", why)

    def test_open_dash_a_unquoted_is_blocked(self):
        rc, _ = run_guard("open -a EasyEDA-Pro --args foo")
        self.assertEqual(rc, 2)

    def test_import_test_is_blocked(self):
        rc, why = run_guard("./tools/easyeda/easyeda-run import-test big.epro2 --via gui")
        self.assertEqual(rc, 2, why)
        self.assertIn("IMPORTER_STALL_KNOWN", why)

    def test_set_document_source_is_blocked(self):
        for variant in ("setDocumentSource", "set_document_source"):
            rc, _ = run_guard("easyeda call %s --payload '{}'" % variant)
            self.assertEqual(rc, 2, variant)

    def test_force_true_is_blocked(self):
        rc, _ = run_guard("easyeda-run mutate --force true")
        self.assertEqual(rc, 2)

    def test_override_cannot_lift_a_prohibition(self):
        rc, _ = run_guard('open -a "EasyEDA-Pro"',
                          env_extra={"K1_INDUCTION_OVERRIDE": "emergency"})
        self.assertEqual(rc, 2, "override must NOT lift a prohibition")


class TestGatedWithoutInduction(unittest.TestCase):
    """Blocked while this agent holds no valid token."""

    @classmethod
    def setUpClass(cls):
        if subprocess.run([sys.executable, str(INDUCT), "--verify"],
                          cwd=str(ROOT), capture_output=True).returncode == 0:
            raise unittest.SkipTest("this agent is already inducted; "
                                    "clear .induction/ to run the RED fixtures")

    def test_doc_reload_is_gated(self):
        rc, why = run_guard("easyeda doc reload --project abc")
        self.assertEqual(rc, 2, why)
        self.assertIn("not inducted", why.lower())
        self.assertIn("--exam", why)

    def test_mutating_verb_is_gated(self):
        rc, _ = run_guard("easyeda call pcb.line.create --payload '{}'")
        self.assertEqual(rc, 2)

    def test_pour_delete_is_gated(self):
        rc, _ = run_guard("easyeda call pcb.pour.delete --payload '{}'")
        self.assertEqual(rc, 2)

    def test_easyeda_run_mutate_is_gated(self):
        rc, _ = run_guard("./tools/easyeda/easyeda-run mutate --project x")
        self.assertEqual(rc, 2)

    def test_freerouting_is_gated(self):
        rc, _ = run_guard("java -jar freerouting.jar -de board.dsn")
        self.assertEqual(rc, 2)

    def test_block_reason_teaches_the_way_out(self):
        _, why = run_guard("easyeda doc reload")
        for expected in ("induct.py --exam", "--submit", "33 questions"):
            self.assertIn(expected, why)

    def test_override_permits_a_gated_command_and_is_logged(self):
        log = ROOT / ".induction" / "override.log"
        before = log.read_text() if log.is_file() else ""
        rc, _ = run_guard("easyeda call pcb.line.create --payload '{}'",
                          env_extra={"K1_INDUCTION_OVERRIDE": "unit test"})
        self.assertEqual(rc, 0)
        self.assertTrue(log.is_file(), "override was not logged")
        self.assertIn("unit test", log.read_text()[len(before):])


class TestAlwaysAllowed(unittest.TestCase):
    """The gate must never stop an agent becoming inducted, or diagnosing."""

    def test_induction_itself_is_allowed(self):
        for cmd in ("python3 tools/induction/induct.py --exam",
                    "python3 tools/induction/induct.py --submit answers.json"):
            rc, why = run_guard(cmd)
            self.assertEqual(rc, 0, why)

    def test_reads_and_diagnostics_are_allowed(self):
        for cmd in ("./tools/easyeda/easyeda-run download --project x --out y.epro2",
                    "./tools/easyeda/easyeda-run canary --project x",
                    "bash tools/easyeda/preflight.sh proj doc",
                    "easyeda daemon health",
                    "easyeda doc ls --project x",
                    "git status",
                    "python3 -m unittest discover",
                    "python3 tools/injection_check.py",
                    "cat AGENTS.md",
                    "ls docs/"):
            rc, why = run_guard(cmd)
            self.assertEqual(rc, 0, "%s was blocked: %s" % (cmd, why))

    def test_doc_ls_allowed_but_doc_reload_gated(self):
        """The allow-list must not accidentally whitelist the destroyer."""
        self.assertEqual(run_guard("easyeda doc ls --project x")[0], 0)
        self.assertEqual(run_guard("easyeda doc reload --project x")[0], 2)

    def test_unrelated_work_is_untouched(self):
        for cmd in ("npm test", "ls -la", "grep -r foo .", "python3 script.py"):
            self.assertEqual(run_guard(cmd)[0], 0, cmd)


class TestSessionBinding(unittest.TestCase):
    """A token must not leak across sessions."""

    def test_unknown_session_is_blocked_even_if_the_os_user_holds_a_token(self):
        payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
                   "session_id": "session-that-never-inducted",
                   "tool_input": {"command": "easyeda doc reload --project x"}}
        env = dict(os.environ); env.pop("K1_INDUCTION_OVERRIDE", None)
        p = subprocess.run([sys.executable, str(GUARD)], input=json.dumps(payload),
                           capture_output=True, text=True, timeout=90, env=env,
                           cwd=str(ROOT))
        self.assertEqual(p.returncode, 2,
                         "a session with no token must be blocked regardless of "
                         "any token held by the OS user")

    def test_deny_path_cannot_fail_open(self):
        """A bug while COMPOSING a denial must still deny.

        Found during this gate's own construction: a format-string error in the
        explanation made the guard allow a `doc reload`. Never again.
        """
        import importlib.util
        spec = importlib.util.spec_from_file_location("guard", GUARD)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        m.induction_reason = lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom"))
        txt = m.safe_induction_reason("something", "sess")
        self.assertIn("BLOCKED", txt)
        self.assertIn("--exam", txt)


class TestGuardRobustness(unittest.TestCase):

    def test_malformed_payload_fails_open(self):
        p = subprocess.run([sys.executable, str(GUARD)], input="not json",
                           capture_output=True, text=True, timeout=60, cwd=str(ROOT))
        self.assertEqual(p.returncode, 0, "guard must fail OPEN, never deadlock the tree")

    def test_empty_command_fails_open(self):
        rc, _ = run_guard("")
        self.assertEqual(rc, 0)

    def test_mcp_tool_payloads_are_scanned(self):
        rc, _ = run_guard("open -a EasyEDA-Pro", tool="mcp__remote__device_bash")
        self.assertEqual(rc, 2, "MCP tool payloads must be scanned too")


if __name__ == "__main__":
    unittest.main(verbosity=2)
