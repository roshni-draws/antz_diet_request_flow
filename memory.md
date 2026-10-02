# Diet module tablet prototype: working memory

Handoff notes for anyone (human or AI) picking this folder up. Read this first, then `prd.md` and `design-system.md`.

## What this is

A clickable, self-contained HTML prototype of the **Antz Diet module on a tablet** (iPad-sized, 810 x 1080 portrait and 1080 x 810 landscape). It covers:

- the Modules home with the Diet tile
- the Diet home with three tabs: Diet Directory, Diet by Species, Diet Request
- adding diets (base, year-round, seasonal, time-bound) through a wizard
- the diet change request flow with roles (Dietician, Head Dietician, Kitchen) and a request state machine
- Head Dietician configuration of requests into proposed diets

Everything runs in the browser with no server. Each HTML file inlines its CSS, JS, SVG icons and data. Only Google Fonts (Inter) loads from the network. State lives in memory and resets on reload.

## File map

Main flow:

| File | What it is |
|---|---|
| `diet-module-flow.html` | Screen 1. Modules home (bare, no bottom tab bar). The Diet tile opens `diet-home.html`. |
| `diet-home.html` | Screen 2. **The main prototype.** Tabbed Diet home with Directory, Diet by Species and Diet Request. Generated, never hand-edit. |

Legacy or superseded (kept for reference, not linked from the main flow except where noted):

| File | What it is |
|---|---|
| `diet-module.html` | Earlier self-contained Modules home screen with the Diet tile. Superseded by `diet-module-flow.html`. |
| `diet-button.html` | The Diet module tile on its own (icon plus label), for review of the tile and icon. |
| `diet-icon.svg` | The Diet tile icon as a standalone SVG. |
| `diet-tab-preview.html` | Tablet preview frame used early to check the tile in context. |
| `diet-tab-screen.html` | Earlier Antz Modules screen mock with the bottom tab bar. |
| `diet-directory.html` | Standalone Diet Directory. Superseded by `diet-home.html#directory`, rebuilt on the same module and data. **Must stay unchanged** (see below). |
| `diet-by-species.html` | Earlier standalone Diet by Species. Superseded by `diet-home.html#species`. |
| `diet-request.html` | Earlier standalone Diet Request list. Superseded by `diet-home.html#request`. |

Other:

| Path | What it is |
|---|---|
| `_build/` | The generator. Source of truth for every HTML file above that is generated. |
| `screens/` | Review screenshots (PNG), named `diet-home-<feature>-<state>-<portrait or landscape>.png`. About 24 MB. |
| `memory.md`, `prd.md`, `design-system.md` | These docs. |

## How to build

```
cd "_build"
python3 build.py
```

- Python 3 only, no packages to install.
- `build.py` writes into the folder above `_build/` (or into `$DIET_OUT` if set).
- It runs `pages.py` (the earlier standalone pages) and `home2.py` (the Diet home and the standalone directory). `home2.py` pulls in `req.py`, `sp3.py` (which pulls in `sample.py` and `wiz.py`), `roles.py` and `hdq.py`.
- Input data: `bsdata.json` (species and plans), `v2dir.json` (directory diets), `lookups.json` (masters: items, mixes, recipes, time bands, reasons, dietitians), `icons.json` (Antz icon set), `dataset.json` (early module data).
- **Never hand-edit `diet-home.html`.** Edit the `.py` files and rebuild.
- **`diet-directory.html` must not change.** It is 121870 characters (121949 bytes). The build prints its character count; if it changes, a shared CSS or icon change leaked into it. `home2.py` builds it from `_HEAD_DIR` and `HELPERS_JS_DIR` to keep it stable.
- The JS lives inside Python triple-quoted strings. In non-raw strings a backslash must be doubled (`\\d` in Python becomes `\d` in JS).
- There is no automated test suite in the folder. Playwright scripts used during development are not part of the repo.

## Module map inside `_build/`

| File | Contents |
|---|---|
| `build.py` | Tokens, base CSS, shell, status bar, app bar, `page()`, icon helpers. |
| `pages.py` | Earlier standalone pages. |
| `home2.py` | Diet home: tabs, router, Directory module, legacy request list, standalone directory. |
| `sp3.py` | Diet by Species: list, segments, species detail, header card, scope card, plans, plan card, Diet history sheet. |
| `sample.py` | SAMPLE DATA: extra holdings, sample plans, the six sample requests. |
| `wiz.py` | Add diet wizard, request side panel, apply dates, Prefill with AI (simulated), bands header. |
| `req.py` | Request diet change form, request badges, configuration choice sheet. |
| `roles.py` | Users and roles, request store, state machine, request detail screen. |
| `hdq.py` | Head Dietician request queue (To configure, Configured by me, All). |

## Data sources

- **Diet Directory:** V2 Tab prototype `diet/directory` data (32 diets), in `v2dir.json`.
- **Diet by Species:** Dev system local screens `diet/by-species` data (221 species, their plans, holdings), in `bsdata.json`.
- **Look and feel:** the Antz diet tablet prototype at antz-diet.pages.dev (tokens, type, cards, ribbons, tabs).
- **Request flow:** V2 Tab prototype request flow (`dr-core.js` statuses and transitions, `request.js` actions).
- **Masters:** `lookups.json` (24 items, 19 mixes and recipes, time bands, reasons, dietitians).
- **SAMPLE DATA** (`sample.py`, all marked in comments):
  - Coypu: 14 enclosures in 3 sections, 38 animals, plans 150 to 152, plus D-154 (seasonal on Coypu 9, used to show the overlap warning).
  - Common Buttonquail: Quail Yard section with 8 pens, plan 153.
  - Holdings for Southern Cassowary, Geoffroy's Marmoset and Golden-Headed Lion Tamarin.
  - Six requests, all raised by Hydar Ali (Dietician):

| ID | Species and target | Type | Priority | Start status |
|---|---|---|---|---|
| DR-00430 | Coypu, enclosure Coypu 9 | Temporary, 10 to 31 Oct 2026 | High | Requested |
| DR-00431 | Southern Cassowary, whole species (no diet) | Base diet | Medium | Requested |
| DR-00432 | Common Buttonquail, section Quail Yard | Seasonal, 1 Nov to 28 Feb | Low | Requested |
| DR-00433 | Coypu, whole species | Base diet change | Medium | Configuring |
| DR-00434 | Geoffroy's Marmoset, animal Tavi (AYO 13) | Animal-specific | High | Requested |
| DR-00435 | Golden-Headed Lion Tamarin, section Tamarin Island | Site / section | Low | Requested |

## URL routes and params

Query param:

- `?as=<role>` sets the Viewing as role: `dietician`, `head-dietician` (default), `kitchen-head`, `kitchen-operator`. Kept in the URL when the role is switched.

Hash routes in `diet-home.html`:

| Route | Opens |
|---|---|
| `#directory` | Diet Directory tab |
| `#directory/D-273` | Directory with diet D-273 open |
| `#species` or `#species/<seg>` | Diet by Species, segment `all`, `with` or `without` |
| `#species/<seg>/<tsn>` | Species detail |
| `#species/<seg>/<tsn>/<planId>` | Species detail with a plan selected |
| `#species/<seg>/<tsn>/new/<kind or base>/<step>` | Add diet wizard (`year-round`, `seasonal`, `time-bound`, `base`) |
| `#species/<seg>/<tsn>/request/new/<step>` | Request diet change form (`where`, `details`) |
| `#request` | Diet Request tab |
| `#request/<id>` | Request detail, for example `#request/DR-00430` |

Not in the URL: the Diet history sheet segment, sheet and menu open states, request tab segment and filters.

## Roles

| Role | User | Can |
|---|---|---|
| Dietician | Hydar Ali (u-dt) | Raise requests, edit own requests before acceptance, reply to clarification. Sees My requests only. |
| Head Dietician | Dr. Meera Iyer (u-dm) | Raise, review, accept, reject, ask for clarification, configure, send to Kitchen. Edits diets. Sees all requests. |
| Kitchen Head | Suresh Gowda | Kitchen review actions (delay, request adjustment, accept and send to prep), through a prototype grant. |
| Kitchen Operator | Anil Kumar | Same kitchen actions. |

Gating uses body attributes `data-write` and `data-raise` plus `RQ.can()` checks. Switch roles with the Viewing as button in the app bar.

## Decisions and user preferences

- **Keep it simple.** The user pushes back on extra features, extra steps and clever UI. Change only what was asked.
- No em dashes in visible text. Tap targets 44 px or more. Always check portrait and landscape.
- Never write to the kitchen folder (read-only source) or to Figma files.
- `diet-directory.html` must stay byte-stable.
- **All four configuration options are always allowed** (New base diet, Year-round, Seasonal, Time-bound). No disabled options; facts show as neutral info notes. An existing diet at the scope becomes "Edit D-x" and saves as a proposed change.
- **Accept goes straight to configuration.** No confirm sheet. Closing the sheet leaves the request in Configuring with Apply to configuration available.
- **Requests merged into Diet history.** The standalone Requests card on Species detail was removed. Diet history has Diets and Requests segments; the history button carries the open request count.
- **Only configurable sample requests.** The 11 original site requests and fake "configured by" history were removed.
- **Head Dietician request queue:** To configure, Configured by me, All, with a few contextual chips and a Filters sheet.
- **Bands header:** Prefill with AI plus one "Prefill from" menu; Add time band moved to the end of the bands list.
- **Prefill with AI is simulated** with in-page rules over the masters. No network calls.
- Proposed diets are never active. Phase 1 ends at Sent to prep.

## Deviations from the source

- V2 configure is a proposed-mode editor with no kind choice. Here the HD picks the kind in a sheet and the normal add diet wizard runs in request mode.
- V2 species page lists up to 3 requests in an "Active diet and requests" block. Here requests live in the Diet history sheet.
- Diet history, header card, scope card and target lists were redesigned for tablet (container queries, scalable target lists).
- Directory data comes from the V2 prototype while species data comes from the Dev system, so diet IDs between the tabs do not correspond.
- Base diets of many sample species share the same plan (shown as D-273), so their item amounts are generic.
- The Kitchen Head gets kitchen actions only through a prototype grant.

## Known issues and open items

- **Cassowary AI similar species:** Prefill with AI on DR-00431 starts from California Quail D-273 and scales to 28 animals, which gives large kg amounts because the sample base diet is generic.
- **Prefill alternatives with no quantity:** "Prefill from" a diet can copy alternatives without a quantity. Opening and saving that line then fails with "Enter a quantity greater than zero for each alternative." AI lines avoid this; the normal prefill does not.
- **History segment not in URL:** the Diet history Diets or Requests choice is not deep-linkable.
- **Landscape list does not scroll to the selection:** in Diet by Species landscape, opening a species by URL does not scroll the left list to the selected card.
- **Dietician and Kitchen chips:** their Diet Request views still use 5 status chips in a row; only the HD view was simplified.
- **First diet scope question:** a species with no diet always starts with a species-wide base diet. Whether a first diet may start at site, section or animal level is still open.

## Changelog

### 2026-10-01

- Diet tile and icon, tablet preview, Modules screens (`diet-module.html`, `diet-module-flow.html`).
- Diet home with three tabs; V2 directory module; standalone directory rebuilt on the same module.
- Diet by Species: segments, species detail from the Dev system, header card redesign, scope card with scalable target lists, plans and plan card.
- Add diet wizard: base diet with scope step, year-round, seasonal (day and month window), time-bound, overlap checks, prefill options.
- Request diet change form and request detail from V2; Viewing as roles and the full state machine.
- Head Dietician configuration: choice sheet, wizard in request mode with request side panel, proposed plans linked to requests, Change configuration.
- All four options allowed, edit as proposed change, overlap as warning in request mode.
- HD request queue: To configure, Configured by me, All, contextual chips, Filters and Sort sheets.
- Sample data reset to six configurable requests; Accept goes straight to configuration.
- `_build/` copy of the generator with README.
- Request side panel scrolls with pinned header and footer; Apply dates from request.
- Prefill with AI (simulated) with preview, reason tags and AI line tags.
- Feeding time bands header redesign with a Prefill from menu.
- Requests merged into Diet history; history button count badge.

### 2026-10-02

- Added `memory.md`, `prd.md` and `design-system.md`.
- Kitchen module (`kitchen-home.html`, `_build/kitchen.py`):
  - Kitchen tile on the Modules screen. Shared Viewing-as across pages (`antz.viewer`).
  - Dashboard:
    - 4 equal area cards; only Diet requests is clickable.
    - Needs attention line on top.
    - Receiving KPIs with deltas against the previous period.
    - Detail rows: Diet requests, Receiving, Returns, Vendor performance, Stock and expiry.
    - Overview | Follow-ups & receipts split (`#dashboard/overview`, `#dashboard/followups`).
    - SAMPLE DATA in `kitchen-sample.json` and `kitchen-stock.json`.
- Kitchen Head request review in `diet-home.html`:
  - Stock auto-resolution: main item, then HD alternatives in order; the first at 100% wins.
  - When nothing resolves: readjust round trip with a required reason. Bulk "Send all ready to prep".
  - 2 tabs: Overview and Diet & stock. Impact removed.
  - "Ready to Prepare" relabelled "Sent to prep" (internal key `ready` unchanged).
- Meal Group Management: all 7 tiles open full-screen pages at `#meal-groups/<slug>`.
  - Prep Sheet: request lines tagged "From DR-x" and "Alternative: X for Y".
  - Packaging list, Keeper Areas, Keeper Staff, Wastage setup, Piece Weights, Packing Stations: built faithfully from Dev system_local. Modules in `_build/mg_*.py`, seeds in `meal-groups.json`, edits in `antz.kitchen.mg`.
  - Piece Weights feeds the Prep Sheet's Pieces column. Keeper Staff feeds Keeper Areas, which feeds Packaging list and Wastage setup.
- HANDOFF.md rewritten for the Diet and Kitchen state.
