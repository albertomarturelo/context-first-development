#!/usr/bin/env python3
"""Build the telemetry-report screenshots as PNG, one light and one dark each.

Renders the real dashboard template
(templates/.agents/skills/telemetry-report/scripts/dashboard.html) over a
deterministic SAMPLE dataset: a fictional project, fictional people, no
one's real usage. The page title says so, so a screenshot never passes for
evidence. Edit this file, then run:

    python3 scripts/build-telemetry-screenshots.py

Needs Google Chrome or Chromium (headless). Set CHROME to its binary if it
is not found. Writes docs/screenshots/telemetry-<shot>-<theme>.png.
"""
import datetime as dt
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates/.agents/skills/telemetry-report/scripts/dashboard.html"
OUT = ROOT / "docs" / "screenshots"
TODAY = dt.date(2026, 11, 20)
FIRST = TODAY - dt.timedelta(days=59)
GENERATED = "2026-11-20 18:00 UTC"

# Context commits. The first one is the effect the before/after table exists
# to show: CLAUDE.md turned into an index, so every session starts lighter.
CHANGES = [
    ("2026-09-30", "a41c2e0", "docs: add CONVENTIONS.md from the first three corrections", 1.00, 0.92),
    ("2026-10-15", "7d09b13", "docs: CLAUDE.md becomes an index; details move to docs/", 0.62, 0.55),
    ("2026-11-04", "c3e58aa", "docs: ADR for idempotent invoice export", 1.00, 0.85),
]
BRANCHES = ["feat/142-invoice-export", "fix/151-rounding-on-credit-notes", "feat/138-tax-id-validation",
            "chore/160-upgrade-node-22", "feat/147-dunning-emails", "fix/155-timezone-in-statements", "main"]
SKILLS = [("session-start", 0.9), ("session-close", 0.85), ("issue-start", 0.5), ("review-pr", 0.35),
          ("issue-new", 0.2)]
AGENTS = [("claude", "claude-sonnet-5-5", 0.62), ("codex", "gpt-5-codex", 0.25),
          ("copilot-cli", "claude-haiku-5-5", 0.13)]
PEOPLE = [("ana@example.com", "Ana"), ("ben@example.com", "Ben"), ("chen@example.com", "Chen"),
          ("dana@example.com", "Dana")]
REPOS = ["github.com/acme/billing", "github.com/acme/web"]


def factors(day):
    """Multipliers on context-at-start and orientation cost after each change."""
    ctx = orient = 1.0
    for d, _, _, c, o in CHANGES:
        if day >= dt.date.fromisoformat(d):
            ctx, orient = ctx * c, orient * o
    return ctx, orient


def sessions(rng, people=(None,), repos=(None,)):
    rows, buckets, runs = [], [], []
    for offset in range((TODAY - FIRST).days + 1):
        day = FIRST + dt.timedelta(days=offset)
        if day.weekday() >= 5 and rng.random() < 0.85:
            continue
        ctx_f, orient_f = factors(day)
        for dev in people:
            for repo in repos:
                for _ in range(rng.choice([1, 2, 2, 3, 3, 4]) if dev is None else rng.choice([0, 1, 1, 2])):
                    agent, model, _ = rng.choices(AGENTS, weights=[w for *_, w in AGENTS])[0]
                    branch = BRANCHES[min(int(offset / 9 + rng.random() * 2), len(BRANCHES) - 1)]
                    if rng.random() < 0.12:
                        branch = "main"
                    turns = rng.randint(3, 14)
                    n = turns * rng.randint(4, 9)
                    o = int(turns * rng.uniform(900, 1700))
                    ctx0 = int(rng.uniform(52000, 66000) * ctx_f)
                    i, w = int(n * rng.uniform(200, 600)), int(ctx0 * rng.uniform(0.9, 1.6))
                    r = int(n * ctx0 * rng.uniform(1.0, 1.5))
                    edits = rng.random() > 0.15
                    hour = rng.randint(9, 18)
                    idx = len(rows)
                    row = {"id": "%08x" % rng.getrandbits(32), "a": agent, "d": day.isoformat(),
                           "start": "%s %02d:%02d" % (day.isoformat(), hour, rng.randint(0, 59)),
                           "active": turns * rng.randint(3, 6), "turns": turns, "n": n,
                           "sub": rng.randint(0, n // 6), "models": [model], "branches": [branch],
                           "o": o, "f": i + w, "r": r, "ctx0": ctx0, "ctxmax": int(ctx0 * rng.uniform(1.6, 2.8)),
                           "orient": int(rng.uniform(34000, 52000) * orient_f) if edits else None,
                           "edit_min": rng.randint(2, 9) if edits else None}
                    extra = {}
                    if dev is not None:
                        extra = {"dev": dev, "repo": repo}
                        row["start"] = day.isoformat()   # published reports carry no time of day
                    rows.append(dict(row, **extra))
                    buckets.append(dict({"d": row["d"], "b": branch, "n": n, "i": i, "o": o, "r": r, "w": w,
                                         "a": agent, "s": idx}, **extra))
                    if agent == "claude":
                        for skill, p in SKILLS:
                            if rng.random() < p:
                                k = rng.randint(2, 8)
                                runs.append(dict({"d": row["d"], "a": agent, "k": skill, "n": k,
                                                  "o": k * rng.randint(250, 700), "f": k * rng.randint(1500, 5000),
                                                  "r": k * ctx0}, **extra))
    rows.sort(key=lambda s: s["start"])
    return rows, buckets, runs


def local_payload():
    rows, buckets, runs = sessions(random.Random(7))
    return {"project": "acme-billing · sample data", "generated": GENERATED, "today": TODAY.isoformat(),
            "agents": [a for a, *_ in AGENTS], "sessions": rows, "buckets": buckets, "runs": runs,
            "changes": [{"d": d, "sha": sha, "subject": s} for d, sha, s, *_ in CHANGES],
            "health": {"claude_files": 96, "codex_files": 41, "copilot_cli_scanned": 22}}


def team_payload():
    rows, buckets, runs = sessions(random.Random(11), [p for p, _ in PEOPLE], REPOS)
    reporting = [{"repo": repo, "dev": dev, "label": label, "gaps": [],
                  "updated": ("2026-10-29" if label == "Dana" else "2026-11-19"), "stale": label == "Dana"}
                 for repo in REPOS for dev, label in PEOPLE]
    return {"mode": "team", "project": "2 repositories · sample data", "generated": GENERATED,
            "today": TODAY.isoformat(), "agents": [a for a, *_ in AGENTS],
            "people": [{"id": i, "label": l} for i, l in PEOPLE], "repos": REPOS,
            "reporting": reporting, "stale_days": 14, "sessions": rows, "buckets": buckets, "runs": runs,
            "changes": [{"d": d, "sha": sha, "subject": s, "repo": REPOS[0]} for d, sha, s, *_ in CHANGES],
            "health": {"repos_read": 2}}


# Each shot keeps the header and the sections named here; the rest is hidden.
SHOTS = {
    "overview": (local_payload, ["#tiles", "#chart-card"], 800),
    "context-changes": (local_payload, ["#impact"], 500),
    "team": (team_payload, ["#tiles", "#repos-card"], 625),
}


def page(payload, keep, theme):
    html = TEMPLATE.read_text(encoding="utf-8")
    # Pin the theme instead of following the OS: light drops the dark block,
    # dark applies it unconditionally.
    dark = "@media (prefers-color-scheme: dark)"
    html = html.replace(dark, "@media all" if theme == "dark" else "@media not all")
    sel = ", ".join(keep)
    hide = "footer, .card:not(:is(%s)):not(:has(%s))%s { display: none !important; }" % (
        sel, sel, "" if "#tiles" in keep else ", #tiles, #filters")
    html = html.replace("</style>", hide + "\n</style>")
    return html.replace("__DATA__", json.dumps(payload, separators=(",", ":")).replace("</", "<\\/"))


def chrome():
    for c in [os.environ.get("CHROME"), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser")]:
        if c and os.path.exists(c):
            return c
    sys.exit("✗ Chrome or Chromium not found; set CHROME to its binary.")


def main():
    binary = chrome()
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for name, (build, keep, height) in SHOTS.items():
            payload = build()
            for theme in ("light", "dark"):
                src = Path(tmp) / ("%s-%s.html" % (name, theme))
                src.write_text(page(payload, keep, theme), encoding="utf-8")
                dst = OUT / ("telemetry-%s-%s.png" % (name, theme))
                subprocess.run([binary, "--headless", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                                "--force-device-scale-factor=2", "--window-size=1120,%d" % height,
                                "--user-data-dir=" + str(Path(tmp) / "profile"),
                                "--screenshot=" + str(dst), src.as_uri()],
                               check=True, capture_output=True)
                print("wrote", dst.relative_to(ROOT))


if __name__ == "__main__":
    main()
