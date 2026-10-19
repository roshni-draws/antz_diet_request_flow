# home2.py: exec'd by build.py after pages.py (shares globals).
# Tabbed diet-home.html (Directory from the V2 tab prototype data, Species + Request from the site),
# plus the standalone diet-directory.html rebuilt on the same directory module.

# ---------------------------------------------------------------- V2 directory data (dashes made plain)
_raw = open(os.path.join(HERE, 'v2dir.json')).read()
_raw = _raw.replace(' – ', ' to ').replace('–', '-').replace('—', '-')
V2DIR = json.loads(_raw)
_sites = []
for d in V2DIR['diets']:
    for s in d.get('sites') or []:
        if s not in _sites: _sites.append(s)
V2DIR['sites'] = (V2DIR.get('sites') or []) + [s for s in _sites if s not in (V2DIR.get('sites') or [])]
N_DIR = len(V2DIR['diets'])

ALL_ICONS = ['back', 'search', 'filter-2', 'dropdown', 'location-icon', 'time', 'calendar', 'star', 'paw', 'sort', 'close',
             'just-tick-mark', 'pencil', 'timer', 'reason-or-list', 'alert', 'approved', 'info', 'history', 'download',
             'menu-vertical', 'add', 'transfer', 'grid', 'list', 'image', 'user', 'notes-new', 'checkbox-checked', 'checkbox-unchecked', 'book']

# ---------------------------------------------------------------- CSS
HEAD_CSS = '''    /* =========================================================
       6. HEADER CARD + MAIN TABS  (Antz Species Diet header:
       app bar, hairline, three equal tabs with a 3px underline)
       ========================================================= */
    .head { background: var(--white); position: relative; z-index: 2; }
    .head .bar { border-bottom: 1px solid var(--line); }
    .mtabs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); background: var(--white); }
    .mtab {
      height: 56px; display: flex; align-items: center; justify-content: center; padding: 0 var(--sp-8);
      color: var(--md3-on-surface-variant); border-bottom: 3px solid transparent; white-space: nowrap;
      transition: color 200ms var(--ease), border-color 200ms var(--ease), background-color 200ms var(--ease);
    }
    @media (hover: hover) { .mtab:hover { background: #FAFCFB; } }
    .mtab[aria-selected="true"] { color: var(--md3-primary); border-bottom-color: var(--md3-primary); }
    .pane[hidden] { display: none !important; }

    /* =========================================================
       7. SEGMENTS  (secondary filter row inside a tab body:
       Antz .spchip segmented chips, dark teal when on)
       ========================================================= */
    .segrow { display: flex; gap: var(--sp-8); padding: var(--sp-16) 0 0; overflow-x: auto; scrollbar-width: none; }
    .segrow::-webkit-scrollbar { display: none; }
    .segrow .spchip { flex: none; }
    .spchip .n { font-variant-numeric: tabular-nums; opacity: .8; }
    /* species coverage segments: full-width pill track, sub-level of the main tabs */
    .segwrap { margin: 0 calc(-1 * var(--sp-16)); padding: var(--sp-12) var(--sp-16); background: var(--white); border-top: 1px solid var(--line); }
    .seg3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 4px; padding: 4px; border-radius: 12px; background: var(--neutral05); }
    .seg3 button {
      min-height: 44px; padding: 0 var(--sp-8); border-radius: 9px; color: var(--md3-on-surface-variant); white-space: nowrap;
      transition: background-color 200ms var(--ease), color 200ms var(--ease), box-shadow 200ms var(--ease);
    }
    .seg3 button[aria-selected="true"] { background: var(--white); color: var(--md3-on-primary-container); font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,.12); }
    @media (hover: hover) { .seg3 button[aria-selected="false"]:hover { color: var(--head); } }
    .spgroups { display: grid; gap: var(--sp-8); }
    .spgroup__h { color: var(--md3-on-secondary-container); margin: var(--sp-8) 0 var(--sp-12); }
    .spgroup + .spgroup .spgroup__h { margin-top: var(--sp-16); }
    .spgroup__none { color: var(--md3-neutral-secondary); padding: var(--sp-12) 0; }
    .rowlabel { color: var(--md3-neutral-secondary); flex: none; align-self: center; min-width: 92px; }
'''

DIR_CSS2 = '''    /* =========================================================
       8. DIRECTORY  (V2 tab prototype content in Antz app style)
       landscape: list 40% + detail 60%; portrait: list, detail opens as a panel
       ========================================================= */
    .fchips { display: flex; flex-wrap: wrap; gap: var(--sp-8); padding-top: var(--sp-12); }
    .fchip {
      display: inline-flex; align-items: center; gap: var(--sp-8); height: 40px; padding: 0 var(--sp-12) 0 var(--sp-16);
      border: 1px solid var(--md3-outline-variant); border-radius: 12px; background: var(--white); color: var(--md3-on-surface);
    }
    .linkbtn { display: inline-flex; align-items: center; gap: 6px; min-height: 40px; padding: 0 var(--sp-8); border-radius: 8px; color: var(--md3-on-surface); }
    .linkbtn[aria-disabled="true"] { color: var(--md3-neutral-secondary); }
    @media (hover: hover) { .linkbtn:hover { background: var(--md3-displaybg-primary); } }
    .dd-split { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--sp-16); align-items: start; }
    .dd-detail { display: none; }
    .ddlist { display: grid; gap: var(--sp-8); }
    .ddrow {
      width: 100%; display: flex; align-items: center; gap: var(--sp-12); padding: var(--sp-12) var(--sp-16); min-height: 76px;
      text-align: left; background: var(--white); border-radius: var(--radius); box-shadow: inset 0 0 0 2px transparent;
      -webkit-tap-highlight-color: transparent; transition: box-shadow 200ms var(--ease), transform 120ms var(--ease);
    }
    .ddrow:active { transform: scale(.99); }
    .ddrow[aria-current="true"] { box-shadow: inset 0 0 0 2px var(--md3-primary); }
    .ddrow__t { flex: 1; min-width: 0; display: grid; gap: 4px; }
    .ddrow__t b { color: var(--head); }
    .ddrow__t b.off { color: var(--md3-neutral-secondary); }
    .ddrow__t .lb { color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .tags { display: flex; flex-wrap: wrap; gap: 6px; }
    .tag { display: inline-flex; align-items: center; gap: 4px; height: 24px; padding: 0 8px; border-radius: 4px; white-space: nowrap; font-size: 12px; font-weight: 600; }
    .tag.grey { color: var(--md3-neutral-secondary); background: var(--neutral05); }
    .tag.green { color: var(--md3-on-surface); background: var(--md3-on-background); }
    .tag.orange { color: #C2401F; background: var(--tertiary-a10); }
    .tag.blue { color: #00799A; background: var(--add-primary-a10); }
    .tag.teal { color: var(--md3-on-primary-container); background: var(--md3-displaybg-primary); }
    .tag.red { color: var(--md3-error); background: var(--error-a5); }
    .ddrow .chev { transform: rotate(-90deg); color: var(--md3-on-primary-container); }

    .dpane { background: var(--white); border-radius: var(--radius); padding: var(--sp-20); display: grid; gap: var(--sp-16); }
    .dpane + .dpane { margin-top: var(--sp-16); }
    .dp-head { display: flex; align-items: flex-start; gap: var(--sp-12); }
    .dp-head .grow { flex: 1; min-width: 0; display: grid; gap: 4px; }
    .dp-id { display: flex; align-items: center; flex-wrap: wrap; gap: var(--sp-8); }
    .dp-id b { color: var(--md3-on-secondary-container); }
    .dp-acts { display: flex; gap: 4px; flex: none; }
    .win { display: inline-flex; align-items: center; gap: 6px; height: 28px; padding: 0 10px; border-radius: 6px; font-size: 14px; font-weight: 500; }
    .win.current { color: var(--md3-on-surface); background: var(--md3-on-background); }
    .win.off { color: #00799A; background: var(--add-primary-a10); }
    .win.inactive { color: var(--md3-neutral-secondary); background: var(--neutral05); }
    .cert { display: flex; align-items: center; gap: var(--sp-12); padding: var(--sp-12); border-radius: var(--radius); background: var(--md3-background); }
    .cert.none { background: var(--error-a5); }
    .cert__ic { width: 40px; height: 40px; border-radius: 8px; display: grid; place-items: center; flex: none; background: var(--white); color: var(--md3-primary); }
    .cert.none .cert__ic { color: var(--md3-error); }
    .cert__t { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .cert__t b { color: var(--head); }
    .dseg { display: inline-flex; padding: 4px; gap: 4px; border-radius: 10px; border: 1px solid var(--md3-outline-variant); justify-self: start; }
    .dseg button { height: 36px; padding: 0 var(--sp-16); border-radius: 6px; color: var(--ink); display: inline-flex; align-items: center; gap: 6px; }
    .dseg button[aria-pressed="true"] { background: var(--md3-on-primary-container); color: var(--white); }

    /* items table (Antz diet pane: TIME / DAY / ITEM / DAILY AMT) */
    .dtab-wrap { border: 1px solid var(--md3-surface-variant); border-radius: var(--radius); overflow: hidden; overflow-x: auto; }
    .dtab { width: 100%; border-collapse: collapse; }
    .dtab th { background: var(--md3-surface-variant); color: var(--ink); text-align: left; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; padding: 10px 12px; }
    .dtab th.amt, .dtab td.amt { text-align: right; }
    .dtab td { padding: 12px; vertical-align: top; border-top: 1px solid var(--md3-surface-variant); color: var(--head); }
    .dtab td + td { border-left: 1px solid var(--md3-surface-variant); }
    .dtab td.time { font-weight: 600; white-space: nowrap; }
    .dtab td.day { color: var(--ink); white-space: nowrap; }
    .dtab td.amt { font-weight: 600; white-space: nowrap; }
    .it-n { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; font-weight: 600; }
    .it-k { font-size: 11px; font-weight: 600; letter-spacing: .04em; color: var(--ink); background: var(--neutral05); border-radius: 999px; padding: 2px 8px; }
    .it-p { color: var(--ink); font-style: italic; }
    .it-parts { margin: 6px 0 0; padding-left: 10px; border-left: 2px solid var(--md3-surface-variant); display: grid; gap: 2px; color: var(--ink); }
    .it-parts em { color: var(--md3-neutral-secondary); }
    .it-alt { color: var(--ink); margin-top: 4px; }
    .it-alt b { color: var(--head); font-weight: 500; }
    .it-ex { color: var(--md3-neutral-secondary); margin-top: 4px; }

    /* nutrition */
    .nut { display: grid; gap: var(--sp-16); }
    .nut__help { display: flex; gap: 8px; align-items: center; color: var(--ink); }
    .nut__sec h4 { color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; margin-bottom: 4px; }
    .nut__row { display: flex; justify-content: space-between; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--line); }
    .nut__row b { color: var(--head); font-variant-numeric: tabular-nums; }
    .nut__row b.zero { color: var(--md3-neutral-secondary); font-weight: 500; }
    .nut__row small { color: var(--md3-neutral-secondary); font-weight: 400; }

    /* notes, remark, change reason */
    .kv { display: grid; grid-template-columns: max-content 1fr; gap: 6px 16px; }
    .kv dt { color: var(--md3-neutral-secondary); }
    .kv dd { color: var(--head); }
    .sub h3 { color: var(--head); margin-bottom: 8px; }
    .remark { display: flex; gap: 10px; padding: var(--sp-12) var(--sp-16); border-radius: var(--radius); background: #FCF4AE; color: var(--head); }
    .remark svg { color: #8A6D00; }
    .reason { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; color: var(--ink); }

    /* fed to species */
    .fed-h { display: flex; align-items: center; flex-wrap: wrap; gap: var(--sp-12); }
    .fed-h h3 { flex: 1; color: var(--head); }
    .fed-tools { display: flex; align-items: center; flex-wrap: wrap; gap: var(--sp-8); }
    .fed-tools .hint { flex: 1; color: var(--md3-neutral-secondary); min-width: 180px; }
    .sgrid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--sp-12); }
    .scard { display: flex; gap: var(--sp-12); align-items: flex-start; padding: var(--sp-12); border: 1px solid var(--md3-surface-variant); border-radius: var(--radius); }
    .scard.sel { border-color: var(--md3-primary); background: rgba(55,189,105,.05); }
    .scard__ic { width: 40px; height: 40px; flex: none; border-radius: 50%; display: grid; place-items: center; background: var(--md3-surface-variant); color: var(--ink); }
    .scard__t { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .scard__t b { color: var(--head); }
    .scard__t i { color: var(--ink); }
    .scard__m { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; color: var(--md3-neutral-secondary); margin-top: 4px; }
    .ck { width: 44px; height: 44px; margin: -10px -6px -10px -10px; display: grid; place-items: center; color: var(--md3-on-primary-container); flex: none; }
    .slist { display: grid; }
    .slist .scard { border: 0; border-bottom: 1px solid var(--line); border-radius: 0; align-items: center; }

    @media (orientation: landscape) {
      .dd-split { grid-template-columns: minmax(0, 2fr) minmax(0, 3fr); }
      .dd-detail { display: block; position: sticky; top: var(--sp-16); max-height: calc(100dvh - var(--status-h) - 138px - 32px); overflow-y: auto; border-radius: var(--radius); }
      .sgrid { grid-template-columns: minmax(0, 1fr); }
    }

    /* =========================================================
       9. PANEL, SHEET, TOAST  (portrait diet detail, filters, feedback)
       ========================================================= */
    .dpanel { position: fixed; inset: var(--status-h) 0 0 0; z-index: 20; display: grid; grid-template-rows: auto 1fr; background: var(--md3-background);
      transform: translateX(0); transition: transform 260ms var(--ease); }
    .dpanel[hidden] { display: none; }
    .dpanel__body { overflow-y: auto; padding: var(--sp-16) var(--sp-16) var(--sp-32); }
    .scrim { position: fixed; inset: 0; z-index: 30; background: rgba(0,0,0,.4); display: flex; align-items: flex-end; justify-content: center; }
    .scrim[hidden] { display: none; }
    .sheet { width: min(640px, 100%); max-height: 86dvh; overflow-y: auto; background: var(--white); border-radius: 16px 16px 0 0; padding: var(--sp-8) var(--sp-24) var(--sp-24); display: grid; gap: var(--sp-20); }
    .sheet .grab { width: 40px; height: 4px; border-radius: 2px; background: var(--md3-outline-variant); justify-self: center; }
    .sheet__h { display: flex; align-items: center; justify-content: space-between; }
    .sheet__h h2 { color: var(--head); }
    .sheet__g { display: grid; gap: var(--sp-12); }
    .sheet__g h3 { color: var(--ink); }
    .sheet__g .chips { display: flex; flex-wrap: wrap; gap: var(--sp-8); }
    .sheet__f { display: flex; gap: var(--sp-12); }
    .btn { flex: 1; height: 48px; border-radius: 8px; display: inline-flex; align-items: center; justify-content: center; gap: 8px; font-weight: 600; font-size: 16px; }
    .btn.pri { background: var(--md3-primary); color: var(--white); }
    .btn.sec { border: 1px solid var(--md3-outline-variant); color: var(--md3-on-primary-container); }
    .btn:active { transform: scale(.98); }
    .toast { position: fixed; left: 50%; bottom: 32px; z-index: 40; transform: translate(-50%, 16px); opacity: 0; pointer-events: none;
      max-width: calc(100% - 32px); padding: 12px 20px; border-radius: 8px; background: var(--md3-on-primary-container); color: var(--white);
      transition: opacity 200ms var(--ease), transform 200ms var(--ease); }
    .toast.on { opacity: 1; transform: translate(-50%, 0); }
'''

def _strip_heading(css):
    return css

SP_CSS2 = SP_CSS.replace('6. SPECIES CARDS', '10. SPECIES CARDS')
RQ_CSS2 = RQ_CSS[RQ_CSS.index('    /* =========================================================\n       7. REQUEST CARDS'):].replace('7. REQUEST CARDS', '11. REQUEST CARDS')

# ---------------------------------------------------------------- JS
HELPERS_JS = icon_js(ALL_ICONS) + '''  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function plural(n, a, b) { return n + ' ' + (n === 1 ? a : (b || a + 's')); }
  var LAND = window.matchMedia('(orientation: landscape)');
  var toastT;
  function toast(msg) { var t = document.getElementById('toast'); t.textContent = msg; t.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove('on'); }, 2400); }
  var TYPE = { yearround: ['Year-round', 'time'], seasonal: ['Seasonal', 'star'], timebound: ['Time-Bound', 'calendar'], none: ['Not scheduled', 'time'] };
  var STATUS = { active: 'Active', inactive: 'Inactive', unassigned: 'Not assigned' };
  function ttag(t) { return '<span class="ttag ' + t + ' t-body-medium">' + ic(TYPE[t][1], 16) + TYPE[t][0] + '</span>'; }
  function pill(s) { return '<span class="pill ' + s + ' t-body-medium">' + STATUS[s] + '</span>'; }
'''

DIR_JS = '''  /* ---------------- Diet Directory (V2 tab prototype: diet/directory.html + directory.js + directory.data.js) ---------------- */
  var DIRD = ''' + json.dumps(V2DIR, ensure_ascii=False).replace('</', '<\\/') + ''';
  function DirModule(root, opt) {
    var DIETS = DIRD.diets, PREFIX = opt.prefix;
    var CLS = [['all', 'All'], ['mammalia', 'Mammalia'], ['aves', 'Aves'], ['reptilia', 'Reptilia'], ['other', 'Other']];
    var DEF = { site: '', cert: '', upd: '' };
    var UPD = { pending: 'Needs verification', approved: 'Update approved', any: 'Any updated diet' };
    var NUT = [['Macros', [['energy', 'Energy', 'kcal', 1], ['protein', 'Protein', 'g', 1], ['fat', 'Fat', 'g', 1], ['carbohydrate', 'Carbohydrate', 'g', 1], ['fiber', 'Fiber', 'g'], ['moisture', 'Moisture', '%']]],
      ['Minerals', [['calcium', 'Calcium', 'mg'], ['phosphorus', 'Phosphorus', 'mg']]],
      ['Vitamins', [['vitaminA', 'Vitamin A', 'IU'], ['vitaminD', 'Vitamin D', 'IU'], ['vitaminE', 'Vitamin E', 'mg'], ['vitaminC', 'Vitamin C', 'mg']]]];
    var st = { q: '', ver: '', cls: 'all', f: { site: '', cert: '', upd: '' }, sel: DIRD.selectedId || DIETS[0].id, tab: 'items', view: 'cards', picked: {}, panel: null };
    function find(id) { for (var i = 0; i < DIETS.length; i++) if (DIETS[i].id === id) return DIETS[i]; return null; }
    function label(d) { if (d.listLabel) return d.listLabel; var sp = d.species || []; return sp.length ? sp[0].name + (sp.length > 1 ? ' +' + (sp.length - 1) : '') : 'No species'; }
    function matches(d, skip) {
      var q = st.q.trim().toLowerCase(), qid = q.replace(/^d-?/, '');
      if (skip !== 'cls' && st.cls !== 'all' && !(d.species || []).some(function (s) { return s.cls === st.cls; })) return false;
      if (st.f.site && (d.sites || []).indexOf(st.f.site) === -1) return false;
      if (skip !== 'ver' && st.ver === 'verified' && !d.verified) return false;
      if (skip !== 'ver' && st.ver === 'unverified' && d.verified) return false;
      if (st.f.cert === 'certified' && !d.dietitian) return false;
      if (st.f.cert === 'uncertified' && d.dietitian) return false;
      if (st.f.upd === 'pending' && d.update !== 'pending') return false;
      if (st.f.upd === 'approved' && d.update !== 'approved') return false;
      if (st.f.upd === 'any' && d.update !== 'pending' && d.update !== 'approved') return false;
      if (q) {
        var idHit = d.id.toLowerCase().indexOf(q) !== -1 || (qid && d.id.toLowerCase().replace('d-', '').indexOf(qid) === 0);
        var spHit = (d.species || []).some(function (s) { return (s.name || '').toLowerCase().indexOf(q) !== -1 || (s.sci || '').toLowerCase().indexOf(q) !== -1; });
        if (!idHit && !spHit) return false;
      }
      return true;
    }
    function count(key, val) { var s = st[key]; st[key] = val; var n = DIETS.filter(function (d) { return matches(d); }).length; st[key] = s; return n; }
    function nFilters() { return (st.f.site ? 1 : 0) + (st.f.cert ? 1 : 0) + (st.f.upd ? 1 : 0); }

    root.innerHTML =
      '<div class="spband"><label class="spsearch">' + ic('search', 20) + '<span class="sr-only">Search diets</span><input class="t-body-regular" type="search" data-q placeholder="Search Diet ID or species" autocomplete="off"></label>' +
      '<button class="spfilter" type="button" data-filters aria-label="Filters">' + ic('filter-2', 24) + '<span class="t-minor-medium" data-fn hidden></span></button></div>' +
      '<div class="segrow" role="group" aria-label="Verification" data-ver></div>' +
      '<div class="segrow" role="group" aria-label="Animal class" data-cls></div>' +
      '<div class="fchips" data-active hidden></div>' +
      '<div class="list-bar"><h2 class="t-minor-medium" data-count aria-live="polite"></h2><span class="t-body-regular" style="color:var(--md3-neutral-secondary)">Total: ' + DIETS.length + '</span></div>' +
      '<div class="dd-split"><div class="ddlist" data-list></div><div class="dd-detail" data-detail></div></div>';
    var $ = function (sel) { return root.querySelector(sel); };

    function drawFilters() {
      $('[data-ver]').innerHTML = '<span class="rowlabel t-body-medium">Verification</span>' + [['', 'All'], ['verified', 'Verified'], ['unverified', 'Unverified']].map(function (v) {
        return '<button type="button" class="spchip t-body-medium" data-v="' + v[0] + '" aria-pressed="' + (st.ver === v[0]) + '">' + v[1] + ' <span class="n">' + count('ver', v[0]) + '</span></button>';
      }).join('');
      $('[data-cls]').innerHTML = '<span class="rowlabel t-body-medium">Class</span>' + CLS.map(function (c) {
        return '<button type="button" class="spchip t-body-medium" data-c="' + c[0] + '" aria-pressed="' + (st.cls === c[0]) + '">' + c[1] + ' <span class="n">' + count('cls', c[0]) + '</span></button>';
      }).join('');
      var act = [];
      if (st.f.site) act.push(['site', 'Site: ' + st.f.site]);
      if (st.f.cert) act.push(['cert', st.f.cert === 'certified' ? 'Certified' : 'Uncertified']);
      if (st.f.upd) act.push(['upd', UPD[st.f.upd]]);
      var a = $('[data-active]'); a.hidden = !act.length;
      a.innerHTML = act.map(function (x) { return '<button type="button" class="fchip t-body-medium" data-unf="' + x[0] + '" aria-label="Remove ' + esc(x[1]) + '">' + esc(x[1]) + ic('close', 20) + '</button>'; }).join('') +
        (act.length > 1 ? '<button type="button" class="linkbtn t-body-medium" data-unf="*">Clear all</button>' : '');
      var n = nFilters(), fb = $('[data-filters]'), fn = $('[data-fn]');
      fb.classList.toggle('on', n > 0); fn.hidden = !n; fn.textContent = n;
    }
    function rowHtml(d, on) {
      var tags = '<span class="tag ' + (d.verified ? 'green' : 'grey') + '">' + (d.verified ? 'Verified' : 'Unverified') + '</span>' +
        (d.active === false ? '<span class="tag grey">Inactive</span>' : '') +
        (d.update === 'pending' ? '<span class="tag orange">Update pending</span>' : d.update === 'approved' ? '<span class="tag green">Update approved</span>' : '') +
        (d.chips || []).filter(function (c) { return String(c).toLowerCase() !== 'inactive'; }).map(function (c) { return '<span class="tag teal">' + esc(c) + '</span>'; }).join('');
      return '<button type="button" class="ddrow" data-id="' + esc(d.id) + '"' + (on ? ' aria-current="true"' : '') + '>' +
        '<span class="ddrow__t"><b class="t-minor-title' + (d.active === false ? ' off' : '') + '">' + esc(d.id) + '</b><span class="lb t-body-regular">' + esc(label(d)) + '</span><span class="tags">' + tags + '</span></span>' +
        '<span class="chev">' + ic('dropdown', 24) + '</span></button>';
    }
    function drawList() {
      var list = DIETS.filter(function (d) { return matches(d); });
      $('[data-count]').textContent = 'Diets (' + list.length + ')';
      var split = LAND.matches;
      if (split && list.length && !list.some(function (d) { return d.id === st.sel; })) st.sel = list[0].id;
      $('[data-list]').innerHTML = list.length ? list.map(function (d) { return rowHtml(d, split && d.id === st.sel); }).join('') :
        '<div class="empty"><span class="ei">' + ic('search', 24) + '</span><b class="t-minor-title">No diets match</b><span class="t-body-regular">Try another ID, species or filter.</span><button type="button" class="chip t-body-medium" data-clearall style="margin-top:8px">Clear search and filters</button></div>';
      return list;
    }
    function fmt(v) { v = Number(v) || 0; return v.toLocaleString('en-IN', { maximumFractionDigits: 2 }); }
    function itemCell(it, cols) {
      var m = it.mix, h = '<div class="it-n">' + esc(it.name) + (m ? '<span class="it-k">' + (m.label === 'RECIPE' ? 'RECIPE' : 'MIX') + '</span>' : '') + '</div>';
      var meta = [it.prep, it.cut].filter(Boolean).map(esc).join(', ');
      if (meta) h += '<div class="it-p t-body-regular">(' + meta + ')</div>';
      if (m && m.meta) h += '<div class="it-ex t-body-regular">' + esc(m.meta) + '</div>';
      if (m && m.parts && m.parts.length) h += '<div class="it-parts t-body-regular">' + m.parts.map(function (q) { q = typeof q === 'string' ? { name: q } : q; return '<span>' + esc(q.name) + (q.note ? ' <em>' + esc(q.note) + '</em>' : '') + '</span>'; }).join('') + '</div>';
      (it.alts || []).forEach(function (a) { a = typeof a === 'string' ? { name: a } : a; var q = a.amount || a.ratio; h += '<div class="it-alt t-body-regular">or <b>' + esc(a.name) + '</b>' + (a.prep ? ' (' + esc(a.prep) + ')' : '') + (q ? ' · ' + esc(q) : '') + '</div>'; });
      if (it.notes) h += '<div class="it-ex t-body-regular">' + esc(it.notes) + '</div>';
      return h;
    }
    function bands(d) {
      var sch = d.schedule || [], cols = d.columns || [];
      if (!sch.length) return '<div class="empty"><b class="t-minor-title">No items in this plan yet</b></div>';
      var rows = '';
      sch.forEach(function (b) {
        var n = 0; (b.days || []).forEach(function (g) { n += Math.max(1, (g.items || []).length); });
        var first = true;
        (b.days || []).forEach(function (g) {
          var its = g.items && g.items.length ? g.items : [null];
          its.forEach(function (it, i) {
            rows += '<tr>' + (first ? '<td class="time" rowspan="' + n + '">' + esc(b.time) + '</td>' : '') + (i === 0 ? '<td class="day t-body-regular" rowspan="' + its.length + '">' + esc(g.day) + '</td>' : '') +
              (it ? '<td>' + itemCell(it, cols) + '</td><td class="amt">' + esc(it.amount || '-') + '</td>' + cols.map(function (c, k) { return '<td class="amt">' + esc((it.extra || [])[k] || '-') + '</td>'; }).join('')
                : '<td colspan="' + (2 + cols.length) + '" class="t-body-regular" style="color:var(--md3-neutral-secondary)">No items</td>') + '</tr>';
            first = false;
          });
        });
      });
      return '<div class="dtab-wrap"><table class="dtab t-body-regular"><thead><tr><th>Time</th><th>Day</th><th>Item</th><th class="amt">Daily amt</th>' + cols.map(function (c) { return '<th class="amt">' + esc(c) + '</th>'; }).join('') + '</tr></thead><tbody>' + rows + '</tbody></table></div>';
    }
    function nutrition(d) {
      var nv = d.nutrition || {};
      return '<div class="nut"><p class="nut__help t-body-regular">' + ic('info', 20) + 'Per animal, per day. Totals across every item in this plan.</p>' + NUT.map(function (s) {
        return '<div class="nut__sec"><h4>' + s[0] + '</h4>' + s[1].map(function (r) { var v = Number(nv[r[0]]) || 0;
          return '<div class="nut__row t-body-regular"><span>' + r[1] + '</span><b class="' + (v === 0 ? 'zero' : '') + '">' + fmt(v) + ' <small>' + r[2] + '</small></b></div>'; }).join('') + '</div>';
      }).join('') + '</div>';
    }
    function extras(d) {
      var n = d.notes || {}, h = '', kv = '';
      if (st.tab === 'items' && n.kitchen) kv += '<dt>Kitchen</dt><dd>' + esc(n.kitchen) + '</dd>';
      if (st.tab === 'items' && n.site) kv += '<dt>Site</dt><dd>' + esc(n.site) + '</dd>';
      if (kv) h += '<div class="sub"><h3 class="t-minor-title">Notes</h3><dl class="kv t-body-regular">' + kv + '</dl></div>';
      if (d.remark) h += '<div class="remark t-body-regular">' + ic('info', 20) + '<div><b class="t-body-title">Remark</b><br>' + esc(d.remark) + '</div></div>';
      if (d.changeReason && d.changeReason.label) h += '<p class="reason t-body-regular">' + ic('history', 20) + 'Change reason <span class="tag orange">' + esc(d.changeReason.label) + '</span>' + (d.changeReason.detail ? '<span>' + esc(d.changeReason.detail) + '</span>' : '') + '</p>';
      return h;
    }
    function kindTag(k) { k = k || 'Base'; return '<span class="tag ' + (/season/i.test(k) ? 'orange' : /time/i.test(k) ? 'blue' : 'green') + '">' + esc(k) + '</span>'; }
    function species(d) {
      var sp = d.species || [], picked = st.picked[d.id] || {}, any = Object.keys(picked).some(function (k) { return picked[k]; });
      var h = '<section class="dpane"><div class="fed-h"><h3 class="t-minor-title">Fed to ' + plural(sp.length, 'species', 'species') + '</h3>' +
        '<div class="dseg" role="group" aria-label="Species view"><button type="button" data-view="cards" aria-pressed="' + (st.view === 'cards') + '" class="t-body-medium">' + ic('grid', 18) + 'Cards</button><button type="button" data-view="list" aria-pressed="' + (st.view === 'list') + '" class="t-body-medium">' + ic('list', 18) + 'List</button></div></div>' +
        '<div class="fed-tools"><span class="hint t-body-regular">Select species to move to another diet.</span>' +
        '<button type="button" class="linkbtn t-body-medium" data-move' + (any ? '' : ' aria-disabled="true"') + '>' + ic('transfer', 20) + 'Move to another diet</button>' +
        '<button type="button" class="linkbtn t-body-medium" data-addsp>' + ic('add', 20) + 'Add species</button></div>';
      if (!sp.length) return h + '<div class="empty"><b class="t-minor-title">No species yet</b></div></section>';
      h += '<div class="' + (st.view === 'cards' ? 'sgrid' : 'slist') + '">' + sp.map(function (s, i) {
        var on = !!picked[i];
        return '<div class="scard' + (on ? ' sel' : '') + '"><button type="button" class="ck" data-pick="' + i + '" aria-pressed="' + on + '" aria-label="Select ' + esc(s.name) + '">' + ic(on ? 'checkbox-checked' : 'checkbox-unchecked', 24) + '</button>' +
          (st.view === 'cards' ? '<span class="scard__ic">' + ic('paw', 22) + '</span>' : '') +
          '<span class="scard__t"><b class="t-body-title">' + esc(s.name) + '</b>' + (s.sci ? '<i class="t-body-regular">' + esc(s.sci) + '</i>' : '') +
          '<span class="scard__m t-body-regular">' + (s.animals != null ? plural(s.animals, 'animal') + ' held' : '') + kindTag(s.kind) + '</span></span></div>';
      }).join('') + '</div></section>';
      return h;
    }
    function detailHtml(d) {
      if (!d) return '<section class="dpane"><div class="empty"><b class="t-minor-title">Select a diet</b><span class="t-body-regular">Pick a diet to see its plan.</span></div></section>';
      var inactiveChip = (d.chips || []).some(function (c) { return String(c).toLowerCase() === 'inactive'; });
      var w = d.window && !(d.window.state === 'inactive' && inactiveChip) ? '<span class="win ' + d.window.state + '">' + ic(d.window.state === 'inactive' ? 'close' : 'calendar', 18) + esc(d.window.text) + '</span>' : '';
      var chips = (d.chips || []).map(function (c) { return String(c).toLowerCase() === 'inactive' ? '<span class="tag grey">Inactive</span>' : '<span class="tag teal">' + esc(c) + '</span>'; }).join('');
      var cert = d.dietitian ? '<div class="cert"><span class="cert__ic">' + ic('approved', 24) + '</span><span class="cert__t"><b class="t-body-title">' + esc(d.dietitian.name) + '</b><span class="t-body-regular">Certified dietitian · ' + esc(d.dietitian.date) + '</span></span><button type="button" class="iconbtn" data-certchange aria-label="Change the certifying dietitian">' + ic('pencil', 22) + '</button></div>'
        : '<div class="cert none"><span class="cert__ic">' + ic('alert', 24) + '</span><span class="cert__t"><b class="t-body-title">Uncertified</b><span class="t-body-regular">No dietitian behind this diet yet</span></span><button type="button" class="chip t-body-medium" data-certify>' + ic('approved', 18) + 'Certify</button></div>';
      return '<section class="dpane"><div class="dp-head"><div class="grow"><div class="dp-id"><b class="t-medium-medium">' + esc(d.id) + '</b>' +
        '<span class="tag ' + (d.verified ? 'green' : 'grey') + '">' + (d.verified ? 'Verified' : 'Unverified') + '</span>' +
        (d.update === 'pending' ? '<span class="tag orange">Update pending</span>' : d.update === 'approved' ? '<span class="tag green">Update approved</span>' : '') + '</div>' +
        '<span class="t-body-regular" style="color:var(--ink)">' + esc(label(d)) + '</span></div>' +
        '<div class="dp-acts"><button type="button" class="iconbtn" data-act="edit" aria-label="Edit diet">' + ic('pencil', 22) + '</button><button type="button" class="iconbtn" data-act="pdf" aria-label="Download PDF">' + ic('download', 22) + '</button><button type="button" class="iconbtn" data-act="more" aria-label="Plan actions">' + ic('menu-vertical', 22) + '</button></div></div>' +
        ((w || chips) ? '<div class="tags">' + w + chips + '</div>' : '') + cert +
        '<div class="dseg" role="group" aria-label="Diet view"><button type="button" data-dtab="items" aria-pressed="' + (st.tab === 'items') + '" class="t-body-medium">Items</button><button type="button" data-dtab="nutrition" aria-pressed="' + (st.tab === 'nutrition') + '" class="t-body-medium">Nutrition</button></div>' +
        (st.tab === 'nutrition' ? nutrition(d) : bands(d)) + extras(d) + '</section>' + species(d);
    }
    function host() { return LAND.matches ? $('[data-detail]') : (st.panel ? document.querySelector('#dpanel .dpanel__body') : null); }
    function drawDetail() { var h = host(); if (h) h.innerHTML = detailHtml(find(st.sel)); }
    function openPanel(id) {
      var d = find(id), p = document.getElementById('dpanel'); if (!d) return;
      st.sel = id; st.panel = id;
      p.querySelector('[data-ptitle]').textContent = d.id; p.querySelector('[data-psub]').textContent = label(d);
      p.hidden = false; drawDetail(); p.querySelector('.dpanel__body').scrollTop = 0;
    }
    function closePanel() { st.panel = null; document.getElementById('dpanel').hidden = true; }
    function draw() { drawFilters(); drawList(); drawDetail(); }

    root.addEventListener('input', function (e) { if (e.target.matches('[data-q]')) { st.q = e.target.value; drawFilters(); drawList(); drawDetail(); } });
    root.addEventListener('click', function (e) {
      var t;
      if ((t = e.target.closest('[data-v]'))) { st.ver = t.getAttribute('data-v'); draw(); return; }
      if ((t = e.target.closest('[data-c]'))) { st.cls = t.getAttribute('data-c'); draw(); return; }
      if ((t = e.target.closest('[data-unf]'))) { var k = t.getAttribute('data-unf'); if (k === '*') st.f = { site: '', cert: '', upd: '' }; else st.f[k] = ''; draw(); return; }
      if (e.target.closest('[data-clearall]')) { st.q = ''; st.ver = ''; st.cls = 'all'; st.f = { site: '', cert: '', upd: '' }; $('[data-q]').value = ''; draw(); return; }
      if (e.target.closest('[data-filters]')) { openSheet(); return; }
      if ((t = e.target.closest('.ddrow'))) {
        var id = t.getAttribute('data-id');
        if (id !== st.sel) st.tab = 'items';
        st.sel = id;
        if (LAND.matches) { try { history.replaceState(null, '', '#' + PREFIX + id); } catch (x) {} drawList(); drawDetail(); }
        else location.hash = '#' + PREFIX + id;
      }
    });
    function onDetail(e) {
      var d = find(st.sel), t; if (!d) return;
      if ((t = e.target.closest('[data-dtab]'))) { st.tab = t.getAttribute('data-dtab'); drawDetail(); return; }
      if ((t = e.target.closest('[data-view]'))) { st.view = t.getAttribute('data-view'); drawDetail(); return; }
      if ((t = e.target.closest('[data-pick]'))) { var m = st.picked[d.id] = st.picked[d.id] || {}, k = t.getAttribute('data-pick'); m[k] = !m[k]; drawDetail(); return; }
      if (e.target.closest('[data-move]')) { var any = Object.keys(st.picked[d.id] || {}).some(function (k) { return st.picked[d.id][k]; }); toast(any ? 'Moving species to another diet is not part of this prototype.' : 'Select species to move first.'); return; }
      if (e.target.closest('[data-addsp]')) { toast('Adding species is not part of this prototype.'); return; }
      if (e.target.closest('[data-certify], [data-certchange]')) { toast('Certifying a diet is not part of this prototype.'); return; }
      if ((t = e.target.closest('[data-act]'))) { var a = t.getAttribute('data-act'); toast(a === 'edit' ? 'Editing a diet is not part of this prototype.' : a === 'pdf' ? 'Download PDF is not part of this prototype.' : 'Plan actions are not part of this prototype.'); }
    }
    $('[data-detail]').addEventListener('click', onDetail);
    document.querySelector('#dpanel .dpanel__body').addEventListener('click', onDetail);

    /* filters sheet: Site, Certification, Updates (V2 filter sheet) */
    var draft;
    function sheetHtml() {
      function grp(key, title, opts) { return '<div class="sheet__g"><h3 class="t-minor-medium">' + title + '</h3><div class="chips">' + opts.map(function (o) { return '<button type="button" class="spchip t-body-medium" data-sk="' + key + '" data-sv="' + esc(o[0]) + '" aria-pressed="' + (draft[key] === o[0]) + '">' + esc(o[1]) + '</button>'; }).join('') + '</div></div>'; }
      return '<div class="grab"></div><div class="sheet__h"><h2 class="t-major-title" id="sheetT">Filters</h2><button type="button" class="iconbtn" data-sclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
        grp('site', 'Site', [['', 'All sites']].concat(DIRD.sites.map(function (s) { return [s, s]; }))) +
        grp('cert', 'Certification', [['', 'All'], ['uncertified', 'Uncertified'], ['certified', 'Certified']]) +
        grp('upd', 'Updates', [['', 'All'], ['pending', 'Needs verification'], ['approved', 'Update approved'], ['any', 'Any updated diet']]) +
        '<div class="sheet__f"><button type="button" class="btn sec" data-sreset>Reset</button><button type="button" class="btn pri" data-sapply>Apply</button></div>';
    }
    function openSheet() { draft = { site: st.f.site, cert: st.f.cert, upd: st.f.upd }; var s = document.getElementById('sheet'); s.innerHTML = sheetHtml(); document.getElementById('scrim').hidden = false; }
    function closeSheet() { document.getElementById('scrim').hidden = true; }
    document.getElementById('scrim').addEventListener('click', function (e) {
      var t;
      if (e.target === this || e.target.closest('[data-sclose]')) { closeSheet(); return; }
      if ((t = e.target.closest('[data-sk]'))) { draft[t.getAttribute('data-sk')] = t.getAttribute('data-sv'); document.getElementById('sheet').innerHTML = sheetHtml(); return; }
      if (e.target.closest('[data-sreset]')) { draft = { site: '', cert: '', upd: '' }; document.getElementById('sheet').innerHTML = sheetHtml(); return; }
      if (e.target.closest('[data-sapply]')) { st.f = draft; closeSheet(); draw(); }
    });
    LAND.addEventListener('change', function () { if (LAND.matches) closePanel(); else if (opt.currentId && opt.currentId()) openPanel(opt.currentId()); draw(); });
    draw();
    return {
      count: DIETS.length,
      show: function (id) {
        if (id && find(id)) { if (id !== st.sel) st.tab = 'items'; st.sel = id; if (LAND.matches) { closePanel(); drawList(); drawDetail(); } else openPanel(id); }
        else { closePanel(); drawList(); drawDetail(); }
      },
      hasPanel: function () { return !!st.panel; },
    };
  }
'''

SP_JS = '''  /* ---------------- Diet by Species (site #/diets) ---------------- */
  function SpModule(root) {
    var SPECIES = ''' + json.dumps(sp_list, ensure_ascii=False).replace('</', '<\\/') + ''';
    var CLASSES = ''' + json.dumps(CLASSES) + ''';
    var st = { seg: 'all', q: '', cls: [], sort: 'count', open: {}, chips: false };
    var SEGS = [['all', 'All'], ['with', 'Species with diet'], ['without', 'Species without diet']];
    root.innerHTML =
      '<div class="segwrap"><div class="seg3" role="tablist" aria-label="Diet coverage" data-seg></div></div>' +
      '<div class="spband"><label class="spsearch">' + ic('search', 20) + '<span class="sr-only">Search species</span><input class="t-body-regular" type="search" data-q placeholder="Search" autocomplete="off"></label>' +
      '<button class="spfilter" type="button" data-fbtn aria-pressed="false" aria-label="Filter by class">' + ic('filter-2', 24) + '<span class="t-minor-medium" data-fn hidden></span></button></div>' +
      '<div class="spchips" data-chips hidden role="group" aria-label="Class"></div>' +
      '<div class="list-bar"><h2 class="t-minor-medium" data-count aria-live="polite"></h2><button class="chip t-body-medium" type="button" data-sort>' + ic('sort', 18) + '<span data-sortl></span></button></div>' +
      '<div class="spcards" data-list></div>';
    var $ = function (s) { return root.querySelector(s); };
    function initials(n) { return n.split(/[\\s-]+/).filter(Boolean).slice(0, 2).map(function (w) { return w[0]; }).join('').toUpperCase(); }
    function match(s) { var q = st.q.trim().toLowerCase(); return (!q || (s.name + ' ' + s.sci).toLowerCase().indexOf(q) !== -1) && (!st.cls.length || st.cls.indexOf(s.cls) !== -1); }
    function inSeg(s, t) { return t === 'all' || (t === 'with' ? !s.none : s.none); }
    function row(d) { return '<div class="sprow">' + ttag(d.type) + '<span class="t"><b class="t-body-title">Diet ' + d.code + '</b><span class="t-body-regular">' + esc(d.name) + (d.when ? ' • ' + esc(d.when) : '') + '</span></span>' + pill(d.status) + '</div>'; }
    function card(s) {
      var open = !!st.open[s.id];
      var right = s.none ? '<span class="spn"><span class="gap t-body-medium">No diet yet</span></span>' : '<span class="spn"><span class="v t-stat-title">' + s.active + '</span><span class="l t-body-regular">' + (s.active === 1 ? 'Active diet' : 'Active diets') + '</span></span>';
      var panel = open ? '<div class="spdiets" id="sp-' + s.id + '">' + (s.diets.length ? s.diets.map(row).join('') : '<p class="spnone t-body-regular">No diet is set for this species yet. Raise a diet request to add one.</p><a class="spmore t-body-medium" href="#request">Go to Diet Request' + ic('dropdown', 20) + '</a>') + '</div>' : '';
      return '<div class="spwrap"><button class="spcard" type="button" data-sp="' + s.id + '" aria-expanded="' + open + '" aria-controls="sp-' + s.id + '"><span class="spav t-minor-title" aria-hidden="true">' + initials(s.name) + '</span>' +
        '<span class="grow"><span class="n t-minor-title">' + esc(s.name) + '</span><span class="m t-minor-italic">' + esc(s.sci) + '</span><span class="c t-body-regular">' + esc(s.cls) + (s.animals ? ' • ' + plural(s.animals, 'animal') : '') + '</span></span>' +
        right + '<span class="chev">' + ic('dropdown', 24) + '</span></button>' + panel + '</div>';
    }
    function draw() {
      var base = SPECIES.filter(match);
      $('[data-seg]').innerHTML = SEGS.map(function (t) { return '<button type="button" role="tab" class="t-body-medium" data-s="' + t[0] + '" aria-selected="' + (st.seg === t[0]) + '">' + t[1] + ' - ' + base.filter(function (s) { return inSeg(s, t[0]); }).length + '</button>'; }).join('');
      var list = base.filter(function (s) { return inSeg(s, st.seg); });
      list.sort(function (a, b) { return st.sort === 'name' ? a.name.localeCompare(b.name) : (b.active - a.active) || a.name.localeCompare(b.name); });
      $('[data-count]').textContent = 'Species (' + list.length + ')';
      var empty = '<div class="empty" style="grid-column:1/-1"><span class="ei">' + ic('search', 24) + '</span><b class="t-minor-title">No species match</b><span class="t-body-regular">Try a common or scientific name, or clear the filters.</span></div>';
      if (st.seg === 'all') {
        var w = list.filter(function (s) { return !s.none; }), wo = list.filter(function (s) { return s.none; });
        $('[data-list]').className = 'spgroups';
        $('[data-list]').innerHTML = !list.length ? empty :
          [['Species with diet', w], ['Species without diet', wo]].map(function (g) {
            return '<section class="spgroup" aria-label="' + g[0] + '"><h3 class="spgroup__h t-minor-title">' + g[0] + ' (' + g[1].length + ')</h3>' +
              (g[1].length ? '<div class="spcards">' + g[1].map(card).join('') + '</div>' : '<p class="spgroup__none t-body-regular">None match the search or filter.</p>') + '</section>';
          }).join('');
        return finish();
      }
      $('[data-list]').className = 'spcards';
      $('[data-list]').innerHTML = list.length ? list.map(card).join('') : '<div class="empty" style="grid-column:1/-1"><span class="ei">' + ic('search', 24) + '</span><b class="t-minor-title">No species match</b><span class="t-body-regular">Try a common or scientific name, or clear the filters.</span></div>';
      finish();
    }
    function finish() {
      $('[data-fn]').hidden = !st.cls.length; $('[data-fn]').textContent = st.cls.length; $('[data-fbtn]').classList.toggle('on', st.cls.length > 0);
      $('[data-chips]').innerHTML = CLASSES.map(function (c) { return '<button type="button" class="spchip t-body-medium" data-cl="' + c + '" aria-pressed="' + (st.cls.indexOf(c) !== -1) + '">' + c + '</button>'; }).join('');
      $('[data-sortl]').textContent = st.sort === 'name' ? 'Name A-Z' : 'Most diets';
    }
    root.addEventListener('input', function (e) { if (e.target.matches('[data-q]')) { st.q = e.target.value; draw(); } });
    root.addEventListener('click', function (e) {
      var t;
      if ((t = e.target.closest('[data-s]'))) { var k = t.getAttribute('data-s'); if (k !== st.seg) location.hash = '#species/' + k; return; }
      if ((t = e.target.closest('[data-fbtn]'))) { var c = $('[data-chips]'); c.hidden = !c.hidden; t.setAttribute('aria-pressed', String(!c.hidden)); return; }
      if ((t = e.target.closest('[data-cl]'))) { var i = st.cls.indexOf(t.getAttribute('data-cl')); if (i === -1) st.cls.push(t.getAttribute('data-cl')); else st.cls.splice(i, 1); draw(); return; }
      if (e.target.closest('[data-sort]')) { st.sort = st.sort === 'count' ? 'name' : 'count'; draw(); return; }
      if ((t = e.target.closest('[data-sp]'))) { st.open[t.getAttribute('data-sp')] = !st.open[t.getAttribute('data-sp')]; draw(); }
    });
    draw();
    return { count: SPECIES.length, setSeg: function (k) { if (SEGS.some(function (x) { return x[0] === k; }) && k !== st.seg) { st.seg = k; draw(); } } };
  }
'''

RQ_JS = '''  /* ---------------- Diet Request (site #/requests) ---------------- */
  function RqModule(root) {
    var REQS = REQS_ALL;
    var PRIO = { high: ['!!!', 'High priority', 0], medium: ['!!', 'Medium priority', 1], low: ['!', 'Low priority', 2] };
    var VIEWS = {
      office: [['all', 'All', null], ['pending', 'Pending review', ['requested', 'under_review']], ['configuring', 'Configuring', ['configuring']], ['adjustment', 'Needs adjustment', ['adjustment']], ['kitchen', 'Kitchen review', ['kitchen_review']], ['delayed', 'Delayed', ['delayed']], ['done', 'Completed', ['ready', 'applied']], ['closed', 'Rejected', ['rejected', 'cancelled']]],
      kitchen: [['attention', 'Requires attention', ['kitchen_review']], ['delayed', 'Delayed', ['delayed']], ['adjustment', 'Needs adjustment', ['adjustment']], ['done', 'Sent to prep', ['ready', 'applied']], ['all', 'All', null]],
      mine: [['all', 'All', null], ['pending', 'Pending review', ['requested', 'under_review']], ['progress', 'In progress', ['configuring', 'adjustment', 'kitchen_review', 'delayed', 'with_kitchens']], ['done', 'Scheduled / Live', ['ready', 'applied', 'scheduled', 'live']], ['closed', 'Rejected', ['rejected', 'cancelled']]],
    };
    function mode() { return !RQ.can('seeAll') ? 'mine' : RQ.can('kitchenAct') ? 'kitchen' : 'office'; }
    var SEGS = VIEWS.office, curMode = null;
    var st = { seg: 'all', sort: 'priority' };
    root.innerHTML = '<div data-legacy><div class="segrow" role="group" aria-label="Request status" data-seg></div>' +
      '<div class="list-bar"><h2 class="t-minor-medium" data-count aria-live="polite"></h2><button class="chip t-body-medium" type="button" data-sort>' + ic('filter-2', 18) + '<span data-sortl></span></button></div>' +
      '<div class="rqcards" data-list></div></div><div data-hdq hidden></div><div data-kq hidden></div>';
    var $ = function (s) { return root.querySelector(s); };
    var hdq = HdQueue(root.querySelector('[data-hdq]')), kq = HdQueue(root.querySelector('[data-kq]'), true);
    function inSeg(r, t) { var v = SEGS.filter(function (x) { return x[0] === t; })[0]; return !v || !v[2] || v[2].indexOf(r.status) !== -1; }
    function card(r) {
      var p = PRIO[r.prio];
      return '<a class="hdcard' + (r.label === 'Cancelled' ? ' struck' : '') + '" href="#request/' + r.id + '" aria-label="Open ' + r.id + ': ' + esc(r.title) + '"><div class="hd-top"><span class="grow"><span class="hd-id t-minor-title">' + r.id + '</span><span class="hd-cat t-body-medium">' + esc(r.sp) + '</span><span class="hd-where t-body-regular">' + esc(r.where) + '</span></span>' +
        '<span class="ribbon ' + r.prio + '" title="' + p[1] + '" aria-label="' + p[1] + '">' + p[0] + '</span></div>' +
        '<div class="hd-body"><span class="hd-title t-medium-medium">' + esc(r.title) + '</span><span class="hd-text t-body-regular">' + esc(r.text) + '</span><span class="hd-by t-body-regular"><b class="t-body-title">' + esc(r.by.name + (RQ.isMine(r) ? ' (You)' : '')) + '</b> • ' + r.date + '</span></div>' +
        '<div class="hd-band ' + r.tone + ' t-minor-medium">' + ic(r.icon, 20) + esc(r.label) + '</div></a>';
    }
    function draw() {
      var hd = RQ.can('configure'), kv = !hd && RQ.can('kitchenAct'); $('[data-legacy]').hidden = hd || kv; $('[data-hdq]').hidden = !hd; $('[data-kq]').hidden = !kv; if (hd) { curMode = 'hd'; hdq.draw(); return; } if (kv) { curMode = 'kitchen'; kq.draw(); return; }
      var m = mode(); if (m !== curMode) { curMode = m; SEGS = VIEWS[m]; st.seg = SEGS[0][0]; }
      REQS = RQ.visible();
      $('[data-seg]').innerHTML = SEGS.map(function (t) { return '<button type="button" class="spchip t-body-medium" data-s="' + t[0] + '" aria-pressed="' + (st.seg === t[0]) + '">' + t[1] + ' <span class="n">' + REQS.filter(function (r) { return inSeg(r, t[0]); }).length + '</span></button>'; }).join('');
      var list = REQS.filter(function (r) { return inSeg(r, st.seg); });
      list.sort(function (a, b) { return st.sort === 'recent' ? b.iso.localeCompare(a.iso) : (PRIO[a.prio][2] - PRIO[b.prio][2]) || b.iso.localeCompare(a.iso); });
      $('[data-count]').innerHTML = (curMode === 'mine' ? '<span class="seg-mine">My requests</span> (' + list.length + ')' : 'Requests (' + list.length + ')');
      $('[data-list]').innerHTML = list.length ? list.map(card).join('') : '<div class="empty" style="grid-column:1/-1"><span class="ei">' + ic('reason-or-list', 24) + '</span><b class="t-minor-title">No requests to show</b><span class="t-body-regular">' + esc(curMode === 'mine' ? 'Viewing as ' + RQ.viewer.title + '. Requests you raise appear here.' : 'Nothing in this view right now.') + '</span></div>';
      $('[data-sortl]').textContent = st.sort === 'recent' ? 'Recent' : 'Priority';
    }
    root.addEventListener('click', function (e) {
      var t;
      if ((t = e.target.closest('[data-s]'))) { st.seg = t.getAttribute('data-s'); draw(); return; }
      if (e.target.closest('[data-sort]')) { st.sort = st.sort === 'priority' ? 'recent' : 'priority'; draw(); }
    });
    draw();
    RQ.listeners.push(draw);
    return { count: REQS.length };
  }
'''

exec(open(os.path.join(HERE, 'req.py')).read())
exec(open(os.path.join(HERE, 'sp3.py')).read())
exec(open(os.path.join(HERE, 'roles.py')).read())
exec(open(os.path.join(HERE, 'hdq.py')).read())

# ---------------------------------------------------------------- Directory for diet-home.html: the diets that exist in the species data
# diet-directory.html keeps the V2 data and module unchanged; diet-home.html gets a directory built from BS (sample.py: 5 base diets),
# with "Used by" lists that match the species tab, and the dead controls replaced (Edit opens the species edit wizard).
_MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
def _dmy(iso): return '%d %s %s' % (int(iso[8:10]), _MON[int(iso[5:7]) - 1], iso[:4]) if iso else ''
def _cls(c): c = (c or '').lower(); return c if c in ('mammalia', 'aves', 'reptilia') else 'other'
_byk = {}
for _s in BS['species']:
    for _pid in _s['plans']:
        _p = BS['plans'][str(_pid)]
        _byk.setdefault(_p.get('sharedFrom') or _p['id'], []).append((_s, _p))
_hd = []
for _k, _us in _byk.items():
    _s0, _p0 = _us[0]
    _e = {'id': 'D-%s' % _k, 'tsn': _s0['tsn'], 'planId': _p0['id'], 'verified': bool(_p0.get('verified')), 'update': _p0.get('update', 'none'), 'active': True,
          'window': {'text': 'Year-round since ' + _dmy(_p0.get('created')), 'state': 'current'}, 'by': _p0.get('by'),
          'dietitian': {'name': _p0['dietitian'], 'date': _dmy(_p0.get('created'))} if _p0.get('dietitian') else None,
          'schedule': _p0.get('schedule', []), 'nutrition': _p0.get('nutrition', {}), 'columns': _p0.get('columns'),
          'species': [{'name': x['name'], 'sci': x['sci'], 'animals': x['animals'], 'kind': 'Base', 'cls': _cls(x['cls']), 'tsn': x['tsn'], 'planId': q['id']} for x, q in _us],
          'sites': sorted({e['site'] for x, q in _us for e in x['enclosures']})}
    if _p0.get('notes'): _e['notes'] = _p0['notes']
    if _p0.get('remark'): _e['remark'] = _p0['remark']
    _hd.append({k: v for k, v in _e.items() if v is not None})
V2DIR_HOME = {'sites': sorted({x for d in _hd for x in d['sites']}), 'selectedId': _hd[0]['id'] if _hd else None, 'diets': _hd}
N_DIR_HOME = len(_hd)
_dj = json.dumps(V2DIR, ensure_ascii=False).replace('</', '<\\/')
assert DIR_JS.count(_dj) == 1
DIR_JS_HOME = DIR_JS.replace(_dj, json.dumps(V2DIR_HOME, ensure_ascii=False).replace('</', '<\\/'))
_a, _b = DIR_JS_HOME.index('    function species(d) {'), DIR_JS_HOME.index('    function host() {')
DIR_JS_HOME = DIR_JS_HOME[:_a] + """    function species(d) {
      var sp = d.species || [];
      return '<section class="dpane"><h3 class="t-minor-title">Used by ' + plural(sp.length, 'species', 'species') + '</h3>' + (sp.length ? '<ul class="shlist">' + sp.map(function (s) {
        return '<li><a class="shrow" href="#species/all/' + s.tsn + '/' + s.planId + '"><span class="t-body-title">' + esc(s.name) + '</span>' + (s.sci ? '<i class="t-body-regular">' + esc(s.sci) + '</i>' : '') + '</a></li>'; }).join('') + '</ul>' : '<p class="t-body-regular dp-none">No species use this diet.</p>') + '</section>';
    }
    function detailHtml(d) {
      if (!d) return '<section class="dpane"><div class="empty"><b class="t-minor-title">No diets yet</b><span class="t-body-regular">Create a base diet from Diet by Species.</span></div></section>';
      var meta = ['Base diet', d.window ? d.window.text : '', d.by ? 'Created by ' + d.by : '', d.dietitian ? 'Certified by ' + d.dietitian.name : 'Not certified'].filter(Boolean).join(' · ');
      return '<section class="dpane"><div class="dp-head"><div class="grow"><div class="tags"><span class="tag ' + (d.verified ? 'green' : 'grey') + '">' + (d.verified ? 'Verified' : 'Unverified') + '</span>' +
        (d.update === 'pending' ? '<span class="tag orange">Update pending</span>' : d.update === 'approved' ? '<span class="tag green">Update approved</span>' : '') + '</div>' +
        '<p class="dp-meta t-body-regular">' + esc(meta) + '</p></div>' +
        (d.planId ? '<button type="button" class="btn sec dp-edit" data-act="edit" aria-label="Edit ' + esc(d.id) + '">' + ic('pencil', 20) + 'Edit</button>' : '') + '</div>' +
        '<div class="dseg" role="group" aria-label="Diet view"><button type="button" data-dtab="items" aria-pressed="' + (st.tab === 'items') + '" class="t-body-medium">Items</button><button type="button" data-dtab="nutrition" aria-pressed="' + (st.tab === 'nutrition') + '" class="t-body-medium">Nutrition</button></div>' +
        (st.tab === 'nutrition' ? nutrition(d) : bands(d)) + extras(d) + '</section>' + species(d);
    }
""" + DIR_JS_HOME[_b:]
_a, _b = DIR_JS_HOME.index('    function onDetail(e) {'), DIR_JS_HOME.index("    $('[data-detail]').addEventListener('click', onDetail);")
DIR_JS_HOME = DIR_JS_HOME[:_a] + """    function onDetail(e) {
      var d = find(st.sel), t; if (!d) return;
      if ((t = e.target.closest('[data-dtab]'))) { st.tab = t.getAttribute('data-dtab'); drawDetail(); return; }
      if (e.target.closest('[data-act="edit"]') && d.planId && HOOKS.editPlan) HOOKS.editPlan(d.tsn, d.planId);
    }
""" + DIR_JS_HOME[_b:]

OVERLAYS = f'''  <div class="dpanel" id="dpanel" hidden role="dialog" aria-modal="true" aria-labelledby="dpT">
    <header class="bar"><button class="iconbtn" type="button" data-pback aria-label="Back to the diet list">{svg("back", 24)}</button><div class="bar__hd"><h1 class="t-medium-medium" id="dpT" data-ptitle></h1><p class="t-body-regular" data-psub></p></div></header>
    <div class="dpanel__body"></div>
  </div>
  <div class="scrim" id="scrim" hidden><div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="sheetT"></div></div>
  <div class="toast t-body-medium" id="toast" role="status" aria-live="polite"></div>'''

SP_OVERLAYS = f'''  <div class="dpanel" id="spanel" hidden role="dialog" aria-modal="true" aria-labelledby="spT">
    <header class="bar"><button class="iconbtn" type="button" data-spback aria-label="Back to the species list">{svg("back", 24)}</button><div class="bar__hd"><h1 class="t-medium-medium" id="spT" data-ptitle></h1><p class="t-body-regular" data-psub style="font-style:italic"></p></div><button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button></header>
    <div class="dpanel__body"></div>
  </div>
'''

SP_OVERLAYS = SP_OVERLAYS + WIZ_OVERLAY + REQ_OVERLAY + ROLE_OVERLAY

SITE_BTN = (f'<button class="sitebtn" type="button" aria-label="Site: All Sites">{svg("location-icon", 24)}'
            f'<span class="t-minor-medium">All Sites</span>{svg("dropdown", 20)}</button>')

# ---------------------------------------------------------------- diet-home.html (tabbed)
N_REQ = len(_req_seed)
TABS = [('directory', 'Diet Directory', N_DIR_HOME), ('species', 'Diet by Species', N_SP), ('request', 'Diet Request', N_REQ)]
tabs_html = ''.join(f'<a class="mtab t-minor-medium" role="tab" id="t-{k}" href="#{k}" aria-controls="p-{k}" aria-selected="false">{l} - {n}</a>' for k, l, n in TABS)
panes = ''.join(f'<section class="pane" id="p-{k}" role="tabpanel" aria-labelledby="t-{k}" hidden></section>' for k, _, _ in TABS)

home_body = f'''  <div class="app">
{STATUS_HTML}
    <div class="head">
      <header class="bar">
        <a class="iconbtn" href="diet-module-flow.html" data-aslink="diet-module-flow.html" aria-label="Back to Modules">{svg("back", 24)}</a>
        <div class="bar__hd"><h1 class="t-medium-medium">Diet</h1></div>
        <button class="asbtn" id="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button>
        {SITE_BTN}
      </header>
      <nav class="mtabs" role="tablist" aria-label="Diet sections">{tabs_html}</nav>
    </div>
    <main class="main" id="main">{panes}</main>
  </div>
{SP_OVERLAYS}{OVERLAYS}'''

home_js = HELPERS_JS + REQ_SHARED_JS + HDQ_JS + DIR_JS_HOME + SP_JS + RQ_JS + '''  /* ---------------- tabs + hash routing (#directory, #directory/D-273, #species, #request) ---------------- */
  var KEYS = ['directory', 'species', 'request'];
  (function () { var a = new URLSearchParams(location.search).get('as'); var ok = function (k) { return USERS.some(function (u) { return u.key === k; }); }, sv = savedViewer(); setViewer(ok(a) ? a : ok(sv) ? sv : 'biologist', true); })();
  document.addEventListener('click', function (e) { if (e.target.closest('.asbtn')) openRoles(); });
  function parse() { var h = location.hash.replace(/^#/, ''), p = h.split('/'); return { tab: KEYS.indexOf(p[0]) !== -1 ? p[0] : 'directory', id: p[0] === 'directory' && p[1] ? decodeURIComponent(p[1]) : null, seg: p[0] === 'species' ? (p[1] || 'all') : null, tsn: p[0] === 'species' && p[2] ? Number(p[2]) : null, plan: p[0] === 'species' && p[3] && p[3] !== 'new' && p[3] !== 'request' ? Number(p[3]) : null, nk: p[0] === 'species' && p[3] === 'new' ? (p[4] || 'base') : null, nstep: p[0] === 'species' && p[3] === 'new' ? (p[5] || null) : null, rq: p[0] === 'species' && p[3] === 'request' ? (p[5] || 'where') : null, rid: p[0] === 'request' && p[1] ? decodeURIComponent(p[1]) : null }; }
  var dir = DirModule(document.getElementById('p-directory'), { prefix: 'directory/', currentId: function () { return parse().id; } });
  var spm = SpModule(document.getElementById('p-species'));
  RqModule(document.getElementById('p-request'));
  var cur = null, pushedPanel = false, rdPushed = false;
  var rqd = ReqDetail();
  function route() {
    var r = parse();
    KEYS.forEach(function (k) {
      var on = k === r.tab;
      document.getElementById('t-' + k).setAttribute('aria-selected', String(on));
      document.getElementById('p-' + k).hidden = !on;
    });
    if (cur !== r.tab) { document.getElementById('main').scrollTop = 0; cur = r.tab; }
    if (r.tab === 'directory') dir.show(r.id); else dir.show(null);
    if (r.tab === 'species') spm.show(r.seg, r.tsn, r.plan, r.nk, r.nstep, r.rq); else spm.show('all', null, null);
    if (r.rid) { if (!rqd.open(r.rid, rdPushed)) { try { history.replaceState(null, '', '#request'); } catch (x) {} } } else rqd.close();
  }
  document.querySelector('.mtabs').addEventListener('click', function (e) { var a = e.target.closest('.mtab'); if (!a) return; e.preventDefault(); var k = a.getAttribute('href').slice(1); if (parse().tab !== k || location.hash.indexOf('/') !== -1) location.hash = '#' + k; });
  document.querySelector('[data-pback]').addEventListener('click', function () { if (history.length > 1 && pushedPanel) history.back(); else location.hash = '#directory'; });
  window.addEventListener('hashchange', function () { var r = parse(); pushedPanel = !!r.id; spPushed = !!r.tsn; rdPushed = !!r.rid; route(); });
  var spPushed = false;
  document.querySelector('[data-spback]').addEventListener('click', function () { if (spPushed && history.length > 1) history.back(); else location.hash = '#species/' + (parse().seg || 'all'); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { if (!document.getElementById('scrim').hidden) document.getElementById('scrim').hidden = true; else if (dir.hasPanel()) document.querySelector('[data-pback]').click(); else if (!document.getElementById('rqsheet').hidden) document.getElementById('rqsheet').hidden = true; else if (rqd.isOpen()) document.querySelector('#rqd [data-rdback]').click(); else if (spm.escape()) {} else if (spm.hasPanel()) document.querySelector('[data-spback]').click(); } });
  route();
'''

page('diet-home.html', 'Diet',
     'Screen 2 - Diet home: one tabbed screen (Diet Directory | Diet by Species | Diet Request). Back: diet-module-flow.html. '
     'Routes: #directory (#directory/D-273 opens a diet), #species, #request. Directory content: V2 Tab prototype diet/directory (directory.data.js, 32 diets). '
     'Species and Request content: Antz diet tablet prototype (antz-diet.pages.dev). Visual language: that site.',
     HEAD_CSS + DIR_CSS2 + SP_CSS2 + RQ_CSS2 + SP3_CSS + WIZ_CSS + REQ_CSS + ROLE_CSS + HDQ_CSS, home_body, home_js)

# ---------------------------------------------------------------- diet-directory.html (standalone, same module)
_a = HEAD_CSS.index('    /* species coverage segments'); _b = HEAD_CSS.index('    .rowlabel {')
_HEAD_DIR = HEAD_CSS[:_a] + HEAD_CSS[_b:]
dir_body2 = f'''  <div class="app">
{STATUS_HTML}
    <div class="head">
      <header class="bar">
        <a class="iconbtn" href="diet-home.html#directory" aria-label="Back to Diet">{svg("back", 24)}</a>
        <div class="bar__hd"><h1 class="t-medium-medium">Diet Directory</h1></div>
        {SITE_BTN}
      </header>
    </div>
    <main class="main" id="main"><section class="pane" id="p-directory"></section></main>
  </div>
{OVERLAYS}'''

HELPERS_JS_DIR = icon_js([i for i in ALL_ICONS if i not in ('image', 'user', 'notes-new')]) + HELPERS_JS[len(icon_js(ALL_ICONS)):]
dir_js2 = HELPERS_JS_DIR + DIR_JS + '''  function idFromHash() { var h = location.hash.replace(/^#/, ''); return h ? decodeURIComponent(h) : null; }
  var dir = DirModule(document.getElementById('p-directory'), { prefix: '', currentId: idFromHash });
  var pushedPanel = false;
  document.querySelector('[data-pback]').addEventListener('click', function () { if (pushedPanel) history.back(); else { try { history.replaceState(null, '', location.pathname + location.search); } catch (x) {} dir.show(null); } });
  window.addEventListener('hashchange', function () { pushedPanel = !!idFromHash(); dir.show(idFromHash()); });
  dir.show(idFromHash());
'''

page('diet-directory.html', 'Diet Directory',
     'SUPERSEDED by the Diet Directory tab in diet-home.html (diet-home.html#directory). Rebuilt here on the same directory module and data '
     '(V2 Tab prototype diet/directory, 32 diets) so it matches. #D-273 opens a diet. Back: diet-home.html#directory.',
     _HEAD_DIR + DIR_CSS2, dir_body2, dir_js2)
