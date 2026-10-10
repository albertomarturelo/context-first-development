#!/usr/bin/env python3
"""Build the README diagrams as SVG, one light and one dark file each.

Single source for every figure in docs/diagrams/. Edit this file, then run:

    python3 scripts/build-diagrams.py

Palette: the Signal tokens (flat, hairline borders, one amber accent spent
in one place per figure, ink-blue neutrals). No dependencies.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "docs" / "diagrams"

THEMES = {
    "light": dict(bg="#E7E8EC", surface="#F2F3F6", surface2="#FBFBFD",
                  border="#CBCFD8", text="#171921", muted="#565B68",
                  accent="#A8690F", on_accent="#FBFBFD",
                  success="#2C7A6B", danger="#AF463C"),
    "dark": dict(bg="#0F1118", surface="#171A22", surface2="#1E222D",
                 border="#2B303C", text="#E9EAF0", muted="#969CAB",
                 accent="#F0A93E", on_accent="#14161C",
                 success="#63B9AB", danger="#DC7A70"),
}

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


class Fig:
    def __init__(self, w, h, theme, label):
        self.w, self.h, self.c, self.label = w, h, THEMES[theme], label
        self.parts = []

    # -- primitives -------------------------------------------------------
    def text(self, x, y, s, size=14, color="text", anchor="start",
             weight=400, mono=False):
        fam = MONO if mono else SANS
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{self.c[color]}" '
            f'text-anchor="{anchor}">{escape(s)}</text>')

    def rect(self, x, y, w, h, fill="surface", stroke="border", r=10,
             dashed=False, width=1):
        dash = ' stroke-dasharray="5 4"' if dashed else ""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{self.c[fill] if fill else "none"}" '
            f'stroke="{self.c[stroke]}" stroke-width="{width}"{dash}/>')

    def path(self, d, color="muted", dashed=False, arrow=True, width=1.5):
        dash = ' stroke-dasharray="6 5"' if dashed else ""
        end = f' marker-end="url(#a-{color})"' if arrow else ""
        self.parts.append(
            f'<path d="{d}" fill="none" stroke="{self.c[color]}" '
            f'stroke-width="{width}" stroke-linecap="round" '
            f'stroke-linejoin="round"{dash}{end}/>')

    def circle(self, x, y, r, fill="surface2", stroke="muted", width=1.5):
        self.parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{self.c[fill]}" '
            f'stroke="{self.c[stroke]}" stroke-width="{width}"/>')

    # -- composites -------------------------------------------------------
    def header(self, kicker, title):
        self.text(40, 46, kicker, 12, "muted", weight=600, mono=True)
        self.text(40, 78, title, 22, "text", weight=700)

    def chip(self, x, y, w, name, desc="", h=36, fill="surface2"):
        self.rect(x, y, w, h, fill=fill, r=8)
        self.text(x + 12, y + h / 2 + 4.5, name, 13, "text", mono=True)
        if desc:
            self.text(x + w - 12, y + h / 2 + 4.5, desc, 12, "muted",
                      anchor="end")

    def tag(self, x, y, w, s, color):
        self.rect(x, y, w, 26, fill="surface2", stroke=color, r=13)
        self.text(x + w / 2, y + 17.5, s, 12, color, anchor="middle",
                  weight=600)

    def render(self):
        c = self.c
        markers = "".join(
            f'<marker id="a-{k}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{c[k]}"/></marker>'
            for k in ("muted", "accent", "text", "success", "danger"))
        grid = (f'<pattern id="grid" width="46" height="46" '
                f'patternUnits="userSpaceOnUse"><path d="M46 0 L0 0 0 46" '
                f'fill="none" stroke="{c["text"]}" stroke-opacity="0.04"/>'
                f'</pattern>')
        body = "\n".join(self.parts)
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} '
            f'{self.h}" width="{self.w}" height="{self.h}" role="img" '
            f'aria-label="{escape(self.label)}">\n'
            f'<title>{escape(self.label)}</title>\n'
            f'<defs>{markers}{grid}</defs>\n'
            f'<rect x="0.5" y="0.5" width="{self.w - 1}" height="{self.h - 1}"'
            f' rx="14" fill="{c["bg"]}" stroke="{c["border"]}"/>\n'
            f'<rect x="0.5" y="0.5" width="{self.w - 1}" height="{self.h - 1}"'
            f' rx="14" fill="url(#grid)"/>\n{body}\n</svg>\n')


# ---------------------------------------------------------------------------
def how_it_works(t):
    f = Fig(1000, 600, t, "Without CFD every session starts from zero and "
            "you re-explain, re-correct and re-argue. With CFD each session "
            "writes what it learned into the repo and the next one reads it "
            "back.")
    f.header("WHY CFD", "The session forgets. The repo remembers.")
    xs, w = (40, 367, 694), 266

    f.text(40, 132, "WITHOUT CFD", 12, "danger", weight=700, mono=True)
    before = [("Monday", "you explain the architecture",
               "agent writes the feature"),
              ("Tuesday", "you explain it again",
               "agent repeats Monday's mistake"),
              ("Wednesday", "agent revives a rejected idea",
               "you argue it all over again")]
    for x, (day, a, b) in zip(xs, before):
        f.rect(x, 146, w, 104, fill="surface")
        f.text(x + 18, 176, day, 16, weight=700)
        f.text(x + 18, 202, a, 13, "muted")
        f.text(x + 18, 224, b, 13, "muted")
    for x in xs[:2]:
        f.path(f"M{x + w + 4} 198 L{x + w + 57} 198", color="danger",
               dashed=True)
        f.text(x + w + 30, 188, "lost", 11, "danger", anchor="middle",
               mono=True)

    f.text(40, 298, "WITH CFD", 12, "success", weight=700, mono=True)
    after = [("Monday", "decision → ADR",
              "correction → CONVENTIONS.md"),
             ("Tuesday", "/session-start: ~1–3k tokens",
              "picks up where Monday stopped"),
             ("Wednesday", "agent cites the ADR",
              "rejected idea stays rejected")]
    for i, (x, (day, a, b)) in enumerate(zip(xs, after)):
        f.rect(x, 312, w, 104, fill="surface")
        f.text(x + 18, 342, day, 16, weight=700)
        f.text(x + 18, 368, a, 13, "muted", mono=a.startswith("/"))
        f.text(x + 18, 390, b, 13, "muted")
        f.path(f"M{x + 90} 420 L{x + 90} 470")
        f.path(f"M{x + 176} 470 L{x + 176} 420")
        f.text(x + 82, 450, "close", 11, "muted", anchor="end", mono=True)
        f.text(x + 184, 450, "start", 11, "muted", mono=True)

    f.rect(40, 474, 920, 96, fill="surface", stroke="accent", width=2)
    f.text(58, 500, "the repo · versioned · reviewed · read by any agent",
           12, "accent", weight=600, mono=True)
    for i, n in enumerate(["CLAUDE.md", "CURRENT_STATUS.md", "decisions/",
                           "CONVENTIONS.md", "issue #N"]):
        f.chip(56 + i * 180, 516, 168, n, "", h=36)
    return f


def solo(t):
    f = Fig(1000, 450, t, "The solo loop: start, pick one issue, implement, "
            "open the PR and review it yourself, fix the findings, close, "
            "merge; corrections and decisions are written down as they "
            "happen.")
    f.header("CASE 1 · ONE DEVELOPER, ONE REPO",
             "One loop. One issue per session.")
    steps = [("1", "/session-start", "reads STATUS +", "decisions index"),
             ("2", "/issue-start N", "loads the AC", "+ its ADRs"),
             ("3", "implement", "one AC item", "at a time"),
             ("4", "PR + /review-pr", "self-review; fix", "findings now"),
             ("5", "/session-close", "updates STATUS;", "docs ship with code"),
             ("6", "merge", "closes the issue", "")]
    x0, w, gap, y, h = 42, 136, 20, 120, 100
    for i, (n, title, l1, l2) in enumerate(steps):
        x = x0 + i * (w + gap)
        hot = i == 4
        f.rect(x, y, w, h, fill="surface", stroke="accent" if hot else
               "border", width=2 if hot else 1)
        f.text(x + 12, y + 22, n, 11, "accent" if hot else "muted",
               weight=700, mono=True)
        f.text(x + 12, y + 46, title, 13, "text", weight=600,
               mono=title.startswith("/"))
        f.text(x + 12, y + 70, l1, 12, "muted")
        if l2:
            f.text(x + 12, y + 86, l2, 12, "muted")
        if i < len(steps) - 1:
            f.path(f"M{x + w + 2} {y + h / 2} L{x + w + gap - 2} {y + h / 2}")
    f.text(x0 + 4 * (w + gap) + w / 2, y - 10, "the habit that makes it work",
           12, "accent", anchor="middle", weight=600)

    # mid-session events under step 3
    cx = x0 + 2 * (w + gap) + w / 2
    f.rect(214, 280, 236, 64, fill="surface2", dashed=True)
    f.text(228, 305, "You correct a pattern", 13, weight=600)
    f.text(228, 328, "→ rule in CONVENTIONS.md", 12, "muted", mono=True)
    f.rect(470, 280, 236, 64, fill="surface2", dashed=True)
    f.text(484, 305, "A decision surfaces", 13, weight=600)
    f.text(484, 328, "→ /new-decision, ADR first", 12, "muted", mono=True)
    f.path(f"M{cx - 20} {y + h + 4} L332 276", dashed=True)
    f.path(f"M{cx + 20} {y + h + 4} L588 276", dashed=True)

    # loop back
    last = x0 + 5 * (w + gap) + w / 2
    first = x0 + w / 2
    f.path(f"M{last} {y + h + 4} L{last} 400 Q{last} 410 {last - 10} 410 "
           f"L{first + 10} 410 Q{first} 410 {first} 400 L{first} {y + h + 4}")
    f.text(500, 432, "next session starts where this one stopped", 12,
           "muted", anchor="middle")
    return f


def team(t):
    f = Fig(1000, 480, t, "In a team, each developer's status file stays on "
            "their laptop; the tracker says who does what; shared rules on "
            "main change only through a reviewed PR that passes CI.")
    f.header("CASE 2 · A TEAM ON ONE REPO",
             "Personal state stays local. Shared truth goes through review.")
    f.text(40, 124, "ON EACH LAPTOP", 12, "muted", weight=600, mono=True)
    f.text(430, 124, "SHARED", 12, "muted", weight=600, mono=True)

    for i, who in enumerate(["Developer A", "Developer B"]):
        y = 140 + i * 160
        f.rect(40, y, 250, 130, fill="surface")
        f.text(58, y + 30, who + " + agent", 15, weight=700)
        f.chip(56, y + 46, 218, "CURRENT_STATUS.md", "", h=32)
        f.text(58, y + 100, "gitignored: personal memory", 12, "muted")
        f.text(58, y + 118, "of where they stopped", 12, "muted")

    f.rect(430, 140, 230, 110, fill="surface")
    f.text(448, 170, "Tracker", 15, weight=700)
    f.text(448, 196, "issues with AC · assignees", 12, "muted")
    f.text(448, 216, "who does what, right now", 12, "muted")

    f.rect(430, 310, 230, 120, fill="surface")
    f.text(448, 340, "CI on every PR", 15, weight=700)
    for i, s in enumerate(["ADR contract", "ADR slugs unique",
                           "context freshness (warns)"]):
        f.text(448, 366 + i * 20, "· " + s, 12, "muted")

    f.rect(720, 140, 240, 290, fill="surface", stroke="accent", width=2)
    f.text(738, 170, "main", 15, "accent", weight=700, mono=True)
    for i, (n, d) in enumerate([("CLAUDE.md", "index"),
                                ("decisions/", "ADRs"),
                                ("CONVENTIONS.md", "rules"),
                                (".agents/skills/", "rituals")]):
        f.chip(736, 188 + i * 44, 208, n, d, h=34)
    f.text(738, 382, "changes only through", 12, "muted")
    f.text(738, 400, "a reviewed PR", 12, "muted")

    # both developers feed one bus
    f.path("M290 205 L322 205", arrow=False)
    f.path("M290 365 L322 365", arrow=False)
    f.path("M322 195 L322 370", arrow=False)
    f.path("M322 195 L426 195")
    f.text(374, 185, "claim issues", 12, "muted", anchor="middle")
    f.path("M322 370 L426 370")
    f.text(374, 360, "open PRs", 12, "muted", anchor="middle")
    f.text(374, 392, "code + docs", 12, "muted", anchor="middle")
    f.path("M664 370 L716 370")
    f.text(690, 360, "merge", 12, "muted", anchor="middle")
    return f


def worktrees(t):
    f = Fig(1000, 580, t, "Parallel loops: decisions for the batch land on "
            "main first; each worktree runs one issue with one agent on its "
            "own paths; a mid-loop decision lands on main as its own PR, "
            "siblings rebase, and merges happen one at a time.")
    f.header("CASE 3 · PARALLEL LOOPS IN GIT WORKTREES",
             "Isolate files per worktree. Settle decisions on main first.")
    main_y = 190
    f.text(40, main_y + 24, "main", 13, weight=700, mono=True)
    f.path(f"M40 {main_y} L960 {main_y}", color="text", arrow=False, width=2)

    lanes = [(285, "wt-1 · Claude Code · #41 · src/auth/", 600),
             (375, "wt-2 · Codex · #42 · src/billing/", 760),
             (465, "wt-3 · Copilot · #43 · docs/api/", 920)]
    bx = 150
    f.path(f"M{bx} {main_y} L{bx} {lanes[-1][0] - 10} "
           f"Q{bx} {lanes[-1][0]} {bx + 10} {lanes[-1][0]}", arrow=False)
    for y, label, mx in lanes:
        if y != lanes[-1][0]:
            f.path(f"M{bx} {y - 10} Q{bx} {y} {bx + 10} {y}", arrow=False)
        f.path(f"M{bx + 10} {y} L{mx - 10} {y} Q{mx} {y} {mx} {y - 10} "
               f"L{mx} {main_y + 9}")
        f.text(bx + 18, y - 12, label, 12, mono=True)
        for sx in range(bx + 60, mx - 40, 90):
            busy = (470,) if y == 375 else (530,)
            if all(abs(sx - b) > 22 for b in busy):
                f.circle(sx, y, 4.5)
    # rebase markers on wt-1 and wt-3 after the mid-loop ADR
    for y in (285, 465):
        f.circle(530, y, 6, fill="surface2", stroke="text")
        f.text(530, y + 22, "rebase", 11, "muted", anchor="middle", mono=True)

    # main commits
    f.circle(bx - 50, main_y, 8, fill="accent", stroke="accent")
    f.text(bx - 50, main_y - 46, "ADRs for the batch", 12, "accent",
           anchor="middle", weight=700)
    f.text(bx - 50, main_y - 28, "decided first", 12, "accent",
           anchor="middle")
    f.circle(470, main_y, 7, fill="surface2", stroke="text")
    f.text(470, main_y - 46, "mid-loop ADR", 12, anchor="middle", weight=600)
    f.text(470, main_y - 28, "lands as own PR", 12, "muted", anchor="middle")
    for mx, n in ((600, "#41"), (760, "#42"), (920, "#43")):
        f.circle(mx, main_y, 7, fill="surface2", stroke="success")
        f.text(mx, main_y - 46, f"merge {n}", 12, anchor="middle",
               weight=600)
        f.text(mx, main_y - 28, "rebased + reviewed", 12, "muted",
               anchor="middle")
    # wt-2 surfaces a decision
    f.rect(458, 363, 24, 24, fill="surface2", stroke="danger", r=4)
    f.text(470, 380, "!", 13, "danger", anchor="middle", weight=700)
    f.path(f"M470 359 L470 {main_y + 11}", color="danger", dashed=True)
    f.text(490, 402, "new ADR needed: stop, land it first", 11, "danger",
           mono=True)

    f.rect(40, 506, 920, 50, fill="surface")
    f.text(58, 536, "You orchestrate:", 13, weight=700)
    f.text(190, 536, "disjoint targets per issue  ·  every merge reviewed "
           "against current main  ·  loops ≤ what you can review (2–3)",
           13, "muted")
    return f


def agents(t):
    f = Fig(1000, 460, t, "Several agents, one source: CLAUDE.md and "
            ".agents/skills are the only copies; AGENTS.md and .claude/skills "
            "are symlinks, so every agent reads the same context from the "
            "path it expects.")
    f.header("CASE 4 · SEVERAL AGENTS, ONE SOURCE",
             "One copy of the context. Every agent finds it where it looks.")
    for y, link, canon, desc in ((130, "AGENTS.md", "CLAUDE.md", "the index"),
                                 (262, ".claude/skills/", ".agents/skills/",
                                  "the procedures")):
        f.rect(40, y + 22, 180, 46, fill="surface2", dashed=True, r=8)
        f.text(56, y + 50, link, 13, mono=True)
        f.path(f"M224 {y + 45} L316 {y + 45}")
        f.text(270, y + 36, "symlink", 11, "muted", anchor="middle",
               mono=True)
        f.rect(320, y, 250, 90, fill="surface", stroke="accent", width=2)
        f.text(340, y + 38, canon, 15, "accent", weight=700, mono=True)
        f.text(340, y + 62, desc + " · the only copy", 12, "muted")

    rows = [("Claude Code", "CLAUDE.md · .claude/skills · /name"),
            ("Codex", "AGENTS.md · .agents/skills · $name"),
            ("GitHub Copilot", "AGENTS.md · .agents/skills · /name"),
            ("Gemini CLI", "AGENTS.md* · .agents/skills")]
    for i, (name, reads) in enumerate(rows):
        y = 110 + i * 66
        f.rect(680, y, 280, 56, fill="surface")
        f.text(696, y + 23, name, 14, weight=700)
        f.text(696, y + 43, reads, 11, "muted", mono=True)
    f.path("M572 175 L596 175 L596 307 L572 307", arrow=False)
    f.path("M596 241 L676 241")
    f.text(636, 231, "read by", 12, "muted", anchor="middle")
    f.text(636, 261, "every agent", 12, "muted", anchor="middle")
    f.text(680, 392, "* one config line; see the per-agent table", 11,
           "muted")
    f.rect(40, 404, 920, 40, fill="surface")
    f.text(58, 429, "CI runs the same checks on every PR, whichever agent "
           "wrote it. Hooks are a Claude Code bonus, not the guarantee.",
           13, "muted")
    return f


FIGURES = {"how-it-works": how_it_works, "case-solo": solo,
           "case-team": team, "case-worktrees": worktrees,
           "case-agents": agents}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in FIGURES.items():
        for theme in THEMES:
            (OUT / f"{name}-{theme}.svg").write_text(build(theme).render())
    print(f"wrote {len(FIGURES) * len(THEMES)} files to {OUT}")
