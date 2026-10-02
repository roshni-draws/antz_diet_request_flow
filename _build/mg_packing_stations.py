# mg_packing_stations.py: exec'd by kitchen.py. Meal Group Management > Packing Stations.
# Source: Dev system_local kitchen/packing-stations.{html,js,data.js} (Kitchen select, enabled stations rail, the station's
# packages in feeding-time order, read only) plus masters/packing-stations.data.js, which that page reads to decide which
# stations are enabled (Add station, Edit station, Disable / Enable; name unique per kitchen; kitchen fixed after creation).
# Both live here as two segments. Saved in MGSTORE 'packing-stations'; MGAPI.stations() gives other pages the same list.
MGMOD = {'icons': ['search', 'add', 'pencil', 'time'], 'css': '''    /* Packing Stations */
    .st-seg { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .st-seg button { min-height: 44px; }
    .st-kit { display: flex; align-items: center; gap: 8px; color: var(--ink); }
    .st-kit select { height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--head); font: inherit; font-weight: 500; }
    .st-grid { display: grid; gap: 16px; align-items: start; }
    .st-rail { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 2px; }
    .st-rail .cap { display: none; }
    .st-st { flex: none; display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 14px; border-radius: 8px; background: var(--white); border: 1px solid var(--md3-outline-variant); color: var(--ink); font: inherit; font-weight: 500; text-align: left; }
    .st-st[aria-pressed="true"] { background: var(--md3-on-primary-container); border-color: var(--md3-on-primary-container); color: var(--white); }
    .st-none { color: var(--md3-neutral-secondary); }
    .st-main { min-width: 0; }
    .st-pkgs { display: grid; gap: 12px; }
    .st-pkg { border: 1px solid var(--md3-surface-variant); border-radius: 10px; overflow: hidden; }
    .st-pkg .hd { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 12px; padding: 10px 12px; background: var(--md3-background); }
    .st-pkg .time { display: inline-flex; align-items: center; gap: 4px; font-weight: 600; color: var(--md3-on-primary-container); font-variant-numeric: tabular-nums; }
    .st-pkg .dest { color: var(--head); font-weight: 600; }
    .st-pkg .cap2 { color: var(--md3-neutral-secondary); font-size: 13px; }
    .st-line { display: flex; justify-content: space-between; gap: 12px; padding: 8px 12px; border-top: 1px solid var(--line); color: var(--head); }
    .st-line .q { font-variant-numeric: tabular-nums; color: var(--ink); white-space: nowrap; }
    .st-dim b { color: var(--md3-neutral-secondary); font-weight: 500; }
    .st-chip.on { background: #E3F4EA; color: #1E6B3C; } .st-chip.off { background: var(--md3-background); color: var(--md3-neutral-secondary); }
    @media (orientation: landscape) {
      .st-grid { grid-template-columns: 260px minmax(0, 1fr); }
      .st-rail { display: grid; gap: 4px; overflow: visible; }
      .st-rail .cap { display: block; color: var(--md3-neutral-secondary); font-size: 13px; padding: 0 2px 4px; }
      .st-st { width: 100%; }
    }
''', 'js': r'''  (function () {
    var DAY = { 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun' };
    var st = { view: 'pack', k: 0, s: 0, q: '', kf: '', status: 'all', more: false }, body = null;
    function data() { return MGSTORE.get('packing-stations'); }
    function kitchens(D) { return D.kitchens.filter(function (k) { return k.type === 'KITCHEN'; }).sort(function (a, b) { return a.name.localeCompare(b.name); }); }
    MGAPI.stations = function () { var D = data(); return D ? D.stations.map(function (s) { return { id: s.id, name: s.name, kitchen: s.kitchen, active: s.isActive !== false }; }) : []; };
    /* Opens Items to pack on one station (used by the Kitchen Operator's Requests view) */
    MGAPI.stationOpen = function (id) { var D = data(), r = D.stations.filter(function (x) { return x.id === id; })[0]; if (!r) return; var ks = kitchens(D), k = ks.map(function (x) { return x.name; }).indexOf(r.kitchen); if (k === -1) return;
      st.view = 'pack'; st.k = k; st.s = Math.max(0, D.stations.filter(function (x) { return x.kitchen === r.kitchen && x.isActive !== false; }).indexOf(r)); };
    function days(p) { var d = (p.days || []).slice().sort(function (a, b) { return a - b; }); return d.length === 7 ? 'Daily' : d.map(function (x) { return DAY[x] || x; }).join(', '); }
    function packView(D) {
      var ks = kitchens(D);
      if (!ks.length) return '<div class="empty"><span class="ei">' + ic('list', 24) + '</span><b class="t-minor-title">No kitchens marked yet</b><span class="t-body-regular">Mark the kitchen entities in Masters, Kitchens/Warehouse, by setting their Type to Kitchen.</span></div>';
      var k = ks[Math.min(st.k, ks.length - 1)], stations = D.stations.filter(function (s) { return s.kitchen === k.name && s.isActive !== false; }), sel = stations[st.s];
      var h = '<div class="mgbar"><label class="st-kit"><span class="t-body-medium">Kitchen</span><select data-stk aria-label="Kitchen">' + ks.map(function (x, i) { return '<option value="' + i + '"' + (x === k ? ' selected' : '') + '>' + esc(x.name) + '</option>'; }).join('') + '</select></label></div>' +
        '<div class="st-grid"><nav class="st-rail" aria-label="Packing stations"><span class="cap">Packing stations · ' + stations.length + '</span>' +
        stations.map(function (s, i) { return '<button type="button" class="st-st" data-sti="' + i + '" aria-pressed="' + (i === st.s) + '">' + esc(s.name) + '</button>'; }).join('') +
        (stations.length ? '' : '<p class="st-none t-body-regular">No enabled packing stations in this kitchen. Add or enable them under Stations.</p>') + '</nav>' +
        '<section class="drow st-main"><h3 class="t-minor-title">' + (sel ? 'Items to pack · ' + esc(sel.name) : 'Items to pack') + '</h3>';
      if (!sel) h += '<p class="st-none t-body-regular">Select a packing station.</p>';
      else {
        var pk = (D.packages[sel.id] || []).slice().sort(function (a, b) { return String(a.t).localeCompare(String(b.t)); });
        h += pk.length ? '<div class="st-pkgs">' + pk.map(function (p) {
          var dest = [p.site, p.section, p.enc].filter(Boolean).join(' › ') || '-';
          return '<div class="st-pkg"><div class="hd"><span class="time">' + ic('time', 16) + esc(p.t) + '</span><span class="dest">' + esc(dest) + '</span><span class="cap2">' + esc(days(p)) + '</span>' + (p.n != null ? '<span class="cap2">· ' + p.n + ' animal' + (p.n === 1 ? '' : 's') + '</span>' : '') + '</div>' +
            ((p.items || []).length ? p.items.map(function (it) { return '<div class="st-line t-body-regular"><span>' + esc(it[0]) + '</span><span class="q">' + fmtN(it[1]) + (it[2] ? ' ' + esc(it[2]) : '') + '</span></div>'; }).join('') : '<div class="st-line st-none">No items in this package.</div>') + '</div>';
        }).join('') + '</div>' : '<p class="st-none t-body-regular">Nothing is configured for this station yet. Add packages in the packing workspace.</p>';
      }
      return h + '</section></div>';
    }
    function stationsView(D) {
      var ed = canEdit(), q = st.q.trim().toLowerCase();
      var rows = D.stations.filter(function (s) { return (!st.kf || s.kitchen === st.kf) && (st.status === 'all' || (st.status === 'active') === (s.isActive !== false)) && (!q || (s.name + ' ' + s.kitchen).toLowerCase().indexOf(q) !== -1); });
      var shown = st.more || rows.length <= 11 ? rows : rows.slice(0, 10);
      var kn = D.kitchens.map(function (k) { return k.name; });
      return '<section class="drow"><div class="mgbar"><label class="mgsearch">' + ic('search', 20) + '<input type="search" data-stq placeholder="Search" value="' + esc(st.q) + '" aria-label="Search stations" autocomplete="off"></label>' +
        '<label class="st-kit"><span class="sr-only">Kitchen</span><select data-stkf aria-label="Kitchen"><option value="">All kitchens</option>' + kn.map(function (n) { return '<option' + (st.kf === n ? ' selected' : '') + '>' + esc(n) + '</option>'; }).join('') + '</select></label>' +
        '<label class="st-kit"><span class="sr-only">Status</span><select data-stst aria-label="Status">' + [['all', 'All'], ['active', 'Enabled'], ['inactive', 'Disabled']].map(function (o) { return '<option value="' + o[0] + '"' + (st.status === o[0] ? ' selected' : '') + '>' + o[1] + '</option>'; }).join('') + '</select></label>' +
        (ed ? '<button type="button" class="btn pri ksm" data-stadd>' + ic('add', 20) + 'Add station</button>' : '<span class="mgro">' + ic('info', 16) + 'Read only</span>') + '</div>' +
        '<p class="kcap t-body-regular">' + ic('info', 16) + esc('Work benches inside each kitchen where packages are assembled. Package templates are managed in the Operations workspace.') + '</p>' +
        (rows.length ? '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Name</th><th>Kitchen</th><th>Status</th>' + (ed ? '<th></th>' : '') + '</tr></thead><tbody>' +
          shown.map(function (s) { var on = s.isActive !== false; var cls = (ed ? 'mgrow' : '') + (on ? '' : ' st-dim'); return '<tr' + (cls.trim() ? ' class="' + cls.trim() + '"' : '') + (ed ? ' data-stid="' + s.id + '"' : '') + '><td><b>' + esc(s.name) + '</b></td><td>' + esc(s.kitchen || '-') + '</td><td><span class="kchip st-chip ' + (on ? 'on">Enabled' : 'off">Disabled') + '</span></td>' + (ed ? '<td class="r"><button type="button" class="btn sec ksm">' + ic('pencil', 18) + 'Edit</button></td>' : '') + '</tr>'; }).join('') + '</tbody></table></div>' +
          (shown.length < rows.length || st.more && rows.length > 11 ? '<button type="button" class="linkbtn t-body-medium kmore" data-stmore>' + (st.more ? 'Show fewer' : 'Show all ' + rows.length) + '</button>' : '')
          : '<div class="empty"><span class="ei">' + ic('list', 24) + '</span><b class="t-minor-title">No ' + (st.status === 'all' ? '' : st.status === 'active' ? 'enabled ' : 'disabled ') + 'stations.</b></div>') + '</section>';
    }
    function draw(b) {
      body = b || body; var D = data();
      body.innerHTML = '<div class="mgpane"><p class="t-body-regular st-none">' + esc(D.header.subtitle) + '</p>' +
        '<div class="seg3 st-seg" role="tablist" aria-label="Packing stations view"><button type="button" role="tab" class="t-body-medium" data-stv="pack" aria-selected="' + (st.view === 'pack') + '">Items to pack</button><button type="button" role="tab" class="t-body-medium" data-stv="list" aria-selected="' + (st.view === 'list') + '">Stations - ' + D.stations.length + '</button></div>' +
        (st.view === 'pack' ? packView(D) : stationsView(D)) + '</div>';
    }
    function form(id) {
      var D = data(), r = id != null ? D.stations.filter(function (s) { return s.id === id; })[0] : null, kn = D.kitchens.map(function (k) { return k.name; });
      var sh = mgSheet(mgSheetHead(r ? 'Edit station' : 'Add station', '') + '<div class="mgform">' +
        '<label class="mgf" data-stfn><span>Name *</span><input type="text" data-stn value="' + esc(r ? r.name : '') + '" autocomplete="off"><small data-sth></small></label>' +
        '<label class="mgf"><span>Kitchen *</span><select data-stkk' + (r ? ' disabled' : '') + '>' + (r ? '' : '<option value="">Select kitchen</option>') + kn.map(function (n) { return '<option' + (r && r.kitchen === n ? ' selected' : '') + '>' + esc(n) + '</option>'; }).join('') + '</select>' + (r ? '<small>Stations stay with their kitchen</small>' : '') + '</label></div>' +
        '<div class="sheet__f">' + (r ? '<button type="button" class="btn ' + (r.isActive !== false ? 'danger' : 'sec') + '" data-sttog>' + (r.isActive !== false ? 'Disable' : 'Enable') + '</button>' : '<button type="button" class="btn sec" data-mgclose>Cancel</button>') + '<button type="button" class="btn pri" data-stsave>Save</button></div>', r ? 'Edit station' : 'Add station');
      var n = sh.querySelector('[data-stn]'), kk = sh.querySelector('[data-stkk]'), save = sh.querySelector('[data-stsave]');
      function err(m) { sh.querySelector('[data-stfn]').classList.toggle('err', !!m); sh.querySelector('[data-sth]').textContent = m || ''; }
      function can() { save.disabled = !n.value.trim() || (!r && !kk.value); }
      can(); n.addEventListener('input', function () { err(''); can(); }); kk.addEventListener('change', can);
      save.addEventListener('click', function () {
        var name = n.value.trim(), k = r ? r.kitchen : kk.value; if (!name || !k) return;
        if (D.stations.some(function (x) { return x !== r && x.kitchen === k && x.name.toLowerCase() === name.toLowerCase(); })) return err('A station named "' + name + '" already exists in ' + k + '.');
        if (r) r.name = name; else D.stations.push({ id: D.stations.reduce(function (m, x) { return Math.max(m, x.id); }, 0) + 1, name: name, kitchen: k, isActive: true });
        MGSTORE.set('packing-stations', D); mgClose(); draw(); toast(r ? 'Station saved' : name + ' added');
      });
      n.addEventListener('keydown', function (e) { if (e.key === 'Enter' && !save.disabled) { e.preventDefault(); save.click(); } });
      var tg = sh.querySelector('[data-sttog]');
      if (tg) tg.addEventListener('click', function () {
        var on = r.isActive !== false;
        function go() { r.isActive = !on; MGSTORE.set('packing-stations', D); mgClose(); st.s = 0; draw(); toastUndo(r.name + (on ? ' disabled' : ' enabled'), function () { var D2 = data(); D2.stations.forEach(function (x) { if (x.id === r.id) x.isActive = on; }); MGSTORE.set('packing-stations', D2); draw(); }); }
        if (on) mgConfirm({ title: 'Disable ' + r.name + '?', text: 'It leaves the station rail of ' + r.kitchen + ' and the packaging list. You can enable it again here.', ok: 'Disable', danger: true, onOk: go }); else go();
      });
    }
    var qT;
    MGP['packing-stations'] = { title: 'Packing Stations', sub: 'What each bench packs, and the stations of each kitchen', draw: draw,
      click: function (e) { var t;
        if ((t = e.target.closest('[data-stv]'))) { st.view = t.getAttribute('data-stv'); draw(); return; }
        if ((t = e.target.closest('[data-sti]'))) { st.s = Number(t.getAttribute('data-sti')); draw(); return; }
        if (e.target.closest('[data-stadd]') && canEdit()) { form(null); return; }
        if (e.target.closest('[data-stmore]')) { st.more = !st.more; draw(); return; }
        if ((t = e.target.closest('[data-stid]')) && canEdit()) form(Number(t.getAttribute('data-stid'))); },
      change: function (e) { var t = e.target;
        if (t.matches('[data-stk]')) { st.k = Number(t.value); st.s = 0; draw(); }
        if (t.matches('[data-stkf]')) { st.kf = t.value; draw(); }
        if (t.matches('[data-stst]')) { st.status = t.value; draw(); } },
      input: function (e) { if (e.target.matches('[data-stq]')) { clearTimeout(qT); var v = e.target.value; qT = setTimeout(function () { st.q = v; draw(); var i = body.querySelector('[data-stq]'); i.focus(); i.setSelectionRange(v.length, v.length); }, 150); } } };
  })();
'''}
