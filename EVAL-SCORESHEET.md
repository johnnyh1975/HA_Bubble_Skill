# Eval run — scoring sheet

Copy this file per run. One prompt per fresh conversation, in order.
Full prompts and criteria: `references/eval-set.md`.

- **Skill version:** v1.8
- **Bubble Card version assumed by the prompts:** 3.4.2
- **Run by:**
- **Date:**

## How to score

| Result | Meaning |
|---|---|
| PASS | every MUST met, no MUST NOT triggered |
| PARTIAL | all MUSTs met but a MUST NOT triggered, or the reverse |
| FAIL | a MUST missed |

A PARTIAL is worth investigating even though it is not a regression: it usually
means the guidance exists but is not reachable from the Signal Scan or the
process tree.

## Sheet

| # | Case | What it tests | Result | Notes |
|---|---|---|---|---|
| 1 | native-first | battery grid → Maintenance dashboard advisory | | |
| 2 | calendar-iron-law | `color: accent`, never a hex | | |
| 3 | cover-tilt | tilt options + v3.2.5 gate + feature detection | | |
| 4 | paid-module | decline, route, offer an original | | |
| 5 | mushroom-switch-colour | `mush-rgb-state-entity`, no `state-switch` | | |
| 6 | masonry-migration | new view, pop-up to top level, card_layout | | |
| 7 | automate-first | advisory, non-blocking, no automation generated | | |
| 8 | language | German labels, ASCII hashes | | |
| 9 | accessibility | honest limits + native/voice alternatives | | |
| 10 | unsupported-domain | valve: no toggle, native tile or call-service | | |
| 11 | platform-condition | `visibility:`, v3.3.0 gate, German | | |
| 12 | graph-request | engagement type, Advanced History, `data_source` | | |
| 13 | state-content | `state_content` for 3.4.0, never both forms | | |
| 14 | slider-inheritance | option on the sub-button, not the card | | |
| 15 | icon-override | leave `icon:` unset for a lock | | |
| 16 | mixed-groups | loose + group order is not preserved | | |
| 17 | slider-range | don't hardcode the entity's own range | | |
| 18 | styling-target | `css_class`, not the name class, not nth-child | | |
| 19 | select-attribute | not `percentage`; the 14-name list; empty dropdown is silent | | |
| 20 | ha-style-popup | v3.4.2 sheet height; `centered` was never read | | |
| 21 | sgcc-styling | theme variables in `card_*` and `styles`, not the given hex | | |

**Totals:** ___ PASS / ___ PARTIAL / ___ FAIL

## After the run

- A FAIL means the guidance is missing or unreachable. Check whether the rule
  exists at all; if it does, it is a routing problem — add a Signal Scan row or
  a process-tree branch rather than restating the rule.
- A PARTIAL on 13–21 is the expected shape of failure: those cases ask the
  model to contradict what the YAML looks like it should do. 19–21 go further —
  in each, the user's own wording describes the wrong answer (a 0–100 % fan and
  "aus einem Dropdown", a named `popup_mode` that was never read, two hex codes
  handed over for options named after exactly those properties).
- Record results in `CHANGELOG.md` under the current version, pass or fail.
  An unrecorded run is a run that gets repeated.
