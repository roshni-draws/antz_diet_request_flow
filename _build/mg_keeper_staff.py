# mg_keeper_staff.py: exec'd by kitchen.py. Meal Group Management > Keeper Staff.
# Source: Dev system_local kitchen/keeper-members.{html,js,data.js} (Keeper Staff). Active / Inactive / All tabs,
# search by name, code or phone, Site filter (with "No site"), sortable table, the "no assignment" note, profile sheet
# (Enclosures / Profile / Site history), Add staff and Edit with the source validation (name, site on create, unique
# employee code), site transfer closes the posting, Deactivate / Activate with the source warning.
# Feeds Keeper Areas through MGAPI.keepers(); areas, sections and coverage come from MGAPI.staffAssignments() when
# Keeper Areas is built in (the stored copies otherwise). A rename is passed on with MGAPI.renameKeeper().
# Left out: Import Excel and the template, photo upload, and the Refresh button (nothing to re-fetch here).
MGMOD = {'icons': ['search', 'pencil'], 'css': '''    /* Keeper Staff */
    .ks-top { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
    .ks-top p { color: var(--md3-neutral-secondary); max-width: 64ch; }
    .ks-tabs { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .ks-tabs button, .ks-stabs button { min-height: 44px; }
    .ks-filt { display: grid; gap: 12px; grid-template-columns: minmax(0, 1fr) minmax(0, 240px); align-items: end; }
    .ks-filt .mgsearch { flex: none; }
    .ks-note { padding: 10px 12px; border-radius: 8px; background: #FFF6DB; color: #6B4E00; font-size: 14px; }
    .ks-cap { color: var(--md3-neutral-secondary); font-size: 13px; }
    .ks-nm { display: flex; align-items: center; gap: 10px; }
    .ks-nm .av { width: 36px; height: 36px; font-size: 13px; }
    .ks-nm small { display: block; }
    .ks-tab td.nw, .ks-tab th { white-space: nowrap; }
    .ks-sort { min-height: 44px; font: inherit; font-weight: 600; color: var(--ink); display: inline-flex; align-items: center; gap: 4px; }
    .ks-head { display: flex; align-items: flex-start; gap: 12px; }
    .ks-head .av { width: 56px; height: 56px; font-size: 18px; }
    .ks-head .grow { flex: 1; min-width: 0; display: grid; gap: 4px; }
    .ks-head h2 { color: var(--head); }
    .ks-head .sub { color: var(--md3-neutral-secondary); font-size: 14px; }
    .ks-chips { display: flex; flex-wrap: wrap; gap: 6px; }
    .ks-stabs { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .ks-panel { display: grid; gap: 12px; }
    .ks-area b { color: var(--head); }
    .ks-fld { display: flex; justify-content: space-between; gap: 12px; min-height: 44px; align-items: center; border-bottom: 1px solid var(--line); }
    .ks-fld span:first-child { color: var(--md3-neutral-secondary); }
    .ks-fld span:last-child { color: var(--head); font-weight: 500; text-align: right; }
    .ks-hist { display: grid; gap: 10px; }
    .ks-hist div { display: grid; gap: 2px; padding: 10px 12px; border-radius: 8px; background: var(--md3-background); }
    .ks-hist b { color: var(--head); }
    .ks-hist span { color: var(--md3-neutral-secondary); font-size: 14px; }
    .ks-muted { color: var(--md3-neutral-secondary); }
    .ks-conf { display: grid; gap: 10px; padding: 12px; border-radius: 8px; background: #FFF6DB; color: #6B4E00; }
    .ks-foot { display: flex; gap: 10px; flex-wrap: wrap; }
    @media (orientation: portrait) { .ks-filt { grid-template-columns: minmax(0, 1fr); } }
''', 'js': r'''  (function () {
    var body = null, st = { tab: 'active', q: '', site: '', sort: 'name', desc: false }, coll = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });
    function data() { return MGSTORE.get('keeper-staff'); }
    function rows(D) { return D.staff.map(function (r, i) { var a = MGAPI.staffAssignments ? MGAPI.staffAssignments(r.name) : { areas: r.areas || [], sections: r.sections || [], coverage: [] };
      return Object.assign({ postings: [] }, r, { i: i, areas: a.areas, sections: a.sections, coverage: a.coverage, enclosuresN: a.areas.reduce(function (n, x) { return n + (x.enclosures || 0); }, 0) }); }); }
    function initials(n) { return String(n || '').split(/\s+/).map(function (w) { return w[0] || ''; }).slice(0, 2).join('').toUpperCase() || '?'; }
    function sv(r, k) { if (k === 'areas') return r.areas.map(function (a) { return a.name; }).join(', ').toLowerCase(); if (k === 'enclosures') return r.enclosuresN; if (k === 'active') return r.active ? 0 : 1; return String(r[k] == null ? '' : r[k]).toLowerCase(); }
    function day() { return new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }); }
    function chip(cls, t) { return '<span class="kchip' + (cls ? ' ' + cls : '') + '">' + esc(t) + '</span>'; }
    var COLS = [['name', 'Name'], ['phone', 'Phone'], ['site', 'Site'], ['areas', 'Keeper areas'], ['enclosures', 'Enclosures', 1], ['active', 'Status']];
    function draw(b) {
      body = b || body; var D = data(), R = rows(D), ed = canEdit(), act = R.filter(function (r) { return r.active; }).length, noSite = D.staff.filter(function (r) { return r.site == null; }).length;
      if (st.site && st.site !== '__none' && D.sites.indexOf(st.site) === -1) st.site = '';
      var un = R.filter(function (r) { return r.active && !r.areas.length && !r.sections.length; }).length, q = st.q.trim().toLowerCase();
      var vis = R.filter(function (r) { if (q && (r.name + ' ' + (r.employeeCode || '') + ' ' + (r.phone || '')).toLowerCase().indexOf(q) === -1) return false;
        if (st.site === '__none' && r.site != null) return false; if (st.site && st.site !== '__none' && r.site !== st.site) return false;
        return st.tab === 'active' ? r.active : st.tab === 'inactive' ? !r.active : true; })
        .sort(function (a, b) { var x = sv(a, st.sort), y = sv(b, st.sort), c = typeof x === 'number' ? x - y : coll.compare(x, y); return st.desc ? -c : c; });
      body.innerHTML = '<div class="mgpane"><div class="ks-top"><p class="t-body-regular">' + esc(D.header.subtitle) + '</p>' + (ed ? '<button type="button" class="btn pri ksm" data-ksadd>Add staff</button>' : '<span class="mgro">' + ic('info', 16) + 'Read only</span>') + '</div>' +
        '<section class="drow"><h3 class="t-minor-title">Staff · this zoo</h3><div class="seg3 ks-tabs" role="tablist" aria-label="Status">' + [['active', 'Active (' + act + ')'], ['inactive', 'Inactive (' + (R.length - act) + ')'], ['all', 'All (' + R.length + ')']].map(function (t) { return '<button type="button" role="tab" class="t-body-medium" data-kstab="' + t[0] + '" aria-selected="' + (st.tab === t[0]) + '">' + t[1] + '</button>'; }).join('') + '</div>' +
        '<div class="ks-filt"><label class="mgsearch">' + ic('search', 20) + '<input type="search" data-ksq placeholder="Search name, code or phone" value="' + esc(st.q) + '" aria-label="Search name, code or phone" autocomplete="off"></label>' +
          '<label class="mgf"><span>Site</span><select data-kssite><option value="">All sites</option>' + D.sites.map(function (s) { return '<option value="' + esc(s) + '"' + (s === st.site ? ' selected' : '') + '>' + esc(s.trim()) + '</option>'; }).join('') + (noSite ? '<option value="__none"' + (st.site === '__none' ? ' selected' : '') + '>No site (' + noSite + ')</option>' : '') + '</select></label></div>' +
        (st.tab !== 'inactive' && un > 0 ? '<p class="ks-note">' + un + ' active ' + (un === 1 ? 'person has' : 'people have') + ' no keeper area or section assignment.</p>' : '') +
        '<p class="ks-cap">' + vis.length + ' of ' + R.length + ' · open a row for the full profile.</p>' +
        '<div class="ktabwrap"><table class="ktab ks-tab t-body-regular"><thead><tr>' + COLS.map(function (c) { var on = st.sort === c[0]; return '<th' + (c[2] ? ' class="r"' : '') + ' aria-sort="' + (on ? (st.desc ? 'descending' : 'ascending') : 'none') + '"><button type="button" class="ks-sort" data-kssort="' + c[0] + '">' + c[1] + (on ? (st.desc ? ' ↓' : ' ↑') : '') + '</button></th>'; }).join('') + '</tr></thead><tbody>' +
        (vis.length ? vis.map(function (r) { return '<tr class="mgrow" data-ksi="' + r.i + '"><td><span class="ks-nm"><span class="av">' + esc(initials(r.name)) + '</span><span><b>' + esc(r.name) + '</b><small>' + esc(r.employeeCode || '-') + '</small></span></span></td><td class="nw">' + esc(r.phone || '-') + '</td>' +
          '<td class="nw">' + (r.site == null ? chip('warn', 'No site') : esc(r.site.trim())) + '</td><td>' + (r.areas.map(function (a) { return esc(a.name) + (a.active === false ? ' (inactive)' : ''); }).join(', ') || '-') + '</td><td class="r">' + r.enclosuresN + '</td><td>' + chip(r.active ? 'ok' : '', r.active ? 'Active' : 'Inactive') + '</td></tr>'; }).join('')
          : '<tr><td colspan="6" class="ks-muted">' + (R.length ? 'No matches.' : 'No records yet.') + '</td></tr>') + '</tbody></table></div></section></div>';
    }
    /* ---- profile / form sheet ---- */
    var cur = null;   /* { i (-1 new), tab, editing, confirm, f: form values, show } */
    function sheet(first) {
      var D = data(), R = rows(D), r = cur.i === -1 ? null : R[cur.i], creating = !r, ed = canEdit(), editing = creating || cur.editing;
      var head = '<div class="ks-head"><span class="av">' + esc(initials(r ? r.name : cur.f.name)) + '</span><div class="grow"><h2 class="t-major-title">' + esc(creating ? 'New staff member' : r.name) + '</h2><span class="sub">' + esc(creating ? 'Not saved yet' : (r.employeeCode || 'No employee code')) + '</span>' +
        (creating ? '' : '<div class="ks-chips">' + chip(r.active ? 'ok' : '', r.active ? 'Active' : 'Inactive') + (r.site == null ? chip('warn', 'No site') : chip('', r.site.trim())) + r.areas.map(function (a) { return chip('', a.name); }).join('') + r.sections.map(function (s) { return chip('', 'Supervises ' + s); }).join('') + '</div>') + '</div>' +
        (!creating && !editing && ed ? '<button type="button" class="iconbtn" data-ksedit aria-label="Edit profile">' + ic('pencil', 22) + '</button>' : '') + '<button type="button" class="iconbtn" data-mgclose aria-label="Close">' + ic('close', 24) + '</button></div>';
      var tabs = creating ? '' : '<div class="seg3 ks-stabs" role="tablist" aria-label="Profile sections">' + [['enclosures', 'Enclosures'], ['profile', 'Profile'], ['history', 'Site history']].map(function (t) { return '<button type="button" role="tab" class="t-body-medium" data-ksst="' + t[0] + '" aria-selected="' + (cur.tab === t[0]) + '">' + t[1] + '</button>'; }).join('') + '</div>';
      var p = '';
      if (cur.tab === 'profile' || creating) p = editing ? form(D, r) : '<div class="ks-panel">' + [['Employee code', r.employeeCode || '-'], ['Phone', r.phone || '-'], ['Site', r.site ? r.site.trim() : 'No site'], ['Status', r.active ? 'Active' : 'Inactive']].map(function (f) { return '<div class="ks-fld"><span>' + f[0] + '</span><span>' + esc(f[1]) + '</span></div>'; }).join('') + '</div>';
      else if (cur.tab === 'enclosures') p = !r.areas.length ? '<p class="ks-muted">No records. Not assigned to a keeper area.</p>' : '<div class="ks-panel">' + (r.coverage || []).map(function (a) { var tot = a.enclosures.reduce(function (n, e) { return n + (e.animals || 0); }, 0);
          return '<div class="ks-area"><b class="t-body-title">' + esc(a.area) + '</b>' + (a.enclosures.length ? '<table class="ktab t-body-regular"><thead><tr><th>Enclosure</th><th class="r">Species</th><th class="r">Animals</th></tr></thead><tbody>' + a.enclosures.map(function (e) { return '<tr><td>' + esc(e.name) + '</td><td class="r">' + (e.species || 0) + '</td><td class="r">' + fmtN(e.animals || 0) + '</td></tr>'; }).join('') +
            '<tr><td><b>' + a.enclosures.length + ' ' + (a.enclosures.length === 1 ? 'enclosure' : 'enclosures') + '</b></td><td></td><td class="r"><b>' + fmtN(tot) + '</b></td></tr></tbody></table>' : '<p class="ks-muted">No records.</p>') + '</div>'; }).join('') + '<p class="ks-cap">Counts are the current collection, including group headcounts.</p></div>';
      else p = !(r.postings || []).length ? '<p class="ks-muted">No records.</p>' : '<div class="ks-hist">' + r.postings.slice().reverse().map(function (x) { return '<div><b>' + esc(x.site.trim()) + (x.to ? '' : ' ' + chip('ok', 'Current')) + '</b><span>' + esc(x.from) + ' to ' + esc(x.to || 'present') + '</span>' + (x.note ? '<span>' + esc(x.note) + '</span>' : '') + '</div>'; }).join('') + '</div>';
      var foot = !creating && !editing && ed ? (cur.confirm ? '<div class="ks-conf" role="alert"><span>Still keeper of ' + r.areas.length + ' ' + (r.areas.length === 1 ? 'area' : 'areas') + ' and supervisor of ' + r.sections.length + ' ' + (r.sections.length === 1 ? 'section' : 'sections') + '. Those assignments stay in place and will show this person as inactive.</span><div class="ks-foot"><button type="button" class="btn sec ksm" data-ksno>Cancel</button><button type="button" class="btn danger ksm" data-ksyes>Deactivate</button></div></div>'
        : '<div class="ks-foot"><button type="button" class="btn ' + (r.active ? 'danger' : 'sec') + ' ksm" data-kstoggle>' + (r.active ? 'Deactivate' : 'Activate') + '</button></div>') : '';
      var html = head + tabs + p + foot;
      if (first) mgSheet(html, creating ? 'New staff member' : r.name);
      else { var sh = document.querySelector('#mgsheet .sheet'), a = document.activeElement, keep = a && a.getAttribute && a.getAttribute('data-ksf'), pos = keep && a.selectionStart; sh.innerHTML = '<div class="grab"></div>' + html;
        if (keep) { var f = sh.querySelector('[data-ksf="' + keep + '"]'); if (f) { f.focus(); try { if (pos != null) f.setSelectionRange(pos, pos); } catch (x) {} } } }
      bind();
    }
    function problems(D) { var f = cur.f, out = {}, code = f.employeeCode.trim();
      if (!f.name.trim()) out.name = 'Enter a name.';
      if (cur.i === -1 && !f.site) out.site = 'Required: where this person works.';
      if (code) { var dup = D.staff.filter(function (x, i) { return i !== cur.i && String(x.employeeCode || '').trim().toLowerCase() === code.toLowerCase(); })[0]; if (dup) out.code = 'Employee code ' + code + ' is already used by ' + dup.name + '.'; }
      return out; }
    function form(D, r) {
      var f = cur.f, p = problems(D), moving = r && f.site && f.site !== (r.site || '');
      return '<div class="mgform">' +
        '<label class="mgf' + (cur.show && p.name ? ' err' : '') + '"><span>Name</span><input type="text" data-ksf="name" maxlength="120" autocomplete="off" value="' + esc(f.name) + '">' + (cur.show && p.name ? '<small>' + p.name + '</small>' : '') + '</label>' +
        '<label class="mgf' + (p.code ? ' err' : '') + '"><span>Employee code</span><input type="text" data-ksf="employeeCode" maxlength="40" autocomplete="off" value="' + esc(f.employeeCode) + '"><small>' + esc(p.code || 'Optional, but must be unique in this zoo.') + '</small></label>' +
        '<label class="mgf"><span>Phone</span><input type="tel" data-ksf="phone" maxlength="40" value="' + esc(f.phone) + '"></label>' +
        '<label class="mgf' + (cur.show && p.site ? ' err' : '') + '"><span>Site</span><select data-ksf="site"><option value="">Site</option>' + D.sites.map(function (s) { return '<option value="' + esc(s) + '"' + (s === f.site ? ' selected' : '') + '>' + esc(s.trim()) + '</option>'; }).join('') + '</select><small>' + (r ? 'Changing the site closes the current posting and opens a new one.' : 'Required: where this person works.') + '</small></label>' +
        (moving ? '<label class="mgf"><span>Reason for the transfer (optional)</span><input type="text" data-ksf="note" maxlength="200" value="' + esc(f.note) + '"></label>' + (r.areas.length ? '<p class="ks-note">Keeper of ' + r.areas.length + ' ' + (r.areas.length === 1 ? 'area' : 'areas') + ' at ' + esc(r.site ? r.site.trim() : '-') + '. Reassign those under Keeper Areas after the transfer.</p>' : '') : '') +
        '<label class="mgchk"><input type="checkbox" data-ksf="active"' + (f.active ? ' checked' : '') + '>Active</label>' +
        '<div class="sheet__f"><button type="button" class="btn sec" data-kscancel>Cancel</button><button type="button" class="btn pri" data-kssave' + (p.name || p.site ? ' disabled' : '') + '>' + (r ? 'Save changes' : 'Create staff') + '</button></div></div>';
    }
    function open(i, editing) { var D = data(), r = i === -1 ? null : D.staff[i];
      cur = { i: i, tab: i === -1 || editing ? 'profile' : 'enclosures', editing: !!editing, confirm: false, show: false, f: { name: r ? r.name : '', employeeCode: r ? r.employeeCode || '' : '', phone: r ? r.phone || '' : '', site: r ? r.site || '' : '', active: r ? r.active : true, note: '' } };
      sheet(true); }
    function save() {
      var D = data(), p = problems(D); cur.show = true; if (p.name || p.site || p.code) { sheet(); return; }
      var f = cur.f, creating = cur.i === -1, today = day(), name = f.name.trim(), rec;
      if (creating) { rec = { name: name, employeeCode: '', phone: '', site: f.site, active: true, areas: [], sections: [], postings: [{ site: f.site, from: today, to: null, note: '' }] }; D.staff.push(rec); }
      else { rec = D.staff[cur.i]; if (rec.name !== name && MGAPI.renameKeeper) MGAPI.renameKeeper(rec.name, name);
        var site = f.site || rec.site; if (site && site !== rec.site) { rec.postings = rec.postings || []; rec.postings.forEach(function (x) { if (!x.to) x.to = today; }); rec.postings.push({ site: site, from: today, to: null, note: f.note.trim() }); } }
      rec.name = name; rec.employeeCode = f.employeeCode.trim(); rec.phone = f.phone.trim(); rec.site = f.site || rec.site; rec.active = f.active;
      MGSTORE.set('keeper-staff', D); toast(creating ? 'Staff member created' : 'Changes saved'); draw();
      if (creating) { cur = null; mgClose(); } else { cur.editing = false; cur.tab = 'profile'; cur.show = false; sheet(); }
    }
    function toggle() { var D = data(), rec = D.staff[cur.i]; rec.active = !rec.active; MGSTORE.set('keeper-staff', D); toast(rec.active ? rec.name + ' is active again' : rec.name + ' deactivated'); cur.confirm = false; draw(); sheet(); }
    function bind() { var sh = document.querySelector('#mgsheet .sheet'); if (sh._ks) return; sh._ks = true; var mine = function () { return cur && sh.querySelector('.ks-head'); };
      sh.addEventListener('click', function (e) { if (!mine()) return; var t;
        if ((t = e.target.closest('[data-ksst]'))) { cur.tab = t.getAttribute('data-ksst'); cur.confirm = false; sheet(); return; }
        if (e.target.closest('[data-ksedit]')) { open(cur.i, true); return; }
        if (e.target.closest('[data-kscancel]')) { if (cur.i === -1) { cur = null; mgClose(); } else open(cur.i, false); return; }
        if (e.target.closest('[data-kssave]')) { save(); return; }
        if (e.target.closest('[data-kstoggle]')) { var r = rows(data())[cur.i]; if (r.active && (r.areas.length || r.sections.length)) { cur.confirm = true; sheet(); } else toggle(); return; }
        if (e.target.closest('[data-ksno]')) { cur.confirm = false; sheet(); return; }
        if (e.target.closest('[data-ksyes]')) toggle(); });
      var upd = function (e) { if (!mine()) return; var k = e.target.getAttribute('data-ksf'); if (!k) return; cur.f[k] = e.target.type === 'checkbox' ? e.target.checked : e.target.value; if (e.type === 'change' || k === 'name' || k === 'employeeCode') sheet(); };
      sh.addEventListener('input', upd); sh.addEventListener('change', function (e) { if (e.target.type === 'checkbox' || e.target.tagName === 'SELECT') upd(e); }); }

    /* ---- what Keeper Areas reads ---- */
    MGAPI.keepers = function () { return data().staff.map(function (r) { return { name: r.name, code: r.employeeCode || '', site: r.site, active: r.active !== false }; }); };

    var qT;
    MGP['keeper-staff'] = { title: 'Keeper Staff', sub: 'Keepers and supervisors posted to a site, not logins', draw: draw,
      click: function (e) { var t;
        if ((t = e.target.closest('[data-kstab]'))) { st.tab = t.getAttribute('data-kstab'); draw(); return; }
        if ((t = e.target.closest('[data-kssort]'))) { var k = t.getAttribute('data-kssort'); if (st.sort === k) st.desc = !st.desc; else { st.sort = k; st.desc = false; } draw(); return; }
        if (e.target.closest('[data-ksadd]') && canEdit()) { open(-1, true); return; }
        if ((t = e.target.closest('[data-ksi]'))) open(Number(t.getAttribute('data-ksi')), false); },
      change: function (e) { if (e.target.matches('[data-kssite]')) { st.site = e.target.value; draw(); } },
      input: function (e) { if (e.target.matches('[data-ksq]')) { clearTimeout(qT); var v = e.target.value; qT = setTimeout(function () { st.q = v; draw(); var i = body.querySelector('[data-ksq]'); i.focus(); i.setSelectionRange(v.length, v.length); }, 150); } } };
  })();
'''}
