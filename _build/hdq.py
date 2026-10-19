# hdq.py: exec'd by home2.py after roles.py. Dietician view of the Diet Request tab:
# To configure / Configured by me / All, contextual sub-chips, Filters sheet, Sort control.
# Shared bucket helpers (RQ.hd*) are also used by the Species "Requests for this species" card.

HDQ_CSS = '''    /* =========================================================
       14. HEAD DIETICIAN REQUEST QUEUE (To configure / Configured by me / All)
       ========================================================= */
    .hdq .segwrap { margin-top: 0; }
    .hdq .seg3 button .n { font-variant-numeric: tabular-nums; margin-left: 4px; opacity: .75; }
    .hdq__bar { display: flex; align-items: center; gap: 8px; padding: 12px 0 0; }
    .hdq__chips { display: flex; gap: 8px; flex: 1; min-width: 0; overflow-x: auto; scrollbar-width: none; padding: 2px 0; }
    .hdq__chips::-webkit-scrollbar { display: none; }
    .hdq__chips .spchip { flex: none; height: 44px; }
    .hdq__chips .spchip .n { font-variant-numeric: tabular-nums; opacity: .8; }
    .hdq__tools { display: flex; gap: 8px; flex: none; }
    .hdq__tools .chip { height: 44px; padding: 0 14px; }
    .hdq__tools .chip b { font-weight: 600; color: var(--head); }
    .hdq__tools .chip .dot { min-width: 20px; height: 20px; border-radius: 10px; padding: 0 6px; background: var(--md3-on-primary-container); color: var(--white); font-size: 12px; display: inline-grid; place-items: center; }
    .hdq__active { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; padding: 10px 0 0; }
    .hdq__active .fchip { display: inline-flex; align-items: center; gap: 4px; min-height: 36px; padding: 0 4px 0 12px; border-radius: 18px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .hdq__active .fchip button { width: 44px; height: 44px; margin: -4px -4px -4px 0; display: grid; place-items: center; border-radius: 22px; color: inherit; }
    .hdq__active .linkbtn { min-height: 44px; padding: 0 8px; }
    .hdq .list-bar { margin-top: 12px; }
    .hdq .list-bar small { color: var(--md3-neutral-secondary); font-weight: 400; }
    article.hdcard { cursor: pointer; }
    article.hdcard:active { transform: scale(.995); }
    .hdx__prop { display: flex; align-items: center; gap: 8px; color: var(--head); }
    .hdx__prop svg { color: var(--md3-on-primary-container); flex: none; }
    .hdx__prop .tag { margin-left: auto; }
    .kind { display: inline-flex; align-items: center; gap: 6px; justify-self: start; min-height: 28px; padding: 0 10px; border-radius: 6px; }
    .kind.ok { background: var(--md3-on-background); color: var(--md3-on-surface); }
    .kind.bad { background: var(--error-a5); color: #B3213F; }
    .hdx__foot .btn + .btn { margin-left: -4px; }
    .kbulk { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; justify-content: space-between; margin-top: 12px; padding: 12px 16px; border-radius: var(--radius); background: var(--white); color: var(--ink); }
    .kbulk .btn { flex: none; height: 44px; padding: 0 18px; }
    .kblist { list-style: none; margin: 0; padding: 0; display: grid; gap: 8px; max-height: 50dvh; overflow-y: auto; }
    .kblist li { display: flex; align-items: center; gap: 12px; min-height: 56px; padding: 6px 12px 6px 0; border-radius: 8px; background: var(--md3-background); overflow: hidden; }
    .kblist .ribbon { margin: 0; min-width: 44px; height: 32px; font-size: 15px; padding: 0 8px 0 16px; }
    .kblist .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .kblist small { color: var(--ink); }
    .hdx__foot { display: flex; align-items: center; gap: 12px; margin: 0 2px 2px; padding: 8px 8px 8px 14px; min-height: 60px; border-radius: 0 0 6px 6px; }
    .hdx__foot .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .hdx__foot .grow b { display: flex; align-items: center; gap: 8px; }
    .hdx__foot .grow small { color: var(--md3-on-surface-variant); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .hdx__foot.review { background: var(--moderate-a10); color: var(--md3-on-tertiary-container); }
    .hdx__foot.config { background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .hdx__foot.back { background: var(--error-a5); color: var(--md3-error); }
    .hdx__foot.wait { background: var(--neutral05); color: var(--md3-on-surface-variant); }
    .hdx__foot .btn { flex: none; height: 44px; min-width: 112px; padding: 0 16px; font-size: 15px; }
    .fsheet { display: grid; gap: 16px; }
    .fsheet h4 { color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; margin-bottom: 8px; }
    .fsheet .opts { display: flex; flex-wrap: wrap; gap: 8px; }
    .fsheet .opts .spchip { height: 44px; }
    .fsheet select { width: 100%; height: 48px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--ink); font: inherit; }
    .fsheet .g2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .sortopts { display: grid; gap: 8px; }
    .sortopts button { display: flex; align-items: center; justify-content: space-between; min-height: 52px; padding: 0 16px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); text-align: left; }
    .sortopts button[aria-checked="true"] { border-color: var(--md3-on-primary-container); background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); font-weight: 600; }
    @media (orientation: portrait) { .hdq__tools .chip .lbl { display: none; } }
'''

HDQ_JS = r'''  /* ---------------- Dietician queue buckets (shared with the Species requests card) ---------------- */
  RQ.TODO = ['requested', 'under_review', 'configuring', 'adjustment'];
  RQ.DOWN = ['kitchen_review', 'delayed', 'ready', 'applied', 'with_kitchens', 'scheduled', 'live'];
  RQ.hdBucket = function (r) { if (RQ.TODO.indexOf(r.status) !== -1) return 'todo'; if (RQ.DOWN.indexOf(r.status) !== -1 && r.configuredBy && r.configuredBy.id === RQ.viewer.id) return 'mine'; return null; };
  RQ.hdSub = function (r) { return { requested: 'review', under_review: 'review', configuring: 'configuring', adjustment: 'sentback', kitchen_review: 'kitchen', delayed: 'delayed', ready: 'done', applied: 'done', with_kitchens: RQ.lateBy && RQ.lateBy(r) ? 'delayed' : 'kitchen', scheduled: 'done', live: 'done' }[r.status] || 'other'; };
  RQ.SUBL = { review: 'Needs review', configuring: 'Configuring', sentback: 'Sent back', kitchen: 'With kitchen', delayed: 'Delayed', done: 'Scheduled / Live' };
  /* next step for To configure: [tone, label, detail, button, action] */
  RQ.hdNext = function (r) {
    if (r.status === 'requested' || r.status === 'under_review') {
      if (r.clarify && !r.clarify.answer) return ['wait', 'Answer pending: waiting on requester', 'You asked: ' + r.clarify.question, 'Open', 'open'];
      if (r.clarify && r.clarify.answer) return ['review', 'Reply received: review and accept', r.clarify.answer, 'Review', 'open'];
      return ['review', 'Review and accept', 'Raised ' + RQ.ago(r.events[0].at), 'Review', 'open'];
    }
    if (r.status === 'configuring') return r.proposedId ? ['config', 'Proposal saved: certify and send to kitchens', RQ.propText(r), 'Open', 'open'] : ['config', 'Configure', 'Accepted' + (r.acceptedBy ? ' by ' + r.acceptedBy : '') + '. No proposed diet yet.', 'Configure', 'configure'];
    if (r.status === 'adjustment') return ['back', 'Adjust and resend', 'Kitchen: ' + (r.adjustReason || 'asked for an adjustment'), 'Adjust', 'configure'];
    return null;
  };
  RQ.propText = function (r) {
    if (r.proposedId) return String(r.cfgLabel || 'Proposed diet').replace(/ diet$/, '') + ' D-' + r.proposedId + (r.editOfLabel ? ' · Change to ' + r.editOfLabel : '');
    return r.cfgText || '';
  };
  RQ.downLabel = function (r) { return r.status === 'kitchen_review' ? 'With Kitchen' : r.status === 'delayed' ? (r.delayUntil ? 'Delayed to ' + RQ.fmt(r.delayUntil) : 'Delayed') : r.status === 'ready' ? 'Sent to prep' : r.status === 'applied' ? 'Completed · Applied' : r.label; };
  RQ.rType = function (r) { if (r.type) return r.type; var w = String(r.where || ''); return /^Animal/.test(w) ? 'animal' : /^Species/.test(w) ? 'base' : 'site'; };

  /* ---------------- Diet Request tab, Dietician view ---------------- */
  /* Kitchen Head / Operator view of the same queue (V2 diet/requests.js kitchenMode): kitchen-stage requests only */
  RQ.KST = ['configuring', 'kitchen_review', 'delayed', 'adjustment', 'ready', 'applied'];
  RQ.kNext = function (r) {
    if (r.status === 'kitchen_review') return ['review', 'Check stock and accept', 'Sent to Kitchen ' + RQ.ago((r.events.filter(function (e) { return e.kind === 'sent-kitchen'; }).pop() || r.events[0]).at), 'Review', 'open'];
    if (r.status === 'delayed') return ['review', 'Delayed to ' + RQ.fmt(r.delayUntil) + ': accept when ready', r.delayReason || '', 'Review', 'open'];
    if (r.status === 'adjustment') return ['wait', 'Sent back: waiting on the dietician', 'You asked: ' + (r.adjustReason || 'an adjustment'), 'Open', 'open'];
    if (r.status === 'configuring') return ['wait', 'Coming up: the dietician is configuring', 'Not sent to Kitchen yet', 'Open', 'open'];
    return null;
  };
  RQ.kDate = function (r) { return r.season ? 'Every year ' + r.season.from.split('-').reverse().join('-') + ' to ' + r.season.to.split('-').reverse().join('-') : r.start ? 'Starts ' + RQ.fmt(r.start) + (r.end ? ', ends ' + RQ.fmt(r.end) : '') : ''; };
  function HdQueue(root, kitchen) {
    var K = !!kitchen;
    var PRIO = { high: ['!!!', 'High priority', 0], medium: ['!!', 'Medium priority', 1], low: ['!', 'Low priority', 2] };
    var SEGS = K ? [['check', 'To do'], ['ready', 'Ready'], ['all', 'All']] : [['todo', 'To configure'], ['mine', 'Configured by me'], ['all', 'All']];
    var SUBS = K ? { check: [['all', 'All'], ['kpending', 'To prepare'], ['kdelayed', 'Delayed']], ready: [], all: [['all', 'All']] } : { todo: [['all', 'All'], ['review', 'Needs review'], ['configuring', 'Configuring'], ['sentback', 'Sent back']],
      mine: [['all', 'All'], ['kitchen', 'With kitchen'], ['delayed', 'Delayed'], ['done', 'Scheduled / Live']], all: [['open', 'Open'], ['closed', 'Closed']] };
    var SORTS = [['priority', 'Priority'], ['newest', 'Newest'], ['oldest', 'Oldest']];
    var st = { seg: K ? 'check' : 'todo', sub: K ? { check: 'all', ready: 'all', all: 'all' } : { todo: 'all', mine: 'all', all: 'open' }, sort: 'priority', f: { status: [], prio: [], type: '', sp: '', by: '' } };
    var SHEET = null, draftF = null;
    (function () { var q = new URLSearchParams(location.search).get('kq'); if (!q) return; var p = q.split(':'); if (SUBS[p[0]]) { st.seg = p[0]; if (p[1] && SUBS[p[0]].some(function (c) { return c[0] === p[1]; })) st.sub[p[0]] = p[1]; } })();
    root.innerHTML = '<div class="hdq"><div class="segwrap"><div class="seg3" role="tablist" aria-label="' + (K ? 'Kitchen requests' : 'Requests for the dietician') + '" data-hseg></div></div>' +
      '<div class="hdq__bar"><div class="hdq__chips" role="group" aria-label="Narrow this view" data-hsub></div><div class="hdq__tools">' +
      '<button type="button" class="chip t-body-medium" data-hsort aria-haspopup="dialog"></button><button type="button" class="chip t-body-medium" data-hfilt aria-haspopup="dialog"></button></div></div>' +
      '<div class="hdq__active" data-hact hidden></div><div data-kbulkbar></div><div class="list-bar"><h2 class="t-minor-medium" data-hcount aria-live="polite"></h2></div><div class="rqcards" data-hlist></div></div>';
    var $ = function (s) { return root.querySelector(s); };
    var KSEG = { check: ['kitchen_review', 'delayed'], ready: ['ready'], all: RQ.KST }, KSUB = { kreview: 'kitchen_review', kdelayed: 'delayed', kadjust: 'adjustment', kcoming: 'configuring' };
    function inSeg(r, seg) { if (K) { var l = RQ.myLine(r); if (!l) return KSEG[seg].indexOf(r.status) !== -1; return seg === 'all' || (seg === 'ready' ? l.status === 'ready' : l.status !== 'ready'); } return seg === 'all' ? true : RQ.hdBucket(r) === seg; }
    function inSub(r, seg, sub) {
      if (K) { var l2 = RQ.myLine(r); if (!l2) return sub === 'all' || r.status === KSUB[sub]; return sub === 'all' || (sub === 'kdelayed' ? l2.status === 'delayed' : ['pending', 'accepted', 'processing'].indexOf(l2.status) !== -1); }
      if (seg === 'all') return sub === 'closed' ? (r.status === 'rejected' || r.status === 'cancelled') : !(r.status === 'rejected' || r.status === 'cancelled');
      return sub === 'all' || RQ.hdSub(r) === sub;
    }
    function readyList() { return RQ.visible().filter(function (r) { return (r.status === 'kitchen_review' || r.status === 'delayed') && r.proposedId && KS.feas(r).canPrep; }).sort(cmp); }
    function bulkSheet() { SHEET = 'bulk'; var rd = readyList();
      sheet('<div class="sheet__h"><div><h2 class="t-major-title" id="rsT">Send ' + plural(rd.length, 'request') + ' to Prep?</h2><p class="t-body-regular" style="color:var(--ink)">Every line can be prepped from stock. Alternatives are used where the main item is short.</p></div><button type="button" class="iconbtn" data-rsclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
        '<ul class="kblist">' + rd.map(function (r) { var fz = KS.feas(r); return '<li><span class="ribbon ' + r.prio + '" aria-label="' + RQ.PRI[r.prio][1] + ' priority">' + RQ.PRI[r.prio][0] + '</span><span class="grow"><b class="t-body-title">' + esc(r.id + ' · ' + r.title) + '</b><small class="t-body-regular">' + esc(r.sp + ', ' + (r.scopeText || 'Whole species')) + (fz.alt.length ? ' · ' + esc(fz.alt.map(function (l) { return l.chosen.name + ' for ' + l.name; }).join(', ')) : ' · all main items') + '</small></span></li>'; }).join('') + '</ul>' +
        '<div class="sheet__f end"><button type="button" class="btn sec" data-rsclose>Cancel</button><button type="button" class="btn teal" data-kbulkok>Send ' + rd.length + ' to Prep</button></div>'); }
    function inF(r) { var f = st.f;
      if (f.status.length && f.status.indexOf(r.status) === -1) return false;
      if (f.prio.length && f.prio.indexOf(r.prio) === -1) return false;
      if (f.type && RQ.rType(r) !== f.type) return false;
      if (f.sp && r.sp !== f.sp) return false;
      if (f.by && r.by.name !== f.by) return false; return true; }
    function nF() { var f = st.f; return f.status.length + f.prio.length + (f.type ? 1 : 0) + (f.sp ? 1 : 0) + (f.by ? 1 : 0); }
    function cmp(a, b) {
      if (st.sort === 'newest') return b.iso.localeCompare(a.iso) || b.id.localeCompare(a.id);
      if (st.sort === 'oldest') return a.iso.localeCompare(b.iso) || a.id.localeCompare(b.id);
      return (PRIO[a.prio][2] - PRIO[b.prio][2]) || a.iso.localeCompare(b.iso);
    }
    function top(r) { var p = PRIO[r.prio];
      return '<div class="hd-top"><span class="grow"><span class="hd-id t-minor-title">' + r.id + RQ.lateTag(r, K ? RQ.viewer.kitchen : null) + '</span><span class="hd-cat t-body-medium">' + esc(r.sp) + '</span><span class="hd-where t-body-regular">' + esc(r.where) + '</span></span>' +
        '<span class="ribbon ' + r.prio + '" title="' + p[1] + '" aria-label="' + p[1] + '">' + p[0] + '</span></div>'; }
    function body(r, extra) { return '<div class="hd-body"><span class="hd-title t-medium-medium">' + esc(r.title) + '</span><span class="hd-text t-body-regular">' + esc(r.text) + '</span>' + (extra || '') +
      '<span class="hd-by t-body-regular"><b class="t-body-title">' + esc(r.by.name + (RQ.isMine(r) ? ' (You)' : '')) + '</b> • ' + r.date + '</span></div>'; }
    function propLine(r) { var t = RQ.propText(r); return t ? '<span class="hdx__prop t-body-title">' + ic('book', 18) + esc(t) + '</span>' : ''; }
    function kcard(r) {
      var ml = RQ.myLine(r);
      if (ml) { var S = RQ.KLS[ml.status], lab0 = esc(r.id + ': ' + r.title);
        var ex = '<span class="hdx__prop t-body-title">' + ic('book', 18) + esc(RQ.kname(ml.k) + ': ' + ml.items.join(', ')) + '</span>' +
          '<span class="hdx__prop t-body-regular">' + ic('calendar', 18) + esc('Diet starts ' + RQ.fmt(RQ.effStart(r)) + (r.end ? ', ends ' + RQ.fmt(r.end) : '')) + '</span>';
        var nx = { pending: 'Accept your items', accepted: 'Start processing', processing: 'Mark ready when done', delayed: 'Delayed: ready from ' + RQ.fmt(ml.readyFrom), ready: 'Ready' }[ml.status];
        return '<article tabindex="0" class="hdcard hdx" data-hopen="' + r.id + '" aria-label="' + lab0 + '">' + top(r) + body(r, ex) +
          '<div class="hdx__foot ' + (ml.status === 'ready' ? 'wait' : 'review') + '"><span class="grow"><b class="t-minor-medium">' + ic(S[2], 20) + esc(nx) + '</b><small class="t-body-regular">' + esc(ml.status === 'delayed' ? (ml.reason || '') : S[0]) + '</small></span>' +
          '<button type="button" class="btn ' + (ml.status === 'ready' ? 'sec' : 'teal') + '" data-hgo="' + r.id + '" data-hdo="open">Open</button></div></article>'; }
      var n = RQ.kNext(r), lab = esc(r.id + ': ' + r.title), dl = RQ.kDate(r), live = (r.status === 'kitchen_review' || r.status === 'delayed') && r.proposedId, fz = live ? KS.feas(r) : null;
      var extra = propLine(r) + (dl ? '<span class="hdx__prop t-body-regular">' + ic('calendar', 18) + esc(dl) + '</span>' : '') +
        (fz ? (fz.canPrep ? '<span class="kind ok t-body-medium">' + ic('just-tick-mark', 16) + 'Can prep' + (fz.alt.length ? ' · ' + fz.alt.length + ' using ' + (fz.alt.length === 1 ? 'an alternative' : 'alternatives') : '') + '</span>'
          : '<span class="kind bad t-body-medium">' + ic('alert', 16) + 'Needs readjustment: ' + esc(fz.bad.map(function (l) { return l.name; }).join(', ')) + '</span>') : '');
      if (n) return '<article tabindex="0" class="hdcard hdx" data-hopen="' + r.id + '" aria-label="' + lab + '">' + top(r) + body(r, extra) +
        '<div class="hdx__foot ' + n[0] + '"><span class="grow"><b class="t-minor-medium">' + ic(n[0] === 'wait' ? 'timer' : 'time', 20) + esc(n[1]) + '</b><small class="t-body-regular">' + esc(n[2]) + '</small></span>' +
        (fz && fz.canPrep ? '<button type="button" class="btn sec" data-hgo="' + r.id + '" data-hdo="open">Review</button><button type="button" class="btn teal" data-kquick="' + r.id + '">Send to Prep</button>' : '<button type="button" class="btn ' + (n[0] === 'wait' ? 'sec' : 'teal') + '" data-hgo="' + r.id + '" data-hdo="open">' + esc(n[3]) + '</button>') + '</div></article>';
      return '<article tabindex="0" class="hdcard hdx" data-hopen="' + r.id + '" aria-label="' + lab + '">' + top(r) + body(r, extra) +
        '<div class="hd-band ' + r.tone + ' t-minor-medium">' + ic(r.icon, 20) + esc(RQ.downLabel(r)) + (r.readyAt ? '<small class="t-body-regular" style="margin-left:auto;color:var(--md3-on-surface-variant)">Accepted ' + esc(RQ.ago(r.readyAt)) + '</small>' : '') + '</div></article>';
    }
    function card(r) {
      if (K) return kcard(r);
      var b = RQ.hdBucket(r), lab = esc(r.id + ': ' + r.title);
      if (b === 'todo') { var n = RQ.hdNext(r);
        return '<article tabindex="0" class="hdcard hdx" data-hopen="' + r.id + '" aria-label="' + lab + '">' + top(r) + body(r, r.proposedId || r.status === 'adjustment' ? propLine(r) : '') +
          '<div class="hdx__foot ' + n[0] + '"><span class="grow"><b class="t-minor-medium">' + ic(n[0] === 'back' ? 'close' : n[0] === 'config' ? 'pencil' : n[0] === 'wait' ? 'timer' : 'time', 20) + esc(n[1]) + '</b><small class="t-body-regular">' + esc(n[2]) + '</small></span>' +
          '<button type="button" class="btn ' + (n[4] === 'open' && n[0] === 'wait' ? 'sec' : 'teal') + '" data-hgo="' + r.id + '" data-hdo="' + n[4] + '">' + esc(n[3]) + '</button></div></article>';
      }
      var mine = r.configuredBy && r.configuredBy.id === RQ.viewer.id, cfg = r.configuredBy ? (mine ? 'Configured by you' : 'Configured by ' + r.configuredBy.name) : '';
      if (RQ.DOWN.indexOf(r.status) !== -1) {
        return '<article tabindex="0" class="hdcard hdx" data-hopen="' + r.id + '" aria-label="' + lab + '">' + top(r) + body(r, propLine(r)) +
          '<div class="hd-band ' + r.tone + ' t-minor-medium">' + ic(r.icon, 20) + esc(RQ.downLabel(r)) + (cfg ? '<small class="t-body-regular" style="margin-left:auto;color:var(--md3-on-surface-variant)">' + esc(cfg) + '</small>' : '') + '</div></article>';
      }
      return '<article tabindex="0" class="hdcard hdx' + (r.status === 'cancelled' ? ' struck' : '') + '" data-hopen="' + r.id + '" aria-label="' + lab + '">' + top(r) + body(r) +
        '<div class="hd-band ' + r.tone + ' t-minor-medium">' + ic(r.icon, 20) + esc(r.label) + '</div></article>';
    }
    function fLabel(k, v) { if (k === 'status') return (RQ.ST[v] || [v])[0]; if (k === 'prio') return RQ.PRI[v][1] + ' priority'; if (k === 'type') return (RQ.TYPES.filter(function (t) { return t[0] === v; })[0] || [0, v])[1]; if (k === 'by') return 'By ' + v; return v; }
    function draw() {
      var all = RQ.visible(), segN = {}; SEGS.forEach(function (s) { segN[s[0]] = all.filter(function (r) { return inSeg(r, s[0]) && (s[0] !== 'all' || true); }).length; });
      $('[data-hseg]').innerHTML = SEGS.map(function (s) { return '<button type="button" role="tab" class="t-body-medium" data-hs="' + s[0] + '" aria-selected="' + (st.seg === s[0]) + '">' + s[1] + '<span class="n">' + segN[s[0]] + '</span></button>'; }).join('');
      var base = all.filter(function (r) { return inSeg(r, st.seg) && inF(r); }), sub = st.sub[st.seg];
      $('[data-hsub]').innerHTML = SUBS[st.seg].map(function (c) { return '<button type="button" class="spchip t-body-medium" data-hsb="' + c[0] + '" aria-pressed="' + (sub === c[0]) + '">' + c[1] + ' <span class="n">' + base.filter(function (r) { return inSub(r, st.seg, c[0]); }).length + '</span></button>'; }).join('');
      var sl = SORTS.filter(function (x) { return x[0] === st.sort; })[0][1], n = nF();
      $('[data-hsort]').innerHTML = ic('sort', 18) + '<span>Sort: <b>' + sl + '</b></span>'; $('[data-hsort]').setAttribute('aria-label', 'Sort: ' + sl + '. Change sort order');
      $('[data-hfilt]').innerHTML = ic('filter-2', 18) + '<span class="lbl">Filters</span>' + (n ? '<span class="dot">' + n + '</span>' : ''); $('[data-hfilt]').setAttribute('aria-label', 'Filters' + (n ? ', ' + n + ' active' : ''));
      var act = [];
      ['status', 'prio'].forEach(function (k) { st.f[k].forEach(function (v) { act.push([k, v]); }); }); ['type', 'sp', 'by'].forEach(function (k) { if (st.f[k]) act.push([k, st.f[k]]); });
      var A = $('[data-hact]'); A.hidden = !act.length;
      A.innerHTML = act.map(function (a) { return '<span class="fchip t-body-medium">' + esc(fLabel(a[0], a[1])) + '<button type="button" data-hrm="' + a[0] + ':' + esc(a[1]) + '" aria-label="Remove filter ' + esc(fLabel(a[0], a[1])) + '">' + ic('close', 16) + '</button></span>'; }).join('') + (act.length ? '<button type="button" class="linkbtn t-body-medium" data-hclear>Clear</button>' : '');
      var list = base.filter(function (r) { return inSub(r, st.seg, sub); }).sort(cmp);
      var BB = $('[data-kbulkbar]'); if (BB && !K) { var rd = K && st.seg === 'check' ? readyList() : [];
        var tot = all.filter(function (r) { return r.status === 'kitchen_review' || r.status === 'delayed'; }).length; BB.innerHTML = K && st.seg === 'check' ? '<div class="kbulk"><span class="t-body-regular">' + (rd.length === tot ? '<b class="t-body-title">' + (tot === 1 ? 'The request' : 'All ' + tot + ' requests') + '</b> can be prepped now.' : '<b class="t-body-title">' + rd.length + ' of ' + tot + '</b> requests can be prepped now. The rest need a readjustment.') + '</span><button type="button" class="btn teal" data-kbulk' + (rd.length ? '' : ' disabled') + '>' + ic('just-tick-mark', 18) + 'Send all ready to prep (' + rd.length + ')</button></div>' : ''; }
      var head = (K ? { check: 'To do', ready: 'Ready', all: 'Your kitchen requests' } : { todo: 'To configure', mine: 'Configured by me', all: 'All requests' })[st.seg];
      $('[data-hcount]').innerHTML = esc(head) + ' (' + list.length + ')' + (st.seg !== 'all' && sub !== 'all' ? ' <small class="t-body-regular">· ' + esc(SUBS[st.seg].filter(function (c) { return c[0] === sub; })[0][1]) + '</small>' : '');
      var emptyTxt = K ? (st.seg === 'check' ? 'Nothing to do. Diets that dieticians send to your kitchen appear here.' : st.seg === 'ready' ? 'Requests you mark ready appear here.' : 'Nothing matches this view.') : st.seg === 'todo' ? 'Nothing waiting on you. New requests and anything Kitchen sends back appear here.' : st.seg === 'mine' ? 'Requests you configure and send to Kitchen appear here.' : 'Nothing matches this view.';
      $('[data-hlist]').innerHTML = list.length ? list.map(card).join('') : '<div class="empty" style="grid-column:1/-1"><span class="ei">' + ic('reason-or-list', 24) + '</span><b class="t-minor-title">' + (n ? 'No requests match these filters' : 'All clear') + '</b><span class="t-body-regular">' + esc(n ? 'Remove a filter or clear them all.' : emptyTxt) + '</span></div>';
    }
    /* ---------- sheets (Sort, Filters) on the shared #rqsheet ---------- */
    function sortSheet() { SHEET = 'sort';
      sheet('<div class="sheet__h"><div><h2 class="t-major-title" id="rsT">Sort requests</h2></div><button type="button" class="iconbtn" data-rsclose aria-label="Close">' + ic('close', 24) + '</button></div><div class="sortopts" role="radiogroup" aria-label="Sort">' +
        SORTS.map(function (s) { return '<button type="button" role="radio" class="t-body-medium" data-hso="' + s[0] + '" aria-checked="' + (st.sort === s[0]) + '"><span>' + s[1] + (s[0] === 'priority' ? ' <small style="font-weight:400;color:var(--md3-neutral-secondary)">then oldest first</small>' : '') + '</span>' + (st.sort === s[0] ? ic('just-tick-mark', 20) : '') + '</button>'; }).join('') + '</div>'); }
    function opts(list, cur, ph) { return '<option value="">' + esc(ph) + '</option>' + list.map(function (v) { return '<option value="' + esc(v) + '"' + (v === cur ? ' selected' : '') + '>' + esc(v) + '</option>'; }).join(''); }
    function filtSheet() { SHEET = 'filt'; var f = draftF, all = RQ.visible();
      var sps = all.map(function (r) { return r.sp; }).filter(function (v, i, a) { return a.indexOf(v) === i; }).sort(), bys = all.map(function (r) { return r.by.name; }).filter(function (v, i, a) { return a.indexOf(v) === i; }).sort();
      var cnt = all.filter(function (r) { return inSeg(r, st.seg) && (function () { var k = st.f; st.f = f; var ok = inF(r); st.f = k; return ok; })(); }).length;
      sheet('<div class="sheet__h"><div><h2 class="t-major-title" id="rsT">Filters</h2><p class="t-body-regular" style="color:var(--ink)">Applies to ' + esc({ todo: 'To configure', mine: 'Configured by me', all: 'All' }[st.seg]) + '</p></div><button type="button" class="iconbtn" data-rsclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
        '<div class="fsheet"><div><h4>Status</h4><div class="opts">' + Object.keys(RQ.ST).map(function (k) { return '<button type="button" class="spchip t-body-medium" data-hfs="status:' + k + '" aria-pressed="' + (f.status.indexOf(k) !== -1) + '">' + esc(RQ.ST[k][0]) + '</button>'; }).join('') + '</div></div>' +
        '<div><h4>Priority</h4><div class="opts">' + ['high', 'medium', 'low'].map(function (k) { return '<button type="button" class="spchip t-body-medium" data-hfs="prio:' + k + '" aria-pressed="' + (f.prio.indexOf(k) !== -1) + '">' + RQ.PRI[k][0] + ' ' + RQ.PRI[k][1] + '</button>'; }).join('') + '</div></div>' +
        '<div><h4>Type</h4><div class="opts">' + RQ.TYPES.map(function (t) { return '<button type="button" class="spchip t-body-medium" data-hft="' + t[0] + '" aria-pressed="' + (f.type === t[0]) + '">' + esc(t[1]) + '</button>'; }).join('') + '</div></div>' +
        '<div class="g2"><label><h4>Species</h4><select data-hfsel="sp" aria-label="Species">' + opts(sps, f.sp, 'Any species') + '</select></label><label><h4>Requester</h4><select data-hfsel="by" aria-label="Requester">' + opts(bys, f.by, 'Anyone') + '</select></label></div></div>' +
        '<div class="sheet__f end"><button type="button" class="btn sec" data-hfreset>Reset</button><button type="button" class="btn teal" data-hfok>Show ' + cnt + ' request' + (cnt === 1 ? '' : 's') + '</button></div>'); }
    var RSel = document.getElementById('rqsheet');
    RSel.addEventListener('click', function (e) {
      if (!SHEET) return; var t;
      if (e.target === RSel || e.target.closest('[data-rsclose]')) { SHEET = null; return; }
      if ((t = e.target.closest('[data-hso]'))) { st.sort = t.getAttribute('data-hso'); SHEET = null; closeSheet3(); draw(); e.stopPropagation(); return; }
      if ((t = e.target.closest('[data-hfs]'))) { var kv = t.getAttribute('data-hfs').split(':'), arr = draftF[kv[0]], i = arr.indexOf(kv[1]); if (i === -1) arr.push(kv[1]); else arr.splice(i, 1); filtSheet(); e.stopPropagation(); return; }
      if ((t = e.target.closest('[data-hft]'))) { var v = t.getAttribute('data-hft'); draftF.type = draftF.type === v ? '' : v; filtSheet(); e.stopPropagation(); return; }
      if (e.target.closest('[data-hfreset]')) { draftF = { status: [], prio: [], type: '', sp: '', by: '' }; filtSheet(); e.stopPropagation(); return; }
      if (e.target.closest('[data-kbulkok]')) { var rd = readyList(); rd.forEach(function (r) { ACT.prep(r, {}); }); SHEET = null; closeSheet3(); RQ.changed(); toast(plural(rd.length, 'request') + ' sent to prep.'); e.stopPropagation(); return; }
      if (e.target.closest('[data-hfok]')) { st.f = draftF; draftF = null; SHEET = null; closeSheet3(); draw(); e.stopPropagation(); return; }
    }, true);
    RSel.addEventListener('change', function (e) { if (SHEET === 'filt' && e.target.matches('[data-hfsel]')) { draftF[e.target.getAttribute('data-hfsel')] = e.target.value; filtSheet(); } });
    function go(id, act) {
      location.hash = '#request/' + id;
      if (act === 'open') return;
      setTimeout(function () { var r = RQ.get(id); if (!r) return;
        if (act === 'configure' && HOOKS.configure) HOOKS.configure(r);
        if (act === 'send') { var b = document.querySelector('#rqd [data-ract="send"]'); if (b) b.click(); } }, 120);
    }
    root.addEventListener('click', function (e) {
      var t;
      if ((t = e.target.closest('[data-hs]'))) { st.seg = t.getAttribute('data-hs'); draw(); return; }
      if ((t = e.target.closest('[data-hsb]'))) { st.sub[st.seg] = t.getAttribute('data-hsb'); draw(); return; }
      if (e.target.closest('[data-hsort]')) { sortSheet(); return; }
      if (e.target.closest('[data-hfilt]')) { draftF = JSON.parse(JSON.stringify(st.f)); filtSheet(); return; }
      if ((t = e.target.closest('[data-hrm]'))) { var kv = t.getAttribute('data-hrm').split(':'), k = kv[0], v = kv.slice(1).join(':'); if (Array.isArray(st.f[k])) st.f[k] = st.f[k].filter(function (x) { return x !== v; }); else st.f[k] = ''; draw(); return; }
      if (e.target.closest('[data-hclear]')) { st.f = { status: [], prio: [], type: '', sp: '', by: '' }; draw(); return; }
      if (e.target.closest('[data-kbulk]')) { bulkSheet(); return; }
      if ((t = e.target.closest('[data-kquick]'))) { var qr = RQ.get(t.getAttribute('data-kquick')); if (qr && KS.feas(qr).canPrep) { ACT.prep(qr, {}); RQ.changed(); toast(qr.id + ' sent to prep.'); } return; }
      if ((t = e.target.closest('[data-hgo]'))) { go(t.getAttribute('data-hgo'), t.getAttribute('data-hdo')); return; }
      if ((t = e.target.closest('[data-hopen]'))) { go(t.getAttribute('data-hopen'), 'open'); return; }
    });
    root.addEventListener('keydown', function (e) { var t = e.target.closest && e.target.closest('article[data-hopen]'); if (t && e.target === t && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); go(t.getAttribute('data-hopen'), 'open'); } });
    return { draw: draw, setSeg: function (s, sub) { st.seg = s; if (sub) st.sub[s] = sub; draw(); } };
  }
'''
