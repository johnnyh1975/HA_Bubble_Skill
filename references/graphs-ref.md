# Graphs & History Reference
# ha-bubble-dashboard skill
# Covers: choosing a graph card, Statistics Graph Chart Card (SGCC) for
#         dashboard use, the Advanced History panel, theming and database load.
# Sources: SGCC README (v4.02-era) and Advanced History README v2.0.1.
#          SGCC ships as a minified bundle — see #sgcc-status.

---

## #graph-decision

### Which graph card — decide before generating

Graphs are Bucket 3 content (deep engagement). Before picking a card, apply
`dashboard-system.md#native-first`: a graph on the Overview view is almost
always the wrong answer, and the calmest dashboard has few or none.

| Need | Use |
|------|-----|
| A history graph, no styling requirement | Native `history-graph` — zero dependencies |
| Long-term statistics, no styling requirement | Native `statistics-graph` |
| A small, compact trend line inside a dashboard | `custom:mini-graph-card`, or SGCC in `sparkline: true` mode |
| Multiple entities, dual axes, comparisons, non-timeline chart types | `custom:statistics-graph-chart-card` (SGCC) |
| Ad-hoc exploration across areas/devices, no dashboard needed | **Advanced History panel** — `#advanced-history`. Often the right answer instead of building more cards. |

**Every one of the custom options is a HACS install the user must make.** Name
the dependency and the native fallback in the same breath — a missing custom
element renders as a red error box, and nothing in the YAML tells the user an
install step was implied.

### mini-graph-card or SGCC sparkline — they overlap

Both cover "a small trend line on a dashboard", so this is a dependency
decision, not a feature decision:

| | mini-graph-card | SGCC (`sparkline: true`) |
|---|---|---|
| Source | Open, auditable, forkable | **Minified bundle** (`#sgcc-status`) |
| Size | Small, does one thing | Large, does many things |
| Maintenance | Mature and slow — the maintainer has had an open call for help since 2021 and issue creation is restricted, though releases still land (HA 2026.6 card-suggestion support shipped) | Actively developed, frequent releases |
| Scope creep risk | None | The card can do far more than a sparkline needs |

**The rules that follow from this:**

1. **If the user already has one installed, use that one.** Neither is worth a
   second dependency for the same job.
2. **If SGCC is already going in** — for a richer graph elsewhere, or because
   they want the Advanced History panel — do **not** also add mini-graph-card.
   `sparkline: true` covers the compact case, and one dependency beats two.
3. **If a sparkline is the only graph need**, mini-graph-card is the
   proportionate choice: small, open, and auditable. Pulling in a large
   minified bundle for one trend line is not.
4. **Never make the whole graph capability rest on an unauditable component
   by default.** That is the strongest argument for keeping mini-graph-card in
   the picture even though SGCC can technically replace it.

**Do not reach for SGCC by default.** It is a large, feature-rich card; on a
dashboard that needs one trend line, `mini-graph-card` or a native card is the
proportionate choice. SGCC earns its place when the user needs what it uniquely
does: several entities on two axes, period comparison, or a non-timeline chart
type.

---

## #sgcc-status

### Statistics Graph Chart Card — what to know before recommending

- **HACS:** the README's install steps say to search HACS directly, but the
  repository still carries a *HACS: Custom* badge. Tell the user to search
  first, and to add
  `https://github.com/cataseven/Statistics-Graph-Chart-Card` as a custom
  repository (Category: Frontend) if it does not appear. Hard-refresh after.
- **Card type:** `custom:statistics-graph-chart-card`
- **Minimum HA:** 2024.1.0.

> **Source-first verification is not possible for this card.** SGCC is
> distributed as a **minified/protected bundle** — the readable source is not
> published, and the repository is not set up for external code review. Every
> other component in this skill was verified against its source; this one is
> documented from its README only. Treat option behaviour here as *upstream's
> claim*, not as verified fact, and say so if a user is deciding whether to
> depend on it. This is a maintenance-risk consideration, not an accusation:
> the card is actively maintained and widely used.

Practical consequences to raise when it matters:
- A minified bundle cannot be audited, patched locally, or forked if the
  maintainer stops. The degradation path is a rewrite to native cards, not a
  quick fix.
- Bug reports are the only channel; there is no PR route.
- Pin expectations accordingly for wall panels and other unattended displays,
  where a broken card is not noticed quickly.

---

## #sgcc-dashboard-use

### SGCC options that matter for dashboard generation

SGCC has a very large option surface (13 chart modes, hundreds of keys, a full
visual editor). Generating a maximal config is the wrong instinct — start
minimal and let the user refine in the editor, which is genuinely good.

**Minimal card:**

```yaml
type: custom:statistics-graph-chart-card
card_header: Living room
entities:
  - entity: sensor.temperature_living
    name: Temperature
```

**The handful of options worth setting deliberately:**

| Option | Why it matters here |
|--------|--------------------|
| `sparkline: true` | Strips all chrome — no header, axes, grid or toolbar. Timeline mode only. This is the calm-tech-compatible form: a trend shape without a data-analysis surface. Prefer it for anything outside the Activity view. |
| `height: auto` | Makes the card participate in **sections** grid sizing instead of a fixed pixel height, so it lines up with neighbouring cards and resizes from the Layout tab. Use this in sections views; a fixed number pins the graph regardless of the cell. |
| `hours_to_show` | Default 24. Keep the window as short as the question needs. |
| `group_by` | `interval` (default), `hour`, `Nh`, `date`, `week`, `month`, `year`, `raw`. `raw` draws every recorded sample at its exact timestamp — the right pick for step charts of binary or state sensors. |
| `data_source` | `auto` / `statistics` / `history`. See `#graph-performance` — this is the option that protects the database. |
| `chart_mode` | `timeline` (default) plus scatter, pie, ranking, radialbar, polararea, radar, heatmap, calendar, gauge, box, waterfall, histogram. Anything other than `timeline` is a deliberate analysis choice; do not pick one for decoration. |
| `card_shadow` / `card_border` | Set both `false` when the card sits inside a decorated background or a Bubble pop-up, so it does not double up on the theme's card chrome. |

**Iron Law applies unchanged.** Entity `color:` and `card_icon_color:` accept
any CSS value — so use `var(--accent-color)` and the theme's colour variables,
never a hex literal. SGCC reads `--primary-font-family` for canvas-rendered
charts, so typography follows the theme automatically. The period-highlight
band can be themed globally with `--sgc-period-highlight-color`.

---

## #graph-performance

### Keep graphs off the database's back

A dashboard full of graphs is the most common cause of a sluggish Home
Assistant. Two mechanisms matter:

- **`data_source`** — `auto` (default) reads raw history for short windows and
  long-term statistics for long ones. `statistics` always routes through the
  5-minute statistics buckets; upstream reports 287 rows / 33 ms versus
  21,995 rows / 1.7 s for the same 24-hour window of a high-frequency feed.
  `history` forces raw recorder history. For any high-frequency sensor
  (power, price feeds, network counters), set `statistics` explicitly rather
  than relying on auto-detection.
- **`group_by: date | week | month | year`** fetches native HA statistics
  periods, which also bypasses the recorder retention limit — a full year of
  data displays even with a 10-day purge. Statistics values come from
  5-minute buckets, so they are close but not tick-identical to raw history.

Also relevant: entities need `state_class` for long-term statistics to exist at
all. If a user asks why a long range is empty, that is the first thing to check
— and the fix is an ha-yaml handoff, not a card option.

`update_interval` sets auto-refresh in seconds (minimum 5). Leave it unset
unless there is a reason; `0` disables background polling entirely, which is a
reasonable choice on a wall panel.

---

## #advanced-history

### Advanced History — the exploration panel

**Advanced History** (integration, HACS default catalogue, v2.0.1 at time of
writing) adds a Home Assistant sidebar *panel* that keeps the familiar History
workflow but renders with SGCC. It can also optionally replace the native
history graph inside entity More Info dialogs.

**Dependency chain — install in this order:**
1. Statistics Graph Chart Card **v3.32+** via HACS (v4.02+ for multiple
   panels, which need independent Energy Date Sync collections).
2. Advanced History via HACS → Integrations, then restart HA.
3. Settings → Devices & services → Add integration → *Advanced History*.

If the card is missing, the panel shows an *Install using HACS* link rather
than failing silently.

**Why this belongs in a dashboard skill.** It is not a card, so it never
competes for space on a view — and that is exactly the point. The
engagement-type model says deep-engagement content should not sit on a
glanceable surface. Advanced History gives that content somewhere to live:

> When a user asks for "a view with graphs of everything so I can dig into it
> later", the honest answer is often that they want an exploration tool, not a
> dashboard view. Offer Advanced History alongside the Activity view rather
> than building twelve graph cards nobody looks at.

Capabilities worth knowing when making that offer: native target picker across
areas/devices/entities, multiple independent panels, dual Y axes, Energy-style
date navigation and period comparison, state timelines, per-target attribute
selection, saved bookmarks synced per user, undo/redo, and visual editing of
the current chart through the SGCC editor.

**Scope boundary.** Configuring the panel, its card defaults, and its bookmarks
happens in its own UI and YAML — this skill points users to it and explains
when it is the better answer, but does not generate its configuration.

---
