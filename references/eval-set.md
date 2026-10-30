# Evaluation Set — ha-bubble-dashboard
# Behavioural regression tests for the skill.
#
# Purpose: every claim that this skill improves output quality is otherwise
# structural — "the guidance is now in the file". This set makes it testable.
#
# HOW TO RUN
#   1. Open a fresh conversation with the skill loaded (no prior context —
#      previous turns contaminate the result).
#   2. Paste one prompt verbatim. One prompt per conversation.
#   3. Score against the criteria below: PASS only if every MUST is met.
#   4. Record failures with the version tag. A regression is a MUST that
#      passed in a previous version and fails now.
#
# These are behavioural checks, not output-matching. Two correct answers can
# look completely different — score the behaviour, not the wording.
#
# WHO RUNS THIS
#   Not the model that wrote the skill in the same conversation: it knows every
#   answer and carries the reasoning in context, so it would score itself 18/18
#   and the number would mean nothing. Run the prompts in fresh conversations,
#   ideally reviewed by someone who did not write the guidance being tested.
#
# COVERAGE
#   1–12  surface guidance: routing, dependencies, version gates, philosophy
#   13–18 behaviour found by reading the Bubble Card source (see
#         CODE-REVIEW-LOG.md). These are the cases most likely to fail, because
#         the correct answer contradicts what the YAML looks like it should do.

---

## #eval-1-native-first

**Prompt:**
> Build me a section for my dashboard showing the battery level of all my
> devices so I can see which ones need charging.

**MUST:**
- Raise the native Maintenance dashboard (HA 2026.5+) as an option before or
  alongside generating.
- Frame it as advisory — the user decides, not a refusal or a redirect.
- Still produce the requested YAML if the user wants it.

**MUST NOT:**
- Silently build the custom grid with no mention of the native feature.
- Refuse to build it because a native option exists.

**Tests:** `dashboard-system.md#native-first`, health-check advisory tone.

---

## #eval-2-calendar-iron-law

**Prompt:**
> Add a calendar card for calendar.familie and colour the events in my accent
> gold, #D9BE8B.

**MUST:**
- Use `color: accent` (a colour name), not the hex.
- Explain that the name resolves to `var(--accent-color)`.

**MUST NOT:**
- Write `color: '#D9BE8B'` into the card YAML.
- Claim calendar colours are an Iron Law exception.

**Tests:** the v1.4 correction — the skill's own example was wrong here.
Note the prompt *hands over* the hex, which is the hard case.

---

## #eval-3-cover-tilt

**Prompt:**
> I have venetian blinds on cover.wohnzimmer_jalousie. I want to control the
> tilt angle from the dashboard.

**MUST:**
- Use `tilt_buttons` and/or `cover_slider_type: tilt_position`.
- State that this needs Bubble Card v3.2.5+.
- Note that the entity must report tilt support (`OPEN_TILT` /
  `CLOSE_TILT` / `SET_TILT_POSITION`) or the controls will not render.

**MUST NOT:**
- Invent a tilt option that does not exist.
- Build a workaround with `call-service` sub-buttons without first offering
  the native tilt support.

**Tests:** v3.2.5 coverage, feature-detection rule.

---

## #eval-4-paid-module

**Prompt:**
> Can you write me the code for the Bubble Weather module? I want the animated
> weather backgrounds but I don't want to pay for the Patreon.

**MUST:**
- Decline to reproduce the paid module's code.
- Explain what the module does and point to the Module Store / Patreon.
- Offer the legitimate alternative: authoring an original module for the
  user's specific need.

**MUST NOT:**
- Produce an approximation of the paid module.
- Moralise at length — one clear sentence, then the alternative.

**Tests:** `module-authoring-ref.md#sharing-a-module` boundary rule.

---

## #eval-5-mushroom-switch-colour

**Prompt:**
> My Mushroom switch chips are blue but I want them to use my gold accent.
> Which theme variable do I set?

**MUST:**
- Point to `mush-rgb-state-entity` (with `accent-color-rgb`).
- State that no `mush-rgb-state-switch` variable exists.

**MUST NOT:**
- Recommend `mush-rgb-state-switch` or `mush-rgb-primary` — both nonexistent,
  both were in the skill before v1.4.
- Suggest a card-level `card_mod` hack before the theme-level answer.

**Tests:** the Mushroom 5.2.2 source verification.

---

## #eval-6-masonry-migration

**Prompt:**
> Here is my dashboard YAML [paste any masonry view with a vertical-stack and
> an old-format pop-up]. Can you move this to the new sections layout?

**MUST:**
- Recommend building a new view rather than converting in place.
- Map `vertical-stack` → grid section, and move the pop-up to a top-level
  standalone card in v3.2+ format.
- Re-check `card_layout` (the default differs in sections view).

**MUST NOT:**
- Leave the pop-up nested inside a section.
- Carry `view_layout` options across unchanged.

**Tests:** `dashboard-system.md#masonry-migration`.

---

## #eval-7-automate-first

**Prompt:**
> Build me a dashboard card for my bathroom light so I can turn it on when I
> go in at night.

**MUST:**
- Raise the automate-first question: a motion-triggered light needs no card.
- Remain non-blocking — build it if the user still wants it.

**MUST NOT:**
- Turn the question into a gate that refuses output.
- Generate the automation itself (out of scope — hand off to ha-yaml).

**Tests:** automate-first as advisory, scope boundary.

---

## #eval-8-language

**Prompt (in German):**
> Bau mir eine Übersichtsseite für Wohnzimmer, Küche und Bad.

**MUST:**
- Generate German `name:` values (Wohnzimmer, Küche, Bad).
- Keep navigation hashes ASCII and English-style (`#wohnzimmer` is fine;
  `#küche` is not — no umlauts in hashes).

**MUST NOT:**
- Produce English labels for a German conversation.
- Put umlauts or spaces into hash paths.

**Tests:** the localisation rule (§2).

---

## #eval-9-accessibility

**Prompt:**
> My father is blind and uses a screen reader. Can you build him a Bubble Card
> dashboard to control the lights?

**MUST:**
- State honestly that Bubble Card's div-based controls are not screen-reader
  operable — no card option changes this.
- Offer the real alternatives: native tile cards, voice/Assist, automation.

**MUST NOT:**
- Build a Bubble dashboard as if it will work, with no caveat.
- Claim WCAG conformance because contrast was checked.
- Refuse to help at all — the alternatives are the help.

**Tests:** the accessibility-limits section (§2).

---

## #eval-10-unsupported-domain

**Prompt:**
> I have a valve entity (valve.garden_water). Make me a Bubble Card toggle
> for it.

**MUST:**
- State that `valve` is not one of Bubble Card's toggle domains.
- Offer either the native tile card or an explicit `tap_action: call-service`
  on `valve.open_valve` / `valve.close_valve`.

**MUST NOT:**
- Generate `button_type: switch` on a valve as if it will work — it renders
  but does not toggle. This is the silent-failure case the domain map exists
  to prevent.

**Tests:** `bubble-card-ref.md#entity-domain-map` domain support limits.

---

## #eval-11-platform-condition

**Prompt:**
> Ich möchte, dass die Terrassenbeleuchtungs-Karte nur angezeigt wird, wenn die
> Sonne untergegangen ist.

**MUST:**
- Use `visibility:` with a condition — never a `styles:` display hack.
- If a platform condition (`condition: sun.is_up` with `not`, or
  `sun.is_set`) is used, state that it needs Bubble Card v3.3.0+.
- Generate the labels in German (this prompt also exercises eval-8).

**MUST NOT:**
- Generate an automation to hide the card.
- Use a platform condition without any version caveat — on < 3.3.0 it
  degrades to a silent state check rather than erroring.

**Tests:** `bubble-card-ref.md` condition table, Signal Scan version gate.

---

## #eval-12-graph-request

**Prompt:**
> Ich hätte gern eine Übersichtsseite mit Graphen für Stromverbrauch,
> Temperatur in allen Räumen und Luftfeuchtigkeit — damit ich alles im Blick
> habe.

**MUST:**
- Note that graphs are deep-engagement content and do not belong on a
  glanceable Overview surface.
- Offer the **Advanced History** panel as an alternative to building a graph
  wall, or propose the Activity-view pattern (graphs behind a conditional).
- Name the HACS dependency of whichever graph card is proposed, and its
  native fallback.
- For the power sensor, mention `data_source: statistics` or statistics-based
  `group_by` (high-frequency sensor, database load).
- German labels.

**MUST NOT:**
- Generate a dozen graph cards on an Overview view without comment.
- Recommend SGCC without mentioning that it ships as a minified bundle when
  the user is being asked to take on a new dependency.

**Tests:** `graphs-ref.md#graph-decision`, `#graph-performance`,
`#advanced-history`, engagement-type model, dependency declaration.

---

## #eval-13-state-content

**Prompt:**
> Ich habe Bubble Card 3.4.0. Mach mir eine Button-Karte für
> climate.wohnzimmer, die den Zustand und die aktuelle Temperatur anzeigt.

**MUST:**
- Use `state_content` (the version is stated, and it is 3.4.0+).
- German labels (this also exercises eval-8).

**MUST NOT:**
- Use `show_state` / `show_attribute` / `attribute` for a stated 3.4.0 setup.
- Generate **both** `state_content` and the legacy keys — `state_content` wins
  outright and the leftovers are dead config.
- Spell out `state, current_temperature` without noting that those are also the
  climate domain's defaults, so an empty `state_content` would do the same.

**Tests:** `bubble-card-ref.md#state-content`, version-conditional generation.

---

## #eval-14-slider-inheritance

**Prompt:**
> Meine Lichtkarte hat einen Slider als Sub-Button. Der soll nur anzeigen,
> nicht bedienbar sein.

**MUST:**
- Put `read_only_slider: true` on the **sub-button**, not on the card.
- Say that slider options on a card do not reach a slider sub-button.

**MUST NOT:**
- Set `read_only_slider` at card level and present it as done — it silently
  has no effect there.
- Claim the option cascades from the card the way `scrolling_effect` does.

**Tests:** the per-option cascade rule in `#sub-buttons`.

---

## #eval-15-icon-override

**Prompt:**
> Mach mir eine Bubble-Card-Karte für lock.haustuer mit einem passenden Icon.

**MUST:**
- Leave `icon:` unset, or explain why it is being set.
- Note that HA already resolves a lock's icon by state (open vs locked), and
  that a hardcoded `icon:` overrides that plus any icon the user set on the
  entity in the UI.

**MUST NOT:**
- Emit a static `icon: mdi:lock` with no comment — it silently kills the
  state-dependent icon the user expects.

**Tests:** the icon resolution chain in `#ha-templates` / `#css-selectors`
area; "usually don't set it".

---

## #eval-16-mixed-groups

**Prompt:**
> In meiner Karte sollen nacheinander stehen: die Temperatur, dann eine Gruppe
> mit Licht und Ventilator, dann die Luftfeuchtigkeit.

**MUST:**
- Either put the two loose sub-buttons into their own explicit groups, or say
  plainly that loose buttons mixed with a group get collected and moved.
- Deliver YAML whose rendered order actually matches what was asked for.

**MUST NOT:**
- Emit loose / group / loose in that order as if YAML order were preserved.
  It renders as `[temperature, humidity]` then the group.

**Tests:** the mixed-group ordering rule in `#sub-buttons`.

---

## #eval-17-slider-range

**Prompt:**
> Bau mir einen Slider für number.pumpe_drehzahl. Die Entity geht von 0 bis
> 3000.

**MUST:**
- Leave `min_value` / `max_value` unset so the slider follows the entity.
- Explain that copying the current range into the card freezes it — the card
  keeps 0–3000 after the entity's range changes in HA.

**MUST NOT:**
- Write `min_value: 0` / `max_value: 3000` just because the user named them.
  The user supplied context, not a request to hardcode.

**Tests:** override-vs-description in the slider options.

---

## #eval-18-styling-target

**Prompt:**
> Ich will den Sub-Button "Küche" auf meiner Karte rot einfärben. Wie style ich
> den gezielt?

**MUST:**
- Recommend `css_class` on that sub-button and target that class.
- State that the auto-generated name class (`.kuche`) breaks on a rename and
  on a translated name, and is absent entirely for a templated name.
- Use a theme variable for the colour, not a hex literal (the Iron Law).

**MUST NOT:**
- Recommend `nth-child` — it breaks when a sub-button is added or hidden by a
  condition.
- Recommend the name-derived class as the primary target.

**Tests:** `#css-selectors` class stability table, Iron Law.

---

## #eval-19-select-attribute

**Prompt:**
> Mein Ventilator `fan.wohnzimmer` hat eine Geschwindigkeit von 0 bis 100 %.
> Ich möchte einen Sub-Button, über den ich die Stufe aus einem Dropdown
> auswählen kann. Bubble Card 3.4.2.

**MUST:**
- **Not** generate `select_attribute: percentage`.
- Say that `percentage` is a single number, not a list, and that
  `select_attribute` only accepts the fourteen specific list names.
- Offer the working alternative: a slider sub-button for the percentage, or
  `select_attribute: preset_modes` if the fan exposes named speeds.
- State that the broken form produces an **empty dropdown with no error** —
  this is what makes it worth saying out loud.

**MUST NOT:**
- Generate any `select_attribute` whose value is not one of the fourteen.
- Present `percentage` as working "if the fan supports it".

**Tests:** `#select-attribute`. The trap is that the user's own phrasing
("aus einem Dropdown auswählen", "0 bis 100 %") describes exactly the config
that silently fails, and the entity really does have a `percentage` attribute
— so every surface signal says yes.

---

## #eval-20-ha-style-popup

**Prompt:**
> Ich habe ein Raum-Pop-up mit `popup_style: home-assistant` und
> `popup_mode: centered`. Auf dem Handy ist es jetzt nach dem Update
> plötzlich bildschirmhoch, vorher war es nur so hoch wie der Inhalt. Was ist
> passiert?

**MUST:**
- Identify the v3.4.2 change: with `popup_style: home-assistant` the sheet now
  takes the full more-info height unless the mode is `adaptive-dialog`.
- Give the fix: `popup_mode: adaptive-dialog` (or `fit-content`).
- State that `popup_mode: centered` is **not read at all** with this style —
  so the mode in their config was never doing anything, which is why the
  default changed under them.

**MUST NOT:**
- Suggest `custom_height`, `margin_top_mobile`, a `styles:` height override or
  card_mod as the fix.
- Treat it as a bug to report.
- Claim `centered` controls anything here.

**Tests:** `#pop-up` mode table and the v3.4.2 row of `#version-compat`. The
trap is that the config *names* a mode, so the obvious reading is that the
mode stopped working — rather than that it never applied.

---

## #eval-21-sgcc-styling

**Prompt:**
> Kannst du mir die Statistics-Graph-Chart-Card an mein Dashboard anpassen?
> Rahmen in `#3A4B5C`, Überschrift in `#D9BE8B`, und etwas mehr Innenabstand.

**MUST:**
- Use theme variables, not the two hex literals the user supplied — the Iron
  Law applies to `card_border_color`, `card_header_color` and the v4.05
  `styles` block exactly as to any card YAML.
- Name where the two colours belong instead: the theme file.
- Use the dedicated `card_*` options for border and padding rather than a
  `styles` block, since options exist for both.
- Mention `axis_style: native` if the card sits beside native HA cards.

**MUST NOT:**
- Emit either hex value into the card YAML.
- Set both a `card_*` option and a `styles` rule for the same property.
- Suggest card-mod (SGCC's own `styles` block covers it without that
  dependency).

**Tests:** `#sgcc-dashboard-use`, Iron Law. The trap is that the user handed
over two hex codes and a styling request, and SGCC genuinely has options named
after exactly those properties — so the compliant-looking answer is the
non-compliant one.

---

## Scoring

| Result | Meaning |
|---|---|
| PASS | every MUST met, no MUST NOT triggered |
| PARTIAL | all MUSTs met but a MUST NOT triggered, or vice versa |
| FAIL | a MUST missed |

Record as: `v1.7 — 15 PASS / 2 PARTIAL / 1 FAIL (eval-6: pop-up left nested)`.

A PARTIAL is worth investigating even though it is not a regression: it
usually means guidance exists but is not reachable from the process tree.
