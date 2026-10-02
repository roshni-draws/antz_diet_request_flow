#!/usr/bin/env python3
"""Builds the Diet flow screens (self-contained HTML) into 'Final screens _diet /'.
Shared sections are assembled here so every page carries the same tokens / base / shell / status bar / app bar CSS."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
# Output: the folder that holds _build/ (Final screens _diet /), or DIET_OUT if set.
OUT = os.environ.get('DIET_OUT') or (os.path.dirname(HERE) + os.sep if os.path.basename(HERE) == '_build' else "/Users/roshnishenoy/Documents/work/lset /antz/Antz App /Final screens _diet /")
ICONS = json.load(open(os.path.join(HERE, 'icons.json')))
DATA = json.load(open(os.path.join(HERE, 'dataset.json') if os.path.exists(os.path.join(HERE, 'dataset.json')) else os.path.join(HERE, '..', 'site', 'dataset.json')))

MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
def md(s): m, d = s.split('-'); return f"{int(d)} {MON[int(m)-1]}"
def ymd(s): y, m, d = s.split('-'); return f"{int(d)} {MON[int(m)-1]} {y}"
def hm(s):
    h, m = map(int, s.split(':')); ap = 'am' if h < 12 else 'pm'; h12 = h % 12 or 12
    return f"{h12}:{m:02d} {ap}"

SP = {s['id']: s for s in DATA['sp']}
PLANS = []
for p in DATA['plans']:
    t = p.get('type')
    when = ''
    if t == 'seasonal': when = f"{md(p['from'])} → {md(p['to'])}"
    elif t == 'timebound': when = f"{ymd(p['start'])} → {ymd(p['end'])}"
    PLANS.append({
        'code': p['code'].replace('Diet ', ''), 'name': p['name'], 'sp': p['sp'], 'spn': SP[p['sp']]['name'],
        'type': t or 'none', 'when': when, 'status': p['status'], 'times': [hm(x) for x in p['times']],
        'items': p['items'], 'levels': len(p['levels']),
    })
N_DIETS = len(PLANS)
N_ACTIVE = sum(1 for p in PLANS if p['status'] == 'active')
N_SP = len(DATA['sp'])
N_SP_WITH = sum(1 for s in DATA['sp'] if not s['none'])

# requests: as listed on the site's Requests > All tab (12 Jun 2026 demo day)
REQS = [
    ['DR-00424', 'Asiatic Lion', 'Animal · Raja · Lion Enclosure A', 'high', 'Soft food after dental surgery', 'Raja has dental surgery on 14 Jun. The vet recommends boneless, minced meat for two weeks, then back to the standard diet.', '12 Jun 2026', '2026-06-12', 'awaiting', 'Awaiting approval', 'wait', 'time'],
    ['DR-00421', 'African Cuckoo-Hawk', 'Enclosure · Aviary 03', 'medium', 'Fewer chicks, more calcium for Aviary 03', 'Birds in Aviary 03 are gaining weight on the High Protein Diet. Reduce day-old chicks from 4 to 3 a day and add a calcium supplement.', '10 Jun 2026', '2026-06-10', 'completed', 'Completed · Awaiting kitchen', 'wait', 'time'],
    ['DR-00417', 'African Cuckoo-Hawk', 'Animal · Tara · Aviary 05', 'medium', 'Extra protein while Tara moults', 'Tara has started her moult. Add extra protein for three weeks so the new feathers come in well.', '9 Jun 2026', '2026-06-09', 'approved', 'Approved · Animal moved', 'wait', 'just-tick-mark'],
    ['DR-00415', 'African Cuckoo-Hawk', 'Animal · Kiara · Aviary 03', 'high', 'Soft food after wing surgery', 'Kiara had a wing fracture repaired on 8 Jun. The vet asks for soft, easily digested food for two weeks.', '8 Jun 2026', '2026-06-08', 'completed', 'Completed · Applied', 'ok', 'just-tick-mark'],
    ['DR-00423', 'Sloth Bear', 'Section · Bear Wing', 'low', 'Monsoon diet for Bear Wing', 'In the monsoon the bears in Bear Wing eat less fruit and need more protein. Suggest a monsoon diet from July to September.', '5 Jun 2026', '2026-06-05', 'progress', 'In Progress', 'wait', 'pencil'],
    ['DR-00419', 'Great Hornbill', 'Enclosure · Hornbill Aviary', 'high', 'More fruit for the breeding pair', 'Kavi and Meera are nesting. Increase figs and add a second mouse so the female is fed well while sealed in the nest.', '1 Jun 2026', '2026-06-01', 'completed', 'Completed · Kitchen in progress · Delayed to 20 Jun', 'wait', 'timer'],
    ['DR-00416', 'Spotted Deer', 'Site · Rescue Centre', 'high', 'Richer diet for rescued deer', 'Rescued deer at the Rescue Centre are underweight. They need a richer diet than the zoo herd until they recover condition.', '28 May 2026', '2026-05-28', 'completed', 'Completed · Kitchen in progress · Delayed to 15 Jun', 'wait', 'timer'],
    ['DR-00412', 'Indian Star Tortoise', 'Species · Species-wide', 'low', 'Winter: fewer greens', 'Tortoises eat less in winter. Suggest cutting the greens by a third from November to February.', '18 May 2026', '2026-05-18', 'closed', 'Rejected', 'bad', 'close'],
    ['DR-00410', 'Asiatic Lion', 'Section · Big Cats', 'low', 'Add bone meal for Big Cats', 'Add bone meal to the evening feed for all lions in Big Cats.', '15 May 2026', '2026-05-15', 'closed', 'Cancelled', 'bad', 'close'],
    ['DR-00402', 'African Cuckoo-Hawk', 'Enclosure · Aviary 03', 'medium', 'Breeding diet for Aviary 03', 'Aviary 03 has two breeding pairs this season. Raise protein for the birds in this aviary.', '12 Mar 2026', '2026-03-12', 'completed', 'Completed · Applied', 'ok', 'just-tick-mark'],
    ['DR-00398', 'Asiatic Lion', 'Species · Species-wide', 'medium', 'Leaner lion diet', 'Keepers report the lions leave meat every evening. Reduce the meat and add liver for vitamins.', '28 Jan 2026', '2026-01-28', 'completed', 'Completed · Applied', 'ok', 'just-tick-mark'],
]
REQ_KEYS = ['id', 'sp', 'where', 'prio', 'title', 'text', 'date', 'iso', 'group', 'label', 'tone', 'icon']
REQS = [dict(zip(REQ_KEYS, r)) for r in REQS]
N_REQ = len(REQS)
N_AWAIT = sum(1 for r in REQS if r['group'] == 'awaiting')
N_OPEN_HIGH = sum(1 for r in REQS if r['prio'] == 'high' and r['tone'] == 'wait')


def svg(name, size=24, cls='', grad=None):
    body = ICONS[name]
    if grad:
        body = body.replace('currentColor', f'url(#{grad})')
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} width="{size}" height="{size}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{body}</svg>'


def icon_js(names):
    m = {n: ICONS[n] for n in names}
    return ('/* Antz app icons (from the live prototype\'s icon library), inline */\n  const IC = ' + json.dumps(m) + ';\n'
            "  function ic(n, s) { s = s || 24; return '<svg width=\"' + s + '\" height=\"' + s + '\" viewBox=\"0 0 24 24\" aria-hidden=\"true\" focusable=\"false\">' + IC[n] + '</svg>'; }\n")


FONTS = '''  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">'''

COMMON_CSS = '''    /* =========================================================
       1. TOKENS
       Flow tokens (diet-module-flow.html) + Antz app tokens taken from
       the live prototype (app/tokens.css, MD3_Antz Figma styles).
       ========================================================= */
    :root {
      /* flow */
      --white: #FFFFFF;
      --status-h: 24px;
      --ring: #1F515B;
      --ease: cubic-bezier(.2,.7,.2,1);
      /* Antz app colour (MD3_Antz) */
      --md3-primary: #37BD69;
      --md3-on-surface: #006D35;
      --md3-on-primary-container: #1F515B;
      --md3-on-secondary-container: #1F415B;
      --md3-secondary: #00D6C9;
      --md3-secondary-dark: #00ABAB;
      --md3-tertiary: #FA6140;
      --md3-error: #E93353;
      --md3-add-primary: #00AFD6;
      --md3-moderate-secondary: #E4B819;
      --md3-on-tertiary-container: #250E01;
      --md3-on-surface-variant: #44544A;
      --md3-neutral-secondary: #7A8684;
      --md3-background: #EFF5F2;
      --md3-on-background: #E1F9ED;
      --md3-displaybg-primary: #E8F4F2;
      --md3-surface-variant: #DAE7DF;
      --md3-outline-variant: #C3CEC7;
      /* app aliases (diet.css) */
      --head: #000000;
      --ink: var(--md3-on-surface-variant);
      --line: rgba(0,0,0,.05);
      --neutral05: rgba(0,0,0,.05);
      --primary-a10: rgba(55,189,105,.10);
      --tertiary-a10: rgba(250,97,64,.10);
      --add-primary-a10: rgba(0,175,214,.10);
      --moderate-a10: rgba(228,184,25,.10);
      --error-a5: rgba(233,51,83,.05);
      --card-shadow: 0 2px 8px rgba(0,0,0,.08);
      --grad-greenturq: linear-gradient(116.5deg, var(--md3-secondary) 8.77%, var(--md3-primary) 101.99%);
      /* spacing (app sp scale) */
      --sp-4: 4px; --sp-8: 8px; --sp-12: 12px; --sp-16: 16px; --sp-20: 20px; --sp-24: 24px; --sp-32: 32px;
      --radius: 8px;            /* app card radius */
    }

    /* =========================================================
       2. BASE  (reset + Antz text styles)
       ========================================================= */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: 100%; }
    html { -webkit-text-size-adjust: 100%; overflow-x: clip; }
    body {
      background: var(--md3-background); color: var(--ink); overflow: hidden;
      font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 14px; -webkit-font-smoothing: antialiased;
    }
    button, input { font: inherit; color: inherit; background: none; border: 0; }
    button { cursor: pointer; }
    a { color: inherit; text-decoration: none; }
    :focus { outline: none; }
    :focus-visible { outline: 2px solid var(--ring); outline-offset: 2px; }
    [hidden] { display: none !important; }
    svg { display: block; flex: none; }
    .sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }
    .icon-defs { position: absolute; width: 0; height: 0; overflow: hidden; }
    .t-stat-title    { font-size: 28px; font-weight: 600; line-height: normal; }
    .t-major-title   { font-size: 24px; font-weight: 600; line-height: normal; }
    .t-medium-medium { font-size: 20px; font-weight: 500; line-height: normal; }
    .t-minor-title   { font-size: 16px; font-weight: 600; line-height: normal; }
    .t-minor-medium  { font-size: 16px; font-weight: 500; line-height: normal; }
    .t-minor-italic  { font-size: 16px; font-weight: 400; line-height: normal; font-style: italic; }
    .t-body-title    { font-size: 14px; font-weight: 600; line-height: normal; }
    .t-body-medium   { font-size: 14px; font-weight: 500; line-height: normal; letter-spacing: .1px; }
    .t-body-regular  { font-size: 14px; font-weight: 400; line-height: normal; }
    .t-subtext-title { font-size: 12px; font-weight: 600; line-height: normal; }

    /* =========================================================
       3. SHELL  (status bar / app bar / scrolling main)
       ========================================================= */
    .app { display: grid; grid-template-rows: var(--status-h) auto 1fr; height: 100dvh; }
    .main { overflow-y: auto; overflow-x: hidden; padding: 0 var(--sp-16) var(--sp-32); }

    /* =========================================================
       4. STATUS BAR  (same as diet-module-flow.html)
       ========================================================= */
    .status {
      display: flex; align-items: center; justify-content: space-between; padding: 0 10px;
      background: var(--white); color: #0E1512;
      font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums;
    }
    .status__l { display: flex; gap: 10px; }
    .status__l span + span { font-weight: 500; }
    .status__r { display: flex; align-items: center; gap: 5px; }

    /* =========================================================
       5. APP BAR  (Antz #bar: back, title, site picker)
       ========================================================= */
    .bar {
      display: flex; align-items: center; gap: var(--sp-8);
      padding: var(--sp-16); background: var(--white); border-bottom: 1px solid var(--line);
    }
    .bar__hd { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
    .bar__hd h1 { color: var(--md3-on-primary-container); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .bar__hd p { color: var(--ink); }
    .iconbtn {
      width: 44px; height: 44px; border-radius: 22px; display: grid; place-items: center; flex: none;
      color: var(--md3-on-primary-container); transition: background-color 200ms var(--ease), transform 120ms var(--ease);
    }
    @media (hover: hover) { .iconbtn:hover { background: var(--md3-displaybg-primary); } }
    .iconbtn:active { transform: scale(.94); background: var(--md3-surface-variant); }
    .sitebtn { display: flex; align-items: center; gap: var(--sp-8); height: 48px; padding: 0 var(--sp-8); color: var(--head); border-radius: 8px; }
    @media (hover: hover) { .sitebtn:hover { background: var(--md3-displaybg-primary); } }
'''

TOOLS_CSS = '''    /* =========================================================
       TABS  (Antz .sdtabs: full-width, green underline)
       ========================================================= */
    .sdtabs { display: flex; margin: 0 calc(-1 * var(--sp-16)); background: var(--white); }
    .sdtabs button {
      flex: 1; height: 56px; display: flex; align-items: center; justify-content: center; gap: 4px;
      color: var(--md3-on-surface-variant); border-bottom: 3px solid transparent;
      transition: color 200ms var(--ease), border-color 200ms var(--ease);
    }
    .sdtabs button[aria-selected="true"] { color: var(--md3-primary); border-bottom-color: var(--md3-primary); }

    /* =========================================================
       SEARCH BAND  (Antz .spband: search field + filter button)
       ========================================================= */
    .spband {
      display: flex; align-items: center; gap: var(--sp-12); margin: 0 calc(-1 * var(--sp-16));
      padding: var(--sp-16) var(--sp-20); background: rgba(255,255,255,.75);
    }
    .spsearch {
      flex: 1; min-width: 0; height: 48px; display: flex; align-items: center; gap: var(--sp-8); padding: 12px;
      border: 1px solid var(--neutral05); border-radius: 8px; background: var(--neutral05); color: var(--md3-neutral-secondary);
    }
    .spsearch:focus-within { border-color: var(--md3-on-primary-container); background: var(--white); }
    .spsearch input { flex: 1; min-width: 0; height: 100%; color: var(--head); }
    .spsearch input::placeholder { color: var(--md3-neutral-secondary); }
    .spfilter {
      min-width: 48px; height: 48px; flex: none; display: inline-flex; align-items: center; justify-content: center; gap: var(--sp-4);
      padding: 0 var(--sp-12); border: 1px solid var(--neutral05); border-radius: 8px; background: var(--neutral05); color: var(--head);
      transition: background-color 200ms var(--ease), transform 120ms var(--ease);
    }
    .spfilter.on { background: var(--md3-on-primary-container); border-color: var(--md3-on-primary-container); color: var(--white); }
    .spfilter[aria-pressed="true"]:not(.on) { border-color: var(--md3-on-primary-container); background: var(--white); }
    .spfilter:active { transform: scale(.96); }

    /* filter chips (Antz .spchip: grey, dark teal when on) */
    .spchips { display: flex; flex-wrap: wrap; gap: var(--sp-12); padding: var(--sp-16) 0 0; }
    .spchip {
      height: 40px; padding: 0 var(--sp-16); border-radius: 6px; background: var(--neutral05); color: var(--md3-on-surface-variant);
      display: inline-flex; align-items: center; gap: 6px; transition: background-color 200ms var(--ease), color 200ms var(--ease);
    }
    .spchip[aria-pressed="true"] { background: var(--md3-on-primary-container); color: var(--white); }

    /* list bar (Antz .list-bar: count + sort chip) */
    .list-bar { display: flex; align-items: center; justify-content: space-between; gap: var(--sp-12); margin: var(--sp-16) 0 var(--sp-8); }
    .list-bar h2 { color: var(--md3-on-surface-variant); }
    .chip {
      height: 40px; padding: 0 var(--sp-16); border-radius: 999px; border: 1px solid var(--md3-outline-variant);
      background: var(--white); color: var(--ink); display: inline-flex; align-items: center; gap: var(--sp-8); white-space: nowrap;
      transition: transform 120ms var(--ease);
    }
    .chip:active { transform: scale(.97); }

    /* type tags (Antz .ttag) */
    .ttag { display: inline-flex; align-items: center; gap: 4px; padding: 4px 6px; border-radius: 4px; white-space: nowrap; }
    .ttag.yearround { color: var(--md3-on-surface); background: var(--md3-on-background); }
    .ttag.seasonal { color: var(--md3-tertiary); background: var(--tertiary-a10); }
    .ttag.timebound { color: var(--md3-add-primary); background: var(--add-primary-a10); }
    .ttag.none { color: var(--md3-neutral-secondary); background: var(--neutral05); }

    /* status pill (Antz "Active" pill on the diet pane) */
    .pill { display: inline-flex; align-items: center; height: 24px; padding: 0 10px; border-radius: 999px; white-space: nowrap; }
    .pill.active { color: var(--md3-on-surface); background: var(--md3-on-background); }
    .pill.inactive { color: var(--md3-neutral-secondary); background: var(--neutral05); }
    .pill.unassigned { color: var(--md3-neutral-secondary); background: transparent; border: 1px dashed var(--md3-outline-variant); }

    /* empty state (Antz .empty) */
    .empty { padding: var(--sp-32) var(--sp-24); text-align: center; display: flex; flex-direction: column; align-items: center; gap: var(--sp-8); background: var(--white); border-radius: var(--radius); }
    .empty .ei { width: 48px; height: 48px; border-radius: 50%; display: grid; place-items: center; background: var(--md3-background); color: var(--md3-outline-variant); margin-bottom: var(--sp-4); }
    .empty b { color: var(--head); }
'''

RM_CSS = '''    /* =========================================================
       REDUCED MOTION
       ========================================================= */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { transition: none !important; }
      .iconbtn:active, .chip:active, .spfilter:active, .card-press:active { transform: none !important; }
    }
'''

STATUS_HTML = '''    <div class="status" aria-hidden="true">
      <div class="status__l"><span>3:42 PM</span><span>Wed 30 Sep</span></div>
      <div class="status__r">
        <svg width="17" height="12" viewBox="0 0 17 12"><path fill="currentColor" d="M8.5 2.2c2.4 0 4.6.9 6.3 2.5l1.2-1.2A10.6 10.6 0 0 0 8.5.5 10.6 10.6 0 0 0 1 3.5l1.2 1.2A9 9 0 0 1 8.5 2.2Zm0 3.4c1.5 0 2.9.6 3.9 1.5l1.2-1.2a7.3 7.3 0 0 0-10.2 0l1.2 1.2c1-.9 2.4-1.5 3.9-1.5Zm0 3.4c.6 0 1.2.2 1.6.6L8.5 11.2 6.9 9.6c.4-.4 1-.6 1.6-.6Z"/></svg>
        <span>80%</span>
        <svg width="27" height="13" viewBox="0 0 27 13"><rect x=".5" y=".5" width="23" height="12" rx="3.5" fill="none" stroke="currentColor" opacity=".4"/><rect x="2" y="2" width="16.4" height="9" rx="2" fill="currentColor"/><path d="M25 4.5v4a2 2 0 0 0 0-4Z" fill="currentColor" opacity=".4"/></svg>
      </div>
    </div>'''


def bar(title, back_href, back_label, sub='', site=True):
    s = f'<p class="t-body-regular">{sub}</p>' if sub else ''
    site_btn = (f'<button class="sitebtn" type="button" aria-label="Site: All Sites">{svg("location-icon", 24)}'
                f'<span class="t-minor-medium">All Sites</span>{svg("dropdown", 20)}</button>') if site else ''
    return f'''    <header class="bar">
      <a class="iconbtn" href="{back_href}" aria-label="{back_label}">{svg("back", 24)}</a>
      <div class="bar__hd"><h1 class="t-medium-medium">{title}</h1>{s}</div>
      {site_btn}
    </header>'''


def page(fname, title, top_comment, css, body, js='', tools=True):
    html = f'''<!DOCTYPE html>
<!-- {top_comment} -->
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{title}</title>
{FONTS}
  <style>
{COMMON_CSS}{TOOLS_CSS if tools else ''}{css}{RM_CSS}  </style>
</head>
<body>
{body}
{('  <script>' + chr(10) + '  (function () {' + chr(10) + "  'use strict';" + chr(10) + js + '  })();' + chr(10) + '  </script>') if js else ''}
</body>
</html>
'''
    assert '—' not in html and '–' not in html, fname
    open(OUT + fname, 'w').write(html)
    print('wrote', fname, len(html))


GRAD_DEFS = '''  <svg class="icon-defs" aria-hidden="true" focusable="false">
    <defs>
      <!-- Antz Gradients/greenturq: Secondary #00D6C9 to Primary #37BD69 -->
      <linearGradient id="g-turq" x1="2" y1="2" x2="22" y2="22" gradientUnits="userSpaceOnUse">
        <stop offset="0" stop-color="#00D6C9"/><stop offset="1" stop-color="#37BD69"/>
      </linearGradient>
    </defs>
  </svg>'''

exec(open(os.path.join(HERE, 'pages.py')).read())
exec(open(os.path.join(HERE, 'home2.py')).read())
exec(open(os.path.join(HERE, 'kitchen.py')).read())
