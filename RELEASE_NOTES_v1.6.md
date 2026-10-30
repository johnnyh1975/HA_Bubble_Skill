# ha-bubble-dashboard v1.6

**Graph and history coverage, plus a CI pipeline — and the bug that pipeline
found on its first run.**

Two new components supported, a dependency the skill had been generating
without declaring, and seven broken view scaffolds fixed.

---

## ⚠️ Read this first

**Delete `references/dashboard-recipes.md` if it still exists in your install.**
It was removed in v1.4 as a verified duplicate, but anyone who *synced* the
skill folder rather than replacing it still has the stale copy — where it
silently competes with `dashboard-system.md` as a source of truth.

```bash
rm references/dashboard-recipes.md
```

**Re-copy `theme/Casa5HeyneV2.yaml`** to `/config/themes/` and run
`frontend.reload_themes` if you have not since v1.4.

**Repository layout changed.** Tooling moved to `scripts/`. The release bundle
now excludes it, so what you install is only the skill: `SKILL.md`, `README`,
`CHANGELOG`, `available-skills-entry.md`, `references/` and `theme/`.

---

## 🐛 The big fix: seven broken view scaffolds

New CI validates every fenced YAML block in the documentation — those blocks
*are* the product, users copy them into Home Assistant. On its first run it
found a defect that had already shipped:

```yaml
  cards:            # wrong
    sections:
```

View scaffolds nested `sections:` underneath `cards:` instead of making them
siblings. In a sections view, `sections:` holds the card grid and `cards:`
holds top-level cards (pop-ups, the HBS footer) — the skill's own §4 rule.
**The nested form does not parse, so anyone copying an affected scaffold got a
dashboard that would not load.**

Affected and fixed: the core dashboard example in `SKILL.md` itself, four
scaffolds in `dashboard-system.md` (Scenes, Activity, Settings, Energy), the
Music scaffold (which also needed reordering — its pop-ups preceded the
sections), and two in `recipes-5view.md`.

Also fixed: `mush-rgb-state-alarm-triggered:"var(…)"` in
`mushroom-theme-ref.md` was missing the space after the colon, so that line
silently did nothing when copied into a theme.

---

## 📊 New: graph and history coverage

New reference file `graphs-ref.md`, deliberately scoped rather than
exhaustive:

- **`#graph-decision`** — a decision table rather than a product tour: native
  `history-graph` / `statistics-graph` → mini-graph-card → Statistics Graph
  Chart Card → the Advanced History panel. Every custom option is a HACS
  install, and the rule is now that the dependency and its native fallback get
  named in the same breath.
- **`#advanced-history`** — the Advanced History panel (integration v2.0.1,
  requires SGCC v3.32+, v4.02+ for multiple panels). It is not a card, so it
  never competes for dashboard space. That makes it the honest answer to "a
  page with graphs of everything": the user wants an exploration tool, not a
  dashboard view.
- **`#sgcc-dashboard-use`** — the handful of options that matter when
  generating, not the full 4,700-line surface: `sparkline: true` (chrome-free,
  the calm-technology-compatible form), `height: auto` (participates in
  sections grid sizing), `group_by: raw` for step charts.
- **`#graph-performance`** — `data_source: statistics` and statistics-based
  `group_by` keep a graph-heavy dashboard off the recorder's back. Upstream
  measures 287 rows / 33 ms versus 21,995 rows / 1.7 s for the same window.
  This is the most common cause of "my Home Assistant got slow after I
  rebuilt my dashboard".
- **`#sgcc-status`** — stated plainly: Statistics Graph Chart Card ships as a
  **minified, protected bundle**, so the source-first verification this skill
  uses for every other component is impossible for it. Documented from its
  README only, with the maintenance consequences for unattended wall panels.

**mini-graph-card was being generated in 15 places without ever being declared
as a dependency.** Now declared, with the overlap against SGCC's sparkline
mode addressed directly: use whichever is already installed; never add
mini-graph-card when SGCC is going in anyway; prefer the small open card when
a sparkline is the only need; and don't let the whole graph capability rest on
an unauditable bundle by default.

---

## 🔧 New: CI pipeline

The repository had no workflows, no tags and no releases — every version was a
hand-passed zip.

| Workflow | Trigger | What it does |
|---|---|---|
| `verify.yml` | push, PR | `verify.py` (13 structural checks), `test_verify.py`, `token_budget.py --check`. Comments the SKILL.md token delta on PRs. |
| `upstream-drift.yml` | weekly | Compares component pins against upstream releases, opening one issue when a pin falls behind. Also an advisory link check. |
| `release.yml` | tag `v*` | Verifies, asserts the tag matches `SKILL.md`, builds `.zip` and `.skill` bundles without `scripts/`, verifies the packaged tree, publishes the release. |

**`verify.py` — 13 checks**, each one added because that class of bug shipped
at least once: anchor integrity, anchor-list sync, YAML validity (including
every fenced example), theme light/dark symmetry, nonexistent component
variables, the Iron Law in card examples, version consistency, Anthropic's
SKILL.md frontmatter spec, metadata sanity, routing coverage, duplicate
content, and orphaned files.

**`test_verify.py` — the answer to "who checks the checker".** It injects each
bug class into a throwaway copy and asserts `verify.py` still catches it.
13/13. This exists because `verify.py` missed a stale metadata comment: nothing
was testing the tester.

**`token_budget.py`** guards what actually costs: SKILL.md is loaded in full
for every request, while reference files are anchor-routed and only cost what
is read. On this library a troubleshooting question spends roughly 96% of its
tokens on SKILL.md. Budgets are enforced on that file and on any single anchor
large enough that routing stops helping.

**Adopted from `skill-creator`:** Anthropic's frontmatter spec, reimplemented
as a check rather than vendored, to keep the repo MIT-only. The skill passes
the official validator unchanged. Added on top: a warning above 900
description characters — the current description sits at 877/1024, and every
new TRIGGER line eats headroom.

### Two checker bugs the checker found

CI on the live repository flagged a 4,217-token anchor in
`dashboard-recipes.md` — a file deleted in v1.4. Two checks should have caught
it directly and did not:

- `check_orphans` counted a CHANGELOG mention as a live reference. The
  changelog says "Deleted `dashboard-recipes.md`", which made the deleted file
  look referenced. Only SKILL.md and other reference files now count.
- No duplicate detection existed at all, despite a 50 KB exact duplicate being
  the largest structural defect in this project's history.

The lesson generalises: a check that reads *any* mention as a reference will be
defeated by the file that documents deletions.

---

## Component pins

| Component | Version |
|---|---|
| Bubble Card | 3.3.0 |
| Bubble Card Tools | 1.0.2 |
| Streamline Card | 0.2.2 |
| Sidebar Card | 0.1.9.9 |
| Mushroom | 5.2.2 (source-verified) |
| Statistics Graph Chart Card | 4.02-era (README-documented — minified bundle) |
| Advanced History | 2.0.1 |
| HA minimum | 2024.3.0 |
| Guidance verified against | HA 2026.9 |

## Upgrade notes

- Delete `references/dashboard-recipes.md` if present (see above).
- Re-copy the theme file if you have not since v1.4; it gained the ZONE 6
  Mushroom state mapping and light-mode colour parity.
- If you copied `mush-rgb-state-switch` or `mush-rgb-primary` into a custom
  theme, remove them — neither variable exists in Mushroom.
- No breaking changes to generated YAML formats. Existing dashboards are
  unaffected; the scaffold fix only affects newly generated views.

**Full changelog:** see `CHANGELOG.md`.
