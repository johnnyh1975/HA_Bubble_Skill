# Mushroom Cards Theme Reference
# ha-bubble-dashboard skill
# Covers: the three-layer variable architecture, HA bridge wiring,
#         complete state colour mapping, integration block for theme files,
#         palette swap impact, and what card-level overrides can/cannot do.

---

## #architecture

### The three-layer Mushroom variable architecture

Mushroom's colour system has three distinct layers. The Casa5HeyneV2 theme
currently implements Layer 2a only. This reference documents Layers 2b and 2c
and how to wire all three into the HA theme system.

```
Layer 2a — Base colour palette (raw RGB triplets)
  mush-rgb-orange:  255, 152, 0
  mush-rgb-green:   76, 175, 80
  mush-rgb-blue:    33, 150, 243
  ...20 colours total

        ↓ referenced by

Layer 2b — Entity-domain state mapping (var() chain within Mushroom)
  mush-rgb-state-light:        var(--mush-rgb-orange)
  mush-rgb-state-fan:          var(--mush-rgb-green)
  mush-rgb-state-climate-heat: var(--mush-rgb-deep-orange)
  ...14 domain groups

        ↓ consumed by

Layer 2c — HA RGB bridge (parallel to accent-color chain)
  accent-color-rgb: "217, 190, 139"     ← accent as RGB triplet
  mush-rgb-primary: var(--accent-color-rgb)  ← connects Mushroom to HA accent
```

**What this enables:**
- Changing `accent-color` → also moves `mush-rgb-primary` → can drive
  `mush-rgb-state-switch` and `mush-rgb-state-entity` to match Bubble Card
- Changing `mush-rgb-orange` → immediately shifts all light, cover, lock,
  and climate-dry icons without touching entity card YAML
- Palette swaps stay in the theme file — no card-level changes needed

**The constraint:** Mushroom uses `R, G, B` triplets (no `rgb()` wrapper).
HA's `accent-color` is a hex value. The bridge variable `accent-color-rgb`
must be set in parallel — both must be updated when swapping the accent.

---

## #ha-bridge

### Layer 2c — HA RGB bridge variables

These variables connect HA's hex colour system to Mushroom's RGB triplet
system. Add them to the mode-independent section of the theme (not inside
`modes.light` or `modes.dark`) for values that are the same in both modes,
and inside each mode block for the disabled colour which differs.

**Bridge variables (add to mode-independent theme block):**

```yaml
# ── Mushroom ↔ HA accent bridge ──────────────────────────────
# These connect Mushroom's RGB triplet system to the HA accent chain.
# Update accent-color-rgb whenever accent-color changes.
# Format: "R, G, B" (bare integers, no rgb() wrapper)
accent-color-rgb:   "217, 190, 139"   # ← RGB of #D9BE8B (gold — update with accent)

# mush-rgb-primary wires Mushroom to the HA accent
mush-rgb-primary:   "var(--accent-color-rgb)"

# HA also ships these natively (since 2022.11) — reference in Mushroom vars:
# --rgb-primary-color     → same as accent-color in RGB
# --rgb-accent-color      → same as accent-color in RGB
# --rgb-primary-text-color
# --rgb-secondary-text-color
# --rgb-card-background-color
```

**Why `accent-color-rgb` and not `var(--rgb-primary-color)`?**
HA ships `--rgb-primary-color` natively since 2022.11, but its value is
controlled by HA's internal colour processing — in some HA versions it does
not reliably reflect custom theme accent values. The explicit `accent-color-rgb`
variable in the theme file is the reliable approach.

---

## #state-mapping

### Layer 2b — Complete state colour mapping

All `mush-rgb-state-*` variables and their default values from official Mushroom Themes.
These go in the **mode-independent** section — they reference Layer 2a variables
which are defined per-mode.

**Simple domain states (single colour, entity on/off only):**

```yaml
# ── Mushroom state colour mapping (mode-independent) ─────────
mush-rgb-state-fan:    "var(--mush-rgb-green)"   # fan ON → green
mush-rgb-state-light:  "var(--mush-rgb-orange)"  # light ON → orange
mush-rgb-state-entity: "var(--mush-rgb-blue)"    # generic entity → blue
mush-rgb-state-switch: "var(--mush-rgb-blue)"    # switch ON → blue
```

**Person presence states (3 sub-states):**

```yaml
mush-rgb-state-person-home:     "var(--mush-rgb-success)"  # → green
mush-rgb-state-person-not-home: "var(--mush-rgb-danger)"   # → red
mush-rgb-state-person-zone:     "var(--mush-rgb-info)"     # → blue
mush-rgb-state-person-unknown:  "var(--mush-rgb-grey)"     # → grey
```

**Cover states (2 sub-states):**

```yaml
mush-rgb-state-cover-open:   "var(--mush-rgb-blue)"      # open → blue
mush-rgb-state-cover-closed: "var(--mush-rgb-disabled)"  # closed → grey
```

**Alarm states (3 sub-states):**

```yaml
mush-rgb-state-alarm-disarmed: "var(--mush-rgb-info)"    # disarmed → blue
mush-rgb-state-alarm-armed:    "var(--mush-rgb-success)" # armed → green
mush-rgb-state-alarm-triggered:"var(--mush-rgb-danger)"  # triggered → red
```

**Climate HVAC mode states (8 sub-states):**

```yaml
mush-rgb-state-climate-auto:      "var(--mush-rgb-green)"      # auto → green
mush-rgb-state-climate-cool:      "var(--mush-rgb-blue)"       # cool → blue
mush-rgb-state-climate-dry:       "var(--mush-rgb-orange)"     # dry → orange
mush-rgb-state-climate-fan-only:  "var(--mush-rgb-blue-grey)"  # fan → blue-grey
mush-rgb-state-climate-heat:      "var(--mush-rgb-deep-orange)"# heat → deep orange
mush-rgb-state-climate-heat-cool: "var(--mush-rgb-green)"      # heat-cool → green
mush-rgb-state-climate-idle:      "var(--mush-rgb-grey)"       # idle → grey
mush-rgb-state-climate-off:       "var(--mush-rgb-disabled)"   # off → disabled
```

**Semantic aliases (reference Layer 2a colours by meaning):**

```yaml
mush-rgb-info:    "var(--mush-rgb-blue)"    # informational state
mush-rgb-success: "var(--mush-rgb-green)"   # success / home / armed
mush-rgb-warning: "var(--mush-rgb-orange)"  # warning
mush-rgb-danger:  "var(--mush-rgb-red)"     # error / not-home / triggered
```

**Disabled state (per-mode — different in light and dark):**

```yaml
# modes.light:
mush-rgb-disabled: "189, 189, 189"   # light grey
# modes.dark:
mush-rgb-disabled: "111, 111, 111"   # dark grey
```

---

## #colour-palette

### Layer 2a — Complete base colour palette

The official Mushroom colour values. These can be overridden in the theme to
shift domain icon colours globally without touching state mappings.

```yaml
# Official Mushroom palette (Material Design colours)
mush-rgb-red:         "244, 67, 54"
mush-rgb-pink:        "233, 30, 99"
mush-rgb-purple:      "106, 107, 201"
mush-rgb-deep-purple: "111, 66, 193"
mush-rgb-indigo:      "63, 81, 181"
mush-rgb-blue:        "33, 150, 243"
mush-rgb-light-blue:  "3, 169, 244"
mush-rgb-cyan:        "0, 188, 212"
mush-rgb-teal:        "0, 150, 136"
mush-rgb-green:       "76, 175, 80"
mush-rgb-light-green: "139, 195, 74"
mush-rgb-lime:        "205, 220, 57"
mush-rgb-yellow:      "255, 235, 59"
mush-rgb-amber:       "255, 193, 7"
mush-rgb-orange:      "255, 152, 0"
mush-rgb-deep-orange: "255, 111, 0"
mush-rgb-brown:       "121, 85, 72"
mush-rgb-light-grey:  "189, 189, 189"
mush-rgb-grey:        "158, 158, 158"
mush-rgb-dark-grey:   "96, 96, 96"
mush-rgb-blue-grey:   "96, 125, 139"
mush-rgb-black:       "0, 0, 0"
mush-rgb-white:       "255, 255, 255"
```

**Casa5HeyneV2 overrides from official Mushroom defaults:**

| Variable | Official value | Casa5 override | Reason |
|----------|---------------|----------------|--------|
| `mush-rgb-blue` | `33, 150, 243` | `37, 43, 56` | Replaced with dark text colour — makes entity/switch icons read as text-coloured rather than blue |
| `mush-rgb-purple` | `106, 107, 201` | `156, 39, 176` | Shifted to more saturated Material purple |
| `mush-rgb-deep-orange` | `255, 111, 0` | `255, 87, 34` | Slightly more orange-red |

> **Important:** The Casa5 `mush-rgb-blue` override (`37, 43, 56`) means any
> Mushroom state that points to `var(--mush-rgb-blue)` will show the dark text
> colour, not a true blue. `mush-rgb-state-entity`, `mush-rgb-state-switch`,
> `mush-rgb-state-cover-open`, and `mush-rgb-state-alarm-disarmed` are all
> affected. This is a deliberate design choice — to get true blue states,
> restore `mush-rgb-blue: "33, 150, 243"`.

---

## #structure-vars

### Structure variables — geometry and typography

These are mode-independent and control layout, sizing, and typography.
They are already partially set in Casa5HeyneV2. The full canonical set:

```yaml
# ── Mushroom layout ──────────────────────────────────────────
mush-spacing: "12px"            # base spacing unit throughout

# ── Title card ───────────────────────────────────────────────
mush-title-padding:        "24px 12px 8px"
mush-title-spacing:        "8px"
mush-title-font-size:      "24px"
mush-title-font-weight:    "normal"
mush-title-line-height:    "32px"
mush-title-color:          "var(--primary-text-color)"
mush-title-letter-spacing: "-0.288px"

mush-subtitle-font-size:      "16px"
mush-subtitle-font-weight:    "normal"
mush-subtitle-line-height:    "24px"
mush-subtitle-color:          "var(--secondary-text-color)"
mush-subtitle-letter-spacing: "0px"

# ── Card text ────────────────────────────────────────────────
mush-card-primary-font-size:      "14px"
mush-card-secondary-font-size:    "12px"
mush-card-primary-font-weight:    "500"
mush-card-secondary-font-weight:  "400"
mush-card-primary-line-height:    "20px"
mush-card-secondary-line-height:  "16px"
mush-card-primary-color:          "var(--primary-text-color)"
mush-card-secondary-color:        "var(--primary-text-color)"
mush-card-primary-letter-spacing: "0.1px"
mush-card-secondary-letter-spacing: "0.4px"

# ── Chip ─────────────────────────────────────────────────────
mush-chip-spacing:          "8px"
mush-chip-padding:          "0 0.25em"
mush-chip-height:           "36px"
mush-chip-border-radius:    "19px"
mush-chip-border-width:     "var(--ha-card-border-width, 1px)"
mush-chip-border-color:     "var(--ha-card-border-color, var(--divider-color))"
mush-chip-box-shadow:       "var(--ha-card-box-shadow, none)"
mush-chip-font-size:        "0.3em"
mush-chip-font-weight:      "bold"
mush-chip-icon-size:        "0.5em"
mush-chip-avatar-padding:   "0.1em"
mush-chip-avatar-border-radius: "50%"
mush-chip-background:       "var(--ha-card-background, white)"

# ── Controls ─────────────────────────────────────────────────
mush-control-border-radius: "12px"
mush-control-height:        "42px"
mush-control-button-ratio:  "1"
mush-control-icon-size:     "0.5em"
mush-control-spacing:       "12px"
mush-slider-threshold:      "10"

# ── Badge ────────────────────────────────────────────────────
mush-badge-size:          "16px"
mush-badge-icon-size:     "0.75em"
mush-badge-border-radius: "50%"

# ── Icon ─────────────────────────────────────────────────────
mush-icon-border-radius:  "50%"    # 50% = round; "12px" = square-ish
mush-icon-size:           "36px"   # Casa5 uses 54px — larger than default
mush-icon-symbol-size:    "0.6em"
```

**Casa5HeyneV2 structure overrides from official Mushroom defaults:**

| Variable | Official | Casa5 | Effect |
|----------|---------|-------|--------|
| `mush-icon-size` | `36px` | `54px` | Larger icon container — more prominent |
| `mush-icon-symbol-size` | `0.6em` | `0.5em` | Slightly smaller symbol inside larger container |
| `mush-icon-border-radius` | `50%` | `50%` | Same — round icons |

---

## #integration-block

### The complete Mushroom ↔ HA integration block

This is the full block to add to the **mode-independent** section of the theme
(before `modes:`). It wires all three layers and is missing from Casa5HeyneV2
today. The `casa5heynev2-template.yaml` has been updated to include this.

```yaml
# ════════════════════════════════════════════════════════════════
# MUSHROOM ↔ HA INTEGRATION BLOCK
# Wires all three layers of Mushroom's colour system to HA variables.
# This section goes in the MODE-INDEPENDENT part of the theme (before modes:)
# ════════════════════════════════════════════════════════════════

# ── Layer 2c: HA RGB bridge ──────────────────────────────────
# Update accent-color-rgb whenever accent-color changes.
# Format: "R, G, B" — bare integers, no rgb() wrapper.
accent-color-rgb: "217, 190, 139"        # RGB of #D9BE8B — matches light mode

# mush-rgb-primary wires Mushroom to the HA accent lever
mush-rgb-primary: "var(--accent-color-rgb)"

# ── Layer 2b: Entity-domain state mapping ────────────────────
# Points each domain state to a Layer 2a colour variable.
# Change the target (e.g. var(--mush-rgb-amber)) to remap a domain.

# Simple domains
mush-rgb-state-fan:    "var(--mush-rgb-green)"    # fan ON
mush-rgb-state-light:  "var(--mush-rgb-orange)"   # light ON
mush-rgb-state-entity: "var(--mush-rgb-blue)"     # generic entity
mush-rgb-state-switch: "var(--mush-rgb-blue)"     # switch ON

# Person presence
mush-rgb-state-person-home:     "var(--mush-rgb-success)"
mush-rgb-state-person-not-home: "var(--mush-rgb-danger)"
mush-rgb-state-person-zone:     "var(--mush-rgb-info)"
mush-rgb-state-person-unknown:  "var(--mush-rgb-grey)"

# Cover
mush-rgb-state-cover-open:   "var(--mush-rgb-blue)"
mush-rgb-state-cover-closed: "var(--mush-rgb-disabled)"

# Alarm
mush-rgb-state-alarm-disarmed:  "var(--mush-rgb-info)"
mush-rgb-state-alarm-armed:     "var(--mush-rgb-success)"
mush-rgb-state-alarm-triggered: "var(--mush-rgb-danger)"

# Climate HVAC modes
mush-rgb-state-climate-auto:      "var(--mush-rgb-green)"
mush-rgb-state-climate-cool:      "var(--mush-rgb-blue)"
mush-rgb-state-climate-dry:       "var(--mush-rgb-orange)"
mush-rgb-state-climate-fan-only:  "var(--mush-rgb-blue-grey)"
mush-rgb-state-climate-heat:      "var(--mush-rgb-deep-orange)"
mush-rgb-state-climate-heat-cool: "var(--mush-rgb-green)"
mush-rgb-state-climate-idle:      "var(--mush-rgb-grey)"
mush-rgb-state-climate-off:       "var(--mush-rgb-disabled)"

# Semantic aliases — used by state mapping above
mush-rgb-info:    "var(--mush-rgb-blue)"
mush-rgb-success: "var(--mush-rgb-green)"
mush-rgb-warning: "var(--mush-rgb-orange)"
mush-rgb-danger:  "var(--mush-rgb-red)"

# ── Mushroom structure (already in Casa5 — listed for completeness) ──
mush-icon-border-radius: "50%"
mush-icon-size:          "54px"
mush-icon-symbol-size:   "0.5em"
mush-spacing:            "12px"
mush-control-border-radius: "var(--ha-card-border-radius, 16px)"
mush-chip-background:    "var(--ha-card-background, white)"
mush-chip-border-radius: "calc(var(--ha-card-border-radius, 16px) + 4px)"
mush-chip-border-color:  "var(--ha-card-border-color, var(--divider-color))"
mush-chip-border-width:  "var(--ha-card-border-width, 1px)"
mush-card-primary-color:   "var(--primary-text-color)"
mush-card-secondary-color: "var(--secondary-text-color)"
mush-title-color:          "var(--primary-text-color)"
mush-subtitle-color:       "var(--secondary-text-color)"
```

---

## #palette-swap-impact

### What changes during a palette swap

When you perform an accent-only or full palette swap, these additional lines
must be updated for Mushroom to stay in sync:

**Accent-only swap — add to the 8 standard accent lines:**

```yaml
# In the mode-independent block (not inside modes:)
accent-color-rgb: "NR, NG, NB"   # ← RGB of new accent hex
# mush-rgb-primary automatically follows via var(--accent-color-rgb)
```

**No other Mushroom changes needed for an accent swap** — the state mappings
point to named colour variables, not the accent. Only `mush-rgb-state-switch`
and `mush-rgb-state-entity` would need updating if you want those to follow
the accent (they currently point to `mush-rgb-blue`).

**To make switches and generic entities follow the accent:**

```yaml
# In mode-independent block — override state mappings to use accent
mush-rgb-state-switch: "var(--mush-rgb-primary)"
mush-rgb-state-entity: "var(--mush-rgb-primary)"
```

**Full palette swap — update Layer 2a base colours if backgrounds shift significantly:**
The disabled colour is the only one that commonly needs updating:

```yaml
modes:
  light:
    mush-rgb-disabled: "189, 189, 189"   # stays the same for light neutrals
  dark:
    mush-rgb-disabled: "111, 111, 111"   # stays the same for dark neutrals
```

For very warm full palettes (like Warm Cream), consider softening `mush-rgb-blue`
slightly toward `45, 50, 65` so entity/switch icons don't clash with the warm bg.

---

## #card-override-limits

### What card-level overrides can and cannot do

**Can override in card YAML (using card_mod or entity `icon_color`):**

```yaml
# Mushroom entity card — override state colour per-card
type: custom:mushroom-entity-card
entity: switch.fan
icon_color: teal         # named colour or CSS colour

# card_mod approach — more control
card_mod:
  style: |
    :host {
      --mush-rgb-state-switch: var(--mush-rgb-teal);
    }
```

**Cannot override from the theme file:**
- `icon_color:` set directly in card YAML always wins over theme state colours
- Template card icon colours are set via `icon_color` in card config, not via
  `mush-rgb-state-*` variables (template card uses `--primary-text-color` by default)

**Priority order (highest wins):**
```
card YAML icon_color:
    > card_mod :host style
    > theme mush-rgb-state-* (Layer 2b)
    > theme mush-rgb-* base colour (Layer 2a)
    > Mushroom default
```

---

## #accent-colour-for-switches

### Wiring switches to the accent colour

The most common customisation request: make switches follow the accent colour
(like Bubble Card active buttons do) rather than the Mushroom default blue.

**Option A — Theme-level (applies to all switches everywhere):**
```yaml
# In mode-independent block
mush-rgb-state-switch: "var(--mush-rgb-primary)"
mush-rgb-state-entity: "var(--mush-rgb-primary)"
```

**Option B — Per-card (only this switch):**
```yaml
type: custom:mushroom-entity-card
entity: switch.my_switch
icon_color: >-
  {{ 'amber' if is_state('switch.my_switch', 'on') else '' }}
```

**Option C — card_mod (no HACS dependency beyond Mushroom):**
```yaml
type: custom:mushroom-entity-card
entity: switch.my_switch
card_mod:
  style: |
    :host {
      --mush-rgb-state-switch: var(--mush-rgb-primary);
    }
```

Option A is the recommended approach for a unified theme. It means every
Mushroom switch and entity card shows the accent colour when active —
identical behaviour to Bubble Card.

---

## #chip-card

### Mushroom chip card — the most common Mushroom component on Bubble Card dashboards

The Mushroom chip card (`mushroom-chips-card`) renders a compact horizontal
row of icon+label chips. It is the most common Mushroom component used
alongside Bubble Card — typically as a glanceable status bar above the HBS
footer, or as a quick-access strip at the top of a pop-up.

**When to use it:**
- Showing presence status (who is home) at a glance
- Quick sensor readings (temperature, humidity, CO2) as a chip strip
- Alarm state indicator
- Weather summary chip

**Basic structure:**
```yaml
type: custom:mushroom-chips-card
chips:
  - type: entity
    entity: person.alice
    content_info: name
    tap_action:
      action: more-info

  - type: entity
    entity: sensor.living_room_temperature
    content_info: state
    icon: mdi:thermometer
    tap_action:
      action: none

  - type: entity
    entity: binary_sensor.motion_living_room
    content_info: none
    icon: mdi:motion-sensor
    tap_action:
      action: none

  - type: weather
    entity: weather.home
    show_conditions: true
    show_temperature: true
    tap_action:
      action: more-info
```

**Chip types available:**

| Type | Use |
|------|-----|
| `entity` | Any HA entity — shows icon + optional state/name |
| `weather` | Weather entity with condition icon + temperature |
| `back` | Navigation back button (for sub-views) |
| `menu` | Opens the sidebar |
| `template` | Full Jinja2 template for icon, content, tap action |
| `alarm-control-panel` | Alarm status chip |
| `spacer` | Empty flexible space between chips |

### Chip card theme variables

These variables are already wired in the mode-independent block of the template.
Override them in the theme for global chip styling.

```yaml
# In mode-independent theme block (or in modes.light/dark for mode-specific)
mush-chip-spacing:       "8px"     # gap between chips
mush-chip-padding:       "0 0.25em"
mush-chip-height:        "36px"    # chip height
mush-chip-border-radius: "19px"    # default: very rounded (pill shape)
mush-chip-border-width:  "var(--ha-card-border-width, 1px)"
mush-chip-border-color:  "var(--ha-card-border-color, var(--divider-color))"
mush-chip-background:    "var(--ha-card-background, white)"  # inherits card bg
mush-chip-font-size:     "0.3em"   # relative to chip height
mush-chip-font-weight:   "bold"
mush-chip-icon-size:     "0.5em"   # relative to chip height
```

**Making chips square (for a more dashboard-like look):**
```yaml
mush-chip-border-radius: "var(--ha-card-border-radius, 16px)"  # matches cards
mush-chip-padding:       "0 12px"
```

### Side-by-side with Bubble Card — full example

The most common pattern: Bubble Card slider controls the entity, Mushroom chip
shows its state. Both pick up the theme accent colour automatically.

```yaml
# Section in a pop-up or view

# Bubble Card slider — controls the light
- type: custom:bubble-card
  card_type: button
  button_type: slider
  entity: light.living_room_ceiling
  name: Ceiling
  light_slider_type: brightness
  card_layout: large

# Mushroom chip strip — glanceable status for the room
- type: custom:mushroom-chips-card
  chips:
    # Light state chip — active icon turns accent colour (via mush-rgb-state-light)
    - type: entity
      entity: light.living_room_ceiling
      content_info: state
      icon: mdi:lightbulb

    # Temperature chip
    - type: entity
      entity: sensor.living_room_temperature
      content_info: state
      icon: mdi:thermometer

    # Presence chip — green when home (via mush-rgb-state-person-home)
    - type: entity
      entity: person.alice
      content_info: name
```

**How the theme integration connects them:**
- Bubble Card active state → `var(--accent-color)` → `mush-rgb-primary` → gold
- Mushroom light chip active → `mush-rgb-state-light` → `mush-rgb-orange` → orange
- Mushroom person home chip → `mush-rgb-state-person-home` → `mush-rgb-success` → green

These are intentionally different: Bubble Card uses the accent colour for active
states, while Mushroom uses semantic domain colours. This is the correct design —
Bubble Card is the control surface, Mushroom is the status surface.

**To make the Mushroom light chip match the Bubble Card accent:**
```yaml
# In mode-independent theme block
mush-rgb-state-light: "var(--mush-rgb-primary)"  # light chip → accent colour
```

---

## #template-chip

### Mushroom template chip — the most powerful chip type

The template chip lets you write Jinja2 to control icon, content, colour,
and tap action. It is the chip type users most often need help with because
it unlocks dynamic behaviour that fixed entity chips cannot express.

**Full template chip structure:**
```yaml
type: custom:mushroom-chips-card
chips:
  - type: template
    icon: >-
      {% if is_state('alarm_control_panel.home', 'disarmed') %}
        mdi:shield-check
      {% elif is_state('alarm_control_panel.home', 'armed_away') %}
        mdi:shield-lock
      {% else %}
        mdi:shield-alert
      {% endif %}
    icon_color: >-
      {% if is_state('alarm_control_panel.home', 'disarmed') %}
        green
      {% elif is_state('alarm_control_panel.home', 'armed_away') %}
        blue
      {% else %}
        red
      {% endif %}
    content: >-
      {{ states('alarm_control_panel.home') | replace('_', ' ') | title }}
    tap_action:
      action: more-info
      entity: alarm_control_panel.home
    hold_action:
      action: navigate
      navigation_path: '#security'
```

**Template chip fields:**

| Field | Type | Description |
|-------|------|-------------|
| `icon` | Jinja2 string | MDI icon name — full expression |
| `icon_color` | Jinja2 string | Named CSS colour or `var(--css-variable)` |
| `content` | Jinja2 string | Label text below/beside icon |
| `badge_icon` | Jinja2 string | Optional small badge icon on the chip |
| `badge_color` | Jinja2 string | Badge colour |
| `picture` | Jinja2 string | Entity picture URL |
| `tap_action` | object | Standard HA action |
| `hold_action` | object | Standard HA action |
| `double_tap_action` | object | Standard HA action |

**Common template chip patterns:**

```yaml
# Presence summary chip — shows count of people home
- type: template
  icon: mdi:account-group
  icon_color: >-
    {% set home = states | selectattr('domain','eq','person')
       | selectattr('state','eq','home') | list | count %}
    {{ 'green' if home > 0 else 'grey' }}
  content: >-
    {% set home = states | selectattr('domain','eq','person')
       | selectattr('state','eq','home') | list | count %}
    {{ home }} home
  tap_action:
    action: navigate
    navigation_path: '#presence'

# Active lights count chip
- type: template
  icon: mdi:lightbulb-group
  icon_color: >-
    {% set on = states.light | selectattr('state','eq','on') | list | count %}
    {{ 'amber' if on > 0 else 'grey' }}
  content: >-
    {% set on = states.light | selectattr('state','eq','on') | list | count %}
    {% if on > 0 %}{{ on }} on{% else %}all off{% endif %}
  tap_action:
    action: navigate
    navigation_path: '#living-room'

# Theme-aware icon colour using CSS variables
- type: template
  icon: mdi:thermometer
  icon_color: "var(--accent-color)"    # uses theme accent directly
  content: "{{ states('sensor.living_room_temperature') }}°"
  tap_action:
    action: none
```

**Colour values for `icon_color` and `badge_color`:**
Named CSS colours (`red`, `green`, `blue`, `orange`, `grey`, `amber`, `teal`),
hex values (`#D9BE8B`), or CSS variables (`var(--accent-color)`).
Mushroom resolves named colours to its `mush-rgb-*` palette internally.

---

## #mushroom-cards-overview

### When to use Mushroom Cards vs Bubble Cards

Both can control the same entities. The choice comes down to layout philosophy:

| Scenario | Use | Reason |
|----------|-----|--------|
| Room pop-up control panel | **Bubble Card** | Full-width sliders, sub-buttons, cover cards — Bubble is designed for this |
| Glanceable status row (chip bar) | **Mushroom chip card** | Compact horizontal chips — Bubble has no equivalent |
| Dashboard room navigation button | **Bubble Card button** | Supports PIR sensor ordering, HBS integration |
| Quick entity state at a glance | **Mushroom entity card** | Smaller footprint than Bubble button |
| Light with colour wheel | **Mushroom light card** | Full HSL/RGB colour picker — Bubble sliders do brightness/temp/hue separately |
| Person/presence display | **Either** | Mushroom person card has photo support; Bubble button shows state only |
| Inside a pop-up as a content card | **Bubble Card** | Native inside Bubble pop-ups; Mushroom cards work but have no Bubble-specific sub-buttons |

### Mushroom entity card — most common alongside Bubble Card

```yaml
type: custom:mushroom-entity-card
entity: light.living_room
name: Living Room Light          # optional — defaults to friendly name
icon: mdi:lightbulb              # optional
icon_color: orange               # static colour OR leave blank for state-based colour
fill_container: false            # true = stretch to fill the section width
tap_action:
  action: toggle
hold_action:
  action: more-info
```

**`icon_color` options:**
Named CSS colours (`red`, `orange`, `green`, `blue`, `purple`, `grey`, `amber`, `teal`)
or `var(--accent-color)` to follow the HA theme accent.

**State-based colour:** leave `icon_color` blank — Mushroom will use the
`mush-rgb-state-*` mapping from the theme (e.g. light → orange by default,
configurable via ZONE 6 in `casa5heynev2-template.yaml`).

### Mushroom light card — RGB colour picker

```yaml
type: custom:mushroom-light-card
entity: light.living_room_rgb
name: Living Room               # optional
show_brightness_control: true   # brightness slider
show_color_control: true        # colour wheel (only for RGB lights)
show_color_temp_control: true   # colour temperature (only for CCT lights)
collapsible_controls: false     # true = hide sliders until tapped
use_light_color: true           # tint the icon background to match the light colour
fill_container: false
```

**When to use vs Bubble Card sliders:**
Use the Mushroom light card when you want a single compact card with all
controls (brightness + colour wheel) in one. Use Bubble Card sliders when
you want separate cards for each dimension inside a pop-up.

### Mushroom person card

```yaml
type: custom:mushroom-person-card
entity: person.alice
layout: horizontal              # horizontal / vertical
fill_container: false
tap_action:
  action: more-info
```

Person cards show the entity picture (profile photo) if set on the person
entity. Bubble Card buttons show a generic icon. Use Mushroom person cards
in presence pop-ups where photos matter.

### Mushroom climate card

```yaml
type: custom:mushroom-climate-card
entity: climate.living_room
show_temperature_control: true  # +/- temperature buttons
fill_container: false
hvac_modes:                     # limit visible HVAC mode buttons
  - heat
  - cool
  - off
```

Compact alternative to Bubble Card climate card for secondary displays.
Bubble Card climate is richer (sub-buttons, full slider); Mushroom climate
is better for at-a-glance chips in a chip bar context.

### Layout option — fill_container

All Mushroom cards support `fill_container: true` which stretches the card
to fill the width of its parent container. Useful in sections grid contexts
where you want Mushroom cards to match the visual weight of Bubble Cards.

