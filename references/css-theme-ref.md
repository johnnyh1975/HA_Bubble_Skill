# CSS Theme Reference
# ha-bubble-dashboard skill — Phase 2
# Covers: Casa5HeyneV2 var() architecture, Bubble↔HA bridge,
#         full light/dark variable catalogue, accent-swap mechanics.

---

## #var-chain

### The Architecture Principle

The theme is built on a strict one-directional chain:

```
Bubble Card CSS variable
    │  points via var() to
    ▼
HA standard variable  (ha-card-background, primary-color, accent-color …)
    │  resolved from
    ▼
Concrete value in modes.light or modes.dark
```

**Rule: concrete hex/rgb values live ONLY in `modes.light` and `modes.dark`.**
The global (mode-independent) section and every `--bubble-*` mapping contain
only `var()` references — never raw colours. This is what makes light/dark
switching and accent swapping work with a 3–5 line theme diff.

### Why this matters for card YAML

When you write a Bubble Card, you must NEVER set a colour directly:

```yaml
# WRONG — breaks light/dark, breaks accent swap
styles: |
  ha-card { --bubble-main-background-color: #FFFFFF; }

# CORRECT — flows through the chain automatically
# (no styles: override needed — the theme handles it)
```

If you need a card-level colour override, always reference a theme variable:

```yaml
styles: |
  ha-card { --bubble-accent-color: var(--primary-color); }
```

---

## #bubble-vars

### Global Bubble Card mappings (mode-independent)

These are set once at the top level of the theme and resolve automatically
in both light and dark mode via the HA variables they point to.

| Bubble variable | Maps to | Effect |
|-----------------|---------|--------|
| `--bubble-main-background-color` | `var(--ha-card-background, var(--card-background-color, #fff))` | Card body background |
| `--bubble-secondary-background-color` | `transparent` | Secondary surfaces (e.g. sub-button area) |
| `--bubble-pop-up-main-background-color` | `var(--ha-card-background, var(--card-background-color))` | Pop-up body background |
| `--bubble-border` | `var(--ha-card-border-width, 1px) solid var(--ha-card-border-color, var(--divider-color))` | Full border shorthand — width + style + colour |
| `--bubble-border-radius` | `var(--ha-card-border-radius, 16px)` | Corner radius for all cards |
| `--bubble-button-border-radius` | `var(--bubble-border-radius)` | Button inherits card radius |
| `--bubble-icon-border-radius` | `32px` | Icon container — pill shape |
| `--bubble-pop-up-border-radius` | `calc(var(--ha-card-border-radius, 16px) * 1.4)` | Slightly larger than card radius |
| `--bubble-accent-color` | `var(--primary-color)` | → `var(--accent-color)` — the single colour lever |
| `--bubble-default-color` | `var(--primary-color)` | Alias of accent for legacy use |
| `--bubble-button-accent-color` | `var(--accent-color-background-opacity)` | 25% opacity accent for active button bg |
| `--bubble-icon-background-color` | `var(--state-inactive-color)` | Icon container bg when entity is off |
| `--bubble-climate-button-background-color` | `var(--bubble-icon-background-color)` | Climate mode buttons |
| `--bubble-select-list-background-color` | `var(--card-background-color)` | Dropdown list surface |
| `--bubble-list-item-accent-color` | `none` | Selected list item — no tint by default |

### Structural HA card variables (mode-independent)

These shape geometry and are not colour-sensitive:

| Variable | Value | Purpose |
|----------|-------|---------|
| `--ha-card-border-radius` | `16px` | Base radius — Bubble inherits via var() |
| `--ha-card-border-width` | `1px` | Border thickness |
| `--ha-card-backdrop-filter` | `none` | No blur effect by default |
| `--mdc-shape-small` | `8px` | MDC chip / input radius |
| `--mdc-shape-medium` | `12px` | MDC dialog / menu radius |
| `--mdc-icon-size` | `22px` | Global icon size |

---

## #ha-vars

### The accent lever — how one colour controls everything

Setting `accent-color` in each mode is the single most powerful change you
can make. Follow the chain to see every element it controls:

```
accent-color: "#D9BE8B"          ← SET THIS to change the whole palette
    │
    ├─→ primary-color: var(--accent-color)
    │       └─→ bubble-accent-color: var(--primary-color)
    │               └─→ HBS active button background
    │               └─→ Slider fill colour
    │               └─→ Active icon tint
    │
    ├─→ state-active-color: var(--accent-color)
    │       └─→ Button background when entity is ON
    │
    ├─→ accent-color-background-opacity: rgba(R,G,B, 0.25)   ← ALSO UPDATE
    │       └─→ bubble-button-accent-color (active bg overlay)
    │
    ├─→ accent-medium-color: rgba(R,G,B, 0.5)                ← ALSO UPDATE
    │       └─→ Switch unchecked button (light mode)
    │       └─→ Slider secondary colour
    │
    ├─→ ha-color-primary-* opacity scale                     ← ALSO UPDATE
    │       └─→ ha-color-primary-30 (0.85 opacity)
    │       └─→ ha-color-primary-80 (0.35 opacity)
    │       └─→ ha-color-primary-90 (0.25 opacity)
    │       └─→ ha-color-primary-95 (0.15 opacity)
    │
    ├─→ mdc-theme-primary: var(--accent-color)
    │       └─→ Toggle switches, radio buttons, focus rings
    │
    ├─→ mdc-ripple-color: rgba(R,G,B, 0.20)                  ← ALSO UPDATE
    │       └─→ Touch ripple on interactive elements
    │
    └─→ sidebar-selected-icon-color: var(--accent-color)
            └─→ Active nav item in both Sidebar Card and HA sidebar
```

**Minimum set of lines to update for an accent swap (per mode):**

```yaml
accent-color:                    "#NEWHEX"
accent-color-background-opacity: "rgba(NR,NG,NB, 0.25)"
accent-medium-color:             "rgba(NR,NG,NB, 0.5)"
ha-color-primary-30:             "rgba(NR,NG,NB, 0.85)"
ha-color-primary-80:             "rgba(NR,NG,NB, 0.35)"
ha-color-primary-90:             "rgba(NR,NG,NB, 0.25)"
ha-color-primary-95:             "rgba(NR,NG,NB, 0.15)"
mdc-ripple-color:                "rgba(NR,NG,NB, 0.20)"
```

For a full palette swap (backgrounds + text + accent), see `#full-palette-swap`.

---

## #light-mode

### Complete light mode variable catalogue

**Text**

| Variable | Value | Contrast on #FFF | Role |
|----------|-------|-----------------|------|
| `text-color` | `#555A60` | 7.0:1 ✓ AAA | Primary body text |
| `primary-text-color` | `var(--text-color)` | — | Alias |
| `secondary-text-color` | `rgba(37,43,56,0.3)` | ~3.5:1 | Subdued labels |
| `primary-text-color--half-opacity` | `rgba(85,90,96,0.5)` | ~3.0:1 | Icon colour in inactive state |
| `primary-text-color--light` | `#d7d8d9` | 1.2:1 | Decorative only — never body text |
| `text-medium-color` | `#80828A` | 4.6:1 ✓ AA | Mid-emphasis text |
| `disabled-text-color` | `#626569` | 5.9:1 ✓ AA | Disabled / unavailable |

**Accent & state**

| Variable | Value | Note |
|----------|-------|------|
| `accent-color` | `#D9BE8B` | Warm gold. 1.9:1 on white — decorative only, not text |
| `primary-color` | `var(--accent-color)` | HA primary = accent |
| `warning-color` | `#FA7575` | Fixed — do not change with accent swap |
| `state-active-color` | `var(--accent-color)` | Entity ON background tint |
| `state-inactive-color` | `rgba(0,0,0,0.08)` | Icon bg when OFF |
| `accent-color-background-opacity` | `rgba(217,190,139,0.25)` | 25% accent overlay |
| `accent-medium-color` | `rgba(217,190,139,0.5)` | 50% accent |

**Backgrounds**

| Variable | Value | Role |
|----------|-------|------|
| `background-color` | `#F8F8F8` | Lovelace page background |
| `ha-card-background` | `#FFFFFF` | Card surface → `--bubble-main-background-color` |
| `card-background-color` | `#FFFFFF` | Alias used by dropdowns |
| `secondary-background-color` | `rgb(230,230,230)` | Slightly darker surface |
| `background-color-2` | `#E8E8E8` | Slider track, switch track |

**Borders & shadows**

| Variable | Value | Note |
|----------|-------|------|
| `divider-color` | `rgba(0,0,0,0.08)` | Fallback in `--bubble-border` |
| `ha-card-border-color` | `rgba(0,0,0,0.06)` | Subtle card outline |
| `ha-card-box-shadow` | `0px 0px 0px 0px rgba(0,0,0,0)` | No shadow by default |

**Sidebar**

| Variable | Value |
|----------|-------|
| `sidebar-background-color` | `#F8F8F8` |
| `sidebar-icon-color` | `rgb(95,99,104)` |
| `sidebar-selected-icon-color` | `var(--accent-color)` |
| `sidebar-selected-text-color` | `var(--sidebar-selected-icon-color)` |
| `sidebar-selected-bg` | `var(--accent-color)` |

**More-info dialog**

| Variable | Value |
|----------|-------|
| `more-info-header-background` | `#f0ece3` — warm tint matching gold accent |
| `paper-dialog-background-color` | `var(--card-background-color)` |

---

## #dark-mode

### Complete dark mode variable catalogue

**Text**

| Variable | Value | Contrast on #252B38 | Role |
|----------|-------|---------------------|------|
| `text-color` | `#FFFFFF` | 13.5:1 ✓ AAA | Primary body text |
| `secondary-text-color` | `#818793` (via `--primary-text-color--light`) | 4.9:1 ✓ AA | Subdued labels |
| `primary-text-color--half-opacity` | `rgba(255,255,255,0.5)` | ~4.5:1 | Icon colour inactive |
| `text-medium-color` | `#80828A` | 3.8:1 ✓ AA large | Mid-emphasis |
| `disabled-text-color` | `#626569` | 2.7:1 — large text only | Unavailable |

**Accent & state**

| Variable | Value | Note |
|----------|-------|------|
| `accent-color` | `#D9BE8B` | Same gold in dark — 3.0:1 on #252B38 ✓ UI components |
| `primary-color` | `var(--accent-color)` | |
| `warning-color` | `#FA7575` | Fixed |
| `state-active-color` | `var(--accent-color)` | |
| `state-inactive-color` | `rgba(255,255,255,0.10)` | Lighter inactive bg for dark |
| `accent-color-background-opacity` | `rgba(217,190,139,0.25)` | |
| `accent-medium-color` | `var(--accent-color)` | Full opacity in dark (not 50%) |

**Backgrounds**

| Variable | Value | Role |
|----------|-------|------|
| `background-color` | `#202631` | Page background |
| `ha-card-background` | `#252B38` | Card surface — blue-shifted dark |
| `card-background-color` | `var(--ha-card-background)` | |
| `background-color-2` | `#3a3c55` | Slider/switch track |
| `secondary-background-color` | `var(--background-color)` | Same as page in dark |

**Borders**

| Variable | Value |
|----------|-------|
| `divider-color` | `var(--ha-card-background)` — card colour as divider |
| `ha-card-border-color` | `#2D3341` |
| `ha-card-box-shadow` | `0px 0px 0px 0px rgba(0,0,0,0)` |

**More-info dialog**

| Variable | Value |
|----------|-------|
| `more-info-header-background` | `#132c41` — deep blue |
| `paper-dialog-background-color` | `#132c41` |

---

## #how-to-swap-accent

### Accent-only swap (safest — 8 lines per mode)

Replace the gold `#D9BE8B` with a new colour. Update only the lines in the
accent lever chain. Everything else (backgrounds, text, borders) stays the same.

**Template — paste into both `modes.light` and `modes.dark`, adjusting values:**

```yaml
# Replace NEWHEX and NR,NG,NB with your chosen colour
accent-color:                    "NEWHEX"
accent-color-background-opacity: "rgba(NR,NG,NB, 0.25)"
accent-medium-color:             "rgba(NR,NG,NB, 0.5)"   # light mode
# accent-medium-color:           "NEWHEX"                 # dark mode (full opacity)
ha-color-primary-30:             "rgba(NR,NG,NB, 0.85)"
ha-color-primary-40:             "NEWHEX"
ha-color-primary-80:             "rgba(NR,NG,NB, 0.35)"
ha-color-primary-90:             "rgba(NR,NG,NB, 0.25)"
ha-color-primary-95:             "rgba(NR,NG,NB, 0.15)"
mdc-ripple-color:                "rgba(NR,NG,NB, 0.20)"
```

**Also update in the mode-independent block (ZONE 6 — Mushroom sync):**

```yaml
# One additional line to keep Mushroom in sync with the new accent
accent-color-rgb: "NR, NG, NB"   # same R,G,B as above — format: bare integers
# mush-rgb-primary automatically follows via var(--accent-color-rgb)
```

Without this line, Bubble Card active states will shift to the new accent
but Mushroom switches and entity cards will not.

**WCAG check before committing any accent:**

| Pair to check | Required ratio | Formula |
|---------------|---------------|---------|
| Accent on light card (#FFFFFF) | ≥ 3:1 for UI components | Luminance check |
| Accent on dark card (#252B38) | ≥ 3:1 for UI components | Luminance check |
| Accent on light bg (#F8F8F8) | ≥ 3:1 for UI components | |
| Text (#555A60) on accent bg | ≥ 4.5:1 if text appears on accent surface | |

The gold `#D9BE8B` is 1.9:1 on white — it fails even the 3:1 UI component
threshold on light backgrounds. It is used purely as a tint/overlay colour,
never as a standalone UI element. Any replacement accent must achieve ≥ 3:1
on both the light (#FFFFFF) and dark (#252B38) card backgrounds to be usable
as an icon colour and slider fill.

Use `colour-intelligence-ref.md#wcag-checks` for pre-calculated ratios on
all six ready-made palette recipes.

---

## #full-palette-swap

### Full palette generation (backgrounds + text + accent)

A full swap changes all three zones: the accent lever, the background tones,
and optionally the text colours. The theme structure supports this cleanly
because concrete values are isolated in `modes.light` and `modes.dark`.

**Variables to change for a full palette (light mode):**

Zone 1 — accent lever (8 lines, see #how-to-swap-accent above)

Zone 2 — backgrounds (5 lines):
```yaml
background-color:           "NEW_PAGE_BG"     # e.g. #F5F0E8 for warm cream
ha-card-background:         "NEW_CARD_BG"     # e.g. #FFFDF7 for warm white
card-background-color:      "NEW_CARD_BG"     # must match ha-card-background
secondary-background-color: "NEW_SECONDARY"   # e.g. rgb(230,224,210)
background-color-2:         "NEW_TRACK"       # slider/switch track
```

Zone 3 — text (optional, only if backgrounds shift enough to affect contrast):
```yaml
text-color:                       "NEW_TEXT"   # verify ≥ 7:1 on NEW_CARD_BG
primary-text-color--half-opacity: "rgba(NR,NG,NB,0.5)"
secondary-text-color:             "rgba(NR,NG,NB,0.3)"
```

Zone 4 — sidebar (if sidebar background should match new page tone):
```yaml
sidebar-background-color:     "NEW_PAGE_BG"
app-header-background-color:  "NEW_PAGE_BG"
```

Zone 5 — dialog accent tint (light mode only):
```yaml
more-info-header-background:  "NEW_DIALOG_TINT"  # e.g. warm tint of new bg
```

**Full palette for dark mode — variables to change:**
```yaml
background-color:    "NEW_DARK_PAGE"    # e.g. #1A1F2B
ha-card-background:  "NEW_DARK_CARD"   # e.g. #20273A, blue-shift from page
background-color-2:  "NEW_DARK_TRACK"  # e.g. #2E3550
sidebar-background-color:       "NEW_DARK_SIDEBAR"
app-header-background-color:    "NEW_DARK_SIDEBAR"
more-info-header-background:    "NEW_DARK_DIALOG"
paper-dialog-background-color:  "NEW_DARK_DIALOG"
```

**Constraint: keep the blue-shift in dark mode.** The relationship between
`background-color` and `ha-card-background` in dark mode should maintain a
visible step — cards must be lighter than the page. The current step is
`#202631` → `#252B38` (roughly +5% luminance). Do not set them equal.

**Do not change in a full palette swap:**
- `warning-color: #FA7575` — fixed semantic red
- `ha-card-border-radius`, `ha-card-border-width` — structural, not palette
- `--bubble-border-radius`, `--bubble-icon-border-radius` — structural
- Mushroom `mush-rgb-*` values — they are fixed entity-domain colours
- Font family variables — separate concern

---

## #theme-file-structure

### How to deliver a theme YAML

**Do not use this section to reconstruct a theme.** Use the canonical template:

```
references/casa5heynev2-template.yaml
```

Copy that file, rename the top-level key to the new theme name, then apply
diffs from the relevant anchors in this file. The template has all 500+ variables
pre-populated with the correct var() chains, ZONE markers, Mushroom integration,
and Bubble Card mappings.

**Delivery steps (always include these):**
1. Place the `.yaml` file in `/config/themes/`
2. Run `frontend.reload_themes` (Developer Tools → Actions → search "reload themes")
3. Select the theme: Profile → Theme → `{ThemeName}`

**Naming convention:** `Casa5HeyneV2-{Variant}.yaml` — e.g. `Casa5HeyneV2-Slate.yaml`.
The top-level YAML key must match the filename without `.yaml` exactly — this is
what appears in the Profile → Theme picker.

---

## #mushroom-vars

### Mushroom RGB variables — entity-domain icon colours

These variables control the colour of icons for specific entity domains
in Mushroom Cards and HA's own entity pictures. They are set as RGB triplets
(no `rgb()` wrapper) so they can be used with opacity in CSS `rgba()` calls.

**Do not change these in palette swaps** — they are semantic domain colours,
not palette colours. The only exception is `mush-rgb-blue` which in this
theme is set to the dark text colour rather than a true blue.

| Variable | RGB value | Domain / use |
|----------|-----------|--------------|
| `mush-rgb-blue` | `37, 43, 56` | Info state, HA default blue (overridden to dark text) |
| `mush-rgb-red` | `244, 67, 54` | Alert, danger state |
| `mush-rgb-pink` | `233, 30, 99` | — |
| `mush-rgb-purple` | `156, 39, 176` | — |
| `mush-rgb-deep-purple` | `103, 58, 183` | — |
| `mush-rgb-indigo` | `63, 81, 181` | — |
| `mush-rgb-light-blue` | `3, 169, 244` | — |
| `mush-rgb-cyan` | `0, 188, 212` | — |
| `mush-rgb-teal` | `0, 150, 136` | — |
| `mush-rgb-green` | `76, 175, 80` | Success, motion on, presence home |
| `mush-rgb-light-green` | `139, 195, 74` | — |
| `mush-rgb-lime` | `205, 220, 57` | — |
| `mush-rgb-yellow` | `255, 235, 59` | — |
| `mush-rgb-amber` | `255, 193, 7` | Warning state |
| `mush-rgb-orange` | `255, 152, 0` | Motion sensor on, heating active |
| `mush-rgb-deep-orange` | `255, 87, 34` | — |
| `mush-rgb-brown` | `121, 85, 72` | — |
| `mush-rgb-grey` | `158, 158, 158` | Unavailable, unknown state |
| `mush-rgb-blue-grey` | `96, 125, 139` | — |
| `mush-rgb-black` | `0, 0, 0` | — |
| `mush-rgb-white` | `255, 255, 255` | — |

**Semantic aliases (point to colour variables above):**

| Variable | Points to | Meaning |
|----------|-----------|---------|
| `mush-rgb-info` | `var(--mush-rgb-blue)` | Informational state |
| `mush-rgb-success` | `var(--mush-rgb-green)` | Success / active / home |
| `mush-rgb-warning` | `var(--mush-rgb-orange)` | Warning / heating |
| `mush-rgb-danger` | `var(--mush-rgb-red)` | Error / alarm |

**Why motion sensors show orange:** The HA sensor domain maps `motion` to
`mush-rgb-orange` by default. The `#FA7575` warning red is for alarm/danger
states, not motion. This is correct — do not change `mush-rgb-orange` to match
the warning red.

---

## #app-header-vars

### App header and sidebar variables

These control the HA top header bar and the native HA sidebar
(not Sidebar Card — the built-in HA navigation).

| Variable | Light value | Dark value | Effect |
|----------|-------------|------------|--------|
| `app-header-background-color` | `#F8F8F8` | `#212736` | Top header bar background |
| `app-header-text-color` | `rgb(95,99,104)` | `#FFFFFF` | Header icon and text colour |
| `app-header-edit-background-color` | `#555A60` | `#555A60` | Header colour when in edit mode |
| `sidebar-background-color` | `#F8F8F8` | `#212736` | HA native sidebar background |
| `sidebar-icon-color` | `rgb(95,99,104)` | `#818793` | Inactive nav icon colour |
| `sidebar-text-color` | `var(--sidebar-icon-color)` | — | Nav item label |
| `sidebar-selected-icon-color` | `var(--accent-color)` | `var(--accent-color)` | Active nav icon → accent |
| `sidebar-selected-text-color` | `var(--sidebar-selected-icon-color)` | — | Active nav label |
| `sidebar-selected-background-color` | `var(--primary-background-color)` | — | Active item bg |
| `sidebar-selected-bg` | `var(--accent-color)` | `var(--accent-color)` | Active indicator bar |

**In palette swaps:** when changing `background-color`, also change
`app-header-background-color` and `sidebar-background-color` to match — they
should be identical to the page background for a seamless look.

---

## #font-size-vars

### HA 2025+ font size variables

These variables were added in HA 2025.x to allow theme-level font size
control without card-mod. They are referenced in §2 Accessibility for
wall-panel setups.

| Variable | Default | Effect |
|----------|---------|--------|
| `ha-font-size-body` | `14px` | Base body text size across all HA UI |
| `ha-font-size-small` | `12px` | Small/secondary text (state labels, timestamps) |
| `ha-font-size-heading` | `16px` | Card header text |
| `ha-font-size-subheading` | `14px` | Section subheadings |
| `ha-font-size-l` | `18px` | Large display values (energy numbers etc.) |
| `ha-font-size-xl` | `24px` | Extra-large display |

**Wall-panel override pattern** (add to `modes.light` and `modes.dark`):
```yaml
ha-font-size-body:       "16px"   # readable at 1.5m
ha-font-size-small:      "14px"   # labels still readable
ha-font-size-heading:    "18px"   # card headers prominent
ha-font-size-subheading: "15px"
```

**Note:** `ha-font-size-*` variables may not yet be respected by all HA
cards in every release — test after applying. Bubble Card uses its own
internal font sizing for card content, which follows the HA body font size
but may not pick up all `ha-font-size-*` changes.

---

## #additional-light-mode-vars

### Remaining light mode variables not covered above

**Selection and card states:**

| Variable | Value | Effect |
|----------|-------|--------|
| `ha-card-background-selected` | `var(--ha-card-background)` | Selected card background |
| `ha-card-background-unselected` | `var(--background-color)` | Unselected card in a grid |
| `welcome-card-background` | `rgba(255,255,255,0.75)` | HA Welcome card overlay |

**State and badge colours:**

| Variable | Value | Effect |
|----------|-------|--------|
| `state-icon-color` | `var(--accent-color)` | Default entity icon when active |
| `state-icon-active-color` | `rgb(95,99,104)` | Active state icon (intentionally muted) |
| `state-icon-unavailable-color` | `var(--disabled-text-color)` | Unavailable entity icon |
| `label-badge-red` | `#FA7575` | Badge colour matching warning-color |
| `label-badge-green` | `rgb(109,192,113)` | Success badge |
| `label-badge-blue` | `rgb(26,115,232)` | Info badge |
| `label-badge-yellow` | `rgb(217,183,87)` | Warning badge |

**Switch and slider colours (follow the accent lever automatically):**

| Variable | Value | Notes |
|----------|-------|-------|
| `switch-checked-button-color` | `var(--accent-color)` | Toggle ON button |
| `switch-checked-track-color` | `var(--accent-color)` | Toggle ON track |
| `switch-unchecked-button-color` | `var(--accent-medium-color)` | Toggle OFF button |
| `switch-unchecked-track-color` | `var(--background-color-2)` | Toggle OFF track |
| `paper-slider-active-color` | `var(--accent-color)` | Slider filled portion |
| `paper-slider-secondary-color` | `var(--accent-medium-color)` | Slider secondary |

These all inherit from the accent lever chain automatically — changing
`accent-color` updates all of them without additional changes.
