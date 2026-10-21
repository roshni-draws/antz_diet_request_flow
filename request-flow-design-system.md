# Design system: Diet request flow (tablet)

This covers the flow from species detail, to a request, to the dietician, to kitchen lines, to the diet's start date. Global tokens and base components come from [design-system.md](design-system.md), which this file does not repeat. This file adds what the request flow uses, overrides or introduces.

Every value is taken from the generator CSS and markup in `_build/` (commit 79fef1f plus the 19 Oct 2026 work). File references are `file:line` in `_build/`. Anything not confirmed in code is marked **TBD**. Light theme only.

## 1. Overview

**Scope:**
- Diet by Species → species detail (one section) → scope and target → inherited diet card.
- Request form (Biologist) → "Send to dietician" picker.
- Dietician queue → request detail → configure → certify and send.
- Kitchen lines (K1, K2, K3) → delay → "Diet starts <date>" → Scheduled → Live → automatic return to the base diet.

**Targets:** tablet, touch first. 810 x 1080 portrait and 1080 x 810 landscape.

**Principles:**

| Principle | What it means in the flow |
|---|---|
| One section per detail, no cards in cards | The species detail is one white surface (`.spsheet`); summary, scope and diet are separated by 32 px and headings, never boxed again. |
| One request entry per view | The request button sits on the diet card or the empty state for the current level, never in the summary. Primary is filled teal; secondary is outlined. |
| No coloured edge strips on rounded cards | State is shown with tags, badges and tinted backgrounds. Request notes (`.rnote`) had inset 4 px strips; they were replaced with tints. |
| Spacing over dividers | The summary row, the stat dividers and the plan header line were removed; gaps carry the grouping. |
| Touch targets | At least 48 x 48 px on the species list, species detail and request form, with at least 8 px between adjacent targets. |

## 2. Foundations used by the flow

### 2.1 Colour

Global values are defined in `build.py:80-118`. Contrast ratios below were measured on the rendered pair; tinted backgrounds were composited over white.

| Token | Hex | Role in the flow | Contrast |
|---|---|---|---|
| `--head` | `#000000` | Titles, item names, names in rows | |
| `--ink` (`--md3-on-surface-variant`) | `#44544A` | Body text, meta lines, secondary labels. **Replaces `--md3-neutral-secondary` for text on the species views.** | 8.04 on white, 7.28 on `#EFF5F2` |
| `--md3-neutral-secondary` | `#7A8684` | Still used for small captions in older parts (`.tgh`, `.pchip .l2`, `.tl small`, `.curdiet small`) | **3.77 on white, 3.41 on `#EFF5F2` (fails 4.5:1)** |
| `--white` | `#FFFFFF` | The section surface, sticky action row background, sheets | |
| `--md3-background` | `#EFF5F2` | Page background, target rows, current diet box, kitchen preview rows | |
| `--md3-on-primary-container` | `#1F515B` | **Primary teal.** Primary buttons (`.btn.teal`), selected chips, selected picker row border, focus ring, toasts | White on teal 8.80 |
| `--md3-primary` | `#37BD69` | Global green: `.btn.pri`, selected plan chip and target row border, done timeline step, online dot | White on green **2.43 (fails)** |
| `--md3-on-surface` | `#006D35` | Green text: Year-round tags, "Online" label, target diet label | 5.86 on `#E1F9ED`, 6.48 on white |
| `--md3-displaybg-primary` | `#E8F4F2` | Teal tint: teal tags, selected picker row | Teal text on it 7.82 |
| `--md3-outline-variant` | `#C3CEC7` | Borders of outlined buttons, plan chips, picker rows, kitchen lines | 1.62 on white (boundary only; text and icons inside carry the meaning) |
| `--md3-error` | `#E93353` | Errors, red tags (including Late), danger button | 3.87 on `--error-a5` |
| `#FFF6DB` (literal) | | Warning tint: `.rnote.warn`, `.dpempty`, `.hist.due` | Text 19.46, icon `#8A5A00` 5.49 |
| `--moderate-a10` | `rgba(228,184,25,.10)` | Open request badge (`.rqb`, text `#6B5200`), "review" queue footer | 6.97 |

**Override: teal primary instead of global green.** On the species views and in the request flow, primary actions use `.btn.teal` (`roles.py:170`), for example Request new diet, Request diet change, Create base diet, Certify and send, Accept and Mark ready. The reason is contrast: white on `--md3-primary` is 2.43:1, while white on teal is 8.80:1. `.btn.pri` (green) is still used in the wizard and request form footers (see section 9).

### 2.2 Type

The scale is defined in `build.py:142-151`. Inter, `line-height: normal`.

| Class | Size / weight | Used for |
|---|---|---|
| `.t-stat-title` | 28 / 600 | Summary stats (38, 1, 1) |
| `.t-major-title` | 24 / 600 | Species name (landscape), sheet titles |
| `.t-medium-medium` | 20 / 500 | Form card titles ("Send to dietician"), diet ID on the inherited card |
| `.t-minor-title` | 16 / 600 | Section headings ("Species-wide diets", "Diet for Thistle", "Kitchens") |
| `.t-minor-italic` | 16 / 400 italic | Scientific name |
| `.t-body-title` | 14 / 600 | Names in rows, kitchen name, dietician name |
| `.t-body-medium` | 14 / 500 | Buttons in chips, "Online" / "Offline", applies text |
| `.t-body-regular` | 14 / 400 | Meta lines, items, reasons |

**13 px minimum for small labels on the species views:**
- Tags: `#spanel .tag, .sp-detail .tag { font-size: 13px; height: 26px }` (`sp3.py:144`). The global `.tag` is 12 px / 24 px (`home2.py:88`).
- Scope sub-labels: `.scopes .spchip small` 13 px (`sp3.py:76`).
- Also 13 px: open request badge `.rqb` (`req.py:7`), form errors `.ferr` (`req.py:18`), status chip `.stchip` (`req.py:53`).
- Still at 12 px: `.tgh` group headers (`sp3.py:97`), `.pchip .l2` (`sp3.py:110`), table headers `.dtab th` (`home2.py:121`), the Diet history count `.hcount` (`sp3.py:36`).

### 2.3 Spacing

The scale is `--sp-4, 8, 12, 16, 20, 24, 32` (`build.py:118`).

| Gap | Where |
|---|---|
| 32 | Between groups in the section (`.spsheet` gap, `sp3.py:163`); between stats (`.hero__stats`, `sp3.py:57`) |
| 24 | Section side and bottom padding (`.spsheet` padding 20 / 24 / 24) |
| 16 | Inside the plan card (`.dpane` gap, `home2.py:97`); summary row gap |
| 12 | Between buttons in an action row (`.dp-btns`, `.cobtns`); between kitchen lines' groups (`.klist`) |
| 8 | Between chips, target rows (`.targets`), picker rows (`.dpick`), kitchen lines (`.klist ul`) |

### 2.4 Radius and elevation

- **Radius:** `--radius: 8px` for the section, picker rows, kitchen lines, notes and buttons. Tags 4 px. Pills (`.chip`, `.rqb`, `.asbtn`) 999 px. Bottom sheets 16 px top corners (`home2.py:187`).
- **Elevation:**
  - The section and cards are flat (no shadow).
  - Queue cards use `--card-shadow: 0 2px 8px rgba(0,0,0,.08)` (`pages.py:324`).
  - Selected states use a 1 px ring, not elevation: `box-shadow: 0 0 0 1px` (`.pchip`, `.dp`, `.prio`).
  - The selected target row uses an inset 2 px ring.

### 2.5 Motion

- **Press:**
  - `.btn:active` `scale(.98)` (`home2.py:198`); `.chip:active` `.97` (`build.py:241`); `.iconbtn:active` `.94` (`build.py:186`); `.spfilter:active` `.96` (`build.py:223`).
  - The summary's old request button pressed to `.96`; that button was removed with the one-request-per-view change.
  - **TBD:** one press scale across buttons (`.96` is the target used in the cleanup review).
- **Transitions:**
  - Fades on the target list: 160 ms opacity (`sp3.py:86`).
  - Switch: 200 ms.
  - Toast: 200 ms opacity and translate (`home2.py:199`).
  - "Also used by" chevron rotation: 150 ms, only under `prefers-reduced-motion: no-preference`.
- **Reduced motion:** `RM_CSS` (`build.py:262-268`) removes every transition and the press scale on `.iconbtn`, `.chip` and `.spfilter`.

## 3. Components

Component count: **18**.

### 3.1 Single-section sheet (`.spsheet`)
- **Purpose:** hold the whole species detail as one surface.
- **Anatomy:** summary, then scope, then the diet card or empty state, then "Also used by" (when the diet is shared).
- **Tokens:** `--white`, `--radius`, padding `--sp-20 --sp-24 --sp-24`, gap `--sp-32`.
- **Code:** `sp3.py:163-165`; the wrapper is added in `drawDetail` (`sp3.py:549`). Children (`.hero`, `.card2`, `.dpane`, `.callout`) lose their own background, radius, padding and margin inside it.
- **Do:** separate groups with space and a heading. **Don't:** add borders or another white box inside.

### 3.2 Summary row, stats and Diet history
- **Anatomy:**
  - Landscape only: species name (h2) and scientific name.
  - Taxonomy ID, class tag, Certified tag.
  - Stats: Animals, Site(s), Active diet(s).
  - **Diet history** button.
- **States:**
  - The Diet history button shows a count (`.hcount`) of open requests.
  - `.due` (amber tint `#FFF6DB`, border `#E2B33C`) when something waits on the viewer.
  - It opens the Requests list when there are open requests, otherwise Diets.
- **Sizes:** the button is 48 px tall (`sp3.py:63`). Stats have a minimum width of 72 px and a 32 px gap.
- **Code:** `hero()` `sp3.py:326`; CSS `sp3.py:36-70`. The button uses class `hist` so it doesn't pick up the request page's `.hbtn`.
- **Copy:** "Animals", "Site" / "Sites", "Active diet" / "Active diets", "Diet history".
- **Don't:** put a request button here (one request entry per view).

### 3.3 Scope chips, target rows and filter chips
- **Scope chips:**
  - Species-wide, Site-wide (hidden for one site with no site diets), Section-wide, Enclosure-wide, Animal-wide.
  - Two lines: label plus a 13 px sub-label ("0 diets · 3 sections", "All on species diet", "n with own diet", "No diet yet").
  - Minimum height 52 px. Selected: teal fill, white text.
  - Code: `scopeCard()` `sp3.py:394`; `.scopes` `sp3.py:74-76`.
- **Target list:**
  - Search field (48 px), quick filter chips (48 px, `sp3.py:82`), a count ("38 animals"), group headers (`.tgh`, sticky), and rows.
  - Scroll area: maximum height 360 px (296 px in landscape), with top and bottom fade cues.
  - Code: `targetsShell()` `sp3.py:369`, `drawTargets()` `:378`.
- **Target row (`.tgt`):**
  - Name (plus `#id` for named animals), sub-line (sex · enclosure, or "n animals"), and an optional "n open request" badge.
  - On the right, the diet the target gets: "Species diet D-273" (`--md3-on-surface`), "Enclosure diet D-x", or "No diet" (`--ink`, 400).
  - Minimum height 52 px; selected: white background plus an inset 2 px green ring.
- **Filter chips:**
  - Enclosures: All / Own diet / Inherited.
  - Animals: All / Own diet / Species diet, a divider, then Male / Female.

### 3.4 Plan card and inherited diet card
- **Plan card** (species level, or a target with its own plans), `planCard()` `sp3.py:473`:
  - Heading "Species-wide diets" or "Diets for <target>", and "Show inactive (n)" switch.
  - Plan chips (`.pchip`, 48 px; selected: green ring) plus "+" (`.addchip` 48 x 48, dashed).
  - **Action row** (`.dp-head`, sticky): tags (status, Own diet), applies text, meta line, return note, and buttons.
  - Items | Nutrition, then notes, remark and reason.
- **Inherited diet card** (a target without its own plan), `inheritedCard()` `sp3.py:497`:
  - "Diet for <target>".
  - Diet ID (20 / 500) plus kind tag, and the tag "Base diet · Inherited from species" (or "Inherited from section <name>").
  - Meta line; **Request new diet** (teal) and **+ New plan** (outlined); open request badge; Items | Nutrition.
- **Sticky action row:** `position: sticky; top: 0; background: var(--white)` (`sp3.py:136`), so the actions stay in reach while the table scrolls.
- **Button group:** `.dp-btns` with a 12 px gap, right aligned, at most 50% of the row width (`sp3.py:137`).
- **Copy patterns:**
  - Applies: "Base diet. Every site, section, enclosure and animal of this species gets it." / "Replaces D-273 for Coypu 1." / "Runs on top of the year-round diet for these dates."
  - Meta: "Year-round since 22 Sep 2026 · Created by Narendra M · Certified by Amruth reddy" (or "Not certified").
  - Return note: "After 30 Nov 2026, automatically returns to base diet D-273." / "Each year after 15 Nov, automatically returns to base diet D-x."
- **Don't:** repeat the diet ID or kind in both the chip and the header. The chip carries the kind.

### 3.5 Items | Nutrition tabs and table
- **Tabs (`.dseg`):** two buttons with `aria-pressed`. Selected: teal fill. On the species views the buttons are 48 px tall (`sp3.py:140`); elsewhere 36 px (`home2.py:115`).
- **Table (`.dtab`):**
  - Columns: TIME, DAY, ITEM, DAILY AMT (plus Female / Male or band columns when amounts are tailored).
  - Header: `--md3-surface-variant`, 12 px uppercase.
  - Cells: 12 px padding, `--md3-surface-variant` lines. Amounts right aligned, 600 weight.
  - Wrapper `.dtab-wrap` has `overflow-x: auto`. No horizontal scroll was measured at 810 or 1080 with the sample diets.
- **Item cell:** name, MIX / RECIPE tag, "(prep)", mix parts, and "or <alternative> · <qty>" lines.
- **Code:** `table()` `sp3.py:436`, `nutrition()` `:453`, CSS `home2.py:114-127`.

### 3.6 Empty states (`.callout`, `.dpempty`)

| State | Title | Body | Actions |
|---|---|---|---|
| Species with no base diet | "No base diet yet" | "Create the base diet first. It is the always-on default for everyday feeding. …" | Create base diet (teal, dieticians in charge) · Request a base diet (outlined, Biologist) · "Only dieticians in charge of this species can create diets." for other roles |
| Target with nothing to inherit | "No diet yet" | "No diet applies to <target> yet. Request one and the dietician configures it." | Request new diet (teal) |
| Scope chosen, no target picked | "Pick an animal to see its diets" (species with a diet) / "Pick an animal to see its diet" (no diet) | "Choose an animal above. Each row shows the diet it gets today." / "Choose an animal above." | none |
| Request form, no eligible dietician | "No dietician is in charge of <target>" | "Ask an administrator to assign a dietician to this species or location. The request cannot be sent until then." | none; Continue is blocked |

- **Code:** `callout()` `sp3.py:519`, call sites in `detailHtml()` `sp3.py:522`; `.dpempty` `req.py:34-37` (warning tint, `alert` icon `#8A5A00`).
- The callout icon sits in a 56 px circle on `--md3-background`, and the text is centred with a maximum width of 56ch.

### 3.7 Buttons

| Variant | Class | Look | Used for |
|---|---|---|---|
| Primary (flow) | `.btn.teal` | Teal fill, white 16 / 600, 48 px tall, radius 8 | Request new diet, Request diet change, Create base diet, Accept request, Certify and send, Accept, Mark processing, Mark ready |
| Secondary | `.btn.sec` | 1 px `--md3-outline-variant`, teal text | Edit, + New plan, Report delay, Change configuration, Ask for clarification |
| Danger | `.btn.danger` | 1 px error border, error text | Reject |
| Global primary | `.btn.pri` | Green fill, white text (2.43:1) | Wizard and request form footers (Continue, Submit request) |
| Add chip | `.addchip` | 48 x 48, dashed border, teal "+" | New plan on the plan chips row |

- **Sizes:** `.btn` is 48 px tall (`home2.py:195`); `.dp-edit` sets a minimum height of 44 px and padding 0 16 (`sp3.py:148`), but the `.btn` height of 48 px wins. Queue card buttons are 44 px tall (`hdq.py:49`).
- **Order:** primary first, then secondary, in one row (`.dp-btns`, `.cobtns`). When both are visible, the filled one is the action the role came for.

### 3.8 Tags and badges

| Tag | Class / colour | Text | Contrast |
|---|---|---|---|
| Kind: Year-round | `.ttag.yearround` (`build.py:245`) | "Year-round" with clock icon | 5.86 |
| Kind: Time-bound | `.ttag.timebound` | "Time-bound" with calendar icon | **2.35 (fails)** |
| Kind: Seasonal | `.ttag.seasonal` | "Seasonal" with star icon | **2.74 (fails)** |
| Inherited | `.tag.teal` | "Base diet · Inherited from species" / "Inherited from section <name>" | 7.82 |
| Status | `.tag.grey` (ink on the species views) / `.tag.green` | "Unverified" / "Verified", "Inactive" | 7.18 / 5.86 |
| Pending update | `.tag.orange` | "Update pending" | 4.64 |
| Own diet | `.tag.blue` | "Own diet" | 4.54 |
| Late | `.tag.red.late` with timer icon (`roles.py:282`) | "Late · 1 day" / "Late · n days" | **3.87 (fails at 13 px)** |
| Offline flag | `.tag.orange` | "May reply later" | 4.64 |
| Open request badge | `.rqb` (`req.py:7`) | "1 open request" / "n open requests" with clock icon | 6.97 |
| Kitchen line status | `.tag` by state (section 4) | "Waiting", "Accepted", "Processing", "Ready", "Delayed · ready from 8 Nov 2026" | per colour |

**Do:** pair every colour with a word, and an icon where there is one. **Don't:** use a coloured edge strip to show state.

### 3.9 Request form steps
- **Shell:** full-screen sheet with a close icon (48 px on the species views), the title "Request Diet Change", the species name, and a step bar ("1. Where it applies", "2. Request").
- **Context strip:** "Coypu · Animal-wide · Thistle · D-273".
- **Step 1, Where it applies:** linked selects (Site, Section, Enclosure, Individual animal, each "(optional)"), the read-only "Current diet" box (`.curdiet`), then **Send to dietician**.
- **Step 2, Request:** Request type select; Priority as three 72 px radio cards (`.prio`, `!!!` / `!!` / `!` markers on tertiary, secondary-dark and secondary fills); Short title (optional); Start and End; Reason; Notes; an info note naming the dietician.
- **Fields:** `.fld` inputs have a minimum height of 48 px and radius 8; focus border teal plus a 2 px tint ring; errors `.ferr` 13 px `--md3-error`; required marker `*` in error colour.
- **Footer:** Cancel (ghost), Back (secondary), Continue / Submit request (`.btn.pri`, green).
- **Code:** `openRequest()` `req.py:259`, `rfWhere()` `:290`, `rfDetails()` `:303`, `drawRF()` `:314`; CSS `req.py:4-39`, `wiz.py:37-46`.

### 3.10 "Send to dietician" picker row
- **Anatomy (`.dp`, `role="radio"`):** a 40 px initials avatar, the name (14 / 600), the eligibility scope (14 / 400 ink, for example "Site: Cow Land"), the "May reply later" tag for offline dieticians, then the status dot and label.
- **Status:**
  - Online: a 10 px filled dot in `--md3-primary`, with the label "Online" in `--md3-on-surface`.
  - Offline: a 10 px hollow dot (2 px `--ink` ring), with the label "Offline" in ink.
  - The label carries the meaning; the dot is decorative (`aria-hidden`).
- **States:**
  - Default: 1 px outline.
  - Selected (`aria-checked="true"`): 1 px teal border plus a 1 px teal ring, `--md3-displaybg-primary` fill.
  - Error: `aria-invalid` on the group plus `.ferr` "Choose a dietician to send this request to."
- **Size and order:** each row is at least 64 px tall, with 8 px between rows. Online dieticians are listed first, then by name.
- **Code:** `rfPicker()` `req.py:341`; CSS `req.py:22-37`.
- **Copy:**
  - Heading: "Send to dietician *".
  - Hint: "Dieticians in charge of <target>. Pick one to review and approve the request."
  - Toast: "Request DR-00001 sent to Hydar Ali."

### 3.11 Dietician queue card (`.hdcard.hdx`)
- **Anatomy:**
  - Top: ID, Late tag, species, where, priority ribbon.
  - Body: title, reason, proposed diet line, "Requester • date".
  - Footer strip (`.hdx__foot`): next step, detail, and button.
- **Footer tones (tinted backgrounds, not edge strips):** `review` (`--moderate-a10`), `config` (teal tint), `back` (`--error-a5`), `wait` (`--neutral05`). The footer is at least 60 px tall; its button is 44 px tall and at least 112 px wide.
- **Copy:** "Review and accept" / "Configure" / "Proposal saved: certify and send to kitchens", plus "Raised 5 days ago".
- **Kitchen Head variant (`kcard`):** "K3 · Fruit Store: Apple, Bannana", "Diet starts 8 Nov 2026, ends 30 Nov 2026", and next step "Accept your items" / "Start processing" / "Mark ready when done" / "Delayed: ready from 8 Nov 2026".
- **Code:** `hdq.py:136` (`top`), `:142` (`kcard`), `:161` (`card`), CSS `hdq.py:25-49`.

### 3.12 Request detail: Sent to, progress, Kitchens
- **Rows (`.srow`):** Applies to, Current diet, Request, Diet type, Priority, Notes, Proposed diet, Requested by, **Sent to** ("Hydar Ali · Dietician · Species: Coypu"), Accepted by ("Dietician · certified the diet").
- **Progress (`.tl`):**
  - Six steps:
    1. Request submitted
    2. Dietician reviewing
    3. Configured and certified
    4. Kitchens preparing
    5. Scheduled
    6. Live
  - Markers are 28 px: done = green fill, current = teal ring with a 3 px halo, rejected = red fill. A 2 px connector line joins them.
  - Header: "Step 4 of 6: Kitchens preparing".
  - Code: `RQ.timeline` `roles.py:303`, CSS `req.py:71-84`.
- **Kitchens (`.klist`):**
  - Heading "Kitchens" with "2 of 3 ready", or "Your kitchen" with "K3 · Fruit Store" for a Kitchen Head.
  - Each line (`.kl`): kitchen name, status tag, Late tag, items, reason (when delayed), "Kitchen not set in masters …" (when needed), and "<who> · <date, time>".
  - Each line is outlined, radius 8, padding 12 / 16, with 8 px between lines.
  - Code: `klinesHtml()` `roles.py:465`, CSS `roles.py:179-187`.

### 3.13 Kitchen Head line actions and the Report delay sheet
- **Actions by line state** (footer, `actionsFor()` `roles.py:441`):

| Line state | Buttons |
|---|---|
| Waiting | Report delay (secondary), Accept (teal) |
| Accepted | Report delay, Mark processing |
| Processing | Report delay, Mark ready |
| Delayed | Change delay, Mark ready |

- **Report delay sheet** (`FORMS.kdelay` `roles.py:438`):
  - Title "Report a delay".
  - Text: "The whole diet starts on the latest ready date across kitchens. Everyone on the request sees the date and your reason."
  - Fields: **Ready from** (date, required, not before today) and **Reason** (required; hint "Enter the reason, for example Need to procure item.").
  - Buttons: Cancel, Report delay. Toast: "Delay reported."
- **Certify sheet** (`FORMS.certify` `roles.py:437`): a preview list (`.kprev`) with one row per kitchen ("K1 · Central Kitchen" / "Carrot, Beans, Maize, Cooked Veg Mix, Rice"), then "Certify and send".

### 3.14 Start and return notes (`.rnote`)
- **Start note:**
  - Calendar icon; `.warn` tint (`#FFF6DB`, icon `#8A5A00`) when a kitchen is late.
  - "**Diet starts 8 Nov 2026**", then "Delayed by K3 · Fruit Store: Apple, Bannana. Need to procure item. Ready from 8 Nov 2026."
  - Small print: "The whole diet starts on one date: the latest ready date across kitchens. The current diet stays until then." (when live: "The new diet is active.").
- **Return note:** history icon, outlined. "**Ends 30 Nov 2026**", then "Automatically returns to base diet D-273 after 30 Nov 2026."
- **Other notes:** Locked, Clarification requested or answered, Rejected (`.rnote.bad`: error tint).
- **Code:** `notes()` `roles.py:475`; CSS `roles.py:172-177`, `:192-193`. The old inset edge strips are removed.

### 3.15 Toasts
- **Look:** teal fill, white text (8.80:1), radius 8, padding 12 / 20. Centred, 104 px from the bottom on diet-home (`roles.py:214`); 2400 ms.
- **Action toast** (`toastAct`): an inline button (`.tact`, at least 36 px tall); stays for 6000 ms.
- **Strings:**
  - "Request DR-00001 sent to Hydar Ali." with the "View request" action
  - "Proposed diet D-308 saved to DR-00001. It is not active."
  - "Certified and sent to the kitchens."
  - "Marked ready for K3 · Fruit Store. All kitchens ready: diet starts 8 Nov 2026."
  - "Delay reported."
  - "Choose a dietician to send this request to."
- **TBD:** the 36 px action button in the toast is under the 48 px target.

### 3.16 Diet history button and sheet
- **Segments:** "Diets (n)" and "Requests (n)".
- **Requests grouping:** for a dietician, To configure / Configured by me / Other; for the Biologist, Open then Closed.
- **Rows:** priority ribbon, ID · title, type · target · dates, requester, status tag.
- **Code:** `historyHtml()` `sp3.py:559`; the validity column uses `dd-mm-yy` (`sp3.py:580`).

### 3.17 Also used by (`details.shared`)
- **Anatomy:** a collapsed summary "Also used by n other species" (44 px tall, chevron rotates), then a 2-column list of species links (`.shrow`, 44 px tall).
- **Code:** `shared()` `sp3.py:511`, CSS `sp3.py:151-160`.
- **TBD:** 44 px, under the 48 px target.

### 3.18 Viewing as sheet
- **Purpose:** a demo role switcher listing 12 roles, each with a one-line description (dieticians: online or offline plus scopes; Kitchen Heads: their kitchen).
- **Button:** the "Viewing as: <name> · <title>" pill is 48 px tall in the species panel (`sp3.py:143`) and 44 px elsewhere (`roles.py:73`).

## 4. Status system

### 4.1 Request states

| State | Label text | Tone / colour | Icon |
|---|---|---|---|
| requested | "Requested" | wait (amber `.stchip`, `#FFF4CC` / `#6B5200`) | time |
| under_review | "Under Dietician Review" | wait | time |
| configuring | "Configuring" | wait | pencil |
| with_kitchens | "With kitchens · 2 of 3 ready" or "With kitchens · starts 8 Nov" | wait | time |
| scheduled | "Starts 8 Nov" | ok (green `.stchip.ok`, `#D7F5E3` / `#006D35`) | calendar |
| live | "Live since 12 Oct" | ok | just-tick-mark |
| rejected | "Rejected" | bad (`#FFE0E5` / `#E93353`) | close |
| cancelled | "Cancelled" (**not reachable in v1**) | bad | close |

Sources: `RQ.ST` `roles.py:229`, `RQ.decorate` (labels), `.stchip` `req.py:53-54`. Older states (`kitchen_review`, `delayed`, `adjustment`, `ready`, `applied`) remain in code but no request uses them.

### 4.2 Kitchen line states (`RQ.KLS` `roles.py:318`)

| State | Label | Tag colour | Icon |
|---|---|---|---|
| pending | "Waiting" | `.tag.grey` | time |
| accepted | "Accepted" | `.tag.teal` | just-tick-mark |
| processing | "Processing" | `.tag.teal` | timer |
| ready | "Ready" | `.tag.green` | just-tick-mark |
| delayed | "Delayed · ready from 8 Nov 2026" | `.tag.orange` | timer |

### 4.3 SLA badge rules (`RQ.late`, `RQ.lateTag` `roles.py:277-283`)

| Who | Counted from | Late when | Badge |
|---|---|---|---|
| Dietician | Submission (`events[0].at`) | Still Requested, Under review or Configuring after 1 day (High), 3 days (Medium) or 7 days (Low) | "Late · n days" (days over the limit), red tag with timer icon, on queue cards |
| Kitchen line | Sent to kitchens (`sentAt`) | Still Waiting, Accepted or Processing after 1 day (a Delayed line is not late) | Same badge on the line and on the Kitchen Head's card |

## 5. Content and voice

- **Sentence case** for titles, buttons and tags ("Request new diet", "Certify and send to kitchens", "Time-bound"). The tags were changed from "Time-Bound" and "Sex-Based".
- **Dates:**
  - "8 Nov 2026" (`RQ.fmt`, `dmy()`); "8 Nov" when short in labels.
  - "Year-round since 22 Sep 2026"; ranges "12 Oct 2026 to 30 Nov 2026".
  - Never dd-mm-yy in the species views.
  - Exception: the Diet history table still shows `dd-mm-yy` validity (`sp3.py:580`); listed in section 9.
- **Separators:** a middle dot " · " between facts. No em or en dashes (enforced by `page()` in `build.py`).
- **CTA labels:**
  - Request: Request new diet, Request diet change, Request a base diet.
  - Diet: Create base diet, New plan, Edit.
  - Review: Accept request, Reject, Ask for clarification, Configure diet, Change configuration, Certify and send to kitchens.
  - Kitchen: Accept, Mark processing, Mark ready, Report delay, Change delay.
- **Delay message format:** "Delayed by <Kn> · <kitchen>: <items>. <reason>. Ready from <date>."
- **Next-step lines** (request footer):
  - "You to review", "Hydar Ali to review", "You to certify and send to kitchens"
  - "Waiting on K3", "You to mark ready when the items arrive"
  - "Diet starts 8 Nov 2026. Nothing else to do."
- **Empty or blocked:** say what is missing and what to do ("Ask an administrator to assign a dietician …"). No "Oops", no exclamation marks.

## 6. Layout patterns

**Portrait 810 (full-screen panel):**
```
┌ ← Coypu / Myocastor coypus          [Viewing as] ┐  panel header (h1 gets focus on open)
│ ┌──────────── one section (.spsheet) ──────────┐ │
│ │ TSN · class                                   │ │
│ │ 38 Animals  1 Site  1 Active diet [History]   │ │
│ │                                     32px      │ │
│ │ SCOPE  [Species][Section][Enclosure][Animal]  │ │
│ │ search · filters · target rows (scroll 360)   │ │
│ │                                     32px      │ │
│ │ Diet for Thistle                              │ │
│ │ D-273 Year-round · tag · meta  [Request][+]   │ │  sticky action row
│ │ [Items|Nutrition]  table                      │ │
│ └───────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────┘
```

**Landscape 1080 (list : detail = 2fr : 3fr, `sp3.py` landscape media query):**
```
┌ Species list (2fr) ──────┐┌ Detail (3fr, sticky, own scroll) ┐
│ [card] Coypu  1 Active ▸ ││ Coypu / Myocastor coypus          │
│ [card] ...               ││ TSN · stats · [Diet history]      │
│                          ││ SCOPE ... target rows (296)       │
│                          ││ Diet card, sticky action row      │
└──────────────────────────┘└───────────────────────────────────┘
```

- **Sticky actions:** the plan and inherited card action row (`sp3.py:136`); the request detail footer (`.rqd__foot`); the wizard footer.
- **Overflow rules:**
  - No horizontal page scroll at 810 or 1080 (measured).
  - Tables scroll horizontally inside `.dtab-wrap` only if needed.
  - Target lists scroll vertically, with containment (`overscroll-behavior: contain`) and fade cues.
  - Long names wrap (`overflow-wrap: anywhere` on the species name).
- **Container query:** the summary row stacks under 640 px of section width (`@container hero`).

## 7. Accessibility

- **Targets:** at least 48 x 48 on the species list, detail and request form (measured with getBoundingClientRect: 0 under 48, except the bare search text inside a 48 px label). Rules are at `sp3.py:139-144`.
- **Focus:**
  - The global `:focus-visible` ring is 2 px teal with a 2 px offset (`build.py:137`).
  - Opening the portrait species panel moves focus to the panel `h1` (`openPanel()` `sp3.py:550`).
- **Labels:**
  - Icon buttons have `aria-label` (for example "Edit D-273", "New plan for Thistle").
  - The picker is a radiogroup labelled by "Send to dietician", with `aria-required`, and `aria-invalid` plus `aria-describedby` on error.
  - The online dot is `aria-hidden`; the label carries the status.
  - Toasts use `role="status"`.
- **Contrast** (section 2.1): body and action text pass. Known failures are listed in section 9.
- **Known gaps:**
  - The green Continue / Submit request in the form footer is 2.43:1.
  - Time-bound and Seasonal kind tags are 2.35 and 2.74.
  - The red Late tag is 3.87 at 13 px.
  - Toast action, "Also used by" rows and queue card buttons are under 48 px.
  - Screen reader output is not verified; 200% zoom is not verified.

## 8. Roles × UI matrix

| Control | Biologist | Dietician in charge of the species | Dietician not in charge | Kitchen Head K1 / K2 / K3 |
|---|---|---|---|---|
| Request new diet / Request diet change / Request a base diet | Yes | No | No | No |
| Edit, + New plan, "+" chip, Create base diet | No | Yes | No (removed from the DOM) | No |
| Diet history | Yes (own requests) | Yes (requests sent to them) | Yes (requests sent to them) | Yes (requests with their line) |
| Request tab view | My requests | Queue: To configure / Configured by me / All | Same, only their requests | To do / Ready / All for their line |
| Accept, Reject, Ask for clarification, Configure, Certify and send | No | Yes, on requests sent to them | Yes, on requests sent to them | No |
| Kitchens section on a request | All lines | All lines | All lines | Own line only ("Your kitchen") |
| Accept / Mark processing / Mark ready / Report delay | No | No | No | Own line only |
| Edit request (until accepted) | Own requests | No | No | No |

"In charge of" means one of the dietician's scopes matches the species' class, the species, or one of its sites, sections, enclosures or animals (`mayEdit()`). Directory Edit applies the same check.

## 9. Known gaps / tokens to fix globally

| Item | Today | Proposal |
|---|---|---|
| `--md3-neutral-secondary` `#7A8684` | 3.77:1 on white, 3.41:1 on `#EFF5F2`; overridden with `--ink` only on the species views | Darken the token globally, or move its text uses to `--ink`. Needs a design decision; it affects Kitchen and Security. |
| Global primary `.btn.pri` `#37BD69` with white | 2.43:1; still on the request form and wizard footers | Use teal `.btn.teal` for primary actions everywhere, or darken the green fill. |
| Kind tag text (`.ttag.timebound` `#00AFD6`, `.ttag.seasonal` `#FA6140`) | 2.35 and 2.74 | Use the darker text colours already used by `.tag.blue` (`#00799A`, 4.54) and `.tag.orange` (`#C2401F`, 4.64). |
| `.tag.red` (Late) | 3.87 at 13 px | **TBD:** darker red text token. |
| Shared controls at 44 px (`.iconbtn`, `.asbtn`, `.chip` 40, `.spchip` 40, `.seg3`, `.dseg` 36) | 48 px only on the species views via scoped rules | Raise the shared components to 48 px across Diet, Kitchen and Security. |
| Press scale | `.98` `.btn`, `.97` `.chip`, `.96` `.spfilter`, `.94` `.iconbtn` | **TBD:** one value. |
| Diet history validity `dd-mm-yy` (`sp3.py:580`) | Ambiguous date format | Use `dmy()` ("8 Nov 2026") as elsewhere. |
| `.tgh`, `.pchip .l2`, `.dtab th`, `.hcount` at 12 px | Below the 13 px floor used elsewhere in the flow | Raise to 13 px. |

## 10. Changelog

- **19 Oct 2026:** first version, written from `_build/` at commit 79fef1f plus that day's work.
  - Covers the single-section species detail, inherited diet card, one request entry per view and teal primary.
  - Covers the "Send to dietician" picker with online / offline, the dietician queue, Certify and send, kitchen lines K1 to K3 with Report delay, the "Diet starts" and auto-return notes, and the SLA late badges.
  - Records the contrast measurements and known gaps.
