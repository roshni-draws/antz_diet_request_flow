# newui.py: exec'd by build.py after figma_bar.py. "New UI": the same screens drawn with the Antz Design Library
# (claude.ai artifact G4z41FWKrhN6kDySJuK6Za, app/components.css, tablet components approved 2026-09-21).
# A skin only: every rule is scoped under html.ui-new, so with the switch off the prototype is exactly as before.
# Mapping (ours -> library): app bar -> .hdr; main / transfer tabs -> .tab-primary pill tabs; segmented controls -> .tab-seg;
# filter chips -> .tab-dd / .app-filter-chip; search -> .tab-search; icon buttons -> .tab-iconbox; inputs -> .app-field;
# buttons -> .btn (4px); list cards -> .app-listing-card (10px); panels -> .pcard / .card; underline tabs -> .app-tab.
NEWUI_CSS = r'''  <style id="ui-new-css">
    /* ===== New UI: Antz Design Library skin (only when html.ui-new) ===== */
    html.ui-new { --dl-head: #1F415B; --dl-teal: #1F515B; --dl-muted: #7A8684; --dl-line: #C3CEC7; --dl-outline: #839D8D; --dl-n05: rgba(0,0,0,.05); --dl-a10: rgba(0,0,0,.10); --dl-sec: #DDEBE9; --dl-surface: #F2FFF8; --dl-green: #37BD69; --radius: 10px; --card-shadow: none; }
    /* header: .hdr (white, 20px, title in OnSecondaryContainer, subtitle neutralSecondary) */
    html.ui-new .bar { padding: 20px 20px 20px 16px; gap: 12px; border-bottom: 0; box-shadow: 0 4px 4px 0 rgba(0,0,0,.05); }
    html.ui-new .bar__hd h1 { color: var(--dl-head); }
    html.ui-new .bar__hd p { color: var(--dl-muted); }
    html.ui-new .bar .iconbtn, html.ui-new .sthero .iconbtn, html.ui-new .gthero .iconbtn { border-radius: 8px; }
    html.ui-new .asbtn { border-radius: 8px; border-color: var(--dl-line); min-height: 40px; }
    html.ui-new .sitebtn { height: 40px; padding: 6px 12px; border-radius: 8px; background: #fff; border: 1px solid var(--dl-line); }
    /* primary tabs: .tab-primary pills (40px, min 138, radius 8, grey + hairline shadow; active dark teal) */
    html.ui-new .mtabs, html.ui-new .txtabs, html.ui-new .rdtabs { display: flex !important; gap: 12px; padding: 16px 20px 12px; background: #fff; border-bottom: 0; overflow-x: auto; scrollbar-width: none; grid-template-columns: none !important; }
    html.ui-new .mtabs[hidden], html.ui-new .txtabs[hidden], html.ui-new .rdtabs[hidden], html.ui-new [hidden] { display: none !important; }
    html.ui-new .mtabs::-webkit-scrollbar, html.ui-new .txtabs::-webkit-scrollbar { display: none; }
    html.ui-new .mtab, html.ui-new .txtab, html.ui-new .rdtab { flex: 0 0 auto; height: 40px; min-height: 40px; min-width: 138px; padding: 8px 16px; border: 0 !important; border-radius: 8px; background: var(--dl-n05); color: var(--md3-on-surface-variant); box-shadow: 0 1px 3px 0 var(--dl-a10); font-weight: 500; }
    html.ui-new .mtab[aria-selected="true"], html.ui-new .txtab[aria-selected="true"], html.ui-new .rdtab[aria-selected="true"] { background: var(--dl-teal); color: #fff; box-shadow: none; filter: drop-shadow(0 1px 1.5px var(--dl-a10)); }
    html.ui-new .txtab .n, html.ui-new .rdtab .n { background: rgba(255,255,255,.18); color: inherit; }
    html.ui-new .txtab:not([aria-selected="true"]) .n { background: #fff; color: var(--dl-teal); }
    html.ui-new .head .mtabs { border-top: 1px solid var(--line); }
    /* segmented controls: .tab-seg (white track radius 14, items radius 10, active dark teal) */
    html.ui-new .seg3, html.ui-new .dseg, html.ui-new .dvtabs, html.ui-new .sdtabs { padding: 5px; gap: 0; border-radius: 14px; background: #fff; box-shadow: 0 1px 3px var(--dl-a10); }
    html.ui-new .seg3 button, html.ui-new .dseg button, html.ui-new .dseg a, html.ui-new .dvtabs button, html.ui-new .sdtabs button { min-height: 36px; height: 36px; border-radius: 10px; border: 0; color: var(--md3-on-surface-variant); background: transparent; box-shadow: none; }
    html.ui-new .seg3 button[aria-selected="true"], html.ui-new .dseg button[aria-pressed="true"], html.ui-new .dseg a[aria-selected="true"], html.ui-new .dvtabs button[aria-selected="true"], html.ui-new .sdtabs button[aria-selected="true"] { background: var(--dl-teal); color: #fff; font-weight: 500; }
    html.ui-new .dvtabs button[aria-selected="true"] .n { background: rgba(255,255,255,.2); color: #fff; }
    /* filter chips: .tab-dd / .app-filter-chip (white, radius 8, outline) */
    html.ui-new .spchip, html.ui-new .pchip, html.ui-new .daychips button, html.ui-new .pl-chip, html.ui-new .ws-chip { border-radius: 8px; background: #fff; border: 1px solid var(--dl-line); color: var(--md3-on-surface-variant); }
    html.ui-new .spchip[aria-pressed="true"], html.ui-new .daychips button[aria-pressed="true"], html.ui-new .pl-chip[aria-pressed="true"], html.ui-new .ws-chip[aria-pressed="true"] { background: var(--dl-teal); border-color: var(--dl-teal); color: #fff; }
    html.ui-new .pchip:has(input:checked) { background: var(--dl-teal); border-color: var(--dl-teal); color: #fff; }
    /* search + icon buttons: .tab-search (outlined) and .tab-iconbox (44px, displaybgSecondary) */
    html.ui-new .spsearch { background: #fff; border: 1px solid var(--dl-line); border-radius: 8px; height: 44px; }
    html.ui-new .spfilter { width: 44px; min-width: 44px; height: 44px; border-radius: 8px; background: var(--dl-sec); border-color: transparent; }
    html.ui-new .spfilter.on, html.ui-new .spfilter[aria-pressed="true"] { background: var(--dl-teal); color: #fff; }
    html.ui-new .ddate.spfilter { width: auto; padding: 0 12px; background: #fff; border: 1px solid var(--dl-line); }
    html.ui-new .ddate.spfilter.on { background: var(--dl-teal); color: #fff; border-color: var(--dl-teal); }
    html.ui-new .ddate.spfilter.on svg { color: #fff; }
    /* buttons: .btn (radius 4, 40px; primary green, secondary outlined teal, reject outlined error) */
    html.ui-new .btn { border-radius: 4px; }
    html.ui-new .btn.sec { border: 1px solid var(--dl-teal); color: var(--dl-teal); background: #fff; }
    html.ui-new .btn.danger { border: .5px solid var(--md3-error); }
    html.ui-new .btn.add, html.ui-new .btn.exit { border-radius: 4px; }
    html.ui-new .cfgedit, html.ui-new .linkbtn.gadd { border-radius: 4px; }
    /* inputs: .app-field (56px, radius 4, Outline border on Surface; focus 1.5px Primary on white) */
    html.ui-new .gin input, html.ui-new .fgrid input[type=text], html.ui-new .fgrid input[type=date], html.ui-new .fgrid input[type=time], html.ui-new .fgrid select, html.ui-new .txform input, html.ui-new .txform textarea { height: 56px; border-radius: 4px; border: 1px solid var(--dl-outline); background: var(--dl-surface); color: var(--dl-teal); }
    html.ui-new .txform textarea { min-height: 88px; height: auto; }
    html.ui-new .gin input:focus, html.ui-new .fgrid input:focus, html.ui-new .fgrid select:focus, html.ui-new .txform input:focus, html.ui-new .txform textarea:focus { background: #fff; border: 1.5px solid var(--dl-green); box-shadow: none; outline: none; }
    html.ui-new .gin.ro b { height: 56px; border-radius: 4px; }
    html.ui-new .gin.bad input { border-color: var(--md3-error); background: #fff; }
    /* list cards: .app-listing-card (white, radius 10, no shadow) and panels: .pcard (radius 8, 16px) */
    html.ui-new .gvc, html.ui-new .txc, html.ui-new .stcard, html.ui-new .spk, html.ui-new .cfgrow, html.ui-new .dvc, html.ui-new .rqcard, html.ui-new .spcard, html.ui-new .dietcard { border-radius: 10px; box-shadow: none; }
    html.ui-new .gvc[aria-current="true"], html.ui-new .txc[aria-current="true"] { border-color: var(--dl-teal); }
    html.ui-new .dpan, html.ui-new .dsum, html.ui-new .tabcard, html.ui-new .kpanel, html.ui-new .scard, html.ui-new .dcard, html.ui-new .sum4 > *, html.ui-new .kcard { border-radius: 8px; box-shadow: none; }
    html.ui-new .gacc__i { border-radius: 8px; }
    /* tags: .app-tag radius 5 */
    html.ui-new .tag, html.ui-new .gplus, html.ui-new .gtab, html.ui-new .gchip, html.ui-new .dctag, html.ui-new .gcond, html.ui-new .gexp, html.ui-new .slive, html.ui-new .ttag, html.ui-new .pill, html.ui-new .dmv { border-radius: 5px; }
    /* sheets keep their shape; the grab bar and title follow the header colour */
    html.ui-new .sheet__h h2 { color: var(--dl-head); }
    /* Modules screen tiles */
    html.ui-new .tile, html.ui-new .row { border-radius: 10px; box-shadow: none; }
    html.ui-new .head .title { color: var(--dl-head); }
  </style>
'''
NEWUI_HEAD = '''  <script>try { if (localStorage.getItem('antz.ui') === 'new') document.documentElement.classList.add('ui-new'); } catch (e) {}</script>
'''
