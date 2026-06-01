# Troubleshooting Reference
# ha-bubble-dashboard skill
# Covers: symptom → cause → fix for all common failure modes.
# Start here when something is broken before generating new YAML.

---

## #first-steps

### Always run these three steps first

Whatever the symptom, these three steps resolve 60% of Lovelace issues:

1. **Hard refresh browser** — Ctrl+Shift+R (Win/Linux) or Cmd+Shift+R (Mac).
   Clears cached JS bundles. Required after any config change.
2. **Check browser console** — F12 → Console tab. Any red errors point directly
   to the broken card, resource, or YAML key.
3. **Check HA logs** — Settings → System → Logs. Filter for `lovelace` or `bubble`.
   HA-level errors (bad YAML, missing integration) appear here, not in the browser.

Run these before using any specific symptom section below.

---


## #cache-issues

### Symptom: changes not appearing after editing dashboard or templates

The single most common issue. HA and browsers aggressively cache Lovelace
resources.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Card changes not visible | Browser cache | Hard refresh: Ctrl+Shift+R (Win/Linux) or Cmd+Shift+R (Mac) |
| Streamline template "not found" after adding | Old JS bundle cached | Hard refresh + HA restart |
| New theme not in profile dropdown | Theme not loaded | Developer Tools → Actions → `frontend.reload_themes` |
| Custom card missing after HACS install | Resource not registered or cached | Clear cache + HA restart |
| Module changes not taking effect | Bubble Card Tools cache | Hard refresh; if persistent, HA restart |

**Run `#first-steps` first.** Then:
1. Developer Tools → Actions → `frontend.reload_themes` (theme-related)
2. Restart Home Assistant (if custom card or Streamline template issue)
3. Clear browser storage: DevTools → Application → Storage → Clear site data

---

## #theme-not-applying

### Symptom: theme selected in profile but colours unchanged

| Symptom | Cause | Fix |
|---------|-------|-----|
| All HA colours unchanged | Theme YAML key doesn't match file/theme name | The YAML key (e.g. `Casa5HeyneV2:`) must exactly match what appears in Profile → Theme. No spaces difference. |
| Theme shows in dropdown but doesn't apply | File not in `/config/themes/` directory | Confirm path: `/config/themes/YourTheme.yaml` |
| Theme loads but Bubble Cards use wrong colours | `--bubble-*` variables not pointing to `var(--primary-color)` | Check `bubble-accent-color` in global section — must be `"var(--primary-color)"` not a hex value |
| Light/dark colours swapped | `modes.light`/`modes.dark` content accidentally transposed | Compare background-color values: light should be `#F8F8F8`, dark should be `#202631` |
| Theme applies to HA but not Bubble Cards | Bubble Card version mismatch with CSS variable names | Check `bubble-card-ref.md#version-compat` — some variables changed between v3.0 and v3.2 |
| `frontend.reload_themes` action not found | HA version < 2023.x | Use Developer Tools → Services (deprecated UI) → `frontend.reload_themes` |
| Alexandria font not loading | `extra_module_url` missing or font JS file absent | Add to `configuration.yaml`: `frontend: extra_module_url: - /local/alexandria-font.js` — verify file exists at `/config/www/alexandria-font.js` |

**Diagnostic steps:**
1. Open HA DevTools → Template — run `{{ states('sensor.anything') }}` to confirm HA is responsive
2. Open browser DevTools → Elements — inspect a `ha-card` element and check computed CSS variables
3. Look for `--bubble-accent-color` in computed styles — if it shows a hex value, the theme global block is wrong

---

## #popup-not-opening

### Symptom: clicking a button does nothing or navigates away from dashboard

| Symptom | Cause | Fix |
|---------|-------|-----|
| Button does nothing | `navigation_path` hash doesn't match pop-up `hash` | Hash must be identical including `#` prefix: `'#living-room'` on both the button and the pop-up |
| Pop-up hash mismatch | Case difference | Hashes are case-sensitive. Use lowercase-hyphenated: `'#living-room'` not `'#Living-Room'` |
| Navigates to a different view instead of opening pop-up | Pop-up not a top-level card in the current view | Pop-ups must be in `cards:` at the view level, not inside `sections:` or any stack |
| Pop-up flickers and closes immediately | `close_by_clicking_outside: true` combined with tap_action on the triggering button | Set `close_by_clicking_outside: false` on the pop-up, or restructure the trigger |
| Pop-up opens but is empty | `cards:` block missing or indented wrong | v3.2+ pop-ups require a `cards:` key — verify YAML indentation |
| Pop-up content cut off at bottom | `with_bottom_offset` not set | Add `with_bottom_offset: true` when HBS footer is present |
| Pop-up too wide on mobile | `width_desktop` set too large | `width_desktop` only applies to desktop — pop-ups are full-width on mobile by design |
| Trigger entity not opening pop-up | `trigger_entity` + `trigger_state` mismatch | Verify the entity's state string exactly — use Template DevTools to check |

**Quick diagnostic:**
- Open browser console (F12) and navigate to the pop-up hash manually: type `#living-room` in the URL bar after `/lovelace/home`. If the pop-up opens, the issue is with the button's `navigation_path`, not the pop-up itself.

---

## #streamline-not-found

### Symptom: "template not found" or card shows error

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Template 'X' not found` error on card | Template name typo, or file not loaded | Check exact spelling — template names are case-sensitive. Then hard refresh + HA restart. |
| Template works then stopped | Browser cache after HA update | Hard refresh browser. Note: Streamline revalidates templates in the background after the first load — most template edits propagate without a hard refresh. HA restart only required if the card resource itself is missing (HACS reinstall). |
| Template file changes not reflected | File saved but browser shows old content | HA restart required after editing `streamline_templates.yaml` |
| `!include_dir_named` parse error | User is on UI-mode Lovelace, not YAML-mode | Only valid in YAML-mode. UI-mode users must use the auto-load file at `/config/www/community/streamline-card/streamline_templates.yaml` |
| Template loads but `[[variable]]` not substituted | Variable name mismatch between template and usage | Check exact variable name spelling in both the template `default:` block and the `variables:` list at the call site |
| `styles_javascript` not evaluating `[[entity]]` | `[[variable]]` is substituted as a string before JS runs | The substituted value in JS will be a plain string — use it directly: `states['[[entity]]'].state` (works because `[[entity]]` is replaced with the actual entity ID before JS evaluation) |
| "Visual editor not supported" warning | Expected — not an error | Streamline Card has no visual editor. Always edit in raw YAML mode. |

---

## #sidebar-not-showing

### Symptom: Sidebar Card invisible, mispositioned, or showing errors

| Symptom | Cause | Fix |
|---------|-------|-----|
| Sidebar not visible at all | `sidebar:` config not at root of dashboard YAML | `sidebar:` must be at the same indent level as `views:`, not inside a view |
| Sidebar missing on desktop only | `width.desktop` set to 0 | Set `width: { desktop: 20 }` |
| Sidebar missing on mobile | Expected — use `width: { mobile: 0 }` pattern | Mobile nav is handled by HBS footer. This is correct behaviour. |
| JS resource error in console | Resource not registered | Settings → Dashboards → ⋮ → Resources → verify `/hacsfiles/sidebar-card/sidebar-card.js` is listed as JavaScript Module |
| `bottomCard` fails on refresh (`setConfig is not a function`) | Known v0.1.9.9 bug | Refresh page again. For critical content, use a Bubble Card sub-buttons footer instead. |
| `showTopMenuOnMobile` not working | HA 2026.1 mobile overhaul changed behaviour | Test on the installed HA version. May need `hideHassSidebar: false` as workaround. |
| Sidebar overlaps content | Width too large | Reduce `width.desktop` from default — try `18` or `20` percent |
| Template messages not updating | Jinja2 template syntax error | Test template in Developer Tools → Template first |
| Clock not showing | `clock: true` or `digitalClock: true` not set | Both are `false` by default — explicitly set one to `true` |

---

## #bubble-styling-ignored

### Symptom: `styles:` block has no visible effect

| Symptom | Cause | Fix |
|---------|-------|-----|
| CSS in `styles:` not applying | CSS specificity too low | Add `!important` to the specific property |
| `styles:` with JS template (`${...}`) has no effect | DOM manipulation placed before CSS assignments | JS DOM statements (`setAttribute`, `.innerText =`) must come AFTER all CSS property assignments in the `styles:` block |
| Background colour not changing | Wrong CSS selector | Use `ha-card` for the card container, `.bubble-button-background` for the coloured fill layer |
| Icon not changing with JS template | Wrong element reference | Use `icon.setAttribute("icon", "mdi:...")` — `icon` is the pre-bound element reference |
| Sub-button CSS selector not matching | Sub-button class name not matching | Classes are generated from the sub-button name. Spaces become dashes, lowercase. `My Button` → `.my-button`. Alternatively use positional: `.bubble-sub-button-1` |
| `var(--theme-variable)` not resolving in `styles:` | Variable not defined in theme | Check that the variable exists in `css-theme-ref.md#light-mode` or `#dark-mode` |
| Module not applying | Module not listed in `modules:` on card, or Bubble Card Tools integration not installed | Verify Bubble Card Tools integration is added in Settings → Integrations |

---

## #version-migration

### Symptom: YAML that worked before is now broken after Bubble Card update

| Version jump | What broke | Migration fix |
|-------------|-----------|---------------|
| Pre-v3.0 → v3.0+ | Module system changed | Old per-card CSS modules need converting to new YAML file format in `/config/bubble_card/modules/` |
| Pre-v3.1 → v3.1+ | `subButtonIcon[N]` index order | Bottom sub-buttons now indexed first. Recount all JS template sub-button references. |
| Pre-v3.2 → v3.2+ | Pop-up format completely changed | Pop-ups must be standalone top-level cards with `cards:` block. The UI shows a migration prompt — use it, then review generated YAML. |
| Pre-v3.2 → v3.2+ | `bubble-pop-up-fix.js` removed | Remove any reference to this script from resources. |
| Pre-v3.2 → v3.2+ | Pop-up modes added | Existing pop-ups get `popup_mode: default` automatically. Optionally migrate to `fit-content` or `centered` where appropriate. |

**Migration checklist for v3.2+ upgrade:**
- [ ] Run the in-UI migration (Dashboard → edit → HA prompts to migrate pop-ups)
- [ ] Remove `bubble-pop-up-fix.js` from resources if present
- [ ] Verify all pop-ups are now standalone top-level cards with `cards:` block
- [ ] Check `subButtonIcon[N]` references if using JS templates with sub-buttons
- [ ] Clear browser cache after migration

---

## #hbs-not-ordering

### Symptom: HBS footer doesn't reorder by room activity

| Symptom | Cause | Fix |
|---------|-------|-----|
| `auto_order: true` but order never changes | No `N_pir_sensor` defined for buttons | Add `N_pir_sensor: binary_sensor.room_motion` for each button. Without sensors, disable `auto_order`. |
| Order resets on page load | Expected — `auto_order` sorts by last-triggered sensor at load time | This is correct behaviour. The most recently active room appears first. |
| Buttons not highlighting active view | `highlight_current_view: false` | Set `highlight_current_view: true` |
| HBS overlapping page content | `with_bottom_offset` not set on pop-ups | Set `with_bottom_offset: true` on every pop-up in the view |
| HBS not full-width on desktop | `width_desktop` set | Remove or increase `width_desktop` — default is `100%` |

---

## #sections-layout-issues

### Symptom: cards not laying out as expected in sections view

| Symptom | Cause | Fix |
|---------|-------|-----|
| All cards stacking in one column | `max_columns` not set or set to 1 | Set `max_columns: 3` for "both equally" layouts |
| Pop-up not found / won't open | Pop-up placed inside `sections:` block | Pop-ups must be top-level `cards:` entries, not inside any section |
| Card not spanning full width | `column_span` not set on section | Add `column_span: 3` (or `max_columns` value) to the section containing the card |
| HBS footer inside a section | HBS placed inside `sections:` | HBS must be a top-level `cards:` entry after the `sections:` block |
| Unexpected gaps in grid | Empty sections or mismatched column spans | All column spans across a row should sum to `max_columns` |
| Section row gaps larger than expected after HA update | HA 2026.4 increased the default `ha-view-sections-row-gap` value | Add to your theme: `ha-view-sections-row-gap: "4px"` or set per-view in raw config under `theme_options:` |

---

## #cardmod-overflow-clipping

### Symptom: card border-radius or box-shadow clipped inside pop-ups

When using a global `card-mod-card` theme rule that sets `overflow: hidden`,
`border-radius`, or `box-shadow`, cards inside Bubble Card pop-ups are clipped —
rounded corners and shadows get cut off on all sides.

| Symptom | Cause | Fix |
|---------|-------|-----|
| Card corners clipped inside pop-up | Pop-up container applies its own `overflow: hidden` context | Add `overflow: visible !important` to `.bubble-pop-up-inner` in your card-mod rule |
| `box-shadow` invisible inside pop-up | Same overflow context issue | Same fix — or use `filter: drop-shadow()` instead of `box-shadow` (not affected by overflow) |
| Works on dashboard, fails only in pop-up | Global card-mod rule conflicts with pop-up container | Scope your card-mod rule to exclude pop-up contents: add `:not(.is-popup) ha-card { ... }` |

**Workaround CSS** (add to your global `card-mod-card` or theme `card-mod-theme`):
```css
/* Allow pop-up inner container to show overflow from child cards */
.bubble-pop-up-inner {
  overflow: visible !important;
}
/* or scope your rule to exclude pop-up children */
:not(.bubble-pop-up) ha-card {
  border-radius: 28px;
  overflow: hidden;
  /* your other styles */
}
```

**Skill note:** The skill recommends avoiding `card-mod` on Bubble Cards entirely.
If you need global card styling, use a Bubble Card module (`is_global: true`) instead
of `card-mod-card` — Bubble Card modules do not conflict with the pop-up overflow context.

---

## #general-diagnostic-checklist

When stuck and the specific symptom isn't listed above, run through:

```
1. Run #first-steps (hard refresh, console, HA logs) — see top of file
2. Inspect CSS variables in DevTools:
   - Open DevTools (F12) → Elements tab
   - Click on a `ha-card` element in the DOM
   - In the Styles panel, look at "Computed" tab
   - Search for: --bubble-accent-color, --accent-color, --ha-card-background
   - If --bubble-accent-color shows a hex value (not var()) → theme var() chain broken
   - If --accent-color shows #7B7B7B (HA default) → theme not applied to this element
4. Check HA logs: Settings → System → Logs (filter for "lovelace" or "bubble")
5. Verify YAML syntax: paste into yamlchecker.com or use HA raw editor validation
6. Confirm component versions: HACS → check Bubble Card, Streamline Card versions
7. Test in a fresh browser profile (rules out extensions interfering)
8. Disable other custom cards temporarily (rules out conflicts)
```

---

## #sub-buttons-not-showing

### Symptom: sub-buttons not rendering or showing incorrectly

| Symptom | Cause | Fix |
|---------|-------|-----|
| Sub-buttons completely missing | `sub_button:` at wrong indentation level | Must be a direct child of the card config, not nested inside another key |
| Main sub-buttons not showing | `main:` block missing or using old flat list syntax | v3.1+ requires `sub_button: main: - ...` and `sub_button: bottom: - ...` structure |
| Bottom sub-buttons not showing | `bottom:` block missing the `group:` key | Bottom sub-buttons require a `group:` list inside the bottom section |
| Sub-button shows wrong icon | `subButtonIcon[N]` index wrong in JS template | v3.1+: bottom sub-buttons are indexed first. Recount from 0 starting at first bottom button |
| Sub-button background always grey | `state_background: false` set, or entity is unavailable | Check entity is available; set `state_background: true` for state-coloured background |
| Sub-button width wrong on bottom | `fill_width: true` (default) stretches each item | Set `fill_width: false` for chip-style buttons in a bottom group |
| Slider sub-button not draggable | `read_only_slider: true` set | Remove or set to `false` to enable interaction |
| Select sub-button shows no options | `select_attribute:` value doesn't match a real attribute | Check actual attribute name in Developer Tools → States → entity |
| Bottom group not inline | `buttons_layout: inline` not set | Add `buttons_layout: inline` to the bottom group object |

**Quick sub-button structure reference:**
```yaml
sub_button:
  main:                          # right side of card
    - entity: sensor.battery
      show_icon: true
      show_background: false
  bottom:                        # full-width row below card
    - name: Quick actions
      buttons_layout: inline
      justify_content: center
      group:                     # required for bottom
        - entity: light.room
          fill_width: false
```

---

## #card-state-stale

### Symptom: card state not updating / showing stale values

| Symptom | Cause | Fix |
|---------|-------|-----|
| Card shows old state after entity changes | HA WebSocket connection dropped | Reload the page (not hard refresh) — WebSocket reconnects automatically |
| Card permanently stuck on one state | Entity unavailable in HA | Check HA Developer Tools → States — if state shows "unavailable", the integration has a problem, not the dashboard |
| Streamline card not updating | `_javascript` expression error returning `undefined` | Open browser console — JS errors from Streamline are logged there. Add null safety: `states['entity']?.state ?? 'off'` |
| Pop-up content not updating when open | Pop-up renders cards on open; some cards don't auto-refresh | Add `background_update: true` on any Bubble Card inside a pop-up that must update live (note: increases resource use) |
| Sensor value updating in HA but not on card | Card render is throttled | This is expected — Lovelace throttles renders. Not a bug. |
| Slider position doesn't match actual brightness | `slider_live_update: false` (default) | The slider updates on release, not while dragging. Set `slider_live_update: true` to change this (not recommended on slow networks). |
| Media player art not refreshing | `cover_background: true` caches the image URL | HA appends a cache-buster to image URLs — if the media player integration doesn't update the artwork URL, the image won't refresh. Integration issue, not Bubble Card. |

---

## #font-not-loading

### Symptom: font not loading / dashboard showing system font

> **Full troubleshooting is in `typography-ref.md#font-troubleshooting`** — covers
> all symptoms, causes, and fixes for all font loading methods.

**Quick fixes for the most common cases:**

| Symptom | Most likely cause | Quick fix |
|---------|------------------|-----------|
| System font everywhere | `extra_module_url` missing | Add `/local/alexandria-font.js` to `configuration.yaml` → restart HA |
| JS file not found error | File not at `/config/www/` | Create at `/config/www/alexandria-font.js` — see §1 Installation step 5 |
| Works on desktop, not Companion App | Google Fonts CDN blocked | Self-host font files locally — see `typography-ref.md#alexandria` |
| Theme applies but font still wrong | Legacy `paper-font-*` variables missing | Add all 7 `paper-font-*` variables to mode-independent theme block |
| Font flashes on load | Google Fonts async loading (expected) | Use `font-display: block` with self-hosted files to eliminate |

---

## #popup-z-index

### Symptom: pop-up opens behind other elements or is partially hidden

| Symptom | Cause | Fix |
|---------|-------|-----|
| Pop-up appears behind the HBS footer | HBS footer has a higher z-index | Set `z_index: 5` on the pop-up (default is 3). Only use if confirmed z-index conflict. |
| Pop-up clipped at top or sides | `margin_top_mobile` or `width_desktop` too aggressive | Remove or reduce `margin_top_mobile`. Default width is correct — don't force 100% on desktop. |
| Pop-up visible but backdrop missing | `shadow_opacity` set to 0 | Set `shadow_opacity: 30` for a subtle backdrop |
| Pop-up not dismissing when clicking outside | `close_by_clicking_outside: false` explicitly set | Change to `true` (the default) |
| Pop-up opens at wrong position on tablet | `popup_mode: default` doesn't centre on mid-size screens | Try `popup_mode: centered` for better tablet positioning |
| Multiple pop-ups open simultaneously | `close_by_clicking_outside: false` on all + navigation buttons | Ensure each pop-up's close button is visible, or add `auto_close: 30000` |
| Second pop-up requires two taps to open | v3.2.x behaviour change — navigating to a new hash closes the current pop-up first | Expected. Add a dedicated "go to X" button inside each pop-up that closes the current one and opens the next: use `navigation_path` to the new hash. Users need one more tap; design the navigation flow around this. |
| Cards inside pop-up have clipped corners or shadows | Global card-mod rule with `overflow: hidden` conflicts with pop-up container | See `troubleshooting-ref.md#cardmod-overflow-clipping` |
| Pop-up not visible at all after navigating to hash | Pop-up card not a top-level view card | Pop-ups must be in `cards:` at the view root — not inside `sections:`, not inside any stack. See Iron Law: PLACEMENT. |
