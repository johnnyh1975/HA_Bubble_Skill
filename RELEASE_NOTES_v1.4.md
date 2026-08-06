# ha-bubble-dashboard v1.4

**Ecosystem alignment, native-first guidance, and structural cleanup.**

Verified against Bubble Card v3.2.5 source, Mushroom v5.2.2 source, and
Home Assistant release notes through 2026.7.

---

## Highlights

- 🏠 **Native-first check** — before building battery grids, security logs,
  weather forecasts or media transport controls, the skill now checks whether
  native HA (Maintenance dashboard, Security Activity list, tile card
  features) already covers it — and says so, as an advisory.
- 🔀 **Native card interop** — guidance for mixing native tile / heading /
  area cards into Bubble dashboards: what inherits from the Casa5HeyneV2
  theme automatically, what doesn't, and when the native card is the better
  pick.
- 🧭 **Masonry → sections migration guide** — a safe don't-convert-in-place
  workflow with a construct-by-construct mapping table.
- 📋 **Entity inventory snippet** — a one-off Developer Tools → Template
  evaluation that produces an area-grouped, device-class-annotated entity
  list for the classification workflow.
- 🧱 **Module authoring reference** — new `module-authoring-ref.md` with the
  full Bubble Card editor-schema field catalog, the v3.2.4 object selector
  (groups, conditional fields, variants), and the module sharing/export
  format — built from and verified against actual v3.2.4 source.

## Bubble Card v3.2.5 — cover tilt

- 🪟 **Cover tilt support** (the v3.2.5 headline feature) is fully
  documented: `tilt_buttons` (top / bottom / left / right / hidden),
  `open_tilt_service`, `close_tilt_service`, plus
  `cover_slider_type: tilt_position` to drive tilt from the card slider or a
  slider sub-button. Includes the feature-detection rule — tilt options are
  only emitted when the entity actually reports tilt support — and two
  troubleshooting entries for the common failure modes.
- Pop-up fixes noted in the compat table: the shared `hui-card` is no longer
  hidden inside grid/masonry layout boundaries, and pop-up shells detach
  properly when leaving editor mode.

## 24 previously undocumented options

The v3.2.4 verification pass scanned editor schemas only — which misses every
YAML option the editor doesn't surface. A full source scan closed the gap:

- **Slider:** `slider_value_position`, `relative_slide`,
  `invert_slider_value`, `hue_force_saturation` (+ `_value`),
  `cover_slider_type`
- **sub-buttons card:** `menu_style`, `labels_below`, `hide_button_labels`,
  `compact_mode`, `space_between_buttons`, `footer_width` — including the
  trap that `labels_below` does nothing without `menu_style: true`
- **Calendar:** `event_action`, `show_place`, `show_started_events`
- **Core / climate:** `show_last_updated`, `sub_button_justify_content`,
  `hide_temperature`

## Corrections

- 🎨 **Iron Law violation in the skill's own calendar example.** It used a
  hardcoded hex. Bubble Card resolves a colour *name* to
  `var(--<name>-color)`, so `color: accent` was available all along. Fixed,
  documented, and added to Common Pitfalls.
- ❌ **`mush-rgb-state-switch` does not exist** in Mushroom. Switch entities
  are coloured by `mush-rgb-state-entity`. Removed from docs and theme.
- ❌ **`mush-rgb-primary` does not exist** either. The accent bridge now
  wires `accent-color-rgb` into the specific state variables.
- ➕ Added the missing Mushroom state groups (vacuum, media-player, lock and
  its three sub-states, number, humidifier, update) — including the upstream
  quirk that `mush-rgb-update-off` / `-installing` carry no `state-` segment.
- 🔧 **Theme divergence resolved.** The shipped `Casa5HeyneV2.yaml` was
  missing the entire ZONE 6 state mapping (45 keys), and its light mode had
  none of the `mush-rgb-*` colours the dark mode had — Mushroom silently fell
  back to its own defaults in light mode. Both theme files are now aligned
  and YAML-validated.

## Bubble Card v3.2.4 compatibility

- Version-compat table extended with v3.2.3 (smart entity/card suggestions
  via the HA 2026.6 picker, `close_action` navigation fix, iOS pop-up
  visibility fix) and v3.2.4 (standalone pop-ups reliable inside
  `vertical-stack`, explicit pop-up-in-pop-up warning).
- Full scan of all v3.2.4 card editor schemas against the reference — no
  undocumented YAML-facing options; all documented options confirmed.
- New troubleshooting section `#nested-popup-warning` distinguishing true
  pop-up-in-pop-up nesting (always unsupported) from pop-ups inside
  vertical stacks (fixed in v3.2.4 — just update).
- Corrected module-authoring documentation: removed a `variables:` +
  `{{mustache}}` pattern that does not exist in Bubble Card's module system,
  and the non-existent `supported: [all]` literal.

## Native HA alignment (researched against HA 2026.1–2026.7)

- New `dashboard-system.md#native-first` — the native-first check table plus
  "when is a custom Bubble dashboard worth it?" positioning against the
  native Home dashboard (the default for new installs since HA 2026.2), and
  hybrid-setup guidance. Advisory tone throughout — the user always decides.
- New `dashboard-system.md#native-interop` — theme inheritance rules for
  native cards, Bubble-mechanism boundaries (`--bubble-*` vars and modules
  don't apply), visual grouping rules, and the Iron Law extended to native
  card YAML.
- Health-check mode gained a native-feature advisory category (Advisory
  only — never Critical or Significant).
- New `streamline-ref.md#maintenance-status` — an honest project-health note
  (single-maintainer adaptation of the unmaintained decluttering-card) with
  the graceful degradation path and a recommend-only-when-DRY-is-real rule.
- Paid-module boundary rule: Patreon-distributed Bubble Card modules
  (Bubble Badges 2, Bubble Weather, Custom Dropdown…) are never reproduced —
  the skill explains, routes to the Module Store/Patreon, or authors an
  original module instead.

## New capabilities

- `dashboard-system.md#entity-inventory` — the Collect step, made easy.
- `dashboard-system.md#masonry-migration` — old masonry dashboards →
  sections view, including the `card_layout` default change gotcha.
- `dashboard-system.md#wall-panel-hardening` — burn-in, screen-off
  automation handoff, kiosk-mode / Fully Kiosk pointers (named, not
  configured), dedicated non-admin user, stale-cache reliability.

## Tooling

- 🔍 **`verify.py`** — a structural self-check you can run before any release:
  `python3 verify.py`. Eight checks (anchor integrity, anchor-list sync, YAML
  validity, theme light/dark symmetry, nonexistent component variables, Iron
  Law in card examples, version consistency, orphan files). Each one exists
  because that bug class shipped at least once. It caught five stale anchor
  entries and a version drift on its first run.
- 🧪 **`references/eval-set.md`** — ten behavioural regression prompts with
  MUST / MUST NOT criteria, run in fresh conversations. Structural checks
  prove the library is sound; these prove it changes behaviour.

## Coverage and honesty

- 🧭 **Entity domain map extended** with `siren`, `remote` and `lawn_mower`
  (a Bubble Card toggle domain with a built-in icon that was missing), plus
  explicit "no Bubble support, use the native tile" entries for `valve`,
  `water_heater`, `todo` and `image`. The toggle and slider domain lists from
  v3.2.5 source are now documented, so an unsupported domain gets an honest
  answer instead of a control that renders but never toggles.
- ♿ **Accessibility limits stated plainly.** Bubble Card's div-based controls
  are not screen-reader operable, sliders expose no role or value, tap targets
  sit outside the tab order, and pop-ups do not trap focus. No card option
  fixes this — so the skill now says so and offers native tile cards, voice
  or automation instead, and never claims WCAG conformance from contrast
  checks alone.
- 🌍 **Localisation rule.** Dashboard labels are generated in the user's
  language; navigation hashes stay ASCII; entity friendly names win where a
  voice assistant is in use.
- ✅ **Test dashboard is now a real smoke test** — all 11 documented card types
  (was 8), including a tilt-enabled cover. Two defects fixed along the way:
  a stale version string, and an HBS footer that was not the last top-level
  card, violating a rule the skill itself enforces.

## Structural cleanup

- **Theme de-duplication.** `references/casa5heynev2-template.yaml` is gone;
  `theme/Casa5HeyneV2.yaml` is the single source for both theme generation and
  user installation. The two copies had drifted twice — the shipped file was
  missing the entire ZONE 6 mapping, and mode-specific greys disagreed.
- Deleted `references/dashboard-recipes.md` (~50 KB) — a verified 100%
  duplicate of content inside `dashboard-system.md`, referenced nowhere.
- Deduplicated the Overview and Rooms view YAML: `recipes-5view.md`
  Recipes 8–9 are now the single YAML source; `dashboard-system.md` keeps
  design rationale, structure diagrams and component notes. The scaffolds
  for Scenes / Activity / Settings / Energy / Music intentionally remain in
  `dashboard-system.md` — their recipes summarise patterns and point there.
- CHANGELOG now opens with a standing per-HA-release verification checklist
  (monthly HA releases broke frontend assumptions twice in 2026 already).
- README and `available-skills-entry.md` brought fully up to date with the
  new triggers, symptoms, and file inventory.

## Component pins

| Component | Version |
|---|---|
| Bubble Card | 3.2.5 |
| Bubble Card Tools | 1.0.2 |
| Streamline Card | 0.2.2 |
| Sidebar Card | 0.1.9.9 |
| HA minimum | 2024.3.0 |
| Mushroom | 5.2.2 (verified) |
| Guidance verified against | HA 2026.7 |

## Upgrade notes

- **File removed:** `references/dashboard-recipes.md`. If you sync the skill
  folder rather than replacing it, delete this file manually — a stale copy
  reintroduces the divergence risk this release eliminates.
- **Theme file updated.** `Casa5HeyneV2.yaml` gained the ZONE 6 Mushroom
  state mapping and light-mode colour parity. Re-copy it to
  `/config/themes/` and run `frontend.reload_themes`. Existing dashboards and
  card YAML are unaffected — this only changes theme variables.
- If you previously copied `mush-rgb-state-switch` or `mush-rgb-primary` into
  a custom theme, remove them: they never did anything.
- **File removed:** `references/casa5heynev2-template.yaml`. If you referenced
  it in a Project upload or a script, point at `theme/Casa5HeyneV2.yaml`
  instead — it is the same theme, now the only copy.
- 22 files total.

**Full changelog:** see `CHANGELOG.md`.
