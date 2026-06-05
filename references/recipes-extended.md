# Extended Recipes Reference
# ha-bubble-dashboard skill
# Covers: security, energy, vacuum, presence/person panel,
#         bathroom, garage — complete copy-paste YAML.
# All recipes use var() chains — no hardcoded colours.

---

## #security-popup

### Security pop-up — camera + lock + alarm

```yaml
type: custom:bubble-card
card_type: pop-up
hash: '#security'
name: Security
icon: mdi:shield-home
width_desktop: "600px"
popup_mode: centered
with_bottom_offset: true
cards:

  # ── Alarm ───────────────────────────────────────────────
  - type: custom:bubble-card
    card_type: separator
    name: Alarm
    icon: mdi:alarm-light

  - type: custom:bubble-card
    card_type: button
    button_type: state
    entity: alarm_control_panel.home_alarm
    name: Alarm System
    icon: mdi:shield-home
    show_state: true
    card_layout: large
    button_action:
      tap_action:
        action: more-info

  # ── Locks ───────────────────────────────────────────────
  - type: custom:bubble-card
    card_type: separator
    name: Locks
    icon: mdi:door-closed-lock

  - type: custom:bubble-card
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

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: lock.back_door
    name: Back Door
    icon: mdi:door-closed-lock
    card_layout: large
    button_action:
      tap_action:
        action: toggle
      hold_action:
        action: more-info

  # ── Cameras ─────────────────────────────────────────────
  - type: custom:bubble-card
    card_type: separator
    name: Cameras
    icon: mdi:cctv

  - type: picture-entity
    entity: camera.front_door
    show_name: true
    show_state: false
    camera_view: live

  - type: picture-entity
    entity: camera.garden
    show_name: true
    show_state: false
    camera_view: auto

  # ── Doors & Windows ─────────────────────────────────────
  - type: custom:bubble-card
    card_type: separator
    name: Sensors
    icon: mdi:door-open

  - type: custom:bubble-card
    card_type: button
    button_type: state
    entity: binary_sensor.front_door_contact
    name: Front Door
    show_state: true
    card_layout: large

  - type: custom:bubble-card
    card_type: button
    button_type: state
    entity: binary_sensor.back_door_contact
    name: Back Door
    show_state: true
    card_layout: large
```

---

## #energy-view

### Energy overview section — power sensors + grid + solar

```yaml
# Section inside a view — use column_span: 3 for full width
- type: custom:bubble-card
  card_type: separator
  name: Energy
  icon: mdi:lightning-bolt

# Grid power (import/export)
- type: custom:bubble-card
  card_type: button
  button_type: state
  entity: sensor.grid_power
  name: Grid
  icon: mdi:transmission-tower
  show_state: true
  card_layout: large
  sub_button:
    main:
      - entity: sensor.grid_imported_today
        show_state: true
        show_icon: true
        icon: mdi:arrow-down
        show_name: false
        show_background: false
      - entity: sensor.grid_exported_today
        show_state: true
        show_icon: true
        icon: mdi:arrow-up
        show_name: false
        show_background: false

# Solar production
- type: custom:bubble-card
  card_type: button
  button_type: state
  entity: sensor.solar_power
  name: Solar
  icon: mdi:solar-power
  show_state: true
  card_layout: large
  sub_button:
    main:
      - entity: sensor.solar_produced_today
        show_state: true
        show_icon: true
        icon: mdi:sun-wireless
        show_name: false
        show_background: false

# Home consumption
- type: custom:bubble-card
  card_type: button
  button_type: state
  entity: sensor.home_power
  name: Home
  icon: mdi:home-lightning-bolt
  show_state: true
  card_layout: large
  sub_button:
    main:
      - entity: sensor.home_energy_today
        show_state: true
        show_icon: true
        icon: mdi:counter
        show_name: false
        show_background: false

# Battery storage (if present)
- type: custom:bubble-card
  card_type: button
  button_type: state
  entity: sensor.battery_state_of_charge
  name: Battery
  icon: mdi:battery-charging
  show_state: true
  card_layout: large
  sub_button:
    main:
      - entity: sensor.battery_power
        show_state: true
        show_icon: false
        show_name: false
        show_background: false
```

---

## #vacuum-popup

### Vacuum control pop-up

```yaml
type: custom:bubble-card
card_type: pop-up
hash: '#vacuum'
name: Robot Vacuum
icon: mdi:robot-vacuum
width_desktop: "480px"
popup_mode: fit-content
with_bottom_offset: true
cards:

  - type: custom:bubble-card
    card_type: separator
    name: Control
    icon: mdi:robot-vacuum

  # Status and dock/undock
  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: vacuum.robot
    name: Robot
    icon: mdi:robot-vacuum
    show_state: true
    card_layout: large
    button_action:
      tap_action:
        action: toggle            # starts cleaning / pauses
      hold_action:
        action: call-service
        service: vacuum.return_to_base
        target:
          entity_id: vacuum.robot

  - type: custom:bubble-card
    card_type: separator
    name: Zones
    icon: mdi:map-marker-radius

  # Zone buttons — adjust service calls to your vacuum integration
  - type: custom:bubble-card
    card_type: button
    button_type: name
    name: Kitchen
    icon: mdi:chef-hat
    button_action:
      tap_action:
        action: call-service
        service: vacuum.send_command
        target:
          entity_id: vacuum.robot
        data:
          command: app_zoned_clean
          params: [[26234, 26042, 27284, 27642, 1]]  # adjust coordinates

  - type: custom:bubble-card
    card_type: button
    button_type: name
    name: Living Room
    icon: mdi:sofa
    button_action:
      tap_action:
        action: call-service
        service: vacuum.send_command
        target:
          entity_id: vacuum.robot
        data:
          command: app_zoned_clean
          params: [[24732, 28236, 26982, 29486, 1]]  # adjust coordinates

  - type: custom:bubble-card
    card_type: separator
    name: Status
    icon: mdi:information

  - type: custom:bubble-card
    card_type: button
    button_type: state
    entity: sensor.robot_battery_level
    name: Battery
    icon: mdi:battery
    show_state: true

  - type: custom:bubble-card
    card_type: button
    button_type: state
    entity: sensor.robot_last_clean_area
    name: Last Area
    show_state: true
```

---

## #presence-panel

### Person / presence panel pop-up

```yaml
type: custom:bubble-card
card_type: pop-up
hash: '#presence'
name: People
icon: mdi:account-group
width_desktop: "480px"
popup_mode: fit-content
with_bottom_offset: true
cards:

  - type: custom:bubble-card
    card_type: separator
    name: At Home
    icon: mdi:home-account

  # One card per person — repeat as needed
  - type: custom:bubble-card
    card_type: button
    button_type: state
    entity: person.alice
    name: Alice
    show_state: true
    card_layout: large
    button_action:
      tap_action:
        action: more-info
    sub_button:
      main:
        - entity: device_tracker.alice_phone
          show_state: false
          show_icon: true
          icon: mdi:cellphone
          show_background: false
          show_name: false

  - type: custom:bubble-card
    card_type: button
    button_type: state
    entity: person.bob
    name: Bob
    show_state: true
    card_layout: large
    button_action:
      tap_action:
        action: more-info

  - type: custom:bubble-card
    card_type: separator
    name: Guest Mode
    icon: mdi:account-key

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: input_boolean.guest_mode
    name: Guest Mode
    icon: mdi:account-key
    card_layout: large
```

---

## #bathroom-popup

### Bathroom pop-up — light + humidity + heated towel rail

```yaml
type: custom:bubble-card
card_type: pop-up
hash: '#bathroom'
name: Bathroom
icon: mdi:shower
width_desktop: "480px"
popup_mode: fit-content
with_bottom_offset: true
cards:

  - type: custom:bubble-card
    card_type: separator
    name: Lighting
    icon: mdi:lightbulb

  - type: custom:bubble-card
    card_type: button
    button_type: slider
    entity: light.bathroom
    name: Bathroom Light
    icon: mdi:ceiling-light
    card_layout: large
    light_slider_type: brightness

  # Night light if separate circuit
  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: switch.bathroom_night_light
    name: Night Light
    icon: mdi:lightbulb-night
    card_layout: large

  - type: custom:bubble-card
    card_type: separator
    name: Climate
    icon: mdi:thermometer-water

  # Heated towel rail
  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: switch.heated_towel_rail
    name: Towel Rail
    icon: mdi:radiator
    card_layout: large
    show_state: true

  - type: custom:bubble-card
    card_type: separator
    name: Sensors
    icon: mdi:water-percent

  # Humidity + temperature chip bar
  - type: custom:bubble-card
    card_type: sub-buttons
    hide_main_background: true
    sub_button:
      bottom:
        - name: Sensors
          buttons_layout: inline
          justify_content: flex-start
          group:
            - entity: sensor.bathroom_temperature
              show_state: true
              show_icon: true
              icon: mdi:thermometer
              fill_width: false
              show_background: true
              show_name: false
            - entity: sensor.bathroom_humidity
              show_state: true
              show_icon: true
              icon: mdi:water-percent
              fill_width: false
              show_background: true
              show_name: false

  # Ventilation fan — auto-triggers on humidity, manual override here
  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: switch.bathroom_fan
    name: Fan
    icon: mdi:fan
    show_state: true
    card_layout: large
```

---

## #garage-popup

### Garage pop-up — cover + camera + car presence + EV charger

```yaml
type: custom:bubble-card
card_type: pop-up
hash: '#garage'
name: Garage
icon: mdi:garage
width_desktop: "600px"
popup_mode: centered
with_bottom_offset: true
cards:

  - type: custom:bubble-card
    card_type: separator
    name: Door
    icon: mdi:garage-open

  - type: custom:bubble-card
    card_type: cover
    entity: cover.garage_door
    name: Garage Door
    card_layout: large

  # Status chip bar
  - type: custom:bubble-card
    card_type: sub-buttons
    hide_main_background: true
    sub_button:
      bottom:
        - name: Status
          buttons_layout: inline
          justify_content: flex-start
          group:
            - entity: binary_sensor.garage_door_contact
              show_name: true
              name: Door
              show_state: false
              show_icon: true
              fill_width: false
              show_background: true
              state_background: true
            - entity: binary_sensor.car_present
              show_name: true
              name: Car
              show_state: false
              show_icon: true
              icon: mdi:car
              fill_width: false
              show_background: true
              state_background: true

  - type: custom:bubble-card
    card_type: separator
    name: Camera
    icon: mdi:cctv

  - type: picture-entity
    entity: camera.garage
    show_name: false
    show_state: false
    camera_view: live

  - type: custom:bubble-card
    card_type: separator
    name: EV Charger
    icon: mdi:ev-station

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: switch.ev_charger
    name: EV Charger
    icon: mdi:ev-station
    show_state: true
    card_layout: large
    sub_button:
      main:
        - entity: sensor.ev_charger_power
          show_state: true
          show_icon: true
          icon: mdi:lightning-bolt
          show_name: false
          show_background: false

  - type: custom:bubble-card
    card_type: separator
    name: Lighting
    icon: mdi:lightbulb

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: light.garage
    name: Garage Light
    icon: mdi:ceiling-light
    card_layout: large
```

---

## #office-popup

### Home office pop-up — computer, light, monitor, desk accessories

```yaml
type: custom:bubble-card
card_type: pop-up
hash: '#office'
name: Office
icon: mdi:desk-lamp
width_desktop: "480px"
popup_mode: fit-content
with_bottom_offset: true
cards:

  - type: custom:bubble-card
    card_type: separator
    name: Lighting
    icon: mdi:lightbulb

  - type: custom:bubble-card
    card_type: button
    button_type: slider
    entity: light.office_desk_lamp
    name: Desk Lamp
    icon: mdi:desk-lamp
    card_layout: large
    light_slider_type: brightness

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: light.office_overhead
    name: Overhead
    icon: mdi:ceiling-light
    card_layout: large

  - type: custom:bubble-card
    card_type: separator
    name: Devices
    icon: mdi:desktop-tower-monitor

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: switch.office_computer
    name: Computer
    icon: mdi:desktop-tower
    show_state: true
    card_layout: large

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: switch.office_monitor
    name: Monitor
    icon: mdi:monitor
    card_layout: large

  - type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: switch.office_desk_power
    name: Desk Power
    icon: mdi:power-socket
    card_layout: large

  - type: custom:bubble-card
    card_type: separator
    name: Climate
    icon: mdi:thermometer

  - type: custom:bubble-card
    card_type: sub-buttons
    hide_main_background: true
    sub_button:
      bottom:
        - name: Sensors
          buttons_layout: inline
          justify_content: flex-start
          group:
            - entity: sensor.office_temperature
              show_state: true
              show_icon: true
              icon: mdi:thermometer
              fill_width: false
              show_background: true
              show_name: false
            - entity: sensor.office_co2
              show_state: true
              show_icon: true
              icon: mdi:molecule-co2
              fill_width: false
              show_background: true
              show_name: false
```

---

## #streamline-templates-extended

### Streamline templates for repeated room types

Use these when you have 3 or more rooms of the same type (3 bathrooms,
2 garages, multiple offices). Add to `streamline_templates.yaml`.

**Block 1 — Add to `streamline_templates.yaml`:**

```yaml
# ── Bathroom template ─────────────────────────────────────
bathroom_popup_button:
  default:
    - light_icon: mdi:ceiling-light
    - fan_entity: ""
    - towel_entity: ""
  card:
    type: custom:bubble-card
    card_type: button
    button_type: name
    entity: '[[light_entity]]'
    name: '[[name]]'
    icon: mdi:shower
    card_layout: large
    button_action:
      tap_action:
        action: navigate
        navigation_path: '[[hash]]'

# ── Garage template ───────────────────────────────────────
garage_cover_button:
  default:
    - icon: mdi:garage
  card:
    type: custom:bubble-card
    card_type: cover
    entity: '[[entity]]'
    name: '[[name]]'
    icon_open: mdi:garage-open
    icon_close: mdi:garage
    card_layout: large

# ── Office device template ────────────────────────────────
office_device_button:
  default:
    - button_type: switch
    - card_layout: large
  card:
    type: custom:bubble-card
    card_type: button
    button_type: '[[button_type]]'
    entity: '[[entity]]'
    name: '[[name]]'
    icon: '[[icon]]'
    card_layout: '[[card_layout]]'
    show_state: true

# ── Security lock template ────────────────────────────────
security_lock_button:
  card:
    type: custom:bubble-card
    card_type: button
    button_type: switch
    entity: '[[entity]]'
    name: '[[name]]'
    icon: mdi:door-closed-lock
    card_layout: large
    button_action:
      tap_action:
        action: toggle
      hold_action:
        action: more-info
```

**Block 2 — Card usage examples:**

```yaml
# Three bathrooms using the same template
- type: custom:streamline-card
  template: bathroom_popup_button
  variables:
    - light_entity: light.bathroom_main
    - name: Main Bathroom
    - hash: '#bathroom-main'

- type: custom:streamline-card
  template: bathroom_popup_button
  variables:
    - light_entity: light.bathroom_ensuite
    - name: En-suite
    - hash: '#bathroom-ensuite'

- type: custom:streamline-card
  template: bathroom_popup_button
  variables:
    - light_entity: light.bathroom_guest
    - name: Guest Bathroom
    - hash: '#bathroom-guest'

# Two garages
- type: custom:streamline-card
  template: garage_cover_button
  variables:
    - entity: cover.garage_main
    - name: Main Garage

- type: custom:streamline-card
  template: garage_cover_button
  variables:
    - entity: cover.garage_workshop
    - name: Workshop

# Office devices
- type: custom:streamline-card
  template: office_device_button
  variables:
    - entity: switch.office_computer
    - name: Computer
    - icon: mdi:desktop-tower

- type: custom:streamline-card
  template: office_device_button
  variables:
    - entity: switch.office_monitor
    - name: Monitor
    - icon: mdi:monitor

# Security locks
- type: custom:streamline-card
  template: security_lock_button
  variables:
    - entity: lock.front_door
    - name: Front Door

- type: custom:streamline-card
  template: security_lock_button
  variables:
    - entity: lock.back_door
    - name: Back Door
```

---

## #recipe-7-5view-scaffold

### Recipe 7 — 5-view dashboard outer scaffold

The top-level view and path definitions for the complete 5-view system.
Paste this as the root structure, then fill each view with its content
from Recipes 8–12 and `dashboard-system.md`.

```yaml
# ── Root dashboard configuration ────────────────────────────────────────────
# Copy this as your dashboard YAML root.
# Replace all REPLACE markers before delivering.
# Theme must be set to Casa5HeyneV2 (or your generated palette variant).

title: Home
views:

  # View 1 — Overview (see Recipe 8)
  - title: Overview
    path: overview
    type: sections
    max_columns: 3
    icon: mdi:home-variant
    theme: Casa5HeyneV2              # REPLACE with your palette variant name
    cards: []                        # Replaced by Recipe 8 content

  # View 2 — Rooms (see Recipe 9)
  - title: Rooms
    path: rooms
    type: sections
    max_columns: 3
    icon: mdi:floor-plan
    theme: Casa5HeyneV2
    cards: []                        # Replaced by Recipe 9 content

  # View 3 — Scenes (see Recipe 10)
  - title: Scenes
    path: scenes
    type: sections
    max_columns: 3
    icon: mdi:palette
    theme: Casa5HeyneV2
    cards: []                        # Replaced by Recipe 10 content

  # View 4 — Activity (see Recipe 11)
  - title: Activity
    path: activity
    type: sections
    max_columns: 2
    icon: mdi:history
    theme: Casa5HeyneV2
    cards: []                        # Replaced by Recipe 11 content

  # View 5 — Settings (see Recipe 12)
  - title: Settings
    path: settings
    type: sections
    max_columns: 3
    icon: mdi:cog
    theme: Casa5HeyneV2
    cards: []                        # Replaced by Recipe 12 content

  # Extension: Energy — add when relevant (see Recipe 13)
  # - title: Energy
  #   path: energy
  #   type: sections
  #   max_columns: 2
  #   icon: mdi:lightning-bolt
  #   theme: Casa5HeyneV2
  #   cards: []

  # Extension: Music — add when relevant (see Recipe 14)
  # - title: Music
  #   path: music
  #   type: sections
  #   max_columns: 2
  #   icon: mdi:music
  #   theme: Casa5HeyneV2
  #   cards: []
```

**Iron Law reminder:** theme is set at view level, not card level.
Never set `theme:` on individual cards. All colour flows from the view
theme through `var()` chains — zero hardcoded hex in any card YAML.

---

## #recipe-8-overview

### Recipe 8 — Overview view cards

Replace the `cards: []` in the Overview view from Recipe 7 with this content.
Full detail with design rationale in `dashboard-system.md#view-overview`.

```yaml
cards:

  # ── Chip bar — always visible ────────────────────────────────────────────
  - type: grid
    column_span: 3
    cards:
      - type: custom:mushroom-chips-card
        chips:
          - type: weather
            entity: weather.home                # REPLACE
            show_conditions: true
            show_temperature: true
            tap_action:
              action: more-info

          - type: entity
            entity: sensor.outdoor_temperature  # REPLACE
            content_info: state
            icon: mdi:thermometer
            tap_action:
              action: none

          - type: entity
            entity: person.alice                # REPLACE — repeat per person
            content_info: name
            tap_action:
              action: more-info

          - type: entity
            entity: alarm_control_panel.home    # REPLACE
            content_info: state
            icon: mdi:shield-home
            tap_action:
              action: more-info

          - type: template
            icon: mdi:lightbulb
            content: >
              {% set n = states.light
                 | selectattr('state','eq','on') | list | count %}
              {{ n }} light{{ 's' if n != 1 }}
            icon_color: >
              {% set n = states.light
                 | selectattr('state','eq','on') | list | count %}
              {{ 'amber' if n > 0 else 'grey' }}
            tap_action:
              action: none

          - type: entity
            entity: sensor.current_power        # REPLACE — remove if not available
            content_info: state
            icon: mdi:flash
            tap_action:
              action: none

  # ── Alert strip — conditionally visible ─────────────────────────────────
  # Requires input_boolean.home_alerts_active — hand off to ha-yaml.
  # The automation sets this to on when any alert condition is true.
  - type: conditional
    conditions:
      - condition: state
        entity: input_boolean.home_alerts_active  # REPLACE — create via ha-yaml
        state: "on"
    card:
      type: grid
      column_span: 3
      cards:
        - type: custom:bubble-card
          card_type: separator
          name: Alerts
          icon: mdi:alert-circle
          styles: |
            .bubble-separator {
              background: rgba(var(--rgb-warning-color), 0.15);
              border-left: 3px solid var(--warning-color);
            }

        - type: custom:bubble-card
          card_type: button
          button_type: state
          entity: binary_sensor.front_door      # REPLACE — repeat per alert entity
          name: Front Door
          icon: mdi:door-open
          show_state: true
          card_layout: normal
          button_action:
            tap_action:
              action: none

  # ── Per-room status grid — state only, no controls ───────────────────────
  - type: grid
    column_span: 3
    cards:
      - type: custom:bubble-card
        card_type: separator
        name: Home Status
        icon: mdi:home-analytics

      - type: custom:bubble-card
        card_type: button
        button_type: state
        name: Living Room
        icon: mdi:sofa
        entity: light.living_room_group         # REPLACE
        show_state: false
        card_layout: normal
        button_action:
          tap_action:
            action: none                        # No controls on Overview
        sub_button:
          main:
            - entity: sensor.living_room_temperature  # REPLACE
              show_state: true
              show_icon: true
              icon: mdi:thermometer
              show_background: false
            - entity: binary_sensor.living_room_motion  # REPLACE
              show_state: false
              show_icon: true
              icon: mdi:motion-sensor
              show_background: true
              state_background: true

      # REPLACE: copy the above block for each room
      - type: custom:bubble-card
        card_type: button
        button_type: state
        name: Kitchen
        icon: mdi:chef-hat
        entity: light.kitchen_group             # REPLACE
        show_state: false
        card_layout: normal
        button_action:
          tap_action:
            action: none

      - type: custom:bubble-card
        card_type: button
        button_type: state
        name: Bedroom
        icon: mdi:bed
        entity: light.bedroom_group             # REPLACE
        show_state: false
        card_layout: normal
        button_action:
          tap_action:
            action: none

  # ── Away mode panel — visible when nobody home ───────────────────────────
  - type: conditional
    conditions:
      - condition: template
        value_template: >
          {{ states.person | selectattr('state','eq','home')
             | list | count == 0 }}
    card:
      type: grid
      column_span: 3
      cards:
        - type: custom:bubble-card
          card_type: separator
          name: Nobody Home
          icon: mdi:home-export-outline

        - type: custom:bubble-card
          card_type: button
          button_type: state
          entity: alarm_control_panel.home      # REPLACE
          name: Security
          show_state: true
          card_layout: normal
          button_action:
            tap_action:
              action: none

        - type: custom:bubble-card
          card_type: button
          button_type: state
          entity: binary_sensor.any_light_on    # REPLACE — template sensor
          name: Lights
          icon: mdi:lightbulb
          show_state: true
          card_layout: normal
          button_action:
            tap_action:
              action: none

  # ── HBS footer — always last ─────────────────────────────────────────────
  - type: custom:bubble-card
    card_type: horizontal-buttons-stack
    auto_order: false
    highlight_current_view: true
    is_sidebar_hidden: true
    rise_animation: false
    1_name: Overview
    1_icon: mdi:home-variant
    1_link: /lovelace/overview
    2_name: Rooms
    2_icon: mdi:floor-plan
    2_link: /lovelace/rooms
    3_name: Scenes
    3_icon: mdi:palette
    3_link: /lovelace/scenes
    4_name: Activity
    4_icon: mdi:history
    4_link: /lovelace/activity
    5_name: Settings
    5_icon: mdi:cog
    5_link: /lovelace/settings
```

---

## #recipe-9-rooms

### Recipe 9 — Rooms view cards

Replace the `cards: []` in the Rooms view from Recipe 7 with this content.
Add one pop-up and one room button per room.
Full detail in `dashboard-system.md#view-rooms`.

```yaml
cards:

  # ── Pop-ups — top-level, before sections ────────────────────────────────
  # One pop-up per room. Use Recipe 1 (SKILL.md §7) for pop-up content.
  # Use recipes-extended.md for bathroom, garage, security, vacuum rooms.

  - type: custom:bubble-card
    card_type: pop-up
    hash: '#living-room'
    name: Living Room
    icon: mdi:sofa
    entity: light.living_room_group             # REPLACE
    width_desktop: "560px"
    with_bottom_offset: true
    cards:
      # Lights
      - type: custom:bubble-card
        card_type: separator
        name: Lights
        icon: mdi:lightbulb

      - type: custom:bubble-card
        card_type: button
        button_type: slider
        entity: light.living_room_ceiling       # REPLACE
        name: Ceiling
        icon: mdi:ceiling-light
        light_slider_type: brightness
        card_layout: large

      - type: custom:bubble-card
        card_type: button
        button_type: slider
        entity: light.living_room_floor         # REPLACE
        name: Floor Lamp
        icon: mdi:floor-lamp
        light_slider_type: brightness
        card_layout: large

      # Climate
      - type: custom:bubble-card
        card_type: separator
        name: Climate
        icon: mdi:thermometer

      - type: custom:bubble-card
        card_type: button
        button_type: state
        entity: climate.living_room             # REPLACE
        name: Thermostat
        icon: mdi:thermostat
        show_state: true
        card_layout: large
        button_action:
          tap_action:
            action: more-info

      # Media
      - type: custom:bubble-card
        card_type: separator
        name: Media
        icon: mdi:television

      - type: custom:bubble-card
        card_type: media-player
        entity: media_player.living_room        # REPLACE
        name: TV
        card_layout: large
        cover_background: true

  # REPLACE: add one pop-up per additional room

  # ── Sections ─────────────────────────────────────────────────────────────
  sections:

    # Active rooms chip bar
    - type: grid
      column_span: 3
      cards:
        - type: custom:bubble-card
          card_type: sub-buttons
          hide_main_background: true
          sub_button:
            bottom:
              - name: Active Rooms
                buttons_layout: inline
                justify_content: flex-start
                group:
                  - entity: light.living_room_group   # REPLACE
                    show_name: true
                    name: Living Room
                    show_state: false
                    show_icon: true
                    fill_width: false
                    show_background: true
                    state_background: true
                  - entity: light.kitchen_group        # REPLACE
                    show_name: true
                    name: Kitchen
                    show_state: false
                    show_icon: true
                    fill_width: false
                    show_background: true
                    state_background: true
                  # REPLACE: add chip per room

    # Room button grid — 2-column for finger-sized buttons
    - type: grid
      column_span: 2
      cards:
        - type: custom:bubble-card
          card_type: button
          button_type: name
          name: Living Room
          icon: mdi:sofa
          entity: light.living_room_group       # REPLACE
          card_layout: large
          button_action:
            tap_action:
              action: navigate
              navigation_path: '#living-room'
          sub_button:
            main:
              - entity: sensor.living_room_temperature  # REPLACE
                show_state: true
                show_icon: true
                show_background: false

        - type: custom:bubble-card
          card_type: button
          button_type: name
          name: Kitchen
          icon: mdi:chef-hat
          entity: light.kitchen_group           # REPLACE
          card_layout: large
          button_action:
            tap_action:
              action: navigate
              navigation_path: '#kitchen'

        - type: custom:bubble-card
          card_type: button
          button_type: name
          name: Bedroom
          icon: mdi:bed
          entity: light.bedroom_group           # REPLACE
          card_layout: large
          button_action:
            tap_action:
              action: navigate
              navigation_path: '#bedroom'

        # REPLACE: add one button per room

    # Quick actions — full width
    - type: grid
      column_span: 3
      cards:
        - type: custom:bubble-card
          card_type: separator
          name: Quick Actions
          icon: mdi:lightning-bolt-outline

        - type: custom:bubble-card
          card_type: button
          button_type: name
          name: All Lights Off
          icon: mdi:lightbulb-off-outline
          card_layout: normal
          button_action:
            tap_action:
              action: call-service
              service: light.turn_off
              data:
                entity_id: all

        - type: custom:bubble-card
          card_type: button
          button_type: name
          name: Away Mode
          icon: mdi:home-export-outline
          card_layout: normal
          button_action:
            tap_action:
              action: call-service
              service: scene.turn_on
              target:
                entity_id: scene.away           # REPLACE

        - type: custom:bubble-card
          card_type: button
          button_type: name
          name: Good Night
          icon: mdi:weather-night
          card_layout: normal
          button_action:
            tap_action:
              action: call-service
              service: scene.turn_on
              target:
                entity_id: scene.good_night     # REPLACE

  # ── HBS footer ───────────────────────────────────────────────────────────
  - type: custom:bubble-card
    card_type: horizontal-buttons-stack
    auto_order: false
    highlight_current_view: true
    is_sidebar_hidden: true
    rise_animation: false
    1_name: Overview
    1_icon: mdi:home-variant
    1_link: /lovelace/overview
    2_name: Rooms
    2_icon: mdi:floor-plan
    2_link: /lovelace/rooms
    3_name: Scenes
    3_icon: mdi:palette
    3_link: /lovelace/scenes
    4_name: Activity
    4_icon: mdi:history
    4_link: /lovelace/activity
    5_name: Settings
    5_icon: mdi:cog
    5_link: /lovelace/settings
```

---

## #recipe-10-scenes

### Recipe 10 — Scenes view cards

See `dashboard-system.md#view-scenes` for full scaffold.
Key patterns summarised here for quick reference.

**Scene button pattern (copy for each scene):**
```yaml
- type: custom:bubble-card
  card_type: button
  button_type: name
  name: Movie                         # REPLACE scene name
  icon: mdi:movie                     # REPLACE icon
  card_layout: large
  button_action:
    tap_action:
      action: call-service
      service: scene.turn_on
      target:
        entity_id: scene.movie        # REPLACE scene entity
```

**Active scene chip (top of view, full-width section):**
```yaml
- type: grid
  column_span: 3
  cards:
    - type: custom:mushroom-chips-card
      chips:
        - type: template
          icon: mdi:palette
          content: >
            {% set s = states('input_select.active_scene') %}
            {{ s if s not in ['unknown','unavailable'] else 'No active scene' }}
          tap_action:
            action: none
```

**Guest mode toggle (bottom of view):**
```yaml
- type: custom:bubble-card
  card_type: button
  button_type: switch
  entity: input_boolean.guest_mode    # REPLACE — create via ha-yaml
  name: Guest Mode
  icon: mdi:account-plus
  card_layout: large
  sub_button:
    main:
      - name: Disables presence tracking
        show_name: true
        show_icon: false
        show_background: false
```

**ha-yaml handoff for Scenes view:**
```
# Create via ha-yaml skill:
# input_select.active_scene
#   options: [Wake Up, Bright, Relax, Dinner, Movie, Away, Night, Guest Mode]
#   Automation: when scene.* is called → set input_select to scene name
# input_boolean.guest_mode
#   When on: suspend presence-based automations, set neutral lighting
```

---

## #recipe-11-activity

### Recipe 11 — Activity view cards

See `dashboard-system.md#view-activity` for the complete scaffold with
all 8 category pairs. Key patterns summarised here.

**Category pair pattern (copy for each of the 8 categories):**
```yaml
# One section per category
- type: grid
  column_span: 2
  cards:
    # Left — event card (Option C) — tap toggles the graph
    - type: custom:bubble-card
      card_type: button
      button_type: state
      entity: sensor.last_person_event     # REPLACE per category
      name: Presence                       # REPLACE category name
      icon: mdi:account-multiple           # REPLACE icon
      show_state: true
      card_layout: normal
      button_action:
        tap_action:
          action: call-service
          service: input_boolean.toggle
          data:
            entity_id: input_boolean.show_presence_graph  # REPLACE per category

    # Right — graph (Option B) — hidden until tapped
    - type: conditional
      conditions:
        - condition: state
          entity: input_boolean.show_presence_graph  # REPLACE per category
          state: "on"
      card:
        type: custom:mini-graph-card
        entities:
          - entity: person.alice           # REPLACE per category
        name: Presence History             # REPLACE
        hours_to_show: 24
        points_per_hour: 2
        line_width: 2
```

**8 categories and their entity/boolean pairs:**

| Category | Event sensor | Graph entity | input_boolean |
|---|---|---|---|
| Presence | `sensor.last_person_event` | `person.*` | `show_presence_graph` |
| Doors & Windows | `sensor.last_door_event` | `binary_sensor.*_door` | `show_doors_graph` |
| Motion | `sensor.last_motion_event` | `binary_sensor.*_motion` | `show_motion_graph` |
| Automation | `sensor.last_automation_run` | logbook card | `show_automation_graph` |
| Energy | `sensor.current_power` | `sensor.current_power` | `show_energy_graph` |
| Maintenance | `sensor.maintenance_due_count` | battery sensors | `show_maintenance_graph` |
| Devices | `sensor.devices_offline_count` | connectivity sensors | `show_devices_graph` |
| Infrastructure | `sensor.infra_offline_count` | ping sensors | `show_infrastructure_graph` |

**ha-yaml handoff for Activity view:**
```
# Create via ha-yaml skill:
# Template sensors:
#   sensor.last_person_event  — last person home/away, name, timestamp
#   sensor.last_door_event    — last door/window opened, entity name, timestamp
#   sensor.last_motion_event  — last motion, room name, timestamp
#   sensor.last_automation_run — last automation triggered, name, timestamp
#   sensor.maintenance_due_count — count of batteries < 20% + overdue items
#   sensor.devices_offline_count — count of smart home device unavailable sensors
#   sensor.infra_offline_count  — count of ping sensor unavailable states
#
# input_boolean helpers (8 total):
#   input_boolean.show_presence_graph
#   input_boolean.show_doors_graph
#   input_boolean.show_motion_graph
#   input_boolean.show_automation_graph
#   input_boolean.show_energy_graph
#   input_boolean.show_maintenance_graph
#   input_boolean.show_devices_graph
#   input_boolean.show_infrastructure_graph
```

---

## #recipe-12-settings

### Recipe 12 — Settings view cards

See `dashboard-system.md#view-settings` for full scaffold.
Key patterns summarised here.

**Automation override toggle pattern:**
```yaml
- type: custom:bubble-card
  card_type: button
  button_type: switch
  entity: input_boolean.override_motion_lights  # REPLACE
  name: Motion Lighting Override                # REPLACE
  icon: mdi:motion-sensor-off                  # REPLACE
  card_layout: normal
  sub_button:
    main:
      - name: Keeps lights manual today         # REPLACE — describe what it does
        show_name: true
        show_icon: false
        show_background: false
```

**Quick link to HA native page:**
```yaml
- type: custom:bubble-card
  card_type: button
  button_type: name
  name: Automations
  icon: mdi:robot
  card_layout: normal
  button_action:
    tap_action:
      action: navigate
      navigation_path: /config/automation
```

**Maintenance → Activity cross-link:**
The offline devices card in Settings links back to Activity for detail:
```yaml
button_action:
  tap_action:
    action: navigate
    navigation_path: /lovelace/activity
```

---

## #recipe-13-energy-ext

### Recipe 13 — Energy extension view

See `dashboard-system.md#extension-energy` for the full scaffold.
Add this view when the user has solar panels, smart plugs with power
monitoring, or the HA Energy integration configured.

**Required sensors checklist:**
```
sensor.current_power        ← current draw in W or kW
sensor.daily_energy         ← today's total in kWh
sensor.solar_production     ← optional: solar generation in W/kW
sensor.grid_import          ← optional: grid import kWh
sensor.grid_export          ← optional: grid export kWh (solar excess)
sensor.*_power              ← optional: per-device power sensors
```

**Minimum viable Energy view (no solar, no per-device):**
```yaml
- title: Energy
  path: energy
  type: sections
  max_columns: 2
  icon: mdi:lightning-bolt
  theme: Casa5HeyneV2                  # REPLACE
  cards:
    sections:
      - type: grid
        column_span: 2
        cards:
          - type: custom:mushroom-chips-card
            chips:
              - type: entity
                entity: sensor.current_power    # REPLACE
                content_info: state
                icon: mdi:flash
                tap_action:
                  action: none
              - type: entity
                entity: sensor.daily_energy     # REPLACE
                content_info: state
                icon: mdi:counter
                tap_action:
                  action: none

      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.current_power        # REPLACE
            name: Current Draw
            icon: mdi:flash
            show_state: true
            card_layout: large

      - type: grid
        column_span: 2
        cards:
          - type: custom:mini-graph-card
            entities:
              - entity: sensor.current_power    # REPLACE
            name: Power — Last 24 Hours
            hours_to_show: 24
            points_per_hour: 4
            line_width: 2
            show:
              fill: true

      - type: grid
        column_span: 2
        cards:
          - type: custom:mini-graph-card
            entities:
              - entity: sensor.daily_energy     # REPLACE
            name: Daily Usage — This Week
            hours_to_show: 168
            points_per_hour: 0.5
            aggregate_func: max
            group_by: date

    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      auto_order: false
      highlight_current_view: true
      is_sidebar_hidden: true
      rise_animation: false
      1_name: Overview
      1_icon: mdi:home-variant
      1_link: /lovelace/overview
      2_name: Rooms
      2_icon: mdi:floor-plan
      2_link: /lovelace/rooms
      3_name: Scenes
      3_icon: mdi:palette
      3_link: /lovelace/scenes
      4_name: Activity
      4_icon: mdi:history
      4_link: /lovelace/activity
      5_name: Settings
      5_icon: mdi:cog
      5_link: /lovelace/settings
      6_name: Energy
      6_icon: mdi:lightning-bolt
      6_link: /lovelace/energy
```

---

## #recipe-14-music-ext

### Recipe 14 — Music extension view

See `dashboard-system.md#extension-music` for the full scaffold.
Add this view when the user has a multi-room audio system.

**Platform compatibility note:**
```
media_player.join / unjoin supported:
  ✓ Sonos
  ✓ Google Cast
  ✓ Music Assistant
  ✗ Spotify (no native grouping via HA)
  ✗ Apple AirPlay (use Shortcuts instead)
```

**Minimum viable Music view (single zone, no grouping):**
```yaml
- title: Music
  path: music
  type: sections
  max_columns: 1
  icon: mdi:music
  theme: Casa5HeyneV2                  # REPLACE
  cards:
    sections:
      - type: grid
        column_span: 1
        cards:
          - type: custom:bubble-card
            card_type: media-player
            entity: media_player.living_room    # REPLACE
            name: Now Playing
            card_layout: large
            cover_background: true
            show_state: true
            min_volume: 0
            max_volume: 100

    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      auto_order: false
      highlight_current_view: true
      is_sidebar_hidden: true
      rise_animation: false
      1_name: Overview
      1_icon: mdi:home-variant
      1_link: /lovelace/overview
      2_name: Rooms
      2_icon: mdi:floor-plan
      2_link: /lovelace/rooms
      3_name: Scenes
      3_icon: mdi:palette
      3_link: /lovelace/scenes
      4_name: Activity
      4_icon: mdi:history
      4_link: /lovelace/activity
      5_name: Settings
      5_icon: mdi:cog
      5_link: /lovelace/settings
      7_name: Music
      7_icon: mdi:music
      7_link: /lovelace/music
```

**Multi-zone pattern** — see `dashboard-system.md#extension-music` for
the full zone pop-up + group control scaffold.
