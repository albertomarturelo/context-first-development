#!/usr/bin/env python3
"""Tests for templates/.agents/skills/telemetry-report/scripts/telemetry.py.

Every adapter is exercised on SYNTHETIC fixtures under scripts/tests/fixtures/
(no real transcript, identity, path or figure). The fixtures carry {PROJECT} and
{OTHER} placeholders that the harness replaces with temporary directories, and
the adapters find them through the environment knobs they already honour
(CLAUDE_CONFIG_DIR, CODEX_HOME, COPILOT_HOME, HOME).

Run: python3 -m unittest discover -s scripts/tests   (scripts/validate-catalog.sh does)
"""

import collections
import importlib.util
import io
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")
SCRIPT = os.path.join(HERE, "..", "..", "templates", ".agents", "skills", "telemetry-report",
                      "scripts", "telemetry.py")
SCRIPT = os.path.normpath(SCRIPT)


def load_module():
    spec = importlib.util.spec_from_file_location("telemetry", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


telemetry = load_module()


class Sandbox:
    """A temporary HOME with one project, one sibling project and the agents'
    log folders, filled from fixtures with the placeholders substituted."""

    def __init__(self):
        self.root = os.path.realpath(tempfile.mkdtemp(prefix="cfd-telemetry-test-"))
        self.home = os.path.join(self.root, "home")
        self.project = os.path.join(self.root, "work", "project")
        self.other = os.path.join(self.root, "work", "project-new")   # a sibling with the same prefix
        for path in (self.home, self.project, self.other):
            os.makedirs(path)
        self.claude = os.path.join(self.home, ".claude")
        self.codex = os.path.join(self.home, ".codex")
        self.copilot = os.path.join(self.home, ".copilot")
        self.env = {
            "HOME": self.home, "CLAUDE_CONFIG_DIR": self.claude, "CODEX_HOME": self.codex,
            "COPILOT_HOME": self.copilot, "COPILOT_OTEL_FILE_EXPORTER_PATH": "", "APPDATA": "",
        }

    def fill(self, text):
        return text.replace("{PROJECT}", self.project).replace("{OTHER}", self.other)

    def copy(self, fixture, dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(os.path.join(FIXTURES, fixture), encoding="utf-8") as fh:
            body = self.fill(fh.read())
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(body)
        return dest

    def install_claude(self):
        slug = re.sub(r"[^A-Za-z0-9]", "-", self.project)
        folder = os.path.join(self.claude, "projects", slug)
        self.copy("claude/project/session-aaaa0001.jsonl", os.path.join(folder, "session-aaaa0001.jsonl"))
        self.copy("claude/project/sub-agent-0001/sub-agent-0001.jsonl",
                  os.path.join(folder, "session-aaaa0001", "sub-agent-0001.jsonl"))
        sibling = re.sub(r"[^A-Za-z0-9]", "-", self.other)
        self.copy("claude/sibling/session-bbbb0002.jsonl",
                  os.path.join(self.claude, "projects", sibling, "session-bbbb0002.jsonl"))

    def install_codex(self):
        day = os.path.join(self.codex, "sessions", "2026", "03", "03")
        for name in ("rollout-project", "rollout-other", "rollout-unknown"):
            self.copy("codex/%s.jsonl" % name, os.path.join(day, name + ".jsonl"))

    def install_copilot_cli(self, sql=None):
        """Build session-store.db from the SQL fixture, or from `sql` when given."""
        os.makedirs(self.copilot, exist_ok=True)
        if sql is None:
            with open(os.path.join(FIXTURES, "copilot-cli", "session-store.sql"), encoding="utf-8") as fh:
                sql = fh.read()
        db = sqlite3.connect(os.path.join(self.copilot, "session-store.db"))
        db.executescript(self.fill(sql))
        db.commit()
        db.close()

    def vscode_outfile(self, export):
        """Point the VS Code `outfile` user setting at `export` (JSONC on purpose)."""
        settings = os.path.join(self.home, "Library", "Application Support", "Code", "User", "settings.json")
        os.makedirs(os.path.dirname(settings), exist_ok=True)
        with open(settings, "w", encoding="utf-8") as fh:
            fh.write('{\n  // a JSONC file: comments and trailing commas are legal here\n'
                     '  "github.copilot.chat.otel.exporterType": "file",\n'
                     '  "github.copilot.chat.otel.outfile": %s,\n}\n' % json.dumps(export))

    def apply_env(self):
        self.saved = {k: os.environ.get(k) for k in self.env}
        os.environ.update(self.env)

    def restore_env(self):
        for k, v in self.saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


class AdapterCase(unittest.TestCase):
    def setUp(self):
        self.box = Sandbox()
        self.box.apply_env()
        self.health = collections.Counter()
        self.addCleanup(self.box.cleanup)
        self.addCleanup(self.box.restore_env)

    def summarize(self, sessions):
        return telemetry.summarize(sessions)


class ClaudeAdapter(AdapterCase):
    def test_reads_one_session_and_skips_the_sibling_project(self):
        self.box.install_claude()
        sessions = telemetry.read_claude(self.box.project, self.health)
        self.assertEqual([s.sid for s in sessions], ["session-aaaa0001"])
        rec = self.summarize(sessions)["claude:session-aaaa0001"]
        row = rec["row"]
        self.assertEqual(row["a"], "claude")
        self.assertEqual(row["n"], 4)            # r1 (two lines, one request), r2, r4, and the subagent's
        self.assertEqual(row["sub"], 1)
        self.assertEqual(row["turns"], 2)        # tool results and the subagent's prompt are not turns
        self.assertEqual(row["o"], 60 + 40 + 20 + 70)   # the repeated r1 line keeps the larger count
        self.assertEqual(row["f"], (100 + 200) + 30 + 10 + 500)
        self.assertEqual(row["r"], 1000 + 1300 + 1330)
        self.assertEqual(row["models"], ["model-a"])
        self.assertEqual(row["branches"], ["feat/demo-12"])
        self.assertEqual(row["ctx0"], 100 + 1000 + 200)
        self.assertEqual(row["orient"], 60 + 100 + 200)  # only r1 came before the Edit in r2
        self.assertEqual(row["d"], "2026-03-02")
        self.assertEqual([r["k"] for r in rec["runs"]], ["session-start"])
        self.assertEqual(self.health["claude_files"], 2)
        self.assertEqual(self.health["claude_bad_lines"], 0)   # the junk line has no "assistant"/"user" marker
        self.assertEqual(self.health["claude_dup_lines"], 1)
        self.assertEqual(self.health["claude_no_usage"], 1)

    def test_no_config_dir_reads_nothing(self):
        self.assertEqual(telemetry.read_claude(self.box.project, self.health), [])
        self.assertEqual(sum(self.health.values()), 0)


class CodexAdapter(AdapterCase):
    def test_reads_the_project_rollout_only(self):
        self.box.install_codex()
        sessions = telemetry.read_codex(self.box.project, self.health)
        self.assertEqual([s.sid for s in sessions], ["codex-session-0001"])
        row = self.summarize(sessions)["codex:codex-session-0001"]["row"]
        self.assertEqual(row["n"], 2)                    # the repeated total is a refresh, not a request
        self.assertEqual(row["turns"], 1)
        self.assertEqual(row["o"], 300 + 100)
        self.assertEqual(row["f"], (1200 - 900) + (1400 - 1300))
        self.assertEqual(row["r"], 900 + 1300)
        self.assertEqual(row["branches"], ["fix/demo-34"])
        self.assertEqual(row["models"], ["model-b"])
        self.assertEqual(row["orient"], 300 + 300)       # one request before apply_patch
        self.assertEqual(self.health["codex_files"], 1)
        self.assertEqual(self.health["codex_unknown_files"], 1)
        self.assertEqual(self.health["codex_bad_lines"], 0)

    def test_no_sessions_dir_reads_nothing(self):
        self.assertEqual(telemetry.read_codex(self.box.project, self.health), [])


class CopilotAdapter(AdapterCase):
    def test_no_export_on_this_machine(self):
        sessions = telemetry.read_copilot(self.box.project, self.health)
        self.assertEqual(sessions, [])
        self.assertEqual(self.health["copilot_source_missing"], 1)
        self.assertEqual(self.health["copilot_scanned"], 0)

    def test_outfile_setting_is_found_in_vscode_user_settings(self):
        export = os.path.join(self.box.root, "otel", "copilot.jsonl")
        self.box.vscode_outfile(export)
        self.assertEqual(telemetry.copilot_export_path(), export)

    def test_export_found_is_reported_as_unread_not_as_zero(self):
        export = os.path.join(self.box.root, "otel", "copilot.jsonl")
        os.makedirs(os.path.dirname(export))
        with open(export, "w", encoding="utf-8") as fh:
            fh.write('{"name":"chat"}\n')
        self.box.vscode_outfile(export)
        self.assertEqual(telemetry.read_copilot(self.box.project, self.health), [])
        self.assertEqual(self.health["copilot_unparsed"], 1)
        self.assertEqual(self.health["copilot_source_missing"], 0)

    def test_shared_env_var_is_not_attributed_to_vscode(self):
        # Copilot CLI honours the same variable: a path there may be the CLI's export.
        export = os.path.join(self.box.root, "otel", "cli.jsonl")
        os.makedirs(os.path.dirname(export))
        open(export, "w").close()
        os.environ["COPILOT_OTEL_FILE_EXPORTER_PATH"] = export
        self.assertIsNone(telemetry.copilot_export_path())
        self.assertEqual(telemetry.read_copilot(self.box.project, self.health), [])
        self.assertEqual(self.health["copilot_source_missing"], 1)


class CopilotCliAdapter(AdapterCase):
    def test_reads_the_project_session_from_the_usage_table(self):
        self.box.install_copilot_cli()
        sessions = telemetry.read_copilot_cli(self.box.project, self.health)
        self.assertEqual([s.sid for s in sessions], ["cli-session-0001"])
        row = self.summarize(sessions)["copilot-cli:cli-session-0001"]["row"]
        self.assertEqual(row["a"], "copilot-cli")
        self.assertEqual(row["n"], 4)                    # rows 5 and 6 are unreadable
        self.assertEqual(row["sub"], 1)
        self.assertEqual(row["turns"], 2)                # distinct main-agent turn indexes
        self.assertEqual(row["o"], 100 + 50 + 30 + 80)   # output already includes reasoning
        self.assertEqual(row["f"], (200 + 300) + (100 + 200) + (500 + 0) + (50 + 50))
        self.assertEqual(row["r"], 1000 + 1500 + 100 + 1900)
        self.assertEqual(row["ctx0"], 1500)              # input_tokens is the whole context
        self.assertEqual(row["ctxmax"], 2000)            # main agent only
        self.assertEqual(row["orient"], (100 + 200 + 300) + (50 + 100 + 200))   # before the apply_patch
        self.assertEqual(row["models"], ["model-c"])
        self.assertEqual(row["branches"], ["feat/demo-56"])
        self.assertEqual(self.health["copilot_cli_scanned"], 2)
        self.assertEqual(self.health["copilot_cli_no_usage"], 1)
        self.assertEqual(self.health["copilot_cli_bad_rows"], 1)

    def test_store_with_sessions_of_other_projects_only(self):
        self.box.install_copilot_cli()
        elsewhere = os.path.join(self.box.root, "work", "elsewhere")
        self.assertEqual(telemetry.read_copilot_cli(elsewhere, self.health), [])
        self.assertEqual(self.health["copilot_cli_scanned"], 2)
        self.assertEqual(self.health["copilot_cli_source_missing"], 0)

    def test_no_store_on_this_machine(self):
        self.assertEqual(telemetry.read_copilot_cli(self.box.project, self.health), [])
        self.assertEqual(self.health["copilot_cli_source_missing"], 1)

    def test_store_from_a_version_without_usage(self):
        self.box.install_copilot_cli(
            "CREATE TABLE sessions (id TEXT, cwd TEXT, branch TEXT);"
            "INSERT INTO sessions VALUES ('old-0001', '{PROJECT}', 'main');")
        self.assertEqual(telemetry.read_copilot_cli(self.box.project, self.health), [])
        self.assertEqual(self.health["copilot_cli_no_usage_table"], 1)
        self.assertEqual(self.health["copilot_cli_scanned"], 1)

    def test_damaged_store_is_reported_not_raised(self):
        os.makedirs(self.box.copilot)
        with open(os.path.join(self.box.copilot, "session-store.db"), "w") as fh:
            fh.write("not a database")
        self.assertEqual(telemetry.read_copilot_cli(self.box.project, self.health), [])
        self.assertEqual(self.health["copilot_cli_unreadable"], 1)


class EndToEnd(AdapterCase):
    def run_script(self, *args):
        out = os.path.join(self.box.root, "out", "index.html")
        done = subprocess.run([sys.executable, SCRIPT, self.box.project, "--out", out] + list(args),
                              capture_output=True, text=True, env=dict(os.environ))
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout, out

    def test_summary_and_dashboard(self):
        self.box.install_claude()
        self.box.install_codex()
        stdout, out = self.run_script()
        self.assertRegex(stdout, r"claude\s+1 sessions\s+4 requests")
        self.assertRegex(stdout, r"codex\s+1 sessions\s+2 requests")
        self.assertRegex(stdout, r"copilot-cli\s+no session store on this machine")
        self.assertRegex(stdout, r"copilot\s+no OpenTelemetry file export on this machine")
        self.assertIn("note  claude_dup_lines", stdout)
        self.assertNotIn("copilot_source_missing", stdout)   # said on the copilot line, not as a gap
        with open(out, encoding="utf-8") as fh:
            html = fh.read()
        data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S).group(1))
        self.assertEqual(data["agents"], ["claude", "codex"])
        self.assertEqual(len(data["sessions"]), 2)
        self.assertEqual(data["health"]["copilot_source_missing"], 1)
        history = os.path.join(os.path.dirname(out), "index.history.json")
        with open(history, encoding="utf-8") as fh:
            self.assertEqual(sorted(json.load(fh)["sessions"]), ["claude:session-aaaa0001", "codex:codex-session-0001"])

    def test_empty_machine(self):
        stdout, _ = self.run_script()
        self.assertRegex(stdout, r"claude\s+0 sessions")
        self.assertRegex(stdout, r"copilot\s+no OpenTelemetry file export on this machine")

    def test_export_present_prints_the_unread_line_and_a_note(self):
        export = os.path.join(self.box.root, "otel", "copilot.jsonl")
        os.makedirs(os.path.dirname(export))
        open(export, "w").close()
        self.box.vscode_outfile(export)
        stdout, _ = self.run_script()
        self.assertRegex(stdout, r"copilot\s+export found, but this version does not read it yet")
        self.assertIn("note  copilot_unparsed", stdout)

    def test_copilot_cli_session_and_no_private_text(self):
        self.box.install_copilot_cli()
        stdout, out = self.run_script()
        self.assertRegex(stdout, r"copilot-cli\s+1 sessions\s+4 requests")
        self.assertIn("note  copilot_cli_bad_rows", stdout)
        self.assertIn("note  copilot_cli_no_usage", stdout)
        history = os.path.join(os.path.dirname(out), "index.history.json")
        for path in (out, history):
            with open(path, encoding="utf-8") as fh:
                body = fh.read()
            self.assertNotIn("SECRET", body)          # prompts, responses, summaries, file paths
        with open(out, encoding="utf-8") as fh:
            data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>',
                                        fh.read(), re.S).group(1))
        self.assertEqual(data["agents"], ["copilot-cli"])
        self.assertEqual(data["sessions"][0]["a"], "copilot-cli")


if __name__ == "__main__":
    unittest.main()
