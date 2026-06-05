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


## Core Recipes

Copy-paste-ready YAML for the most common single-view patterns.
All YAML uses the Casa5HeyneV2 var() chain — no hardcoded colours.
Replace placeholder entity IDs with real entities.

## #recipe-1-room-popup
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

## #recipe-2-hbs
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

## #recipe-3-media-player
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

## #recipe-4-climate
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

## #recipe-5-chip-bar
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

## #recipe-6-streamline
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
