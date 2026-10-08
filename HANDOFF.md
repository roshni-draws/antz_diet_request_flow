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
  - Kitchen: Kitchen Head, Kitchen Operator, Receiving Manager.
  - Inventory (`inventory-home.html`, blank for now): Kitchen Head, Receiving Manager.
  - Security (`security-home.html`): what you see depends on the role.
    - **Security Admin:** Sites | Departments, both for configuration.
      - **Sites:** the same site transfers Security sees. A **Manage sites** button (`#sites/manage`) is where sites, codes and the site in-charge are added and edited.
      - **Departments:** go from a department to its buildings, then to a building's gates (for example Kitchen, then Antz Kitchen, then Gate 1, Gate 2 and Service Gate). You can add departments, buildings and gates, and edit a gate's name, purposes and whether it's active.
      - **Security tablet:** on a building you can choose "Show on security tablet" and tick "On tablet" for each gate.
      - **Building tabs:** each building has Configuration | Dashboard (`#departments/D1/B01`, `.../dashboard`).
        - **Configuration:** the gates, with **Configure tabs** for each gate (Vehicle entry and Vehicle exit only; no transfer tabs, because these departments are not animal related). By default the tabs follow what the gate is used for.
        - **Look:** the two building tabs use the same full-width tab bar as Sites | Departments. Inside a building there is no breadcrumb and no Sites | Departments bar. The header shows the building name, with the department and code below it, and the back arrow goes to the department.
        - **Dashboard:** gate chips (All gates, or one or more gates) and a calendar button in one bar. The filter applies to everything.
          - **Date and time:** the calendar button opens a sheet in the same chip style as the Diet filter sheet. Date: Today, Yesterday, This week, This month, or Custom (From and To). Time of day: All day, Morning, Afternoon, Evening, Night, or Custom (start and end). The button shows what's applied and turns dark teal when it isn't Today, all day.
          - **Summary panel:** Entries, Exits, Inside now, and Exit paperwork (a with / without challan split).
          - **Below:** By gate (entries, exits, without challan, inside) and Latest movements on the left, with Exits without challan (and their reasons) on the right. In portrait, exits without challan comes first.
          - **Vehicles panel** (was Latest movements): tabs All | Checked in | Checked out | Upcoming, with counts. Upcoming vehicles are tagged Due, or Late once their expected time has passed. Tapping a row opens a read-only detail drawer from the right. Checked in and out use the security detail (vehicles, challans, digitised lines, sealed DC, comments, See all timeline) without action buttons. Upcoming shows the expected vehicle, ETA and challan. Escape or the dark area closes it.
          - **Data:** the sample visits come from `_build/security_visits.py` (1 to 30 Sep, nothing after the mock 3:42 PM, plus 2 to 4 vehicles expected later on 30 Sep for each building).
    - **Security:** Sites | Gates.
      - **Sites:** recreated from the mobile screenshots in `secuirty/site transfer`.
        - **Layout:** site cards open a site page with 5 tabs (Animal, Egg, Egg Discard, Hospital and Carcass Transfer). Each has a pending filter. Landscape shows the list and detail side by side; portrait shows the list, then the detail.
        - **Actions:** Security Checkout and Check-in, and Confirm discard.
        - **Timeline:** in the detail footer, matching mobile IMG_0644. See all opens it above Current Status and Hide closes it. Newest is first, each row has its time, a ticked dot and a green card with the event and its value (for example "Animals loaded for transfer 3/3" or "Temperature checked 25°C"). Security actions are added as they happen. When it opens, the detail behind dims (tap the dark area or press Escape to close), the panel slides up, and the rows rise in one after another. The motion is off under reduced motion.
      - **Gates:** the building and gates the admin configured. Tapping a gate opens the gate screen (`_build/security_gate_ui.py`, `#gates/G01/<tab>`), built from the site page's parts.
        - **Layout:** a header band with the building and a gate switcher, then tabs All | Checked in | Checked out (from the admin's Vehicle entry and exit settings). There are no transfer tabs at gates. Below is a search for vendor, DC number or vehicle, with a scan button and a Sealed DC filter.
        - **Cards:** Checked-in (with Record Exit), Draft (tap to finish), and Checked-Out with Sealed DC Uploaded (sealed stamp) or Pending (tap to upload).
        - **Vehicle detail** (tap a card; `#gates/G01/<tab>/<visit id>`): laid out like the transfer detail. Landscape shows the list and detail side by side and opens the first vehicle; portrait shows the list, then the detail with an "All vehicles" link (the All | Checked in | Checked out tabs are hidden while a vehicle is open).
          - **Header:** status chip, vendor, vehicle number, gate, entry time and the driver with call and message.
          - **Sections:**
            - Vehicle entries: one entry can hold several vehicles. Each vehicle is a collapsible row (number and how many challans) holding its details, the challans on it, photos, Edit and Remove. Add vehicle sits in the header.
            - Challan details: collapsible rows showing number, items and "Split across N vehicles" or "On <vehicle>". Chips set which vehicles carry the challan (at least one). Each has photos and Delete. Add challan picks the vehicles.
            - Digitised challans: a dark header bar (Item | Qty, Condition, Expiry), with each line as a white card split in two: the matched item with "On DC 'x'" under it, then qty, condition and an expiry pill. Damaged lines are tinted pink, with a Returned tag and the returned quantity. Before processing the challan shows "Waiting to be digitised" and the footer reads "Inside, waiting for receiving".
            - QA cases (`GSC` / `gtScen` in `security_gate_ui.py`): each gate shows exactly 16 entries.
              - Checked in (8): not processed and processed, each as 1 vehicle 1 challan, 1 vehicle 2 challans, 2 vehicles 2 challans (one each) and 2 vehicles 1 challan (split).
              - Checked out (8): without and with the sealed DC, for the same four combinations.
              - Processed means the challans are digitised and show item lines. Not processed shows "Waiting to be digitised".
              - Three cases include a Damaged line marked "Returned, N returned".
              - Checked-in list cards are tagged "Processed" or "Not processed".
            - Sealed DC: take a photo, or show the stamp once uploaded.
            - Security details.
            - Comments (same as transfers, kept per vehicle).
          - **Look:** sections are split by hairlines. Photos are 64px tiles with one dashed Add tile, each challan has a "Challan 1" label with a delete icon, and the sealed DC box uses the neutral palette.
          - **Footer:** the same See all / Hide timeline as transfers (entry, challans checked, receiving, exit, sealed DC), current status, a progress bar, and Cancel / Mark exit (Check in for drafts, Upload sealed DC for pending exits). A sealed DC attached before the exit is saved as uploaded when the exit is marked.
        - **+ button:** sits over the list in landscape and is hidden while a vehicle is open in portrait.
        - **Log entry** (`#gates/G01/<tab>/new`, opened from + then Log Entry): a form in the detail column, built from the same parts as the entry detail.
          - **Vehicles:** collapsible rows. Each has vehicle number* and vendor*, driver and phone, entry gate (this gate, 3:42 PM) and exit gate ("Decide at the gate"), and a photo box that becomes thumbnails with remove buttons. Add vehicle and Remove vehicle are available.
          - **Challans:** collapsible rows with challan number*, and, when there are 2 or more vehicles, chips for which vehicles carry it. Each has photos. Add challan and Delete challan are available.
          - **Security:** security name (filled in from Viewing as) and a photo.
          - **Footer:** Cancel and Mark entry. Mark entry stays greyed until the required fields are filled; tapping it anyway marks the missing fields and rows in red and moves to the first gap. Saving creates a checked-in, not processed entry and opens its detail.
        - **Record exit** (`#gates/G01/<tab>/exit-<visit id>`): Record Exit on a card, Mark exit on the detail, or + then Log exit (pick the vehicle, then Continue) all open the same log form, already filled from the entry. That means vehicles with driver, phone and vendor, the challans, and the security name.
          - **Header:** "Recording exit".
          - **Gates:** the entry gate shows the time it entered, and the exit gate shows this gate at 3:42 PM, tinted.
          - **Sealed DC:** an extra section. Take a photo, or skip it and the exit saves with the sealed DC pending.
          - **Mark exit:** saves any edits, checks the entry out, and opens its detail.
        - **+ button:** Log Entry (opens the form above), Log Exit (pick the vehicle, sealed DC received or not) and Upload Sealed DC (pick the vehicle, attach a demo photo).
        - **Storage:** changes are kept in localStorage `antz.security.gate`, timed at the mock 3:42 PM.
    - **Storage:** the config is kept in localStorage `antz.security.cfg` and transfer changes in `antz.security.tx`.
    - **Build:** `_build/security.py`, which uses `security-data.json` (from the Tab prototype's `flow-data.js`), `security_tx.py` for the sample transfers, `security_tx_ui.py` and `security_cfg_ui.py`.
  - The Receiving Manager sees the Kitchen Dashboard and Meal Group Management read-only. The Diet requests links stay on the dashboard, because the role has no Diet access.
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

- No coloured edge strips (left or top accent bars) on rounded boxes. Show state with a tag or a count badge instead. The Security page follows this; some Diet and Kitchen notes still have edge strips.

- Keep changes small and do exactly what was asked. No extra features.
- Open results in Arc for review.
- Always check tablet portrait (810 x 1080) and landscape (1080 x 810).
- No em dashes; plain, short copy.
