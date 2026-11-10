#!/usr/bin/env python3
"""Tests for templates/.agents/skills/telemetry-report/scripts/central.py.

Two SYNTHETIC repositories are built in a temporary directory: invented
developers, invented counters, no real data. One is read as a local clone,
the other through a file:// URL, so both ways of opening a repository run.

Run: python3 -m unittest discover -s scripts/tests   (scripts/validate-catalog.sh does)
"""

import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.normpath(os.path.join(HERE, "..", "..", "templates", ".agents", "skills",
                                       "telemetry-report", "scripts", "central.py"))
TODAY = dt.date.today().isoformat()


def row(sid, agent, day, branch, output):
    return {"id": sid, "a": agent, "start": day, "d": day, "active": 10, "turns": 2, "n": 3, "sub": 0,
            "models": ["model-a"], "branches": [branch], "o": output, "f": 100, "r": 1000,
            "ctx0": 1100, "ctxmax": 1500, "edit_min": None, "orient": None}


def month(repo, dev_id, name, sessions):
    return {"schema": "cfd-telemetry/1", "repo": repo, "month": "2026-03",
            "developer": {"id": dev_id, "name": name, "email": dev_id},
            "sessions": {"%s:%s" % (s["a"], s["id"]): {
                "row": s, "runs": [],
                "buckets": [{"d": s["d"], "b": s["branches"][0], "n": s["n"], "i": 50, "o": s["o"], "r": 1000, "w": 50}]}
                for s in sessions}}


def status(repo, dev_id, name, updated, health=None):
    return {"schema": "cfd-telemetry/1", "repo": repo, "updated": updated, "sessions": 1,
            "developer": {"id": dev_id, "name": name, "email": dev_id}, "health": health or {}}


class TeamView(unittest.TestCase):
    def setUp(self):
        self.root = os.path.realpath(tempfile.mkdtemp(prefix="cfd-central-test-"))
        self.addCleanup(shutil.rmtree, self.root, True)
        empty = os.path.join(self.root, "gitconfig")
        open(empty, "w").close()
        self.env = dict(os.environ, GIT_CONFIG_GLOBAL=empty, GIT_CONFIG_NOSYSTEM="1",
                        GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@example.test",
                        GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@example.test")

    def git(self, path, *args, date=None):
        env = dict(self.env)
        if date:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date + "T12:00:00+00:00"
        subprocess.run(["git", "-C", path] + list(args), check=True, capture_output=True, env=env)

    def make_repo(self, name, reports, change_day):
        """A repository whose main touched CLAUDE.md on change_day, plus a
        cfd-telemetry branch holding `reports` ({path: object or raw text})."""
        path = os.path.join(self.root, name)
        os.makedirs(path)
        self.git(path, "init", "-q", "-b", "main")
        with open(os.path.join(path, "CLAUDE.md"), "w") as fh:
            fh.write("# index\n")
        self.git(path, "add", "CLAUDE.md")
        self.git(path, "commit", "-q", "-m", "docs: context index", date=change_day)
        self.git(path, "checkout", "-q", "--orphan", "cfd-telemetry")
        self.git(path, "rm", "-q", "-rf", ".")
        for rel, body in reports.items():
            os.makedirs(os.path.join(path, os.path.dirname(rel)), exist_ok=True)
            with open(os.path.join(path, rel), "w") as fh:
                fh.write(body if isinstance(body, str) else json.dumps(body))
        self.git(path, "add", "reports")
        self.git(path, "commit", "-q", "-m", "telemetry")
        self.git(path, "checkout", "-q", "main")
        return path

    def run_central(self, *repos):
        out = os.path.join(self.root, "out", "index.html")
        done = subprocess.run([sys.executable, SCRIPT, "--out", out] + list(repos),
                              capture_output=True, text=True, env=self.env, cwd=self.root)
        self.assertEqual(done.returncode, 0, done.stderr)
        with open(out, encoding="utf-8") as fh:
            html = fh.read()
        data = json.loads(re.search(r'<script id="data" type="application/json">(.*?)</script>', html, re.S).group(1))
        return done.stdout, data

    def test_two_repositories_two_contributors(self):
        alpha, beta = "example.test/team/alpha", "example.test/team/beta"
        a = self.make_repo("alpha", {
            "reports/bo@example.test/2026-03.json": month(alpha, "bo@example.test", "Bo",
                                                          [row("s-bo-1", "codex", "2026-03-05", "feat/7-login", 900)]),
            "reports/bo@example.test/status.json": status(alpha, "bo@example.test", "Bo", "2026-01-01"),
            "reports/ana@example.test/2026-03.json": month(alpha, "ana@example.test", "Ana",
                                                           [row("s-ana-1", "claude", "2026-03-02", "feat/7-login", 400)]),
            "reports/ana@example.test/status.json": status(alpha, "ana@example.test", "Ana", TODAY,
                                                           {"claude_dup_lines": 3, "claude_files": 9}),
            "reports/zed@example.test/2026-03.json": "{not json",
            "reports/yan@example.test/2026-03.json": dict(month(alpha, "yan@example.test", "Yan", []),
                                                          schema="cfd-telemetry/2"),
        }, "2026-03-04")
        b = self.make_repo("beta", {
            "reports/ana@example.test/2026-03.json": month(beta, "ana@example.test", "Ana",
                                                           [row("s-ana-2", "copilot-cli", "2026-03-06", "feat/7-login", 200)]),
            "reports/ana@example.test/status.json": status(beta, "ana@example.test", "Ana", TODAY),
        }, "2026-03-05")
        stdout, data = self.run_central(a, "file://" + b, os.path.join(self.root, "missing"))

        self.assertEqual(data["mode"], "team")
        self.assertEqual(data["repos"], [alpha, beta])
        self.assertEqual([p["label"] for p in data["people"]], ["Ana", "Bo"])     # alphabetical, never by usage
        self.assertEqual(sorted((s["repo"], s["dev"], s["id"]) for s in data["sessions"]),
                         [(alpha, "ana@example.test", "s-ana-1"), (alpha, "bo@example.test", "s-bo-1"),
                          (beta, "ana@example.test", "s-ana-2")])
        self.assertTrue(all("dev" in b and "repo" in b for b in data["buckets"]))
        self.assertEqual(data["agents"], ["claude", "codex", "copilot-cli"])
        stale = {(r["repo"], r["label"]): r["stale"] for r in data["reporting"]}
        self.assertEqual(stale, {(alpha, "Ana"): False, (alpha, "Bo"): True, (beta, "Ana"): False})
        self.assertEqual([r["gaps"] for r in data["reporting"] if r["label"] == "Ana" and r["repo"] == alpha],
                         [["claude_dup_lines"]])                                  # counts of files read are not gaps
        self.assertEqual(sorted((c["repo"], c["d"]) for c in data["changes"]),
                         [(alpha, "2026-03-04"), (beta, "2026-03-05")])
        h = data["health"]
        self.assertEqual((h["repos_read"], h["repos_unreachable"]), (2, 1))
        self.assertEqual((h["unreadable_files"], h["unknown_schema_files"]), (1, 1))
        self.assertIn("Contributors  2, 1 not reporting", stdout)

        # A second run fetches into the cached clone instead of cloning again.
        _, again = self.run_central("file://" + b)
        self.assertEqual(again["health"].get("repos_fetch_failed", 0), 0)
        self.assertEqual([s["id"] for s in again["sessions"]], ["s-ana-2"])

    def test_repository_without_a_telemetry_branch(self):
        path = os.path.join(self.root, "plain")
        os.makedirs(path)
        self.git(path, "init", "-q", "-b", "main")
        _, data = self.run_central(path)
        self.assertEqual(data["health"]["repos_without_branch"], 1)
        self.assertEqual(data["sessions"], [])

    def test_no_repository_named(self):
        done = subprocess.run([sys.executable, SCRIPT], capture_output=True, text=True, env=self.env, cwd=self.root)
        self.assertNotEqual(done.returncode, 0)


if __name__ == "__main__":
    unittest.main()
