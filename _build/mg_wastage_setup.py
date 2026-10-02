# mg_wastage_setup.py: exec'd by kitchen.py. Meal Group Management > Wastage setup.
# Source: Dev system_local kitchen/wastage-setup.{html,js,css,data.js} + kitchen-store.js (dated snapshot model) + sites.data.js
# (site > section > enclosure) + keeper-areas.data.js. How wastage is weighed and recorded per keeper area, with per-enclosure
# "own settings". Site and section pickers (the source's rail), summary strip, filters, collapsible keeper-area groups.
# Picking one keeper area of a section opens it for editing (kitchen roles): change the area default, change one or ticked
# enclosures, use area default, then Save setup with a "Takes effect from" date (appends one dated snapshot per changed area,
# Undo in the toast). History sheets per area, per enclosure and for the whole scope.
# Saved in MGSTORE 'wastage-setup' (only the setups change). Keeper areas: MGAPI.keeperAreas() when the Keeper Areas page
# offers it ([{ site, section, name, enclosures: [names], active }]), else the areas in the seed.
MGMOD = {'icons': ['search', 'history', 'pencil', 'dropdown', 'info'], 'css': '''    /* Wastage setup */
    .ws-pick { display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .ws-pick small { color: var(--md3-neutral-secondary); font-size: 13px; }
    .ws-sum { display: grid; gap: 1px; grid-template-columns: repeat(3, minmax(0, 1fr)); background: var(--md3-surface-variant); border-radius: var(--radius); overflow: hidden; }
    .ws-sum div { background: var(--white); padding: 12px 14px; display: grid; gap: 2px; }
    .ws-sum small { color: var(--ink); font-size: 13px; }
    .ws-sum b { color: var(--head); font-size: 17px; font-weight: 600; font-variant-numeric: tabular-nums; }
    .ws-sum b.big { font-size: 22px; }
    .ws-chips { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }
    .ws-chips > b { color: var(--head); margin-right: 4px; }
    .ws-chip { min-height: 44px; padding: 0 14px; border-radius: 22px; border: 1px solid var(--md3-outline-variant); background: var(--white); color: var(--ink); font: inherit; font-weight: 500; }
    .ws-chip[aria-pressed="true"] { background: var(--md3-on-primary-container); border-color: var(--md3-on-primary-container); color: var(--white); }
    .ws-scope { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; }
    .ws-scope .nm { color: var(--head); font-weight: 600; font-size: 17px; }
    .ws-scope .meta { color: var(--md3-neutral-secondary); font-size: 13px; display: block; }
    .ws-scope .sp { flex: 1; }
    .ws-filters { display: flex; flex-wrap: wrap; gap: 8px 12px; align-items: center; }
    .ws-filters select { min-height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--head); font: inherit; }
    .ws-note { display: flex; align-items: center; gap: 6px; color: var(--md3-neutral-secondary); font-size: 14px; }
    .ws-ticked { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; padding: 8px 8px 8px 16px; border-radius: var(--radius); background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); font-weight: 600; }
    .ws-ticked .sp { flex: 1; }
    .ws-group { background: var(--white); border-radius: var(--radius); border: 1px solid transparent; }
    .ws-group.chg { border-color: #E3B341; }
    .ws-gh { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 10px; padding: 10px 14px; }
    .ws-gh .tg { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; font: inherit; font-weight: 600; color: var(--head); text-align: left; }
    .ws-gh .tg svg { transition: transform 150ms; }
    .ws-gh .tg[aria-expanded="false"] svg { transform: rotate(-90deg); }
    .ws-gh .ttl { display: grid; } .ws-gh .ttl small { color: var(--md3-neutral-secondary); font-size: 12px; } .ws-gh .ttl b { color: var(--head); }
    .ws-gh .cnt { color: var(--md3-neutral-secondary); font-size: 13px; }
    .ws-gh .sp { flex: 1; }
    .ws-kvs { display: flex; flex-wrap: wrap; gap: 6px; flex-basis: 100%; }
    .ws-kv { display: inline-flex; align-items: center; height: 28px; padding: 0 8px; border-radius: 4px; background: var(--md3-background); color: var(--ink); font-size: 13px; }
    .ws-kv b { color: var(--head); font-weight: 500; margin-left: 4px; }
    .ws-hbtn { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 0 12px; border-radius: 8px; color: var(--md3-on-primary-container); font: inherit; font-size: 14px; font-weight: 600; }
    .ws-hbtn[disabled] { color: var(--md3-neutral-secondary); font-weight: 500; }
    .ws-group .ktabwrap { border-top: 1px solid var(--md3-surface-variant); padding: 0 14px 6px; }
    .ws-group .ktab td { padding: 4px 10px; height: 52px; }
    .ws-group tr.sel td { background: var(--md3-displaybg-primary); }
    .ws-group .ck { width: 44px; }
    .ws-ck { width: 44px; height: 44px; display: grid; place-items: center; }
    .ws-ck input { width: 22px; height: 22px; accent-color: var(--md3-on-primary-container); }
    .ws-set { display: inline-flex; flex-wrap: wrap; align-items: center; gap: 6px; }
    .ws-tag { display: inline-flex; height: 22px; align-items: center; padding: 0 8px; border-radius: 4px; background: var(--md3-background); color: var(--md3-neutral-secondary); font-size: 12px; }
    .ws-tag.own { background: #FFF1CC; color: #7A5600; font-weight: 600; }
    .ws-foot { position: sticky; bottom: 0; display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; padding: 12px 16px; border-radius: var(--radius); background: var(--white); box-shadow: 0 -2px 12px rgba(31,81,91,.12); }
    .ws-foot input { min-height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 10px; font: inherit; color: var(--head); }
    .ws-foot small { color: var(--md3-neutral-secondary); font-size: 13px; flex-basis: 100%; }
    .ws-empty { color: var(--md3-neutral-secondary); padding: 24px; text-align: center; background: var(--white); border-radius: var(--radius); }
    .ws-sw { display: contents; }   /* sheet content wrapper: listeners go here, not on the reused .sheet */
    .ws-radios { display: grid; gap: 6px; }
    .ws-radios > span { color: var(--ink); font-size: 14px; font-weight: 500; }
    .ws-radios .opts { display: flex; flex-wrap: wrap; gap: 8px; }
    .ws-radios label { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 14px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); color: var(--head); }
    .ws-radios label:has(input:checked) { border-color: var(--md3-on-primary-container); background: var(--md3-displaybg-primary); }
    .ws-radios input { width: 20px; height: 20px; accent-color: var(--md3-on-primary-container); }
    .ws-now { color: var(--ink); font-size: 14px; }
    .ws-now b { color: var(--head); }
    .ws-sheet .seg3 { grid-template-columns: repeat(2, minmax(0, 1fr)); } .ws-sheet .seg3 button { min-height: 44px; }
    .ws-sheet .ktab td, .ws-sheet .ktab th { padding: 8px; }
    .ws-sheet .ktab tr.same td { color: var(--md3-neutral-secondary); }
    .ws-sheet .ktab tr.grp td { font-weight: 600; background: var(--md3-background); }
    .ws-sheet .ktab tr.later td { opacity: .7; }
    @media (orientation: landscape) { .ws-sum { grid-template-columns: repeat(6, minmax(0, 1fr)); } .ws-kvs { flex-basis: auto; } }
''', 'js': r'''  (function () {
    var MEAS = ['Item-wise', 'Consolidated', 'Dry + wet'], PER = ['Per feeding', 'Whole day'], AT = ['Enclosure', 'Keeper area'], FAR = '1900-01-01', CAP = 15;
    var coll = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });
    var st = { site: '', sec: '', pick: 'all', open: {}, allOpen: false, q: '', fSet: '', fMeas: '', sel: {}, edits: {}, from: '', more: false }, body = null, D = null, groupsCache = [], allGroups = [];
    function load() { D = MGSTORE.get('wastage-setup'); D.setups = D.setups || {}; if (!st.site) st.site = D.defaultSite; if (!st.from) st.from = D.today; }
    function today() { return D.today; }
    function enc(s) { var p = s.split('|'); return { name: p[0], species: p[1] === '' ? null : Number(p[1]), animals: p[2] === '' ? null : Number(p[2]), area: p[3] || '' }; }
    function siteObj() { return D.sites.filter(function (s) { return s.name === st.site; })[0] || D.sites[0]; }
    function secObj(site) { return st.sec ? site.sections.filter(function (x) { return x.name === st.sec; })[0] || null : null; }
    function areaList() { return typeof MGAPI.keeperAreas === 'function' ? MGAPI.keeperAreas() : D.areas; }
    function areaOf(site, sec, e) {
      var list = areaList();
      if (typeof MGAPI.keeperAreas === 'function') { var a = list.filter(function (x) { return String(x.site).trim() === String(site.name).trim() && x.section === sec.name && x.active !== false && (x.enclosures || []).indexOf(e.name) !== -1; })[0]; return a ? a.name : ''; }
      return e.area && list.some(function (x) { return String(x.site).trim() === String(site.name).trim() && x.section === sec.name && x.name === e.area && x.active !== false; }) ? e.area : '';
    }
    function key(g, e) { return g.site.name + '|' + g.sec.name + '|' + e.name; }
    function gkey(g) { return g.site.name + '|' + g.sec.name + '|' + g.area; }
    function gname(g) { return !g.area ? g.sec.name + ' · Unassigned' : st.sec ? g.area : g.sec.name + ' · ' + g.area; }
    function groupsOf(site, sec) {
      var map = {};
      sec.encl.map(enc).forEach(function (e) { var a = areaOf(site, sec, e); (map[a] = map[a] || []).push(e); });
      var out = Object.keys(map).filter(function (n) { return n; }).sort(coll.compare).map(function (n) { return { site: site, sec: sec, area: n, encl: map[n] }; });
      if (map['']) out.push({ site: site, sec: sec, area: '', encl: map[''] });
      return out;
    }
    /* kitchen-store.js: snapshots newest first; the one in force today is the latest with effectiveFrom <= today */
    function hist(g) { return (D.setups[gkey(g)] || []).slice().sort(function (a, b) { return String(b.effectiveFrom).localeCompare(String(a.effectiveFrom)) || b.id - a.id; }); }
    function snapNow(g) { var l = hist(g); for (var i = 0; i < l.length; i++) if (l[i].effectiveFrom <= today()) return l[i]; return null; }
    function groupBase(g) { var s = snapNow(g), b = D.areaDefault, ex = {};
      ((s && s.exceptions) || []).forEach(function (o) { ex[o.enclosure] = { measured: o.measured, per: o.per }; });
      return { at: g.area ? (s ? s.at : b.at) : 'Enclosure', measured: s ? s.measured : b.measured, per: s ? s.per : b.per, ex: ex }; }
    function setupOf(g) { return st.edits[gkey(g)] || groupBase(g); }
    function sortEx(ex) { return Object.keys(ex).sort().map(function (k) { return [k, ex[k].measured, ex[k].per]; }); }
    function same(a, b) { return JSON.stringify([a.at, a.measured, a.per, sortEx(a.ex)]) === JSON.stringify([b.at, b.measured, b.per, sortEx(b.ex)]); }
    function setSetup(g, next) { var k = gkey(g); if (same(next, groupBase(g))) delete st.edits[k]; else st.edits[k] = next; }
    function copy(s) { return { at: s.at, measured: s.measured, per: s.per, ex: JSON.parse(JSON.stringify(s.ex)) }; }
    function rowState(s, e) { var o = s.ex[e.name]; return o ? { at: 'Enclosure', measured: o.measured, per: o.per, own: true } : { at: s.at, measured: s.measured, per: s.per, own: false }; }
    function settingTxt(s) { return s.at + ' · ' + s.measured + ' · ' + s.per; }
    function stateTxt(s) { return settingTxt(s) + ' · ' + (s.own ? 'own setting' : 'area default'); }
    function sinceTxt(d) { return d == null || d === FAR ? 'Before any setup' : fmtD(d); }
    function filtering() { return !!(st.q.trim() || st.fSet || st.fMeas); }
    function filtered(g) { var q = st.q.trim().toLowerCase(), s = setupOf(g);
      return g.encl.filter(function (e) { var r = rowState(s, e); if (st.fSet === 'default' && r.own) return false; if (st.fSet === 'own' && !r.own) return false; if (st.fMeas && r.measured !== st.fMeas) return false; return !q || (e.name + ' ' + gname(g)).toLowerCase().indexOf(q) !== -1; }); }
    function encHistory(g, name) {
      var b = D.areaDefault, un = !g.area, out = [{ since: null, at: un ? 'Enclosure' : b.at, measured: b.measured, per: b.per, setBy: null }];
      hist(g).slice().reverse().forEach(function (h) {
        var own = (h.exceptions || []).filter(function (x) { return x.enclosure === name; })[0];
        var eff = { at: own || un ? 'Enclosure' : h.at, measured: own ? own.measured : h.measured, per: (own && own.per) || h.per }, last = out[out.length - 1];
        if (h.effectiveFrom === FAR) { last.at = eff.at; last.measured = eff.measured; last.per = eff.per; last.setBy = h.setBy; return; }
        if (last.at !== eff.at || last.measured !== eff.measured || last.per !== eff.per) out.push({ since: h.effectiveFrom, at: eff.at, measured: eff.measured, per: eff.per, setBy: h.setBy });
      });
      return out.reverse();
    }
    function kv(l, v) { return '<span class="ws-kv">' + l + ':<b>' + esc(v) + '</b></span>'; }
    function plural(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }
    function groupHtml(g, gi, edit, force) {
      var id = gkey(g), open = edit || filtering() || (st.open[id] !== undefined ? st.open[id] : (force || st.allOpen));
      var rows = filtered(g), s = setupOf(g), hl = hist(g).length, own = g.encl.filter(function (e) { return rowState(s, e).own; }).length, ed = edit && canEdit();
      var h = '<section class="ws-group' + (st.edits[id] ? ' chg' : '') + '"><div class="ws-gh">';
      if (edit) h += '<span class="ttl"><small>' + (g.area ? 'Keeper area' : 'Unassigned enclosures') + '</small><b>' + esc(gname(g)) + '</b></span>';
      else h += '<button type="button" class="tg" data-wstoggle="' + esc(id) + '" aria-expanded="' + open + '">' + ic('dropdown', 20) + esc(gname(g)) + '</button>';
      h += '<span class="cnt">' + (filtering() ? rows.length + ' of ' + g.encl.length : g.encl.length) + ' enclosure' + (g.encl.length === 1 ? '' : 's') + (own ? ' · ' + own + ' with ' + (own === 1 ? 'its' : 'their') + ' own setting' : '') + '</span><span class="sp"></span>' +
        (ed ? '<button type="button" class="btn sec ksm" data-wsgchange="' + gi + '">' + ic('pencil', 18) + 'Change</button>' : '') +
        '<button type="button" class="ws-hbtn" data-wsghist="' + gi + '"' + (hl ? '' : ' disabled') + '>' + ic('history', 18) + 'History' + (hl ? ' · ' + hl : '') + '</button>' +
        '<span class="ws-kvs">' + kv('Recorded at', s.at) + kv('Measured as', s.measured) + kv('Recorded per', s.per) + '</span></div>';
      if (open) {
        var allOn = rows.length && rows.every(function (e) { return st.sel[key(g, e)]; });
        h += '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr>' + (ed ? '<th class="ck"><label class="ws-ck"><input type="checkbox" data-wsall="' + gi + '"' + (allOn ? ' checked' : '') + ' aria-label="Tick all enclosures of ' + esc(gname(g)) + '"></label></th>' : '') + '<th>Enclosure</th><th>Species · animals</th><th>Setting</th><th>History</th></tr></thead><tbody>' +
          (rows.length ? rows.map(function (e) { var r = rowState(s, e), k = key(g, e), n = encHistory(g, e.name).length - 1;
            return '<tr' + (ed ? ' class="mgrow' + (st.sel[k] ? ' sel' : '') + '" data-wsrow="' + esc(k) + '"' : '') + '>' + (ed ? '<td class="ck"><label class="ws-ck"><input type="checkbox" data-wspick="' + esc(k) + '"' + (st.sel[k] ? ' checked' : '') + ' aria-label="Select ' + esc(e.name) + '"></label></td>' : '') +
              '<td><b>' + esc(e.name) + '</b></td><td>' + (e.species || 0) + ' species · ' + fmtN(e.animals || 0) + ' animal' + ((e.animals || 0) === 1 ? '' : 's') + '</td>' +
              '<td><span class="ws-set">' + esc(settingTxt(r)) + '<span class="ws-tag' + (r.own ? ' own' : '') + '">' + (r.own ? 'Own setting' : 'area default') + '</span></span></td>' +
              '<td><button type="button" class="ws-hbtn" data-wshist="' + esc(k) + '" data-gi="' + gi + '"' + (n ? '' : ' disabled') + ' aria-label="History for ' + esc(e.name) + '">' + (n ? plural(n, 'change') : '-') + '</button></td></tr>'; }).join('')
            : '<tr><td colspan="' + (ed ? 5 : 4) + '" class="ws-now">No enclosures match.</td></tr>') + '</tbody></table></div>';
      }
      return h + '</section>';
    }
    function draw(b) {
      body = b || body; load();
      var site = siteObj(), sec = secObj(site), secs = sec ? [sec] : site.sections, groups = [], h = '', edit = false, shown;
      secs.forEach(function (s) { groupsOf(site, s).forEach(function (g) { groups.push(g); }); });
      allGroups = groups; shown = groups;
      var encN = 0, ownN = 0; groups.forEach(function (g) { encN += g.encl.length; var s = setupOf(g); ownN += g.encl.filter(function (e) { return rowState(s, e).own; }).length; });
      var unSite = 0; site.sections.forEach(function (s) { groupsOf(site, s).forEach(function (g) { if (!g.area) unSite += g.encl.length; }); });
      h += '<div class="ws-pick"><label class="mgf"><span>Site</span><select data-wssite>' + D.sites.map(function (s) { return '<option' + (s.name === site.name ? ' selected' : '') + '>' + esc(s.name) + '</option>'; }).join('') + '</select><small>' + plural(site.sections.length, 'section') + ' · ' + fmtN(site.species) + ' species · ' + fmtN(site.animals) + ' animals</small></label>' +
        '<label class="mgf"><span>Section</span><select data-wssec><option value="">All sections</option>' + site.sections.map(function (s) { return '<option' + (st.sec === s.name ? ' selected' : '') + '>' + esc(s.name) + '</option>'; }).join('') + '</select><small>' + (sec ? fmtN(sec.species) + ' species · ' + fmtN(sec.animals) + ' animals · ' + plural(sec.encl.length, 'enclosure') : fmtN(site.species) + ' species · ' + encN + ' enclosures · ' + unSite + ' unassigned') + '</small></label></div>';
      h += '<div class="ws-sum"><div><small>Site</small><b>' + esc(site.name) + '</b></div><div><small>Keeper area groups</small><b class="big">' + groups.length + '</b></div><div><small>Enclosures</small><b class="big">' + encN + '</b></div><div><small>Own settings</small><b class="big">' + ownN + '</b></div><div><small>Default measured as</small><b>' + esc(D.areaDefault.measured) + '</b></div><div><small>Default recorded per</small><b>' + esc(D.areaDefault.per) + '</b></div></div>';
      if (sec) {
        var gs = groupsOf(site, sec), names = gs.filter(function (g) { return g.area; }).map(function (g) { return g.area; }), unN = gs.filter(function (g) { return !g.area; }).reduce(function (n, g) { return n + g.encl.length; }, 0);
        h += '<div class="ws-chips" role="group" aria-label="Keeper areas"><b>Keeper areas:</b><button type="button" class="ws-chip" data-wspick-area="all" aria-pressed="' + (st.pick === 'all') + '">All</button>' +
          names.map(function (n) { return '<button type="button" class="ws-chip" data-wspick-area="' + esc(n) + '" aria-pressed="' + (st.pick === n) + '">' + esc(n) + '</button>'; }).join('') +
          (unN ? '<button type="button" class="ws-chip" data-wspick-area="__un" aria-pressed="' + (st.pick === '__un') + '">Unassigned · ' + unN + '</button>' : '') + (names.length || unN ? '' : '<span class="ws-now">No keeper areas yet.</span>') + '</div>';
        if (st.pick !== 'all') { edit = true; shown = gs.filter(function (g) { return (g.area || '__un') === st.pick; }); if (!shown.length) { st.pick = 'all'; edit = false; shown = groups; } }
      }
      if (!edit) {
        var sEnc = shown.reduce(function (n, g) { return n + g.encl.length; }, 0), sH = shown.reduce(function (n, g) { return n + hist(g).length; }, 0);
        h += '<div class="ws-scope"><div><span class="nm">' + esc(sec ? sec.name : site.name) + '</span><span class="meta">' + (sec ? esc(site.name) : 'All sections') + ' · ' + plural(shown.length, 'keeper area') + ' · ' + plural(sEnc, 'enclosure') + '</span></div><span class="sp"></span>' +
          (shown.length > 1 && !filtering() ? '<button type="button" class="btn sec ksm" data-wsexpand>' + (st.allOpen ? 'Collapse all' : 'Expand all') + '</button>' : '') +
          '<button type="button" class="ws-hbtn" data-wsscopehist' + (sH ? '' : ' disabled') + '>' + ic('history', 18) + 'History' + (sH ? ' · ' + sH : '') + '</button></div>';
      }
      h += '<div class="ws-filters"><label class="mgsearch">' + ic('search', 20) + '<input type="search" data-wsq placeholder="Filter enclosure or area" value="' + esc(st.q) + '" aria-label="Filter enclosures" autocomplete="off"></label>' +
        '<select data-wsfset aria-label="Filter by setting"><option value="">Any setting</option><option value="default"' + (st.fSet === 'default' ? ' selected' : '') + '>Area default</option><option value="own"' + (st.fSet === 'own' ? ' selected' : '') + '>Own setting</option></select>' +
        '<select data-wsfmeas aria-label="Filter by measured as"><option value="">Measured as: any</option>' + MEAS.map(function (m) { return '<option' + (st.fMeas === m ? ' selected' : '') + '>' + m + '</option>'; }).join('') + '</select></div>' +
        '<p class="ws-note">' + ic('info', 16) + (!canEdit() ? 'Read only for your role.' : edit ? (Object.keys(st.sel).length ? 'Change the ticked enclosures together, or tap a row to open it.' : 'Tap a row to open it. Tick rows to change several together.') : 'Read-only overview. Pick a section, then one keeper area, to make changes.') + '</p>';
      var ticked = Object.keys(st.sel).length;
      if (edit && ticked && canEdit()) h += '<div class="ws-ticked" role="region" aria-label="Ticked enclosures">' + plural(ticked, 'enclosure') + ' ticked<span class="sp"></span><button type="button" class="btn teal ksm" data-wschgticked>Change ticked</button><button type="button" class="btn sec ksm" data-wsclrticked>Clear</button></div>';
      groupsCache = shown;
      var listed = shown.filter(function (g) { return !filtering() || filtered(g).length; }), capped = !edit && !st.more && listed.length > CAP + 1;
      h += listed.length ? (capped ? listed.slice(0, CAP) : listed).map(function (g) { return groupHtml(g, shown.indexOf(g), edit, !!sec); }).join('') +
          (capped ? '<button type="button" class="linkbtn t-body-medium kmore" data-wsmore>Show all ' + listed.length + '</button>' : '')
        : '<p class="ws-empty">' + (shown.length ? 'No enclosures match the filter.' : 'No enclosures.') + '</p>';
      if (edit && canEdit()) { var ch = Object.keys(st.edits).length;
        h += '<div class="ws-foot"><button type="button" class="btn pri ksm" data-wssave' + (ch ? '' : ' disabled') + '>Save setup' + (ch ? ' · ' + plural(ch, 'area') : '') + '</button>' + (ch ? '<button type="button" class="btn sec ksm" data-wsdiscard>Discard changes</button>' : '') +
          '<label class="mgro">Takes effect from <input type="date" data-wsfrom value="' + esc(st.from) + '" min="' + esc(today()) + '" aria-label="Takes effect from"></label><small>Figures already recorded keep the setup they were recorded under.</small></div>'; }
      var foc = document.activeElement && document.activeElement.matches && document.activeElement.matches('[data-wsq]');
      body.innerHTML = '<div class="mgpane">' + h + '</div>';
      if (foc) { var q = body.querySelector('[data-wsq]'); q.focus(); q.setSelectionRange(q.value.length, q.value.length); }
    }
    function radios(name, opts, val) { return '<span class="opts">' + opts.map(function (o) { return '<label><input type="radio" name="' + name + '" value="' + esc(o) + '"' + (o === val ? ' checked' : '') + '>' + esc(o) + '</label>'; }).join('') + '</span>'; }
    /* area default sheet */
    function openGroup(g) {
      var s = setupOf(g), gd = { at: s.at, measured: s.measured, per: s.per };
      var sh = mgSheet('<div class="ws-sw">' + mgSheetHead(gname(g) + ' · area default', '') + '<div class="mgform ws-sheet"><p class="ws-now">Now: <b>' + esc(settingTxt(s)) + '</b></p>' +
        '<div class="ws-radios"><span>Recorded at</span>' + (g.area ? radios('wsga', AT, gd.at) : '<p class="ws-now">Enclosure. Enclosures without a keeper area are always weighed on their own.</p>') + '</div>' +
        '<div class="ws-radios"><span>Measured as</span>' + radios('wsgm', MEAS, gd.measured) + '</div><div class="ws-radios"><span>Recorded per</span>' + radios('wsgp', PER, gd.per) + '</div><p class="ws-now" data-wsbec hidden></p></div>' +
        '<div class="sheet__f"><button type="button" class="btn sec" data-mgclose>Cancel</button><button type="button" class="btn pri" data-wsgapply hidden>Apply</button></div></div>', 'Area default').querySelector('.ws-sw');
      function sync() { var c = s.at !== gd.at || s.measured !== gd.measured || s.per !== gd.per, own = Object.keys(s.ex).length, bec = sh.querySelector('[data-wsbec]');
        sh.querySelector('[data-wsgapply]').hidden = !c; bec.hidden = !c; bec.innerHTML = 'Becomes: <b>' + esc(gd.at + ' · ' + gd.measured + ' · ' + gd.per) + '</b>' + (own ? ' · ' + plural(own, 'enclosure') + ' with an own setting keep it' : ''); }
      sh.addEventListener('change', function (e) { if (e.target.name === 'wsga') gd.at = e.target.value; if (e.target.name === 'wsgm') gd.measured = e.target.value; if (e.target.name === 'wsgp') gd.per = e.target.value; sync(); });
      sh.querySelector('[data-wsgapply]').addEventListener('click', function () { var n = copy(setupOf(g)); n.at = gd.at; n.measured = gd.measured; n.per = gd.per; setSetup(g, n); mgClose(); draw(); });
      sync();
    }
    /* enclosure sheet: one row (Setting / Species) or the ticked rows */
    function hitOf(k) { for (var i = 0; i < allGroups.length; i++) { var g = allGroups[i]; for (var j = 0; j < g.encl.length; j++) if (key(g, g.encl[j]) === k) return { g: g, e: g.encl[j] }; } return null; }
    function openRows(keys) {
      var hits = keys.map(hitOf).filter(Boolean); if (!hits.length) return;
      var one = hits.length === 1 ? hits[0] : null, r0 = one ? rowState(setupOf(one.g), one.e) : null, rd = { m: r0 && r0.own ? r0.measured : '', p: r0 && r0.own ? r0.per : '', tab: 'setting' };
      var sp = one ? (D.species[key(one.g, one.e)] || []) : [];
      var sh = mgSheet('<div class="ws-sw">' + mgSheetHead(one ? one.e.name + ' · ' + gname(one.g) : 'Own setting for ' + hits.length + ' enclosures', '') +
        (one ? '<div class="seg3 ws-sheet" role="tablist" aria-label="Enclosure"><button type="button" role="tab" class="t-body-medium" data-wstab="setting" aria-selected="true">Setting</button><button type="button" role="tab" class="t-body-medium" data-wstab="species" aria-selected="false">' + (one.e.species ? 'Species · ' + one.e.species : 'Species') + '</button></div>' : '') +
        '<div class="mgform ws-sheet" data-wspanel="setting"><p class="ws-now" data-wsnow></p><div class="ws-radios"><span>Measured as</span>' + radios('wsrm', MEAS, rd.m) + '</div><div class="ws-radios"><span>Recorded per</span>' + radios('wsrp', PER, rd.p) + '</div><p class="ws-now" data-wspickmsg>Pick both to go on.</p><div data-wsbec></div></div>' +
        (one ? '<div class="mgform ws-sheet" data-wspanel="species" hidden>' + (sp.length ? '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Species</th><th>Scientific name</th><th class="r">Animals</th><th class="r">Records</th></tr></thead><tbody>' + sp.map(function (x) { return '<tr><td>' + esc(x.name) + '</td><td><i>' + esc(x.scientific) + '</i></td><td class="r">' + x.animals + '</td><td class="r">' + x.records + '</td></tr>'; }).join('') + '</tbody></table></div>' : (one.e.animals ? '' : '<p class="ws-now">No animals are recorded in this enclosure.</p>')) +
          '<p class="kcap t-body-regular">' + (sp.length || one.e.species || 0) + ' species · ' + plural(one.e.animals || 0, 'animal') + ' · ' + esc(one.g.sec.name) + ' · ' + esc(one.g.site.name) + '</p></div>' : '') +
        '<div class="sheet__f"><button type="button" class="btn sec" data-wsdef hidden>Use area default</button><button type="button" class="btn sec" data-mgclose data-wsclose>Cancel</button><button type="button" class="btn pri" data-wsrapply hidden>Apply</button></div></div>', 'Enclosure setting').querySelector('.ws-sw');
      function sync() {
        var ready = !!(rd.m && rd.p), gs = []; hits.forEach(function (x) { if (gs.indexOf(x.g) === -1) gs.push(x.g); });
        var ownN = hits.filter(function (x) { return rowState(setupOf(x.g), x.e).own; }).length, bec = ready ? 'Enclosure · ' + rd.m + ' · ' + rd.p + ' · own setting' : '', species = rd.tab === 'species';
        sh.querySelector('[data-wsnow]').textContent = (one ? 'Now: ' + stateTxt(rowState(setupOf(one.g), one.e)) : ownN + ' of ' + hits.length + ' already on their own') + (gs.length === 1 ? ' · area default is ' + settingTxt(setupOf(gs[0])) : '');
        sh.querySelector('[data-wspickmsg]').hidden = ready;
        sh.querySelector('[data-wsbec]').innerHTML = !ready ? '' : one ? '<p class="ws-now">Becomes: <b>' + esc(bec) + '</b></p>' : '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Enclosure</th><th>Now</th><th>Becomes</th></tr></thead><tbody>' + gs.map(function (g) {
          return (gs.length > 1 ? '<tr class="grp"><td colspan="3">' + esc(gname(g)) + '</td></tr>' : '') + hits.filter(function (x) { return x.g === g; }).map(function (x) { var now = stateTxt(rowState(setupOf(g), x.e)), sm = now === bec; return '<tr' + (sm ? ' class="same"' : '') + '><td><b>' + esc(x.e.name) + '</b></td><td>' + esc(now) + '</td><td>' + (sm ? 'no change' : '<b>' + esc(bec) + '</b>') + '</td></tr>'; }).join(''); }).join('') + '</tbody></table></div>';
        var ap = sh.querySelector('[data-wsrapply]'), df = sh.querySelector('[data-wsdef]');
        ap.hidden = species || !ready; ap.textContent = one ? 'Apply' : 'Apply to ' + hits.length; df.hidden = species || !ownN; df.textContent = 'Use area default' + (one ? '' : ' · ' + ownN);
        sh.querySelector('[data-wsclose]').textContent = species ? 'Close' : 'Cancel';
      }
      function applyTo(fn) { var by = []; hits.forEach(function (x) { var b = by.filter(function (y) { return y.g === x.g; })[0]; if (!b) { b = { g: x.g, es: [] }; by.push(b); } b.es.push(x.e); });
        by.forEach(function (b) { var n = copy(setupOf(b.g)); fn(n, b.es); setSetup(b.g, n); }); st.sel = {}; mgClose(); draw(); }
      sh.addEventListener('change', function (e) { if (e.target.name === 'wsrm') rd.m = e.target.value; if (e.target.name === 'wsrp') rd.p = e.target.value; sync(); });
      sh.addEventListener('click', function (e) { var t = e.target.closest('[data-wstab]'); if (!t) return; rd.tab = t.getAttribute('data-wstab');
        [].forEach.call(sh.querySelectorAll('[data-wstab]'), function (x) { x.setAttribute('aria-selected', String(x === t)); }); [].forEach.call(sh.querySelectorAll('[data-wspanel]'), function (p) { p.hidden = p.getAttribute('data-wspanel') !== rd.tab; }); sync(); });
      sh.querySelector('[data-wsrapply]').addEventListener('click', function () { applyTo(function (s, es) { es.forEach(function (e) { s.ex[e.name] = { measured: rd.m, per: rd.p }; }); }); });
      sh.querySelector('[data-wsdef]').addEventListener('click', function () { applyTo(function (s, es) { es.forEach(function (e) { delete s.ex[e.name]; }); }); });
      sync();
    }
    /* history sheets */
    function histTable(list, withArea) { return '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Since</th>' + (withArea ? '<th>Keeper area</th>' : '') + '<th>Recorded at</th><th>Measured as</th><th>Recorded per</th><th>Own settings</th><th>Set by</th></tr></thead><tbody>' +
      list.map(function (h) { return '<tr' + (h.effectiveFrom > today() ? ' class="later"' : '') + '><td>' + esc(sinceTxt(h.effectiveFrom)) + '</td>' + (withArea ? '<td>' + esc(h.area) + '</td>' : '') + '<td>' + esc(h.at) + '</td><td>' + esc(h.measured) + '</td><td>' + esc(h.per) + '</td><td>' + ((h.exceptions || []).length ? esc(h.exceptions.map(function (x) { return x.enclosure + ' (' + x.measured + ')'; }).join(', ')) : '-') + '</td><td>' + esc(h.setBy || '-') + '</td></tr>'; }).join('') + '</tbody></table></div>'; }
    function encHistTable(list) { return '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Since</th><th>Recorded at</th><th>Measured as</th><th>Recorded per</th><th>Set by</th></tr></thead><tbody>' +
      list.map(function (h) { return '<tr><td>' + esc(sinceTxt(h.since)) + '</td><td>' + esc(h.at) + '</td><td>' + esc(h.measured) + '</td><td>' + esc(h.per) + '</td><td>' + esc(h.setBy || 'Default') + '</td></tr>'; }).join('') + '</tbody></table></div>'; }
    function openHist(title, html) { mgSheet(mgSheetHead(title + ' · wastage setup history', '') + '<div class="ws-sheet">' + html + '</div><div class="sheet__f"><button type="button" class="btn sec" data-mgclose>Close</button></div>', 'History'); }
    /* save: one dated snapshot per changed keeper area; Undo restores them */
    function save() {
      var keys = Object.keys(st.edits); if (!keys.length) return;
      var from = st.from < today() ? today() : st.from, before = [], id = 0;
      Object.keys(D.setups).forEach(function (k) { D.setups[k].forEach(function (s) { if (s.id > id) id = s.id; }); });
      keys.forEach(function (gk) { var g = allGroups.filter(function (x) { return gkey(x) === gk; })[0], n = st.edits[gk]; if (!g) return;
        before.push({ key: gk, list: D.setups[gk] ? JSON.parse(JSON.stringify(D.setups[gk])) : null });
        (D.setups[gk] = D.setups[gk] || []).push({ id: ++id, at: g.area ? n.at : 'Enclosure', measured: n.measured, per: n.per, exceptions: Object.keys(n.ex).sort(coll.compare).map(function (e) { return { enclosure: e, measured: n.ex[e].measured, per: n.ex[e].per }; }), effectiveFrom: from, setBy: VIEWER.name }); });
      MGSTORE.set('wastage-setup', D); st.edits = {}; st.sel = {}; draw();
      toastUndo('Saved · ' + plural(before.length, 'keeper area') + ' · in force from ' + fmtD(from), function () { load(); before.forEach(function (b) { if (b.list) D.setups[b.key] = b.list; else delete D.setups[b.key]; }); MGSTORE.set('wastage-setup', D); draw(); toast('Undone. The earlier setup is in force again.'); });
    }
    var qT;
    MGP['wastage-setup'] = { title: 'Wastage setup', sub: 'How wastage is weighed and recorded', draw: function (b) { draw(b); },
      click: function (e) { var t;
        if ((t = e.target.closest('[data-wstoggle]'))) { var id = t.getAttribute('data-wstoggle'); st.open[id] = t.getAttribute('aria-expanded') !== 'true'; draw(); return; }
        if (e.target.closest('[data-wsexpand]')) { st.allOpen = !st.allOpen; st.open = {}; draw(); return; }
        if (e.target.closest('[data-wsmore]')) { st.more = true; draw(); return; }
        if ((t = e.target.closest('[data-wspick-area]'))) { var v = t.getAttribute('data-wspick-area'); st.pick = st.pick === v && v !== 'all' ? 'all' : v; st.sel = {}; draw(); return; }
        if ((t = e.target.closest('[data-wsgchange]'))) { openGroup(groupsCache[Number(t.getAttribute('data-wsgchange'))]); return; }
        if (e.target.closest('[data-wssave]')) { save(); return; }
        if (e.target.closest('[data-wsdiscard]')) { st.edits = {}; draw(); return; }
        if (e.target.closest('[data-wschgticked]')) { openRows(Object.keys(st.sel)); return; }
        if (e.target.closest('[data-wsclrticked]')) { st.sel = {}; draw(); return; }
        if ((t = e.target.closest('[data-wsghist]'))) { var g0 = groupsCache[Number(t.getAttribute('data-wsghist'))]; openHist(gname(g0), histTable(hist(g0), false)); return; }
        if (e.target.closest('[data-wsscopehist]')) { var list = []; groupsCache.forEach(function (g) { hist(g).forEach(function (x) { list.push(Object.assign({ area: gname(g) }, x)); }); });
          list.sort(function (a, b) { return String(b.effectiveFrom).localeCompare(String(a.effectiveFrom)) || b.id - a.id; }); openHist(st.sec || st.site, histTable(list, true)); return; }
        if ((t = e.target.closest('[data-wshist]'))) { var hg = groupsCache[Number(t.getAttribute('data-gi'))], en = t.getAttribute('data-wshist').split('|')[2]; if (hg) openHist(en, encHistTable(encHistory(hg, en))); return; }
        if ((t = e.target.closest('[data-wsall]'))) { var g = groupsCache[Number(t.getAttribute('data-wsall'))]; filtered(g).forEach(function (x) { var k = key(g, x); if (t.checked) st.sel[k] = true; else delete st.sel[k]; }); draw(); return; }
        if ((t = e.target.closest('[data-wspick]'))) { var k2 = t.getAttribute('data-wspick'); if (t.checked) st.sel[k2] = true; else delete st.sel[k2]; draw(); return; }
        if (e.target.closest('.ws-ck')) return;
        if ((t = e.target.closest('tr[data-wsrow]')) && canEdit() && st.pick !== 'all') openRows([t.getAttribute('data-wsrow')]);
      },
      input: function (e) { if (e.target.matches('[data-wsq]')) { clearTimeout(qT); var v = e.target.value; qT = setTimeout(function () { st.q = v; draw(); }, 150); } },
      change: function (e) { var t = e.target;
        if (t.matches('[data-wssite]')) { st.site = t.value; st.sec = ''; st.pick = 'all'; st.open = {}; st.sel = {}; st.edits = {}; st.more = false; draw(); }
        if (t.matches('[data-wssec]')) { st.sec = t.value; st.pick = 'all'; st.open = {}; st.sel = {}; st.edits = {}; st.more = false; draw(); }
        if (t.matches('[data-wsfset]')) { st.fSet = t.value; draw(); }
        if (t.matches('[data-wsfmeas]')) { st.fMeas = t.value; draw(); }
        if (t.matches('[data-wsfrom]')) { if (t.value) st.from = t.value < today() ? today() : t.value; draw(); } } };
  })();
'''}
