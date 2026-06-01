# ha-bubble-dashboard — Changelog

---

## v1.6 — 2026-05-30

### Community forum findings — Bubble Card thread pages 151–153

- `bubble-card-ref.md#version-compat` — version pin corrected to 3.2.1 (stable
  release confirmed in forum). HA 2026.4 and 2026.5 compatibility notes added:
  2026.4 changed section row gaps (ha-view-sections-row-gap); 2026.5 broke visual
  editor fields (fixed in Bubble Card v3.2.1+).
- `bubble-card-ref.md` — `rows:` key documented in button options table. Decimal
  values (e.g. `rows: 1.4`) allow fine-grained card height control between
  card_layout presets.
- `bubble-card-ref.md#pop-up` — `sub_button:` added to pop-up options table.
  v3.2.1 automatically shows pop-up header when sub-buttons are configured.
- `bubble-card-ref.md#css-variables` — sub-button font size CSS selectors
  documented: `.bubble-sub-button` and `.bubble-sub-button-bottom-container
  .bubble-sub-button` for per-row font size control.
- `bubble-card-ref.md#modules` — Patreon modules section added: Bubble Badges v2,
  Bubble Weather, Bubble Calendar Enhanced, Bubble Neon, Custom Dropdown. Guidance
  on how to handle Patreon modules in the skill (acknowledge, do not generate).
  Community module pointer (Bubble Graph Pro, GitHub Discussions).
- `css-theme-ref.md` — `ha-view-sections-row-gap` added to structural variables
  table with HA 2026.4 change note and override pattern.
- `troubleshooting-ref.md#sections-layout-issues` — section row gap row added for
  HA 2026.4 ha-view-sections-row-gap change.
- `troubleshooting-ref.md#popup-not-opening` — two-tap pop-up navigation row
  added (v3.2.x behaviour change), card-mod overflow clipping pointer added.
- `troubleshooting-ref.md#cardmod-overflow-clipping` — new symptom section for
  card border-radius/box-shadow clipping inside pop-ups caused by global card-mod
  `overflow: hidden` rules. CSS workaround and Bubble Card module alternative.
- `SKILL.md Common Pitfalls` — two-tap pop-up navigation pitfall row added.
- `SKILL.md §8 Performance notes` — background_update note updated for v3.2.1:
  intelligent lazy loading now default; manual background_update: true no longer
  needed and may cause redundant updates.

---
## v1.5 — 2026-05-29

### Fixed
- `test-dashboard.yaml` structural bug: `sections:` now correctly sits as a sibling
  of `cards:` at the view level. HBS card placed inside `cards:` list. YAML validates
  clean. HOW TO USE section now covers both UI-mode and YAML-mode users.
- `SKILL.md §3a` broken anchor: `css-theme-ref.md#wcag-checks` corrected to
  `colour-intelligence-ref.md#wcag-checks` (WCAG checks have always been in
  colour-intelligence-ref, not css-theme-ref).
- `colour-intelligence-ref.md` section order: `#two-modes` and
  `#advisory-conversation-flow` moved to the top (before all recipe blocks)
  so the workflow-entry sections are reachable without scrolling.
- `SKILL.md §7 Recipe 6` — REPLACE comments added to all entity ID placeholders
  in the Streamline usage block, matching the convention established in Recipe 0.
- `SKILL.md §1 step 5` — inline font loader JS replaced with a pointer to
  `typography-ref.md#alexandria`. Eliminates duplicate CDN URL that would need
  updating in two places.
- `sidebar-ref.md#known-issues` — HA 2026.x `hideHassSidebar` workaround added:
  use `hideHassSidebar: false` + CSS in the extra_module_url JS file to hide
  native sidebar elements.
- `troubleshooting-ref.md` — shared `#first-steps` block added at the top covering
  hard refresh, browser console, and HA logs. Duplicated steps removed from
  `#theme-not-applying` and `#general-diagnostic-checklist`.

---
## v1.4 — 2026-05-29

### Added
- `references/test-dashboard.yaml` — complete importable Lovelace dashboard
  assembling Recipes 0–5: sensor chip bar, room nav button, climate cards,
  media player, HBS footer. All entity IDs marked with REPLACE comments.
  Can be used to validate YAML structure after recipe changes.
- `mushroom-theme-ref.md#template-chip` — full template chip documentation:
  all fields, worked examples (alarm state, presence count, active lights,
  theme-aware icon colour), colour value reference.
- `SKILL.md §4` — card_layout decision guide: when to use normal / large /
  large-2-rows / large-sub-buttons-grid with visual result descriptions.
- `SKILL.md §2` — panel view type documented: type: panel for wall panels
  and kiosk dashboards, when to use and when not to.
- `typography-ref.md#alexandria` — variable font approach: single woff2 file
  covering all weights (font-weight: 100 900), simpler than 5 separate files.
  Includes @font-face example for variable font self-hosting.

### Fixed
- `colour-intelligence-ref.md` — orphaned anchor #full-palette-recipes (continued)
  renamed to #full-palette-recipes-dark. All references updated.
- `colour-intelligence-ref.md` — added "user supplies specific hex" row to
  advisory mood→recipe table, pointing to #bring-your-own-accent.
- `SKILL.md` process flowchart — full dashboard branch now asks wall-panel vs
  general before routing to Recipe 0, ensuring single-mode + size overrides
  are applied from the start.
- `SKILL.md §1` step 8 — Mushroom install note now states HA restart required;
  ZONE 6 Mushroom integration is not hot-reloaded.
- `SKILL.md` Recipe 0 — entity IDs now have REPLACE comments and routing note
  to Recipe 1 for pop-up content, reducing copy-paste errors.
- `css-theme-ref.md#theme-file-structure` — skeleton replaced with a clean
  pointer to casa5heynev2-template.yaml. Eliminates redundant parallel structure.
- `SKILL.md` process flowchart — condensed from 55 to 35 lines without losing
  routing logic. Troubleshooting sub-tree moved to a compact table.
- `SKILL.md` Reference Files section — converted from 10 verbose anchor tables
  to compact inline lists. Saved ~80 lines; all anchors preserved with ★ markers.
- SKILL.md token count reduced from ~16,800 to ~15,700 (~7% reduction).

---
## v1.3 — 2026-05-29

### Added
- `references/mushroom-theme-ref.md` — complete Mushroom ↔ HA three-layer
  integration reference: architecture, HA RGB bridge (Layer 2c), full
  mush-rgb-state-* domain mapping (Layer 2b, 22 variables), complete base
  colour palette (Layer 2a), integration block, palette swap impact guide,
  card-level override limits, accent-for-switches patterns.
- `references/typography-ref.md` — complete font reference: three loading
  methods (CDN, self-hosted, system stack), full HA font variable catalogue
  (modern + legacy paper-font-* block), wall-panel size overrides, Alexandria
  profile, 4 swap recipes (Inter, Geist, DM Sans, system stack), single-mode
  theme structure, font troubleshooting.
- `references/casa5heynev2-template.yaml` — Mushroom integration block added
  to mode-independent section: ZONE 6 (accent-color-rgb + mush-rgb-primary),
  all 22 mush-rgb-state-* mappings, semantic aliases, structure vars wired to
  HA card variables. Both modes gained mush-rgb-disabled and complete palette
  including previously-missing mush-rgb-light-grey, dark-grey, light-green.
- `SKILL.md §3` — split into §3a (CSS Theme — Colour) and §3b (CSS Theme —
  Typography). §3a gained single-mode vs both-modes decision gate as first
  sub-section. §3b covers font delivery format, decision questions, and
  font-only update pattern.
- `SKILL.md` Iron Law — note added clarifying combined light/dark is a
  recommendation not a law. Single-mode is correct for fixed displays.
- Process flowchart — font/typography branch added before colour branch.
  Wall-panel/single-mode decision added. Troubleshooting font-not-loading
  routes to typography-ref#font-troubleshooting.
- Mushroom chip card documentation in mushroom-theme-ref.md.
- Bubble Card + Mushroom side-by-side worked example.
- HA mode-selection explanation in typography-ref#single-mode-themes.
- DevTools CSS variable inspection step in troubleshooting-ref diagnostic checklist.
- Mushroom wall-panel font sizing note in §3b and §8 checklist.
- Font Recipe 2 (Geist) now fully specified with complete variable block.
- Self-hosting guide for Alexandria specifically in typography-ref#alexandria.

### Fixed
- All 12 palette recipes (6 accent + 6 full palette) in colour-intelligence-ref.md
  now include ZONE 6 accent-color-rgb line for Mushroom sync.
- Triple-c typo in mushroom-theme-ref.md (#acccent → #accent).
- Stale §3 reference in §2 accessibility (→ §3a).
- font-not-loading in troubleshooting-ref now defers to typography-ref#font-troubleshooting
  rather than maintaining a parallel table.
- §1 Installation: Mushroom Cards added as optional component, font loader
  creation step added.
- Process flow "new/modified theme" branch simplified — single-mode decision
  consolidated into §3a.
- "Preserving non-colour structure" note in §3a updated to reflect Mushroom
  state mapping now in mode-independent block.
- available-skills-entry.md SYMPTOMS aligned with SKILL.md canonical set.

---
## v1.2 — 2026-05-29

### Structural fixes
- Process flowchart: added troubleshooting branch as first gate, routing to all 10
  troubleshooting-ref.md anchors by symptom type. Added recipes-extended.md route
  for room-specific requests. Added entity-domain-map step for unclear domains.
- Iron Law: added Law 6 (PLACEMENT) — pop-ups and HBS must be top-level view cards.
- Common Pitfalls: 3 new rows — sections: placement, Streamline cache reminder,
  entity-domain-map check for complex domains. Table now 13 rows.
- §4 decision tree: explicit redirect to #entity-domain-map for 12 complex domains
  (fan, vacuum, lock, alarm, camera, humidifier, number, timer, counter, person,
  weather, update). Rule added: never guess from training data.
- Reference table: recipes-extended.md fully listed with 8 anchors. Troubleshooting
  anchors expanded to 10. colour-intelligence anchors expanded to 8.
- SYMPTOMS blocks: SKILL.md expanded to 15 items (canonical). available-skills-entry
  expanded to 12 items. Both now cover: sections placement, cache reminder,
  entity-domain-map, template file, masonry view, deprecated fix.js.

### Content depth additions
- css-theme-ref.md: 4 new sections — full Mushroom RGB catalogue (20 colours +
  4 semantic aliases), app-header/sidebar variable table, HA 2025+ font-size
  variables with wall-panel override pattern, remaining state/badge/switch vars.
- troubleshooting-ref.md: 4 new symptom sections — sub-buttons not showing,
  card state stale, font not loading, pop-up z-index issues. Now 271 lines.
- bubble-card-ref.md: RGB/colour-temperature light handling guide with 4-slider
  pattern and supported_color_modes check. Full conditional visibility section
  with 5 condition type examples. Camera entity note (use picture-entity for live).
- §5 Sidebar Card: HBS-only fallback pattern when Sidebar Card issues are a
  dealbreaker. Includes chip-bar context panel as sidebar substitute.
- §8 Checklist: expanded from 18 to 28 items. New sections view block (5 items),
  extended recipe item, RGB light check, entity-domain-map check, template file
  check, fallback offer item.
- §2 UX Principles: multi-view dashboard design guidance — when to split views,
  linking views from HBS, sub-view pattern, HA native sub-views.
- colour-intelligence-ref.md: Rule 7 (dark-mode accent brightness). New
  #bring-your-own-accent section with hex→RGB conversion and 4-step template.
  Advisory flow: background-only swap path added. #accent-swap-recipes updated
  with cross-reference to #bring-your-own-accent.
- recipes-extended.md: #streamline-templates-extended section with Streamline
  templates for bathroom, garage, office device, and security lock patterns.
  Usage examples for repeated room types (3 bathrooms, 2 garages).
- CHANGELOG: update triggers table added.

### Infrastructure
- casa5heynev2-template.yaml: all German comments translated to English.
  Line-number references in header replaced with search-by-comment-text
  instructions (drift-proof). All 9 ZONE markers verified intact.


## v1.1 — 2026-05-28

### Added
- `references/troubleshooting-ref.md` — symptom → cause → fix tables for all
  common failure modes: theme not applying, pop-up not opening, Streamline
  template not found, sidebar not showing, styling ignored, version migration,
  HBS ordering issues, sections layout issues, general diagnostic checklist
- `references/recipes-extended.md` — 6 additional room recipes: security
  pop-up (camera + lock + alarm), energy view, vacuum control pop-up, person/
  presence panel, bathroom, garage, home office
- `references/casa5heynev2-template.yaml` — canonical pre-populated theme
  template with ZONE markers for palette swaps. Use as base for all theme
  generation — never reconstruct from scratch.
- `bubble-card-ref.md#entity-domain-map` — full entity domain → Bubble Card
  type mapping table covering 25 domains including fan, vacuum, alarm,
  lock, camera, humidifier, number, timer, counter. Sub-button patterns
  for complex domains.
- `bubble-card-ref.md#module-authoring` — complete module authoring guide:
  YAML structure, global vs scoped, variables system, when to use modules
  vs styles:
- `colour-intelligence-ref.md#advisory-conversation-flow` — scripted 3-step
  advisory conversation: elicitation → shortlist → generate. Mood-to-recipe
  mapping table for prescriptive mode.
- `colour-intelligence-ref.md` — Full Palettes 4–6: Midnight Slate, Dusk
  Mauve, Midnight Steel — completing the full palette set for all 6 accent
  recipes.
- `streamline-ref.md#bubble-card-interaction` — Streamline + Bubble Card
  interaction patterns: [[variable]] substitution timing rule, sub_button
  templating, navigation_path as variable, cards_javascript for dynamic
  lists, known gotchas.
- `SKILL.md` — Sections view anatomy section in §2 explaining view structure,
  column_span rules, where pop-ups and HBS must live.
- `SKILL.md` — Accessibility sub-section in §2: motion sensitivity, icon+
  label redundancy, wall-panel font sizing, voice assistant name alignment.
- `SKILL.md` — Recipe 0: complete single-view dashboard scaffold with sections
  structure, pop-up placement, and HBS footer positioning.
- `SKILL.md` — Expanded reference table: all 47 anchors across 5 reference
  files now cited with when-to-use conditions. Anchor call-outs added to
  every §N section header.
- `SKILL.md` — Cross-skill handoff section in §8.

### Fixed
- Reference table previously cited only 9 of 47 anchors — now all 47 listed.
- `css-theme-ref.md#theme-file-structure` was a skeleton — replaced by the
  canonical `casa5heynev2-template.yaml` file.
- `bubble-card-ref.md` missing entity domains: fan, vacuum, alarm_control_panel,
  lock, camera, humidifier, number, input_number, timer, counter, event.

### Component versions pinned
- Bubble Card: 3.2.2
- Bubble Card Tools: 1.0.2
- Streamline Card: 0.2.2
- Sidebar Card: 0.1.9.9
- HA minimum: 2024.3.0

---

## v1.0 — 2026-05-28 (initial)

- SKILL.md: metadata, iron law, process, pitfalls table, §§1–8
- bubble-card-ref.md: all card types, CSS variables, JS API, version compat
- css-theme-ref.md: var() chain map, light/dark catalogues, swap templates
- streamline-ref.md: template anatomy, variable syntax, JS keys, UI/YAML modes
- sidebar-ref.md: all options, menu config, known issues, combined example
- colour-intelligence-ref.md: Casa5 profile, WCAG checks, harmony rules,
  6 accent recipes (A–F), 3 full palette recipes (1–3)
- available-skills-entry.md: system prompt trigger block

---

## Update triggers — watch these for next skill revision

Update this skill when any of the following occur. Check release notes for
breaking changes before updating — do not assume backwards compatibility.

| Component | Watch for | Key risk |
|-----------|-----------|----------|
| **Bubble Card** next release (v3.3+) | New card types, changed option names, pop-up mode additions | Sub-button schema changes; new `card_layout` values; CSS variable renames |
| **Bubble Card Tools** update | Module system changes, new module store entries | Module YAML structure changes; new `is_global` or `variables` behaviour |
| **Streamline Card** past v0.2.2 | Template syntax changes, `!include` support improvements | `[[variable]]` syntax changes; new `_javascript` context variables |
| **Sidebar Card** new active release | Any version past v0.1.9.9 | `bottomCard` bug fix status; `showTopMenuOnMobile` HA 2026.x fix |
| **HA 2025.x / 2026.x** | Sections view API changes, new theme variables, mobile dashboard overhaul | New `column_span` behaviour; new `ha-font-size-*` variables; sidebar nav changes |
| **Casa5HeyneV2 theme** upstream update | New variables added, var() chain restructured | New `--bubble-*` mappings; Mushroom RGB variable additions |

**Minimum update checklist when a component updates:**
1. Read the full release notes / changelog for the component
2. Check `#version-compat` in bubble-card-ref.md — add new breaking changes
3. Update `metadata:` version pins in SKILL.md
4. Run through all recipes in §7 and recipes-extended.md — validate YAML still correct
5. Update this CHANGELOG with a new version entry
