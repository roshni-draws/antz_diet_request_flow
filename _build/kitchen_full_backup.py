# kitchen_full_backup.py: NOT exec'd by build.py. The earlier full kitchen-home build (Kitchen Dashboard and Keeper Areas as
# Meal Group Management), kept for reuse. To restore, exec this instead of kitchen.py in build.py.
# kitchen.py: exec'd by build.py after home2.py. Builds kitchen-home.html, the target of the Kitchen tile on
# diet-module-flow.html. Two tabs: Kitchen Dashboard (#dashboard) and Meal Group Management (#meal-groups).
# Source (read-only): V2 Tab prototype of dev kitchen, kitchen/dashboard.* (Kitchen & Warehouse Dashboard) and the
# "Meal Group Mgmt" nav group, of which Keeper Areas (kitchen/keeper-areas.*) holds the meal groups themselves.
# Data: kitchen-data.json, copied unchanged from kitchen/dashboard.data.js, keeper-areas.data.js and sites.data.js.
# Reuses the Diet home shell (HEAD_CSS, DIR_CSS2, STATUS_HTML, SITE_BTN, helpers) without changing it.

_kraw = open(os.path.join(HERE, 'kitchen-data.json'), encoding='utf-8').read().replace(' – ', ' to ').replace('–', '-').replace('—', '-')
KDATA = json.loads(_kraw)
K_ICONS = ['back', 'search', 'dropdown', 'location-icon', 'time', 'timer', 'calendar', 'alert', 'info', 'list', 'user', 'grid', 'paw',
           'transfer', 'close', 'add', 'pencil', 'approved', 'book', 'cancel', 'just-tick-mark', 'history']
N_AREAS = len(KDATA['areas']['areas'])

KITCHEN_CSS = '''    /* =========================================================
       K. KITCHEN HOME  (Kitchen Dashboard + Meal Group Management)
       ========================================================= */
    .mtabs.k2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .seg2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .seg3 button .n { margin-left: 4px; opacity: .75; font-variant-numeric: tabular-nums; }
    .kpane { display: grid; gap: 16px; padding-top: 16px; }
    .kcard { background: var(--white); border-radius: var(--radius); padding: 16px 20px; display: grid; gap: 12px; min-width: 0; align-content: start; }
    .kcard > h3, .khd h3 { color: var(--head); }
    .khd { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
    .khd small, .kcap { color: var(--md3-neutral-secondary); }
    .kcap { display: flex; gap: 6px; align-items: flex-start; font-size: 13px; }
    .kcap svg { flex: none; margin-top: 1px; }
    .kctx { display: grid; gap: 10px; }
    .kline { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; color: var(--ink); }
    .kline svg { color: var(--md3-on-primary-container); }
    .krow { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .krow .spchip { height: 44px; }
    .krow .lab { color: var(--ink); font-weight: 600; margin-right: 4px; }
    .krow .sp { flex: 1; }
    .kdate { display: inline-flex; align-items: center; gap: 6px; color: var(--head); font-weight: 600; }
    .kgrid { display: grid; gap: 16px; grid-template-columns: minmax(0, 1fr); }
    .tiles { display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .tiles.t3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .tile2 { border-radius: 8px; padding: 12px 14px; display: grid; gap: 2px; background: var(--md3-background); text-align: left; min-height: 88px; align-content: start; }
    .tile2 .n { color: var(--ink); font-size: 13px; font-weight: 600; }
    .tile2 b { font-size: 28px; font-weight: 600; color: var(--head); font-variant-numeric: tabular-nums; }
    .tile2 small { color: var(--md3-neutral-secondary); font-size: 12px; }
    .tile2.warn { background: #FFF6DB; } .tile2.warn .n { color: #6B4E00; }
    .tile2.bad { background: rgba(233, 51, 83, .10); } .tile2.bad .n { color: #B3213F; }
    .tile2.ok b { color: var(--md3-on-surface); }
    button.tile2 { cursor: pointer; } button.tile2:active { transform: scale(.98); }
    .kpi { position: relative; }
    .kpi .ki { position: absolute; top: 12px; right: 12px; width: 36px; height: 36px; border-radius: 8px; display: grid; place-items: center; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .kpi .dl { justify-self: start; margin-top: 6px; display: inline-flex; align-items: center; height: 22px; padding: 0 8px; border-radius: 4px; background: var(--neutral05); color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; }
    .ktab { width: 100%; border-collapse: collapse; }
    .ktab th { text-align: left; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; color: var(--ink); background: var(--md3-surface-variant); padding: 8px 10px; }
    .ktab td { padding: 10px; border-top: 1px solid var(--md3-surface-variant); color: var(--head); vertical-align: top; }
    .ktab td small { display: block; color: var(--md3-neutral-secondary); }
    .ktab .r { text-align: right; font-variant-numeric: tabular-nums; }
    .ktab .unit { display: inline-flex; height: 22px; padding: 0 8px; border-radius: 4px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); font-size: 12px; font-weight: 600; align-items: center; }
    .bars { display: flex; align-items: flex-end; gap: 14px; height: 160px; padding: 8px 4px 0; border-bottom: 1px solid var(--md3-surface-variant); }
    .bars .col { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 6px; min-width: 0; height: 100%; }
    .bars .pair { flex: 1; min-height: 0; display: flex; align-items: flex-end; gap: 4px; }
    .bars .pair i { width: 18px; border-radius: 3px 3px 0 0; background: var(--md3-primary); }
    .bars .pair i.r { background: var(--md3-tertiary); }
    .bars small { color: var(--md3-neutral-secondary); font-size: 12px; white-space: nowrap; }
    .legend { display: flex; gap: 16px; color: var(--ink); font-size: 13px; }
    .legend span { display: inline-flex; align-items: center; gap: 6px; }
    .legend i { width: 10px; height: 10px; border-radius: 2px; background: var(--md3-primary); } .legend i.r { background: var(--md3-tertiary); }
    .hbars { display: grid; gap: 8px; }
    .hbar { display: grid; grid-template-columns: minmax(0, 150px) minmax(0, 1fr) auto; align-items: center; gap: 10px; color: var(--head); }
    .hbar span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .hbar i { height: 10px; border-radius: 5px; background: var(--md3-primary); display: block; }
    .hbar.r i { background: var(--md3-tertiary); }
    .hbar b { font-variant-numeric: tabular-nums; min-width: 36px; text-align: right; }
    .qchips { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
    .qchips span { display: inline-flex; height: 28px; padding: 0 10px; border-radius: 6px; background: var(--neutral05); color: var(--head); align-items: center; font-variant-numeric: tabular-nums; }
    .krows { display: grid; gap: 8px; }
    .kr { display: flex; align-items: center; gap: 12px; min-height: 60px; padding: 10px 12px; border-radius: 8px; background: var(--md3-background); }
    .kr .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .kr .grow b { color: var(--head); }
    .kr .grow small { color: var(--ink); }
    .kr .when { text-align: right; color: var(--ink); font-size: 13px; display: grid; gap: 4px; justify-items: end; }
    .morebtn { justify-self: start; min-height: 44px; padding: 0 12px; border-radius: 8px; color: var(--md3-on-primary-container); font-weight: 600; }
    .morebtn:hover { background: var(--md3-displaybg-primary); }
    /* meal groups */
    .kpick { display: grid; gap: 12px; grid-template-columns: minmax(0, 1fr); }
    .ksel { display: flex; align-items: center; gap: 12px; }
    .ksel .ic2 { width: 40px; height: 40px; border-radius: 8px; display: grid; place-items: center; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); flex: none; }
    .ksel label { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .ksel small { color: var(--md3-neutral-secondary); font-size: 12px; }
    .kselect { width: 100%; height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--head); font: inherit; font-weight: 600; }
    .kselect:focus { border-color: var(--md3-on-primary-container); }
    .ksearch { height: 48px; display: flex; align-items: center; gap: 8px; padding: 0 12px; border: 1px solid var(--neutral05); border-radius: 8px; background: var(--neutral05); color: var(--md3-neutral-secondary); }
    .ksearch:focus-within { border-color: var(--md3-on-primary-container); background: var(--white); }
    .ksearch input { flex: 1; min-width: 0; height: 100%; border: 0; background: none; color: var(--head); font: inherit; }
    .ksearch input:focus { outline: none; }
    .kaddbtn { display: inline-flex; align-items: center; gap: 8px; height: 44px; padding: 0 16px; border-radius: 8px; background: var(--md3-on-primary-container); color: var(--white); font-weight: 600; }
    .kagrid { display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .kacard { display: grid; gap: 8px; text-align: left; padding: 14px 16px; border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); min-height: 132px; align-content: start; }
    .kacard:active { transform: scale(.99); }
    .kacard .top { display: flex; align-items: flex-start; gap: 8px; }
    .kacard .top b { flex: 1; min-width: 0; color: var(--head); font-size: 16px; font-weight: 600; }
    .kacard .sub { color: var(--md3-neutral-secondary); font-size: 13px; }
    .kacard .ln { display: flex; align-items: center; gap: 6px; color: var(--ink); min-width: 0; }
    .kacard .ln svg { color: var(--md3-on-primary-container); flex: none; }
    .kacard .ln span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .kacard .ln.none { color: var(--md3-neutral-secondary); }
    .kstats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
    .kchips { display: flex; flex-wrap: wrap; gap: 8px; }
    .kchip { display: inline-flex; align-items: center; gap: 4px; min-height: 36px; padding: 0 4px 0 12px; border-radius: 18px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); font-weight: 500; }
    .kchip.ro { padding-right: 12px; }
    .kchip button { width: 44px; height: 44px; margin: -4px -4px -4px 0; display: grid; place-items: center; border-radius: 22px; }
    .kenc { max-height: 280px; overflow-y: auto; overscroll-behavior: contain; display: grid; gap: 6px; }
    .kenc .kr { min-height: 52px; }
    .kfld { display: grid; gap: 6px; }
    .kfld > span { font-weight: 600; color: var(--head); }
    .kfld .req { color: var(--md3-error); }
    .kfld input[type="text"] { height: 48px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; font: inherit; color: var(--head); background: var(--white); }
    .kfld input[type="text"]:focus { border-color: var(--md3-on-primary-container); outline: none; }
    .kfld.err input, .kfld.err select { border-color: var(--md3-error); }
    .kfld .ferr { color: var(--md3-error); font-size: 13px; }
    .kfld .help { color: var(--md3-neutral-secondary); font-size: 13px; }
    .ktog { display: flex; align-items: center; gap: 12px; min-height: 48px; }
    .ktog input { width: 22px; height: 22px; accent-color: var(--md3-on-primary-container); }
    .kencpick { display: flex; flex-wrap: wrap; gap: 8px; max-height: 240px; overflow-y: auto; }
    .kencpick button { min-height: 44px; padding: 0 14px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); background: var(--white); color: var(--head); text-align: left; }
    .kencpick button small { color: var(--md3-neutral-secondary); margin-left: 4px; }
    .kencpick button[aria-pressed="true"] { background: var(--md3-on-primary-container); border-color: var(--md3-on-primary-container); color: var(--white); }
    .kencpick button[aria-pressed="true"] small { color: rgba(255,255,255,.8); }
    .btn.teal { background: var(--md3-on-primary-container); color: var(--white); }
    .btn.danger { border: 1px solid var(--md3-error); color: var(--md3-error); }
    .sheet__f.end { justify-content: flex-end; flex-wrap: wrap; }
    .sheet__f.end .btn { flex: none; min-width: 120px; padding: 0 20px; }
    .sheet__f .sp { flex: 1; }
    @media (orientation: landscape) {
      .kgrid.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .tiles.t4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
      .tiles.t5 { grid-template-columns: repeat(5, minmax(0, 1fr)); }
      .kpick { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .kagrid { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      .kenc { max-height: 200px; }
    }
    @media (orientation: portrait) {
      .tiles.t5 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    }
'''

KITCHEN_JS = r'''  var KD = __KDATA__;
  /* ======================= shell: tabs (#dashboard, #meal-groups) ======================= */
  var KEYS = ['dashboard', 'meal-groups'];
  function curTab() { var h = location.hash.replace(/^#/, ''); return KEYS.indexOf(h) !== -1 ? h : 'dashboard'; }
  function route() { var t = curTab(); KEYS.forEach(function (k) { document.getElementById('t-' + k).setAttribute('aria-selected', String(k === t)); document.getElementById('p-' + k).hidden = k !== t; }); document.getElementById('main').scrollTop = 0; }
  window.addEventListener('hashchange', route);
  document.querySelector('.mtabs').addEventListener('click', function (e) { var a = e.target.closest('.mtab'); if (!a) return; e.preventDefault(); location.hash = a.getAttribute('href'); });
  var SH = document.getElementById('ksheet');
  function sheet(html) { SH.querySelector('.sheet').innerHTML = '<div class="grab"></div>' + html; SH.hidden = false; }
  function closeSheet() { SH.hidden = true; MG.sheet = null; }
  function fmtN(n) { return Number(n).toLocaleString('en-IN', { maximumFractionDigits: 2 }); }

  /* ======================= Kitchen Dashboard (kitchen/dashboard.js) ======================= */
  var D = KD.dashboard;
  var GR = [['today', 'Today'], ['week', 'This week'], ['month', 'This month'], ['custom', 'Custom']];
  var DS = { view: 'overview', grain: D.defaultGrain || 'today', wh: '', rev: 'latest', expAll: false };
  var dash = document.getElementById('p-dashboard');
  function per() { return D.periods[DS.grain] || {}; }
  function pd(k) { var p = per(); return p[k] || D[k] || []; }
  function byWh(list) { return list.filter(function (r) { return !DS.wh || r.warehouse === DS.wh; }); }
  function hbars(list, red) { var mx = Math.max.apply(null, list.map(function (x) { return x.qty || x.lines || 0; }).concat([1]));
    return list.length ? '<div class="hbars">' + list.map(function (x) { var v = x.qty != null ? x.qty : x.lines; return '<div class="hbar' + (red ? ' r' : '') + ' t-body-regular"><span title="' + esc(x.name || x.reason) + '">' + esc((x.name || x.reason) + (x.unit ? ' (' + x.unit + ')' : '')) + '</span><i style="width:' + Math.max(4, v / mx * 100) + '%"></i><b>' + fmtN(v) + '</b></div>'; }).join('') + '</div>' : '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">Nothing in this period.</p>'; }
  function overview() {
    var a = D.attention, k = per().kpis || D.kpis, s = D.stock, tr = pd('trend'), mx = Math.max.apply(null, tr.map(function (t) { return t.receipts; }).concat([1]));
    var exp = byWh(D.expiry), shown = DS.expAll ? exp : exp.slice(0, 8);
    return '<section class="kcard"><h3 class="t-minor-title">' + ic('alert', 20).replace('<svg', '<svg style="display:inline;vertical-align:-4px;margin-right:6px"') + 'Needs attention</h3><div class="tiles t3">' +
        '<button type="button" class="tile2 warn" data-kgo="follow"><span class="n">Pending challans</span><b>' + a.pendingChallans + '</b><small>All dates · open Follow-ups</small></button>' +
        '<button type="button" class="tile2" data-kgo="missing"><span class="n">Missing signed DCs</span><b>' + a.missingSignedDcs + '</b><small>Receipts to review</small></button>' +
        '<button type="button" class="tile2 bad" data-kgo="expiry"><span class="n">Expired</span><b>' + a.expired + '</b><small>View expiry watchlist</small></button></div></section>' +
      '<section class="tiles t4">' + [['Receipts', k.receipts, 'Goods receipts in this period', 'list'], ['Products on receipts', k.products, 'Distinct products, including returned lines', 'grid'], ['Suppliers', k.suppliers, 'Vendors with receipts in this period', 'user'], ['Receipts with returns', k.returns, (k.receipts ? Math.round(k.returns / k.receipts * 1000) / 10 : 0) + '% of receipts · ' + plural(k.returnedLines || 0, 'returned line'), 'transfer']].map(function (x) {
        return '<div class="tile2 kpi" style="background:var(--white)"><span class="ki">' + ic(x[3], 20) + '</span><span class="n">' + x[0] + '</span><b>' + fmtN(x[1]) + '</b><small>' + esc(x[2]) + '</small><span class="dl">No change</span></div>'; }).join('') + '</section>' +
      '<p class="kcap">' + ic('info', 16) + 'Changes compare with ' + esc(per().compare || '') + '. The current period may still be in progress.</p>' +
      '<div class="kgrid two"><section class="kcard"><div class="khd"><h3 class="t-minor-title">Received and returned quantities</h3></div><p class="kcap" style="margin-top:-6px">Received is accepted into inventory. Returned quantities are separate.</p>' +
        '<table class="ktab t-body-regular"><thead><tr><th>Unit</th><th class="r">Received</th><th class="r">Returned</th></tr></thead><tbody>' + pd('quantities').map(function (q) { return '<tr><td><span class="unit">' + esc(q.unit) + '</span></td><td class="r"><b>' + fmtN(q.received) + '</b></td><td class="r">' + fmtN(q.returned) + '</td></tr>'; }).join('') + '</tbody></table>' +
        '<p class="kcap">' + ic('info', 16) + 'Compatible units are converted to kg, ltr or nos. Other units remain separate.</p></section>' +
      '<section class="kcard"><div class="khd"><h3 class="t-minor-title">Receiving trend</h3><small class="t-body-regular">Daily receipts and those with returns</small></div>' +
        '<div class="bars" role="img" aria-label="Receiving trend">' + tr.map(function (t) { return '<div class="col"><div class="pair"><i style="height:' + (t.receipts / mx * 100) + '%" title="' + t.receipts + ' receipts"></i><i class="r" style="height:' + Math.max(t.withReturns ? 3 : 0, t.withReturns / mx * 100) + '%" title="' + t.withReturns + ' with returns"></i></div><small>' + esc(t.date) + '</small></div>'; }).join('') + '</div>' +
        '<div class="legend"><span><i></i>Receipts</span><span><i class="r"></i>With returns</span></div></section>' +
      '<section class="kcard"><h3 class="t-minor-title">Top received items</h3>' + hbars(pd('topReceived')) + '</section>' +
      '<section class="kcard"><h3 class="t-minor-title">Top returned items</h3>' + hbars(pd('topReturned'), true) + '</section>' +
      '<section class="kcard"><div class="khd"><h3 class="t-minor-title">Top suppliers</h3><small class="t-body-regular">By receipt count</small></div><table class="ktab t-body-regular"><thead><tr><th>Supplier</th><th class="r">Receipts</th><th class="r">Return rate</th></tr></thead><tbody>' +
        pd('suppliers').map(function (x) { var hi = parseFloat(x.returnRate) >= 50; return '<tr><td><b>' + esc(x.name) + '</b></td><td class="r">' + x.receipts + '</td><td class="r">' + (hi ? '<span class="tag red">' + esc(x.returnRate) + '</span>' : esc(x.returnRate)) + '</td></tr>'; }).join('') + '</tbody></table>' +
        '<p class="kcap">' + ic('info', 16) + 'Return rate is receipts with returns divided by all receipts.</p></section>' +
      '<section class="kcard"><div class="khd"><h3 class="t-minor-title">Why goods were returned</h3><small class="t-body-regular">' + plural(pd('returnReasons').reduce(function (n, r) { return n + r.lines; }, 0), 'returned product line') + ', grouped by reason</small></div>' + hbars(pd('returnReasons'), true) + '</section></div>' +
      '<section class="kcard"><div class="khd"><h3 class="t-minor-title">Current stock <span class="tag teal" style="margin-left:6px">Now</span></h3><small class="t-body-regular">Recorded stock in this warehouse selection, independent of the receiving period</small></div><div class="tiles t5">' +
        [['Products', s.products, 'in store', ''], ['Containers', s.containers, 'in store', ''], ['Expired', s.expired, 'containers', 'bad'], ['Expiring', s.expiring7, 'within 7 days', 'warn'], ['In transit', s.transit, 'containers', '']].map(function (x) { return '<div class="tile2 ' + x[3] + '"><span class="n">' + x[0] + '</span><b>' + fmtN(x[1]) + '</b><small>' + x[2] + '</small></div>'; }).join('') + '</div>' +
        '<div class="qchips"><b class="t-body-title" style="margin-right:4px">In-store quantity</b>' + s.inStore.map(function (q) { return '<span class="t-body-medium">' + fmtN(q.qty) + ' ' + esc(q.unit) + '</span>'; }).join('') + '</div></section>' +
      '<section class="kcard" id="kexpiry"><div class="khd"><h3 class="t-minor-title">Expiry watchlist</h3><small class="t-body-regular">Expired stock and stock expiring through ' + esc(D.expiryThrough) + ', earliest expiry first</small></div>' +
        (exp.length ? '<div class="krows">' + shown.map(function (e) { return '<div class="kr"><span class="grow"><b class="t-body-title">' + esc(e.product) + '</b><small class="t-body-regular">' + esc(e.batch + ' · ' + e.warehouse) + '</small></span><span class="when"><span>' + esc(e.expires) + '</span>' + (e.status === 'Expired' ? '<span class="tag red">' + ic('alert', 14) + 'Expired</span>' : '<span class="tag orange">' + ic('timer', 14) + 'Soon</span>') + '</span></div>'; }).join('') + '</div>' +
          (exp.length > 8 ? '<button type="button" class="morebtn t-body-medium" data-kexp>' + (DS.expAll ? 'Show fewer' : 'Show all ' + exp.length) + '</button>' : '') : '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">Nothing expiring in this warehouse.</p>') +
        '<p class="kcap">' + ic('info', 16) + 'Expired and soon-to-expire counts are separate. In-transit containers are excluded from in-store totals.</p></section>' +
      '<p class="kcap">' + ic('info', 16) + 'Receiving and returns use the receipt date. Stock is the current recorded position. Quantities in different units are never added together. Times use Asia/Kolkata.</p>';
  }
  function follow() {
    var rows = byWh(D.pending), all = pd('receipts'), missing = all.filter(function (r) { return !r.signedDc; }), list = DS.rev === 'missing' ? missing : all;
    return '<section class="kcard"><div class="khd"><h3 class="t-minor-title">Waiting to be received (' + rows.length + ')</h3><small class="t-body-regular">Delivery challans that arrived but are not received yet</small></div>' +
        (rows.length ? '<div class="krows">' + rows.map(function (r) { return '<div class="kr"><span class="grow"><b class="t-body-title">DC ' + esc(r.dc) + ' · ' + esc(r.vendor) + '</b><small class="t-body-regular">' + esc('Vehicle ' + r.vehicle + ' · ' + r.warehouse) + '</small></span><span class="when"><span>Arrived ' + esc(r.arrived) + '</span><span class="tag orange">' + ic('timer', 14) + 'Waiting ' + esc(r.waiting) + '</span></span></div>'; }).join('') + '</div>' : '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">No challans waiting for this warehouse.</p>') + '</section>' +
      '<section class="kcard"><div class="khd"><h3 class="t-minor-title">Receipts to review</h3></div><div class="krow" role="group" aria-label="Receipts">' +
        [['latest', 'Latest receipts', all.length], ['missing', 'Missing signed DC', missing.length]].map(function (x) { return '<button type="button" class="spchip t-body-medium" data-krev="' + x[0] + '" aria-pressed="' + (DS.rev === x[0]) + '">' + x[1] + ' <span class="n">' + x[2] + '</span></button>'; }).join('') + '</div>' +
        (list.length ? '<div class="krows">' + list.map(function (r) { return '<div class="kr"><span class="grow"><b class="t-body-title">' + esc(r.grn) + ' · ' + esc(r.vendor) + '</b><small class="t-body-regular">' + esc(r.warehouse + ' · ' + plural(r.lines, 'line')) + '</small></span><span class="when"><span>Received ' + esc(r.received) + '</span>' + (r.signedDc ? '<span class="tag green">Signed DC uploaded</span>' : '<span class="tag orange">Signed DC missing</span>') + '</span></div>'; }).join('') + '</div>' : '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">No receipts here.</p>') + '</section>';
  }
  function drawDash() {
    var p = per();
    dash.innerHTML = '<div class="segwrap"><div class="seg3 seg2" role="tablist" aria-label="Dashboard views">' +
        [['overview', 'Overview', ''], ['follow', 'Follow-ups & receipts', D.pending.length]].map(function (x) { return '<button type="button" role="tab" class="t-body-medium" data-kv="' + x[0] + '" aria-selected="' + (DS.view === x[0]) + '">' + x[1] + (x[2] !== '' ? '<span class="n">' + x[2] + '</span>' : '') + '</button>'; }).join('') + '</div></div>' +
      '<div class="kpane"><section class="kcard kctx"><div class="kline t-body-regular">' + ic('location-icon', 18) + '<span>' + esc(DS.wh || 'All permitted warehouses') + '</span><span>·</span>' + ic('time', 18) + '<span>' + esc(D.updated) + '</span></div>' +
        '<div class="krow" role="group" aria-label="Period">' + GR.map(function (g) { return '<button type="button" class="spchip t-body-medium" data-kg="' + g[0] + '" aria-pressed="' + (DS.grain === g[0]) + '">' + g[1] + '</button>'; }).join('') + '<span class="sp"></span><span class="kdate t-body-medium">' + ic('calendar', 18) + esc(p.label || '') + '</span></div>' +
        '<div class="krow" role="group" aria-label="Warehouse"><span class="lab t-body-medium">Warehouse</span>' + D.warehouses.map(function (w, i) { var v = i === 0 ? '' : w; return '<button type="button" class="spchip t-body-medium" data-kw="' + esc(v) + '" aria-pressed="' + (DS.wh === v) + '">' + esc(w) + '</button>'; }).join('') + '</div></section>' +
      (DS.view === 'overview' ? overview() : follow()) + '</div>';
  }
  dash.addEventListener('click', function (e) {
    var t;
    if ((t = e.target.closest('[data-kv]'))) { DS.view = t.getAttribute('data-kv'); drawDash(); return; }
    if ((t = e.target.closest('[data-kg]'))) { DS.grain = t.getAttribute('data-kg'); drawDash(); return; }
    if ((t = e.target.closest('[data-kw]'))) { DS.wh = t.getAttribute('data-kw'); drawDash(); return; }
    if ((t = e.target.closest('[data-krev]'))) { DS.rev = t.getAttribute('data-krev'); drawDash(); return; }
    if (e.target.closest('[data-kexp]')) { DS.expAll = !DS.expAll; drawDash(); return; }
    if ((t = e.target.closest('[data-kgo]'))) { var g = t.getAttribute('data-kgo');
      if (g === 'expiry') { var x = document.getElementById('kexpiry'); if (x) x.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; }
      DS.view = 'follow'; DS.rev = g === 'missing' ? 'missing' : 'latest'; drawDash(); document.getElementById('main').scrollTop = 0; }
  });

  /* ======================= Meal Group Management: keeper areas (kitchen/keeper-areas.js) ======================= */
  var SITES = KD.sites, AREAS = KD.areas.areas, KEEPERS = KD.areas.keepers;
  var MG = { site: KD.areas.defaultSite, section: '', q: '', status: 'active', sheet: null };
  var mg = document.getElementById('p-meal-groups');
  function siteObj(n) { return SITES.filter(function (s) { return s.name.trim() === String(n).trim(); })[0]; }
  function secObj(site, n) { return (site ? site.sections : []).filter(function (x) { return x.name === n; })[0]; }
  /* an enclosure belongs to the area named on it, else to an area that lists it in the same section */
  function areaOf(site, sec, e) { if (e.area) return e.area; var a = AREAS.filter(function (x) { return x.site.trim() === site.name.trim() && x.section === sec.name && (x.enclosures || []).indexOf(e.name) !== -1; })[0]; return a ? a.name : ''; }
  function enclOf(a) { var s = siteObj(a.site), sec = secObj(s, a.section); return sec ? sec.encl.filter(function (e) { return areaOf(s, sec, e) === a.name; }) : []; }
  function stats(a) { var es = enclOf(a); return { n: es.length, sp: es.reduce(function (n, e) { return n + (e.species || 0); }, 0), an: es.reduce(function (n, e) { return n + (e.animals || 0); }, 0) }; }
  function siteAreas() { return AREAS.filter(function (a) { return a.site.trim() === MG.site.trim() && (!MG.section || a.section === MG.section); }); }
  function matches(a) { var q = MG.q.trim().toLowerCase(); if (!q) return true; return [a.name, a.section].concat(a.keepers || []).concat(enclOf(a).map(function (e) { return e.name; })).some(function (x) { return String(x).toLowerCase().indexOf(q) !== -1; }); }
  function siteSummary() { var s = siteObj(MG.site), secs = MG.section ? [secObj(s, MG.section)] : s.sections, en = 0, un = 0, an = 0;
    secs.forEach(function (x) { x.encl.forEach(function (e) { en++; an += e.animals || 0; if (!areaOf(s, x, e)) un++; }); }); return { secs: s.sections.length, en: en, un: un, an: an }; }
  function drawMG() {
    var s = siteObj(MG.site), sum = siteSummary(), base = siteAreas().filter(matches), act = base.filter(function (a) { return a.active !== false; }), ina = base.filter(function (a) { return a.active === false; });
    var list = (MG.status === 'active' ? act : MG.status === 'inactive' ? ina : base).slice().sort(function (a, b) { return a.section.localeCompare(b.section) || a.name.localeCompare(b.name); });
    var qv = MG.q;
    mg.innerHTML = '<div class="kpane"><section class="kcard"><div class="kpick">' +
        '<div class="ksel"><span class="ic2">' + ic('location-icon', 22) + '</span><label><span class="sr-only">Site</span><select class="kselect" data-mgsite>' + SITES.map(function (x) { return '<option' + (x.name.trim() === MG.site.trim() ? ' selected' : '') + '>' + esc(x.name.trim()) + '</option>'; }).join('') + '</select><small>' + plural(sum.secs, 'section') + ' · ' + fmtN(sum.an) + ' animals</small></label></div>' +
        '<div class="ksel"><span class="ic2">' + ic('grid', 22) + '</span><label><span class="sr-only">Section</span><select class="kselect" data-mgsec><option value="">All sections</option>' + s.sections.map(function (x) { return '<option' + (x.name === MG.section ? ' selected' : '') + '>' + esc(x.name) + '</option>'; }).join('') + '</select><small>' + plural(sum.en, 'enclosure') + ' · ' + sum.un + ' unassigned</small></label></div></div>' +
        '<label class="ksearch">' + ic('search', 22) + '<span class="sr-only">Search keeper areas</span><input type="search" data-mgq placeholder="Search area, keeper or enclosure" value="' + esc(qv) + '" autocomplete="off"></label>' +
        '<div class="krow" role="group" aria-label="Status">' + [['active', 'Active', act.length], ['inactive', 'Inactive', ina.length], ['all', 'All', base.length]].map(function (x) { return '<button type="button" class="spchip t-body-medium" data-mgst="' + x[0] + '" aria-pressed="' + (MG.status === x[0]) + '">' + x[1] + ' <span class="n">' + x[2] + '</span></button>'; }).join('') + '<span class="sp"></span><button type="button" class="kaddbtn t-body-medium" data-mgnew>' + ic('add', 20) + 'New keeper area</button></div></section>' +
      '<div class="khd"><h3 class="t-minor-title">Keeper areas (' + list.length + ')</h3><small class="t-body-regular">Meal groups: the enclosures each keeper feeds</small></div>' +
      (list.length ? '<div class="kagrid">' + list.map(function (a) { var st = stats(a), i = AREAS.indexOf(a);
        return '<button type="button" class="kacard" data-mgopen="' + i + '"><span class="top"><b>' + esc(a.name) + '</b>' + (a.active === false ? '<span class="pill inactive t-body-medium">Inactive</span>' : '<span class="pill active t-body-medium">Active</span>') + '</span><span class="sub">' + esc(a.section) + '</span>' +
          '<span class="ln' + ((a.keepers || []).length ? '' : ' none') + ' t-body-regular">' + ic('user', 18) + '<span>' + esc((a.keepers || []).length ? a.keepers.join(', ') : 'No keepers yet') + '</span></span>' +
          '<span class="ln t-body-regular">' + ic('grid', 18) + '<span><b style="color:var(--head)">' + st.n + '</b> enclosures · ' + st.sp + ' species · ' + plural(st.an, 'animal') + '</span></span></button>'; }).join('') + '</div>' :
        '<div class="empty"><span class="ei">' + ic('user', 24) + '</span><b class="t-minor-title">' + (base.length ? 'No keeper areas match' : 'No keeper areas yet') + '</b><span class="t-body-regular">' + (base.length ? 'Try another search or status.' : (MG.section ? 'This section has' : 'This site has') + ' no keeper area. Create one to start assigning enclosures.') + '</span></div>') + '</div>';
  }
  function detail(i) {
    var a = AREAS[i], st = stats(a), es = enclOf(a); MG.sheet = { mode: 'detail', i: i };
    sheet('<div class="sheet__h"><div><h2 class="t-major-title" id="ksT">' + esc(a.name) + '</h2><p class="t-body-regular" style="color:var(--ink)">' + esc(a.section + ' · ' + a.site.trim()) + '</p></div><button type="button" class="iconbtn" data-kclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
      '<div class="krow">' + (a.active === false ? '<span class="pill inactive t-body-medium">Inactive</span>' : '<span class="pill active t-body-medium">Active</span>') + '</div>' +
      '<div class="kstats">' + [['Enclosures', st.n], ['Species', st.sp], ['Animals', st.an]].map(function (x) { return '<div class="tile2"><span class="n">' + x[0] + '</span><b>' + fmtN(x[1]) + '</b></div>'; }).join('') + '</div>' +
      '<div class="sheet__g"><h3 class="t-minor-title">Keepers</h3>' + ((a.keepers || []).length ? '<div class="kchips">' + a.keepers.map(function (k) { var kk = KEEPERS.filter(function (x) { return x.name === k; })[0]; return '<span class="kchip ro t-body-medium">' + ic('user', 16) + esc(k) + (kk ? ' <small style="opacity:.7">' + esc(kk.code) + '</small>' : '') + '</span>'; }).join('') + '</div>' : '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">No keepers yet. Edit the area to add one.</p>') + '</div>' +
      '<div class="sheet__g"><h3 class="t-minor-title">Enclosures (' + es.length + ')</h3>' + (es.length ? '<div class="kenc">' + es.map(function (e) { return '<div class="kr"><span class="grow"><b class="t-body-title">' + esc(e.name) + '</b>' + (e.code ? '<small class="t-body-regular">' + esc(e.code) + '</small>' : '') + '</span><span class="when"><span>' + (e.species != null ? plural(e.species, 'species', 'species') : '-') + '</span><span>' + (e.animals != null ? plural(e.animals, 'animal') : 'No animals recorded') + '</span></span></div>'; }).join('') + '</div>' : '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">No enclosures assigned.</p>') + '</div>' +
      '<div class="sheet__f end"><button type="button" class="btn danger" data-mgdel>Delete</button><span class="sp"></span><button type="button" class="btn sec" data-mgtoggle>' + (a.active === false ? 'Activate' : 'Deactivate') + '</button><button type="button" class="btn teal" data-mgedit>' + ic('pencil', 20) + 'Edit</button></div>');
  }
  function form(i) {
    var a = i == null ? null : AREAS[i], site = siteObj(MG.site);
    var reuse = !!(MG.sheet && MG.sheet.mode === 'form' && MG.sheet.i === i && MG.sheet.F);
    var F = reuse ? MG.sheet.F : { section: a ? a.section : MG.section, name: a ? a.name : '', keepers: a ? (a.keepers || []).slice() : [], active: a ? a.active !== false : true, encl: {}, errs: {} };
    if (a && !reuse) enclOf(a).forEach(function (e) { F.encl[e.name] = true; });
    MG.sheet = { mode: 'form', i: i, F: F };
    var so = secObj(site, F.section);
    sheet('<div class="sheet__h"><div><h2 class="t-major-title" id="ksT">' + (a ? 'Edit keeper area' : 'New keeper area') + '</h2><p class="t-body-regular" style="color:var(--ink)">' + esc(site.name.trim()) + '</p></div><button type="button" class="iconbtn" data-kclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
      '<label class="kfld' + (F.errs.section ? ' err' : '') + '"><span>Section <b class="req">*</b></span><select class="kselect" data-ff="section"><option value="">Choose section</option>' + site.sections.map(function (x) { return '<option' + (x.name === F.section ? ' selected' : '') + '>' + esc(x.name) + '</option>'; }).join('') + '</select>' + (F.errs.section ? '<span class="ferr">' + F.errs.section + '</span>' : '<span class="help">The area belongs to this section.</span>') + '</label>' +
      '<label class="kfld' + (F.errs.name ? ' err' : '') + '"><span>Area name or code <b class="req">*</b></span><input type="text" data-ff="name" value="' + esc(F.name) + '" placeholder="Macaw walk" autocomplete="off">' + (F.errs.name ? '<span class="ferr">' + F.errs.name + '</span>' : '') + '</label>' +
      '<div class="kfld"><span>Keepers <span style="color:var(--md3-neutral-secondary);font-weight:400">(optional)</span></span>' + (F.keepers.length ? '<div class="kchips">' + F.keepers.map(function (k) { return '<span class="kchip t-body-medium">' + esc(k) + '<button type="button" data-unk="' + esc(k) + '" aria-label="Remove ' + esc(k) + '">' + ic('close', 16) + '</button></span>'; }).join('') + '</div>' : '') +
        '<select class="kselect" data-ff="keeper" style="font-weight:400"><option value="">Add keeper</option>' + KEEPERS.filter(function (k) { return F.keepers.indexOf(k.name) === -1; }).map(function (k) { return '<option value="' + esc(k.name) + '">' + esc(k.name + ' · ' + k.code) + '</option>'; }).join('') + '</select></div>' +
      '<div class="kfld"><span>Enclosures in this section</span>' + (so ? (so.encl.length ? '<div class="kencpick">' + so.encl.map(function (e) { var other = areaOf(site, so, e), mine = !!F.encl[e.name], inOther = other && (!a || other !== a.name); return '<button type="button" data-fenc="' + esc(e.name) + '" aria-pressed="' + mine + '">' + esc(e.name) + (inOther && !mine ? '<small>in ' + esc(other) + '</small>' : '') + '</button>'; }).join('') + '</div><span class="help">' + plural(Object.keys(F.encl).length, 'enclosure') + ' selected. Picking one from another area moves it here.</span>' : '<span class="help">This section has no enclosures.</span>') : '<span class="help">Choose a section first.</span>') + '</div>' +
      '<label class="ktog"><input type="checkbox" data-ff="active"' + (F.active ? ' checked' : '') + '><span><b class="t-body-title">Active</b><br><small class="t-body-regular" style="color:var(--md3-neutral-secondary)">Unassign enclosures before deactivating</small></span></label>' +
      '<div class="sheet__f end"><button type="button" class="btn sec" data-kclose>Cancel</button><button type="button" class="btn teal" data-mgsave>Save</button></div>');
  }
  function save() {
    var S = MG.sheet, F = S.F, a = S.i == null ? null : AREAS[S.i], site = siteObj(MG.site); F.errs = {};
    if (!F.section) F.errs.section = 'Choose a section.';
    if (!F.name.trim()) F.errs.name = 'Enter a name or code.';
    else if (AREAS.some(function (x) { return x !== a && x.site.trim() === site.name.trim() && x.name.toLowerCase() === F.name.trim().toLowerCase(); })) F.errs.name = 'An area with this name already exists on this site.';
    if (!F.active && Object.keys(F.encl).length) { F.active = true; form(S.i); toast('Unassign its enclosures before deactivating.'); return; }
    if (F.errs.section || F.errs.name) { form(S.i); return; }
    var nm = F.name.trim(), so = secObj(site, F.section), oldName = a ? a.name : null;
    if (!a) { a = { name: nm, site: site.name, section: F.section, keepers: [], enclosures: [], active: true }; AREAS.push(a); }
    a.name = nm; a.section = F.section; a.keepers = F.keepers.slice(); a.active = F.active;
    site.sections.forEach(function (x) { x.encl.forEach(function (e) { if (oldName && e.area === oldName) e.area = ''; }); });
    so.encl.forEach(function (e) { if (F.encl[e.name]) e.area = nm; else if (e.area === nm) e.area = ''; });
    AREAS.forEach(function (x) { if (x !== a && x.section === so.name) x.enclosures = (x.enclosures || []).filter(function (n) { return !F.encl[n]; }); });
    a.enclosures = Object.keys(F.encl);
    closeSheet(); drawMG(); toast((S.i == null ? 'Keeper area created: ' : 'Saved: ') + nm);
  }
  mg.addEventListener('click', function (e) {
    var t;
    if ((t = e.target.closest('[data-mgst]'))) { MG.status = t.getAttribute('data-mgst'); drawMG(); return; }
    if (e.target.closest('[data-mgnew]')) { MG.sheet = null; form(null); return; }
    if ((t = e.target.closest('[data-mgopen]'))) { detail(Number(t.getAttribute('data-mgopen'))); }
  });
  mg.addEventListener('change', function (e) {
    var t = e.target;
    if (t.matches('[data-mgsite]')) { MG.site = t.value; MG.section = ''; drawMG(); }
    if (t.matches('[data-mgsec]')) { MG.section = t.value; drawMG(); }
  });
  mg.addEventListener('input', function (e) { if (e.target.matches('[data-mgq]')) { MG.q = e.target.value; var pos = e.target.selectionStart; drawMG(); var n = mg.querySelector('[data-mgq]'); n.focus(); try { n.setSelectionRange(pos, pos); } catch (x) {} } });
  SH.addEventListener('click', function (e) {
    var t, S = MG.sheet;
    if (e.target === SH || e.target.closest('[data-kclose]')) { closeSheet(); return; }
    if (!S) return;
    if (S.mode === 'detail') {
      var a = AREAS[S.i];
      if (e.target.closest('[data-mgedit]')) { MG.sheet = null; form(S.i); return; }
      if (e.target.closest('[data-mgtoggle]')) { if (a.active !== false && enclOf(a).length) { toast('Unassign its enclosures before deactivating.'); return; } a.active = a.active === false; detail(S.i); drawMG(); toast(a.name + (a.active ? ' is active' : ' is inactive')); return; }
      if (e.target.closest('[data-mgdel]')) { if (!window.confirm('Delete ' + a.name + '? Its enclosures become unassigned.')) return; var s = siteObj(a.site); s.sections.forEach(function (x) { x.encl.forEach(function (en) { if (en.area === a.name) en.area = ''; }); }); AREAS.splice(S.i, 1); closeSheet(); drawMG(); toast(a.name + ' deleted'); }
      return;
    }
    var F = S.F;
    if ((t = e.target.closest('[data-unk]'))) { F.keepers = F.keepers.filter(function (k) { return k !== t.getAttribute('data-unk'); }); form(S.i); return; }
    if ((t = e.target.closest('[data-fenc]'))) { var n = t.getAttribute('data-fenc'); if (F.encl[n]) delete F.encl[n]; else F.encl[n] = true; form(S.i); return; }
    if (e.target.closest('[data-mgsave]')) save();
  });
  SH.addEventListener('change', function (e) {
    var S = MG.sheet, t = e.target; if (!S || S.mode !== 'form') return; var F = S.F;
    if (t.matches('[data-ff="section"]')) { F.section = t.value; F.encl = {}; delete F.errs.section; form(S.i); }
    if (t.matches('[data-ff="keeper"]') && t.value) { F.keepers.push(t.value); form(S.i); }
    if (t.matches('[data-ff="active"]')) F.active = t.checked;
  });
  SH.addEventListener('input', function (e) { var S = MG.sheet; if (S && S.mode === 'form' && e.target.matches('[data-ff="name"]')) S.F.name = e.target.value; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !SH.hidden) closeSheet(); });

  drawDash(); drawMG(); route();
'''

_kbody = f'''  <div class="app">
{STATUS_HTML}
    <div class="head">
      <header class="bar">
        <a class="iconbtn" href="diet-module-flow.html" aria-label="Back to Modules">{svg("back", 24)}</a>
        <div class="bar__hd"><h1 class="t-medium-medium">Kitchen</h1></div>
        {SITE_BTN}
      </header>
      <nav class="mtabs k2" role="tablist" aria-label="Kitchen sections"><a class="mtab t-minor-medium" role="tab" id="t-dashboard" href="#dashboard" aria-controls="p-dashboard" aria-selected="true">Kitchen Dashboard</a><a class="mtab t-minor-medium" role="tab" id="t-meal-groups" href="#meal-groups" aria-controls="p-meal-groups" aria-selected="false">Meal Group Management</a></nav>
    </div>
    <main class="main" id="main"><section class="pane" id="p-dashboard" role="tabpanel" aria-labelledby="t-dashboard"></section><section class="pane" id="p-meal-groups" role="tabpanel" aria-labelledby="t-meal-groups" hidden></section></main>
  </div>
  <div class="scrim" id="ksheet" hidden><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="ksT"></div></div>
  <div class="toast t-body-medium" id="toast" role="status" aria-live="polite"></div>'''

_khelp = icon_js(K_ICONS) + HELPERS_JS[len(icon_js(ALL_ICONS)):]
page('kitchen-home.html', 'Kitchen',
     'Kitchen home: Kitchen Dashboard (#dashboard) and Meal Group Management (#meal-groups). Target of the Kitchen tile on diet-module-flow.html. '
     'Source (read-only): V2 Tab prototype of dev kitchen, kitchen/dashboard and the Meal Group Mgmt group (Keeper Areas). Data copied unchanged into _build/kitchen-data.json. '
     'Generated by _build/kitchen.py, do not hand-edit.',
     HEAD_CSS + DIR_CSS2 + KITCHEN_CSS, _kbody,
     _khelp + KITCHEN_JS.replace('__KDATA__', json.dumps(KDATA, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')))
