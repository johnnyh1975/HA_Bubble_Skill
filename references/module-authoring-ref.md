# Module Authoring Reference
# ha-bubble-dashboard skill
# Covers: full Bubble Card module editor-schema field catalog, the object
#         selector's groups/conditional-fields/variants (v3.2.4), grid and
#         expandable layout, and the module-sharing/export format.
# Source: Bubble Card v3.2.4 — src/modules/editor-schema-docs.md,
#         src/modules/export.js, src/modules/utils.js, src/modules/parser.js
# For the quick-start module structure and when to use a module vs `styles:`,
# see bubble-card-ref.md#module-authoring first. Read this file only when
# writing a module's `editor:` schema, or packaging a module for sharing.

---

## #basic-structure

A module's `editor:` key is an array of form-field objects, each rendered as
one control in the Module Editor. This is entirely separate from the module's
`code:` block — `editor:` only builds the configuration *form*; the field
values are then read back inside `code:` via `this.config.<module_id>?.<field_name>`
(see bubble-card-ref.md#module-authoring for that access pattern). There is no
`variables:` key and no `{{mustache}}` interpolation anywhere in Bubble Card.

```yaml
editor:
  - name: color
    label: "Color"
    selector:
      select:
        options:
          - label: "Red"
            value: "red"
          - label: "Blue"
            value: "blue"
  - name: icon_size
    label: "Icon Size"
    selector:
      number:
        min: 20
        max: 50
        unit_of_measurement: "px"
```

---

## #field-properties

Every field, of any type, supports:

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | **Required.** The key under which the value is stored (`this.config.<module_id>?.<name>`). |
| `label` | string | Displayed field name. |
| `required` | boolean | Whether the field must be filled in. |
| `disabled` | boolean | Whether the field is disabled. |
| `default` | any | Default value if unset. |

---

## #field-types

Prefer **selector-based fields** (`selector:` key) — they render Home
Assistant's native rich controls. **Legacy type-based fields** (`type:` key)
still work but are plainer; only use them for a quick one-off.

### Basic input

```yaml
- name: title
  label: "Title"
  selector:
    text: {}
      # multiline: boolean | type: "email"/"url"/"password" | autocomplete: string
      # prefix: string | suffix: string

- name: opacity
  label: "Opacity"
  selector:
    number:
      min: 0
      max: 100
      step: 5
      unit_of_measurement: "%"
      mode: slider            # "box" or "slider" (default: slider)
      min_step: 1

- name: show_icon
  label: "Show Icon"
  selector:
    boolean: {}              # no options

- name: theme
  label: "Theme"
  selector:
    select:
      options:
        - label: "Light"
          value: "light"
        - label: "Dark"
          value: "dark"
      multiple: false        # allow multi-select
      custom_value: false    # allow free-text values too
      mode: dropdown          # "dropdown" or "list"
      # translation_key: string

- name: background_color
  label: "Background Color"
  selector:
    ui_color:
      # default_color: string | include_none: boolean | include_state: boolean

- name: custom_icon
  label: "Custom Icon"
  selector:
    icon: {}                 # no options
```

### Home Assistant references

```yaml
- name: target_entity
  selector:
    entity:
      filter: { domain: light }        # domain, device_class, integration, supported_features
      # include_entities / exclude_entities: string[] | multiple: boolean

- name: device
  selector:
    device:
      filter: { integration: zwave }   # integration, manufacturer, model
      # entity.domain / entity.device_class | multiple: boolean

- name: area
  selector:
    area: {}                # entity.domain/device_class, device.integration/manufacturer/model, multiple

- name: card_theme
  selector:
    theme: {}                # include_default: boolean

- name: labels
  selector:
    label: { multiple: true }

- name: floor
  selector:
    floor: {}

- name: dashboard
  selector:
    dashboard: { include_dashboards: ["lovelace"] }

- name: config_entry
  selector:
    config_entry: { domain: zwave_js }

- name: addon
  selector:
    addon: {}                # name: string filter
```

### Date & time

```yaml
- name: start_time
  selector: { time: {} }

- name: event_date
  selector:
    date: {}                 # min/max: ISO date string

- name: event_datetime
  selector:
    datetime: {}              # min/max: ISO datetime string

- name: timeout
  selector:
    duration: { enable_day: false }

- name: schedule
  selector: { schedule: {} }
```

### Advanced

```yaml
# Complex entity-state/time/numeric conditions — see #condition-selector below
- name: conditions
  selector: { condition: {} }

- name: tap_action
  selector:
    action:
      actions: ["more-info", "toggle", "call-service", "navigate", "url", "none"]

- name: target
  selector:
    target:
      entity: { domain: light }   # same shape as entity/device/area selectors

- name: template
  selector: { template: {} }

- name: media
  selector:
    media:
      filter_media_source: true
      filter_local_media: true

- name: attribute            # only works alongside an entity selector at the same level
  selector:
    attribute:
      entity_id: string        # required
      # hide_attributes: string[]

- name: target_state          # only works alongside an entity selector at the same level
  selector:
    state:
      entity_id: string        # required
      # attribute: string — select from an attribute instead of state

- name: config_file
  selector: { file: { accept: ".yaml,.json" } }

- name: qr_data
  selector: { qr_code: {} }

- name: agent
  selector: { conversation_agent: {} }

- name: backup
  selector: { backup: { integration: google_assistant } }

- name: assistance_pipeline
  selector: { assistance: {} }

- name: location
  selector:
    location: { radius: true, icon: "mdi:home" }
```

### #condition-selector

Lets a module define complex show/hide logic (entity state, numeric, time...).
Evaluate it at runtime in `code:` with `checkConditionsMet` (one of the JS
template functions always available, alongside `hass`, `entity`, `state`,
`icon`, `card`, `name`):

```yaml
# Module configuration example
my_module:
  element_to_show:
    condition:
      - condition: state
        entity_id: light.living_room
        state: 'on'
      - condition: numeric_state
        entity_id: sensor.temperature
        above: 20
```
```js
// In module code
const elementConfig = this.config.my_module?.element_to_show;
if (!elementConfig?.condition || checkConditionsMet([].concat(elementConfig.condition), hass)) {
  // Show element when living room light is ON and temperature is above 20
}
```

### #object-selector

The richest field type — captures a structured object, or (with `multiple: true`)
a reorderable list of objects, each defined by its own set of sub-fields (any
selector type, nested). `label_field` / `description_field` control what each
list-item row displays.

```yaml
- name: items
  label: "Items"
  selector:
    object:
      fields:
        name:
          label: "Name"
          selector: { text: {} }
        icon:
          label: "Icon"
          selector: { icon: {} }
      label_field: name
      description_field: icon
      multiple: true
```

**v3.2.4 additions — groups, conditional fields, and variants** (all UI-only;
the stored configuration always stays flat):

| Option | Description |
|--------|-------------|
| `fields.*.group` | Renders the field inside a collapsible section titled with this string. Fields sharing a `group` land in the same section. Adding a `group` to an existing module is fully backward compatible — it changes rendering only. |
| `fields.*.group_icon` | Optional MDI icon for the group's section header. |
| `fields.*.visible_if` | JS expression evaluated against the item's current data as `item`, the live `hass`, and the card's config as `card` (e.g. `item.target === 'card'`). `hass` and `card` can be `undefined` on early renders — guard them (`card && card.entity`). Field only renders while truthy. Re-evaluated live. Broken expressions fail **open** (field stays visible). |
| `fields.*.warn_if` | Same-shaped JS expression as `visible_if`. While truthy, shows `warn_text` as an amber alert above the field (e.g. warn about a missing entity). Broken expressions fail **silent** (no warning shown). |
| `fields.*.warn_text` | The warning message shown while `warn_if` is truthy. |
| `fields.*.default` | For text-based sub-fields, shown as input placeholder. For single-select dropdowns, shown as the selected value while unset — display only, doesn't write a value. |
| `fields.*.variant_of` | Marks this field as an alternate representation of the named base field (e.g. a static color vs. a state→color map vs. a JS expression). The family collapses into one mode dropdown plus only the active variant's input. Stored values keep their own keys. |
| `fields.*.variant` | Display label for this variant in the mode dropdown (defaults to the field key). On the *base* field, renames the base mode's label instead (default `"Static"`). |
| `fields.*.cluster_of` | Groups this field visually inside the named base field's box (same visual style as variants) without collapsing into a mode dropdown — for fields that are one logical unit (e.g. a mode select plus its parameters). Every member stays a real, independently stored field with its own `visible_if`. Composes with variants (cluster members append after variant rows). |
| `label_field` | Property key used as each item's label. |
| `description_field` | Property key (or list of keys, first-with-a-value wins) used as each item's secondary text. |
| `multiple` | If `true`, the field stores a list of objects instead of one. |

```yaml
- name: badges
  label: "Badges"
  selector:
    object:
      fields:
        name:
          label: "Name"
          selector: { text: {} }
        background_color:
          label: "Background color"
          group: "Appearance"
          group_icon: "mdi:palette"
          selector: { ui_color: {} }
        text_color:
          label: "Text color"
          group: "Appearance"
          selector: { ui_color: {} }
        mode:
          label: "Color mode"
          selector:
            select:
              options: [{ label: Static, value: static }, { label: "State map", value: state_map }]
        color_static:
          label: "Color"
          variant_of: mode
          variant: Static
          selector: { ui_color: {} }
        color_state_map:
          label: "State → color map"
          variant_of: mode
          variant: "State map"
          selector: { object: { fields: { state: { selector: { text: {} } }, color: { selector: { ui_color: {} } } }, multiple: true } }
      multiple: true
```

*Rule of thumb: `variant_of` when only one of the alternatives should ever be
stored/active at a time; `cluster_of` when several real fields should visually
group but all stay independently active.*

---

## #advanced-structure

### Grid layout

```yaml
- type: grid
  name: appearance
  column_min_width: "200px"   # optional
  schema:
    - name: color
      selector: { select: { options: [{label: Red, value: red}, {label: Blue, value: blue}] } }
    - name: size
      selector: { number: { min: 10, max: 100 } }
```

### Expandable sections

```yaml
- type: expandable
  name: advanced_settings
  title: "Advanced Settings"
  icon: "mdi:tune"
  expanded: false
  schema:
    - name: animation_speed
      selector: { number: { min: 1, max: 10 } }
```

---

## #legacy-fields

Still supported, but prefer selector-based fields above for a richer UI:

```yaml
- { name: title, label: "Title", type: string }
- { name: count, label: "Count", type: integer, valueMin: 0, valueMax: 100 }
- { name: opacity, label: "Opacity", type: float }
- { name: enabled, label: "Enabled", type: boolean }
- name: mode
  type: select
  options: [["auto", "Automatic"], ["manual", "Manual"]]
- name: features
  type: multi_select
  options: [["animations", "Animations"], ["colors", "Custom Colors"]]
```

---

## #best-practices

1. Only expose fields the user actually needs to configure — every extra
   field is a decision the module's user has to make.
2. Labels should be short and descriptive, not restate the field name.
3. Provide `default`s where a sensible one exists.
4. Group related fields with `grid`/`expandable`/the object selector's `group`
   rather than a long flat list.
5. Use `description` (on the module itself, not the field) for anything that
   needs more explanation than a label allows.
6. Test the rendered form before sharing — some selector types are less
   battle-tested inside Bubble Card's Module Editor than others; if one
   misbehaves, fall back to a simpler selector or a legacy field.

---

## #complete-example

```yaml
icon_badge_set:
  name: "Icon Badge Set"
  version: "1.1"
  creator: "YourName"
  description: |
    Adds a configurable set of small badges around the card's main icon.
  editor:
    - name: color_mode
      label: "Color Mode"
      selector:
        select:
          options:
            - { label: "Custom Color", value: custom }
            - { label: "Theme Color", value: theme }
    - name: custom_color
      label: "Custom Color"
      selector: { ui_color: {} }
    - type: expandable
      title: "Advanced Settings"
      expanded: false
      schema:
        - name: animation
          label: "Animation"
          selector: { boolean: {} }
        - name: animation_speed
          label: "Animation Speed"
          selector: { number: { min: 1, max: 10, step: 0.1 } }
        - name: opacity
          label: "Opacity"
          selector: { number: { min: 0, max: 100, unit_of_measurement: "%" } }
  code: |
    .bubble-icon-container {
      opacity: ${(this.config.icon_badge_set?.opacity ?? 100) / 100} !important;
      ${this.config.icon_badge_set?.animation ? `animation: bubble-badge-pulse ${(2 / (this.config.icon_badge_set?.animation_speed || 5)).toFixed(2)}s ease-in-out infinite;` : ''}
    }
```

---

## #sharing-a-module

### Paid / Patreon modules — boundary rule

A growing set of official Bubble Card modules (Bubble Badges 2, Bubble
Weather, Custom Dropdown, Bubble Neon, Bubble Calendar Enhanced…) is
distributed through the developer's Patreon. When a user asks to recreate
one of these:

- **Never reproduce or approximate the paid module's code** — not from
  memory, not from user-pasted excerpts.
- Do explain what the module does and route the user to the Module Store /
  Patreon for the original.
- Offer the legitimate alternative: author an original module for the user's
  specific need using this reference — a from-scratch module solving their
  concrete problem is in scope; a clone of a paid product is not.


Bubble Card's Module Editor can export a module two ways. When a user asks
Claude to "package this module to share" or "write the GitHub post for my
module", produce output matching these exact formats — they're generated by
Bubble Card itself (`generateYamlExport` / `generateGitHubExport`), and the
Module Store expects them.

**Plain YAML export** (what "Download as YAML" produces) — just the clean
module object, keys in this order: `name, version, creator, link, supported,
description, code, editor`, plus `is_global` only if `true`. Omit `supported`
entirely if the module applies to every card type, omit `link` if empty.

```yaml
icon_badge_set:
  name: "Icon Badge Set"
  version: "1.1"
  creator: "YourName"
  description: |
    Adds a configurable set of small badges around the card's main icon.
  code: |
    .bubble-icon-container { ... }
  editor:
    - name: color_mode
      ...
```

**GitHub Discussion export** (what "Copy for GitHub" produces, for posting to
the [Share your Modules](https://github.com/Clooos/Bubble-Card/discussions/categories/share-your-custom-styles-templates-and-dashboards)
category — this is how modules reach the in-editor Module Store):

````markdown
# {name}

**Version:** {version}
**Creator:** {creator}

> [!IMPORTANT]
> **Supported cards:**
>  - All cards are supported          <!-- or a bullet list of Title Case card names -->

{description}
Configure this module via the editor or in YAML, for example:

```yaml
{module_id}:
    {first_editor_field_name}: YOUR_VALUE
```

---

<details>

<summary><b>🧩 Get this Module</b></summary>

<br>

> To use this module, simply install it from the Module Store (from the editor of any card > Modules), or copy and paste the following configuration into a `/www/bubble/modules/{module_id}.yaml` file.

```yaml
{module_id}:
    name: "{name}"
    version: "{version}"
    creator: "{creator}"
    link: "https://github.com/Clooos/Bubble-Card/discussions/XXXX"

    supported:            <!-- omit this whole key if all cards are supported -->
        - button

    description: |
        {description, each line indented 8 spaces}
        <br><br>
        <code-block><pre>
        {module_id}: 
            {first_editor_field_name}: YOUR_VALUE
        </pre></code-block>

    code: |
        {code, each line indented 8 spaces}

    editor:
      {editor schema, dumped as YAML and indented 6 spaces}
```

</details>

---

### Screenshot:

Important: The first screenshot here will be used on the Module Store, so please provide one.
````

Notes on generating this:
- `supported` is omitted from both the inline example and the full YAML block
  whenever it's unset or covers every card type — never write out all card
  IDs by hand.
- The `link:` placeholder (`.../discussions/XXXX`) is intentional — the real
  discussion number doesn't exist until the user actually posts it. Tell the
  user to come back and fill it in after posting, if they ask.
- The inline config example always uses only the **first** `editor:` field's
  `name` as the example key — not every field. This matches Bubble Card's own
  generator; don't "improve" it by listing every field.
