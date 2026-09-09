# ha-bubble-dashboard — Changelog


## Standing check — run on every HA minor release

Monthly HA releases have repeatedly broken frontend assumptions (2026.5:
editor fields + iOS pop-up DOM change; 2026.1: mobile navigation overhaul).
On each HA minor release, verify before trusting the skill's guidance:

- [ ] Pop-up rendering and visibility (sections-layout DOM changes)
- [ ] Bubble Card editor fields present (HA form-schema changes)
- [ ] Sidebar Card `showTopMenuOnMobile` / native mobile nav behaviour
- [ ] Card-suggestion registration still functioning (HA 2026.6+ picker)
- [ ] New native dashboard features that extend the `#native-first` table
      (Maintenance/Security dashboards, tile card features, heading card)
- [ ] Bubble Card / Streamline / Sidebar / Bubble Card Tools version pins

**When verifying a component release, scan the source tree — not the release
notes and not the editor schemas alone.** Editor-only scans miss every
YAML-facing option the editor doesn't surface; a `config.*` grep across
`src/` is the reliable method. The same applies to CSS variables: check the
actual `var()` fallback chain in source rather than trusting documentation.

---

## v1.6 — 2026-08-29

New capability: graph and history coverage. Adds support for two components
the skill did not previously know about, and closes a dependency the skill had
been generating without ever declaring.

### New reference: `graphs-ref.md`

The skill generated `custom:mini-graph-card` in 15 places without ever
declaring it as a dependency, and had no guidance on choosing a graph card at
all. New reference file, deliberately scoped rather than exhaustive:

- **`#graph-decision`** — the decision table (native `history-graph` /
  `statistics-graph` → mini-graph-card → SGCC → Advanced History panel), with
  the rule that every custom option is a HACS install that must be named
  alongside its native fallback.
- **`#sgcc-status`** — Statistics Graph Chart Card ships as a **minified,
  protected bundle**, so source-first verification (this skill's standing
  method) is impossible for it. Documented from README only, stated plainly,
  with the maintenance consequences for unattended wall panels.
- **`#sgcc-dashboard-use`** — the handful of options that matter for
  generation rather than the full 4700-line surface: `sparkline` (chrome-free,
  the calm-tech-compatible form), `height: auto` (participates in sections
  grid sizing), `group_by: raw` for step charts, plus the Iron Law reminder
  that `color:` takes CSS values, so theme variables belong there.
- **`#graph-performance`** — `data_source: statistics` and statistics-based
  `group_by` as the mechanisms that keep a graph-heavy dashboard off the
  database's back; upstream measures 287 rows/33 ms vs 21,995 rows/1.7 s for
  the same window. Plus the `state_class` prerequisite for long ranges, which
  is an ha-yaml handoff rather than a card option.
- **`#advanced-history`** — the panel (integration v2.0.1, requires SGCC
  v3.32+, v4.02+ for multiple panels). Positioned through the engagement-type
  model: it is not a card, so it never competes for dashboard space, which
  makes it the honest answer to "a page with graphs of everything" — an
  exploration tool rather than a glanceable surface.

- **The mini-graph-card / SGCC-sparkline overlap** is addressed explicitly
  rather than left for the reader. Both cover "a small trend line", so the
  choice is a dependency decision: use whichever is already installed; never
  add mini-graph-card when SGCC is going in anyway (sparkline covers it);
  prefer the small open card when a sparkline is the only need; and don't let
  the whole graph capability rest on an unauditable bundle by default. The
  Activity scaffold now labels its `mini-graph-card` usage as a *placeholder*
  with an instruction to ask, not a recommendation.
- SGCC's install path is documented honestly: the README's steps imply the
  default HACS catalogue while the repository still carries a *HACS: Custom*
  badge, so the guidance covers both.

Wired in: prerequisites table, process-tree route, two Signal Scan rows, the
Activity scaffold, four troubleshooting entries, a health-check graph-density
advisory, and `#eval-12-graph-request`.

### CI pipeline

- **`verify.yml`** — runs `verify.py` on every push and pull request, plus an
  advisory external-link check (non-blocking: upstream repos rename, and a
  redirect on someone else's URL should not fail a docs change).
- **`upstream-drift.yml`** — weekly job comparing the component pins in
  SKILL.md against the latest upstream releases via the GitHub API, opening or
  updating a single issue when a pin falls behind. This automates the failure
  mode that has actually recurred here: guidance going stale because a release
  shipped unnoticed. The issue body repeats the standing rule — scan the
  source tree, not the release notes.
- **`release.yml`** — on a `v*` tag: verify, assert the tag matches the
  `version` in SKILL.md metadata, build both a `.zip` and a `.skill` bundle,
  re-run `verify.py` against the *packaged* copy, and publish a GitHub
  Release. The repo previously had no tags and no releases; every version was
  a hand-passed zip.
- **`check_upstream.py`** — the drift checker, also usable locally.
- **`test_verify.py`** — negative tests for `verify.py`, run in CI. A checker
  that only ever passes proves nothing; this injects each bug class into a
  throwaway copy of the library and asserts the checker still catches it. Ten
  cases, one per shipped bug class, currently 10/10. This closes a real gap:
  `verify.py` missed the stale frontmatter comment because nothing tested the
  tester.

### Fenced YAML validation — and the defect it found

`verify.py` validated the two standalone `.yaml` files but never the ~205
fenced YAML blocks in the documentation, which *are* the product: users copy
them into Home Assistant. Parsing them found a defect in seven scaffolds,
including the core dashboard example in SKILL.md itself.

**The bug:** view scaffolds nested `sections:` underneath `cards:`

```yaml
  cards:            # wrong
    sections:
```

instead of making them siblings. In a sections view, `sections:` holds the
card grid and `cards:` holds top-level cards (pop-ups, the HBS footer) — the
skill's own §4 rule. The nested form does not parse, so anyone copying an
affected scaffold got a dashboard that would not load. Affected: the SKILL.md
core example, four scaffolds in `dashboard-system.md` (Scenes, Activity,
Settings, Energy), the Music scaffold (which also needed reordering, as its
pop-ups preceded the sections), and two in `recipes-5view.md`.

Also fixed: `mush-rgb-state-alarm-triggered:"var(…)"` in
`mushroom-theme-ref.md` was missing the space after the colon, so that line
silently did nothing when copied into a theme.

**New check (`yaml-examples`)** parses every fenced block, skipping the ones
that legitimately are not plain YAML — HA `!include*` tags, `{placeholder}`
keys, Streamline `[[variable]]` templates, and deliberately-partial
WRONG/CORRECT teaching fragments. `verify.py` is now 12 checks.

This is the clearest argument yet for the CI work: the defect had shipped, was
invisible to every existing check, and sat in the most-copied example in the
library.

### Token budget monitoring

- **`token_budget.py`** — measures the footprint that actually matters:
  SKILL.md as the fixed per-session cost, versus the anchor-routed reference
  library that only costs what is read. Enforces a ceiling on SKILL.md and a
  per-anchor ceiling above which routing stops helping, and reports growth
  over a committed baseline (`token-baseline.json`).
- Wired into `verify.yml`; on pull requests a sticky comment reports the
  SKILL.md delta, so a change that adds to the every-session cost says so in
  review instead of surfacing months later.
- Motivating measurement: SKILL.md grew from 14,959 to 15,928 tokens (+6.5%)
  during this release's work without anyone noticing. It sits at 15,928/17,000
  now — comfortable, but the trend is the point. Largest anchor is
  `#view-activity-scaffold` at 3,483; median across 162 anchors is 516.
- `test_verify.py` gained a case for the budget guard: 11/11.

### Two checker bugs found by the checker

CI on the live repository flagged `dashboard-recipes.md#view-activity` at 4,217
tokens — a file deleted in v1.4. It had survived because the repo was synced
rather than replaced, exactly the case the v1.4 upgrade note warned about. The
token budget caught it only by accident, through an oversized anchor.

Two checks that should have caught it directly did not:

- **`check_orphans` counted a CHANGELOG mention as a live reference.** The
  changelog says "Deleted `dashboard-recipes.md`" — which made the deleted file
  look referenced. Fixed: only SKILL.md and other reference files count as
  routing references. Changelog history does not.
- **No duplicate detection existed at all**, despite a 50 KB exact duplicate
  being the single largest structural defect in this project's history. New
  `check_duplicates` compares normalised 400-character windows across
  reference files and fails above 60% containment.

Both are now regression-tested (`test_verify.py`: 13/13). `verify.py` is at
13 checks.

The lesson generalises: a check that reads *any* mention as a reference will
be defeated by the file that documents deletions.

### Link check tuning

The external-link job reported one error: Patreon returns 403 to automated
requests. The link is correct — Patreon simply blocks bots. Excluded, along
with `homeassistant.local` (the reader's own LAN address) and `example.com`
(a placeholder in sample YAML).

The exclusion list is documented in the workflow with the reason for each
entry, and the standing rule is stated there: exclusions are for links that
*cannot* be checked, not for links we would rather not fix. A check that
reports a known false positive every run teaches people to ignore it — which
is worse than not having it.

The library has 7 unique external links in total, so this check is cheap
insurance rather than a major safeguard.

### Repository layout

Repository tooling moved from the skill root into `scripts/`
(`verify.py`, `test_verify.py`, `token_budget.py`, `check_upstream.py`,
`token-baseline.json`). The repo *is* the skill, so anything at the top level
ends up in what users install — the release bundle was shipping a test
harness, a token estimator and a drift checker to people who only wanted the
dashboard guidance.

`release.yml` now excludes `scripts/`, `CHANGELOG-v*-detail.md` and
`RELEASE_NOTES_v*.md` from the bundle, and verifies the packaged tree by
copying the checker in temporarily rather than shipping it. Every tool
resolves the skill root as its parent directory, so all paths still work.

### CI hardening

- Least-privilege `permissions:` on all three workflows (`contents: read`
  except where a job must write), `concurrency` groups (cancel superseded PR
  runs; never cancel a half-published release), `timeout-minutes`, and a
  pinned PyYAML version.
- **Release body defect fixed before it shipped:** `body_path: CHANGELOG.md`
  would have pasted all 480+ lines of history into every GitHub Release. The
  workflow now extracts only the tagged version's section (104 lines for
  v1.6) and fails the release if no such section exists.
- `.github/dependabot.yml` — monthly updates for third-party actions, the main
  supply-chain surface. Note in the file: pin to commit SHAs for the stricter
  guarantee; Dependabot maintains SHA pins too.
- PR template with the project's actual invariants as a checklist (source-tree
  scanning, routing reachability, the Iron Law, version gating), and two issue
  templates — "Claude generated something wrong" and "a component released",
  the two report types this repo actually receives.

### Adopted from skill-creator

Anthropic's `skill-creator` bundles `quick_validate.py`, which enforces the
SKILL.md frontmatter spec. Rather than vendor Apache-licensed code into an MIT
repo, the same rules were reimplemented as a `verify.py` check: exactly one
SKILL.md, `name`/`description` required, kebab-case name within 64 chars,
description within 1024 chars and free of angle brackets. The skill passes the
official validator unchanged.

Added on top: a warning above 900 description characters. The current
description is 877/1024 — every new TRIGGER or SYMPTOM line eats headroom, and
hitting the limit mid-edit is a bad time to find out.

`verify.py` is now 11 checks; workflow YAML joined the validity pass.

### Fixes

- Frontmatter defect: the `mushroom` pin carried a stale trailing comment
  claiming HA 2026.7 while `ha_checked` said 2026.9 — a leftover from an
  earlier edit. Fixed, and `verify.py` gained a tenth check (metadata lines
  with two comments), negative-tested.
- New pins recorded for the two added components. SGCC's is deliberately
  vague (`4.02-era`) because the bundle is minified and carries no readable
  version constant — an honest pin beats a guessed one.

### Behavioural tests

- `#eval-12-graph-request` — a German-language prompt asking for an overview
  page full of graphs, exercising the engagement-type argument, the Advanced
  History alternative, dependency declaration, and the `data_source`
  performance point in one case.

---

## v1.5 — 2026-08-29

Component currency: Bubble Card v3.3.0 support and alignment with Home
Assistant 2026.8/2026.9. Verified against the v3.3.0 source tree and HA
release notes through 2026.9.

### Bubble Card 3.2.5 → 3.3.0

- **Platform conditions documented.** v3.3.0 ports Home Assistant's own
  `domain.name` conditions to the client — 141 of them (`sun.is_up`,
  `motion.is_detected`, `climate.is_heating`, `lock.is_unlocked`,
  `zone.in_zone`, `select.is_option_selected`…) usable directly in
  `visibility:`. Documented with the caveats that matter: astral maths is
  approximated, `for:` durations drift because there is no recorder priming
  pass, recorder-history conditions cannot be ported, and an unsupported type
  falls back to a silent state check rather than failing loudly. Explicitly
  version-gated — on < 3.3.0 these misbehave rather than error.
- **Lovelace condition table completed** — `not`, `time`, `location`,
  `template` and `view_columns` were supported but undocumented.
- **`grid_options`** added: native HA sections sizing (`{rows, columns}`),
  preferred over `rows:` inside a sections view.
- **Installation change for manual installs.** The `translations/` folder is
  gone; editor dictionaries now sit beside `bubble-card.js` as
  `bubble-card-<lang>.json`. Documented in §1 with two troubleshooting entries
  (editor reverting to English, "Custom element doesn't exist" after update).
- **Six undocumented per-sub-button options** added: `sub_button_type`
  (now including `dropdown`), `show_button_info`, `hide_when_parent_unavailable`,
  `light_background`, `css_class` (the supported alternative to brittle
  `nth-child` selectors in `styles:`), and the `always_visible` interaction
  with `slider_value_position`.
- Signal Scan row for conditional-visibility requests, so the version gate
  fires before generation rather than after.

### Module authoring — two missing chapters

Diffed the skill's module reference against Bubble Card's own bundled
`src/modules/module-documentation.md` (1422 lines). Two substantial chapters
were absent:

- **New `#module-performance`.** Module `code:` runs on every style pass of
  every carrying card, and a pop-up rebuilds all its cards on each open —
  roughly seven passes per card. v3.3.0 adds `hasChanged(label, ...values)`
  and `onTeardown(fn)` to gate work and release timers/observers. Upstream
  measured one module going from 7.2 s to 3.7 s cold pop-up open on a low-end
  iPad. Includes the compatibility rule that matters most: referencing a name
  the installed version lacks throws and makes Bubble Card skip the *entire*
  module, so `typeof` guards are mandatory for shared modules.
- **New `#module-suggestions`.** Modules can join the HA 2026.6+ card picker
  via `suggestions:` (`extends: native|base`, `config` with `${entity}`,
  `domains`, `condition`, `label`) or `suggestions_code:` for computed
  configurations. 24 suggestions per module per entity, no global cap.

### Home Assistant 2026.8 / 2026.9 alignment

- **Breaking change handled: vacuum `battery_level` removed (HA 2026.8).** Two
  places in the skill generated `attribute: battery_level` sub-buttons — the
  generic battery example and the Streamline device template. Both now use the
  device's battery *sensor* with `show_state: true`. Troubleshooting entry
  added listing the eight affected integrations.
- **Developer Tools → Tools rename (HA 2026.8)** applied across all references,
  with the old name noted where a user on an older version would look for it.
- **New `dashboard-system.md#entity-rename-risk`.** Renaming entity IDs became
  a two-click UI operation in 2026.8, and HA's repair flow covers automations
  and scripts far better than Lovelace — a renamed entity leaves a card showing
  "Entity not available", silently. Guidance sequences the work (rename, then
  repair via §9 health check) rather than discouraging it. Signal Scan row and
  troubleshooting entry added.
- **Native-first table extended** with the capacity-weighted combined battery
  level (2026.8) and the clock card's date support (2026.8).
- **Accessibility section strengthened.** HA 2026.9 makes charts a real focus
  stop — keyboard-navigable data points, live-region announcements, and an
  audio tone tracking the curve. That is a concrete capability a custom graph
  card cannot match, and it is now part of the native-alternative argument.
- **Template performance note.** HA 2026.8 made numeric templates up to 40%
  faster and cached dashboard templates. The scope rule is unchanged, but a
  template sensor can no longer be justified on performance grounds alone.
- Device-registry split (2026.8) noted in troubleshooting: entity-based card
  YAML is unaffected; only device-ID references need review.

### Method note

The `config.*` source scan produced two false positives this round —
`unit_system` and `time_zone` are `hass.config.*` reads, not YAML options.
Scanning for `config.` alone conflates the card config with the HA config
object; distinguish the two before documenting an option.

---

## v1.4 — 2026-08-06

Ecosystem alignment, source-verified component updates, and a rebuilt routing
layer. Verified against Bubble Card v3.2.5 source, Mushroom v5.2.2 source, and
HA release notes through 2026.7.

Development detail for this release is preserved in
`CHANGELOG-v1.4-detail.md`; this entry is the summary.

### Component updates

- **Bubble Card pin 3.2.2 → 3.2.5.** Compat table rows for v3.2.3 (card
  suggestions via the HA 2026.6 picker, `close_action` fix, iOS pop-up
  visibility), v3.2.4 (standalone pop-ups reliable inside `vertical-stack`;
  true pop-up-in-pop-up nesting still unsupported) and v3.2.5 (cover tilt —
  `tilt_buttons`, `open_tilt_service`, `close_tilt_service`,
  `cover_slider_type: tilt_position`, with the feature-detection rule).
- **New Mushroom pin 5.2.2**, verified against `src/utils/theme.ts`.
- **24 previously undocumented Bubble Card options added.** The earlier
  verification scanned editor schemas only, which misses every YAML option the
  editor does not surface. A full `config.*` source scan closed the gap:
  six slider options, the six sub-buttons layout options, three calendar
  options, plus `show_last_updated`, `sub_button_justify_content` and
  `hide_temperature`.

### Corrections

- **Iron Law violation in the skill's own calendar example.** It used a
  hardcoded hex; `color:` resolves a colour *name* to `var(--<name>-color)`,
  so `color: accent` was available all along.
- **Two nonexistent Mushroom variables removed** — `mush-rgb-state-switch`
  (switches follow `mush-rgb-state-entity`) and `mush-rgb-primary`. Both were
  documented across 22 places and would have silently done nothing. Added the
  missing state groups (vacuum, media-player, lock + sub-states, number,
  humidifier, update) including the upstream quirk that `mush-rgb-update-off`
  and `-installing` carry no `state-` segment.
- **Module-authoring corrections** — removed a `variables:` + `{{mustache}}`
  pattern that does not exist in Bubble Card's module system, and the
  nonexistent `supported: [all]` literal.

### Native HA alignment

- New `#native-first` — the native-first check (parallel to automate-first):
  battery grids → Maintenance dashboard, security logs → Security Activity
  list, weather and media → tile features. Plus positioning against the native
  Home dashboard (default for new installs since HA 2026.2) and hybrid setups.
- New `#native-interop` — mixing native tile/heading/area cards into Bubble
  layouts: theme inheritance, Bubble-mechanism boundaries, grouping rules.
- Health-check gained a native-feature advisory category (Advisory only).

### Process routing rebuilt

- **New Signal Scan layer.** The process tree routed on *output type*, but
  most failure modes are *input signals* — the user's language, a stated
  accessibility need, a natively covered feature, an unsupported entity
  domain. A nine-row scan now runs ahead of the tree, is multi-select, and
  never withholds output. Actively routed eval cases: 3/10 → 10/10.
- **Process tree completed** — `calendar`, `select`, `separator` and
  `sub-buttons` were documented but had no route at all. Added, plus a branch
  for requests that describe a situation rather than name a card.
- Common Pitfalls trimmed 17 → 13 rows; four were intake signals and moved.

### New capabilities

- `#entity-inventory` — Developer Tools template snippet producing an
  area-grouped, device-class-annotated entity list for the Collect step.
- `#masonry-migration` — masonry → sections with a construct mapping table.
- `#wall-panel-hardening` — burn-in, screen-off handoff, kiosk pointers.
- `module-authoring-ref.md` — Bubble Card editor field catalog, v3.2.4 object
  selector, both export formats, plus the paid-module boundary rule.
- Localisation rule and an honest statement of Bubble Card's accessibility
  limits (div-based controls are not screen-reader operable; never claim WCAG
  conformance from contrast checks alone).
- Entity domain map extended with `siren`, `remote`, `lawn_mower`, and
  explicit no-support entries for `valve`, `water_heater`, `todo`, `image`.

### Tooling

- **`verify.py`** — nine structural checks (anchors, anchor-list sync, YAML
  validity, theme mode symmetry, banned variables, Iron Law in card examples,
  version consistency, routing coverage, orphan files). Each exists because
  that bug class shipped at least once; the routing check is negative-tested.
- **`references/eval-set.md`** — ten behavioural regression prompts with
  MUST / MUST NOT criteria, run in fresh conversations.

### Structural

- Deleted `dashboard-recipes.md` (~50 KB, verified duplicate, referenced
  nowhere) and `casa5heynev2-template.yaml` (theme existed in two copies that
  had already drifted twice). `theme/Casa5HeyneV2.yaml` is now the single
  theme source.
- Overview and Rooms view YAML deduplicated — `recipes-5view.md` Recipes 8–9
  are the single source; `dashboard-system.md` keeps design rationale.
- Token routing: `health-check-ref.md` split into five anchors (core path
  −14%), and the two largest view anchors split into design notes plus a
  separate `-scaffold` anchor so planning does not load generation YAML.
- Test dashboard is now a real smoke test — all 11 documented card types
  (was 8), with two defects fixed: a stale version string and an HBS footer
  that was not the last top-level card.


## v1.3 — 2026-06-05

### Architecture — token optimisation

**SKILL.md reduced from 2162 → 937 lines (−57%).**
All content preserved — reorganised for on-demand loading rather than always-in-context.

**New reference files:**
- `health-check-ref.md` — extracted from §9. Contains full parse template (Steps 1–5),
  structural pattern examples, colour scan exclusions, entity scan rules, finding
  categories, output format, tone guides, and partial YAML handling.
- `recipes-5view.md` — extracted from `recipes-extended.md`. Contains Recipes 7–14:
  5-view outer scaffold + per-view card YAML for Overview, Rooms, Scenes, Activity,
  Settings, Energy extension, Music extension.

**Content moved to existing reference files:**
- `dashboard-system.md` — full-dashboard workflow (Steps 1–6), device-type profiles
  table, sections view anatomy diagram, multi-view design rules, panel view.
- `bubble-card-ref.md` — touch target sizing table, performance notes
  (`background_update` deprecation, cover_background, auto_order, Streamline JS lag).
- `typography-ref.md` — font-only update variable list (`ha-font-family-*`,
  all `paper-font-*`, `primary-font-family`) with diff delivery format.
- `streamline-ref.md` — two-block delivery format (Block 1: template, Block 2: usage).

**`recipes-extended.md` restructured:**
- Recipes 7–14 moved to `recipes-5view.md`
- Core Recipes 1–6 (room pop-up, HBS, media player, climate, chip bar, Streamline)
  retained alongside room pop-up patterns
- Recipe 1–6 anchor format standardised to `## #anchor` style

**SKILL.md changes:**
- §2 UX Principles: Type B subsections (full-dashboard workflow, device-type profiles,
  sections anatomy, multi-view design, panel view) replaced with compact summaries +
  pointers; Type C subsections (progressive disclosure, touch targets, state colour,
  mobile-first, information density) trimmed in place
- §3b, §5, §6: compressed to route-only stubs pointing to reference files
- §7: Recipe 0 retained inline; Recipes 1–6 pointer to `recipes-extended.md`;
  Recipes 7–14 pointer to `recipes-5view.md`
- §8: 4 redundant pitfall entries removed (covered by Iron Law); cross-skill
  handoffs compressed to table; performance notes moved to `bubble-card-ref.md`
- §9: replaced with 3-line pointer to `health-check-ref.md`
- Stale text corrected: §2 header, §7 "same file" note, test-dashboard note,
  triple blank lines collapsed

### Fixes
- Two content gaps identified and filled during cross-check against v1.2:
  font-only update variable list (was missing from `typography-ref.md`),
  Streamline two-block delivery format (was missing from `streamline-ref.md`)
- Recipe 1–6 inline anchors `{#anchor}` converted to `## #anchor` format for
  consistency with rest of skill

---

---

## v1.2 — 2026-06-05

### Major additions

**5-view dashboard system** (`references/dashboard-system.md` — new file)
Complete information architecture for Home Assistant dashboards built on
principled UX foundations. Five views with defined purposes and engagement
types: Overview (complications), Rooms (brief interaction), Scenes (brief
interaction), Activity (passive review), Settings (deep engagement). Two
extension views: Energy (+E) and Music (+M) added when relevant.

**Activity view — hide/show graph mechanism**
Eight paired category sections in two groups — Home Activity (Presence, Doors
& Windows, Motion, Automation) and Home Health (Energy, Maintenance, Devices,
Infrastructure). Each category: Option C event card + Option B graph hidden
until tapped. Tap toggles an input_boolean; graph appears inline. Eight helpers
+ template sensor ha-yaml handoff block included.

**Recipes 7–14** (`references/recipes-extended.md`)
Eight new complete copy-paste YAML recipes covering the full 5-view system:
scaffold (R7), Overview (R8), Rooms (R9), Scenes (R10), Activity (R11),
Settings (R12), Energy extension (R13), Music extension (R14).

### §2 UX Principles — full rewrite

**Automate first** — new first principle replacing the 3-tier importance model.
The best dashboard control is the automation that makes the control unnecessary.
Includes optional opening question with explicit skip conditions.

**Engagement-type model** — four types sorted by interaction cost with Tier 0
(no UI — automation) as the explicit first filter. Table format with HA
equivalents and content rules.

**Full-dashboard design workflow** — six-step design-first process: collect →
classify (Buckets 0–3) → present classification → apply device-type profile →
generate from 5-view system → offer follow-up. Classification is always shown
to the user before YAML is generated. Claude never refuses a classification
decision — user has final say.

**Device-type profiles** — five-row lookup table replacing six separate
questions. One device type answer provides: max_columns, card_layout, font size,
nav pattern, theme mode.

### §9 Health-Check Mode (new section)

Audits existing dashboard YAML and returns a prioritised findings list.
Triggers on: "review my dashboard", "health check", "what's wrong with my YAML",
"audit", "improve this". Starts immediately without upfront questions — works
with partial YAML and notes coverage gaps at the end.

**Parsing strategy:** eight structural checks in sequence — view type, top-level
card placement, hardcoded colours, pop-up format, performance flags
(background_update, rise_animation), engagement-type mixing, automate-first
candidates, missing complications tier, structural best practices.

**Three severity tiers:**
- 🔴 Critical — Iron Law violations and broken functionality (hardcoded hex,
  pop-up inside sections, masonry view type, missing hash on pop-up)
- 🟡 Significant — materially degraded UX (mixed engagement types, theme on
  individual cards, deprecated pop-up format, background_update misuse)
- 🟢 Advisory — improvement opportunities (automate-first candidates, missing
  chip bar, 5-view alignment opportunity — always optional, never prescriptive)

**Consistent output format:** findings grouped by severity, each with location,
issue, and specific fix. Summary section always notes what is working correctly.

**Automate-first tone:** neutral — names the entity, notes what it typically
indicates, suggests the automation alternative, acknowledges the user may have
a reason for keeping it.

**5-view alignment:** Advisory only, never Critical or Significant. Framed as
an option with a concrete mapping of existing content to the 5-view structure.

**Process flowchart:** health-check trigger added as a top-level branch —
routes immediately to §9 without passing through the card/dashboard path.

---

### Common Pitfalls
New row: "I'll add a card for every device I have" → automate-first check.

### Reference files table
`dashboard-system.md` added. `recipes-extended.md` anchors updated R7–R14.

---

## v1.1 — 2026-05-30

### Added
- Complete Mushroom ↔ HA three-layer CSS integration (`mushroom-theme-ref.md`)
  with ZONE 6 accent-color-rgb bridge wiring all 12 palette recipes
- `references/typography-ref.md` — font loading methods, HA font variable
  catalogue, wall-panel size overrides, Alexandria self-hosting guide
- `references/recipes-extended.md` — security, energy, vacuum, bathroom,
  garage, office pop-up recipes and Streamline room templates
- `references/troubleshooting-ref.md` — 14 symptom sections
- `references/test-dashboard.yaml` — complete importable dashboard
- Bubble Card 3.2.2 source analysis: ~18 undocumented pop-up options
  documented (adaptive-dialog, correct bg_opacity/width_desktop defaults,
  empty-column card type, footer_mode, rise_animation, hide_gradient)
- Streamline Card 0.2.2 source analysis: areas context variable documented,
  !include tag confirmed in both UI-mode and YAML-mode
- Community forum findings pages 149–153: version corrections, HA 2026.4/2026.5
  compatibility notes, rows: key, sub-button font selectors, background_update
  v3.2.1 behaviour change, card-mod overflow clipping patterns
- Single-mode theme support documented for wall panels and kiosks
- Iron Law expanded to 6 rules
- Process flowchart condensed with troubleshooting-first gate
