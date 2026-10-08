# security.py: exec'd by modules.py. Security home: Sites | Departments, then the buildings and gates inside one
# (from kitchen/Roshni/Tab prototype security-sites.html + flow-data.js). Role views in security_cfg_ui.py: Security Admin gets
# Sites | Departments (configuration), Security gets Sites (site transfers) | Gates (the gates the admin configured).
SEC = json.load(open(os.path.join(HERE, 'security-data.json'), encoding='utf-8'))   # SAMPLE DATA: sites, departments, buildings, gates, vehicles inside
exec(open(os.path.join(HERE, 'security_tx.py')).read())
exec(open(os.path.join(HERE, 'security_tx_ui.py')).read())
exec(open(os.path.join(HERE, 'security_visits.py')).read())
exec(open(os.path.join(HERE, 'security_cfg_ui.py')).read())
exec(open(os.path.join(HERE, 'security_gate_ui.py')).read())
SEC_TABS = '      <nav class="mtabs k2" role="tablist" aria-label="Security sections"><a class="mtab t-minor-medium" role="tab" id="t-sites" href="#sites" aria-selected="true">Sites</a><a class="mtab t-minor-medium" role="tab" id="t-two" href="#departments" aria-selected="false">Departments</a></nav>'
SEC_CSS = """    /* =========================================================
       16. SECURITY  (Sites | Departments, then the buildings and gates inside)
       ========================================================= */
    .mtabs.k2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .sgrid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--sp-16); margin-top: var(--sp-16); }
    @media (orientation: portrait) { .sgrid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    .spk { display: grid; gap: var(--sp-8); align-content: start; justify-items: start; padding: var(--sp-20); border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); text-align: left; width: 100%; min-height: 120px; transition: transform 120ms var(--ease); }
    button.spk:active { transform: scale(.98); }
    .spk__top { display: flex; align-items: center; gap: var(--sp-12); width: 100%; }
    .spk__ico { width: 44px; height: 44px; border-radius: var(--radius); display: grid; place-items: center; flex: none; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .spk__ico svg { fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .spk__name { flex: 1; min-width: 0; color: var(--head); }
    .spk__chev { color: var(--md3-neutral-secondary); transform: rotate(180deg); }
    .spk__sub { color: var(--ink); }
    .spk__note { color: var(--md3-neutral-secondary); }
    .slive { display: inline-flex; align-items: center; height: 26px; padding: 0 10px; border-radius: 999px; background: var(--add-primary-a10); color: #006F88; font-size: 13px; font-weight: 600; white-space: nowrap; }
    .mono { font-variant-numeric: tabular-nums; font-family: ui-monospace, "SF Mono", Menlo, monospace; font-size: 13px; }
    .sgates { display: flex; flex-wrap: wrap; gap: var(--sp-8); padding-top: var(--sp-12); border-top: 1px solid var(--md3-surface-variant); width: 100%; }
    .sgate { display: inline-flex; align-items: center; gap: 6px; min-height: 32px; padding: 4px 10px; border-radius: 6px; background: var(--md3-background); color: var(--head); font-size: 13px; }
    .sgate small { color: var(--md3-neutral-secondary); font-size: 12px; }
    .sgate.off { color: var(--md3-neutral-secondary); background: transparent; border: 1px dashed var(--md3-outline-variant); }
    .scrumb { display: flex; align-items: center; gap: var(--sp-16); margin-top: var(--sp-16); }
    .scrumb .chip { color: var(--md3-on-primary-container); min-height: 44px; }
    .scrumb h2 { color: var(--head); }
    .scrumb p { color: var(--ink); }
"""
SEC_JS = (r"""  /* ---------------- Security: Sites | Departments (Tab prototype security-sites.html) ---------------- */
  var SD = __SEC__;
  var SICO = { site: '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    bld: '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M11 21v-3h2v3"/>',
    D1: '<path d="M4 11h16M6 11v6a3 3 0 0 0 3 3h6a3 3 0 0 0 3-3v-6M9 8c-.8-.8-.8-1.7 0-2.5M12 8c-.8-.8-.8-1.7 0-2.5M15 8c-.8-.8-.8-1.7 0-2.5"/>',
    D2: '<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v8M8 12h8"/>',
    D3: '<path d="M3 20V9l9-5 9 5v11"/><path d="M7 20v-7h10v7M7 16.5h10"/>',
    D4: '<path d="M14.5 5.5l4 4M13 7 4.5 15.5a2.1 2.1 0 0 0 3 3L16 10M12 4.5l2-1.5 6.5 6.5-1.5 2"/>',
    D5: '<path d="M10.5 20.5a5 5 0 0 1-7-7l6-6a5 5 0 0 1 7 7z"/><path d="M8.5 8.5l7 7"/>' };
  function sic(k) { return '<svg width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + (SICO[k] || SICO.bld) + '</svg>'; }
  function sby(list, id) { return list.filter(function (x) { return x.id === id; })[0] || {}; }
  function sgates(bid) { return SD.gates.filter(function (g) { return g.bld === bid; }); }
  function slive(blds) { return blds.reduce(function (n, b) { return n + sgates(b.id).reduce(function (m, g) { return m + g.live; }, 0); }, 0); }
  function sblds(kind, id) { return SD.buildings.filter(function (b) { return kind === 'sites' ? b.site === id : b.dept === id; }); }
  function plural(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }
  function liveChip(n) { return n ? '<span class="slive">' + plural(n, 'vehicle') + ' inside</span>' : ''; }
""" + TX_JS + CFG_JS + GATE_JS + """  window.addEventListener('hashchange', srender);
  srender();
""").replace('__SEC__', json.dumps(SEC, ensure_ascii=False, separators=(',', ':'))).replace('__TX__', json.dumps(TX, ensure_ascii=False, separators=(',', ':'))).replace('__TXM__', json.dumps(TX_META, ensure_ascii=False, separators=(',', ':'))).replace('__VIS__', json.dumps(VISITS, ensure_ascii=False, separators=(',', ':'))).replace('__CFGV__', __import__('hashlib').md5(json.dumps(SEC, sort_keys=True).encode()).hexdigest()[:10]).replace('__TXV__', __import__('hashlib').md5(json.dumps(TX, sort_keys=True).encode()).hexdigest()[:10])
mod_page('security', 'Security', 'security', SEC_TABS, SEC_CSS + TX_CSS + CFG_CSS + GATE_CSS, SEC_JS, TX_HTML + '\n' + GATE_HTML)
