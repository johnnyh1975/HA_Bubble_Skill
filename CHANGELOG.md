# ha-bubble-dashboard — Changelog


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
