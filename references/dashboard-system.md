# Dashboard System Reference
# ha-bubble-dashboard skill
# Covers: 5-view standard dashboard architecture + 2 extension views.
# Read this file before generating any full dashboard from scratch.
# All recipes use var() chains — no hardcoded colours.
# Replace placeholder entity IDs with real entities before delivering.

---

## #system-overview

### The 5-view dashboard system

The 5-view system is the recommended structure for all new Home Assistant
dashboards built with this skill. Each view has exactly one purpose and one
engagement type. Users always know where to go.

| # | View | Icon | Purpose | Engagement type |
|---|---|---|---|---|
| 1 | Overview | `mdi:home-variant` | What is happening right now | Complications — passive |
| 2 | Rooms | `mdi:floor-plan` | What I want to control | Brief interaction |
| 3 | Scenes | `mdi:palette` | How I want the home to feel | Brief interaction |
| 4 | Activity | `mdi:history` | What has happened | Passive review |
| 5 | Settings | `mdi:cog` | How the home is configured | Deep engagement |

**Extension views** (add when the domain is actively used):

| + | View | Icon | Purpose | Add when |
|---|---|---|---|---|
| +E | Energy | `mdi:lightning-bolt` | Consumption, solar, cost | Solar panels or active energy monitoring |
| +M | Music | `mdi:music` | Multi-room audio control | Multi-room audio system (Sonos, Cast, etc.) |

**The core principle:** each view has one engagement type. Never mix engagement
types on the same view. The Overview is never a control surface. The Rooms view
never shows history. The Settings view never competes with the Overview for
daily attention.

---

## #native-first

### The native-first check

Home Assistant's built-in dashboards have converged on much of this skill's
philosophy. As of HA 2026.2 the new Home dashboard ("Overview") is the default
for all new installations — summary cards, favourites and area views with no
YAML at all. HA 2026.5 added a native Maintenance dashboard (battery states
for every device in one overview), an Activity list on the Security dashboard
(state-change log for locks and sensors), customisable Overview summaries and
the Shortcut card. HA 2026.6 rebuilt the add-card dialog around entities and
added forecast features to the weather tile plus a full set of media-player
tile features (source picker, sound mode, mute, reorderable playback buttons).

**The rule, parallel to automate-first:** before building a custom section,
check whether native HA already provides it. Building UI the platform ships
for free adds maintenance surface without adding capability — the same logic
that says a motion-triggered light does not need a card.

| Before building this… | …check this native feature first |
|---|---|
| Battery grid (Settings / Activity view) | Maintenance dashboard (HA 2026.5+) |
| Security / door event log | Security dashboard → Activity list (HA 2026.5+) |
| Weather forecast pop-up or graph | Weather tile forecast features (HA 2026.6+) |
| Full media transport controls | Media player tile features (HA 2026.5/2026.6+) |
| Generic "everything" dashboard | Native Home dashboard — may be enough |
| Combined battery state of charge for a storage system | Energy dashboard's combined battery level, capacity-weighted (HA 2026.8+) |
| A clock card with the date under the time | Native clock card — it does dates now (HA 2026.8+) |

**Tone:** always Advisory. Present the native option, state the trade-off,
and let the user decide. Never refuse to build the custom version.

### When is a custom Bubble dashboard worth it?

The native Home dashboard is auto-generated and generic. A custom Bubble
build earns its maintenance cost when the user wants:

- **Curation** — the engagement-type model: only what automation cannot
  handle, structured by interaction type. Native shows everything by area.
- **Progressive disclosure** — room pop-ups, HBS footer navigation, the
  5-view system. Native has no equivalent to pop-up-based room control.
- **Identity** — the Casa5HeyneV2 theme, custom typography, wall-panel
  single-mode designs. Native styling is fixed.
- **Fixed displays** — kiosk and wall-panel layouts (`#device-type-profiles`,
  `#wall-panel-hardening`). Native layouts are not designed for this.

If none of these apply — the user just wants "a dashboard" — say so honestly:
the native default plus a few favourites may serve them better than a custom
build they must maintain. Hybrid setups (native Home dashboard for daily use,
one custom Bubble wall-panel view) are valid and common.

---

## #navigation-layer

### Navigation: Sidebar Card + HBS footer

The 5-view system uses a two-component navigation layer:

**Desktop — Sidebar Card:**
Always visible on desktop. Shows clock, date, contextual home state summary,
and nav links to all 5 (or 7) views.

**Mobile — HBS footer:**
Always present. Links to view paths, not pop-up hashes. Fixed order —
`auto_order: false`. No `_pir_sensor` — views are not room-based.

**Combined pattern (default — "both equally"):**
```yaml
# At root of dashboard YAML — Sidebar Card config
sidebar:
  width:
    mobile: 0
    tablet: 0
    desktop: 20          # only appears on desktop
  digitalClock: true
  date: true
  dateFormat: "dddd, D MMMM"
  template: |
    <li>
      {% if now().hour < 12 %}Good morning
      {% elif now().hour < 18 %}Good afternoon
      {% else %}Good evening{% endif %}
    </li>
    {% set lights = states.light | selectattr('state','eq','on') | list | count %}
    {% if lights > 0 %}<li>{{ lights }} light{{ 's' if lights > 1 }} on</li>{% endif %}
    {% set people = states.person | selectattr('state','eq','home') | list | count %}
    {% if people > 0 %}<li>{{ people }} home</li>{% else %}<li>Nobody home</li>{% endif %}
  menu:
    - name: Overview
      path: /lovelace/overview
      icon: mdi:home-variant
    - name: Rooms
      path: /lovelace/rooms
      icon: mdi:floor-plan
    - name: Scenes
      path: /lovelace/scenes
      icon: mdi:palette
    - name: Activity
      path: /lovelace/activity
      icon: mdi:history
    - name: Settings
      path: /lovelace/settings
      icon: mdi:cog
    # Extension views — add when relevant:
    # - name: Energy
    #   path: /lovelace/energy
    #   icon: mdi:lightning-bolt
    # - name: Music
    #   path: /lovelace/music
    #   icon: mdi:music
```

**HBS footer (place as last card on every view):**
```yaml
- type: custom:bubble-card
  card_type: horizontal-buttons-stack
  auto_order: false              # views have fixed order
  highlight_current_view: true
  is_sidebar_hidden: true        # Sidebar Card handles desktop nav
  rise_animation: false          # never use on fixed-view nav

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

  # Extension views — add when relevant:
  # 6_name: Energy
  # 6_icon: mdi:lightning-bolt
  # 6_link: /lovelace/energy
  # 7_name: Music
  # 7_icon: mdi:music
  # 7_link: /lovelace/music
```

**Note on HBS button count:** 5 buttons is comfortable. 7 is the practical
limit before the footer feels crowded on small phones. If adding both extension
views, test on mobile before delivering.

---


## #classification-output

### Mapping classification output to the 5-view system

When the full-dashboard workflow (§2#full-dashboard-workflow) produces a
classification, map the buckets to views as follows:

| Bucket | Maps to | Recipe |
|---|---|---|
| Bucket 0 — Automate | ha-yaml handoff note | None — note per entity |
| Bucket 1 — Complications | Overview chip bar + per-room status | #view-overview |
| Bucket 2 — Brief interaction | Rooms view buttons + pop-ups | #view-rooms |
| Bucket 2 — Scenes | Scenes view | #view-scenes |
| Bucket 3 — Deep engagement | Settings view + extension views | #view-settings |

**Activity view** is not populated from the classification — it is populated
from HA history data automatically once template sensors and helpers are in place.
Generate it with placeholder entity IDs and note the ha-yaml handoff.

**Standard generation order:**
1. Navigation layer (Sidebar + HBS) — shared across all views
2. Overview view — chip bar + room status grid (Bucket 1 entities)
3. Rooms view — room buttons + pop-ups (Bucket 2 entities, grouped by room)
4. Scenes view — scene buttons (existing HA scenes, grouped by time of day)
5. Activity view — category pairs with placeholder sensors + ha-yaml handoff
6. Settings view — override toggles + maintenance + quick links
7. Offer: "Want me to generate the Energy or Music extension views?"

---

## #full-dashboard-workflow

### Full-dashboard design workflow

Run this workflow whenever generating a full dashboard from scratch.

**Step 1 — Collect**

Ask for (or infer from context):
- Entity list or room/device description
- Primary device: phone / tablet / desktop / both (→ `#device-type-profiles`)
- Fixed display? wall panel / kiosk → single-mode theme question

If the user hasn't listed entities: "List your devices or entity IDs — rooms,
sensors, lights, climate, media players, covers. Don't filter yet, just list
everything."

If the user says "build something typical" with no entities → use Recipe 0
placeholder entities and note that.

**Producing the entity list — offer this snippet** (see `#entity-inventory`):
if the user has HA open, the fastest way to collect a complete, area-grouped
inventory is a one-off template evaluation — not a template sensor, so it
stays within this skill's scope.


**Step 2 — Classify**

Sort every entity into one of four buckets before writing any YAML.

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

Look up the device in `#device-type-profiles`. Apply max_columns, card_layout,
font size, and nav pattern before generating any YAML.

**Step 5 — Generate from the 5-view system**

Map the classification output to views — see `#classification-output`.
Read the relevant view sections before generating.

**Step 6 — After delivery**

Offer two things, briefly:
- "Want me to generate the Activity or Settings view?"
- "Want the automation suggestions for the Bucket 0 items? I'll hand those
  off to the ha-yaml skill with context."

---

## #entity-rename-risk

### Entity IDs can now be renamed from the UI — plan for it

Since HA 2026.8, renaming an entity ID is a two-click operation in the entity
settings, and HA nudges people toward tidy, consistent naming. Dashboards are
the most fragile consumer of entity IDs: nothing validates them, and a card
pointing at a renamed entity simply shows *Entity not available* — silently,
and often only on one view the user rarely opens.

**When a user mentions renaming entities, or asks for help tidying entity IDs:**

- Say plainly that dashboard YAML does not follow renames. HA's repair flow
  covers automations and scripts far better than it covers Lovelace.
- Recommend the order: rename first, then fix the dashboard — and offer the
  health check (§9) against the pasted YAML afterwards to find the orphans.
- For a Streamline-templated dashboard, entity IDs usually sit in the template
  *arguments*, so the damage is concentrated and easy to repair — one more
  argument for templating repeated structures.
- `sensor.` entities feeding a graph or a template sensor are the ones people
  forget; the card breaks quietly rather than visibly.

Renaming is not a bad idea — consistent IDs make everything downstream easier.
The point is to sequence it, not to discourage it.

---

## #entity-inventory

### Entity inventory snippet — the Collect step, made easy

Paste this into **Tools → Template** (named *Developer Tools* before HA
2026.8), then copy the output back
into the conversation. It is a one-off evaluation — nothing is created or
saved in HA.

```jinja2
{%- for area in areas() %}
## {{ area_name(area) }}
{%- for eid in area_entities(area) %}
{%- set d = eid.split('.')[0] %}
{%- if d in ['light','switch','climate','cover','fan','media_player',
             'vacuum','lock','camera','alarm_control_panel','humidifier',
             'scene','script','person','binary_sensor','sensor',
             'input_boolean','input_select','select'] %}
- {{ eid }}{% if state_attr(eid,'device_class') %} ({{ state_attr(eid,'device_class') }}){% endif %}
{%- endif %}
{%- endfor %}
{%- endfor %}
```

**Notes:**
- Output is grouped by HA area — rooms come for free if areas are assigned.
- Entities with no area do not appear; ask the user to mention anything
  missing ("anything important not in the list?").
- `device_class` is included where set — it improves Bucket 0 classification
  (motion, door, window, power…).
- If the list is very long, ask the user to trim domains they know they
  don't want on a dashboard before classification.

---

## #device-type-profiles

### Device-type profiles

One lookup replaces six separate questions. Apply before generating any
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

## #wall-panel-hardening

### Wall-panel & kiosk hardening — advisory notes

These points are advisory and mostly outside YAML generation scope — raise
them when a wall-panel or kiosk profile is selected, then let the user decide.

**Display protection:**
- OLED / AMOLED panels: prefer a dark single-mode theme and avoid static
  high-contrast elements that never move (large white chip bars, permanent
  bright separators). LCD panels are far less burn-in prone.
- Schedule the screen off when the room is unoccupied — a device automation
  (via the companion app or Fully Kiosk) is the calm-tech answer and doubles
  as burn-in protection. Hand off the automation itself to ha-yaml.

**Kiosk behaviour:**
- Hiding the HA header and sidebar on a fixed display is usually done with
  the community `kiosk-mode` frontend module (HACS) or the kiosk settings of
  Fully Kiosk Browser on Android panels. Both are outside this skill's YAML
  scope — name them, don't configure them.
- Use a dedicated non-admin HA user for the panel: it prevents accidental
  edits and limits what a guest can reach from the device.

**Reliability:**
- After HA updates, wall panels are the devices most likely to show stale
  cached frontend code — a scheduled nightly browser restart (Fully Kiosk
  supports this) avoids most of it. Symptoms and fixes:
  `troubleshooting-ref.md#cache-issues`.
- Motion-sensitivity rules for always-on displays (no long animations, no
  `rise_animation`) are in SKILL.md §2 Accessibility and apply here in full.

---

## #sections-anatomy

### Sections view anatomy

Sections view (default since HA 2024.3) is the required view type for all
new dashboards.

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
Set `column_span` on the *section*, not the card:
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

## #multi-view-design

### Multi-view dashboard design

The 5-view system is the recommended structure. Split to additional views only
when a specific domain needs its own canvas.

A single view with pop-ups is valid for simple homes or when the user
explicitly wants a minimal single-view dashboard.

**When to add a view beyond the 5-view system:**
- More than 8–10 room buttons in the Rooms view (split into zones)
- A domain needs always-visible display that doesn't fit Overview (security cameras)
- Different user groups need completely different primary views (family vs admin)

**Linking views from the HBS footer:**
```yaml
1_name: Overview
1_icon: mdi:home-variant
1_link: /lovelace/overview
# Note: no 1_pir_sensor — views are not room-based, no auto_order
```

---

## #panel-view

### Panel view — for wall panels and kiosk dashboards

The `type: panel` view type forces a single card to fill the entire screen.

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
- Dashboards that need to work on both phone and desktop
- Any view containing pop-ups (positioning may shift)
# Dashboard Recipes Reference
# ha-bubble-dashboard skill
# View-by-view YAML for the 5-view system + 2 extension views.
# Read dashboard-system.md#classification-output to map entities to views before using these.
# All recipes use var() chains — no hardcoded colours.
# Replace placeholder entity IDs with real entities before delivering.

---

## #masonry-migration

### Masonry → sections migration guide

For users with an old masonry dashboard (the pre-2024 default, or any view
with no `type:` set) who want the sections layout this skill targets.

**Step 0 — don't convert in place.** Create a new view (`type: sections`) in
the same dashboard, migrate into it, verify, then delete the old view. The
old view stays functional throughout.

**Step 1 — take stock of the old view:**
- Pop-ups: any format — old stack-based pop-ups must also migrate to the
  v3.2+ standalone format (`bubble-card-ref.md#version-compat`).
- HBS footer: note its position — it moves to last top-level card.
- `vertical-stack` / `horizontal-stack` groupings — these become sections.
- Conditional cards — unchanged, they work identically in sections.

**Step 2 — mapping table:**

| Masonry construct | Sections equivalent |
|---|---|
| Implicit column flow | `type: grid` sections + `column_span` |
| `vertical-stack` group | One grid section containing the same cards |
| `horizontal-stack` (≤2 cards) | Cards side-by-side in a grid section |
| `horizontal-stack` (3+ cards) | Split — wrapping is unpredictable on mobile |
| Pop-up inside a stack | Standalone pop-up, top-level `cards:` entry |
| HBS anywhere | Last top-level `cards:` entry |
| `view_layout` options | Remove — replaced by `column_span` / `max_columns` |

**Step 3 — re-check `card_layout`.** In sections view, Bubble Cards default
to `large` — cards that looked right as `normal` in masonry may render
differently. Apply the card_layout decision guide (SKILL.md §4) per card
rather than carrying old values blindly.

**Step 4 — set `max_columns`** per the device-type profile, then verify with
the §8 pre-output checklist. Layout problems after migration:
`troubleshooting-ref.md#sections-layout-issues`.

---

## #native-interop

### Mixing native cards into a Bubble dashboard

Native HA cards (tile, heading, area, weather, media control) can sit inside
the same sections as Bubble Cards. This is often the right call when a native
tile feature covers the need — see `#native-first`.

**What inherits from the Casa5HeyneV2 theme automatically:** native cards
read the standard HA theme variables the theme already defines — card
background, `ha-card-border-radius`, primary/secondary text colours, the font
stack and the state colour tokens. A native tile dropped into a Bubble
dashboard picks up the palette and typography without any extra work.

**What does NOT apply to native cards:** `--bubble-*` variables, Bubble Card
modules, and Bubble `styles:` blocks. Do not attempt to restyle native cards
with Bubble mechanisms; if a native card needs adjustment beyond what the
theme provides, that is a signal to use the Bubble equivalent instead.

**When the native card is the better pick:**

- **Weather with forecast** — the weather tile's temperature / precipitation
  forecast features (HA 2026.6+) replace any custom forecast construction.
  Never rebuild a forecast with sub-buttons.
- **Media player with full transport** — media tile features (HA 2026.5/2026.6+)
  cover source, sound mode, mute and reorderable buttons. The Bubble
  media-player card remains the pick for pop-up contexts and visual
  consistency in room pop-ups; the tile wins for a dedicated media section.
- **Section anchors with status** — the native heading card supports badges
  and buttons with visibility conditions (HA 2026.2+); the Bubble separator
  remains the default inside pop-ups.

**Visual consistency rules:**

1. Group native cards in their own section rows rather than interleaving them
   card-by-card with Bubble Cards — shape language differs slightly (tile
   icon disc vs Bubble icon circle) and grouping keeps this deliberate.
2. Keep the engagement-type rule: a native tile with controls belongs on a
   brief-interaction surface, not on the Overview view.
3. All colour still comes from the theme — the Iron Law applies to native
   cards too. No hardcoded hex in native card YAML.

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

**Copy-paste YAML:** `recipes-5view.md#recipe-8-overview` — the single source
for this view's card YAML. Do not reconstruct it from this section.

**Component design notes:**

- **Chip bar** (full-width section) — weather, outdoor temperature, one chip
  per person, alarm state, a template chip counting lights on (amber when > 0),
  and optionally current power. Every chip is `tap_action: none` or `more-info`
  — never a control.
- **Alert strip** — conditionally visible via `input_boolean.home_alerts_active`,
  set to `on` by an automation when any alert condition is true (hand off to
  ha-yaml for the automation). Hidden entirely when all clear — the calmest
  alert is the one that isn't there.
- **Per-room status grid** — state-only cards, `tap_action: none`, one card per
  room. Sub-buttons show temperature and motion state. The room button's active
  state (accent colour) shows when lights are on — no interaction needed to
  read it.
- **Away mode panel** — conditionally visible when no `person` entity is
  `home`. The per-room grid is still rendered, but the away panel draws the
  eye first when visible. Shows security state and a lights summary
  (template sensor via ha-yaml — the recipe uses `binary_sensor.any_light_on`
  as the placeholder).

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

**Copy-paste YAML:** `recipes-5view.md#recipe-9-rooms` — the single source
for this view's card YAML (room buttons, pop-ups, and HBS footer). Do not
reconstruct it from this section.

**Component design notes:**

- One `card_layout: large` button per room, tap navigates to the room's
  pop-up hash. Pop-ups are top-level `cards:` entries — never inside sections.
- Room pop-up content follows Recipe 1 and the room-type patterns in
  `recipes-extended.md` (security, vacuum, bathroom, garage, office…).
- This is the only view where brief-interaction controls live — Overview
  stays passive, deep-engagement content goes to Activity/Settings.

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

**Copy-paste YAML:** `#view-scenes-scaffold` — the complete Scenes view scaffold is
a separate anchor so the design notes above can be read without loading it.

---

## #view-scenes-scaffold

### Scenes view — complete scaffold

Design rationale and helper requirements: `#view-scenes`.

**Complete Scenes view scaffold:**
```yaml
- title: Scenes
  path: scenes
  type: sections
  max_columns: 3
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

  cards:
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

**Copy-paste YAML:** `#view-activity-scaffold` — the complete Activity view scaffold is
a separate anchor so the design notes above can be read without loading it.

---

## #view-activity-scaffold

### Activity view — complete scaffold

Design rationale and helper requirements: `#view-activity`.

> **Graph card choice — ask, don't assume.** This scaffold is written with
> `custom:mini-graph-card`, but that is a placeholder, not a recommendation.
> Ask what the user already has installed and substitute per
> `graphs-ref.md#graph-decision`: the native `history-graph` needs no
> dependency at all, and if SGCC is already in the setup, use it in
> `sparkline: true` mode rather than adding a second graph dependency. Whatever is chosen, the graphs stay hidden
> behind the conditional until the event card is tapped: this view is
> deep-engagement content, not a wall of charts.

**Complete Activity view scaffold:**
```yaml
- title: Activity
  path: activity
  type: sections
  max_columns: 2
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

  cards:
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

  cards:
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

  cards:
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

    # HBS footer
    - type: custom:bubble-card
      card_type: horizontal-buttons-stack
      # ... (see #navigation-layer)
```

---

