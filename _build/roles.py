# roles.py: exec'd by home2.py right after req.py. "Viewing as" role switcher + the full request state
# machine from the V2 tab prototype (diet/dr-core.js ACCESS + transitions, request.js actions).

# SAMPLE DATA only: every request is on a species with real data, so each one configures end to end.
_req_seed = [dict(x) for x in SAMPLE_REQS]
import hashlib as _hl
SEED_V = _hl.md5((json.dumps(_req_seed, sort_keys=True) + open(os.path.join(HERE, 'kitchen-sample.json'), encoding='utf-8').read()).encode()).hexdigest()[:10]   # bumps when requests or kitchen SAMPLE DATA change
# Shared demo state (diet-home.html and kitchen-home.html): requests, proposed plans and the viewer live in
# localStorage, wrapped in try/catch; with no storage everything falls back to the seed above.
STORE_JS = '''  var RQS_KEY = 'antz.diet.requests', VIEW_KEY = 'antz.viewer', SEED_V = '__SEEDV__';
  function lsGet(k) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : null; } catch (x) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (x) {} }
  function storedReqs() { var s = lsGet(RQS_KEY); return s && s.v === SEED_V && Array.isArray(s.reqs) ? s : null; }
  function savedViewer() { var v = lsGet(VIEW_KEY); return typeof v === 'string' ? v : null; }
  function saveViewer(k) { lsSet(VIEW_KEY, k); }
  function resetDemo() { try { localStorage.removeItem(RQS_KEY); } catch (x) {} location.reload(); }
  /* Module access per role (same table as diet-module-flow.html): Diet for Dietician, Head Dietician, Kitchen Head;
     Kitchen for Kitchen Head, Kitchen Operator, Receiving Manager; Inventory for Kitchen Head and Receiving Manager;
     Security for Security and Security Admin. guardModule shows a full-screen No access state (with Viewing as)
     over a module the role cannot use, and returns false. */
  var MODS = { diet: ['dietician', 'head-dietician', 'kitchen-head'], kitchen: ['kitchen-head', 'kitchen-operator', 'receiving-manager'],
    inventory: ['kitchen-head', 'receiving-manager'], security: ['security', 'security-admin'] };
  var MODFILE = { diet: ['Diet', 'diet-home.html'], kitchen: ['Kitchen', 'kitchen-home.html'], inventory: ['Inventory', 'inventory-home.html'], security: ['Security', 'security-home.html'] };
  function canModule(mod, key) { return MODS[mod].indexOf(key) !== -1; }
  function guardModule(mod, u) {
    var el = document.getElementById('noacc');
    if (canModule(mod, u.key)) { if (el) el.hidden = true; return true; }
    if (!el) { el = document.createElement('div'); el.id = 'noacc'; el.className = 'noacc'; el.setAttribute('role', 'alertdialog'); el.setAttribute('aria-labelledby', 'noaccT'); document.body.appendChild(el); }
    var other = ['diet', 'kitchen', 'inventory', 'security'].filter(function (m) { return m !== mod && canModule(m, u.key); })[0], home = 'diet-module-flow.html?as=' + u.key, back = typeof IC !== 'undefined' && IC.back ? ic('back', 24) : '&lsaquo;';
    el.innerHTML = '<header class="bar"><a class="iconbtn" href="' + home + '" aria-label="Back to Modules">' + back + '</a><div class="bar__hd"><h1 class="t-medium-medium">' + MODFILE[mod][0] + '</h1></div><button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button></header>' +
      '<div class="noacc__in"><div class="noacc__card"><span class="noacc__i" aria-hidden="true">!</span><h2 class="t-major-title" id="noaccT">No access for ' + u.title + '</h2>' +
      '<p class="t-body-regular">The ' + MODFILE[mod][0] + ' module is not part of the ' + u.title + ' role. Switch role with Viewing as, or go back to Modules.</p>' +
      '<div class="noacc__f"><a class="btn sec" href="' + home + '">Back to Modules</a>' + (other ? '<a class="btn pri" href="' + MODFILE[other][1] + '?as=' + u.key + '">Open ' + MODFILE[other][0] + '</a>' : '') + '</div></div></div>';
    el.hidden = false; return false;
  }
'''
STORE_JS = STORE_JS.replace('__SEEDV__', SEED_V)
_ksd = json.load(open(os.path.join(HERE, 'kitchen-sample.json'), encoding='utf-8'))
KSTOCK_JSON = json.dumps({'wh': _ksd['stock']['warehouse'], 'items': _ksd['stock']['items'], 'expired': _ksd['stock']['expired']}, separators=(',', ':'))   # SAMPLE DATA

ROLE_CSS = '''    /* =========================================================
       15. VIEWING AS  (demo role switcher) + REQUEST ACTIONS
       ========================================================= */
    .asbtn { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; max-width: 46vw; padding: 0 12px; border-radius: 999px; border: 1px solid var(--md3-outline-variant); background: var(--white); color: var(--md3-on-primary-container); }
    .rdtabs { display: flex; gap: 0; overflow-x: auto; scrollbar-width: none; background: var(--white); border-bottom: 1px solid var(--line); padding: 0 8px; }
    .rdtabs::-webkit-scrollbar { display: none; }
    .rdtab { flex: 1 0 auto; min-height: 52px; padding: 0 16px; color: var(--md3-on-surface-variant); border-bottom: 3px solid transparent; white-space: nowrap; }
    .rdtab[aria-selected="true"] { color: var(--md3-primary); border-bottom-color: var(--md3-primary); }
    .rdtab .n { margin-left: 6px; font-size: 13px; opacity: .75; }
    .kstock { background: var(--white); border-radius: var(--radius); padding: 16px 20px; display: grid; gap: 12px; margin-top: 16px; }
    .kstock__h { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
    .kstock__h .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .kstock__h b { color: var(--head); }
    .kstock__h small { color: var(--md3-neutral-secondary); }
    .btn.ksm { flex: none; height: 44px; padding: 0 16px; font-size: 15px; }
    .knote2 { display: flex; gap: 10px; align-items: flex-start; padding: 12px 14px; border-radius: 8px; }
    .knote2 svg { flex: none; margin-top: 1px; }
    .knote2.ok { background: var(--primary-a10); color: var(--md3-on-surface); }
    .knote2.warn { background: #FFF6DB; color: #6B4E00; }
    .knote2.bad { background: var(--error-a5); color: #B3213F; }
    .knote2.info { background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .knote2 small { color: inherit; opacity: .85; }
    .kcap2 { display: flex; gap: 6px; align-items: flex-start; color: var(--md3-neutral-secondary); font-size: 13px; }
    .kcap2 svg { flex: none; margin-top: 2px; }
    .ktot { display: flex; flex-wrap: wrap; gap: 6px 16px; color: var(--ink); }
    .ktot b { color: var(--head); }
    .kgrid2 { display: grid; grid-template-columns: minmax(0, 1fr) 96px 96px 150px; gap: 12px; align-items: center; }
    .kgrid2 .r { text-align: right; }
    .kgrid2 .num { font-variant-numeric: tabular-nums; color: var(--head); font-weight: 600; }
    .khead { color: var(--ink); font-size: 12px; padding: 0 14px; }
    .klines { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; }
    .kline2 { border-radius: 8px; background: var(--md3-background); padding: 12px 14px; display: grid; gap: 10px; border-left: 4px solid transparent; }
    .kline2.bad { border-left-color: var(--md3-error); background: var(--white); box-shadow: inset 0 0 0 1px var(--md3-surface-variant); }
    .kline2.fix { border-left-color: var(--md3-on-primary-container); }
    .kline2 small { display: block; color: var(--md3-neutral-secondary); }
    .kline2 b { color: var(--head); }
    .kst { display: inline-flex; align-items: center; gap: 4px; height: 28px; padding: 0 10px; border-radius: 6px; font-size: 13px; font-weight: 600; white-space: nowrap; }
    .kst.ok { background: var(--md3-on-background); color: var(--md3-on-surface); }
    .kst.fix { background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .kst.short { background: #FFF6DB; color: #6B4E00; }
    .kst.main { background: var(--md3-on-background); color: var(--md3-on-surface); }
    .kst.alt { background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .kl2__h { display: flex; align-items: center; gap: 12px; }
    .kl2__h .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .kcands { display: flex; flex-wrap: wrap; gap: 8px; }
    .kc { display: inline-flex; align-items: center; gap: 6px; min-height: 36px; padding: 0 12px; border-radius: 18px; border: 1px solid var(--md3-outline-variant); background: var(--white); color: var(--ink); font-size: 14px; font-variant-numeric: tabular-nums; }
    .kc b { color: var(--head); font-weight: 600; }
    .kc small { color: var(--md3-neutral-secondary); font-size: 12px; }
    .kc.on { border-color: var(--md3-on-primary-container); background: var(--md3-on-primary-container); color: var(--white); }
    .kc.on b, .kc.on small { color: var(--white); }
    .kc.shortc { background: var(--md3-background); }
    .kwill { display: grid; gap: 2px; color: var(--head); }
    .rdtabs.two { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 0; }
    .kl3 { display: grid; grid-template-columns: 110px minmax(0, 1fr) 120px 150px; gap: 12px; align-items: center; }
    .kl3 small { display: block; color: var(--md3-neutral-secondary); }
    .kl3__qty { text-align: right; font-variant-numeric: tabular-nums; color: var(--head); }
    .kl3__qty s { color: var(--md3-neutral-secondary); margin-right: 4px; }
    .kl3__st { justify-self: end; }
    .kline2.gone { opacity: .6; background: var(--md3-background); }
    .kline2.gone b { text-decoration: line-through; }
    @media (orientation: portrait) { .kl3 { grid-template-columns: 84px minmax(0, 1fr) 96px auto; gap: 8px; } }
    .kwill .wl b { color: var(--md3-on-primary-container); }
    .kwill small { color: var(--md3-neutral-secondary); font-size: 13px; }
    .kwill.bad, .kwill.bad .wl b { color: #B3213F; }
    .kst.none { background: var(--error-a5); color: #B3213F; }
    .kalts { display: grid; gap: 8px; padding-top: 10px; border-top: 1px solid var(--md3-surface-variant); }
    .kalts p { display: flex; align-items: center; gap: 6px; color: var(--head); }
    .kalt { display: flex; align-items: center; gap: 12px; min-height: 56px; padding: 8px 14px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); background: var(--white); }
    .kalt.ok { cursor: pointer; } .kalt.no { opacity: .7; background: var(--md3-background); }
    .kalt input { width: 22px; height: 22px; accent-color: var(--md3-on-primary-container); flex: none; }
    .kalt .grow { flex: 1; min-width: 0; display: grid; }
    .kalt:has(input:checked) { border-color: var(--md3-on-primary-container); background: var(--md3-displaybg-primary); }
    .ksub2 { display: grid; gap: 4px; justify-items: start; padding: 10px 14px; border-radius: 8px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .ksub2 .btn { margin-top: 6px; }
    .ksub2 .linkbtn { min-height: 44px; padding: 0 4px; }
    .rqd__foot .now .kblk { display: flex; gap: 6px; align-items: center; margin-top: 4px; }
    .rqd__foot .now .kblk, .rqd__foot .now .kblk span, .rqd__foot .now .kblk b { color: #B3213F; font-size: 13px; line-height: 1.3; }
    .rqd__foot .now .kblk b { font-weight: 700; }
    .rqd__foot .btn[disabled] { opacity: .45; cursor: not-allowed; }
    .ktab2 { width: 100%; border-collapse: collapse; }
    .ktab2 th { text-align: left; font-size: 12px; font-weight: 600; color: var(--ink); padding: 0 10px 8px; border-bottom: 1px solid var(--md3-surface-variant); vertical-align: bottom; }
    .ktab2 th small { display: block; font-weight: 400; color: var(--md3-neutral-secondary); }
    .ktab2 td { padding: 10px; border-bottom: 1px solid var(--line); color: var(--head); vertical-align: top; }
    .ktab2 td small { display: block; color: var(--md3-neutral-secondary); }
    .ktab2 .r { text-align: right; font-variant-numeric: tabular-nums; }
    .ktab2 tr.changed td { background: #FFFBEB; } .ktab2 tr.added td { background: var(--md3-displaybg-primary); } .ktab2 tr.removed td { background: var(--error-a5); } .ktab2 tr.removed td b { text-decoration: line-through; }
    @media (orientation: portrait) { .kgrid2 { grid-template-columns: minmax(0, 1fr) 84px 84px 132px; gap: 8px; } }
    .rqreset { justify-self: start; min-height: 44px; color: var(--md3-neutral-secondary); }
    .asbtn span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .asbtn small { color: var(--md3-neutral-secondary); font-weight: 400; }
    @media (hover: hover) { .asbtn:hover { background: var(--md3-displaybg-primary); } }
    .roles { display: grid; gap: 8px; }
    .role { display: flex; align-items: center; gap: 12px; min-height: 64px; padding: 10px 14px; border-radius: var(--radius); border: 1px solid var(--md3-outline-variant); text-align: left; width: 100%; background: var(--white); }
    .role[aria-checked="true"] { border-color: var(--md3-on-primary-container); box-shadow: 0 0 0 1px var(--md3-on-primary-container); background: var(--md3-displaybg-primary); }
    .role .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .role .grow b { color: var(--head); }
    .role .grow span { color: var(--ink); }
    .role .grow small { color: var(--md3-neutral-secondary); }
    .rqd__foot .acts { display: flex; gap: var(--sp-8); flex-wrap: wrap; justify-content: flex-end; }
    .rqd__foot .acts .btn { flex: none; min-width: 0; padding: 0 var(--sp-16); white-space: nowrap; }
    .btn.teal { background: var(--md3-on-primary-container); color: var(--white); }
    .btn.danger { border: 1px solid var(--md3-error); color: var(--md3-error); }
    .rnote { display: flex; gap: 10px; padding: var(--sp-12) var(--sp-16); border-radius: var(--radius); background: var(--white); color: var(--ink); box-shadow: inset 4px 0 0 var(--md3-on-primary-container); }
    .rnote.bad { box-shadow: inset 4px 0 0 var(--md3-error); }
    .rnote.warn { box-shadow: inset 4px 0 0 var(--md3-moderate-secondary); }
    .rnote b { color: var(--head); }
    .rnote small { color: var(--md3-neutral-secondary); display: block; }
    .propline { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .ro-note { display: none; color: var(--md3-neutral-secondary); }
    /* No access state (guardModule) */
    .noacc { position: fixed; inset: var(--status-h) 0 0 0; z-index: 28; display: grid; grid-template-rows: auto 1fr; background: var(--md3-background); }
    .noacc[hidden] { display: none; }
    .noacc .bar { background: var(--white); }
    .noacc__in { display: grid; place-items: center; padding: 24px 16px; }
    .noacc__card { width: min(520px, 100%); display: grid; gap: 12px; justify-items: center; text-align: center; padding: 32px 24px; border-radius: var(--radius); background: var(--white); }
    .noacc__card h2 { color: var(--head); }
    .noacc__card p { color: var(--ink); }
    .noacc__i { width: 56px; height: 56px; border-radius: 50%; display: grid; place-items: center; background: #FFF6DB; color: #8A5A00; font-size: 28px; font-weight: 700; }
    .noacc__f { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin-top: 8px; }
    .noacc__f .btn { flex: none; min-width: 180px; height: 48px; padding: 0 20px; text-decoration: none; }
    /* role gating: write = diet-plans.write (Head Dietician), raise = Dietician / Head Dietician */
    body:not([data-write]) [data-createbase], body:not([data-write]) .addchip, body:not([data-write]) [data-newplan],
    body:not([data-write]) [data-cert], body:not([data-write]) [data-certify], body:not([data-write]) [data-certchange],
    body:not([data-write]) [data-act="edit"], body:not([data-write]) [data-move], body:not([data-write]) [data-addsp] { display: none !important; }
    body:not([data-raise]) [data-rqnew] { display: none !important; }
    body:not([data-write]) .ro-note { display: block; }
    .seg-mine { color: var(--md3-on-primary-container); }
    .toast { bottom: 104px; }
'''

ROLE_OVERLAY = '''  <div class="scrim" id="rqsheet" hidden><div class="sheet" role="dialog" aria-modal="true" aria-labelledby="rsT"></div></div>'''

REQ_SHARED_JS = '''  /* ---------------- Diet requests: roles, store, state machine, detail (V2 dr-core.js / request.js) ---------------- */
  var USERS = [
    { key: 'dietician', id: 'u-dt', name: 'Hydar Ali', role: 'DIETICIAN', title: 'Dietician', perms: ['diet-plans.read'] },
    { key: 'head-dietician', id: 'u-dm', name: 'Dr. Meera Iyer', role: 'DIET_MANAGER', title: 'Head Dietician', prd: 'Diet Manager', perms: ['diet-plans.read', 'diet-plans.write', 'diet-plans.verify'] },
    { key: 'kitchen-head', id: 'u-kh', name: 'Suresh Gowda', role: 'KITCHEN_HEAD', title: 'Kitchen Head', perms: ['diet-plans.read', 'packing.read'], proto: ['packing.write', 'inventory.read'] },
    { key: 'kitchen-operator', id: 'u-ko', name: 'Anil Kumar', role: 'KITCHEN_OPERATOR', title: 'Kitchen Operator', perms: ['diet-plans.read', 'packing.read', 'packing.write', 'inventory.read'] },    { key: 'receiving-manager', id: 'u-rm', name: 'Farhan Shaikh', role: 'RECEIVING_MANAGER', title: 'Receiving Manager', perms: [] },
    { key: 'security', id: 'u-sg', name: 'Ravi Naik', role: 'SECURITY', title: 'Security', perms: [] },
    { key: 'security-admin', id: 'u-sa', name: 'Priya Desai', role: 'SECURITY_ADMIN', title: 'Security Admin', perms: [] },
  ];
  var REQS_ALL = ''' + json.dumps(_req_seed, ensure_ascii=False).replace('</', '<\\/') + ''';
''' + STORE_JS + '''  var RQ_STORE = storedReqs(); if (RQ_STORE) REQS_ALL = RQ_STORE.reqs;
  var RQ_PLANS = (RQ_STORE && RQ_STORE.plans) || {}, RQ_GONE = (RQ_STORE && RQ_STORE.gone) || [];
  REQS_ALL.forEach(function (r) { r.by = r.by || { id: 'u-carol', name: 'Carol Steve', role: 'Site Manager' }; r.events = r.events || [{ kind: 'submitted', at: r.iso + 'T09:00', by: r.by.name, text: 'Request submitted' }]; });
  var RQ = {
    PRI: { high: ['!!!', 'High', 'Clinical or urgent. Needs action today.'], medium: ['!!', 'Medium', 'Needed within the next few days.'], low: ['!', 'Low', 'Routine change with no deadline.'] },
    TYPES: [['temporary', 'Temporary / Time-bound'], ['base', 'Base diet change'], ['site', 'Site / Section-specific'], ['animal', 'Animal-specific']],
    STEPS: ['Request submitted', 'Dietician reviewing', 'New diet configured', 'Kitchen processing', 'Sent to prep', 'Preparing diet', 'Dispatched', 'Approved'],
    ST: {
      requested: ['Requested', 'wait', 'time', 2], under_review: ['Under Dietician Review', 'wait', 'time', 2], configuring: ['Configuring', 'wait', 'pencil', 3], adjustment: ['Needs Adjustment', 'bad', 'close', 3],
      kitchen_review: ['Kitchen Review', 'wait', 'time', 4], delayed: ['Delayed', 'wait', 'timer', 4], ready: ['Sent to prep', 'ok', 'just-tick-mark', 5], rejected: ['Rejected', 'bad', 'close', 2],
      applied: ['Completed · Applied', 'ok', 'just-tick-mark', 6], cancelled: ['Cancelled', 'bad', 'close', 2],
    },
    OPEN: ['requested', 'under_review', 'configuring', 'adjustment', 'kitchen_review', 'delayed'],
    viewer: USERS[1],
    MON: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    fmt: function (iso) { if (!iso) return ''; var p = iso.slice(0, 10).split('-'); return Number(p[2]) + ' ' + RQ.MON[Number(p[1]) - 1] + ' ' + p[0]; },
    fmtDT: function (iso) { return RQ.fmt(iso) + (iso && iso.length > 10 ? ', ' + iso.slice(11, 16) : ''); },
    now: function () { var d = new Date(), p = function (n) { return ('0' + n).slice(-2); }; return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + 'T' + p(d.getHours()) + ':' + p(d.getMinutes()); },
    ago: function (iso) { if (!iso) return ''; var q = iso.split(/[-T:]/).map(Number), m = Math.round((Date.now() - new Date(q[0], q[1] - 1, q[2], q[3] || 0, q[4] || 0).getTime()) / 60000); if (m < 1) return 'Just now'; if (m < 60) return m + ' min ago'; var h = Math.round(m / 60); if (h < 24) return h + ' h ago'; var d = Math.round(h / 24); return d === 1 ? 'Yesterday' : d < 7 ? d + ' days ago' : RQ.fmt(iso); },
    initials: function (n) { return String(n || '?').replace(/^Dr\\.?\\s+/i, '').split(/\\s+/).filter(Boolean).slice(0, 2).map(function (w) { return w[0].toUpperCase(); }).join(''); },
    get: function (id) { for (var i = 0; i < REQS_ALL.length; i++) if (REQS_ALL[i].id === id) return REQS_ALL[i]; return null; },
    has: function (perm, u) { u = u || RQ.viewer; return u.perms.indexOf(perm) !== -1 || (u.proto || []).indexOf(perm) !== -1; },
    can: function (key, u) { u = u || RQ.viewer;
      switch (key) {
        case 'seeAll': return RQ.has('diet-plans.write', u) || RQ.has('packing.read', u);
        case 'raise': return RQ.has('diet-plans.read', u) && (u.role === 'DIETICIAN' || u.role === 'DIET_MANAGER');
        case 'review': case 'configure': case 'write': return RQ.has('diet-plans.write', u);
        case 'kitchenAct': return RQ.has('packing.write', u) && RQ.has('inventory.read', u) && !RQ.has('diet-plans.write', u);
        default: return RQ.has(key, u);
      } },
    isMine: function (r, u) { u = u || RQ.viewer; return !!(r.by && r.by.id === u.id); },
    visible: function () { return RQ.can('seeAll') ? REQS_ALL : REQS_ALL.filter(function (r) { return RQ.isMine(r); }); },
    canEdit: function (r) { return RQ.isMine(r) && (r.status === 'requested' || r.status === 'under_review'); },
    decorate: function (r) { var s = RQ.ST[r.status] || RQ.ST.requested; r.label = r.status === 'delayed' && r.delayUntil ? 'Delayed to ' + RQ.fmt(r.delayUntil).replace(/ \\d{4}$/, '') : s[0]; r.tone = s[1]; r.icon = s[2]; return r; },
    isOpen: function (r) { return RQ.OPEN.indexOf(r.status) !== -1; },
    nextId: function () { var n = Math.max.apply(null, REQS_ALL.map(function (r) { return Number(r.id.replace(/\\D/g, '')); })) + 1; return 'DR-' + ('0000' + n).slice(-5); },
    ev: function (r, kind, text) { r.events.push({ kind: kind, at: RQ.now(), by: RQ.viewer.name, role: RQ.viewer.title, text: text }); },
    listeners: [],
    save: function () { lsSet(RQS_KEY, { v: SEED_V, reqs: REQS_ALL, plans: RQ_PLANS, gone: RQ_GONE }); },
    keepPlan: function (p) { RQ_PLANS[p.id] = p; RQ.save(); },
    dropPlan: function (id) { delete RQ_PLANS[id]; if (RQ_GONE.indexOf(id) === -1) RQ_GONE.push(id); RQ.save(); },
    restorePlans: function (PL, BY) {
      RQ_GONE.forEach(function (id) { var p = PL[id]; if (!p) return; delete PL[id]; var s = BY[p.species]; if (s) s.plans = (s.plans || []).filter(function (x) { return x !== id; }); });
      Object.keys(RQ_PLANS).forEach(function (k) { var p = RQ_PLANS[k]; PL[p.id] = p; var s = BY[p.species]; if (s && (s.plans || []).indexOf(p.id) === -1) s.plans = [p.id].concat(s.plans || []); });
    },
    changed: function () { RQ.save(); REQS_ALL.forEach(RQ.decorate); RQ.listeners.forEach(function (f) { f(); }); var t = document.getElementById('t-request'); if (t) t.textContent = (RQ.can('seeAll') ? 'Diet Request - ' : 'My Requests - ') + RQ.visible().length; },
    timeline: function (r) {
      var cur = (RQ.ST[r.status] || RQ.ST.requested)[3], end = r.status === 'rejected' || r.status === 'cancelled';
      return RQ.STEPS.map(function (label, i) {
        var n = i + 1, state = n < cur ? 'done' : n === cur ? 'current' : 'pending', sub = '';
        if (r.status === 'applied' && n >= 6) state = 'pending';
        if (r.status === 'applied' && n === 5) state = 'done';
        if (end && n >= 2) state = n === 2 ? 'rejected' : 'skipped';
        if (n === 1) { state = 'done'; sub = RQ.fmtDT(r.events[0].at) + ' by ' + r.by.name; }
        if (n === 2) sub = r.status === 'rejected' ? 'Rejected' + (r.rejectBy ? ' by ' + r.rejectBy : '') + (r.rejectReason ? ': ' + r.rejectReason : '') : r.status === 'cancelled' ? 'Cancelled by the requester' :
          state === 'done' ? 'Accepted' + (r.acceptedBy ? ' by ' + r.acceptedBy : '') : r.clarify && !r.clarify.answer ? 'Clarification requested' : r.status === 'requested' ? 'Waiting for the Head Dietician' : 'In review';
        if (n === 3) sub = state === 'done' ? (r.proposedId ? (r.cfgLabel ? r.cfgLabel + ' ' : '') + 'D-' + r.proposedId + ' (Proposed) sent to Kitchen' : 'Configured') : r.status === 'adjustment' ? 'Needs adjustment' + (r.adjustReason ? ': ' + r.adjustReason : '') : state === 'current' ? (r.proposedId ? 'Configured as ' + (r.cfgLabel || 'proposed diet') + ' D-' + r.proposedId + (r.editOf ? ' (Proposed change to ' + r.editOfLabel + ')' : ' (Proposed)') : 'Waiting for configuration') : '';
        if (n === 4) sub = state === 'done' ? 'Accepted by Kitchen' : r.status === 'delayed' ? 'Delayed to ' + RQ.fmt(r.delayUntil) + (r.delayReason ? ': ' + r.delayReason : '') : state === 'current' ? 'Stock and feasibility check' : '';
        if (n === 5 && state !== 'pending') sub = r.status === 'applied' ? 'Applied by the kitchen' : r.readyAt ? 'Since ' + RQ.fmtDT(r.readyAt) : '';
        return { n: n, label: label, state: state, sub: sub };
      });
    },
    next: function (r) {
      var me = function (ok, who) { return ok ? 'You' : who; };
      switch (r.status) {
        case 'requested': case 'under_review': if (r.clarify && !r.clarify.answer) return me(RQ.isMine(r), r.by.name) + ' to reply to the question'; return me(RQ.can('review'), 'Head Dietician') + ' to review';
        case 'configuring': return me(RQ.can('configure'), 'Head Dietician') + ' to configure the new diet';
        case 'adjustment': return me(RQ.can('configure'), 'Head Dietician') + ' to adjust and send again';
        case 'kitchen_review': return me(RQ.can('kitchenAct'), 'Kitchen') + ' to check stock and accept';
        case 'delayed': return me(RQ.can('kitchenAct'), 'Kitchen') + ' to accept by ' + RQ.fmt(r.delayUntil);
        case 'ready': return 'Kitchen to prepare. Phase 1 ends here.';
        case 'rejected': return 'Closed. The request was rejected.';
        case 'cancelled': return 'Closed. The request was cancelled.';
        default: return 'Later phase: read only';
      }
    },
  };
  REQS_ALL.forEach(RQ.decorate);

  /* ---------- Viewing as (dr-core.js mountActions) ---------- */
  function applyRole() { guardModule('diet', RQ.viewer); [].forEach.call(document.querySelectorAll('a[data-aslink]'), function (a) { a.setAttribute('href', a.getAttribute('data-aslink') + '?as=' + RQ.viewer.key); }); var b = document.body; if (RQ.can('write')) b.setAttribute('data-write', ''); else b.removeAttribute('data-write'); if (RQ.can('raise')) b.setAttribute('data-raise', ''); else b.removeAttribute('data-raise');
    [].forEach.call(document.querySelectorAll('.asbtn'), function (btn) { btn.innerHTML = ic('user', 20) + '<span class="t-body-medium">Viewing as: ' + esc(RQ.viewer.name) + ' <small>· ' + esc(RQ.viewer.title) + '</small></span>' + ic('dropdown', 18); }); }
  function setViewer(key, silent) {
    var u = USERS.filter(function (x) { return x.key === key; })[0]; if (!u) return;
    RQ.viewer = u; saveViewer(key); applyRole();
    try { var q = new URLSearchParams(location.search); q.set('as', key); history.replaceState(history.state, '', location.pathname + '?' + q.toString() + location.hash); } catch (x) {}
    RQ.changed();
    if (!silent) toast('Viewing as: ' + u.title + ', ' + u.name);
  }
  var RS = document.getElementById('rqsheet');
  function sheet(html) { RS.querySelector('.sheet').innerHTML = '<div class="grab"></div>' + html; RS.hidden = false; }
  function closeSheet3() { RS.hidden = true; }
  function openRoles() {
    sheet('<div class="sheet__h"><div><h2 class="t-major-title" id="rsT">Viewing as</h2><p class="t-body-regular" style="color:var(--ink)">Demo only. Switch role to see what each one can do.</p></div><button type="button" class="iconbtn" data-rsclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
      '<div class="roles" role="radiogroup" aria-label="Role">' + USERS.map(function (u) {
        var what = { DIETICIAN: 'Raises requests. Sees My requests only.', DIET_MANAGER: 'Raises, reviews and configures requests. Edits diets.', KITCHEN_HEAD: 'Diet, Kitchen and Inventory. Kitchen review: delay, ask for adjustment, send to prep.', KITCHEN_OPERATOR: 'Kitchen only: requests sent to prep and Meal Group Management. No Diet module.', RECEIVING_MANAGER: 'Inventory and Kitchen. No Diet module.', SECURITY: 'Security module only.', SECURITY_ADMIN: 'Security module only.' }[u.role];
        return '<button type="button" class="role" role="radio" data-as="' + u.key + '" aria-checked="' + (u === RQ.viewer) + '"><span class="av">' + RQ.initials(u.name) + '</span><span class="grow"><b class="t-minor-title">' + esc(u.title) + '</b><span class="t-body-regular">' + esc(u.name) + (u.prd ? ' · PRD role name: ' + u.prd : '') + '</span><small class="t-body-regular">' + esc(what) + '</small></span>' + (u === RQ.viewer ? ic('just-tick-mark', 22) : '') + '</button>';
      }).join('') + '</div><button type="button" class="linkbtn t-body-medium rqreset" data-rqreset>' + ic('history', 18) + 'Reset demo data</button>');
  }

  /* ---------- kitchen stock check (V2 dr-core.js DR.needs / DR.stock / DR.feasibility), SAMPLE DATA stock ---------- */
  var KSTOCK = ''' + KSTOCK_JSON + ''';
  /* Auto-resolution (kitchen): per diet line the candidates are the main item, then the Head Dietician's
     alternatives on that line, in order. The first candidate whose usable stock fully covers its own required
     quantity is the one prepped. If none covers it, the line is unresolved and the request needs a readjustment. */
  var KS = {
    conv: function (q, f, t) { if (f === t) return q; if (f === 'g' && t === 'kg') return q / 1000; if (f === 'kg' && t === 'g') return q * 1000; if (f === 'ml' && t === 'ltr') return q / 1000; if (f === 'ltr' && t === 'ml') return q * 1000; if ((f === 'nos' && t === 'pcs') || (f === 'pcs' && t === 'nos')) return q; return null; },
    q: function (v) { return (Math.round(v * 100) / 100).toLocaleString('en-IN'); },
    pq: function (s) { var mm = /^([0-9.]+)\\s*(.*)$/.exec(s || ''); return mm ? { qty: Number(mm[1]), unit: mm[2] } : null; },
    plabel: function (p) { return p ? 'D-' + (p.sharedFrom || p.id) : ''; },
    needs: function (plan) {
      var m = {}, order = [];
      ((plan && plan.schedule) || []).forEach(function (b) { (b.days || []).forEach(function (g) { (g.items || []).forEach(function (x) {
        var a0 = KS.pq(x.amount) || { qty: 0, unit: '' };
        if (!m[x.name]) { m[x.name] = { name: x.name, qty: 0, unit: a0.unit, mix: !!x.mix, bands: [], days: [], preps: [], cuts: [], alts: [] }; order.push(x.name); }
        var e = m[x.name], v = KS.conv(a0.qty, a0.unit, e.unit); e.qty += v == null ? a0.qty : v;
        if (e.bands.indexOf(b.time) === -1) e.bands.push(b.time); if (e.days.indexOf(g.day) === -1) e.days.push(g.day);
        if (x.prep && e.preps.indexOf(x.prep) === -1) e.preps.push(x.prep); if (x.cut && e.cuts.indexOf(x.cut) === -1) e.cuts.push(x.cut);
        (x.alts || []).forEach(function (al) { al = typeof al === 'string' ? { name: al } : al; if (!e.alts.some(function (y) { return y.name === al.name; })) { var aq = KS.pq(al.amount); e.alts.push({ name: al.name, qty: aq ? aq.qty : null, unit: aq ? aq.unit : null, prep: al.prep || null }); } });
      }); }); });
      return order.map(function (k) { return m[k]; });
    },
    cand: function (name, qty, unit, main, prep, cut) {
      var su = KSTOCK.items[name], need = qty, u = unit, avail = 0, known = !!su;
      if (su) { var cv = KS.conv(qty, unit, su[1]); if (cv != null) { need = cv; u = su[1]; avail = su[0]; } }
      var ex = KSTOCK.expired[name], exq = ex ? KS.conv(ex[0], ex[1], u) || 0 : 0;
      return { name: name, need: need, unit: u, avail: avail, pct: need > 0 ? avail / need : 1, ok: avail + 1e-9 >= need, main: main, known: known, expired: exq, prep: prep || null, cut: cut || null };
    },
    lines: function (r) {
      var plan = HOOKS.planOf ? HOOKS.planOf(r.proposedId) : null;
      return KS.needs(plan).map(function (n) {
        if (n.mix) return { name: n.name, need: n.qty, unit: n.unit, mix: true, cands: [], chosen: null, status: 'main', bands: n.bands, reason: 'Mix, made up in the kitchen' };
        var cands = [KS.cand(n.name, n.qty, n.unit, true, n.preps[0], n.cuts[0])].concat(n.alts.map(function (a) { return KS.cand(a.name, a.qty != null ? a.qty : n.qty, a.unit || n.unit, false, a.prep, null); }));
        var ci = -1; for (var i = 0; i < cands.length; i++) if (cands[i].ok) { ci = i; break; }
        var best = cands.slice().sort(function (a, b) { return b.pct - a.pct; })[0], shortTxt = function (c) { return c.name + ' short, ' + KS.q(c.avail) + ' of ' + KS.q(c.need) + ' ' + c.unit; };
        return { name: n.name, need: cands[0].need, unit: cands[0].unit, cands: cands, chosen: ci >= 0 ? cands[ci] : null, ci: ci, best: best, bands: n.bands,
          status: ci === 0 ? 'main' : ci > 0 ? 'alt' : 'unresolved', reason: ci > 0 ? cands.slice(0, ci).map(shortTxt).join('; ') : ci < 0 ? 'Most stock: ' + best.name + ' ' + Math.min(100, Math.round(best.pct * 100)) + '% (' + KS.q(best.avail) + ' of ' + KS.q(best.need) + ' ' + best.unit + ')' : '' };
      });
    },
    feas: function (r) { var l = KS.lines(r), bad = l.filter(function (x) { return x.status === 'unresolved'; }); return { lines: l, bad: bad, alt: l.filter(function (x) { return x.status === 'alt'; }), canPrep: l.length > 0 && !bad.length }; },
    pctList: function (l) { return l.cands.map(function (c) { return c.name + ' ' + Math.min(100, Math.round(c.pct * 100)) + '%'; }).join(', '); },
  };
  RQ.kitchenView = function () { return RQ.can('kitchenAct') && !RQ.can('configure'); };

  /* ---------- request transitions (dr-core.js) ---------- */
  var ACT = {
    openForReview: function (r) { if (r.status === 'requested' && RQ.can('review')) { r.status = 'under_review'; RQ.ev(r, 'review', 'Opened for review'); RQ.changed(); } },
    accept: function (r) { r.status = 'configuring'; r.acceptedBy = RQ.viewer.name; RQ.ev(r, 'accepted', 'Request accepted. Editing is locked for the requester.'); },
    reject: function (r, f) { r.status = 'rejected'; r.rejectReason = f.reason; r.rejectBy = RQ.viewer.name; RQ.ev(r, 'rejected', 'Rejected: ' + f.reason); },
    clarify: function (r, f) { r.status = 'under_review'; r.clarify = { question: f.question, by: RQ.viewer.name, at: RQ.now(), answer: null }; RQ.ev(r, 'clarify', 'Clarification requested: ' + f.question); },
    reply: function (r, f) { r.clarify.answer = f.answer; r.clarify.answeredAt = RQ.now(); RQ.ev(r, 'answered', 'Clarification answered: ' + f.answer); },
    send: function (r) { var again = r.status === 'adjustment'; r.status = 'kitchen_review'; r.adjustReason = null; r.delayUntil = null; RQ.ev(r, 'sent-kitchen', again ? 'Sent to Kitchen again after adjustment' : 'Sent to Kitchen'); },
    delay: function (r, f) { r.status = 'delayed'; r.delayUntil = f.until; r.delayReason = f.reason; RQ.ev(r, 'delayed', 'Delayed to ' + RQ.fmt(f.until) + ': ' + f.reason + (f.notes ? ' (' + f.notes + ')' : '')); },
    adjust: function (r, f) { r.status = 'adjustment'; r.adjustReason = f.reason; r.delayUntil = null; RQ.ev(r, 'adjustment', 'Adjustment requested: ' + f.reason); },
    readjust: function (r, f) { ACT.adjust(r, f); },
    prep: function (r, f) { var L0 = KS.lines(r); r.kitchen = r.kitchen || {}; r.kitchen.accepted = { by: RQ.viewer.name, role: RQ.viewer.title, at: RQ.now(), lines: L0, prepped: L0.map(function (l) { return { line: l.name, prep: l.chosen ? l.chosen.name : null, qty: l.chosen ? l.chosen.need : null, unit: l.chosen ? l.chosen.unit : null }; }) }; r.status = 'ready'; r.readyAt = RQ.now(); r.delayUntil = null; RQ.ev(r, 'sent-prep', 'Sent to prep.' + (function () { var alt = L0.filter(function (l) { return l.status === 'alt'; }); return alt.length ? ' Prepping ' + alt.map(function (l) { return l.chosen.name + ' for ' + l.name; }).join(', ') + '.' : ''; })() + (f && f.notes ? ' Notes: ' + f.notes : '')); },
  };
  var FORMS = {
    accept: { title: 'Accept request', text: 'Accepting locks editing for the requester. Nothing becomes active. You choose how to configure it next.', ok: 'Accept and configure', fields: [], toast: 'Request accepted. Status Configuring.' },
    reject: { title: 'Reject request', text: 'The request ends. The requester sees your reason, the date and your name.', ok: 'Reject request', cls: 'danger', fields: [['reason', 'Reason for rejecting', 'textarea', 'Enter the reason for rejecting.']], toast: 'Request rejected' },
    clarify: { title: 'Ask for clarification', text: 'The requester can edit the request and reply until you accept it.', ok: 'Send question', fields: [['question', 'Question for the requester', 'textarea', 'Enter your question.']], toast: 'Question sent to the requester' },
    reply: { title: 'Reply to the Head Dietician', text: '', ok: 'Send reply', fields: [['answer', 'Your reply', 'textarea', 'Reply to the question to save.']], toast: 'Reply sent' },
    send: { title: 'Send to Kitchen', text: 'Kitchen checks stock and feasibility next. The active diet does not change.', ok: 'Send to Kitchen', fields: [], toast: 'Sent to Kitchen. Status Kitchen Review.' },
    delay: { title: 'Delay this request', text: 'The request stays with Kitchen as Delayed until the expected date.', ok: 'Delay request', fields: [['reason', 'Reason', 'textarea', 'Enter the reason for the delay.'], ['until', 'Expected date', 'date', 'Pick the date you expect to accept by.'], ['notes', 'Notes', 'textarea-opt', '']], toast: 'Request delayed' },
    readjust: { title: 'Request readjustment', text: 'The request goes back to the Head Dietician to change the diet. Say which line cannot be fulfilled and what would work.', ok: 'Request readjustment', fields: [['reason', 'Reason', 'textarea', 'Enter the reason for the readjustment.']], toast: 'Sent back to the Head Dietician. Status Needs Adjustment.' },
    adjust: { title: 'Request adjustment', text: 'The request goes back to the Head Dietician to configure again. The active diet does not change.', ok: 'Request adjustment', fields: [['reason', 'Reason', 'textarea', 'Enter the reason for the adjustment.']], toast: 'Returned to the Head Dietician. Status Needs Adjustment.' },
    prep: { title: 'Accept and send to Prep', text: 'Every item is treated as available in this prototype. The request is marked Sent to prep.', ok: 'Accept / Send to Prep', fields: [['notes', 'Notes for the prep team', 'textarea-opt', '']], toast: 'Sent to prep.' },
  };
  function actionsFor(r) {
    var a = [];
    if (RQ.canEdit(r)) { if (r.clarify && !r.clarify.answer) a.push(['reply', 'Reply to question', 'teal']); a.push(['edit', 'Edit request', r.clarify && !r.clarify.answer ? 'sec' : 'teal']); }
    if (RQ.can('review') && (r.status === 'requested' || r.status === 'under_review')) a.push(['reject', 'Reject', 'danger'], ['clarify', 'Ask for clarification', 'sec'], ['accept', 'Accept request', 'teal']);
    if (RQ.can('configure') && (r.status === 'configuring' || r.status === 'adjustment')) {
      a.push(['configure', r.proposedId ? 'Change configuration' : 'Apply to configuration', r.proposedId ? 'sec' : 'teal']);
      if (r.proposedId) a.push(['send', r.status === 'adjustment' ? 'Send to Kitchen again' : 'Send to Kitchen', 'teal']);
    }
    if (RQ.can('kitchenAct') && (r.status === 'kitchen_review' || r.status === 'delayed')) { var okp = !r.proposedId || KS.feas(r).canPrep; if (okp) a.push(['delay', 'Delay', 'sec'], ['adjust', 'Request adjustment', 'sec'], ['prep', 'Send to Prep', 'pri']); else a.push(['delay', 'Delay', 'sec'], ['prep', 'Send to Prep', 'sec', true], ['readjust', 'Request readjustment', 'teal']); }
    return a;
  }
  var HOOKS = { configure: null, edit: null };

  function ReqDetail() {
    var el = document.getElementById('rqd'), cur = null, files = [], showEv = false, pushed = false, pend = null;
    function row(icn, title, body) { return '<div class="srow"><span class="ic2">' + ic(icn, 22) + '</span><div><h3 class="t-minor-title">' + esc(title) + '</h3>' + body + '</div></div>'; }
    function pb(p) { return '<span class="pribadge ' + p + '">' + RQ.PRI[p][0] + ' ' + RQ.PRI[p][1] + '</span>'; }
    function notes(r) {
      var h = '';
      if (r.status === 'rejected' && r.rejectReason) h += '<div class="rnote bad t-body-regular">' + ic('close', 20) + '<div><b>Rejected</b><br>' + esc(r.rejectReason) + '<small>' + esc((r.rejectBy ? 'By ' + r.rejectBy + '. ' : '') + 'The request has ended.') + '</small></div></div>';
      if (r.clarify && !r.clarify.answer) h += '<div class="rnote warn t-body-regular">' + ic('info', 20) + '<div><b>Clarification requested</b><br>' + esc(r.clarify.question) + '<small>' + esc(r.clarify.by + ', ' + RQ.fmtDT(r.clarify.at) + (RQ.isMine(r) ? '. Reply to continue.' : '. Waiting for the requester.')) + '</small></div></div>';
      if (r.clarify && r.clarify.answer) h += '<div class="rnote t-body-regular">' + ic('info', 20) + '<div><b>Clarification answered</b><br>' + esc(r.clarify.answer) + '<small>' + esc('Question: ' + r.clarify.question) + '</small></div></div>';
      if (RQ.isMine(r) && r.acceptedBy && RQ.isOpen(r) && r.status !== 'requested' && r.status !== 'under_review') h += '<div class="rnote t-body-regular">' + ic('alert', 20) + '<div><b>Locked</b><small>Accepted by ' + esc(r.acceptedBy) + '. The request can no longer be edited.</small></div></div>';
      if (r.status === 'adjustment' && r.adjustReason) h += '<div class="rnote bad t-body-regular">' + ic('close', 20) + '<div><b>Kitchen asked for an adjustment</b><br>' + esc(r.adjustReason) + (RQ.can('configure') ? '<small>Change the proposed diet and send it again.</small>' : '') + '</div></div>';
      if (r.status === 'delayed' && r.delayUntil) h += '<div class="rnote warn t-body-regular">' + ic('timer', 20) + '<div><b>Delayed to ' + esc(RQ.fmt(r.delayUntil)) + '</b><br>' + esc(r.delayReason || '') + '</div></div>';
      if (r.status === 'ready') h += '<div class="rnote t-body-regular">' + ic('just-tick-mark', 20) + '<div><b>Sent to prep</b><br>Kitchen accepted ' + (r.proposedId ? 'D-' + r.proposedId + ' (Proposed)' : 'the diet') + '. Phase 1 stops here. The active diet does not change.</div></div>';
      return h;
    }
    var ktab = null, kpick = {}, KTAB0 = (function () { try { return new URLSearchParams(location.search).get('tab'); } catch (x) { return null; } })();
    var KLIVE = ['kitchen_review', 'delayed'], KSENT = ['kitchen_review', 'delayed', 'ready', 'applied', 'adjustment'];
    function ktabs(r) {
      var l = [['overview', 'Overview']];
      if (r.proposedId && KSENT.indexOf(r.status) !== -1) l.push(['diet', 'Diet & stock']);
      return l;
    }
    var KST = { main: ['main', 'just-tick-mark', 'Main item'], alt: ['alt', 'transfer', 'Using alternative'], unresolved: ['none', 'close', 'Unavailable'] };
    function kchip(st) { var k = KST[st] || KST.main; return '<span class="kst ' + k[0] + '">' + ic(k[1], 14) + k[2] + '</span>'; }
    function knote(cls, icn, html) { return '<div class="knote2 ' + cls + ' t-body-regular">' + ic(icn, 20) + '<div>' + html + '</div></div>'; }
    function candChips(l) { return '<div class="kcands" role="list">' + l.cands.map(function (c, i) { var on = l.chosen && l.chosen.name === c.name, pct = Math.min(100, Math.round(c.pct * 100));
      return '<span role="listitem" class="kc' + (on ? ' on' : c.ok ? ' okc' : ' shortc') + '" title="' + esc((i ? 'Alternative ' + i : 'Main item') + ': ' + KS.q(c.avail) + ' of ' + KS.q(c.need) + ' ' + c.unit) + '"><b>' + esc(c.name) + '</b> ' + pct + '%' + (on ? ic('just-tick-mark', 14) : '') + '<small>' + KS.q(c.avail) + ' ' + esc(c.unit) + '</small></span>'; }).join('') + '</div>'; }
    function dietStockPanel(r) {
      var live = KLIVE.indexOf(r.status) !== -1, stockable = ['kitchen_review', 'delayed', 'ready', 'applied'].indexOf(r.status) !== -1, f = KS.feas(r), acc = r.kitchen && r.kitchen.accepted;
      var lines = live || !acc ? f.lines : acc.lines, C = cmpRows(r), h = '';
      var byName = {}; C.rows.forEach(function (x) { byName[x.name] = x; });
      var overlay = C.p && (C.p.kind === 'seasonal' || C.p.kind === 'time-bound'), removed = overlay ? [] : C.rows.filter(function (x) { return x.kind === 'removed'; });   // seasonal and time-bound diets sit on top of the current diet, so nothing is removed
      if (RQ.viewer.role === 'KITCHEN_HEAD') h += '<p class="kcap2 t-body-regular">' + ic('info', 16) + 'Prototype: the Kitchen Head gets inventory and packing access for this demo. The documented role has no stock visibility.</p>';
      var nAlt = lines.filter(function (l) { return l.status === 'alt'; }).length, bad = lines.filter(function (l) { return l.status === 'unresolved'; });
      var head = !stockable ? knote('info', 'info', '<b>Stock is checked once the diet is with Kitchen.</b>')
        : !live ? knote('info', 'history', '<b>Prepped as recorded at acceptance</b><br><small>' + esc(acc ? acc.by + ', ' + RQ.fmtDT(acc.at) : 'Accepted ' + (r.readyAt ? RQ.fmtDT(r.readyAt) : 'earlier')) + '</small>')
        : !bad.length ? knote('ok', 'just-tick-mark', '<b>' + (lines.length === 1 ? 'The item can' : 'All ' + lines.length + ' items can') + ' be prepped</b>' + (nAlt ? ' · ' + nAlt + ' using ' + (nAlt === 1 ? 'an alternative' : 'alternatives') : ' · all main items'))
        : knote('bad', 'alert', '<b>' + plural(bad.length, 'item') + ' cannot be fulfilled:</b> ' + bad.map(function (l) { var alts = l.cands.slice(1).map(function (c) { return c.name; }); return esc(l.name) + (alts.length ? ' (and ' + esc(alts.join(', ')) + ')' : ''); }).join('; ') + '. Request a readjustment from the Head Dietician.');
      var TAG = { changed: ['orange', 'Changed'], added: ['teal', 'New'], removed: ['red', 'Removed'] };
      h += '<section class="kstock"><div class="kstock__h"><span class="grow"><b class="t-minor-title">Diet &amp; stock</b><small class="t-body-regular">' + esc('D-' + r.proposedId + ' (Proposed, not active) vs ' + (C.c ? KS.plabel(C.c) : 'no current diet') + '. Per day, ' + KSTOCK.wh + '.') + '</small></span>' +
        (live ? '<button type="button" class="btn sec ksm" data-krecheck>' + ic('history', 18) + 'Recheck stock</button>' : '') + '</div>' + head +
        (live && r.kitchen && r.kitchen.checkedAt ? '<p class="kcap2 t-body-regular">' + ic('time', 16) + 'Stock checked ' + esc(RQ.ago(r.kitchen.checkedAt)) + '</p>' : '') +
        '<ul class="klines">' + lines.map(function (l) {
          var x0 = byName[l.name] || {}, kind = x0.kind, pp = x0.prop || {}, cq = x0.cur;
          var x = '<li class="kline2 ' + (l.status === 'unresolved' && stockable ? 'bad' : l.status === 'alt' && stockable ? 'fix' : '') + '" data-kline="' + esc(l.name) + '"><div class="kl3"><span class="kl3__band t-body-regular">' + esc((l.bands || []).join(', ') || '-') + '<small>' + esc((pp.days || []).join(', ')) + '</small></span>' +
            '<span class="kl3__item"><b class="t-body-title">' + esc(l.name) + '</b>' + (TAG[kind] ? ' <span class="tag ' + TAG[kind][0] + '">' + TAG[kind][1] + '</span>' : '') + '<small class="t-body-regular">' + esc([(pp.preps || []).join(', '), (pp.cuts || []).length ? 'cut ' + pp.cuts.join(', ') : ''].filter(Boolean).join(', ') || 'No preparation') + '</small></span>' +
            '<span class="kl3__qty t-body-regular">' + (kind === 'changed' && cq ? '<s>' + KS.q(cq.qty) + ' ' + esc(cq.unit) + '</s> ' : '') + '<b>' + KS.q(pp.qty != null ? pp.qty : l.need) + ' ' + esc(pp.unit || l.unit) + '</b></span>' +
            '<span class="kl3__st">' + (stockable ? kchip(l.status) : '') + '</span></div>';
          if (stockable && !l.mix) {
            x += candChips(l);
            if (l.chosen) x += '<p class="kwill t-body-regular"><span class="wl">Will prep: <b>' + esc(l.chosen.name) + '</b> ' + KS.q(l.chosen.need) + ' ' + esc(l.chosen.unit) + '</span>' + (l.reason ? '<small>' + esc(l.reason) + '</small>' : '') + '</p>';
            else x += '<p class="kwill bad t-body-regular"><span class="wl"><b>Cannot be fulfilled.</b> No candidate covers ' + KS.q(l.need) + ' ' + esc(l.unit) + '.</span><small>' + esc(l.reason) + '. No partial prep.</small></p>';
          } else if (l.mix) x += '<p class="kwill t-body-regular">' + esc(l.reason) + '</p>';
          return x + '</li>'; }).join('') +
        removed.map(function (x) { return '<li class="kline2 gone"><div class="kl3"><span class="kl3__band t-body-regular">' + esc((x.cur.bands || []).join(', ')) + '</span><span class="kl3__item"><b class="t-body-title">' + esc(x.name) + '</b> <span class="tag red">Removed</span><small class="t-body-regular">Not in the proposed diet. No stock check.</small></span><span class="kl3__qty t-body-regular"><s>' + KS.q(x.cur.qty) + ' ' + esc(x.cur.unit) + '</s></span><span class="kl3__st"></span></div></li>'; }).join('') + '</ul>' +
        '<p class="kcap2 t-body-regular">' + ic('info', 16) + 'The first candidate in order whose stock covers 100% of the requirement is prepped. Alternatives come from the proposed diet lines. Nothing changes in the Prep Sheet until the diet becomes active. Stock levels are SAMPLE DATA.</p></section>';
      return h;
    }
    function cmpRows(r) {
      var c = HOOKS.currentOf ? HOOKS.currentOf(r) : null, p = HOOKS.planOf ? HOOKS.planOf(r.proposedId) : null, cn = KS.needs(c), pn = KS.needs(p), names = [];
      cn.concat(pn).forEach(function (x) { if (names.indexOf(x.name) === -1) names.push(x.name); });
      return { c: c, p: p, rows: names.map(function (n) { var a = cn.filter(function (x) { return x.name === n; })[0], b = pn.filter(function (x) { return x.name === n; })[0];
        var kind = a && b ? (Math.abs((KS.conv(a.qty, a.unit, b.unit) || a.qty) - b.qty) < 1e-9 ? 'same' : 'changed') : b ? 'added' : 'removed'; return { name: n, cur: a, prop: b, kind: kind }; }) };
    }
    function draw() {
      var r = cur; if (!r) return; RQ.decorate(r);
      var KV = RQ.kitchenView(), TB = KV ? ktabs(r) : null, nav = el.querySelector('[data-rdtabs]');
      if (KV) { if (KTAB0) { ktab = { overview: 'overview', diet: 'diet', stock: 'diet', impact: 'diet', activity: 'overview' }[KTAB0] || null; KTAB0 = null; }
        if (!ktab || !TB.some(function (t) { return t[0] === ktab; })) ktab = KLIVE.indexOf(r.status) !== -1 && r.proposedId ? 'diet' : 'overview';
        nav.innerHTML = TB.map(function (t) { var n = 0; return '<button type="button" role="tab" class="rdtab t-minor-medium" data-ktab="' + t[0] + '" aria-selected="' + (ktab === t[0]) + '">' + t[1] + (n ? '<span class="n">' + n + '</span>' : '') + '</button>'; }).join(''); nav.hidden = false; }
      else { nav.hidden = true; nav.innerHTML = ''; }
      var showEvOrig = showEv;
      document.getElementById('rqdT').textContent = r.id; el.querySelector('[data-rdsub]').textContent = r.sp + ' · ' + r.title;
      var stc = r.tone === 'ok' ? 'ok' : r.tone === 'bad' ? 'bad' : '';
      var hero = '<section class="dhero" aria-label="Request summary"><span class="ribbon ' + r.prio + '" title="' + RQ.PRI[r.prio][1] + ' priority" aria-label="' + RQ.PRI[r.prio][1] + ' priority">' + RQ.PRI[r.prio][0] + '</span>' +
        '<div class="dhero__sp"><span class="dhero__tile">' + ic('paw', 26) + '</span><span><b>' + esc(r.sp) + '</b>' + (r.sci ? '<i class="t-body-regular">' + esc(r.sci) + '</i>' : '') + '</span></div>' +
        '<p class="dhero__meta t-body-regular"><b>' + esc(r.id) + '</b><span>' + esc(RQ.fmtDT(r.events[0].at)) + '</span><span class="stchip ' + stc + '">' + ic(r.icon, 16) + esc(r.label) + '</span></p>' +
        '<div class="dhero__who"><span class="av">' + RQ.initials(r.by.name) + '</span><span class="grow"><b class="t-body-title">' + esc(r.by.name + (RQ.isMine(r) ? ' (You)' : '')) + '</b><small class="t-body-regular">' + esc(r.by.role) + '</small></span>' +
        (r.tsn ? '<a class="hbtn t-body-medium" href="#species/all/' + r.tsn + (r.proposedId || r.planId ? '/' + (r.proposedId || r.planId) : '') + '">' + ic('paw', 20) + 'View species</a>' : '') + '</div></section>';
      var typeTxt = (RQ.TYPES.filter(function (t) { return t[0] === r.type; })[0] || [0, ''])[1];
      var secs = '<section class="srows" aria-label="Request">' +
        row('location-icon', 'Applies to', '<p class="t-body-regular"><b>' + esc(r.scopeText || r.where.split(' · ').slice(1).join(' · ') || 'Whole species') + '</b>' + esc(r.where.split(' · ')[0]) + '</p>') +
        (r.currentLabel ? row('book', 'Current diet', '<p class="t-body-regular"><b>' + esc(r.currentLabel) + '</b>' + (r.currentLabel === 'No active diet' ? 'This species has no diet yet' : 'Active, not changed by this request') + '</p><span class="tag teal" style="margin-top:6px">' + (r.type === 'base' ? 'Change requested' : 'New diet requested') + '</span>') : '') +
        row('reason-or-list', 'Request', '<p class="t-body-regular"><b>' + esc(r.title) + '</b>' + esc(r.text) + '</p>') +
        (typeTxt ? row('calendar', 'Diet type', '<p class="t-body-regular">' + esc(typeTxt + (r.start ? ' · ' + RQ.fmt(r.start) + (r.end ? ' to ' + RQ.fmt(r.end) : ' onwards') : '')) + '</p>') : '') +
        row('alert', 'Priority', '<p class="t-body-regular">' + pb(r.prio) + esc(RQ.PRI[r.prio][2]) + '</p>') +
        (r.notes ? row('notes-new', 'Notes', '<p class="t-body-regular">' + esc(r.notes) + '</p>') : '') +
        (r.proposedId ? row('book', 'Proposed diet', '<div class="propline"><b class="t-body-title" style="color:var(--head)">D-' + r.proposedId + ' (Proposed)</b><span class="tag grey">Proposed · not active</span>' + (r.editOf ? '<span class="tag teal">Change to ' + esc(r.editOfLabel || '') + '</span>' : '') + (r.tsn ? '<a class="linkbtn t-body-medium" href="#species/all/' + r.tsn + '/' + r.proposedId + '">Open in species</a>' : '') + '</div>') : '') +
        row('user', 'Requested by', '<div style="display:flex;gap:10px;align-items:center"><span class="av">' + RQ.initials(r.by.name) + '</span><span><b class="t-body-title" style="color:var(--head)">' + esc(r.by.name + (RQ.isMine(r) ? ' (You)' : '')) + '</b><small class="t-body-regular">' + esc(r.by.role + ' · ' + RQ.fmtDT(r.events[0].at)) + '</small></span></div>') +
        (r.acceptedBy ? row('just-tick-mark', 'Accepted by', '<p class="t-body-regular"><b>' + esc(r.acceptedBy) + '</b>Head Dietician</p>') : '') + '</section>';
      var tl = RQ.timeline(r), curS = tl.filter(function (x) { return x.state === 'current'; })[0];
      var prog = '<section class="tl" aria-label="Progress"><h3 class="t-minor-title">Progress <small class="t-body-regular">' + (r.status === 'rejected' || r.status === 'cancelled' ? r.label : curS ? 'Step ' + curS.n + ' of 8: ' + curS.label : 'Phase 1 done') + '</small></h3><ol>' +
        tl.map(function (t) { return '<li class="' + t.state + '"><span class="mk" aria-hidden="true">' + (t.state === 'done' ? ic('just-tick-mark', 16) : t.state === 'rejected' ? ic('close', 16) : t.state === 'current' ? '<i style="width:10px;height:10px;border-radius:50%;background:currentColor;display:block"></i>' : '') + '</span><div><b class="t-body-title">' + esc(t.label) + '</b>' + (t.state === 'current' ? ' <span class="tag teal">Now</span>' : '') + (t.sub ? '<small class="t-body-regular">' + esc(t.sub) + '</small>' : '') + '</div></li>'; }).join('') + '</ol></section>';
      var canChat = RQ.can('seeAll') || RQ.isMine(r), msgs = r.events.filter(function (e) { return showEv || e.kind === 'comment'; });
      var chat = '<section class="chat" aria-label="Chat"><div class="chat__h"><h3 class="t-minor-title">' + ic('reason-or-list', 20) + (RQ.kitchenView() ? 'Chat and activity' : 'Chat') + ' <small class="t-body-regular">' + plural(r.events.filter(function (e) { return e.kind === 'comment'; }).length, 'message') + '</small></h3><button type="button" class="chip t-body-medium" data-rdev aria-pressed="' + showEv + '">' + ic('history', 18) + (showEv ? 'Hide updates' : 'Show updates') + '</button></div>' +
        (msgs.length ? '<ol class="thread" data-thread>' + msgs.map(function (m) {
          if (m.kind !== 'comment') return '<li class="msg ev"><span></span><div class="bub t-body-regular"><div class="meta">' + esc(RQ.fmtDT(m.at) + ' · ' + m.by + (m.role ? ', ' + m.role : '')) + '</div>' + esc(m.text) + '</div></li>';
          var mine = m.by === RQ.viewer.name;
          return '<li class="msg' + (mine ? ' me' : '') + '"><span class="av">' + RQ.initials(m.by) + '</span><div class="bub t-body-regular"><div class="meta">' + esc(m.by + (mine ? ' (You)' : '') + (m.role ? ', ' + m.role : '') + ' · ' + RQ.ago(m.at)) + '</div>' + (m.text ? esc(m.text) : '') +
            (m.files && m.files.length ? '<div>' + m.files.map(function (f) { return '<span class="file">' + ic('notes-new', 16) + esc(f) + '</span>'; }).join('') + '</div>' : '') + '</div></li>';
        }).join('') + '</ol>' : '<p class="noms t-body-regular">' + ic('reason-or-list', 20) + 'No messages yet. Ask a question or share a file with everyone working on this request.</p>') +
        (canChat ? '<div class="composer"><span class="av">' + RQ.initials(RQ.viewer.name) + '</span><label><span class="sr-only">Write a message</span><input type="text" data-rdmsg placeholder="Write a message" autocomplete="off"></label>' +
        '<button type="button" class="att" data-rdattach aria-label="Attach a file">' + ic('add', 24) + '</button><button type="button" class="send" data-rdsend aria-label="Send">' + ic('back', 22).replace('<svg', '<svg style="transform:rotate(180deg)"') + '</button>' +
        (files.length ? '<div class="pending-files">' + files.map(function (f, i) { return '<span>' + ic('notes-new', 14) + esc(f) + '<button type="button" class="iconbtn" style="width:32px;height:32px" data-rdrmf="' + i + '" aria-label="Remove ' + esc(f) + '">' + ic('close', 16) + '</button></span>'; }).join('') + '</div>' : '') +
        '<input type="file" data-rdfile multiple hidden></div>' : '') + '</section>';
      var nt = notes(r); showEv = showEvOrig;
      el.querySelector('[data-rdbody]').innerHTML = !KV || ktab === 'overview' ? hero + (nt ? '<div style="display:grid;gap:12px">' + nt + '</div>' : '') + '<div class="rqd__cols"><div style="display:grid;gap:16px">' + secs + '</div><div style="display:grid;gap:16px">' + prog + '</div></div>' + chat
        : hero + dietStockPanel(r);
      var acts = actionsFor(r), lastSt = r.events.filter(function (e) { return e.kind !== 'comment'; }).pop();
      el.querySelector('[data-rdfoot]').innerHTML = '<div class="now"><small class="t-body-regular">Current status · ' + esc(RQ.ago(lastSt.at)) + '</small><b>' + esc(r.label) + '</b><span class="t-body-medium">' + esc(RQ.next(r)) + '</span>' + (function () { var b = acts.filter(function (a) { return a[0] === 'prep' && a[3]; })[0]; if (!b) return ''; var n = KS.feas(r).bad.length; return '<span class="kblk t-body-regular" id="kblk">' + ic('alert', 16) + '<span><b>Send to Prep is blocked.</b> ' + plural(n, 'item') + ' cannot be fulfilled.</span></span>'; })() + '</div>' +
        '<div class="acts">' + (acts.length ? acts.map(function (a) { return '<button type="button" class="btn ' + a[2] + '" data-ract="' + a[0] + '"' + (a[3] ? ' disabled aria-describedby="kblk"' : '') + '>' + esc(a[1]) + '</button>'; }).join('') : '<button type="button" class="btn sec" data-rdback>Back</button>') + '</div>';
      var th = el.querySelector('[data-thread]'); if (th) th.scrollTop = th.scrollHeight;
    }
    function openForm(kind) {
      var F = FORMS[kind], r = cur; pend = { kind: kind, errs: {}, vals: {} };
      function body() {
        return '<div class="sheet__h"><div><h2 class="t-major-title" id="rsT">' + esc(F.title) + '</h2><p class="t-body-regular" style="color:var(--ink)">' + esc(r.id + ' · ' + r.sp) + '</p></div><button type="button" class="iconbtn" data-rsclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
          (kind === 'reply' && r.clarify ? '<div class="rnote warn t-body-regular">' + ic('info', 20) + '<div><b>The Head Dietician asked</b><br>' + esc(r.clarify.question) + '</div></div>' : '') +
          (F.text ? '<p class="t-body-regular" style="color:var(--ink)">' + esc(F.text) + '</p>' : '') +
          F.fields.map(function (f) { var opt = /opt/.test(f[2]), err = pend.errs[f[0]], v = pend.vals[f[0]] || '';
            var tag = f[2] === 'date' ? '<input type="date" data-rsf="' + f[0] + '" value="' + esc(v) + '" min="' + RQ.now().slice(0, 10) + '">' : '<textarea data-rsf="' + f[0] + '">' + esc(v) + '</textarea>';
            return '<label class="fld' + (err ? ' err' : '') + '"><span>' + esc(f[1]) + (opt ? ' <span style="color:var(--md3-neutral-secondary);font-weight:400">(optional)</span>' : ' <b class="req">*</b>') + '</span>' + tag + (err ? '<span class="ferr">' + esc(err) + '</span>' : '') + '</label>'; }).join('') +
          '<div class="sheet__f end"><button type="button" class="btn sec" data-rsclose>Cancel</button><button type="button" class="btn ' + (F.cls || 'teal') + '" data-rsok>' + esc(F.ok) + '</button></div>';
      }
      pend.body = body; sheet(body());
    }
    function submitForm() {
      var F = FORMS[pend.kind], r = cur; pend.errs = {};
      F.fields.forEach(function (f) { var v = (pend.vals[f[0]] || '').trim(); if (!/opt/.test(f[2]) && !v) pend.errs[f[0]] = f[3]; });
      if (pend.kind === 'delay' && pend.vals.until && pend.vals.until < RQ.now().slice(0, 10)) pend.errs.until = 'The expected date cannot be in the past.';
      if (Object.keys(pend.errs).length) { RS.querySelector('.sheet').innerHTML = '<div class="grab"></div>' + pend.body(); return; }
      var vals = {}; Object.keys(pend.vals).forEach(function (k) { vals[k] = pend.vals[k].trim(); });
      var kind = pend.kind; ACT[kind](r, vals); var msg = F.toast; closeSheet3(); pend = null; RQ.changed(); draw(); toast(msg);
      if (kind === 'accept' && RQ.can('configure') && HOOKS.configure) setTimeout(function () { HOOKS.configure(r); }, 60);
    }
    RS.addEventListener('click', function (e) {
      var t;
      if (e.target.closest('[data-rqreset]')) { if (window.confirm('Reset the demo data? Request changes are cleared on both pages.')) resetDemo(); return; }
      if (e.target === RS || e.target.closest('[data-rsclose]')) { closeSheet3(); pend = null; return; }
      if ((t = e.target.closest('[data-as]'))) { closeSheet3(); setViewer(t.getAttribute('data-as')); return; }
      if (e.target.closest('[data-rsok]') && pend) submitForm();
    });
    RS.addEventListener('input', function (e) { if (pend && e.target.matches('[data-rsf]')) pend.vals[e.target.getAttribute('data-rsf')] = e.target.value; });
    el.addEventListener('click', function (e) {
      var t;
      if (e.target.closest('[data-rdback]')) { if (pushed && history.length > 1) history.back(); else location.hash = '#request'; return; }
      if ((t = e.target.closest('[data-ract]'))) { var k = t.getAttribute('data-ract');
        if (k === 'configure') { if (HOOKS.configure) HOOKS.configure(cur); return; }
        if (k === 'prep' && RQ.kitchenView() && !KS.feas(cur).canPrep) { toast(plural(KS.feas(cur).bad.length, 'item') + ' cannot be fulfilled. Request a readjustment.'); return; }
        if (k === 'readjust') { openForm(k); var fb = KS.feas(cur); pend.vals.reason = fb.bad.map(function (l) { return l.name + ' cannot be fulfilled: ' + KS.pctList(l) + '.'; }).join(' '); RS.querySelector('.sheet').innerHTML = '<div class="grab"></div>' + pend.body(); return; }
        if (k === 'accept') { var ar = cur; ACT.accept(ar); RQ.changed(); draw(); if (RQ.can('configure') && HOOKS.configure) HOOKS.configure(ar); else toast(FORMS.accept.toast); return; }
        if (k === 'edit') { if (HOOKS.edit) HOOKS.edit(cur); return; }
        openForm(k); return; }
      if ((t = e.target.closest('[data-ktab]'))) { ktab = t.getAttribute('data-ktab'); draw(); el.querySelector('.rqd__body').scrollTop = 0; return; }
      if (e.target.closest('[data-krecheck]')) { cur.kitchen = cur.kitchen || {}; cur.kitchen.checkedAt = RQ.now(); RQ.save(); draw(); var fr = KS.feas(cur); toast('Stock rechecked. ' + (fr.canPrep ? 'Every item is available or resolved.' : plural(fr.bad.length, 'item') + ' still unavailable.')); return; }
      if ((t = e.target.closest('[data-kapply]'))) { var it = t.getAttribute('data-kapply'), to = kpick[it], ln = KS.lines(cur).filter(function (x) { return x.name === it; })[0]; if (!to || !ln) return;
        cur.kitchen = cur.kitchen || {}; cur.kitchen.subs = cur.kitchen.subs || {}; cur.kitchen.subs[it] = { from: it, to: to, qty: ln.need, unit: ln.unit, by: RQ.viewer.name, at: RQ.now() }; delete kpick[it];
        RQ.ev(cur, 'alt', 'Alternative applied: ' + it + ' → ' + to); RQ.changed(); toast('Alternative applied: ' + it + ' → ' + to); return; }
      if ((t = e.target.closest('[data-kundo]'))) { var iu = t.getAttribute('data-kundo'); if (cur.kitchen && cur.kitchen.subs) delete cur.kitchen.subs[iu]; RQ.ev(cur, 'alt-undo', 'Alternative removed for ' + iu); RQ.changed(); toast('Alternative removed for ' + iu); return; }
      if (e.target.closest('[data-rdev]')) { showEv = !showEv; draw(); return; }
      if (e.target.closest('[data-rdattach]')) { el.querySelector('[data-rdfile]').click(); return; }
      if ((t = e.target.closest('[data-rdrmf]'))) { files.splice(Number(t.getAttribute('data-rdrmf')), 1); var v = el.querySelector('[data-rdmsg]').value; draw(); el.querySelector('[data-rdmsg]').value = v; return; }
      if (e.target.closest('[data-rdsend]')) send();
    });
    el.addEventListener('change', function (e) { if (e.target.matches('[data-kpick]')) { kpick[e.target.getAttribute('data-kpick')] = e.target.value; draw(); return; } if (e.target.matches('[data-rdfile]')) { [].forEach.call(e.target.files, function (f) { files.push(f.name); }); var v = el.querySelector('[data-rdmsg]').value; draw(); el.querySelector('[data-rdmsg]').value = v; } });
    el.addEventListener('keydown', function (e) { if (e.target.matches('[data-rdmsg]') && e.key === 'Enter') { e.preventDefault(); send(); } });
    function send() { var inp = el.querySelector('[data-rdmsg]'), txt = inp.value.trim(); if (!txt && !files.length) { toast('Type a message or attach a file.'); return; }
      cur.events.push({ kind: 'comment', at: RQ.now(), by: RQ.viewer.name, role: RQ.viewer.title, text: txt, files: files.slice() }); files = []; RQ.save(); draw(); }
    RQ.listeners.push(function () { if (cur) { if (cur.status === 'requested' && RQ.can('review')) { ACT.openForReview(cur); return; } draw(); } });
    return {
      open: function (id, wasPushed) { var r = RQ.get(id); if (!r) { toast('Request ' + id + ' was not found.'); return false; }
        if (!RQ.can('seeAll') && !RQ.isMine(r)) { toast('Viewing as ' + RQ.viewer.title + ': only your own requests are visible.'); return false; }
        if (cur !== r) { files = []; showEv = false; ktab = null; kpick = {}; } cur = r; pushed = !!wasPushed; ACT.openForReview(r); el.hidden = false; draw(); el.querySelector('.rqd__body').scrollTop = 0; return true; },
      close: function () { cur = null; el.hidden = true; },
      isOpen: function () { return !!cur; },
      current: function () { return cur; },
      redraw: draw,
    };
  }
'''
