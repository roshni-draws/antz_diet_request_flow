# Design system: Diet module tablet prototype

The visual language used in `diet-home.html` and the Modules screens. It follows the Antz diet tablet prototype (antz-diet.pages.dev) and the Antz Material 3 based tokens. All values come from the CSS in `_build/` (`build.py` holds the tokens and base; component CSS sits in `home2.py`, `pages.py`, `sp3.py`, `wiz.py`, `req.py`, `roles.py`, `hdq.py`).

Light theme only. There is no dark mode in this prototype.

## 1. Colour tokens

Defined on `:root` in `build.py`.

### Core

| Token | Value | Role |
|---|---|---|
| `--md3-background` | `#EFF5F2` | Page background behind cards |
| `--white` | `#FFFFFF` | Cards, app bar, tabs, sheets, wizard footer |
| `--md3-on-primary-container` | `#1F515B` | Title teal: app bar titles, teal buttons, selected chips, links, icons, focus ring (`--ring`) |
| `--md3-on-secondary-container` | `#1F415B` | Request IDs, requester names |
| `--md3-primary` | `#37BD69` | Brand green: active tab underline and label, primary (Next, Continue, Save) buttons, success icons |
| `--md3-on-surface` | `#006D35` | Dark green text on green tints (Active, Year-round, done steps) |
| `--md3-on-background` | `#E1F9ED` | Light green tint for Active pills, year-round tags, done steps |
| `--md3-displaybg-primary` | `#E8F4F2` | Light teal tint: hover, selected option cards, teal tags, info notes |
| `--head` | `#000000` | Card titles, item names, primary text |
| `--ink` / `--md3-on-surface-variant` | `#44544A` | Body text, secondary labels |
| `--md3-neutral-secondary` | `#7A8684` | Muted text, helper text, counts |
| `--md3-surface-variant` | `#DAE7DF` | Table headers, pressed states, inner outlines |
| `--md3-outline-variant` | `#C3CEC7` | Borders of chips, inputs, secondary buttons |
| `--line` / `--neutral05` | `rgba(0,0,0,.05)` | Hairlines, grey chips, search field fill |

### Accents and status

| Token | Value | Role |
|---|---|---|
| `--md3-secondary` | `#00D6C9` | Low priority ribbon and badge |
| `--md3-secondary-dark` | `#00ABAB` | Medium priority ribbon and badge |
| `--md3-tertiary` | `#FA6140` | High priority ribbon and badge; seasonal tag text |
| `--md3-error` | `#E93353` | Errors, red tags, danger button, Sent back strip |
| `--md3-add-primary` | `#00AFD6` | Time-bound tag text |
| `--md3-moderate-secondary` | `#E4B819` | Waiting status icons |
| `--md3-on-tertiary-container` | `#250E01` | Text on the waiting band |
| `--primary-a10` | `rgba(55,189,105,.10)` | OK status band |
| `--tertiary-a10` | `rgba(250,97,64,.10)` | Seasonal tag and orange tag fill |
| `--add-primary-a10` | `rgba(0,175,214,.10)` | Time-bound tag and Proposed window fill |
| `--moderate-a10` | `rgba(228,184,25,.10)` | Waiting band, "To configure" header, From DR-x link |
| `--error-a5` | `rgba(233,51,83,.05)` | Bad band, error alerts |

Component-level colours used directly:

| Value | Where |
|---|---|
| `#C2401F` | Orange tag text |
| `#00799A` | Blue tag text, Proposed window text |
| `#8A5A00`, `#6B4E00` | Amber counts and text on the Diet history button and Requests segment when something is waiting to configure |
| `#FFF6DB`, `#FFF4D6`, `#E2B33C` | Amber highlight fill, overlap warning fill, highlight border |
| `#FAFCFB` | Tab hover |
| `rgba(0,0,0,.4)` | Sheet scrim |

### Gradient

- `--grad-greenturq: linear-gradient(116.5deg, #00D6C9 8.77%, #37BD69 101.99%)`, the Antz teal-to-green sweep.
- Diet icon: each part has its own sweep from `#1FDCD0` to `#4FCB90`.
- AI accent: `linear-gradient(90deg, #1F515B, #37BD69)` on the Prefill with AI button border and the AI line tag.

## 2. Typography

Font: **Inter** (Google Fonts), fallback `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`. Base size 14 px, antialiased, line height `normal`.

| Class | Size | Weight | Use |
|---|---|---|---|
| `.t-stat-title` | 28 | 600 | Header stats (Animals held, Diets) |
| `.t-major-title` | 24 | 600 | Sheet titles, species name in header |
| `.t-medium-medium` | 20 | 500 | App bar title, wizard title, card titles, plan IDs |
| `.t-minor-title` | 16 | 600 | Section titles, option titles, request IDs |
| `.t-minor-medium` | 16 | 500 | Tabs, status bands |
| `.t-minor-italic` | 16 | 400 italic | Scientific names |
| `.t-body-title` | 14 | 600 | Row titles, names |
| `.t-body-medium` | 14 | 500, +0.1 letter spacing | Buttons, chips, links |
| `.t-body-regular` | 14 | 400 | Body text |
| `.t-subtext-title` | 12 | 600 | Small labels |

Small caps labels (Reason, Notes, table headers): 12 px, 600, uppercase, 0.04 em tracking, `#7A8684`. Numbers in counts use tabular figures.

## 3. Spacing, radius, elevation

- **Spacing scale:** 4, 8, 12, 16, 20, 24, 32 px (`--sp-4` to `--sp-32`). Page gutter 16 px. Card padding 16 to 20 px. Gaps between cards 16 px.
- **Radius:**
  - 8 px (`--radius`) for cards, inputs, buttons, chips in sheets and the toast.
  - 4 px for tags.
  - 6 px for grey filter chips and window pills.
  - 12 px for segmented tracks and menus.
  - 16 px for the top of sheets.
  - 999 px for pills, step chips and outline chips.
- **Elevation:**
  - `--card-shadow: 0 2px 8px rgba(0,0,0,.08)` on cards that need lift (request cards, hover).
  - Menus use `0 12px 32px rgba(18,52,59,.16)`.
  - Most cards are flat white on the `#EFF5F2` background.
- **Motion:**
  - Easing `cubic-bezier(.2,.7,.2,1)`, 120 to 200 ms.
  - Press feedback `scale(.94)` to `scale(.995)`.
  - All transitions are removed under `prefers-reduced-motion`.

## 4. Components

### App bar
- **Anatomy:** 16 px padding, white background, bottom hairline. Back icon button (44 px round), title (20/500 teal, ellipsis), optional subtitle, Viewing as pill button, site picker (48 px, location icon, "All Sites", caret).
- **States:** icon buttons hover `#E8F4F2`, pressed `#DAE7DF` with `scale(.94)`.
- **Do:** keep one line. **Don't:** add actions beyond role and site.

### Tabs (main)
- **Anatomy:** three equal columns, 56 px high, white, label with count ("Diet Request - 6").
- **States:** default `#44544A`; selected `#37BD69` with a 3 px green underline; hover `#FAFCFB`.
- **Do:** use for the three Diet sections only.

### Segmented control
- **Anatomy:** grey track (`rgba(0,0,0,.05)`, radius 12, 4 px padding), equal segments 44 px high, radius 9, optional count.
- **States:** selected white with `0 1px 3px rgba(0,0,0,.12)`, teal 600 text; unselected `#44544A`.
- **Used for:** species coverage (3), HD request queue (3), Diet history Diets / Requests (2), Directory view.
- **Don't:** use for more than 3 options; use chips instead.

### Chips
- **Filter chip (`.spchip`):**
  - 40 to 44 px high, 0 16 px padding, radius 6, grey fill, `#44544A` text, optional count.
  - Pressed state is solid `#1F515B` with white text.
  - Used for sub-filters, scope chips and reasons.
- **Outline chip (`.chip`):**
  - 40 to 44 px high, pill, 1 px `#C3CEC7` border, white fill, icon plus label.
  - Press `scale(.97)`.
  - Used for secondary actions (Photos, Diet history, Prefill from, Add ingredient).
- **AI chip:** outline chip with a 1.5 px teal-to-green gradient border, sparkle icon in green, label in teal 600.
- **Do:** keep at most 3 to 4 chips per row. **Don't:** let action chips wrap; group them in a menu instead.

### Search field
- 48 px, radius 8, grey fill with hairline border, search icon, placeholder `#7A8684`.
- Focus: teal border and white fill.
- Paired with a 48 px filter button that turns solid teal when filters are on.

### Filter sheet
- Bottom sheet (see below) with labelled groups (small caps labels), multi-select chips, selects for species and requester.
- Footer Reset (secondary) and "Show n requests" (teal) with a live count.
- Active filters appear on the page as removable chips (44 px remove target) plus Clear.

### Cards
- **Content card (`.card2`, `.dpane`):** white, radius 8, padding 16 to 20 px, grid gap 12 to 16.
- **Request card (`.hdcard`):**
  - Top row: ID, species, target, with the priority ribbon at the right.
  - Body: title, two-line clamped text, requester and date.
  - Bottom: status band or next step strip with a button.
  - Card shadow; the whole card is tappable.
- **Header card (species):** container query layout with avatar, name, IDs, primary Request diet change button, stats and secondary buttons.
- **Don't:** nest cards inside cards; use tinted rows inside a card instead.

### List rows
- **Request row (`.sreq`):**
  - Min height 64 px, `#EFF5F2` fill, radius 8, priority ribbon flush left.
  - Title (ID · title), meta line, requester, optional next step (teal) and diet line, status tag at the right.
- **Species card:** avatar initials, name, scientific name, class and animal count, large diet count, chevron.
- **Selected:** 1.5 px green border.

### Priority ribbon
- **Request cards:** 56 x 40 px; **rows:** 48 x 36 px.
- Notched left edge (`clip-path` polygon), white bold text `!!!`, `!!` or `!`.
- High `#FA6140`, Medium `#00ABAB`, Low `#00D6C9`.
- In detail screens a priority badge (`.pribadge`, 28 px) uses the same colours with "!!! High" text.

### Status tags and bands
- **Tag (`.tag`):** 24 px, radius 4, 12/600.

  | Variant | Text | Fill |
  |---|---|---|
  | green | `#006D35` | `#E1F9ED` |
  | orange | `#C2401F` | 10% coral |
  | teal | `#1F515B` | `#E8F4F2` |
  | blue | `#00799A` | 10% cyan |
  | red | `#E93353` | 5% red |
  | grey | `#7A8684` | 5% black |

- **Kind tag (`.ttag`):** Year-round (green), Seasonal (coral on 10% coral), Time-bound (`#00AFD6` on 10% cyan), with an icon.
- **Pill (`.pill`):** 24 px full radius: Active (green), Inactive and Proposed (grey).
- **Window pill (`.win`):** 28 px, current (green), off or proposed (blue), inactive (grey).
- **Status band (`.hd-band`):** 48 px min.

  | Variant | Fill | Text or icon |
  |---|---|---|
  | wait | 10% amber | text `#250E01`, icon `#E4B819` |
  | ok | 10% green | text `#006D35`, icon `#37BD69` |
  | bad | 5% red | `#E93353` |

- **Next step strip (HD):** review (amber tint), config (teal tint), back (red tint), wait (grey). A 44 px teal button sits at the right.

### Badges
- **Open request badge (`.rqb`):** amber tint pill with a clock icon and "n open requests".
  - In the header it opens Diet history on Requests.
  - On a plan card it opens the request.
- **Count badge:** 22 px round count inside a button (Diet history), teal tint by default, amber (`#8A5A00` with white text) when work is waiting.
- **Filters count:** 20 px teal dot with white number.
- **AI line tag:** 11 px bold white "AI" on the AI gradient, radius 4.

### Buttons

| Variant | Spec | Use |
|---|---|---|
| Primary (`.btn.pri`) | 48 px, radius 8, `#37BD69`, white 16/600 | Continue, Next, Save, Accept / Send to Prep |
| Teal (`.btn.teal`) | `#1F515B`, white | Sheet confirm, Accept request, Send to Kitchen, Apply |
| Secondary (`.btn.sec`) | 1 px `#C3CEC7` border, teal text | Back, Cancel in sheets, Change configuration |
| Ghost (`.btn.ghost`) | text only, teal | Wizard Cancel |
| Danger (`.btn.danger`) | 1 px red border, red text | Reject |
| AI | outline chip with gradient border; Generate button is teal with a white sparkle | Prefill with AI |

- **States:** pressed `scale(.98)`; disabled opacity .45 with a not-allowed cursor.
- **Do:** one primary per footer. **Don't:** wrap labels; shorten them instead.

### Bottom sheets
- Scrim `rgba(0,0,0,.4)`; sheet white, width up to 640 px (wide variant 760 px), max height 86 dvh, top radius 16, padding 8 24 24.
- Grab handle, header row with title and 44 px close, content, right-aligned footer (buttons min 120 px).
- Long content scrolls inside the sheet; AI preview scrolls inside its own area so the footer stays visible.

### Wizard
- **Full screen:** title block, step bar, scrolling body, footer.
- **Step bar:** 32 px pills, radius 999, 13/500. Current step is solid teal with white text, done steps are green tint with a tick, later steps are grey.
- **Context strip:** white, radius 8, inset outline, teal text, paw icon. Shows species · scope · target · request · priority.
- **Footer:** white, top hairline. Cancel (ghost) on the left, Back (secondary) and the primary action on the right.
- **Body:** max width 880 px, or 1180 px with the request panel.

### Request side panel
- **Landscape:** a 320 px column, sticky, capped to the visible height.
- **Portrait:** a collapsible `details` bar.
- Pinned header (ribbon, "Request DR-x", title) and pinned footer link "Open full request". The body scrolls.
- Dates row carries an "Apply" link or a "Using" tick.

### Scroll areas with fades
- Inner scroll areas (request panel, scope target lists) use a 24 px mask fade at the top and bottom edge, shown only when more content exists in that direction.

### Menus
- Popover anchored under its button, right aligned, 300 px wide, radius 12, menu shadow.
- Items are 56 px with a title and a one-line hint; hover and focus use the teal tint. Esc closes it.

### Toasts
- Bottom centre, `#1F515B` fill, white text, radius 8, 12 20 px padding, max width viewport minus 32 px.
- Slides up 16 px and fades in 200 ms; auto hides after 2.4 s.
- Sits 104 px from the bottom on screens with a footer. An optional action button sits inline.

### Empty states
- White card, centred, 48 px round icon well, bold title, one line of guidance.
- Say how to populate, for example "Requests you configure and send to Kitchen appear here."

### Tables
- **Items table:** header row on `#DAE7DF` (12/600 uppercase), rows with 10 px padding and hairline separators, right-aligned amounts.
- **History table:** same style, five columns (Diet, Scope, Reason, Validity, Status).
- **Wizard items:** tappable rows open the item sheet; the remove button is 44 px.

### Alerts and notes
- **Alert (`.alert`):** 5% red fill, red text, alert icon. **Info:** teal tint, teal text, info icon. **Warn:** `#FFF4D6` fill, `#6B4E00` text.
- **Info note in option cards:** teal text with an info icon, never red for allowed options.

## 5. Icons

- Antz icon set (`icons.json`), inline SVG sprites rendered at 16, 18, 20, 22 or 24 px, using `currentColor`.
- Examples: back, search, filter-2, dropdown, location-icon, time, calendar, star, paw, sort, close, just-tick-mark, pencil, timer, reason-or-list, alert, approved, info, history, download, menu-vertical, add, transfer, grid, list, image, user, notes-new, book.
- Kinds: Year-round uses time, Seasonal uses star, Time-bound uses calendar, Base uses paw.
- The sparkle icon for AI is a small inline SVG.
- **Diet tile icon** (`diet-icon.svg`): clipboard plus apple glyph traced from the iPad Modules screen.
  - 60 x 70 unit glyph, shown at 75 x 88 pt on the tile.
  - Each part has its own `#1FDCD0` to `#4FCB90` sweep.
  - The tile (`diet-button.html`) matches the other Modules tiles.

## 6. Responsive rules

| | Portrait 810 x 1080 | Landscape 1080 x 810 |
|---|---|---|
| Directory, Species | Single column list; detail opens in a full-screen panel with its own app bar | List and detail side by side |
| Card grids | 1 column (directory cards 2) | 2 to 3 columns |
| Request detail | Stacked sections, timeline below | Two columns (3:2), timeline at the right |
| Wizard request panel | Collapsible bar above or below the step content | Sticky 320 px side column |
| Bands header | Title left, actions right; actions drop below the title as one group if narrow | Same, beside the request panel |
| HD queue tools | Filters button shows icon only | Filters button shows label |

- Container queries drive the species header card so it fits both the full-width panel and the landscape detail column.
- No horizontal page scroll; chip rows scroll horizontally inside themselves when needed.

## 7. Accessibility

- **Focus ring:** `:focus-visible` 2 px `#1F515B` outline with 2 px offset. Mouse focus shows no ring.
- **Tap targets:** 44 px minimum for buttons, chips, icon buttons, menu items and remove controls (sheet chips, filter remove, From DR-x link included).
- **Reduced motion:** all transitions are disabled and press transforms removed under `prefers-reduced-motion: reduce`; the AI spinner stops.
- **Semantics:**
  - Tabs, segmented controls and option cards use `role="tab"` or `role="radio"` with `aria-selected` or `aria-checked`.
  - Menus use `role="menu"`.
  - Sheets are `role="dialog"` with `aria-modal`.
  - Counts and status lines use `aria-live` where they update.
- **Labels:** icon-only buttons have `aria-label`. Priority ribbons have text labels ("High priority"). The Diet history button label includes open and to-configure counts.
- **Contrast notes:**
  - Body text `#44544A` on white and teal `#1F515B` on white pass AA.
  - Green `#37BD69` with white text is used at 16/600 for large button labels only.
  - Low priority white text on `#00D6C9` is the weakest pairing and relies on the bold `!` glyph plus the text label.
  - Amber highlight text was darkened to `#6B4E00` for legibility.
- **Text rule:** no em dashes in visible text.
