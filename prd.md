# PRD: Antz Diet module, tablet flow (as built)

Status: prototype, phase 1. This document describes what exists in `diet-home.html` and `diet-module-flow.html` on 2026-10-02. It does not describe planned work.

## 1. Problem and goals

Diet work in a zoo is split between the people who know what an animal needs (dieticians), the person who owns the diet plans (Head Dietician) and the kitchen that has to prepare it. Changes arrive by word of mouth, get lost, and land in the kitchen without a check on stock.

Goals:

1. One place on a tablet to find any diet, by diet or by species.
2. Let anyone with diet access raise a structured diet change request against a species and a precise target (species, site, section, enclosure or animal).
3. Let the Head Dietician turn a request into a proposed diet with the same tools used to build diets, without touching the active diet.
4. Give the kitchen a clear review step (delay, ask for adjustment, accept) before anything is prepared.
5. Make status and next step obvious to every role.

## 2. Users and roles

| Role | Sample user | Needs |
|---|---|---|
| Dietician | Hydar Ali | Raise and track own requests, answer questions. |
| Head Dietician (Diet Manager) | Dr. Meera Iyer | See what needs review and configuration, build diets, send to kitchen. |
| Kitchen Head | Suresh Gowda | Review proposed diets for stock and feasibility (prototype grant). |
| Kitchen Operator | Anil Kumar | Same kitchen review actions. |

Permissions (from the V2 model): Head Dietician has `diet-plans.write` (review, configure, edit diets, sees all requests). Kitchen roles have packing and inventory access (kitchen actions, see all requests). Dietician sees only own requests. A "Viewing as" switcher in the app bar changes the role (demo only).

## 3. Scope

In scope:

- Modules home with the Diet tile.
- Diet home with three tabs: Diet Directory, Diet by Species, Diet Request.
- Diet by Species: species list, species detail, scope, plans, plan card, Diet history, adding a base diet and other diets.
- Request flow: raise, edit, review, clarify, accept, reject, configure, send to kitchen, kitchen review.
- Head Dietician configuration of requests into proposed diets.

## 4. User flows

### 4.1 Find a diet
Modules home → Diet tile → Diet Directory tab → search or filter → open a diet → Items or Nutrition.

### 4.2 Find a species diet
Diet by Species tab → segment (All, Species with diet, Species without diet) → search or filter → species → choose scope (Species-wide, Section-wide, Enclosure-wide, Animal-wide) and target → choose plan → plan card.

### 4.3 Add a diet
Species detail → Plans "+" → wizard. With no base diet the species gets a species-wide base diet first. Steps vary by kind (see section 7).

### 4.4 Raise a request (Dietician or Head Dietician)
Species detail → Request diet change (header) or Request change (plan card) → Where (Applies to) → Details (type, priority, reason, notes, dates) → Submit → status Requested.

### 4.5 Configure a request (Head Dietician)
Diet Request tab, To configure → Review → Accept → "How should this request be configured?" sheet opens at once → choose option → wizard prefilled from the request → Save proposed diet → request detail → Send to Kitchen.

### 4.6 Kitchen review
Kitchen role → Diet Request tab → request in Kitchen Review → Delay, Request adjustment, or Accept / Send to Prep (Sent to prep). Request adjustment returns it to the Head Dietician as Sent back.

## 5. Functional requirements

### Modules home (`diet-module-flow.html`)
- **DM-01** Show the Antz Modules home with a Diet tile using the Diet icon.
- **DM-02** Tapping the Diet tile opens `diet-home.html`.

### Diet home shell
- **DM-03** App bar with back to Modules, title "Diet", Viewing as button and site picker ("All Sites").
- **DM-04** Three full-width tabs with counts: Diet Directory, Diet by Species, Diet Request. The active tab has a green underline.
- **DM-05** Tabs and detail views are addressable by hash routes (see `memory.md`). Browser back works.
- **DM-06** Viewing as sheet lists the four roles with a one-line description; the choice persists in `?as=`.

### Diet Directory tab
- **DM-07** List the 32 directory diets as cards or as a list (view toggle).
- **DM-08** Search by Diet ID or species name.
- **DM-09** Filter by animal class chips and by verification (All, Verified, Unverified); Filters sheet for site, certification and update state.
- **DM-10** Opening a diet shows its detail with Items and Nutrition views. Portrait opens a full-screen panel; landscape shows list and detail side by side.

### Diet by Species tab
- **DM-11** Segmented control: All, Species with diet, Species without diet, with counts (221, 84, 137 at build time).
- **DM-12** Search species or taxonomy ID; filter by class and verification; sort (Most diets and others).
- **DM-13** Species cards show name, scientific name, class, animal count and active diet count.

### Species detail
- **DM-14** Header card: avatar, name, scientific name, taxonomy ID, class tag, Request diet change button, open request badge, stats (Animals held, Sites, Diets), Photos and Diet history buttons.
- **DM-15** The Diet history button shows a count badge of open requests visible to the viewer. For the Head Dietician it is highlighted when something is waiting to configure.
- **DM-16** The header open request badge opens Diet history on the Requests segment.
- **DM-17** Scope card: Species-wide, Section-wide, Enclosure-wide, Animal-wide, each with diet and target counts. Non-species scopes show a searchable, scrollable target list with quick filters; long lists render in pages.
- **DM-18** Plans row: one chip per plan at the selected scope and target (kind tag, window, Proposed label and source request for proposed plans), plus "+" to add a diet.
- **DM-19** Plan card: diet ID, kind tag, verification, update pending, created by, validity window, scope tag, "From request DR-x" badge on proposed plans, open request badge and Request change link, certifying dietitian, Items or Nutrition table, notes, remark.
- **DM-20** Plan actions: Edit, Download PDF, and a menu with Replace Diet, History, Deactivate or Reactivate.
- **DM-21** A plan card's open request badge opens that request directly.
- **DM-22** If a species has no active plans, show a callout to create the base diet.

### Diet history sheet
- **DM-23** Two-option control at the top: Diets (n) and Requests (n), with an amber count on Requests for HD items waiting to configure.
- **DM-24** Diets: history table (Diet, Scope, Reason, Validity, Status) with Scope chips (All, Species, Site, Animal) and Kind chips (All kinds, Year-round, Seasonal, Time-bound). Proposed plans show a Proposed pill.
- **DM-25** A diet row that came from a request shows "From DR-x", which opens the request.
- **DM-26** Requests: rows with priority ribbon, ID and title, type, target and dates, requester and status tag. Open requests first: for the HD grouped To configure, Configured by me, Other; for other roles one Open group. Closed requests follow.
- **DM-27** HD request rows show the next step and the proposed diet (for example "Time-bound D-315 (Proposed)"). A row opens the request detail. "Open Diet Request tab" link at the bottom.

### Add diet wizard
- **DM-28** Full-screen wizard with title, subtitle (species and scope), step bar, context strip and footer (Cancel, Back, Continue or Next, Create plan or Save proposed diet).
- **DM-29** Steps: Who is it for (first base diet only), Date range or Season window (seasonal and time-bound), How to start (Configure new diet or Adopt an existing diet), Daily amounts (Standard, Tailored by Sex, Age or Weight band; skipped at animal scope), Build diet, Why this change (skipped for the first base diet).
- **DM-30** Build diet: quantity mode, feeding time bands with time band select, clone and remove, item rows (day cadence, item, mix or recipe, daily amount, alternatives, prep, cut, notes), add Ingredient, Mix or Recipe, band notes, notes for the kitchen and site, remark, dietician.
- **DM-31** Bands header: "Feeding time bands (n)" with Prefill with AI and a "Prefill from" menu (Base diet, Current diet at this scope, Another diet, each with a hint; items that do not apply are hidden). "+ Add time band" sits at the end of the bands list.
- **DM-32** Item sheet: kind (Item, Mix, Recipe), master item or mix, quantity, unit, prep, cut, alternatives, cadence (weekly days, every n days, monthly day), notes.
- **DM-33** Validation: required dates, no dates in the past for time-bound, from before to, season start and end not the same day, at least one item with quantity, alternatives need quantity, a reason before saving.
- **DM-34** Outside requests, a year-round diet cannot be added where one already exists; overlapping seasonal or time-bound plans of the same kind block Continue.

### Request diet change form
- **DM-35** Two steps: Where (Applies to: species, site, section, enclosure or animal, with linked pickers) and Details (Diet type: Temporary / Time-bound, Base diet change, Site / Section-specific, Animal-specific; priority High, Medium, Low; reason; notes; dates).
- **DM-36** Submit creates a request in Requested. The requester can edit it until it is accepted.

### Diet Request tab
- **DM-37** Head Dietician view: segmented control To configure (default), Configured by me, All, each with a count.
- **DM-38** Contextual chips: To configure: All, Needs review, Configuring, Sent back. Configured by me: All, With kitchen, Delayed, Sent to prep / Done. All: Open, Closed (Rejected and Cancelled).
- **DM-39** Sort control "Sort: Priority" with Priority (then oldest), Newest, Oldest. Filters sheet: status (multi), priority (multi), type, species, requester, with a live result count; active filters show as removable chips with Clear.
- **DM-40** To configure cards show a next step strip with a button: Review and accept (Review), Answer pending: waiting on requester (Open), Reply received: review and accept, Configure, Proposal saved: send to Kitchen (Send), Adjust and resend (Adjust, with the kitchen reason).
- **DM-41** Configured by me cards show the proposed diet and kind and the kitchen status (With Kitchen, Delayed to date, Sent to prep, Completed · Applied).
- **DM-42** Dietician and Kitchen views keep the earlier status chip list (My requests for the Dietician; Requires attention first for Kitchen).
- **DM-43** Counts on tabs, segments, chips and badges update live as actions happen.

### Request detail
- **DM-44** Header card with species, request ID, date, status chip, requester and View species. Rows for Applies to, Current diet, Request, Diet type, Priority, Notes, Proposed diet, Requested by. Progress timeline (8 steps). Chat with messages, file attachments and an updates toggle.
- **DM-45** Footer shows current status, time since last change, the next step text and the role's actions (section 6).

### Configuration (Head Dietician)
- **DM-46** Accept moves the request to Configuring and opens the configuration sheet immediately.
- **DM-47** Sheet "How should this request be configured?" lists New base diet, Year-round, Seasonal, Time-bound, all always selectable, with info notes. The option suggested by the request is preselected and tagged "Suggested from request". When a proposal exists, "Edit the proposed diet" is added first.
- **DM-48** Continue opens the wizard for that kind, prefilled from the request (scope, dates, reason as remark, notes) with the scope step skipped.
- **DM-49** Request side panel: landscape shows a sticky panel beside the wizard; portrait shows a collapsible bar. Header and "Open full request" are pinned; the body scrolls with edge fades.
- **DM-50** "Apply dates from request" on the dates step (button above the fields and an Apply link in the panel). Shows "Using request dates" when the fields match; hidden when the request has no dates.
- **DM-51** Save creates a proposed, inactive plan linked to the request and returns to the request detail. Saving again replaces the previous proposal.

### Prefill with AI (simulated)
- **DM-52** Sheet "Recommend from request": read-only request title, reason, notes, species, scope, kind and dates; optional "Anything to add?"; Generate with a 1.5 s loading state.
- **DM-53** Preview grouped by time band with item, quantity, unit, prep and days, a reason tag per line, a "Left out" list and the note "AI suggestions are a starting point. Review before saving." Buttons Apply, Regenerate, Cancel.
- **DM-54** Applied lines carry an "AI" tag until edited.

## 6. Request state machine

| Status | Role | Actions | Next status |
|---|---|---|---|
| Requested | Head Dietician | Opening the request | Under Dietician Review |
| Requested / Under Dietician Review | Head Dietician | Accept request | Configuring (configuration sheet opens) |
| | Head Dietician | Reject (reason required) | Rejected |
| | Head Dietician | Ask for clarification (question required) | Under Dietician Review (question pending) |
| | Requester (own request) | Reply to question | same status, answer recorded |
| | Requester (own request) | Edit request | same status |
| Configuring | Head Dietician | Apply to configuration (no proposal) or Change configuration | Configuring (proposal saved or replaced) |
| | Head Dietician | Send to Kitchen (needs a proposal) | Kitchen Review |
| Needs Adjustment | Head Dietician | Change configuration, Send to Kitchen again | Kitchen Review |
| Kitchen Review / Delayed | Kitchen | Delay (reason and expected date) | Delayed |
| | Kitchen | Request adjustment (reason) | Needs Adjustment |
| | Kitchen | Accept / Send to Prep (optional notes) | Sent to prep |
| Sent to prep | All | None (phase 1 ends here) | |
| Rejected, Cancelled, Completed · Applied | All | None | |

Notes: there is no Cancel action in the prototype. Completed · Applied is a defined status but nothing moves a request there in phase 1. The active diet never changes in phase 1.

## 7. Configuration rules

| Option | Opens | Notes shown |
|---|---|---|
| New base diet | Wizard at species scope. Edits the existing base if there is one, else creates it. | Base diets are species-wide. When the request targets a narrower scope, the context strip says "Request targeted ...". |
| Year-round | At species scope: same as base. Elsewhere: wizard at the request's scope; edits the existing year-round diet there if one exists. | "A year-round diet already exists here. You'll propose changes to D-x." |
| Seasonal | Wizard with day and month window, prefilled from the request season or dates. | Without a base: "No base diet yet. This proposal will also need a base diet before it can go live." |
| Time-bound | Wizard with Valid from and Valid to, prefilled from request dates (end defaults to start + 30 days). | Same no-base note. |

- **Suggestion:** a season gives Seasonal, Temporary gives Time-bound, Base diet change gives New base diet at species scope or Year-round elsewhere, anything else gives Year-round.
- **Edit as proposed change:** editing an existing diet opens it prefilled in edit mode, skips How to start and Daily amounts, and saves a proposed plan marked "Proposed change to D-x". D-x stays active until the change is applied.
- **Overlaps:** in request mode, a seasonal or time-bound window overlapping an existing plan of the same kind shows a warning ("Overlaps D-x from ... to ...; the proposal will replace it for those dates") and does not block. Outside requests it blocks.

## 8. Prefill options

- **Prefill from: Base diet** copies the species base diet's bands.
- **Prefill from: Current diet at this scope** copies the default diet at the selected scope. Hidden when it is the base diet.
- **Prefill from: Another diet** opens a picker of species and their diets.
- **Adopt an existing diet** (How to start) shares another species' schedule instead of copying it.
- **Prefill with AI (simulated, no network):**
  - Start from the current diet at this scope, else the base diet, else the base diet of a similar species of the same class.
  - Scale quantities by animal count and round to the master unit.
  - Request words "soft", "chopped", "minced", "mashed" set a soft prep the master offers and drop items only available whole.
  - "no", "avoid", "without" plus a master name exclude it and swap in a soft master item at the same quantity.
  - "add", "include", "extra", "more" plus a master name add it, or raise it by 25%.
  - Only master items, mixes and recipes are used.
- **Apply dates from request** re-applies the request's dates on the dates step.

## 9. Non-functional requirements

- **NFR-01** Tablet sizes: 810 x 1080 portrait and 1080 x 810 landscape. Landscape uses list and detail side by side; portrait uses full-screen panels.
- **NFR-02** Tap targets 44 px or more.
- **NFR-03** No em dashes in visible text.
- **NFR-04** Self-contained HTML; only Google Fonts loads externally. No backend; state resets on reload.
- **NFR-05** Visible focus ring; reduced motion respected for spinners and transitions.
- **NFR-06** `diet-home.html` is generated from `_build/`; `diet-directory.html` stays byte-stable.

## 10. Out of scope / not built

- Applying a proposed diet (activation), Preparing, Dispatched and Approved steps after Sent to prep.
- Cancelling a request.
- Real AI calls, stock checks, nutrition comparison of proposals.
- Persistence, authentication, real permissions, notifications.
- Site picker behaviour beyond "All Sites"; Photos content.
- Editing Diet Directory diets.
- Dark mode.

## 11. Open questions

1. May a species' first diet start at site, section or animal level, or must it always be a species-wide base diet?
2. What happens on Apply: does a proposed change replace the source diet or create a new version?
3. Should seasonal or time-bound proposals for a species with no base diet be allowed to reach the kitchen?
4. Should the Dietician and Kitchen request views get the same simplified segments as the Head Dietician?
5. Should the Diet history segment and filters be deep-linkable?
6. Who can cancel a request, and in which statuses?
