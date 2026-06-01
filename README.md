# ha-bubble-dashboard

A Claude skill library for building Home Assistant dashboards with **Bubble Card**, **Streamline Card**, **Sidebar Card**, and **Mushroom Cards** — anchored to the Casa5HeyneV2 merged HA/Bubble Card/Mushroom CSS theme.

This skill teaches Claude to generate complete, production-quality Lovelace YAML, HA theme files, and colour palettes — with WCAG contrast checking, single-mode wall-panel support, Mushroom state-colour integration, and a full troubleshooting reference.

---

## What this skill covers

| Area | What Claude can do |
|------|--------------------|
| **Dashboard layout** | sections view, pop-ups, HBS footer nav, panel view for wall panels |
| **Bubble Card** | all card types, RGB lights, sub-buttons, modules, JS templates |
| **Streamline Card** | templates, variable syntax, UI-mode vs YAML-mode, DRY decision |
| **Sidebar Card** | desktop nav, clock/date/Jinja2 messages, fallback patterns |
| **Mushroom Cards** | chip bar, template chips, full state-colour integration with HA theme |
| **CSS themes** | complete Casa5HeyneV2 variant generation, accent-only or full palette swap |
| **Colour intelligence** | WCAG contrast checks, harmony rules, 12 ready-made palette recipes |
| **Typography** | font loading (CDN, self-hosted, system), wall-panel size overrides |
| **Troubleshooting** | symptom → cause → fix tables for every common failure mode |

---

## File structure

```
ha-bubble-dashboard/
├── README.md                           ← you are here
├── SKILL.md                            ← main skill file (iron laws, process, §§1–8)
├── CHANGELOG.md                        ← version history and update triggers
├── available-skills-entry.md           ← system prompt entry for disk-based usage
│
├── references/
│   ├── bubble-card-ref.md              ← all card types, CSS vars, JS API, version compat
│   ├── casa5heynev2-template.yaml      ← canonical base theme (copy + diff to generate variants)
│   ├── colour-intelligence-ref.md      ← palette recipes, WCAG checks, advisory flow
│   ├── css-theme-ref.md                ← full HA/Bubble var() chain catalogue
│   ├── mushroom-theme-ref.md           ← Mushroom ↔ HA integration, chip cards, template chip
│   ├── recipes-extended.md             ← security, energy, vacuum, bathroom, garage, office
│   ├── sidebar-ref.md                  ← all options, menu config, known issues
│   ├── streamline-ref.md               ← template anatomy, variable syntax, JS keys
│   ├── test-dashboard.yaml             ← importable dashboard assembling core recipes
│   ├── troubleshooting-ref.md          ← symptom → cause → fix tables
│   └── typography-ref.md               ← font loading, recipes, wall-panel sizes
│
└── theme/
    └── Casa5HeyneV2.yaml               ← the base theme — copy to /config/themes/
```

---

## Two ways to use this skill

### Option A — On disk (Claude computer-use / custom system prompt)

For setups where Claude has file system access (Claude computer-use tool, Claude Code, or custom integrations):

1. Copy the `ha-bubble-dashboard/` folder to `/mnt/skills/user/ha-bubble-dashboard/`
2. Paste the contents of `available-skills-entry.md` into the `<available_skills>` block of your Claude system prompt
3. Claude will load the skill automatically when it detects a relevant request

The `available-skills-entry.md` contains the trigger conditions and symptom patterns that tell Claude when to load the skill. Without it in the system prompt, Claude won't know the skill exists.

### Option B — Uploaded directly to Claude (Projects)

For claude.ai Projects or any setup where you upload files as project knowledge:

1. Upload all `.md` files (SKILL.md + all references/) as project knowledge documents
2. Upload `references/casa5heynev2-template.yaml` as a project knowledge file
3. **The `available-skills-entry.md` is not needed** — files uploaded to a Project are always in context

**Differences when uploaded directly:**
- All reference files are always in Claude's context window simultaneously (higher token usage but no navigation needed)
- Claude doesn't need trigger conditions — it can see the skill content directly
- The process flow and iron laws in SKILL.md still guide Claude's behaviour
- Recommended upload order: SKILL.md first, then reference files alphabetically

---

## Required HA components

All via [HACS](https://hacs.xyz):

| Component | Type | Notes |
|-----------|------|-------|
| [Bubble Card](https://github.com/Clooos/Bubble-Card) | Frontend | Min v3.2.0 |
| [Bubble Card Tools](https://github.com/Clooos/Bubble-Card) | Integration | Enables module system |
| [Streamline Card](https://github.com/brunosabot/streamline-card) | Frontend | Min v0.2.2 |
| [Sidebar Card](https://github.com/DBuit/sidebar-card) | Frontend | Custom repo — add manually |
| [Mushroom](https://github.com/piitaya/lovelace-mushroom) | Frontend | Optional — enables chip cards |

Sidebar Card custom repository URL: `https://github.com/DBuit/sidebar-card`

---

## The base theme

`theme/Casa5HeyneV2.yaml` is a merged HA + Bubble Card + Mushroom theme with:
- Full `var()` chain — all Bubble Card colours point to HA theme variables
- ZONE 6 Mushroom bridge — entity-domain state colours (lights, fans, climate, etc.) wired to HA theme
- Alexandria variable-weight font via Google Fonts CDN
- Six palette zones with search markers for easy accent and full-palette swaps
- Light and dark mode, both complete

**To install the theme:**
1. Copy `Casa5HeyneV2.yaml` to `/config/themes/`
2. Add to `configuration.yaml`:
   ```yaml
   frontend:
     themes: !include_dir_merge_named themes
     extra_module_url:
       - /local/alexandria-font.js
   ```
3. Create `/config/www/alexandria-font.js` — see `references/typography-ref.md#alexandria`
4. Restart HA → Developer Tools → Actions → `frontend.reload_themes`
5. Profile → Theme → `Casa5HeyneV2`

---

## Colour palette system

The skill includes a full colour intelligence layer:

- **6 accent swap recipes** (A–F): Slate, Sage, Terracotta, Dusk, Steel, Original — each 8 lines per mode
- **6 full palette recipes** (1–6): complete light + dark variants changing backgrounds, surfaces, and accent
- **WCAG pre-flight**: all accent ratios pre-calculated against the Casa5 light and dark card surfaces
- **Advisory mode**: Claude presents options with rationale, user picks
- **Prescriptive mode**: Claude maps a mood description to the closest recipe and generates
- **Bring your own hex**: template for any custom colour with hex→RGB conversion steps

---

## Version

Current: **v1.5**  
Component pins: Bubble Card 3.2.1 · Bubble Card Tools 1.0.2 · Streamline Card 0.2.2 · Sidebar Card 0.1.9.9 · HA minimum 2024.3.0

See `CHANGELOG.md` for full version history and update triggers.

---

## License

MIT — free to use, modify, and distribute. Attribution appreciated.
