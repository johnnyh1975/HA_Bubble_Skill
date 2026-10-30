# ha-bubble-dashboard — Changelog


## Standing check — run on every HA minor release

Monthly HA releases have repeatedly broken frontend assumptions (2026.5:
editor fields + iOS pop-up DOM change; 2026.1: mobile navigation overhaul).
On each HA minor release, verify before trusting the skill's guidance:

- [ ] Pop-up rendering and visibility (sections-layout DOM changes)
- [ ] Bubble Card editor fields present (HA form-schema changes)
- [ ] Sidebar Card `showTopMenuOnMobile` / native mobile nav behaviour
- [ ] Card-suggestion registration still functioning (HA 2026.6+ picker)
- [ ] New native dashboard features that extend the `#native-first` table
      (Maintenance/Security dashboards, tile card features, heading card)
- [ ] Bubble Card / Streamline / Sidebar / Bubble Card Tools version pins

**When verifying a component release, scan the source tree — not the release
notes and not the editor schemas alone.** Editor-only scans miss every
YAML-facing option the editor doesn't surface; a `config.*` grep across
`src/` is the reliable method. The same applies to CSS variables: check the
actual `var()` fallback chain in source rather than trusting documentation.

---

## v1.8 — 2026-10-30

Bubble Card v3.4.0 → **v3.4.2** and Statistics Graph Chart Card v4.02 →
**v4.08**. Verified against the v3.4.2 source tree (full `src/` diff, 44
changed files plus 10 new ones) and the SGCC README diff. HA pin moved to
2026.10.

### Four defects in the skill's own guidance

Found while diffing, not while reading release notes — all four had shipped:

- **`select_attribute: percentage` on a fan and `select_attribute: mode` on a
  humidifier were both wrong**, in the `#entity-domain-map` table and in a
  worked example. `select_attribute` reads a closed list of names hard-coded in
  `src/components/dropdown/lists.js`; neither of those is on it, and neither
  ever was. The failure is silent — the card renders options only when the
  attribute is an array and renders none otherwise, so a copied example gave an
  empty dropdown with no console error. New `bubble-card-ref.md#select-attribute`
  documents all fourteen valid names with their services, and the fan example
  now uses a slider.
- **`popup_style: home-assistant` was undocumented entirely.** The skill listed
  two values (`bubble`, `classic`); the source has three, and the third was
  already in the v3.4.0 README — so this was missed in the v1.7 round, not
  newly introduced. It matters more now because v3.4.2 changed its mobile
  height behaviour.
- **`popup_mode` listed `adaptive-dialog` twice** and omitted the fact that
  only two of its four values are read with the HA style.
- **The `--bubble-footer-width` caveat was imprecise** — it lumped the themeable
  knob together with the runtime-derived `--bubble-footer-resolved-width`.

### Bubble Card 3.4.0 → 3.4.2

- **Four new `select_attribute` lists** (v3.4.2): `fan_speed_list` (vacuum →
  `vacuum.set_fan_speed`), `activity_list` (remote → `remote.turn_on`),
  `direction` (fan, gated on the `SET_DIRECTION` feature bit) and
  `alarm_modes` (alarm panel). Two of them are *computed*, not read from
  attributes: `direction`'s options come from HA, and `alarm_modes` is built
  from `supported_features`.
- **The alarm keypad has three routes, not one.** A numeric code on HA frontend
  2026.3+ gets a 12-key keypad inside the dropdown menu; a code with letters,
  or an older frontend, opens the more-info dialog instead; a default code
  stored on the entity skips the prompt. Documented as a table, because
  promising an in-card keypad without checking the frontend version is wrong
  most of the time on older installations.
- **`slide_to_close`** (v3.4.1): `true` / `header` / `false`. `header` is the
  answer to a pop-up holding a map or a chart, where the dismiss gesture fights
  the content. Ignored below v3.4.1 — the gesture stays on there.
- **`popup_style: home-assistant` mobile height changed** (v3.4.2) and this is
  a **behaviour change on upgrade**: the sheet now takes the full more-info
  height unless `popup_mode: adaptive-dialog`. Before v3.4.2 the editor
  disabled the mode control for this style and the sheet followed its content,
  so an existing pop-up with no `popup_mode` changes look when the user
  updates. `popup_mode: centered` is not read at all with this style.
- **`with_bottom_offset`** now also applies with the HA style in any mode,
  because that style is a sheet on a narrow screen whatever its mode says.
- **Calendar card: two changes worth generating differently.**
  `event_action.tap_action` now defaults to `more-info` (was `none`), and that
  `more-info` opens **HA's event dialog** with the event's description and
  location — not the calendar entity's more-info, which only knows the next
  event. The card also subscribes to the event list over the WebSocket, so an
  event edited or deleted further out updates at once; before v3.4.2 only a
  change to the *next* event refreshed it, which is why a wall panel could show
  a cancelled appointment all day. `days` now also sets the subscription
  window.
- **`subButtonState[]` indexing was broken until v3.4.2** (#2165) and the skill
  documented it as if it were not. The walk read ungrouped `main` buttons, then
  every group, and **never read the ungrouped `bottom` ones at all** — so on
  v3.1–v3.4.1 it disagreed with `subButtonIcon[]` on any card mixing groups
  with loose sub-buttons, and some buttons had no index. Now version-gated,
  with the advice to read through `hass` below v3.4.2.
- **`footer_width` behaviour changed** (v3.4.2, #2620). Below a 600 px viewport
  the footer used to be forced full width, discarding a configured width — so
  the same 300 px footer obeyed the setting in landscape and ignored it in
  portrait. It is now clamped to `min(footer_width, content − 16px)`. Any
  `styles:` workaround written for the old behaviour should be removed.
- **Sub-button contrast is now measured, not thresholded** (v3.4.1). New
  `--bubble-sub-button-light-text-color`; `--bubble-sub-button-dark-text-color`
  softened its default from `rgb(0,0,0)` to `rgba(0,0,0,0.65)`. **A `styles:`
  override written to force icon contrast on a light sub-button now fights a
  correct answer** — the guidance says to delete it. Added as a pitfall, since
  the instinct to add one is strong.
- **Render gate rebuilt** (v3.4.2) with a documented symptom attached. v3.4.0
  compared a fixed list of `hass` keys which omitted HA's *formatters* — those
  arrive once translations load, so a card could render a **raw state**
  (`heat_cool` rather than "Heat/Cool") until something made it render again.
  v3.4.2 compares identity across everything outside `states` and skips nothing
  for 10 s after connect or reconnect, measured upstream at 50–70 ms extra on a
  31-card dashboard under a 4× CPU throttle. The fix for that symptom is an
  update, not a template.
- **Sidebar offset mechanism changed at HA 2026.6**, which rewrites part of
  `#wall-panel-hardening`. HA now publishes `--ha-sidebar-width` itself and
  Bubble Card reads it directly — no measuring runs, and kiosk mods cooperate
  by construction because they change that same variable. Below 2026.6 the
  panel is measured, as before. Consequence for themes:
  `--bubble-content-inline-start` **is** settable in a theme on 2026.6+, where
  nothing overwrites it.
- **Four wall-panel defects fixed in v3.4.2**, now a table in
  `#wall-panel-hardening`: a slider sub-button's document listener leaked a
  card per re-layout (the "page gets heavier over days" report); a triggered
  pop-up stayed open after a tablet woke because a rebuilt card took its first
  look for a page load; a third-party card rebuilding the view mid-close
  (#2589) orphaned a bottom-sheet header for the session; and HA's custom-state
  polyfill on Safari < 17.4 made dropdowns inert (#2663) — an old iPad symptom.
- **Legacy pop-up migration now covers `grid` containers**, and the migrated
  standalone pop-up inherits the container's `grid_options` / `layout_options` /
  `view_layout` and merges its `visibility:` conditions. A `grid` whose parent
  key is `sections` or `views` is correctly *not* treated as a container.
- **HA 2026.10 interop**: the conditions editor re-adds an already-ticked user
  to a `condition: user` on each rebuild (#2657); v3.4.2 drops the repeats.
  Also fixed: config-deep-copying plugins (UIX, layout-card) breaking that
  editor.
- Six new troubleshooting rows covering the above symptoms, each pointing at
  "update" rather than at a YAML workaround.

### Statistics Graph Chart Card 4.02 → 4.08

- **The version is readable after all.** `#sgcc-status` said the pin was "an
  era, not a version" because the bundle is minified. Minification does not
  strip the string table: `grep -o "'4\.[0-9][0-9]'"` on the bundle reports it.
  The pin is now `4.08`, and `check_upstream.py`'s note carries the command
  instead of "check manually". The source-review caveat stands unchanged — a
  minified bundle still cannot be audited, patched or forked.
- **`axis_style: native`** (v4.03/4.04) — draws axes, grid and the per-entity
  legend exactly as HA's own charts do, in `--primary-text-color` and
  `--divider-color`. Promoted deliberately: it is the single option that stops
  a custom graph card reading as foreign next to native cards, which is the
  usual case in a sections view.
- **`graph_group` chart pages** (v4.08) — entities sharing a group name are
  drawn on a page of their own, with a dot strip under the graph. One fetch,
  one grid cell and one picker for what used to be N near-identical cards. This
  is the real space lever on a graphs view, so it gets a worked example.
- **`sync_group` and the controller card** (v4.03) — one visible picker drives
  every card in the group; receivers need no picker. Removes N−1 copies of the
  same chrome, which is the calm-technology argument for it.
- **`include_area_names` / `use_only_area_name`** (v4.07) — documented against
  the Advanced History interop it was built for. Advanced History picks targets
  by area and device, so a whole-floor selection arrives as four series all
  called "Temperature"; this option is upstream's own answer, and it beats
  renaming entities (`#entity-rename-risk`).
- **Per-entity `enabled:`** — cross-referenced into `streamline-ref.md`,
  because upstream documents it as built for Streamline: the entity id is not
  even validated when disabled, so an unsubstituted `[[placeholder]]` is
  harmless. Added to the "this instance lacks that sensor" options, ahead of
  forking a template.
- **Iron Law surface widened.** v4.05 added a `styles` block of plain CSS
  (card-mod class names, no card-mod needed) plus `card_background_color`,
  `card_border_*`, `card_padding`, `card_shadow` and `card_header_color`. All
  of it is Iron Law surface and all of it invites a hex literal. Also recorded:
  the `card_*` options are applied **inline**, so a `styles` rule for the same
  property needs `!important` — don't set both.

### Eval set: 18 → 21 cases

Same selection criterion as 13–18, pushed one step further: in each of the
three, the **user's own wording describes the wrong answer**.

- `#eval-19-select-attribute` — a fan "von 0 bis 100 %" and a request for a
  dropdown. Every surface signal says `select_attribute: percentage`; the
  entity really has that attribute; the result is an empty dropdown with no
  error.
- `#eval-20-ha-style-popup` — a pop-up that changed height after an update,
  with `popup_mode: centered` in the config. The obvious reading is that the
  named mode stopped working. The truth is that it was never read.
- `#eval-21-sgcc-styling` — two hex codes handed over, for options named after
  exactly the properties they describe. The compliant-looking answer is the
  non-compliant one.

### CI

- `token_budget.py --check` caught SKILL.md going 15 tokens over budget on the
  first pass. Resolved by **consolidating** rather than raising the budget:
  two of six new Signal Scan rows merged into neighbours, one new pitfall
  merged into the existing `subButtonIcon` row. SKILL.md 16,166 → 16,804
  tokens; baseline moved.
- `verify.py` caught the README and test-dashboard version strings left at 1.7.

**`release.yml`'s manual trigger could not work, and two latent bugs behind
it.** The workflow declared `workflow_dispatch`, but every step derived the
version from `GITHUB_REF_NAME`, which on a dispatch is the *branch* name. The
run died at the version check with `Tag vmain does not match SKILL.md version
1.8`; had it got past that, the publish step had no tag to publish to, because
`action-gh-release` was given no `tag_name`. A button that can only fail with
a confusing message is worse than no button.

- The version is now resolved **once**, in its own step, and every later step
  reads `$VERSION` from the environment. It had been re-derived in four
  places.
- On a **tag push** the tag stays authoritative and must still match
  `SKILL.md`. On a **dispatch** `SKILL.md` is authoritative and the publish
  step creates the tag at the commit being released — so a release no longer
  requires the ability to push a tag.
- A dispatch **refuses to move an existing tag**: if `vX.Y` already exists at
  a different commit the run fails and says so, rather than silently
  re-pointing a published release at another tree. `actions/checkout` runs
  with `fetch-tags: true`, because the default shallow checkout fetches no
  tags and that check would otherwise always pass.
- **The changelog-extraction regex was wrong.** `^## v{version}\b` treats the
  boundary between `8` and `.` as a word boundary, so asking for `1.8` matched
  a `## v1.8.1` heading — and matched it *first*, being higher in the file. The
  first patch release would have shipped the wrong release notes. Now
  `(?![\d.])`.
- `concurrency` is keyed on the workflow rather than on `github.ref`: a
  dispatch from a branch and a tag push for the same version are different
  refs, so the old group let them run against each other.
- `actions/setup-python` v5 → v6. v5 targets Node 20, which the runners now
  force onto Node 24 with a deprecation warning.
- Corrected the file's header comment, which claimed the repo had no tags and
  no releases. It has had both since v1.0; the comment predated them and then
  misled a later reader into repeating the claim.

All five trigger shapes were run against the extracted step before pushing:
dispatch from a branch, a matching tag, a mismatched tag, a dispatch colliding
with an existing tag, and a dispatch with no such tag.


## v1.7 — 2026-09-19

Bubble Card v3.4.0 support. Verified against the v3.4.0 source tree.

### Bubble Card 3.3.0 → 3.4.0

- **`state_content` documented** (new `bubble-card-ref.md#state-content`). One
  ordered list now describes the state line of a card or sub-button, the way
  Home Assistant writes it on its tile card and badges, replacing
  `show_state`, `show_attribute`, `attribute`, `show_last_changed` and
  `show_last_updated`. Includes the domain-default table copied from the HA
  frontend, the zero-attribute suppression rule (an off light shows *Off*, not
  *0 %*), and the aliases.

  The migration behaviour matters more than the syntax: the five legacy keys
  keep working, **but opening the card in the visual editor rewrites them to
  `state_content` on save**. Guidance is therefore version-conditional —
  generate `state_content` for v3.4.0+, legacy keys below it, and never both
  for the same card, since `state_content` wins outright and the leftovers
  become dead config.
- **Home Assistant templates in card config** (new `#ha-templates`). Jinja2
  now evaluates in `name`, `icon`, sub-button `name`, `state_content` items,
  and inside `styles:` alongside the existing JavaScript `${ }` templates.
  Documented with the cost note (evaluated on every relevant state change —
  fine for one card, not for forty), the scope boundary (this is presentation
  templating, template *sensors* remain an ha-yaml handoff), and the Iron Law
  reminder that a template returning a colour must return a theme variable.
- **Render performance rework noted.** v3.4.0 measured 43 renders/second at
  rest on an A10 iPad with 78% of them unnecessary, and added a render gate
  observing each card's real dependency set, plus deferred card updates and
  lazy editor previews. Nothing to generate, but it changes the advice around
  pop-up `performance_mode`: update and measure before reaching for it.
- Two version-compat rows, three troubleshooting entries (legacy keys
  "vanishing" after a UI edit, raw `{{ … }}` on older versions, `state_content`
  silently winning over legacy keys), and two Signal Scan rows so the version
  gate fires before generation.

### Systematic source review — started

Pattern scans find surface; they cannot find behaviour. A file-by-file read of
the Bubble Card source is now underway, tracked in `CODE-REVIEW-LOG.md` so it
survives across sessions. First file done: `cards/pop-up/helpers.js` (3,082
lines), which yielded four behaviours no scan would have surfaced:

- **`performance_mode` content deferral applies only to `popup_mode: default`.**
  Extending it to `adaptive-dialog` was tried upstream and reverted — it pushed
  the open 120 ms past the end of the slide on an iPad 6. Performance mode still
  helps on other modes, through its other effects. Documented beside the mode
  table, because pairing the two expecting deferral is exactly what the option
  names invite.
- **The mechanism behind the top-level pop-up rule.** A pop-up suspends the
  `hui-card` cell hosting it so it reserves no height. Inside a grid, masonry or
  `layout-card` it has no own cell — the nearest wraps the whole view — so
  Bubble Card suspends nothing and the pop-up reserves visible empty space. The
  rule was already there; now it has its reason.
- **`close_on_click` on touch ignores scrolls and drags** (>10 px of movement
  reads as a gesture), and native HA buttons inside a pop-up now work with it.
- Speculative shell warm-up at idle explains the memory-at-rest and fast-first-
  open behaviour of pop-up-heavy dashboards.

Two more pop-up files done:

- **Card order inside a pop-up now has a performance meaning**
  (`cards/create.js`). A large pop-up renders only enough leading cards to fill
  the first viewport before the open transition — the fold estimated from grid
  spans — and hydrates the rest afterwards, one budgeted step at a time.
  Off-screen cards skip `hass` updates until scrolled in. The most-used control
  belongs first in `cards:`, or the user waits for hydration before they can
  touch it. Same ordering the engagement-type model already asks for, now with
  a measurable payoff.
- **`time` and `template` conditions in a pop-up header are expensive**
  (`index.js`). Bubble Card memoises the header against the entities its
  conditions reference; those two cannot be tracked that way, so one of them on
  any header sub-button forces the whole header to refresh on every HA state
  change anywhere. A relative-time field does the same. Cost note added with
  the entity-based alternative.
- **Corrected: pop-up hashes are unique per dashboard, not globally.**
  Registration is keyed on the dashboard path, so `#settings` on two dashboards
  is fine. The option table said "unique" without qualification.
- A templated `name:`/`icon:` is resolved for HA's navigation picker, so a
  pop-up appears there with what it shows rather than raw template text.

Two more files, including a correction to a skill error:

- **`water_heater` was wrongly documented as unsupported.** `isStateOn` handles
  it explicitly — a water heater has no `on`, its state is the operation it
  runs, so anything but `off`/`unknown`/`unavailable` reads as active, the same
  rule HA uses. A `button_type: state` card shows and colours it correctly;
  only toggling and sliding are unavailable. The domain-list paragraph now
  separates *control* from *display*, since active-state detection is a
  broader rule than the toggle/slider sets.
- **`min_value` / `max_value` / `step` are overrides, not descriptions.** Left
  unset the slider reads the entity's own `min_temp`/`max_temp` or `min`/`max`/
  `step`. The `number` row previously said to set them "matching entity" —
  which freezes the range, so the card keeps the old bounds after the entity's
  change. Rewritten, with the safety clamp (climate min+1, others min+100)
  documented as the diagnostic for a slider stuck at a pinned value.
- **A templated `name:` has no fallback**: a plain `name:` falls back to the
  friendly name, a template shows exactly what it returns, empty included.
  Documented with the `or 'default'` pattern.

Two more files, including a second stale claim removed:

- **The `cover_background` performance warning was out of date.** The skill said
  it "fetches album art on every state change — avoid on dashboards with many
  simultaneous media players". The crossfade has since been rewritten because
  the old one raced with itself: it now keys on the target image, runs one fade
  at a time with later requests queued rather than stacked, and keeps only the
  last queued request. Holding "next" costs one extra fade, not one per press,
  and a playing player no longer re-fetches. Rewritten — the remaining cost is
  image decode.
- **Entity-picture precedence on sub-buttons**: an entity with an
  `entity_picture` shows it instead of an icon, suppressed by `force_icon` or
  by the sub-button's **own** `icon` — the card's icon does not suppress it. A
  person sub-button meant to show a face therefore needs no `icon:` at all.
- **`scrolling_effect` cascades** sub-button → card → `true`; documented with
  its real default chain rather than a flat `true`.
- **Timer sub-buttons tick live** while the timer is active, if the state line
  includes `state` or `remaining_time` — the entity itself does not update per
  second.

`sub-button/create.js` done — two findings that change generated YAML:

- **Sub-button classes have different stabilities.** Each carries
  `.bubble-sub-button-<index>`, a class derived from `name:`, and `.<css_class>`
  if set. The name-derived one breaks on a rename *and on a translated name*,
  and is not generated at all for a templated name. The `#css-selectors`
  guidance previously said only "prefer `css_class`"; it now says which of the
  three to target and why — a user who translates their dashboard loses every
  style hung on a name.
- **Mixing loose sub-buttons with explicit groups reorders them.** All loose
  buttons in a section are collected into one automatic group placed where the
  first of them appeared, not interleaved in YAML order. Documented with an
  example, since the YAML reads as though order is preserved and it is not.

`tap-actions.js` and `icon.js` done:

- **`tap_action: none` also removes the press ripple.** Feedback is attached
  only when at least one of tap, double-tap or hold is not `none`, so a
  state-only card *looks* non-interactive rather than merely behaving that
  way. That turns the engagement-type model's "Overview cards take
  `tap_action: none`" from a convention into a mechanical one — the difference
  between a card that ignores a tap and one that never invited it. Hold timing
  (500 ms) documented; the existing 200 ms double-tap note verified correct.
- **`icon:` and `name:` treat an empty template result oppositely.** An icon
  template rendering nothing falls through to the entity's icon; a name
  template shows the empty string. Documented as a pair, since the asymmetry is
  invisible and they sit side by side.
- **Setting `icon:` overrides HA's entire resolution chain** — including the
  entity-registry icon a user set in the UI and the domain state icons (a lock
  showing open vs closed). Added a "usually don't set it" note, which also
  trims generated YAML.

`types/slider/index.js` and `text-scrolling.js` done — the card-near files are
now covered:

- **Slider sub-buttons inherit nothing from the card.** Every slider option is
  read from the sub-button only; setting `tap_to_slide`, `read_only_slider`,
  `min_value` and the rest on the card does nothing for a
  `sub_button_type: slider`. This is **not** the same rule as
  `scrolling_effect`, which does fall back to the card — the cascade is
  per-option, so neither direction can be assumed. Documented with the full
  list.
- An unset slider option stays genuinely absent rather than defaulted, which is
  what lets `slider_value_position` follow the reading direction in RTL
  languages. Pinning it to `right` breaks that.
- **Corrected an imprecision introduced earlier in this review:**
  `show_button_info` forces `slider_value_position: right` only together with
  `always_visible: true`, not unconditionally as the table claimed.
- `scrolling_effect` is cheaper than it looks: only text that actually
  overflows gets a marquee, and a marquee holds a composited layer only while
  genuinely on screen. The option row now says so, and points at the
  motion-sensitivity rule for when to disable it regardless.

### Eval set extended to cover the code review

The eval set tested the surface guidance but none of the behaviour the source
review found — so a passing run would have validated the wrong things. Six
cases added (18 total), chosen by one criterion: **the correct answer
contradicts what the YAML looks like it should do**, which is exactly where a
model reasoning from the config's shape goes wrong.

| Eval | Tests |
|---|---|
| 13 | `state_content` replaces five legacy keys from v3.4.0, never alongside them |
| 14 | slider options do not cascade from the card to a slider sub-button |
| 15 | a hardcoded `icon:` overrides HA's state-dependent resolution chain |
| 16 | loose sub-buttons mixed with a group are collected and moved |
| 17 | `min_value`/`max_value` are overrides that freeze the entity's range |
| 18 | the name-derived CSS class breaks on rename and translation |

Also added: **`EVAL-SCORESHEET.md`**, a per-run sheet with the 18 cases, the
scoring rule, and what to do with each failure shape — a FAIL usually means
missing guidance, a PARTIAL usually means the guidance exists but is not
reachable from the Signal Scan or the process tree, so the fix is routing
rather than restating the rule.

And a note in the eval set on **who may run it**: not the model that wrote the
guidance in the same conversation, which knows every answer and would score
itself 18/18 for nothing. Fresh conversations, ideally reviewed by someone who
did not write the rules being tested.

**Module system: contract read, UI skipped.** The module folder splits cleanly
in two, and only one half is worth reading. `parser.js` and `yaml-schema.js`
define what a valid module *is* — and the skill generates module YAML, so that
contract matters. `store.js`, `editor.js`, `module-editor.js` and the install
flow (~5,500 lines) are the Module Store UI, which the skill never generates
and a user only meets through the interface; skipped deliberately, recorded as
such rather than left ambiguous. Findings:

- **The accepted key set is larger than documented**: `unsupported`,
  `is_global`, the legacy `form_schema` alias of `editor`, plural/singular
  `supported_card(s)`, and the legacy `author` / `type` / `info` container.
  Full table added, with the rule to generate only the modern spellings.
- **`unsupported:` was undocumented** — the inverse of `supported:`, shorter
  for a module that fits everything but one card type and stable when Bubble
  Card adds a card type.
- **`is_global: true` applies a module to every card** with no per-card opt-in.
  Documented with the warning that it makes the performance rules in
  `#module-performance` mandatory rather than optional.
- **`!include` works inside module YAML**, resolved against `/local/bubble/`.

`CODE-REVIEW-LOG.md` carries the coverage table (144 files, 47,582 lines),
the resume procedure, and findings per file. Excluded from the install bundle.

### Coverage audit of the analysis method

The v3.4.0 review used pattern scans over the source tree, not a full read:
144 non-test files, 47,582 lines, of which perhaps 15 files were opened. That
method was tested for its own blind spots and two came back clean — no config
key is read only via destructuring (`const { x } = config`) or bracket
notation, so the `config.x` scan was not missing options. One editor-only key
surfaced, `style_templates`, already documented as the legacy alias of
`modules`.

Opening one previously unread file (`cards/pop-up/migration.js`, 914 lines)
produced one new finding, which is the honest measure of how complete the scan
was: the pop-up migration notice is **one-shot**, recorded in `localStorage`,
and the migration converts legacy content cards to a 12-column grid layout.
Two troubleshooting entries added — a user who dismissed the notice will not
see it again, and migrated cards come out with different widths on purpose.

### Three more undocumented surfaces

Pushed past the YAML option surface after the coverage question. Four scans,
three gaps:

- **Actions** (`#actions`). Bubble Card dispatches a `hass-action` event, so
  the action set is Home Assistant's own, not a Bubble-specific list. Two were
  missing: **`assist`** (with `pipeline_id` and `start_listening`) and
  **`perform-action`**, HA's 2024.8 rename of `call-service`. Both names still
  work; guidance now generates `perform-action` and marks `call-service` as
  legacy.
- **JS template scope** (`#js-templates`). The compiler's in-scope names are
  now listed in full as verified against v3.4.0. One was undocumented:
  **`renderTemplate(template, entity?)`** (v3.4.0+), which renders a Jinja2
  template from inside a JS template — the bridge that lets one `styles:`
  block mix both systems. Noted that it is rarely needed now that Jinja works
  directly in `name`, `icon` and `state_content`, and that it needs a `typeof`
  guard in shared modules.
- **CSS selectors** (new `#css-selectors`). The skill showed about a dozen
  `.bubble-*` classes by example; Bubble Card renders roughly 110 card-facing
  ones. Curated by card type rather than dumped — a full list would be noise,
  and most are structural wrappers nobody targets. The important part is the
  warning attached: these are internal names, not a stable API (the
  `bubble-cover-crossfade-*` set did not exist in earlier 3.x), so prefer a
  `--bubble-*` theme variable where one exists, and use `css_class` to add
  your own rather than depending on Bubble Card's.

Scanned and clean: the YAML option surface (0 gaps) and the module helper API.

### CSS variable catalogue completed

A systematic scan of `--bubble-*` variables found the skill documented 15 of
82 themeable ones. The 15 are the Casa5HeyneV2 mappings and remain the right
default — they drive colour and radius everywhere through the HA variables
they point at — but the missing 63 are the component-level knobs for cases a
global mapping cannot express.

Added to `css-theme-ref.md#bubble-vars`, grouped by component, with the
warning that using them breaks the one-accent-lever property that makes the
theme maintainable, and the reminder that they still belong in the theme
rather than on the card.

The most useful group is the climate HVAC mode colours
(`--bubble-state-climate-heat-color` and siblings) — a common request the
skill previously could not answer, since HA's own climate colours do not
reach Bubble Card.

Runtime-computed variables (pop-up available height, scroll-lock size, mask
stops) are deliberately excluded and called out as ineffective in a theme:
Bubble Card overwrites them on every render. Distinguishing the two was the
point of the scan — reporting all 98 undocumented names would have been noise.

Not a v3.4.0 change: this was a long-standing documentation gap, found only
because this round's analysis went past the YAML option surface.

### Tooling

- **`test_verify.py`**'s version-drift fixture hardcoded `skill v1.6` and broke
  on the version bump — the self-test correctly reported its own fixture as out
  of date rather than passing silently, which is exactly its job. Now
  version-agnostic.

### Verified unchanged

- Module helper API is still `onTeardown` and `hasChanged` at 3.3.0 — no new
  names to guard with `typeof`, so `#module-performance` stands as written.
- Editor schemas are unchanged from 3.3.0. As in the 3.3.0 round, the entire
  new surface lives in runtime code: an editor-level scan would have found
  nothing.

---

## v1.6 — 2026-08-29

New capability: graph and history coverage. Adds support for two components
the skill did not previously know about, and closes a dependency the skill had
been generating without ever declaring.

### New reference: `graphs-ref.md`

The skill generated `custom:mini-graph-card` in 15 places without ever
declaring it as a dependency, and had no guidance on choosing a graph card at
all. New reference file, deliberately scoped rather than exhaustive:

- **`#graph-decision`** — the decision table (native `history-graph` /
  `statistics-graph` → mini-graph-card → SGCC → Advanced History panel), with
  the rule that every custom option is a HACS install that must be named
  alongside its native fallback.
- **`#sgcc-status`** — Statistics Graph Chart Card ships as a **minified,
  protected bundle**, so source-first verification (this skill's standing
  method) is impossible for it. Documented from README only, stated plainly,
  with the maintenance consequences for unattended wall panels.
- **`#sgcc-dashboard-use`** — the handful of options that matter for
  generation rather than the full 4700-line surface: `sparkline` (chrome-free,
  the calm-tech-compatible form), `height: auto` (participates in sections
  grid sizing), `group_by: raw` for step charts, plus the Iron Law reminder
  that `color:` takes CSS values, so theme variables belong there.
- **`#graph-performance`** — `data_source: statistics` and statistics-based
  `group_by` as the mechanisms that keep a graph-heavy dashboard off the
  database's back; upstream measures 287 rows/33 ms vs 21,995 rows/1.7 s for
  the same window. Plus the `state_class` prerequisite for long ranges, which
  is an ha-yaml handoff rather than a card option.
- **`#advanced-history`** — the panel (integration v2.0.1, requires SGCC
  v3.32+, v4.02+ for multiple panels). Positioned through the engagement-type
  model: it is not a card, so it never competes for dashboard space, which
  makes it the honest answer to "a page with graphs of everything" — an
  exploration tool rather than a glanceable surface.

- **The mini-graph-card / SGCC-sparkline overlap** is addressed explicitly
  rather than left for the reader. Both cover "a small trend line", so the
  choice is a dependency decision: use whichever is already installed; never
  add mini-graph-card when SGCC is going in anyway (sparkline covers it);
  prefer the small open card when a sparkline is the only need; and don't let
  the whole graph capability rest on an unauditable bundle by default. The
  Activity scaffold now labels its `mini-graph-card` usage as a *placeholder*
  with an instruction to ask, not a recommendation.
- SGCC's install path is documented honestly: the README's steps imply the
  default HACS catalogue while the repository still carries a *HACS: Custom*
  badge, so the guidance covers both.

Wired in: prerequisites table, process-tree route, two Signal Scan rows, the
Activity scaffold, four troubleshooting entries, a health-check graph-density
advisory, and `#eval-12-graph-request`.

### CI pipeline

- **`verify.yml`** — runs `verify.py` on every push and pull request, plus an
  advisory external-link check (non-blocking: upstream repos rename, and a
  redirect on someone else's URL should not fail a docs change).
- **`upstream-drift.yml`** — weekly job comparing the component pins in
  SKILL.md against the latest upstream releases via the GitHub API, opening or
  updating a single issue when a pin falls behind. This automates the failure
  mode that has actually recurred here: guidance going stale because a release
  shipped unnoticed. The issue body repeats the standing rule — scan the
  source tree, not the release notes.
- **`release.yml`** — on a `v*` tag: verify, assert the tag matches the
  `version` in SKILL.md metadata, build both a `.zip` and a `.skill` bundle,
  re-run `verify.py` against the *packaged* copy, and publish a GitHub
  Release. The repo previously had no tags and no releases; every version was
  a hand-passed zip.
- **`check_upstream.py`** — the drift checker, also usable locally.
- **`test_verify.py`** — negative tests for `verify.py`, run in CI. A checker
  that only ever passes proves nothing; this injects each bug class into a
  throwaway copy of the library and asserts the checker still catches it. Ten
  cases, one per shipped bug class, currently 10/10. This closes a real gap:
  `verify.py` missed the stale frontmatter comment because nothing tested the
  tester.

### Fenced YAML validation — and the defect it found

`verify.py` validated the two standalone `.yaml` files but never the ~205
fenced YAML blocks in the documentation, which *are* the product: users copy
them into Home Assistant. Parsing them found a defect in seven scaffolds,
including the core dashboard example in SKILL.md itself.

**The bug:** view scaffolds nested `sections:` underneath `cards:`

```yaml
  cards:            # wrong
    sections:
```

instead of making them siblings. In a sections view, `sections:` holds the
card grid and `cards:` holds top-level cards (pop-ups, the HBS footer) — the
skill's own §4 rule. The nested form does not parse, so anyone copying an
affected scaffold got a dashboard that would not load. Affected: the SKILL.md
core example, four scaffolds in `dashboard-system.md` (Scenes, Activity,
Settings, Energy), the Music scaffold (which also needed reordering, as its
pop-ups preceded the sections), and two in `recipes-5view.md`.

Also fixed: `mush-rgb-state-alarm-triggered:"var(…)"` in
`mushroom-theme-ref.md` was missing the space after the colon, so that line
silently did nothing when copied into a theme.

**New check (`yaml-examples`)** parses every fenced block, skipping the ones
that legitimately are not plain YAML — HA `!include*` tags, `{placeholder}`
keys, Streamline `[[variable]]` templates, and deliberately-partial
WRONG/CORRECT teaching fragments. `verify.py` is now 12 checks.

This is the clearest argument yet for the CI work: the defect had shipped, was
invisible to every existing check, and sat in the most-copied example in the
library.

### Token budget monitoring

- **`token_budget.py`** — measures the footprint that actually matters:
  SKILL.md as the fixed per-session cost, versus the anchor-routed reference
  library that only costs what is read. Enforces a ceiling on SKILL.md and a
  per-anchor ceiling above which routing stops helping, and reports growth
  over a committed baseline (`token-baseline.json`).
- Wired into `verify.yml`; on pull requests a sticky comment reports the
  SKILL.md delta, so a change that adds to the every-session cost says so in
  review instead of surfacing months later.
- Motivating measurement: SKILL.md grew from 14,959 to 15,928 tokens (+6.5%)
  during this release's work without anyone noticing. It sits at 15,928/17,000
  now — comfortable, but the trend is the point. Largest anchor is
  `#view-activity-scaffold` at 3,483; median across 162 anchors is 516.
- `test_verify.py` gained a case for the budget guard: 11/11.

### Two checker bugs found by the checker

CI on the live repository flagged `dashboard-recipes.md#view-activity` at 4,217
tokens — a file deleted in v1.4. It had survived because the repo was synced
rather than replaced, exactly the case the v1.4 upgrade note warned about. The
token budget caught it only by accident, through an oversized anchor.

Two checks that should have caught it directly did not:

- **`check_orphans` counted a CHANGELOG mention as a live reference.** The
  changelog says "Deleted `dashboard-recipes.md`" — which made the deleted file
  look referenced. Fixed: only SKILL.md and other reference files count as
  routing references. Changelog history does not.
- **No duplicate detection existed at all**, despite a 50 KB exact duplicate
  being the single largest structural defect in this project's history. New
  `check_duplicates` compares normalised 400-character windows across
  reference files and fails above 60% containment.

Both are now regression-tested (`test_verify.py`: 13/13). `verify.py` is at
13 checks.

The lesson generalises: a check that reads *any* mention as a reference will
be defeated by the file that documents deletions.

### Link check — moved off the hot path and made fast

Two rounds of fixes after live CI runs:

*False positives.* Patreon returns 403 to automated requests (the link is
fine in a browser). Excluded, along with `homeassistant.local` (the reader's
own LAN address), `example.com` (a placeholder in sample YAML) and the
`family=FontName` placeholder in the font-loader template. Each exclusion
carries its reason in the workflow, under a standing rule: exclusions are for
links that *cannot* be checked, not for links we would rather not fix. A
check that reports a known false positive every run teaches people to ignore
it, which is worse than not having it.

*Runtime.* The job was slow because the 13 `github.com` links ran
unauthenticated into anonymous rate limits, and lychee then retried with
backoff. Fixed by passing `GITHUB_TOKEN`, capping retries and timeout, and
enabling lychee's cache.

*Placement.* The job moved out of `verify.yml` and into the weekly
`upstream-drift.yml`, where it belongs: a rotted external link is upstream
drift, not a reason to block a pull request. With 7 unique links that do not
change per commit, running it on every push bought nothing and cost minutes
on the critical path. Push and PR runs are now `verify.py`, the self-test and
the token budget only.

### Repository layout

Repository tooling moved from the skill root into `scripts/`
(`verify.py`, `test_verify.py`, `token_budget.py`, `check_upstream.py`,
`token-baseline.json`). The repo *is* the skill, so anything at the top level
ends up in what users install — the release bundle was shipping a test
harness, a token estimator and a drift checker to people who only wanted the
dashboard guidance.

`release.yml` now excludes `scripts/`, `CHANGELOG-v*-detail.md` and
`RELEASE_NOTES_v*.md` from the bundle, and verifies the packaged tree by
copying the checker in temporarily rather than shipping it. Every tool
resolves the skill root as its parent directory, so all paths still work.

### CI hardening

- Least-privilege `permissions:` on all three workflows (`contents: read`
  except where a job must write), `concurrency` groups (cancel superseded PR
  runs; never cancel a half-published release), `timeout-minutes`, and a
  pinned PyYAML version.
- **Release body defect fixed before it shipped:** `body_path: CHANGELOG.md`
  would have pasted all 480+ lines of history into every GitHub Release. The
  workflow now extracts only the tagged version's section (104 lines for
  v1.6) and fails the release if no such section exists.
- `.github/dependabot.yml` — monthly updates for third-party actions, the main
  supply-chain surface. Note in the file: pin to commit SHAs for the stricter
  guarantee; Dependabot maintains SHA pins too.
- PR template with the project's actual invariants as a checklist (source-tree
  scanning, routing reachability, the Iron Law, version gating), and two issue
  templates — "Claude generated something wrong" and "a component released",
  the two report types this repo actually receives.

### Adopted from skill-creator

Anthropic's `skill-creator` bundles `quick_validate.py`, which enforces the
SKILL.md frontmatter spec. Rather than vendor Apache-licensed code into an MIT
repo, the same rules were reimplemented as a `verify.py` check: exactly one
SKILL.md, `name`/`description` required, kebab-case name within 64 chars,
description within 1024 chars and free of angle brackets. The skill passes the
official validator unchanged.

Added on top: a warning above 900 description characters. The current
description is 877/1024 — every new TRIGGER or SYMPTOM line eats headroom, and
hitting the limit mid-edit is a bad time to find out.

`verify.py` is now 11 checks; workflow YAML joined the validity pass.

### Fixes

- Frontmatter defect: the `mushroom` pin carried a stale trailing comment
  claiming HA 2026.7 while `ha_checked` said 2026.9 — a leftover from an
  earlier edit. Fixed, and `verify.py` gained a tenth check (metadata lines
  with two comments), negative-tested.
- New pins recorded for the two added components. SGCC's is deliberately
  vague (`4.02-era`) because the bundle is minified and carries no readable
  version constant — an honest pin beats a guessed one.

### Behavioural tests

- `#eval-12-graph-request` — a German-language prompt asking for an overview
  page full of graphs, exercising the engagement-type argument, the Advanced
  History alternative, dependency declaration, and the `data_source`
  performance point in one case.

---

## v1.5 — 2026-08-29

Component currency: Bubble Card v3.3.0 support and alignment with Home
Assistant 2026.8/2026.9. Verified against the v3.3.0 source tree and HA
release notes through 2026.9.

### Bubble Card 3.2.5 → 3.3.0

- **Platform conditions documented.** v3.3.0 ports Home Assistant's own
  `domain.name` conditions to the client — 141 of them (`sun.is_up`,
  `motion.is_detected`, `climate.is_heating`, `lock.is_unlocked`,
  `zone.in_zone`, `select.is_option_selected`…) usable directly in
  `visibility:`. Documented with the caveats that matter: astral maths is
  approximated, `for:` durations drift because there is no recorder priming
  pass, recorder-history conditions cannot be ported, and an unsupported type
  falls back to a silent state check rather than failing loudly. Explicitly
  version-gated — on < 3.3.0 these misbehave rather than error.
- **Lovelace condition table completed** — `not`, `time`, `location`,
  `template` and `view_columns` were supported but undocumented.
- **`grid_options`** added: native HA sections sizing (`{rows, columns}`),
  preferred over `rows:` inside a sections view.
- **Installation change for manual installs.** The `translations/` folder is
  gone; editor dictionaries now sit beside `bubble-card.js` as
  `bubble-card-<lang>.json`. Documented in §1 with two troubleshooting entries
  (editor reverting to English, "Custom element doesn't exist" after update).
- **Six undocumented per-sub-button options** added: `sub_button_type`
  (now including `dropdown`), `show_button_info`, `hide_when_parent_unavailable`,
  `light_background`, `css_class` (the supported alternative to brittle
  `nth-child` selectors in `styles:`), and the `always_visible` interaction
  with `slider_value_position`.
- Signal Scan row for conditional-visibility requests, so the version gate
  fires before generation rather than after.

### Module authoring — two missing chapters

Diffed the skill's module reference against Bubble Card's own bundled
`src/modules/module-documentation.md` (1422 lines). Two substantial chapters
were absent:

- **New `#module-performance`.** Module `code:` runs on every style pass of
  every carrying card, and a pop-up rebuilds all its cards on each open —
  roughly seven passes per card. v3.3.0 adds `hasChanged(label, ...values)`
  and `onTeardown(fn)` to gate work and release timers/observers. Upstream
  measured one module going from 7.2 s to 3.7 s cold pop-up open on a low-end
  iPad. Includes the compatibility rule that matters most: referencing a name
  the installed version lacks throws and makes Bubble Card skip the *entire*
  module, so `typeof` guards are mandatory for shared modules.
- **New `#module-suggestions`.** Modules can join the HA 2026.6+ card picker
  via `suggestions:` (`extends: native|base`, `config` with `${entity}`,
  `domains`, `condition`, `label`) or `suggestions_code:` for computed
  configurations. 24 suggestions per module per entity, no global cap.

### Home Assistant 2026.8 / 2026.9 alignment

- **Breaking change handled: vacuum `battery_level` removed (HA 2026.8).** Two
  places in the skill generated `attribute: battery_level` sub-buttons — the
  generic battery example and the Streamline device template. Both now use the
  device's battery *sensor* with `show_state: true`. Troubleshooting entry
  added listing the eight affected integrations.
- **Developer Tools → Tools rename (HA 2026.8)** applied across all references,
  with the old name noted where a user on an older version would look for it.
- **New `dashboard-system.md#entity-rename-risk`.** Renaming entity IDs became
  a two-click UI operation in 2026.8, and HA's repair flow covers automations
  and scripts far better than Lovelace — a renamed entity leaves a card showing
  "Entity not available", silently. Guidance sequences the work (rename, then
  repair via §9 health check) rather than discouraging it. Signal Scan row and
  troubleshooting entry added.
- **Native-first table extended** with the capacity-weighted combined battery
  level (2026.8) and the clock card's date support (2026.8).
- **Accessibility section strengthened.** HA 2026.9 makes charts a real focus
  stop — keyboard-navigable data points, live-region announcements, and an
  audio tone tracking the curve. That is a concrete capability a custom graph
  card cannot match, and it is now part of the native-alternative argument.
- **Template performance note.** HA 2026.8 made numeric templates up to 40%
  faster and cached dashboard templates. The scope rule is unchanged, but a
  template sensor can no longer be justified on performance grounds alone.
- Device-registry split (2026.8) noted in troubleshooting: entity-based card
  YAML is unaffected; only device-ID references need review.

### Method note

The `config.*` source scan produced two false positives this round —
`unit_system` and `time_zone` are `hass.config.*` reads, not YAML options.
Scanning for `config.` alone conflates the card config with the HA config
object; distinguish the two before documenting an option.

---

## v1.4 — 2026-08-06

Ecosystem alignment, source-verified component updates, and a rebuilt routing
layer. Verified against Bubble Card v3.2.5 source, Mushroom v5.2.2 source, and
HA release notes through 2026.7.

Development detail for this release is preserved in
`CHANGELOG-v1.4-detail.md`; this entry is the summary.

### Component updates

- **Bubble Card pin 3.2.2 → 3.2.5.** Compat table rows for v3.2.3 (card
  suggestions via the HA 2026.6 picker, `close_action` fix, iOS pop-up
  visibility), v3.2.4 (standalone pop-ups reliable inside `vertical-stack`;
  true pop-up-in-pop-up nesting still unsupported) and v3.2.5 (cover tilt —
  `tilt_buttons`, `open_tilt_service`, `close_tilt_service`,
  `cover_slider_type: tilt_position`, with the feature-detection rule).
- **New Mushroom pin 5.2.2**, verified against `src/utils/theme.ts`.
- **24 previously undocumented Bubble Card options added.** The earlier
  verification scanned editor schemas only, which misses every YAML option the
  editor does not surface. A full `config.*` source scan closed the gap:
  six slider options, the six sub-buttons layout options, three calendar
  options, plus `show_last_updated`, `sub_button_justify_content` and
  `hide_temperature`.

### Corrections

- **Iron Law violation in the skill's own calendar example.** It used a
  hardcoded hex; `color:` resolves a colour *name* to `var(--<name>-color)`,
  so `color: accent` was available all along.
- **Two nonexistent Mushroom variables removed** — `mush-rgb-state-switch`
  (switches follow `mush-rgb-state-entity`) and `mush-rgb-primary`. Both were
  documented across 22 places and would have silently done nothing. Added the
  missing state groups (vacuum, media-player, lock + sub-states, number,
  humidifier, update) including the upstream quirk that `mush-rgb-update-off`
  and `-installing` carry no `state-` segment.
- **Module-authoring corrections** — removed a `variables:` + `{{mustache}}`
  pattern that does not exist in Bubble Card's module system, and the
  nonexistent `supported: [all]` literal.

### Native HA alignment

- New `#native-first` — the native-first check (parallel to automate-first):
  battery grids → Maintenance dashboard, security logs → Security Activity
  list, weather and media → tile features. Plus positioning against the native
  Home dashboard (default for new installs since HA 2026.2) and hybrid setups.
- New `#native-interop` — mixing native tile/heading/area cards into Bubble
  layouts: theme inheritance, Bubble-mechanism boundaries, grouping rules.
- Health-check gained a native-feature advisory category (Advisory only).

### Process routing rebuilt

- **New Signal Scan layer.** The process tree routed on *output type*, but
  most failure modes are *input signals* — the user's language, a stated
  accessibility need, a natively covered feature, an unsupported entity
  domain. A nine-row scan now runs ahead of the tree, is multi-select, and
  never withholds output. Actively routed eval cases: 3/10 → 10/10.
- **Process tree completed** — `calendar`, `select`, `separator` and
  `sub-buttons` were documented but had no route at all. Added, plus a branch
  for requests that describe a situation rather than name a card.
- Common Pitfalls trimmed 17 → 13 rows; four were intake signals and moved.

### New capabilities

- `#entity-inventory` — Developer Tools template snippet producing an
  area-grouped, device-class-annotated entity list for the Collect step.
- `#masonry-migration` — masonry → sections with a construct mapping table.
- `#wall-panel-hardening` — burn-in, screen-off handoff, kiosk pointers.
- `module-authoring-ref.md` — Bubble Card editor field catalog, v3.2.4 object
  selector, both export formats, plus the paid-module boundary rule.
- Localisation rule and an honest statement of Bubble Card's accessibility
  limits (div-based controls are not screen-reader operable; never claim WCAG
  conformance from contrast checks alone).
- Entity domain map extended with `siren`, `remote`, `lawn_mower`, and
  explicit no-support entries for `valve`, `water_heater`, `todo`, `image`.

### Tooling

- **`verify.py`** — nine structural checks (anchors, anchor-list sync, YAML
  validity, theme mode symmetry, banned variables, Iron Law in card examples,
  version consistency, routing coverage, orphan files). Each exists because
  that bug class shipped at least once; the routing check is negative-tested.
- **`references/eval-set.md`** — ten behavioural regression prompts with
  MUST / MUST NOT criteria, run in fresh conversations.

### Structural

- Deleted `dashboard-recipes.md` (~50 KB, verified duplicate, referenced
  nowhere) and `casa5heynev2-template.yaml` (theme existed in two copies that
  had already drifted twice). `theme/Casa5HeyneV2.yaml` is now the single
  theme source.
- Overview and Rooms view YAML deduplicated — `recipes-5view.md` Recipes 8–9
  are the single source; `dashboard-system.md` keeps design rationale.
- Token routing: `health-check-ref.md` split into five anchors (core path
  −14%), and the two largest view anchors split into design notes plus a
  separate `-scaffold` anchor so planning does not load generation YAML.
- Test dashboard is now a real smoke test — all 11 documented card types
  (was 8), with two defects fixed: a stale version string and an HBS footer
  that was not the last top-level card.


## v1.3 — 2026-06-05

### Architecture — token optimisation

**SKILL.md reduced from 2162 → 937 lines (−57%).**
All content preserved — reorganised for on-demand loading rather than always-in-context.

**New reference files:**
- `health-check-ref.md` — extracted from §9. Contains full parse template (Steps 1–5),
  structural pattern examples, colour scan exclusions, entity scan rules, finding
  categories, output format, tone guides, and partial YAML handling.
- `recipes-5view.md` — extracted from `recipes-extended.md`. Contains Recipes 7–14:
  5-view outer scaffold + per-view card YAML for Overview, Rooms, Scenes, Activity,
  Settings, Energy extension, Music extension.

**Content moved to existing reference files:**
- `dashboard-system.md` — full-dashboard workflow (Steps 1–6), device-type profiles
  table, sections view anatomy diagram, multi-view design rules, panel view.
- `bubble-card-ref.md` — touch target sizing table, performance notes
  (`background_update` deprecation, cover_background, auto_order, Streamline JS lag).
- `typography-ref.md` — font-only update variable list (`ha-font-family-*`,
  all `paper-font-*`, `primary-font-family`) with diff delivery format.
- `streamline-ref.md` — two-block delivery format (Block 1: template, Block 2: usage).

**`recipes-extended.md` restructured:**
- Recipes 7–14 moved to `recipes-5view.md`
- Core Recipes 1–6 (room pop-up, HBS, media player, climate, chip bar, Streamline)
  retained alongside room pop-up patterns
- Recipe 1–6 anchor format standardised to `## #anchor` style

**SKILL.md changes:**
- §2 UX Principles: Type B subsections (full-dashboard workflow, device-type profiles,
  sections anatomy, multi-view design, panel view) replaced with compact summaries +
  pointers; Type C subsections (progressive disclosure, touch targets, state colour,
  mobile-first, information density) trimmed in place
- §3b, §5, §6: compressed to route-only stubs pointing to reference files
- §7: Recipe 0 retained inline; Recipes 1–6 pointer to `recipes-extended.md`;
  Recipes 7–14 pointer to `recipes-5view.md`
- §8: 4 redundant pitfall entries removed (covered by Iron Law); cross-skill
  handoffs compressed to table; performance notes moved to `bubble-card-ref.md`
- §9: replaced with 3-line pointer to `health-check-ref.md`
- Stale text corrected: §2 header, §7 "same file" note, test-dashboard note,
  triple blank lines collapsed

### Fixes
- Two content gaps identified and filled during cross-check against v1.2:
  font-only update variable list (was missing from `typography-ref.md`),
  Streamline two-block delivery format (was missing from `streamline-ref.md`)
- Recipe 1–6 inline anchors `{#anchor}` converted to `## #anchor` format for
  consistency with rest of skill

---

---

## v1.2 — 2026-06-05

### Major additions

**5-view dashboard system** (`references/dashboard-system.md` — new file)
Complete information architecture for Home Assistant dashboards built on
principled UX foundations. Five views with defined purposes and engagement
types: Overview (complications), Rooms (brief interaction), Scenes (brief
interaction), Activity (passive review), Settings (deep engagement). Two
extension views: Energy (+E) and Music (+M) added when relevant.

**Activity view — hide/show graph mechanism**
Eight paired category sections in two groups — Home Activity (Presence, Doors
& Windows, Motion, Automation) and Home Health (Energy, Maintenance, Devices,
Infrastructure). Each category: Option C event card + Option B graph hidden
until tapped. Tap toggles an input_boolean; graph appears inline. Eight helpers
+ template sensor ha-yaml handoff block included.

**Recipes 7–14** (`references/recipes-extended.md`)
Eight new complete copy-paste YAML recipes covering the full 5-view system:
scaffold (R7), Overview (R8), Rooms (R9), Scenes (R10), Activity (R11),
Settings (R12), Energy extension (R13), Music extension (R14).

### §2 UX Principles — full rewrite

**Automate first** — new first principle replacing the 3-tier importance model.
The best dashboard control is the automation that makes the control unnecessary.
Includes optional opening question with explicit skip conditions.

**Engagement-type model** — four types sorted by interaction cost with Tier 0
(no UI — automation) as the explicit first filter. Table format with HA
equivalents and content rules.

**Full-dashboard design workflow** — six-step design-first process: collect →
classify (Buckets 0–3) → present classification → apply device-type profile →
generate from 5-view system → offer follow-up. Classification is always shown
to the user before YAML is generated. Claude never refuses a classification
decision — user has final say.

**Device-type profiles** — five-row lookup table replacing six separate
questions. One device type answer provides: max_columns, card_layout, font size,
nav pattern, theme mode.

### §9 Health-Check Mode (new section)

Audits existing dashboard YAML and returns a prioritised findings list.
Triggers on: "review my dashboard", "health check", "what's wrong with my YAML",
"audit", "improve this". Starts immediately without upfront questions — works
with partial YAML and notes coverage gaps at the end.

**Parsing strategy:** eight structural checks in sequence — view type, top-level
card placement, hardcoded colours, pop-up format, performance flags
(background_update, rise_animation), engagement-type mixing, automate-first
candidates, missing complications tier, structural best practices.

**Three severity tiers:**
- 🔴 Critical — Iron Law violations and broken functionality (hardcoded hex,
  pop-up inside sections, masonry view type, missing hash on pop-up)
- 🟡 Significant — materially degraded UX (mixed engagement types, theme on
  individual cards, deprecated pop-up format, background_update misuse)
- 🟢 Advisory — improvement opportunities (automate-first candidates, missing
  chip bar, 5-view alignment opportunity — always optional, never prescriptive)

**Consistent output format:** findings grouped by severity, each with location,
issue, and specific fix. Summary section always notes what is working correctly.

**Automate-first tone:** neutral — names the entity, notes what it typically
indicates, suggests the automation alternative, acknowledges the user may have
a reason for keeping it.

**5-view alignment:** Advisory only, never Critical or Significant. Framed as
an option with a concrete mapping of existing content to the 5-view structure.

**Process flowchart:** health-check trigger added as a top-level branch —
routes immediately to §9 without passing through the card/dashboard path.

---

### Common Pitfalls
New row: "I'll add a card for every device I have" → automate-first check.

### Reference files table
`dashboard-system.md` added. `recipes-extended.md` anchors updated R7–R14.

---

## v1.1 — 2026-05-30

### Added
- Complete Mushroom ↔ HA three-layer CSS integration (`mushroom-theme-ref.md`)
  with ZONE 6 accent-color-rgb bridge wiring all 12 palette recipes
- `references/typography-ref.md` — font loading methods, HA font variable
  catalogue, wall-panel size overrides, Alexandria self-hosting guide
- `references/recipes-extended.md` — security, energy, vacuum, bathroom,
  garage, office pop-up recipes and Streamline room templates
- `references/troubleshooting-ref.md` — 14 symptom sections
- `references/test-dashboard.yaml` — complete importable dashboard
- Bubble Card 3.2.2 source analysis: ~18 undocumented pop-up options
  documented (adaptive-dialog, correct bg_opacity/width_desktop defaults,
  empty-column card type, footer_mode, rise_animation, hide_gradient)
- Streamline Card 0.2.2 source analysis: areas context variable documented,
  !include tag confirmed in both UI-mode and YAML-mode
- Community forum findings pages 149–153: version corrections, HA 2026.4/2026.5
  compatibility notes, rows: key, sub-button font selectors, background_update
  v3.2.1 behaviour change, card-mod overflow clipping patterns
- Single-mode theme support documented for wall panels and kiosks
- Iron Law expanded to 6 rules
- Process flowchart condensed with troubleshooting-first gate
