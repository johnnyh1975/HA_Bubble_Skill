# Bubble Card source review — working log

A systematic read of the Bubble Card source, file by file, looking for
**user-visible behaviour** rather than surface. Pattern scans already cover
the surface (config keys, CSS variables and classes, action types, template
scope) and came back clean. What a scan cannot find is behaviour: defaults,
interactions between options, ordering, edge cases, and anything the card does
that no option name hints at.

**Why this file exists.** The review spans several sessions. This log records
what has been read, what was found, and what is left, so the next session
resumes instead of restarting.

- Source under review: **Bubble Card v3.4.2** (rebased from v3.4.0 — see the
  v3.4.2 diff round below), 144 non-test files, 47,582 lines
- Method: read the file, note anything that changes what the skill should
  generate or warn about, record it here, then apply it to the skill
- Not shipped in the install bundle

## v3.4.2 diff round — 2026-10-30

A version bump does **not** invalidate the per-file reads below, but it does
reopen the files it touched. Diffing is cheaper and more complete than
re-reading, so a bump is handled as a diff round first, and only the files
whose *behaviour* changed go back to `todo`.

Scope: 44 changed non-test `src/` files, 10 new ones, 2 removed
(`bubble-card.js` → `index.js`, a rename). Translations and `dist/` excluded.
Both pattern scans re-run: exactly **one** new card-level config key
(`slide_to_close`) and **three** new CSS variables, of which one is themeable.

| Re-read | Why |
|---|---|
| `components/dropdown/*` | four new lists, alarm keypad, new service calls — **done** |
| `cards/pop-up/style.js` + `editor.js` | HA-style sheet height, mode filtering — **done** |
| `cards/pop-up/slide-to-close.js` | `slide_to_close` modes; still `todo` for the gesture internals, but the option surface is read |
| `cards/pop-up/migration.js` | grid containers + placement/visibility inheritance — **done**, supersedes the `partial` row below |
| `cards/pop-up/changes.js` | trigger state across a card rebuild — **done** |
| `components/sub-button/changes.js` | `subButtonState[]` index fix — **done** |
| `components/sub-button/utils.js` | contrast-based tone replaces the threshold — re-read, finding applied |
| `tools/render-gate.js` | comparison rebuilt + settle window — **done** |
| `tools/content-inset.js` | HA 2026.6 publishes the inset; measuring is now a fallback — **done** |
| `cards/calendar/*` | event dialog, default action, live subscription — **done** |

**What the diff round caught that a release-notes read would not:** that
`popup_mode: centered` is not read at all with the HA style (so the mode in an
existing config was never doing anything), that `subButtonState[]` had been
mis-indexed since v3.1 in a way the skill documented as correct, and that the
skill's own `select_attribute` guidance named two attributes that were never on
the supported list. The first two are in the release notes only as one-line
fixes; the third is not upstream's defect at all.

**Method note for the next bump.** The `config.*` scan is what proved there was
only one new YAML key, which bounded the whole round. Run it *first* — it turns
"what changed?" into "these files, for these reasons".

## How to resume

1. Pick the next file marked `todo` in the coverage table, top-down.
2. Read it in full. Record findings under "Findings" with file and line.
3. Apply each finding to the skill, then mark the row `done`.
4. A file with nothing user-visible in it is still `done` — record "no
   user-visible behaviour" so it is not read twice.

## Coverage

Ordered by expected yield, not by size: card-near logic first, editor and
module-store internals last.

| File | Lines | Status | Note |
|---|---:|---|---|
| `cards/pop-up/helpers.js` | 3082 | **done** | mostly transition/DOM machinery; 4 user-visible behaviours found |
| `cards/pop-up/index.js` | 630 | **done** | hash scoping, condition refresh cost |
| `cards/pop-up/cards/create.js` | 1249 | **done** | fold-first hydration → card order matters |
| `cards/pop-up/slide-to-close.js` | 552 | todo | |
| `cards/pop-up/migration.js` | 914 | partial | one-shot notice + 12-column grid conversion found |
| `tools/utils.js` | 1367 | **done** | corrected a wrong domain-map entry; templated-name semantics |
| `components/slider/create.js` | 993 | **done** | min/max precedence, gesture arbitration |
| `components/sub-button/utils.js` | 559 | **done** | picture precedence, scrolling cascade, live timers |
| `components/sub-button/create.js` | 540 | **done** | class stability, mixed-group ordering |
| `components/sub-button/types/slider/index.js` | 627 | **done** | slider options do NOT inherit from the card |
| `cards/media-player/changes.js` | 667 | **done** | crossfade rewrite invalidates an old perf warning |
| `tools/tap-actions.js` | 668 | **done** | ripple gating confirms the engagement model |
| `tools/icon.js` | 533 | **done** | resolution chain; template fallback asymmetry vs name |
| `tools/text-scrolling.js` | 643 | **done** | marquee cost is bounded; little generation impact |
| `tools/ha-conditions.js` | 901 | partial | condition list enumerated; semantics unread |
| `tools/entity-suggestion.js` | 1024 | todo | picker behaviour |
| `bubble-card.js` | 606 | todo | |
| `tools/style-processor.js` | 812 | partial | template scope read |
| `cards/*/changes.js` (remaining) | ~2000 | todo | per-card-type rendering |
| `editor/bubble-card-editor.js` | 3310 | todo | editor only — low yield for YAML generation |
| `cards/pop-up/editor.js` | 1353 | todo | editor only |
| `modules/parser.js` + `yaml-schema.js` + `export.js` | ~1550 | **done** | the module *contract* — directly generation-relevant |
| `modules/store.js`, `editor.js`, `module-editor.js`, `bct-*`, `install.js`, `registry.js` | ~5500 | **skipped, deliberately** | Module Store UI and install flow. The skill never generates these and a user only meets them through the UI. Revisit only if a module the skill generated is rejected on install. |
| everything else | ~14000 | todo | |

## Feeding findings back into the eval set

A finding is only worth the reading if it survives into generated output. Six
of the behavioural findings are now eval cases 13–18, chosen as the ones where
**the correct answer contradicts what the YAML looks like it should do** —
which is exactly where a model reasoning from the config's shape goes wrong:

| Eval | Finding it tests |
|---|---|
| 13 | `state_content` replaces five legacy keys from v3.4.0, and never alongside them |
| 14 | slider options do not cascade from the card to a slider sub-button |
| 15 | a hardcoded `icon:` overrides HA's state-dependent resolution chain |
| 16 | loose sub-buttons mixed with a group are collected and moved |
| 17 | `min_value`/`max_value` are overrides that freeze the entity's range |
| 18 | the name-derived CSS class breaks on rename and translation |

The v3.4.2 round added three more, at a higher bar: in each of 19–21 the
**user's own wording describes the wrong answer**, so the model has to
contradict the request's surface and not just the config's.

| Eval | Finding it tests |
|---|---|
| 19 | `select_attribute` is a closed list of fourteen names, and a wrong one fails silently |
| 20 | `popup_mode: centered` is not read with `popup_style: home-assistant` — it was never doing anything |
| 21 | SGCC's v4.05 `styles` block and `card_*` options are Iron Law surface |

Add a case for any future finding that meets the same bar. A finding that only
adds information, without contradicting an intuition, does not need one — the
memory-leak fixes and the sidebar-offset change are both worth documenting and
neither is worth an eval.

## Findings

Newest first. Each entry: what was found, why it matters for generation, and
what changed in the skill.

### `modules/parser.js`, `yaml-schema.js` (done)

Read because the skill *generates* module YAML, so the parser's contract is
generation-relevant — unlike the Module Store UI around it, which is skipped
on purpose (see the coverage table).

- **The accepted key set is larger than documented.** Beyond the core
  (`name`, `version`, `description`, `code`, `editor`, `creator`, `link`,
  `supported`), the parser also takes `unsupported`, `is_global`, the legacy
  `form_schema` alias of `editor`, the plural/singular spellings
  `supported_card(s)` / `unsupported_card(s)`, and the legacy `author`, `type`
  and `info` container. → full table added, with the instruction to generate
  only the modern spellings; the aliases exist so old modules keep loading.
- **`unsupported:` was undocumented.** Where `supported:` is an allow-list,
  this excludes — shorter for a module that fits everything but one card type,
  and it does not need updating when Bubble Card adds a card type.
- **`is_global: true` applies a module to every card** with no per-card opt-in.
  → documented with the warning that it makes `#module-performance` mandatory
  rather than optional, since the code then runs on every style pass of every
  card.
- **`!include` works inside module YAML**, resolved against `/local/bubble/`,
  fetched synchronously over XHR. → documented as the way to keep a long
  `code:` block in its own file.

### `components/sub-button/types/slider/index.js` (done)

- **Slider sub-buttons inherit nothing from the card** (l.12). The slider
  config is assembled from `subButton.*` only — `tap_to_slide`,
  `relative_slide`, `read_only_slider`, `slider_live_update`,
  `invert_slider_value`, `slider_fill_orientation`, `slider_value_position`,
  `use_accent_color`, `min_value`/`max_value`/`step`, and the light and cover
  options. Setting any of them on the card does nothing for a
  `sub_button_type: slider`. → documented, with the explicit warning that this
  is **not** the same rule as `scrolling_effect`, which does fall back to the
  card: the cascade is per-option, so neither direction can be assumed.
- An unset option stays genuinely absent rather than being defaulted, which is
  what lets direction-aware defaults work: `slider_value_position` follows the
  document's reading direction in RTL languages when unset, and pinning it to
  `right` breaks that. → noted.
- **Corrected an imprecision I introduced:** `show_button_info` forces
  `slider_value_position: right` only in combination with
  `always_visible: true`; on a tap-to-open slider the configured position still
  applies. The table said it forced it unconditionally.

### `tools/text-scrolling.js` (done)

Little generation impact, but it settles whether `scrolling_effect` is cheap.
Only text that actually overflows gets a marquee (measured in float since
integer rounding hid up to 3 px of real overflow, #2462); a marquee holds a
composited layer **only while its element is genuinely on screen**, with a
second, wider observer doing the measuring early so it is ready on arrival;
measurement is batched per frame and held entirely during a pop-up open.
→ the option row now says leaving it on costs nothing for short labels, and
points at the motion-sensitivity rule for when to turn it off anyway.

### `tools/icon.js` (done)

- **`icon:` and `name:` treat an empty template result oppositely** (l.310).
  An icon template rendering nothing — or not yet rendered — falls through to
  the entity's own icon, as an absent `icon:` would. A name template shows the
  empty string. So a conditional icon template is safe without a default while
  a conditional name template is not. → documented as a pair, since the two
  sit next to each other in `#ha-templates` and the asymmetry is invisible.
- **Setting `icon:` overrides HA's whole resolution chain** (l.230): configured
  icon → entity-registry icon set in the HA UI → platform icons → domain state
  icons (a lock showing open vs closed) → `device_class` icons → domain
  fallback. A hardcoded `icon:` therefore also kills the state-dependent icon a
  user expects. → added a "usually don't set it" note, which also reduces
  generated YAML.

### `tools/tap-actions.js` (done)

- **`tap_action: none` removes the press feedback** (l.294). The ripple and the
  `bubble-action-enabled` class are attached only when at least one of tap,
  double-tap or hold is not `none`. A card with all three at `none` therefore
  *looks* non-interactive rather than merely behaving that way. → This is a
  mechanical argument for the engagement-type model's rule that Overview cards
  carry `tap_action: none` explicitly: it is the difference between a card that
  ignores a tap and one that never invited one. Documented next to the action
  table.
- **Hold fires at 500 ms**; the documented 200 ms double-tap delay is correct
  as written (verified). → hold duration added.
- Movement cancels a tap, with a larger dead zone before it cancels a hold, so
  a press that drifts during a scroll does not fire and a hold survives a small
  tremor. → noted as the explanation for "taps sometimes don't register" on a
  scrolling dashboard.
- Being hidden abandons any armed interaction: the companion app's system
  swipe suspends the page mid-gesture without sending a cancel, which used to
  leave a button pressed and fire it on the next touch anywhere. Internal.

### `components/sub-button/create.js` (done)

- **Every sub-button carries three classes, only one of them stable** (l.466).
  `.bubble-sub-button-<index>` (key with `_` rewritten to `-`), a class derived
  from `name:` (lowercased, accents stripped, non-alphanumerics collapsed, so
  `Küche Licht` → `.kuche-licht`), and `.<css_class>` if set. The name-derived
  one **breaks on a rename and on a translated name**, and is not generated at
  all for a templated `name:`. → sharpens the `css_class` recommendation in
  `#css-selectors`, which previously said only "prefer css_class": now it says
  which of the three to target and why, with the warning that a user who
  translates their dashboard loses every style hung on a name.
- **Mixing loose sub-buttons with explicit groups reorders them** (l.86). All
  loose buttons in a section are collected into one automatic group placed
  where the *first* of them appeared, rather than interleaved in YAML order —
  the same thing the editor does when converting a mixed section. → documented
  with a before/after example and the fix (make every section an explicit
  group when order matters).
- Group containers are inserted by declaration rank rather than appended, so a
  group whose buttons only exist under some conditions no longer lands last
  (#2517). Internal, but it is why conditional groups keep their place.

### `cards/media-player/changes.js` (done)

- **A stale performance warning removed.** The skill said `cover_background`
  "fetches album art on every state change — avoid on dashboards with many
  simultaneous media players". The crossfade was rewritten because the old one
  raced with itself; it now keys on the target image (asking again does
  nothing), runs one fade at a time with later requests queued rather than
  stacked, and keeps only the last queued request — so holding "next" costs one
  extra fade, not one per press. A playing player emitting many updates per
  second no longer re-fetches. → warning rewritten; the remaining cost is image
  decode.
- The rest of the file is crossfade layer management with no YAML surface.

### `components/sub-button/utils.js` (done)

- **Entity-picture precedence** (l.11): a sub-button on an entity with an
  `entity_picture` shows it instead of an icon; `force_icon: true` or the
  sub-button's **own** `icon` suppresses it — the card's icon does not. So a
  person sub-button meant to show a face needs no `icon:`, and one meant to
  show an icon needs its own rather than `force_icon` on the card. → documented.
- **`scrolling_effect` cascades**: sub-button → card → `true`. → added as a row
  with its real default chain.
- **Timer entities tick live** (l.84): a sub-button on a `timer` whose state
  line includes `state` or `remaining_time` counts down on its own beat while
  active, since the entity itself does not update per second. → documented as a
  consequence of the state line, nothing to configure.
- Hidden sub-buttons are momentarily revealed during measurement so a row
  reserves the tallest layout it can take (#2517) — internal, but it explains
  why conditional sub-buttons do not make rows jump.

### `components/slider/create.js` + `slider/helpers.js` (done)

- **`min_value` / `max_value` / `step` are overrides, not descriptions**
  (`helpers.js` l.131). Left unset the slider reads the entity: `min_temp` /
  `max_temp` for climate, the `min` / `max` / `step` attributes otherwise,
  falling back to 0/100/1. Copying an entity's current attribute values into
  the card freezes them — the card keeps the old range after the entity's
  changes in HA. → documented as precedence, and the `number` domain-map row
  rewritten (it previously told the reader to set them "matching entity",
  which is exactly the freeze).
- **Safety clamp** when max is not above min: climate gets min + 1, everything
  else min + 100. A slider stuck at a pinned value is usually an override
  colliding with the entity. → documented as a diagnostic.
- Gesture arbitration: movement on the secondary axis beyond a threshold is
  read as a scroll and releases the slider; an edge-start swipe is left to HA's
  sidebar, notably in the iOS app. Behavioural, no generation impact — but it
  is why a slider near the screen edge can feel unresponsive on iOS.

### `tools/utils.js` (done)

- **Correction to a skill error.** The entity domain map claimed `water_heater`
  had "no Bubble Card support". `isStateOn` (l.414) handles it explicitly: a
  water heater has no `on`, its state is the operation it runs, so anything
  other than `off`/`unknown`/`unavailable` reads as active — the same rule HA
  uses in `stateActive`. So a `button_type: state` card shows and colours it
  correctly; only toggling and sliding are unavailable. → entry rewritten, and
  the domain-list paragraph now separates *control* (the toggle/slider sets)
  from *display* (a broader active-state rule covering numeric states, `open`,
  `playing`, `locked`, `cleaning` and water-heater operations).
- **A templated `name:` has no fallback** (l.349): a plain `name:` falls back
  to the friendly name when absent, a template shows exactly what it returns,
  empty included. A template that can evaluate to nothing leaves the card
  blank. → documented with the `or 'default'` pattern.
- Rendered template output is HTML-escaped where the name is written as markup
  — treated as entity data, not author markup. → noted.
- Relative-time fields share **one page-wide 60-second beat** that stops while
  the page is hidden and catches up on return, rather than one timer per
  element. Supports the header cost note from `index.js`: the beat is cheap,
  the full header refresh it triggers is not.

### `cards/pop-up/cards/create.js` (done)

- **Fold-first hydration** (l.~255). A large pop-up renders only enough leading
  cards to cover the first viewport before the open transition — the fold is
  estimated from each card's grid span, with no layout read — and the rest
  start as placeholder cells hydrated one budgeted step at a time afterwards.
  Off-screen cards also skip `hass` assignments until scrolled in. → **Card
  order in `cards:` now has a performance meaning**, not just a visual one:
  the most-used control belongs first or the user waits for hydration. Applied
  next to the pop-up placement rules.
- Budgets are split by phase: 300 ms per step during the covered pre-open build
  (nothing visible, batching wins), 24 ms per step once the pop-up is visible
  (scroll must stay fluid). Internal, no generation impact.

### `cards/pop-up/index.js` (done)

- **`time` and `template` conditions in a pop-up header force a full header
  refresh on every HA state change anywhere** (l.238). Bubble Card memoises the
  header against the entities its conditions reference; these two cannot be
  tracked that way. A relative-time field in the header does the same. → cost
  note added beside the condition table, pointing at the entity-based
  alternative, which the automate-first principle already favours.
- **Hash registration is keyed on the dashboard path** (l.161), so a hash must
  be unique *within a dashboard*, not globally. `#settings` on two dashboards
  is fine and common. → the `hash` row said "unique" without qualification;
  corrected.
- A templated `name:`/`icon:` is resolved for HA's navigation picker, so a
  pop-up appears there with what it shows rather than raw template text. →
  added to `#ha-templates`.
- Editor-preview copies stay out of hash registration, so a pop-up does not
  look duplicated by its own preview. No generation impact.

### `cards/pop-up/helpers.js` (done)

The bulk of the file is transition timing, shell lifecycle and DOM-boundary
work with no YAML surface. Four behaviours matter for generation:

- **`performance_mode` deferral applies only to `popup_mode: default`**
  (l.158). Content deferral was tried for `adaptive-dialog` and reverted: it
  pushed the open 120 ms past the end of the slide on an iPad 6 for no gain.
  Performance mode still helps on other modes through its other effects (no
  backdrop blur, lighter opening CSS) — just not through deferral. → documented
  next to the pop-up mode table, since pairing the two expecting deferral is
  the mistake this invites.
- **Why pop-ups must be top-level, mechanically** (l.666). A pop-up suspends
  the `hui-card` cell hosting it so it reserves no height. Placed inside a
  grid/masonry/`layout-card`, it has no own cell — the nearest wraps the whole
  view, and suspending that would collapse every card — so Bubble Card treats
  the layout host as a boundary and suspends nothing. The pop-up then reserves
  visible empty space. → added as the mechanism behind the existing rule.
- **`close_on_click` on touch ignores scrolls and drags** (l.2334): movement
  beyond ~10 px reads as a gesture, not a tap. And native HA buttons inside a
  pop-up now work with it — they suppress the synthetic click, which Bubble
  Card compensates for since v3.4.0 (#2573). → option description extended.
- **Speculative shell warm-up** (l.2833): every registered pop-up's shell
  (header and structure, no cards) is built at idle after the dashboard loads.
  Nothing to generate, but it explains why a dashboard with many pop-ups costs
  a little memory at rest and why the first open is fast.

Not applied, no generation impact: `location-changed` is replaced by a private
event type because HA 2026.9 answers it with `history.replaceState` calls and
Safari throws past 100 per 10 s (#2606); several transition fixes
(#2548, #2532/#2533/#2544/#2552) that only affect how the open animates.

### `cards/pop-up/migration.js` (partial)

- **The legacy-pop-up migration notice is one-shot.** Dismissal is recorded in
  `localStorage`, so it never appears again. A user who clicked it away will
  not find it, and may believe migration is unavailable. Migration remains
  reachable by editing the legacy card. → troubleshooting entry added.
- **Migration reflows content cards into a 12-column grid**
  (`POPUP_GRID_COLUMN_COUNT = 12`), dropping per-card column settings that no
  longer apply and keeping auto-height only where it still makes sense. Cards
  come out at different widths on purpose. → troubleshooting entry added.

### Method check (not a file)

Tested the pattern-scan method for its own blind spots: no config key is read
only via destructuring (`const { x } = config`) or bracket notation, so the
`config.x` scan was not missing options. One editor-only key, `style_templates`,
already documented as the legacy alias of `modules`.
