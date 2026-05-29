# Sidebar Card Reference
# ha-bubble-dashboard skill — Phase 4b
# Source: Sidebar Card v0.1.9.9 README + community forum

---

## #known-issues

### Health status and known issues

> **Sidebar Card is maintenance-only as of v0.1.9.9.** No new features are
> planned. The core functionality (navigation menu, clock, date, template
> messages) is stable. Two known issues affect advanced usage:

| Issue | Severity | Workaround |
|-------|----------|------------|
| `bottomCard` fails intermittently on page refresh (`setConfig is not a function`) | Medium — affects all bottomCard users | Refresh page again; or avoid `bottomCard` for critical content. Use a Bubble Card sub-buttons footer instead. |
| `showTopMenuOnMobile` behaviour changed in HA 2026.1 following the mobile Home dashboard overhaul | Low–Medium | **Workaround:** set `hideHassSidebar: false` to keep the native HA sidebar visible, then use CSS to hide the native sidebar elements: add `app-header { display: none }` and `ha-sidebar { display: none }` to your theme's `extra_module_url` JS file. Test after each HA update. |

**Recommendation for "both equally" device targets:** implement Sidebar Card
for desktop only via `width: { mobile: 0, tablet: 0, desktop: 20 }`. The HBS
footer covers mobile navigation — do not rely on Sidebar Card on mobile.

---

## #installation

### Installation and resource setup

Sidebar Card is not in the default HACS catalogue. Add as a custom repository:

1. HACS → ⋮ → Custom repositories
2. URL: `https://github.com/DBuit/sidebar-card` → Category: Frontend → Add
3. Find "Sidebar Card" in HACS → Download
4. Add resource: Settings → Dashboards → ⋮ → Resources → Add:
   - URL: `/hacsfiles/sidebar-card/sidebar-card.js`
   - Type: JavaScript Module

### Configuration location

The sidebar configuration lives at the **root of the Lovelace dashboard YAML**,
at the same level as `resources:` and `views:`. It is **not a card** — it
wraps the entire dashboard.

```yaml
resources:
  - url: /hacsfiles/sidebar-card/sidebar-card.js
    type: module

sidebar:
  title: "My Home"
  # ... options below

views:
  - title: Home
    # ...
```

In UI-mode dashboards, add `sidebar:` in the raw configuration editor
(Dashboard → ⋮ → Edit dashboard → ⋮ → Raw configuration editor).

---

## #main-options

### All sidebar options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `title` | string | — | Title displayed at the top of the sidebar |
| `clock` | boolean | false | Show analog clock |
| `digitalClock` | boolean | false | Show digital clock |
| `digitalClockWithSeconds` | boolean | false | Show seconds on digital clock |
| `twelveHourVersion` | boolean | false | 12-hour format for digital clock |
| `period` | boolean | false | Show AM/PM (requires `twelveHourVersion`) |
| `date` | boolean | false | Show current date |
| `dateFormat` | string | `DD MMMM` | Date format (moment.js syntax) |
| `sidebarMenu` | object | — | Navigation menu items — see `#sidebar-menu` |
| `updateMenu` | boolean | true | Update active state when navigating |
| `template` | template | — | Jinja2 template for dynamic messages — see `#template-messages` |
| `style` | css | — | CSS overrides for sidebar colours — see `#style` |
| `width` | object | — | Width per breakpoint — see `#width-breakpoints` |
| `breakpoints` | object | — | Override breakpoint sizes |
| `bottomCard` | object | — | Card rendered at the bottom — see `#bottom-card` |
| `showTopMenuOnMobile` | boolean | false | Show HA top menu on mobile |
| `hideHassSidebar` | boolean | false | Hide the HA native left sidebar |
| `hideTopMenu` | boolean | false | Hide the HA top menu bar |
| `hideOnPath` | array | — | Paths where sidebar is hidden, e.g. `/lovelace/camera` |
| `debug` | boolean | false | Log debug messages to browser console |

**Override disable:** Append `?sidebarOff` to any URL to temporarily disable
the sidebar (useful for debugging): `http://homeassistant.local:8123/lovelace/home?sidebarOff`

---

## #width-breakpoints

### Width and breakpoints

```yaml
sidebar:
  width:
    mobile: 0        # hidden on mobile (0 = not shown)
    tablet: 0        # hidden on tablet
    desktop: 20      # 20% width on desktop

  # Optional — override the breakpoint thresholds (px)
  breakpoints:
    mobile: 768      # ≤ 768px = mobile
    tablet: 1024     # ≤ 1024px = tablet, > 1024px = desktop
```

**"Both equally" pattern — desktop only:**
```yaml
sidebar:
  width:
    mobile: 0
    tablet: 0
    desktop: 20
  hideHassSidebar: true
  showTopMenuOnMobile: true
```

---

## #sidebar-menu

### sidebarMenu — navigation items

```yaml
sidebar:
  sidebarMenu:
    - action: navigate
      navigation_path: "/lovelace/home"
      name: "Home"
      icon: mdi:home
      active: true               # marks this item as active on load
    - action: navigate
      navigation_path: "/lovelace/lights"
      name: "Lights"
      icon: mdi:lightbulb
    - action: navigate
      navigation_path: "/lovelace/climate"
      name: "Climate"
      icon: mdi:thermometer
    - action: toggle
      entity: switch.away_mode
      name: Away Mode
      icon: mdi:bag-suitcase
      state: switch.away_mode    # entity whose state colours the icon
    - action: call-service
      service: script.goodnight
      icon: mdi:weather-night
      name: Goodnight
```

**Menu item options:**

| Option | Type | Description |
|--------|------|-------------|
| `action` | string | `navigate` / `toggle` / `call-service` / `more-info` / `url` / `none` |
| `navigation_path` | string | Path for `navigate` action (e.g. `/lovelace/home`) |
| `url_path` | string | URL for `url` action — opens in new tab |
| `entity` | string | Entity for `toggle` or `more-info` |
| `service` | string | Service for `call-service` (e.g. `script.turn_on`) |
| `service_data` | object | Service data payload |
| `name` | string | Menu item label |
| `icon` | string | MDI icon |
| `state` | string | Entity whose state drives the icon on/off colour |
| `active` | boolean | Mark item as active on initial load |

**Active state:** When using `action: navigate` with Lovelace view paths, the
sidebar automatically highlights the active item based on the current URL.
No manual `active:` needed unless you want to pre-select an item on first load.

---

## #template-messages

### Jinja2 template messages

The `template:` option renders a list of `<li>` items using HA Jinja2 templates.
Each item must start with `<li>` and end with `</li>`.

```yaml
sidebar:
  template: |
    <li>
      {% if now().hour < 5 %} Good night 🌙
      {% elif now().hour < 12 %} Good morning ☕
      {% elif now().hour < 18 %} Good afternoon 👋
      {% else %} Good evening 👋{% endif %}
    </li>
    {% if states('sensor.bin_collection') == 'today' %}
    <li>🗑️ Bin collection today</li>
    {% endif %}
    {% set lights_on = states('sensor.lights_on_count') | int(0) %}
    {% if lights_on > 0 %}
    <li>💡 {{ lights_on }} light{{ 's' if lights_on > 1 }} on</li>
    {% endif %}
    {% if states('person.alice') == 'not_home' %}
    <li>🚗 Alice is away</li>
    {% endif %}
```

**Template tips:**
- Use `states('sensor.X')` for entity state values
- Use `state_attr('entity_id', 'attribute')` for attributes
- Avoid complex calculations — keep templates lightweight
- Unicode emoji work directly in template strings

---

## #style

### CSS style overrides

```yaml
sidebar:
  style: |
    :host {
      --sidebar-background: var(--background-color);
      --sidebar-text-color: var(--text-color);
      --face-color: var(--ha-card-background);
      --face-border-color: var(--ha-card-background);
      --clock-hands-color: var(--text-color);
      --clock-seconds-hand-color: var(--accent-color);
      --clock-middle-background: var(--ha-card-background);
      --clock-middle-border: var(--text-color);
    }
```

**Always use `var(--theme-variable)` references** in sidebar styles — never
hardcode hex values. This ensures the sidebar inherits light/dark mode changes
from the Casa5HeyneV2 theme automatically.

---

## #bottom-card

### bottomCard — card at the bottom of the sidebar

> **Warning:** `bottomCard` has a known intermittent bug where it fails to
> render on page refresh (`setConfig is not a function`). Use it for
> non-critical supplementary content only.

```yaml
sidebar:
  bottomCard:
    type: custom:bubble-card
    cardOptions:
      card_type: button
      button_type: state
      entity: weather.home
      name: Weather
      show_state: true
      card_layout: large
    cardStyle: |
      :host {
        width: 100%;
        background: transparent;
        padding: 8px;
      }
```

**bottomCard options:**

| Option | Description |
|--------|-------------|
| `type` | Any HA card type or custom card type |
| `cardOptions` | Card configuration (same as YAML card config) |
| `cardStyle` | CSS applied to the card host element |

**Alternative to bottomCard (more reliable):**
Use a Bubble Card `sub-buttons` card with `footer_mode: true` at the bottom
of the view instead. It avoids the `setConfig` bug and integrates better
with the Bubble Card styling system.

---

## #combined-example

### Complete sidebar configuration — "both equally" pattern

```yaml
sidebar:
  title: "My Home"
  digitalClock: true
  twelveHourVersion: false
  date: true
  dateFormat: "dddd, D MMMM"
  hideHassSidebar: true
  hideTopMenu: true
  showTopMenuOnMobile: true

  width:
    mobile: 0
    tablet: 0
    desktop: 22

  breakpoints:
    mobile: 768
    tablet: 1024

  sidebarMenu:
    - action: navigate
      navigation_path: "/lovelace/home"
      name: "Home"
      icon: mdi:home
    - action: navigate
      navigation_path: "/lovelace/rooms"
      name: "Rooms"
      icon: mdi:floor-plan
    - action: navigate
      navigation_path: "/lovelace/energy"
      name: "Energy"
      icon: mdi:lightning-bolt
    - action: navigate
      navigation_path: "/lovelace/settings"
      name: "Settings"
      icon: mdi:cog

  template: |
    <li>
      {% if now().hour < 12 %}Good morning{% elif now().hour < 18 %}Good afternoon{% else %}Good evening{% endif %}
    </li>
    {% set lights = states.light | selectattr('state','eq','on') | list | count %}
    {% if lights > 0 %}<li>{{ lights }} light{{ 's' if lights > 1 }} on</li>{% endif %}

  style: |
    :host {
      --sidebar-background: var(--background-color);
      --sidebar-text-color: var(--text-color);
      --clock-seconds-hand-color: var(--accent-color);
    }
```
