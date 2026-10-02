# mg_packaging_list.py: exec'd by kitchen.py. Meal Group Management > Packaging list.
# Source: Dev system_local kitchen/packaging-list.{html,js,css,data.js} (+ sites.data.js, keeper-areas.data.js).
# A read-only report: site and section pickers, keeper-area chips, a stat strip, and the tabs Packaging list, Diet,
# Species, Ingredients, Enclosures, Forecast and Piece Weights. The source works every figure out with packaging-engine.js
# from the diet data; this page shows the rows the source data file captured for each site and section scope
# (mgdata_packaging-list.json). Keeper areas come from the Keeper Areas page when it offers MGAPI.areas(); piece weights
# from the Piece Weights page (mgPieceWeights()); a delivery's packing station from MGAPI.stations() when that page offers it.
MGMOD = {'icons': ['search', 'calendar', 'time', 'paw', 'dropdown', 'back', 'info', 'alert'], 'css': '''    /* Packaging list */
    .pl-scope { display: grid; gap: 14px; }
    .pl-pick { display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .pl-pick .mgf small { min-height: 18px; }
    .pl-chips { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
    .pl-chips > b { color: var(--head); font-size: 14px; font-weight: 600; margin-right: 4px; }
    .pl-chip { min-height: 44px; padding: 0 14px; border-radius: 8px; background: var(--neutral05); color: var(--ink); font: inherit; font-weight: 500; }
    .pl-chip[aria-pressed="true"] { background: var(--md3-on-primary-container); color: var(--white); }
    .pl-chip.un { color: #8A5A00; }
    .pl-chip.un[aria-pressed="true"] { color: var(--white); }
    .pl-stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1px; background: var(--md3-surface-variant); border: 1px solid var(--md3-surface-variant); border-radius: 10px; overflow: hidden; }
    .pl-stats > div { display: grid; gap: 2px; padding: 10px 14px; background: var(--white); min-width: 0; }
    .pl-stats .cap { font-size: 13px; color: var(--md3-neutral-secondary); }
    .pl-stats .v { font-size: 20px; font-weight: 600; color: var(--head); font-variant-numeric: tabular-nums; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .pl-stats .v.g { color: var(--md3-on-primary-container); }
    .pl-stats .v.sm { font-size: 15px; }
    .pl-tabs { display: flex; gap: 4px; overflow-x: auto; border-bottom: 1px solid var(--md3-surface-variant); scrollbar-width: none; }
    .pl-tabs::-webkit-scrollbar { display: none; }
    .pl-tab { flex: none; min-height: 48px; padding: 0 16px; font: inherit; font-weight: 500; color: var(--ink); border-bottom: 3px solid transparent; white-space: nowrap; }
    .pl-tab[aria-selected="true"] { color: var(--md3-on-primary-container); border-bottom-color: var(--md3-on-primary-container); font-weight: 600; }
    .pl-body { display: grid; gap: 14px; min-width: 0; }
    .pl-ihead { display: flex; flex-wrap: wrap; align-items: center; gap: 10px 12px; }
    .pl-ihead h3 { display: flex; align-items: baseline; gap: 8px; color: var(--head); margin-right: auto; }
    .pl-ihead h3 span { color: var(--md3-neutral-secondary); font-weight: 500; font-size: 15px; }
    .pl-seg { display: inline-grid; grid-auto-flow: column; grid-auto-columns: auto; }
    .pl-seg button { min-height: 44px; padding: 0 12px; white-space: nowrap; }
    .pl-sel { min-width: 170px; }
    .pl-sel select { min-height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--head); font: inherit; width: 100%; }
    .pl-nodiet { display: inline-flex; align-items: center; gap: 6px; min-height: 32px; padding: 0 10px; border-radius: 6px; background: #FBE4E8; color: #A3122E; font-size: 13px; font-weight: 600; }
    .pl-tog { min-height: 44px; padding: 0 14px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); background: var(--white); color: var(--ink); font: inherit; font-weight: 500; }
    .pl-tog[aria-pressed="true"] { background: #FBE4E8; border-color: #F3B8C3; color: #A3122E; }
    .pl-did { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; font-weight: 600; color: var(--md3-on-primary-container); }
    .pl-did svg { transition: transform 160ms var(--ease); color: var(--ink); transform: rotate(180deg); }
    .pl-did[aria-expanded="true"] svg { transform: rotate(-90deg); }
    @media (prefers-reduced-motion: reduce) { .pl-did svg { transition: none; } }
    .pl-cert { display: flex; width: max-content; margin-left: 24px; height: 22px; align-items: center; padding: 0 8px; border-radius: 4px; font-size: 12px; font-weight: 600; background: #FFF1CC; color: #7A5600; }
    .pl-cert.ok { background: #E3F4EA; color: #1E6B3C; }
    .pl-sc { display: inline-flex; height: 24px; align-items: center; padding: 0 8px; border-radius: 4px; font-size: 13px; font-weight: 500; background: var(--md3-background); color: var(--ink); white-space: nowrap; }
    .pl-tg { display: block; color: var(--md3-neutral-secondary); font-size: 13px; margin-top: 2px; }
    .pl-alt { display: block; color: var(--md3-neutral-secondary); font-size: 12px; }
    .pl-dsub td { background: var(--md3-background); }
    .pl-ditems { display: grid; gap: 12px; padding: 4px 0; }
    .pl-dband { display: grid; gap: 6px; }
    .pl-dtime { display: inline-flex; align-items: center; gap: 6px; font-weight: 600; color: var(--head); }
    .pl-dday { font-size: 13px; font-weight: 600; color: var(--ink); margin-top: 4px; }
    .pl-dlist { display: grid; gap: 6px; list-style: none; margin: 0; padding: 0; }
    .pl-dlist li { padding: 8px 12px; border-radius: 8px; background: var(--white); display: grid; gap: 4px; }
    .pl-dlist .r { display: flex; flex-wrap: wrap; align-items: baseline; gap: 6px 10px; }
    .pl-dlist .nm { font-weight: 600; color: var(--head); }
    .pl-dlist .pp { color: var(--md3-neutral-secondary); font-size: 13px; }
    .pl-dlist .amt { margin-left: auto; font-weight: 600; color: var(--head); font-variant-numeric: tabular-nums; }
    .pl-dlist .mx, .pl-dlist .altn { font-size: 12px; font-weight: 600; padding: 1px 6px; border-radius: 4px; background: var(--md3-surface-variant); color: var(--md3-on-primary-container); }
    .pl-dlist .alts, .pl-dlist .pts { display: flex; flex-wrap: wrap; gap: 6px; font-size: 13px; color: var(--ink); }
    .pl-dlist .alts .lb { color: var(--md3-neutral-secondary); }
    .pl-dlist .ach { padding: 2px 8px; border-radius: 4px; background: #FFF6DB; color: #6B4E00; }
    .pl-dlist .ach .q { margin-left: 6px; color: var(--md3-neutral-secondary); }
    .pl-dnone { color: var(--md3-neutral-secondary); }
    .pl-sp b { display: block; color: var(--head); }
    .pl-sp em { display: block; color: var(--md3-neutral-secondary); font-size: 13px; }
    .pl-dchip { display: inline-flex; height: 24px; align-items: center; padding: 0 8px; border-radius: 4px; background: var(--md3-surface-variant); color: var(--md3-on-primary-container); font-size: 13px; font-weight: 600; white-space: nowrap; }
    .pl-dchip.no { background: #FBE4E8; color: #A3122E; }
    .pl-warn { color: #A3122E; font-weight: 600; }
    .pl-muted, .ktab td.pl-muted, .ktab tr.mut td { color: var(--md3-neutral-secondary); }
    .pl-ing { display: grid; gap: 2px; }
    .pl-ing .grp { margin-top: 10px; padding: 6px 0; font-size: 12px; font-weight: 700; letter-spacing: .04em; color: var(--md3-neutral-secondary); }
    .pl-ing .it { display: grid; grid-template-columns: minmax(0, 1fr) auto 48px; gap: 12px; align-items: center; min-height: 44px; padding: 0 12px; border-radius: 8px; background: var(--md3-background); color: var(--head); }
    .pl-ing .it small { color: var(--md3-neutral-secondary); font-size: 13px; }
    .pl-ing .it b { text-align: right; font-variant-numeric: tabular-nums; }
    .pl-row { display: flex; flex-wrap: wrap; align-items: flex-end; gap: 10px 12px; }
    .pl-row .sp { flex: 1; }
    .pl-date { display: inline-flex; align-items: stretch; border: 1px solid var(--md3-outline-variant); border-radius: 8px; background: var(--white); }
    .pl-date button { width: 44px; min-height: 44px; display: grid; place-items: center; color: var(--md3-on-primary-container); }
    .pl-date button.nx svg { transform: rotate(180deg); }
    .pl-date label { display: grid; align-content: center; padding: 0 8px; border-left: 1px solid var(--md3-surface-variant); border-right: 1px solid var(--md3-surface-variant); }
    .pl-date input { border: 0; background: none; font: inherit; color: var(--head); min-height: 26px; }
    .pl-date small { color: var(--md3-neutral-secondary); font-size: 12px; }
    .pl-bands { display: flex; flex-wrap: wrap; gap: 8px; }
    .pl-msg { color: var(--md3-neutral-secondary); padding: 8px 0; }
    .pl-ledger { display: grid; gap: 2px; }
    .pl-ledger b { color: var(--head); }
    .pl-ledger .sub { color: var(--md3-neutral-secondary); font-size: 13px; }
    .pl-ledger .amt { font-weight: 600; color: var(--md3-on-primary-container); font-variant-numeric: tabular-nums; }
    .pl-pills { display: flex; flex-wrap: wrap; gap: 6px; }
    .pl-pill { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 12px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); background: var(--white); font: inherit; color: var(--head); text-align: left; }
    .pl-pill .pa { font-weight: 600; color: var(--md3-on-primary-container); font-variant-numeric: tabular-nums; white-space: nowrap; }
    @media (hover: hover) { .pl-pill:hover { border-color: var(--md3-on-primary-container); } }
    .pl-totals { display: flex; flex-wrap: wrap; gap: 8px 20px; justify-content: flex-end; color: var(--head); }
    .pl-band { background: var(--md3-background); }
    .pl-band td { font-weight: 600; color: var(--head); }
    .pl-dt { display: grid; gap: 4px; }
    .pl-dt .kv { display: flex; justify-content: space-between; gap: 12px; color: var(--ink); }
    .pl-dt .kv b { color: var(--head); }
    @media (orientation: landscape) {
      .pl-pick { grid-template-columns: repeat(2, minmax(0, 320px)); }
      .pl-stats { grid-template-columns: repeat(var(--n), minmax(0, 1fr)); }
    }
''', 'js': r'''  (function () {
    var CLASSES = ['all', 'Mammalia', 'Aves', 'Reptilia', 'Other'], LEVELS = ['species', 'site', 'section', 'enclosure', 'animal'];
    var LEVEL_LABEL = { species: 'Species-wide', site: 'Site', section: 'Section', enclosure: 'Enclosure', animal: 'Animal' };
    var PRESETS = [['day', 'Today'], ['week', 'This week'], ['month', 'This month'], ['next7', 'Next 7 days'], ['next15', 'Next 15 days'], ['next30', 'Next 30 days']];
    var TABS = [['packaging', 'Packaging list'], ['diet', 'Diet'], ['species', 'Species'], ['ingredients', 'Ingredients'], ['enclosures', 'Enclosures'], ['forecast', 'Forecast'], ['pieces', 'Piece Weights']];
    var CAP = 40, D0 = null, st = null, body = null, DETAILS = [];
    function D() { if (!D0) D0 = MGSTORE.get('packaging-list'); return D0; }
    function S0() { if (!st) { var d = D(); st = { site: d.defaultSite, section: d.defaultSection || '', pick: 'all', tab: d.defaultTab || 'diet', cls: 'all', dScope: 'all', open: {}, spQ: '', spCls: 'all', noDiet: false, ingQ: '', encScope: 'all', pwView: 'all', pwQ: '', day: d.today, pack: false, band: 'all', fcPreset: 'day', fc: null, fcQ: '', more: {} }; } return st; }
    var byName = function (a, b) { return String(a).localeCompare(String(b), undefined, { numeric: true, sensitivity: 'base' }); };
    function tr(s) { return String(s || '').trim(); }
    function addDays(iso, n) { var d = new Date(iso + 'T00:00:00'); d.setDate(d.getDate() + n); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
    function wday(iso) { return new Date(iso + 'T00:00:00').toLocaleDateString('en-GB', { weekday: 'long' }); }
    /* Opens the Packaging list tab on one site and section (used by the Kitchen Operator's Requests view) */
    MGAPI.plOpen = function (site, section) { S0(); var d = D(); if (!d.sites.some(function (x) { return x.name === site; })) return; st.site = site; st.section = section || ''; st.pick = 'all'; st.tab = 'packaging'; st.pack = false; };
    function areas() { var a = MGAPI.areas ? MGAPI.areas() : null; return a && a.length ? a : D().areas; }
    function scope() {
      var d = D(), site = d.sites.filter(function (s) { return s.name === st.site; })[0] || d.sites[0], sec = st.section ? site.sections.filter(function (c) { return c.name === st.section; })[0] || null : null;
      var key = site.name + '|' + (sec ? sec.name : '*');
      return { site: site, section: sec, secs: sec ? [sec] : site.sections, data: d.scopes[key] || { diets: [], species: [], ingredients: [], enclosureSpecies: {}, pieceWeights: [], packaging: [], noDiet: null } };
    }
    function areaOf(site, secName, encName) {
      var a = areas().filter(function (x) { return x.active !== false && tr(x.site) === tr(site.name) && x.section === secName && (x.enclosures || []).indexOf(encName) !== -1; })[0];
      if (a) return a.name;
      var sec = site.sections.filter(function (c) { return c.name === secName; })[0], e = sec ? sec.encl.filter(function (x) { return x[0] === encName; })[0] : null;
      return e && e[1] ? e[1] : '';
    }
    function areaRec(site, secName, name) { return areas().filter(function (x) { return tr(x.site) === tr(site.name) && x.section === secName && x.name === name; })[0] || null; }
    function inPick(sc, secName, encName) { if (!sc.section || st.pick === 'all') return true; var a = areaOf(sc.site, secName, encName); return st.pick === '__un' ? !a : a === st.pick; }
    /* packaging rows name an enclosure as 'AG 4' (a section scope) or 'Agumbe › AG 4' (a site scope) */
    function splitEnc(sc, s) { var p = String(s).split(' › '); if (p.length > 1) return { sec: p[0], enc: p.slice(1).join(' › ') }; var sec = sc.section ? sc.section.name : ''; if (!sec) sc.site.sections.some(function (c) { if (c.encl.some(function (e) { return e[0] === s; })) { sec = c.name; return true; } return false; }); return { sec: sec, enc: s }; }
    /* quantities: weights in g, volumes in ml, other units kept apart */
    function base(q, u) { return u === 'kg' ? { v: q * 1000, f: 'g' } : u === 'ltr' ? { v: q * 1000, f: 'ml' } : { v: q, f: u }; }
    function qL(v, f) { var r = function (x) { return fmtN(Math.round(x * 100) / 100); }; return f === 'g' ? (v >= 1000 ? r(v / 1000) + ' kg' : r(v) + ' g') : f === 'ml' ? (v >= 1000 ? r(v / 1000) + ' ltr' : r(v) + ' ml') : r(v) + ' ' + f; }
    function totals(map) { return Object.keys(map).map(function (f) { return qL(map[f], f); }); }
    function stations() { try { return MGAPI.stations ? MGAPI.stations() : []; } catch (x) { return []; } }
    function stationFor(sec, enc) { var s = stations().filter(function (x) { return x.active !== false && (x.packages || []).some(function (p) { return p.enclosure === enc && (!p.section || p.section === sec); }); })[0]; return s ? s.name : ''; }
    function encSpecies(sc, secName, encName) { var m = sc.data.enclosureSpecies || {}; return m[encName] || m[secName + ' › ' + encName] || []; }
    function seg(key, opts, val) { return '<div class="seg3 pl-seg" role="tablist" aria-label="' + key + '">' + opts.map(function (o) { return '<button type="button" role="tab" class="t-body-medium" data-plseg="' + key + '" data-v="' + esc(o[0]) + '" aria-selected="' + (val === o[0]) + '">' + esc(o[1]) + '</button>'; }).join('') + '</div>'; }
    function search(key, ph, val) { return '<label class="mgsearch">' + ic('search', 20) + '<input type="search" data-plq="' + key + '" placeholder="' + esc(ph) + '" value="' + esc(val) + '" aria-label="' + esc(ph) + '" autocomplete="off"></label>'; }
    function capRows(key, list) { var open = st.more[key] || list.length <= CAP + 1; return { rows: open ? list : list.slice(0, CAP), more: list.length > CAP + 1 ? '<button type="button" class="linkbtn t-body-medium kmore" data-plmore="' + key + '">' + (st.more[key] ? 'Show fewer' : 'Show all ' + list.length) + '</button>' : '' }; }

    function top(sc) {
      var site = sc.site, sec = sc.section, d = D();
      var siteSub = site.sections.length + ' sections · ' + fmtN(site.species) + ' species · ' + fmtN(site.animals) + ' animals';
      var secAreas = sec ? areas().filter(function (a) { return tr(a.site) === tr(site.name) && a.section === sec.name; }) : [];
      var secSub = sec ? secAreas.length + ' area' + (secAreas.length === 1 ? '' : 's') + ' · ' + sec.species + ' species · ' + fmtN(sec.animals) + ' animals' : site.sections.length + ' sections';
      var h = '<section class="drow pl-scope"><div class="pl-pick">' +
        '<label class="mgf"><span>Site</span><select data-plsite>' + d.sites.map(function (s) { return '<option value="' + esc(s.name) + '"' + (s.name === site.name ? ' selected' : '') + '>' + esc(tr(s.name)) + '</option>'; }).join('') + '</select><small>' + esc(siteSub) + '</small></label>' +
        '<label class="mgf"><span>Section</span><select data-plsec><option value="">All sections</option>' + site.sections.map(function (c) { return '<option value="' + esc(c.name) + '"' + (sec && c.name === sec.name ? ' selected' : '') + '>' + esc(c.name) + '</option>'; }).join('') + '</select><small>' + esc(secSub) + '</small></label></div>';
      if (sec) {
        var un = sec.encl.filter(function (e) { return !areaOf(site, sec.name, e[0]); }).length;
        h += '<div class="pl-chips" role="group" aria-label="Keeper areas"><b>Keeper areas</b><button type="button" class="pl-chip" data-plpick="all" aria-pressed="' + (st.pick === 'all') + '">All</button>' +
          secAreas.map(function (a) { return '<button type="button" class="pl-chip" data-plpick="' + esc(a.name) + '" aria-pressed="' + (st.pick === a.name) + '">' + esc(a.name) + '</button>'; }).join('') +
          (un ? '<button type="button" class="pl-chip un" data-plpick="__un" aria-pressed="' + (st.pick === '__un') + '">Unassigned · ' + un + '</button>' : '') + '</div>';
      }
      var encN = sc.secs.reduce(function (n, c) { return n + c.encl.length; }, 0), areasN = areas().filter(function (a) { return tr(a.site) === tr(site.name) && (!sec || a.section === sec.name); }).length;
      var cells = [['Species', sec ? sec.species : site.species, 1], ['Diets', sc.data.diets.length, 0], ['Enclosures', encN, 1], ['Animals', sec ? sec.animals : site.animals, 1], ['Keeper areas', areasN, 0]];
      if (sec) cells.push(['Supervisor', sec.supervisor || '-', 0]);
      h += '<div class="pl-stats" style="--n:' + cells.length + '">' + cells.map(function (x) { var num = typeof x[1] === 'number'; return '<div><span class="cap">' + x[0] + '</span><span class="v' + (num && x[2] && x[1] > 0 ? ' g' : '') + (num ? '' : ' sm') + '">' + (num ? fmtN(x[1]) : esc(x[1])) + '</span></div>'; }).join('') + '</div></section>';
      return h;
    }

    /* ---- Packaging list: calculated for a date, by feeding time; Pack item | Deliver to ---- */
    function packRows(sc) { return (sc.data.packaging || []).map(function (p) { var e = splitEnc(sc, p.enclosure); return { feeding: p.feeding, sec: e.sec, enc: e.enc, items: p.items }; }).filter(function (r) { return inPick(sc, r.sec, r.enc); }); }
    function packItems(rows) {
      var m = {}, order = [];
      rows.forEach(function (r) { r.items.forEach(function (it) { var b = base(it.qty, it.unit), k = it.name + '|' + (it.prep || '') + '|' + b.f;
        if (!m[k]) { m[k] = { name: it.name, prep: it.prep || '', f: b.f, amount: 0, dest: {} }; order.push(k); }
        m[k].amount += b.v; var dk = r.sec + '|' + r.enc; (m[k].dest[dk] = m[k].dest[dk] || { sec: r.sec, enc: r.enc, amount: 0, feeding: r.feeding }).amount += b.v; }); });
      return order.map(function (k) { return m[k]; });
    }
    function T_packaging(sc) {
      DETAILS = [];
      var all = packRows(sc), bands = all.map(function (r) { return r.feeding; }).filter(function (v, i, a) { return a.indexOf(v) === i; }).sort();
      var h = '<div class="pl-row"><div class="pl-date" role="group" aria-label="Date"><button type="button" data-plday="-1" aria-label="Previous day">' + ic('back', 20) + '</button><label><input type="date" data-plq="day" value="' + esc(st.day) + '" aria-label="Date"><small>' + esc(st.day ? wday(st.day) : 'Pick a date') + '</small></label><button type="button" class="nx" data-plday="1" aria-label="Next day">' + ic('back', 20) + '</button></div>' +
        '<span class="sp"></span><button type="button" class="btn pri ksm" data-plcalc' + (st.day ? '' : ' disabled') + '>Calculate packaging list</button></div>';
      if (!st.pack) return h + '<p class="pl-msg">Select the location and dates, then calculate.</p>';
      if (!all.length) return h + '<p class="pl-msg">No items to pack for these dates and location.</p>';
      h += '<div class="pl-bands" role="group" aria-label="Feeding time">' + ['all'].concat(bands).map(function (b) { return '<button type="button" class="pl-chip" data-plband="' + esc(b) + '" aria-pressed="' + (st.band === b) + '">' + esc(b === 'all' ? 'All times' : b) + '</button>'; }).join('') + '</div>';
      var rows = all.filter(function (r) { return st.band === 'all' || r.feeding === st.band; }), items = packItems(rows), bySec = !sc.section && new Set(rows.map(function (r) { return r.sec; })).size > 1, tot = {};
      items.forEach(function (g) { tot[g.f] = (tot[g.f] || 0) + g.amount; });
      h += '<div class="ktabwrap"><table class="ktab t-body-regular" aria-label="Keeper packaging list"><thead><tr><th>Pack item</th><th>Deliver to</th></tr></thead><tbody>' + items.map(function (g) {
        var lines = [], dests = Object.keys(g.dest).map(function (k) { return g.dest[k]; });
        if (bySec) { var bs = {}; dests.forEach(function (x) { (bs[x.sec] = bs[x.sec] || { name: x.sec, amount: 0, list: [] }).amount += x.amount; bs[x.sec].list.push(x); }); Object.keys(bs).sort(byName).forEach(function (k) { lines.push(bs[k]); }); }
        else dests.sort(function (a, b) { return byName(a.enc, b.enc); }).forEach(function (x) { lines.push({ name: x.enc, amount: x.amount, list: [x] }); });
        return '<tr><td><div class="pl-ledger"><b>' + esc(g.name) + '</b>' + (g.prep ? '<span class="sub">' + esc(g.prep) + '</span>' : '') + '<span class="amt">' + esc(qL(g.amount, g.f)) + '</span></div></td><td><div class="pl-pills">' + lines.map(function (l) {
          DETAILS.push({ item: g.name, prep: g.prep, f: g.f, band: st.band, dest: l.name, amount: l.amount, list: l.list, bySec: bySec });
          return '<button type="button" class="pl-pill" data-pldet="' + (DETAILS.length - 1) + '" aria-label="' + esc(l.name + ', ' + qL(l.amount, g.f)) + '"><span>' + esc(l.name) + '</span><span class="pa">' + esc(qL(l.amount, g.f)) + '</span></button>'; }).join('') + '</div></td></tr>';
      }).join('') + '</tbody></table></div>' +
        '<div class="pl-totals">' + totals(tot).map(function (t) { return '<b>Total: ' + esc(t) + '</b>'; }).join('') + '</div>' +
        '<p class="kcap t-body-regular">' + ic('info', 16) + 'Weights are shown in kg/gm and volumes in ltr/ml. Count-only items retain their configured unit. SAMPLE DATA: the packaging captured for ' + esc(fmtD(D().today)) + ' is used for every date.</p>';
      return h;
    }
    function openDetail(i, sc) {
      var d = DETAILS[i]; if (!d) return;
      var keepers = {};
      d.list.forEach(function (x) { var a = areaOf(sc.site, x.sec, x.enc), r = a ? areaRec(sc.site, x.sec, a) : null; (r && r.keepers || []).forEach(function (k) { keepers[k] = 1; }); });
      var kp = Object.keys(keepers).sort();
      var rows = d.list.slice().sort(function (a, b) { return byName(a.enc, b.enc); }).map(function (x) {
        var sp = encSpecies(sc, x.sec, x.enc), stn = stationFor(x.sec, x.enc);
        return '<tr><td><b>' + esc(x.enc) + '</b>' + (d.bySec ? '<small>' + esc(x.sec) + '</small>' : '') + (stn ? '<small>Packed at ' + esc(stn) + '</small>' : '') + '</td><td>' + (sp.length ? sp.map(function (p) { return esc(p[0]) + ' <span class="pl-muted">' + p[1] + '</span>'; }).join(', ') : '<span class="pl-muted">-</span>') + '</td><td class="r"><b>' + esc(qL(x.amount, d.f)) + '</b></td></tr>'; }).join('');
      mgSheet(mgSheetHead(d.item + (d.prep ? ' · ' + d.prep : ''), [d.band === 'all' ? 'All times' : d.band, fmtD(st.day), d.dest].join(' · ')) +
        '<div class="pl-dt"><div class="kv"><span>Deliver to</span><b>' + esc(d.dest) + '</b></div><div class="kv"><span>Amount</span><b>' + esc(qL(d.amount, d.f)) + '</b></div>' + (kp.length ? '<div class="kv"><span>' + (kp.length === 1 ? 'Keeper' : 'Keepers') + '</span><b>' + esc(kp.join(', ')) + '</b></div>' : '') + '</div>' +
        '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Enclosure</th><th>Species · Animals</th><th class="r">Amount</th></tr></thead><tbody>' + rows + '</tbody></table></div>' +
        '<div class="sheet__f"><button type="button" class="btn sec" data-mgclose>Close</button></div>', 'Delivery');
    }

    /* ---- Diet ---- */
    function kind(x) { var s = String(x.scope || '').toLowerCase(); return s.indexOf('species') === 0 ? 'species' : s.indexOf('animal') === 0 ? 'animal' : LEVELS.indexOf(s) !== -1 ? s : 'species'; }
    function plan(x) { var p = D().dietSchedules[x.id]; return p && p.schedule ? p : null; }
    function altCount(x) { var p = plan(x), n = 0; if (p) p.schedule.forEach(function (b) { (b.days || []).forEach(function (g) { (g.items || []).forEach(function (it) { n += (it.alts || []).length; }); }); }); return n; }
    function dietItems(x) {
      var p = plan(x); if (!p || !p.schedule.length) return '<p class="pl-dnone">No item list stored for ' + esc(x.id) + '.</p>';
      var cols = p.columns || [];
      return p.schedule.map(function (band) {
        var days = band.days || [], split = days.length > 1 || (days[0] && days[0].day !== 'Daily');
        return '<div class="pl-dband"><div class="pl-dtime">' + ic('time', 16) + esc(band.time) + '</div>' + days.map(function (g) {
          return (split ? '<div class="pl-dday">' + esc(g.day) + '</div>' : '') + '<ul class="pl-dlist">' + (g.items || []).map(function (it) {
            var m = it.mix, meta = [], na = (it.alts || []).length;
            if (it.prep) meta.push(esc(it.prep)); if (it.cutSize || it.cut) meta.push('Cut ' + esc(it.cutSize || it.cut));
            var extra = cols.map(function (c, i) { var v = (it.extra || [])[i]; return v ? '<span>' + esc(c) + ' <b>' + esc(v) + '</b></span>' : ''; }).join('');
            return '<li><div class="r"><span class="nm">' + esc(it.name) + '</span>' + (m ? '<span class="mx">Mix</span>' : '') + (na ? '<span class="altn">' + na + ' alt</span>' : '') + (meta.length ? '<span class="pp">' + meta.join(' · ') + '</span>' : '') + (m && m.meta ? '<span class="pp">' + esc(m.meta) + '</span>' : '') + '<span class="amt">' + esc(it.amount || '') + '</span></div>' +
              (extra ? '<div class="pts">' + extra + '</div>' : '') + (m && m.parts && m.parts.length ? '<div class="pts">' + m.parts.map(function (q) { if (typeof q === 'string') q = { name: q }; return '<span>' + esc(q.name) + (q.note ? ' <em>' + esc(q.note) + '</em>' : '') + '</span>'; }).join('') + '</div>' : '') +
              (na ? '<div class="alts"><span class="lb">Alternatives</span>' + it.alts.map(function (a) { if (typeof a === 'string') a = { name: a }; return '<span class="ach">or <b>' + esc(a.name) + '</b>' + (a.prep ? ' <em>' + esc(a.prep) + '</em>' : '') + '<span class="q">' + esc(a.amount || a.ratio || 'same qty') + '</span></span>'; }).join('') + '</div>' : '') + '</li>';
          }).join('') + '</ul>';
        }).join('') + '</div>';
      }).join('');
    }
    function T_diet(sc) {
      var all = sc.data.diets || [], rows = all.filter(function (x) { return (st.cls === 'all' || (x.classes || []).indexOf(st.cls) !== -1) && (st.dScope === 'all' || kind(x) === st.dScope); });
      var kinds = {}; all.forEach(function (x) { var k = kind(x); kinds[k] = (kinds[k] || 0) + 1; });
      var nd = sc.data.noDiet, anyOpen = rows.some(function (x) { return st.open[x.id]; });
      return '<div class="pl-ihead"><h3 class="t-minor-title">Diets<span>' + rows.length + ' of ' + all.length + '</span></h3>' + (nd ? '<span class="pl-nodiet">' + ic('alert', 16) + 'No diet · ' + nd.species + ' species · ' + fmtN(nd.animals) + ' animals</span>' : '') + '</div>' +
        '<div class="mgbar">' + seg('cls', CLASSES.map(function (c) { return [c, c === 'all' ? 'All' : c]; }), st.cls) +
          '<label class="pl-sel"><select data-pldscope aria-label="Plan scope"><option value="all">All scopes</option>' + LEVELS.map(function (k) { return '<option value="' + k + '"' + (st.dScope === k ? ' selected' : '') + '>' + LEVEL_LABEL[k] + (kinds[k] ? ' (' + kinds[k] + ')' : '') + '</option>'; }).join('') + '</select></label>' +
          (rows.length ? '<button type="button" class="btn sec ksm" data-plexpall="' + (anyOpen ? '0' : '1') + '">' + (anyOpen ? 'Collapse all' : 'Expand all') + '</button>' : '') + '</div>' +
        '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Diet</th><th>Scope</th><th class="r">Time blocks</th><th class="r">Items</th><th class="r">Species</th><th class="r">Animals</th><th class="r">Encl</th><th class="r">Keeper areas</th><th class="r">Sections</th></tr></thead><tbody>' +
        (rows.length ? rows.map(function (x) { var open = !!st.open[x.id], na = altCount(x);
          return '<tr><td><button type="button" class="pl-did" data-pldiet="' + esc(x.id) + '" aria-expanded="' + open + '">' + ic('back', 16) + esc(x.id) + '</button><span class="pl-cert' + (x.certified ? ' ok' : '') + '">' + (x.certified ? 'Certified' : 'Not certified') + '</span></td>' +
            '<td><span class="pl-sc">' + esc(LEVEL_LABEL[kind(x)]) + '</span>' + (x.target ? '<span class="pl-tg">' + esc(x.target) + '</span>' : '') + '</td><td class="r">' + x.timeBlocks + '</td><td class="r"><b>' + x.items + '</b>' + (na ? '<span class="pl-alt">+' + na + ' alt</span>' : '') + '</td>' +
            '<td class="r">' + x.species + '</td><td class="r">' + fmtN(x.animals) + '</td><td class="r">' + (x.enclApprox ? '≈' : '') + x.encl + '</td><td class="r">' + x.keeperAreas + '</td><td class="r">' + x.sections + '</td></tr>' +
            (open ? '<tr class="pl-dsub"><td colspan="9"><div class="pl-ditems">' + dietItems(x) + '</div></td></tr>' : ''); }).join('')
          : '<tr><td colspan="9" class="pl-muted">' + (all.length ? 'No diets match these filters.' : 'No diets.') + '</td></tr>') + '</tbody></table></div>';
    }
    /* ---- Species ---- */
    function T_species(sc) {
      var all = sc.data.species || [], q = st.spQ.trim().toLowerCase();
      var list = all.filter(function (x) { return (st.spCls === 'all' || x[2] === st.spCls || (st.spCls === 'Other' && ['Mammalia', 'Aves', 'Reptilia'].indexOf(x[2]) === -1)) && (!st.noDiet || x[4] > 0) && (!q || (x[0] + ' ' + (x[1] || '') + ' ' + (x[3] || '')).toLowerCase().indexOf(q) !== -1); });
      var C = capRows('sp', list);
      return '<div class="pl-ihead"><h3 class="t-minor-title">Species<span>' + all.length + '</span></h3></div><div class="mgbar">' + search('sp', 'Search species or diet', st.spQ) + seg('spCls', CLASSES.map(function (c) { return [c, c === 'all' ? 'All' : c]; }), st.spCls) +
        '<button type="button" class="pl-tog" data-plnodiet aria-pressed="' + st.noDiet + '">No diet</button></div>' +
        '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Species</th><th>Diet</th><th>Section</th><th class="r">Keeper areas</th><th class="r">Encl</th><th class="r">Animals</th></tr></thead><tbody>' +
        (C.rows.length ? C.rows.map(function (x) { return '<tr><td class="pl-sp"><b>' + esc(x[0]) + '</b><em>' + esc(x[1] || '') + '</em></td><td>' + (x[3] ? '<span class="pl-dchip">' + esc(x[3]) + '</span> ' : '') + (x[4] ? '<span class="pl-dchip no">' + x[4] + ' no diet</span>' : '') + (!x[3] && !x[4] ? '<span class="pl-muted">-</span>' : '') + '</td>' +
          '<td>' + esc(x[5] || '-') + '</td><td class="r' + (x[6] ? '' : ' pl-warn') + '">' + (x[6] || 0) + '</td><td class="r">' + (x[7] || 0) + '</td><td class="r">' + fmtN(x[8] || 0) + '</td></tr>'; }).join('')
          : '<tr><td colspan="6" class="pl-muted">' + (all.length ? 'No species match.' : 'No species.') + '</td></tr>') + '</tbody></table></div>' + C.more;
    }
    /* ---- Ingredients ---- */
    function T_ingredients(sc) {
      var groups = sc.data.ingredients || [], q = st.ingQ.trim().toLowerCase(), n = groups.reduce(function (k, g) { return k + g.items.length; }, 0);
      var bodyH = groups.map(function (g) { var its = g.items.filter(function (i) { return !q || i.name.toLowerCase().indexOf(q) !== -1; }); if (!its.length) return '';
        return '<div class="grp">' + esc(g.group) + '</div>' + its.map(function (i) { return '<div class="it t-body-regular"><span>' + esc(i.name) + '</span><small>' + esc(i.prep || '') + '</small><b>' + i.count + '</b></div>'; }).join(''); }).join('');
      return '<div class="pl-ihead"><h3 class="t-minor-title">Ingredients<span>' + n + ' unique items</span></h3></div><div class="mgbar">' + search('ing', 'Search ingredients', st.ingQ) + '</div>' +
        (bodyH ? '<div class="pl-ing">' + bodyH + '</div><p class="kcap t-body-regular">' + ic('info', 16) + 'The number is how many diets in this scope ask for the item (alternatives not counted).</p>' : '<p class="pl-msg">' + (n ? 'No ingredients match.' : 'No ingredients.') + '</p>');
    }
    /* ---- Enclosures ---- */
    function T_enclosures(sc) {
      var list = []; sc.secs.forEach(function (c) { c.encl.forEach(function (e) { if (inPick(sc, c.name, e[0])) list.push({ sec: c.name, e: e, area: areaOf(sc.site, c.name, e[0]) }); }); });
      var rows = list.filter(function (x) { return st.encScope === 'all' || (st.encScope === 'assigned' ? !!x.area : !x.area); }), C = capRows('enc', rows);
      return '<div class="pl-ihead"><h3 class="t-minor-title">Enclosures<span>' + list.length + '</span></h3>' + seg('encScope', [['assigned', 'Assigned'], ['unassigned', 'Unassigned'], ['all', 'All enclosures']], st.encScope) + '</div>' +
        '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Enclosure</th>' + (sc.section ? '' : '<th>Section</th>') + '<th>Keeper area</th><th>Species · Animals</th></tr></thead><tbody>' +
        (C.rows.length ? C.rows.map(function (x) { var sp = encSpecies(sc, x.sec, x.e[0]).slice().sort(function (p, q) { return byName(p[0], q[0]); }), e = x.e;
          var cell = sp.length ? sp.map(function (p) { return esc(p[0]) + ' <span class="pl-muted">' + p[1] + '</span>'; }).join(' · ') : (e[3] ? (e[2] || 0) + ' species · ' + fmtN(e[3]) + ' animals' : '-');
          return '<tr' + (e[3] || sp.length ? '' : ' class="mut"') + '><td><b>' + esc(e[0]) + '</b></td>' + (sc.section ? '' : '<td>' + esc(x.sec) + '</td>') + '<td' + (x.area ? '' : ' class="pl-muted"') + '>' + esc(x.area || 'Unassigned') + '</td><td>' + cell + '</td></tr>'; }).join('')
          : '<tr><td colspan="4" class="pl-muted">No enclosures.</td></tr>') + '</tbody></table></div>' + C.more;
    }
    /* ---- Forecast: the daily packaging times the days of the period ---- */
    function presetRange(p, anchor) {
      var d = new Date(anchor + 'T00:00:00'), from = new Date(d), to = new Date(d), iso = function (x) { return x.getFullYear() + '-' + ('0' + (x.getMonth() + 1)).slice(-2) + '-' + ('0' + x.getDate()).slice(-2); };
      if (p === 'week') { from.setDate(d.getDate() - (d.getDay() + 6) % 7); to = new Date(from); to.setDate(from.getDate() + 6); }
      if (p === 'month') { from.setDate(1); to = new Date(d.getFullYear(), d.getMonth() + 1, 0); }
      if (p.indexOf('next') === 0) to.setDate(d.getDate() + Number(p.slice(4)) - 1);
      return { from: iso(from), to: iso(to) };
    }
    function T_forecast(sc) {
      var R = presetRange(st.fcPreset, D().today), days = Math.round((new Date(R.to) - new Date(R.from)) / 864e5) + 1;
      var h = '<div class="pl-row"><label class="mgf pl-sel"><span>Period</span><select data-plfc>' + PRESETS.map(function (p) { return '<option value="' + p[0] + '"' + (p[0] === st.fcPreset ? ' selected' : '') + '>' + p[1] + '</option>'; }).join('') + '</select><small>' + esc((R.from === R.to ? fmtD(R.from) : fmtD(R.from) + ' to ' + fmtD(R.to)) + ' · ' + days + ' day' + (days === 1 ? '' : 's')) + '</small></label>' +
        '<span class="sp"></span><button type="button" class="btn pri ksm" data-plfccalc>Calculate forecast</button></div>';
      if (!st.fc) return h + '<p class="pl-msg">Select the location and dates, then calculate.</p>';
      var rows = packRows(sc); if (!rows.length) return h + '<p class="pl-msg">No material requirements for these dates and location.</p>';
      var grpOf = {}; (sc.data.ingredients || []).forEach(function (g) { g.items.forEach(function (i) { grpOf[i.name] = g.group; }); });
      var items = packItems(rows), q = st.fcQ.trim().toLowerCase(), cats = {}, tot = {};
      items.filter(function (g) { return !q || g.name.toLowerCase().indexOf(q) !== -1; }).forEach(function (g) {
        var sp = {}, an = 0; Object.keys(g.dest).forEach(function (k) { var x = g.dest[k]; encSpecies(sc, x.sec, x.enc).forEach(function (p) { sp[p[0]] = 1; an += p[1]; }); });
        var c = grpOf[g.name] || 'OTHER', row = { name: g.name + (g.prep ? ' · ' + g.prep : ''), sp: Object.keys(sp).length, an: an, f: g.f, amount: g.amount * st.fc.days };
        (cats[c] = cats[c] || { label: c, items: [], tot: {} }).items.push(row); cats[c].tot[g.f] = (cats[c].tot[g.f] || 0) + row.amount; tot[g.f] = (tot[g.f] || 0) + row.amount; });
      var keys = Object.keys(cats).sort(function (a, b) { return (a === 'MIXES & RECIPES' ? 1 : 0) - (b === 'MIXES & RECIPES' ? 1 : 0) || a.localeCompare(b); });
      return h + '<p class="kcap t-body-regular">' + esc(fmtD(st.fc.from) + ' to ' + fmtD(st.fc.to)) + ' · Calculated ' + esc(st.fc.at) + '. Animal locations and headcounts reflect the current collection.</p>' +
        '<div class="mgbar">' + search('fc', 'Search ingredients', st.fcQ) + '</div>' +
        '<div class="ktabwrap"><table class="ktab t-body-regular" aria-label="Material forecast"><thead><tr><th>Item</th><th class="r">Species</th><th class="r">Animals</th><th class="r">Total</th></tr></thead><tbody>' +
        keys.map(function (k) { var c = cats[k]; return '<tr class="pl-band"><td colspan="3">' + esc(c.label) + '</td><td class="r">' + esc(totals(c.tot).join(' · ')) + '</td></tr>' +
          c.items.map(function (r) { return '<tr><td>' + esc(r.name) + '</td><td class="r">' + r.sp + '</td><td class="r">' + fmtN(r.an) + '</td><td class="r"><b>' + esc(qL(r.amount, r.f)) + '</b></td></tr>'; }).join(''); }).join('') + '</tbody></table></div>' +
        '<div class="pl-totals">' + totals(tot).map(function (t) { return '<b>Total: ' + esc(t) + '</b>'; }).join('') + '</div>' +
        '<p class="kcap t-body-regular">' + ic('info', 16) + 'Weights below 1 kg are shown in gm; volumes below 1 ltr in ml. Larger quantities use kg/ltr. SAMPLE DATA: the daily packaging times the days of the period.</p>';
    }
    /* ---- Piece Weights: the cut sizes this scope's diets ask for, with the weights from the Piece Weights page ---- */
    function T_pieces(sc) {
      var PW = mgPieceWeights(), all = (sc.data.pieceWeights || []).map(function (r) { var m = PW.filter(function (p) { return p.name === r.name && (p.cutSize || '-') === (r.cutSize || '-'); })[0]; return m ? Object.assign({}, r, { weight: m.weight, status: m.status }) : r; });
      var q = st.pwQ.trim().toLowerCase(), n = { missing: 0, set: 0, counted: 0 }; all.forEach(function (r) { n[r.status] = (n[r.status] || 0) + 1; });
      var rows = all.filter(function (r) { return (st.pwView === 'all' || r.status === st.pwView) && (!q || r.name.toLowerCase().indexOf(q) !== -1); }), ed = canEdit() && !!MGP['piece-weights'];
      return '<div class="pl-ihead"><h3 class="t-minor-title">Piece weights, ' + esc(sc.section ? sc.section.name : tr(sc.site.name)) + '<span>' + all.length + '</span></h3></div><div class="mgbar">' +
        seg('pwView', [['missing', 'Missing ' + n.missing], ['set', 'Set ' + n.set], ['counted', 'Counted ' + n.counted], ['all', 'All']], st.pwView) + search('pw', 'Search ingredient', st.pwQ) + '</div>' +
        '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Item</th><th>Main UOM</th><th>Cut size</th><th class="r">1 piece =</th><th class="r">Used in</th>' + (ed ? '<th></th>' : '') + '</tr></thead><tbody>' +
        (rows.length ? rows.map(function (r) { return '<tr><td><b>' + esc(r.name) + '</b></td><td>' + esc(r.uom) + '</td><td>' + esc(r.cutSize || '-') + '</td><td class="r">' + (r.status === 'counted' ? '<span class="pl-muted">counted</span>' : r.weight != null ? fmtN(r.weight) + ' g' : '<span class="pl-warn">Missing</span>') + '</td><td class="r">' + (r.usedIn || 0) + '</td>' +
          (ed ? '<td class="r"><button type="button" class="btn sec ksm" data-plpw>' + (r.weight != null ? 'Edit' : 'Set weight') + '</button></td>' : '') + '</tr>'; }).join('')
          : '<tr><td colspan="' + (ed ? 6 : 5) + '" class="pl-muted">' + (all.length ? 'Nothing in this view.' : 'No diet in this scope asks for anything by the piece.') + '</td></tr>') + '</tbody></table></div>' +
        '<p class="kcap t-body-regular">' + ic('info', 16) + 'Only the ingredients this scope\'s diets ask for by the piece, and only the cut sizes those diets name, ingredients reached through a mix included.</p>';
    }
    var T = { packaging: T_packaging, diet: T_diet, species: T_species, ingredients: T_ingredients, enclosures: T_enclosures, forecast: T_forecast, pieces: T_pieces };

    function draw(b) {
      body = b || body; S0(); var sc = scope();
      body.innerHTML = '<div class="mgpane">' + top(sc) + '<section class="drow pl-body"><nav class="pl-tabs" role="tablist" aria-label="Packaging list views">' + TABS.map(function (t) { return '<button type="button" role="tab" class="pl-tab" data-pltab="' + t[0] + '" aria-selected="' + (st.tab === t[0]) + '">' + t[1] + '</button>'; }).join('') + '</nav>' + T[st.tab](sc) + '</section></div>';
      var on = body.querySelector('.pl-tab[aria-selected="true"]'); if (on && on.scrollIntoView) { var nav = on.parentNode; nav.scrollLeft = Math.max(0, on.offsetLeft - nav.clientWidth / 2 + on.clientWidth / 2); }
    }
    function reset() { st.pick = 'all'; st.pack = false; st.band = 'all'; st.fc = null; st.open = {}; st.more = {}; }
    function refocus(key) { var i = body.querySelector('[data-plq="' + key + '"]'); if (i) { i.focus(); var v = i.value; try { i.setSelectionRange(v.length, v.length); } catch (x) {} } }
    var qT;
    MGP['packaging-list'] = { title: 'Packaging list', sub: 'What to pack for each enclosure, by feeding time', draw: draw,
      click: function (e) { var t, sc = scope();
        if ((t = e.target.closest('[data-pltab]'))) { st.tab = t.getAttribute('data-pltab'); draw(); return; }
        if ((t = e.target.closest('[data-plpick]'))) { st.pick = t.getAttribute('data-plpick'); st.pack = false; st.fc = null; st.band = 'all'; draw(); return; }
        if ((t = e.target.closest('[data-plseg]'))) { st[t.getAttribute('data-plseg')] = t.getAttribute('data-v'); st.more = {}; draw(); return; }
        if (e.target.closest('[data-plnodiet]')) { st.noDiet = !st.noDiet; draw(); return; }
        if ((t = e.target.closest('[data-pldiet]'))) { var id = t.getAttribute('data-pldiet'); st.open[id] = !st.open[id]; draw(); return; }
        if ((t = e.target.closest('[data-plexpall]'))) { var openAll = t.getAttribute('data-plexpall') === '1'; st.open = {}; if (openAll) (sc.data.diets || []).forEach(function (x) { st.open[x.id] = true; }); draw(); return; }
        if ((t = e.target.closest('[data-plmore]'))) { var k = t.getAttribute('data-plmore'); st.more[k] = !st.more[k]; draw(); return; }
        if ((t = e.target.closest('[data-plday]'))) { st.day = addDays(st.day || D().today, Number(t.getAttribute('data-plday'))); st.pack = false; st.band = 'all'; draw(); return; }
        if (e.target.closest('[data-plcalc]')) { st.pack = true; var bs = packRows(sc).map(function (r) { return r.feeding; }).sort(); st.band = bs[0] || 'all'; draw(); return; }
        if ((t = e.target.closest('[data-plband]'))) { st.band = t.getAttribute('data-plband'); draw(); return; }
        if ((t = e.target.closest('[data-pldet]'))) { openDetail(Number(t.getAttribute('data-pldet')), sc); return; }
        if (e.target.closest('[data-plfccalc]')) { var R = presetRange(st.fcPreset, D().today); st.fc = { from: R.from, to: R.to, days: Math.round((new Date(R.to) - new Date(R.from)) / 864e5) + 1, at: new Date().toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) }; draw(); return; }
        if (e.target.closest('[data-plpw]')) { MGPUSHED = true; location.hash = '#meal-groups/piece-weights'; return; }
      },
      change: function (e) { var t = e.target;
        if (t.matches('[data-plsite]')) { st.site = t.value; st.section = ''; reset(); draw(); }
        else if (t.matches('[data-plsec]')) { st.section = t.value; reset(); draw(); }
        else if (t.matches('[data-pldscope]')) { st.dScope = t.value; draw(); }
        else if (t.matches('[data-plfc]')) { st.fcPreset = t.value; st.fc = null; draw(); }
        else if (t.matches('[data-plq="day"]')) { st.day = t.value; st.pack = false; st.band = 'all'; draw(); }
      },
      input: function (e) { var t = e.target, k = t.getAttribute('data-plq'); if (!k || k === 'day') return; clearTimeout(qT); var v = t.value;
        qT = setTimeout(function () { st[{ sp: 'spQ', ing: 'ingQ', pw: 'pwQ', fc: 'fcQ' }[k]] = v; st.more = {}; draw(); refocus(k); }, 150); } };
  })();
'''}
