# Streamline Card Reference
# ha-bubble-dashboard skill — Phase 4a
# Source: Streamline Card v0.2.2 README + community issues

---

## #ui-mode-vs-yaml-mode

### Critical: ask before generating template config

Streamline Card behaves differently depending on how the user's Lovelace
dashboards are managed. Always clarify before generating any Streamline config.

**UI-mode (default for most users):**
- Dashboards managed through the HA interface (Settings → Dashboards)
- `!include_dir_named` in dashboard raw config throws a parse error
- **Correct approach:** templates live in the auto-load file:
  `/config/www/community/streamline-card/streamline_templates.yaml`
- No dashboard-level include is needed — Streamline loads this file automatically
- After adding new templates: clear browser cache + restart HA

**YAML-mode (advanced users):**
- `lovelace:` with `mode: yaml` in `configuration.yaml`
- Can use `!include_dir_named` and `!include` in dashboard YAML
- Templates can be split across multiple files
- Dashboard config requires a top-level `streamline_templates:` key

**Ask the user:**
> "Are your dashboards managed through the HA UI (default), or do you use
> YAML-mode Lovelace with a `ui-lovelace.yaml` file?"

---

## #template-anatomy

### Template structure

Every template has up to three parts:

```yaml
# In streamline_templates.yaml (UI-mode) or dashboard config (YAML-mode)

my_template_name:
  default:                      # optional — default values for variables
    - variable_name: "default value"
    - another_variable: "mdi:lightbulb"
  card:                         # use 'card' for Lovelace cards
    type: custom:bubble-card
    card_type: button
    button_type: "[[button_type]]"
    entity: "[[entity]]"
    name: "[[name]]"
    icon: "[[icon]]"
```

**Using the template:**

```yaml
type: custom:streamline-card
template: my_template_name
variables:
  - entity: light.living_room
  - name: Living Room
  - button_type: slider
  # icon uses default value — no need to specify
```

**`card` vs `element`:**
- Use `card:` for standard Lovelace cards (most cases)
- Use `element:` for picture-elements cards

---
---

## #delivery-format

### Template delivery format

Always deliver Streamline output in two clearly labelled blocks:

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

Remind user to clear browser cache after adding new templates.



## #variable-syntax

### `[[variable_name]]` syntax rules

Variables are double-bracket placeholders replaced at render time.

```yaml
# String variable inline — no quotes needed if part of a larger string
name: "[[room_name]] Light"

# Variable as the entire value — MUST use single quotes around the brackets
entity: '[[entity]]'
icon: '[[icon]]'
button_type: '[[type]]'

# In nested objects — use single quotes
tap_action:
  action: navigate
  navigation_path: '[[hash]]'
```

**Rules:**
- If `[[var]]` is the entire YAML value, wrap in single quotes: `'[[var]]'`
- If `[[var]]` is part of a longer string, no extra quotes needed
- Variables not provided at use-time fall back to `default:` values
- Variables with no default and no value are replaced with an empty string

**Default values:**

```yaml
my_light_template:
  default:
    - icon: mdi:ceiling-light        # used when icon is not specified at call site
    - button_type: switch            # used when button_type is not specified
  card:
    type: custom:bubble-card
    card_type: button
    button_type: '[[button_type]]'
    entity: '[[entity]]'
    icon: '[[icon]]'
```

---

## #javascript-keys

### `_javascript` key suffix — dynamic values and styling

Append `_javascript` to any YAML key to evaluate its value as JavaScript.

```yaml
my_template:
  card:
    type: custom:bubble-card
    card_type: button
    button_type: state
    entity: '[[entity]]'
    # Dynamic CSS styling based on entity state
    styles_javascript: |
      const state = states['[[entity]]'].state;
      return `
        .bubble-button-background {
          opacity: 1 !important;
          background-color: ${
            state === 'on' ? 'var(--accent-color)' : 'var(--state-inactive-color)'
          } !important;
        }
      `;
```

**JavaScript context variables:**

| Variable | Description |
|----------|-------------|
| `states` | All HA entity states object — `states['sensor.temp'].state` |
| `user` | Current user object — `user.name`, `user.is_admin` |
| `variables` | All template variables as an object — `variables.entity` |
| `areas` | HA area registry — `areas` is an object keyed by area ID with `name`, `icon`, and `aliases`. Example: `Object.values(areas).filter(a => a.name === 'Kitchen')[0]` |

**`areas` usage examples:**

```yaml
# Show which area an entity belongs to
styles_javascript: |
  const entity = states['[[entity]]'];
  const areaId = entity.area_id;
  const area = areaId ? areas[areaId] : null;
  return `.bubble-name::after { content: " (${area?.name ?? 'unassigned'})"; }`;

# Generate cards for all entities in a named area
area_lights_template:
  card:
    type: grid
    columns: 2
    cards_javascript: |
      const targetArea = Object.values(areas).find(a => a.name === '[[area_name]]');
      if (!targetArea) return [];
      return Object.entries(states)
        .filter(([id, s]) => s.area_id === targetArea.area_id && id.startsWith('light.'))
        .map(([entity]) => ({
          type: 'custom:bubble-card',
          card_type: 'button',
          button_type: 'slider',
          entity
        }));
```

**`cards_javascript` — dynamic card arrays:**

```yaml
lights_grid_template:
  card:
    type: grid
    columns: 3
    cards_javascript: |
      const onLights = states['[[group_entity]]'].attributes.entity_id || [];
      return onLights.map(entity => ({
        type: 'custom:bubble-card',
        card_type: 'button',
        button_type: 'slider',
        entity: entity
      }));
```

**Important:** `_javascript` keys are powerful but add complexity and can fail
silently. Use them only when YAML variables alone cannot express the required
logic. Always test in browser console.

---

## #dry-decision

### When to create a Streamline template

Apply the DRY rule: create a template when the same card structure appears
3 or more times with only variable substitutions.

**Good template candidates:**

```yaml
# Room light button — identical structure, different entity/name/icon
room_light_template:
  default:
    - icon: mdi:ceiling-light
    - button_type: slider
  card:
    type: custom:bubble-card
    card_type: button
    button_type: '[[button_type]]'
    entity: '[[entity]]'
    name: '[[name]]'
    icon: '[[icon]]'
    card_layout: large
    button_action:
      tap_action:
        action: toggle
    hold_action:
      action: more-info

# Usage (repeat for every room light)
- type: custom:streamline-card
  template: room_light_template
  variables:
    - entity: light.living_room_ceiling
    - name: Ceiling
    - icon: mdi:ceiling-light-outline

# Cover card — open/stop/close always same structure
cover_template:
  card:
    type: custom:bubble-card
    card_type: cover
    entity: '[[entity]]'
    name: '[[name]]'
    icon_open: mdi:blinds-open
    icon_close: mdi:blinds
    card_layout: large

# Climate zone — same controls, different entity
climate_zone_template:
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

**Do not template:**
- One-off cards with unique structure
- Cards where the logic differs significantly between instances
- Cards with fewer than 3 instances — inline YAML is cleaner

---

## #file-organisation

### Template file organisation (UI-mode)

All templates live in a single file for UI-mode setups:

```
/config/www/community/streamline-card/streamline_templates.yaml
```

Organise by domain with comments:

```yaml
# ============================================================
# Streamline Templates — Casa5HeyneV2 Dashboard
# ============================================================

# ── Lights ────────────────────────────────────────────────
room_light_template:
  # ...

ceiling_light_slider:
  # ...

# ── Covers ────────────────────────────────────────────────
cover_template:
  # ...

# ── Climate ───────────────────────────────────────────────
climate_zone_template:
  # ...

# ── Sensors ───────────────────────────────────────────────
sensor_chip_template:
  # ...
```

**After editing the file:**
1. Clear browser cache (hard refresh: Ctrl+Shift+R / Cmd+Shift+R) on first setup
2. **After the first visit, Streamline revalidates templates in the background
   automatically** — changes often propagate without a hard refresh. If templates
   don't update, hard refresh is the fallback. HA restart is only required if
   the card itself can't be found (resource not registered).

### `!include` tag — splitting templates across files (UI-mode and YAML-mode)

Streamline's `!include` tag loads an external YAML file relative to the current
file's URL. This works in **both UI-mode and YAML-mode** — it is processed by
Streamline itself, not by HA's YAML parser (unlike `!include_dir_named` which
is HA-only and requires YAML-mode).

```yaml
# streamline_templates.yaml — main file
# Use !include to load templates from separate files

lights: !include templates/lights.yaml
covers: !include templates/covers.yaml
climate: !include templates/climate.yaml
sensor_chips: !include templates/sensors.yaml
```

```
/config/www/community/streamline-card/
  streamline_templates.yaml      ← main file with !include tags
  templates/
    lights.yaml                  ← light-specific templates
    covers.yaml
    climate.yaml
    sensors.yaml
```

**`!include` vs `!include_dir_named`:**

| Feature | `!include` (Streamline) | `!include_dir_named` (HA YAML) |
|---------|------------------------|-------------------------------|
| Works in UI-mode | ✓ Yes | ✗ No |
| Works in YAML-mode | ✓ Yes | ✓ Yes |
| Processes by | Streamline Card | Home Assistant |
| Path is relative to | Current YAML file | config directory |
| Supports nested includes | ✓ Yes | Limited |

**When to use `!include`:** UI-mode users with large template libraries who
want to split templates across multiple files without switching to YAML-mode.
This is the recommended approach for libraries beyond ~20 templates.

### Template file organisation (YAML-mode)

Split by domain using HA's native `!include_dir_named`:

```yaml
# ui-lovelace.yaml or dashboard file
streamline_templates:
  lights: !include_dir_named streamline_templates/lights/
  covers: !include_dir_named streamline_templates/covers/
  climate: !include_dir_named streamline_templates/climate/
```

---

## #known-limitations

### Streamline Card limitations (v0.2.2)

- **No visual editor.** Always shows "Visual editor not supported". YAML-only.
- **No template inheritance.** Cannot chain templates (no `base_template:`).
  Each template is fully self-contained.
- **UI editor templates not accessible from auto-load file.** Templates in
  `streamline_templates.yaml` are loaded for card rendering but not shown in
  the HA dashboard editor template picker.
- **Background revalidation covers most template changes** — a hard refresh
  is usually not needed after editing templates. If a template does not update,
  hard refresh first; HA restart only if the card resource itself is missing.
- **`!include_dir_named` requires YAML-mode.** UI-mode users must use Streamline's
  own `!include` tag or the single auto-load file.
- **`!include` paths are URL-relative** to the YAML file they appear in, not
  to the HA config directory. This differs from HA's `!include` behaviour.

---

## #bubble-card-interaction

### Streamline + Bubble Card interaction patterns

These patterns cover the most common Streamline/Bubble Card combination
gotchas and advanced uses.

#### The [[variable]] substitution timing rule

`[[variable]]` substitution happens BEFORE JavaScript evaluation.
This means variables resolve to plain strings in JS context — which is
exactly what you want for entity IDs:

```yaml
# This WORKS — [[entity]] is replaced with the entity ID string
# before the JS engine sees it
styles_javascript: |
  const s = states['[[entity]]'].state;
  return `.bubble-button-background {
    background: ${s === 'on' ? 'var(--accent-color)' : 'var(--state-inactive-color)'} !important;
  }`;

# This FAILS — you cannot use [[entity]] as a variable reference inside JS
# [[entity]] is not a JS variable, it's a text substitution
styles_javascript: |
  const entityId = [[entity]];   # WRONG — this breaks JS syntax
```

#### Templating sub_button blocks

```yaml
# Template with parameterised sub-buttons
light_with_battery:
  card:
    type: custom:bubble-card
    card_type: button
    button_type: slider
    entity: '[[entity]]'
    name: '[[name]]'
    card_layout: large
    sub_button:
      main:
        - entity: '[[battery_sensor]]'
          show_attribute: true
          attribute: battery_level
          show_icon: true
          icon: mdi:battery
          show_background: false
          show_name: false
          show_state: false

# Usage
- type: custom:streamline-card
  template: light_with_battery
  variables:
    - entity: light.bedroom
    - name: Bedroom
    - battery_sensor: sensor.bedroom_light_battery
```

#### Templating tap_action navigation paths

```yaml
room_nav_button:
  card:
    type: custom:bubble-card
    card_type: button
    button_type: name
    entity: '[[entity]]'
    name: '[[name]]'
    icon: '[[icon]]'
    card_layout: large
    button_action:
      tap_action:
        action: navigate
        navigation_path: '[[hash]]'   # ← hash as variable

# Usage
- type: custom:streamline-card
  template: room_nav_button
  variables:
    - entity: light.living_room_group
    - name: Living Room
    - icon: mdi:sofa
    - hash: '#living-room'
```

#### cards_javascript for dynamic card lists

```yaml
# Generate a card per entity in a group
group_lights_template:
  card:
    type: grid
    columns: 2
    cards_javascript: |
      const groupEntity = states['[[group_entity]]'];
      const members = groupEntity?.attributes?.entity_id || [];
      return members.map(entity => ({
        type: 'custom:bubble-card',
        card_type: 'button',
        button_type: 'slider',
        entity: entity,
        card_layout: 'large',
        light_slider_type: 'brightness'
      }));

# Usage
- type: custom:streamline-card
  template: group_lights_template
  variables:
    - group_entity: light.living_room_group
```

#### Known gotchas

- **Empty `[[variable]]` in YAML value position**: if a variable is not
  provided and has no default, it resolves to empty string. An empty string
  as the entire YAML value (`entity: ''`) will cause the card to error.
  Always provide defaults for required variables.

- **Nested quotes in navigation_path**: if the hash contains a `#`, wrap
  in single quotes at the template level. The `[[hash]]` substitution
  must preserve the quotes: `navigation_path: '[[hash]]'` with
  `- hash: '#kitchen'` at the call site works correctly.

- **`styles_javascript` returning nothing**: if the JS function returns
  `undefined` (e.g. due to a missing entity in `states`), the `styles:`
  block becomes empty and the card loses all custom styling. Always add
  a null check: `const s = states['[[entity]]']?.state ?? 'off';`
