# req.py: exec'd by home2.py. Diet Request flow from the V2 tab prototype (diet/dr-core.js openForm,
# request.js detail), in the Antz app style. REQ_FORM_JS goes inside SpModule; REQ_DETAIL_JS at top level.

REQ_CSS = '''    /* =========================================================
       14. DIET REQUEST  (request form, open-request badges, request detail)
       ========================================================= */
    .rqb { display: inline-flex; align-items: center; gap: 6px; min-height: 32px; padding: 0 10px; border-radius: 999px; background: var(--moderate-a10); color: #6B5200; font-size: 13px; font-weight: 600; white-space: nowrap; }
    button.rqb { cursor: pointer; }
    .rqline { display: flex; align-items: center; gap: var(--sp-8); flex-wrap: wrap; }
    .hero__acts { flex-wrap: wrap; }
    .prisel { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--sp-12); }
    .prio { display: flex; gap: 12px; align-items: flex-start; text-align: left; padding: 14px; min-height: 72px; border-radius: var(--radius); border: 1px solid var(--md3-outline-variant); background: var(--white); }
    .prio[aria-checked="true"] { border-color: var(--md3-on-primary-container); box-shadow: 0 0 0 1px var(--md3-on-primary-container); }
    .prio .m { min-width: 40px; height: 32px; display: grid; place-items: center; border-radius: 6px; color: var(--white); font-weight: 700; letter-spacing: 1px; }
    .prio.high .m { background: var(--md3-tertiary); } .prio.medium .m { background: var(--md3-secondary-dark); } .prio.low .m { background: var(--md3-secondary); }
    .prio b { color: var(--head); display: block; }
    .prio small { color: var(--ink); font-size: 13px; }
    .fld .ferr { color: var(--md3-error); font-size: 13px; }
    .curdiet { display: grid; gap: 2px; padding: var(--sp-12) var(--sp-16); border-radius: 8px; background: var(--md3-background); }
    .curdiet b { color: var(--head); }
    .curdiet small { color: var(--md3-neutral-secondary); }
    .toast .tact { margin-left: 12px; min-height: 36px; padding: 0 12px; border-radius: 6px; background: rgba(255,255,255,.16); color: var(--white); font-weight: 600; }
    .rqd { position: fixed; inset: var(--status-h) 0 0 0; z-index: 22; display: grid; grid-template-rows: auto 1fr auto; background: var(--md3-background); }
    .rqd[hidden] { display: none; }
    .rqd__body { overflow-y: auto; padding: var(--sp-16) var(--sp-16) var(--sp-24); }
    .rqd__inner { max-width: 1040px; margin: 0 auto; display: grid; gap: var(--sp-16); }
    .rqd__cols { display: grid; gap: var(--sp-16); align-items: start; }
    .dhero { position: relative; overflow: hidden; border-radius: var(--radius); background: var(--md3-on-primary-container); color: var(--white); padding: var(--sp-20); display: grid; gap: var(--sp-12); }
    .dhero .ribbon { position: absolute; top: 16px; right: 0; margin: 0; }
    .dhero__sp { display: flex; gap: var(--sp-12); align-items: center; padding-right: 72px; }
    .dhero__tile { width: 48px; height: 48px; border-radius: 8px; display: grid; place-items: center; background: rgba(255,255,255,.14); }
    .dhero__sp b { display: block; font-size: 22px; font-weight: 600; }
    .dhero__sp i { color: rgba(255,255,255,.75); }
    .dhero__meta { display: flex; flex-wrap: wrap; gap: var(--sp-12); align-items: center; color: rgba(255,255,255,.85); }
    .dhero__meta b { color: var(--white); }
    .dhero .stchip { display: inline-flex; align-items: center; gap: 6px; height: 28px; padding: 0 10px; border-radius: 6px; background: #FFF4CC; color: #6B5200; font-size: 13px; font-weight: 600; }
    .dhero .stchip.ok { background: #D7F5E3; color: var(--md3-on-surface); } .dhero .stchip.bad { background: #FFE0E5; color: var(--md3-error); }
    .dhero__who { display: flex; align-items: center; gap: var(--sp-12); padding-top: var(--sp-12); border-top: 1px solid rgba(255,255,255,.18); flex-wrap: wrap; }
    .dhero__who .grow { flex: 1; min-width: 0; display: grid; }
    .dhero__who small { color: rgba(255,255,255,.75); }
    .av { width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; flex: none; background: var(--md3-surface-variant); color: var(--md3-on-primary-container); font-weight: 600; font-size: 14px; }
    .dhero .av { background: var(--white); }
    .hbtn { min-height: 44px; padding: 0 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,.4); color: var(--white); display: inline-flex; align-items: center; gap: 8px; text-decoration: none; }
    .srows { background: var(--white); border-radius: var(--radius); padding: var(--sp-8) var(--sp-20); }
    .srow { display: grid; grid-template-columns: 40px 1fr; gap: var(--sp-12); padding: var(--sp-16) 0; border-bottom: 1px solid var(--line); }
    .srow:last-child { border-bottom: 0; }
    .srow .ic2 { width: 40px; height: 40px; border-radius: 8px; display: grid; place-items: center; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .srow h3 { color: var(--head); margin-bottom: 4px; }
    .srow p { color: var(--ink); }
    .srow p b { color: var(--head); display: block; }
    .srow small { color: var(--md3-neutral-secondary); display: block; }
    .pribadge { display: inline-flex; align-items: center; gap: 6px; height: 28px; padding: 0 10px; border-radius: 6px; color: var(--white); font-weight: 700; margin-right: 8px; }
    .pribadge.high { background: var(--md3-tertiary); } .pribadge.medium { background: var(--md3-secondary-dark); } .pribadge.low { background: var(--md3-secondary); }
    .tl { background: var(--white); border-radius: var(--radius); padding: var(--sp-16) var(--sp-20); }
    .tl h3 { color: var(--head); margin-bottom: 8px; display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
    .tl h3 small { color: var(--md3-neutral-secondary); font-weight: 400; }
    .tl ol { list-style: none; display: grid; }
    .tl li { position: relative; display: grid; grid-template-columns: 28px 1fr; gap: 12px; padding: 8px 0; }
    .tl li::before { content: ""; position: absolute; left: 13px; top: 34px; bottom: -8px; width: 2px; background: var(--md3-surface-variant); }
    .tl li:last-child::before { display: none; }
    .tl .mk { width: 28px; height: 28px; border-radius: 50%; display: grid; place-items: center; border: 2px solid var(--md3-outline-variant); background: var(--white); color: var(--md3-neutral-secondary); position: relative; z-index: 1; }
    .tl li.done .mk { background: var(--md3-primary); border-color: var(--md3-primary); color: var(--white); }
    .tl li.current .mk { border-color: var(--md3-on-primary-container); color: var(--md3-on-primary-container); box-shadow: 0 0 0 3px rgba(31,81,91,.15); }
    .tl li.rejected .mk { background: var(--md3-error); border-color: var(--md3-error); color: var(--white); }
    .tl li b { color: var(--head); }
    .tl li.pending b, .tl li.skipped b { color: var(--md3-neutral-secondary); font-weight: 500; }
    .tl li small { display: block; color: var(--md3-neutral-secondary); }
    .chat { background: var(--white); border-radius: var(--radius); padding: var(--sp-16) var(--sp-20); display: grid; gap: var(--sp-12); }
    .chat__h { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .chat__h h3 { flex: 1; color: var(--head); display: flex; align-items: center; gap: 8px; }
    .chat__h h3 small { color: var(--md3-neutral-secondary); font-weight: 400; }
    .thread { list-style: none; display: grid; gap: var(--sp-12); max-height: 360px; overflow-y: auto; }
    .msg { display: grid; grid-template-columns: 40px 1fr; gap: 10px; }
    .msg .bub { background: var(--md3-background); border-radius: 0 12px 12px 12px; padding: 10px 12px; color: var(--head); }
    .msg.me .bub { background: var(--md3-displaybg-primary); }
    .msg .meta { color: var(--md3-neutral-secondary); font-size: 12px; margin-bottom: 4px; }
    .msg .file { display: inline-flex; align-items: center; gap: 6px; margin-top: 6px; margin-right: 6px; padding: 6px 10px; border-radius: 6px; background: var(--white); border: 1px solid var(--md3-surface-variant); color: var(--md3-on-primary-container); font-size: 13px; }
    .msg.ev .bub { background: transparent; border: 1px dashed var(--md3-outline-variant); color: var(--ink); }
    .noms { display: flex; gap: 8px; align-items: center; padding: 12px; border-radius: 8px; background: var(--md3-background); color: var(--ink); }
    .composer { display: grid; grid-template-columns: 40px 1fr 48px 48px; gap: 8px; align-items: center; padding-top: var(--sp-12); border-top: 1px solid var(--line); }
    .composer label { display: block; min-width: 0; }
    .composer input[type=text] { width: 100%; min-height: 48px; padding: 0 12px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; font: inherit; }
    .composer .send { width: 48px; height: 48px; border-radius: 8px; background: var(--md3-on-primary-container); color: var(--white); display: grid; place-items: center; }
    .composer .att { width: 48px; height: 48px; border-radius: 8px; display: grid; place-items: center; color: var(--md3-on-primary-container); }
    .pending-files { grid-column: 2 / -1; display: flex; flex-wrap: wrap; gap: 6px; }
    .pending-files span { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 6px; background: var(--md3-background); font-size: 13px; }
    .rqd__foot { display: flex; align-items: center; gap: var(--sp-16); padding: var(--sp-12) var(--sp-16); background: var(--white); border-top: 1px solid var(--line); flex-wrap: wrap; }
    .rqd__foot .now { flex: 1; min-width: 240px; display: grid; }
    .rqd__foot .now small { color: var(--md3-neutral-secondary); }
    .rqd__foot .now b { color: var(--md3-on-primary-container); font-size: 18px; }
    .rqd__foot .now span { color: var(--md3-on-surface); font-weight: 600; }
    .hdcard { text-decoration: none; color: inherit; -webkit-tap-highlight-color: transparent; transition: transform 120ms var(--ease), box-shadow 200ms var(--ease); }
    a.hdcard:active { transform: scale(.99); }
    @media (hover: hover) { a.hdcard:hover { box-shadow: 0 4px 14px rgba(0,0,0,.12); } }
    @media (orientation: landscape) { .rqd__cols { grid-template-columns: minmax(0, 3fr) minmax(0, 2fr); } }
    @media (orientation: portrait) { .prisel { grid-template-columns: minmax(0, 1fr); } }
'''

REQ_OVERLAY = f'''  <div class="wiz" id="rqf" hidden role="dialog" aria-modal="true" aria-labelledby="rqfT">
    <header class="bar"><button class="iconbtn" type="button" data-rfclose aria-label="Close">{svg("close", 24)}</button><div class="bar__hd"><small>Diet request</small><h1 class="t-medium-medium" id="rqfT">Request Diet Change</h1><p class="t-body-regular" data-rfsub></p></div></header>
    <div class="steps" data-rfsteps aria-label="Steps"></div>
    <div class="wiz__body"><div class="wiz__inner" data-rfbody></div></div>
    <div class="wiz__foot" data-rffoot></div>
  </div>
  <div class="rqd" id="rqd" hidden role="dialog" aria-modal="true" aria-labelledby="rqdT">
    <div class="rqd__top"><header class="bar"><button class="iconbtn" type="button" data-rdback aria-label="Back">{svg("back", 24)}</button><div class="bar__hd"><h1 class="t-medium-medium" id="rqdT"></h1><p class="t-body-regular" data-rdsub></p></div><button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button></header><nav class="rdtabs two" role="tablist" aria-label="Request views" data-rdtabs hidden></nav></div>
    <div class="rqd__body"><div class="rqd__inner" data-rdbody></div></div>
    <div class="rqd__foot" data-rdfoot></div>
  </div>'''

# ------------------------------------------------------------------ shared request helpers (top level)
REQ_SHARED_JS = '''  /* ---------------- Diet requests: shared store + detail (V2 dr-core.js / request.js) ---------------- */
  var REQS_ALL = ''' + json.dumps(REQS, ensure_ascii=False).replace('</', '<\\/') + ''';
  REQS_ALL.forEach(function (r) { r.by = r.by || { name: 'Carol Steve', role: 'Site Manager' }; r.events = r.events || [{ kind: 'submitted', at: r.iso + 'T09:00', by: r.by.name, text: 'Request submitted' }]; });
  var RQ = {
    PRI: { high: ['!!!', 'High', 'Clinical or urgent. Needs action today.'], medium: ['!!', 'Medium', 'Needed within the next few days.'], low: ['!', 'Low', 'Routine change with no deadline.'] },
    TYPES: [['temporary', 'Temporary / Time-bound'], ['base', 'Base diet change'], ['site', 'Site / Section-specific'], ['animal', 'Animal-specific']],
    STEPS: ['Request submitted', 'Dietician reviewing', 'New diet configured', 'Kitchen processing', 'Sent to prep', 'Preparing diet', 'Dispatched', 'Approved'],
    me: { name: 'Dr. Meera Iyer', role: 'Head Dietician' },
    MON: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    fmt: function (iso) { if (!iso) return ''; var p = iso.slice(0, 10).split('-'); return Number(p[2]) + ' ' + RQ.MON[Number(p[1]) - 1] + ' ' + p[0]; },
    fmtDT: function (iso) { return RQ.fmt(iso) + (iso && iso.length > 10 ? ', ' + iso.slice(11, 16) : ''); },
    now: function () { var d = new Date(), p = function (n) { return ('0' + n).slice(-2); }; return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + 'T' + p(d.getHours()) + ':' + p(d.getMinutes()); },
    ago: function (iso) { if (!iso) return ''; var q = iso.split(/[-T:]/).map(Number), m = Math.round((Date.now() - new Date(q[0], q[1] - 1, q[2], q[3] || 0, q[4] || 0).getTime()) / 60000); if (m < 1) return 'Just now'; if (m < 60) return m + ' min ago'; var h = Math.round(m / 60); if (h < 24) return h + ' h ago'; var d = Math.round(h / 24); return d === 1 ? 'Yesterday' : d < 7 ? d + ' days ago' : RQ.fmt(iso); },
    initials: function (n) { return String(n || '?').replace(/^Dr\\.?\\s+/i, '').split(/\\s+/).filter(Boolean).slice(0, 2).map(function (w) { return w[0].toUpperCase(); }).join(''); },
    get: function (id) { for (var i = 0; i < REQS_ALL.length; i++) if (REQS_ALL[i].id === id) return REQS_ALL[i]; return null; },
    isOpen: function (r) { return r.tone === 'wait'; },
    nextId: function () { var n = Math.max.apply(null, REQS_ALL.map(function (r) { return Number(r.id.replace(/\\D/g, '')); })) + 1; return 'DR-' + ('0000' + n).slice(-5); },
    listeners: [],
    changed: function () { RQ.listeners.forEach(function (f) { f(); }); var t = document.getElementById('t-request'); if (t) t.textContent = 'Diet Request - ' + REQS_ALL.length; },
    step: function (r) {
      if (r.label === 'Rejected') return { cur: 2, end: 'rejected' }; if (r.label === 'Cancelled') return { cur: 2, end: 'cancelled' };
      if (r.group === 'awaiting') return { cur: 2 }; if (r.group === 'approved' || r.group === 'progress') return { cur: 3 };
      if (/Applied/.test(r.label)) return { cur: 6, phaseDone: true }; return { cur: 4, delayed: /Delayed/.test(r.label) };
    },
    timeline: function (r) {
      var s = RQ.step(r);
      return RQ.STEPS.map(function (label, i) {
        var n = i + 1, state = n < s.cur ? 'done' : n === s.cur ? 'current' : 'pending', sub = '';
        if (s.phaseDone && n >= 6) state = 'pending';
        if (s.phaseDone && n === 5) state = 'done';
        if (s.end && n >= 2) state = n === 2 ? 'rejected' : 'skipped';
        if (n === 1) { state = 'done'; sub = RQ.fmtDT(r.events[0].at) + ' by ' + r.by.name; }
        if (n === 2) sub = s.end === 'rejected' ? 'Rejected by the Head Dietician' : s.end === 'cancelled' ? 'Cancelled by the requester' : state === 'current' ? 'Waiting for the Head Dietician' : state === 'done' ? 'Accepted' : '';
        if (n === 3 && state === 'current') sub = 'Being configured';
        if (n === 4 && state === 'current') sub = s.delayed ? r.label.split(' · ').pop() : 'Stock and feasibility check';
        if (n === 5 && state === 'done') sub = 'Applied by the kitchen';
        return { n: n, label: label, state: state, sub: sub };
      });
    },
    next: function (r) {
      var s = RQ.step(r);
      if (s.end) return s.end === 'rejected' ? 'Closed. The request was rejected.' : 'Closed. The request was cancelled.';
      if (s.cur === 2) return 'Head Dietician to review'; if (s.cur === 3) return 'Head Dietician to configure the new diet';
      if (s.cur === 4) return 'Kitchen to check stock and accept'; return 'Sent to prep. Later steps are not part of this phase.';
    },
  };

  function ReqDetail() {
    var el = document.getElementById('rqd'), cur = null, files = [], showEv = false;
    function row(icn, title, body) { return '<div class="srow"><span class="ic2">' + ic(icn, 22) + '</span><div><h3 class="t-minor-title">' + esc(title) + '</h3>' + body + '</div></div>'; }
    function pb(p) { return '<span class="pribadge ' + p + '">' + RQ.PRI[p][0] + ' ' + RQ.PRI[p][1] + '</span>'; }
    function draw() {
      var r = cur; if (!r) return;
      document.getElementById('rqdT').textContent = r.id; el.querySelector('[data-rdsub]').textContent = r.sp + ' · ' + r.title;
      var stc = r.tone === 'ok' ? 'ok' : r.tone === 'bad' ? 'bad' : '';
      var hero = '<section class="dhero" aria-label="Request summary"><span class="ribbon ' + r.prio + '" title="' + RQ.PRI[r.prio][1] + ' priority" aria-label="' + RQ.PRI[r.prio][1] + ' priority">' + RQ.PRI[r.prio][0] + '</span>' +
        '<div class="dhero__sp"><span class="dhero__tile">' + ic('paw', 26) + '</span><span><b>' + esc(r.sp) + '</b>' + (r.sci ? '<i class="t-body-regular">' + esc(r.sci) + '</i>' : '') + '</span></div>' +
        '<p class="dhero__meta t-body-regular"><b>' + esc(r.id) + '</b><span>' + esc(RQ.fmtDT(r.events[0].at)) + '</span><span class="stchip ' + stc + '">' + ic(r.icon, 16) + esc(r.label) + '</span></p>' +
        '<div class="dhero__who"><span class="av">' + RQ.initials(r.by.name) + '</span><span class="grow"><b class="t-body-title">' + esc(r.by.name + (r.mine ? ' (You)' : '')) + '</b><small class="t-body-regular">' + esc(r.by.role) + '</small></span>' +
        (r.tsn ? '<a class="hbtn t-body-medium" href="#species/all/' + r.tsn + (r.planId ? '/' + r.planId : '') + '">' + ic('paw', 20) + 'View species</a>' : '') + '</div></section>';
      var typeTxt = (RQ.TYPES.filter(function (t) { return t[0] === r.type; })[0] || [0, ''])[1];
      var secs = '<section class="srows" aria-label="Request">' +
        row('location-icon', 'Applies to', '<p class="t-body-regular"><b>' + esc(r.scopeText || r.where.split(' · ').slice(1).join(' · ') || 'Whole species') + '</b>' + esc(r.where.split(' · ')[0]) + '</p>') +
        (r.currentLabel ? row('book', 'Current diet', '<p class="t-body-regular"><b>' + esc(r.currentLabel) + '</b>' + (r.currentLabel === 'No active diet' ? 'This species has no diet yet' : 'Active, not changed by this request') + '</p><span class="tag teal" style="margin-top:6px">' + (r.type === 'base' ? 'Change requested' : 'New diet requested') + '</span>') : '') +
        row('reason-or-list', 'Request', '<p class="t-body-regular"><b>' + esc(r.title) + '</b>' + esc(r.text) + '</p>') +
        (typeTxt ? row('calendar', 'Diet type', '<p class="t-body-regular">' + esc(typeTxt + (r.start ? ' · ' + RQ.fmt(r.start) + (r.end ? ' to ' + RQ.fmt(r.end) : ' onwards') : '')) + '</p>') : '') +
        row('alert', 'Priority', '<p class="t-body-regular">' + pb(r.prio) + esc(RQ.PRI[r.prio][2]) + '</p>') +
        (r.notes ? row('notes-new', 'Notes', '<p class="t-body-regular">' + esc(r.notes) + '</p>') : '') +
        row('user', 'Requested by', '<div style="display:flex;gap:10px;align-items:center"><span class="av">' + RQ.initials(r.by.name) + '</span><span><b class="t-body-title" style="color:var(--head)">' + esc(r.by.name + (r.mine ? ' (You)' : '')) + '</b><small class="t-body-regular">' + esc(r.by.role + ' · ' + RQ.fmtDT(r.events[0].at)) + '</small></span></div>') + '</section>';
      var tl = RQ.timeline(r), curS = tl.filter(function (x) { return x.state === 'current'; })[0];
      var prog = '<section class="tl" aria-label="Progress"><h3 class="t-minor-title">Progress <small class="t-body-regular">' + (r.label === 'Rejected' || r.label === 'Cancelled' ? r.label : curS ? 'Step ' + curS.n + ' of 8: ' + curS.label : 'Phase 1 done') + '</small></h3><ol>' +
        tl.map(function (t) { return '<li class="' + t.state + '"><span class="mk" aria-hidden="true">' + (t.state === 'done' ? ic('just-tick-mark', 16) : t.state === 'rejected' ? ic('close', 16) : t.state === 'current' ? '<i style="width:10px;height:10px;border-radius:50%;background:currentColor;display:block"></i>' : '') + '</span><div><b class="t-body-title">' + esc(t.label) + '</b>' + (t.state === 'current' ? ' <span class="tag teal">Now</span>' : '') + (t.sub ? '<small class="t-body-regular">' + esc(t.sub) + '</small>' : '') + '</div></li>'; }).join('') + '</ol></section>';
      var msgs = r.events.filter(function (e) { return showEv || e.kind === 'comment'; });
      var chat = '<section class="chat" aria-label="Chat"><div class="chat__h"><h3 class="t-minor-title">' + ic('reason-or-list', 20) + 'Chat <small class="t-body-regular">' + plural(r.events.filter(function (e) { return e.kind === 'comment'; }).length, 'message') + '</small></h3><button type="button" class="chip t-body-medium" data-rdev aria-pressed="' + showEv + '">' + ic('history', 18) + (showEv ? 'Hide updates' : 'Show updates') + '</button></div>' +
        (msgs.length ? '<ol class="thread" data-thread>' + msgs.map(function (m) {
          if (m.kind !== 'comment') return '<li class="msg ev"><span></span><div class="bub t-body-regular"><div class="meta">' + esc(RQ.fmtDT(m.at)) + '</div>' + esc(m.text + ' by ' + m.by) + '</div></li>';
          return '<li class="msg' + (m.mine ? ' me' : '') + '"><span class="av">' + RQ.initials(m.by) + '</span><div class="bub t-body-regular"><div class="meta">' + esc(m.by + (m.mine ? ' (You)' : '') + ' · ' + RQ.ago(m.at)) + '</div>' + (m.text ? esc(m.text) : '') +
            (m.files && m.files.length ? '<div>' + m.files.map(function (f) { return '<span class="file">' + ic('notes-new', 16) + esc(f) + '</span>'; }).join('') + '</div>' : '') + '</div></li>';
        }).join('') + '</ol>' : '<p class="noms t-body-regular">' + ic('reason-or-list', 20) + 'No messages yet. Ask a question or share a file with everyone working on this request.</p>') +
        '<div class="composer"><span class="av">' + RQ.initials(RQ.me.name) + '</span><label><span class="sr-only">Write a message</span><input type="text" data-rdmsg placeholder="Write a message" autocomplete="off"></label>' +
        '<button type="button" class="att" data-rdattach aria-label="Attach a file">' + ic('add', 24) + '</button><button type="button" class="send" data-rdsend aria-label="Send">' + ic('back', 22).replace('<svg', '<svg style="transform:rotate(180deg)"') + '</button>' +
        (files.length ? '<div class="pending-files">' + files.map(function (f, i) { return '<span>' + ic('notes-new', 14) + esc(f) + '<button type="button" class="iconbtn" style="width:32px;height:32px" data-rdrmf="' + i + '" aria-label="Remove ' + esc(f) + '">' + ic('close', 16) + '</button></span>'; }).join('') + '</div>' : '') +
        '<input type="file" data-rdfile multiple hidden></div></section>';
      el.querySelector('[data-rdbody]').innerHTML = hero + '<div class="rqd__cols"><div style="display:grid;gap:16px">' + secs + '</div><div style="display:grid;gap:16px">' + prog + '</div></div>' + chat;
      el.querySelector('[data-rdfoot]').innerHTML = '<div class="now"><small class="t-body-regular">Current status · ' + esc(RQ.ago(r.events.filter(function (e) { return e.kind !== 'comment'; }).pop().at)) + '</small><b>' + esc(r.label) + '</b><span class="t-body-medium">' + esc(RQ.next(r)) + '</span></div>' +
        '<button type="button" class="btn sec" data-rdback style="flex:none;min-width:140px">Back</button>';
      var th = el.querySelector('[data-thread]'); if (th) th.scrollTop = th.scrollHeight;
    }
    el.addEventListener('click', function (e) {
      var t;
      if (e.target.closest('[data-rdback]')) { if (pushed && history.length > 1) history.back(); else location.hash = '#request'; return; }
      if (e.target.closest('[data-rdev]')) { showEv = !showEv; draw(); return; }
      if (e.target.closest('[data-rdattach]')) { el.querySelector('[data-rdfile]').click(); return; }
      if ((t = e.target.closest('[data-rdrmf]'))) { files.splice(Number(t.getAttribute('data-rdrmf')), 1); var v = el.querySelector('[data-rdmsg]').value; draw(); el.querySelector('[data-rdmsg]').value = v; return; }
      if (e.target.closest('[data-rdsend]')) send();
    });
    el.addEventListener('change', function (e) { if (e.target.matches('[data-rdfile]')) { [].forEach.call(e.target.files, function (f) { files.push(f.name); }); var v = el.querySelector('[data-rdmsg]').value; draw(); el.querySelector('[data-rdmsg]').value = v; } });
    el.addEventListener('keydown', function (e) { if (e.target.matches('[data-rdmsg]') && e.key === 'Enter') { e.preventDefault(); send(); } });
    function send() { var inp = el.querySelector('[data-rdmsg]'), txt = inp.value.trim(); if (!txt && !files.length) { toast('Type a message or attach a file.'); return; }
      cur.events.push({ kind: 'comment', at: RQ.now(), by: RQ.me.name, mine: true, text: txt, files: files.slice() }); files = []; draw(); }
    var pushed = false;
    return {
      open: function (id, wasPushed) { var r = RQ.get(id); if (!r) { toast('Request ' + id + ' was not found.'); return false; } if (cur !== r) { files = []; showEv = false; } cur = r; pushed = !!wasPushed; el.hidden = false; draw(); el.querySelector('.rqd__body').scrollTop = 0; return true; },
      close: function () { cur = null; el.hidden = true; },
      isOpen: function () { return !!cur; },
      addFile: function (name) { files.push(name); draw(); },
    };
  }
'''

# ------------------------------------------------------------------ request form (inside SpModule)
REQ_FORM_JS = '''    /* ======================= REQUEST DIET CHANGE (V2 dr-core.js openForm) ======================= */
    var RF = null;
    function openReqs(s, scope, ref) { return RQ.visible().filter(function (r) { return r.tsn === s.tsn && RQ.isOpen(r) && (scope == null || (r.scope === scope && (scope === 'species' || r.scopeRef === ref))); }); }
    function reqBadge(list) { if (!list.length) return ''; return '<button type="button" class="rqb" data-rqopen="' + list[0].id + '" aria-label="' + plural(list.length, 'open request') + ', open ' + list[0].id + '">' + ic('time', 16) + plural(list.length, 'open request') + '</button>'; }
    function activeFor(s, scope, ref) {
      var at = plansOf(s).filter(function (p) { return p.active && !p.from && !p.to && p.scope === scope && (scope === 'species' || p.ref === ref); })[0];
      return at || basePlan(s) || null;
    }
    function rfScope() { return RF.f.animal ? 'animal' : RF.f.enclosure ? 'enclosure' : RF.f.section ? 'section' : RF.f.site ? 'site' : 'species'; }
    function rfRef() { var sc = rfScope(); return sc === 'species' ? null : Number(RF.f[sc]); }
    function rfRefName() {
      var s = BY[RF.tsn], sc = rfScope(), e;
      if (sc === 'animal') { var a = (s.animalList || []).filter(function (x) { return String(x.id) === RF.f.animal; })[0]; return a ? animalLabel(a) : null; }
      if (sc === 'enclosure') { e = encById(s, Number(RF.f.enclosure)); return e ? e.name : null; }
      if (sc === 'section') { e = (s.enclosures || []).filter(function (x) { return String(x.sectionId) === RF.f.section; })[0]; return e ? e.section : null; }
      if (sc === 'site') { e = (s.enclosures || []).filter(function (x) { return String(x.siteId) === RF.f.site; })[0]; return e ? e.site : null; }
      return null;
    }
    function rfHash(step) { return '#species/' + st.seg + '/' + RF.tsn + '/request/new/' + step; }
    function openRequest(ctx, fromHash) {
      var s = BY[st.tsn]; if (!s) return;
      ctx = ctx || {};
      var f = { site: '', section: '', enclosure: '', animal: '', type: 'temporary', priority: '', title: '', start: '', end: '', reason: '', notes: '' };
      var scope = ctx.scope || 'species', ref = ctx.ref;
      if (scope !== 'species' && ref != null) {
        var e0;
        if (scope === 'site') f.site = String(ref);
        if (scope === 'section') { f.section = String(ref); e0 = (s.enclosures || []).filter(function (e) { return e.sectionId === ref; })[0]; }
        if (scope === 'enclosure') { f.enclosure = String(ref); e0 = encById(s, ref); }
        if (scope === 'animal') { f.animal = String(ref); var a0 = (s.animalList || []).filter(function (a) { return a.id === ref; })[0]; e0 = a0 && encById(s, a0.enclosure); if (e0) f.enclosure = String(e0.id); }
        if (e0) { f.section = String(e0.sectionId); f.site = String(e0.siteId); }
        f.type = scope === 'animal' ? 'animal' : 'site';
      }
      if (ctx.plan) f.type = PLANS[ctx.plan] && (PLANS[ctx.plan].from || PLANS[ctx.plan].to) ? 'temporary' : scope === 'species' ? 'base' : f.type;
      if (ctx.edit) { var R0 = ctx.edit; f.type = R0.type; f.priority = R0.prio; f.title = R0.title; f.start = R0.start || ''; f.end = R0.end || ''; f.reason = R0.text; f.notes = R0.notes || ''; }
      RF = { tsn: s.tsn, f: f, plan: ctx.plan || null, step: 'where', errs: {}, from: ctx.from || 'species', edit: ctx.edit ? ctx.edit.id : null };
      var h = rfHash('where'); if (fromHash) { try { history.replaceState(null, '', h); } catch (x) {} } else location.hash = h;
      document.getElementById('rqf').hidden = false; drawRF();
    }
    function closeRF() { RF = null; document.getElementById('rqf').hidden = true; }
    function sel(key, label, options, o) { o = o || {}; return fld(label + (o.opt ? ' <span style="color:var(--md3-neutral-secondary);font-weight:400">(optional)</span>' : ''), '<select data-rf="' + key + '"' + (o.dis ? ' disabled' : '') + '>' + options.map(function (x) { return '<option value="' + esc(x[0]) + '"' + (String(x[0]) === String(RF.f[key]) ? ' selected' : '') + '>' + esc(x[1]) + '</option>'; }).join('') + '</select>' + (RF.errs[key] ? '<span class="ferr">' + esc(RF.errs[key]) + '</span>' : ''), { req: o.req, err: !!RF.errs[key] }); }
    function inp(key, label, type, o) { o = o || {}; var tag = type === 'textarea' ? '<textarea data-rf="' + key + '" placeholder="' + esc(o.ph || '') + '">' + esc(RF.f[key]) + '</textarea>' : '<input type="' + type + '" data-rf="' + key + '" value="' + esc(RF.f[key]) + '" placeholder="' + esc(o.ph || '') + '"' + (o.min ? ' min="' + o.min + '"' : '') + '>';
      return fld(label + (o.opt ? ' <span style="color:var(--md3-neutral-secondary);font-weight:400">(optional)</span>' : ''), tag + (RF.errs[key] ? '<span class="ferr">' + esc(RF.errs[key]) + '</span>' : ''), { req: o.req, err: !!RF.errs[key] }); }
    function rfStrip() {
      var s = BY[RF.tsn], sc = rfScope(), nm = rfRefName(), cur = activeFor(s, sc, rfRef()), p0 = RF.plan ? PLANS[RF.plan] : null, p = p0 && p0.scope === sc && (sc === 'species' || p0.ref === rfRef()) ? p0 : null;
      var parts = [s.name, ({ species: 'Species-wide', site: 'Site-wide', section: 'Section-wide', enclosure: 'Enclosure-wide', animal: 'Animal-wide' })[sc]];
      if (nm) parts.push(nm); parts.push(p ? shownId(p) : cur ? shownId(cur) : 'No active diet');
      return '<div class="ctxstrip t-body-medium">' + ic('reason-or-list', 18) + '<span>' + esc(parts.join(' · ')) + '</span>' + (RF.step !== 'where' ? '<button type="button" class="linkbtn t-body-medium" data-rfgo="where">Change</button>' : '') + '</div>';
    }
    function uniqBy(list, k, lab) { var seen = {}, out = []; list.forEach(function (e) { if (!seen[e[k]]) { seen[e[k]] = 1; out.push([String(e[k]), lab(e)]); } }); return out; }
    function rfWhere() {
      var s = BY[RF.tsn], E = s.enclosures || [], f = RF.f;
      var inSite = E.filter(function (e) { return !f.site || String(e.siteId) === f.site; }), inSec = inSite.filter(function (e) { return !f.section || String(e.sectionId) === f.section; });
      var inEnc = inSec.filter(function (e) { return !f.enclosure || String(e.id) === f.enclosure; }).map(function (e) { return e.id; });
      var pl = RF.plan ? PLANS[RF.plan] : null, cur = pl && pl.scope === rfScope() && (pl.scope === 'species' || pl.ref === rfRef()) ? pl : activeFor(s, rfScope(), rfRef());
      return '<section class="wcard"><h2 class="t-medium-medium">Where the change applies</h2><p class="sub t-body-regular">Leave a level on "All" to apply the request more widely.</p>' +
        fld('Species', '<input type="text" value="' + esc(s.name) + '" disabled>') +
        '<div class="g2">' + sel('site', 'Site', [['', 'All sites']].concat(uniqBy(E, 'siteId', function (e) { return e.site; })), { opt: true }) +
        sel('section', 'Section', [['', 'All sections']].concat(uniqBy(inSite, 'sectionId', function (e) { return e.section; })), { opt: true }) +
        sel('enclosure', 'Enclosure', [['', 'All enclosures']].concat(uniqBy(inSec, 'id', function (e) { return e.name; })), { opt: true }) +
        sel('animal', 'Individual animal', [['', 'All animals']].concat((s.animalList || []).filter(function (a) { return inEnc.indexOf(a.enclosure) !== -1; }).map(function (a) { return [String(a.id), animalLabel(a) + (a.label ? ' (#' + a.id + ')' : '')]; })), { opt: true }) + '</div>' +
        '<div class="curdiet t-body-regular"><span class="t-body-medium" style="color:var(--ink)">Current diet</span><b>' + esc(cur ? shownId(cur) + ' ' + (KIND[cur.kind] || KIND.base)[1] : 'No active diet') + '</b><small>Read only. It stays active while the request is open.</small></div></section>';
    }
    function rfDetails() {
      var f = RF.f;
      return '<section class="wcard"><h2 class="t-medium-medium">Request</h2>' + sel('type', 'Request type', RQ.TYPES, { req: true }) +
        '<div class="fld' + (RF.errs.priority ? ' err' : '') + '"><span id="rfPriL">Priority <b class="req">*</b></span><div class="prisel" role="radiogroup" aria-labelledby="rfPriL" aria-required="true">' +
        ['high', 'medium', 'low'].map(function (p) { return '<button type="button" class="prio ' + p + '" role="radio" aria-checked="' + (f.priority === p) + '" data-rfpri="' + p + '"><span class="m" aria-hidden="true">' + RQ.PRI[p][0] + '</span><span><b class="t-minor-title">' + RQ.PRI[p][1] + '</b><small>' + RQ.PRI[p][2] + '</small></span></button>'; }).join('') +
        '</div>' + (RF.errs.priority ? '<span class="ferr">' + esc(RF.errs.priority) + '</span>' : '') + '</div>' +
        inp('title', 'Short title', 'text', { opt: true, ph: 'For example Temporary Recovery Diet' }) +
        '<div class="g2">' + inp('start', 'Start', 'date', { req: true }) + inp('end', 'End', 'date', { req: f.type === 'temporary', opt: f.type !== 'temporary', min: f.start }) + '</div>' +
        inp('reason', 'Reason', 'textarea', { req: true, ph: 'Why the diet needs to change' }) + inp('notes', 'Notes', 'textarea', { opt: true }) +
        alertBox('The Head Dietician reviews the request next. The active diet does not change.', true) + '</section>';
    }
    function drawRF() {
      if (!RF) return;
      var s = BY[RF.tsn], steps = [['where', 'Where it applies'], ['details', 'Request']], idx = RF.step === 'where' ? 0 : 1;
      document.querySelector('#rqf [data-rfsub]').textContent = s.name + (RF.edit ? ' · ' + RF.edit : '');
      document.getElementById('rqfT').textContent = RF.edit ? 'Edit request' : 'Request Diet Change';
      document.querySelector('#rqf [data-rfsteps]').innerHTML = steps.map(function (x, i) { return '<span class="' + (i === idx ? 'on' : i < idx ? 'done' : '') + '">' + (i < idx ? ic('just-tick-mark', 16) : (i + 1) + '.') + ' ' + x[1] + '</span>'; }).join('');
      document.querySelector('#rqf [data-rfbody]').innerHTML = rfStrip() + (RF.step === 'where' ? rfWhere() : rfDetails());
      document.querySelector('#rqf [data-rffoot]').innerHTML = '<button type="button" class="btn ghost" data-rfclose>Cancel</button><span class="sp"></span>' + (idx ? '<button type="button" class="btn sec" data-rfback>Back</button><button type="button" class="btn pri" data-rfsubmit>' + ic('just-tick-mark', 20) + (RF.edit ? 'Save changes' : 'Submit request') + '</button>' : '<button type="button" class="btn pri" data-rfnext>Continue</button>');
    }
    function rfValidate() {
      var f = RF.f, e = {};
      if (!f.priority) e.priority = 'Choose how urgent this request is.';
      if (!f.reason.trim()) e.reason = 'Say why the diet needs to change.';
      if (!f.start) e.start = 'Enter the start date.';
      if (f.type === 'temporary' && !f.end) e.end = 'A temporary diet needs an end date.';
      if (f.start && f.end && f.end < f.start) e.end = 'The end date is before the start date.';
      if (f.type === 'animal' && !f.animal) e.type = 'Choose the animal (in Where it applies) for an animal-specific diet.';
      if (f.type === 'site' && !f.site) e.type = 'Choose the site or section (in Where it applies) for a site-specific diet.';
      return e;
    }
    function rfSubmit() {
      RF.errs = rfValidate(); var n = Object.keys(RF.errs).length;
      if (n) { drawRF(); toast('Fix the ' + (n === 1 ? 'highlighted field' : n + ' highlighted fields') + ' to submit.'); return; }
      var s = BY[RF.tsn], f = RF.f, sc = rfScope(), ref = rfRef(), nm = rfRefName(), p0 = RF.plan ? PLANS[RF.plan] : null, cur = p0 && p0.scope === sc && (sc === 'species' || p0.ref === ref) ? p0 : activeFor(s, sc, ref), at = RQ.now();
      var where = ({ species: 'Species', site: 'Site', section: 'Section', enclosure: 'Enclosure', animal: 'Animal' })[sc] + ' · ' + (nm || 'Species-wide');
      if (RF.edit) { var R1 = RQ.get(RF.edit); Object.assign(R1, { where: where, scope: sc, scopeRef: ref, scopeText: nm || 'Whole species', prio: f.priority, title: f.title.trim() || R1.title, text: f.reason.trim(), notes: f.notes.trim(), type: f.type, start: f.start, end: f.end });
        RQ.ev(R1, 'updated', 'Request updated by the requester'); RQ.changed(); var rid = R1.id; closeRF(); try { history.replaceState(null, '', '#request/' + rid); } catch (x) {} window.dispatchEvent(new HashChangeEvent('hashchange')); toast(rid + ' updated'); return; }
      var rec = { id: RQ.nextId(), status: 'requested', sp: s.name, sci: s.sci, tsn: s.tsn, where: where, scope: sc, scopeRef: ref, scopeText: nm || 'Whole species', prio: f.priority,
        title: f.title.trim() || { temporary: 'Temporary Diet Change', base: 'Base Diet Change', site: 'Site / Section Diet', animal: 'Animal-specific Diet' }[f.type],
        text: f.reason.trim(), notes: f.notes.trim(), type: f.type, start: f.start, end: f.end, date: RQ.fmt(at), iso: at.slice(0, 10), group: 'awaiting', label: 'Awaiting approval', tone: 'wait', icon: 'time',
        currentLabel: cur ? shownId(cur) + ' ' + (KIND[cur.kind] || KIND.base)[1] : 'No active diet', planId: cur ? cur.id : null, by: { id: RQ.viewer.id, name: RQ.viewer.name, role: RQ.viewer.title }, events: [{ kind: 'submitted', at: at, by: RQ.viewer.name, role: RQ.viewer.title, text: 'Request submitted' }] };
      REQS_ALL.unshift(RQ.decorate(rec)); RQ.changed();
      var back = '#species/' + st.seg + '/' + s.tsn + (RF.plan ? '/' + RF.plan : '');
      if (RF.from === 'scope' || RF.from === 'plan') { st.scope = sc === 'enclosure' || sc === 'section' || sc === 'site' || sc === 'animal' ? sc : st.scope; if (sc !== 'species') st.ref = ref; }
      closeRF(); try { history.replaceState(null, '', back); } catch (x) {}
      drawList(); if (LAND.matches) drawDetail(); else openPanel();
      toastAct('Request ' + rec.id + ' submitted. The Head Dietician reviews it next.', 'View request', '#request/' + rec.id);
    }
    function toastAct(msg, label, href) {
      var t = document.getElementById('toast'); t.innerHTML = esc(msg) + '<button type="button" class="tact" data-tgo="' + href + '">' + esc(label) + '</button>'; t.style.pointerEvents = 'auto'; t.classList.add('on');
      clearTimeout(toastAct.t); toastAct.t = setTimeout(function () { t.classList.remove('on'); t.style.pointerEvents = ''; }, 6000); toastAct.at = Date.now();
    }
    window.addEventListener('hashchange', function () { if (toastAct.at && Date.now() - toastAct.at > 400) { var t = document.getElementById('toast'); t.classList.remove('on'); t.style.pointerEvents = ''; toastAct.at = 0; } });
    document.getElementById('toast').addEventListener('click', function (e) { var b = e.target.closest('[data-tgo]'); if (b) { this.classList.remove('on'); this.style.pointerEvents = ''; location.hash = b.getAttribute('data-tgo'); } });
    var rqf = document.getElementById('rqf');
    rqf.addEventListener('click', function (e) {
      if (!RF) return; var t;
      if (e.target.closest('[data-rfclose]')) { var back = RF.edit ? '#request/' + RF.edit : '#species/' + st.seg + '/' + RF.tsn + (RF.plan ? '/' + RF.plan : ''); closeRF(); try { history.replaceState(null, '', back); } catch (x) {} window.dispatchEvent(new HashChangeEvent('hashchange')); return; }
      if (e.target.closest('[data-rfnext]')) { RF.step = 'details'; location.hash = rfHash('details'); drawRF(); return; }
      if (e.target.closest('[data-rfback]')) { history.back(); return; }
      if ((t = e.target.closest('[data-rfgo]'))) { history.back(); return; }
      if ((t = e.target.closest('[data-rfpri]'))) { RF.f.priority = t.getAttribute('data-rfpri'); delete RF.errs.priority; drawRF(); return; }
      if (e.target.closest('[data-rfsubmit]')) rfSubmit();
    });
    rqf.addEventListener('input', function (e) { if (!RF) return; var t = e.target; if (t.matches('[data-rf]') && t.tagName !== 'SELECT') { RF.f[t.getAttribute('data-rf')] = t.value; } });
    rqf.addEventListener('change', function (e) {
      if (!RF) return; var t = e.target; if (!t.matches('[data-rf]')) return; var k = t.getAttribute('data-rf'), s = BY[RF.tsn], f = RF.f; f[k] = t.value; delete RF.errs[k];
      var E = s.enclosures || [];
      if (k === 'site') { var s1 = E.filter(function (x) { return String(x.sectionId) === f.section; })[0]; if (!s1 || String(s1.siteId) !== f.site) f.section = f.enclosure = f.animal = ''; }
      if (k === 'section') { var s2 = E.filter(function (x) { return String(x.sectionId) === f.section; })[0]; if (s2) f.site = String(s2.siteId); var e2 = encById(s, Number(f.enclosure)); if (!e2 || String(e2.sectionId) !== f.section) f.enclosure = f.animal = ''; }
      if (k === 'enclosure') { var e3 = encById(s, Number(f.enclosure)); if (e3) { f.section = String(e3.sectionId); f.site = String(e3.siteId); } var a3 = (s.animalList || []).filter(function (a) { return String(a.id) === f.animal; })[0]; if (!a3 || String(a3.enclosure) !== f.enclosure) f.animal = ''; }
      if (k === 'animal') { var a4 = (s.animalList || []).filter(function (a) { return String(a.id) === f.animal; })[0], e4 = a4 && encById(s, a4.enclosure); if (e4) { f.enclosure = String(e4.id); f.section = String(e4.sectionId); f.site = String(e4.siteId); } }
      if (k === 'type' || k === 'site' || k === 'section' || k === 'enclosure' || k === 'animal') { delete RF.errs.type; drawRF(); }
    });
    function rfRoute(tsn, step) {
      if (RF && RF.tsn === tsn) { RF.step = step === 'details' ? 'details' : 'where'; document.getElementById('rqf').hidden = false; drawRF(); return; }
      st.tsn = tsn; openRequest({ scope: 'species' }, true);
    }
    HOOKS.edit = function (rec) { if (!BY[rec.tsn]) { toast('This request has no species record here to edit against.'); return; } st.tsn = rec.tsn; resetScope(); if (LAND.matches) { drawList(); drawDetail(); } else openPanel(); openRequest({ scope: rec.scope, ref: rec.scopeRef, edit: rec, from: 'edit' }); };
    /* ---------- Apply to configuration: "How should this request be configured?" ---------- */
    var CFG = null;
    var CFG_LABEL = { base: 'Base diet', 'year-round': 'Year-round diet', seasonal: 'Seasonal diet', 'time-bound': 'Time-bound diet' };
    function cfgOptions(rec) {
      var s = BY[rec.tsn], sc = rec.scope, ref = sc === 'species' ? null : rec.scopeRef, base = basePlan(s), here = sc === 'species' ? base : scopePlansFor(s, sc, ref).filter(isDefault)[0];
      var scName = sc === 'species' ? 'this species' : 'this ' + sc, prop = rec.proposedId && PLANS[rec.proposedId];
      var noBase = 'No base diet yet. This proposal will also need a base diet before it can go live.';
      var baseNote = base ? (sc === 'species' ? 'A base diet already exists. You’ll propose changes to ' + shownId(base) + '.' : 'Base diets are species-wide. This will propose a change to the ' + s.name + ' base diet (' + shownId(base) + ').')
        : (sc === 'species' ? 'This species has no base diet yet. This will create the species-wide base.' : 'Base diets are species-wide. This will create the species-wide base.');
      var o = [];
      if (prop) o.push({ k: 'proposed', t: 'Edit the proposed diet', tail: shownId(prop), d: 'Reopen the current proposal with its items, dates and notes.', note: 'Saving replaces ' + shownId(prop) + ' on this request.' });
      o.push({ k: 'base', t: 'New base diet', tail: base ? 'Edit ' + shownId(base) : '', d: 'The always-on default for the whole species.', note: baseNote, edit: base ? base.id : null, species: true });
      if (sc === 'species') o.push({ k: 'year-round', t: 'Year-round', tail: base ? 'Edit ' + shownId(base) : '', d: 'An always-on default for this species.', note: 'At species level the year-round diet is the base diet. ' + (base ? 'You’ll propose changes to ' + shownId(base) + '.' : 'This will create the species-wide base.'), edit: base ? base.id : null, species: true });
      else o.push({ k: 'year-round', t: 'Year-round', tail: here ? 'Edit ' + shownId(here) : '', d: 'An always-on default for ' + scName + ', on top of the base diet.', note: here ? 'A year-round diet already exists here. You’ll propose changes to ' + shownId(here) + '.' : !base ? noBase : '', edit: here ? here.id : null });
      o.push({ k: 'seasonal', t: 'Seasonal', d: 'A day and month window that repeats every year.', note: base ? '' : noBase });
      o.push({ k: 'time-bound', t: 'Time-bound', d: 'Applies once between a from and a to date.', note: base ? '' : noBase });
      var sug = rec.season ? 'seasonal' : rec.type === 'temporary' ? 'time-bound' : rec.type === 'base' ? (sc === 'species' ? 'base' : 'year-round') : sc === 'species' ? 'base' : 'year-round';
      o.forEach(function (x) { x.sug = x.k === sug; });
      return o;
    }
    function drawCfg() {
      var rec = RQ.get(CFG.id), o = cfgOptions(rec);
      if (!CFG.pick || !o.filter(function (x) { return x.k === CFG.pick; }).length) { var first = o.filter(function (x) { return x.sug; })[0] || o[0]; CFG.pick = first.k; }
      var ICN = { proposed: 'pencil', base: 'paw', 'year-round': 'time', seasonal: 'star', 'time-bound': 'calendar' };
      sheet('<div class="sheet__h"><div><h2 class="t-major-title" id="rsT">How should this request be configured?</h2><p class="t-body-regular" style="color:var(--ink)">' + esc(rec.id + ' · ' + rec.sp + ' · ' + (rec.scopeText || 'Whole species')) + '</p></div><button type="button" class="iconbtn" data-rsclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
        '<div class="cfgs" role="radiogroup" aria-label="Configuration type">' + o.map(function (x) {
          return '<button type="button" class="cfg' + (x.k === 'proposed' ? ' cur' : '') + '" role="radio" data-cfgk="' + x.k + '" aria-checked="' + (CFG.pick === x.k) + '"><span class="oi">' + ic(ICN[x.k], 22) + '</span><span class="grow"><b class="t-minor-title">' + x.t + (x.tail ? '<em class="cfg__tail"> · ' + esc(x.tail) + '</em>' : '') + (x.sug ? ' <span class="tag green">Suggested from request</span>' : '') + '</b><span class="t-body-regular">' + esc(x.d) + '</span>' +
            (x.note ? '<small class="note t-body-regular">' + ic('info', 16) + '<span>' + esc(x.note) + '</span></small>' : '') + '</span></button>';
        }).join('') + '</div>' +
        '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">The result is a proposed diet linked to ' + esc(rec.id) + '. It is not active and goes to Kitchen when you send it.</p>' +
        '<div class="sheet__f end"><button type="button" class="btn sec" data-rsclose>Cancel</button><button type="button" class="btn teal" data-cfggo>Continue to configure</button></div>');
    }
    document.getElementById('rqsheet').addEventListener('click', function (e) {
      if (!CFG) return; var t;
      if ((t = e.target.closest('[data-cfgk]'))) { CFG.pick = t.getAttribute('data-cfgk'); drawCfg(); return; }
      if (e.target.closest('[data-cfggo]') && CFG.pick) { var id = CFG.id, k = CFG.pick; CFG = null; closeSheet3(); startConfig(RQ.get(id), k); return; }
      if (e.target.closest('[data-rsclose]') || e.target === this) CFG = null;
    }, true);
    function startConfig(rec, k) {
      var x = cfgOptions(rec).filter(function (y) { return y.k === k; })[0] || {}, prop = k === 'proposed' ? PLANS[rec.proposedId] : null;
      st.tsn = rec.tsn; resetScope();
      if (prop) { if (prop.scope !== 'species') { st.scope = prop.scope; st.ref = prop.ref; } }
      else if (!x.species && rec.scope !== 'species') { st.scope = rec.scope; st.ref = rec.scopeRef; }
      if (LAND.matches) { drawList(); drawDetail(); } else openPanel();
      if (prop) { var pk = prop.kind === 'seasonal' ? 'seasonal' : prop.kind === 'time-bound' ? 'time-bound' : 'year-round';
        openWizard(pk, pk === 'year-round' && prop.scope === 'species', false, rec, rec.cfgKind || pk, { source: prop.id, editOf: prop.editOf || null, reopen: true }); return; }
      openWizard(x.species ? 'year-round' : k, !!x.species, false, rec, k, { source: x.edit || null, editOf: x.edit || null });
    }
    HOOKS.configure = function (rec) {
      if (!BY[rec.tsn]) { toast('This request has no species record here to configure against.'); return; }
      CFG = { id: rec.id, pick: null }; drawCfg();
    };
'''
