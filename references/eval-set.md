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

## Scoring

| Result | Meaning |
|---|---|
| PASS | every MUST met, no MUST NOT triggered |
| PARTIAL | all MUSTs met but a MUST NOT triggered, or vice versa |
| FAIL | a MUST missed |

Record as: `v1.4 — 8 PASS / 1 PARTIAL / 1 FAIL (eval-6: pop-up left nested)`.

A PARTIAL is worth investigating even though it is not a regression: it
usually means guidance exists but is not reachable from the process tree.
