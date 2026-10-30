# Bubble Card Reference
# ha-bubble-dashboard skill — Phase 3
# Covers: all card types, CSS variables, JS template API,
#         module workflow, version compatibility.
# Source: Bubble Card v3.4.2 source tree (src/) + release notes v3.0–v3.4.2

---

## #version-compat

### Breaking changes by version — check before generating

| Version | Change | Impact on generated YAML |
|---------|--------|--------------------------|
| v3.0.0 | New module system (YAML files via Bubble Card Tools). Accent colour changed to accessible blue as new default. `card_layout: large-sub-buttons-grid` added. Hold/double-tap default changed to `none`. `--bubble-border` CSS variable added. | No YAML breakage, but theme must override accent back to your colour. |
| v3.1.0 | Bubble Card Tools becomes recommended module backend. New `card_type: sub-buttons`. Sub-button types: default/slider/select. New `main`/`bottom` sub-button schema. **`subButtonIcon[]` index reordering: bottom sub-buttons indexed first, main sub-buttons after.** | JS templates using `subButtonIcon[N]` for main sub-buttons will be wrong unless reindexed. |
| v3.2.0 | **Pop-ups fully reworked as standalone cards with `cards:` block.** Pop-up content no longer lives in a separate stack. `bubble-pop-up-fix.js` removed entirely. New pop-up modes: `fit-content`, `centered`, `adaptive-dialog`. UI migration prompt shown. | All pre-v3.2 pop-up YAML is invalid. Always generate v3.2 standalone format. |
| v3.2.2 | Bug fixes: empty column height, migration scoping, climate `swing_horizontal_mode`. Stable. | None. |
| v3.2.3 | Smart entity/card suggestions in the editor (HA 2026.6 integration, editor UX only). `close_action` now fires only on manual pop-up close, not during navigation between pop-ups — fixes nested pop-up navigation. Fixed pop-up header background-color leaking onto child cards. Fixed pop-ups staying visible on iOS due to an HA 2026.5.x sections-layout DOM change. | No YAML changes. If troubleshooting nested-pop-up navigation, confirm the user is on v3.2.3+. |
| v3.2.4 | **Standalone pop-ups nested inside `vertical-stack` / `vertical-stack-in-card` now work correctly** (create, edit, remove, duplicate, move) — this pattern was broken/unreliable in v3.2.0–v3.2.3. Editor now shows an explicit "Nested pop-ups are not supported" warning card if a pop-up is placed inside another pop-up's own `cards:` block (this was always unsupported, just silent before). Improved module-editor object selector for module developers (groups, conditionals, variants — editor UI only, not YAML-facing). Various perf/cleanup fixes for pop-up DOM lifecycle. | If a recipe wraps a Bubble pop-up inside `vertical-stack`/`vertical-stack-in-card`, note it requires v3.2.4+. Never generate a pop-up nested inside another pop-up's `cards:` — this remains unsupported at every version. |
| v3.2.5 | **Cover tilt support** — new `tilt_buttons` (position or `hidden`), `open_tilt_service`, `close_tilt_service` on the cover card, `cover_slider_type: tilt_position` on cover sliders and slider sub-buttons. Editor shows the tilt panel only when the entity reports `OPEN_TILT`/`CLOSE_TILT`/`SET_TILT_POSITION`. Pop-ups inside `grid`/masonry layout boundaries no longer hide the shared `hui-card`; improved pop-up shell detach on leaving editor mode. | Purely additive. Tilt YAML requires v3.2.5+ — on older versions the options are ignored. |
| v3.3.0 | **Platform conditions** — HA's own `domain.name` conditions (`sun.is_up`, `motion.is_detected`, `climate.is_heating`… 141 total) now evaluate client-side in `visibility:`. **`grid_options`** supported for native sections sizing. **Editor translations moved** — the `translations/` folder is gone; dictionaries now sit beside `bubble-card.js` as `bubble-card-<lang>.json`. Dropdown component rewritten with HA 2026.3+ frontend detection (`ha-picker-field`). Legacy `style_templates:` auto-migrates to `modules:`. | Additive for YAML. **Manual installs must delete the old `translations/` folder** and copy the new JSON files; HACS handles it automatically. Platform conditions require v3.3.0+ — on older versions they silently degrade to a state check. |
| v3.4.0 | **`state_content`** — one list replaces `show_state`, `show_attribute`, `attribute`, `show_last_changed` and `show_last_updated`, matching how HA writes its tile card and badges. **Home Assistant (Jinja2) templates** now work in `name`, `icon`, sub-button `name` and inside `state_content` items, alongside the existing JS `${ }` templates in `styles:`. **`popup_style: home-assistant`** — a third pop-up style that reproduces the whole more-info dialog, not just its header. Large render-performance rework (render gate, deferred card updates, lazy editor previews). | Additive and backward-compatible: the five legacy keys keep working and are read into the same list. **But opening a card in the visual editor rewrites them to `state_content` on save.** Generate `state_content` for v3.4.0+ and the legacy keys below it. |
| v3.4.1 | **`slide_to_close`** on pop-ups — `true` (default) / `header` / `false`. Sub-button icons and text pick light or dark by **measured WCAG contrast** against the background they actually paint, replacing a luminance threshold; new `--bubble-sub-button-light-text-color`. Release of a swipe continues at the speed of the finger. Fixes v3.4.0 regressions: a pop-up header left on screen after navigating back, the dashboard shifting sideways when a pop-up opens. | Additive. `slide_to_close` is ignored on older versions, so the gesture stays enabled there — a pop-up you need undismissable needs v3.4.1+. If you had written a `styles:` override to force a dark icon on a light sub-button, **remove it** on v3.4.1+: the card now decides, and the override fights it. |
| v3.4.2 | **Four new dropdown lists** — `fan_speed_list` (vacuum), `activity_list` (remote), `direction` (fan), `alarm_modes` (alarm panel, with an in-menu keypad when a code is needed). **`popup_style: home-assistant` now takes the full more-info sheet height on mobile** unless `popup_mode: adaptive-dialog`. **Calendar: tapping an event opens HA's event dialog** (description + location) and `event_action.tap_action` now defaults to `more-info`; the card also subscribes to the event list, so edits to any event show at once. `subButtonState[]` indexing fixed (#2165). Legacy pop-ups in a `grid` card are migratable and inherit the container's placement and `visibility:`. Memory leak on slider sub-buttons fixed. HA 2026.10 duplicate-user condition worked around. Old-Safari dropdown fix (#2663). | **Behaviour change on upgrade:** an existing `popup_style: home-assistant` pop-up with no `popup_mode` becomes full-height on mobile — add `popup_mode: adaptive-dialog` to keep it content-height. `event_action` left unset now makes events tappable; set `event_action: {tap_action: {action: none}}` to keep them inert. Everything else is additive. |

> **Card order inside a pop-up affects how fast it feels.** Since v3.4.0 a
> large pop-up renders only enough leading cards to fill the first viewport
> before the open transition — the fold is estimated from each card's grid
> span, with no layout read — and the rest start as placeholder cells that
> hydrate one budgeted step at a time afterwards. Off-screen cards also skip
> `hass` updates until they scroll into view.
>
> So the cards a user needs first should be **first in the `cards:` list**, not
> merely visually prominent. This is the same ordering the engagement-type
> model already asks for; it now has a measurable payoff. A pop-up whose most-
> used control sits below the fold makes the user wait for hydration before
> they can touch it.

> **Why pop-ups must be top-level cards, mechanically.** A pop-up suspends the
> layout cell (`hui-card`) that hosts it so it reserves no height in the view.
> A pop-up placed directly inside a grid, masonry or `layout-card` container
> has no cell of its own — the nearest one wraps the whole view, and suspending
> that would collapse every card. Bubble Card therefore treats a layout or view
> host as a boundary and suspends nothing, so the pop-up reserves visible empty
> space in the layout. This is the mechanism behind the placement rule, not
> just a convention.

**Always generate v3.2+ formats.** Never generate the pre-v3.2 pop-up pattern (separate stack + pop-up card at the top of a view). Never reference `bubble-pop-up-fix.js`. Never nest a `card_type: pop-up` inside another pop-up's `cards:` block — always unsupported, and v3.2.4+ surfaces an explicit editor warning for it.

---
**Performance notes:**
- Pop-up content renders lazily — cards update on open, not in background. **v3.2.1+:** `background_update: true` is no longer required and may cause redundant updates — remove it from cards if added in earlier versions.
- `cover_background: true` on media-player cards: **the old "fetches on every state change" warning no longer holds.** The crossfade was rewritten (v3.4.0 lineage) to key on the target image — asking for the same art again does nothing, one fade runs at a time with later requests queued rather than stacked, and only the last queued request survives, so holding "next" costs one extra fade instead of one per press. A playing player emitting many updates per second no longer re-fetches. Reasonable to use on several simultaneous players; the remaining cost is image decode, not repeated fetching.
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
| `hash` | string | **required** | URL hash, e.g. `'#kitchen'`. Lowercase, hyphenated. Must be unique **within a dashboard** — registration is keyed on the dashboard path, so the same hash on two different dashboards is fine and common (`#settings` on each). |
| `name` | string | entity name | Pop-up header title |
| `icon` | string | entity icon | MDI icon for header |
| `entity` | string | — | Optional entity — colours header by state |
| `popup_style` | string | `bubble` | `bubble` / `classic` / `home-assistant` (v3.4.0+). `classic` borrows HA's more-info **header**; `home-assistant` reproduces the whole dialog — geometry, surface and header. On < 3.4.0 an unknown value falls back to `bubble`, so a `home-assistant` pop-up silently looks like a Bubble one. |
| `popup_mode` | string | `default` | `default` / `fit-content` / `centered` / `adaptive-dialog`. **With `popup_style: home-assistant` only two of them are read** — see the mode table below. |
| `with_bottom_offset` | boolean | false | Add bottom offset — set true when an HBS footer is present. Read with `popup_mode: fit-content`, `adaptive-dialog`, **and with `popup_style: home-assistant` in any mode** (v3.4.2+), because that style is a sheet on a narrow screen whatever its mode says. |
| `slide_to_close` | boolean / string | `true` | **v3.4.1+.** `true` — swipe down anywhere in the pop-up to close. `header` — only a swipe starting on the header closes it, so a map, a chart or a scrollable list inside the pop-up can be dragged freely. `false` — off. Ignored below v3.4.1, where the gesture is always on. |
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
| `close_on_click` | `false` | Close the pop-up after ANY tap or click inside it. On touch, a scroll or a drag does **not** close it — movement beyond ~10 px is read as a gesture rather than a tap. Native HA buttons inside a pop-up work too (they suppress the synthetic click; Bubble Card compensates since v3.4.0). |
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

**With `popup_style: home-assistant`, the mode means something else.** That
style carries the more-info dialog's own geometry — a sheet on a narrow screen,
a dialog on a wide one — so it is not the mode's job to decide that any more.
All the mode still decides is the height of that sheet, and only two values are
read:

| `popup_mode` | Sheet on mobile | Use when |
|---|---|---|
| `default` (or unset) | **Full height**, exactly like HA's more-info dialog — the close button and the content sit in the same place every time it opens | Room pop-ups opened one after another; anything a user reaches for repeatedly |
| `adaptive-dialog` (or `fit-content`) | Follows its content | A pop-up with two or three cards, where a full-height sheet would be mostly empty |

`centered` sets nothing here. Generating it alongside
`popup_style: home-assistant` is not an error, it just does nothing — which is
worse, because the YAML reads as if it did.

> **This changed in v3.4.2.** Before it, the HA style was always content-height
> and the editor disabled the mode control. An existing
> `popup_style: home-assistant` pop-up with no `popup_mode` therefore **becomes
> full-height on mobile** when the user updates. If they liked the old look, add
> `popup_mode: adaptive-dialog`. Mention this when touching a dashboard that
> already uses the HA style.

> **`performance_mode: performance` behaves differently per mode.** Its content
> deferral — building the pop-up's cards only after the slide has finished —
> applies **only to `popup_mode: default`**. Upstream tried extending it to
> `adaptive-dialog` and reverted: on an iPad 6 the other effects of performance
> mode (no backdrop blur, lighter opening CSS) already gave a clean transition,
> while deferring the content pushed the open 120 ms past the end of the slide.
> So on the non-default modes, performance mode still helps — just not through
> deferral. Don't pair `performance_mode` with a non-default `popup_mode`
> expecting the deferral benefit.

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
| `scrolling_effect` | boolean | true | Scroll (marquee) text that overflows its container. Only text that actually overflows scrolls, so leaving it on costs nothing for short labels. A running marquee holds a composited layer, but only while the element is genuinely on screen — so many scrolling labels on a long dashboard do not each pay for one. Turn it off where a label must stay still (a wall panel, per the motion-sensitivity rule in SKILL.md §2). |
| `button_action` | object | — | `tap_action`, `double_tap_action`, `hold_action` on the card body |
| `show_last_updated` | boolean | false | Show last updated time (counterpart to `show_last_changed`) |
| `sub_button_justify_content` | string | — | Alignment of the sub-button row: any CSS `justify-content` value (`flex-start`, `center`, `space-between`…) |
| `grid_options` | object | — | Native HA sections sizing: `{rows, columns}`. Set by the HA card-resize UI; prefer it over `rows:` when the card sits in a sections view (v3.3.0+). |

**Slider-specific options:**

| Option | Default | Description |
|--------|---------|-------------|
| `light_slider_type` | `brightness` | `brightness` / `hue` / `saturation` / `white_temp` |
| `min_value` | entity's own | Override. Left unset, the slider reads the entity: `min_temp` for climate, the `min` attribute otherwise, falling back to 0. |
| `max_value` | entity's own | Override. Same chain: `max_temp` for climate, the `max` attribute otherwise, falling back to 100. |
| `step` | — | Step increment |
| `slider_live_update` | false | Update entity while sliding (not recommended for all) |
| `slider_fill_orientation` | `left` | `left` / `right` / `top` / `bottom` |
| `allow_light_slider_to_0` | false | Let slider reach 0% (turns off light) |
> **Don't restate the entity's own range.** `min_value`, `max_value` and
> `step` are overrides that take precedence over the entity; left unset the
> slider reads `min_temp`/`max_temp` for climate and the `min`/`max`/`step`
> attributes otherwise. Copying the current attribute values into the card
> freezes them — the card keeps the old range after the entity's is changed in
> HA. Set them only to deliberately narrow a range (a dimmer capped at 80%),
> and say so in a comment.
>
> A safety clamp applies if the resulting max is not above the min: climate
> gets min + 1, everything else min + 100. A slider that behaves oddly at a
> pinned value is usually a min/max override colliding with the entity.

| `slider_value_position` | `right` | `right` / `left` / `center` / `hidden` — where the value label sits |
| `relative_slide` | false | Slide relative to the current value instead of jumping to the touch point. Mutually exclusive with `tap_to_slide`. |
| `invert_slider_value` | false | Invert the displayed value (e.g. show "closed %" instead of "open %") |
| `cover_slider_type` | `position` | `position` / `tilt_position` — which cover attribute the slider drives (v3.2.5+) |
| `hue_force_saturation` | false | With `light_slider_type: hue`, keep saturation fixed while sliding hue |
| `hue_force_saturation_value` | — | The saturation value (0–100) held when `hue_force_saturation: true` |
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

**Check `supported_color_modes`** on the entity in **Tools** → States
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
| `not` | Inverts the nested conditions |
| `time` | Time-of-day / weekday windows |
| `location` | Person or device_tracker in a zone |
| `template` | Jinja2 template evaluating truthy |
| `view_columns` | Show depending on the view's column count |

> **Cost note — `time` and `template` conditions in a pop-up header.** Bubble
> Card skips re-rendering the pop-up header while nothing the header depends on
> has moved, which it works out from the entities the conditions reference.
> A `condition: time` or `condition: template` cannot be tracked that way, so a
> single one on any header sub-button forces the **whole header to refresh on
> every HA state change, anywhere in the installation**. The same applies to a
> relative-time field (`last_changed`, `last_updated`) in the header.
>
> That is acceptable for one pop-up and expensive on a wall panel with a dozen.
> Where an entity-based equivalent exists, prefer it: `condition: state` on an
> `input_boolean` an automation flips at the time in question costs nothing at
> rest, and the automate-first principle already points that way.

**Platform conditions (v3.3.0+).** Bubble Card now also evaluates Home
Assistant's own `domain.name` conditions client-side — the ones the native
condition builder offers, such as `sun.is_up`, `motion.is_detected`,
`climate.is_heating`, `lock.is_unlocked`, `zone.in_zone`,
`select.is_option_selected`. 141 of them are supported.

```yaml
# v3.3.0+ — a platform condition, not a Lovelace one
visibility:
  - condition: sun.is_up
    entity_id: sun.sun
```

Prefer them where they express the intent more directly than a `state`
comparison: `condition: climate.is_heating` is clearer and more robust than
matching `hvac_action` against a string.

**Caveats — these are client-side ports, not the server evaluating them:**
- Anything requiring astral maths is approximated. Sun elevation bands are
  read from `sun.sun` rather than computed.
- `for:` durations are derived from `last_changed`/`last_updated` without the
  recorder's priming pass, so a condition that was already true before the
  last state change can read as shorter than HA would report.
- Recorder-history-based conditions cannot be ported at all.
- Unsupported condition types fall back to being treated as a `state`
  condition and log a console warning — they do not fail loudly.

On Bubble Card < 3.3.0 a platform condition is an unknown type: it degrades to
a state check and will not behave as intended. Only generate these when the
user is on v3.3.0+.

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
    - entity: sensor.device_battery       # a battery SENSOR, not an attribute
      show_state: true
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

**Mixing loose sub-buttons with explicit groups changes the order.** When a
section contains both, Bubble Card collects *all* the loose ones into a single
automatic group and places it where the **first** of them appeared — it does
not interleave them with the explicit groups in YAML order. So this:

```yaml
main:
  - entity: sensor.a          # loose
  - name: Controls            # explicit group
    group: [...]
  - entity: sensor.b          # loose
```

renders as `[a, b]` first, then the Controls group — not `a, Controls, b`.
The editor does the same thing when it converts a mixed section.

**If order matters, make every section explicit**: put the loose buttons into
their own group with `buttons_layout: inline`, positioned where you want them.
A section of only loose buttons is unaffected — they stay on one line in
declaration order.

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
| `select_attribute` | string | Opens a dropdown for this list. **Only the fourteen names in `#select-attribute` work** — any other attribute renders an empty dropdown that does nothing, with no error. |
| `fill_width` | boolean | Fill available width (default true for bottom) |
| `width` | string/number | Custom width (px for main, % for bottom) |
| `custom_height` | number | Custom height in pixels |
| `content_layout` | string | `icon-left` / `icon-top` / `icon-bottom` / `icon-right` |
| `always_visible` | boolean | Slider only — always show expanded |
| `visibility` | object | HA conditional visibility conditions |

---

## #select-attribute

### `select_attribute` — the only fourteen values that work

A dropdown sub-button (`sub_button_type: dropdown`) and the select card
(`card_type: select`) both read `select_attribute`. It is **not** "any
attribute": it is a closed list, hard-coded in
`src/components/dropdown/lists.js`. An `input_select` or `select` entity needs
no `select_attribute` at all — its `options` are used directly.

| `select_attribute` | Domain | Service called | Since |
|---|---|---|---|
| `hvac_modes` | climate | `climate.set_hvac_mode` | 3.0 |
| `fan_modes` | climate | `climate.set_fan_mode` | 3.0 |
| `swing_modes` | climate | `climate.set_swing_mode` | 3.0 |
| `swing_horizontal_modes` | climate | `climate.set_swing_horizontal_mode` | 3.2.2 |
| `preset_modes` | climate, fan, humidifier… | `<domain>.set_preset_mode` | 3.0 |
| `available_modes` | humidifier | `humidifier.set_mode` | 3.0 |
| `operation_list` | water_heater | `water_heater.set_operation_mode` | 3.0 |
| `effect_list` | light | `light.turn_on` with `effect` | 3.0 |
| `source_list` | media_player | `media_player.select_source` | 3.0 |
| `sound_mode_list` | media_player | `media_player.select_sound_mode` | 3.0 |
| `fan_speed_list` | vacuum | `vacuum.set_fan_speed` | **3.4.2** |
| `activity_list` | remote | `remote.turn_on` with `activity` | **3.4.2** |
| `direction` | fan | `fan.set_direction` | **3.4.2** |
| `alarm_modes` | alarm_control_panel | `alarm_control_panel.alarm_arm_*` / `alarm_disarm` | **3.4.2** |

**The failure mode is silence.** The card reads
`state.attributes[select_attribute]`, and only renders options if that value is
an array. A name that is not on this list — or one that holds a number rather
than a list — produces a dropdown that opens empty and changes nothing. No
console error, no fallback. Two names that look right and are not:

- **`percentage` on a fan.** It is a number, not a list. A fan's speed belongs
  on a slider (`sub_button_type: slider`) or, for named speeds, on
  `preset_modes`.
- **`mode` on a humidifier.** The attribute holding the list is
  `available_modes`; `mode` holds the current one.

**Two of the four new names are computed, not read.** `direction` and
`alarm_modes` are not attributes at all:

- `direction` is offered only when the fan reports the `SET_DIRECTION` feature
  (`supported_features & 4`). The two options (`forward`, `reverse`) come from
  HA, not from the entity, so a fan that has not reported a direction yet still
  gets the dropdown.
- `alarm_modes` is built from the panel's `supported_features`. `disarmed` is
  always offered; each armed mode only if its bit is set.

### Alarm panels — the keypad path

With `select_attribute: alarm_modes` the code prompt is handled for you, but
along three different routes depending on the installation:

| Situation | What happens |
|---|---|
| Panel has no `code_format` | Mode changes immediately |
| `code_arm_required: false`, arming | Arms immediately; disarming still asks |
| A default code is stored on the entity (Settings → entity → alarm options) | HA sends it; no prompt |
| `code_format: number`, HA frontend 2026.3+ | A 12-key keypad replaces the dropdown's options **inside the menu**; a wrong code shakes the dots and clears |
| `code_format: text` (letters), or HA frontend < 2026.3 | The more-info dialog opens instead — the menu has no room for a text field |

So on HA below 2026.3 the gesture leaves the card. Don't promise an in-card
keypad without checking the frontend version.

```yaml
# Arm/disarm from a sub-button — v3.4.2+, HA 2026.3+ for the in-menu keypad
type: custom:bubble-card
card_type: button
button_type: name
entity: alarm_control_panel.home
name: Alarm
sub_button:
  - entity: alarm_control_panel.home
    sub_button_type: dropdown
    select_attribute: alarm_modes
    show_background: true
```

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
`hide_temperature` (hide the current-temperature readout entirely),
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

**Tilt support (v3.2.5+)** — for venetian blinds and any cover reporting
`OPEN_TILT` / `CLOSE_TILT` / `SET_TILT_POSITION`:

```yaml
type: custom:bubble-card
card_type: cover
entity: cover.living_room_venetian
name: Venetian blinds
tilt_buttons: top          # top (default) / bottom / left / right / hidden
open_tilt_service: cover.open_cover_tilt     # optional override
close_tilt_service: cover.close_cover_tilt   # optional override
```

| Option | Default | Description |
|--------|---------|-------------|
| `tilt_buttons` | `top` | Position of the tilt button pair — `top` / `bottom` / `left` / `right` / `hidden` |
| `open_tilt_service` | `cover.open_cover_tilt` | Service called by the open-tilt button |
| `close_tilt_service` | `cover.close_cover_tilt` | Service called by the close-tilt button |

Only emit tilt options when the cover actually supports tilt — the editor
hides the whole panel otherwise, and on a non-tilt cover the buttons do
nothing. To drive tilt from a slider instead of buttons, set
`cover_slider_type: tilt_position` (works on the card slider and inside a
slider sub-button); combine with `tilt_buttons: hidden` for a slider-only
tilt control.

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
    color: accent          # colour NAME → var(--accent-color), not a hex
days: 7
limit: 5
show_end: true
show_progress: true
show_place: true
show_started_events: true
```

**Iron Law on calendar colours.** The `color:` key accepts either a hex
string or a **colour name**. A name is resolved to `var(--<name>-color)`,
so `color: accent` → `var(--accent-color)` and `color: red` →
`var(--red-color)`. Always use the name form — it is the only way to keep
calendar entity colours inside the theme. A raw hex here is a genuine
Iron Law violation, not an exception. (`color: transparent` is a special
case and hides the colour bar entirely.)

| Option | Default | Description |
|--------|---------|-------------|
| `days` | — | Number of days to look ahead. **v3.4.2+: this also sets the live-subscription window** — see the note below. |
| `limit` | — | Maximum number of events shown |
| `show_end` | false | Show event end time |
| `show_progress` | false | Progress bar on events currently running |
| `show_place` | false | Show the event location |
| `show_started_events` | false | Keep events that have already started in the list |
| `scrolling_effect` | true | Scroll long event titles |
| `event_action` | — | `tap_action` / `double_tap_action` / `hold_action` applied to individual events. **Default changed in v3.4.2: `tap_action` is now `more-info`** (it was `none`), and that `more-info` opens **HA's event dialog** with the event's description and location — not the calendar entity's more-info, which only knows the next event. Leave it unset for v3.4.2+. To keep events inert, set `tap_action: {action: none}` explicitly. |

> **The calendar card updates live from v3.4.2.** It now subscribes to the
> event list over the WebSocket, not just to the entity's state. Before that,
> only a change to the *next* event refreshed the card, so an event edited or
> deleted further out stayed wrong until a reload — the usual complaint being a
> wall panel showing a cancelled appointment all day. The subscription window
> runs from local midnight across `days`, which is the same window HA's own
> calendar card uses, so several cards asking for the same range share one
> server fetch. Keep `days` as small as the view needs: a 30-day card is a
> 30-day subscription.

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
footer_full_width: true      # or set footer_width instead
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

**Per-sub-button options beyond the common set:**

| Option | Default | Description |
|--------|---------|-------------|
| `sub_button_type` | `default` | `default` / `slider` / `dropdown` |
| `content_layout` | `icon-left` | Icon/label arrangement inside the button |
| `always_visible` | false | Keep a slider sub-button expanded rather than tap-to-open |
| `show_button_info` | false | Show the value alongside a slider. Forces `slider_value_position: right` — but only when combined with `always_visible: true`; on a tap-to-open slider the configured position still applies. |
| `hide_when_parent_unavailable` | false | Hide this sub-button when the card's main entity is unavailable |
| `light_background` | true | Tint the background from the light's colour |
| `css_class` | — | Adds a custom class to the element, for targeting from `styles:` or a module. Prefer this over brittle `nth-child` selectors. |
| `scrolling_effect` | card's, else `true` | Per-sub-button override. Unset, it inherits the card's `scrolling_effect`; unset there too, scrolling is on. |

> **Slider sub-buttons do not inherit the card's slider settings.** Every
> slider option — `tap_to_slide`, `relative_slide`, `read_only_slider`,
> `slider_live_update`, `invert_slider_value`, `slider_fill_orientation`,
> `slider_value_position`, `use_accent_color`, `min_value` / `max_value` /
> `step`, the light and cover options — is read from the **sub-button** only.
> Setting them on the card has no effect on a `sub_button_type: slider`.
>
> This is not the same rule as `scrolling_effect`, which *does* fall back to
> the card. The cascade is per-option, so don't assume either direction: set
> slider options on each slider sub-button that needs them.
>
> An unset option is genuinely absent rather than defaulted, which is what lets
> direction-aware defaults apply — `slider_value_position` follows the
> document's reading direction in RTL languages when left unset, and pinning it
> to `right` breaks that.

**Entity pictures on sub-buttons.** A sub-button pointing at an entity with an
`entity_picture` (a `person`, a media player with artwork) shows that picture
instead of an icon. Two things suppress it: `force_icon: true`, or setting the
sub-button's own `icon`. The *card's* icon does not — only the sub-button's.
So a person sub-button that should show a face needs no `icon:` at all, and
one that should show an icon needs its own `icon:` rather than `force_icon` on
the card.

**Timer entities tick live.** A sub-button on a `timer` whose state line
includes `state` or `remaining_time` counts down on its own beat while the
timer is `active` — the entity itself does not update every second. Nothing to
configure; it follows from the state line.

**Layout options for the sub-buttons card:**

| Option | Default | Description |
|--------|---------|-------------|
| `hide_main_background` | false | Transparent card — the chip-bar look |
| `footer_mode` | false | Pin the card to the bottom of the viewport |
| `footer_full_width` | false | Footer spans the full width |
| `footer_width` | — | Fixed footer width in px. Ignored when `footer_full_width: true`. **Changed in v3.4.2:** below 600 px viewport width the footer used to be forced to full width, throwing a configured width away — so the same 300 px footer obeyed the setting in landscape and ignored it in portrait (#2620). It is now clamped instead, to `min(footer_width, content width − 16px)`, so a width that fits is honoured at every viewport. A footer with **no** `footer_width` still fills a narrow screen, as before. If a dashboard carried a `styles:` or theme workaround to keep a narrow footer narrow on phones, remove it on v3.4.2+. |
| `footer_bottom_offset` | `16` | Distance from the bottom edge in px |
| `menu_style` | false | Menu-style rendering of the button row |
| `labels_below` | false | Labels under the icons — only effective with `menu_style: true` |
| `hide_button_labels` | false | Icons only, no labels |
| `compact_mode` | false | Tighter button spacing and smaller footprint |
| `space_between_buttons` | false | Distribute buttons with space between them |

`labels_below` silently does nothing without `menu_style: true` — if a user
reports labels not moving, check that pairing first.

---

## #state-content

### `state_content` — what the state line shows (v3.4.0+)

Since v3.4.0 the state line of a card or sub-button is described by a single
ordered list, written the way Home Assistant writes it on its tile card and
badges. It replaces five separate options.

```yaml
type: custom:bubble-card
card_type: button
entity: climate.living_room
state_content:
  - state
  - current_temperature
```

A single value may be given as a string (`state_content: state`). Items are
`state`, an attribute name, `last_changed`, `last_updated`, `last_triggered`,
or a Home Assistant template. `last-changed` and `last-updated` are accepted
as aliases.

**Replaces:**

| Legacy key | `state_content` equivalent |
|---|---|
| `show_state: true` | `- state` |
| `show_attribute: true` + `attribute: brightness` | `- brightness` |
| `show_last_changed: true` | `- last_changed` |
| `show_last_updated: true` | `- last_updated` |
| all off | `state_content: []` |

**Domain defaults when nothing is asked for** (same table as the HA frontend):

```
climate    → state, current_temperature      light  → brightness
cover      → state, current_position         timer  → remaining_time
fan        → percentage                      update → install_status
humidifier → state, current_humidity         valve  → state, current_position
```

Attributes that read zero are left out for `light`, `fan`, `cover` and
`valve`, so an off light shows *Off* rather than *0 %*.

**Version handling.** The five legacy keys still work — they are read into the
same list. But the moment a user opens that card in the visual editor, Bubble
Card migrates them to `state_content` on save. So:

- Target v3.4.0+ → generate `state_content`.
- Target an unknown or older version → generate the legacy keys and say that
  v3.4.0 will rewrite them the first time the card is edited in the UI. That
  rewrite is lossless, not something to warn against.
- Never generate both for the same card: `state_content` wins outright, and
  the legacy keys are then dead config that misleads the next reader.

---

### Render performance in v3.4.0

Home Assistant replaces the whole `hass` object whenever any entity changes,
so every card is asked to render on every state change anywhere in the
installation. Bubble Card v3.4.0 measured 43 renders per second at rest on an
A10 iPad, 78% of them with nothing the card depends on having moved, and added
a render gate that observes each card's actual dependency set to skip those.
Deferred card updates and lazy editor previews were added alongside.

**What this means for generation:** nothing to set — it is automatic. But it
does change the advice around `performance_mode` on pop-ups: that option
remains available for very heavy pop-ups, and is now less often the thing that
was actually needed. On v3.4.0+, update first and measure before reaching for
it.

**v3.4.2 rebuilt the gate's comparison, and that matters for one symptom.**
v3.4.0 compared a fixed list of `hass` keys (`themes`, `locale`, `config`,
`user`, `language`, `entities`, `devices`, `areas`). A list has to be kept
complete, and it was not: HA replaces its *formatters* once translations and
registries have loaded, and those were not on the list, so a card could render
its state line before the formatters arrived and show a **raw state** —
`heat_cool` instead of "Heat/Cool", a number without its unit — until
something else made it render again. v3.4.2 compares identity across
everything outside `states` instead of listing it, and adds a **10-second
settle window** after HA connects or reconnects in which no render is skipped
at all. Upstream measured the cost of that window at 50–70 ms of extra
rendering on a 31-card dashboard under a 4× CPU throttle.

So: a card showing an unformatted state for a moment on load, or a wall panel
showing one after reconnecting, is a known v3.4.0/3.4.1 defect — the fix is to
update, not to add a template.

---

## #ha-templates

### Home Assistant templates in card config (v3.4.0+)

Bubble Card has always supported JavaScript `${ }` templates inside `styles:`.
Since v3.4.0 it also evaluates **Home Assistant (Jinja2) templates** — the
`{{ }}` and `{% %}` syntax from Developer Tools → Template — in a set of
text fields:

- card `name` and `icon`
- sub-button `name`
- items inside `state_content`
- `styles:`, where a block may mix Jinja and `${ }` templates

```yaml
type: custom:bubble-card
card_type: button
entity: light.kitchen
name: "{{ state_attr('light.kitchen','friendly_name') }}"
icon: "{{ 'mdi:lightbulb' if is_state('light.kitchen','on') else 'mdi:lightbulb-outline' }}"
```

**When to reach for this, and when not to.** A Jinja template in `name:` is
evaluated by Home Assistant on every relevant state change. That is cheap for
one card and not cheap for forty. Prefer it where the value genuinely varies;
for a static label, write the label.

**It does not change this skill's scope rule.** Template *sensors* remain an
`ha-yaml` handoff. This is presentation-layer templating on a value the
dashboard already has, not a new entity.

**The Iron Law still applies.** A template that returns a colour must return a
theme variable, not a hex literal.

**A templated `name:` has no fallback.** Where a plain `name:` falls back to
the entity's friendly name when absent, a template shows exactly what it
returns — the empty string included. A template that can evaluate to nothing
(an attribute that is missing while the entity is `unavailable`, say) leaves
the card blank rather than showing the friendly name. Give it a default:

```yaml
name: "{{ state_attr('sensor.x','label') or 'Sensor' }}"
```

Rendered template output is HTML-escaped where the name is written as markup,
so it is treated as entity data rather than author-supplied markup.

**`icon:` behaves the opposite way.** A template that renders nothing — or has
not rendered yet — falls through to the entity's own icon, exactly as an absent
`icon:` would. So a conditional icon template is safe without a default, while
a conditional name template is not.

**Usually don't set `icon:` at all.** Bubble Card follows Home Assistant's own
resolution chain: a configured icon first, then the icon set on the entity in
the HA UI, then platform icons, domain state icons (so a lock shows open or
closed), `device_class` icons, and finally the domain fallback. Setting
`icon:` overrides all of that — including the state-dependent icons a user
would expect. Set it only where the entity genuinely has no sensible icon, or
where the card must differ from the entity on purpose.

A templated `name:` or `icon:` is also resolved for Home Assistant's own
navigation picker, so a pop-up shows up there with what it displays rather
than with the raw template text.

**Version-gate it.** On Bubble Card < 3.4.0 a Jinja template in `name:` is not
evaluated — the user sees the raw `{{ … }}` text on the card. Only generate
these when the user is on v3.4.0+.

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

> **Performance context (HA 2026.8+).** HA's own Jinja2 templates got up to
> 40% faster for numeric results, and templates used on dashboards are now
> cached. That narrows the historic gap between a template sensor and a
> dashboard-side template. It does not change this skill's scope rule —
> template *sensors* are still an ha-yaml handoff — but it does mean a
> template sensor is no longer automatically the faster choice, so don't
> justify one on performance grounds alone.

**Names in scope inside a `styles:` template** (verified against the v3.4.0
compiler):

| Name | What it is |
|------|-----------|
| `hass` | The HA object. Reading an entity through it registers the card's dependency with the render gate (v3.4.0). |
| `entity` | The card's `entity` id |
| `state` | That entity's state |
| `icon` | The card's icon element |
| `subButtonState` | Array of sub-button states |
| `subButtonIcon` | Array of sub-button icon elements |
| `card` | The card element |
| `name` | The card's name |
| `getWeatherIcon` | Weather-icon helper |
| `checkConditionsMet` | Evaluates a condition list |
| `onTeardown` / `hasChanged` | Module helpers, v3.3.0+ |
| `renderTemplate(template, entity?)` | **v3.4.0+** — renders a Home Assistant (Jinja2) template from inside a JS template and returns its text. `entity` defaults to the card's entity. |

`renderTemplate` is what lets one `styles:` block mix both template systems:

```yaml
styles: |
  .bubble-name { content: "${renderTemplate('{{ states("sensor.outside") }}')}"; }
```

Reaching for it is rarely necessary — since v3.4.0 a Jinja template can go
directly in `name:`, `icon:` or `state_content` (`#ha-templates`). Use
`renderTemplate` only when the value must feed a CSS declaration.

Referencing a name the installed version does not provide throws, and Bubble
Card then skips the **whole** template — guard `renderTemplate` with `typeof`
in anything shared.

JS templates go in the `styles:` key. CSS property assignments run first;
DOM-modifying statements must come last.

**Available variables:**

| Variable | Type | Description |
|----------|------|-------------|
| `state` | string | State of the card's `entity` |
| `entity` | string | Entity ID string (e.g. `light.kitchen`) |
| `icon` | element | The main icon element — use `icon.setAttribute("icon", "mdi:...")` |
| `subButtonIcon[N]` | element | Sub-button icon — N starts at 0 for first bottom sub-button (v3.1+) |
| `subButtonState[N]` | string | State of the Nth sub-button's entity. **Reliable only from v3.4.2** — see below. |

> **`subButtonState[N]` was mis-indexed before v3.4.2.** The walk read the
> ungrouped `main` sub-buttons, then every group, and **never read the
> ungrouped `bottom` ones at all** (#2165). So on v3.1–v3.4.1, as soon as a
> card mixes groups with loose sub-buttons, `subButtonState[N]` points at a
> different button than `subButtonIcon[N]` does, and some buttons have no
> index. From v3.4.2 the walk goes section by section — `main`, then `bottom`
> — and in config order inside each, so the index matches what the card shows,
> which is what `subButtonIcon[]` always did.
>
> On a `card_type: sub-buttons` card only the `bottom` section counts: the
> editor refuses to write a `main` section there, so a leftover one in
> hand-written YAML is not on screen and has no index.
>
> **When generating for < 3.4.2, don't index `subButtonState[]` on a card that
> mixes groups and loose sub-buttons.** Read the entity through `hass` instead
> — `hass.states['light.kitchen'].state` — which is unambiguous at every
> version and also registers the dependency with the render gate.
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

## #css-selectors

### Targeting elements from `styles:`

The skill's examples cover the dozen selectors that matter most. Bubble Card
renders around 110 card-facing `.bubble-*` classes in total; the useful ones,
grouped by where they appear:

**Every card**

```
.bubble-container            .bubble-content-container
.bubble-icon  .bubble-main-icon   .bubble-name  .bubble-name-container
.bubble-state  .bubble-background  .bubble-background-color
.bubble-button-card  .bubble-button-card-container  .bubble-button-container
.bubble-entity-picture  .bubble-badge
```

**Sub-buttons**

```
.bubble-sub-button  .bubble-sub-button-container  .bubble-sub-button-group
.bubble-sub-button-icon  .bubble-sub-button-name-container
.bubble-sub-button-image  .bubble-sub-button-info-wrapper
.bubble-sub-button-alignment-lane
```

**Sliders**

```
.bubble-range-slider  .bubble-range-fill  .bubble-range-value
.bubble-slider-dragging      (added while the user is dragging)
.bubble-sub-slider-wrapper   .bubble-sub-slider-close
.bubble-color-track  .bubble-color-cursor  .bubble-color-background
```

**Pop-up**

```
.bubble-pop-up-container  .bubble-header  .bubble-header-container
.bubble-header-actions  .bubble-header-action-button  .bubble-header-action-icon
.bubble-close-button  .bubble-previous-button  .bubble-title
.bubble-scroll-separator
```

**Climate** — `.bubble-climate-plus-button`, `.bubble-climate-minus-button`
(+ `-icon`), `.bubble-climate-temp-display`,
`.bubble-target-temperature-container`, `.bubble-temperature-container`,
`.bubble-high-temp-container`, `.bubble-low-temp-container`

**Cover** — `.bubble-cover-button` (+ `-icon`), `.bubble-cover-background`,
`.bubble-tilt-buttons-container`, and the crossfade layers
(`.bubble-cover-crossfade-layer`, `.bubble-cover-icon-crossfade`)

**Media player** — `.bubble-media-button` (+ `-icon`),
`.bubble-play-pause-button`, `.bubble-next-button`, `.bubble-previous-button`,
`.bubble-mute-button`, `.bubble-volume-button`, `.bubble-volume-slider`
(+ `-wrapper`, `-mute-button`, `-close-button`), `.bubble-artist`,
`.bubble-media-info-container`

**Calendar** — `.bubble-event` (+ `-name`, `-time`, `-place`, `-color`),
`.bubble-day-wrapper`, `.bubble-day-number`, `.bubble-day-month`,
`.bubble-day-chip`, `.bubble-day-events`

**Select / dropdown** — `.bubble-dropdown-container`,
`.bubble-dropdown-select`, `.bubble-dropdown-arrow`,
`.bubble-select-card-container`

**HBS** — `.bubble-buttons-container`, `.bubble-buttons-column-wrapper`,
`.bubble-horizontal-buttons-stack-card-container`

> **These are internal class names, not a stable API.** They change between
> versions without notice — the `bubble-cover-crossfade-*` set, for example,
> did not exist in earlier 3.x releases. Two consequences:
>
> 1. Prefer a **`--bubble-*` theme variable** where one exists
>    (`css-theme-ref.md#bubble-vars`) — that *is* the supported surface.
> 2. When you must target an element, use **`css_class`** on the sub-button
>    (v3.3.0+, `#sub-buttons`) to add your own class rather than depending on
>    Bubble Card's. `nth-child` selectors are worse still: they break when a
>    sub-button is added or hidden by a condition.

**Every sub-button carries three classes, and only one of them is stable:**

| Class | Stability |
|---|---|
| `.bubble-sub-button` | always present |
| `.bubble-sub-button-<index>` | the sub-button's key, with `_` rewritten to `-` (so `main_1` → `.bubble-sub-button-main-1`). Stable while the key is |
| a class from `name:` | derived from the name — lowercased, accents stripped, everything non-alphanumeric collapsed to hyphens, so `Küche Licht` → `.kuche-licht`. **Breaks on a rename, and on a translated name.** Not generated at all for a templated `name:`. |
| `.<css_class>` | normalised the same way, but set deliberately — survives renames, translations and templated names |

So: target `css_class` when you control the YAML, the index class when you do
not, and never the name-derived class in anything shared. A user who translates
their dashboard loses every style hung on a name.

---

## #modules

### Bubble Card module workflow

Modules are reusable CSS/JS templates applied across multiple cards.
Stored as YAML files in `/config/bubble_card/modules/` (requires Bubble Card Tools).
**To write a module, see `#module-authoring` below** (and `module-authoring-ref.md`
for the full `editor:` field catalog and sharing format) — this section covers
only applying an existing module to a card.

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

Bubble Card dispatches a `hass-action` event, so the action set is **Home
Assistant's own**, not a Bubble-specific list — anything HA's action handler
accepts works here.

```yaml
tap_action:
  action: toggle | more-info | navigate | perform-action | url | assist |
          fire-dom-event | none
  # call-service is the pre-2024.8 name for perform-action and still works

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

# Open the Assist dialog
tap_action:
  action: assist
  pipeline_id: last_used          # optional
  start_listening: true           # optional
```

**`perform-action` vs `call-service`.** HA renamed the action in 2024.8;
Bubble Card accepts both (`service:` and `perform_action:` are read as
equivalents). Generate `perform-action` for current setups — `call-service`
is legacy and will read as dated to anyone comparing against HA's own docs.

```yaml
tap_action:
  action: perform-action
  perform_action: light.turn_on
  target:
    entity_id: light.kitchen
  data:
    brightness_pct: 100
```

**Note:** When `double_tap_action` is set, `tap_action` has a 200 ms delay
(verified against the source). Set `double_tap_action: action: none` to disable
and restore instant tap response. A hold fires after **500 ms**.

**`tap_action: none` also removes the ripple.** Bubble Card attaches the
press feedback only when at least one of tap, double-tap or hold is something
other than `none`. A card with all three set to `none` gets no ripple and no
`bubble-action-enabled` class — so it *looks* non-interactive, not just
behaves that way. This is why the Overview view's state-only cards take
`tap_action: none` rather than being left at their default: it is the
difference between a card that ignores a tap and a card that never invited
one.

A tap is cancelled by movement, and a hold survives a little more of it than a
tap does — so a press that drifts during a scroll does not fire, and a hold
does not break on a small tremor. Nothing to configure; worth knowing when a
user reports that taps "sometimes don't register" on a scrolling dashboard.

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
| `fan` | `button` | `switch` for on/off. Speed: a **slider** sub-button for `percentage` (it is a number, not a list — `select_attribute: percentage` renders an empty dropdown), or `select_attribute: preset_modes` for named speeds. `select_attribute: direction` on a reversible fan needs v3.4.2+. |
| `vacuum` | `button` | `switch` for start/stop; add sub-button for `status` attribute display. Suction power: `select_attribute: fan_speed_list` (v3.4.2+). Battery: point at the device's battery **sensor** — HA 2026.8 removed the `battery_level` attribute. |
| `alarm_control_panel` | `button` | `state` display. v3.4.2+: `select_attribute: alarm_modes` on a dropdown sub-button arms and disarms in place, with a keypad when a code is needed — see `#select-attribute`. Below that, `tap_action: more-info` for the arming UI. |
| `lock` | `button` | `switch` (toggles lock/unlock); always add `hold_action: more-info` |
| `camera` | `button` | `state` with `camera_image` entity_picture; use pop-up with `centered` mode for full view. **Note: use `picture-entity` (native HA card) for live streams — Bubble Card does not support camera live video directly.** |
| `humidifier` | `button` | `switch` for on/off; add sub-button `select_attribute: available_modes` (**not** `mode` — that attribute holds the current value, not the list) |
| `remote` | `button` | `switch` for on/off; `select_attribute: activity_list` to pick an activity (v3.4.2+) |
| `number` | `button` | `slider` — leave `min_value` / `max_value` / `step` unset so the slider follows the entity's own `min` / `max` / `step` attributes |
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
| `siren` | `button` | `switch` — Bubble Card treats it as a toggle domain |
| `remote` | `button` | `switch` — toggle domain |
| `lawn_mower` | `button` | `switch` — a toggle domain in Bubble Card, with a built-in `mdi:robot-mower` icon. Add a sub-button on the `activity` attribute for status. |
| `valve` | native tile | **No Bubble Card support.** Not a recognised toggle or slider domain. Use the native HA tile card, or a `button` with an explicit `tap_action: call-service` on `valve.open_valve` / `valve.close_valve`. |
| `water_heater` | `button` (state) | **Partial support — corrected.** Not a toggle or slider domain, so `button_type: switch` will not switch it and there is no `card_type: climate` equivalent. But Bubble Card *does* understand its active state: a water heater has no `on`, its state is the operation it is running, so anything other than `off`/`unknown`/`unavailable` reads as active (same rule HA uses). A `button_type: state` card therefore shows and colours correctly. For setting a temperature, use the native tile card with its temperature feature, or `more-info`. |
| `todo` | native card | **No Bubble Card support.** Use the native todo-list card; a Bubble `button` can navigate to it. |
| `image` | native card | Use the native `picture-entity` / `image` card, same reasoning as `camera`. |

**Domain support is not open-ended.** Bubble Card recognises a fixed set of
toggle and slider domains internally (verified in v3.2.5 source): toggle =
`light`, `switch`, `fan`, `input_boolean`, `lock`, `siren`, `remote`,
`humidifier`, `vacuum`, `lawn_mower`, `script`, `scene`, `automation`,
`cover`, `climate`, `media_player`; slider = `light`, `media_player`,
`cover`, `input_number`, `number`, `climate`, `fan`. These lists govern *control*, not display: a domain outside them can still
render a correct `button_type: state` card, because active-state detection is
a separate and broader rule (numeric states, `open`, `playing`, `locked`,
`cleaning` and others all read as active, and `water_heater` has its own).
What a domain outside these lists cannot do is toggle or slide — `button_type:
switch` or `slider` will not behave as expected — fall back to an explicit `tap_action` or the native
tile, and say so rather than generating a control that silently does nothing.

### Sub-button patterns for complex domains

```yaml
# Fan — on/off switch + speed slider sub-button
# `percentage` is a number, so it belongs on a slider. A dropdown would need a
# list, and `select_attribute: percentage` opens empty (see #select-attribute).
type: custom:bubble-card
card_type: button
button_type: switch
entity: fan.living_room
name: Fan
card_layout: large
sub_button:
  main:
    - name: Speed
      sub_button_type: slider
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

### Writing Bubble Card modules — quick reference

Modules are reusable CSS/JS applied across cards. They live in
`/config/bubble_card/modules/` as `.yaml` files (requires Bubble Card Tools).
**For the full field-type catalog, the object selector (groups/conditionals/
variants), grid/expandable layout, and the module-sharing/export format, see
`module-authoring-ref.md`.**

**Complete module YAML structure:**

```yaml
# /config/bubble_card/modules/my-module.yaml
my_module_id:
  name: "Human-readable name"
  description: "What this module does"
  version: "1.0"
  creator: "YourName"
  link: ""            # optional — URL to a GitHub discussion or source
  supported:
    # List card types this module applies to. Omit entirely to apply
    # to ALL card types — there is no "all" literal value.
    # button | calendar | climate | cover | horizontal-buttons-stack |
    # media-player | pop-up | select | separator | sub-buttons
    - button
    - pop-up
  is_global: false    # true = auto-applies to ALL supported cards
                      # false = only applies when explicitly listed
  editor:              # optional — user-configurable fields (HA form-selector schema)
    - name: radius
      label: "Border radius"
      selector:
        number: { min: 0, max: 40, unit_of_measurement: "px" }
  code: |
    ha-card {
      --bubble-border-radius: ${this.config.my_module_id?.radius || 16}px;
      border: 1px solid var(--divider-color) !important;
    }
    .bubble-icon-container {
      background: var(--state-inactive-color) !important;
    }
```

**Config values are read in `code:` via `this.config.<module_id>?.<field_name>`** —
this is a JS template literal (same template API as a card's `styles:` key: `hass`,
`entity`, `state`, `icon`, `subButtonState`, `subButtonIcon`, `getWeatherIcon`, `card`,
`name`, `checkConditionsMet`). There is **no `variables:` key and no `{{mustache}}`
interpolation syntax** — that pattern does not exist in Bubble Card's module system.
Always use optional chaining (`?.`) since the module may not be configured yet, and
provide a fallback with `||` where sensible.

**Global module pattern — apply across all buttons:**
```yaml
ha_default_bridge:
  name: "HA Theme Bridge"
  description: "Ensures Bubble Card inherits HA theme colours"
  version: "1.0"
  # No 'supported:' key — omitting it applies the module to every card type.
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

**Applying the module to a card** uses the same `modules:` key covered in
`#modules` above — e.g. `modules: [light_card_style, '!ha_default_bridge']`.

**User-configurable module (`editor:` + `this.config`, not `variables:`/`{{}}`):**
```yaml
# In module definition
editor:
  - name: glow_color
    label: "Glow colour"
    selector:
      ui_color: {}
code: |
  ha-card {
    box-shadow: 0 0 12px ${this.config.my_module_id?.glow_color || 'var(--accent-color)'} !important;
  }
```
See `module-authoring-ref.md` for the full field-type catalog (text/number/
boolean/select/color/icon/entity/condition/object/etc.), the object selector's
groups/conditional-fields/variants, and grid/expandable layout.

**When to use modules vs styles::**

| Need | Use |
|------|-----|
| Same CSS on 5+ cards | Module (is_global: false) |
| Same CSS on ALL cards of a type | Module (is_global: true, omit `supported:`) |
| One-off override on a single card | `styles:` key in card YAML |
| Dynamic CSS based on entity state | `styles:` with JS template |
| Reusable AND configurable per card | Module with `editor:` |

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
