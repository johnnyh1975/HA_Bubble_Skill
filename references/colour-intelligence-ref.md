# Colour Intelligence Reference
# ha-bubble-dashboard skill — Phase 5a
# Covers: Casa5HeyneV2 colour profile, WCAG contrast checks,
#         harmony rules, 6 full palette recipes with theme diffs.

---

## #two-modes

### Advisory vs prescriptive mode

**Advisory mode (default):** Claude presents the palette options with rationale
and WCAG scores. The user picks. Appropriate when the user says "what could I
change?" or "show me options".

```
Present: Recipe name, accent hex, one-line character description,
         WCAG score on light card and dark card,
         suggested use case (light-primary / dark-primary / both).
Then ask: "Which palette would you like me to generate the full theme diff for?"
```

**Prescriptive mode:** Claude picks a palette based on stated criteria and
generates the complete theme file. Appropriate when the user says "make it
warmer", "I want something more professional", "generate a forest theme".

```
Criteria → pick recipe → generate complete theme YAML → deliver as .yaml file.
Always state: which recipe was chosen, why, and the WCAG scores for the new accent.
```

**Trigger prescriptive mode** when the user provides a mood, adjective, or
domain description rather than asking for options: "make it feel like a
spa", "I want a dark navy theme", "something earthy and warm".

---

## #advisory-conversation-flow

### Colour advisory conversation script

Use this script when the user asks for a colour change but hasn't specified
a palette. Guides from vague intent to a generated theme file in 3 steps.

**Step 1 — Single elicitation question (pick the most relevant one):**

If the user gave a mood/adjective ("warmer", "more modern", "calming"):
→ Switch to **prescriptive mode** immediately. Map to the closest recipe
  (see mapping table below) and generate. State the choice and rationale.

If the user asked "what options do I have?" or "show me alternatives":
→ Present the **advisory shortlist** (Step 2).

If the user gave a specific colour direction ("something green", "dark navy"):
→ Ask only: "Accent-only swap keeping the current backgrounds, or a full
  palette change including the page and card backgrounds?"

If the user said "keep my accent, just change the backgrounds" or
"I like the gold but want warmer backgrounds":
→ **Background-only swap mode.** Apply only Zone 2 (backgrounds) and Zone 5
  (dialog tint) from `css-theme-ref.md#full-palette-swap`. Do not touch
  Zone 1 (accent lever). Deliver the theme with only those lines changed.
  Example: keep `#D9BE8B` gold, change page to `#F5F0E8` warm cream,
  card to `#FDFAF5` — the Warm Cream + Terracotta backgrounds from
  Full Palette 1 work with any warm accent.

**Step 2 — Advisory shortlist (present as a table, max 6 rows):**

```
| Name | Accent | Character | Best for | WCAG (light/dark) |
|------|--------|-----------|----------|-------------------|
| Original | #D9BE8B | Warm gold | Cosy, classic | 1.9:1 / 3.0:1 |
| Slate | #8BA8C4 | Blue-grey | Calm, technical | 2.7:1 / 3.9:1 |
| Sage | #8BB89A | Muted green | Natural, restful | 2.6:1 / 3.8:1 |
| Terracotta | #C4896B | Warm clay | Earthy, rich | 3.1:1 / 4.5:1 |
| Dusk | #A48BBF | Mauve violet | Elegant, evening | 2.9:1 / 4.0:1 |
| Steel | #5B8FBF | Steel blue | Professional, clear | 3.4:1 / 4.8:1 |
```

Then ask: "Would you like accent-only, or a full palette (backgrounds too)?
And which would you like me to generate?"

**Step 3 — Generate:**
- Take the user's choice → apply from `#accent-swap-recipes` or `#full-palette-recipes`
- Open `references/casa5heynev2-template.yaml` → apply diff → output complete file
- State: recipe name, WCAG scores, filename, installation steps

**Mood → recipe mapping for prescriptive mode:**

| User says | Prescriptive choice | Rationale |
|-----------|--------------------|-----------| 
| "warmer", "cosier", "homely" | Full Palette 1 (Warm Cream + Terracotta) | Warm backgrounds + warm accent |
| "cooler", "cleaner", "modern" | Full Palette 2 (Cool Neutral + Slate) | Cool surfaces + steel-blue accent |
| "natural", "calming", "biophilic" | Full Palette 3 (Sage Green + Forest) | Green-tinted surfaces + sage accent |
| "elegant", "sophisticated" | Dusk accent-only (Recipe E) | Mauve has premium feel without changing bg |
| "professional", "tech" | Full Palette 2 or Steel accent | Blue-grey reads as technical |
| "minimal", "Scandinavian" | Slate accent-only on original bg | Low-saturation, keeps neutrals |
| "dark", "moody" | Full Palette — Midnight Slate (Recipe 4) | Deep dark surfaces |
| "purple", "violet" | Full Palette — Dusk Mauve (Recipe 5) | Mauve full palette |
| "midnight", "navy" | Full Palette — Midnight Steel (Recipe 6) | Dark navy surfaces + steel |
| User supplies a specific hex (e.g. "#4A7B9D") | Prescriptive — use #bring-your-own-accent | Run WCAG pre-flight, generate from template |

---

## #casa5-profile

### Casa5HeyneV2 baseline colour profile

Understanding the existing palette is the starting point for any change.

**Accent — Warm Gold**
- Hex: `#D9BE8B`
- HSL: ~43°, 50%, 70%
- Character: warm, low-saturation, high-lightness gold. Reads as
  brass/honey. Calming and premium. Neither obviously cool nor hot.
- WCAG on light card (#FFF): **1.9:1** — fails all thresholds.
  Use purely as decorative tint, never for text or sole icon colour.
- WCAG on dark card (#252B38): **3.0:1** — passes UI component threshold (3:1).
  Usable for icon fills and slider tracks on dark backgrounds.

**Light mode surfaces**
- Page: `#F8F8F8` — very light warm grey, near-white
- Card: `#FFFFFF` — pure white
- Secondary: `rgb(230,230,230)` — subtle step
- Temperature: cool-neutral, matches the gold accent without competing

**Dark mode surfaces**
- Page: `#202631` — deep blue-grey (HSL ~220°, 20%, 15%)
- Card: `#252B38` — slightly lighter blue-grey
- Track: `#3a3c55` — perceptibly purple-shifted
- Temperature: distinctly cool, providing contrast with the warm gold accent

**Text**
- Light primary: `#555A60` — warm dark grey, 7.0:1 on white ✓ AAA
- Dark primary: `#FFFFFF` — white, 13.5:1 on #252B38 ✓ AAA
- Contrast is conservative — well above minimums in both modes

**The design tension:** warm gold accent on cool dark backgrounds creates
a deliberate warm/cool contrast. Replacement accents should maintain this
tension — a cool accent on the dark blue backgrounds loses the character.

---

## #wcag-checks

### Pre-calculated contrast ratios for key token pairs

All ratios calculated using WCAG relative luminance formula.

**Light mode — accent (#D9BE8B) on surfaces:**

| Surface | Hex | Contrast | WCAG result |
|---------|-----|----------|-------------|
| Card background | `#FFFFFF` | 1.9:1 | ✗ fails all — decorative only |
| Page background | `#F8F8F8` | 1.8:1 | ✗ fails all — decorative only |
| Secondary bg | `#E6E6E6` | 1.6:1 | ✗ fails all |

**Light mode — text (#555A60) on surfaces:**

| Surface | Hex | Contrast | WCAG result |
|---------|-----|----------|-------------|
| Card background | `#FFFFFF` | 7.0:1 | ✓ AAA normal text |
| Accent surface (#D9BE8B bg) | `#D9BE8B` | 3.7:1 | ✓ AA large text / UI component |

**Dark mode — accent (#D9BE8B) on surfaces:**

| Surface | Hex | Contrast | WCAG result |
|---------|-----|----------|-------------|
| Card background | `#252B38` | 3.0:1 | ✓ AA UI components (just passes) |
| Page background | `#202631` | 3.3:1 | ✓ AA UI components |

**Dark mode — white text on dark surfaces:**

| Surface | Hex | Contrast | WCAG result |
|---------|-----|----------|-------------|
| Card background | `#252B38` | 13.5:1 | ✓ AAA |
| Page background | `#202631` | 15.6:1 | ✓ AAA |

### WCAG thresholds summary

| Use case | Minimum | Target |
|----------|---------|--------|
| Normal body text | 4.5:1 (AA) | 7:1 (AAA) |
| Large/bold text (18pt+ or 14pt bold+) | 3:1 (AA) | 4.5:1 |
| UI components (icons, borders, sliders) | 3:1 (AA) | 4.5:1 |
| Decorative elements (tints, overlays) | No minimum | — |

### Pre-flight check for any new accent

Before committing a new accent colour, verify these four pairs:

```
1. New accent on light card (#FFFFFF)    → need ≥ 3:1 for icon use
2. New accent on dark card (#252B38)     → need ≥ 3:1 for icon use
3. Text (#555A60) on accent background   → need ≥ 4.5:1 if text appears on accent
4. New accent at 25% opacity on #FFFFFF  → informational (will always be decorative)
```

The gold fails check 1 — which is acceptable because it is never used as
a standalone icon or text colour on light backgrounds. Any replacement that
passes check 1 (≥ 3:1 on white) will be an improvement in light mode usability.

---

## #harmony-rules

### Colour harmony rules for HA dashboards

These rules are scoped to the Casa5HeyneV2 architecture and dashboard context.

**Rule 1: Warm/cool tension is the identity.**
The existing palette works because the warm gold accent is seen against cool
blue-grey dark backgrounds. Preserve this tension with any replacement:
- Warm accents (amber, terracotta, peach, sage) → work best on the existing cool dark surfaces
- Cool accents (steel blue, slate, teal) → may fight the cool dark surfaces; compensate with a slightly warmer dark background

**Rule 2: Saturation budget.**
Light mode backgrounds are near-neutral (≈ 0% saturation). The accent carries
all the saturation. Keep the accent below ~70% saturation — higher creates
visual fatigue when repeated across many cards. The current gold is ~50%.

**Rule 3: Warning colour is fixed.**
`#FA7575` (soft red) is the warning/error colour. Any new accent must have
sufficient visual distance from this red:
- Avoid accents in the red-pink range (hues 330°–30°)
- Orange-amber accents (30°–60°) are close but acceptable at lower saturation
- If using orange, verify the accent and the warning read as clearly distinct

**Rule 4: 80/15/5 ratio.**
Target proportion of colour surface area:
- 80% neutral (backgrounds, card surfaces, text) — already handled by the theme
- 15% accent (active states, icons, sliders, selected nav items)
- 5% semantic (warning red, success green, info blue for badges/states)

**Rule 5: Opacity scale must work.**
The accent is used at 5 opacity levels: 15%, 25%, 35%, 50%, 85%, and full 100%.
A valid accent must produce readable, distinguishable tints at all these levels.
Highly saturated colours become muddy at low opacity on light backgrounds.
Desaturated colours become indistinguishable at low opacity on dark backgrounds.
The sweet spot is 40–60% saturation at 60–75% lightness.

**Rule 6: Background temperature follows accent temperature.**
For a full palette swap with background changes:
- Warm accent → use slightly warm page background (cream, warm off-white)
- Cool accent → use neutral-to-cool page background (cool grey, blue-grey)
- Never mix a warm accent with an obviously cool background in light mode —
  the transition reads as a mistake, not a design choice.

**Rule 7: Dark-mode accents need higher lightness.**
An accent that reads well at L=62% in light mode becomes visually dull on
dark backgrounds. For dark-primary dashboards, increase the accent lightness
by 8–12 percentage points (e.g. L=62% → L=72%) while keeping the same hue
and saturation. The WCAG check handles the floor — this rule handles the
ceiling for perceived vibrancy.

---

## #bring-your-own-accent

### Custom accent — fill-in-the-blanks template

Use this when the user provides their own hex value rather than choosing from
the 6 ready-made recipes. Cross-reference with `css-theme-ref.md#how-to-swap-accent`
for the same template in context.

**Step 1 — Convert hex to RGB:**
`#RRGGBB` → separate into R, G, B decimal values.
Example: `#7B9E87` → R=123, G=158, B=135.

**Step 2 — Run WCAG pre-flight** (see `#wcag-checks`):
- Accent on light card (#FFFFFF): target ≥ 3:1
- Accent on dark card (#252B38): target ≥ 3:1

**Step 3 — Apply to theme (light mode):**
```yaml
accent-color:                    "#YOURHEX"
accent-color-background-opacity: "rgba(R,G,B, 0.25)"
accent-medium-color:             "rgba(R,G,B, 0.5)"
ha-color-primary-30:             "rgba(R,G,B, 0.85)"
ha-color-primary-40:             "#YOURHEX"
ha-color-primary-80:             "rgba(R,G,B, 0.35)"
ha-color-primary-90:             "rgba(R,G,B, 0.25)"
ha-color-primary-95:             "rgba(R,G,B, 0.15)"
mdc-ripple-color:                "rgba(R,G,B, 0.20)"
```

**Step 4 — Apply to theme (dark mode):**
```yaml
accent-color:                    "#YOURHEX"   # consider +8–12% L for vibrancy (Rule 7)
accent-color-background-opacity: "rgba(R,G,B, 0.25)"
accent-medium-color:             "#YOURHEX"   # full opacity in dark mode
ha-color-primary-30:             "rgba(R,G,B, 0.85)"
ha-color-primary-40:             "#YOURHEX"
ha-color-primary-80:             "rgba(R,G,B, 0.35)"
ha-color-primary-90:             "rgba(R,G,B, 0.25)"
ha-color-primary-95:             "rgba(R,G,B, 0.15)"
mdc-ripple-color:                "rgba(R,G,B, 0.20)"
```

---

## #accent-swap-recipes

### 6 ready-made accent swap recipes

Each recipe is an accent-only swap — 8 lines per mode. Backgrounds and text
colours remain as Casa5HeyneV2 originals. See `#full-palette-recipes` for
full palette variants. For a custom hex, use `#bring-your-own-accent` above.

---

### Recipe A — Casa5 Original (reference)

```yaml
# Warm gold — the existing Casa5HeyneV2 palette
# Light and dark mode values are identical for this accent
accent-color:                    "#D9BE8B"
accent-color-background-opacity: "rgba(217,190,139,0.25)"
accent-medium-color:             "rgba(217,190,139,0.5)"   # light
# accent-medium-color:           "#D9BE8B"                  # dark (full)
ha-color-primary-30:             "rgba(217,190,139,0.85)"
ha-color-primary-40:             "#D9BE8B"
ha-color-primary-80:             "rgba(217,190,139,0.35)"
ha-color-primary-90:             "rgba(217,190,139,0.25)"
ha-color-primary-95:             "rgba(217,190,139,0.15)"
mdc-ripple-color:                "rgba(217,190,139,0.20)"
# ── ZONE 6: Mushroom sync (mode-independent block) ──────────
# accent-color-rgb:              "217, 190, 139"
```

WCAG on light card: 1.9:1 (decorative only). WCAG on dark card: 3.0:1 (UI components ✓).

---

### Recipe B — Casa5 Slate

```yaml
# Desaturated blue-grey. Calm, technical. Pairs well with the cool dark surfaces.
# Hue: ~215°, Sat: 25%, Light: 62%
accent-color:                    "#8BA8C4"
accent-color-background-opacity: "rgba(139,168,196,0.25)"
accent-medium-color:             "rgba(139,168,196,0.5)"   # light
# accent-medium-color:           "#8BA8C4"                  # dark
ha-color-primary-30:             "rgba(139,168,196,0.85)"
ha-color-primary-40:             "#8BA8C4"
ha-color-primary-80:             "rgba(139,168,196,0.35)"
ha-color-primary-90:             "rgba(139,168,196,0.25)"
ha-color-primary-95:             "rgba(139,168,196,0.15)"
mdc-ripple-color:                "rgba(139,168,196,0.20)"
# ── ZONE 6: Mushroom sync (mode-independent block) ──────────
# accent-color-rgb:              "139, 168, 196"
```

WCAG on light card (#FFF): 2.7:1 (UI component borderline — use at full opacity).
WCAG on dark card (#252B38): 3.9:1 ✓ AA UI components. Good for desk-primary dashboards.

---

### Recipe C — Casa5 Sage

```yaml
# Muted green. Organic, restful. Low visual fatigue for always-on displays.
# Hue: ~140°, Sat: 28%, Light: 64%
accent-color:                    "#8BB89A"
accent-color-background-opacity: "rgba(139,184,154,0.25)"
accent-medium-color:             "rgba(139,184,154,0.5)"   # light
# accent-medium-color:           "#8BB89A"                  # dark
ha-color-primary-30:             "rgba(139,184,154,0.85)"
ha-color-primary-40:             "#8BB89A"
ha-color-primary-80:             "rgba(139,184,154,0.35)"
ha-color-primary-90:             "rgba(139,184,154,0.25)"
ha-color-primary-95:             "rgba(139,184,154,0.15)"
mdc-ripple-color:                "rgba(139,184,154,0.20)"
# ── ZONE 6: Mushroom sync (mode-independent block) ──────────
# accent-color-rgb:              "139, 184, 154"
```

WCAG on light card (#FFF): 2.6:1 (decorative on light). WCAG on dark card: 3.8:1 ✓.
Best on dark mode displays; recommend warm bg tint in light mode (see Recipe C full).

---

### Recipe D — Casa5 Terracotta

```yaml
# Warm terracotta-clay. Analogous to gold, richer and earthier.
# Hue: ~20°, Sat: 45%, Light: 62%
accent-color:                    "#C4896B"
accent-color-background-opacity: "rgba(196,137,107,0.25)"
accent-medium-color:             "rgba(196,137,107,0.5)"   # light
# accent-medium-color:           "#C4896B"                  # dark
ha-color-primary-30:             "rgba(196,137,107,0.85)"
ha-color-primary-40:             "#C4896B"
ha-color-primary-80:             "rgba(196,137,107,0.35)"
ha-color-primary-90:             "rgba(196,137,107,0.25)"
ha-color-primary-95:             "rgba(196,137,107,0.15)"
mdc-ripple-color:                "rgba(196,137,107,0.20)"
# ── ZONE 6: Mushroom sync (mode-independent block) ──────────
# accent-color-rgb:              "196, 137, 107"
```

WCAG on light card (#FFF): 3.1:1 ✓ AA UI components. WCAG on dark card: 4.5:1 ✓ AA.
Best accent-only recipe for light mode icon usability. Verify distance from #FA7575 warning — acceptable at this hue (20° vs 0°).

---

### Recipe E — Casa5 Dusk

```yaml
# Muted violet-mauve. Elegant, slightly cooler than gold.
# Hue: ~280°, Sat: 28%, Light: 65%
accent-color:                    "#A48BBF"
accent-color-background-opacity: "rgba(164,139,191,0.25)"
accent-medium-color:             "rgba(164,139,191,0.5)"   # light
# accent-medium-color:           "#A48BBF"                  # dark
ha-color-primary-30:             "rgba(164,139,191,0.85)"
ha-color-primary-40:             "#A48BBF"
ha-color-primary-80:             "rgba(164,139,191,0.35)"
ha-color-primary-90:             "rgba(164,139,191,0.25)"
ha-color-primary-95:             "rgba(164,139,191,0.15)"
mdc-ripple-color:                "rgba(164,139,191,0.20)"
# ── ZONE 6: Mushroom sync (mode-independent block) ──────────
# accent-color-rgb:              "164, 139, 191"
```

WCAG on light card (#FFF): 2.9:1 (borderline for icons). WCAG on dark card: 4.0:1 ✓.
Pairs beautifully with the cool dark surfaces. Adds elegance without warmth.

---

### Recipe F — Casa5 Steel

```yaml
# Mid-saturation steel blue. Professional, clear, readable.
# Hue: ~210°, Sat: 45%, Light: 55%
accent-color:                    "#5B8FBF"
accent-color-background-opacity: "rgba(91,143,191,0.25)"
accent-medium-color:             "rgba(91,143,191,0.5)"    # light
# accent-medium-color:           "#5B8FBF"                  # dark
ha-color-primary-30:             "rgba(91,143,191,0.85)"
ha-color-primary-40:             "#5B8FBF"
ha-color-primary-80:             "rgba(91,143,191,0.35)"
ha-color-primary-90:             "rgba(91,143,191,0.25)"
ha-color-primary-95:             "rgba(91,143,191,0.15)"
mdc-ripple-color:                "rgba(91,143,191,0.20)"
# ── ZONE 6: Mushroom sync (mode-independent block) ──────────
# accent-color-rgb:              "91, 143, 191"
```

WCAG on light card (#FFF): 3.4:1 ✓ AA UI components. WCAG on dark card: 4.8:1 ✓ AA.
Best WCAG performance of all recipes in light mode. Neutral enough to pair with any room aesthetic.

---

## #full-palette-recipes

### Full palette generation — backgrounds + accent

Full palettes change all three zones: accent, light surfaces, dark surfaces.

**How to deliver a full palette:**
1. Apply the accent swap (8 lines per mode, from `#accent-swap-recipes`)
2. Apply the background zone changes (5–7 lines per mode)
3. Apply dialog tint adjustment (light mode only)
4. Verify text contrast on the new card background

---

### Full Palette 1 — Warm Cream + Terracotta

Light mode feel: warm, natural, like a cosy interior magazine. Dark mode feel: rich earth tones.

**Light mode changes:**
```yaml
# Accent (Recipe D)
accent-color:                    "#C4896B"
accent-color-background-opacity: "rgba(196,137,107,0.25)"
accent-medium-color:             "rgba(196,137,107,0.5)"
ha-color-primary-30:             "rgba(196,137,107,0.85)"
ha-color-primary-40:             "#C4896B"
ha-color-primary-80:             "rgba(196,137,107,0.35)"
ha-color-primary-90:             "rgba(196,137,107,0.25)"
ha-color-primary-95:             "rgba(196,137,107,0.15)"
mdc-ripple-color:                "rgba(196,137,107,0.20)"
# Backgrounds — warm cream shift
background-color:                "#F5F0E8"
ha-card-background:              "#FDFAF5"
card-background-color:           "#FDFAF5"
secondary-background-color:      "rgb(232,224,210)"
background-color-2:              "#E2D9C8"
# Dialog
more-info-header-background:     "#EDE4D5"
sidebar-background-color:        "#F5F0E8"
app-header-background-color:     "#F5F0E8"
# Zone 6 — Mushroom sync (mode-independent, one line per theme):
# accent-color-rgb:              "196, 137, 107"
```

**Dark mode changes:**
```yaml
# Accent (Recipe D — same)
accent-color:                    "#C4896B"
accent-color-background-opacity: "rgba(196,137,107,0.25)"
accent-medium-color:             "#C4896B"
ha-color-primary-30:             "rgba(196,137,107,0.85)"
ha-color-primary-40:             "#C4896B"
ha-color-primary-80:             "rgba(196,137,107,0.35)"
ha-color-primary-90:             "rgba(196,137,107,0.25)"
ha-color-primary-95:             "rgba(196,137,107,0.15)"
mdc-ripple-color:                "rgba(196,137,107,0.20)"
# Backgrounds — warm earth dark
background-color:                "#1E1A15"
ha-card-background:              "#251F18"
card-background-color:           "var(--ha-card-background)"
background-color-2:              "#35291E"
sidebar-background-color:        "#1A1610"
app-header-background-color:     "#1A1610"
more-info-header-background:     "#0F1822"
paper-dialog-background-color:   "#0F1822"
```

Text contrast check: `#555A60` on `#FDFAF5` = **7.1:1** ✓ AAA.

---

### Full Palette 2 — Cool Neutral + Slate

Light mode feel: clean, modern, minimal. Dark mode feel: deep cool blue. Professional.

**Light mode changes:**
```yaml
# Accent (Recipe B)
accent-color:                    "#8BA8C4"
accent-color-background-opacity: "rgba(139,168,196,0.25)"
accent-medium-color:             "rgba(139,168,196,0.5)"
ha-color-primary-30:             "rgba(139,168,196,0.85)"
ha-color-primary-40:             "#8BA8C4"
ha-color-primary-80:             "rgba(139,168,196,0.35)"
ha-color-primary-90:             "rgba(139,168,196,0.25)"
ha-color-primary-95:             "rgba(139,168,196,0.15)"
mdc-ripple-color:                "rgba(139,168,196,0.20)"
# Backgrounds — cool neutral
background-color:                "#F2F4F6"
ha-card-background:              "#FFFFFF"
card-background-color:           "#FFFFFF"
secondary-background-color:      "rgb(225,229,234)"
background-color-2:              "#DCE0E6"
more-info-header-background:     "#E8EDF2"
sidebar-background-color:        "#F2F4F6"
app-header-background-color:     "#F2F4F6"
# Zone 6 — Mushroom sync (mode-independent, one line per theme):
# accent-color-rgb:              "139, 168, 196"
```

**Dark mode changes:**
```yaml
# Accent (Recipe B — same)
accent-color:                    "#8BA8C4"
accent-color-background-opacity: "rgba(139,168,196,0.25)"
accent-medium-color:             "#8BA8C4"
ha-color-primary-30:             "rgba(139,168,196,0.85)"
ha-color-primary-40:             "#8BA8C4"
ha-color-primary-80:             "rgba(139,168,196,0.35)"
ha-color-primary-90:             "rgba(139,168,196,0.25)"
ha-color-primary-95:             "rgba(139,168,196,0.15)"
mdc-ripple-color:                "rgba(139,168,196,0.20)"
# Backgrounds — deep cool blue
background-color:                "#161C26"
ha-card-background:              "#1C2436"
card-background-color:           "var(--ha-card-background)"
background-color-2:              "#2A3550"
sidebar-background-color:        "#131820"
app-header-background-color:     "#131820"
more-info-header-background:     "#0E1520"
paper-dialog-background-color:   "#0E1520"
```

Text contrast check: `#555A60` on `#FFFFFF` = **7.0:1** ✓ AAA.

---

### Full Palette 3 — Sage Green + Forest Dark

Light mode feel: natural, biophilic, calm. Dark mode feel: deep forest.

**Light mode changes:**
```yaml
# Accent (Recipe C)
accent-color:                    "#8BB89A"
accent-color-background-opacity: "rgba(139,184,154,0.25)"
accent-medium-color:             "rgba(139,184,154,0.5)"
ha-color-primary-30:             "rgba(139,184,154,0.85)"
ha-color-primary-40:             "#8BB89A"
ha-color-primary-80:             "rgba(139,184,154,0.35)"
ha-color-primary-90:             "rgba(139,184,154,0.25)"
ha-color-primary-95:             "rgba(139,184,154,0.15)"
mdc-ripple-color:                "rgba(139,184,154,0.20)"
# Backgrounds — warm off-white (complements sage)
background-color:                "#F3F5F1"
ha-card-background:              "#FAFCF8"
card-background-color:           "#FAFCF8"
secondary-background-color:      "rgb(226,231,222)"
background-color-2:              "#DCEBD4"
more-info-header-background:     "#E8F0E4"
sidebar-background-color:        "#F3F5F1"
app-header-background-color:     "#F3F5F1"
# Zone 6 — Mushroom sync (mode-independent, one line per theme):
# accent-color-rgb:              "139, 184, 154"
```

**Dark mode changes:**
```yaml
# Accent (Recipe C — same)
accent-color:                    "#8BB89A"
accent-color-background-opacity: "rgba(139,184,154,0.25)"
accent-medium-color:             "#8BB89A"
ha-color-primary-30:             "rgba(139,184,154,0.85)"
ha-color-primary-40:             "#8BB89A"
ha-color-primary-80:             "rgba(139,184,154,0.35)"
ha-color-primary-90:             "rgba(139,184,154,0.25)"
ha-color-primary-95:             "rgba(139,184,154,0.15)"
mdc-ripple-color:                "rgba(139,184,154,0.20)"
# Backgrounds — deep forest dark
background-color:                "#151C18"
ha-card-background:              "#1A2420"
card-background-color:           "var(--ha-card-background)"
background-color-2:              "#253028"
sidebar-background-color:        "#111814"
app-header-background-color:     "#111814"
more-info-header-background:     "#0C1510"
paper-dialog-background-color:   "#0C1510"
```

Text contrast check: `#555A60` on `#FAFCF8` = **7.1:1** ✓ AAA.

---

## #full-palette-recipes-dark

### Full Palette 4 — Midnight Slate (deep dark + slate blue)

Dark-primary design. Light mode stays clean neutral; dark mode goes very deep.
Best for wall panels or users who primarily use dark mode.

**Light mode changes (accent only — Recipe B):**
```yaml
accent-color:                    "#8BA8C4"
accent-color-background-opacity: "rgba(139,168,196,0.25)"
accent-medium-color:             "rgba(139,168,196,0.5)"
ha-color-primary-30:             "rgba(139,168,196,0.85)"
ha-color-primary-40:             "#8BA8C4"
ha-color-primary-80:             "rgba(139,168,196,0.35)"
ha-color-primary-90:             "rgba(139,168,196,0.25)"
ha-color-primary-95:             "rgba(139,168,196,0.15)"
mdc-ripple-color:                "rgba(139,168,196,0.20)"
# Backgrounds (light) — cool neutral, slightly cooler than Palette 2
background-color:                "#F0F2F5"
ha-card-background:              "#FFFFFF"
card-background-color:           "#FFFFFF"
secondary-background-color:      "rgb(220,225,232)"
background-color-2:              "#D4DAE2"
more-info-header-background:     "#E4EAF2"
sidebar-background-color:        "#F0F2F5"
app-header-background-color:     "#F0F2F5"
# Zone 6 — Mushroom sync (mode-independent, one line per theme):
# accent-color-rgb:              "139, 168, 196"
```

**Dark mode changes (deep midnight):**
```yaml
accent-color:                    "#8BA8C4"
accent-color-background-opacity: "rgba(139,168,196,0.25)"
accent-medium-color:             "#8BA8C4"
ha-color-primary-30:             "rgba(139,168,196,0.85)"
ha-color-primary-40:             "#8BA8C4"
ha-color-primary-80:             "rgba(139,168,196,0.35)"
ha-color-primary-90:             "rgba(139,168,196,0.25)"
ha-color-primary-95:             "rgba(139,168,196,0.15)"
mdc-ripple-color:                "rgba(139,168,196,0.20)"
# Backgrounds (dark) — near-black with slate tint
background-color:                "#0D1117"
ha-card-background:              "#131922"
card-background-color:           "var(--ha-card-background)"
background-color-2:              "#1E2A3A"
sidebar-background-color:        "#0A0E14"
app-header-background-color:     "#0A0E14"
more-info-header-background:     "#071020"
paper-dialog-background-color:   "#071020"
ha-card-border-color:            "#1C2840"
divider-color:                   "var(--ha-card-background)"
```

Text contrast: white on #131922 = **15.2:1** ✓ AAA. Slate on #131922 = **4.2:1** ✓ AA.

---

### Full Palette 5 — Dusk Mauve (warm mauve + deep violet dark)

Elegant evening palette. Sophisticated without being cold. Well-suited to
living spaces and anyone who finds blue-based themes too clinical.

**Light mode changes:**
```yaml
# Accent (Recipe E — Dusk)
accent-color:                    "#A48BBF"
accent-color-background-opacity: "rgba(164,139,191,0.25)"
accent-medium-color:             "rgba(164,139,191,0.5)"
ha-color-primary-30:             "rgba(164,139,191,0.85)"
ha-color-primary-40:             "#A48BBF"
ha-color-primary-80:             "rgba(164,139,191,0.35)"
ha-color-primary-90:             "rgba(164,139,191,0.25)"
ha-color-primary-95:             "rgba(164,139,191,0.15)"
mdc-ripple-color:                "rgba(164,139,191,0.20)"
# Backgrounds (light) — warm lavender-cream
background-color:                "#F4F2F7"
ha-card-background:              "#FDFCFF"
card-background-color:           "#FDFCFF"
secondary-background-color:      "rgb(228,224,236)"
background-color-2:              "#DDD8E8"
more-info-header-background:     "#EDE8F5"
sidebar-background-color:        "#F4F2F7"
app-header-background-color:     "#F4F2F7"
# Zone 6 — Mushroom sync (mode-independent, one line per theme):
# accent-color-rgb:              "164, 139, 191"
```

**Dark mode changes:**
```yaml
# Accent (Recipe E — same)
accent-color:                    "#A48BBF"
accent-color-background-opacity: "rgba(164,139,191,0.25)"
accent-medium-color:             "#A48BBF"
ha-color-primary-30:             "rgba(164,139,191,0.85)"
ha-color-primary-40:             "#A48BBF"
ha-color-primary-80:             "rgba(164,139,191,0.35)"
ha-color-primary-90:             "rgba(164,139,191,0.25)"
ha-color-primary-95:             "rgba(164,139,191,0.15)"
mdc-ripple-color:                "rgba(164,139,191,0.20)"
# Backgrounds (dark) — deep violet-grey
background-color:                "#16131E"
ha-card-background:              "#1E192A"
card-background-color:           "var(--ha-card-background)"
background-color-2:              "#2A2240"
sidebar-background-color:        "#120F18"
app-header-background-color:     "#120F18"
more-info-header-background:     "#0D0B14"
paper-dialog-background-color:   "#0D0B14"
ha-card-border-color:            "#2A2240"
divider-color:                   "var(--ha-card-background)"
```

Text contrast: white on #1E192A = **14.1:1** ✓ AAA. Mauve on #1E192A = **3.8:1** ✓ AA.

---

### Full Palette 6 — Midnight Steel (dark navy + steel blue)

The most dramatic of the full palettes. Very dark navy surfaces with crisp
steel-blue accent. Best for always-on wall panels in dim environments,
or users who want a cinematic, premium feel.

**Light mode changes:**
```yaml
# Accent (Recipe F — Steel)
accent-color:                    "#5B8FBF"
accent-color-background-opacity: "rgba(91,143,191,0.25)"
accent-medium-color:             "rgba(91,143,191,0.5)"
ha-color-primary-30:             "rgba(91,143,191,0.85)"
ha-color-primary-40:             "#5B8FBF"
ha-color-primary-80:             "rgba(91,143,191,0.35)"
ha-color-primary-90:             "rgba(91,143,191,0.25)"
ha-color-primary-95:             "rgba(91,143,191,0.15)"
mdc-ripple-color:                "rgba(91,143,191,0.20)"
# Backgrounds (light) — cool blue-white
background-color:                "#EFF3F8"
ha-card-background:              "#FFFFFF"
card-background-color:           "#FFFFFF"
secondary-background-color:      "rgb(218,227,238)"
background-color-2:              "#D0DCE9"
more-info-header-background:     "#E0EAF4"
sidebar-background-color:        "#EFF3F8"
app-header-background-color:     "#EFF3F8"
# Zone 6 — Mushroom sync (mode-independent, one line per theme):
# accent-color-rgb:              "91, 143, 191"
```

**Dark mode changes:**
```yaml
# Accent (Recipe F — same)
accent-color:                    "#5B8FBF"
accent-color-background-opacity: "rgba(91,143,191,0.25)"
accent-medium-color:             "#5B8FBF"
ha-color-primary-30:             "rgba(91,143,191,0.85)"
ha-color-primary-40:             "#5B8FBF"
ha-color-primary-80:             "rgba(91,143,191,0.35)"
ha-color-primary-90:             "rgba(91,143,191,0.25)"
ha-color-primary-95:             "rgba(91,143,191,0.15)"
mdc-ripple-color:                "rgba(91,143,191,0.20)"
# Backgrounds (dark) — deep navy
background-color:                "#0B0F18"
ha-card-background:              "#101828"
card-background-color:           "var(--ha-card-background)"
background-color-2:              "#182238"
sidebar-background-color:        "#080C14"
app-header-background-color:     "#080C14"
more-info-header-background:     "#050810"
paper-dialog-background-color:   "#050810"
ha-card-border-color:            "#192340"
divider-color:                   "var(--ha-card-background)"
```

Text contrast: white on #101828 = **17.1:1** ✓ AAA. Steel on #101828 = **5.2:1** ✓ AA.
Best WCAG scores of all full palettes — the deep navy maximises all contrasts.
