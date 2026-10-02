# mg_piece_weights.py: exec'd by kitchen.py. Meal Group Management > Piece Weights.
# Source: Dev system_local kitchen/piece-weights.{html,js,data.js}. Category rail, Missing / Set / Counted / All toggle,
# search, row tap opens the weight sheet (grams, or Counted). Saved in MGSTORE 'piece-weights'; the Prep Sheet reads the
# same copy through mgPieceWeights(), so a new weight changes its Pieces column.
MGMOD = {'icons': ['search'], 'css': '''    /* Piece Weights */
    .pw-grid { display: grid; gap: 16px; align-items: start; }
    .pw-cats { display: flex; gap: 8px; overflow-x: auto; padding-bottom: 2px; }
    .pw-cat { flex: none; display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 14px; border-radius: 8px; background: var(--white); border: 1px solid var(--md3-outline-variant); color: var(--ink); font: inherit; font-weight: 500; }
    .pw-cat span { color: var(--md3-neutral-secondary); font-variant-numeric: tabular-nums; }
    .pw-cat[aria-pressed="true"] { background: var(--md3-on-primary-container); border-color: var(--md3-on-primary-container); color: var(--white); }
    .pw-cat[aria-pressed="true"] span { color: rgba(255,255,255,.8); }
    .pw-main { display: grid; gap: 14px; min-width: 0; }
    .pw-h { display: flex; align-items: baseline; gap: 8px; color: var(--head); }
    .pw-h span { color: var(--md3-neutral-secondary); font-weight: 500; }
    .pw-seg { grid-template-columns: repeat(4, minmax(0, 1fr)); flex: 1 1 360px; }
    .pw-seg button { min-height: 44px; }
    .pw-miss { color: #A3122E; font-weight: 600; }
    .pw-muted { color: var(--md3-neutral-secondary); }
    .pw-uom { display: inline-flex; height: 24px; align-items: center; padding: 0 8px; border-radius: 4px; background: var(--md3-background); font-size: 13px; color: var(--ink); }
    @media (orientation: landscape) {
      .pw-grid { grid-template-columns: 220px minmax(0, 1fr); }
      .pw-cats { display: grid; gap: 4px; overflow: visible; }
      .pw-cat { justify-content: space-between; width: 100%; }
    }
''', 'js': r'''  (function () {
    var st = { cat: '', view: 'missing', q: '' }, body = null;
    function data() { var d = MGSTORE.get('piece-weights'); if (!st.init) { st.view = d.defaultView || 'missing'; st.init = true; } return d; }
    function cut(r) { return r.cutSize || '-'; }
    function draw(b) {
      body = b || body; var D = data(), items = D.items, ed = canEdit();
      var cats = {}; items.forEach(function (r) { cats[r.category] = (cats[r.category] || 0) + 1; });
      var names = Object.keys(cats).sort(), base = items.filter(function (r) { return !st.cat || r.category === st.cat; });
      var n = { missing: 0, set: 0, counted: 0 }; base.forEach(function (r) { n[r.status] = (n[r.status] || 0) + 1; });
      var q = st.q.trim().toLowerCase(), rows = base.filter(function (r) { return (st.view === 'all' || r.status === st.view) && (!q || (r.name + ' ' + (r.code || '')).toLowerCase().indexOf(q) !== -1); });
      var empty = st.view === 'missing' ? 'Every piece-fed item here has a weight for each of its cut sizes.' : 'Nothing in this view.';
      body.innerHTML = '<div class="mgpane"><p class="t-body-regular pw-muted">' + esc(D.header.subtitle) + '</p><div class="pw-grid">' +
        '<nav class="pw-cats" aria-label="Categories"><button type="button" class="pw-cat" data-pwcat="" aria-pressed="' + !st.cat + '">All items<span>' + items.length + '</span></button>' +
          names.map(function (c) { return '<button type="button" class="pw-cat" data-pwcat="' + esc(c) + '" aria-pressed="' + (st.cat === c) + '">' + esc(c) + '<span>' + cats[c] + '</span></button>'; }).join('') + '</nav>' +
        '<section class="drow pw-main"><h3 class="t-minor-title pw-h">' + esc(st.cat || 'All items') + ' <span>' + base.length + '</span></h3>' +
          '<div class="mgbar"><div class="seg3 pw-seg" role="tablist" aria-label="Show">' + [['missing', 'Missing ' + n.missing], ['set', 'Set ' + n.set], ['counted', 'Counted ' + n.counted], ['all', 'All']].map(function (t) { return '<button type="button" role="tab" class="t-body-medium" data-pwv="' + t[0] + '" aria-selected="' + (st.view === t[0]) + '">' + t[1] + '</button>'; }).join('') + '</div>' +
          '<label class="mgsearch">' + ic('search', 20) + '<input type="search" data-pwq placeholder="Search item" value="' + esc(st.q) + '" aria-label="Search item" autocomplete="off"></label>' + (ed ? '' : '<span class="mgro">' + ic('info', 16) + 'Read only</span>') + '</div>' +
          '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Item</th><th>Category</th><th>Main UOM</th><th>Cut size</th><th class="r">1 piece =</th><th class="r">Used in</th>' + (ed ? '<th></th>' : '') + '</tr></thead><tbody>' +
          (rows.length ? rows.map(function (r) { return '<tr' + (ed ? ' class="mgrow" data-pwi="' + items.indexOf(r) + '"' : '') + '><td><b>' + esc(r.name) + '</b>' + (r.code ? '<small>' + esc(r.code) + '</small>' : '') + '</td><td>' + esc(r.category) + '</td><td><span class="pw-uom">' + esc(r.uom) + '</span></td><td>' + esc(cut(r)) + '</td>' +
            '<td class="r">' + (r.status === 'counted' ? '<span class="pw-muted">counted</span>' : r.weight != null ? fmtN(r.weight) + ' g' : '<span class="pw-miss">Missing</span>') + '</td><td class="r">' + (r.usedIn || 0) + ' diet' + (r.usedIn === 1 ? '' : 's') + '</td>' +
            (ed ? '<td class="r"><button type="button" class="btn sec ksm">' + (r.weight != null ? 'Edit' : 'Set weight') + '</button></td>' : '') + '</tr>'; }).join('') : '<tr><td colspan="' + (ed ? 7 : 6) + '" class="pw-muted">' + empty + '</td></tr>') + '</tbody></table></div></section></div></div>';
    }
    function open(i) {
      var D = data(), r = D.items[i];
      var sh = mgSheet(mgSheetHead(r.name + ' · ' + cut(r), r.category + ' · main UOM ' + r.uom + ' · used in ' + (r.usedIn || 0) + ' diets') +
        '<div class="mgform"><label class="mgf" data-pwf><span>1 piece =</span><input type="number" inputmode="decimal" min="0" step="any" placeholder="grams" data-pww value="' + (r.weight != null ? r.weight : '') + '"><small data-pwh>Weight of one piece in grams.</small></label>' +
        '<label class="mgchk"><input type="checkbox" data-pwc' + (r.status === 'counted' ? ' checked' : '') + '>Counted, track by count, no weight needed</label></div>' +
        '<div class="sheet__f"><button type="button" class="btn sec" data-mgclose>Cancel</button><button type="button" class="btn pri" data-pwsave>Save</button></div>', 'Piece weight');
      var w = sh.querySelector('[data-pww]'), c = sh.querySelector('[data-pwc]'), f = sh.querySelector('[data-pwf]'), h = sh.querySelector('[data-pwh]');
      function err(m) { f.classList.toggle('err', !!m); h.textContent = m || 'Weight of one piece in grams.'; }
      function sync() { w.disabled = c.checked; if (c.checked) err(''); }
      sync(); c.addEventListener('change', sync); w.addEventListener('input', function () { err(''); });
      function save() {
        var raw = w.value.trim(), v = Number(raw);
        if (!c.checked) { if (!raw) return err('Enter the weight of one piece in grams.'); if (!isFinite(v) || v <= 0) return err('Weight must be more than 0 g.'); }
        var before = { status: r.status, weight: r.weight };
        if (c.checked) { r.status = 'counted'; r.weight = null; } else { r.status = 'set'; r.weight = Math.round(v * 100) / 100; }
        MGSTORE.set('piece-weights', D); mgClose(); draw();
        toastUndo(c.checked ? r.name + ' · ' + cut(r) + ' is counted by the piece' : 'Saved · 1 piece of ' + r.name + ' (' + cut(r) + ') = ' + fmtN(r.weight) + ' g', function () { var D2 = MGSTORE.get('piece-weights'); D2.items[i].status = before.status; D2.items[i].weight = before.weight; MGSTORE.set('piece-weights', D2); draw(); });
      }
      sh.querySelector('[data-pwsave]').addEventListener('click', save);
      w.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); save(); } });
    }
    var qT;
    MGP['piece-weights'] = { title: 'Piece Weights', sub: 'What one piece weighs, by cut size', draw: draw,
      click: function (e) { var t; if ((t = e.target.closest('[data-pwcat]'))) { st.cat = t.getAttribute('data-pwcat'); draw(); return true; } if ((t = e.target.closest('[data-pwv]'))) { st.view = t.getAttribute('data-pwv'); draw(); return true; } if ((t = e.target.closest('[data-pwi]')) && canEdit()) { open(Number(t.getAttribute('data-pwi'))); return true; } },
      input: function (e) { if (e.target.matches('[data-pwq]')) { clearTimeout(qT); var v = e.target.value; qT = setTimeout(function () { st.q = v; draw(); var i = body.querySelector('[data-pwq]'); i.focus(); i.setSelectionRange(v.length, v.length); }, 150); return true; } } };
  })();
'''}
