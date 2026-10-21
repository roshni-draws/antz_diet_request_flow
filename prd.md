# PRD: Antz Diet module, tablet flow (as built)

Status: prototype. This document describes what exists in `diet-home.html`, `diet-module-flow.html` and the Diet requests row of `kitchen-home.html` on **19 Oct 2026**, as generated from `_build/` at commit 79fef1f. The routing and multi-kitchen rules follow the locked decisions and v1 scope in `QA/routing-kitchen-scenarios.md`. It does not describe planned work. Anything in scope but not built is marked **Not built**.

## Changelog

- **19 Oct 2026:**
  - Roles: the Head Dietician (Diet Manager) role is removed. The roles are now Biologist (the only requester), Dieticians with scope assignments and an online or offline status, and one Kitchen Head per kitchen (K1, K2, K3).
  - Requests: the Biologist picks the dietician to send each request to. The dietician accepts, configures, certifies and sends to the kitchens.
  - Kitchens: the diet's items are split across kitchens from masters. A Kitchen Head can report a delay, and the whole diet starts on the latest ready date. Temporary and seasonal diets return to the base diet automatically. Late badges follow the SLAs.
  - Sample data: cut to 10 species (5 with a base diet, 5 without), with no seeded requests. The Directory shows only the 5 base diets.
  - Species detail: rebuilt as one section, with an inherited diet card at every level, one request entry per view and 48 px tap targets.
- **2 Oct 2026:** first as-built version: Dietician, Head Dietician and Kitchen review flow.

## 1. Problem and goals

Diet work in a zoo is split between the people who notice what an animal needs (biologists), the dieticians in charge of particular species and areas, and several kitchens that each supply part of a diet. Changes arrive by word of mouth, reach the wrong person, and start before every kitchen can supply its items.

Goals:

1. One place on a tablet to find any diet, by diet or by species, and to see the diet any site, section, enclosure or animal actually gets.
2. Let a biologist raise a structured diet change request against a precise target (species, site, section, enclosure or animal) and send it to a dietician in charge of that target.
3. Let that dietician turn the request into a proposed diet with the same tools used to build diets, certify it, and send it to the kitchens, without touching the active diet.
4. Split the diet across the kitchens that supply its items, let each kitchen report when it will be ready, and start the whole diet on one date.
5. Make status, next step and lateness obvious to every role.

## 2. Users and roles

| Role | Sample users | Needs |
|---|---|---|
| Biologist | Neha Kulkarni | Raise diet requests, pick the dietician, track own requests, answer questions. The only role that can request. |
| Dietician | Hydar Ali (online), Amruth Reddy (online), Priya Nair (**offline**), Kavya Rao (online) | Review requests sent to them; accept, reject or ask for information; configure, certify and send to kitchens. Edit diets of species they are in charge of. |
| Kitchen Head · K1 / K2 / K3 | Suresh Gowda (K1 Central Kitchen), Mohan Das (K2 RNR Kitchen), Lata Pillai (K3 Fruit Store) | See and act on their own kitchen's lines only: accept, mark processing, mark ready, report a delay. |
| Kitchen Operator | Anil Kumar | Kitchen module only (Prep Sheet, Meal Group Management). No Diet module. |
| Receiving Manager | Farhan Shaikh | Inventory and Kitchen. No Diet module. |
| Security, Security Admin | Ravi Naik, Priya Desai | Security module only. |

Dietician scope assignments (SAMPLE DATA, `_build/roles.py` `ROLE_DEFS`):

| Dietician | Status | In charge of |
|---|---|---|
| Hydar Ali | Online | Species: Coypu; Class: Aves |
| Amruth Reddy | Online | Section: Coypu Marsh; Species: Aldabra Giant Tortoise; Class: Reptilia |
| Priya Nair | Offline | Site: Cow Land; Species: European Polecat |
| Kavya Rao | Online | Species: Elephantnose Fish, Meerkat, Geoffroy's Marmoset |

Koi Fish has no dietician on purpose; it shows the "no eligible dietician" case.

Permissions (prototype):

| Capability | Biologist | Dietician | Kitchen Head | Kitchen Operator / Receiving Manager |
|---|---|---|---|---|
| Diet module | Yes | Yes | Yes | No |
| Raise, edit (until accepted) and reply on own requests | Yes | No | No | No |
| See requests | Own only | Only those sent to them | Only those with a line for their kitchen | All (Kitchen module) |
| Accept, reject, ask for information, configure, certify, send to kitchens | No | Yes, on requests sent to them | No | No |
| Create or edit diets (Create base diet, "+", New plan, Edit) | No | Yes, for species they are in charge of (class, species, or one of its sites, sections, enclosures or animals) | No | No |
| Accept, processing, ready, report delay on a kitchen line | No | No | Own kitchen's line only | No |

A "Viewing as" switcher in the app bar changes the role (demo only). The role list is shared by every page. Module access: Diet for Biologist, Dieticians and Kitchen Heads; Kitchen and Inventory for Kitchen Heads (plus Kitchen Operator and Receiving Manager as before); Security for the security roles.

## 3. Scope

In scope and built:

- Modules home with role-based tiles.
- Diet home with three tabs: Diet Directory, Diet by Species, Diet Request.
- Diet by Species: species list; species detail as one section (summary, scope, diet card); the inherited diet at every level; Diet history; creating and editing diets.
- Request flow: raise with dietician picker, edit, review, clarify, accept, reject, configure, certify and send, per-kitchen lines, delay, scheduled, live.
- Automatic return of temporary and seasonal diets to the base diet.
- SLA late badges.

### 3.1 Sample data (as built)

- **10 species** (`_build/sample.py`):
  - **With a base diet:** Coypu (D-273), Fischer's Lovebird (D-283), Aldabra Giant Tortoise (D-263), European Polecat (D-286), Elephantnose Fish (D-307). Each has exactly one species-wide, year-round base diet and nothing else. Every site, section, enclosure and animal inherits it, so the Animal-wide list shows "Species diet D-xxx" on every row.
  - **Without a base diet:** Southern Cassowary, Geoffroy's Marmoset, Meerkat, Green Iguana, Koi Fish. They have no diets at any level.
- **Animal rows:** each species has one animal row per animal held. Coypu has 38 animals in 14 enclosures, 3 sections and 1 site.
- **Requests:** no seeded requests. The Diet Request tab starts at 0. Request IDs start at DR-00001.
- **Diet Directory:** the 5 base diets only, built from the species data, with "Used by" lists that match the species tab. The standalone `diet-directory.html` is unchanged and still uses the older directory data.

## 4. User flows

### 4.1 Find a diet
Modules home → Diet tile → Diet Directory tab → search or filter → open a diet → Items or Nutrition → "Used by" links to the species.

### 4.2 Find the diet a target gets
Diet by Species tab → species → choose a scope (Species-wide, Site-wide, Section-wide, Enclosure-wide, Animal-wide).
- Each target row shows the diet it gets ("Species diet D-273", "Enclosure diet D-x" or "No diet").
- Tapping a target shows that diet in full, with "Base diet · Inherited from species".

### 4.3 Add or edit a diet (dietician in charge)
- **Add:** species detail → "+" or New plan → wizard. A species with no base diet gets its species-wide base diet first.
- **Edit:** opens the wizard prefilled. Saving makes a new version; the old version becomes inactive and stays in Diet history.

### 4.4 Raise a request (Biologist)
1. Species detail → choose scope and target → **Request new diet** (or Request diet change on a species plan, or Request a base diet when there is none).
2. Step 1, Where it applies: the target, then **Send to dietician**: pick one eligible dietician.
3. Step 2, Request: type, priority, dates, reason, notes.
4. Submit. Toast: "Request DR-0000x sent to <dietician>."

### 4.5 Review, configure and send (Dietician)
1. Diet Request tab (only requests sent to them) → open → Accept.
2. The "How should this request be configured?" sheet opens → choose an option → wizard prefilled from the request → Save proposed diet.
3. Back on the request: **Certify and send to kitchens**. The sheet previews the split, for example K1: Carrot, Beans, …; K2: Fish, Curd; K3: Apple, Bannana.

### 4.6 Kitchen lines (Kitchen Head)
- Diet Request tab (only requests with a line for their kitchen) → open → their own line → Accept → Mark processing → Mark ready.
- Or **Report delay** with a ready-from date and a reason, then Mark ready when the items arrive.

### 4.7 Start and end
- When every kitchen line is ready, the request is **Scheduled** with "Diet starts <latest ready date>".
- On that date it becomes **Live** and the proposed diet becomes active.
- A temporary diet shows "Ends <date>. Automatically returns to base diet D-xxx" and switches back after its end date.

## 5. Functional requirements

### Modules home (`diet-module-flow.html`)
- **DM-01** Show the Antz Modules home with one tile per module the viewing role can use (Diet, Kitchen, Inventory, Security).
- **DM-02** Tapping the Diet tile opens `diet-home.html` with the same role.

### Diet home shell
- **DM-03** App bar with back to Modules, title "Diet", Viewing as button and site picker ("All Sites").
- **DM-04** Three full-width tabs with counts: Diet Directory, Diet by Species, Diet Request (shows "My Requests" for the Biologist). The active tab has a green underline.
- **DM-05** Tabs and detail views are addressable by hash routes. Browser back works.
- **DM-06** The Viewing as sheet lists all 12 roles, each with a one-line description (for dieticians: online or offline and their scopes; for Kitchen Heads: their kitchen). The choice persists in `?as=` and across pages.

### Diet Directory tab
- **DM-07** List the 5 base diets (D-273, D-283, D-263, D-286, D-307).
- **DM-08** Search by Diet ID or species name.
- **DM-09** Filter by animal class chips and by verification; Filters sheet for site, certification and update state.
- **DM-10** Opening a diet shows:
  - status tags
  - one line, "Base diet · Year-round since … · Created by … · Certified by …"
  - Edit (dieticians in charge of that species only; it opens the species edit wizard)
  - Items or Nutrition
  - "Used by n species" with links to each species.
  Portrait opens a full-screen panel; landscape shows list and detail side by side.

### Diet by Species tab
- **DM-11** Segmented control: All, Species with diet, Species without diet, with counts (10, 5, 5).
- **DM-12** Search species or taxonomy ID; filter by class and verification; sort.
- **DM-13** Species cards show name, scientific name, class, animal count and active diet count (or "No diet yet").

### Species detail (one section)
- **DM-14** The species detail is one continuous section. Summary, scope and the diet are separated by space and headings, not separate cards. The species name appears once: in the panel header in portrait, at the top of the section in landscape.
- **DM-15** Summary: taxonomy ID and class tag, then stats (Animals, Sites, Active diets), then a Diet history button. The button shows a count of open requests visible to the viewer and opens the Requests list when there are any.
- **DM-16** Scope: Species-wide, Site-wide (hidden when the species is at one site with no site diets), Section-wide, Enclosure-wide and Animal-wide, each with counts.
  - Non-species scopes show a searchable, scrollable target list in pages.
  - Each row shows the diet that target gets: "Species diet D-273", "Section diet D-x", "Enclosure diet D-x" or "No diet".
  - Quick filters: Own diet / Inherited (enclosures), and Own diet / Species diet with Male / Female (animals).
- **DM-17** Diet card at species level: heading "Species-wide diets", one chip per plan (diet ID, kind tag, window), and "+" for dieticians in charge. The selected plan shows:
  - status tags
  - what it applies to ("Base diet. Every site, section, enclosure and animal of this species gets it.")
  - a meta line: when, created by, certified by
  - for temporary or seasonal plans, "After <date>, automatically returns to base diet D-xxx."
  - Items or Nutrition, then notes, remark and reason.
- **DM-18** Diet card actions sit in a row that stays in view while the Items table scrolls:
  - **Request diet change:** Biologist only.
  - **Edit:** dieticians in charge of this species only. Editing saves a new version and makes the old one inactive.
- **DM-19** A selected target with no plan of its own shows the **inherited diet card**:
  - "Diet for <target>"
  - diet ID and kind tag, and a tag such as "Base diet · Inherited from species"
  - the meta line, then Items or Nutrition
  - **Request new diet** (Biologist, primary) and **+ New plan** (dieticians in charge, secondary)
  - an open-request badge when one exists
- **DM-20** One request entry per view: the request button sits on the diet card or the empty state for the current level, never in the summary.
- **DM-21** Empty states:
  - **No base diet:** shows "No base diet yet" with Create base diet (dieticians in charge) and Request a base diet (Biologist).
  - **Target with nothing to inherit:** shows "No diet yet" with Request new diet.
- **DM-22** "Also used by n other species" is a collapsed list of links (only when the diet is shared).
- **DM-23** Tablet targets: every control on the species list, species detail and request form is at least 48 x 48 px, with at least 8 px between adjacent chips and buttons. There is no horizontal scroll at 810 or 1080.

### Diet history sheet
- **DM-24** Two segments: Diets (n) and Requests (n).
- **DM-25** Diets: history table (Diet, Scope, Reason, Validity, Status) with Scope and Kind chips. Proposed plans show a Proposed pill; a row from a request shows "From DR-x".
- **DM-26** Requests: the viewer's visible requests for this species.
  - For a dietician they are grouped To configure, Configured by me, Other; for the Biologist, Open then Closed.
  - A row opens the request detail.

### Add diet wizard
- **DM-27** Full-screen wizard with title, subtitle (species and scope), step bar, context strip and footer (Cancel, Back, Continue or Next, Create plan, Save proposed diet or Save changes).
- **DM-28** Steps: Who is it for (first base diet only), Date range or Season window (seasonal and time-bound), How to start (Configure new diet or Adopt an existing diet), Daily amounts (skipped at animal scope), Build diet, Why this change (skipped for the first base diet).
- **DM-29** Build diet: quantity mode, feeding time bands, item rows (day cadence, item, mix or recipe, daily amount, alternatives, prep, cut, notes), notes for the kitchen and site, remark, dietician. Prefill with AI (simulated) and "Prefill from" menu.
- **DM-30** Edit mode ("Edit D-x"): prefilled from the diet; saving creates a new version and deactivates the old one ("D-y saved. It replaces D-x, which is now inactive.").
- **DM-31** Validation: required dates, no past start for time-bound (except an unchanged start when editing), from before to, at least one item with quantity, a reason before saving. Outside requests, a second year-round diet at the same level and overlapping windows of the same kind are blocked.

### Request diet change form (Biologist)
- **DM-32** Step 1, **Where it applies**: species, then optional site, section, enclosure and individual animal (linked pickers), and the current diet the target gets (read only, including inherited diets).
- **DM-33** **Send to dietician** (required), below the target:
  - **Who is listed:** only eligible dieticians, meaning those whose scope matches the target's class, species, site, section, enclosure or animal.
  - **Each row shows:** name, the scope that makes them eligible (for example "Site: Cow Land"), and an online or offline dot plus label. Online dieticians are listed first.
  - **Offline dieticians:** selectable, but flagged "May reply later".
  - **No eligible dietician:** shows "No dietician is in charge of <target>. Ask an administrator to assign a dietician to this species or location. The request cannot be sent until then."
  - **Validation:** Continue and Submit are blocked until a dietician is picked.
- **DM-34** Step 2, **Request**: type (Temporary / Time-bound, Base diet change, Site / Section-specific, Animal-specific), priority (High, Medium, Low), start and end dates, reason, notes. A note names the picked dietician who reviews it next.
- **DM-35** Submit creates the request in Requested, assigned to the picked dietician. The requester can edit it, including the dietician, until it is accepted.

### Diet Request tab
- **DM-36** **Biologist:** "My requests" with chips All, Pending review, In progress, Scheduled / Live, Rejected.
- **DM-37** **Dietician:** only requests sent to them.
  - Segments: To configure, Configured by me, All.
  - Chips: Needs review, Configuring, Sent back; With kitchen, Delayed, Scheduled / Live; Open, Closed.
  - Sort and Filters sheet.
  - Cards show the next step (Review and accept, Configure, "Proposal saved: certify and send to kitchens").
- **DM-38** **Kitchen Head:** only requests with a line for their kitchen.
  - Segments: To do, Ready, All. Chips: To prepare, Delayed.
  - Cards show their kitchen's items, "Diet starts …" and the next step for their line.
- **DM-39** **SLA late badge** "Late · n days", shown on cards and kitchen lines:
  - **Dietician:** a request still Requested, Under review or Configuring more than 1 / 3 / 7 days after submission (High / Medium / Low).
  - **Kitchen:** a line still Waiting, Accepted or Processing more than 1 day after it was sent.
  - There is no escalation target (**Not built**, see section 11).
- **DM-40** Counts on tabs, segments, chips and badges update live.

### Request detail
- **DM-41** Header card with species, request ID, date, status chip, requester and View species.
- **DM-42** Notes shown above the rows:
  - **Start date:** "Diet starts <date>", with the reason when a kitchen is late (for example "Delayed by K3 · Fruit Store: Apple, Bannana. Need to procure item. Ready from 8 Nov 2026.").
  - **End date:** "Ends <date>. Automatically returns to base diet D-xxx after <date>." for temporary diets.
  - **Other notes:** Locked, Clarification and Rejected.
- **DM-43** Rows: Applies to, Current diet, Request, Diet type, Priority, Notes, Proposed diet, Requested by, **Sent to** (dietician and why they are eligible), Accepted by (and certified).
- **DM-44** **Kitchens** section: one line per kitchen with its items, a status tag (Waiting, Accepted, Processing, Ready, Delayed · ready from <date>), the delay reason, the late badge and who acted when. A Kitchen Head sees only their own line, headed "Your kitchen".
- **DM-45** Progress timeline, 6 steps:
  1. Request submitted
  2. Dietician reviewing
  3. Configured and certified
  4. Kitchens preparing (per-kitchen status)
  5. Scheduled (start date)
  6. Live

  Chat with messages and attachments.
- **DM-46** Footer: current status, time since the last change, the next step text and the role's actions (section 6).

### Configuration (Dietician)
- **DM-47** Accept moves the request to Configuring and opens "How should this request be configured?" immediately. Options: Edit the proposed diet (when one exists), New base diet (edits the base when there is one), Year-round, Seasonal, Time-bound. The option suggested by the request is preselected.
- **DM-48** Continue opens the wizard prefilled from the request (scope, dates, reason, notes), with the request side panel and "Apply dates from request".
- **DM-49** Saving creates a proposed, inactive diet linked to the request and returns to the request detail. Saving again replaces the proposal.
- **DM-50** **Certify and send to kitchens** stamps the dietician as the certifier, splits the proposed diet into one line per kitchen (section 7), and moves the request to With kitchens.

### Kitchen split and lines
- **DM-51** Item → kitchen mapping comes from masters (`_build/kitchens.json`). Dieticians do not pick kitchens. An item with no mapping goes to K1 and the line says "Kitchen not set in masters for <item>".
- **DM-52** Kitchen Head actions on their own line:
  - Waiting: Accept or Report delay.
  - Accepted: Mark processing or Report delay.
  - Processing: Mark ready or Report delay.
  - Delayed: Mark ready or Change delay.
- **DM-53** **Report delay** asks for a **Ready from** date (not in the past) and a **Reason** (for example "Need to procure item"). The line becomes "Delayed · ready from <date>", and everyone on the request sees the date and reason.
- **DM-54** No rerouting to another kitchen and no substitution in v1. Alternates stay in masters.
- **DM-55** Kitchen module (`kitchen-home.html`): the Diet requests row on the dashboard counts the Kitchen Head's own lines (To prepare, Delayed, Ready) and lists their open lines with the items and ready-from date.

### Start date, live and auto-return
- **DM-56** The effective start is the latest of the requested start date and every line's ready-from date. The whole diet, with every kitchen's items, starts on that date. There is no phased start.
- **DM-57** When every line is Ready, the request becomes Scheduled ("Starts <date>"). On the effective date it becomes Live ("Live since <date>"):
  - The proposed diet becomes active and verified.
  - A replacement base diet deactivates the diet it changes.
  - A temporary request makes the new diet time-bound from the start to the end date, on top of the base diet.
- **DM-58** Temporary (time-bound) diets switch off automatically once their end date has passed; the base diet applies again. Seasonal plans show "Each year after <date>, automatically returns to base diet D-xxx."

### Prefill with AI (simulated)
- **DM-59** Sheet "Recommend from request": read-only request summary, optional "Anything to add?", Generate with a loading state; a preview with a reason tag per line and a "Left out" list; Apply, Regenerate, Cancel. Applied lines carry an "AI" tag until edited.

## 6. State machines

### 6.1 Request

| Status | Who | Action | Next status |
|---|---|---|---|
| Requested | Assigned dietician | Opening the request | Under Dietician Review |
| Requested / Under Dietician Review | Assigned dietician | Accept request | Configuring (configuration sheet opens) |
| | Assigned dietician | Reject (reason required) | Rejected |
| | Assigned dietician | Ask for clarification (question required) | Under Dietician Review (question pending) |
| | Biologist (own request) | Reply to question; Edit request | same status |
| Configuring | Assigned dietician | Configure diet / Change configuration | Configuring (proposal saved or replaced) |
| | Assigned dietician | Certify and send to kitchens (needs a proposal) | With kitchens (one line per kitchen) |
| With kitchens | Kitchen Heads | Line actions (6.2) | With kitchens, until every line is Ready |
| With kitchens | System | Every line Ready | Scheduled (effective start = latest ready date) |
| Scheduled | System | Effective date reached | Live (proposed diet becomes active) |
| Live (temporary) | System | End date passed | Diet returns to the base diet automatically |
| Rejected, Cancelled | All | None | |

Labels: "With kitchens · 2 of 3 ready", "With kitchens · starts 8 Nov" (when a line is delayed past the requested start), "Starts 8 Nov", "Live since 12 Oct".

**Not built:** withdraw or cancel by the Biologist. The Cancelled status exists, but nothing moves a request there.

### 6.2 Kitchen line (one kitchen's items on one request)

| Status | Kitchen Head of that kitchen | Next status |
|---|---|---|
| Waiting | Accept | Accepted |
| Waiting / Accepted / Processing | Report delay (ready-from date, reason) | Delayed |
| Accepted | Mark processing | Processing |
| Processing | Mark ready | Ready |
| Delayed | Mark ready (the ready-from date is kept and still sets the start) | Ready |
| Delayed | Change delay | Delayed (new date or reason) |

No reroute, substitution or adjustment request from the kitchen in v1. The older single-kitchen statuses (Kitchen Review, Delayed, Needs Adjustment, Sent to prep) remain in the code for old-style requests, but no request uses them now.

## 7. Configuration and kitchen rules

| Option | Opens | Notes shown |
|---|---|---|
| New base diet | Wizard at species scope; edits the existing base if there is one, else creates it. | Base diets are species-wide. When the request targets a narrower scope, the context strip says "Request targeted …". |
| Year-round | At species scope: same as base. Elsewhere: wizard at the request's scope; edits the year-round diet there if one exists. | "A year-round diet already exists here. You'll propose changes to D-x." |
| Seasonal | Wizard with a day and month window, prefilled from the request. | Without a base: "No base diet yet. This proposal will also need a base diet before it can go live." |
| Time-bound | Wizard with Valid from and Valid to, prefilled from request dates. | Same no-base note. |

- **Edit as proposed change:** editing an existing diet in a request saves a proposed plan marked "Proposed change to D-x". D-x stays active until the change goes live.
- **Overlaps:** in request mode an overlapping seasonal or time-bound window warns and does not block. Outside requests it blocks.

Item → kitchen mapping (`_build/kitchens.json`, **placeholder**):

| Kitchen | Name | Source | Items |
|---|---|---|---|
| K1 | Central Kitchen | masters "central kitchen" | Carrot, Beans, Maize, Rice, Ragi, Sweet Potato, Spinach, Cucumber, Sunflower Seeds, Cooked Veg Mix, Morning Grain Mix |
| K2 | RNR Kitchen | masters "RNR Kitchen" | Fish, Chicken, Mutton, Egg, Curd, MilK, Mealworm |
| K3 | Fruit Store | **added; not in the kitchen replica** | Apple, Bannana, Papaya, Guava, Watermelon, Grapes, Pomegranate, Pipeapple, Orange, Lime, Lemon, Grapefruit |

The kitchen dev local copy has only the two kitchens and no item → kitchen field, so this mapping is ours until the real source is confirmed.

How each base diet splits:
- **D-273 Coypu:**
  - K1: Carrot, Beans, Maize, Cooked Veg Mix, Rice
  - K2: Fish, Curd
  - K3: Apple, Bannana
- **D-283 Fischer's Lovebird:** K1, K2, K3.
- **D-263 Aldabra Giant Tortoise:** K1, K2, K3.
- **D-286 European Polecat:** K1, K2.
- **D-307 Elephantnose Fish:** K1, K2.

## 8. Prefill options

- **Prefill from: Base diet** copies the species base diet's bands.
- **Prefill from: Current diet at this scope** copies the default diet at the selected scope; hidden when it is the base diet.
- **Prefill from: Another diet** opens a picker of species and their diets.
- **Adopt an existing diet** (How to start) shares another species' schedule instead of copying it.
- **Prefill with AI (simulated, no network):**
  - Starts from the current diet, else the base diet, else a similar species' base.
  - Scales quantities by animal count.
  - Applies request words ("soft", "no", "add", "more" and similar) to master items only.
- **Apply dates from request** re-applies the request's dates on the dates step.

## 9. Non-functional requirements

- **NFR-01** Tablet sizes: 810 x 1080 portrait and 1080 x 810 landscape. Landscape uses list and detail side by side (2:3); portrait uses full-screen panels.
- **NFR-02** Tap targets: 48 px or more on the species list, species detail and request form, with at least 8 px between adjacent controls. Other views keep 44 px or more.
- **NFR-03** No em dashes in visible text.
- **NFR-04** Self-contained HTML; only Google Fonts loads externally. No backend:
  - Requests, proposed diets and the viewing role are kept in the browser's localStorage and shared by diet-home and kitchen-home. "Reset demo data" clears them.
  - Diet edits made outside a request reset on reload.
- **NFR-05** Visible focus ring; reduced motion respected.
- **NFR-06** `diet-home.html` and `kitchen-home.html` are generated from `_build/`. `diet-directory.html` stays byte-stable. `diet-module-flow.html` and this PRD are hand-written.

## 10. Deferred / out of scope v1

- Rerouting a line to another kitchen, and any kitchen-to-kitchen transfer.
- Substitutes in the kitchen flow, substitute approval, and nutrient-tolerance checks (alternates stay in masters).
- Kitchen "request adjustment" in the new flow (the Kitchen Head can only report a delay).
- Requesters other than the Biologist: keeper, vet, curator, kitchen, dietician.
- Taxonomy-group and multi-animal requests; duplicate and conflicting request detection.
- **Not built:** Biologist withdraw or cancel (in v1 scope).
- Escalation targets for late requests; notifications outside the app (only in-app badges and toasts exist).
- Dietician leave, delegates and reassignment; forwarding a request to another dietician.
- Phased start, kitchen lead times, stock checks in the line flow, cost and nutrition impact.
- Persistence beyond the browser, authentication, real permissions.
- Site picker behaviour beyond "All Sites"; Photos (removed from the species summary).
- Dark mode.

## 11. Open decisions

1. **Item → kitchen mapping source:** K3 Fruit Store and the whole mapping in `_build/kitchens.json` are placeholders. Where do the real item → kitchen assignments live?
2. **Animal requests and the base diet:** should an animal-level request be allowed to configure "New base diet · Edit D-273", which changes the whole species, or only animal-level diets?
3. **Late requests:** with no supervisor role, who is notified when a dietician or kitchen is late? The badge alone, or a named person?
4. **Biologist withdraw:** in v1 scope but not built. Until which status may the Biologist withdraw, and what happens to kitchen lines already accepted?
5. **Day zero for the SLA:** does a pending clarification pause the SLA clock?
