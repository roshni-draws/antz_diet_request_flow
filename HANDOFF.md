# Handoff: Antz Diet and Kitchen tablet prototype

Updated 2026-10-02. For detail see `memory.md` (working memory, routes, changelog), `prd.md` (requirements, state machine) and `design-system.md` (tokens and components).

## 1. Current state

Two browser-only modules (no server), sharing roles and request state through localStorage:

- **Modules screen** `diet-module-flow.html` (hand-made) with the **Diet** and **Kitchen** tiles.
- **Diet module** `diet-home.html`. It has Diet Directory, Diet by Species, Diet Request with four roles, the add diet wizard, Head Dietician (HD) configuration into proposed diets, and the Kitchen Head review of requests (stock check, readjust, Send to prep).
- **Kitchen module** `kitchen-home.html`. The Kitchen Dashboard is split into Overview and Follow-ups & receipts. Meal Group Management has 7 tiles. Each tile opens a full-screen page: Prep Sheet, Packaging list, Keeper Areas, Keeper Staff, Wastage setup, Piece Weights and Packing Stations.

## 2. Start here

| URL | Shows |
|---|---|
| `kitchen-home.html?as=kitchen-head#dashboard/overview` | Needs attention, 4 area cards, receiving KPIs with deltas, detail rows, Stock and expiry |
| `kitchen-home.html?as=kitchen-head#dashboard/followups` | Waiting to be received, Receipts to review (Latest or Missing signed DC) |
| `kitchen-home.html#meal-groups` | The 7 tiles |
| `#meal-groups/<slug>` | `prep-sheet`, `packaging-list`, `keeper-areas`, `keeper-staff`, `wastage-setup`, `piece-weights`, `packing-stations` |
| `diet-home.html?as=kitchen-head#request` | Kitchen queue: To check, Sent to prep, All (`&kq=check`, `ready`, `all:kadjust`, `check:kreview`, `check:kdelayed`) |
| `diet-home.html?as=kitchen-head&tab=diet#request/DR-00427` | Kitchen request detail on the Diet & stock tab (`tab=overview` for Overview) |
| `diet-home.html?as=head-dietician#request` | HD queue: To configure, Configured by me, All |
| `diet-home.html?as=head-dietician#request/DR-00430` | HD request detail. DR-00430 to DR-00435 are the six configurable samples |
| `diet-home.html?as=dietician#request` | Dietician's My requests |

**Kitchen demo script** (Viewing as: Kitchen Head):

1. On the Dashboard, tap Diet requests and open each request. The stock check resolves by itself:
   - DR-00418 uses the main item.
   - DR-00420 uses Lime for Orange.
   - DR-00427 uses Lemon for Orange.
   - DR-00426 is unresolved: Send to Prep is blocked.
2. On DR-00426, use Request readjustment, which needs a reason.
   - Switch to Head Dietician and open To configure › Sent back.
   - Adjust and add Grapefruit as an alternative, then resend.
   - Back as Kitchen Head, it now shows "Will prep: Grapefruit". Use Send to Prep.
3. In the To check segment, tap "Send all ready to prep (n)" and confirm.
4. Open Meal Group Management › Prep Sheet. Request lines show "From DR-x" and "Alternative: Lime for Orange".
5. In Piece Weights, change Apple Whole from 180 g to 200 g. The Prep Sheet's Pieces for Apple change from 3,806 to 3,425.

## 3. How to change things

Edit `_build/`, then run `cd _build && python3 build.py`. That runs `pages.py`, then `home2.py` (which runs `req.py`, `sp3.py` with `sample.py` and `wiz.py`, `roles.py` and `hdq.py`), then `kitchen.py` (which runs the `mg_*.py` modules).

| File | Owns |
|---|---|
| `build.py` | Tokens, base CSS, shell, `page()` writer (asserts no em or en dash) |
| `home2.py` | Diet home tabs, router, Directory |
| `sp3.py` | Diet by Species, species detail, plans, Diet history; HOOKS (`planOf`, `currentOf`) |
| `wiz.py` | Add diet wizard, request side panel, AI prefill, bands header |
| `req.py` | Request form, badges, configuration choice sheet, detail header |
| `roles.py` | Users, request store and state machine (RQ, ACT), request detail, Kitchen stock check (KS), shared store (`STORE_JS`) |
| `hdq.py` | HD queue and the Kitchen queue (segments, quick Send to Prep, bulk send) |
| `sample.py` | SAMPLE DATA: 6 HD requests, 11 kitchen-stage requests, proposed plans D-401 to D-411, extra items (Orange, Lime, Lemon, Grapefruit) |
| `kitchen.py` | `kitchen-home.html`: dashboard, Prep Sheet, the meal-group page setup (routes, MGSTORE, bottom sheet, `mgPieceWeights()`) |
| `mg_packaging_list.py`, `mg_keeper_areas.py`, `mg_keeper_staff.py`, `mg_wastage_setup.py`, `mg_piece_weights.py`, `mg_packing_stations.py` | One page module each. Each sets `MGMOD` (css, js, icons) and registers `MGP[slug]`. Cross-page lookups go through `MGAPI` (`keepers`, `keeperAreas`/`areas`, `stations`, `staffAssignments`, `renameKeeper`) |
| `kitchen-sample.json` | SAMPLE receipts (22, 1 to 25 Sep 2026), pending challans, periods, kitchen stock used by the stock check |
| `kitchen-stock.json` | SAMPLE stock batches (Stock and expiry row, Needs attention), challan vehicles |
| `prep-sheet.json` | Prep Sheet source rows (Dev system) |
| `meal-groups.json` | Seed for the 6 meal-group pages, one key per slug (Dev system data) |
| `kitchen_full_backup.py` | Earlier keeper-area build, not run |

Guard rules:

- Never hand-edit generated HTML (`diet-home.html`, `kitchen-home.html`, `diet-directory.html` and the other built pages).
- `diet-module-flow.html` is hand-made: edit it directly.
- `diet-directory.html` must stay unchanged at 121870 characters (the build prints it).
- The `kitchen/` source folder and Figma files are read-only.
- No em or en dashes. Tap targets are 44 px or more. Check portrait and landscape.
- JS inside non-raw Python strings needs doubled backslashes. `KITCHEN_JS`, `HDQ_JS` and the `mg_*` JS are raw strings, so use single backslashes there.
- Test builds of one page: `KH_OUT=kh-test.html MG_ONLY=piece-weights python3 build.py` writes the kitchen page under another name. Delete it afterwards.

## 4. Shared demo state

| Key | Holds | Reset |
|---|---|---|
| `antz.viewer` | The Viewing-as role, shared by every page. `?as=` overrides it | Change role |
| `antz.diet.requests` | `{v, reqs, plans, gone}`: request changes and proposed plans | Ignored when `SEED_V` changes. `SEED_V` is an md5 of the request seed plus `kitchen-sample.json`, so editing either resets everyone. **Reset demo data** clears it |
| `antz.kitchen.mg` | Meal-group page edits, keyed by slug | Not version-checked. **Reset demo data does not clear it**; clear site data instead |

`kitchen-stock.json` and `meal-groups.json` are kept out of `SEED_V` on purpose, so editing them does not wipe request state.

## 5. Key decisions

- **Stock auto-resolution:** for each line, try the main item, then the HD's alternatives in order. The first that covers 100% is prepped. If none does, the line is unresolved: Send to Prep is blocked and the kitchen asks for a readjustment, with a required reason. There is no partial prep. Send to Prep saves the chosen items (`r.kitchen.accepted.lines`), and the Prep Sheet reads them.
- **Kitchen request detail** has 2 tabs: Overview (with chat and activity) and Diet & stock. The Impact tab and its "What changes" strip were removed.
- **"Sent to prep"** is the label everywhere; the internal status key stays `ready`.
- **Dashboard:**
  - 4 equal area cards; only Diet requests links out.
  - Needs attention sits on top, under the filters.
  - The receiving KPIs compare with the previous period of the same length.
  - Overview | Follow-ups & receipts split, with `#dashboard/<view>` and Back.
- **Meal-group pages** follow the Dev system_local kitchen pages faithfully (no extra features). Kitchen roles edit; diet roles see them read-only.
- **Role access** (`MODS` in `roles.py` `STORE_JS`, same table in `diet-module-flow.html`):
  - Diet: Dietician, Head Dietician, Kitchen Head.
  - Kitchen: Kitchen Head, Kitchen Operator.
  - The Modules screen has the Viewing-as pill and shows tiles by role.
  - Opening a module the role can't use shows "No access for <role>" (`guardModule`).
  - The Kitchen Operator gets Requests | Meal Group Management (`#requests`, read-only list of Sent to prep). There is no Dashboard, and Prep Sheet "From DR" links go to `#requests/<id>`.
- Accept goes straight to configuration. All four HD options are allowed; editing an existing diet becomes a proposed change.

## 6. How to verify

Use Playwright with local Chrome at **810 x 1080** and **1080 x 810**, and look at every shot (`screens/`). The scripts lived in the session scratchpad and may be gone. Worth recreating:

- **khauto:** the 4 stock outcomes above, readjust › HD resend with Grapefruit › Send to Prep, bulk send, dashboard counts.
- **kdash:** dashboard figures per period and warehouse, deltas, Needs attention links, Overview and Follow-ups routes, Back.
- **Meal-group CRUD:** one script per page. Open the tile, then create, edit, and delete or deactivate. Check the dietician is read-only, no target under 44 px, no sideways scroll, no page errors.
- **Prep Sheet link:** send a request to prep, check the From and Alternative tags, change a piece weight and check Pieces.
- **simple.js:** the six HD samples through configuration. `hdreq.js` is outdated: it expects the old Accept confirm sheet.

## 7. Open items (prioritised)

1. Reset demo data does not clear `antz.kitchen.mg`.
2. Dashboard: the top row's Receiving, Returns and Vendor numbers repeat the Receipts, Receipts with rejections and Suppliers cards. Decide whether the top cards should lead with other numbers.
3. Prep Sheet "Today" uses the real date, but the mock status bar says Wed 30 Sep and the dashboard data is 25 Sep.
4. Packing stations don't say which enclosures each station packs, so the packaging list can't show "Packed at".
5. AI prefill for Cassowary starts from California Quail D-273, which gives very large kg amounts.
6. "Prefill from" a diet can copy alternatives with no quantity; saving that line then fails validation.
7. First-diet scope: may a species' first diet start at site, section or animal level, or must it be a species-wide base?
8. `hdreq.js` and `hdcfg.js` are outdated.
9. Other decisions needed:
   - Should the Dietician view get the simplified segments the HD view has?
   - What should Apply do with a proposed change to an existing diet?
   - Packaging list repeats the 25 Sep figures for every date.

## 8. Not yet pushed

Target: GitHub `roshni-draws/ANTS_diet_tab`. Nothing is committed or pushed.

- [ ] Real-looking staff names in `_build/bsdata.json`, `lookups.json`, `meal-groups.json` and the generated HTML (for example Hydar Ali, Nidhin Pratap, keeper and supervisor names).
- [ ] Permission to publish internal prototype data (`v2dir.json`, `bsdata.json`, `dataset.json`, `meal-groups.json`).
- [ ] `screens/` is 24 MB or more of PNGs: keep it, move it to Git LFS, or leave it out.
- [ ] Remove the local `/Users/...` fallback output path in `_build/build.py`.
- [ ] Delete stray test outputs (`kh-*.html`) if any are left.

## 9. User preferences

- Keep changes small and do exactly what was asked. No extra features.
- Open results in Arc for review.
- Always check tablet portrait (810 x 1080) and landscape (1080 x 810).
- No em dashes; plain, short copy.
