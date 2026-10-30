# ha-bubble-dashboard — v1.4 development detail

Full working record of the v1.4 development passes. The summarised release
entry lives in `CHANGELOG.md`; this file preserves the detail for anyone
tracing why a specific decision was made.

---

## v1.4 — 2026-08-06

### Bubble Card version compatibility — v3.2.2 → v3.2.4

Skill was pinned to Bubble Card v3.2.2; updated against actual v3.2.4 source
(confirmed via `src/var/version.js` and official GitHub release notes for
v3.2.3 and v3.2.4).

**`bubble-card-ref.md`:**
- `#version-compat` table: added v3.2.3 row (smart entity/card suggestions,
  `close_action` fix for nested pop-up navigation, pop-up header colour-leak
  fix, iOS pop-up-visibility fix) and v3.2.4 row (standalone pop-ups now work
  reliably inside `vertical-stack`/`vertical-stack-in-card`; explicit editor
  warning for true pop-up-in-pop-up nesting; module-editor object-selector
  improvements for module developers — editor-only, not YAML-facing).
- Source header updated from v3.2.2 to v3.2.4.
- Added explicit rule: never nest a `card_type: pop-up` inside another
  pop-up's `cards:` block — unsupported at every version.

**`troubleshooting-ref.md`:**
- New `#nested-popup-warning` section distinguishing two symptoms that look
  similar but aren't: (1) true pop-up-in-pop-up nesting, always unsupported,
  fix is to use hash navigation instead; (2) pop-up nested inside a
  `vertical-stack`/`vertical-stack-in-card`, which was unreliable pre-v3.2.4
  and just needs an update.
- `#version-migration` table: added v3.2.4 row for the `vertical-stack-in-card`
  fix.

**`SKILL.md`:**
- Added `#nested-popup-warning` to both the troubleshooting quick-route table
  and the compact anchor list.

**Verification performed:** full scan of all card `editor.js` schema files in
actual (non-minified) v3.2.4 source against `bubble-card-ref.md` — no
undocumented YAML-facing options found; all previously-documented options
(`footer_mode`, `highlight_current_view`, `auto_order`, `close_by_clicking_outside`,
etc.) confirmed accurate against source. No new card types, no new visibility
condition types.

**Considered and deferred:** a dedicated Bubble Card module-authoring skill —
decided against as a separate skill; added as a reference file instead (below).

### Module authoring — correctness fix + new reference file

**Fixed factual errors in `bubble-card-ref.md#module-authoring`,** found by
diffing the section against the actual (non-minified) v3.2.4 module-system
source (`modules/parser.js`, `modules/utils.js`, `modules/export.js`):
- Removed a `variables:` key + `{{mustache}}` interpolation pattern that does
  not exist anywhere in Bubble Card's module system. The real mechanism is an
  `editor:` key (HA form-selector schema array) read back via
  `this.config.<module_id>?.<field_name>` inside the `code:` JS template —
  same access pattern as a card's `styles:` key.
- Removed `supported: [all]` — `'all'` is not a recognised literal anywhere in
  `getAvailableCardTypes()`. Applying a module to every card type means
  omitting `supported:` entirely.
- Section shortened to a quick-start (structure + corrected examples) and now
  points to the new `module-authoring-ref.md` for the full field catalog.

**New `references/module-authoring-ref.md`** — built from Bubble Card's own
bundled `src/modules/editor-schema-docs.md` (introduced alongside the v3.2.4
object-selector PR #2489), restructured and condensed rather than reprinted
verbatim:
- Full `editor:` field-type catalog (selector-based fields grouped as basic
  input / HA references / date-time / advanced, plus legacy type-based fields)
- Object selector in full, including the v3.2.4 additions: `group`/`group_icon`,
  `visible_if`/`warn_if`/`warn_text` (conditional fields), `variant_of`/`variant`
  (mutually-exclusive alternatives collapsed into one dropdown), `cluster_of`
  (visual-only grouping of independent fields)
- Grid and expandable-section layout
- A complete worked module example
- Module distribution/sharing formats (`#sharing-a-module`), sourced from
  `modules/export.js`'s `generateYamlExport`/`generateGitHubExport` — the
  plain-YAML download format and the exact GitHub Discussion markdown format
  the Module Store expects, with the quirks preserved (only the first
  `editor:` field appears in the inline example; `supported:` omitted when
  all cards apply; placeholder discussion link)

**Routing:** added to `SKILL.md`'s top-level decision tree and both reference
indexes. `bubble-card-ref.md#module-authoring` is read first for the module's
top-level structure; `module-authoring-ref.md` is only pulled in for the
`editor:` schema or the sharing/export format — keeping it out of context for
ordinary dashboard-generation requests, per the on-demand loading pattern from
v1.2→v1.3.

### Redundancy pass — `#modules` vs `#module-authoring`

Split ownership so each syntax pattern lives in exactly one place:
- `#modules` now owns *applying/excluding* a module (`modules:` key,
  `'!module_id'` exclusion) — trimmed its duplicate module-YAML-structure
  example, added a pointer to `#module-authoring` for writing one.
- `#module-authoring` now owns *writing* a module — dropped its duplicate
  "applying a module to a card" example, replaced with a one-line pointer
  back to `#modules`.
- Net: both sections shorter, no content lost, no pattern duplicated.

**`bubble_card_tools` version confirmed still current at `1.0.2`.**

---


### Full-scope review — structural optimisation + ecosystem alignment (2026-07-03)

**Structural (token footprint + one-source-of-truth):**
- Deleted `references/dashboard-recipes.md` (~50 KB) — verified 100% duplicate
  of content inside `dashboard-system.md`, referenced nowhere. Cross-check:
  chunk-level containment scan, 0 unique chunks.
- Deduplicated `dashboard-system.md#view-overview` and `#view-rooms`: full
  YAML removed (the refined copies in `recipes-5view.md` Recipes 8–9 are the
  single source), sections rewritten as design rationale + component notes +
  pointer. Cross-check: component/entity coverage scan confirmed Recipes 8–9
  are supersets; the one divergent placeholder (`sensor.lights_on_count` vs
  `binary_sensor.any_light_on`) noted in prose. Scenes/Activity/Settings/
  Energy/Music scaffolds intentionally remain in dashboard-system.md — their
  recipes summarise patterns and point here; that division is by design.

**Ecosystem alignment (researched against HA 2026.1–2026.7 release notes):**
- New `dashboard-system.md#native-first` — the native-first check (parallel
  to automate-first): battery grids → Maintenance dashboard, security logs →
  Security Activity list, weather forecasts → weather tile features, media
  transport → media tile features. Plus "when is a custom Bubble dashboard
  worth it?" positioning vs the native Home dashboard (default since 2026.2)
  and hybrid-setup guidance. Advisory tone throughout.
- New `dashboard-system.md#native-interop` — mixing native tile/heading/area
  cards into Bubble layouts: what inherits from the Casa5HeyneV2 theme, what
  doesn't (--bubble-* vars, modules), when native wins, visual grouping rules.
- New `health-check-ref.md` native-feature advisory category (Advisory only).
- New `streamline-ref.md#maintenance-status` — honest project-health note
  (single maintainer, decluttering-card lineage, graceful degradation path).
- New paid-module boundary rule in `module-authoring-ref.md#sharing-a-module`
  + Common Pitfalls row: never reproduce Patreon module code; explain, route,
  or author an original module instead.

**New capabilities:**
- `dashboard-system.md#entity-inventory` — Developer Tools → Template snippet
  producing an area-grouped, device-class-annotated entity list for the
  Collect step (one-off evaluation, within Iron Law scope).
- `dashboard-system.md#masonry-migration` — masonry → sections migration
  guide: don't-convert-in-place workflow, construct mapping table,
  card_layout re-check, verification pointers.
- `dashboard-system.md#wall-panel-hardening` — advisory notes: burn-in,
  screen-off automation handoff, kiosk-mode/Fully Kiosk pointers (named, not
  configured), dedicated non-admin user, stale-cache reliability.

**Routing & metadata:**
- SKILL.md: process-tree routes for masonry migration and native interop;
  §2 "Native first" subsection; Collect/Classify steps extended; two new
  Common Pitfalls rows; §8 Scope checklist items (native-first advisory,
  no paid-module reproduction); §6 project-health pointer; anchor lists
  updated; frontmatter TRIGGERS/SYMPTOMS extended; `ha_checked: 2026.7`.
- README: file tree completed (module-authoring-ref.md), coverage table
  extended (native interop, module authoring).
- available-skills-entry.md: new triggers (masonry migration, native-vs-
  custom decisions) and symptoms (rebuilding native features without
  advisory, reproducing paid module code).
- CHANGELOG: standing per-HA-release verification checklist added (above).


### Source-verified scan — Bubble Card v3.2.5 + Mushroom v5.2.2 (2026-08-06)

Full scan of both component source trees, not release notes or docs.

**Bubble Card v3.2.5 (released 2026-07-10):**
- Version pin raised 3.2.4 → 3.2.5; compat table row added.
- **Cover tilt support documented** — `tilt_buttons` (top/bottom/left/right/
  hidden), `open_tilt_service`, `close_tilt_service`, plus
  `cover_slider_type: position|tilt_position` for slider-driven tilt on both
  the card slider and slider sub-buttons. Includes the feature-detection rule
  (only emit tilt options when the entity reports OPEN_TILT / CLOSE_TILT /
  SET_TILT_POSITION) and two troubleshooting entries.
- Pop-up fixes noted: shared `hui-card` no longer hidden inside grid/masonry
  layout boundaries; improved shell detach on leaving editor mode.

**Method fix — the previous scan had a blind spot.** The v3.2.4 verification
checked editor schemas only, which misses every YAML option not surfaced in
the editor. A full `config.*` scan of the source found **24 undocumented
options**, now added:
- Slider: `slider_value_position`, `relative_slide`, `invert_slider_value`,
  `hue_force_saturation` + `hue_force_saturation_value`, `cover_slider_type`
- sub-buttons card: `menu_style`, `labels_below`, `hide_button_labels`,
  `compact_mode`, `space_between_buttons`, `footer_width` (with the
  `labels_below` requires `menu_style` gotcha)
- Calendar: `event_action`, `show_place`, `show_started_events`
- Core: `show_last_updated`, `sub_button_justify_content`
- Climate: `hide_temperature`

**Iron Law violation fixed in the skill's own example.** The calendar recipe
used `color: '#D9BE8B'`. Source shows `color:` resolves a colour *name* to
`var(--<name>-color)`, so `color: accent` is theme-compliant. Example
corrected, rule documented, Common Pitfalls row added.

**Mushroom v5.2.2 — two factual errors corrected:**
- `mush-rgb-state-switch` does not exist. Switch entities are coloured by
  `mush-rgb-state-entity`. Removed from docs and theme template.
- `mush-rgb-primary` does not exist. The accent bridge now wires
  `accent-color-rgb` into the specific state variables instead.
- Added the missing state groups: vacuum, media-player, lock (+ locked /
  unlocked / pending), number, humidifier, and update — including the
  upstream naming inconsistency (`mush-rgb-update-off` and
  `mush-rgb-update-installing` carry no `state-` segment).
- Five new Mushroom troubleshooting entries covering these traps.

**Theme divergence resolved.** `theme/Casa5HeyneV2.yaml` and
`references/casa5heynev2-template.yaml` had drifted: the shipped theme was
missing the entire ZONE 6 state mapping (45 keys) and its light mode lacked
every `mush-rgb-*` colour the dark mode had — meaning Mushroom silently fell
back to its own defaults in light mode. Both files are now aligned and
YAML-validated, with the corrected (non-existent-variable-free) ZONE 6.


### Tooling, coverage and honesty pass (2026-08-06)

**New: `verify.py`** — a dependency-light structural self-check, run from the
skill root. Eight checks, each of which exists because that bug class shipped
at least once: anchor integrity, SKILL.md anchor-list sync, YAML validity,
theme light/dark symmetry, banned (nonexistent) component variables, Iron Law
in card examples, version-string consistency, orphaned reference files. It
found five stale anchor-list entries and one version drift on first run.

**New: `references/eval-set.md`** — ten behavioural regression prompts with
MUST / MUST NOT criteria, run in fresh conversations. Until now every claim
that a release improved output quality was structural ("the guidance is in the
file"); this makes it testable and gives future versions a regression baseline.

**Theme de-duplication.** `references/casa5heynev2-template.yaml` deleted;
`theme/Casa5HeyneV2.yaml` is now the single source for both generation and
user installation, with all 10 references rewired. The two copies had already
drifted twice (ZONE 6 missing entirely from the shipped file, mode-specific
disabled greys differing) — the same failure mode as the deleted
`dashboard-recipes.md`. `verify.py`'s theme-symmetry check guards the
remaining risk.

**Test dashboard is now a real smoke test.** Extended from 8 to all 11
documented card types (added `calendar`, `select`, `empty-column`, plus a
tilt-enabled cover). Fixed two defects found while doing so: the file claimed
skill v1.5, and the HBS footer was not the last top-level card — the file
violated a rule the skill itself enforces.

**Entity domain map extended.** Added `siren`, `remote` and `lawn_mower` (a
Bubble Card toggle domain with a built-in icon, previously absent), and
documented `valve`, `water_heater`, `todo` and `image` as having no Bubble
Card support with the native-card fallback. Added the explicit toggle/slider
domain lists from v3.2.5 source, so unsupported domains produce an honest
answer rather than a control that renders but silently does nothing.

**Accessibility — limits stated plainly.** New subsection in §2: Bubble Card's
div-based controls are not screen-reader operable, sliders expose no role or
value, tap targets are generally outside the tab order, and pop-ups do not
trap focus. No card option fixes this, so the guidance is to say so and offer
native tile cards, voice/Assist or automation instead. Explicit instruction
never to claim WCAG conformance on the basis of the contrast checks.

**Localisation.** New §2 subsection: generate `name:` labels in the user's
language, keep navigation hashes ASCII, and let entity friendly names win
where a voice assistant is in use. Bubble Card localises its editor but not
dashboard labels — those come from generated YAML.

**Note on Sidebar Card:** a project-health section was considered for parity
with Streamline's new `#maintenance-status`, but `sidebar-ref.md#known-issues`
already covers maintenance status, both known issues and the Bubble
sub-buttons fallback. No change made.


### Process routing rebuilt — Signal Scan layer (2026-08-06)

**Diagnosis.** A traceability audit of the ten eval cases found that the
process tree routes on *output type* ("what card is being built"), while seven
of ten failure modes are *input signals* — properties of the request that are
invisible from the output type: the user's language, a stated accessibility
need, a feature native HA already covers, an unsupported entity domain. Those
seven relied on always-in-context prose being noticed rather than on routing.
Two of them (language, accessibility) had no trigger keyword anywhere.

**New: Signal Scan** — a nine-row table ahead of the process tree, scanned
before answering, orthogonal to output type and explicitly multi-select. Each
row states the signal and the action, and the section closes with the rule
that no signal is ever a refusal: they add a sentence or a question, never
withhold output.

**Process tree completed.** The output-type branch was missing four documented
card types entirely — `calendar`, `select`, `separator` and `sub-buttons` had
no route at all (the same coverage gap the test dashboard had). Added, plus a
tilt pointer on `#cover` and a new branch for requests that describe a
*situation* rather than a card type, which previously had no handling.

**Common Pitfalls trimmed 17 → 13 rows.** The four rows that were really
intake signals (battery/security/forecast sections, automate-first,
paid modules, wall-panel single-mode) moved into the Signal Scan, where they
fire proactively instead of relying on the model catching itself mid-mistake.

**Result:** actively routed eval cases went from 3/10 to 10/10.
Cost: +557 tokens on SKILL.md (+3.9%), the always-in-context file — a
deliberate trade, since the routing layer is what makes the other 130k tokens
of reference material reachable at all.

**verify.py gained a routing-coverage check** (now 9 checks): every documented
card type must be reachable from the process tree, and every eval must declare
what it tests. Negative-tested — removing the calendar route makes it fail.

