---
name: ha-bubble-dashboard
description: >
  Home Assistant dashboard design with Bubble Card 3.x, Streamline Card, Sidebar Card and Mushroom — including a merged HA/Bubble/Mushroom CSS theme with colour intelligence, palette recipes, WCAG checks, typography, wall-panel support and full troubleshooting.
  
  TRIGGERS: Bubble Card (any card type), Lovelace dashboards, CSS themes, colour palettes, fonts, Streamline templates, Sidebar Card nav, Mushroom chips, room pop-ups, wall panels, troubleshooting.
  
  SYMPTOMS: hardcodes hex in YAML · uses pre-v3.2 pop-up format · places pop-up or HBS inside sections: · generates themes from scratch · uses masonry view · skips UI-mode question for Streamline · omits JS font loader · generates automations instead of navigate actions.

metadata:
  version: 1.3
  bubble_card: "3.2.1"   # 3.2.2 is a patch on top; 3.2.1 is the stable base
  streamline_card: "0.2.2"
  sidebar_card: "0.1.9.9"
  bubble_card_tools: "1.0.2"
  ha_minimum: "2024.3.0"
---

# HA Dashboard UX

Reference skill for building Home Assistant dashboards using Bubble Card, Streamline
Card, and Sidebar Card — with the Casa5HeyneV2 merged HA/Bubble Card theme as the
CSS foundation.

---

## The Iron Law

```
COLOURS:    Never hardcode hex in card YAML. Always var(--ha-variable) → theme file.
POP-UPS:    Always use v3.2+ standalone format with cards: block. No separate stacks.
TEMPLATES:  Read bubble-card-ref.md before generating any Bubble Card YAML.
THEMES:     Output is a .yaml theme file for /config/themes/ — not inline card styles.
DASHBOARD:  Ask UI-mode vs YAML-mode before using Streamline Card !include syntax.
PLACEMENT:  Pop-ups and HBS footer are top-level view cards ONLY — never inside sections:
```

These six rules prevent 95% of errors. Violating any of them produces YAML that
either silently breaks or conflicts with the theme architecture.

**Note — light/dark mode:** Both modes is the default recommendation, not a law.
Single-mode themes are correct for wall panels, kiosk setups, and fixed displays.
Ask before generating both modes: see §3a for the decision question.

---

## The Process

```
User request
    │
    ├── repair / debug / "not working"? → troubleshooting-ref.md (see anchor table below)
    ├── font / typography?              → typography-ref.md#architecture first
    ├── colour / palette?               → §3a + colour-intelligence-ref.md#two-modes
    │                                     Ask: wall panel? → single-mode
    ├── "review/audit/health check/     → §9 Health-Check Mode — parse YAML,
    │    what's wrong with my YAML?"      deliver findings immediately, no upfront questions
    └── card / dashboard / navigation?  → continue ↓

Identify output type
  ├── Pop-up           → bubble-card-ref.md#version-compat + #pop-up
  ├── Button / slider  → bubble-card-ref.md#button
  ├── Media player     → bubble-card-ref.md#media-player
  ├── Climate / cover  → bubble-card-ref.md#climate or #cover
  ├── HBS footer       → bubble-card-ref.md#horizontal-buttons-stack
  ├── Sidebar Card     → sidebar-ref.md#known-issues + #combined-example
  ├── Streamline       → ask UI-mode or YAML-mode first, then streamline-ref.md
  ├── Room pop-up      → check recipes-extended.md for matching room type
  └── Full dashboard   → §2#full-dashboard-workflow (classify first, then generate)
                         Ask: wall panel? → single-mode + size overrides
                         5-view system → dashboard-system.md → Recipes 7–14 (recipes-5view.md)

Entity domain unclear?  → bubble-card-ref.md#entity-domain-map
UI-mode or YAML-mode?   → ask if Streamline or full dashboard
Mobile / desktop / both? → ask if full dashboard or nav question
Generate → checklist (§8) → deliver
```

**Troubleshooting quick-route** (read troubleshooting-ref.md anchor):

| Symptom | Anchor |
|---------|--------|
| Theme not applying | `#theme-not-applying` |
| Pop-up not opening | `#popup-not-opening` |
| Streamline "not found" | `#streamline-not-found` |
| Sidebar not showing | `#sidebar-not-showing` |
| Styling ignored | `#bubble-styling-ignored` |
| Broke after update | `#version-migration` |
| HBS not reordering | `#hbs-not-ordering` |
| Layout wrong | `#sections-layout-issues` |
| Font not loading | `typography-ref.md#font-troubleshooting` |
| Unknown | `#general-diagnostic-checklist` |

---

## Common Pitfalls

| Thought | Reality |
|---------|---------|
| "This is v3.1 pop-up format, it's fine" | CHECK. v3.2 migrated all pop-ups. Generate the standalone format with cards: always. |
| "I'll use card-mod to style this Bubble Card" | AVOID. Use styles: in the card YAML or a Bubble Card module instead. |
| "subButtonIcon[0] is the first main sub-button" | WRONG since v3.1. Bottom sub-buttons are indexed first. Main sub-buttons come after. |
| "I'll use !include_dir_named for Streamline templates" | ASK FIRST. Only works in YAML-mode Lovelace. UI-mode users get a parse error. |
| "The template is added, let's move on" | NOTE. Streamline revalidates templates in the background after the first page load — most edits propagate automatically. If a template doesn't appear, hard-refresh first. HA restart only if the Streamline card resource is missing entirely. |
| "The HA default styling module is required" | NO. It is optional. The skill outputs a merged theme file that handles Bubble ↔ HA alignment. |
| "Sidebar Card has no issues on HA 2026" | CAUTION. bottomCard has an intermittent setConfig bug. showTopMenuOnMobile behaviour changed in HA 2026.1. Test after install. |
| "Clicking a button inside pop-up A should open pop-up B directly" | CHANGED in v3.2.x. Navigating from one open pop-up to another now closes the first pop-up — a second tap is required to open the next. Workaround: add a dismiss button to each pop-up, or use `close_by_clicking_outside: false` to prevent accidental dismissal while navigating. |
| "I swapped the accent, Bubble Card updated but Mushroom is still blue" | EXPECTED without ZONE 6 update. Set `accent-color-rgb: "NR,NG,NB"` in the mode-independent block so `mush-rgb-primary` picks up the new accent. |
| "I'll generate both light and dark mode for this wall panel" | ASK FIRST. Fixed-display setups (wall panels, kiosks) need single-mode themes. Generating both wastes maintenance surface and risks accidental mode switching. |
| "I'll just update the font variables in the theme" | INCOMPLETE. Font changes also require a JS loader file at /config/www/ and an extra_module_url entry in configuration.yaml. Theme variables alone have no effect without the loader. |
| "I'll generate automations for this dashboard button" | STOP. Send the user to ha-yaml for the automation. Only generate the navigate tap_action here. |
| "A button card is fine for this fan/vacuum/lock" | CHECK. Use bubble-card-ref.md#entity-domain-map first — complex domains need sub-button patterns, not a plain switch button. |
| "I'll add a card for every device I have" | STOP. Ask whether automation already handles it. The dashboard is for what automation cannot do — every unnecessary card competes for attention with the ones that matter. |

---

## Reference Files

Read the relevant file BEFORE generating YAML. Every anchor is reachable.

**bubble-card-ref.md** — any Bubble Card YAML:
`#version-compat`★ · `#pop-up` · `#button` · `#sub-buttons` · `#horizontal-buttons-stack` · `#media-player` · `#climate` · `#cover` · `#select` · `#separator` · `#calendar` · `#sub-buttons-only` · `#css-variables` · `#js-templates` · `#modules` · `#module-authoring` · `#actions` · `#entity-domain-map`★

**css-theme-ref.md** — theme colour YAML:
`#var-chain`★ · `#ha-vars` · `#bubble-vars` · `#light-mode` · `#dark-mode` · `#how-to-swap-accent` · `#full-palette-swap` · `#theme-file-structure` · `#mushroom-vars` · `#app-header-vars` · `#font-size-vars`

**typography-ref.md** — font or typography change:
`#architecture`★ · `#loading-methods` · `#ha-variables` · `#size-system` · `#alexandria` · `#font-only-update` · `#swap-recipes` · `#single-mode-themes` · `#font-troubleshooting`

**streamline-ref.md** — Streamline templates:
`#ui-mode-vs-yaml-mode`★ · `#template-anatomy` · `#variable-syntax` · `#javascript-keys` · `#dry-decision` · `#file-organisation` (incl. `!include` tag + background revalidation) · `#known-limitations` · `#bubble-card-interaction`

**sidebar-ref.md** — Sidebar Card config:
`#known-issues`★ · `#installation` · `#main-options` · `#width-breakpoints` · `#sidebar-menu` · `#template-messages` · `#style` · `#bottom-card` · `#combined-example`

**colour-intelligence-ref.md** — palette or accent:
`#two-modes`★ · `#casa5-profile` · `#wcag-checks` · `#harmony-rules` · `#bring-your-own-accent` · `#advisory-conversation-flow` · `#accent-swap-recipes` · `#full-palette-recipes` · `#full-palette-recipes-dark`

**mushroom-theme-ref.md** — Mushroom Cards theming:
`#architecture`★ · `#ha-bridge` · `#state-mapping` · `#colour-palette` · `#structure-vars` · `#integration-block` · `#palette-swap-impact` · `#card-override-limits` · `#accent-colour-for-switches` · `#chip-card` · `#template-chip`

**casa5heynev2-template.yaml** — base for all theme generation. Never reconstruct from scratch.

**test-dashboard.yaml** — complete importable dashboard assembling Recipes 0–5. Recipes 1–6 are in `recipes-extended.md`. Use to verify YAML validity or as a starter dashboard.

**troubleshooting-ref.md** — when something is broken:
`#cache-issues`★ · `#theme-not-applying` · `#popup-not-opening` · `#streamline-not-found` · `#sidebar-not-showing` · `#bubble-styling-ignored` · `#version-migration` · `#hbs-not-ordering` · `#sections-layout-issues` · `#sub-buttons-not-showing` · `#card-state-stale` · `#font-not-loading` · `#popup-z-index` · `#cardmod-overflow-clipping` · `#general-diagnostic-checklist`★

**dashboard-system.md** — architecture, workflow, device profiles, view YAML:
`#system-overview`★ · `#navigation-layer` · `#classification-output` · `#full-dashboard-workflow` · `#device-type-profiles` · `#sections-anatomy` · `#multi-view-design` · `#panel-view` · `#view-overview` · `#view-rooms` · `#view-scenes` · `#view-activity` · `#view-settings` · `#extension-energy` · `#extension-music`

**recipes-extended.md** — room pop-up patterns + core recipes 1–6:
`#security-popup` · `#energy-view` · `#vacuum-popup` · `#presence-panel` · `#bathroom-popup` · `#garage-popup` · `#office-popup` · `#streamline-templates-extended` · `#recipe-1-room-popup` · `#recipe-2-hbs` · `#recipe-3-media-player` · `#recipe-4-climate` · `#recipe-5-chip-bar` · `#recipe-6-streamline`

**recipes-5view.md** — 5-view scaffold + per-view card YAML:
`#recipe-7-5view-scaffold` · `#recipe-8-overview` · `#recipe-9-rooms` · `#recipe-10-scenes` · `#recipe-11-activity` · `#recipe-12-settings` · `#recipe-13-energy-ext` · `#recipe-14-music-ext`

★ = always read this anchor first for this file type

## §1 Installation & Prerequisites

> No reference file needed for installation steps — all content is in this section.

### Required components (all via HACS)

| Component | Type | HACS search term | Min version |
|-----------|------|-----------------|-------------|
| Bubble Card | Frontend | `Bubble Card` | 3.2.0 |
| Bubble Card Tools | Integration | `Bubble Card Tools` | 1.0.2 |
| Streamline Card | Frontend | `Streamline Card` | 0.2.2 |
| Sidebar Card | Frontend | custom repo: `https://github.com/DBuit/sidebar-card` | 0.1.9.9 |

> **Sidebar Card** is not in the default HACS catalogue. Add it as a custom
> repository: HACS → ⋮ → Custom repositories → URL above → Category: Frontend.

### Optional components — enhance theme integration

| Component | Type | HACS search term | Adds |
|-----------|------|-----------------|------|
| Mushroom | Frontend | `Mushroom` | Chip cards, compact entity cards. Fully integrated with the Casa5HeyneV2 theme via the Mushroom ↔ HA ZONE 6 bridge. Without it, mushroom-theme-ref.md applies only if Mushroom is already installed. |

> **Mushroom is not required** for Bubble Card dashboards. Install it only if
> you want Mushroom chip bars or entity cards alongside Bubble Card. If installed,
> the theme handles state colour integration automatically via the ZONE 6 block.

### Installation order

1. Install **Bubble Card** via HACS → Frontend. Clear browser cache.
2. Install **Bubble Card Tools** via HACS → Integrations. Restart HA. Add the
   integration: Settings → Devices & Services → Add Integration → "Bubble Card Tools".
   This creates `/config/bubble_card/modules/` for module YAML files.
3. Install **Streamline Card** via HACS → Frontend. After install, copy the example
   template file:
   ```
   /config/www/community/streamline-card/streamline_templates.example.yaml
     → rename to →
   /config/www/community/streamline-card/streamline_templates.yaml
   ```
   Clear browser cache and restart HA. This is the auto-load path for UI-mode users.
4. Install **Sidebar Card** via HACS → Frontend (custom repo). Add the JS resource:
   Settings → Dashboards → ⋮ → Resources → Add → `/hacsfiles/sidebar-card/sidebar-card.js`
   → JavaScript Module.
5. Create the **font loader file** at `/config/www/alexandria-font.js`.
   See `typography-ref.md#alexandria` for the exact file content (CDN and
   self-hosted variants). This file is separate from the theme YAML — both
   are required for the font to load.
6. Add the **Casa5HeyneV2 theme** (or your merged theme YAML) to `/config/themes/`.
   In `configuration.yaml` add (if not already present):
   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
     extra_module_url:
       - /local/alexandria-font.js    # loads the font created in step 5
   ```
   Restart HA after editing `configuration.yaml`.
   Reload themes: Developer Tools → Actions → `frontend.reload_themes`.
7. Set the theme: Profile → Theme → select your theme name.
8. **(Optional) Install Mushroom** via HACS → Frontend if you want Mushroom chip
   cards. After install, **restart HA** — the ZONE 6 Mushroom integration is not
   hot-reloaded. The state colour mapping activates after restart.

### What you get without Bubble Card Tools

Bubble Card Tools enables the Module Editor and Module Store in the Bubble Card UI
editor. Without it, Bubble Card still works fully — you just cannot install or create
modules through the UI. Modules can be written manually as YAML and placed in
`/config/bubble_card/modules/` if the integration is installed.

### What Streamline Card does not support

- Visual editor in the HA dashboard UI (always shows "Visual editor not supported")
- Template inheritance (templates are self-contained, no base template chaining)
- `!include_dir_named` in UI-mode Lovelace dashboards (YAML-mode only)

---

## §2 UX Principles

> **UX workflow + 5-view system:** `dashboard-system.md` · **Layout issues:** `troubleshooting-ref.md`
> **Full dashboard design workflow:** `§2#full-dashboard-workflow` — run this before generating any full dashboard.
> **5-view system:** `dashboard-system.md` — architecture + workflow + view YAML · `recipes-5view.md` — Recipes 7–14

These rules govern every dashboard decision. Read before designing any layout.

---

### Automate first

**The best dashboard control is the automation that makes the control unnecessary.**

Before adding a card for any device, ask whether automation already handles it —
or should. A motion sensor that triggers lights does not need a card. Blinds that
close at sunset do not need a button. A climate schedule that runs on time does
not need a manual override on the main view.

The dashboard is for what automation genuinely cannot handle: conscious choices,
contextual overrides, things users deliberately decide in the moment. Everything
else should run silently in the background.

This is not a philosophical preference — it is a practical design rule. Every
unnecessary card on a dashboard competes for attention with the cards that matter.
The result is a dashboard users stop looking at because looking at it costs more
than it returns.

**When Claude applies this:**
Claude raises the automate-first question when starting a full dashboard from
scratch, when a user lists devices without any filtering, or when a request would
produce a card for something that is clearly automation-territory (motion sensors,
time-based covers, scheduled climate).

Claude does NOT raise it when: the user has already made explicit card decisions,
the user is adding to an existing dashboard, the user says "just build it", or
the context makes clear the user is a power user who has already automated what
they want automated.

**The optional opening question** — ask once at the start of a full-dashboard
request when the user's intent is unclear:

> "Before I generate the dashboard: are there devices you're planning to add
> mainly because they could be controlled manually, even though automation
> handles most of what they do? It helps keep the result focused — we can
> always add more later."

If the user engages → run the classification workflow (§2#full-dashboard-workflow).
If the user says "just build it" → build it, applying the engagement-type model
silently to produce a well-structured result without debate.

---

### The engagement-type model

The right question for every card is not "how important is this device?" but
"what type of engagement does this actually need?" — and the first answer is
always whether it needs any UI at all.

| Engagement type | Interaction cost | HA equivalent | Content rule |
|---|---|---|---|
| **No UI at all** | Zero — automated | Automation / script | Everything a human doesn't need to decide |
| **Complications** | Zero — passive | Chip bar, Overview view | State that informs without requiring action |
| **Brief interaction** | One tap, seconds | Room button → pop-up | Things adjusted manually, regularly |
| **Deep engagement** | Multi-step, minutes | Secondary view | History, config, scenes, rarely-changed settings |

**The first question for every card:** does this belong in row 1 — should it be
automated instead? The dashboard only contains what automation cannot handle, or
what users consciously choose to control manually.

**Never mix engagement types on the same surface.** Complications lose their
peripheral quality when surrounded by interactive controls. Brief-interaction
controls get ignored when buried next to deep-engagement content. Each view in
the 5-view system has exactly one engagement type — this is why the system works.

---

### Full-dashboard design workflow

> Read `dashboard-system.md#full-dashboard-workflow` for the complete 6-step process (Collect → Classify → Present → Profile → Generate → Offer).

Steps in brief:
1. **Collect** — entity list, primary device, fixed display?
2. **Classify** — sort every entity into Bucket 0 (automate) / 1 (complications) / 2 (brief interaction) / 3 (deep engagement). Full bucket definitions: `dashboard-system.md#full-dashboard-workflow`.
3. **Present** — show classification to user before writing any YAML. Never refuse based on it — user has final say.
4. **Profile** — apply device-type profile (`dashboard-system.md#device-type-profiles`)
5. **Generate** — map buckets to 5-view structure (`dashboard-system.md#classification-output`)
6. **Offer** — "Want the Activity/Settings view?" + "Want Bucket 0 automation suggestions?"

---

### Device-type profiles

> Full table: `dashboard-system.md#device-type-profiles`

| Device | max_columns | card_layout | Font | Nav | Theme mode |
|---|---|---|---|---|---|
| Phone | 2 | large | 14px | HBS only | Both |
| 10" wall tablet | 3 | large | 16px↑ | HBS + sidebar | Single-mode |
| Desktop | 4 | normal | 14px | Sidebar + HBS | Both |
| e-ink | 2 | large | 16px↑ | HBS only | Single-mode light |
| Phone + desktop | 3 | large | 14px | HBS + sidebar (hidden mobile) | Both |

Wall tablet / e-ink → always ask single-mode. Wall tablet font bump → also set Mushroom sizes separately (`typography-ref.md#size-system`).

---

### Progressive disclosure via pop-ups

Pop-ups are the primary progressive disclosure mechanism — group all room controls behind one button. Sizing rules: `bubble-card-ref.md#pop-up`.

- Default desktop width: `560px`
- `popup_mode: fit-content` for simple single-entity pop-ups
- `popup_mode: centered` for cameras or complex layouts
- Always `with_bottom_offset: true` when HBS footer is present

---

### Navigation patterns

| Scenario | Pattern |
|----------|---------|
| Mobile primary | HBS footer only |
| Desktop primary | Sidebar Card |
| Both equally | HBS footer + Sidebar Card (`mobile: 0, tablet: 0, desktop: 20`) |

Default "both equally": HBS is primary nav, Sidebar Card desktop-only, `is_sidebar_hidden: true` on HBS.

5-view nav: HBS buttons link to `/lovelace/view-path`, not pop-up hashes. No `auto_order`, no `_pir_sensor`.

---

### Touch target sizing

> Full table: `bubble-card-ref.md#touch-targets`

Never reduce HBS buttons (48px), sub-buttons main (36px), or slider track (44px) with custom CSS.

---

### State colour feedback

Variables live in the theme — never override with hardcoded values:
- On → `state-active-color` (→ `accent-color`)
- Off → `state-inactive-color` (8% black / 10% white)
- Unavailable → icon dims to `disabled-text-color` — show dimmed, never hide
- RGB sliders → `--bubble-range-fill` tracks light colour — do not override with static colour

---

### Mobile-first layout rules

- View type: always `sections`. Never `masonry`.
- `max_columns`: 2 mobile / 3 tablet+desktop / 4 desktop-only
- `card_layout: large` for primary controls; `normal` for secondary/info cards
- Avoid horizontal-stack with more than 2 cards — wrapping is unpredictable on narrow screens

---

### Information density

- Max 6–8 interactive elements per view before introducing pop-ups
- Use `card_type: separator` with icon to divide pop-up content into named sections
- `show_state: true` only when state adds meaning beyond icon (temperature, media title)
- Sub-buttons for secondary info (battery, last-changed) — they don't compete with primary control

---

### Naming conventions

- Pop-up hash: lowercase hyphenated — `'#living-room'` not `'#LivingRoom'`
- HBS button order: most-occupied rooms first; use `auto_order: true` with `_pir_sensor`
- Card names: match entity friendly name — no dashboard-specific aliases

---

### Sections view anatomy

> Full structure diagram + column_span table: `dashboard-system.md#sections-anatomy`

Key rules:
- Pop-ups → top-level `cards:` entries, before `sections:` block — never inside sections
- HBS → last top-level `cards:` entry — never inside sections
- `section type: grid` always for Bubble Card content
- `column_span` on the section, not the card

---

### Accessibility

**Motion sensitivity (wall panels):**
- No CSS `animation:`/`transition:` > 300ms on always-on displays
- Never `rise_animation: true` on HBS for wall panels

**Icon + label redundancy:**
- Never rely on colour alone to convey state — icon shape or label text must also differ

**Font size at distance:**
- Wall panels viewed at 1.5m+ → `ha-font-size-body: "16px"` in theme, `card_layout: large` on all primary cards

**Voice assistant alignment:**
- `name:` must match entity friendly name — dashboard aliases break voice commands

---

### When to use Streamline Card templates

Apply the DRY rule: 3+ identical card structures with only variable substitutions → extract a template. See `streamline-ref.md#dry-decision`.

---

### Multi-view design + Panel view

> `dashboard-system.md#multi-view-design` · `dashboard-system.md#panel-view`

Single view with pop-ups is valid for simple homes. Add views only when:
- 8–10+ room buttons (split into zones)
- Domain needs always-visible display (cameras)
- Different user groups need different primary views

`type: panel` → single card fills entire screen. Use for kiosk tablets, full-screen nav panels, picture-elements overlays.

---

## §3a CSS Theme — Colour

> **Read before starting:** `css-theme-ref.md#var-chain` → `#ha-vars` → `#how-to-swap-accent` or `#full-palette-swap`
> **For palette decisions:** `colour-intelligence-ref.md#two-modes` → `#wcag-checks` → `#harmony-rules` → `#accent-swap-recipes` or `#full-palette-recipes`
> **For Mushroom integration:** `mushroom-theme-ref.md#integration-block` → `#palette-swap-impact`
> **For generation:** use `references/casa5heynev2-template.yaml` as the base — never reconstruct from scratch.

The theme is the single source of truth for all colours. Card YAML never
contains colour values — it inherits everything through the var() chain.

### Single-mode vs both-modes — ask first

Before generating any theme, determine the display context:

```
Is this dashboard for a fixed display?
(wall panel / kiosk / tablet always-on / e-ink)
    │ yes → single-mode theme
    │         → Ask: light or dark?
    │         → Use only modes.light or modes.dark block
    │         → See typography-ref.md#single-mode-themes for structure
    │ no  → both modes (default)
    │         → Full template with modes.light + modes.dark
```

**Signals that single-mode is correct:**
- User mentions "wall panel", "kiosk", "always on", "mounted tablet"
- User says "I only ever use dark mode" / "I never use dark mode"
- User describes an embedded or offline HA installation
- HA Companion App with theme locked in Profile settings

**Default:** if the user doesn't specify, generate both modes and note that
single-mode is available for fixed displays.

### The delivery contract

Every colour-related output from this skill is a complete `.yaml` file
delivered for `/config/themes/`. Never deliver:
- Inline `style:` blocks with hex values on individual cards
- Partial theme snippets without the full var() chain intact
- `--bubble-*` overrides with hardcoded hex in card YAML

### How to approach a colour/palette request

```
User asks for colour/palette change
    │
    ▼
Single-mode or both? (see above)
    │
    ▼
Advisory or prescriptive? (see colour-intelligence-ref.md#two-modes)
    │
    ├── Advisory  → present palette table from #accent-swap-recipes
    │               wait for user choice
    │               generate complete theme YAML
    │
    └── Prescriptive → map user description to a recipe
                       generate complete theme YAML
                       state the recipe chosen and its WCAG scores
    │
    ▼
Accent-only, background-only, or full palette?
    │
    ├── Accent only      → 8 lines per mode + Zone 6 accent-color-rgb
    ├── Background only  → Zone 2 + Zone 5 only (see colour-intelligence-ref.md#advisory-conversation-flow)
    └── Full palette     → all zones per mode (see css-theme-ref.md#full-palette-swap)
    │
    ▼
Run WCAG pre-flight (colour-intelligence-ref.md#wcag-checks):
  1. New accent on light card (#FFFFFF or new card bg) ≥ 3:1?
  2. New accent on dark card (#252B38 or new card bg) ≥ 3:1?
  3. Text (#555A60 or new text) on new card bg ≥ 7:1?
  4. New accent visually distinct from #FA7575 warning?
    │
    ▼
Deliver complete Casa5HeyneV2-derived theme YAML
Tell user: filename, where to place it, reload_themes action, profile selection
```

### Naming generated themes

Ask the user for a theme name before generating. If not provided, use:
`Casa5HeyneV2-{RecipeName}` — e.g. `Casa5HeyneV2-Slate.yaml`.

The theme key in YAML must match the filename (without `.yaml`) exactly —
this is what appears in Profile → Theme.

### Preserving the non-colour structure

When generating a full theme, always carry forward verbatim:
- All typography variables (mode-independent block)
- All structural variables (`ha-card-border-radius`, `mdc-shape-*`, `mdc-icon-size`)
- All Bubble Card var() mappings (mode-independent block)
- All Mushroom state mapping and structure variables (mode-independent block)
- `warning-color: "#FA7575"` — do not change this

Only the colour zones change (accent lever + optional background zones).

---

## §3b CSS Theme — Typography

> **Read before starting:** `typography-ref.md#architecture`
> **Font swap:** `typography-ref.md#swap-recipes`
> **Custom font from scratch:** `typography-ref.md#loading-methods` + `#ha-variables`
> **Wall-panel sizes:** `typography-ref.md#size-system`
> **Font-only update lines:** `typography-ref.md#font-only-update` — exact variable list + diff format
> **Single-mode themes:** `typography-ref.md#single-mode-themes`

Typography changes are independent of colour changes and can be combined or handled separately.

**In scope when:** user asks to change font · wall panel needs larger text · font looks different across devices · headings vs body font · new theme from scratch.

**Mushroom font sizing — not inherited from HA:**
Mushroom has its own size variables. If bumping `ha-font-size-body` for a wall panel, also set:
```yaml
mush-card-primary-font-size:   "15px"   # default 14px
mush-card-secondary-font-size: "13px"   # default 12px
mush-chip-font-size:           "0.35em" # default 0.3em
```

**Font delivery always requires three things:** JS loader file at `/config/www/` + `extra_module_url` entry in `configuration.yaml` + theme variable changes. See `typography-ref.md#loading-methods` for exact file content. Remind user: restart HA, then hard-refresh browser.

**Before generating, ask if not specified:**
- Local font files (offline, no FOUT) or Google Fonts CDN (easier)?
- For existing Alexandria users: complete new file, or just the changed lines?

---

## §4 Bubble Card

> **Always read first:** `bubble-card-ref.md#version-compat`
> **Card type unknown?** `bubble-card-ref.md#entity-domain-map`
> **Then read the card-specific anchor** from the decision tree below before generating YAML.

Read `references/bubble-card-ref.md` before generating any Bubble Card YAML.

### Card type decision tree

```
What entity domain / use case?
    │
    ├── light / switch / input_boolean / script / scene → button
    │     ├── needs brightness slider? → button_type: slider
    │     └── needs toggle?           → button_type: switch
    │
    ├── climate                       → climate card
    ├── cover / blind                 → cover card
    ├── media_player                  → media-player card
    ├── input_select / select         → select card
    ├── sensor / display only         → button (button_type: state)
    ├── section divider / header      → separator
    ├── navigation hub / footer nav   → horizontal-buttons-stack
    ├── chip bar / sub-button-only    → sub-buttons (hide_main_background: true)
    ├── calendar                      → calendar
    ├── modal detail / room controls  → pop-up (standalone, cards: block)
    │
    └── fan / vacuum / lock / alarm / camera / humidifier /
        number / timer / counter / person / weather / update
        → bubble-card-ref.md#entity-domain-map (full table + sub-button patterns)
```

**Rule: if the domain is not in the abbreviated list above, always consult
`bubble-card-ref.md#entity-domain-map` before generating.** The full table
covers 25 domains — guessing from training data produces wrong card types.

### card_layout decision guide

| Value | When to use | Visual |
|-------|-------------|--------|
| `normal` | Secondary info cards, sensors, compact views | Small — icon + name on one line |
| `large` | Primary room controls, HBS-adjacent cards, wall panels | Tall — icon top, name + state below; finger-sized |
| `large-2-rows` | Cards with long state text or two-line labels | `large` height with a second text row |
| `large-sub-buttons-grid` | Cards whose sub-buttons need a 2-column grid layout | `large` height with sub-buttons arranged in a grid |

**Default rule:** use `large` for all primary control cards (lights, covers, climate).
Use `normal` for secondary / informational cards (sensors, last-changed displays).
Only use `large-2-rows` or `large-sub-buttons-grid` when the content specifically
requires it — avoid them as defaults since they push more content off-screen.

### Sub-button decision

Add sub-buttons when the card needs to show secondary information or quick
actions without opening a pop-up:
- Battery level on a sensor card → `main` sub-button, `show_attribute: true`
- Quick scene triggers below a room button → `bottom` sub-button group
- HVAC mode selector on climate card → `main` sub-button, `select_attribute: hvac_modes`

Never use sub-buttons to recreate the primary control — the primary control
belongs on the card body itself.

### Pop-up composition rules

1. Always standalone v3.2+ format — never inside a stack
2. Start with a `separator` card as the first content item
3. Group controls by device type within the pop-up using separators
4. Max ~8–10 cards inside a pop-up before considering a sub-view instead
5. Set `with_bottom_offset: true` whenever an HBS footer is present
6. Use `width_desktop: "560px"` as the default — override only for camera/map

### Modules vs styles:

| Use case | Approach |
|----------|----------|
| Reusable CSS applied to many cards | Bubble Card module (in bubble_card/modules/) |
| One-off CSS tweak on a single card | `styles:` key in card YAML |
| Dynamic colour or icon based on state | `styles:` with JS template |
| Never | card-mod on a Bubble Card |

---

## §5 Sidebar Card

> **Always read first:** `sidebar-ref.md#known-issues` — health status and HA 2026.x caveats
> **Then:** `sidebar-ref.md#installation` → `#width-breakpoints` → `#combined-example`
> **Clock + fallback patterns:** `sidebar-ref.md#template-messages` · `sidebar-ref.md#bottom-card`

Read `references/sidebar-ref.md` before generating any Sidebar Card config.

**Default for "both equally" targets:** include Sidebar Card, desktop-only (`mobile: 0, tablet: 0, desktop: 20`).
Pair with HBS footer for mobile. Set `is_sidebar_hidden: true` on HBS when Sidebar Card is present.

**Before delivering, confirm:**
- HA ≥ 2024.3 (sections view compatibility)
- User aware of `bottomCard` reliability issue → add warning comment if they use it
- HA 2026.x → advise testing `showTopMenuOnMobile` after install

**If `bottomCard` issues are persistent:** offer the HBS-only fallback pattern from `sidebar-ref.md#bottom-card`.

---

## §6 Streamline Card

> **Always read first:** `streamline-ref.md#ui-mode-vs-yaml-mode` — must ask before generating
> **Then:** `streamline-ref.md#template-anatomy` → `#variable-syntax` → `#dry-decision`
> **JS templates:** `streamline-ref.md#javascript-keys` — [[variable]] substitution-before-evaluation gotcha
> **Delivery format:** `streamline-ref.md#delivery-format` — always two labelled blocks (template + usage)

Read `references/streamline-ref.md` before generating any Streamline config.

**Mandatory first question** — ask before writing any template YAML:
> "Are your Lovelace dashboards managed through the HA UI, or do you use YAML-mode with a `ui-lovelace.yaml` file?"

- UI-mode → templates to `streamline_templates.yaml` only; usage YAML separate for dashboard editor
- YAML-mode → may use `!include` and `!include_dir_named`; split files for many templates

Remind user to clear browser cache after adding new templates.

---

## §7 Recipes

> **Core recipes (1–6):** `recipes-extended.md` · **5-view recipes (7–14):** `recipes-5view.md`
> — Recipe 0 (scaffold) is below. Recipes 1–6 are in `recipes-extended.md#recipe-1-room-popup` through `#recipe-6-streamline`. Recipes 7–14 are in `recipes-5view.md`.
> — Room pop-up patterns (security, energy, vacuum, presence, bathroom, garage) are in `recipes-extended.md`.

Recipe 0 is the outer view wrapper — always start here for a full dashboard.
All YAML uses the Casa5HeyneV2 var() chain — no hardcoded colours.
Replace placeholder entity IDs (e.g. `light.living_room`) with real entities.

### Recipe 0 — Complete single-view dashboard scaffold

The outer wrapper every dashboard needs. Pop-ups go in `cards:` at the view
level. HBS footer is always the last card. Sections contain all other cards.

```yaml
# Dashboard title matches the theme name — set in HA dashboard settings
views:
  - title: Home
    path: home
    type: sections
    max_columns: 3          # 3 = works on tablet + desktop, wraps on mobile
    cards:

      # ── Pop-ups (always top-level, before sections) ──────
      # REPLACE: update hash, name, icon, entity to match your rooms
      - type: custom:bubble-card
        card_type: pop-up
        hash: '#living-room'         # REPLACE: '#your-room-name'
        name: Living Room            # REPLACE: your room name
        icon: mdi:sofa               # REPLACE: your room icon
        width_desktop: "560px"
        with_bottom_offset: true
        cards:
          # pop-up content cards here (see Recipe 1)

      - type: custom:bubble-card
        card_type: pop-up
        hash: '#kitchen'             # REPLACE
        name: Kitchen                # REPLACE
        icon: mdi:chef-hat           # REPLACE
        width_desktop: "560px"
        with_bottom_offset: true
        cards:
          # pop-up content cards here

      # ── Sections (the visible card grid) ─────────────────
      sections:

        # Section 1 — full-width header row (chip bar)
        - type: grid
          column_span: 3          # span all 3 columns = full width
          cards:
            - type: custom:bubble-card
              card_type: sub-buttons
              hide_main_background: true
              sub_button:
                bottom:
                  - name: Chips
                    buttons_layout: inline
                    justify_content: flex-start
                    group:
                      - entity: sensor.living_room_temperature
                        show_state: true
                        show_icon: true
                        fill_width: false
                        show_background: true

        # Section 2 — room control buttons
        - type: grid
          column_span: 2
          cards:
            - type: custom:bubble-card
              card_type: button
              button_type: name
              name: Living Room
              icon: mdi:sofa
              entity: light.living_room_group
              card_layout: large
              button_action:
                tap_action:
                  action: navigate
                  navigation_path: '#living-room'

            - type: custom:bubble-card
              card_type: button
              button_type: name
              name: Kitchen
              icon: mdi:chef-hat
              entity: light.kitchen_group
              card_layout: large
              button_action:
                tap_action:
                  action: navigate
                  navigation_path: '#kitchen'

        # Section 3 — secondary info (1 column)
        - type: grid
          column_span: 1
          cards:
            - type: custom:bubble-card
              card_type: climate
              entity: climate.living_room
              name: Climate
              card_layout: large

      # ── HBS Footer (always last card in view) ──────────────
      - type: custom:bubble-card
        card_type: horizontal-buttons-stack
        auto_order: true
        highlight_current_view: true
        is_sidebar_hidden: true
        1_name: Living Room
        1_icon: mdi:sofa
        1_link: '#living-room'
        1_entity: light.living_room_group
        1_pir_sensor: binary_sensor.living_room_motion
        2_name: Kitchen
        2_icon: mdi:chef-hat
        2_link: '#kitchen'
        2_entity: light.kitchen_group
        2_pir_sensor: binary_sensor.kitchen_motion
```

**column_span rules:**
- `column_span: 3` on a `max_columns: 3` view = full width
- `column_span: 2` = two-thirds width (desktop), full width (mobile auto-wrap)
- `column_span: 1` = one-third width (desktop), full width (mobile)
- Pop-ups do NOT go inside `sections:` — they are top-level `cards:` before the sections block
- HBS does NOT go inside `sections:` — it is a top-level `cards:` entry after sections

## §8 Pitfalls & Pre-Output Checklist

> **Something broken?** Go to `references/troubleshooting-ref.md` first — symptom → cause → fix tables.
> **Version issues?** `bubble-card-ref.md#version-compat` and `troubleshooting-ref.md#version-migration`

### Pre-output checklist — run before delivering any YAML

**Colour & theme**
- [ ] Single-mode vs both-modes: wall panel / kiosk → single mode; general → both
- [ ] No hex values in card YAML — only `var(--ha-variable)` references
- [ ] Theme output is a complete `.yaml` file based on `casa5heynev2-template.yaml`
- [ ] Accent lever chain complete — all 8 opacity variables updated
- [ ] Mushroom sync: `accent-color-rgb` updated in mode-independent block (ZONE 6)
- [ ] `warning-color: "#FA7575"` preserved unchanged
- [ ] Text contrast ≥ 7:1 on new card background (if backgrounds changed)
- [ ] New accent ≥ 3:1 on both light and dark card backgrounds

**Typography (only if font was changed)**
- [ ] JS loader file content delivered — complete, ready to place in `/config/www/`
- [ ] `configuration.yaml` `extra_module_url` entry shown
- [ ] All legacy `paper-font-*` variables included in theme
- [ ] `primary-font-family` updated in both `modes.light` and `modes.dark`
- [ ] Wall-panel size override applied if fixed-display context (`ha-font-size-body: "16px"`)
- [ ] If Mushroom + wall panel: `mush-card-primary-font-size` set separately (does not inherit from ha-font-size-body)
- [ ] User reminded: restart HA, then hard-refresh browser

**Dashboard structure (sections view)**
- [ ] View type is `sections`, not `masonry`
- [ ] Pop-ups are top-level `cards:` entries — NOT inside `sections:` block
- [ ] HBS footer is the LAST top-level `cards:` entry — NOT inside `sections:`
- [ ] `column_span` set correctly on sections (max_columns value = full width)
- [ ] `section type: grid` used for all sections containing Bubble Cards

**Pop-ups**
- [ ] Pop-up is a standalone top-level card with `cards:` block (v3.2+)
- [ ] Pop-up is NOT inside a `horizontal-stack`, `vertical-stack`, or `sections:`
- [ ] `with_bottom_offset: true` set when HBS footer is present
- [ ] Hash is lowercase, hyphenated, e.g. `'#living-room'`
- [ ] Extended recipe consulted for security / energy / vacuum / bathroom / garage rooms

**Bubble Card general**
- [ ] No `card-mod` applied to Bubble Cards
- [ ] `subButtonIcon[N]` index accounts for v3.1+ bottom-first ordering
- [ ] No reference to `bubble-pop-up-fix.js`
- [ ] Card type matches the entity domain — complex domains checked in `#entity-domain-map`
- [ ] RGB lights: `supported_color_modes` checked before generating hue/saturation sliders

**Streamline Card**
- [ ] UI-mode vs YAML-mode clarified before generating template config
- [ ] Template + usage YAML delivered in two clearly labelled blocks
- [ ] User reminded to clear browser cache and restart HA after adding templates

**Sidebar Card**
- [ ] Config is at root of dashboard YAML, not inside `views:`
- [ ] Width set to `mobile: 0, tablet: 0` for "both equally" targets
- [ ] `bottomCard` usage flagged with known reliability warning
- [ ] Fallback HBS-only pattern offered if user reports bottomCard issues

**Scope**
- [ ] No automations generated — navigate tap_action only
- [ ] No helpers or template sensors generated
- [ ] Out-of-scope items redirected to `ha-yaml` or `ha-best-practices`

### Cross-skill handoffs

| Request type | This skill | ha-yaml skill |
|---|---|---|
| Button `tap_action` (navigate / call-service on existing entity) | ✓ Generate it | — |
| Automation triggered by button press or state change | Tell user to use ha-yaml; provide entity_id + desired action + service | ✓ |
| Template sensor needed for a card display value | Generate card with `sensor.placeholder_name` + comment | ✓ Create the sensor |
| Timer, sequence, condition logic behind a button | navigate tap_action only | ✓ Everything else |

When handing off to ha-yaml, always provide: entity_id to trigger from, desired action, service to call (e.g. `scene.turn_on`).
When a card needs a template sensor, use `sensor.placeholder_name` with comment `# Replace with template sensor from ha-yaml skill`.


### Additional pitfall reference

See the Common Pitfalls table at the top of this file (Thought / Reality format).
That table covers the most frequent failure modes in one place.

### Performance notes

> See `bubble-card-ref.md#version-compat` for pop-up lazy-loading, `background_update` deprecation, cover_background, auto_order, and Streamline JS performance notes.

## §9 Health-Check Mode

> **Trigger:** user pastes existing dashboard YAML and asks for a review, audit,
> or says "what's wrong with my dashboard", "health check", "improve this",
> "review my YAML", or similar.
> **Do not trigger** for new dashboard generation — use §2#full-dashboard-workflow.

Read `references/health-check-ref.md` in full before proceeding.
Complete the structured parse (Step 1) before generating any findings.
Deliver findings using the output format in that file — never free-form prose.
