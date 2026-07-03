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

---

## v1.4 — 2026-07-03

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
