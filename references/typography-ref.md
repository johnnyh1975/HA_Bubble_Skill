# Typography Reference
# ha-bubble-dashboard skill
# Covers: font loading architecture, all HA font variables,
#         wall-panel size overrides, 4 swap recipes, troubleshooting.
# Current theme font: Alexandria (Google Fonts)

---

## #architecture

### How HA font loading works end-to-end

HA does not load custom fonts natively. The loading chain is:

```
configuration.yaml
  └─ frontend:
       extra_module_url:
         - /local/alexandria-font.js     ← JS file Claude generates or delivers
               │
               ▼
         Creates a <link> element pointing to the font source
         (Google Fonts CDN or self-hosted files)
               │
               ▼
         Font downloads and registers in the browser
               │
               ▼
Theme YAML
  └─ ha-font-family-body: "Alexandria, sans-serif"
  └─ ha-font-family-heading: "Alexandria, sans-serif"
  └─ paper-font-*: "var(--primary-font-family)"   ← legacy variables
               │
               ▼
         HA and all cards (Bubble Card, Mushroom, native) render in the new font
```

**The two failure points:**
1. The JS file is not at `/config/www/` → font never loads, no browser error
2. The theme variables are set but the JS file is missing → same silent failure

**Scope:** This loading mechanism applies globally to the entire HA interface —
not just to dashboards. Changing the font changes it everywhere: sidebar, settings,
energy dashboard, history cards. This is correct and expected.

---

## #loading-methods

### Three font loading methods

#### Method 1 — Google Fonts CDN (recommended for most users)

Easiest. Requires internet access from the HA device.

**Step 1:** Create `/config/www/your-font.js`:
```javascript
// /config/www/your-font.js
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://fonts.googleapis.com/css2?family=FontName:wght@300;400;500;600;700&display=swap';
document.head.appendChild(link);
```

**Step 2:** Add to `configuration.yaml`:
```yaml
frontend:
  extra_module_url:
    - /local/your-font.js
```

**Step 3:** Restart HA. No further action needed — the font loads on every page visit.

**Limitation:** Font will not load if the HA device has no internet access (e.g. offline
HA installations, Raspberry Pi behind a firewall). Use Method 2 in that case.

---

#### Method 2 — Self-hosted font files (offline / reliable)

More setup, but works without internet. No flash of unstyled text.

**Step 1:** Download font files (`.woff2` format) and place in `/config/www/fonts/`:
```
/config/www/fonts/
  YourFont-Regular.woff2
  YourFont-Medium.woff2
  YourFont-SemiBold.woff2
  YourFont-Bold.woff2
```

**Step 2:** Create `/config/www/your-font.js`:
```javascript
// /config/www/your-font.js
const style = document.createElement('style');
style.textContent = `
  @font-face {
    font-family: 'YourFont';
    src: url('/local/fonts/YourFont-Regular.woff2') format('woff2');
    font-weight: 400;
    font-display: block;  /* block prevents flash of unstyled text */
  }
  @font-face {
    font-family: 'YourFont';
    src: url('/local/fonts/YourFont-Medium.woff2') format('woff2');
    font-weight: 500;
    font-display: block;
  }
  @font-face {
    font-family: 'YourFont';
    src: url('/local/fonts/YourFont-SemiBold.woff2') format('woff2');
    font-weight: 600;
    font-display: block;
  }
  @font-face {
    font-family: 'YourFont';
    src: url('/local/fonts/YourFont-Bold.woff2') format('woff2');
    font-weight: 700;
    font-display: block;
  }
`;
document.head.appendChild(style);
```

**Step 3:** Add to `configuration.yaml` (same as Method 1):
```yaml
frontend:
  extra_module_url:
    - /local/your-font.js
```

---

#### Method 3 — System font stack (no loading required)

No JS file needed. Uses fonts already installed on the viewing device. Fastest
rendering, zero network dependency, but appearance varies across devices and OSes.

**Skip the `extra_module_url` step entirely.** Just set in the theme:
```yaml
ha-font-family-body: >-
  -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
ha-font-family-heading: >-
  -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
```

Best for: performance-critical wall panels, offline installations, users who prefer
consistent system rendering over a custom typeface.

---

## #ha-variables

### Complete HA font variable catalogue

**Modern variables (HA 2024.x+) — set these in the mode-independent theme block:**

| Variable | Default | Effect |
|----------|---------|--------|
| `ha-font-family-body` | system font | Primary body text across all HA UI |
| `ha-font-family-heading` | system font | Card headers, dialog titles |
| `ha-font-family-code` | monospace | Code blocks, developer tools |
| `ha-font-size-body` | `14px` | Base text size |
| `ha-font-size-small` | `12px` | Secondary/subdued text, timestamps |
| `ha-font-size-heading` | `16px` | Card header size |
| `ha-font-size-subheading` | `14px` | Section subheadings |
| `ha-font-size-l` | `18px` | Large display values |
| `ha-font-size-xl` | `24px` | Extra-large values (energy totals) |

**Legacy variables — required for full coverage (HA 2023.x and older cards):**

These must be set in the mode-specific block (`modes.light` and `modes.dark`)
because they reference `--primary-font-family` which is mode-set.

```yaml
# Set in modes.light and modes.dark
primary-font-family: "YourFont, fallback, sans-serif"

# Set in mode-independent block
paper-font-common-base_-_font-family: "var(--primary-font-family)"
paper-font-common-code_-_font-family: "var(--primary-font-family)"
paper-font-body1_-_font-family:       "var(--primary-font-family)"
paper-font-subhead_-_font-family:     "var(--primary-font-family)"
paper-font-headline_-_font-family:    "var(--primary-font-family)"
paper-font-caption_-_font-family:     "var(--primary-font-family)"
paper-font-title_-_font-family:       "var(--primary-font-family)"
ha-card-header-font-family:           "var(--primary-font-family)"
```

**Why both modern and legacy?**
Modern HA uses `ha-font-family-*`. Older custom cards (pre-2024 Mushroom versions,
third-party cards, some HA built-in cards) still consume `paper-font-*`. Omitting
the legacy block causes a visible mix of fonts on dashboards with older cards.

**Safe to omit:** `ha-font-family-code` — only affects developer tools and code
blocks. Most dashboard users never see it.

---

## #size-system

### Font size variables and wall-panel overrides

**Default HA sizes are calibrated for desktop browsers at arm's length.**
For wall panels viewed from 1–2 metres, these need upward adjustment.

**Standard override for wall-panel dashboards:**
```yaml
# Add to mode-independent block in theme file
ha-font-size-body:       "16px"   # readable at 1.5m (default 14px)
ha-font-size-small:      "14px"   # subdued text stays readable
ha-font-size-heading:    "18px"   # card headers prominent
ha-font-size-subheading: "16px"   # matches new body size
```

**Bubble Card interaction:** Bubble Card reads `ha-font-size-body` for card
body text. Setting it to `16px` also increases Bubble Card text without any
card-level changes.

**Mushroom Card interaction:** Mushroom has its own size variables
(`mush-card-primary-font-size`, `mush-card-secondary-font-size`). These do
not inherit from `ha-font-size-*` — set them separately in the theme if needed:
```yaml
mush-card-primary-font-size:   "15px"   # default 14px
mush-card-secondary-font-size: "13px"   # default 12px
mush-chip-font-size:           "0.35em" # relative to chip height (default 0.3em)
```

**Rule: whenever setting `ha-font-size-body` above 14px for a wall panel,
also check if Mushroom Cards is installed — if so, set the three Mushroom
size variables above to maintain visual consistency.**

**Accessibility threshold:** 16px is the minimum for sustained reading at 1.5m.
For panels mounted at 2m+, use 18px body size. Above that, rely on `card_layout:
large` for Bubble Cards rather than increasing font size further — very large text
on small cards breaks the layout.

---

## #alexandria

### Alexandria — the current theme font

**About:**
- Variable-weight sans-serif designed for multi-script legibility
- Supports weights 100–900 in a single variable font file
- Excellent Latin + Arabic coverage — well-suited for multilingual setups
- Google Fonts URL: `https://fonts.googleapis.com/css2?family=Alexandria:wght@300;400;500;600;700&display=swap`

**Weight usage in Casa5HeyneV2:**

| Weight | Use in theme |
|--------|-------------|
| 300 | Loaded but not explicitly used |
| 400 | Body text (`ha-font-size-body`), secondary card text |
| 500 | Card primary text (`mush-card-primary-font-weight: 500`) |
| 600 | Loaded but not explicitly used |
| 700 | MCG title (`mcg-title-font-weight: 700`) |

**CDN stability note:** Google Fonts has 99.9%+ uptime but does go down occasionally.
For production wall panels, use Method 2 (self-hosted) to eliminate this dependency.

**Current JS loader for Alexandria:**
```javascript
// /config/www/alexandria-font.js
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://fonts.googleapis.com/css2?family=Alexandria:wght@300;400;500;600;700&display=swap';
document.head.appendChild(link);
```

**Self-hosting Alexandria (no CDN dependency):**

> **Simpler option — variable font file:** Alexandria is available as a single
> variable font file that covers all weights (100–900) in one download. This is
> simpler than downloading 5 separate woff2 files:
> ```
> /config/www/fonts/Alexandria[wght].woff2   (variable font — all weights)
> ```
> Download from Google Fonts → "Download family" → extract the `wght` woff2 file.
> Then your `@font-face` block becomes one entry with `font-weight: 100 900`.

Full multi-weight approach (if variable font is unavailable):
```
/config/www/fonts/
  alexandria-300.woff2   (Light)
  alexandria-400.woff2   (Regular)
  alexandria-500.woff2   (Medium)
  alexandria-600.woff2   (SemiBold)
  alexandria-700.woff2   (Bold)
```

Then your self-hosted loader for a variable font (`/config/www/alexandria-font.js`):
```javascript
const style = document.createElement('style');
style.textContent = `
  @font-face {
    font-family: 'Alexandria';
    src: url('/local/fonts/Alexandria[wght].woff2') format('woff2');
    font-weight: 100 900;   /* covers all weights in one file */
    font-display: block;
  }
`;
document.head.appendChild(style);
```

Or the multi-weight approach for separate files:
```javascript
const style = document.createElement('style');
style.textContent = `
  @font-face { font-family:'Alexandria'; font-weight:300;
    src:url('/local/fonts/alexandria-300.woff2') format('woff2'); font-display:block; }
  @font-face { font-family:'Alexandria'; font-weight:400;
    src:url('/local/fonts/alexandria-400.woff2') format('woff2'); font-display:block; }
  @font-face { font-family:'Alexandria'; font-weight:500;
    src:url('/local/fonts/alexandria-500.woff2') format('woff2'); font-display:block; }
  @font-face { font-family:'Alexandria'; font-weight:600;
    src:url('/local/fonts/alexandria-600.woff2') format('woff2'); font-display:block; }
  @font-face { font-family:'Alexandria'; font-weight:700;
    src:url('/local/fonts/alexandria-700.woff2') format('woff2'); font-display:block; }
`;
document.head.appendChild(style);
```

`font-display: block` prevents flash of unstyled text — the page waits for
the font before rendering text. Use `swap` instead if you prefer instant
render with a brief system-font flash.

---

## #swap-recipes

### 4 ready-made font swap recipes

Each recipe includes: the JS loader file content, the theme variable changes,
and notes on rendering character.

---

### Font Recipe 1 — Inter (modern, geometric, highly readable)

**Character:** Clean, neutral, engineered for screen legibility. Popular in
dashboards that lean technical or professional. Excellent at small sizes.

**JS loader** (`/config/www/inter-font.js`):
```javascript
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap';
document.head.appendChild(link);
```

**Theme changes** (in mode-independent block):
```yaml
ha-font-family-body:    "Inter, sans-serif"
ha-font-family-heading: "Inter, sans-serif"
ha-font-family-code:    "Inter, monospace"
paper-font-common-base_-_font-family: "var(--primary-font-family)"
paper-font-common-code_-_font-family: "var(--primary-font-family)"
paper-font-body1_-_font-family:       "var(--primary-font-family)"
paper-font-subhead_-_font-family:     "var(--primary-font-family)"
paper-font-headline_-_font-family:    "var(--primary-font-family)"
paper-font-caption_-_font-family:     "var(--primary-font-family)"
paper-font-title_-_font-family:       "var(--primary-font-family)"
ha-card-header-font-family:           "var(--primary-font-family)"
```

**In both `modes.light` and `modes.dark`:**
```yaml
primary-font-family: "Inter, sans-serif"
```

**configuration.yaml:**
```yaml
frontend:
  extra_module_url:
    - /local/inter-font.js
```

---

### Font Recipe 2 — Geist (modern, technical, Vercel's design language)

**Character:** Sharp, contemporary, slightly condensed. Strong technical/developer
aesthetic. Very good at 14px. Similar to Inter but with more personality.
Pairs well with the Midnight Slate and Steel palettes.

**JS loader** (`/config/www/geist-font.js`):
```javascript
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap';
document.head.appendChild(link);
```

**`configuration.yaml`:**
```yaml
frontend:
  extra_module_url:
    - /local/geist-font.js
```

**Theme changes** (mode-independent block):
```yaml
ha-font-family-body:    "Geist, sans-serif"
ha-font-family-heading: "Geist, sans-serif"
ha-font-family-code:    "Geist, monospace"
paper-font-common-base_-_font-family: "var(--primary-font-family)"
paper-font-common-code_-_font-family: "var(--primary-font-family)"
paper-font-body1_-_font-family:       "var(--primary-font-family)"
paper-font-subhead_-_font-family:     "var(--primary-font-family)"
paper-font-headline_-_font-family:    "var(--primary-font-family)"
paper-font-caption_-_font-family:     "var(--primary-font-family)"
paper-font-title_-_font-family:       "var(--primary-font-family)"
ha-card-header-font-family:           "var(--primary-font-family)"
```

**In both `modes.light` and `modes.dark`:**
```yaml
primary-font-family: "Geist, sans-serif"
```

---

### Font Recipe 3 — DM Sans (humanist, warm, approachable)

**Character:** Friendly and legible without being clinical. Warmer than Inter,
less corporate than Roboto. Pairs exceptionally well with the Casa5 warm gold
accent. Good choice if Alexandria feels too geometric.

**JS loader** (`/config/www/dm-sans-font.js`):
```javascript
const link = document.createElement('link');
link.rel = 'stylesheet';
link.href = 'https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap';
document.head.appendChild(link);
```

**Theme changes:** Replace `Alexandria` with `DM Sans` in all font family variables.

---

### Font Recipe 4 — System stack (zero loading, maximum reliability)

**Character:** Matches the user's operating system. Renders instantly with no
network dependency. Inconsistent across devices but always fast.

**No JS loader file needed.**

**Theme changes** (mode-independent block):
```yaml
ha-font-family-body: >-
  -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
  "Helvetica Neue", Arial, sans-serif
ha-font-family-heading: >-
  -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
  "Helvetica Neue", Arial, sans-serif
ha-font-family-code: >-
  "SF Mono", "Fira Code", "Fira Mono", "Roboto Mono",
  Consolas, monospace
```

**In both modes:**
```yaml
primary-font-family: >-
  -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
  "Helvetica Neue", Arial, sans-serif
```

**No `extra_module_url` change needed** — remove the existing entry to avoid
loading the Alexandria JS file unnecessarily.

---

## #single-mode-themes

### How HA selects which theme mode to use

Before building a single-mode theme, understand how HA decides which mode to show:

**1. System preference (default for most users)**
HA reads the browser's `prefers-color-scheme` media query. If the browser/OS is
set to dark mode, HA uses `modes.dark`. If light, it uses `modes.light`. This
changes automatically when the user changes their OS theme.

**2. Profile override (per-user setting)**
Profile → Theme → enable/disable "Dark mode" toggle. This overrides the system
preference for that user only. If set, it stays regardless of OS changes.

**3. Companion App**
The HA Companion App respects the app's own dark/light setting, which may differ
from the OS. A phone in dark mode with the Companion App set to "Match system" will
use dark mode; setting the app to "Light" forces light regardless.

**4. What happens with a single-mode theme:**
- If the theme only has `modes.light` and the user's device is in dark mode →
  HA uses the `modes.light` block. The user sees the light theme even in "dark mode".
- If the theme only has `modes.dark` and the user's device is in light mode →
  HA uses the `modes.dark` block. The user sees the dark theme in "light mode".

**For wall panels:** this is the desired behaviour. A kiosk tablet is always in the
same visual state regardless of OS preferences.

**For general users:** be explicit when delivering a single-mode theme:
> "This is a light-mode-only theme. If your device is in dark mode, HA will
> still show the light theme. To add dark mode later, add a `dark:` block under
> `modes:` in the theme file."

### Single-mode theme structure — light only or dark only

For fixed-display setups (wall panels, kiosk mode, e-ink) where mode switching
never occurs, a single-mode theme is the correct choice.

**When to recommend single-mode:**
- User mentions a wall-mounted tablet, kiosk, or display panel
- HA Companion App with theme locked in Profile settings
- The user says "I always use dark mode" or "never use dark mode"
- Offline / embedded HA installations where system preference detection is unreliable

**Single-mode theme structure — dark only example:**
```yaml
MyTheme-Dark:

  # Mode-independent block (identical to full theme)
  ha-card-border-radius: "16px"
  # ... all bubble-*, mush-rgb-state-*, typography variables ...

  # Single mode block — no modes.light
  modes:
    dark:
      primary-font-family: "Alexandria, sans-serif"
      accent-color:         "#D9BE8B"
      background-color:     "#202631"
      ha-card-background:   "#252B38"
      # ... all other dark mode values ...
```

**Single-mode theme structure — light only:**
```yaml
MyTheme-Light:

  # Mode-independent block
  # ...

  modes:
    light:
      primary-font-family: "Alexandria, sans-serif"
      accent-color:         "#D9BE8B"
      background-color:     "#F8F8F8"
      ha-card-background:   "#FFFFFF"
      # ... all light mode values ...
```

**Delivering a single-mode theme:**
Tell the user: "I've generated a light-mode-only theme. If you ever want to
add dark mode later, the structure supports adding a `dark:` block under `modes:`
without changing anything else."

---

## #font-troubleshooting

### Font troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Font looks like system sans-serif (Arial / Helvetica) | `extra_module_url` entry missing or wrong path | Verify `/config/www/your-font.js` exists. Add to `configuration.yaml` and restart HA. |
| Font loads in browser but not in Companion App | Google Fonts CDN blocked on mobile network | Switch to Method 2 (self-hosted). Or: open the app on Wi-Fi where CDN is accessible. |
| Flash of unstyled text on every page load | Google Fonts `display=swap` behaviour (expected with CDN) | Use `display=block` in a self-hosted `@font-face` declaration (Method 2) to eliminate. |
| Theme applies but some cards show wrong font | Legacy `paper-font-*` variables missing from theme | Add the full legacy block to mode-independent section — all 7 `paper-font-*` variables. |
| Font changes but Mushroom cards still wrong | `mush-card-primary-font-size` set to px value overriding the font | Mushroom font sizing is independent — set `mush-card-primary-color: var(--primary-text-color)` and verify `mush-card-primary-font-size` is not set to a px value that conflicts. |
| Wall-panel text too small at 2m viewing distance | `ha-font-size-body` still at default `14px` | Apply the wall-panel size override block: `ha-font-size-body: "18px"`. |
| Font only loads on first visit, then reverts | Browser caching the old theme | Hard refresh (Ctrl+Shift+R), then clear site data in DevTools if still wrong. |
| `extra_module_url` path not working | Path uses wrong prefix | Use `/local/` prefix for files in `/config/www/`. `/config/www/font.js` → `/local/font.js`. |
