# kitchen.py: exec'd by build.py after home2.py. Builds kitchen-home.html, the target of the Kitchen tile on
# diet-module-flow.html. Two tabs: Kitchen Dashboard (#dashboard) and Meal Group Management (#meal-groups).
# Dashboard: modelled on Dev system_local kitchen/dashboard (figures from _build/kitchen-data.json, the V2 copy of the same page's
# data, because the Dev page computes from inventory files and shows zeros without them), led by a Diet requests card that reads
# the shared request store (STORE_JS in roles.py), the same data as diet-home.html.
# Meal Group Management: 7 tiles, each a full-screen page (#meal-groups/<slug>): Prep Sheet here, the other 6 in mg_<slug>.py with seeds in meal-groups.json. Viewing as: same 4 roles and sheet as diet-home.html, shared through localStorage.
# The earlier full dashboard and keeper-area build is kept in kitchen_full_backup.py (not exec'd).

_kraw = open(os.path.join(HERE, 'kitchen-data.json'), encoding='utf-8').read().replace(' \u2013 ', ' to ').replace('\u2013', '-').replace('\u2014', '-')
KDASH = json.load(open(os.path.join(HERE, 'kitchen-sample.json'), encoding='utf-8'))   # SAMPLE DATA receipts (kitchen-data.json is no longer used)
KSTK = json.load(open(os.path.join(HERE, 'kitchen-stock.json'), encoding='utf-8'))   # SAMPLE DATA stock batches for the Stock & expiry row (own file so the request seed version does not change)
PSDATA = json.load(open(os.path.join(HERE, 'prep-sheet.json'), encoding='utf-8'))   # source data (Dev system prep sheet + piece weights)
PSCHED = {str(r['proposedId']): BS['plans'][str(r['proposedId'])]['schedule'] for r in _req_seed if r.get('proposedId') and str(r['proposedId']) in BS['plans']}
K_ICONS = ['back', 'location-icon', 'dropdown', 'grid', 'user', 'close', 'just-tick-mark', 'history', 'time', 'timer', 'calendar', 'alert', 'info', 'list', 'transfer', 'reason-or-list', 'book', 'paw']

# ---- Meal Group Management pages: one module per tile, _build/mg_<slug>.py, each setting MGMOD = {'css', 'js', 'icons'}.
# Seed data per page: meal-groups.json[slug] (falls back to mgdata_<slug>.json while a page is being built).
# MG_ONLY=slug1,slug2 limits the modules; KH_OUT=name.html writes the kitchen page under another name (isolated test builds).
MG_SLUGS = ['packaging-list', 'keeper-areas', 'keeper-staff', 'wastage-setup', 'piece-weights', 'packing-stations']
_mg_only = [x for x in os.environ.get('MG_ONLY', '').split(',') if x]
_mg_all = json.load(open(os.path.join(HERE, 'meal-groups.json'), encoding='utf-8')) if os.path.exists(os.path.join(HERE, 'meal-groups.json')) else {}
MGSEED, MG_MODS = {}, []
for _slug in MG_SLUGS:
    if _mg_only and _slug not in _mg_only: continue
    _mp = os.path.join(HERE, 'mg_' + _slug.replace('-', '_') + '.py')
    if not os.path.exists(_mp): continue
    _dp = os.path.join(HERE, 'mgdata_' + _slug + '.json')
    if _slug in _mg_all: MGSEED[_slug] = _mg_all[_slug]
    elif os.path.exists(_dp): MGSEED[_slug] = json.load(open(_dp, encoding='utf-8'))
    MGMOD = None
    exec(open(_mp, encoding='utf-8').read())
    if MGMOD: MG_MODS.append(dict(MGMOD, slug=_slug))
for _m in MG_MODS:
    for _i in _m.get('icons', []):
        if _i not in K_ICONS: K_ICONS.append(_i)

MG_TILES = [
    ('packaging-list', 'Packaging list', '<rect x="10" y="9" width="28" height="33" rx="4"/><rect x="18" y="5.5" width="12" height="6" rx="2"/><path d="M15.5 20h1M15.5 27.5h1M15.5 35h1M21.5 20h11M21.5 27.5h11M21.5 35h7"/>'),
    ('keeper-areas', 'Keeper Areas', '<circle cx="24" cy="16" r="5"/><path d="M14.5 37a9.5 9.5 0 0 1 19 0"/><circle cx="11.5" cy="20" r="3.5"/><circle cx="36.5" cy="20" r="3.5"/><path d="M4.5 35a7 7 0 0 1 8.5-6.8M43.5 35a7 7 0 0 0-8.5-6.8"/>'),
    ('keeper-staff', 'Keeper Staff', '<rect x="6" y="12" width="36" height="26" rx="4"/><path d="M20 12V8h8v4"/><circle cx="16.5" cy="22.5" r="3.5"/><path d="M11 32.5a5.5 5 0 0 1 11 0M27 21h9M27 27.5h6"/>'),
    ('wastage-setup', 'Wastage setup', '<path d="M24 9v30M16 40h16M9 14.5h30"/><circle cx="24" cy="9" r="1.6"/><path d="M9 14.5 4.5 26M9 14.5 13.5 26M39 14.5 34.5 26M39 14.5 43.5 26M3.5 26a5.5 3.6 0 0 0 11 0zM33.5 26a5.5 3.6 0 0 0 11 0z"/>'),
    ('piece-weights', 'Piece Weights', '<path d="M24 4.5v6"/><circle cx="24" cy="23" r="10.5"/><path d="M24 23l4.5-5.5M20 15.5h8"/><path d="M24 33.5v3.5a3.6 3.6 0 1 1-3.6 3.6"/>'),
    ('packing-stations', 'Packing Stations', '<rect x="5" y="15" width="38" height="6.5" rx="2"/><path d="M10 21.5V40M38 21.5V40M10 32h28"/><path d="M16 15v-4h8v4"/>'),
    ('prep-sheet', 'Prep Sheet', '<path d="M4.5 29.5C10 21.5 19 17.5 29 17.5v12H6.8c-1.6 0-2.8-.9-2.3 0z"/><rect x="29" y="20" width="14.5" height="7.5" rx="3.75"/><path d="M8 36.5h32"/>'),
]
_mg_grad = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs><linearGradient id="kgrad" x1="4" y1="4" x2="44" y2="44" gradientUnits="userSpaceOnUse">'
            '<stop offset="0" stop-color="#1FDCD0"/><stop offset="1" stop-color="#4FCB90"/></linearGradient></defs></svg>')
MG_HTML = _mg_grad + '<div class="mgtiles" role="group" aria-label="Meal Group Management">' + ''.join(
    f'<button type="button" class="mgtile" data-mg="{i}" aria-label="{t}"><svg viewBox="0 0 48 48" fill="none" stroke="url(#kgrad)" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{d}</svg><span>{t}</span></button>'
    for i, t, d in MG_TILES) + '</div>'

KITCHEN_CSS = '''    /* =========================================================
       K. KITCHEN HOME
       ========================================================= */
    .mtabs.k2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .av { width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; flex: none; background: var(--md3-surface-variant); color: var(--md3-on-primary-container); font-weight: 600; font-size: 14px; }
    .ribbon { flex: none; min-width: 56px; height: 40px; padding: 0 12px 0 20px; display: grid; place-items: center; color: var(--white); clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 12px 50%); font-size: 20px; font-weight: 700; letter-spacing: 1px; }
    .ribbon.low { background: var(--md3-secondary); } .ribbon.medium { background: var(--md3-secondary-dark); } .ribbon.high { background: var(--md3-tertiary); }
    /* Kitchen Dashboard: filters row, 4 equal summary cards, 4 stacked detail rows (one layout for all) */
    .kpane { display: grid; gap: 16px; padding: 16px 0 8px; }
    .kfilt { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .kfilt .spchip { height: 44px; }
    .kfilt .sp { flex: 1; }
    .kfilt label { display: inline-flex; align-items: center; gap: 8px; color: var(--ink); }
    .kfilt select { height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--head); font: inherit; font-weight: 500; }
    .kfilt select:focus { border-color: var(--md3-on-primary-container); outline: none; }
    .kfilt .kdate { color: var(--ink); display: inline-flex; align-items: center; gap: 6px; }
    .ksum { display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .scard { display: grid; gap: 6px; align-content: start; min-height: 132px; padding: 16px; border-radius: var(--radius); background: var(--white); border: 1px solid transparent; color: var(--ink); }
    .scard .lab { display: flex; align-items: center; gap: 8px; font-size: 14px; font-weight: 600; color: var(--ink); }
    .scard .lab svg { color: var(--md3-on-primary-container); }
    .scard .lab .chev { margin-left: auto; display: inline-flex; }
    .scard b { font-size: 32px; line-height: 1.1; font-weight: 600; color: var(--md3-on-primary-container); font-variant-numeric: tabular-nums; }
    .scard b small { font-size: 14px; font-weight: 500; color: var(--ink); margin-left: 6px; }
    .scard .sup { font-size: 13px; color: var(--md3-neutral-secondary); }
    .alertx { color: #8A5A00; font-weight: 600; }
    a.scard, a.kfr, a.kitem { transition: border-color 200ms var(--ease), background-color 200ms var(--ease), transform 120ms var(--ease); }
    @media (hover: hover) { a.scard:hover, a.kfr:hover, a.kitem:hover { border-color: var(--md3-on-primary-container); } }
    a.scard:active, a.kfr:active, a.kitem:active { transform: scale(.99); }
    .scard .go { justify-self: start; display: inline-flex; align-items: center; gap: 4px; font-size: 13px; font-weight: 600; color: var(--md3-on-primary-container); margin-top: 2px; }
    .drow { background: var(--white); border-radius: var(--radius); padding: 18px 20px 20px; display: grid; gap: 16px; }
    .drow__h { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
    .drow__h h3 { color: var(--head); }
    .drow__h p { color: var(--md3-neutral-secondary); margin-top: 2px; }
    .drow__h .per { flex: none; display: inline-flex; align-items: center; height: 28px; padding: 0 10px; border-radius: 6px; background: var(--md3-background); color: var(--ink); font-size: 13px; font-weight: 500; white-space: nowrap; }
    .drow__b { display: grid; gap: 16px; grid-template-columns: minmax(0, 1fr); }
    .kfs { display: grid; gap: 8px; align-content: start; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .kfs.k3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .kfr { display: flex; align-items: center; justify-content: space-between; gap: 12px; min-height: 48px; padding: 0 14px; border-radius: 8px; background: var(--md3-background); border: 1px solid transparent; color: var(--ink); }
    .kfr b { color: var(--md3-on-primary-container); font-size: 18px; font-weight: 600; font-variant-numeric: tabular-nums; white-space: nowrap; }
    .kfr.wide { grid-column: 1 / -1; }
    .kfr.alert b, .kfr.alert span { color: #8A5A00; }
    .kpanel { display: grid; gap: 8px; align-content: start; min-width: 0; }
    .kpanel h4 { color: var(--head); font-size: 14px; font-weight: 600; }
    .kitem { display: flex; align-items: center; gap: 12px; min-height: 56px; padding: 6px 12px 6px 0; border-radius: 8px; background: var(--md3-background); border: 1px solid transparent; overflow: hidden; }
    .kitem .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .kitem .grow b { color: var(--head); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .kitem .grow small { color: var(--ink); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .kitem .ribbon { margin: 0; min-width: 44px; height: 32px; font-size: 15px; padding: 0 8px 0 16px; }
    .kitem .st { flex: none; font-size: 13px; font-weight: 600; color: var(--ink); }
    .kitem .st.alertx { color: #8A5A00; }
    .ktab { width: 100%; border-collapse: collapse; }
    .ktab th { text-align: left; font-size: 12px; font-weight: 600; color: var(--ink); padding: 0 12px 8px; border-bottom: 1px solid var(--md3-surface-variant); }
    .ktab td { padding: 12px; color: var(--head); border-bottom: 1px solid var(--line); }
    .ktab tr:last-child td { border-bottom: 0; }
    .ktab .r { text-align: right; font-variant-numeric: tabular-nums; }
    .ktab .hi { color: #B3213F; font-weight: 600; }
    .bars { display: flex; align-items: flex-end; gap: 16px; height: 152px; padding: 8px 4px 0; border-bottom: 1px solid var(--md3-surface-variant); }
    .bars .col { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; gap: 6px; min-width: 0; height: 100%; }
    .bars .pair { flex: 1; min-height: 0; display: flex; align-items: flex-end; gap: 4px; }
    .bars .pair i { width: 16px; border-radius: 3px 3px 0 0; background: var(--md3-on-primary-container); }
    .bars .pair i.r { background: rgba(31, 81, 91, .35); }
    .bars small { color: var(--md3-neutral-secondary); font-size: 12px; white-space: nowrap; }
    .bars.many { gap: 4px; } .bars.many .pair { gap: 1px; } .bars.many .pair i { width: 6px; } .bars.many small { font-size: 11px; }
    .legend { display: flex; gap: 16px; color: var(--ink); font-size: 13px; }
    .legend span { display: inline-flex; align-items: center; gap: 6px; }
    .legend i { width: 10px; height: 10px; border-radius: 2px; background: var(--md3-on-primary-container); } .legend i.r { background: rgba(31, 81, 91, .35); }
    .hbars { display: grid; gap: 10px; }
    .hbar { display: grid; grid-template-columns: minmax(0, 170px) minmax(0, 1fr) 44px; align-items: center; gap: 12px; color: var(--head); min-height: 24px; }
    .hbar span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .hbar i { height: 8px; border-radius: 4px; background: var(--md3-on-primary-container); display: block; }
    .hbar b { font-variant-numeric: tabular-nums; text-align: right; font-weight: 600; }
    .kempty { color: var(--md3-neutral-secondary); }
    .kcap { display: flex; gap: 6px; align-items: flex-start; font-size: 13px; color: var(--md3-neutral-secondary); }
    .kcap svg { flex: none; margin-top: 1px; }
    .kpanels2 { display: grid; gap: 16px; grid-template-columns: minmax(0, 1fr); }
    .kstack { display: grid; gap: 20px; min-width: 0; }
    /* Kitchen Operator Requests */
    .rvtop { display: grid; gap: 12px; }
    .rvseg { max-width: 520px; }
    .rvseg button { min-height: 44px; }
    .kfsel select { height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--head); font: inherit; font-weight: 500; }
    .rvcard { gap: 12px; scroll-margin: 16px; }
    .rvcard.hl { box-shadow: 0 0 0 2px var(--md3-on-primary-container); }
    .rvhead { display: flex; align-items: flex-start; gap: 12px; }
    .rvhead .ribbon { margin-left: -20px; flex: none; }
    .rvhead .grow { flex: 1; min-width: 0; }
    .rvhead h3 { color: var(--head); }
    .rvhead p { color: var(--ink); }
    .rvmeta { display: flex; align-items: center; gap: 6px; color: var(--ink); }
    .rvmeta svg { flex: none; color: var(--md3-on-primary-container); }
    .rvsec h4 { font-size: 14px; font-weight: 600; color: var(--head); margin-bottom: 6px; }
    .rvitems { display: flex; flex-wrap: wrap; gap: 6px; }
    .rvitem { display: inline-flex; align-items: center; gap: 6px; min-height: 32px; padding: 0 10px; border-radius: 6px; background: var(--md3-background); color: var(--head); font-size: 14px; font-weight: 500; }
    .rvitem small { color: var(--md3-neutral-secondary); font-weight: 400; font-size: 13px; }
    .rvitem.alt { background: #FFF6DB; color: #6B4E00; }
    .rvacts { display: flex; flex-wrap: wrap; gap: 8px; }
    .kdseg { margin-top: 0; }
    .kdseg .seg3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .kdseg .seg3 button { min-height: 44px; }
    .kkpis { display: grid; gap: 10px; }
    .kkpis__h { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; padding: 4px 2px 0; }
    .kkpis__h h3 { color: var(--head); }
    .kkpis__h span { color: var(--md3-neutral-secondary); font-size: 13px; }
    .kcard2 { position: relative; display: grid; gap: 4px; align-content: start; padding: 14px 16px; border-radius: var(--radius); background: var(--white); border: 1px solid var(--md3-surface-variant); }
    .kcard2 .lab { color: var(--ink); padding-right: 32px; }
    .kcard2 .ki { position: absolute; top: 12px; right: 12px; width: 32px; height: 32px; border-radius: 8px; display: grid; place-items: center; background: var(--md3-background); color: var(--md3-on-primary-container); }
    .kcard2 b { font-size: 24px; line-height: 1.2; font-weight: 600; color: var(--head); font-variant-numeric: tabular-nums; }
    .kcard2 .sup { font-size: 13px; color: var(--md3-neutral-secondary); }
    .kd { justify-self: start; font-size: 13px; font-weight: 600; }
    .kd.same { color: var(--md3-neutral-secondary); font-weight: 500; } .kd.good { color: #1E6B3C; } .kd.bad { color: #8A5A00; }
    .kattn__l { display: inline-flex; align-items: center; gap: 6px; font-weight: 600; margin-right: 2px; }
    .kattn__i { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 0 6px; border-radius: 8px; background: transparent; color: #6B4E00; font: inherit; font-size: 14px; font-weight: 500; text-decoration: underline; text-underline-offset: 3px; text-decoration-color: rgba(107,78,0,.35); }
    .kattn__i small { text-decoration: none; display: inline-flex; height: 22px; align-items: center; padding: 0 6px; border-radius: 4px; background: #FFE9A8; font-size: 12px; }
    .kattn { display: flex; align-items: center; flex-wrap: wrap; gap: 0 2px; padding: 4px 8px 4px 14px; border-radius: var(--radius); background: #FFF6DB; color: #6B4E00; }
    .kattn svg { flex: none; margin-top: 1px; }
    .kattn b { font-weight: 600; }
    .kfollow { display: grid; gap: 20px; padding-top: 16px; border-top: 1px solid var(--md3-surface-variant); }
    .kpanel__h { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
    .kseg.two { grid-template-columns: repeat(2, auto); }
    .kseg button { min-height: 44px; padding: 0 14px; }
    .ktabwrap { overflow-x: auto; }
    .ktab td small { display: block; color: var(--md3-neutral-secondary); font-size: 13px; }
    .ktab td b { font-weight: 600; }
    .kchip { display: inline-flex; align-items: center; height: 26px; padding: 0 10px; border-radius: 6px; font-size: 13px; font-weight: 500; white-space: nowrap; background: var(--md3-surface-variant); color: var(--md3-on-primary-container); }
    .kchip.ok { background: #E3F4EA; color: #1E6B3C; } .kchip.bad { background: #FBE4E8; color: #A3122E; } .kchip.warn { background: #FFF1CC; color: #7A5600; }
    .kwait { font-variant-numeric: tabular-nums; white-space: nowrap; } .kwait.late { color: #8A5A00; font-weight: 600; }
    .kmore { justify-self: start; min-height: 44px; }
    .kfr.kqty { flex-wrap: wrap; padding: 8px 14px; }
    .kqchips { display: flex; flex-wrap: wrap; gap: 6px; }
    @media (orientation: landscape) {
      .ksum { grid-template-columns: repeat(4, minmax(0, 1fr)); }
      .drow__b { grid-template-columns: 280px minmax(0, 1fr); gap: 24px; }
      .kfs, .kfs.k3 { grid-template-columns: minmax(0, 1fr); }
      .kpanels2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    /* Prep Sheet */
    .pspane { display: grid; gap: 16px; max-width: 1080px; margin: 0 auto; }
    .pscard { gap: 14px; }
    .psdate { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; justify-content: space-between; }
    .psseg { flex: 1 1 320px; max-width: 460px; }
    .psday { display: inline-flex; align-items: center; gap: 6px; color: var(--head); }
    .psdates, .psfilters { display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .psf { display: grid; gap: 4px; }
    .psf span { color: var(--ink); }
    .psf select, .psf input { height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--head); font: inherit; }
    .psapplied { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    .pschip { display: inline-flex; align-items: center; gap: 4px; min-height: 36px; padding: 0 4px 0 12px; border-radius: 18px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .pschip button { width: 44px; height: 44px; margin: -4px -4px -4px 0; display: grid; place-items: center; border-radius: 22px; }
    .psapplied .linkbtn { min-height: 44px; }
    .drow__h.psh { align-items: center; flex-wrap: wrap; }
    .psbar { display: inline-flex; align-items: center; gap: 10px; flex-wrap: wrap; justify-content: flex-end; }
    .ksm { min-height: 44px; }
    .psfresh { display: inline-flex; align-items: center; gap: 6px; height: 32px; padding: 0 12px; border-radius: 16px; background: var(--neutral05); color: var(--ink); }
    .psfresh.busy { background: #FFF6DB; color: #6B4E00; }
    .pspin { width: 14px; height: 14px; border-radius: 50%; border: 2px solid rgba(107,78,0,.3); border-top-color: #6B4E00; animation: aispin .8s linear infinite; }
    @keyframes aispin { to { transform: rotate(360deg); } }
    @media (prefers-reduced-motion: reduce) { .pspin { animation: none; } }
    .psro { color: var(--md3-neutral-secondary); }
    .pswrap { overflow-x: auto; }
    .pstab { width: 100%; border-collapse: collapse; }
    .pstab th { text-align: left; font-size: 12px; font-weight: 600; color: var(--ink); padding: 0 10px 6px; border-bottom: 1px solid var(--md3-surface-variant); }
    .pstab th.r { text-align: right; }
    .pssort { min-height: 44px; font: inherit; font-weight: 600; color: var(--ink); }
    .pstab td { padding: 12px 10px; border-bottom: 1px solid var(--line); color: var(--head); vertical-align: top; }
    .pstab tr:last-child td { border-bottom: 0; }
    .pstab td small { display: block; color: var(--md3-neutral-secondary); }
    .pstab td small.u { display: inline; }
    .pstab .r { text-align: right; font-variant-numeric: tabular-nums; }
    .pstags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
    .pstag { display: inline-flex; align-items: center; min-height: 28px; padding: 0 10px; border-radius: 6px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); font-size: 13px; }
    a.pstag { min-height: 32px; }
    .pstag.alt { background: #FFF6DB; color: #6B4E00; }
    @media (orientation: landscape) { .psfilters { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
    /* Meal Group Management: tiles in the Modules tile style, smaller */
    .mgtiles { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 16px; padding-top: 16px; }
    .mgtile {
      display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; height: 132px; padding: 12px;
      background: var(--white); border-radius: 12px; box-shadow: 0 1px 2px rgba(31,65,91,.04); color: #425349; text-align: center;
      -webkit-tap-highlight-color: transparent; touch-action: manipulation; user-select: none; -webkit-user-select: none;
      transition: transform 160ms var(--ease), box-shadow 220ms var(--ease), background-color 220ms var(--ease);
    }
    .mgtile svg { width: 44px; height: 44px; }
    .mgtile span { font-size: 16px; line-height: 1.2; font-weight: 600; letter-spacing: -.012em; }
    @media (hover: hover) { .mgtile:hover { box-shadow: 0 2px 4px rgba(31,65,91,.06), 0 8px 18px rgba(31,65,91,.07); } }
    .mgtile:active { transform: scale(.98); background: #F5FAF7; }
    .mgtile:focus-visible { outline-offset: 3px; }
    @media (orientation: landscape) { .mgtiles { grid-template-columns: repeat(4, minmax(0, 1fr)); } }
    @media (prefers-reduced-motion: reduce) { .mgtile { transition: none; } .mgtile:active { transform: none; } }
    .toast { position: fixed; left: 50%; bottom: 32px; z-index: 40; transform: translate(-50%, 16px); opacity: 0; pointer-events: none;
      max-width: calc(100% - 32px); padding: 12px 20px; border-radius: 8px; background: var(--md3-on-primary-container); color: var(--white);
      transition: opacity 200ms var(--ease), transform 200ms var(--ease); }
    .toast.on { opacity: 1; transform: translate(-50%, 0); }
'''

KITCHEN_JS = r'''  var DD = __KDASH__;
  var REQ_SEED = __REQSEED__;
  /* ---------------- viewing as (same 4 roles as diet-home.html, shared through localStorage) ---------------- */
  var USERS = [
    { key: 'dietician', name: 'Hydar Ali', title: 'Dietician', role: 'DIETICIAN', what: 'Raises requests. Sees My requests only.' },
    { key: 'head-dietician', name: 'Dr. Meera Iyer', title: 'Head Dietician', role: 'DIET_MANAGER', prd: 'Diet Manager', what: 'Raises, reviews and configures requests. Edits diets.' },
    { key: 'kitchen-head', name: 'Suresh Gowda', title: 'Kitchen Head', role: 'KITCHEN_HEAD', what: 'Kitchen review: delay, ask for adjustment, send to prep (prototype grant).' },
    { key: 'kitchen-operator', name: 'Anil Kumar', title: 'Kitchen Operator', role: 'KITCHEN_OPERATOR', what: 'Requests sent to prep and Meal Group Management. No Kitchen Dashboard, no Diet module.' } ];
  var VIEWER = (function () { var a = new URLSearchParams(location.search).get('as'), sv = savedViewer(), ok = function (k) { return USERS.some(function (u) { return u.key === k; }); }; return USERS.filter(function (u) { return u.key === (ok(a) ? a : ok(sv) ? sv : 'kitchen-head'); })[0]; })();
  function isKitchen() { return VIEWER.role === 'KITCHEN_HEAD' || VIEWER.role === 'KITCHEN_OPERATOR'; }
  function initials(n) { return String(n).replace(/^Dr\.?\s+/i, '').split(/\s+/).slice(0, 2).map(function (w) { return w[0].toUpperCase(); }).join(''); }
  var RS = document.getElementById('rqsheet');
  function applyViewer(silent) {
    saveViewer(VIEWER.key); guardModule('kitchen', VIEWER);
    try { var q = new URLSearchParams(location.search); q.set('as', VIEWER.key); history.replaceState(history.state, '', location.pathname + '?' + q.toString() + location.hash); } catch (x) {}
    [].forEach.call(document.querySelectorAll('a[data-aslink]'), function (a) { a.setAttribute('href', a.getAttribute('data-aslink') + '?as=' + VIEWER.key); });
    [].forEach.call(document.querySelectorAll('.asbtn'), function (b) { b.innerHTML = ic('user', 20) + '<span class="t-body-medium">Viewing as: ' + esc(VIEWER.name) + ' <small>· ' + esc(VIEWER.title) + '</small></span>' + ic('dropdown', 18); });
    drawDash(); if (typeof drawPS === 'function' && !document.getElementById('pspanel').hidden) drawPS(); if (typeof drawMG === 'function' && !document.getElementById('mgpanel').hidden) { if (!MGS.hidden) mgClose(); drawMG(); } if (typeof route === 'function' && document.getElementById('p-requests')) route(); if (!silent) toast('Viewing as: ' + VIEWER.title + ', ' + VIEWER.name);
  }
  function openRoles() {
    RS.querySelector('.sheet').innerHTML = '<div class="grab"></div><div class="sheet__h"><div><h2 class="t-major-title" id="rsT">Viewing as</h2><p class="t-body-regular" style="color:var(--ink)">Demo only. Switch role to see what each one can do.</p></div><button type="button" class="iconbtn" data-rsclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
      '<div class="roles" role="radiogroup" aria-label="Role">' + USERS.map(function (u) { return '<button type="button" class="role" role="radio" data-as="' + u.key + '" aria-checked="' + (u === VIEWER) + '"><span class="av">' + initials(u.name) + '</span><span class="grow"><b class="t-minor-title">' + esc(u.title) + '</b><span class="t-body-regular">' + esc(u.name) + (u.prd ? ' · PRD role name: ' + u.prd : '') + '</span><small class="t-body-regular">' + esc(u.what) + '</small></span>' + (u === VIEWER ? ic('just-tick-mark', 22) : '') + '</button>'; }).join('') + '</div>' +
      '<button type="button" class="linkbtn t-body-medium rqreset" data-rqreset>' + ic('history', 18) + 'Reset demo data</button>';
    RS.hidden = false;
  }
  RS.addEventListener('click', function (e) {
    var t;
    if (e.target === RS || e.target.closest('[data-rsclose]')) { RS.hidden = true; return; }
    if (e.target.closest('[data-rqreset]')) { if (window.confirm('Reset the demo data? Request changes are cleared on both pages.')) resetDemo(); return; }
    if ((t = e.target.closest('[data-as]'))) { VIEWER = USERS.filter(function (u) { return u.key === t.getAttribute('data-as'); })[0]; RS.hidden = true; applyViewer(); }
  });
  document.addEventListener('click', function (e) { if (e.target.closest('.asbtn')) openRoles(); });
  var toastT;
  function toast(msg) { var t = document.getElementById('toast'); t.textContent = msg; t.classList.remove('act'); t.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove('on'); }, 2400); }

  /* ---------------- tabs (#dashboard, #meal-groups) ---------------- */
  /* Kitchen Head: Dashboard | Meal Group Management. Kitchen Operator: Requests | Meal Group Management (no Dashboard). */
  var ALLKEYS = ['requests', 'dashboard', 'meal-groups'];
  function isOperator() { return VIEWER.role === 'KITCHEN_OPERATOR'; }
  function tabKeys() { return isOperator() ? ['requests', 'meal-groups'] : ['dashboard', 'meal-groups']; }
  function curTab() { var h = location.hash.replace(/^#/, '').split('/')[0], K = tabKeys(); return K.indexOf(h) !== -1 ? h : K[0]; }
  function route() { var t = curTab(), K = tabKeys(); ALLKEYS.forEach(function (k) { var tb = document.getElementById('t-' + k); tb.hidden = K.indexOf(k) === -1; tb.setAttribute('aria-selected', String(k === t)); document.getElementById('p-' + k).hidden = k !== t; });
    if (t === 'requests') drawReqs();
    if (t === 'dashboard' && typeof drawDash === 'function' && dashView() !== DS.view) { DS.view = dashView(); drawDash(); var mn = document.getElementById('main'); if (mn) mn.scrollTop = 0; }
    var ps = location.hash === '#meal-groups/prep-sheet', pan = document.getElementById('pspanel'); if (ps) { drawPS(); pan.hidden = false; } else { pan.hidden = true; PSPUSHED = false; } }
  window.addEventListener('hashchange', route);
  document.querySelector('.mtabs').addEventListener('click', function (e) { var a = e.target.closest('.mtab'); if (!a) return; e.preventDefault(); location.hash = a.getAttribute('href'); });

  /* ---------------- Kitchen Dashboard ---------------- */
  var PRI = { high: ['!!!', 'High priority', 0], medium: ['!!', 'Medium priority', 1], low: ['!', 'Low priority', 2] };
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function fmtD(iso) { var p = String(iso || '').slice(0, 10).split('-'); return p.length === 3 ? Number(p[2]) + ' ' + MON[Number(p[1]) - 1] + ' ' + p[0] : ''; }
  function fmtN(n) { return Number(n).toLocaleString('en-IN', { maximumFractionDigits: 2 }); }
  var GR = [['today', 'Today'], ['week', 'This week'], ['month', 'This month'], ['custom', 'Custom']];
  var DS = { grain: 'today', wh: '', rev: 'latest', more: {}, view: 'overview' };
  function dashView() { return location.hash === '#dashboard/followups' ? 'followups' : 'overview'; }
  var KST = __KSTK__;
  /* every figure below is worked out from the SAMPLE DATA receipts for the chosen period and warehouse */
  var UO = ['kg', 'ltr', 'nos'];
  function dayList(f, t) { var out = [], d = new Date(f + 'T00:00:00'), e = new Date(t + 'T00:00:00'); while (d <= e) { out.push(d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2)); d.setDate(d.getDate() + 1); } return out; }
  function shortD(iso) { var p = iso.split('-'); return Number(p[2]) + ' ' + MON[Number(p[1]) - 1]; }
  var CACHE = {};
  function per() {
    var key = DS.grain + '|' + DS.wh; if (CACHE[key]) return CACHE[key];
    var P = DD.periods[DS.grain], rs = DD.receipts.filter(function (r) { return r.date >= P.from && r.date <= P.to && (!DS.wh || r.warehouse === DS.wh); });
    var hasRet = function (r) { return r.lines.some(function (l) { return l.returned > 0; }); }, items = {}, sup = {}, q = {}, ti = {}, rr = {};
    rs.forEach(function (r) {
      var s = sup[r.supplier] = sup[r.supplier] || { name: r.supplier, receipts: 0, ret: 0, acc: [] }; s.receipts++; if (hasRet(r)) s.ret++;
      r.lines.forEach(function (l) { items[l.item] = 1; var u = q[l.unit] = q[l.unit] || { unit: l.unit, received: 0, returned: 0 }; u.received += l.received; u.returned += l.returned; s.acc.push(l.received / ((l.received + l.returned) || 1));
        if (l.returned) { var t = ti[l.item] = ti[l.item] || { name: l.item, unit: l.unit, qty: 0 }; t.qty += l.returned; rr[l.reason] = (rr[l.reason] || 0) + 1; } });
    });
    var suppliers = Object.keys(sup).map(function (k) { var s = sup[k], acc = s.acc.reduce(function (a, b) { return a + b; }, 0) / (s.acc.length || 1) * 100; return { name: s.name, receipts: s.receipts, returnRate: (s.ret / s.receipts * 100).toFixed(1) + '%', rate: s.ret / s.receipts * 100, acc: Math.round(acc * 10) / 10 }; })
      .sort(function (a, b) { return b.receipts - a.receipts || b.acc - a.acc || a.name.localeCompare(b.name); });
    var nret = rs.filter(hasRet).length;
    return CACHE[key] = {
      label: P.from === P.to ? fmtD(P.from) : shortD(P.from) + ' to ' + fmtD(P.to),
      kpis: { receipts: rs.length, products: Object.keys(items).length, suppliers: suppliers.length, returns: nret, returnedLines: Object.keys(ti).length },
      quantities: UO.map(function (u) { return q[u] || { unit: u, received: 0, returned: 0 }; }).concat(Object.keys(q).filter(function (u) { return UO.indexOf(u) === -1; }).map(function (u) { return q[u]; })),
      trend: dayList(P.from, P.to).map(function (d) { var day = rs.filter(function (r) { return r.date === d; }); return { date: shortD(d), receipts: day.length, withReturns: day.filter(hasRet).length }; }),
      topReturned: Object.keys(ti).map(function (k) { return ti[k]; }).sort(function (a, b) { return b.qty - a.qty; }),
      returnReasons: Object.keys(rr).map(function (k) { return { reason: k, lines: rr[k] }; }).sort(function (a, b) { return b.lines - a.lines || a.reason.localeCompare(b.reason); }),
      suppliers: suppliers,
      topReceived: (function () { var t = {}; rs.forEach(function (r) { r.lines.forEach(function (l) { if (l.unit === 'kg' && l.received) { var x = t[l.item] = t[l.item] || { name: l.item, unit: 'kg', qty: 0 }; x.qty += l.received; } }); }); return Object.keys(t).map(function (k) { return t[k]; }).sort(function (a, b) { return b.qty - a.qty || a.name.localeCompare(b.name); }).slice(0, 8); })(),
      receipts: rs.slice().sort(function (a, b) { return (b.date + b.time).localeCompare(a.date + a.time); }) };
  }
  function pd(k) { return per()[k] || []; }
  /* Source KPI cards: Receipts, Products on receipts, Suppliers, Receipts with rejections, each compared with the
     previous period of the same length (today vs yesterday, this week vs the 5 days before, and so on) */
  function kpisFor(f, t) {
    var rs = DD.receipts.filter(function (r) { return r.date >= f && r.date <= t && (!DS.wh || r.warehouse === DS.wh); }), it = {}, su = {}, rl = 0, rr = 0;
    rs.forEach(function (r) { su[r.supplier] = 1; var ret = false; r.lines.forEach(function (l) { it[l.item] = 1; if (l.returned > 0) { rl++; ret = true; } }); if (ret) rr++; });
    return { receipts: rs.length, products: Object.keys(it).length, suppliers: Object.keys(su).length, rejected: rr, retLines: rl };
  }
  function prevRange() { var P = DD.periods[DS.grain], n = dayList(P.from, P.to).length, d = new Date(P.from + 'T00:00:00'); d.setDate(d.getDate() - 1);
    var to = isoD(d); d.setDate(d.getDate() - (n - 1)); return { from: isoD(d), to: to }; }
  function delta(cur, prev, upBad) {
    if (cur === prev) return '<span class="kd same">No change</span>';
    if (!prev) return '<span class="kd ' + (upBad ? 'bad' : 'good') + '">↑ from 0</span>';
    var p = Math.abs((cur - prev) / prev * 100).toFixed(1), up = cur > prev;
    return '<span class="kd ' + (up === !upBad ? 'good' : 'bad') + '">' + (up ? '↑ ' : '↓ ') + p + '%</span>';
  }
  function kpiRow() {
    var P = DD.periods[DS.grain], R = prevRange(), c = kpisFor(P.from, P.to), p = kpisFor(R.from, R.to);
    var pct = c.receipts ? (Math.round(c.rejected / c.receipts * 1000) / 10) + '% of receipts, ' : '';
    var card = function (lab, icon, v, d, sub) { return '<div class="kcard2"><span class="lab t-body-medium">' + lab + '</span><span class="ki">' + ic(icon, 20) + '</span><b>' + fmtN(v) + '</b>' + d + '<span class="sup">' + sub + '</span></div>'; };
    var rng = R.from === R.to ? fmtD(R.from) : shortD(R.from) + ' to ' + fmtD(R.to);
    return '<section class="kkpis" aria-labelledby="kkpiT"><div class="kkpis__h"><h3 class="t-body-title" id="kkpiT">Receiving in this period</h3><span class="t-body-regular">' + esc(per().label) + '</span></div>' +
      '<div class="ksum k2">' + card('Receipts', 'list', c.receipts, delta(c.receipts, p.receipts), 'Goods receipts in this period') +
        card('Products on receipts', 'grid', c.products, delta(c.products, p.products), 'Distinct products, including rejected lines') +
        card('Suppliers', 'user', c.suppliers, delta(c.suppliers, p.suppliers), 'Vendors with receipts in this period') +
        card('Receipts with rejections', 'transfer', c.rejected, delta(c.rejected, p.rejected, true), pct + plural2(c.retLines, 'returned line')) + '</div>' +
      '<p class="kcap t-body-regular">' + ic('info', 16) + 'Changes compare with ' + esc(rng) + '.' + (p.receipts ? '' : ' No receipts were recorded then.') + ' The current period may still be in progress.</p></section>';
  }
  function reqs() { var s = storedReqs(); return s ? s.reqs : REQ_SEED; }
  function dietLink(q, id) { return 'diet-home.html?as=' + VIEWER.key + (q ? '&kq=' + q : '') + '#request' + (id ? '/' + id : ''); }
  function hbars(list) { var mx = Math.max.apply(null, list.map(function (x) { return x.qty != null ? x.qty : x.lines; }).concat([1]));
    return list.length ? '<div class="hbars">' + list.map(function (x) { var v = x.qty != null ? x.qty : x.lines; return '<div class="hbar t-body-regular"><span title="' + esc(x.name || x.reason) + '">' + esc((x.name || x.reason) + (x.unit ? ' (' + x.unit + ')' : '')) + '</span><i style="width:' + Math.max(3, v / mx * 100) + '%"></i><b>' + fmtN(v) + '</b></div>'; }).join('') + '</div>' : '<p class="kempty t-body-regular">Nothing in this period.</p>'; }
  function rowH(title, desc, chip) { return '<div class="drow__h"><div><h3 class="t-minor-title">' + title + '</h3><p class="t-body-regular">' + desc + '</p></div><span class="per">' + esc(chip || per().label || '') + '</span></div>'; }
  function kfr(label, val, o) { o = o || {}; var cls = (o.alert ? ' alert' : '') + (o.wide ? ' wide' : ''); var inner = '<span class="t-body-medium">' + label + '</span><b>' + val + '</b>'; return o.href ? '<a class="kfr' + cls + '" href="' + o.href + '">' + inner + '</a>' : '<div class="kfr' + cls + '">' + inner + '</div>'; }
  /* Follow-ups (source "Follow-ups & receipts" tab): challans waiting, oldest first, waiting time from the SAMPLE clock */
  var NOW = new Date(KST.now + ':00'), MONS = { Jan: 0, Feb: 1, Mar: 2, Apr: 3, May: 4, Jun: 5, Jul: 6, Aug: 7, Sep: 8, Sept: 8, Oct: 9, Nov: 10, Dec: 11 };
  function arrivedAt(s) { var m = /^(\d+) (\w+), (\d+):(\d+)$/.exec(s || ''); return m ? new Date(NOW.getFullYear(), MONS[m[2]], +m[1], +m[3], +m[4]) : NOW; }
  function waitLab(ms) { var mi = Math.max(0, Math.round(ms / 60000)), h = Math.floor(mi / 60), d = Math.floor(h / 24); return d ? d + ' d ' + (h % 24) + ' h' : h ? h + ' h ' + (mi % 60) + ' min' : mi + ' min'; }
  function pending() { return DD.pending.filter(function (r) { return !DS.wh || r.warehouse === DS.wh; }).map(function (r) { var a = arrivedAt(r.arrived); return { dc: r.dc, vehicle: (KST.vehicles || {})[r.dc] || '', vendor: r.vendor, warehouse: r.warehouse, arrived: r.arrived, ms: NOW - a }; }).sort(function (a, b) { return b.ms - a.ms; }); }
  /* Current stock (source "Current stock" + "Expiry watchlist"): recorded now, independent of the receiving period */
  function stockNow() {
    var today = KST.now.slice(0, 10), lim = (function () { var d = new Date(today + 'T00:00:00'); d.setDate(d.getDate() + (KST.expiryDays || 7)); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); })();
    var bs = KST.batches.filter(function (b) { return !DS.wh || b.warehouse === DS.wh; }), ins = bs.filter(function (b) { return b.status === 'in_store'; });
    var good = ins.filter(function (b) { return b.expires >= today; }), q = {};
    good.forEach(function (b) { q[b.unit] = (q[b.unit] || 0) + b.qty; });
    var watch = ins.filter(function (b) { return b.expires <= lim; }).map(function (b) { return { item: b.item, batch: b.batch, warehouse: b.warehouse, qty: b.qty, unit: b.unit, expires: b.expires, expired: b.expires < today }; }).sort(function (a, b) { return a.expires.localeCompare(b.expires) || a.item.localeCompare(b.item); });
    return { products: good.map(function (b) { return b.item; }).filter(function (v, i, a) { return a.indexOf(v) === i; }).length, containers: ins.length,
      expired: watch.filter(function (w) { return w.expired; }).length, soon: watch.filter(function (w) { return !w.expired; }).length, transit: bs.filter(function (b) { return b.status === 'in_transit'; }).length,
      qty: ['kg', 'ltr', 'g', 'pcs'].filter(function (u) { return q[u]; }).map(function (u) { return { unit: u, qty: Math.round(q[u] * 100) / 100 }; }), watch: watch, through: fmtD(lim), days: KST.expiryDays || 7 };
  }
  function capList(key, list, n) { var open = DS.more[key] || list.length <= n + 1; return { rows: open ? list : list.slice(0, n), more: list.length > n + 1 ? '<button type="button" class="linkbtn t-body-medium kmore" data-kmore="' + key + '" aria-expanded="' + !!open + '">' + (open ? 'Show fewer' : 'Show all ' + list.length) + '</button>' : '' }; }
  function attn(m) {
    var a = [];
    if (m.pendList.length) a.push('<button type="button" class="kattn__i" data-kgo="followups">' + plural2(m.pendList.length, 'pending challan') + ' <small>All dates</small></button>');
    if (m.missAll) a.push('<button type="button" class="kattn__i" data-kgo="missing">' + plural2(m.missAll, 'missing signed DC') + ' <small>All dates</small></button>');
    if (m.stk.expired) a.push('<button type="button" class="kattn__i" data-kgo="expiry">' + m.stk.expired + ' expired, view watchlist</button>');
    return a.length ? '<div class="kattn" role="status"><span class="kattn__l t-body-medium">' + ic('alert', 18) + 'Needs attention</span>' + a.join('') + '</div>' : '';
  }
  function plural2(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }
  function model() {
    var all = reqs(), c = function (s) { return all.filter(function (r) { return r.status === s; }).length; };
    var k = per().kpis || DD.kpis, q = pd('quantities'), su = pd('suppliers').slice().sort(function (a, b) { return b.receipts - a.receipts || a.name.localeCompare(b.name); });
    var acc = su.length ? su.reduce(function (n, x) { return n + x.acc; }, 0) / su.length : 0;
    return { kr: c('kitchen_review'), dl: c('delayed'), ad: c('adjustment'), rd: c('ready'), all: all, k: k, q: q, su: su, acc: Math.round(acc * 10) / 10,
      pendList: pending(), missAll: DD.receipts.filter(function (r) { return !r.signedDc && (!DS.wh || r.warehouse === DS.wh); }).length, stk: stockNow(),
      pend: DD.pending.filter(function (r) { return !DS.wh || r.warehouse === DS.wh; }).length, rate: k.receipts ? Math.round(k.returns / k.receipts * 1000) / 10 : 0 };
  }
  function summary(m) {
    var stage = m.kr + m.dl + m.ad + m.rd, kg = m.q.filter(function (x) { return x.unit === 'kg'; })[0];
    var retQ = m.q.filter(function (x) { return x.returned; });
    return '<section class="ksum" aria-label="Summary">' +
      '<a class="scard" href="' + dietLink('check') + '" aria-label="Diet requests: ' + stage + ' at kitchen stage, open"><span class="lab">' + ic('reason-or-list', 20) + 'Diet requests<span class="chev">' + ic('back', 18).replace('<svg', '<svg style="transform:rotate(180deg)"') + '</span></span><b>' + stage + '<small>at kitchen stage</small></b><span class="sup">' + m.kr + ' to check, ' + (m.dl ? '<span class="alertx">' + m.dl + ' delayed</span>' : '0 delayed') + '</span></a>' +
      '<div class="scard"><span class="lab">' + ic('list', 20) + 'Receiving</span><b>' + fmtN(m.k.receipts) + '<small>' + (m.k.receipts === 1 ? 'receipt' : 'receipts') + '</small></b><span class="sup">' + (kg ? fmtN(kg.received) + ' kg received' : 'Nothing received in kg') + '</span></div>' +
      '<div class="scard"><span class="lab">' + ic('transfer', 20) + 'Returns</span><b>' + fmtN(m.k.returns) + '<small>' + (m.k.returns === 1 ? 'receipt with returns' : 'receipts with returns') + '</small></b><span class="sup">' + (retQ.length ? retQ.map(function (x) { return fmtN(x.returned) + ' ' + x.unit; }).join(', ') + ' returned' : 'Nothing returned') + '</span></div>' +
      '<div class="scard"><span class="lab">' + ic('user', 20) + 'Vendor performance</span><b>' + fmtN(m.su.length) + '<small>active suppliers</small></b><span class="sup">' + m.acc + '% average acceptance</span></div></section>';
  }
  function dietRow(m) {
    var top = m.all.filter(function (r) { return r.status === 'kitchen_review' || r.status === 'delayed'; }).sort(function (a, b) { return PRI[a.prio][2] - PRI[b.prio][2] || String(a.iso).localeCompare(String(b.iso)); }).slice(0, 3);
    return '<section class="drow">' + rowH('Diet requests', 'Proposed diets at the kitchen stage, from the Diet Request flow.') + '<div class="drow__b"><div class="kfs">' +
      kfr('Kitchen review', m.kr, { href: dietLink('check:kreview') }) + kfr('Delayed', m.dl, { href: dietLink('check:kdelayed'), alert: m.dl > 0 }) + kfr('Needs adjustment', m.ad, { href: dietLink('all:kadjust') }) + kfr('Sent to prep', m.rd, { href: dietLink('ready') }) + '</div>' +
      '<div class="kpanel"><h4>Top requests by priority</h4>' + (top.length ? top.map(function (r) { var dl = r.status === 'delayed'; return '<a class="kitem" href="' + dietLink('', r.id) + '"><span class="ribbon ' + r.prio + '" aria-label="' + PRI[r.prio][1] + '">' + PRI[r.prio][0] + '</span><span class="grow"><b class="t-body-title">' + esc(r.id + ' · ' + r.title) + '</b><small class="t-body-regular">' + esc(r.sp + ', ' + (r.scopeText || 'Whole species')) + '</small></span><span class="st' + (dl ? ' alertx' : '') + '">' + (dl && r.delayUntil ? 'Delayed to ' + fmtD(r.delayUntil).replace(/ \d{4}$/, '') : 'Kitchen review') + '</span></a>'; }).join('') : '<p class="kempty t-body-regular">Nothing waiting on the kitchen.</p>') + '</div></div></section>';
  }
  function recvRow(m) {
    var tr = pd('trend'), mx = Math.max.apply(null, tr.map(function (t) { return t.receipts; }).concat([1])), miss = pd('receipts').filter(function (r) { return !r.signedDc; });
    return '<section class="drow">' + rowH('Receiving', 'Goods received into the kitchen stores. Challans and receipts to follow up are under Follow-ups &amp; receipts.') + '<div class="drow__b"><div class="kfs">' +
      m.q.map(function (x) { return kfr('Received (' + esc(x.unit) + ')', fmtN(x.received)); }).join('') + kfr('Pending challans', m.pend, { alert: m.pend > 0 }) + kfr('Missing signed DC', miss.length, { alert: miss.length > 0, wide: true }) + '</div>' +
      '<div class="kstack"><div class="kpanel"><h4>Receiving trend</h4><div class="bars' + (tr.length > 8 ? ' many' : '') + '" role="img" aria-label="Receipts per day">' + tr.map(function (t, i) { return '<div class="col"><div class="pair"><i style="height:' + (t.receipts / mx * 100) + '%" title="' + t.receipts + ' receipts"></i><i class="r" style="height:' + (t.withReturns / mx * 100) + '%" title="' + t.withReturns + ' with returns"></i></div><small>' + (tr.length > 8 && i % 4 !== 0 && i !== tr.length - 1 ? '&nbsp;' : esc(t.date)) + '</small></div>'; }).join('') + '</div>' +
      '<div class="legend"><span><i></i>Receipts</span><span><i class="r"></i>With returns</span></div></div>' +
      '<div class="kpanel"><h4>Top received items (kg)</h4>' + hbars(pd('topReceived')) + '</div></div></div></section>';
  }
  function followRows(m) {
    var rc = pd('receipts'), miss = rc.filter(function (r) { return !r.signedDc; }), revList = DS.rev === 'missing' ? miss : rc;
    var W = capList('wait', m.pendList, 4), R = capList('rev', revList, 5);
    var wait = '<section class="drow">' + rowH('Waiting to be received (' + m.pendList.length + ')', 'Pending delivery challans from all arrival dates, oldest first.', 'All dates') +
      (m.pendList.length ? '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>DC / Vehicle</th><th>Vendor</th><th>Warehouse</th><th>Arrived</th><th class="r">Waiting</th></tr></thead><tbody>' +
        W.rows.map(function (r) { return '<tr><td><b>' + esc(r.dc) + '</b><small>' + esc(r.vehicle) + '</small></td><td>' + esc(r.vendor) + '</td><td>' + esc(r.warehouse) + '</td><td>' + esc(r.arrived) + '</td><td class="r"><span class="kwait' + (r.ms > 864e5 ? ' late' : '') + '">' + waitLab(r.ms) + '</span></td></tr>'; }).join('') + '</tbody></table></div>' + W.more
        : '<p class="kempty t-body-regular">No delivery challans are waiting.</p>') + '</section>';
    var rev = '<section class="drow" id="krev">' + rowH('Receipts to review', 'Goods receipts in this period. Upload the signed delivery challan for any marked Missing.') + '<div class="kpanel__h"><div class="seg3 two kseg" role="tablist" aria-label="Receipts to review">' +
        '<button type="button" role="tab" class="t-body-medium" data-krev="latest" aria-selected="' + (DS.rev === 'latest') + '">Latest (' + rc.length + ')</button><button type="button" role="tab" class="t-body-medium" data-krev="missing" aria-selected="' + (DS.rev === 'missing') + '">Missing signed DC (' + miss.length + ')</button></div></div>' +
      (revList.length ? '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>GRN</th><th>Vendor</th><th>Warehouse</th><th>Received</th><th class="r">Lines</th><th>Signed DC</th></tr></thead><tbody>' +
        R.rows.map(function (r) { return '<tr><td><b>' + esc(r.grn) + '</b></td><td>' + esc(r.supplier) + '</td><td>' + esc(r.warehouse) + '</td><td>' + esc(shortD(r.date) + ', ' + r.time) + '</td><td class="r">' + r.lines.length + '</td><td>' + (r.signedDc ? '<span class="kchip ok">Uploaded</span>' : '<span class="kchip bad">Missing</span>') + '</td></tr>'; }).join('') + '</tbody></table></div>' + R.more
        : '<p class="kempty t-body-regular">' + (DS.rev === 'missing' ? 'Every receipt in this period has a signed DC.' : 'No receipts in this period. Try a different date range.') + '</p>') + '</section>';
    return wait + rev;
  }


  function retRow(m) {
    return '<section class="drow">' + rowH('Returns', 'Goods sent back to the supplier at receiving.') + '<div class="drow__b"><div class="kfs">' +
      kfr('Receipts with returns', fmtN(m.k.returns)) + kfr('Return rate', m.rate + '%') + kfr('Returned items', fmtN(m.k.returnedLines)) + kfr('Returned', (m.q.filter(function (x) { return x.returned; }).map(function (x) { return fmtN(x.returned) + ' ' + esc(x.unit); }).join(', ') || '0')) + '</div>' +
      '<div class="kpanels2"><div class="kpanel"><h4>Top returned items</h4>' + hbars(pd('topReturned')) + '</div><div class="kpanel"><h4>Return reasons</h4>' + hbars(pd('returnReasons')) + '</div></div></div></section>';
  }
  function vendRow(m) {
    var worst = m.su.slice().sort(function (a, b) { return (parseFloat(b.returnRate) || 0) - (parseFloat(a.returnRate) || 0); })[0];
    return '<section class="drow">' + rowH('Vendor performance', 'Suppliers by receipts in this period.') + '<div class="drow__b"><div class="kfs k3">' +
      kfr('Active suppliers', m.su.length) + kfr('Average acceptance', m.acc + '%') + (worst ? kfr('Highest return rate', esc(worst.returnRate)) : '') + '</div>' +
      '<div class="kpanel"><table class="ktab t-body-regular"><thead><tr><th>Supplier</th><th class="r">Receipts</th><th class="r">Return rate</th><th class="r">Acceptance</th></tr></thead><tbody>' + m.su.map(function (x) { var rr = parseFloat(x.returnRate) || 0; return '<tr><td>' + esc(x.name) + '</td><td class="r">' + x.receipts + '</td><td class="r' + (rr >= 50 ? ' hi' : '') + '">' + esc(x.returnRate) + '</td><td class="r">' + x.acc.toFixed(1) + '%</td></tr>'; }).join('') + '</tbody></table>' +
      '<p class="kcap">' + ic('info', 16) + 'Return rate is receipts with returns divided by all receipts. Acceptance is the share of each delivered line accepted at receiving. All receiving, returns and vendor figures are SAMPLE DATA.</p></div></div></section>';
  }
  function stockRow(m) {
    var S = m.stk, E = capList('exp', S.watch, 6);
    return '<section class="drow" id="kstock">' + rowH('Stock and expiry', 'Recorded stock in this warehouse selection, independent of the receiving period.', 'Now') + '<div class="drow__b"><div class="kfs">' +
      kfr('Products in store', S.products) + kfr('Containers in store', S.containers) + kfr('Expired containers', S.expired, { alert: S.expired > 0 }) + kfr('Expiring in ' + S.days + ' days', S.soon, { alert: S.soon > 0 }) + kfr('Containers in transit', S.transit, { wide: true }) +
      '<div class="kfr wide kqty"><span class="t-body-medium">In-store quantity</span><span class="kqchips">' + (S.qty.length ? S.qty.map(function (q) { return '<span class="kchip">' + fmtN(q.qty) + ' ' + esc(q.unit) + '</span>'; }).join('') : 'No stock recorded') + '</span></div></div>' +
      '<div class="kpanel"><h4>Expiry watchlist</h4><p class="kcap t-body-regular">Expired stock and stock expiring through ' + esc(S.through) + ', earliest expiry first.</p>' +
        (S.watch.length ? '<div class="ktabwrap"><table class="ktab t-body-regular"><thead><tr><th>Product</th><th>Batch</th><th>Warehouse</th><th class="r">Quantity</th><th>Expires</th><th>Status</th></tr></thead><tbody>' +
          E.rows.map(function (w) { return '<tr><td><b>' + esc(w.item) + '</b></td><td>' + esc(w.batch) + '</td><td>' + esc(w.warehouse) + '</td><td class="r">' + fmtN(w.qty) + ' ' + esc(w.unit) + '</td><td>' + esc(shortD(w.expires)) + '</td><td>' + (w.expired ? '<span class="kchip bad">Expired</span>' : '<span class="kchip warn">Expiring</span>') + '</td></tr>'; }).join('') + '</tbody></table></div>' + E.more
          : '<p class="kempty t-body-regular">No expired or near-expiry stock recorded.</p>') +
      '<p class="kcap t-body-regular">' + ic('info', 16) + 'Expired and soon-to-expire counts are separate. In-transit containers are not in the in-store totals. Stock figures are SAMPLE DATA.</p></div></div></section>';
  }
  var dash = document.getElementById('p-dashboard');
  function drawDash() {
    var m = model();
    var fuN = m.pendList.length + pd('receipts').filter(function (r) { return !r.signedDc; }).length;
    dash.innerHTML = '<div class="segwrap kdseg"><div class="seg3" role="tablist" aria-label="Dashboard view"><button type="button" role="tab" class="t-body-medium" data-kview="overview" aria-selected="' + (DS.view === 'overview') + '">Overview</button><button type="button" role="tab" class="t-body-medium" data-kview="followups" aria-selected="' + (DS.view === 'followups') + '">Follow-ups &amp; receipts - ' + fuN + '</button></div></div>' +
      '<div class="kpane"><div class="kfilt" role="group" aria-label="Filters">' + GR.map(function (g) { return '<button type="button" class="spchip t-body-medium" data-kg="' + g[0] + '" aria-pressed="' + (DS.grain === g[0]) + '">' + g[1] + '</button>'; }).join('') +
        '<span class="sp"></span><label><span class="sr-only">Warehouse</span><select data-kw aria-label="Warehouse">' + DD.warehouses.map(function (w, i) { var v = i === 0 ? '' : w; return '<option value="' + esc(v) + '"' + (DS.wh === v ? ' selected' : '') + '>' + esc(w) + '</option>'; }).join('') + '</select></label></div>' +
      (DS.view === 'followups' ? followRows(m) : attn(m) + summary(m) + kpiRow() + dietRow(m) + recvRow(m) + retRow(m) + vendRow(m) + stockRow(m)) + '</div>';
  }
  dash.addEventListener('click', function (e) { var t; if ((t = e.target.closest('[data-kg]'))) { DS.grain = t.getAttribute('data-kg'); DS.more = {}; drawDash(); } if ((t = e.target.closest('[data-krev]'))) { DS.rev = t.getAttribute('data-krev'); DS.more.rev = false; drawDash(); } if ((t = e.target.closest('[data-kview]'))) { var v = t.getAttribute('data-kview'); if (v !== DS.view) location.hash = '#dashboard/' + v; return; }
    if ((t = e.target.closest('[data-kgo]'))) { var g = t.getAttribute('data-kgo'); if (g === 'expiry') { var st = document.getElementById('kstock'); if (st) st.scrollIntoView({ behavior: 'smooth', block: 'start' }); return; } if (g === 'missing') DS.rev = 'missing'; location.hash = '#dashboard/followups'; return; }
    if ((t = e.target.closest('[data-kmore]'))) { var k = t.getAttribute('data-kmore'); DS.more[k] = !DS.more[k]; drawDash(); } });
  dash.addEventListener('change', function (e) { if (e.target.matches('[data-kw]')) { DS.wh = e.target.value; drawDash(); } });
  window.addEventListener('pageshow', function () { drawDash(); });
  window.addEventListener('storage', function (e) { if (e.key === RQS_KEY || e.key === null) drawDash(); });

  /* ---------------- Kitchen Operator: Requests (read only) ----------------
     Every request the Kitchen Head sent to prep (status ready, or applied), from the shared request state. Items are the
     ones the stock check chose at Send to Prep (reqLines). Where it goes: Prep Sheet always; Packaging list and Packing
     Stations when the request's enclosure or section is found in their data. */
  var RV = { when: 'today', station: '', section: '' }, rqp = document.getElementById('p-requests');
  function reqWhere(r) {
    var name = r.scope === 'animal' ? String(r.scopeText || '').split(' · ').pop() : r.scopeText, out = { site: '', section: '', encl: '', stations: [] };
    var pl = MGSEED['packaging-list'], ps = MGP['packing-stations'] ? MGSTORE.get('packing-stations') : null;
    if (pl && name) pl.sites.some(function (s) { return s.sections.some(function (c) {
      if (r.scope === 'section' && c.name === name) { out.site = s.name; out.section = c.name; return true; }
      if ((r.scope === 'enclosure' || r.scope === 'animal') && c.encl.some(function (e) { return e[0] === name; })) { out.site = s.name; out.section = c.name; out.encl = name; return true; } }); });
    if (ps && out.section) ps.stations.forEach(function (st) { if (st.isActive === false) return; var hit = (ps.packages[st.id] || []).some(function (p) { return out.encl ? p.enc === out.encl : p.section === out.section; }); if (hit) out.stations.push({ id: st.id, name: st.name }); });
    return out;
  }
  function reqActive(r, day) { return r.start <= day && (!r.end || r.end >= day); }
  function drawReqs() {
    var today = isoD(new Date()), all = reqs().filter(function (r) { return r.status === 'ready' || r.status === 'applied'; }).map(function (r) { return { r: r, w: reqWhere(r) }; });
    var inWhen = function (x) { return RV.when === 'all' || (RV.when === 'today' ? reqActive(x.r, today) : x.r.start > today); };
    var stations = [], sections = [];
    all.forEach(function (x) { x.w.stations.forEach(function (s) { if (stations.indexOf(s.name) === -1) stations.push(s.name); }); if (x.w.section && sections.indexOf(x.w.section) === -1) sections.push(x.w.section); });
    var list = all.filter(function (x) { return inWhen(x) && (!RV.station || x.w.stations.some(function (s) { return s.name === RV.station; })) && (!RV.section || x.w.section === RV.section); })
      .sort(function (a, b) { return PRI[a.r.prio][2] - PRI[b.r.prio][2] || String(a.r.start).localeCompare(String(b.r.start)); });
    var n = { today: all.filter(function (x) { return reqActive(x.r, today); }).length, upcoming: all.filter(function (x) { return x.r.start > today; }).length, all: all.length };
    var sel = function (key, label, opts) { return opts.length ? '<label class="kfsel"><span class="sr-only">' + label + '</span><select data-rvf="' + key + '" aria-label="' + label + '"><option value="">All ' + label.toLowerCase() + 's</option>' + opts.sort().map(function (o) { return '<option' + (RV[key] === o ? ' selected' : '') + '>' + esc(o) + '</option>'; }).join('') + '</select></label>' : ''; };
    var focus = (/^#requests\/(DR-\d+)$/.exec(location.hash) || [])[1];
    var card = function (x) { var r = x.r, w = x.w, lines = reqLines(r);
      var dates = 'From ' + fmtD(r.start) + (r.end ? ' to ' + fmtD(r.end) : ', no end date');
      var items = lines.length ? lines.map(function (l) { return '<span class="rvitem' + (l.alt ? ' alt' : '') + '">' + esc(l.alt ? l.item + ' instead of ' + l.alt : l.item) + ' <small>' + fmtN(l.qty) + ' ' + esc(l.unit) + (l.prep ? ', ' + esc(l.prep) : '') + '</small></span>'; }).join('') : '<span class="kempty t-body-regular">No items recorded.</span>';
      var where = w.section ? esc(w.site.trim() + ' › ' + w.section + (w.encl ? ' › ' + w.encl : '')) + (w.stations.length ? ' · Packed at ' + esc(w.stations.map(function (s) { return s.name; }).join(', ')) : '') : 'Not in the packaging list data';
      return '<article class="drow rvcard' + (focus === r.id ? ' hl' : '') + '" id="rv-' + r.id + '"><div class="rvhead"><span class="ribbon ' + r.prio + '" aria-label="' + PRI[r.prio][1] + '">' + PRI[r.prio][0] + '</span><div class="grow"><h3 class="t-minor-title">' + esc(r.id + ' · ' + r.title) + '</h3><p class="t-body-regular">' + esc(r.sp + ', ' + (r.scopeText || 'Whole species')) + '</p></div><span class="kchip' + (r.status === 'ready' ? ' ok' : '') + '">' + (r.status === 'ready' ? 'Sent to prep' : 'Applied') + '</span></div>' +
        '<p class="rvmeta t-body-regular">' + ic('calendar', 16) + esc(dates) + '</p>' +
        '<div class="rvsec"><h4>Items to prep</h4><div class="rvitems">' + items + '</div></div>' +
        '<p class="rvmeta t-body-regular">' + ic('location-icon', 16) + where + '</p>' +
        '<div class="rvacts"><button type="button" class="btn pri ksm" data-rvps="' + r.id + '">Open in Prep Sheet</button>' +
          (w.section && MGP['packaging-list'] ? '<button type="button" class="btn sec ksm" data-rvpl="' + r.id + '">Packaging list</button>' : '') +
          (w.stations.length && MGP['packing-stations'] ? '<button type="button" class="btn sec ksm" data-rvst="' + w.stations[0].id + '">' + esc(w.stations[0].name.split(' - ')[0]) + ' in Packing Stations</button>' : '') + '</div></article>'; };
    rqp.innerHTML = '<div class="kpane"><div class="rvtop"><div class="seg3 rvseg" role="tablist" aria-label="When">' + [['today', 'Today'], ['upcoming', 'Upcoming'], ['all', 'All']].map(function (t) { return '<button type="button" role="tab" class="t-body-medium" data-rvw="' + t[0] + '" aria-selected="' + (RV.when === t[0]) + '">' + t[1] + ' - ' + n[t[0]] + '</button>'; }).join('') + '</div>' +
        '<div class="kfilt">' + sel('station', 'Station', stations) + sel('section', 'Section', sections) + '<span class="sp"></span><span class="kdate t-body-regular">' + ic('calendar', 16) + esc(dayLab(today)) + '</span></div></div>' +
      '<p class="kcap t-body-regular">' + ic('info', 16) + 'Diets the Kitchen Head sent to prep, with the items the stock check chose. Read only. Request lines are SAMPLE DATA.</p>' +
      (list.length ? list.map(card).join('') : '<div class="empty"><span class="ei">' + ic('list', 24) + '</span><b class="t-minor-title">Nothing sent to prep ' + (RV.when === 'today' ? 'for today' : RV.when === 'upcoming' ? 'that starts later' : 'yet') + '</b><span class="t-body-regular">When the Kitchen Head sends a request to prep, it shows here.</span></div>') + '</div>';
    if (focus) { var f = document.getElementById('rv-' + focus); if (f) setTimeout(function () { f.scrollIntoView({ block: 'center' }); }, 30); }
  }
  rqp.addEventListener('click', function (e) { var t, r;
    if ((t = e.target.closest('[data-rvw]'))) { RV.when = t.getAttribute('data-rvw'); drawReqs(); return; }
    if ((t = e.target.closest('[data-rvps]'))) { r = RQ_GET(t.getAttribute('data-rvps')); var today = isoD(new Date());
      if (r && reqActive(r, today)) PSS.range = 'today'; else if (r) { PSS.range = 'custom'; PSS.from = r.start; PSS.to = r.start; }
      PSS.site = PSS.sp = PSS.item = PSS.prep = ''; PSPUSHED = true; location.hash = '#meal-groups/prep-sheet'; return; }
    if ((t = e.target.closest('[data-rvpl]'))) { r = RQ_GET(t.getAttribute('data-rvpl')); var w = reqWhere(r); if (MGAPI.plOpen) MGAPI.plOpen(w.site, w.section); MGPUSHED = true; location.hash = '#meal-groups/packaging-list'; return; }
    if ((t = e.target.closest('[data-rvst]'))) { if (MGAPI.stationOpen) MGAPI.stationOpen(Number(t.getAttribute('data-rvst'))); MGPUSHED = true; location.hash = '#meal-groups/packing-stations'; }
  });
  rqp.addEventListener('change', function (e) { var t = e.target; if (t.matches('[data-rvf]')) { RV[t.getAttribute('data-rvf')] = t.value; drawReqs(); } });
  function RQ_GET(id) { return reqs().filter(function (r) { return r.id === id; })[0] || null; }

  /* ---------------- Meal Group Management: tiles, not wired yet ---------------- */
  var mgp = document.getElementById('p-meal-groups');
  mgp.innerHTML = __MG_HTML__;
  mgp.addEventListener('click', function (e) { var b = e.target.closest('[data-mg]'); if (!b) return; var g = b.getAttribute('data-mg'); if (g === 'prep-sheet') { PSPUSHED = true; location.hash = '#meal-groups/prep-sheet'; return; } if (MGP[g]) { MGPUSHED = true; location.hash = '#meal-groups/' + g; return; } toast(b.querySelector('span').textContent + ': coming soon'); });

  /* ---------------- Prep Sheet (Dev system kitchen/prep-sheet: date range, filters, freshness, table) ----------------
     Rows: the source rows (diet plans) plus every request that reached Sent to prep, for the days of its period that fall in
     the range, using the item actually chosen per line at acceptance (the Kitchen stock check). Shared request state comes
     from localStorage with the seed as fallback. */
  var PSD = __PSDATA__, PSCHED = __PSCHED__, PSPUSHED = false, PS_SITE = 'Antz site';   /* every prep line in this prototype belongs to the demo site */
  var PSS = { range: 'today', from: '', to: '', site: '', sp: '', item: '', prep: '', sort: 'name', dir: 1, computedAt: Date.now(), took: 0, busy: false };
  function isoD(d) { return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function addD(s, n) { var d = new Date(s + 'T00:00:00'); d.setDate(d.getDate() + n); return isoD(d); }
  function dayLab(s) { var d = new Date(s + 'T00:00:00'); return d.toLocaleDateString('en-GB', { weekday: 'short' }) + ' ' + fmtD(s); }
  function psRange() { var t = isoD(new Date()); if (PSS.range === 'tomorrow') return { from: addD(t, 1), to: addD(t, 1) }; if (PSS.range === 'custom') { var f = PSS.from || t, to = PSS.to && PSS.to >= f ? PSS.to : f; return { from: f, to: to }; } return { from: t, to: t }; }
  function activeDays(r, R) { var n = 0, d = R.from;
    while (d <= R.to && n < 400) {
      var on = false;
      if (r.season) { var md = d.slice(5), a = r.season.from, b = r.season.to; on = a <= b ? md >= a && md <= b : md >= a || md <= b; }
      else if (r.start) on = d >= r.start && (!r.end || d <= r.end);
      if (on) n++; d = addD(d, 1); }
    return n; }
  function pq(s) { var m = /^([0-9.]+)\s*(.*)$/.exec(s || ''); return m ? { qty: Number(m[1]), unit: m[2] } : null; }
  function reqLines(r) {
    var snap = r.kitchen && r.kitchen.accepted && r.kitchen.accepted.lines;
    if (snap) return snap.filter(function (l) { return !l.mix && l.chosen; }).map(function (l) { return { item: l.chosen.name, qty: l.chosen.need, unit: l.chosen.unit, prep: l.chosen.prep || ((l.cands || [])[0] || {}).prep || null, cut: l.chosen.cut || null, alt: l.status === 'alt' ? l.name : null }; });
    var out = [];
    (PSCHED[String(r.proposedId)] || []).forEach(function (b) { (b.days || []).forEach(function (g) { (g.items || []).forEach(function (x) { if (x.mix) return; var a = pq(x.amount); if (a) out.push({ item: x.name, qty: a.qty, unit: a.unit, prep: x.prep || null, cut: x.cut || null, alt: null }); }); }); });
    return out;
  }
  function pieceW(name, cut, prep) { var c = cut || (!prep || prep === 'Whole' ? 'Whole' : null); if (!c) return null; return mgPieceWeights().filter(function (p) { return p.status === 'set' && p.weight > 0 && p.name === name && (p.cutSize || 'Whole') === c; })[0] || null; }
  function codeOf(name) { var p = mgPieceWeights().filter(function (x) { return x.name === name; })[0]; return p ? p.code : ''; }
  function psRows() {
    var R = psRange(), m = {}, order = [];
    function add(name, cut, prep, amt, unit, src) { var k = [name, cut || '', prep || '', unit].join('|'); if (!m[k]) { m[k] = { name: name, code: codeOf(name), cut: cut, prep: prep, amount: 0, unit: unit, src: [], species: [] }; order.push(k); } m[k].amount += amt; if (src) { m[k].src.push(src); if (m[k].species.indexOf(src.sp) === -1) m[k].species.push(src.sp); } }
    var nd = 1; for (var d = R.from; d < R.to && nd < 400; d = addD(d, 1)) nd++;
    PSD.rows.forEach(function (r) { add(r.name, r.cutSize, r.prep, r.amount * nd, r.unit, null); });
    reqs().filter(function (r) { return r.status === 'ready' || r.status === 'applied'; }).forEach(function (r) { var n = activeDays(r, R); if (!n) return;
      reqLines(r).forEach(function (l) { add(l.item, l.cut, l.prep, l.qty * n, l.unit, { id: r.id, sp: r.sp, alt: l.alt ? l.item + ' for ' + l.alt : null, days: n }); }); });
    var rows = order.map(function (k) { var x = m[k], w = pieceW(x.name, x.cut, x.prep), g = { kg: 1000, g: 1 }[x.unit]; x.pieces = w && g ? Math.round(x.amount * g / w.weight) : null; return x; });
    return rows.filter(function (x) { return (!PSS.item || x.name === PSS.item) && (!PSS.prep || (x.prep || '') === PSS.prep) && (!PSS.sp || x.species.indexOf(PSS.sp) !== -1) && (!PSS.site || PSS.site === PS_SITE); })
      .sort(function (a, b) { var k = PSS.sort, va = k === 'name' ? a.name : a[k] == null ? -1 : a[k], vb = k === 'name' ? b.name : b[k] == null ? -1 : b[k]; return (va < vb ? -1 : va > vb ? 1 : 0) * PSS.dir; });
  }
  function psSel(key, label, opts) { return '<label class="psf"><span class="t-body-medium">' + label + '</span><select data-psf="' + key + '"><option value="">All</option>' + opts.map(function (o) { return '<option' + (PSS[key] === o ? ' selected' : '') + '>' + esc(o) + '</option>'; }).join('') + '</select></label>'; }
  function drawPS() {
    var R = psRange(), all = (function () { var k = { item: PSS.item, prep: PSS.prep, sp: PSS.sp }; PSS.item = PSS.prep = PSS.sp = ''; var a = psRows(); PSS.item = k.item; PSS.prep = k.prep; PSS.sp = k.sp; return a; })(), rows = psRows(), body = document.querySelector('#pspanel [data-psbody]');
    var uniq = function (a) { return a.filter(function (v, i) { return v && a.indexOf(v) === i; }).sort(); };
    var spOpts = uniq(PSD.species.concat([].concat.apply([], all.map(function (x) { return x.species; }))));
    var applied = [['site', 'Site'], ['sp', 'Species'], ['item', 'Item'], ['prep', 'Preparation']].filter(function (f) { return PSS[f[0]]; });
    var fromReq = rows.filter(function (x) { return x.src.length; }).length, canAct = isKitchen();
    var mins = Math.max(0, Math.round((Date.now() - PSS.computedAt) / 60000));
    var fresh = PSS.busy ? '<span class="psfresh busy t-body-medium"><i class="pspin" aria-hidden="true"></i>Rebuilding</span>' : '<span class="psfresh t-body-medium">' + ic('time', 16) + 'Computed ' + (mins < 1 ? 'just now' : mins + ' min ago') + (PSS.took ? ' · took ' + PSS.took + 's' : '') + '</span>';
    var TH = function (k, l, r) { return '<th' + (r ? ' class="r"' : '') + '>' + (k ? '<button type="button" class="pssort" data-pssort="' + k + '">' + l + (PSS.sort === k ? (PSS.dir > 0 ? ' ↑' : ' ↓') : '') + '</button>' : l) + '</th>'; };
    body.innerHTML = '<div class="pspane"><section class="drow pscard"><div class="psdate"><div class="seg3 psseg" role="tablist" aria-label="Date range">' + [['today', 'Today'], ['tomorrow', 'Tomorrow'], ['custom', 'Custom']].map(function (x) { return '<button type="button" role="tab" class="t-body-medium" data-psr="' + x[0] + '" aria-selected="' + (PSS.range === x[0]) + '">' + x[1] + '</button>'; }).join('') + '</div>' +
        '<span class="psday t-body-medium">' + ic('calendar', 18) + esc(R.from === R.to ? dayLab(R.from) : dayLab(R.from) + ' to ' + dayLab(R.to)) + '</span></div>' +
        (PSS.range === 'custom' ? '<div class="psdates"><label class="psf"><span class="t-body-medium">From</span><input type="date" data-psd="from" value="' + esc(R.from) + '"></label><label class="psf"><span class="t-body-medium">To</span><input type="date" data-psd="to" value="' + esc(R.to) + '"></label></div>' : '') +
        '<div class="psfilters">' + psSel('site', 'Site', uniq(PSD.sites.map(function (x) { return x.trim(); }))) + psSel('sp', 'Species', spOpts) + psSel('item', 'Diet item', uniq(all.map(function (x) { return x.name; }))) + psSel('prep', 'Preparation', uniq(all.map(function (x) { return x.prep; }))) + '</div>' +
        (applied.length ? '<div class="psapplied">' + applied.map(function (f) { return '<span class="pschip t-body-medium">' + f[1] + ': ' + esc(PSS[f[0]]) + '<button type="button" data-psrm="' + f[0] + '" aria-label="Remove ' + f[1] + ' filter">' + ic('close', 16) + '</button></span>'; }).join('') + '<button type="button" class="linkbtn t-body-medium" data-psclear>Clear all</button></div>' : '') + '</section>' +
      '<section class="drow"><div class="drow__h psh"><h3 class="t-minor-title">Items to prepare (' + rows.length + ')</h3><span class="psbar">' + fresh + (canAct ? '<button type="button" class="btn sec ksm" data-psrefresh' + (PSS.busy ? ' disabled' : '') + '>' + ic('history', 18) + 'Refresh</button>' : '<span class="t-body-regular psro">Read only</span>') + '</span></div>' +
        (fromReq ? '<p class="kcap t-body-regular">' + ic('info', 16) + fromReq + (fromReq === 1 ? ' line comes' : ' lines come') + ' from Diet Requests sent to prep (SAMPLE DATA). Each uses the item the stock check chose.</p>' : '') +
        (rows.length ? '<div class="pswrap"><table class="pstab t-body-regular"><thead><tr>' + TH('name', 'Item') + TH('', 'Cut size') + TH('', 'Prep') + TH('pieces', 'Pieces', true) + TH('amount', 'Amount', true) + '</tr></thead><tbody>' +
          rows.map(function (x) { return '<tr><td><b>' + esc(x.name) + '</b>' + (x.code ? '<small>' + esc(x.code) + '</small>' : '') + (x.src.length ? '<span class="pstags">' + x.src.map(function (s) { return '<a class="pstag t-body-medium" href="' + (isOperator() ? '#requests/' + s.id : 'diet-home.html?as=' + VIEWER.key + '#request/' + s.id) + '">From ' + esc(s.id) + '</a>' + (s.alt ? '<span class="pstag alt t-body-medium">Alternative: ' + esc(s.alt) + '</span>' : ''); }).join('') + '</span>' : '') + '</td>' +
            '<td>' + esc(x.cut || '-') + '</td><td>' + esc(x.prep || '-') + '</td><td class="r">' + (x.pieces != null ? fmtN(x.pieces) : '-') + '</td><td class="r"><b>' + fmtN(Math.round(x.amount * 100) / 100) + '</b> <small class="u">' + esc(x.unit) + '</small></td></tr>'; }).join('') + '</tbody></table></div>'
          : '<div class="empty"><span class="ei">' + ic('list', 24) + '</span><b class="t-minor-title">Nothing to prepare</b><span class="t-body-regular">No diet needs these items in this range. Change the dates or clear the filters.</span></div>') +
        '<p class="kcap t-body-regular">' + ic('info', 16) + 'Pieces use the saved piece weight for the item and cut size. Amounts from Diet Requests are per day times the days of the request in this range.</p></section></div>';
  }
  var psp = document.getElementById('pspanel');
  psp.addEventListener('click', function (e) { var t;
    if (e.target.closest('[data-psback]')) { if (PSPUSHED && history.length > 1) history.back(); else location.hash = '#meal-groups'; return; }
    if ((t = e.target.closest('[data-psr]'))) { PSS.range = t.getAttribute('data-psr'); drawPS(); return; }
    if ((t = e.target.closest('[data-pssort]'))) { var k = t.getAttribute('data-pssort'); if (PSS.sort === k) PSS.dir = -PSS.dir; else { PSS.sort = k; PSS.dir = k === 'name' ? 1 : -1; } drawPS(); return; }
    if ((t = e.target.closest('[data-psrm]'))) { PSS[t.getAttribute('data-psrm')] = ''; drawPS(); return; }
    if (e.target.closest('[data-psclear]')) { PSS.site = PSS.sp = PSS.item = PSS.prep = ''; drawPS(); return; }
    if (e.target.closest('[data-psrefresh]')) { PSS.busy = true; drawPS(); var t0 = Date.now(); setTimeout(function () { PSS.busy = false; PSS.computedAt = Date.now(); PSS.took = Math.max(1, Math.round((Date.now() - t0) / 1000)); drawPS(); toast('Prep sheet rebuilt'); }, 1500); }
  });
  psp.addEventListener('change', function (e) { var t = e.target; if (t.matches('[data-psf]')) { PSS[t.getAttribute('data-psf')] = t.value; drawPS(); } if (t.matches('[data-psd]')) { PSS[t.getAttribute('data-psd')] = t.value; drawPS(); } });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !RS.hidden) RS.hidden = true; });

  /* ---------------- Meal Group Management pages: registry, store, full-screen panel, bottom sheet ----------------
     Events inside the page body are passed to MGP[slug].click / input / change / keydown (e). toastUndo(msg, fn) shows Undo.
     A module registers MGP[slug] = { title, sub, draw(body) } and may set MGP[slug].onViewer. It reads its seed with
     MGSTORE.get(slug) (a deep copy of MGSEED[slug], or the saved copy) and saves with MGSTORE.set(slug, data).
     canEdit() is true for kitchen roles. mgSheet(html) opens a bottom sheet and returns it; mgClose() closes it;
     mgConfirm(o) asks before a destructive action. */
  var MGAPI = {};   /* cross-page lookups a module offers others, e.g. MGAPI.stations(), MGAPI.keepers() */
  var MGSEED = __MGSEED__, MGP = {}, MGK = 'antz.kitchen.mg', MGPUSHED = false;
  var MGSTORE = { all: lsGet(MGK) || {},
    get: function (k) { var v = this.all[k] != null ? this.all[k] : MGSEED[k]; return v == null ? null : JSON.parse(JSON.stringify(v)); },
    set: function (k, v) { this.all[k] = v; lsSet(MGK, this.all); },
    reset: function () { this.all = {}; try { localStorage.removeItem(MGK); } catch (x) {} } };
  function canEdit() { return isKitchen(); }
  var MGS = document.getElementById('mgsheet');
  function mgSheet(html, label) { var old = MGS.querySelector('.sheet'), sh = old.cloneNode(false); old.parentNode.replaceChild(sh, old); sh.innerHTML = '<div class="grab"></div>' + html; sh.setAttribute('aria-label', label || 'Details'); MGS.hidden = false; var f = sh.querySelector('input:not([type=hidden]):not([disabled]), select, textarea'); if (f) setTimeout(function () { try { f.focus(); } catch (x) {} }, 60); return sh; }
  function mgClose() { MGS.hidden = true; MGS.querySelector('.sheet').innerHTML = ''; }
  function mgSheetHead(title, sub) { return '<div class="sheet__h"><div><h2 class="t-major-title">' + esc(title) + '</h2>' + (sub ? '<p class="t-body-regular" style="color:var(--ink)">' + esc(sub) + '</p>' : '') + '</div><button type="button" class="iconbtn" data-mgclose aria-label="Close">' + ic('close', 24) + '</button></div>'; }
  function mgConfirm(o) { var sh = mgSheet(mgSheetHead(o.title, '') + '<p class="t-body-regular" style="color:var(--ink)">' + esc(o.text) + '</p><div class="sheet__f"><button type="button" class="btn sec" data-mgclose>Cancel</button><button type="button" class="btn ' + (o.danger ? 'danger' : 'pri') + '" data-mgok>' + esc(o.ok || 'Confirm') + '</button></div>', o.title);
    sh.querySelector('[data-mgok]').addEventListener('click', function () { mgClose(); o.onOk(); }); }
  MGS.addEventListener('click', function (e) { if (e.target === MGS || e.target.closest('[data-mgclose]')) mgClose(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !MGS.hidden) mgClose(); });
  function mgSlug() { var m = /^#meal-groups\/([a-z-]+)$/.exec(location.hash); return m && MGP[m[1]] ? m[1] : null; }
  var mgpan = document.getElementById('mgpanel');
  function drawMG() { var k = mgSlug(); if (!k) return; var p = MGP[k]; mgpan.querySelector('#mgT').textContent = p.title; mgpan.querySelector('[data-mgsub]').textContent = p.sub || ''; mgpan.setAttribute('data-mg', k); p.draw(mgpan.querySelector('[data-mgbody]')); }
  function routeMG() { var k = mgSlug(); if (k) { if (mgpan.getAttribute('data-open') !== k) { mgpan.setAttribute('data-open', k); mgpan.querySelector('[data-mgbody]').scrollTop = 0; drawMG(); } mgpan.hidden = false; } else { mgpan.hidden = true; mgpan.removeAttribute('data-open'); MGPUSHED = false; if (!MGS.hidden) mgClose(); } }
  window.addEventListener('hashchange', routeMG);
  mgpan.addEventListener('click', function (e) { if (e.target.closest('[data-mgback]')) { if (MGPUSHED && history.length > 1) history.back(); else location.hash = '#meal-groups'; return; } var p = MGP[mgSlug()]; if (p && p.click) p.click(e); });
  ['input', 'change', 'keydown'].forEach(function (ty) { mgpan.addEventListener(ty, function (e) { var p = MGP[mgSlug()]; if (p && p[ty]) p[ty](e); }); });
  var toastU;
  function toastUndo(msg, fn) { var t = document.getElementById('toast'); t.innerHTML = '<span>' + esc(msg) + '</span><button type="button" class="tundo">Undo</button>'; t.classList.add('on', 'act'); clearTimeout(toastT); clearTimeout(toastU);
    var b = t.querySelector('.tundo'); b.addEventListener('click', function () { t.classList.remove('on', 'act'); fn(); });
    toastU = setTimeout(function () { t.classList.remove('on', 'act'); }, 5000); }
  function mgPieceWeights() { var d = MGP['piece-weights'] && MGSTORE.get('piece-weights'); return d && d.items ? d.items : PSD.pieceWeights; }
/*__MG_MODULES__*/
  applyViewer(true); route(); routeMG();
'''


MG_CSS = '''    /* Meal Group Management pages: shared toolbar, search, forms, tables, sheets */
    .mgpane { display: grid; gap: 16px; max-width: 1080px; margin: 0 auto; }
    .mgbar { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; }
    .mgbar .sp { flex: 1; }
    .mgsearch { display: flex; align-items: center; gap: 8px; height: 44px; padding: 0 12px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; background: var(--white); color: var(--md3-neutral-secondary); flex: none; min-height: 44px; min-width: 0; }
    .mgbar .mgsearch { flex: 1 1 220px; }
    .mgsearch input { flex: 1; min-width: 0; height: 100%; border: 0; outline: none; background: none; font: inherit; color: var(--head); }
    .mgsearch:focus-within { border-color: var(--md3-on-primary-container); }
    .mgsheet { gap: 16px; }
    .mgform { display: grid; gap: 14px; }
    .mgform .two { display: grid; gap: 12px; grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .mgf { display: grid; gap: 4px; }
    .mgf > span { color: var(--ink); font-size: 14px; font-weight: 500; }
    .mgf input:not([type=checkbox]):not([type=radio]), .mgf select, .mgf textarea { min-height: 44px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; padding: 0 12px; background: var(--white); color: var(--head); font: inherit; width: 100%; }
    .mgf textarea { padding: 10px 12px; min-height: 88px; resize: vertical; }
    .mgf input:focus, .mgf select:focus, .mgf textarea:focus { border-color: var(--md3-on-primary-container); outline: none; }
    .mgf.err input, .mgf.err select, .mgf.err textarea { border-color: var(--md3-error); }
    .mgf small { color: var(--md3-neutral-secondary); font-size: 13px; }
    .mgf.err small { color: var(--md3-error); }
    .mgchk { display: flex; align-items: center; gap: 10px; min-height: 44px; color: var(--head); }
    .mgchk input { width: 22px; height: 22px; accent-color: var(--md3-on-primary-container); flex: none; }
    .mgro { display: inline-flex; align-items: center; gap: 6px; color: var(--md3-neutral-secondary); font-size: 14px; }
    .mgrow { cursor: pointer; }
    @media (hover: hover) { .mgrow:hover td { background: var(--md3-background); } }
    .iconbtn.sm { width: 44px; height: 44px; }
    .toast.act { pointer-events: auto; display: flex; align-items: center; gap: 12px; padding-right: 6px; }
    .toast .tundo { min-height: 44px; padding: 0 14px; border-radius: 8px; color: #9DE6D9; font: inherit; font-weight: 600; }
'''

_kbody = f'''  <div class="app">
{STATUS_HTML}
    <div class="head">
      <header class="bar">
        <a class="iconbtn" href="diet-module-flow.html" data-aslink="diet-module-flow.html" aria-label="Back to Modules">{svg("back", 24)}</a>
        <div class="bar__hd"><h1 class="t-medium-medium">Kitchen</h1></div>
        <button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button>
        {SITE_BTN}
      </header>
      <nav class="mtabs k2" role="tablist" aria-label="Kitchen sections"><a class="mtab t-minor-medium" role="tab" id="t-requests" href="#requests" aria-controls="p-requests" aria-selected="false" hidden>Requests</a><a class="mtab t-minor-medium" role="tab" id="t-dashboard" href="#dashboard" aria-controls="p-dashboard" aria-selected="true">Kitchen Dashboard</a><a class="mtab t-minor-medium" role="tab" id="t-meal-groups" href="#meal-groups" aria-controls="p-meal-groups" aria-selected="false">Meal Group Management</a></nav>
    </div>
    <main class="main" id="main"><section class="pane" id="p-dashboard" role="tabpanel" aria-labelledby="t-dashboard"></section><section class="pane" id="p-requests" role="tabpanel" aria-labelledby="t-requests" hidden></section><section class="pane" id="p-meal-groups" role="tabpanel" aria-labelledby="t-meal-groups" hidden></section></main>
  </div>
  <div class="dpanel" id="pspanel" hidden role="dialog" aria-modal="true" aria-labelledby="psT">
    <header class="bar"><button class="iconbtn" type="button" data-psback aria-label="Back to Meal Group Management">{svg("back", 24)}</button><div class="bar__hd"><h1 class="t-medium-medium" id="psT">Prep Sheet</h1><p class="t-body-regular">Pieces and weight to prepare, by cut size and preparation</p></div><button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button></header>
    <div class="dpanel__body" data-psbody></div>
  </div>
  <div class="dpanel" id="mgpanel" hidden role="dialog" aria-modal="true" aria-labelledby="mgT">
    <header class="bar"><button class="iconbtn" type="button" data-mgback aria-label="Back to Meal Group Management">{svg("back", 24)}</button><div class="bar__hd"><h1 class="t-medium-medium" id="mgT"></h1><p class="t-body-regular" data-mgsub></p></div><button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button></header>
    <div class="dpanel__body" data-mgbody></div>
  </div>
  <div class="scrim" id="mgsheet" hidden><div class="sheet mgsheet" role="dialog" aria-modal="true"></div></div>
{ROLE_OVERLAY}
  <div class="toast t-body-medium" id="toast" role="status" aria-live="polite"></div>'''

_khelp = icon_js(K_ICONS) + "  function esc(s) { return String(s == null ? '' : s).replace(/[&<>\"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;' }[c]; }); }\n" + STORE_JS
_kjs = KITCHEN_JS.replace('/*__MG_MODULES__*/', ''.join('  /* ---- page module: ' + m['slug'] + ' (_build/mg_' + m['slug'].replace('-', '_') + '.py) ---- */\n' + m['js'] + '\n' for m in MG_MODS)).replace('__MGSEED__', json.dumps(MGSEED, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')).replace('__MG_HTML__', json.dumps(MG_HTML)).replace('__KDASH__', json.dumps(KDASH, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')).replace('__KSTK__', json.dumps(KSTK, ensure_ascii=False, separators=(',', ':'))).replace('__PSDATA__', json.dumps(PSDATA, ensure_ascii=False, separators=(',', ':'))).replace('__PSCHED__', json.dumps(PSCHED, ensure_ascii=False, separators=(',', ':'))).replace('__REQSEED__', json.dumps(_req_seed, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
page(os.environ.get('KH_OUT', 'kitchen-home.html'), 'Kitchen',
     'Kitchen home: Kitchen Dashboard (#dashboard) and Meal Group Management (#meal-groups). Target of the Kitchen tile on diet-module-flow.html. '
     'Generated by _build/kitchen.py, do not hand-edit. Earlier full build kept in _build/kitchen_full_backup.py.',
     HEAD_CSS + DIR_CSS2 + ROLE_CSS + KITCHEN_CSS + MG_CSS + ''.join(m.get('css', '') for m in MG_MODS), _kbody, _khelp + _kjs)
