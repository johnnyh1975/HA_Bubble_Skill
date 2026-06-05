# Health-Check Mode

**Trigger:** user pastes existing dashboard YAML and asks for a review, audit,
or says "what's wrong with my dashboard", "health check", "improve this",
"review my YAML", or similar.
**Do not trigger** for new dashboard generation — use §2#full-dashboard-workflow.

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
