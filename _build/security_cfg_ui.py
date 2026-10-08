# security_cfg_ui.py: exec'd by security.py. Role views of the Security home:
#   Security Admin: Sites (same site transfers as Security, plus Manage sites: add / edit sites and in-charge) | Departments (configuration). Departments: department >
#     buildings > gates, add / edit gates, and pick the building + gates the Security tablet shows.
#   Security: Sites (site transfers, security_tx_ui.py) | Gates (the gates the admin configured, then a gate's vehicles).
# Config lives in localStorage 'antz.security.cfg' (seeded from security-data.json), shared by both roles.
CFG_CSS = """    /* =========================================================
       18. SECURITY CONFIG (admin) + GATES (security)
       ========================================================= */
    .cfgbar { display: flex; align-items: center; justify-content: space-between; gap: var(--sp-12); margin-top: var(--sp-16); }
    .cfgbar h2 { color: var(--head); }
    .cfgbar p { color: var(--ink); }
    .btn.add { flex: none; height: 44px; padding: 0 16px; font-size: 15px; background: var(--md3-on-primary-container); color: var(--white); }
    .btn.add svg { fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; }
    .cfglist { display: grid; gap: var(--sp-12); margin-top: var(--sp-16); }
    .cfgrow { display: flex; align-items: center; gap: var(--sp-16); min-height: 76px; padding: var(--sp-12) var(--sp-16) var(--sp-12) var(--sp-20); border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); width: 100%; text-align: left; }
    a.cfgrow:active { transform: scale(.995); }
    .cfgrow .gico { width: 48px; height: 48px; border-radius: 8px; display: grid; place-items: center; flex: none; background: var(--md3-surface-variant); color: var(--md3-neutral-secondary); }
    .cfgrow .gico svg { fill: none; stroke: currentColor; stroke-width: 1.6; }
    .cfgrow .grow { flex: 1; min-width: 0; display: grid; gap: 3px; }
    .cfgrow .grow b { color: var(--head); font-size: 18px; font-weight: 500; }
    .cfgrow .grow span { color: var(--ink); }
    .cfgrow .chev { color: var(--md3-on-primary-container); transform: rotate(180deg); }
    .cfgrow.off { opacity: .6; }
    .cfgedit { min-height: 44px; padding: 0 14px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); color: var(--md3-on-primary-container); font-weight: 500; flex: none; }
    .tag { display: inline-flex; align-items: center; gap: 4px; height: 24px; padding: 0 8px; border-radius: 6px; font-size: 12px; font-weight: 600; white-space: nowrap; }
    .tag.on { background: var(--md3-on-background); color: var(--md3-on-surface); }
    .tag.off { background: var(--neutral05); color: var(--md3-neutral-secondary); }
    .tag.tab { background: var(--add-primary-a10); color: #006F88; }
    .crumbs { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; margin-top: var(--sp-16); color: var(--ink); }
    .crumbs a { min-height: 44px; display: inline-flex; align-items: center; padding: 0 4px; color: var(--md3-on-primary-container); font-weight: 500; }
    .crumbs b { color: var(--head); font-weight: 600; }
    .tabcard { display: flex; align-items: center; gap: var(--sp-16); margin-top: var(--sp-16); padding: var(--sp-16) var(--sp-20); border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); }
    .tabcard .tag { flex: none; }
    .tabcard .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .tabcard b { color: var(--head); }
    .tabcard span { color: var(--ink); }
    .tabcard .btn { flex: none; height: 44px; padding: 0 16px; font-size: 15px; }
    .onsw { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 4px; color: var(--ink); font-size: 13px; flex: none; }
    .onsw input { width: 22px; height: 22px; accent-color: var(--md3-on-primary-container); }
    .gloc { display: flex; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: var(--sp-24); color: var(--head); font-size: 17px; }
    .gloc svg { fill: none; stroke: currentColor; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; color: var(--md3-on-primary-container); }
    .gloc i { width: 5px; height: 5px; border-radius: 50%; background: var(--head); }
    .glab { margin-top: var(--sp-20); color: var(--head); font-weight: 600; }
    .glist { display: grid; gap: var(--sp-16); margin-top: var(--sp-16); }
    @media (orientation: landscape) { .glist.two { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    .gvis { display: grid; gap: var(--sp-12); margin-top: var(--sp-12); }
    .gvis h3 { display: flex; align-items: center; gap: 8px; margin-top: var(--sp-12); color: var(--head); }
    .gvis h3 small { color: var(--md3-neutral-secondary); font-weight: 500; }
    .gv { display: flex; align-items: center; gap: var(--sp-16); padding: var(--sp-12) var(--sp-16); border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); }
    .gv .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .gv b { color: var(--head); font-weight: 600; }
    .gv span, .gv small { color: var(--ink); }
    .gv .when { text-align: right; color: var(--md3-on-primary-container); font-weight: 500; flex: none; }
    .fgrid { display: grid; gap: var(--sp-12); }
    .fgrid label { display: grid; gap: 6px; color: var(--ink); font-weight: 500; }
    .fgrid input[type=text], .fgrid select { height: 48px; padding: 0 12px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); background: var(--white); color: var(--head); font: inherit; }
    .fgrid input[type=text]:focus, .fgrid select:focus { border-color: var(--md3-on-primary-container); outline: none; }
    .pchips { display: flex; flex-wrap: wrap; gap: 8px; }
    .pchip { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 0 14px; border-radius: 22px; border: 1px solid var(--md3-outline-variant); color: var(--ink); cursor: pointer; }
    .pchip input { position: absolute; opacity: 0; pointer-events: none; }
    .pchip:has(input:checked) { background: var(--md3-on-primary-container); border-color: var(--md3-on-primary-container); color: var(--white); }
    .pchip:has(input:focus-visible) { outline: 2px solid var(--ring); outline-offset: 2px; }
    .fgrid label.onsw { display: inline-flex; justify-self: start; }
    .ferr { color: var(--md3-error); font-size: 13px; }
    .sheet .acts2 { display: flex; gap: var(--sp-12); }
    .btabs { margin: 0 calc(-1 * var(--sp-16)); border-top: 0; border-top: 1px solid var(--line); border-bottom: 1px solid var(--line); }
    /* building Dashboard: one filter bar, one summary panel, then what needs a look, by gate, latest movements */
    .dbar { display: flex; align-items: center; flex-wrap: wrap; gap: var(--sp-12) var(--sp-16); margin-top: var(--sp-16); }
    .dbar .dlab { color: var(--md3-neutral-secondary); }
    .dbar .ddate { margin-left: auto; gap: 8px; padding: 0 14px; }
    .dchips { padding: 0; }
    .calform { gap: var(--sp-20); }
    .cwin { color: var(--md3-neutral-secondary); }
    .fcols { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-12); }
    .fgrid input[type=date], .fgrid input[type=time] { height: 48px; padding: 0 12px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); background: var(--white); color: var(--head); font: inherit; }
    .dsum { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)) minmax(0, 1.6fr); margin-top: var(--sp-16); border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); }
    .dstat { display: grid; align-content: start; gap: 2px; padding: var(--sp-20); }
    .dstat + .dstat { border-left: 1px solid var(--md3-surface-variant); }
    .dstat span { color: var(--ink); }
    .dstat b { color: var(--head); font-size: 32px; line-height: 1.15; font-weight: 600; font-variant-numeric: tabular-nums; }
    .dstat small { color: var(--md3-neutral-secondary); font-size: 12px; }
    .dpaper { display: grid; align-content: start; gap: 10px; padding: var(--sp-20); border-left: 1px solid var(--md3-surface-variant); }
    .dpaper > span { color: var(--ink); }
    .dsplit { display: flex; height: 10px; border-radius: 5px; overflow: hidden; gap: 2px; }
    .dsplit i { display: block; min-width: 4px; }
    .dsplit .w { background: var(--md3-primary); } .dsplit .n { background: var(--md3-error); }
    .dleg { display: flex; flex-wrap: wrap; gap: 4px 20px; }
    .dleg p { display: flex; align-items: baseline; gap: 6px; color: var(--ink); }
    .dleg b { color: var(--head); font-size: 20px; font-weight: 600; font-variant-numeric: tabular-nums; }
    .dleg .n b { color: #B3213F; }
    @media (orientation: portrait) {
      .dsum { grid-template-columns: repeat(3, minmax(0, 1fr)); }
      .dpaper { grid-column: 1 / -1; border-left: 0; border-top: 1px solid var(--md3-surface-variant); }
    }
    .dcols { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); gap: var(--sp-16); margin-top: var(--sp-16); align-items: start; }
    @media (orientation: portrait) { .dcols { grid-template-columns: minmax(0, 1fr); } .dcols > div:last-child { order: -1; } }   /* portrait: what needs a look comes first */
    .dpan { border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); overflow: hidden; }
    .dpan + .dpan { margin-top: var(--sp-16); }
    .dpan__h { display: flex; align-items: baseline; gap: 8px; padding: var(--sp-16) var(--sp-20) var(--sp-8); color: var(--head); }
    .dpan__h small { color: var(--md3-neutral-secondary); font-weight: 500; }
    .dpan__h .cnt { display: inline-grid; place-items: center; min-width: 26px; height: 22px; padding: 0 8px; border-radius: 11px; background: var(--neutral05); color: var(--ink); font-size: 12px; font-weight: 600; }
    .dpan__h .cnt.bad { background: var(--error-a5); color: #B3213F; }
    .sdtab { width: 100%; border-collapse: collapse; }
    .sdtab th { text-align: left; font-size: 12px; font-weight: 500; color: var(--md3-neutral-secondary); padding: 4px 20px 8px; }
    .sdtab td { padding: 12px 20px; border-top: 1px solid var(--md3-surface-variant); color: var(--head); font-variant-numeric: tabular-nums; }
    .sdtab td small { display: block; color: var(--md3-neutral-secondary); font-size: 12px; }
    .sdtab .r { text-align: right; }
    .sdtab td.bad b { display: inline-grid; place-items: center; min-width: 28px; height: 24px; padding: 0 8px; border-radius: var(--radius); background: var(--error-a5); color: #B3213F; }
    .dlist { display: grid; }
    .drow { display: flex; align-items: flex-start; gap: var(--sp-12); padding: 12px 20px; border-top: 1px solid var(--md3-surface-variant); }
    .drow .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .drow b { color: var(--head); font-weight: 600; }
    .drow span, .drow small { color: var(--ink); }
    .drow small { font-size: 13px; }
    .drow .when { flex: none; color: var(--md3-neutral-secondary); font-size: 13px; text-align: right; font-variant-numeric: tabular-nums; }
    .dmv { flex: none; width: 40px; height: 24px; margin-top: 1px; border-radius: 6px; display: grid; place-items: center; font-size: 12px; font-weight: 600; }
    .dmv.in { background: var(--add-primary-a10); color: #006F88 !important; }
    .dmv.up { background: #FFF3D6; color: #8A5A00 !important; }
    .dmv.late { background: #FBE3E7; color: #C3213F !important; }
    .dvtabs { display: flex; gap: 4px; margin: 0 var(--sp-20) var(--sp-8); padding: 4px; border-radius: var(--radius); background: var(--neutral05); overflow-x: auto; scrollbar-width: none; }
    .dvtabs button { flex: 1 0 auto; display: inline-flex; align-items: center; justify-content: center; gap: 6px; min-height: 40px; padding: 0 12px; border-radius: 6px; color: var(--ink); white-space: nowrap; }
    .dvtabs button[aria-selected="true"] { background: var(--white); color: var(--md3-on-primary-container); font-weight: 600; box-shadow: 0 1px 2px rgba(31,65,91,.12); }
    .dvtabs .n { min-width: 20px; height: 20px; padding: 0 6px; border-radius: 10px; display: inline-grid; place-items: center; background: var(--add-primary-a10); color: #006F88; font-size: 12px; font-weight: 600; }
    button.dveh { width: 100%; text-align: left; cursor: pointer; }
    @media (hover: hover) { button.dveh:hover { background: var(--md3-background); } }
    .dveh .dchev { flex: none; align-self: center; color: var(--md3-neutral-secondary); transform: rotate(180deg); }
    .ddrawer { position: fixed; inset: var(--status-h) 0 0 0; z-index: 25; background: rgba(12, 28, 33, .45); display: flex; justify-content: flex-end; }
    .ddrawer[hidden] { display: none; }
    .ddrawer__p { width: min(620px, 100%); height: 100%; display: grid; grid-template-rows: auto 1fr; background: var(--white); box-shadow: -12px 0 32px rgba(12, 28, 33, .25); }
    .ddrawer.anim { animation: tlfade 200ms ease-out both; } .ddrawer.anim .ddrawer__p { animation: ddin 300ms cubic-bezier(.16, 1, .3, 1) both; }
    @keyframes ddin { from { transform: translateX(48px); opacity: .6; } to { transform: none; opacity: 1; } }
    @media (prefers-reduced-motion: reduce) { .ddrawer.anim, .ddrawer.anim .ddrawer__p { animation: none; } }
    .ddrawer__h { display: flex; align-items: center; gap: 10px; padding: 8px 8px 8px var(--sp-20); border-bottom: 1px solid var(--line); }
    .ddrawer__h b { color: var(--head); font-variant-numeric: tabular-nums; }
    .ddrawer__h span { flex: 1; min-width: 0; color: var(--ink); }
    .ddrawer__b { min-height: 0; display: grid; overflow: hidden; position: relative; }
    .ddrawer__b > .txdb { overflow-y: auto; }
    .ddrawer__b .txback { display: none !important; }
    .dmv.out { background: var(--md3-on-background); color: var(--md3-on-surface) !important; }
    .dnote { padding: 4px 20px 16px; color: var(--ink); }
    .dmore { display: block; width: 100%; min-height: 48px; border-top: 1px solid var(--md3-surface-variant); color: var(--md3-on-surface); font-weight: 600; }
    .dseg { width: 100%; max-width: 520px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px; margin-top: var(--sp-12); padding: 4px; border-radius: var(--radius); background: var(--neutral05); }
    .dseg a { min-height: 44px; display: grid; place-items: center; border-radius: 8px; color: var(--ink); }
    .dseg a[aria-selected="true"] { background: var(--white); color: var(--md3-on-primary-container); box-shadow: var(--card-shadow); font-weight: 600; }
    .cfgrow--gate { display: grid; gap: 10px; }
    .cfgrow__top { display: flex; align-items: center; gap: var(--sp-16); }
    .gtabs { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; padding-top: 10px; border-top: 1px solid var(--md3-surface-variant); }
    .gtabs > span:first-child { color: var(--ink); margin-right: 4px; }
    .gtab { display: inline-flex; align-items: center; height: 28px; padding: 0 10px; border-radius: 14px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); font-size: 13px; font-weight: 500; }
    .gtabs .linkbtn { margin-left: auto; min-height: 44px; padding: 0 6px; color: var(--md3-on-surface); font-weight: 600; }
    .gtabbar { display: flex; gap: 0; margin-top: var(--sp-16); overflow-x: auto; scrollbar-width: none; background: var(--white); border-radius: 10px 10px 0 0; border-bottom: 1px solid var(--line); }
    .gtabbar a { flex: 1 0 auto; min-height: 50px; display: grid; place-items: center; padding: 0 14px; color: var(--md3-on-surface-variant); border-bottom: 3px solid transparent; white-space: nowrap; }
    .gtabbar a[aria-selected="true"] { color: var(--md3-on-surface); border-bottom-color: var(--md3-on-surface); font-weight: 600; }
    .tag.bad { background: var(--error-a5); color: #B3213F; margin-left: 8px; }
    .gv .when { display: grid; justify-items: end; gap: 4px; }
"""

CFG_JS = r"""  /* ---------------- Security config (admin) + Gates (security) ---------------- */
  var CFG_KEY = 'antz.security.cfg', CFG_V = '__CFGV__';
  var SEED = JSON.parse(JSON.stringify(SD)); SEED.sites.forEach(function (s) { s.incharge = TXM.incharge[s.id] || ''; }); SEED.tablet = { bld: 'B01', gates: ['G01', 'G02', 'G03'] };
  (function () { var s = lsGet(CFG_KEY); SD = s && s.v === CFG_V && s.cfg ? s.cfg : JSON.parse(JSON.stringify(SEED)); })();
  function cfgSave() { lsSet(CFG_KEY, { v: CFG_V, cfg: SD }); }
  function inch(id) { return sby(SD.sites, id).incharge || ''; }
  function isAdmin() { return VIEWER.key === 'security-admin'; }
  function two() { return isAdmin() ? 'departments' : 'gates'; }
  var PURP = ['Entry', 'Exit', 'Service', 'Staff', 'Waste removal', 'Emergency'];
  var VISITS = __VIS__;
  /* tabs a gate shows on the security tablet: set per gate by the admin, else from what the gate is used for */
  /* gate departments are not animal related, so a gate only has vehicle tabs (site transfers live under Sites) */
  var GTAB = { entry: 'Vehicle entry', exit: 'Vehicle exit' }, GTABK = Object.keys(GTAB);
  function gTabs(g) { var keep = (g.tabs || []).filter(function (k) { return GTAB[k]; }); if (keep.length) return keep; var p = g.purposes, t = [];
    if (p.indexOf('Entry') !== -1 || p.indexOf('Service') !== -1 || p.indexOf('Staff') !== -1 || p.indexOf('Emergency') !== -1) t.push('entry');
    if (p.indexOf('Exit') !== -1 || p.indexOf('Service') !== -1 || p.indexOf('Waste removal') !== -1) t.push('exit');
    return t.length ? t : ['entry']; }
  var GICO = '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true"><rect x="5" y="5" width="14" height="14" rx="1" stroke-dasharray="2 1.6"/><rect x="9.2" y="9.2" width="5.6" height="5.6"/></svg>';
  var PIN = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/></svg>';
  var BLD = '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="3" width="10" height="18" rx="1"/><path d="M14 9h6v12h-6M7 7h4M7 11h4M7 15h4M16.5 13h1M16.5 16.5h1"/></svg>';
  var PLUS = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>';
  function chev() { return ic('back', 20).replace('<svg', '<svg class="chev"'); }
  function nextId(list, pre) { var n = 0; list.forEach(function (x) { var m = Number(String(x.id).replace(/\D/g, '')); if (m > n) n = m; }); return pre + ('0' + (n + 1)).slice(-2); }
  function onTab(g) { return SD.tablet && SD.tablet.gates.indexOf(g.id) !== -1; }
  function setTabs() {
    var a = document.getElementById('t-two'); a.textContent = isAdmin() ? 'Departments' : 'Gates'; a.setAttribute('href', '#' + two());
    var r = sparse(); document.getElementById('t-sites').setAttribute('aria-selected', String(r.tab === 'sites')); a.setAttribute('aria-selected', String(r.tab !== 'sites'));
  }
  function sparse() { var h = location.hash.replace(/^#/, '').split('/'); var t = h[0] === 'departments' || h[0] === 'gates' ? h[0] : 'sites'; return { tab: t, id: h[1] || '', type: h[2] || '', tx: h[3] || '' }; }
  var SEC_READY = true;
  function onViewer() { if (SEC_READY) { document.getElementById('main').innerHTML = ''; srender(); } }
  function srender() {
    var r = sparse(), main = document.getElementById('main');
    if (r.tab !== 'sites' && r.tab !== two()) { location.replace('#' + two()); return; }
    if (r.tab === 'sites' && r.id === 'manage' && !isAdmin()) { location.replace('#sites'); return; }
    setTabs();
    /* inside a building (admin) the building has its own tabs, so the Sites | Departments bar is hidden and back goes to the department */
    var inB = r.tab === 'departments' && location.hash.split('/').length > 2, nav = document.querySelector('.head .mtabs'), bk = document.querySelector('.head .bar .iconbtn');
    nav.hidden = inB;
    var hd = document.querySelector('.head .bar__hd'), bb = inB ? sby(SD.buildings, location.hash.split('/')[2]) : null;
    hd.innerHTML = inB && bb.id ? '<h1 class="t-medium-medium">' + esc(bb.name) + '</h1><p class="t-body-regular">' + esc(sby(SD.departments, r.id).name) + ' \u00b7 <span class="mono">' + esc(bb.code) + '</span></p>' : '<h1 class="t-medium-medium">Security</h1>';
    if (inB) { bk.setAttribute('href', '#departments/' + r.id); bk.setAttribute('aria-label', 'Back to ' + (sby(SD.departments, r.id).name || 'department')); }
    else { bk.setAttribute('href', 'diet-module-flow.html?as=' + VIEWER.key); bk.setAttribute('aria-label', 'Back to Modules'); }
    if (r.tab !== 'gates') gateClose();
    var manage = r.tab === 'sites' && r.id === 'manage';
    if (r.tab !== 'sites' || manage) { document.getElementById('stpanel').hidden = true; TXCUR = null; }
    if (r.tab === 'sites') { if (manage) adminSites(main); else { if (!main.querySelector('.stsearch')) txSites(); txRoute(); } return; }
    if (r.tab === 'gates') { secGates(main, r); return; }
    gateClose();
    adminDepts(main, r);
  }

  /* ---- Security Admin: Sites ---- */
  function adminSites(main) {
    main.innerHTML = '<nav class="crumbs t-body-regular" aria-label="Breadcrumb"><a href="#sites">Sites</a>\u203a<b>Manage sites</b></nav><div class="cfgbar" style="margin-top:4px"><div><h2 class="t-minor-title">' + plural(SD.sites.length, 'site') + '</h2><p class="t-body-regular">Sites, their codes and the site in-charge security calls.</p></div><button type="button" class="btn add" data-cfg="site">' + PLUS + 'Add site</button></div>' +
      '<div class="cfglist">' + SD.sites.map(function (s) { var b = sblds('sites', s.id); return '<div class="cfgrow"><span class="spk__ico">' + sic('site') + '</span><span class="grow"><b>' + esc(s.name) + '</b><span class="t-body-regular"><span class="mono">' + esc(s.code) + '</span> · ' + plural(b.length, 'building') + ' · In-charge: ' + esc(s.incharge || 'Not set') + '</span></span><button type="button" class="cfgedit t-body-medium" data-cfg="site" data-id="' + s.id + '">Edit</button></div>'; }).join('') + '</div>';
    main.scrollTop = 0;
  }
  /* ---- Security Admin: Departments > buildings > gates ---- */
  function adminDepts(main, r) {
    var parts = location.hash.replace(/^#/, '').split('/'), d = parts[1] ? sby(SD.departments, parts[1]) : null, b = parts[2] ? sby(SD.buildings, parts[2]) : null;
    if (!d || !d.id) {
      main.innerHTML = '<div class="cfgbar"><div><h2 class="t-minor-title">' + plural(SD.departments.length, 'department') + '</h2><p class="t-body-regular">Each department has buildings, and each building has gates.</p></div><button type="button" class="btn add" data-cfg="dept">' + PLUS + 'Add department</button></div>' +
        '<div class="sgrid">' + SD.departments.map(function (x) { var bl = sblds('departments', x.id), g = bl.reduce(function (n, y) { return n + sgates(y.id).length; }, 0), tb = bl.some(function (y) { return SD.tablet && SD.tablet.bld === y.id; });
          return '<a class="spk" href="#departments/' + x.id + '"><span class="spk__top"><span class="spk__ico">' + sic(x.id) + '</span><b class="spk__name t-minor-title">' + esc(x.name) + '</b>' + ic('back', 20).replace('<svg', '<svg class="spk__chev"') + '</span><span class="spk__sub t-body-regular">' + plural(bl.length, 'building') + ' · ' + plural(g, 'gate') + '</span>' + (tb ? '<span class="tag tab">On security tablet</span>' : '') + '</a>'; }).join('') + '</div>';
      main.scrollTop = 0; return;
    }
    var crumbs = '<nav class="crumbs t-body-regular" aria-label="Breadcrumb"><a href="#departments">All departments</a>›' + (b && b.id ? '<a href="#departments/' + d.id + '">' + esc(d.name) + '</a>›<b>' + esc(b.name) + '</b>' : '<b>' + esc(d.name) + '</b>') + '</nav>';
    if (!b || !b.id) {
      var bl = sblds('departments', d.id);
      main.innerHTML = crumbs + '<div class="cfgbar"><div><h2 class="t-minor-title">' + plural(bl.length, 'building') + ' in ' + esc(d.name) + '</h2></div><button type="button" class="btn add" data-cfg="bld">' + PLUS + 'Add building</button></div>' +
        '<div class="cfglist">' + bl.map(function (x) { var gs = sgates(x.id); return '<a class="cfgrow" href="#departments/' + d.id + '/' + x.id + '"><span class="spk__ico">' + sic('bld') + '</span><span class="grow"><b>' + esc(x.name) + '</b><span class="t-body-regular"><span class="mono">' + esc(x.code) + '</span> · ' + esc(sby(SD.sites, x.site).name || '') + ' · ' + plural(gs.length, 'gate') + '</span></span>' + (SD.tablet && SD.tablet.bld === x.id ? '<span class="tag tab">On security tablet</span>' : '') + chev() + '</a>'; }).join('') + (bl.length ? '' : '<div class="empty"><b class="t-minor-title">No buildings yet</b><span class="t-body-regular">Add the first building in ' + esc(d.name) + '.</span></div>') + '</div>';
      main.scrollTop = 0; return;
    }
    var gs = sgates(b.id), isTab = SD.tablet && SD.tablet.bld === b.id, dash = parts[3] === 'dashboard', base = '#departments/' + d.id + '/' + b.id;
    var seg = '<nav class="mtabs k2 btabs" role="tablist" aria-label="' + esc(b.name) + '"><a role="tab" class="mtab t-minor-medium" href="' + base + '" aria-selected="' + !dash + '">Configuration</a><a role="tab" class="mtab t-minor-medium" href="' + base + '/dashboard" aria-selected="' + dash + '">Dashboard</a></nav>';
    if (dash) { main.innerHTML = seg + bldDash(b, gs); main.scrollTop = 0; return; }
    main.innerHTML = seg +
      '<div class="tabcard">' + (isTab ? '<span class="tag on">On tablet</span>' : '<span class="tag off">Not on tablet</span>') + '<span class="grow"><b class="t-minor-title">' + (isTab ? 'Shown on the security tablet' : 'Not on the security tablet') + '</b><span class="t-body-regular">' + (isTab ? 'Security sees the ticked gates below in their Gates tab, each with the tabs set here.' : 'The tablet shows ' + esc(sby(SD.buildings, SD.tablet && SD.tablet.bld).name || 'no building') + ' now. Switch it to ' + esc(b.name) + ' to give security these gates.') + '</span></span>' + (isTab ? '' : '<button type="button" class="btn pri" data-settab="' + b.id + '">Show on security tablet</button>') + '</div>' +
      '<div class="cfgbar"><div><h2 class="t-minor-title">Gates</h2><p class="t-body-regular"><span class="mono">' + esc(b.code) + '</span> · ' + esc(sby(SD.sites, b.site).name || '') + '</p></div><button type="button" class="btn add" data-cfg="gate">' + PLUS + 'Add gate</button></div>' +
      '<div class="cfglist">' + gs.map(function (g) { return '<div class="cfgrow cfgrow--gate' + (g.active ? '' : ' off') + '"><div class="cfgrow__top"><span class="gico">' + GICO + '</span><span class="grow"><b>' + esc(g.name) + '</b><span class="t-body-regular">' + esc(g.purposes.join(' + ') || 'No purpose set') + '</span></span>' + (g.active ? '' : '<span class="tag off">Inactive</span>') +
        (isTab ? '<label class="onsw"><input type="checkbox" data-ontab="' + g.id + '"' + (onTab(g) ? ' checked' : '') + (g.active ? '' : ' disabled') + '>On tablet</label>' : '') + '<button type="button" class="cfgedit t-body-medium" data-cfg="gate" data-id="' + g.id + '">Edit</button></div>' +
        '<div class="gtabs"><span class="t-body-medium">Tabs at this gate</span>' + gTabs(g).map(function (k) { return '<span class="gtab">' + GTAB[k] + '</span>'; }).join('') + '<button type="button" class="linkbtn t-body-medium" data-cfg="tabs" data-id="' + g.id + '">Configure tabs</button></div></div>'; }).join('') + (gs.length ? '' : '<div class="empty"><b class="t-minor-title">No gates yet</b><span class="t-body-regular">Add the gates for ' + esc(b.name) + '.</span></div>') + '</div>';
    main.scrollTop = 0;
  }
  /* ---- building Dashboard (admin): entries, exits, exits with and without a challan ---- */
  var DVT = 'all', DVMORE = false, DMORE = false, DGATES = {}, DPER = 'today';
  /* custom range from the calendar sheet: dates (from, to) and a time of day window (tf, tt) that also applies to the presets */
  var DR = { from: '2026-09-24', to: '2026-09-30', tf: '00:00', tt: '23:59' };
  var TWIN = [['00:00', '23:59', 'All day'], ['06:00', '12:00', 'Morning'], ['12:00', '17:00', 'Afternoon'], ['17:00', '22:00', 'Evening'], ['22:00', '06:00', 'Night']];
  function inTime(iso) { var t = iso.slice(11, 16); return DR.tf <= DR.tt ? t >= DR.tf && t <= DR.tt : t >= DR.tf || t <= DR.tt; }
  function inPer(iso) { if (!iso) return false; var d = iso.slice(0, 10), dd = Number(iso.slice(8, 10));
    var ok = DPER === 'custom' ? d >= DR.from && d <= DR.to : iso.slice(0, 7) === '2026-09' && (DPER === 'month' || (DPER === 'week' ? dd >= 24 : DPER === 'yday' ? dd === 29 : dd === 30));
    return ok && inTime(iso); }
  function allDay() { return DR.tf === '00:00' && DR.tt === '23:59'; }
  function fdate(d) { return Number(d.slice(8, 10)) + ' ' + MON[Number(d.slice(5, 7)) - 1]; }
  function ftime(t) { var h = Number(t.slice(0, 2)), m = t.slice(3, 5); return (h % 12 || 12) + ':' + m + (h < 12 ? ' AM' : ' PM'); }
  function perLabel() { var d = DPER === 'today' ? 'Today, 30 Sep' : DPER === 'yday' ? 'Yesterday, 29 Sep' : DPER === 'week' ? 'This week, 24 to 30 Sep' : DPER === 'month' ? 'This month, September' : (DR.from === DR.to ? fdate(DR.from) + ' 2026' : fdate(DR.from) + ' to ' + fdate(DR.to) + ' 2026');
    return d + (allDay() ? '' : ', ' + ftime(DR.tf) + ' to ' + ftime(DR.tt)); }
  /* date presets and time-of-day windows, same chip pattern as the Diet filter sheet */
  var DPRE = [['today', 'Today', '2026-09-30', '2026-09-30'], ['yday', 'Yesterday', '2026-09-29', '2026-09-29'], ['week', 'This week', '2026-09-24', '2026-09-30'], ['month', 'This month', '2026-09-01', '2026-09-30'], ['custom', 'Custom', '', '']];
  function calSheet() {
    var tw = TWIN.filter(function (w) { return w[0] === DR.tf && w[1] === DR.tt; })[0], dp = DPRE.filter(function (x) { return x[0] === DPER; })[0] || DPRE[0];
    var from = DPER === 'custom' ? DR.from : dp[2], to = DPER === 'custom' ? DR.to : dp[3];
    var chip = function (attr, v, l, on) { return '<button type="button" class="spchip t-body-medium" ' + attr + '="' + v + '" aria-pressed="' + on + '">' + l + '</button>'; };
    sheet2('<div class="sheet__h"><h2 class="t-major-title">Date and time</h2><button type="button" class="iconbtn" data-txclose aria-label="Close">' + ic('close', 24) + '</button></div><form class="fgrid calform" data-calform>' +
      '<div class="sheet__g"><h3 class="t-minor-medium">Date</h3><div class="chips">' + DPRE.map(function (x) { return chip('data-cdp', x[0], x[1], x[0] === dp[0]); }).join('') + '</div>' +
      '<div class="fcols" data-crange' + (dp[0] === 'custom' ? '' : ' hidden') + '><label>From<input type="date" name="from" min="2026-09-01" max="2026-09-30" value="' + from + '"></label><label>To<input type="date" name="to" min="2026-09-01" max="2026-09-30" value="' + to + '"></label></div></div>' +
      '<div class="sheet__g"><h3 class="t-minor-medium">Time of day</h3><div class="chips">' + TWIN.map(function (w) { return chip('data-ctw', w[0] + '-' + w[1], w[2], w === tw); }).join('') + chip('data-ctw', 'custom', 'Custom', !tw) + '</div>' +
      '<p class="t-body-regular cwin" data-cwin>' + (tw && tw[2] === 'All day' ? 'Every movement in the day' : ftime(DR.tf) + ' to ' + ftime(DR.tt)) + '</p>' +
      '<div class="fcols" data-ctime' + (tw ? ' hidden' : '') + '><label>Start time<input type="time" name="tf" value="' + DR.tf + '"></label><label>End time<input type="time" name="tt" value="' + DR.tt + '"></label></div></div>' +
      '<p class="ferr" hidden></p><div class="sheet__f"><button type="button" class="btn sec" data-calreset>Reset</button><button type="submit" class="btn pri">Apply</button></div></form>');
  }
  function gname(id) { return sby(SD.gates, id).name || id; }
  function bldDash(b, gs) {
    var sel = (DGATES[b.id] || []).filter(function (id) { return gs.some(function (g) { return g.id === id; }); }), on = function (id) { return !sel.length || sel.indexOf(id) !== -1; };
    var vis = VISITS.filter(function (v) { return v.bld === b.id; }), en = vis.filter(function (v) { return inPer(v.enteredAt) && on(v.gate); }), ex = vis.filter(function (v) { return inPer(v.exitedAt) && on(v.exitGate); });
    var nc = ex.filter(function (v) { return !v.exitChallan; }), wc = ex.length - nc.length, inside = vis.filter(function (v) { return v.state === 'INSIDE' && on(v.gate); });
    var gsel = gs.filter(function (g) { return on(g.id); }), per = DPER === 'today' ? 'today' : DPER === 'yday' ? 'yesterday' : DPER === 'week' ? 'this week' : DPER === 'month' ? 'this month' : 'in this range';
    var stat = function (l, n, s) { return '<div class="dstat"><span class="t-body-medium">' + l + '</span><b>' + n + '</b><small>' + s + '</small></div>'; };
    var h = '<div class="dbar"><div class="spchips dchips" role="group" aria-label="Gates"><button type="button" class="spchip t-body-medium" data-dgate="" aria-pressed="' + !sel.length + '">All gates</button>' + gs.map(function (g) { return '<button type="button" class="spchip t-body-medium" data-dgate="' + g.id + '" aria-pressed="' + (sel.indexOf(g.id) !== -1) + '">' + esc(g.name) + '</button>'; }).join('') + '</div>' +
      '<button type="button" class="spfilter ddate t-body-medium' + (DPER !== 'today' || !allDay() ? ' on' : '') + '" data-cal aria-haspopup="dialog" aria-label="Date and time: ' + esc(perLabel()) + '">' + ic('calendar', 20) + '<span>' + esc(perLabel()) + '</span></button></div>';
    h += '<section class="dsum" aria-label="Summary">' + stat('Entries', en.length, 'Vehicles in, ' + per) + stat('Exits', ex.length, 'Vehicles out, ' + per) + stat('Inside now', inside.length, 'Entered, not out yet') +
      '<div class="dpaper"><span class="t-body-medium">Exit paperwork</span>' + (ex.length ? '<div class="dsplit" role="img" aria-label="' + wc + ' with challan, ' + nc.length + ' without"><i class="w" style="flex:' + wc + '"></i>' + (nc.length ? '<i class="n" style="flex:' + nc.length + '"></i>' : '') + '</div>' : '') +
      '<div class="dleg"><p><b>' + wc + '</b>with challan</p><p class="n"><b>' + nc.length + '</b>without challan</p></div></div></section>';
    var rows = nc.slice().sort(function (a, c) { return a.exitedAt < c.exitedAt ? 1 : -1; });
    var side = '<section class="dpan' + (nc.length ? ' alert' : '') + '"><h3 class="dpan__h t-minor-title">Exits without challan <span class="cnt' + (nc.length ? ' bad' : '') + '">' + nc.length + '</span></h3>' +
      (nc.length ? '<div class="dlist">' + rows.slice(0, DMORE ? rows.length : 6).map(function (v) { return '<div class="drow"><span class="grow"><b class="mono">' + esc(v.vehicleNo) + '</b><span class="t-body-regular">' + esc(v.vendor) + '</span><small>' + esc(v.exitNote || 'No reason given') + '</small></span><span class="when">' + dshort(v.exitedAt) + '<br>' + hm(v.exitedAt) + '<br>' + esc(gname(v.exitGate)) + '</span></div>'; }).join('') + '</div>' + (rows.length > 6 && !DMORE ? '<button type="button" class="dmore t-body-medium" data-dmore>Show all ' + rows.length + '</button>' : '')
        : '<p class="dnote t-body-regular">Every exit ' + per + ' left with a challan.</p>') + '</section>';
    var table = '<section class="dpan"><h3 class="dpan__h t-minor-title">By gate</h3><table class="sdtab"><thead><tr><th>Gate</th><th class="r">Entries</th><th class="r">Exits</th><th class="r">Without challan</th><th class="r">Inside now</th></tr></thead><tbody>' +
      gsel.map(function (g) { var e1 = en.filter(function (v) { return v.gate === g.id; }).length, x = ex.filter(function (v) { return v.exitGate === g.id; }), n1 = x.filter(function (v) { return !v.exitChallan; }).length; return '<tr><td><b>' + esc(g.name) + '</b><small>' + esc(g.purposes.join(' + ')) + '</small></td><td class="r">' + e1 + '</td><td class="r">' + x.length + '</td><td class="r' + (n1 ? ' bad' : '') + '">' + (n1 ? '<b>' + n1 + '</b>' : '0') + '</td><td class="r">' + inside.filter(function (v) { return v.gate === g.id; }).length + '</td></tr>'; }).join('') + '</tbody></table></section>';
    /* vehicles in this period, split All | Checked in | Checked out | Upcoming; tap one for its detail (read only) */
    var vin = vis.filter(function (v) { return v.state === 'INSIDE' && on(v.gate) && (inPer(v.enteredAt) || DPER !== 'custom'); }),
      vout = vis.filter(function (v) { return v.state === 'EXITED' && inPer(v.exitedAt) && on(v.exitGate); }),
      vup = vis.filter(function (v) { return v.state === 'UPCOMING' && on(v.gate) && (DPER === 'today' || DPER === 'week' || DPER === 'month' || inPer(v.eta)); });
    var key = function (v) { return v.state === 'UPCOMING' ? v.eta : v.exitedAt || v.enteredAt || ''; };
    var lists = { in: vin, out: vout, up: vup, all: vin.concat(vout, vup) }, cur = lists[DVT] ? DVT : 'all', lst = lists[cur].slice().sort(function (a, c) { return key(a) < key(c) ? 1 : -1; });
    var tag = function (v) { return v.state === 'UPCOMING' ? (v.eta <= '2026-09-30T15:42' ? '<span class="dmv late">Late</span>' : '<span class="dmv up">Due</span>') : v.state === 'INSIDE' ? '<span class="dmv in">In</span>' : '<span class="dmv out">Out</span>'; };
    var moves = '<section class="dpan"><h3 class="dpan__h t-minor-title">Vehicles</h3><div class="dvtabs" role="tablist" aria-label="Vehicles">' + [['all', 'All'], ['in', 'Checked in'], ['out', 'Checked out'], ['up', 'Upcoming']].map(function (t) { return '<button type="button" role="tab" class="t-body-medium" data-dvt="' + t[0] + '" aria-selected="' + (t[0] === cur) + '">' + t[1] + '<span class="n">' + lists[t[0]].length + '</span></button>'; }).join('') + '</div><div class="dlist">' +
      lst.slice(0, DVMORE ? lst.length : 8).map(function (v) { var t = key(v); return '<button type="button" class="drow dveh" data-dveh="' + v.id + '">' + tag(v) + '<span class="grow"><b class="mono">' + esc(v.vehicleNo) + '</b><span class="t-body-regular">' + esc(v.vendor) + ', ' + esc(gname(v.state === 'EXITED' ? v.exitGate : v.gate)) + (v.state === 'EXITED' && !v.exitChallan ? ', no challan' : '') + (v.state === 'UPCOMING' && v.challanNo ? ', DC ' + esc(v.challanNo) : '') + '</span></span><span class="when">' + (v.state === 'UPCOMING' ? 'ETA ' : '') + (DPER === 'today' ? '' : dshort(t) + '<br>') + hm(t) + '</span>' + ic('back', 18).replace('<svg', '<svg class="dchev"') + '</button>'; }).join('') + '</div>' +
      (lst.length > 8 && !DVMORE ? '<button type="button" class="dmore t-body-medium" data-dvmore>Show all ' + lst.length + '</button>' : '') + (lst.length ? '' : '<p class="dnote t-body-regular">' + (cur === 'up' ? 'No vehicles expected.' : 'No vehicles ' + per + '.') + '</p>') + '</section>';
    return h + '<div class="dcols"><div>' + table + moves + '</div><div>' + side + '</div></div>';
  }
  /* ---- Security: Gates (configured by the Security Admin) ---- */
  var VST = [['AT_GATE', 'At the gate'], ['UPCOMING', 'Expected'], ['INSIDE', 'Inside'], ['EXITED', 'Left']];
  function hm(iso) { if (!iso) return ''; var p = iso.split(/[-T:]/).map(Number), h = p[3] % 12 || 12; return h + ':' + ('0' + p[4]).slice(-2) + (p[3] < 12 ? ' AM' : ' PM'); }
  function secGates(main, r) {
    var b = sby(SD.buildings, SD.tablet && SD.tablet.bld), gs = b.id ? sgates(b.id).filter(function (g) { return g.active && onTab(g); }) : [];
    var loc = b.id ? '<div class="gloc">' + PIN + '<span>' + esc(b.name) + '</span><i></i>' + BLD + '<span>' + esc(sby(SD.departments, b.dept).name) + ' · <span class="mono">' + esc(b.code) + '</span></span></div>' : '';
    var g = r.id ? gs.filter(function (x) { return x.id === r.id; })[0] : null;
    if (!g) {
      if (r.id === '' && typeof gateClose === 'function') gateClose();
      main.innerHTML = loc + (gs.length ? '<p class="glab t-body-title">Gates</p><div class="glist">' + gs.map(function (x) { return '<a class="cfgrow" href="#gates/' + x.id + '"><span class="gico">' + GICO + '</span><span class="grow"><b>' + esc(x.name) + '</b><span class="t-body-regular">' + esc(x.purposes.join(' + ')) + '</span></span>' + (x.live ? '<span class="slive">' + plural(x.live, 'vehicle') + '</span>' : '') + chev() + '</a>'; }).join('') + '</div>'
        : '<div class="empty" style="margin-top:24px"><b class="t-minor-title">No gates on this tablet yet</b><span class="t-body-regular">The Security Admin picks the building and gates for this tablet under Departments.</span></div>');
      main.scrollTop = 0; return;
    }
    /* the gate opens as its own screen (security_gate_ui.py); the gate list stays underneath */
    if (!main.querySelector('.glist')) { var rr = { id: '' }; secGates(main, rr); }
    gatePanel(g, b, r.type, r.tx);
  }
  /* ---- config sheets ---- */
  function field(lab, name, val, ph) { return '<label>' + lab + '<input type="text" name="' + name + '" value="' + esc(val || '') + '" placeholder="' + (ph || '') + '" autocomplete="off"></label>'; }
  function cfgSheet(kind, id) {
    var parts = location.hash.replace(/^#/, '').split('/'), x, h = '';
    if (kind === 'site') { x = id ? sby(SD.sites, id) : {}; h = sheetHead(id ? 'Edit site' : 'Add site') + '<form class="fgrid" data-cfgform="site" data-id="' + (id || '') + '">' + field('Site name*', 'name', x.name, 'e.g. Reptile Park') + field('Code*', 'code', x.code, 'e.g. RP') + field('Site in-charge', 'incharge', x.incharge, 'Name') + '<p class="ferr" hidden></p><div class="acts2"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">' + (id ? 'Save' : 'Add site') + '</button></div></form>'; }
    if (kind === 'dept') h = sheetHead('Add department') + '<form class="fgrid" data-cfgform="dept">' + field('Department name*', 'name', '', 'e.g. Quarantine') + '<p class="ferr" hidden></p><div class="acts2"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">Add department</button></div></form>';
    if (kind === 'bld') h = sheetHead('Add building', esc(sby(SD.departments, parts[1]).name)) + '<form class="fgrid" data-cfgform="bld">' + field('Building name*', 'name', '', 'e.g. Reptile Kitchen') + field('Code*', 'code', '', 'e.g. KIT-04') + '<label>Site<select name="site">' + SD.sites.map(function (s) { return '<option value="' + s.id + '">' + esc(s.name) + '</option>'; }).join('') + '</select></label><p class="ferr" hidden></p><div class="acts2"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">Add building</button></div></form>';
    if (kind === 'gate') { x = id ? sby(SD.gates, id) : { purposes: ['Entry', 'Exit'], active: true }; h = sheetHead(id ? 'Edit gate' : 'Add gate', esc(sby(SD.buildings, parts[2]).name)) + '<form class="fgrid" data-cfgform="gate" data-id="' + (id || '') + '">' + field('Gate name*', 'name', x.name, 'e.g. Gate 3') +
      '<fieldset style="border:0;display:grid;gap:8px"><legend class="t-body-medium" style="color:var(--ink);margin-bottom:8px">What the gate is used for*</legend><div class="pchips">' + PURP.map(function (p) { return '<label class="pchip t-body-medium"><input type="checkbox" name="p" value="' + p + '"' + (x.purposes.indexOf(p) !== -1 ? ' checked' : '') + '>' + p + '</label>'; }).join('') + '</div></fieldset>' +
      '<label class="onsw" style="font-size:15px;color:var(--head)"><input type="checkbox" name="active"' + (x.active ? ' checked' : '') + '>Gate is active</label><p class="ferr" hidden></p><div class="acts2"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">' + (id ? 'Save' : 'Add gate') + '</button></div></form>'; }
    if (kind === 'tabs') { x = sby(SD.gates, id); var on = gTabs(x); h = sheetHead('Tabs at ' + esc(x.name), 'What security sees on the tablet at this gate') + '<form class="fgrid" data-cfgform="tabs" data-id="' + id + '"><div class="pchips">' + GTABK.map(function (k) { return '<label class="pchip t-body-medium"><input type="checkbox" name="t" value="' + k + '"' + (on.indexOf(k) !== -1 ? ' checked' : '') + '>' + GTAB[k] + '</label>'; }).join('') + '</div><p class="t-body-regular" style="color:var(--ink)">Vehicle entry gives security the Checked in tab, Vehicle exit the Checked out tab. All is always there.</p><p class="ferr" hidden></p><div class="acts2"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">Save tabs</button></div></form>'; }
    sheet2(h); var f = document.querySelector('#txsheet input[type=text]'); if (f) f.focus();
  }
  document.getElementById('main').addEventListener('click', function (e) {
    var b;
    if ((b = e.target.closest('[data-dvt]'))) { DVT = b.getAttribute('data-dvt'); DVMORE = false; srender(); return; }
    if (e.target.closest('[data-dvmore]')) { DVMORE = true; srender(); return; }
    if ((b = e.target.closest('[data-dveh]'))) { drawerOpen(b.getAttribute('data-dveh'), true); return; }
    if ((b = e.target.closest('[data-dmore]'))) { DMORE = true; srender(); return; }
    if (e.target.closest('[data-cal]')) { calSheet(); return; }
    if ((b = e.target.closest('[data-dper]'))) { DPER = b.getAttribute('data-dper'); DMORE = false; srender(); return; }
    if ((b = e.target.closest('[data-dgate]'))) { DMORE = false; var gid = b.getAttribute('data-dgate'), bid = location.hash.split('/')[2], cur = DGATES[bid] || []; DGATES[bid] = !gid ? [] : cur.indexOf(gid) !== -1 ? cur.filter(function (x) { return x !== gid; }) : cur.concat([gid]); srender(); return; }
    if ((b = e.target.closest('[data-cfg]'))) { cfgSheet(b.getAttribute('data-cfg'), b.getAttribute('data-id')); return; }
    if ((b = e.target.closest('[data-settab]'))) { var id = b.getAttribute('data-settab'); SD.tablet = { bld: id, gates: sgates(id).filter(function (g) { return g.active; }).map(function (g) { return g.id; }) }; cfgSave(); srender(); toast(sby(SD.buildings, id).name + ' is now on the security tablet'); }
  });
  document.getElementById('main').addEventListener('change', function (e) {
    var id = e.target.getAttribute('data-ontab'); if (!id) return; var l = SD.tablet.gates.filter(function (x) { return x !== id; }); if (e.target.checked) l.push(id); SD.tablet.gates = l; cfgSave(); toast(sby(SD.gates, id).name + (e.target.checked ? ' added to' : ' removed from') + ' the security tablet');
  });
  document.getElementById('txsheet').addEventListener('click', function (e) {
    var b = e.target.closest('[data-cdp], [data-ctw]'); if (!b) return; var f = b.closest('form');
    [].forEach.call(b.parentNode.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); });
    if (b.hasAttribute('data-cdp')) { var x = DPRE.filter(function (d) { return d[0] === b.getAttribute('data-cdp'); })[0]; f.querySelector('[data-crange]').hidden = x[0] !== 'custom'; if (x[0] !== 'custom') { f.from.value = x[2]; f.to.value = x[3]; } return; }
    var v = b.getAttribute('data-ctw'); f.querySelector('[data-ctime]').hidden = v !== 'custom';
    if (v !== 'custom') { var p = v.split('-'); f.tf.value = p[0]; f.tt.value = p[1]; }
    f.querySelector('[data-cwin]').textContent = v === '00:00-23:59' ? 'Every movement in the day' : ftime(f.tf.value) + ' to ' + ftime(f.tt.value);
  });
  document.getElementById('txsheet').addEventListener('input', function (e) { var f = e.target.form; if (f && f.hasAttribute('data-calform') && (e.target.name === 'tf' || e.target.name === 'tt') && f.tf.value && f.tt.value) f.querySelector('[data-cwin]').textContent = ftime(f.tf.value) + ' to ' + ftime(f.tt.value); });
  document.getElementById('txsheet').addEventListener('click', function (e) {
    if (!e.target.closest('[data-calreset]')) return; DPER = 'today'; DR = { from: '2026-09-24', to: '2026-09-30', tf: '00:00', tt: '23:59' }; DMORE = false; document.getElementById('txsheet').hidden = true; srender();
  });
  document.getElementById('txsheet').addEventListener('submit', function (e) {
    var cf = e.target; if (cf.hasAttribute('data-calform')) { e.preventDefault(); var er = cf.querySelector('.ferr');
      if (!cf.from.value || !cf.to.value || cf.from.value > cf.to.value) { er.textContent = 'Pick a start date on or before the end date.'; er.hidden = false; return; }
      if (!cf.tf.value || !cf.tt.value) { er.textContent = 'Pick a start and end time.'; er.hidden = false; return; }
      DR = { from: cf.from.value, to: cf.to.value, tf: cf.tf.value, tt: cf.tt.value };
      DPER = DR.from === '2026-09-30' && DR.to === '2026-09-30' ? 'today' : DR.from === '2026-09-29' && DR.to === '2026-09-29' ? 'yday' : DR.from === '2026-09-24' && DR.to === '2026-09-30' ? 'week' : DR.from === '2026-09-01' && DR.to === '2026-09-30' ? 'month' : 'custom';
      DMORE = false; document.getElementById('txsheet').hidden = true; srender(); return; }
    var f = e.target, kind = f.getAttribute('data-cfgform'); if (!kind) return; e.preventDefault();
    var id = f.getAttribute('data-id'), parts = location.hash.replace(/^#/, '').split('/'), err = f.querySelector('.ferr'), v = function (n) { return f[n] ? f[n].value.trim() : ''; };
    function bad(m) { err.textContent = m; err.hidden = false; }
    if (kind !== 'tabs' && !v('name')) return bad('Enter a name.');
    if (kind === 'site') { if (!v('code')) return bad('Enter a code.'); var s = id ? sby(SD.sites, id) : { id: nextId(SD.sites, 'S') }; s.name = v('name'); s.code = v('code').toUpperCase(); s.incharge = v('incharge'); if (!id) { SD.sites.push(s); TX[s.id] = []; } }
    if (kind === 'dept') SD.departments.push({ id: nextId(SD.departments, 'D'), name: v('name') });
    if (kind === 'bld') { if (!v('code')) return bad('Enter a code.'); SD.buildings.push({ id: nextId(SD.buildings, 'B'), dept: parts[1], site: f.site.value, name: v('name'), code: v('code').toUpperCase(), note: '' }); }
    if (kind === 'tabs') { var ts = [].map.call(f.querySelectorAll('input[name=t]:checked'), function (x) { return x.value; }); if (!ts.length) return bad('Pick at least one tab.'); sby(SD.gates, id).tabs = ts; cfgSave(); document.getElementById('txsheet').hidden = true; toast('Tabs saved for ' + sby(SD.gates, id).name); srender(); return; }
    if (kind === 'gate') { var ps = [].map.call(f.querySelectorAll('input[name=p]:checked'), function (x) { return x.value; }); if (!ps.length) return bad('Pick at least one use.'); var g = id ? sby(SD.gates, id) : { id: nextId(SD.gates, 'G'), bld: parts[2], live: 0 }; g.name = v('name'); g.purposes = ps; g.active = f.active.checked; if (!id) { SD.gates.push(g); if (SD.tablet && SD.tablet.bld === g.bld && g.active) SD.tablet.gates.push(g.id); } if (!g.active) SD.tablet.gates = SD.tablet.gates.filter(function (x) { return x !== g.id; }); }
    cfgSave(); document.getElementById('txsheet').hidden = true; toast(id ? 'Saved' : 'Added ' + v('name')); srender();
  });
"""
