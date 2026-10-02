# mg_keeper_areas.py: exec'd by kitchen.py. Meal Group Management > Keeper Areas.
# Source: Dev system_local kitchen/keeper-areas.{html,js,data.js} + sites.data.js + site-rail.js (variant 'areas').
# Site picker and section rail, Areas / Enclosures tabs, All / Assigned / Unassigned toggle and enclosure filter,
# row selection with the bulk bar (Assign to area / Clear area, toast with Undo), New / Edit keeper area sheet
# (section, name, keepers, section supervisor, enclosures, enclosure range, active) with the source validation.
# Keepers and supervisors come from Keeper Staff through MGAPI.keepers (fallback: this page's own keepers list).
# Offers MGAPI.keeperSites(), MGAPI.keeperAreas(), MGAPI.staffAssignments(name), MGAPI.renameKeeper(old, new).
# Left out: Import Excel and the Excel template (file import), and renaming an area's Wastage setup.
MGMOD = {'icons': ['search', 'dropdown'], 'css': '''    /* Keeper Areas */
    .ka-grid { display: grid; gap: 16px; align-items: start; }
    .ka-rail { display: grid; gap: 12px; align-content: start; padding: 16px; }
    .ka-rail .mgf select { font-weight: 500; }
    .ka-sitel { color: var(--md3-neutral-secondary); font-size: 13px; }
    .ka-list { display: none; flex-direction: column; gap: 6px; max-height: 560px; overflow-y: auto; padding-right: 2px; }
    .ka-it { flex: none; display: grid; gap: 4px; text-align: left; min-height: 56px; padding: 8px 12px; border-radius: 8px; border: 1px solid var(--line); background: var(--white); color: var(--head); font: inherit; }
    .ka-it .t { display: flex; justify-content: space-between; gap: 8px; font-weight: 600; font-size: 14px; }
    .ka-it .t span { color: var(--md3-neutral-secondary); font-weight: 500; font-variant-numeric: tabular-nums; }
    .ka-it .s { font-size: 12px; color: var(--md3-neutral-secondary); }
    .ka-it .s .w { color: #8A5A00; }
    .ka-it[aria-pressed="true"] { border-color: var(--md3-on-primary-container); background: var(--md3-displaybg-primary); }
    .ka-secsel { display: grid; }
    .ka-main { display: grid; gap: 14px; min-width: 0; }
    .ka-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
    .ka-top p { color: var(--md3-neutral-secondary); max-width: 60ch; }
    .ka-tabs { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .ka-tabs button, .ka-scope button { min-height: 44px; }
    .ka-scope { grid-template-columns: repeat(3, minmax(0, 1fr)); flex: 1 1 300px; }
    .ka-ck { width: 52px; }
    .ka-ck input { width: 22px; height: 22px; accent-color: var(--md3-on-primary-container); }
    .ka-sel td { background: var(--md3-displaybg-primary); }
    .ka-un { color: #8A5A00; font-weight: 500; }
    .ka-muted { color: var(--md3-neutral-secondary); }
    .ka-bulk { position: sticky; bottom: 0; z-index: 2; display: flex; flex-wrap: wrap; align-items: center; gap: 10px; padding: 12px 16px; border-radius: var(--radius); background: var(--white); box-shadow: 0 -2px 12px rgba(31,81,91,.16); }
    .ka-bulk select { min-height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); font: inherit; color: var(--head); flex: 1 1 200px; }
    .ka-bulk b { color: var(--head); }
    .ka-box { display: grid; gap: 2px; max-height: 240px; overflow-y: auto; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 4px 8px; }
    .ka-box label { display: flex; align-items: center; gap: 10px; min-height: 44px; color: var(--head); }
    .ka-box label input { width: 22px; height: 22px; accent-color: var(--md3-on-primary-container); flex: none; }
    .ka-box label span { margin-left: auto; color: var(--md3-neutral-secondary); font-size: 13px; }
    .ka-box label.dis { color: var(--md3-neutral-secondary); }
    .ka-box .none { padding: 12px 4px; color: var(--md3-neutral-secondary); }
    .ka-pick { color: var(--head); font-size: 14px; }
    .ka-range { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 10px; align-items: start; }
    .ka-alert { padding: 10px 12px; border-radius: 8px; font-size: 14px; }
    .ka-alert.ok { background: #E3F4EA; color: #1E6B3C; } .ka-alert.warn { background: #FFF6DB; color: #6B4E00; } .ka-alert.bad { background: #FBE4E8; color: #A3122E; }
    @media (orientation: landscape) {
      .ka-grid { grid-template-columns: 280px minmax(0, 1fr); }
      .ka-list { display: flex; }
      .ka-secsel { display: none; }
    }
''', 'js': r'''  (function () {
    var D = null, body = null, more = {};
    var st = { site: null, section: null, tab: null, scope: null, q: '', rq: '', sel: {} };
    var coll = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });
    function n0(v) { return v === '' || v == null ? null : Number(v); }
    function parse(d) { d.sites.forEach(function (s) { s.sections.forEach(function (sec) { sec.encl = sec.encl.map(function (x) { var p = x.split('|'); return { name: p[0], code: p[1] || '', species: n0(p[2]), animals: n0(p[3]), area: p[4] || '', _sec: sec.name, _site: s.name }; }); }); }); return d; }
    function data() { if (!D) { D = parse(MGSTORE.get('keeper-areas')); if (!st.tab) { st.site = lsGet('antz.kitchen.site') || D.defaultSite; st.tab = D.defaultTab || 'areas'; st.scope = D.defaultScope || 'unassigned'; } } return D; }
    function persist() {
      var out = JSON.parse(JSON.stringify(D, function (k, v) { return k === '_sec' || k === '_site' ? undefined : v; }));
      out.sites.forEach(function (s) { s.sections.forEach(function (sec) { sec.encl = sec.encl.map(function (e) { return [e.name, e.code, e.species == null ? '' : e.species, e.animals == null ? '' : e.animals, e.area].join('|').replace(/\|+$/, ''); }); }); });
      MGSTORE.set('keeper-areas', out);
    }
    function siteObj(name) {
      var d = data();
      if (name === 'All sites') { var secs = []; d.sites.forEach(function (s) { s.sections.forEach(function (x) { secs.push(Object.assign({}, x, { siteName: s.name, encl: x.encl, _ref: x })); }); });
        return { name: 'All sites', all: true, species: d.sites.reduce(function (n, s) { return n + s.species; }, 0), animals: d.sites.reduce(function (n, s) { return n + s.animals; }, 0), sections: secs }; }
      return d.sites.filter(function (s) { return s.name === name; })[0] || d.sites[0];
    }
    function secObj(site, sec) { var s = data().sites.filter(function (x) { return x.name === site; })[0]; return s ? s.sections.filter(function (x) { return x.name === sec; })[0] : null; }
    function secKey(s, site) { return (s.siteName || site.name) + '§' + s.name; }
    function curSec(site) { if (!st.section) return null; return site.sections.filter(function (s) { return secKey(s, site) === st.section; })[0] || null; }
    function staffList(siteName) {
      var list = MGAPI.keepers ? MGAPI.keepers() : (data().keepers || []).map(function (k) { return { name: k.name, code: k.code || '', site: null, active: true }; });
      return list.filter(function (k) { return k.active && (!siteName || k.site == null || k.site === siteName); }).sort(function (a, b) { return coll.compare(a.name, b.name); });
    }
    function areasOf(site, sec) { return data().areas.filter(function (a) { return (site.all || a.site === site.name) && (!sec || (a.site === (sec.siteName || site.name) && a.section === sec.name)); }); }
    function enclOfArea(a) { var s = secObj(a.site, a.section); return s ? s.encl.filter(function (e) { return e.area === a.name; }) : []; }
    function encls(site, sec) {
      var rows = []; (sec ? [sec] : site.sections).forEach(function (s) { s.encl.forEach(function (e) { rows.push(e); }); });
      if (!sec) { var coded = rows.filter(function (e) { return e.code; }).sort(function (a, b) { return a.name < b.name ? -1 : a.name > b.name ? 1 : 0; }); rows = coded.concat(rows.filter(function (e) { return !e.code; })); }
      return rows;
    }
    function un(list) { return list.filter(function (e) { return !e.area; }).length; }
    function cap(key, list, n) { var open = more[key] || list.length <= n + 1; return { rows: open ? list : list.slice(0, n), more: list.length > n + 1 ? '<button type="button" class="linkbtn t-body-medium kmore" data-kamore="' + key + '">' + (more[key] ? 'Show fewer' : 'Show all ' + list.length) + '</button>' : '' }; }

    function railHtml(site, sec) {
      var d = data(), q = st.rq.trim().toLowerCase(), all = encls(site, null);
      var item = function (s) {
        var on = s ? secKey(s, site) === st.section : !st.section, strip, right;
        if (!s) { right = fmtN(site.animals); strip = site.sections.length + ' sections · ' + fmtN(site.species) + ' species · ' + fmtN(all.length) + ' enclosures' + (un(all) ? ' · <span class="w">' + fmtN(un(all)) + ' unassigned</span>' : ''); }
        else { var u = un(s.encl); right = fmtN(s.animals); var na = areasOf(site, s).length; strip = na + (na === 1 ? ' area · ' : ' areas · ') + fmtN(s.species) + ' species' + (u ? ' · <span class="w">' + fmtN(u) + ' unassigned</span>' : ''); }
        return '<button type="button" class="ka-it" data-kasec="' + (s ? esc(secKey(s, site)) : '') + '" aria-pressed="' + on + '"><span class="t"><b>' + esc(s ? s.name + (site.all ? ' · ' + s.siteName.trim() : '') : 'All sections') + '</b><span>' + right + '</span></span><span class="s">' + strip + '</span></button>';
      };
      var secs = site.sections.filter(function (s) { return !q || s.name.toLowerCase().indexOf(q) !== -1; });
      return '<aside class="drow ka-rail" aria-label="Site and section">' +
        '<label class="mgf"><span>Site</span><select data-kasite>' + ['All sites'].concat(d.sites.map(function (s) { return s.name; })).map(function (n) { return '<option value="' + esc(n) + '"' + (n === site.name ? ' selected' : '') + '>' + esc(n.trim()) + '</option>'; }).join('') + '</select></label>' +
        '<p class="ka-sitel">' + site.sections.length + ' sections · ' + fmtN(site.species) + ' species · ' + fmtN(site.animals) + ' animals · ' + fmtN(un(all)) + ' unassigned Encl</p>' +
        '<label class="mgf ka-secsel"><span>Section</span><select data-kasecsel><option value="">All sections (' + fmtN(all.length) + ' enclosures)</option>' + site.sections.map(function (s) { var k = secKey(s, site); return '<option value="' + esc(k) + '"' + (k === st.section ? ' selected' : '') + '>' + esc(s.name + (site.all ? ' · ' + s.siteName.trim() : '')) + ' (' + areasOf(site, s).length + ' areas, ' + un(s.encl) + ' unassigned)</option>'; }).join('') + '</select></label>' +
        '<div class="ka-list"><label class="mgsearch">' + ic('search', 20) + '<input type="search" data-karq placeholder="Search sections" value="' + esc(st.rq) + '" aria-label="Search sections" autocomplete="off"></label>' + item(null) + secs.map(item).join('') + (q && !secs.length ? '<p class="ka-muted">No matches.</p>' : '') + '</div></aside>';
    }
    function areasHtml(site, sec) {
      var list = areasOf(site, sec), ed = canEdit();
      if (!list.length) return '<div class="empty"><span class="ei">' + ic('user', 24) + '</span><b class="t-minor-title">No keeper areas</b><span class="t-body-regular">' + (sec ? 'This section has no keeper area yet. Create one to start assigning enclosures.' : 'No keeper area on this site yet. Create one to start assigning enclosures.') + '</span></div>';
      var C = cap('areas', list, 25);
      return '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Keeper area</th><th>Section</th><th>Keepers</th><th class="r">Enclosures</th><th class="r">Species</th><th class="r">Animals</th><th>Status</th></tr></thead><tbody>' +
        C.rows.map(function (a) { var es = enclOfArea(a), sp = es.reduce(function (n, e) { return n + (e.species || 0); }, 0), an = es.reduce(function (n, e) { return n + (e.animals || 0); }, 0);
          return '<tr' + (ed ? ' class="mgrow" data-kaarea="' + data().areas.indexOf(a) + '"' : '') + '><td><b>' + esc(a.name) + '</b></td><td>' + esc(a.section) + '</td><td>' + ((a.keepers || []).length ? esc(a.keepers.join(', ')) : '<span class="ka-muted">-</span>') + '</td><td class="r">' + es.length + '</td><td class="r">' + (sp || '-') + '</td><td class="r">' + (an ? fmtN(an) : '-') + '</td><td>' + (a.active === false ? '<span class="kchip">Inactive</span>' : '<span class="kchip ok">Active</span>') + '</td></tr>'; }).join('') + '</tbody></table></div>' + C.more;
    }
    function encHtml(site, sec) {
      var all = encls(site, sec), asg = all.filter(function (e) { return !!e.area; }), ed = canEdit(), q = st.q.trim().toLowerCase();
      var cnt = { all: all.length, assigned: asg.length, unassigned: all.length - asg.length };
      var rows = all.filter(function (e) { if (st.scope === 'assigned' && !e.area) return false; if (st.scope === 'unassigned' && e.area) return false; return !q || (e.name + ' ' + e.code + ' ' + e.area).toLowerCase().indexOf(q) !== -1; });
      var C = cap('enc', rows, 50);
      return '<div class="mgbar"><div class="seg3 ka-scope" role="tablist" aria-label="Show">' + [['all', 'All'], ['assigned', 'Assigned'], ['unassigned', 'Unassigned']].map(function (t) { return '<button type="button" role="tab" class="t-body-medium" data-kascope="' + t[0] + '" aria-selected="' + (st.scope === t[0]) + '">' + t[1] + ' ' + cnt[t[0]] + '</button>'; }).join('') + '</div>' +
        '<label class="mgsearch">' + ic('search', 20) + '<input type="search" data-kaq placeholder="Filter enclosures" value="' + esc(st.q) + '" aria-label="Filter enclosures" autocomplete="off"></label></div>' +
        '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr>' + (ed ? '<th class="ka-ck"><span class="sr-only">Select</span></th>' : '') + '<th>Enclosure</th><th>Code</th><th>Keeper area</th><th class="r">Species</th><th class="r">Animals</th></tr></thead><tbody>' +
        (rows.length ? C.rows.map(function (e) { var k = e._site + '§' + e._sec + '§' + e.name, on = !!st.sel[k];
          return '<tr' + (ed ? ' class="mgrow' + (on ? ' ka-sel' : '') + '" data-kakey="' + esc(k) + '"' : '') + '>' + (ed ? '<td class="ka-ck"><input type="checkbox"' + (on ? ' checked' : '') + ' aria-label="Select ' + esc(e.name) + '" tabindex="-1"></td>' : '') + '<td><b>' + esc(e.name) + '</b></td><td>' + (e.code ? esc(e.code) : '-') + '</td>' +
            (e.area ? '<td>' + esc(e.area) + '</td>' : '<td class="ka-un">Unassigned</td>') + '<td class="r">' + (e.species != null ? e.species : '-') + '</td><td class="r">' + (e.animals != null ? fmtN(e.animals) : '-') + '</td></tr>'; }).join('')
          : '<tr><td colspan="' + (ed ? 6 : 5) + '" class="ka-muted">' + (all.length ? 'No matches.' : 'No records.') + '</td></tr>') + '</tbody></table></div>' + C.more;
    }
    function selected() { return Object.keys(st.sel).map(function (k) { var p = k.split('§'), s = secObj(p[0], p[1]), e = s && s.encl.filter(function (x) { return x.name === p[2]; })[0]; return e ? { site: p[0], section: p[1], e: e } : null; }).filter(Boolean); }
    function bulkHtml() {
      var sel = selected(); if (!sel.length || st.tab !== 'enclosures' || !canEdit()) return '';
      var secs = {}; sel.forEach(function (x) { secs[x.site + '§' + x.section] = 1; }); var keys = Object.keys(secs);
      var list = keys.length === 1 ? data().areas.filter(function (a) { return a.site + '§' + a.section === keys[0] && a.active !== false; }) : [];
      return '<div class="ka-bulk" role="region" aria-label="Selected enclosures"><b class="t-body-medium">' + sel.length + ' selected</b>' +
        '<select data-kabarea aria-label="Assign to area"' + (keys.length > 1 ? ' title="Pick enclosures from one section to assign them to an area."' : '') + '><option value="">' + (keys.length > 1 ? 'Pick enclosures from one section' : 'Assign to area') + '</option>' + list.map(function (a) { return '<option>' + esc(a.name) + '</option>'; }).join('') + '</select>' +
        '<button type="button" class="btn pri ksm" data-kaassign disabled>Assign</button><button type="button" class="btn sec ksm" data-kaclear' + (sel.some(function (x) { return !!x.e.area; }) ? '' : ' disabled') + '>Clear area</button><button type="button" class="btn sec ksm" data-kacancel>Cancel</button></div>';
    }
    function draw(b) {
      body = b || body; data();
      var site = siteObj(st.site), sec = curSec(site), ed = canEdit();
      var nA = areasOf(site, sec).length, nE = encls(site, sec).length;
      body.innerHTML = '<div class="mgpane"><div class="ka-grid">' + railHtml(site, sec) +
        '<section class="ka-main"><div class="ka-top"><p class="t-body-regular">' + esc((sec ? sec.name + ': ' : '') + 'Group a section\'s enclosures into the areas a keeper works.') + '</p>' + (ed ? '<button type="button" class="btn pri ksm" data-kanew>Create keeper area</button>' : '<span class="mgro">' + ic('info', 16) + 'Read only</span>') + '</div>' +
        '<div class="drow"><div class="seg3 ka-tabs" role="tablist" aria-label="View"><button type="button" role="tab" class="t-body-medium" data-katab="areas" aria-selected="' + (st.tab === 'areas') + '">Areas · ' + nA + '</button><button type="button" role="tab" class="t-body-medium" data-katab="enclosures" aria-selected="' + (st.tab === 'enclosures') + '">Enclosures · ' + nE + '</button></div>' +
        (st.tab === 'areas' ? areasHtml(site, sec) : encHtml(site, sec)) + '</div>' + bulkHtml() + '</section></div></div>';
    }
    /* ---- New / Edit keeper area sheet ---- */
    var dr = null;
    function drSec() { var v = dr.secVal; if (!v) return null; var p = v.split('§'); return secObj(p[0], p[1]); }
    function drSite() { return dr.secVal ? dr.secVal.split('§')[0] : null; }
    function errors() {
      var name = dr.name.trim(), sec = drSec(), out = {};
      if (!sec) out.section = 'Pick a section.';
      if (!name) out.name = 'Enter an area name or code.';
      else if (sec) { var dup = data().areas.filter(function (a) { return a !== dr.area && a.site === drSite() && a.name.trim().toLowerCase() === name.toLowerCase(); })[0]; if (dup) out.name = 'An area named "' + dup.name + '" already exists on this site.'; }
      if (!dr.active && Object.keys(dr.encl).length) out.active = 'Unassign enclosures before deactivating.';
      return out;
    }
    function openSheet(area) {
      var site = siteObj(st.site), sec = curSec(site);
      if (area && !site.all && area.site !== site.name) site = siteObj(area.site);
      dr = { area: area, secVal: area ? area.site + '§' + area.section : (sec ? secKey(sec, site) : ''), name: area ? area.name : '', active: !area || area.active !== false, encl: {}, keepers: {}, sup: null, show: false, range: '', msg: null, site: site };
      if (area) { enclOfArea(area).forEach(function (e) { dr.encl[e.name] = true; }); (area.keepers || []).forEach(function (n) { dr.keepers[n] = true; }); }
      var s0 = drSec(); dr.sup = s0 && s0.supervisor || '';
      formDraw(true);
    }
    function formDraw(first) {
      var site = dr.site, sec = drSec(), siteName = drSite(), self = dr.area ? dr.area.name : null, er = errors();
      var opts = site.sections.map(function (s) { return { v: secKey(s, site), l: site.all ? s.name + ' · ' + s.siteName.trim() : s.name }; });
      var staff = staffList(siteName), kn = Object.keys(dr.keepers);
      kn.forEach(function (n) { if (!staff.some(function (k) { return k.name === n; })) staff.unshift({ name: n, code: '' }); });
      var sups = staffList(siteName); if (dr.sup && !sups.some(function (k) { return k.name === dr.sup; })) sups.unshift({ name: dr.sup, code: '' });
      var nameErr = dr.show || dr.name.trim() ? er.name : '';
      var html = mgSheetHead(dr.area ? 'Edit keeper area' : 'New keeper area', site.all ? '' : site.name.trim()) + '<div class="mgform">' +
        '<label class="mgf' + (dr.show && er.section ? ' err' : '') + '"><span>Section</span><select data-kaf="secVal"' + (dr.area ? ' disabled' : '') + '><option value="">Pick a section</option>' + opts.map(function (o) { return '<option value="' + esc(o.v) + '"' + (o.v === dr.secVal ? ' selected' : '') + '>' + esc(o.l) + '</option>'; }).join('') + '</select><small>' + (dr.show && er.section ? er.section : 'The area belongs to this section.') + '</small></label>' +
        '<label class="mgf' + (nameErr ? ' err' : '') + '"><span>Area name / code</span><input type="text" data-kaf="name" maxlength="120" autocomplete="off" value="' + esc(dr.name) + '">' + (nameErr ? '<small>' + esc(nameErr) + '</small>' : '') + '</label>' +
        '<div class="mgf"><span>Keepers</span><p class="ka-pick">' + (kn.length ? esc(kn.join(', ')) : '<span class="ka-muted">None picked</span>') + '</p><div class="ka-box" role="group" aria-label="Keepers">' + (staff.length ? staff.map(function (k) { return '<label><input type="checkbox" data-kak="' + esc(k.name) + '"' + (dr.keepers[k.name] ? ' checked' : '') + '>' + esc(k.name) + (k.code ? '<span>' + esc(k.code) + '</span>' : '') + '</label>'; }).join('') : '<p class="none">No keeper staff yet. Add them under Keeper Staff.</p>') + '</div></div>' +
        '<label class="mgf"><span>Section supervisor</span><select data-kaf="sup"' + (sec ? '' : ' disabled') + '><option value="">' + (sec ? 'None' : '-') + '</option>' + sups.map(function (k) { return '<option value="' + esc(k.name) + '"' + (k.name === dr.sup ? ' selected' : '') + '>' + esc(k.name) + (k.code ? ' · ' + esc(k.code) : '') + '</option>'; }).join('') + '</select></label>' +
        '<div class="mgf"><span>Enclosures in this section (' + Object.keys(dr.encl).length + ' picked)</span><div class="ka-box" role="group" aria-label="Enclosures in this section">' + (sec && sec.encl.length ? sec.encl.map(function (e) { var other = e.area && e.area !== self ? e.area : '';
          return '<label' + (other ? ' class="dis"' : '') + '><input type="checkbox" data-kae="' + esc(e.name) + '"' + (dr.encl[e.name] ? ' checked' : '') + (other ? ' disabled' : '') + '>' + esc(e.name) + (other ? '<span>' + esc(other) + '</span>' : e.code ? '<span>' + esc(e.code) + '</span>' : '') + '</label>'; }).join('') : '<p class="none">' + (sec ? 'No enclosures in this section.' : 'Pick a section first.') + '</p>') + '</div></div>' +
        '<div class="ka-range"><label class="mgf"><span>Enclosure range</span><input type="text" data-kaf="range" placeholder="G1/74 to G1/80" autocomplete="off" value="' + esc(dr.range) + '"><small>Includes both ends. Adds to your current selection.</small></label><button type="button" class="btn sec ksm" data-karange style="margin-top:24px"' + (dr.range.trim() ? '' : ' disabled') + '>Add range</button></div>' +
        (dr.msg ? '<p class="ka-alert ' + dr.msg[0] + '" role="status">' + esc(dr.msg[1]) + '</p>' : '') +
        '<label class="mgchk"><input type="checkbox" data-kaf="active"' + (dr.active ? ' checked' : '') + '>Active (unassign enclosures before deactivating)</label>' +
        (er.active ? '<p class="ka-alert bad" role="alert">' + esc(er.active) + '</p>' : '') + '</div>' +
        '<div class="sheet__f"><button type="button" class="btn sec" data-mgclose>Cancel</button><button type="button" class="btn pri" data-kasave' + (er.section || !dr.name.trim() ? ' disabled' : '') + '>Save</button></div>';
      var sh, focusSel = null;
      if (first) sh = mgSheet(html, dr.area ? 'Edit keeper area' : 'New keeper area');
      else { sh = document.querySelector('#mgsheet .sheet'); var a = document.activeElement, keep = a && a.getAttribute && a.getAttribute('data-kaf'), pos = keep && a.selectionStart, top = sh.scrollTop, boxes = [].map.call(sh.querySelectorAll('.ka-box'), function (x) { return x.scrollTop; });
        sh.innerHTML = '<div class="grab"></div>' + html; sh.scrollTop = top; [].forEach.call(sh.querySelectorAll('.ka-box'), function (x, i) { x.scrollTop = boxes[i] || 0; });
        if (keep) { var f = sh.querySelector('[data-kaf="' + keep + '"]'); if (f) { f.focus(); try { if (pos != null) f.setSelectionRange(pos, pos); } catch (x) {} } } }
      if (!sh._ka) { sh._ka = true; var mine = function () { return dr && sh.querySelector('[data-kasave]'); };
        sh.addEventListener('input', function (e) { var k = e.target.getAttribute('data-kaf'); if (!mine() || !k) return; if (k === 'name' || k === 'range') { dr[k] = e.target.value; if (k === 'range') dr.msg = null; formDraw(); } });
        sh.addEventListener('change', function (e) { if (!mine()) return; var t = e.target, k = t.getAttribute('data-kaf');
          if (k === 'secVal') { dr.secVal = t.value; dr.encl = {}; var s = drSec(); dr.sup = s && s.supervisor || ''; formDraw(); }
          else if (k === 'sup') dr.sup = t.value;
          else if (k === 'active') { dr.active = t.checked; formDraw(); }
          else if (t.hasAttribute('data-kak')) { if (t.checked) dr.keepers[t.getAttribute('data-kak')] = true; else delete dr.keepers[t.getAttribute('data-kak')]; formDraw(); }
          else if (t.hasAttribute('data-kae')) { if (t.checked) dr.encl[t.getAttribute('data-kae')] = true; else delete dr.encl[t.getAttribute('data-kae')]; formDraw(); } });
        sh.addEventListener('keydown', function (e) { if (mine() && e.key === 'Enter' && e.target.getAttribute('data-kaf') === 'range') { e.preventDefault(); addRange(); } });
        sh.addEventListener('click', function (e) { if (!mine()) return; if (e.target.closest('[data-karange]')) addRange(); if (e.target.closest('[data-kasave]')) save(); });
      }
    }
    /* Enclosure range "G1/74 to G1/80" against this section's codes (source: src/lib/keeper-enclosure-range.ts) */
    function resolveRange(input, enclosures, self) {
      var m = input.trim().match(/^(.+?)\s+to\s+(.+)$/i), a = m && m[1].trim().match(/^(.*?)(\d+)$/), b = m && m[2].trim().match(/^(.*?)(\d+)$/);
      if (!a || !b) throw new Error('Enter a range such as G1/74 to G1/80.');
      var prefix = a[1].toLowerCase(); if (prefix !== b[1].toLowerCase()) throw new Error('Both ends must use the same prefix, such as G1/.');
      var first = Number(a[2]), last = Number(b[2]); if (last < first || last - first >= 10000) throw new Error('Use an ascending range of up to 10,000 enclosures.');
      var byNum = {}; enclosures.forEach(function (e) { var p = String(e.code || e.name).trim().match(/^(.*?)(\d+)$/); if (p && p[1].toLowerCase() === prefix) (byNum[Number(p[2])] = byNum[Number(p[2])] || []).push(e); });
      var names = [], issues = [];
      for (var n = first; n <= last; n++) { var c = byNum[n] || [], label = a[1] + n;
        if (!c.length) issues.push(label + ': not found in this section'); else if (c.length > 1) issues.push(label + ': more than one matching enclosure'); else if (c[0].area && c[0].area !== self) issues.push(label + ': assigned to another area'); else names.push(c[0].name); }
      if (issues.length) throw new Error('Range not added. ' + issues.slice(0, 8).join('; ') + (issues.length > 8 ? '; and ' + (issues.length - 8) + ' more' : '') + '.');
      return names;
    }
    function addRange() {
      try { var sec = drSec(); if (!sec) throw new Error('Pick a section first.');
        var names = resolveRange(dr.range, sec.encl, dr.area ? dr.area.name : null), before = Object.keys(dr.encl).length;
        names.forEach(function (n) { dr.encl[n] = true; }); dr.msg = ['ok', (Object.keys(dr.encl).length - before) + ' enclosures added to selection. Save the area to apply.'];
      } catch (err) { dr.msg = ['warn', err.message]; }
      formDraw();
    }
    function save() {
      var er = errors(); dr.show = true; if (er.section || er.name || er.active) { formDraw(); return; }
      var d = data(), sec = drSec(), siteName = drSite(), name = dr.name.trim(), a = dr.area, creating = !a;
      if (creating) { a = { name: name, site: siteName, section: sec.name, keepers: [], active: true }; d.areas.push(a); }
      var oldName = a.name; a.name = name; a.keepers = Object.keys(dr.keepers); a.active = dr.active;
      sec.encl.forEach(function (e) { if (dr.encl[e.name]) e.area = name; else if (e.area === oldName || e.area === name) e.area = ''; });
      if (dr.sup) sec.supervisor = dr.sup; else delete sec.supervisor;
      d.areas.sort(function (x, y) { return coll.compare(x.site, y.site) || coll.compare(x.section, y.section) || coll.compare(x.name, y.name); });
      persist(); dr = null; mgClose(); draw(); toast(creating ? 'Keeper area created' : 'Keeper area saved');
    }
    function undoAreas(list, was) { return function () { list.forEach(function (x, i) { x.e.area = was[i] || ''; }); persist(); draw(); }; }

    /* ---- what other pages read ---- */
    MGAPI.keeperSites = function () { return data().sites; };
    MGAPI.areas = function () { return MGAPI.keeperAreas(); };   /* the name the Packaging List page reads */
    MGAPI.keeperAreas = function () { return data().areas.map(function (a) { return Object.assign({}, a, { enclosures: enclOfArea(a).map(function (e) { return e.name; }) }); }); };
    MGAPI.staffAssignments = function (name) {
      var d = data(), areas = d.areas.filter(function (a) { return (a.keepers || []).indexOf(name) !== -1; }), sections = [];
      d.sites.forEach(function (s) { s.sections.forEach(function (x) { if (x.supervisor === name) sections.push(x.name); }); });
      return { areas: areas.map(function (a) { return { name: a.name, enclosures: enclOfArea(a).length, active: a.active !== false }; }), sections: sections,
        coverage: areas.map(function (a) { return { area: a.name, enclosures: enclOfArea(a).map(function (e) { return { name: e.name, species: e.species || 0, animals: e.animals || 0 }; }) }; }) };
    };
    MGAPI.renameKeeper = function (from, to) { var d = data(), hit = false;
      d.areas.forEach(function (a) { var i = (a.keepers || []).indexOf(from); if (i !== -1) { a.keepers[i] = to; hit = true; } });
      d.sites.forEach(function (s) { s.sections.forEach(function (x) { if (x.supervisor === from) { x.supervisor = to; hit = true; } }); });
      if (hit) persist(); };

    var qT;
    MGP['keeper-areas'] = { title: 'Keeper Areas', sub: 'Group enclosures into the areas a keeper works', draw: function (b) { more = {}; draw(b); },
      onReset: function () { D = null; st.tab = null; },
      click: function (e) { var t;
        if ((t = e.target.closest('[data-kasec]'))) { st.section = t.getAttribute('data-kasec') || null; st.sel = {}; more = {}; draw(); return; }
        if ((t = e.target.closest('[data-katab]'))) { st.tab = t.getAttribute('data-katab'); draw(); return; }
        if ((t = e.target.closest('[data-kascope]'))) { st.scope = t.getAttribute('data-kascope'); more.enc = false; draw(); return; }
        if ((t = e.target.closest('[data-kamore]'))) { var k = t.getAttribute('data-kamore'); more[k] = !more[k]; draw(); return; }
        if (!canEdit()) return;
        if (e.target.closest('[data-kanew]')) { openSheet(null); return; }
        if ((t = e.target.closest('[data-kaarea]'))) { openSheet(data().areas[Number(t.getAttribute('data-kaarea'))]); return; }
        if ((t = e.target.closest('[data-kakey]'))) { var k2 = t.getAttribute('data-kakey'); if (st.sel[k2]) delete st.sel[k2]; else st.sel[k2] = true; draw(); return; }
        if (e.target.closest('[data-kacancel]')) { st.sel = {}; draw(); return; }
        if (e.target.closest('[data-kaassign]')) { var to = body.querySelector('[data-kabarea]').value, sel = selected(); if (!to || !sel.length) return;
          var moved = sel.filter(function (x) { return x.e.area !== to; }), was = moved.map(function (x) { return x.e.area; });
          moved.forEach(function (x) { x.e.area = to; }); st.sel = {}; persist(); draw(); toastUndo(moved.length + ' enclosure' + (moved.length === 1 ? '' : 's') + ' assigned to ' + to, undoAreas(moved, was)); return; }
        if (e.target.closest('[data-kaclear]')) { var sl = selected().filter(function (x) { return !!x.e.area; }); if (!sl.length) return; var w2 = sl.map(function (x) { return x.e.area; });
          sl.forEach(function (x) { x.e.area = ''; }); st.sel = {}; persist(); draw(); toastUndo(sl.length + ' enclosure' + (sl.length === 1 ? '' : 's') + ' unassigned', undoAreas(sl, w2)); } },
      change: function (e) { var t = e.target;
        if (t.matches('[data-kasite]')) { st.site = t.value; lsSet('antz.kitchen.site', t.value); st.section = null; st.sel = {}; more = {}; draw(); }
        else if (t.matches('[data-kasecsel]')) { st.section = t.value || null; st.sel = {}; more = {}; draw(); }
        else if (t.matches('[data-kabarea]')) { body.querySelector('[data-kaassign]').disabled = !t.value; } },
      input: function (e) { var t = e.target; if (t.matches('[data-kaq]') || t.matches('[data-karq]')) { var key = t.matches('[data-kaq]') ? 'q' : 'rq', sel = key === 'q' ? '[data-kaq]' : '[data-karq]', v = t.value; clearTimeout(qT);
        qT = setTimeout(function () { st[key] = v; if (key === 'q') more.enc = false; draw(); var i = body.querySelector(sel); if (i) { i.focus(); i.setSelectionRange(v.length, v.length); } }, 150); } } };
  })();
'''}
