# Bubble Card Reference
# ha-bubble-dashboard skill — Phase 3
# Covers: all card types, CSS variables, JS template API,
#         module workflow, version compatibility.
# Source: Bubble Card v3.2.2 README + release notes v3.0–v3.2

---

## #version-compat

### Breaking changes by version — check before generating

| Version | Change | Impact on generated YAML |
|---------|--------|--------------------------|
| v3.0.0 | New module system (YAML files via Bubble Card Tools). Accent colour changed to accessible blue as new default. `card_layout: large-sub-buttons-grid` added. Hold/double-tap default changed to `none`. `--bubble-border` CSS variable added. | No YAML breakage, but theme must override accent back to your colour. |
| v3.1.0 | Bubble Card Tools becomes recommended module backend. New `card_type: sub-buttons`. Sub-button types: default/slider/select. New `main`/`bottom` sub-button schema. **`subButtonIcon[]` index reordering: bottom sub-buttons indexed first, main sub-buttons after.** | JS templates using `subButtonIcon[N]` for main sub-buttons will be wrong unless reindexed. |
| v3.2.0 | **Pop-ups fully reworked as standalone cards with `cards:` block.** Pop-up content no longer lives in a separate stack. `bubble-pop-up-fix.js` removed entirely. New pop-up modes: `fit-content`, `centered`, `adaptive-dialog`. UI migration prompt shown. | All pre-v3.2 pop-up YAML is invalid. Always generate v3.2 standalone format. |
| v3.2.2 | Bug fixes: empty column height, migration scoping, climate `swing_horizontal_mode`. Stable. | None. |

**Always generate v3.2+ formats.** Never generate the pre-v3.2 pop-up pattern (separate stack + pop-up card at the top of a view). Never reference `bubble-pop-up-fix.js`.

---
**Performance notes:**
- Pop-up content renders lazily — cards update on open, not in background. **v3.2.1+:** `background_update: true` is no longer required and may cause redundant updates — remove it from cards if added in earlier versions.
- `cover_background: true` on media-player cards fetches album art on every state change — avoid on dashboards with many simultaneous media players.
- `auto_order: true` on HBS requires PIR sensors to work well — set `auto_order: false` if no sensors present.
- Streamline `_javascript` keys re-evaluate on every state change — keep JS logic minimal on low-powered devices (Raspberry Pi 3/4).

---



## #pop-up

### Pop-up card — v3.2+ standalone format

Pop-ups are **top-level cards** in a view. They are hidden by default and
opened by navigating to their `hash`. Content cards are defined inside the
pop-up using the `cards:` key — not in a surrounding stack.

```yaml
# CORRECT — v3.2+ standalone format
type: custom:bubble-card
card_type: pop-up
hash: '#living-room'
name: Living Room
icon: mdi:sofa
entity: light.living_room       # optional — colours header by light state
width_desktop: "560px"
with_bottom_offset: true        # required when HBS footer is present
cards:
  - type: custom:bubble-card
    card_type: separator
    name: Lights
    icon: mdi:lightbulb-group
  - type: custom:bubble-card
    card_type: button
    entity: light.living_room_ceiling
    button_type: slider
  # add more cards here
```

```yaml
# WRONG — pre-v3.2 format — NEVER generate this
type: vertical-stack
cards:
  - type: custom:bubble-card
    card_type: pop-up
    hash: '#living-room'
  - type: custom:bubble-card
    card_type: button
    entity: light.living_room
```

**Opening a pop-up from a button:**

```yaml
type: custom:bubble-card
card_type: button
button_type: name
name: Living Room
icon: mdi:sofa
button_action:
  tap_action:
    action: navigate
    navigation_path: '#living-room'
```

### Pop-up options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `hash` | string | **required** | Unique URL hash, e.g. `'#kitchen'`. Lowercase, hyphenated. |
| `name` | string | entity name | Pop-up header title |
| `icon` | string | entity icon | MDI icon for header |
| `entity` | string | — | Optional entity — colours header by state |
| `popup_style` | string | `bubble` | `bubble` or `classic` |
| `popup_mode` | string | `default` | `default` / `fit-content` / `centered` / `adaptive-dialog` / `adaptive-dialog` |
| `with_bottom_offset` | boolean | false | Add bottom offset — set true when HBS footer is present |
| `full_width_on_mobile` | boolean | false | Expand to full width on mobile (use with `centered` mode) |
| `width_desktop` | string | `100%` | Width on desktop, e.g. `560px` |
| `margin_top_mobile` | string | — | Top margin on mobile, e.g. `-56px` if header hidden |
| `bg_color` | string | — | Custom background colour hex/rgba |
| `bg_opacity` | string | — | 0–100, background opacity |
| `bg_blur` | string | — | 0–100, blur (only when bg_opacity < 100) |
| `shadow_opacity` | string | — | 0–100, backdrop shadow |
| `auto_close` | string | — | Timeout ms, e.g. `10000` for 10 s |
| `close_on_click` | boolean | false | Close after any interaction |
| `close_by_clicking_outside` | boolean | true | Click outside to close |
| `trigger_entity` | string | — | Open pop-up when entity reaches `trigger_state` |
| `trigger_state` | string | — | Required with `trigger_entity` |
| `trigger_close` | boolean | false | Close when trigger state leaves `trigger_state` |
| `show_header` | boolean | true | Show/hide the entire header |
| `show_close_button` | boolean | true | Show/hide close button |
| `show_previous_button` | boolean | false | Show back button to previous pop-up |
| `buttons_position` | string | `right` | `right` or `left` for header buttons |
| `cards` | list | — | Content cards (any Bubble Card or HA card type) |
| `open_action` | object | — | Action triggered when pop-up opens |
| `close_action` | object | — | Action triggered when pop-up closes |
| `sub_button` | object | — | Sub-buttons on the pop-up header. **v3.2.1+:** pop-up automatically shows header when sub-buttons are configured. Same `main`/`bottom` schema as button cards. |

**Visual style options:**

| Option | Default | Values | Notes |
|--------|---------|--------|-------|
| `popup_style` | `bubble` | `bubble` / `classic` | `classic` gives a traditional dialog header with title bar appearance |
| `bg_color` | theme bg | any CSS colour | Custom pop-up background colour — use `var(--ha-card-background)` to match cards |
| `bg_opacity` | `88` | 0–100 | Pop-up background opacity — 88 = slightly transparent by default, not 100 |
| `bg_blur` | `10` | 0–100 | Blur applied to the pop-up background |
| `backdrop_blur` | `0` | 0–100 | Blur applied to the backdrop behind the pop-up (separate from `bg_blur`) |
| `shadow_opacity` | `0` | 0–100 | Drop shadow under the pop-up |
| `hide_backdrop` | `false` | bool | Hides the dark overlay entirely (requires page refresh) |
| `margin` | `7px` | CSS value | Centering correction for some themes (e.g. `13px`) |
| `margin_top_mobile` | `0px` | CSS value | Top offset on mobile — use `-56px` if your header is hidden |
| `margin_top_desktop` | `0px` | CSS value | Top offset on desktop — use `50vh` for a half-screen pop-up |
| `width_desktop` | `540px` | CSS value | Width on desktop — mobile is always full width |

**Header controls (all new in v3.2.0):**

| Option | Default | Notes |
|--------|---------|-------|
| `show_header` | `true` | Set `false` to hide the entire header including close/back buttons. Close via long swipe or click outside. |
| `show_close_button` | `true` | Hide the X button while keeping the rest of the header |
| `show_previous_button` | `false` | Show a back/previous button (←) in the header |
| `buttons_position` | `right` | `right` / `left` — position of the header action buttons |

**Behaviour options:**

| Option | Default | Notes |
|--------|---------|-------|
| `close_by_clicking_outside` | `true` | Set `false` to prevent closing when clicking the backdrop. Requires page refresh after change. |
| `close_on_click` | `false` | Close the pop-up after ANY tap or click inside it |
| `auto_close` | — | Milliseconds until auto-close (e.g. `15000` for 15s) |
| `slide_to_close_distance` | `400` | Pixel distance of a downward swipe to close (increase to make harder to dismiss accidentally) |
| `background_update` | `false` | Force cards to update even when pop-up is closed. **Not recommended** — v3.2.1 does intelligent lazy updates by default. Only enable if specific cards don't refresh on open. |
| `performance_mode` | `default` | `default` / `performance` — `performance` slightly delays content rendering and disables backdrop blur for older/slower devices |
| `trigger_close` | `true` | Whether to close the pop-up when trigger conditions are no longer met |
| `main_buttons_position` | `default` | Position of sub-buttons on the pop-up header: `default` (right side of header) / `bottom` (below header as a row) |
| `main_buttons_alignment` | `end` | Alignment when `main_buttons_position: bottom`: `start` / `center` / `end` |
| `main_buttons_full_width` | auto | Whether header sub-buttons span full width. Defaults to `true` when position is `bottom`. |

**Trigger (auto-open) options:**

| Option | Notes |
|--------|-------|
| `trigger` | Array of HA conditions (same format as Lovelace conditional card). Pop-up opens when ALL conditions pass. |
| `trigger_close` | `true` — close when conditions stop being met. Set `false` to keep open. |

```yaml
# Example: open security pop-up when motion detected
trigger:
  - condition: state
    entity: binary_sensor.front_door_motion
    state: "on"
trigger_close: true
```

**Legacy trigger (deprecated, still works):**
`trigger_entity:` + `trigger_state:` — the old way to auto-open. Use `trigger:` conditions array instead.

**popup_mode — when to use each:**

| Mode | Behaviour | Use when |
|------|-----------|----------|
| `default` | Full-height bottom sheet — slides up from the bottom | Room controls, long content lists |
| `fit-content` | Shrinks to content height — slides up from bottom | Short pop-ups with 1–4 cards |
| `centered` | Centered dialog — appears in the middle of the screen | Confirmations, settings, secondary views |
| `adaptive-dialog` | Centered on desktop, bottom sheet on mobile | Mixed device usage — best of both modes |

**empty-column card_type:**
A blank placeholder card (`card_type: empty-column`) that fills a grid column without displaying content.
Useful for alignment in sections grids when you need an empty slot.
```yaml
type: custom:bubble-card
card_type: empty-column
```
| `close_action` | object | — | Action triggered when pop-up closes |

### Pop-up CSS variables

| Variable | Effect |
|----------|--------|
| `--bubble-pop-up-border-radius` | Pop-up corner radius |
| `--bubble-pop-up-main-background-color` | Pop-up body background |
| `--bubble-pop-up-background-color` | Pop-up container background |
| `--bubble-backdrop-background-color` | Backdrop/overlay behind pop-up |

---

## #horizontal-buttons-stack

### Horizontal buttons stack (HBS) — footer navigation

HBS is a scrollable footer that opens pop-ups and can auto-reorder by room
occupancy. **It must be the last card in a view and cannot be inside any stack.**

```yaml
type: custom:bubble-card
card_type: horizontal-buttons-stack
auto_order: true
highlight_current_view: true
is_sidebar_hidden: true          # set true when Sidebar Card is present on desktop
1_name: Living Room
1_icon: mdi:sofa
1_link: '#living-room'
1_entity: light.living_room      # colours the button by light state
1_pir_sensor: binary_sensor.living_room_motion
2_name: Kitchen
2_icon: mdi:chef-hat
2_link: '#kitchen'
2_entity: light.kitchen
2_pir_sensor: binary_sensor.kitchen_motion
3_name: Bedroom
3_icon: mdi:bed
3_link: '#bedroom'
3_entity: light.bedroom
3_pir_sensor: binary_sensor.bedroom_motion
```

**HBS options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `N_link` | string | **required** | Hash or path to navigate to |
| `N_name` | string | — | Button label |
| `N_icon` | string | — | MDI icon |
| `N_entity` | string | — | Light entity — colours button background |
| `N_pir_sensor` | string | — | Motion sensor for `auto_order` |
| `auto_order` | boolean | false | Reorder buttons by last-triggered pir_sensor. Set false if no sensors. |
| `highlight_current_view` | boolean | false | Highlight the active hash button |
| `is_sidebar_hidden` | boolean | false | Fix HBS position when Sidebar Card hides the HA sidebar |
| `rise_animation` | boolean | true | Entrance animation on page load |
| `hide_gradient` | boolean | false | Hide scroll gradient at edges |
| `width_desktop` | string | `100%` | Width on desktop |
| `margin` | string | — | Centering correction on mobile if needed |

---

## #button

### Button card

The most versatile card. Four types: switch (toggle), slider, state (read),
name (label only).

```yaml
# Switch button — toggles entity
type: custom:bubble-card
card_type: button
button_type: switch
entity: switch.living_room_fan
name: Fan
icon: mdi:fan
show_state: true
card_layout: large

# Slider button — light dimmer
type: custom:bubble-card
card_type: button
button_type: slider
entity: light.bedroom_ceiling
name: Ceiling
icon: mdi:ceiling-light
light_slider_type: brightness

# State button — sensor display
type: custom:bubble-card
card_type: button
button_type: state
entity: sensor.living_room_temperature
name: Temperature
show_state: true
card_layout: large
```

**Button options (common):**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entity` | string | required | Entity to control or display |
| `button_type` | string | `switch` | `switch` / `slider` / `state` / `name` |
| `name` | string | entity name | Display name |
| `icon` | string | entity icon | MDI icon |
| `show_state` | boolean | false | Show state text |
| `show_name` | boolean | true | Show name |
| `show_icon` | boolean | true | Show icon |
| `show_attribute` | boolean | false | Show an attribute below the name |
| `attribute` | string | — | Attribute to show (requires `show_attribute: true`) |
| `show_last_changed` | boolean | false | Show last changed time |
| `card_layout` | string | `normal` | `normal` / `large` / `large-2-rows` / `large-sub-buttons-grid` |
| `rows` | number | auto | Override the card's height as a multiplier of the base row height. Values like `1.4` give 40% more height than the default. Useful for fine-tuning spacing when `card_layout: large` is too tall and `normal` is too short, or when sub-buttons need extra vertical room. Decimal values accepted. |
| `rows` | number | — | Height in section view rows |
| `force_icon` | boolean | false | Prefer icon over entity picture |
| `use_accent_color` | boolean | false | Use theme accent instead of light colour (lights only) |
| `scrolling_effect` | boolean | true | Scroll text when it overflows |
| `button_action` | object | — | `tap_action`, `double_tap_action`, `hold_action` on the card body |

**Slider-specific options:**

| Option | Default | Description |
|--------|---------|-------------|
| `light_slider_type` | `brightness` | `brightness` / `hue` / `saturation` / `white_temp` |
| `min_value` | — | Custom min (for non-standard entities) |
| `max_value` | — | Custom max |
| `step` | — | Step increment |
| `slider_live_update` | false | Update entity while sliding (not recommended for all) |
| `slider_fill_orientation` | `left` | `left` / `right` / `top` / `bottom` |
| `allow_light_slider_to_0` | false | Let slider reach 0% (turns off light) |
| `light_transition` | false | Enable smooth brightness transitions |
| `light_transition_time` | 500 | Transition time in ms |
| `tap_to_slide` | false | Tap to activate slider instead of hold |
| `read_only_slider` | false | Display only, no control |

### RGB and colour-temperature lights

For lights that support colour or colour temperature, compose multiple slider
cards — one per dimension. Use `light_slider_type` to target each attribute.

**When to use each slider type:**

| `light_slider_type` | Use when | Entity attribute |
|--------------------|----------|-----------------|
| `brightness` | Any dimmable light | `brightness` (0–255) |
| `white_temp` | Tunable white / CCT lights | `color_temp_kelvin` |
| `hue` | RGB / RGBW lights | `hue` (0–360°) |
| `saturation` | RGB / RGBW lights | `saturation` (0–100%) |

**Full RGB colour-picker pattern — four sliders in a pop-up:**
```yaml
# Inside a pop-up cards: block

- type: custom:bubble-card
  card_type: separator
  name: Ambiance
  icon: mdi:palette

# 1 — Brightness (all dimmable lights)
- type: custom:bubble-card
  card_type: button
  button_type: slider
  entity: light.living_room_rgb
  name: Brightness
  light_slider_type: brightness

# 2 — Colour temperature (if light supports it)
- type: custom:bubble-card
  card_type: button
  button_type: slider
  entity: light.living_room_rgb
  name: Warmth
  light_slider_type: white_temp

# 3 — Hue (colour)
- type: custom:bubble-card
  card_type: button
  button_type: slider
  entity: light.living_room_rgb
  name: Colour
  light_slider_type: hue

# 4 — Saturation
- type: custom:bubble-card
  card_type: button
  button_type: slider
  entity: light.living_room_rgb
  name: Saturation
  light_slider_type: saturation
```

**Practical note:** Most users only need brightness + white_temp. Reserve the
hue/saturation sliders for lights that are genuinely used for colour — adding
them to a tunable-white-only light (which doesn't support hue) has no effect.

**Check `supported_color_modes`** on the entity in Developer Tools → States
before generating colour sliders. If the list contains only `color_temp`, skip
hue and saturation.

### Conditional card visibility

Use `visibility:` to show a card only when a condition is true. This is the
correct pattern — never use JS `display: none` hacks in `styles:` for
structural show/hide.

```yaml
type: custom:bubble-card
card_type: button
button_type: state
entity: sensor.washing_machine_power
name: Washing Machine
show_state: true
visibility:
  - condition: state
    entity: binary_sensor.washing_machine_running
    state: "on"
```

**Supported condition types:**

| Condition | Example |
|-----------|---------|
| `state` | Show when entity has a specific state |
| `numeric_state` | Show when entity value above/below a threshold |
| `screen` | Show only on mobile or desktop |
| `user` | Show only for specific HA users |
| `and` | All conditions must pass |
| `or` | Any condition must pass |

**Use case patterns:**
```yaml
# Show EV charger card only when car is home
visibility:
  - condition: state
    entity: device_tracker.my_car
    state: "home"

# Show high-power warning only when consumption spikes
visibility:
  - condition: numeric_state
    entity: sensor.home_power
    above: 5000

# Show card only on desktop (not mobile)
visibility:
  - condition: screen
    media_query: "(min-width: 768px)"
```

---

## #sub-buttons

### Sub-buttons — v3.1+ schema

Sub-buttons have two positions: `main` (right side of card) and `bottom`
(full-width row below card content). Each section can contain grouped buttons.

```yaml
sub_button:
  main:
    - entity: sensor.battery_level
      show_attribute: true
      attribute: battery_level
      show_icon: true
      icon: mdi:battery
      show_background: false
      show_name: false
      show_state: false
  bottom:
    - name: Quick actions
      buttons_layout: inline
      justify_content: center
      group:
        - entity: light.living_room
          show_name: true
          fill_width: false
        - entity: switch.fan
          show_name: true
          fill_width: false
```

**Sub-button JS template index order (v3.1+):**
Bottom sub-buttons are indexed first, then main sub-buttons.

```yaml
# Example: 2 bottom buttons + 1 main button
# subButtonIcon[0] = first bottom button
# subButtonIcon[1] = second bottom button
# subButtonIcon[2] = first main button
```

**Sub-button options:**

| Option | Type | Description |
|--------|------|-------------|
| `entity` | string | Entity to control/display |
| `name` | string | Label |
| `icon` | string | MDI icon |
| `sub_button_type` | string | `default` / `slider` / `select` |
| `show_background` | boolean | Show background (state-coloured when on) |
| `state_background` | boolean | Colour background by entity state |
| `show_state` | boolean | Show entity state |
| `show_name` | boolean | Show name |
| `show_icon` | boolean | Show icon |
| `show_attribute` | boolean | Show attribute value |
| `attribute` | string | Attribute to display |
| `select_attribute` | string | Opens dropdown for this attribute list |
| `fill_width` | boolean | Fill available width (default true for bottom) |
| `width` | string/number | Custom width (px for main, % for bottom) |
| `custom_height` | number | Custom height in pixels |
| `content_layout` | string | `icon-left` / `icon-top` / `icon-bottom` / `icon-right` |
| `always_visible` | boolean | Slider only — always show expanded |
| `visibility` | object | HA conditional visibility conditions |

---

## #media-player

### Media player card

```yaml
type: custom:bubble-card
card_type: media-player
entity: media_player.living_room_speaker
name: Speaker
card_layout: large
cover_background: true       # blurred album art as card background
show_state: true
min_volume: 0
max_volume: 100
hide:
  power_button: false
  volume_button: false
  previous_button: false
  next_button: false
  play_pause_button: false
```

**Additional options:** `main_buttons_position` (`default` / `bottom`),
`main_buttons_full_width`, `main_buttons_alignment` (`end` / `center` / `start` / `space-between`).

---

## #climate

### Climate card

```yaml
type: custom:bubble-card
card_type: climate
entity: climate.living_room
name: Thermostat
card_layout: large
state_color: true
step: 0.5
sub_button:
  main:
    - name: HVAC mode
      select_attribute: hvac_modes
      show_arrow: true
      state_background: false
```

**Climate-specific options:** `hide_target_temp_low`, `hide_target_temp_high`,
`min_temp`, `max_temp`.

---

## #cover

### Cover card

```yaml
type: custom:bubble-card
card_type: cover
entity: cover.living_room_blinds
name: Blinds
icon_open: mdi:blinds-open
icon_close: mdi:blinds
```

**Cover-specific options:** `icon_up`, `icon_down`, `open_service`,
`stop_service`, `close_service`, `main_buttons_position`.

---

## #select

### Select card — input_select / select entities

```yaml
type: custom:bubble-card
card_type: select
entity: input_select.scene_selector
name: Scene
icon: mdi:palette
show_state: true
```

---

## #separator

### Separator card — section headers inside pop-ups

```yaml
type: custom:bubble-card
card_type: separator
name: Lights
icon: mdi:lightbulb-group
```

Use separators to divide pop-up content into named sections. Always include
both `name` and `icon` — scanability drops significantly without the icon.

---

## #calendar

### Calendar card

```yaml
type: custom:bubble-card
card_type: calendar
entities:
  - entity: calendar.family
    color: '#D9BE8B'
days: 7
limit: 5
show_end: true
show_progress: true
```

---

## #sub-buttons-only

### Sub-buttons only card — chip bars and footer menus

```yaml
# Chip bar example
type: custom:bubble-card
card_type: sub-buttons
hide_main_background: true
sub_button:
  bottom:
    - name: Chips
      buttons_layout: inline
      justify_content: center
      group:
        - entity: person.alice
          show_name: true
          fill_width: false
        - entity: input_boolean.alarm
          show_name: true
          fill_width: false
          name: Alarm
          tap_action:
            action: toggle

# Fixed footer menu
type: custom:bubble-card
card_type: sub-buttons
footer_mode: true
footer_full_width: true
footer_bottom_offset: 16
sub_button:
  bottom:
    - name: Home
      icon: mdi:home
      tap_action:
        action: navigate
        navigation_path: '#home'
    - name: Lights
      icon: mdi:lightbulb
      tap_action:
        action: navigate
        navigation_path: '#lights'
```

---

## #css-variables

### All Bubble Card CSS variables

**Global (apply to all card types when set on `ha-card`):**

| Variable | Effect |
|----------|--------|
| `--bubble-border-radius` | Radius for all supported elements |
| `--bubble-main-background-color` | Main background colour |
| `--bubble-secondary-background-color` | Secondary background |
| `--bubble-accent-color` | Accent colour |
| `--bubble-icon-border-radius` | Icon container radius |
| `--bubble-icon-background-color` | Icon container background |
| `--bubble-sub-button-border-radius` | Sub-button radius |
| `--bubble-sub-button-background-color` | Sub-button background |
| `--bubble-box-shadow` | Box shadow |
| `--bubble-border` | Full border shorthand |

**Per card type (prefix + suffix pattern):**

| Card | Prefix | Available suffixes |
|------|--------|--------------------|
| Button | `--bubble-button-` | `main-background-color`, `border-radius`, `icon-border-radius`, `icon-background-color`, `box-shadow` |
| Pop-up | `--bubble-pop-up-` | `border-radius`, `main-background-color`, `background-color` |
| Media player | `--bubble-media-player-` | `main-background-color`, `border-radius`, `icon-border-radius`, `box-shadow` |
| Climate | `--bubble-climate-` | `main-background-color`, `border-radius`, `button-background-color`, `accent-color` |
| Cover | `--bubble-cover-` | `main-background-color`, `border-radius`, `icon-border-radius`, `box-shadow` |
| Select | `--bubble-select-` | `main-background-color`, `border-radius`, `list-border-radius`, `list-background-color`, `list-width` |
| HBS | `--bubble-horizontal-buttons-stack-` | `border-radius`, `background-color` |
| Sub-buttons | `--bubble-sub-button-` | `border-radius`, `background-color` |
| Slider sub-button | `--bubble-sub-slider-` | `border-radius`, `background-color`, `height` |
| Separator line | `--bubble-line-` | `background-color` |
| Footer | `--bubble-footer-` | `width`, `bottom`, `box-shadow` |

**Sub-button text and content selectors:**
```css
/* Font size for main sub-button labels */
.bubble-sub-button { font-size: 16px !important; }

/* Font size specifically for bottom sub-buttons */
.bubble-sub-button-bottom-container .bubble-sub-button { font-size: 12px !important; }

/* Sub-button icon size */
.bubble-sub-button .bubble-icon { --mdc-icon-size: 18px !important; }
```

**Targeting sub-buttons by position or name:**
```css
.bubble-sub-button-1 { }          /* first sub-button by DOM index */
.bubble-sub-button-2 { }          /* second */
.my-sub-button { }                /* sub-button named "My sub-button" */
.bubble-sub-button-slider-1 { }   /* first slider sub-button */
```

**CSS in card YAML via `styles:`:**
```yaml
styles: |
  ha-card {
    --bubble-main-background-color: var(--ha-card-background) !important;
  }
  .bubble-icon-container {
    background: var(--state-inactive-color) !important;
  }
```

---

## #js-templates

### JavaScript template API

JS templates go in the `styles:` key. CSS property assignments run first;
DOM-modifying statements must come last.

**Available variables:**

| Variable | Type | Description |
|----------|------|-------------|
| `state` | string | State of the card's `entity` |
| `entity` | string | Entity ID string (e.g. `light.kitchen`) |
| `icon` | element | The main icon element — use `icon.setAttribute("icon", "mdi:...")` |
| `subButtonIcon[N]` | element | Sub-button icon — N starts at 0 for first bottom sub-button (v3.1+) |
| `subButtonState[N]` | string | State of Nth sub-button entity |
| `card` | element | The card DOM element |
| `hass` | object | Full HA state object |
| `this` | object | Card config and context |

**Available functions:**

| Function | Use |
|----------|-----|
| `getWeatherIcon(condition)` | Returns MDI icon for a weather condition string |
| `hass.formatEntityState(state)` | Translated state string |
| `hass.formatEntityAttributeValue(state, attr)` | Translated attribute value |

**Example patterns:**

```yaml
# Conditional background colour
styles: |
  .bubble-button-background {
    opacity: 1 !important;
    background-color: ${state === 'on' ? 'var(--accent-color)' : 'var(--state-inactive-color)'} !important;
  }

# Dynamic icon based on state
styles: |
  ${icon.setAttribute("icon", hass.states['vacuum.robot'].state === 'error' ? 'mdi:alert' : 'mdi:robot-vacuum')}

# Show/hide sub-button conditionally (DOM manipulation — must be last)
styles: |
  .bubble-sub-button-1 {
    display: ${hass.states['sensor.battery'].state <= 10 ? '' : 'none'} !important;
  }

# Change card name text
styles: |
  ${card.querySelector('.bubble-name').innerText = "It's " + hass.states['weather.home'].state}
```

**Critical rule:** DOM-modifying statements (`setAttribute`, `.innerText =`)
must always be placed after all CSS property assignments in the `styles:` block.
Mixing order causes the CSS to be treated as JS and breaks both.

---

## #modules

### Bubble Card module workflow

Modules are reusable CSS/JS templates applied across multiple cards.
Stored as YAML files in `/config/bubble_card/modules/` (requires Bubble Card Tools).

**Applying via YAML:**
```yaml
type: custom:bubble-card
card_type: button
entity: light.kitchen
modules:
  - my_module_id
  - another_module_id
```

**Excluding a global module from a specific card:**
```yaml
modules:
  - '!global_module_id'
```

**Module YAML structure (in bubble_card/modules/):**
```yaml
my_module_id:
  name: "My Module Name"
  version: "1.0"
  creator: "YourName"
  supported:
    - button
    - pop-up
  is_global: false
  code: |
    ha-card {
      --bubble-border-radius: 20px;
    }
```

**The "HA default styling" module** (from Module Store) applies HA theme styling
to Bubble Cards automatically. It is optional — the Casa5HeyneV2 theme handles
the same alignment via the var() chain without needing this module.

### Patreon modules (community/paid)

Beyond the free Module Store, Clooos and community members publish additional
modules via Patreon that extend Bubble Card significantly. As of v3.2.1 the
official Patreon modules from Clooos include:

| Module | What it does |
|--------|-------------|
| Bubble Badges v2 | Unlimited icon badges on any sub-button or the main card icon |
| Bubble Weather | Animated weather backgrounds with daily/hourly forecast overlays |
| Bubble Calendar Enhanced | Date/time display on buttons and calendar cards, configurable layout |
| Bubble Neon | Dynamic theme assigning unique vibrant colours to each card automatically |
| Custom Dropdown | Full control over labels, icons, and actions on select cards and sub-buttons |

Patreon: **https://www.patreon.com/Clooos**

**Skill note:** These modules are not documented in this skill — their API may
change between releases and is not publicly versioned. When a user has a Patreon
module installed, acknowledge it exists and advise them to check the module's
own Patreon post for the YAML reference. Do not attempt to generate configuration
for undocumented Patreon module options.

Community-created modules (including Bubble Graph Pro for mini-graph-card integration
by Cedynamix) are shared in the GitHub Discussions section and on Patreon:
https://github.com/Clooos/Bubble-Card/discussions/categories/share-your-custom-styles-templates-and-dashboards

---

## #actions

### Tap, hold, double-tap actions

```yaml
tap_action:
  action: toggle | more-info | navigate | call-service | url | fire-dom-event | none

# Navigate to a pop-up
tap_action:
  action: navigate
  navigation_path: '#kitchen'

# Call a service
tap_action:
  action: call-service
  service: light.turn_on
  target:
    entity_id: light.kitchen
  data:
    brightness_pct: 100

# Open URL
tap_action:
  action: url
  url_path: 'https://example.com'
```

**Note:** When `double_tap_action` is set, `tap_action` has a 200 ms delay.
Set `double_tap_action: action: none` to disable and restore instant tap response.

---

## #entity-domain-map

### Entity domain → Bubble Card type mapping

Use this table whenever the entity domain is unfamiliar or the user hasn't
specified what card type to use. Always verify with `#version-compat` first.

| Entity domain | Primary card type | button_type / notes |
|---------------|-------------------|---------------------|
| `light` | `button` | `slider` (brightness) or `switch` (toggle only) |
| `switch` | `button` | `switch` |
| `input_boolean` | `button` | `switch` |
| `script` | `button` | `switch` (tap runs script) |
| `scene` | `button` | `switch` (tap activates scene) |
| `automation` | `button` | `switch` (toggles on/off) |
| `climate` | `climate` | — |
| `cover` | `cover` | — |
| `media_player` | `media-player` | — |
| `input_select` | `select` | — |
| `select` | `select` | — |
| `fan` | `button` | `switch` for on/off; add sub-button with `select_attribute: percentage` for speed |
| `vacuum` | `button` | `switch` for start/stop; add sub-button for `status` attribute display |
| `alarm_control_panel` | `button` | `state` display; tap_action: `more-info` for arming UI |
| `lock` | `button` | `switch` (toggles lock/unlock); always add `hold_action: more-info` |
| `camera` | `button` | `state` with `camera_image` entity_picture; use pop-up with `centered` mode for full view. **Note: use `picture-entity` (native HA card) for live streams — Bubble Card does not support camera live video directly.** |
| `humidifier` | `button` | `switch` for on/off; add sub-button `select_attribute: mode` |
| `number` | `button` | `slider` with `min_value` / `max_value` / `step` matching entity |
| `input_number` | `button` | `slider` same as `number` |
| `timer` | `button` | `state` showing remaining time; `button_type: switch` starts/cancels |
| `counter` | `button` | `state` showing count value |
| `input_text` | `button` | `state` display only; edit via `more-info` tap |
| `person` | `button` | `state` showing home/not_home; icon from entity picture |
| `device_tracker` | `button` | `state` display; icon tracks presence |
| `binary_sensor` | `button` | `state` — use `show_state: false`, rely on icon + colour |
| `sensor` | `button` | `state` with `show_state: true`; or use sub-button chip |
| `weather` | `button` | `state` with `show_state: true`; JS template for weather icon |
| `input_datetime` | `button` | `state` display; `more-info` for picker |
| `calendar` | `calendar` | multiple entities supported |
| `update` | `button` | `state` — shows update available; `more-info` to install |
| `button` (HA domain) | `button` | `switch` — tap calls `button.press` |
| `event` | `button` | `state` display only — read-only domain |

### Sub-button patterns for complex domains

```yaml
# Fan — on/off switch + speed selector sub-button
type: custom:bubble-card
card_type: button
button_type: switch
entity: fan.living_room
name: Fan
card_layout: large
sub_button:
  main:
    - name: Speed
      select_attribute: percentage
      show_arrow: false
      show_state: true
      show_background: false

# Vacuum — start/stop + status sub-button
type: custom:bubble-card
card_type: button
button_type: switch
entity: vacuum.robot
name: Robot
icon: mdi:robot-vacuum
card_layout: large
sub_button:
  main:
    - show_state: true
      show_icon: true
      show_background: false
      show_name: false

# Lock — toggle with hold-to-more-info safety
type: custom:bubble-card
card_type: button
button_type: switch
entity: lock.front_door
name: Front Door
icon: mdi:door-closed-lock
card_layout: large
button_action:
  tap_action:
    action: toggle
  hold_action:
    action: more-info

# Number — slider mapped to entity min/max
type: custom:bubble-card
card_type: button
button_type: slider
entity: number.heating_setpoint
name: Setpoint
min_value: 5
max_value: 30
step: 0.5
```

---

## #module-authoring

### Writing Bubble Card modules — complete guide

Modules are reusable CSS/JS applied across cards. They live in
`/config/bubble_card/modules/` as `.yaml` files (requires Bubble Card Tools).

**Complete module YAML structure:**

```yaml
# /config/bubble_card/modules/my-module.yaml
my_module_id:
  name: "Human-readable name"
  description: "What this module does"
  version: "1.0"
  creator: "YourName"
  supported:
    # List card types this module applies to. Options:
    # button | pop-up | climate | cover | media-player
    # select | separator | calendar | sub-buttons |
    # horizontal-buttons-stack | all
    - button
    - pop-up
  is_global: false    # true = auto-applies to ALL supported cards
                      # false = only applies when explicitly listed
  variables:          # optional — user-configurable values
    - name: radius
      label: "Border radius"
      default: "16px"
      type: text
  code: |
    ha-card {
      --bubble-border-radius: {{radius}};
      border: 1px solid var(--divider-color) !important;
    }
    .bubble-icon-container {
      background: var(--state-inactive-color) !important;
    }
```

**Global module pattern — apply across all buttons:**
```yaml
ha_default_bridge:
  name: "HA Theme Bridge"
  description: "Ensures Bubble Card inherits HA theme colours"
  version: "1.0"
  supported:
    - all
  is_global: true
  code: |
    ha-card {
      --bubble-accent-color: var(--primary-color) !important;
      --bubble-icon-background-color: var(--state-inactive-color) !important;
      --bubble-button-accent-color: var(--accent-color-background-opacity) !important;
    }
```

**Scoped module — apply only to light buttons:**
```yaml
light_card_style:
  name: "Light Card Style"
  description: "Enhanced styling for light control buttons"
  supported:
    - button
  is_global: false
  code: |
    ha-card {
      --bubble-border-radius: 20px;
    }
    .bubble-button-background {
      transition: background-color 0.3s ease !important;
    }
```

**Applying a module to a card:**
```yaml
type: custom:bubble-card
card_type: button
entity: light.living_room
modules:
  - light_card_style           # scoped module
  - '!ha_default_bridge'       # exclude a global module from this card
```

**Module variable interpolation ({{variable}} syntax):**
```yaml
# In module definition
variables:
  - name: glow_color
    label: "Glow colour"
    default: "var(--accent-color)"
    type: text
code: |
  ha-card {
    box-shadow: 0 0 12px {{glow_color}} !important;
  }

# At use site (Bubble Card module editor or YAML)
# Variables are set in the Module Store UI editor
```

**When to use modules vs styles::**

| Need | Use |
|------|-----|
| Same CSS on 5+ cards | Module (is_global: false) |
| Same CSS on ALL cards of a type | Module (is_global: true) |
| One-off override on a single card | `styles:` key in card YAML |
| Dynamic CSS based on entity state | `styles:` with JS template |
| Reusable AND configurable per card | Module with `variables:` |

---

## #touch-targets

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
