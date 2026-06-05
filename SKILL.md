---
name: ha-bubble-dashboard
description: >
  Home Assistant dashboard design with Bubble Card 3.x, Streamline Card, Sidebar Card and Mushroom — including a merged HA/Bubble/Mushroom CSS theme with colour intelligence, palette recipes, WCAG checks, typography, wall-panel support and full troubleshooting.
  
  TRIGGERS: Bubble Card (any card type), Lovelace dashboards, CSS themes, colour palettes, fonts, Streamline templates, Sidebar Card nav, Mushroom chips, room pop-ups, wall panels, troubleshooting.
  
  SYMPTOMS: hardcodes hex in YAML · uses pre-v3.2 pop-up format · places pop-up or HBS inside sections: · generates themes from scratch · uses masonry view · skips UI-mode question for Streamline · omits JS font loader · generates automations instead of navigate actions.

metadata:
  version: 1
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
                         5-view system → dashboard-system.md → Recipes 7–14

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
| "I'll set bubble-accent-color to #D9BE8B" | WRONG. Set accent-color in the theme file. --bubble-accent-color must point to var(--primary-color). |
| "I'll put the pop-up in a vertical-stack" | FORBIDDEN. Pop-ups (v3.2+) are standalone top-level cards, never inside stacks. |
| "I'll put the pop-up inside sections:" | FORBIDDEN. Same rule — pop-ups and HBS must be top-level cards: entries, not inside the sections: block. |
| "This is v3.1 pop-up format, it's fine" | CHECK. v3.2 migrated all pop-ups. Generate the standalone format with cards: always. |
| "I'll use card-mod to style this Bubble Card" | AVOID. Use styles: in the card YAML or a Bubble Card module instead. |
| "subButtonIcon[0] is the first main sub-button" | WRONG since v3.1. Bottom sub-buttons are indexed first. Main sub-buttons come after. |
| "I'll use !include_dir_named for Streamline templates" | ASK FIRST. Only works in YAML-mode Lovelace. UI-mode users get a parse error. |
| "The template is added, let's move on" | NOTE. Streamline revalidates templates in the background after the first page load — most edits propagate automatically. If a template doesn't appear, hard-refresh first. HA restart only if the Streamline card resource is missing entirely. |
| "The HA default styling module is required" | NO. It is optional. The skill outputs a merged theme file that handles Bubble ↔ HA alignment. |
| "I'll hardcode the card background in the card YAML" | WRONG. All colours flow from the theme file via var() chains. |
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
`#architecture`★ · `#loading-methods` · `#ha-variables` · `#size-system` · `#alexandria` · `#swap-recipes` · `#single-mode-themes` · `#font-troubleshooting`

**streamline-ref.md** — Streamline templates:
`#ui-mode-vs-yaml-mode`★ · `#template-anatomy` · `#variable-syntax` · `#javascript-keys` · `#dry-decision` · `#file-organisation` (incl. `!include` tag + background revalidation) · `#known-limitations` · `#bubble-card-interaction`

**sidebar-ref.md** — Sidebar Card config:
`#known-issues`★ · `#installation` · `#main-options` · `#width-breakpoints` · `#sidebar-menu` · `#template-messages` · `#style` · `#bottom-card` · `#combined-example`

**colour-intelligence-ref.md** — palette or accent:
`#two-modes`★ · `#casa5-profile` · `#wcag-checks` · `#harmony-rules` · `#bring-your-own-accent` · `#advisory-conversation-flow` · `#accent-swap-recipes` · `#full-palette-recipes` · `#full-palette-recipes-dark`

**mushroom-theme-ref.md** — Mushroom Cards theming:
`#architecture`★ · `#ha-bridge` · `#state-mapping` · `#colour-palette` · `#structure-vars` · `#integration-block` · `#palette-swap-impact` · `#card-override-limits` · `#accent-colour-for-switches` · `#chip-card` · `#template-chip`

**casa5heynev2-template.yaml** — base for all theme generation. Never reconstruct from scratch.

**test-dashboard.yaml** — complete importable dashboard assembling Recipes 0–5. Use to verify YAML validity after recipe changes, or as a starter dashboard for users.

**troubleshooting-ref.md** — when something is broken:
`#cache-issues`★ · `#theme-not-applying` · `#popup-not-opening` · `#streamline-not-found` · `#sidebar-not-showing` · `#bubble-styling-ignored` · `#version-migration` · `#hbs-not-ordering` · `#sections-layout-issues` · `#sub-buttons-not-showing` · `#card-state-stale` · `#font-not-loading` · `#popup-z-index` · `#cardmod-overflow-clipping` · `#general-diagnostic-checklist`★

**dashboard-system.md** — 5-view dashboard system:
`#system-overview`★ · `#navigation-layer` · `#view-overview` · `#view-rooms` · `#view-scenes` · `#view-activity` · `#view-settings` · `#extension-energy` · `#extension-music` · `#classification-output`

**recipes-extended.md** — room-specific patterns + 5-view recipes:
`#security-popup` · `#energy-view` · `#vacuum-popup` · `#presence-panel` · `#bathroom-popup` · `#garage-popup` · `#office-popup` · `#streamline-templates-extended` · `#recipe-7-5view-scaffold` · `#recipe-8-overview` · `#recipe-9-rooms` · `#recipe-10-scenes` · `#recipe-11-activity` · `#recipe-12-settings` · `#recipe-13-energy-ext` · `#recipe-14-music-ext`

★ = always read this anchor first for this file type

---

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

> No reference file for UX — all content is in this section and in `references/troubleshooting-ref.md` for layout issues.
> **Full dashboard design workflow:** `§2#full-dashboard-workflow` — run this before generating any full dashboard.
> **5-view system:** `references/dashboard-system.md` — complete architecture, view-by-view design, recipes 7–14.

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

Run this workflow whenever generating a full dashboard from scratch. It replaces
the old pattern of mapping every entity directly to a card.

**Step 1 — Collect**

Ask for (or infer from context):
- Entity list or room/device description
- Primary device: phone / tablet / desktop / both (→ device-type profile below)
- Fixed display? wall panel / kiosk → single-mode theme question

If the user hasn't listed entities: "List your devices or entity IDs — rooms,
sensors, lights, climate, media players, covers. Don't filter yet, just list
everything."

If the user says "build something typical" with no entities → use Recipe 0
placeholder entities and note that.

**Step 2 — Classify**

Sort every entity into one of four buckets. Do this before writing any YAML.

```
Bucket 0 — Automate, don't build
  binary_sensor.*_motion         → automation trigger, not a control
  binary_sensor.*_door/window    → state chip at most, never a control button
  binary_sensor.*_presence       → automation trigger
  Lights where motion sensor exists → suggest automation; keep manual override
                                    inside pop-up only, not on main view
  Covers with sun position logic → suggest automation; pop-up not main view
  sensor.* readings              → chip bar only, never a control card

Bucket 1 — Complications (chip bar / Overview view)
  Temperature / humidity sensors
  Presence indicators (person.*)
  Security state (alarm_control_panel.*)
  Weather sensor
  Active lights count (template sensor)
  Current power draw

Bucket 2 — Brief interaction (room button → pop-up)
  Room light groups
  Climate controls
  Media players
  Covers / blinds (manual override)
  Scenes users consciously trigger
  Locks (manual override)
  input_boolean.* representing real choices (guest mode, sleep mode)

Bucket 3 — Deep engagement (secondary view)
  Energy monitoring graphs
  Automation overview / toggles
  Camera feeds
  Vacuum maps
  Device configuration
  Long-term sensor history
  Infrastructure / server status
```

**Step 3 — Present the classification**

Show the classification to the user before writing any YAML:

```
Here's how I'd structure this before building:

Chip bar / Overview (always visible):
  • [entity list]

Room buttons → pop-ups:
  • [room list with contents]

Secondary views (rarely needed):
  • [entity list]

Not on the dashboard (better as automations):
  • [entity] — suggest: [automation trigger description]
```

Then: "Does this look right? Anything to move or add before I generate?"

If the user confirms → generate.
If the user adjusts → update classification, generate.
If the user says "just build it" → apply classification silently, generate.

**Claude never refuses based on classification.** The user has final say.
If they want a motion sensor card, add it. Note it once, then build.

**Step 4 — Apply device-type profile**

Look up the device in the profile table below. Apply max_columns, card_layout,
font size, and nav pattern before generating any YAML.

**Step 5 — Generate from the 5-view system**

Map the classification output to the 5-view structure:
- Bucket 1 → Overview view chip bar + per-room status grid
- Bucket 2 → Rooms view (room buttons + pop-ups)
- Bucket 3 → Settings view or secondary views
- Bucket 0 → Activity view automation category + ha-yaml handoff note

Read `references/dashboard-system.md` for the complete view-by-view structure
and Recipes 7–14 before generating.

**Step 6 — After delivery**

Offer two things, briefly:
- "Want me to generate the Activity or Settings view?"
- "Want the automation suggestions for the Bucket 0 items? I'll hand those
  off to the ha-yaml skill with context."

---

### Device-type profiles

One lookup replaces six separate questions. Apply this before generating any
full dashboard or setting max_columns, card_layout, or theme mode.

| Device | max_columns | card_layout | Font size | Nav pattern | Theme mode |
|---|---|---|---|---|---|
| Phone (primary) | 2 | large | 14px default | HBS footer only | Both modes |
| 10" wall tablet | 3 | large | 16px (bump up) | HBS + optional sidebar | Single-mode — ask light/dark |
| Desktop browser | 4 | normal | 14px default | Sidebar Card + HBS | Both modes |
| e-ink display | 2 | large | 16px (bump up) | HBS footer only | Single-mode light |
| Both phone + desktop | 3 | large | 14px default | HBS + Sidebar (sidebar hidden mobile) | Both modes |

**Single-mode trigger:** wall tablet and e-ink always prompt the single-mode
question. Phone and desktop browser never do — they get both modes by default.

**Wall tablet font bump:** set `ha-font-size-body: "16px"` and
`ha-font-size-small: "14px"` in the theme. Also set Mushroom font sizes
separately — they do not inherit from `ha-font-size-body`:
```yaml
mush-card-primary-font-size:   "15px"
mush-card-secondary-font-size: "13px"
mush-chip-font-size:           "0.35em"
```

---

### Progressive disclosure via pop-ups

Bubble Card pop-ups are the primary progressive disclosure mechanism. Use them to:
- Group all controls for a single room behind one button
- Show device details (media player art, camera feed, vacuum map) without leaving the view
- Surface rarely-needed controls (climate schedules, cover position fine-tuning)

**Pop-up sizing rules:**
- Default width on desktop: `560px` — wide enough for a 2-column grid of buttons
- Use `popup_mode: fit-content` for simple single-entity pop-ups (climate, cover)
- Use `popup_mode: centered` for camera feeds or complex layouts
- Always set `with_bottom_offset: true` when using an HBS footer

---

### Navigation patterns

**Choose based on primary device:**

| Scenario | Pattern | Why |
|----------|---------|-----|
| Mobile primary | Horizontal buttons stack (HBS) footer | Thumb-reachable, scrollable, auto-orders by room occupancy |
| Desktop primary | Sidebar Card | Persistent nav, clock, weather summary, bottom card slot |
| Both equally | HBS footer + Sidebar Card (sidebar hidden on mobile) | HBS handles mobile; sidebar adds desktop context |

When targeting both equally (the default for this skill): implement HBS as the
primary nav, add Sidebar Card with `width: { mobile: 0, tablet: 0, desktop: 20 }`
so it only appears on desktop. Set `is_sidebar_hidden: true` on the HBS card when
Sidebar Card is present on desktop.

**5-view navigation pattern:**
When using the 5-view system, HBS buttons link to view paths, not pop-up hashes:
```yaml
1_name: Overview
1_icon: mdi:home-variant
1_link: /lovelace/overview
# No 1_pir_sensor — views are not room-based
# No auto_order — view order is fixed and intentional
```

---

### Touch target sizing

All interactive elements must meet minimum sizes for reliable tap accuracy:

| Element | Minimum size | Bubble Card setting |
|---------|--------------|---------------------|
| HBS button | 48×48px | Default — do not reduce with CSS |
| Sub-button (main) | 36×36px | Default |
| Sub-button (bottom group) | 48px height | Set `custom_height: 48` if reducing |
| Pop-up close button | 44×44px | Default — do not hide unless replacing |
| Slider track | 44px tall hit area | Default |

Never reduce icon or button sizes below these thresholds with custom CSS.

---

### State colour feedback

Users need instant visual confirmation that a control worked. Ensure:

- **Active state:** entity `on` → card background uses `state-active-color`
  (→ `accent-color` in Casa5HeyneV2). Never suppress this with a hardcoded background.
- **Inactive state:** entity `off` → `state-inactive-color` (8% black in light,
  10% white in dark). Subtle but distinguishable.
- **Unavailable state:** icon dims to `disabled-text-color`. Do not hide unavailable
  entities — show them dimmed so users know the device exists but is offline.
- **Slider fill:** reflects brightness/volume/position. Do not override
  `--bubble-range-fill` with a static colour — it should track the light colour for
  RGB lights.

---

### Mobile-first layout rules

- Use `sections` view type (default since HA 2024.3). Never `masonry` for new dashboards.
- Set `max_columns: 2` for mobile-friendly views, `max_columns: 4` for desktop-optimised views.
- For "both equally" targets: set `max_columns: 3` — readable on tablet and desktop,
  wraps gracefully to 1–2 columns on phone.
- Card height: use `card_layout: large` for primary room control cards so they are
  finger-sized. Use `card_layout: normal` for secondary/informational cards.
- Avoid horizontal-stack with more than 2 cards — wrapping behaviour is unpredictable
  on narrow screens. Use sub-buttons or a grid section instead.

---

### Information density

- **Max 6–8 interactive elements per view** before introducing pop-ups. Beyond this,
  users stop seeing the dashboard and start hunting.
- Use `card_type: separator` to divide pop-up content into named sections (Lights,
  Covers, Media). Separators with icons dramatically reduce scanning time.
- Use sub-buttons for secondary information (battery level, last changed, brightness
  value) — they do not compete visually with the primary control.
- Show entity state text (`show_state: true`) only when the state adds meaning beyond
  the icon (e.g. temperature value, media title). For binary on/off states, the card
  colour is sufficient.

---

### Naming conventions for dashboards

- Pop-up hash: lowercase, hyphenated room name. `'#living-room'` not `'#LivingRoom'`
- HBS button order: most-occupied rooms first. Use `auto_order: true` with
  `_pir_sensor` references to make this dynamic.
- Card names: match the entity's friendly name in HA. Do not create dashboard-specific
  aliases — it breaks the mental model when users also use the HA app or voice.

---

### Sections view anatomy

Sections view (default since HA 2024.3) is the required view type for all
new dashboards. Understand its structure before generating any full dashboard.

```
view (type: sections, max_columns: N)
  │
  ├── cards:                     ← top-level cards (pop-ups + HBS live here)
  │     ├── [pop-up card]        ← must be top-level, NEVER inside sections
  │     ├── [pop-up card]
  │     ├── sections:            ← the visible grid
  │     │     ├── section        ← column_span controls width
  │     │     │     └── cards: [...]
  │     │     ├── section
  │     │     │     └── cards: [...]
  │     │     └── section
  │     │           └── cards: [...]
  │     └── [HBS footer card]    ← must be LAST top-level card
```

**column_span rules (with max_columns: 3):**

| column_span | Desktop width | Mobile behaviour |
|-------------|--------------|-----------------:|
| 3 | 100% (full width) | Full width |
| 2 | 66% | Full width (auto-wraps) |
| 1 | 33% | Full width (auto-wraps) |

**Making a card span full width:**
Set `column_span` on the *section*, not the card. All cards in a section
share the section's span:
```yaml
sections:
  - type: grid
    column_span: 3        # this section is full-width
    cards:
      - type: custom:bubble-card
        card_type: sub-buttons   # chip bar — now full width
```

**Section `type: grid` is always correct for Bubble Card content.**
Do not use `type: plain` or omit type — it changes padding and may cause
pop-up positioning issues.

---

### Accessibility

Beyond WCAG contrast (covered in §3a), these rules apply to all dashboards.

**Motion sensitivity (wall panels):**
- Never add CSS `animation:` or `transition:` with duration > 300ms on
  always-on displays. Users with vestibular disorders are affected.
- The default Bubble Card transitions are within safe limits — do not extend them.
- Never use `rise_animation: true` on HBS for wall-panel dashboards
  (it plays on every page load).

**Icon + label redundancy:**
- Never rely on colour alone to convey state. An entity's `on`/`off` state
  must be distinguishable by icon shape, label text, OR both — not colour alone.
- The Bubble Card active/inactive colour change is supplementary, not primary.

**Font size for wall panels viewed from distance:**
- Minimum readable font size at 1.5m viewing distance: 16px (HA default is 14px).
- If building for a wall panel: set `ha-font-size-body: "16px"` in the theme
  and `ha-font-size-small: "14px"` to bump the base upward.
- Use `card_layout: large` on all primary control cards for wall panels —
  this increases both touch target and text size.

**Voice assistant alignment:**
- Card `name:` fields should match the entity's friendly name in HA.
- Dashboard-specific aliases ("Main Light" vs the entity's "Living Room Ceiling")
  break the mental model when the user also uses voice ("Hey Google, turn on
  the main light" fails if the entity is named differently).
- Use `show_name: true` and keep names identical to entity friendly names.

---

### When to use Streamline Card templates

Apply the DRY rule: if you have written the same card structure 3 or more times
with only entity/name changes, extract a Streamline template. Good candidates:

- Every room light card (same structure, different entity)
- Every cover card (open/stop/close pattern)
- Every climate card per zone
- Sensor chip bars (same layout, many sensors)

Do not template one-offs or cards with significantly different structure.
The overhead of defining and maintaining a template is not worth it for fewer than
3 instances.

---

### Multi-view dashboard design

The 5-view system (`references/dashboard-system.md`) is the recommended structure
for new dashboards. Use it as the starting point. Split to additional views only
when a specific domain needs its own canvas — see the Energy and Music extension
views in `dashboard-system.md`.

A single view with pop-ups is still valid for simple homes or when the user
explicitly wants a minimal single-view dashboard.

**When to add a view beyond the 5-view system:**
- More than 8–10 room buttons in the Rooms view (split into zones)
- A domain needs always-visible display that doesn't fit Overview (security cameras)
- Different user groups need completely different primary views (family vs admin)

**Linking views from the HBS footer:**
```yaml
# HBS button linking to a view path (5-view nav pattern)
1_name: Overview
1_icon: mdi:home-variant
1_link: /lovelace/overview
# Note: no 1_pir_sensor — views are not room-based, no auto_order
```

---

### Panel view — for wall panels and kiosk dashboards

The `type: panel` view type forces a single card to fill the entire screen.
Use it when a custom card (Bubble Card sub-buttons, a picture-elements card,
or a third-party panel) should take up the full display without the standard
Lovelace grid padding.

```yaml
views:
  - title: Wall Panel
    path: wall-panel
    type: panel          # ← single full-screen card, no grid
    cards:
      - type: custom:bubble-card
        card_type: sub-buttons
        # ... this card now fills the entire screen
```

**When to use `type: panel`:**
- Always-on kiosk tablets where one card fills the screen
- Custom full-screen navigation panels
- Wall panels using a picture-elements overlay card
- Any situation where standard card padding looks wrong at the edges

**When not to use `type: panel`:**
- Standard room dashboards with multiple cards
- Dashboards that need to work on both phone and desktop (panel is desktop-only useful)
- Any view containing pop-ups (pop-ups work in panel views but positioning may shift)
- Surface rarely-needed controls (climate schedules, cover position fine-tuning)

**Pop-up sizing rules:**
- Default width on desktop: `560px` — wide enough for a 2-column grid of buttons
- Use `popup_mode: fit-content` for simple single-entity pop-ups (climate, cover)
- Use `popup_mode: centered` for camera feeds or complex layouts
- Always set `with_bottom_offset: true` when using an HBS footer

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
> **Single-mode themes:** `typography-ref.md#single-mode-themes`

Typography changes are independent of colour palette changes. They can be
combined in one theme delivery or handled separately.

### When typography is in scope

- User asks to change the font
- User mentions a wall panel needs larger text
- User asks why text looks different on different devices
- User wants a different font for headings vs body
- User is setting up a new theme from scratch (font + colour together)

### Mushroom font sizing — not inherited from HA

**Important:** Mushroom Cards has its own font size variables that do not
inherit from `ha-font-size-body`. If you increase `ha-font-size-body` for
a wall panel, Mushroom chip cards and entity cards will remain at their
default sizes unless you also set these separately:

```yaml
# In mode-independent theme block — alongside ha-font-size-body override
mush-card-primary-font-size:   "15px"   # default 14px
mush-card-secondary-font-size: "13px"   # default 12px
mush-chip-font-size:           "0.35em" # default 0.3em (relative to chip height)
```

Always set these when generating wall-panel themes that include Mushroom chips.

### Font delivery format

Always deliver two things together:

**1. The JS loader file** — complete content to create at `/config/www/`:
```javascript
// /config/www/font-name.js
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://fonts.googleapis.com/css2?family=FontName:wght@300;400;500;600;700&display=swap';
document.head.appendChild(link);
```

**2. The `configuration.yaml` addition:**
```yaml
frontend:
  extra_module_url:
    - /local/font-name.js
```

**3. The theme variable changes** — in the complete theme file.

Always remind the user: restart HA after adding `extra_module_url`, then
hard-refresh the browser. Without restart, the font JS file is not loaded.

### Font decision questions

Before generating a font swap, ask if not specified:

> "Do you want to host the font files locally (works offline, no flash of
> unstyled text) or load from Google Fonts CDN (easier setup, requires internet)?"

And for existing Alexandria users changing font only:
> "Do you want a complete new theme file, or just the font-related lines to
> update in your existing theme?"

### Delivering font-only updates

If the user only wants to change the font (not colours), deliver just the
changed lines rather than a full theme file — it's less error-prone for users
to apply a 10-line diff than to replace a 500-line file.

```yaml
# Changes to make in your existing theme file (mode-independent block):
ha-font-family-body:    "NewFont, sans-serif"
ha-font-family-heading: "NewFont, sans-serif"
ha-font-family-code:    "NewFont, monospace"
paper-font-common-base_-_font-family: "var(--primary-font-family)"
paper-font-body1_-_font-family:       "var(--primary-font-family)"
paper-font-subhead_-_font-family:     "var(--primary-font-family)"
paper-font-headline_-_font-family:    "var(--primary-font-family)"
paper-font-caption_-_font-family:     "var(--primary-font-family)"
paper-font-title_-_font-family:       "var(--primary-font-family)"
ha-card-header-font-family:           "var(--primary-font-family)"

# Changes in modes.light AND modes.dark:
primary-font-family: "NewFont, sans-serif"
```

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

Read `references/sidebar-ref.md` before generating any Sidebar Card config.

### When to include Sidebar Card

Default answer for "both equally" device targets: **yes, include it**, but
desktop-only:

```yaml
sidebar:
  width:
    mobile: 0
    tablet: 0
    desktop: 20
```

Pair with HBS footer as the primary mobile navigation. Set
`is_sidebar_hidden: true` on the HBS card so it positions correctly when
the native HA sidebar is hidden by Sidebar Card on desktop.

### Known issue checklist before delivering

Before generating any Sidebar Card config, confirm with the user:
- [ ] HA version ≥ 2024.3? (required for sections view compatibility)
- [ ] Are they aware of the `bottomCard` reliability issue?
  If yes and they want `bottomCard` → add a warning comment in the YAML.
- [ ] Are they on HA 2026.x? If yes, advise testing `showTopMenuOnMobile`
  after install as behaviour may differ from documentation.

### Clock + date + template message pattern

Always include clock, date, and at least one template message for desktop
sidebar setups — a sidebar with only a nav menu is wasted space. The
pattern below is the recommended baseline:

```yaml
sidebar:
  digitalClock: true
  date: true
  dateFormat: "dddd, D MMMM"
  template: |
    <li>
      {% if now().hour < 12 %}Good morning{% elif now().hour < 18 %}Good afternoon{% else %}Good evening{% endif %}
    </li>
    {% set lights = states.light | selectattr('state','eq','on') | list | count %}
    {% if lights > 0 %}<li>{{ lights }} light{{ 's' if lights > 1 }} on</li>{% endif %}
```

### Fallback pattern — when Sidebar Card issues are a dealbreaker

If the user experiences the `bottomCard` bug persistently, or if
`showTopMenuOnMobile` does not behave correctly on their HA version,
offer this HBS-only desktop alternative:

```yaml
# No Sidebar Card — use HBS footer + a full-width context chip bar at the
# top of the view instead. Works reliably on all HA versions.

# Top of view — contextual chip bar replaces the sidebar info panel
- type: custom:bubble-card
  card_type: sub-buttons
  hide_main_background: true
  sub_button:
    bottom:
      - name: Context
        buttons_layout: inline
        justify_content: space-between
        group:
          - entity: sensor.time            # clock equivalent
            show_state: true
            show_icon: false
            fill_width: false
            show_background: false
          - entity: weather.home           # weather summary
            show_state: true
            show_icon: true
            fill_width: false
            show_background: false
          - entity: sensor.lights_on_count # lights summary
            show_state: true
            show_icon: true
            icon: mdi:lightbulb
            fill_width: false
            show_background: false

# Bottom — HBS footer handles all navigation (mobile + desktop)
- type: custom:bubble-card
  card_type: horizontal-buttons-stack
  auto_order: true
  highlight_current_view: true
  is_sidebar_hidden: false    # no Sidebar Card → HA sidebar visible → false
  # ... room buttons as normal
```

**When to suggest this fallback:**
- User confirms persistent `bottomCard setConfig` errors after multiple refreshes
- User on HA 2026.x and `showTopMenuOnMobile` is not working as expected
- User wants a simpler single-component nav that works on all screen sizes

---

## §6 Streamline Card

> **Always read first:** `streamline-ref.md#ui-mode-vs-yaml-mode` — must ask user before generating
> **Then:** `streamline-ref.md#template-anatomy` → `#variable-syntax` → `#dry-decision`
> **JS templates:** `streamline-ref.md#javascript-keys` — note the [[variable]] substitution-before-evaluation gotcha

Read `references/streamline-ref.md` before generating any Streamline config.

### Mandatory first question

Before writing any Streamline template or usage YAML:

> "Are your Lovelace dashboards managed through the HA UI (the default), or
> do you use YAML-mode Lovelace with a `ui-lovelace.yaml` file?"

- **UI-mode answer** → templates go in the auto-load file only. Deliver
  template content as a YAML block to paste into
  `/config/www/community/streamline-card/streamline_templates.yaml`, and
  card usage YAML separately for the dashboard editor.
- **YAML-mode answer** → may use `!include` and `!include_dir_named`.
  Deliver organised as split files if the user has many templates.

### Template delivery format

Always deliver in two clearly labelled blocks:

**Block 1 — Add to `streamline_templates.yaml`:**
```yaml
my_template:
  default:
    - icon: mdi:ceiling-light
  card:
    type: custom:bubble-card
    # ...
```

**Block 2 — Add to dashboard YAML (card usage):**
```yaml
type: custom:streamline-card
template: my_template
variables:
  - entity: light.living_room
  - name: Living Room
```

Remind the user to clear browser cache and restart HA after adding new templates.

---

## §7 Recipes

> **Extended recipes:** `references/recipes-extended.md` — security, energy, vacuum, presence, bathroom, garage
> **Sections scaffold:** Recipe 0 below is the outer view wrapper — always start here for a full dashboard

Complete, copy-paste-ready YAML for the most common dashboard patterns.
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

### Recipe 1 — Room pop-up with lights, cover, and climate

```yaml
# Pop-up — place as a top-level card in the view
type: custom:bubble-card
card_type: pop-up
hash: '#living-room'
name: Living Room
icon: mdi:sofa
entity: light.living_room_group
width_desktop: "560px"
with_bottom_offset: true
cards:

  # ── Lights ──────────────────────────────────────────────
  - type: custom:bubble-card
    card_type: separator
    name: Lights
    icon: mdi:lightbulb-group

  - type: custom:bubble-card
    card_type: button
    button_type: slider
    entity: light.living_room_ceiling
    name: Ceiling
    icon: mdi:ceiling-light
    card_layout: large
    light_slider_type: brightness

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: light.living_room_floor_lamp
    name: Floor Lamp
    icon: mdi:floor-lamp
    card_layout: large

  # ── Cover ───────────────────────────────────────────────
  - type: custom:bubble-card
    card_type: separator
    name: Cover
    icon: mdi:blinds

  - type: custom:bubble-card
    card_type: cover
    entity: cover.living_room_blinds
    name: Blinds
    card_layout: large

  # ── Climate ─────────────────────────────────────────────
  - type: custom:bubble-card
    card_type: separator
    name: Climate
    icon: mdi:thermometer

  - type: custom:bubble-card
    card_type: climate
    entity: climate.living_room
    name: Thermostat
    card_layout: large
    state_color: true
    step: 0.5
```

---

### Recipe 2 — HBS footer navigation (both mobile + desktop)

```yaml
# Place as the LAST card in the view
type: custom:bubble-card
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

3_name: Bedroom
3_icon: mdi:bed
3_link: '#bedroom'
3_entity: light.bedroom_group
3_pir_sensor: binary_sensor.bedroom_motion

4_name: Office
4_icon: mdi:desk-lamp
4_link: '#office'
4_entity: light.office
4_pir_sensor: binary_sensor.office_motion

5_name: Settings
5_icon: mdi:cog
5_link: /lovelace/settings
```

---

### Recipe 3 — Media player card with album art background

```yaml
type: custom:bubble-card
card_type: media-player
entity: media_player.living_room_speaker
name: Speaker
card_layout: large
cover_background: true
show_state: true
min_volume: 0
max_volume: 100
sub_button:
  main:
    - name: Source
      select_attribute: source
      show_arrow: true
      show_state: false
      state_background: false
      show_background: false
```

---

### Recipe 4 — Climate card with HVAC mode sub-button

```yaml
type: custom:bubble-card
card_type: climate
entity: climate.living_room
name: Thermostat
icon: mdi:thermostat
card_layout: large
state_color: true
step: 0.5
sub_button:
  main:
    - name: Mode
      select_attribute: hvac_modes
      show_arrow: true
      show_icon: false
      show_state: true
      state_background: false
      show_background: false
```

---

### Recipe 5 — Sensor chip bar (sub-buttons only)

```yaml
# Glanceable chip bar — place at the top of a view
type: custom:bubble-card
card_type: sub-buttons
hide_main_background: true
sub_button:
  bottom:
    - name: Chips
      buttons_layout: inline
      justify_content: flex-start
      group:
        - entity: sensor.living_room_temperature
          show_name: false
          show_state: true
          show_icon: true
          icon: mdi:thermometer
          fill_width: false
          show_background: true
          state_background: false
        - entity: sensor.living_room_humidity
          show_name: false
          show_state: true
          show_icon: true
          icon: mdi:water-percent
          fill_width: false
          show_background: true
          state_background: false
        - entity: binary_sensor.living_room_motion
          show_name: true
          name: Motion
          show_state: false
          show_icon: true
          fill_width: false
          show_background: true
          state_background: true
        - entity: person.alice
          show_name: true
          show_state: false
          show_icon: true
          fill_width: false
          show_background: true
          state_background: true
```

---

### Recipe 6 — Streamline room light template (UI-mode)

**Block 1 — Add to `streamline_templates.yaml`:**
```yaml
room_light_button:
  default:
    - icon: mdi:ceiling-light
    - button_type: slider
    - card_layout: large
  card:
    type: custom:bubble-card
    card_type: button
    button_type: '[[button_type]]'
    entity: '[[entity]]'
    name: '[[name]]'
    icon: '[[icon]]'
    card_layout: '[[card_layout]]'
    light_slider_type: brightness
    button_action:
      tap_action:
        action: toggle
      hold_action:
        action: more-info

room_cover_button:
  card:
    type: custom:bubble-card
    card_type: cover
    entity: '[[entity]]'
    name: '[[name]]'
    icon_open: '[[icon_open]]'
    icon_close: '[[icon_close]]'
    card_layout: large

room_climate_button:
  default:
    - min_temp: 15
    - max_temp: 28
    - step: 0.5
  card:
    type: custom:bubble-card
    card_type: climate
    entity: '[[entity]]'
    name: '[[name]]'
    card_layout: large
    state_color: true
    min_temp: '[[min_temp]]'
    max_temp: '[[max_temp]]'
    step: '[[step]]'
```

**Block 2 — Card usage in dashboard:**
```yaml
# Ceiling light — uses all defaults (slider, large)
- type: custom:streamline-card
  template: room_light_button
  variables:
    - entity: light.living_room_ceiling
    - name: Ceiling

# Floor lamp — override to switch
- type: custom:streamline-card
  template: room_light_button
  variables:
    - entity: light.living_room_floor_lamp
    - name: Floor Lamp
    - icon: mdi:floor-lamp
    - button_type: switch

# Cover
- type: custom:streamline-card
  template: room_cover_button
  variables:
    - entity: cover.living_room_blinds
    - name: Blinds
    - icon_open: mdi:blinds-open
    - icon_close: mdi:blinds

# Climate
- type: custom:streamline-card
  template: room_climate_button
  variables:
    - entity: climate.living_room
    - name: Thermostat
```

---

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

When a dashboard request bleeds into automation or helper territory, hand off
cleanly rather than refusing or ignoring the need.

**Dashboard button → Automation (hand off to ha-yaml):**

Tell the user:
> "The dashboard button's `tap_action` navigates to the pop-up or calls a
> service directly — I'll generate that. For the automation that runs when the
> button is pressed (e.g. triggering a scene or script), use the ha-yaml skill
> with this context:"

Provide the ha-yaml skill with:
```
Entity to trigger from: [entity_id of the button entity or input_boolean]
Desired action: [what should happen]
Service to call: [e.g. scene.turn_on, script.turn_on, light.turn_on]
```

**Dashboard card → Template sensor (hand off to ha-yaml):**

When a card needs a value that doesn't exist as an entity (e.g. "count of
lights on", "time since last motion"):

Tell the user:
> "This display requires a template sensor. I'll generate the dashboard card
> using a placeholder entity ID — use the ha-yaml skill to create the sensor,
> then replace the placeholder."

Provide the placeholder in the card YAML as `sensor.placeholder_name` with a
comment: `# Replace with template sensor from ha-yaml skill`.

**Dashboard automation trigger → ha-yaml:**

Navigate tap_action is this skill's domain. Everything triggered BY a state
change belongs to ha-yaml:
- `tap_action: navigate` → this skill generates it
- `tap_action: call-service` on existing entities → this skill generates it
- "When I press this button, run a 2-minute timer then turn off the lights" → ha-yaml

### Additional pitfall reference

See the Common Pitfalls table at the top of this file (Thought / Reality format).
That table covers the most frequent failure modes in one place.

### Performance notes

- Pop-up content renders lazily — do not put always-on live sensors in pop-ups
  expecting them to update in the background. They update on pop-up open.
  **v3.2.1 improvement:** cards outside the visible area of a pop-up now update
  more intelligently by default. Manual `background_update: true` is no longer
  required in most cases — remove it from cards if you added it in earlier versions,
  as it may now cause redundant updates.
- `cover_background: true` on media-player cards fetches album art on every
  state change — avoid using it on dashboards with many simultaneous media
  players.
- `auto_order: true` on HBS requires PIR sensors with frequent state changes
  to work well. Without sensors, set `auto_order: false` to avoid unexpected
  reordering.
- Streamline `_javascript` keys re-evaluate on every state change. Keep
  JS template logic minimal — complex expressions in `cards_javascript` can
  cause noticeable render lag on low-powered devices (Raspberry Pi 3/4).

## §9 Health-Check Mode

> **Trigger:** user pastes existing dashboard YAML and asks for a review, audit,
> or says "what's wrong with my dashboard", "health check", "improve this",
> "review my YAML", or similar.
> **Do not trigger** for new dashboard generation — use §2#full-dashboard-workflow.

Health-check mode audits existing YAML and returns a prioritised findings list.
Work with whatever YAML is provided. Start immediately — do not ask scoping
questions upfront. Note incomplete coverage at the end if the YAML appears partial.

---

### Step 1 — Complete the structured parse first

**Before generating any findings**, fill in this parse template mentally.
This forces full structural reading before conclusions — reduces false positives
and missed findings.

```
PARSE PASS — complete before generating findings:

View structure:
  View type: [sections / masonry / panel / unspecified]
  max_columns: [value or MISSING]
  theme: [view-level / card-level / missing]
  Top-level cards: [count and types — pop-ups, HBS, other]
  HBS present: [yes/no] — position: [last / not last / missing]
  Sections count: [N]
  Pop-up count: [N]
  Pop-up hashes: [list all hash: values found]
  Navigation targets: [list all navigation_path: '#...' values found]

Cross-reference check:
  Every navigation_path: '#hash' has a matching pop-up hash: '#hash'? [yes/no/partial]
  Every HBS N_link: '/lovelace/path' is a valid view path? [yes/no/unknown]

Colour scan:
  Hardcoded hex (#rrggbb) on colour properties: [yes/no — list locations]
  Hardcoded rgb()/rgba(): [yes/no — list locations]
  Hardcoded named colours on colour properties: [yes/no — list locations]
  var(--...) chains present: [yes/no]

Performance flags:
  background_update: true found: [yes/no — list entities]
  rise_animation: true found: [yes/no]

Entity scan (interactive cards only — button_type: switch/slider or toggle tap_action):
  binary_sensor.* on interactive card: [list]
  sensor.* on interactive card: [list]
  automation-territory patterns: [list]

Card count per view (if multiple views present):
  [View name]: [N cards / N sections]

Chip bar present: [yes/no — mushroom-chips-card or sub-buttons chip strip]

Pop-up format:
  hash: present on all pop-ups: [yes/no]
  open_popup: true found (deprecated): [yes/no]
  with_bottom_offset: true when HBS present: [yes/no]

THEN generate findings from this completed parse.
```

---

### Step 2 — Structural patterns — correct vs incorrect

Use these reference patterns during the parse pass. YAML indentation determines
structure — read indentation carefully before flagging placement issues.

**Pop-up placement — Critical if wrong:**
```yaml
# CORRECT — pop-up as top-level card (indentation level 1 under cards:)
cards:
  - type: custom:bubble-card      # ← top-level
    card_type: pop-up
    hash: '#living-room'
  sections:
    - type: grid
      cards:
        - type: custom:bubble-card
          card_type: button        # ← inside sections: correct

# WRONG — pop-up inside sections: (indentation level 3+ under cards:)
cards:
  sections:
    - type: grid
      cards:
        - type: custom:bubble-card  # ← inside sections: WRONG for pop-ups
          card_type: pop-up
```

**HBS placement — Significant if wrong:**
```yaml
# CORRECT — HBS last top-level card
cards:
  - card_type: pop-up             # pop-ups first
  - card_type: pop-up
  sections: [...]
  - card_type: horizontal-buttons-stack  # ← LAST

# WRONG — HBS not last
cards:
  - card_type: horizontal-buttons-stack  # ← not last
  - card_type: pop-up
  sections: [...]
```

**Theme placement — Significant if on individual cards:**
```yaml
# CORRECT — theme at view level
- title: Overview
  theme: Casa5HeyneV2            # ← view level
  cards: [...]

# WRONG — theme on individual card
- type: custom:bubble-card
  theme: Casa5HeyneV2            # ← card level: Significant finding
```

**Colour values — Critical if hardcoded on colour properties:**
```yaml
# CORRECT — var() chain
styles: |
  .bubble-button { background: var(--accent-color); }

# WRONG — hardcoded hex
styles: |
  .bubble-button { background: #D9BE8B; }   # ← Critical

# WRONG — hardcoded RGB
styles: |
  .bubble-button { color: rgb(217, 190, 139); }  # ← Critical
```

**Pop-up format — Significant if old format:**
```yaml
# CORRECT — v3.2+ format
- type: custom:bubble-card
  card_type: pop-up
  hash: '#living-room'           # ← required in v3.2+
  width_desktop: "560px"
  with_bottom_offset: true

# WRONG — pre-v3.2 format
- type: custom:bubble-card
  card_type: pop-up
  open_popup: true               # ← deprecated: Significant finding
  entity: light.living_room      # ← entity on pop-up root: check v3.2 compat
```

**Navigation cross-reference — Significant if broken:**
```yaml
# CORRECT — button hash matches pop-up hash
- card_type: button
  button_action:
    tap_action:
      navigation_path: '#living-room'   # ← must match ↓

- card_type: pop-up
  hash: '#living-room'                  # ← matched: correct

# WRONG — broken navigation reference
- card_type: button
  tap_action:
    navigation_path: '#bedroom'         # ← no matching pop-up hash: broken link
```

---

### Step 3 — Colour scan exclusions

**Do NOT flag as hardcoded colour:**
```
- YAML comment lines:          # this is a comment with #hex values
- Entity IDs:                  entity: binary_sensor.front_door_0abc
- Icon values:                 icon: mdi:home-variant
- Pop-up hash values:          hash: '#living-room'
- Navigation paths:            navigation_path: '#bedroom'
- HBS link values:             1_link: /lovelace/overview
- Anchor references:           &anchor or *anchor
- HA service names:            service: light.turn_on
- Template strings:            value_template: "{{ '#' ~ state }}"
```

**DO flag as hardcoded colour** — only when the property name is colour-related:
```
Colour property names to scan:
  color, colour, background, background-color, fill, stroke,
  border-color, box-shadow, text-color, icon-color,
  --bubble-*, --mush-*, --ha-*  (CSS variable overrides with hardcoded values)

Pattern: [colour-property]: "#[0-9a-fA-F]{3,6}"   → Critical
Pattern: [colour-property]: "rgb(...)"              → Critical
Pattern: [colour-property]: "rgba(...)"             → Critical
Pattern: [colour-property]: "[named colour]"        → Critical
  Named colours to catch: red, blue, green, yellow, orange, purple,
                           white, black, grey, gray, gold, amber
```

**Borderline cases — do not flag:**
```
icon_color: "amber"    → this is a Mushroom semantic colour token, not hardcoded
icon_color: "red"      → same — Mushroom uses named tokens: do not flag
  Exception: if inside a styles: | CSS block → flag it
```

---

### Step 4 — Entity scan rules

**Only flag interactive cards** — not read-only state displays:

```
INTERACTIVE (flag if automation-territory entity):
  button_type: switch
  button_type: slider
  tap_action: action: toggle
  tap_action: action: call-service (service: light.turn_on / switch.toggle etc.)

NOT INTERACTIVE (do not flag — read-only display):
  button_type: state
  tap_action: action: none
  tap_action: action: more-info
  show_state: true (alone, without toggle action)
```

**Automation-territory entity patterns:**
```
binary_sensor.*_motion     → Advisory — automation trigger, not a control
binary_sensor.*_presence   → Advisory — automation trigger
binary_sensor.*_occupancy  → Advisory — automation trigger
binary_sensor.*_door       → Advisory — state display at most, not a button
binary_sensor.*_window     → Advisory — state display at most
binary_sensor.*_contact    → Advisory — state display at most
sensor.*_temperature       → Advisory if interactive — sensors are read-only
sensor.*_humidity          → Advisory if interactive
sensor.*_power             → Advisory if interactive
sensor.*_energy            → Advisory if interactive
```

**Do not flag:**
```
binary_sensor.*_lock       → legitimate interactive control (lock state)
binary_sensor.*_alarm      → legitimate interactive control
input_boolean.*            → always legitimate — these are designed for manual control
input_select.*             → always legitimate
input_number.*             → always legitimate
```

---

### Step 5 — Engagement-type mixing detection

For each view in the pasted YAML, classify the card types present:

```
Complications (passive):
  mushroom-chips-card, sub-buttons (chip strip), sensor state cards,
  weather card, picture-glance

Brief interaction (one tap):
  bubble-card button, bubble-card media-player, bubble-card pop-up trigger,
  scene buttons, input_boolean switches

Deep engagement (multi-step):
  history-graph, statistics-graph, logbook, mini-graph-card,
  energy-distribution, automation list, config link cards,
  number input cards, select cards
```

**Flag as Significant** when a single view contains cards from more than one
engagement tier — especially Brief interaction mixed with Deep engagement.

**Do not flag** the Overview view for having both Complications and
Brief interaction chips — chip-level brief interaction (weather tap → more-info)
is acceptable on an otherwise passive view. Flag only when full interactive
controls (room buttons, switches) appear alongside history graphs or config cards.

---

### Finding categories and severity

**Critical — fix before using**
Functionality broken or Iron Law violated.

| Finding | Source |
|---|---|
| `type: masonry` or no view type | Outdated view type |
| Pop-up inside `sections:` | Structural placement bug |
| Hardcoded hex / rgb on colour property | Iron Law violation |
| Pop-up missing `hash:` | Pop-up cannot open |
| `open_popup: true` on pop-up | Deprecated pre-v3.2 format |
| Broken navigation cross-reference | Dead link — button goes nowhere |

**Significant — fix soon**
UX materially degraded or behaviour unreliable.

| Finding | Source |
|---|---|
| HBS not last top-level card | HBS positioning rule |
| `background_update: true` on non-realtime entity | Performance |
| Mixed engagement types on one view | Engagement-type model |
| `theme:` set on individual cards | Theme architecture |
| `with_bottom_offset` missing when HBS present | Pop-up overlap |
| Old pop-up format (`open_popup: true`) | Version compat |

**Advisory — consider improving**
Improvement opportunities — never prescriptive.

| Finding | Source |
|---|---|
| Interactive card on automation-territory entity | Automate-first |
| No chip bar / complications tier found | Engagement-type model |
| `rise_animation: true` on likely fixed display | Wall panel best practice |
| Section type not `grid` | Sections anatomy |
| `column_span` not set on sections | Layout reliability |
| `max_columns` not set on view | Device-type profile |
| `name:` missing on cards | Accessibility / naming |
| 5-view alignment opportunity | Optional restructure |

---


---

### Output format

Always deliver findings in this structure. Never free-form prose for findings.

```
## Dashboard Health Check

[If partial YAML: "Note: auditing [N] cards / [N] views provided.
Findings may be incomplete if this is a partial dashboard."]

---

### 🔴 Critical ([N] findings)

**[Finding title]**
Where: [card name / view name / line context]
Issue: [one sentence — what is wrong]
Fix:
  [specific YAML change or instruction]

[repeat per Critical finding]

---

### 🟡 Significant ([N] findings)

**[Finding title]**
Where: [card name / view name]
Issue: [one sentence]
Fix:
  [specific YAML change or instruction]

[repeat per Significant finding]

---

### 🟢 Advisory ([N] findings)

**[Finding title]**
Where: [card name / view name / general]
Issue: [one sentence]
Suggestion:
  [what to consider — not a command]

[repeat per Advisory finding]

---

### Summary

[2–3 sentences: overall assessment, most important action to take first,
and what is working well — always note what is correct, not only problems]

[If applicable: "This dashboard maps well to the 5-view system —
if you want to restructure, [specific suggestion for which views
the existing content would move to]."]

[If partial YAML: "To get a complete audit, paste the full dashboard YAML
including all views and the HBS footer card."]
```

---

### Automate-first findings — tone guide

When flagging an interactive card on an automation-territory entity, always:
1. Name the entity and card specifically
2. Note what it typically indicates
3. Suggest the automation alternative neutrally
4. Acknowledge the user may have a reason for it

Example Advisory finding:
```
**Motion sensor on interactive card**
Where: Living Room pop-up — switch card on binary_sensor.living_room_motion
Issue: Motion sensors are typically automation triggers, not manual controls.
Suggestion:
  If this light is already motion-triggered, this card may be unnecessary.
  Consider removing it and relying on the automation.
  If you need a manual override, use input_boolean.override_motion_lights
  as the card entity instead — hand off the boolean logic to ha-yaml.
  (Keep the card if you have a specific reason for manual motion sensor control.)
```

---

### 5-view alignment — advisory only

If the user's dashboard does not follow the 5-view structure, note it once
at the end of the Advisory section — never as Critical or Significant.
Frame it as an option, not a requirement.

```
**5-view system alignment opportunity**
Where: Overall dashboard structure
Issue: Current dashboard uses [N] view(s) with mixed purposes.
Suggestion:
  The 5-view system (Overview / Rooms / Scenes / Activity / Settings)
  separates engagement types across dedicated views. Your current content
  maps approximately as:
    Overview → [list chips and state cards]
    Rooms    → [list room buttons and pop-ups]
    Settings → [list config and automation cards]
  See references/dashboard-system.md for the full structure and
  Recipes 7–12 for copy-paste scaffolds.
  This is optional — your current structure is valid if it works for you.
```

---

### Partial YAML handling

Never ask the user to provide more YAML before starting. Start immediately.

After delivering findings, add one of these closers if the YAML appears partial:

- Single pop-up only: "This audit covers one pop-up. Paste the full view
  YAML to check view type, HBS placement, and chip bar presence."
- Single view only: "This audit covers one view. Paste all views to check
  cross-view engagement-type mixing and the 5-view alignment."
- Full dashboard: no caveat needed.

If the user then pastes more YAML, run a delta audit — only report new findings
not already covered in the first pass.

---
