# pages.py: exec'd by build.py (shares its globals)

CHEV = svg('dropdown', 24, 'chev')

# ---------------------------------------------------------------- diet-home
HOME_CSS = '''    /* =========================================================
       6. SECTIONS  (three entry cards)
       portrait: stacked, icon + text + chevron, stats row below
       landscape: three across, stats pinned to the bottom
       ========================================================= */
    .sections { display: grid; gap: var(--sp-16); padding-top: var(--sp-16); }
    .sec {
      display: grid; grid-template-columns: 72px 1fr 24px; grid-template-areas: "ic t chev" "st st st";
      align-items: center; column-gap: var(--sp-20); row-gap: var(--sp-20);
      padding: var(--sp-24); background: var(--white); border-radius: var(--radius);
      -webkit-tap-highlight-color: transparent;
      transition: transform 160ms var(--ease), box-shadow 220ms var(--ease), background-color 220ms var(--ease);
    }
    @media (hover: hover) { .sec:hover { box-shadow: var(--card-shadow); } }
    .sec:active { transform: scale(.985); background: #F7FBF9; }
    .sec__ic { grid-area: ic; width: 72px; height: 72px; border-radius: var(--radius); display: grid; place-items: center; background: var(--md3-displaybg-primary); }
    .sec__t { grid-area: t; min-width: 0; display: grid; gap: var(--sp-4); }
    .sec__t b { color: var(--head); }
    .sec__t span { color: var(--ink); max-width: 52ch; }
    .sec .chev { grid-area: chev; transform: rotate(-90deg); color: var(--md3-on-primary-container); }
    .sec__st { grid-area: st; display: flex; gap: var(--sp-32); padding-top: var(--sp-16); border-top: 1px solid var(--line); }
    .stx { display: grid; gap: 2px; }
    .stx .v { color: var(--md3-on-secondary-container); font-variant-numeric: tabular-nums; }
    .stx.ok .v { color: var(--md3-on-surface); }
    .stx .l { color: var(--ink); }
    @media (orientation: landscape) {
      .sections { grid-template-columns: repeat(3, minmax(0, 1fr)); align-items: stretch; padding-top: var(--sp-24); }
      .sec {
        grid-template-columns: 72px 1fr; grid-template-areas: "ic chev" "t t" "st st"; grid-template-rows: auto auto 1fr;
        align-items: start; min-height: 360px;
      }
      .sec .chev { justify-self: end; }
      .sec__st { align-self: end; gap: var(--sp-24); }
    }
'''

def sec_card(href, icon, title, desc, stats):
    st = ''.join(f'<span class="stx{" ok" if ok else ""}"><span class="v t-stat-title">{v}</span><span class="l t-body-regular">{l}</span></span>' for v, l, ok in stats)
    return f'''        <a class="sec card-press" href="{href}">
          <span class="sec__ic">{svg(icon, 40, grad="g-turq")}</span>
          <span class="sec__t"><b class="t-major-title">{title}</b><span class="t-body-regular">{desc}</span></span>
          {CHEV}
          <span class="sec__st">{st}</span>
        </a>'''

home_body = f'''{GRAD_DEFS}
  <div class="app">
{STATUS_HTML}
{bar("Diet", "diet-module-flow.html", "Back to Modules", site=False)}
    <main class="main">
      <nav class="sections" aria-label="Diet sections">
{sec_card("diet-directory.html", "book", "Diet Directory", "Every diet plan with its type, meal times and where it is used.", [(N_DIETS, "Diets", False), (N_ACTIVE, "Active diets", True)])}
{sec_card("diet-by-species.html", "paw", "Diet by Species", "Diets grouped by species, with the active diet count for each.", [(N_SP, "Species", False), (N_SP_WITH, "With a diet", True)])}
{sec_card("diet-request.html", "reason-or-list", "Diet Request", "Raise diet changes and follow them from approval to the kitchen.", [(N_REQ, "Requests", False), (N_AWAIT, "Awaiting approval", False)])}
      </nav>
    </main>
  </div>'''

_old_home = ('diet-home.html', 'Diet',
     'Screen 2 - Diet home (Diet module landing). Back: diet-module-flow.html. Sections: diet-directory.html, diet-by-species.html, diet-request.html. Visual language: Antz diet tablet prototype (antz-diet.pages.dev).',
     HOME_CSS, home_body)

# ---------------------------------------------------------------- shared list JS bits
TYPE_JS = '''  var TYPE = { yearround: ['Year-round', 'time'], seasonal: ['Seasonal', 'star'], timebound: ['Time-Bound', 'calendar'], none: ['Not scheduled', 'time'] };
  var STATUS = { active: 'Active', inactive: 'Inactive', unassigned: 'Not assigned' };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function ttag(t) { return '<span class="ttag ' + t + ' t-body-medium">' + ic(TYPE[t][1], 16) + TYPE[t][0] + '</span>'; }
  function pill(s) { return '<span class="pill ' + s + ' t-body-medium">' + STATUS[s] + '</span>'; }
'''

# ---------------------------------------------------------------- diet-directory
DIR_CSS = '''    /* =========================================================
       6. DIET CARDS  (after the Antz species-page diet cards)
       portrait: 2 columns, landscape: 3 columns
       ========================================================= */
    .dgrid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--sp-12); }
    .dcard { display: flex; flex-direction: column; gap: var(--sp-12); padding: var(--sp-16) var(--sp-20); background: var(--white); border-radius: var(--radius); }
    .dcard__top { display: flex; align-items: center; justify-content: space-between; gap: var(--sp-8); }
    .dcard__t { display: grid; gap: 2px; }
    .dcard__t b { color: var(--head); }
    .dcard__t span { color: var(--ink); }
    .dcard__sp, .dcard__when { display: flex; align-items: center; gap: 6px; color: var(--md3-on-secondary-container); }
    .dcard__when { color: var(--ink); }
    .dcard__sp svg, .dcard__when svg { color: var(--md3-neutral-secondary); }
    .dcard__sp .sp { display: inline-flex; align-items: center; gap: 6px; min-width: 0; }
    .dcard__sp { justify-content: space-between; }
    .dcard__meta { display: flex; flex-wrap: wrap; align-items: center; gap: var(--sp-8); margin-top: auto; padding-top: var(--sp-12); border-top: 1px solid var(--line); color: var(--ink); }
    .mtime { display: inline-flex; align-items: center; gap: 4px; height: 28px; padding: 0 8px; border-radius: 6px; background: var(--md3-background); color: var(--md3-on-primary-container); }
    .dcard__items { flex: none; color: var(--md3-neutral-secondary); font-weight: 400; }
    mark { background: rgba(55,189,105,.22); color: inherit; border-radius: 2px; }
    @media (orientation: landscape) { .dgrid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
'''

dir_data = [{k: p[k] for k in ('code', 'name', 'spn', 'type', 'when', 'status', 'times', 'items')} for p in PLANS]

dir_body = f'''  <div class="app">
{STATUS_HTML}
{bar("Diet Directory", "diet-home.html", "Back to Diet")}
    <main class="main">
      <div class="sdtabs" role="tablist" aria-label="Diet status" id="tabs"></div>
      <div class="spband">
        <label class="spsearch">{svg("search", 20)}<span class="sr-only">Search diets</span><input id="q" class="t-body-regular" type="search" placeholder="Search by diet, code or species" autocomplete="off"></label>
        <button class="spfilter" id="fbtn" type="button" aria-pressed="false" aria-controls="chips" aria-label="Filter by diet type">{svg("filter-2", 24)}<span class="t-minor-medium" id="fn" hidden></span></button>
      </div>
      <div class="spchips" id="chips" hidden role="group" aria-label="Diet type"></div>
      <div class="list-bar"><h2 class="t-minor-medium" id="count" aria-live="polite"></h2><button class="chip t-body-medium" id="sort" type="button">{svg("sort", 18)}<span id="sortl">Code</span></button></div>
      <div class="dgrid" id="list"></div>
    </main>
  </div>'''

dir_js = icon_js(['time', 'star', 'calendar', 'paw', 'search']) + TYPE_JS + '''  var DIETS = ''' + json.dumps(dir_data, ensure_ascii=False) + ''';
  var st = { tab: 'active', q: '', types: [], sort: 'code' };
  var params = new URLSearchParams(location.search);
  if (params.get('q')) st.q = params.get('q');
  if (['active', 'inactive', 'all'].indexOf(params.get('tab')) !== -1) st.tab = params.get('tab');
  var TABS = [['active', 'Active'], ['inactive', 'Inactive'], ['all', 'All']];
  var $ = function (id) { return document.getElementById(id); };
  $('q').value = st.q;

  function hl(s) {
    if (!st.q) return esc(s);
    var i = s.toLowerCase().indexOf(st.q.toLowerCase());
    return i < 0 ? esc(s) : esc(s.slice(0, i)) + '<mark>' + esc(s.slice(i, i + st.q.length)) + '</mark>' + esc(s.slice(i + st.q.length));
  }
  function match(d) {
    var q = st.q.trim().toLowerCase();
    return (!q || (d.name + ' ' + d.code + ' diet ' + d.code + ' ' + d.spn).toLowerCase().indexOf(q) !== -1) && (!st.types.length || st.types.indexOf(d.type) !== -1);
  }
  function inTab(d, t) { return t === 'all' || (t === 'active' ? d.status === 'active' : d.status !== 'active'); }
  function card(d) {
    var times = d.times.map(function (t) { return '<span class="mtime t-body-medium">' + ic('time', 16) + t + '</span>'; }).join('');
    return '<article class="dcard">' +
      '<div class="dcard__top">' + ttag(d.type) + pill(d.status) + '</div>' +
      '<div class="dcard__t"><b class="t-minor-title">' + hl('Diet ' + d.code) + '</b><span class="t-body-regular">' + hl(d.name) + '</span></div>' +
      '<div class="dcard__sp t-body-medium"><span class="sp">' + ic('paw', 16) + hl(d.spn) + '</span><span class="dcard__items">' + d.items + (d.items === 1 ? ' item' : ' items') + '</span></div>' +
      (d.when ? '<div class="dcard__when t-body-regular">' + ic('calendar', 16) + esc(d.when) + '</div>' : '') +
      '<div class="dcard__meta" aria-label="Meal times">' + times + '</div>' +
      '</article>';
  }
  function draw() {
    var base = DIETS.filter(match);
    $('tabs').innerHTML = TABS.map(function (t) {
      var n = base.filter(function (d) { return inTab(d, t[0]); }).length;
      return '<button type="button" role="tab" class="t-minor-medium" data-tab="' + t[0] + '" aria-selected="' + (st.tab === t[0]) + '">' + t[1] + ' - ' + n + '</button>';
    }).join('');
    var list = base.filter(function (d) { return inTab(d, st.tab); });
    list.sort(function (a, b) { return st.sort === 'name' ? a.name.localeCompare(b.name) : (+a.code) - (+b.code); });
    $('count').textContent = 'Diets (' + list.length + ')';
    $('list').innerHTML = list.length ? list.map(card).join('') :
      '<div class="empty" style="grid-column:1/-1"><span class="ei">' + ic('search', 24) + '</span><b class="t-minor-title">No diets match</b><span class="t-body-regular">Try another name, code or species, or clear the filters.</span></div>';
    $('fn').hidden = !st.types.length; $('fn').textContent = st.types.length;
    $('fbtn').classList.toggle('on', st.types.length > 0);
    $('chips').innerHTML = ['yearround', 'seasonal', 'timebound'].map(function (t) {
      return '<button type="button" class="spchip t-body-medium" data-type="' + t + '" aria-pressed="' + (st.types.indexOf(t) !== -1) + '">' + ic(TYPE[t][1], 18) + TYPE[t][0] + '</button>';
    }).join('');
    $('sortl').textContent = st.sort === 'name' ? 'Name A-Z' : 'Code';
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('[data-tab]'); if (b) { st.tab = b.dataset.tab; draw(); } });
  $('q').addEventListener('input', function () { st.q = this.value; draw(); });
  $('fbtn').addEventListener('click', function () { var open = $('chips').hidden; $('chips').hidden = !open; this.setAttribute('aria-pressed', String(open)); });
  $('chips').addEventListener('click', function (e) {
    var b = e.target.closest('[data-type]'); if (!b) return;
    var i = st.types.indexOf(b.dataset.type); if (i === -1) st.types.push(b.dataset.type); else st.types.splice(i, 1); draw();
  });
  $('sort').addEventListener('click', function () { st.sort = st.sort === 'code' ? 'name' : 'code'; draw(); });
  if (params.get('filters') === '1') { $('chips').hidden = false; $('fbtn').setAttribute('aria-pressed', 'true'); }
  draw();
'''

_old_dir = ('diet-directory.html', 'Diet Directory',
     'Screen 3a - Diet Directory (all diets). Back: diet-home.html. Based on the Antz diet tablet prototype species-page diet cards, tabs and search band. ?q= search, ?tab=active|inactive|all, ?filters=1.',
     DIR_CSS, dir_body, dir_js)

# ---------------------------------------------------------------- diet-by-species
SP_CSS = '''    /* =========================================================
       6. SPECIES CARDS  (Antz .spcard) + expandable diet list
       portrait: 1 column, landscape: 2 columns
       ========================================================= */
    .spcards { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--sp-12); align-items: start; }
    .spwrap { background: var(--white); border-radius: var(--radius); overflow: hidden; }
    .spcard {
      width: 100%; display: flex; align-items: center; gap: var(--sp-16); padding: var(--sp-16) var(--sp-20); min-height: 96px; text-align: left;
      -webkit-tap-highlight-color: transparent; transition: background-color 200ms var(--ease);
    }
    @media (hover: hover) { .spcard:hover { background: #FAFCFB; } }
    .spcard:active { background: var(--md3-background); }
    .spav { width: 60px; height: 60px; flex: none; border-radius: 50%; display: grid; place-items: center; background: var(--md3-surface-variant); color: var(--ink); }
    .spcard .grow { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
    .spcard .n { color: var(--head); }
    .spcard .m { color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .spcard .c { color: var(--md3-neutral-secondary); }
    .spn { display: flex; flex-direction: column; align-items: flex-end; flex: none; }
    .spn .v { color: var(--head); font-variant-numeric: tabular-nums; }
    .spn .l { color: var(--ink); }
    .spn .gap { color: var(--md3-tertiary); }
    .spcard .chev { color: var(--md3-on-primary-container); transition: transform 200ms var(--ease); }
    .spcard[aria-expanded="true"] .chev { transform: rotate(180deg); }
    .spdiets { border-top: 1px solid var(--line); padding: var(--sp-8) var(--sp-20) var(--sp-16); display: grid; gap: 0; }
    .sprow { display: grid; grid-template-columns: 124px 1fr auto; align-items: center; gap: var(--sp-12); padding: var(--sp-12) 0; border-bottom: 1px solid var(--line); }
    .sprow:last-of-type { border-bottom: 0; }
    .sprow .ttag { justify-self: start; }
    .sprow .t { min-width: 0; display: grid; gap: 2px; }
    .sprow .t b { color: var(--head); }
    .sprow .t span { color: var(--ink); }
    .spmore { display: inline-flex; align-items: center; gap: 6px; justify-self: start; min-height: 44px; margin-top: var(--sp-4); color: var(--md3-on-surface); }
    .spmore svg { transform: rotate(-90deg); }
    .spnone { padding: var(--sp-12) 0 var(--sp-4); color: var(--ink); }
    @media (orientation: landscape) { .spcards { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
'''

sp_list = []
for s in DATA['sp']:
    ds = [{k: p[k] for k in ('code', 'name', 'type', 'when', 'status')} for p in PLANS if p['sp'] == s['id']]
    order = {'active': 0, 'inactive': 1, 'unassigned': 2}
    ds.sort(key=lambda d: (order[d['status']], int(d['code'])))
    sp_list.append({'id': s['id'], 'name': s['name'], 'sci': s['sci'], 'cls': s['cls'], 'animals': s['animals'], 'active': s['active'], 'none': s['none'], 'diets': ds})
CLASSES = []
for s in DATA['sp']:
    if s['cls'] not in CLASSES: CLASSES.append(s['cls'])

sp_body = f'''  <div class="app">
{STATUS_HTML}
{bar("Diet by Species", "diet-home.html", "Back to Diet")}
    <main class="main">
      <div class="sdtabs" role="tablist" aria-label="Species" id="tabs"></div>
      <div class="spband">
        <label class="spsearch">{svg("search", 20)}<span class="sr-only">Search species</span><input id="q" class="t-body-regular" type="search" placeholder="Search" autocomplete="off"></label>
        <button class="spfilter" id="fbtn" type="button" aria-pressed="false" aria-controls="chips" aria-label="Filter by class">{svg("filter-2", 24)}<span class="t-minor-medium" id="fn" hidden></span></button>
      </div>
      <div class="spchips" id="chips" hidden role="group" aria-label="Class"></div>
      <div class="list-bar"><h2 class="t-minor-medium" id="count" aria-live="polite"></h2><button class="chip t-body-medium" id="sort" type="button">{svg("sort", 18)}<span id="sortl">Most diets</span></button></div>
      <div class="spcards" id="list"></div>
    </main>
  </div>'''

sp_js = icon_js(['time', 'star', 'calendar', 'search', 'dropdown', 'paw']) + TYPE_JS + '''  var SPECIES = ''' + json.dumps(sp_list, ensure_ascii=False) + ''';
  var CLASSES = ''' + json.dumps(CLASSES) + ''';
  var st = { tab: 'with', q: '', cls: [], sort: 'count', open: {} };
  var params = new URLSearchParams(location.search);
  if (params.get('open')) params.get('open').split(',').forEach(function (k) { st.open[k] = true; });
  var TABS = [['with', 'Species with diet'], ['without', 'Species without diet'], ['all', 'All species']];
  var $ = function (id) { return document.getElementById(id); };
  function initials(n) { return n.split(/[\\s-]+/).filter(Boolean).slice(0, 2).map(function (w) { return w[0]; }).join('').toUpperCase(); }
  function match(s) {
    var q = st.q.trim().toLowerCase();
    return (!q || (s.name + ' ' + s.sci).toLowerCase().indexOf(q) !== -1) && (!st.cls.length || st.cls.indexOf(s.cls) !== -1);
  }
  function inTab(s, t) { return t === 'all' || (t === 'with' ? !s.none : s.none); }
  function row(d) {
    return '<div class="sprow">' + ttag(d.type) + '<span class="t"><b class="t-body-title">Diet ' + d.code + '</b><span class="t-body-regular">' + esc(d.name) + (d.when ? ' • ' + esc(d.when) : '') + '</span></span>' + pill(d.status) + '</div>';
  }
  function card(s) {
    var open = !!st.open[s.id];
    var right = s.none ? '<span class="spn"><span class="gap t-body-medium">No diet yet</span></span>'
      : '<span class="spn"><span class="v t-stat-title">' + s.active + '</span><span class="l t-body-regular">' + (s.active === 1 ? 'Active diet' : 'Active diets') + '</span></span>';
    var panel = '';
    if (open) {
      panel = '<div class="spdiets" id="p-' + s.id + '">' + (s.diets.length ? s.diets.map(row).join('') +
        '<a class="spmore t-body-medium" href="diet-directory.html?tab=all&q=' + encodeURIComponent(s.name) + '">Open in Diet Directory' + ic('dropdown', 20) + '</a>'
        : '<p class="spnone t-body-regular">No diet is set for this species yet. Raise a diet request to add one.</p><a class="spmore t-body-medium" href="diet-request.html">Go to Diet Request' + ic('dropdown', 20) + '</a>') + '</div>';
    }
    return '<div class="spwrap"><button class="spcard" type="button" data-sp="' + s.id + '" aria-expanded="' + open + '" aria-controls="p-' + s.id + '">' +
      '<span class="spav t-minor-title" aria-hidden="true">' + initials(s.name) + '</span>' +
      '<span class="grow"><span class="n t-minor-title">' + esc(s.name) + '</span><span class="m t-minor-italic">' + esc(s.sci) + '</span>' +
      '<span class="c t-body-regular">' + esc(s.cls) + (s.animals ? ' • ' + s.animals + (s.animals === 1 ? ' animal' : ' animals') : '') + '</span></span>' +
      right + '<span class="chev">' + ic('dropdown', 24) + '</span></button>' + panel + '</div>';
  }
  function draw() {
    var base = SPECIES.filter(match);
    $('tabs').innerHTML = TABS.map(function (t) {
      var n = base.filter(function (s) { return inTab(s, t[0]); }).length;
      return '<button type="button" role="tab" class="t-minor-medium" data-tab="' + t[0] + '" aria-selected="' + (st.tab === t[0]) + '">' + t[1] + ' - ' + n + '</button>';
    }).join('');
    var list = base.filter(function (s) { return inTab(s, st.tab); });
    list.sort(function (a, b) { return st.sort === 'name' ? a.name.localeCompare(b.name) : (b.active - a.active) || a.name.localeCompare(b.name); });
    $('count').textContent = 'Species (' + list.length + ')';
    $('list').innerHTML = list.length ? list.map(card).join('') :
      '<div class="empty" style="grid-column:1/-1"><span class="ei">' + ic('search', 24) + '</span><b class="t-minor-title">No species match</b><span class="t-body-regular">Try a common or scientific name, or clear the filters.</span></div>';
    $('fn').hidden = !st.cls.length; $('fn').textContent = st.cls.length;
    $('fbtn').classList.toggle('on', st.cls.length > 0);
    $('chips').innerHTML = CLASSES.map(function (c) { return '<button type="button" class="spchip t-body-medium" data-cls="' + c + '" aria-pressed="' + (st.cls.indexOf(c) !== -1) + '">' + c + '</button>'; }).join('');
    $('sortl').textContent = st.sort === 'name' ? 'Name A-Z' : 'Most diets';
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('[data-tab]'); if (b) { st.tab = b.dataset.tab; draw(); } });
  $('q').addEventListener('input', function () { st.q = this.value; draw(); });
  $('fbtn').addEventListener('click', function () { var open = $('chips').hidden; $('chips').hidden = !open; this.setAttribute('aria-pressed', String(open)); });
  $('chips').addEventListener('click', function (e) {
    var b = e.target.closest('[data-cls]'); if (!b) return;
    var i = st.cls.indexOf(b.dataset.cls); if (i === -1) st.cls.push(b.dataset.cls); else st.cls.splice(i, 1); draw();
  });
  $('sort').addEventListener('click', function () { st.sort = st.sort === 'count' ? 'name' : 'count'; draw(); });
  $('list').addEventListener('click', function (e) { var b = e.target.closest('[data-sp]'); if (b) { st.open[b.dataset.sp] = !st.open[b.dataset.sp]; draw(); } });
  draw();
'''

page('diet-by-species.html', 'Diet by Species',
     'SUPERSEDED by the Diet by Species tab in diet-home.html (diet-home.html#species). Kept as the earlier standalone version. Screen 3b - Diet by Species. Back: diet-home.html. Based on the Antz diet tablet prototype Species Diet screen (#/diets). Tap a species to list its diets. ?open=LI,BT expands species.',
     SP_CSS, sp_body, sp_js)

# ---------------------------------------------------------------- diet-request
RQ_CSS = '''    /* =========================================================
       6. COUNT TABS  (Antz .ctabs: count over label)
       ========================================================= */
    .ctabs { display: flex; margin: 0 calc(-1 * var(--sp-16)); background: var(--white); overflow-x: auto; scrollbar-width: none; }
    .ctab {
      flex: 1 0 auto; min-width: 112px; display: flex; flex-direction: column; align-items: center; gap: 2px;
      padding: var(--sp-8) var(--sp-12); border-bottom: 3px solid transparent; color: var(--md3-on-surface-variant);
      transition: border-color 200ms var(--ease);
    }
    .ctab .c { color: var(--md3-on-surface-variant); font-variant-numeric: tabular-nums; }
    .ctab[aria-selected="true"] { border-bottom-color: var(--md3-primary); }
    .ctab[aria-selected="true"] .c { color: var(--md3-primary); }

    /* =========================================================
       7. REQUEST CARDS  (Antz .hdcard: id, species, where, priority ribbon, body, status band)
       portrait: 1 column, landscape: 2 columns
       ========================================================= */
    .rqcards { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--sp-16); align-items: start; }
    .hdcard { display: flex; flex-direction: column; border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); overflow: hidden; }
    .hd-top { display: flex; align-items: flex-start; gap: var(--sp-12); padding: var(--sp-12) 0 var(--sp-12) var(--sp-16); border-bottom: 1px solid var(--line); }
    .hd-top .grow { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 2px; }
    .hd-id { color: var(--md3-on-secondary-container); }
    .hd-cat { color: var(--md3-neutral-secondary); }
    .hd-where { color: var(--md3-on-surface-variant); }
    .ribbon {
      flex: none; min-width: 56px; height: 40px; padding: 0 var(--sp-12) 0 var(--sp-20); display: grid; place-items: center;
      color: var(--white); clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 12px 50%); margin-top: var(--sp-4);
      font-size: 20px; font-weight: 700; letter-spacing: 1px;
    }
    .ribbon.low { background: var(--md3-secondary); }
    .ribbon.medium { background: var(--md3-secondary-dark); }
    .ribbon.high { background: var(--md3-tertiary); }
    .hd-body { display: flex; flex-direction: column; gap: var(--sp-8); padding: var(--sp-12) var(--sp-16); }
    .hd-title { color: var(--head); }
    .hd-text { color: var(--md3-on-surface-variant); display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
    .hd-by { color: var(--md3-on-surface-variant); }
    .hd-by b { color: var(--md3-on-secondary-container); }
    .hdcard.struck .hd-title, .hdcard.struck .hd-text { text-decoration: line-through; }
    .hd-band { display: flex; align-items: center; gap: var(--sp-8); margin: 0 2px 2px; padding: var(--sp-8) 14px; min-height: 48px; border-radius: 0 0 6px 6px; }
    .hd-band.wait { background: var(--moderate-a10); color: var(--md3-on-tertiary-container); }
    .hd-band.wait svg { color: var(--md3-moderate-secondary); }
    .hd-band.ok { background: var(--primary-a10); color: var(--md3-on-surface); }
    .hd-band.ok svg { color: var(--md3-primary); }
    .hd-band.bad { background: var(--error-a5); color: var(--md3-error); }
    .list-bar { margin-top: var(--sp-16); }
    @media (orientation: landscape) {
      .rqcards { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .hd-title { font-size: 18px; }
    }
'''

rq_body = f'''  <div class="app">
{STATUS_HTML}
{bar("Diet Request", "diet-home.html", "Back to Diet")}
    <main class="main">
      <nav class="ctabs" role="tablist" aria-label="Request status" id="tabs"></nav>
      <div class="list-bar"><h2 class="t-minor-medium" id="count" aria-live="polite"></h2><button class="chip t-body-medium" id="sort" type="button">{svg("filter-2", 18)}<span id="sortl">Priority</span></button></div>
      <div class="rqcards" id="list"></div>
    </main>
  </div>'''

rq_js = icon_js(['time', 'just-tick-mark', 'pencil', 'timer', 'close', 'reason-or-list']) + '''  var REQS = ''' + json.dumps(REQS, ensure_ascii=False) + ''';
  var PRIO = { high: ['!!!', 'High priority', 0], medium: ['!!', 'Medium priority', 1], low: ['!', 'Low priority', 2] };
  var TABS = [['awaiting', 'Awaiting approval'], ['approved', 'Approved'], ['progress', 'In Progress'], ['completed', 'Completed'], ['all', 'All']];
  var params = new URLSearchParams(location.search);
  var st = { tab: TABS.some(function (t) { return t[0] === params.get('tab'); }) ? params.get('tab') : 'all', sort: params.get('sort') === 'recent' ? 'recent' : 'priority' };
  var $ = function (id) { return document.getElementById(id); };
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function inTab(r, t) { return t === 'all' || r.group === t; }
  function card(r) {
    var p = PRIO[r.prio];
    return '<article class="hdcard' + (r.label === 'Cancelled' ? ' struck' : '') + '">' +
      '<div class="hd-top"><span class="grow"><span class="hd-id t-minor-title">' + r.id + '</span><span class="hd-cat t-body-medium">' + esc(r.sp) + '</span><span class="hd-where t-body-regular">' + esc(r.where) + '</span></span>' +
      '<span class="ribbon ' + r.prio + '" title="' + p[1] + '" aria-label="' + p[1] + '">' + p[0] + '</span></div>' +
      '<div class="hd-body"><span class="hd-title t-medium-medium">' + esc(r.title) + '</span><span class="hd-text t-body-regular">' + esc(r.text) + '</span>' +
      '<span class="hd-by t-body-regular"><b class="t-body-title">Carol Steve</b> • ' + r.date + '</span></div>' +
      '<div class="hd-band ' + r.tone + ' t-minor-medium">' + ic(r.icon, 20) + esc(r.label) + '</div></article>';
  }
  function draw() {
    $('tabs').innerHTML = TABS.map(function (t) {
      var n = REQS.filter(function (r) { return inTab(r, t[0]); }).length;
      return '<button type="button" role="tab" class="ctab" data-tab="' + t[0] + '" aria-selected="' + (st.tab === t[0]) + '"><span class="c t-medium-medium">' + n + '</span><span class="l t-body-regular">' + t[1] + '</span></button>';
    }).join('');
    var list = REQS.filter(function (r) { return inTab(r, st.tab); });
    list.sort(function (a, b) { return st.sort === 'recent' ? b.iso.localeCompare(a.iso) : (PRIO[a.prio][2] - PRIO[b.prio][2]) || b.iso.localeCompare(a.iso); });
    $('count').textContent = 'Requests (' + list.length + ')';
    $('list').innerHTML = list.length ? list.map(card).join('') :
      '<div class="empty" style="grid-column:1/-1"><span class="ei">' + ic('reason-or-list', 24) + '</span><b class="t-minor-title">No requests</b></div>';
    $('sortl').textContent = st.sort === 'recent' ? 'Recent' : 'Priority';
  }
  $('tabs').addEventListener('click', function (e) { var b = e.target.closest('[data-tab]'); if (b) { st.tab = b.dataset.tab; draw(); } });
  $('sort').addEventListener('click', function () { st.sort = st.sort === 'priority' ? 'recent' : 'priority'; draw(); });
  draw();
'''

page('diet-request.html', 'Diet Request',
     'SUPERSEDED by the Diet Request tab in diet-home.html (diet-home.html#request). Kept as the earlier standalone version. Screen 3c - Diet Request. Back: diet-home.html. Based on the Antz diet tablet prototype Requests screen (#/requests). ?tab=awaiting|approved|progress|completed|all, ?sort=recent.',
     RQ_CSS, rq_body, rq_js)
