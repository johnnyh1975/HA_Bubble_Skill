# Dashboard Recipes Reference
# ha-bubble-dashboard skill
# View-by-view YAML for the 5-view system + 2 extension views.
# Read dashboard-system.md#classification-output to map entities to views before using these.
# All recipes use var() chains — no hardcoded colours.
# Replace placeholder entity IDs with real entities before delivering.

---

## #view-overview

### View 1 — Overview

**Purpose:** What is happening right now. No controls. Pure complications tier.
**Path:** `/lovelace/overview`
**max_columns:** 3 (default) — adjust per device-type profile

**Structure:**
```
[Full-width chip bar]          ← always visible — weather, presence, status
[Alert strip]                  ← conditionally visible — hidden when all clear
[Per-room status grid]         ← state only, no controls
[Away mode panel]              ← conditionally visible — when nobody home
[HBS footer]                   ← last card, always
```

**Chip bar (full-width section):**
```yaml
- type: grid
  column_span: 3
  cards:
    - type: custom:mushroom-chips-card
      chips:
        - type: weather
          entity: weather.home
          show_conditions: true
          show_temperature: true
          tap_action:
            action: more-info

        - type: entity
          entity: sensor.outdoor_temperature    # REPLACE
          content_info: state
          icon: mdi:thermometer
          tap_action:
            action: none

        - type: entity
          entity: person.alice                  # REPLACE — repeat per person
          content_info: name
          tap_action:
            action: more-info

        - type: entity
          entity: alarm_control_panel.home      # REPLACE
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
          entity: sensor.current_power          # REPLACE — optional
          content_info: state
          icon: mdi:flash
          tap_action:
            action: none
```

**Alert strip (conditionally visible):**

Requires `input_boolean.home_alerts_active` — set to `on` by an automation
when any alert condition is true. Hand off to ha-yaml skill for the automation.

```yaml
- type: conditional
  conditions:
    - condition: state
      entity: input_boolean.home_alerts_active   # REPLACE — create via ha-yaml
      state: "on"
  card:
    type: grid
    column_span: 3
    cards:
      - type: custom:bubble-card
        card_type: separator
        name: Alerts
        icon: mdi:alert
        # styles: accent colour for separator when alerts active
        styles: |
          .bubble-separator { background: var(--warning-color); }

      - type: custom:bubble-card
        card_type: button
        button_type: state
        entity: binary_sensor.front_door         # REPLACE — repeat per alert
        name: Front Door
        icon: mdi:door-open
        show_state: true
        card_layout: normal
        button_action:
          tap_action:
            action: none
```

**Per-room status grid:**

State-only cards — `tap_action: none`. One card per room. Sub-buttons show
temperature and motion state. The room button's active state (accent colour)
shows when lights are on — no interaction needed to read it.

```yaml
- type: grid
  column_span: 3
  cards:
    - type: custom:bubble-card
      card_type: separator
      name: Home Status
      icon: mdi:home

    - type: custom:bubble-card
      card_type: button
      button_type: state
      name: Living Room
      icon: mdi:sofa
      entity: light.living_room_group           # REPLACE
      show_state: false
      card_layout: normal
      button_action:
        tap_action:
          action: none                          # Overview = no controls
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

    # REPLACE: repeat for each room
    - type: custom:bubble-card
      card_type: button
      button_type: state
      name: Kitchen
      icon: mdi:chef-hat
      entity: light.kitchen_group               # REPLACE
      show_state: false
      card_layout: normal
      button_action:
        tap_action:
          action: none
```

**Away mode panel (conditionally visible):**

Shown when no person entity is `home`. Replaces the per-room grid visually
when the house is empty. The per-room grid is still rendered but the away
panel draws the eye first when visible.

```yaml
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
        name: Away
        icon: mdi:home-export-outline

      - type: custom:bubble-card
        card_type: button
        button_type: state
        entity: alarm_control_panel.home        # REPLACE
        name: Security
        show_state: true
        card_layout: normal
        button_action:
          tap_action:
            action: none

      - type: custom:bubble-card
        card_type: button
        button_type: state
        entity: sensor.lights_on_count          # REPLACE — template sensor
        name: Lights
        icon: mdi:lightbulb
        show_state: true
        card_layout: normal
        button_action:
          tap_action:
            action: none
```

---

## #view-rooms

### View 2 — Rooms

**Purpose:** What I want to control. Brief interaction.
**Path:** `/lovelace/rooms`
**max_columns:** 3 (default)

**Structure:**
```
[Pop-ups]                      ← top-level cards, before sections
[Full-width chip bar]          ← active room summary
[Room button grid]             ← 2-column, large cards
[Quick actions bar]            ← full-width, bottom of sections
[HBS footer]                   ← last top-level card
```

**Complete Rooms view scaffold:**
```yaml
- title: Rooms
  path: rooms
  type: sections
  max_columns: 3
  cards:

    # ── Pop-ups — top-level, before sections ────────────────
    - type: custom:bubble-card
      card_type: pop-up
      hash: '#living-room'
      name: Living Room
      icon: mdi:sofa
      entity: light.living_room_group           # REPLACE
      width_desktop: "560px"
      with_bottom_offset: true
      cards:
        # Use Recipe 1 pattern — see §7 in SKILL.md
        # Use recipes-extended.md for bathroom, garage, security, vacuum

    - type: custom:bubble-card
      card_type: pop-up
      hash: '#kitchen'
      name: Kitchen
      icon: mdi:chef-hat
      entity: light.kitchen_group               # REPLACE
      width_desktop: "560px"
      with_bottom_offset: true
      cards:
        # Recipe 1 pattern

    # REPLACE: add one pop-up per room

    # ── Sections ────────────────────────────────────────────
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
                - name: Active
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
                    - entity: light.kitchen_group       # REPLACE
                      show_name: true
                      name: Kitchen
                      show_state: false
                      show_icon: true
                      fill_width: false
                      show_background: true
                      state_background: true
                    # REPLACE: add chip per room

      # Room button grid
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Living Room
            icon: mdi:sofa
            entity: light.living_room_group     # REPLACE
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
            entity: light.kitchen_group         # REPLACE
            card_layout: large
            button_action:
              tap_action:
                action: navigate
                navigation_path: '#kitchen'

          # REPLACE: add one button per room

      # Quick actions bar
      - type: grid
        column_span: 3
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Quick Actions
            icon: mdi:lightning-bolt

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: All Lights Off
            icon: mdi:lightbulb-off
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

    # ── HBS footer — last top-level card ────────────────────
    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      # ... (see #navigation-layer for full HBS nav config)
```

---

## #view-scenes

### View 3 — Scenes

**Purpose:** How I want the home to feel. Brief interaction.
**Path:** `/lovelace/scenes`
**max_columns:** 3

**Structure:**
```
[Active scene chip]            ← always visible — which scene is active
[Morning group]
[Evening group]
[Entertainment group]
[Away / Security group]
[Guest mode toggle]            ← input_boolean, not a scene
[HBS footer]
```

**Complete Scenes view scaffold:**
```yaml
- title: Scenes
  path: scenes
  type: sections
  max_columns: 3
  cards:
    sections:

      # Active scene chip
      - type: grid
        column_span: 3
        cards:
          - type: custom:mushroom-chips-card
            chips:
              - type: template
                icon: mdi:palette
                content: >
                  {% set s = states('input_select.active_scene') %}
                  {{ s if s != 'unknown' else 'No active scene' }}
                # Requires input_select.active_scene — hand off to ha-yaml
                tap_action:
                  action: none

      # Morning scenes
      - type: grid
        column_span: 3
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Morning
            icon: mdi:weather-sunrise

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Wake Up
            icon: mdi:alarm
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.wake_up        # REPLACE

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Bright
            icon: mdi:brightness-7
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.bright         # REPLACE

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Energise
            icon: mdi:lightning-bolt
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.energise       # REPLACE

      # Evening scenes
      - type: grid
        column_span: 3
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Evening
            icon: mdi:weather-sunset

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Relax
            icon: mdi:sofa
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.relax          # REPLACE

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Dinner
            icon: mdi:food-fork-drink
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.dinner         # REPLACE

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Cosy
            icon: mdi:candle
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.cosy           # REPLACE

      # Entertainment scenes
      - type: grid
        column_span: 3
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Entertainment
            icon: mdi:television-play

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Movie
            icon: mdi:movie
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.movie          # REPLACE

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Gaming
            icon: mdi:controller
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.gaming         # REPLACE

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Party
            icon: mdi:party-popper
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.party          # REPLACE

      # Away / Security scenes
      - type: grid
        column_span: 3
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Away & Security
            icon: mdi:shield-home

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Away
            icon: mdi:home-export-outline
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.away           # REPLACE

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Vacation
            icon: mdi:airplane
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.vacation       # REPLACE

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Night
            icon: mdi:weather-night
            card_layout: large
            button_action:
              tap_action:
                action: call-service
                service: scene.turn_on
                target:
                  entity_id: scene.night          # REPLACE

      # Guest mode — persistent toggle, not a scene
      - type: grid
        column_span: 3
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Modes
            icon: mdi:account-group

          - type: custom:bubble-card
            card_type: button
            button_type: switch
            entity: input_boolean.guest_mode      # REPLACE — create via ha-yaml
            name: Guest Mode
            icon: mdi:account-plus
            card_layout: large
            sub_button:
              main:
                - name: Disables presence tracking
                  show_name: true
                  show_icon: false
                  show_background: false

    # HBS footer
    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      # ... (see #navigation-layer)
```

**ha-yaml handoff for Scenes view:**
```
# Hand off to ha-yaml skill:
# 1. input_select.active_scene — tracks which scene was last activated
#    Trigger: scene activated → set input_select option to scene name
# 2. input_boolean.guest_mode — disables presence tracking automations
#    When on: pause person-based automations, set neutral lighting defaults
```

---

## #view-activity

### View 4 — Activity

**Purpose:** What has happened. Passive review.
**Path:** `/lovelace/activity`
**max_columns:** 2 (event card left, graph right — pair pattern)

**Architecture:**

Each category uses a paired card pattern:
- **Left:** Bubble Card state button showing the last event (Option C)
- **Right:** Graph card showing the pattern — hidden until the event card is tapped (Option B)
- **Mechanism:** tapping the event card toggles an `input_boolean`, the graph
  card is wrapped in a conditional that reads that boolean

**8 input_boolean helpers required** — hand off to ha-yaml:
```
# ha-yaml handoff — create these helpers:
input_boolean:
  show_presence_graph:
    name: Show Presence Graph
  show_doors_graph:
    name: Show Doors Graph
  show_motion_graph:
    name: Show Motion Graph
  show_automation_graph:
    name: Show Automation Graph
  show_energy_graph:
    name: Show Energy Graph
  show_maintenance_graph:
    name: Show Maintenance Graph
  show_devices_graph:
    name: Show Devices Graph
  show_infrastructure_graph:
    name: Show Infrastructure Graph
```

**Template sensors required** — hand off to ha-yaml:
```
# ha-yaml handoff — create these template sensors:
# sensor.last_person_event     — last person home/away + name + timestamp
# sensor.last_door_event       — last door/window opened + which one
# sensor.last_motion_event     — last motion detected + room
# sensor.last_automation_run   — last automation triggered + name
# sensor.maintenance_due_count — count of items below threshold or overdue
# sensor.devices_offline_count — count of smart home devices unavailable
# sensor.infra_offline_count   — count of infrastructure devices offline
```

**Category pair template (repeat for each category):**
```yaml
# One section per category — column_span: 2 puts event left, graph right
- type: grid
  column_span: 2
  cards:
    # Left — event card (Option C)
    - type: custom:bubble-card
      card_type: button
      button_type: state
      entity: sensor.last_person_event          # REPLACE per category
      name: Presence
      icon: mdi:account-multiple
      show_state: true
      card_layout: normal
      button_action:
        tap_action:
          action: call-service
          service: input_boolean.toggle
          data:
            entity_id: input_boolean.show_presence_graph  # REPLACE per category

    # Right — graph (Option B) — hidden until event card tapped
    - type: conditional
      conditions:
        - condition: state
          entity: input_boolean.show_presence_graph       # REPLACE per category
          state: "on"
      card:
        type: custom:mini-graph-card
        entities:
          - entity: person.alice                          # REPLACE per category
          - entity: person.bob
        name: Presence History
        hours_to_show: 24
        points_per_hour: 4
        line_width: 2
        show:
          labels: false
          points: false
          legend: true
```

**Complete Activity view scaffold:**
```yaml
- title: Activity
  path: activity
  type: sections
  max_columns: 2
  cards:
    sections:

      # ── Home Activity ──────────────────────────────────────

      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Home Activity
            icon: mdi:home-clock

      # Presence
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.last_person_event
            name: Presence
            icon: mdi:account-multiple
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: input_boolean.toggle
                data:
                  entity_id: input_boolean.show_presence_graph
          - type: conditional
            conditions:
              - condition: state
                entity: input_boolean.show_presence_graph
                state: "on"
            card:
              type: custom:mini-graph-card
              entities:
                - entity: person.alice            # REPLACE
                - entity: person.bob              # REPLACE
              name: Presence History
              hours_to_show: 24
              points_per_hour: 2
              line_width: 2

      # Doors & Windows
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.last_door_event
            name: Doors & Windows
            icon: mdi:door
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: input_boolean.toggle
                data:
                  entity_id: input_boolean.show_doors_graph
          - type: conditional
            conditions:
              - condition: state
                entity: input_boolean.show_doors_graph
                state: "on"
            card:
              type: custom:mini-graph-card
              entities:
                - entity: binary_sensor.front_door      # REPLACE
                - entity: binary_sensor.back_door       # REPLACE
              name: Door History
              hours_to_show: 24
              points_per_hour: 4

      # Motion
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.last_motion_event
            name: Motion
            icon: mdi:motion-sensor
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: input_boolean.toggle
                data:
                  entity_id: input_boolean.show_motion_graph
          - type: conditional
            conditions:
              - condition: state
                entity: input_boolean.show_motion_graph
                state: "on"
            card:
              type: custom:mini-graph-card
              entities:
                - entity: binary_sensor.living_room_motion  # REPLACE
                - entity: binary_sensor.kitchen_motion      # REPLACE
              name: Motion History
              hours_to_show: 24
              points_per_hour: 4

      # Automation
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.last_automation_run
            name: Automations
            icon: mdi:robot
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: input_boolean.toggle
                data:
                  entity_id: input_boolean.show_automation_graph
          - type: conditional
            conditions:
              - condition: state
                entity: input_boolean.show_automation_graph
                state: "on"
            card:
              type: logbook                       # logbook for automation history
              entities:
                - automation.motion_lights        # REPLACE — key automations only
                - automation.climate_schedule     # REPLACE
              hours_to_show: 24

      # ── Home Health ────────────────────────────────────────

      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Home Health
            icon: mdi:heart-pulse

      # Energy
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.current_power          # REPLACE
            name: Energy
            icon: mdi:flash
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: input_boolean.toggle
                data:
                  entity_id: input_boolean.show_energy_graph
          - type: conditional
            conditions:
              - condition: state
                entity: input_boolean.show_energy_graph
                state: "on"
            card:
              type: custom:mini-graph-card
              entities:
                - entity: sensor.current_power    # REPLACE
              name: Power History
              hours_to_show: 24
              points_per_hour: 4
              line_width: 2
              show:
                fill: true

      # Maintenance
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.maintenance_due_count
            name: Maintenance
            icon: mdi:wrench
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: input_boolean.toggle
                data:
                  entity_id: input_boolean.show_maintenance_graph
          - type: conditional
            conditions:
              - condition: state
                entity: input_boolean.show_maintenance_graph
                state: "on"
            card:
              type: custom:mini-graph-card
              entities:
                - entity: sensor.vacuum_battery   # REPLACE — low battery devices
                - entity: sensor.smoke_detector_battery  # REPLACE
              name: Battery Levels
              hours_to_show: 168                  # 7 days
              points_per_hour: 1
              line_width: 2

      # Devices (smart home)
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.devices_offline_count
            name: Devices
            icon: mdi:devices
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: input_boolean.toggle
                data:
                  entity_id: input_boolean.show_devices_graph
          - type: conditional
            conditions:
              - condition: state
                entity: input_boolean.show_devices_graph
                state: "on"
            card:
              type: custom:mini-graph-card
              entities:
                - entity: binary_sensor.zigbee_coordinator_connectivity  # REPLACE
                - entity: binary_sensor.zwave_stick_connectivity          # REPLACE
                - entity: binary_sensor.hacs_connectivity                 # REPLACE
              name: Device Connectivity
              hours_to_show: 24
              points_per_hour: 2
              line_width: 2
              fill: false

      # Infrastructure
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.infra_offline_count
            name: Infrastructure
            icon: mdi:server-network
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: input_boolean.toggle
                data:
                  entity_id: input_boolean.show_infrastructure_graph
          - type: conditional
            conditions:
              - condition: state
                entity: input_boolean.show_infrastructure_graph
                state: "on"
            card:
              type: custom:mini-graph-card
              entities:
                # Basic network gear
                - entity: binary_sensor.router_ping       # REPLACE
                - entity: binary_sensor.wifi_ap_ping      # REPLACE
                # Extended infrastructure — add what you have:
                # - entity: binary_sensor.nas_ping
                # - entity: binary_sensor.firewall_ping   # pfSense / OPNsense
                # - entity: binary_sensor.homelab_ping
                # - entity: binary_sensor.ups_status
              name: Infrastructure Uptime
              hours_to_show: 24
              points_per_hour: 2
              line_width: 2
              fill: false

    # HBS footer
    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      # ... (see #navigation-layer)
```

**Fallback — use this if template sensors are not yet set up:**
Replace the Option C event cards with a single logbook card:
```yaml
- type: logbook
  entities:
    - person.alice
    - binary_sensor.front_door
    - alarm_control_panel.home
    # Add your key entities
  hours_to_show: 24
```
Swap in the full Option C + Option B pattern once template sensors are in place.

---

## #view-settings

### View 5 — Settings

**Purpose:** How the home is configured. Deep engagement.
**Path:** `/lovelace/settings`
**max_columns:** 3

**Structure:**
```
[Automation overrides]         ← input_boolean toggles
[Maintenance — actionable]     ← what needs attention now
[Threshold controls]           ← number inputs
[Quick links]                  ← navigate to HA native editors
[Admin section]                ← conditionally visible — admin user only
[HBS footer]
```

**Note on Maintenance split:**
Activity / Maintenance = what happened (events, timestamps, history)
Settings / Maintenance = what needs action now (below threshold, overdue, offline)

```yaml
- title: Settings
  path: settings
  type: sections
  max_columns: 3
  cards:
    sections:

      # Automation overrides
      - type: grid
        column_span: 3
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Automation Overrides
            icon: mdi:robot-off

          - type: custom:bubble-card
            card_type: button
            button_type: switch
            entity: input_boolean.override_motion_lights  # REPLACE — via ha-yaml
            name: Motion Lighting Override
            icon: mdi:motion-sensor-off
            card_layout: normal
            sub_button:
              main:
                - name: Keeps lights manual today
                  show_name: true
                  show_icon: false
                  show_background: false

          - type: custom:bubble-card
            card_type: button
            button_type: switch
            entity: input_boolean.override_climate       # REPLACE
            name: Climate Override
            icon: mdi:thermostat-auto
            card_layout: normal
            sub_button:
              main:
                - name: Manual temperature control
                  show_name: true
                  show_icon: false
                  show_background: false

          - type: custom:bubble-card
            card_type: button
            button_type: switch
            entity: input_boolean.holiday_mode          # REPLACE
            name: Holiday Mode
            icon: mdi:airplane
            card_layout: normal
            sub_button:
              main:
                - name: Simulates occupancy while away
                  show_name: true
                  show_icon: false
                  show_background: false

      # Maintenance — actionable items only
      - type: grid
        column_span: 3
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Maintenance
            icon: mdi:wrench-clock

          # Low battery devices (show when battery < 20%)
          - type: conditional
            conditions:
              - condition: template
                value_template: "{{ states('sensor.vacuum_battery') | int < 20 }}"
            card:
              type: custom:bubble-card
              card_type: button
              button_type: state
              entity: sensor.vacuum_battery      # REPLACE
              name: Vacuum Battery Low
              icon: mdi:robot-vacuum
              show_state: true
              card_layout: normal

          # Offline devices — always visible, shows count
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.devices_offline_count
            name: Offline Devices
            icon: mdi:devices
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: navigate
                navigation_path: /lovelace/activity  # → Activity view for detail

          # Maintenance schedule
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: input_datetime.next_filter_change  # REPLACE — via ha-yaml
            name: Filter Change
            icon: mdi:air-filter
            show_state: true
            card_layout: normal

      # Threshold controls
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Thresholds
            icon: mdi:tune

          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: input_number.motion_timeout  # REPLACE — via ha-yaml
            name: Motion Timeout
            icon: mdi:timer
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: more-info

          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: input_number.climate_setback # REPLACE
            name: Climate Setback
            icon: mdi:thermometer-minus
            show_state: true
            card_layout: normal
            button_action:
              tap_action:
                action: more-info

      # Quick links to HA native pages
      - type: grid
        column_span: 1
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: HA Links
            icon: mdi:open-in-new

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

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Devices
            icon: mdi:chip
            card_layout: normal
            button_action:
              tap_action:
                action: navigate
                navigation_path: /config/devices

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Energy Dashboard
            icon: mdi:lightning-bolt
            card_layout: normal
            button_action:
              tap_action:
                action: navigate
                navigation_path: /energy

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Full Logbook
            icon: mdi:history
            card_layout: normal
            button_action:
              tap_action:
                action: navigate
                navigation_path: /logbook

      # Admin section — conditionally visible (admin user only)
      - type: grid
        column_span: 3
        cards:
          # Requires template: {{ is_admin }} — or user context check
          # Show only for admin user. Hand off logic to ha-yaml skill.
          - type: custom:bubble-card
            card_type: separator
            name: Admin
            icon: mdi:shield-account

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Integrations
            icon: mdi:puzzle
            card_layout: normal
            button_action:
              tap_action:
                action: navigate
                navigation_path: /config/integrations

    # HBS footer
    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      # ... (see #navigation-layer)
```

---

## #extension-energy

### Extension View +E — Energy

**Purpose:** Consumption, solar production, cost monitoring.
**Path:** `/lovelace/energy`
**max_columns:** 2
**Add when:** user has solar panels, energy monitoring sensors, or actively
tracks consumption.

**Required sensors:** `sensor.current_power`, `sensor.daily_energy`,
optionally `sensor.solar_production`, `sensor.grid_import`, `sensor.grid_export`.
If using the HA Energy integration, these are available automatically.

```yaml
- title: Energy
  path: energy
  type: sections
  max_columns: 2
  cards:
    sections:

      # Summary chip bar
      - type: grid
        column_span: 2
        cards:
          - type: custom:mushroom-chips-card
            chips:
              - type: entity
                entity: sensor.current_power     # REPLACE
                content_info: state
                icon: mdi:flash
                tap_action:
                  action: none

              - type: entity
                entity: sensor.daily_energy      # REPLACE
                content_info: state
                icon: mdi:counter
                tap_action:
                  action: none

              - type: entity
                entity: sensor.solar_production  # REPLACE — remove if no solar
                content_info: state
                icon: mdi:solar-panel
                tap_action:
                  action: none

              - type: template
                icon: mdi:currency-eur           # REPLACE currency icon
                content: >
                  {{ (states('sensor.daily_energy') | float * 0.30)
                     | round(2) }} €
                  # REPLACE: adjust rate (0.30 = €0.30/kWh)
                tap_action:
                  action: none

      # Live consumption
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.current_power         # REPLACE
            name: Current Draw
            icon: mdi:flash
            show_state: true
            card_layout: large
            sub_button:
              main:
                - entity: sensor.daily_energy    # REPLACE
                  show_state: true
                  show_icon: true
                  icon: mdi:counter
                  show_background: false

      # Daily consumption graph
      - type: grid
        column_span: 2
        cards:
          - type: custom:mini-graph-card
            entities:
              - entity: sensor.current_power     # REPLACE
                name: Consumption
            name: Power — Last 24 Hours
            hours_to_show: 24
            points_per_hour: 4
            line_width: 2
            show:
              fill: true
              legend: false

      # Solar production graph (remove if no solar)
      - type: grid
        column_span: 2
        cards:
          - type: custom:mini-graph-card
            entities:
              - entity: sensor.solar_production  # REPLACE
                name: Solar
                color: var(--warning-color)
              - entity: sensor.current_power     # REPLACE
                name: Consumption
            name: Solar vs Consumption
            hours_to_show: 24
            points_per_hour: 4
            line_width: 2

      # Device breakdown
      - type: grid
        column_span: 1
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Devices
            icon: mdi:power-plug

          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.washing_machine_power # REPLACE
            name: Washing Machine
            icon: mdi:washing-machine
            show_state: true
            card_layout: normal

          - type: custom:bubble-card
            card_type: button
            button_type: state
            entity: sensor.dishwasher_power      # REPLACE
            name: Dishwasher
            icon: mdi:dishwasher
            show_state: true
            card_layout: normal

          # REPLACE: add per-device power sensors

      # Weekly comparison
      - type: grid
        column_span: 1
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: History
            icon: mdi:chart-bar

          - type: custom:mini-graph-card
            entities:
              - entity: sensor.daily_energy      # REPLACE
            name: This Week
            hours_to_show: 168                   # 7 days
            points_per_hour: 0.5
            aggregate_func: max
            group_by: date

    # HBS footer
    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      # ... (see #navigation-layer)
```

---

## #extension-music

### Extension View +M — Music

**Purpose:** Multi-room audio control across all zones.
**Path:** `/lovelace/music`
**max_columns:** 2
**Add when:** user has a multi-room audio system (Sonos, Cast, Spotify Connect, etc.)

**Note on group controls:** `media_player.join` and `media_player.unjoin` are
required for zone grouping. Supported platforms: Sonos, Cast, Music Assistant.
Check platform documentation before generating group control cards.

```yaml
- title: Music
  path: music
  type: sections
  max_columns: 2
  cards:

    # ── Zone pop-ups — top-level ─────────────────────────────
    - type: custom:bubble-card
      card_type: pop-up
      hash: '#zone-living-room'
      name: Living Room
      icon: mdi:sofa
      width_desktop: "560px"
      with_bottom_offset: true
      cards:
        - type: custom:bubble-card
          card_type: separator
          name: Living Room Audio
          icon: mdi:speaker

        - type: custom:bubble-card
          card_type: media-player
          entity: media_player.living_room      # REPLACE
          name: Living Room
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
                show_state: true
                show_background: false

    # REPLACE: add one pop-up per zone

    sections:

      # Now playing — master card
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: media-player
            entity: media_player.living_room    # REPLACE — primary player or group
            name: Now Playing
            card_layout: large
            cover_background: true
            show_state: true
            min_volume: 0
            max_volume: 100

      # Zone grid
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Zones
            icon: mdi:speaker-multiple

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Living Room
            icon: mdi:sofa
            entity: media_player.living_room    # REPLACE
            card_layout: large
            button_action:
              tap_action:
                action: navigate
                navigation_path: '#zone-living-room'
            sub_button:
              main:
                - entity: media_player.living_room  # REPLACE
                  show_attribute: true
                  attribute: volume_level
                  show_icon: true
                  icon: mdi:volume-high
                  show_background: false

          # REPLACE: add one button per zone

      # Group controls
      - type: grid
        column_span: 2
        cards:
          - type: custom:bubble-card
            card_type: separator
            name: Group Control
            icon: mdi:speaker-multiple

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Sync All Zones
            icon: mdi:link
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: media_player.join
                data:
                  group_members:
                    - media_player.kitchen        # REPLACE
                    - media_player.bedroom        # REPLACE
                  entity_id: media_player.living_room  # REPLACE — leader

          - type: custom:bubble-card
            card_type: button
            button_type: name
            name: Separate All Zones
            icon: mdi:link-off
            card_layout: normal
            button_action:
              tap_action:
                action: call-service
                service: media_player.unjoin
                data:
                  entity_id:
                    - media_player.living_room    # REPLACE — list all zones
                    - media_player.kitchen
                    - media_player.bedroom

    # HBS footer
    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      # ... (see #navigation-layer)
```

---

