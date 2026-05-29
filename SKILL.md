---
name: ha-bubble-dashboard
description: >
  Home Assistant dashboard and card design using Bubble Card 3.x, Bubble Card Tools,
  Streamline Card, and Sidebar Card — anchored to the Casa5HeyneV2 merged
  HA/Bubble Card theme architecture.

  TRIGGER THIS SKILL WHEN:
  - User asks to create, design, or improve a Lovelace dashboard or view
  - User asks for help with Bubble Card (any card type: pop-up, button, media-player, climate, cover, select, separator, calendar, sub-buttons)
  - User asks for a CSS theme, colour palette, or accent colour change for HA
  - User asks to change or customise the dashboard font or typography
  - User asks to create or modify a Streamline Card template
  - User asks to configure Sidebar Card or dashboard navigation
  - User asks why their Bubble Card theme/colour is not reflecting the HA theme
  - User asks to create a room pop-up, footer nav, or control panel
  - User asks for dashboard UX advice or layout recommendations
  - User asks about wall-panel, kiosk, or fixed-display dashboard setup
  - Troubleshooting: pop-up not opening, theme not applying, Streamline template
    not found, sidebar not showing, card styling being ignored, font not loading

  SYMPTOMS — Claude is going wrong without this skill when it:
  - Hardcodes hex colours directly in Bubble Card YAML instead of using var() chains
  - Generates a pop-up using the pre-v3.2 format (separate stack + pop-up card) instead of the v3.2+ standalone format with a cards: block
  - Places a pop-up or HBS footer inside sections: instead of as a top-level view card
  - Generates a pop-up inside a horizontal-stack or vertical-stack
  - Uses the deprecated bubble-pop-up-fix.js script or references it
  - Generates Streamline Card YAML using !include_dir_named without first asking whether the user is in UI-mode or YAML-mode Lovelace
  - Does not remind the user to clear browser cache and restart HA after adding Streamline templates
  - References subButtonIcon[0] for a main sub-button without accounting for v3.1+ index reordering (bottom sub-buttons are indexed first)
  - Applies the --bubble-accent-color variable directly with a hex value instead of pointing it to var(--accent-color)
  - Tells the user to install Bubble Card Tools and apply the HA default styling module as a mandatory setup step (it is optional)
  - Recommends card-mod for styling Bubble Cards (Bubble Card has its own styles: system)
  - Generates automations, helpers, or template sensors — those belong to ha-yaml and ha-best-practices skills
  - Uses a plain button card for fan, vacuum, lock, alarm, or camera entities without checking entity-domain-map
  - Reconstructs a theme YAML from scratch instead of using references/casa5heynev2-template.yaml as the base
  - Uses masonry view type instead of sections for new dashboards
  - Generates both light and dark mode without first asking whether the user has a fixed-display (wall panel / kiosk)
  - Delivers a font change without providing the JS loader file and configuration.yaml change
  - Tells the user a font change only requires theme variable updates (it also requires the JS loader and HA restart)

  OUT OF SCOPE — do not use this skill for:
  - HA automations, scripts, blueprints, or helpers → use ha-yaml
  - Template sensors or binary sensor helpers → use ha-yaml
  - Custom integration development → use ha-integration-dev
  - ESPHome firmware → use esphome skill
  - Mushroom Cards (not part of this stack)

  PAIRS WITH:
  - ha-yaml: automations triggered from dashboard buttons
  - ha-best-practices: entity naming, helper selection feeding dashboard cards

metadata:
  version: 1
  bubble_card: "3.2.2"
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
  └── Full dashboard   → Ask: wall panel? → single-mode + size overrides
                         §2 UX → Recipe 0 scaffold → card refs as needed

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
| "The template is added, let's move on" | STOP. Remind the user to hard-refresh the browser and restart HA after adding Streamline templates — without this the template won't load. |
| "The HA default styling module is required" | NO. It is optional. The skill outputs a merged theme file that handles Bubble ↔ HA alignment. |
| "I'll hardcode the card background in the card YAML" | WRONG. All colours flow from the theme file via var() chains. |
| "Sidebar Card has no issues on HA 2026" | CAUTION. bottomCard has an intermittent setConfig bug. showTopMenuOnMobile behaviour changed in HA 2026.1. Test after install. |
| "I swapped the accent, Bubble Card updated but Mushroom is still blue" | EXPECTED without ZONE 6 update. Set `accent-color-rgb: "NR,NG,NB"` in the mode-independent block so `mush-rgb-primary` picks up the new accent. |
| "I'll generate both light and dark mode for this wall panel" | ASK FIRST. Fixed-display setups (wall panels, kiosks) need single-mode themes. Generating both wastes maintenance surface and risks accidental mode switching. |
| "I'll just update the font variables in the theme" | INCOMPLETE. Font changes also require a JS loader file at /config/www/ and an extra_module_url entry in configuration.yaml. Theme variables alone have no effect without the loader. |
| "I'll generate automations for this dashboard button" | STOP. Send the user to ha-yaml for the automation. Only generate the navigate tap_action here. |
| "A button card is fine for this fan/vacuum/lock" | CHECK. Use bubble-card-ref.md#entity-domain-map first — complex domains need sub-button patterns, not a plain switch button. |

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
`#ui-mode-vs-yaml-mode`★ · `#template-anatomy` · `#variable-syntax` · `#javascript-keys` · `#dry-decision` · `#file-organisation` · `#known-limitations` · `#bubble-card-interaction`

**sidebar-ref.md** — Sidebar Card config:
`#known-issues`★ · `#installation` · `#main-options` · `#width-breakpoints` · `#sidebar-menu` · `#template-messages` · `#style` · `#bottom-card` · `#combined-example`

**colour-intelligence-ref.md** — palette or accent:
`#two-modes`★ · `#casa5-profile` · `#wcag-checks` · `#harmony-rules` · `#bring-your-own-accent` · `#advisory-conversation-flow` · `#accent-swap-recipes` · `#full-palette-recipes` · `#full-palette-recipes-dark`

**mushroom-theme-ref.md** — Mushroom Cards theming:
`#architecture`★ · `#ha-bridge` · `#state-mapping` · `#colour-palette` · `#structure-vars` · `#integration-block` · `#palette-swap-impact` · `#card-override-limits` · `#accent-colour-for-switches` · `#chip-card` · `#template-chip`

**casa5heynev2-template.yaml** — base for all theme generation. Never reconstruct from scratch.

**test-dashboard.yaml** — complete importable dashboard assembling Recipes 0–5. Use to verify YAML validity after recipe changes, or as a starter dashboard for users.

**troubleshooting-ref.md** — when something is broken:
`#cache-issues`★ · `#theme-not-applying` · `#popup-not-opening` · `#streamline-not-found` · `#sidebar-not-showing` · `#bubble-styling-ignored` · `#version-migration` · `#hbs-not-ordering` · `#sections-layout-issues` · `#sub-buttons-not-showing` · `#card-state-stale` · `#font-not-loading` · `#popup-z-index` · `#general-diagnostic-checklist`★

**recipes-extended.md** — room-specific patterns:
`#security-popup` · `#energy-view` · `#vacuum-popup` · `#presence-panel` · `#bathroom-popup` · `#garage-popup` · `#office-popup` · `#streamline-templates-extended`

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

These rules govern every dashboard decision. Read before designing any layout.

### The hierarchy of information

A well-designed dashboard answers questions in order of urgency without requiring
navigation. Structure information in three tiers:

```
Tier 1 — Glanceable (visible immediately, no interaction)
  Status of the home at a glance: occupied rooms, active lights, climate.
  Cards: state buttons, sensor displays, the HBS footer showing room activity.

Tier 2 — Actionable (one tap, inside a pop-up)
  Controls for a specific room or system: lights, covers, climate, media.
  Cards: Bubble Card pop-ups triggered from HBS or room buttons.

Tier 3 — Detailed (two taps, inside a nested section or sub-view)
  History, statistics, configuration, rarely-changed settings.
  Cards: energy graphs, automations overview, device settings.
```

Never mix tiers on the same surface. Putting energy history next to one-tap
light toggles trains users to ignore the important controls.

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

### Mobile-first layout rules

- Use `sections` view type (default since HA 2024.3). Never `masonry` for new dashboards.
- Set `max_columns: 2` for mobile-friendly views, `max_columns: 4` for desktop-optimised views.
- For "both equally" targets: set `max_columns: 3` — readable on tablet and desktop,
  wraps gracefully to 1–2 columns on phone.
- Card height: use `card_layout: large` for primary room control cards so they are
  finger-sized. Use `card_layout: normal` for secondary/informational cards.
- Avoid horizontal-stack with more than 2 cards — wrapping behaviour is unpredictable
  on narrow screens. Use sub-buttons or a grid section instead.

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

### Naming conventions for dashboards

- Pop-up hash: lowercase, hyphenated room name. `'#living-room'` not `'#LivingRoom'`
- HBS button order: most-occupied rooms first. Use `auto_order: true` with
  `_pir_sensor` references to make this dynamic.
- Card names: match the entity's friendly name in HA. Do not create dashboard-specific
  aliases — it breaks the mental model when users also use the HA app or voice.

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
|-------------|--------------|-----------------|
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

### Multi-view dashboard design

A single view with pop-ups handles most home dashboards. Split to multiple
views when the single view feels crowded or when users have distinct contexts
(e.g. a dedicated energy view, a wall-panel view, an admin view).

**When to add a second view:**
- More than 8–10 room buttons in the HBS footer (scrolling becomes awkward)
- A category of cards needs always-visible display (energy, security cameras)
- Different user groups need different primary views (family vs admin)
- A wall-panel scenario needs a simplified always-on view

**Linking views from the HBS footer:**
```yaml
# HBS button linking to a full view instead of a pop-up hash
5_name: Energy
5_icon: mdi:lightning-bolt
5_link: /lovelace/energy    # path to the second view, not a hash
# Note: no 5_pir_sensor — energy view is not room-based
```

**Sub-view pattern (pop-up containing a navigate button):**
For rarely-needed detail pages, link from within a pop-up rather than
adding a top-level HBS button:
```yaml
# Inside a pop-up cards: block
- type: custom:bubble-card
  card_type: button
  button_type: name
  name: Energy History
  icon: mdi:chart-line
  button_action:
    tap_action:
      action: navigate
      navigation_path: /lovelace/energy
```

**HA native sub-views** (accessible via sidebar but not from HBS) are a third
option for admin-only content. Generate them as standard Lovelace views and
advise the user to hide them from the sidebar if needed.

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
- `cover_background: true` on media-player cards fetches album art on every
  state change — avoid using it on dashboards with many simultaneous media
  players.
- `auto_order: true` on HBS requires PIR sensors with frequent state changes
  to work well. Without sensors, set `auto_order: false` to avoid unexpected
  reordering.
- Streamline `_javascript` keys re-evaluate on every state change. Keep
  JS template logic minimal — complex expressions in `cards_javascript` can
  cause noticeable render lag on low-powered devices (Raspberry Pi 3/4).
