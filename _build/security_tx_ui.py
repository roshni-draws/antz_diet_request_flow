# security_tx_ui.py: exec'd by security.py. Sites tab: site cards, then a site page with the five transfer tabs from the
# mobile screenshots (secuirty/site transfer). Tablet layout: landscape is list + detail side by side, portrait is the list
# and then the detail full width. Routes: #sites, #sites/S1 (Animal Transfer), #sites/S1/<type>, #sites/S1/<type>/<id>.
TX_CSS = """    /* =========================================================
       17. SITE TRANSFERS  (Sites tab: site cards, site page, transfer tabs, list + detail)
       ========================================================= */
    .av { width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; flex: none; background: var(--md3-surface-variant); color: var(--md3-on-primary-container); font-weight: 600; font-size: 14px; }
    .stsearchrow { display: flex; align-items: center; gap: var(--sp-12); margin-top: var(--sp-16); }
    .stsearch { flex: 1; }
    .stcards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--sp-16); margin-top: var(--sp-16); }
    @media (orientation: portrait) { .stcards { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    .stcard { position: relative; display: grid; grid-template-rows: 1fr auto; min-height: 168px; border-radius: var(--radius); overflow: hidden; color: var(--white); background: var(--stc, #2C4F5A); box-shadow: var(--card-shadow); transition: transform 120ms var(--ease); }
    .stcard:active { transform: scale(.985); }
    .stcard__art { position: absolute; right: -10px; top: -14px; width: 150px; height: 150px; opacity: .13; color: var(--white); }
    .stcard__art svg { width: 100%; height: 100%; fill: none; stroke: currentColor; stroke-width: 1.2; }
    .stcard__top { position: relative; padding: var(--sp-16) var(--sp-20); display: grid; align-content: start; gap: 6px; }
    .stcard__top b { font-size: 22px; font-weight: 600; }
    .stcard__top small { opacity: .8; font-size: 13px; }
    .stcard__pend { justify-self: start; display: inline-flex; align-items: center; height: 26px; padding: 0 10px; border-radius: 999px; background: rgba(255,255,255,.18); font-size: 13px; font-weight: 600; }
    .stcard__foot { position: relative; display: flex; align-items: center; gap: var(--sp-8); padding: 6px 8px 6px var(--sp-20); background: rgba(0,0,0,.28); }
    .stcard__foot span { flex: 1; min-width: 0; display: flex; align-items: center; gap: 6px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
    .ricon { width: 44px; height: 44px; border-radius: 22px; display: grid; place-items: center; flex: none; color: inherit; }
    svg.si { fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .ricon svg, .stico svg { fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    @media (hover: hover) { .ricon:hover { background: rgba(255,255,255,.14); } }
    .stpanel { grid-template-rows: auto auto 1fr; }
    .sthero { position: relative; overflow: hidden; display: flex; align-items: flex-end; gap: var(--sp-16); padding: var(--sp-12) var(--sp-16) var(--sp-16); min-height: 112px; background: var(--stc, #2C4F5A); color: var(--white); }
    .sthero .iconbtn { position: absolute; left: 8px; top: 8px; color: var(--white); }
    .sthero .stcard__art { width: 220px; height: 220px; right: 24px; top: -30px; }
    .sthero__t { position: relative; flex: 1; min-width: 0; display: grid; gap: 2px; padding: 8px 0 0 48px; }
    @media (orientation: portrait) { .sthero { min-height: 150px; } .sthero__t { padding: 44px 0 0; } }
    .sthero__t small { letter-spacing: .14em; font-size: 11px; font-weight: 600; opacity: .85; }
    .sthero__t h2 { font-size: 26px; font-weight: 600; }
    .sthero__p { position: relative; display: flex; align-items: center; gap: var(--sp-8); }
    .stpill { display: inline-flex; align-items: center; gap: 6px; height: 44px; padding: 0 14px; border-radius: 8px; border: 1px solid rgba(255,255,255,.35); background: rgba(0,0,0,.22); }
    .sthero__p .ricon { border-radius: 8px; border: 1px solid rgba(255,255,255,.35); background: rgba(0,0,0,.22); color: #7FE0A6; }
    .txtabs { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); background: var(--white); border-bottom: 1px solid var(--line); }
    .txtab { height: 52px; display: flex; align-items: center; justify-content: center; gap: 6px; padding: 0 6px; color: var(--md3-on-surface-variant); border-bottom: 3px solid transparent; white-space: nowrap; }
    .txtab[aria-selected="true"] { color: var(--md3-on-surface); border-bottom-color: var(--md3-on-surface); font-weight: 600; }
    .txtab .n { min-width: 22px; height: 22px; padding: 0 6px; border-radius: 11px; display: inline-grid; place-items: center; background: var(--add-primary-a10); color: #006F88; font-size: 12px; font-weight: 600; }
    .txbody { min-height: 0; display: grid; grid-template-columns: minmax(340px, 400px) minmax(0, 1fr); background: var(--md3-surface-variant); }
    .txbody.red { background: #F6E4E7; }
    .txlist { min-height: 0; overflow-y: auto; padding: 0 var(--sp-16) var(--sp-24); border-right: 1px solid rgba(0,0,0,.06); }
    .txdet { min-height: 0; overflow: hidden; display: grid; grid-template-rows: 1fr auto; background: var(--white); }
    @media (orientation: portrait) {
      .txbody { grid-template-columns: minmax(0, 1fr); }
      .txbody.sel .txlist { display: none; }
      .txbody:not(.sel) .txdet { display: none; }
      .txlist { border-right: 0; }
    }
    .txbar { position: sticky; top: 0; z-index: 1; display: flex; align-items: center; justify-content: space-between; gap: var(--sp-12); padding: var(--sp-12) 0; background: inherit; }
    .txlist { background: inherit; }
    .txbar h3 { color: var(--md3-on-primary-container); }
    .txfilt { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 0 10px; border-radius: 8px; color: var(--md3-on-surface); font-weight: 500; }
    .txfilt.on { background: var(--white); }
    .txfilt svg { fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; }
    .txcards { display: grid; gap: var(--sp-12); }
    .txc { display: grid; gap: 6px; width: 100%; padding: var(--sp-12) var(--sp-16); border-radius: var(--radius); background: var(--white); text-align: left; box-shadow: var(--card-shadow); border: 2px solid transparent; }
    .txc[aria-current="true"] { border-color: var(--md3-on-primary-container); }
    .txc__r { display: flex; align-items: flex-start; gap: var(--sp-12); }
    .txc__r .grow { flex: 1; min-width: 0; display: grid; gap: 4px; }
    .txid { justify-self: start; display: inline-flex; align-items: center; gap: 6px; height: 28px; padding: 0 10px; border-radius: 14px; background: var(--md3-background); color: var(--head); font-weight: 600; font-size: 14px; }
    .txid svg { fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .txid.red { background: #FBE9EC; color: #6E1027; }
    .txid.plain { background: none; padding: 0; height: auto; font-size: 17px; color: var(--md3-on-primary-container); }
    .txplace { display: flex; align-items: center; gap: 8px; color: var(--md3-on-primary-container); }
    .txplace b { font-weight: 600; }
    .txplace small { color: var(--md3-neutral-secondary); }
    .mk { flex: none; width: 18px; height: 8px; display: inline-flex; align-items: center; }
    .mk::before { content: ""; width: 10px; height: 2px; }
    .mk::after { content: ""; width: 8px; height: 8px; }
    .mk.fr::before { background: #2DB45D; } .mk.fr::after { background: #2DB45D; border-radius: 50%; }
    .mk.to::before { background: #E93353; } .mk.to::after { background: #E93353; border-radius: 1px; }
    .txmeta { color: var(--ink); }
    .txst { flex: none; max-width: 120px; text-align: center; color: var(--md3-on-primary-container); font-size: 13px; font-weight: 600; line-height: 1.25; }
    .txst.done { padding: 8px 12px; border-radius: 6px; background: #000; color: var(--white); }
    .txst.muted { color: var(--md3-neutral-secondary); font-weight: 500; }
    .txtop { display: flex; justify-content: space-between; gap: 8px; color: var(--md3-neutral-secondary); font-size: 13px; }
    .txtop b { color: var(--head); font-weight: 600; }
    .txband { margin: 4px -10px -6px; padding: 8px 12px; border-radius: 6px; font-weight: 500; }
    .txband.pend { background: #CFF5F1; color: #0E4F57; }
    .txband.done { background: #E3F8EA; color: #12723A; }
    .txband.muted { background: var(--md3-background); color: var(--ink); }
    .txby { display: flex; align-items: center; gap: 8px; color: var(--head); font-weight: 500; }
    .txby .av { width: 28px; height: 28px; font-size: 11px; }
    .txchk { display: grid; gap: 2px; margin-top: 4px; padding: 12px 14px; border-radius: 8px; background: #FBE3E7; }
    .txchk b { display: flex; align-items: center; gap: 6px; color: var(--head); font-weight: 500; }
    .txchk small { color: var(--ink); }
    .txchk span { color: #C3213F; }
    .txempty { padding: var(--sp-32) var(--sp-16); text-align: center; color: var(--ink); }
    .txdh { display: grid; gap: 6px; padding: var(--sp-16) var(--sp-20); color: var(--white); background: var(--txh, #1F515B); }
    .txdh__r { display: flex; align-items: center; gap: var(--sp-12); }
    .txdh__r .grow { flex: 1; min-width: 0; display: grid; gap: 6px; }
    .txdh h3 { font-size: 20px; font-weight: 600; }
    .txdh .txplace { color: var(--white); font-size: 16px; }
    .txdh .txplace small { color: rgba(255,255,255,.75); }
    .txdh .sub { color: rgba(255,255,255,.85); }
    .txdh .txby { color: var(--white); }
    .txdh .ricon { width: 40px; height: 40px; background: rgba(0,0,0,.3); color: var(--white); }
    .qr { width: 56px; height: 56px; flex: none; background: var(--white); border-radius: 6px; padding: 5px; }
    .txdb { min-height: 0; overflow-y: auto; }
    .txrow { display: flex; align-items: center; gap: var(--sp-16); min-height: 64px; padding: 10px var(--sp-20); background: #EFFAF5; border-bottom: 1px solid rgba(0,0,0,.05); }
    .txrow.red { background: #FCF1F3; }
    .txrow.plain { background: var(--white); }
    .txrow .stico { flex: none; color: var(--head); }
    .txrow .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .txrow small { color: var(--ink); font-size: 12px; }
    .txrow b { color: var(--head); font-size: 17px; font-weight: 500; }
    .txrow .linkbtn { min-height: 44px; padding: 0 8px; color: var(--md3-on-surface); font-weight: 600; }
    .txrow.red .linkbtn { color: #C3213F; }
    .txappr { display: grid; gap: 10px; width: 100%; }
    .txappr div { display: flex; align-items: center; gap: 10px; }
    .txappr .grow b { font-size: 16px; }
    .txappr .ok { color: var(--md3-on-surface); }
    .ring { width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center; border: 1.5px solid var(--md3-primary); color: var(--md3-on-surface); font-weight: 600; font-size: 14px; flex: none; }
    .txani { display: flex; gap: var(--sp-12); margin: 0 var(--sp-20) var(--sp-12); padding: var(--sp-12); border-radius: var(--radius); background: #E6F2EF; }
    .txani.red { background: #FBE3E7; }
    .txani__img { position: relative; width: 104px; height: 104px; flex: none; border-radius: 8px; display: grid; place-items: center; background: linear-gradient(135deg, #C9DCD5, #9DBDB2); color: rgba(255,255,255,.9); }
    .txani__img svg { width: 44px; height: 44px; }
    .txani__img i { position: absolute; left: 6px; top: 6px; min-width: 24px; height: 22px; padding: 0 5px; border-radius: 4px; background: #00B3D6; color: var(--white); font-style: normal; font-size: 11px; font-weight: 700; display: grid; place-items: center; }
    .txani.red .txani__img i { background: #F46A4E; }
    .txani .grow { display: grid; align-content: start; gap: 3px; color: var(--md3-on-primary-container); }
    .txani .grow b { font-weight: 600; }
    .txani .grow em { color: var(--ink); }
    .txsec { display: flex; align-items: center; gap: 8px; padding: var(--sp-12) var(--sp-20) 8px; color: var(--head); font-weight: 500; }
    .txsec .grow { flex: 1; }
    .txgrid2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--sp-12); padding: var(--sp-12) var(--sp-20); border-bottom: 1px solid rgba(0,0,0,.05); }
    .txgrid2 div { display: grid; gap: 4px; }
    .txgrid2 small { display: flex; align-items: center; gap: 6px; color: var(--head); font-size: 15px; }
    .txgrid2 b { color: var(--md3-on-primary-container); font-weight: 500; }
    .txphotos { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: var(--sp-12); padding: 0 var(--sp-20) var(--sp-12); }
    .txphoto { border-radius: var(--radius); background: var(--white); box-shadow: 0 1px 4px rgba(0,0,0,.1); overflow: hidden; }
    .txphoto div { height: 110px; display: grid; place-items: center; background: linear-gradient(135deg, #F2D6CC, #D9A796); color: rgba(255,255,255,.9); }
    .txphoto p { padding: 8px 10px; color: var(--ink); font-size: 12px; }
    .txcom { display: grid; gap: 8px; padding: 0 var(--sp-20) var(--sp-16); }
    .txcom form { display: flex; align-items: center; gap: 8px; min-height: 52px; padding: 4px 4px 4px 14px; border-radius: var(--radius); border: 1px solid var(--md3-outline-variant); background: var(--white); }
    .txcom input { flex: 1; min-width: 0; height: 44px; color: var(--head); }
    .txcom .send { width: 44px; height: 44px; display: grid; place-items: center; color: var(--md3-neutral-secondary); }
    .txcom .send svg { fill: currentColor; }
    .txcm { display: flex; gap: 10px; padding: 10px 12px; border-radius: 8px; background: var(--md3-background); }
    .txcm .av { width: 32px; height: 32px; font-size: 12px; }
    .txcm b { color: var(--head); font-weight: 600; font-size: 13px; }
    .txcm small { color: var(--md3-neutral-secondary); font-size: 12px; }
    .txcm p { color: var(--head); }
    .txfoot { display: grid; gap: 10px; padding: var(--sp-16) var(--sp-20) var(--sp-20); border-top: 1px solid var(--md3-surface-variant); border-radius: 18px 18px 0 0; box-shadow: 0 -4px 16px rgba(0,0,0,.06); background: var(--white); }
    .txfoot__h { display: flex; align-items: flex-end; gap: 12px; }
    .txfoot__h .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .txfoot__h small { color: var(--ink); }
    .txfoot__h b { color: var(--md3-on-primary-container); font-size: 20px; font-weight: 500; }
    /* open timeline: lifts over the detail on a dark scrim, slides up */
    .txdet > div { position: relative; }
    .tlscrim { position: absolute; inset: 0; z-index: 2; width: 100%; border: 0; background: rgba(12, 28, 33, .55); cursor: pointer; }
    .txfoot.open { position: absolute; left: 0; right: 0; bottom: 0; z-index: 3; box-shadow: 0 -12px 32px rgba(12, 28, 33, .28); }
    .tlscrim.anim { animation: tlfade 220ms ease-out both; }
    .txfoot.open.anim { animation: tlrise 320ms cubic-bezier(.16, 1, .3, 1) both; }
    .txfoot.open.anim .tlx li { animation: tlitem 360ms cubic-bezier(.16, 1, .3, 1) both; }
    .txfoot.open.anim .tlx li:nth-child(2) { animation-delay: 40ms; } .txfoot.open.anim .tlx li:nth-child(3) { animation-delay: 80ms; } .txfoot.open.anim .tlx li:nth-child(4) { animation-delay: 120ms; } .txfoot.open.anim .tlx li:nth-child(n+5) { animation-delay: 160ms; }
    @keyframes tlfade { from { opacity: 0; } to { opacity: 1; } }
    @keyframes tlrise { from { transform: translateY(40px); opacity: .6; } to { transform: none; opacity: 1; } }
    @keyframes tlitem { from { transform: translateY(10px); opacity: 0; } to { transform: none; opacity: 1; } }
    @media (prefers-reduced-motion: reduce) { .tlscrim.anim, .txfoot.open.anim, .txfoot.open.anim .tlx li { animation: none; } }
    .tlx { overflow-y: auto; overscroll-behavior: contain; }   /* fixed height so the footer keeps its room in the detail grid */
    .tlx { list-style: none; display: grid; gap: 0; padding-bottom: 6px; }
    .tlx li { position: relative; display: grid; grid-template-columns: 76px 28px minmax(0, 1fr); align-items: center; gap: 10px; padding: 6px 0; }
    .tlx li + li::before { content: ""; position: absolute; left: 99px; top: -30%; height: 60%; width: 2px; background: var(--md3-on-primary-container); opacity: .55; }
    .tlx__t { color: var(--ink); font-size: 14px; text-align: right; display: grid; }
    .tlx__t small { color: var(--md3-neutral-secondary); font-size: 11px; }
    .tlx__d { position: relative; z-index: 1; width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center; background: var(--md3-on-primary-container); color: var(--white); box-shadow: 0 0 0 2px var(--white), 0 0 0 3.5px var(--md3-on-primary-container); }
    .tlx__c { display: grid; gap: 2px; padding: 12px 14px; border-radius: var(--radius); background: #E3F8EA; color: var(--head); }
    .tlx__c b { color: #11823B; font-size: 20px; font-weight: 600; }
    .tlx__c small { color: var(--ink); font-size: 12px; }
    .tlx li.now .tlx__c { box-shadow: inset 0 0 0 1.5px #11823B; }
    .txprog { height: 8px; border-radius: 4px; background: var(--md3-surface-variant); overflow: hidden; }
    .txprog i { display: block; height: 100%; border-radius: 4px; background: #11823B; }
    .btn.dark { background: var(--md3-on-primary-container); color: var(--white); height: 56px; font-size: 18px; font-weight: 500; }
    .btn.dark[disabled] { background: var(--md3-surface-variant); color: var(--white); cursor: not-allowed; }
    .txform { display: grid; gap: 10px; }
    .txform input, .txform textarea { width: 100%; min-height: 52px; padding: 12px 14px; border-radius: 8px; border: 1px solid #2BC4B4; background: #E3F7F4; color: var(--head); font: inherit; }
    .txform textarea { min-height: 76px; resize: vertical; border-color: #E5506A; background: #FBEAED; }
    .txform input::placeholder, .txform textarea::placeholder { color: var(--md3-on-primary-container); }
    .txback { display: none; }
    @media (orientation: portrait) { .txback { display: flex; align-items: center; gap: 8px; min-height: 48px; padding: 0 var(--sp-12); background: var(--white); color: var(--md3-on-primary-container); border-bottom: 1px solid var(--line); width: 100%; } }
    .txopts { display: grid; gap: 8px; }
    .txopt { display: flex; align-items: center; gap: 14px; min-height: 56px; padding: 0 16px; border-radius: 8px; background: var(--md3-background); color: var(--md3-on-primary-container); text-align: left; width: 100%; }
    .txopt .rad { width: 22px; height: 22px; border-radius: 50%; border: 2px solid var(--md3-on-primary-container); display: grid; place-items: center; flex: none; }
    .txopt[aria-checked="true"] .rad { border-color: var(--md3-primary); }
    .txopt[aria-checked="true"] .rad::after { content: ""; width: 12px; height: 12px; border-radius: 50%; background: var(--md3-primary); }
    .txsteps { list-style: none; display: grid; gap: 0; }
    .txsteps li { position: relative; display: flex; gap: 14px; padding: 0 0 18px; }
    .txsteps li::before { content: ""; position: absolute; left: 11px; top: 24px; bottom: 0; width: 2px; background: var(--md3-surface-variant); }
    .txsteps li:last-child::before { display: none; }
    .txsteps li.done::before { background: #11823B; }
    .txsteps .dot { width: 24px; height: 24px; border-radius: 50%; flex: none; border: 2px solid var(--md3-outline-variant); background: var(--white); display: grid; place-items: center; color: var(--white); }
    .txsteps .done .dot { background: #11823B; border-color: #11823B; }
    .txsteps .now .dot { border-color: #11823B; box-shadow: inset 0 0 0 5px var(--white); background: #11823B; }
    .txsteps b { display: block; color: var(--head); font-weight: 500; }
    .txsteps small { color: var(--md3-neutral-secondary); }
    .txsteps li.next b { color: var(--md3-neutral-secondary); font-weight: 400; }
    .sheetlist { display: grid; gap: 8px; }
    .sheetlist div { display: flex; align-items: center; gap: 12px; min-height: 56px; padding: 8px 12px; border-radius: 8px; background: var(--md3-background); }
    .sheetlist .grow { flex: 1; min-width: 0; display: grid; }
    .sheetlist b { color: var(--head); font-weight: 600; }
    .sheetlist small { color: var(--ink); }
    .toast { position: fixed; left: 50%; bottom: 32px; z-index: 40; transform: translate(-50%, 16px); opacity: 0; pointer-events: none; max-width: calc(100% - 32px); padding: 12px 20px; border-radius: 8px; background: var(--md3-on-primary-container); color: var(--white); transition: opacity 200ms var(--ease), transform 200ms var(--ease); }
    .toast.on { opacity: 1; transform: translate(-50%, 0); }
"""

TX_HTML = '''  <div class="dpanel stpanel" id="stpanel" hidden role="dialog" aria-modal="true" aria-labelledby="stT"></div>
  <div class="scrim" id="txsheet" hidden><div class="sheet" role="dialog" aria-modal="true"></div></div>
  <div class="toast t-body-medium" id="toast" role="status" aria-live="polite"></div>'''

TX_JS = r"""  /* ---------------- Sites tab: site transfers (mobile screenshots in secuirty/site transfer, tablet layout) ---------------- */
  var TX = __TX__, TXM = __TXM__, TX_KEY = 'antz.security.tx', TX_V = '__TXV__';
  var TXO = (function () { var s = lsGet(TX_KEY); return s && s.v === TX_V && s.o ? s.o : {}; })();   // per-transfer changes: { id: { st, check, comments, log } }
  function txSave() { lsSet(TX_KEY, { v: TX_V, o: TXO }); }
  function txSt(t) { return (TXO[t.id] && TXO[t.id].st) || t.st; }
  function txTone(t) { return TXM.st[txSt(t)]; }
  var TXTYPE = {}; TXM.types.forEach(function (x) { TXTYPE[x[0]] = x; });
  var STC = { S1: '#2C4F5A', S2: '#5A3B2C', S3: '#2C5A43', S4: '#4A4A2C', S5: '#2C3F5A' };
  var SVGI = {
    art: '<path d="M8 60V30l22-16 22 16v30M16 60V38h28v22M22 60V46h16v14M4 60h56M30 14V6M24 9h12"/>',
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 20c1.5-3.5 4.4-5 8-5s6.5 1.5 8 5"/>',
    phone: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    chat: '<rect x="3.5" y="4.5" width="17" height="13" rx="2"/><path d="M8 21l3-3.5M7.5 9h9M7.5 13h6"/>',
    xfer: '<path d="M4 9h13l-3-3M20 15H7l3 3"/>',
    egg: '<path d="M12 3c3.6 0 6.5 5.4 6.5 10a6.5 6.5 0 0 1-13 0C5.5 8.4 8.4 3 12 3z"/>',
    bin: '<path d="M4 7h16M9 7V4h6v3M6.5 7l1 13h9l1-13M10 11v6M14 11v6"/>',
    turn: '<path d="M5 19v-6a4 4 0 0 1 4-4h10M15 5l4 4-4 4"/>',
    q: '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17.5v.1"/>',
    team: '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c1-3.6 3.8-5.5 7-5.5s6 1.9 7 5.5"/>',
    check: '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.8 2.8L16.5 9.5"/>',
    note: '<path d="M6 3h9l4 4v14H6z"/><path d="M14 3v5h5M9 13h7M9 17h5"/>',
    heart: '<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/><path d="M7 12h3l1.5-2 2 4 1.5-2h2"/>',
    tag: '<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.3"/>',
    paw: '<circle cx="7" cy="9" r="1.8"/><circle cx="11" cy="6" r="1.8"/><circle cx="15" cy="6.5" r="1.8"/><circle cx="18" cy="10" r="1.8"/><path d="M8 17c0-3 2-5 4.5-5S17 14 17 17c0 1.7-1.4 2.6-3 2.2-1-.3-2-.3-3 0-1.6.4-3-.5-3-2.2z"/>',
    filter: '<path d="M4 7h16M7 12h10M10 17h4"/>',
    shield: '<path d="M12 3 19 6v5c0 4.5-3 8-7 10-4-2-7-5.5-7-10V6z"/>',
    comment: '<rect x="3.5" y="4.5" width="17" height="13" rx="2"/><path d="M8 21l3-3.5M7.5 9h9M7.5 13h6"/>',
    plus: '<circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/>',
    image: '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.8"/><path d="m4 18 5-5 4 4 3-3 4 4"/>' };
  function si(k, s, vb) { s = s || 22; return '<svg width="' + s + '" height="' + s + '" viewBox="' + (vb || '0 0 24 24') + '" class="si" aria-hidden="true" focusable="false">' + SVGI[k] + '</svg>'; }
  var QR = (function () { var c = '', x, y, on = function (x, y) { if ((x < 3 && y < 3) || (x > 7 && y < 3) || (x < 3 && y > 7)) return !(x % 3 === 1 && y % 3 === 1) || (x % 10 === 1 && y % 10 === 1); return ((x * 7 + y * 13 + x * y) % 5) < 2; };
    for (y = 0; y < 11; y++) for (x = 0; x < 11; x++) if (on(x, y)) c += '<rect x="' + x + '" y="' + y + '" width="1" height="1"/>';
    return '<svg class="qr" viewBox="0 0 11 11" aria-label="Transfer QR code" role="img" fill="#000">' + c + '</svg>'; })();
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function dt(iso) { var p = iso.split(/[-T:]/).map(Number), h = p[3] % 12 || 12; return ('0' + p[2]).slice(-2) + ' ' + MON[p[1] - 1] + ' ' + p[0] + ' • ' + ('0' + h).slice(-2) + ':' + ('0' + p[4]).slice(-2) + (p[3] < 12 ? ' AM' : ' PM'); }
  function dshort(iso) { var p = iso.split(/[-T:]/).map(Number); return p[2] + ' ' + MON[p[1] - 1]; }
  function nowIso() { var d = new Date(2026, 8, 30, new Date().getHours(), new Date().getMinutes()), p = function (n) { return ('0' + n).slice(-2); }; return '2026-09-30T' + p(d.getHours()) + ':' + p(d.getMinutes()); }
  function avi(n) { return '<span class="av" aria-hidden="true">' + initials(n) + '</span>'; }
  var tst; function toast(m) { var t = document.getElementById('toast'); t.textContent = m; t.classList.add('on'); clearTimeout(tst); tst = setTimeout(function () { t.classList.remove('on'); }, 2400); }
  var TXF = {}, TXQ = '';   // filter per type: '' | 'in' | 'out'
  function txOf(site, type) { var f = TXF[type] || ''; return TX[site].filter(function (t) { return t.type === type && (!f || txTone(t)[2] === f); }); }
  function pendCount(site) { return TX[site].filter(function (t) { return txTone(t)[2]; }).length; }
  function unit(t) { return t.type === 'animal' ? (t.qty + (t.qty === 1 ? ' Animal' : ' Animals')) : t.type === 'hospital' ? 'Animals: <b>1</b>' : t.type === 'carcass' ? 'Carcasses: <b>1</b>' : (t.qty + (t.qty === 1 ? ' egg' : ' eggs')); }
  function countLabel(type, n) { return n + ' ' + (type === 'egg' ? (n === 1 ? 'Egg transfer' : 'Egg transfers') : type === 'discard' ? (n === 1 ? 'Egg discard' : 'Egg discards') : (n === 1 ? 'Transfer' : 'Transfers')); }

  function txSites() {
    var q = TXQ.toLowerCase(), list = SD.sites.filter(function (s) { return !q || s.name.toLowerCase().indexOf(q) !== -1 || inch(s.id).toLowerCase().indexOf(q) !== -1; });
    var main = document.getElementById('main');
    if (!main.querySelector('.stsearch')) main.innerHTML = '<div class="stsearchrow"><div class="spsearch stsearch">' + ic('search', 22) + '<input type="search" id="stq" placeholder="Search sites or in-charge" aria-label="Search sites" autocomplete="off"></div>' + (VIEWER.key === 'security-admin' ? '<a class="btn add" href="#sites/manage" style="height:48px">Manage sites</a>' : '') + '</div><div class="stcards" id="stcards"></div>';
    document.getElementById('stcards').innerHTML = list.length ? list.map(function (s) {
      var p = pendCount(s.id), n = TX[s.id].length;
      return '<a class="stcard" href="#sites/' + s.id + '" style="--stc:' + STC[s.id] + '"><span class="stcard__art">' + si('art', 150, '0 0 64 64') + '</span>' +
        '<span class="stcard__top"><b>' + esc(s.name) + '</b><small>' + n + ' transfers</small>' + (p ? '<span class="stcard__pend">' + p + ' pending security</span>' : '') + '</span>' +
        '<span class="stcard__foot"><span class="t-body-regular">' + si('user', 18) + esc(inch(s.id)) + '</span>' +
        '<button type="button" class="ricon" data-call="' + esc(inch(s.id)) + '" aria-label="Call ' + esc(inch(s.id)) + '">' + si('phone', 20) + '</button><button type="button" class="ricon" data-msg="' + esc(inch(s.id)) + '" aria-label="Message ' + esc(inch(s.id)) + '">' + si('chat', 20) + '</button></span></a>';
    }).join('') : '<div class="empty"><b class="t-minor-title">No sites match</b><span class="t-body-regular">Try another name.</span></div>';
  }
  document.getElementById('main').addEventListener('input', function (e) { if (e.target.id === 'stq') { TXQ = e.target.value; txSites(); } });

  function card(t, cur) {
    var st = txTone(t), sel = ' aria-current="' + (t.id === cur) + '"', h = '#sites/' + t.site + '/' + t.type + '/' + t.id;
    var stTxt = '<span class="txst ' + st[1] + '">' + esc(st[0]) + '</span>';
    if (t.type === 'hospital' || t.type === 'carcass') {
      return '<a class="txc" href="' + h + '"' + sel + '><span class="txtop"><span>Requested by <b>' + esc(t.by.split(' ')[0]) + '</b></span><span>' + dt(t.at) + '</span></span>' +
        '<span class="txc__r"><span class="grow"><span class="txid plain">' + t.id + '</span><span class="txmeta t-body-regular">' + unit(t) + '</span>' +
        '<span class="txplace"><span class="mk fr"></span>' + esc(t.fr) + '</span><span class="txplace"><span class="mk to"></span>' + esc(t.to) + '</span></span>' + ic('back', 20).replace('<svg', '<svg style="transform:rotate(180deg);color:var(--md3-neutral-secondary)"') + '</span>' +
        '<span class="txband ' + st[1] + '">' + esc(st[0]) + '</span></a>';
    }
    if (t.type === 'discard') {
      var c = (TXO[t.id] && TXO[t.id].check) || t.check;
      return '<a class="txc" href="' + h + '"' + sel + '><span class="txc__r"><span class="grow"><span class="txid red">' + si('egg', 16) + t.id + '</span><span class="txmeta t-minor-medium" style="color:var(--head)">' + unit(t) + '</span><span class="txmeta t-body-regular">' + dt(t.at) + '</span><span class="txby">' + avi(t.by) + esc(t.by) + '</span></span>' + stTxt + '</span>' +
        (c ? '<span class="txchk"><b>' + avi(c.name).replace('class="av"', 'class="av" style="width:32px;height:32px;background:#00C2B0;color:#fff"') + esc(c.name) + '<span>' + si('shield', 16) + '</span></b><small>Site: ' + esc(t.fr) + '</small>' + (c.note ? '<span class="t-body-regular">' + esc(c.note) + '</span>' : '') + '</span>' : '') + '</a>';
    }
    return '<a class="txc" href="' + h + '"' + sel + '><span class="txc__r"><span class="grow"><span class="txid' + (t.type === 'animal' ? ' plain" style="font-size:15px;color:var(--head)' : '') + '">' + si('xfer', 16) + t.id + '</span>' +
      '<span class="txplace t-minor-title"><span class="mk ' + (t.type === 'egg' && t.toSite === t.fr ? 'fr' : 'to') + '"></span><b>' + esc(t.to) + '</b></span><span class="txmeta t-body-regular">' + unit(t) + '</span><span class="txmeta t-body-regular">' + dt(t.at) + '</span></span>' + stTxt + '</span></a>';
  }

  function action(t) {
    var p = txTone(t)[2];
    if (t.type === 'discard') return p ? '<button type="submit" form="txdf" class="btn dark">Confirm discard</button>' : '';
    if (p === 'out') return '<button type="button" class="btn dark" data-txact="out">Security Checkout</button>';
    if (p === 'in') return '<button type="button" class="btn dark" data-txact="in">Security Check-in</button>';
    return '';
  }

  function detail(t) {
    var st = txTone(t), red = t.type === 'discard' || t.type === 'carcass', o = TXO[t.id] || {}, steps = TXM.steps[t.type], at = TXM.at[t.type][txSt(t)] || 0;
    var by = '<span class="txby">' + avi(t.by) + esc(t.by) + '<button type="button" class="ricon" data-call="' + esc(t.by) + '" aria-label="Call ' + esc(t.by) + '">' + si('phone', 18) + '</button><button type="button" class="ricon" data-msg="' + esc(t.by) + '" aria-label="Message ' + esc(t.by) + '">' + si('chat', 18) + '</button></span>';
    var head = '<div class="txdh" style="--txh:' + (red ? '#4D0A1F' : t.type === 'hospital' ? '#1F415B' : '#1F515B') + '"><h3 id="txT">' + t.id + '</h3><div class="txdh__r"><div class="grow">' +
      (t.type === 'animal' ? '<span class="sub">Inter-site Transfer</span>' : t.type === 'hospital' ? '<span class="sub">Hospitalize animal</span>' : t.type === 'carcass' ? '<span class="sub">Carcass Transfer</span>' : '') +
      '<span class="txplace"><span class="mk fr"></span><b>' + esc(t.fr) + '</b></span>' +
      (t.type === 'discard' ? '<span class="txplace">' + si('egg', 18) + '<b>' + t.qty + (t.qty === 1 ? ' Egg' : ' Eggs') + '</b></span>' : '<span class="txplace"><span class="mk to"></span><b>' + esc(t.to) + '</b>' + (t.type === 'egg' ? '<small>' + esc(t.toSite) + '</small>' : '') + '</span>') +
      '<span class="sub t-body-regular">' + dt(t.at) + '</span>' + by + '</div>' + QR + '</div></div>';
    var rows = '', row = function (ico, lab, val, view, cls) { return '<div class="txrow' + (cls ? ' ' + cls : '') + '"><span class="stico">' + si(ico, 24) + '</span><span class="grow"><small>' + lab + '</small><b>' + val + '</b></span>' + (view ? '<button type="button" class="linkbtn" data-txview="' + view + '">View</button>' : '') + '</div>'; };
    if (t.type === 'animal') {
      rows = row('turn', 'Transfer', unit(t), 'animals') + row('q', 'Reason for transfer', esc(t.reason)) + row('team', 'Transfer Team', t.team + ' Members', 'team') +
        '<div class="txrow"><span class="stico" style="color:var(--md3-on-surface)">' + si('check', 24) + '</span><div class="txappr"><small style="color:var(--ink)">Approved by</small>' + t.approvers.map(function (a) { return '<div>' + avi(a[0]) + '<span class="grow" style="display:grid"><b>' + esc(a[0]) + '</b><small>' + a[1] + ': ' + esc(a[2]) + '</small></span><span class="ok">' + si('check', 22) + '</span></div>'; }).join('') + '</div></div>' +
        '<div class="txrow"><span class="stico" style="color:#00AFD6">' + si('check', 24) + '</span><span class="grow"><b style="font-size:15px">Transfer Checklist</b></span><span class="ring">' + t.checklist + '/7</span></div>';
    } else if (t.type === 'egg') {
      rows = '<div class="txrow"><span class="mk fr"></span><span class="grow"><small>From</small><b>Site : ' + esc(t.fr) + '</b></span></div><div class="txrow"><span class="mk to"></span><span class="grow"><small>To</small><b>' + esc(t.to) + '</b><small style="font-size:14px">Site : ' + esc(t.toSite) + '</small></span></div>' + row('turn', 'Transfer', t.qty + (t.qty === 1 ? ' Egg' : ' Eggs'), 'eggs');
    } else if (t.type === 'discard') {
      rows = '<div class="txrow plain"><span class="mk fr"></span><span class="grow"><small>Site</small><b>' + esc(t.fr) + '</b></span></div>' + '<div class="txrow plain"><span class="stico" style="color:#E93353">' + si('bin', 24) + '</span><span class="grow"><small>Discard</small><b>' + t.qty + (t.qty === 1 ? ' Egg' : ' Eggs') + '</b></span><button type="button" class="linkbtn" style="color:#C3213F" data-txview="eggs">View</button></div>' +
        '<div class="txrow plain"><span class="stico" style="color:#E4B819">' + si('note', 24) + '</span><span class="grow"><small>Notes</small><b>' + esc(t.note) + '</b></span></div>' +
        '<div class="txsec"><span class="grow t-minor-medium">Attachments</span></div><div class="txphotos">' + Array.apply(null, Array(t.photos)).map(function () { return '<div class="txphoto"><div>' + si('image', 36) + '</div><p>Discard request generated<br><b style="color:var(--head)">' + esc(t.by) + '</b> · ' + dshort(t.at) + '</p></div>'; }).join('') + '</div>';
      if (txTone(t)[2]) rows += '<div class="txsec">' + si('shield', 20) + '<span class="grow">Security check</span></div><form class="txform" id="txdf" data-txdiscard style="padding:0 20px 16px"><input type="text" name="g" placeholder="Enter security name*" aria-label="Security name" required value="' + esc(VIEWER.name) + '"><textarea name="c" placeholder="Add comments if any" aria-label="Comments"></textarea></form>';
      var c = o.check || t.check; if (c) rows += '<div class="txsec">' + si('shield', 20) + '<span class="grow">Security check</span></div><div class="txcom"><div class="txcm">' + avi(c.name) + '<div><b>' + esc(c.name) + '</b> <small>Site: ' + esc(t.fr) + '</small><p>' + esc(c.note || 'No comments') + '</p></div></div></div>';
    } else {
      var a = t.animal;
      rows = '<div class="txsec">' + si('paw', 20) + '<span class="grow">' + (t.type === 'carcass' ? 'Selected carcass' : 'Selected animal') + '</span></div>' +
        '<div class="txani' + (red ? ' red' : '') + '"><span class="txani__img"><i>' + a[5] + '</i>' + si('paw', 44) + '</span><span class="grow"><b>AAID: ' + a[2] + '</b>' + (t.type === 'carcass' && a[4] ? '<b>Marking: ' + esc(a[4]) + '</b>' : '') + '<b>' + esc(a[0]) + '</b><em>' + esc(a[1]) + '</em><b>Encl: ' + esc(a[3]) + '</b></span></div>';
      if (t.type === 'hospital') rows += '<div class="txgrid2"><div><small>' + si('heart', 22) + 'Medical ID</small><b>' + t.med + '</b></div><div><small>' + si('tag', 22) + 'Visit type</small><b>' + esc(t.visit) + '</b></div></div>' + row('q', 'Purpose for visit', esc(t.purpose), '', 'plain') + '<div class="txrow plain"><span class="stico" style="color:var(--md3-on-surface)">' + si('check', 24) + '</span><span class="grow"><small>Transfer Checklist</small><b>' + t.checklist + '/7 Filled</b></span></div>';
    }
    var cms = (o.comments || []);
    var com = '<div class="txsec">' + si('comment', 20) + '<span class="grow">Comments</span><small style="color:var(--ink)">' + cms.length + '</small></div><div class="txcom">' + cms.map(function (c) { return '<div class="txcm">' + avi(c.by) + '<div><b>' + esc(c.by) + '</b> <small>' + dt(c.at) + '</small><p>' + esc(c.text) + '</p></div></div>'; }).join('') +
      '<form data-txcom>' + avi(VIEWER.name).replace('class="av"', 'class="av" style="width:32px;height:32px;font-size:12px"') + '<input type="text" name="c" placeholder="Add your comment" aria-label="Add your comment" autocomplete="off"><button type="submit" class="send" aria-label="Send comment"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20.5 21 12 3 3.5l2.5 8.5zm2.5-8.5H13"/></svg></button></form></div>';
    var when = (o.log && o.log.length ? o.log[o.log.length - 1].at : t.at);
    var foot = tlFoot(txEvents(t), esc(st[0]) + (st[2] ? ' at ' + esc(t.fr) : ''), 'Current Status • ' + dshort(when), '<div class="txprog" aria-hidden="true"><i style="width:' + Math.round(at / (steps.length - 1) * 100) + '%"></i></div>' + action(t));
    return '<div class="txdb">' + head + rows + com + '</div>' + foot;
  }

  /* timeline in the detail footer (mobile IMG_0644): See all opens it above the current status, Hide closes it.
     Newest first: time, a ticked dot, and a green card with the event and its value. */
  var TXTL = false;
  function tmin(iso, m) { var d = new Date(iso + ':00'); d.setMinutes(d.getMinutes() + m); var p = function (n) { return ('0' + n).slice(-2); }; return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate()) + 'T' + p(d.getHours()) + ':' + p(d.getMinutes()); }
  function tl12(iso) { var p = iso.split(/[-T:]/).map(Number), h = p[3] % 12 || 12; return h + ':' + ('0' + p[4]).slice(-2) + (p[3] < 12 ? ' AM' : ' PM'); }
  function tlHtml(ev) { return '<ol class="tlx" aria-label="Timeline" style="height:min(42dvh, ' + (ev.length * 74 + 6) + 'px)">' + ev.map(function (e) { return '<li' + (e.now ? ' class="now"' : '') + '><span class="tlx__t">' + tl12(e.at) + '<small>' + dshort(e.at) + '</small></span><span class="tlx__d" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="m5 12 5 5 9-10"/></svg></span><span class="tlx__c"><span>' + esc(e.title) + '</span>' + (e.val ? '<b>' + esc(e.val) + '</b>' : '') + (e.by ? '<small>' + esc(e.by) + '</small>' : '') + '</span></li>'; }).join('') + '</ol>'; }
  var TXTLA = false;   /* play the slide-up only on the tap that opens it, not on every re-render */
  function tlFoot(ev, title, small, extra) { var a = TXTLA; TXTLA = false; return (TXTL ? '<button type="button" class="tlscrim' + (a ? ' anim' : '') + '" data-txsteps aria-label="Close timeline"></button>' : '') + '<div class="txfoot' + (TXTL ? ' open' + (a ? ' anim' : '') : '') + '"' + (TXTL ? ' role="dialog" aria-label="Timeline"' : '') + '>' + (TXTL ? tlHtml(ev) : '') + '<div class="txfoot__h"><span class="grow"><small>' + small + '</small><b>' + title + '</b></span><button type="button" class="linkbtn" style="min-height:44px;color:var(--md3-on-surface)" data-txsteps aria-expanded="' + TXTL + '">' + (TXTL ? 'Hide' : 'See all') + '</button></div>' + extra + '</div>'; }
  function txEvents(t) {
    var steps = TXM.steps[t.type], at = TXM.at[t.type][txSt(t)] || 0, log = (TXO[t.id] || {}).log || [], st = txTone(t), ev = [], n = Number(t.id.replace(/\D/g, '')) || 1;
    var vals = { animal: [['Animals loaded for transfer', t.qty + '/' + t.qty], ['Temperature checked', (24 + n % 5) + '°C']], egg: [['Eggs packed in the carrier', t.qty + '/' + t.qty], ['Carrier temperature', (37 + (n % 2) * .5) + '°C']],
      discard: [['Eggs counted', t.qty + (t.qty === 1 ? ' egg' : ' eggs')]], hospital: [['Animal loaded', '1/1'], ['Transfer checklist', (t.checklist || 0) + '/7']], carcass: [['Carcass bagged and sealed', '1/1']] }[t.type] || [];
    var k = 0, push = function (title, val, by) { ev.push({ at: tmin(t.at, 20 * k++), title: title, val: val, by: by }); };
    for (var i = 0; i <= at && i < steps.length; i++) {
      if (i === 0) push(steps[0], '', t.by);
      else if (i === at && st[2]) { vals.forEach(function (v) { push(v[0], v[1]); }); vals = []; push(st[0] + ' at ' + t.fr, ''); ev[ev.length - 1].now = true; }
      else { if (/Security/.test(steps[i]) && vals.length) { vals.forEach(function (v) { push(v[0], v[1]); }); vals = []; } push(steps[i], ''); }   /* loading checks come just before security */
    }
    if (at === 0 && st[2]) { vals.forEach(function (v) { push(v[0], v[1]); }); push(st[0] + ' at ' + t.fr, ''); ev[ev.length - 1].now = true; }
    log.forEach(function (l) { ev.push({ at: l.at, title: l.kind === 'out' ? (t.type === 'discard' ? 'Discard confirmed' : 'Security checkout done') : 'Security check-in done', val: '', by: l.by }); });
    if (!ev.some(function (e) { return e.now; }) && ev.length) ev[ev.length - 1].now = true;
    return ev.reverse();
  }
  var TXCUR = null;
  function txPanel(r) {
    var P = document.getElementById('stpanel'), keepDb = (P.querySelector('.txdb') || {}).scrollTop || 0, keepLs = (P.querySelector('.txlist') || {}).scrollTop || 0, keepId = TXCUR && TXCUR.id, s = sby(SD.sites, r.id); if (!s.id) { location.hash = '#sites'; return; }
    var type = TXTYPE[r.type] ? r.type : 'animal', list = txOf(s.id, type), land = matchMedia('(orientation: landscape)').matches;
    var cur = r.tx ? TX[s.id].filter(function (t) { return t.id === r.tx; })[0] : (land ? list[0] : null);
    TXCUR = cur || null;
    var f = TXF[type] || '';
    P.innerHTML = '<div class="sthero" style="--stc:' + STC[s.id] + '"><a class="iconbtn" href="#sites" aria-label="Back to Sites">' + ic('back', 24) + '</a><span class="stcard__art">' + si('art', 220, '0 0 64 64') + '</span>' +
      '<div class="sthero__t"><small>SITE</small><h2 id="stT">' + esc(s.name) + '</h2></div><div class="sthero__p"><span class="stpill t-body-medium">' + si('user', 18) + esc(inch(s.id)) + '</span><button type="button" class="ricon" data-call="' + esc(inch(s.id)) + '" aria-label="Call ' + esc(inch(s.id)) + '">' + si('phone', 20) + '</button><button type="button" class="ricon" data-msg="' + esc(inch(s.id)) + '" aria-label="Message ' + esc(inch(s.id)) + '">' + si('chat', 20) + '</button></div>' +
      '<button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role" style="position:absolute;right:12px;top:10px"></button></div>' +
      '<nav class="txtabs" role="tablist" aria-label="Transfer types">' + TXM.types.map(function (x) { var p = TX[s.id].filter(function (t) { return t.type === x[0] && txTone(t)[2]; }).length; return '<a class="txtab t-body-medium" role="tab" href="#sites/' + s.id + '/' + x[0] + '" aria-selected="' + (x[0] === type) + '">' + x[1] + (p ? '<span class="n" aria-label="' + p + ' pending">' + p + '</span>' : '') + '</a>'; }).join('') + '</nav>' +
      '<div class="txbody' + (type === 'discard' || type === 'carcass' ? ' red' : '') + (r.tx && cur ? ' sel' : '') + '"><div class="txlist"><div class="txbar"><h3 class="t-minor-medium">' + countLabel(type, list.length) + '</h3><button type="button" class="txfilt t-minor-medium' + (f ? ' on' : '') + '" data-txfilter aria-haspopup="dialog">' + (f ? (f === 'in' ? 'Check-in pending' : type === 'discard' ? 'Check pending' : 'Checkout pending') : 'Show All') + si('filter', 22) + '</button></div>' +
      '<div class="txcards">' + (list.length ? list.map(function (t) { return card(t, cur && cur.id); }).join('') : '<div class="txempty t-body-regular">Nothing ' + (f ? 'pending here' : 'here yet') + '.</div>') + '</div></div>' +
      '<section class="txdet" aria-labelledby="txT">' + (cur ? '<div style="display:contents">' + '</div>' : '') + (cur ? '<div style="min-height:0;display:grid;grid-template-rows:auto 1fr auto;overflow:hidden"><a class="txback t-body-medium" href="#sites/' + s.id + '/' + type + '">' + ic('back', 20) + 'All ' + TXTYPE[type][1].toLowerCase() + 's</a>' + detail(cur).replace('<div class="txdb">', '<div class="txdb" style="min-height:0">') + '</div>' : '<div class="txempty t-body-regular" style="align-self:center">Pick a transfer to see it here.</div>') + '</section></div>';
    P.hidden = false; [].forEach.call(P.querySelectorAll('.asbtn'), function (b) { b.innerHTML = ic('user', 20) + '<span class="t-body-medium">Viewing as: ' + esc(VIEWER.name) + ' <small>\u00b7 ' + esc(VIEWER.title) + '</small></span>' + ic('dropdown', 18); });
    var sel = P.querySelector('.txc[aria-current="true"]'); if (sel && !r.keep) sel.scrollIntoView({ block: 'nearest' });
    if (r.keep) { var l1 = P.querySelector('.txlist'), d1 = P.querySelector('.txdb'); if (l1) l1.scrollTop = keepLs; if (d1 && keepId && TXCUR && keepId === TXCUR.id) d1.scrollTop = keepDb; }
  }
  function sheet2(html) { var S = document.getElementById('txsheet'); S.firstChild.innerHTML = '<div class="grab"></div>' + html; S.hidden = false; }
  function sheetHead(t, sub) { return '<div class="sheet__h"><div><h2 class="t-major-title">' + t + '</h2>' + (sub ? '<p class="t-body-regular" style="color:var(--ink)">' + sub + '</p>' : '') + '</div><button type="button" class="iconbtn" data-txclose aria-label="Close">' + ic('close', 24) + '</button></div>'; }
  function advance(t, kind, extra) {
    var nx = { animal: { out: 'transit', in: 'done' }, egg: { out: 'transit', in: 'done' }, hospital: { out: 'transit', in: 'done' }, carcass: { out: 'transit', in: 'done' }, discard: { out: 'dchecked' } }[t.type][kind];
    var o = TXO[t.id] = TXO[t.id] || {}; o.st = nx; o.log = (o.log || []).concat([{ at: nowIso(), by: VIEWER.name, kind: kind }]); if (extra) o.check = extra; txSave();
  }
  document.getElementById('stpanel').addEventListener('click', function (e) {
    var b, t = TXCUR, r = sparse();
    if ((b = e.target.closest('[data-call]'))) { e.preventDefault(); toast('Calling ' + b.getAttribute('data-call') + ' (demo)'); return; }
    if ((b = e.target.closest('[data-msg]'))) { e.preventDefault(); toast('Message to ' + b.getAttribute('data-msg') + ' (demo)'); return; }
    if (e.target.closest('[data-txfilter]')) {
      var type = r.type || 'animal', f = TXF[type] || '', opts = type === 'discard' ? [['', 'Show All'], ['out', 'Security Check Pending']] : [['', 'Show All'], ['in', 'Security Check-in Pending'], ['out', 'Security Checkout Pending']];
      sheet2(sheetHead('Filter by', TXTYPE[type][1]) + '<div class="txopts" role="radiogroup">' + opts.map(function (x) { var n = TX[r.id].filter(function (t) { return t.type === type && (!x[0] || txTone(t)[2] === x[0]); }).length; return '<button type="button" class="txopt t-minor-medium" role="radio" aria-checked="' + (x[0] === f) + '" data-txf="' + x[0] + '"><span class="rad"></span><span style="flex:1">' + x[1] + '</span><span class="t-body-regular" style="color:var(--ink)">' + n + '</span></button>'; }).join('') + '</div>');
      return;
    }
    if (!t) return;
    if ((b = e.target.closest('[data-txview]'))) {
      var v = b.getAttribute('data-txview');
      if (v === 'animals') sheet2(sheetHead(unit(t), t.id) + '<div class="sheetlist">' + t.animals.map(function (a) { return '<div><span class="av">' + si('paw', 20) + '</span><span class="grow"><b>' + esc(a[0]) + '</b><small><em>' + esc(a[1]) + '</em> · AAID ' + a[2] + ' · ' + esc(a[3]) + '</small></span></div>'; }).join('') + '</div>');
      else if (v === 'team') { var names = ['Mahesh Rathod', 'Kiran Joshi', 'Neha Bansal', 'Arjun Mehta', 'Lata Rao', 'Reena Patil', 'Dilip Vaghela', 'Sourav Tambe']; sheet2(sheetHead(t.team + ' members', 'Transfer team for ' + t.id) + '<div class="sheetlist">' + Array.apply(null, Array(Math.min(t.team, 8))).map(function (_, i) { return '<div>' + avi(names[i]) + '<span class="grow"><b>' + names[i] + '</b><small>' + ['Keeper', 'Vet', 'Driver', 'Curator'][i % 4] + '</small></span></div>'; }).join('') + (t.team > 8 ? '<p class="t-body-regular" style="color:var(--ink)">and ' + (t.team - 8) + ' more</p>' : '') + '</div>'); }
      else sheet2(sheetHead(t.qty + (t.qty === 1 ? ' egg' : ' eggs'), t.id) + '<div class="sheetlist">' + Array.apply(null, Array(t.qty)).map(function (_, i) { return '<div><span class="av">' + si('egg', 20) + '</span><span class="grow"><b>Egg ' + (i + 1) + (t.species ? ' · ' + esc(t.species[0]) : '') + '</b><small>' + (t.type === 'discard' ? esc(t.note) : 'Clutch ' + t.id.slice(-3)) + '</small></span></div>'; }).join('') + '</div>');
      return;
    }
    if (e.target.closest('[data-txsteps]')) { TXTL = !TXTL; TXTLA = TXTL; txRoute(true); return; }
    if ((b = e.target.closest('[data-txact]'))) {
      var k = b.getAttribute('data-txact');
      sheet2(sheetHead(k === 'out' ? 'Security checkout' : 'Security check-in', t.id + ' · ' + (k === 'out' ? 'leaving ' + esc(t.fr) : 'arriving at ' + esc(t.to))) +
        '<p class="t-body-regular" style="color:var(--ink)">Check the ' + (t.type === 'animal' ? 'animals, crates and transfer team' : t.type === 'egg' ? 'egg count and the carrier' : t.type === 'carcass' ? 'carcass bag seal and vehicle' : 'animal and the vehicle') + ' against this transfer before you confirm.</p>' +
        '<form class="txform" data-txconfirm="' + k + '"><input type="text" name="g" placeholder="Enter security name*" aria-label="Security name" required value="' + esc(VIEWER.name) + '"><textarea name="c" placeholder="Add comments if any" aria-label="Comments"></textarea><button type="submit" class="btn dark">' + (k === 'out' ? 'Confirm checkout' : 'Confirm check-in') + '</button></form>');
      return;
    }
  });
  document.getElementById('stpanel').addEventListener('submit', function (e) {
    var f = e.target, t = TXCUR; e.preventDefault(); if (!t) return;
    if (f.hasAttribute('data-txcom')) { var v = f.c.value.trim(); if (!v) return; var o = TXO[t.id] = TXO[t.id] || {}; o.comments = (o.comments || []).concat([{ by: VIEWER.name, at: nowIso(), text: v }]); txSave(); txRoute(true); return; }
    if (f.hasAttribute('data-txdiscard')) { if (!f.g.value.trim()) { f.g.focus(); return; } advance(t, 'out', { name: f.g.value.trim(), note: f.c.value.trim() }); toast(t.id + ': discard confirmed'); txRoute(true); }
  });
  document.getElementById('stpanel').addEventListener('input', function (e) { var f = e.target.form, b = document.querySelector('[form="txdf"]'); if (f && f.hasAttribute('data-txdiscard') && b) b.disabled = !f.g.value.trim(); });
  var TXS = document.getElementById('txsheet');
  TXS.addEventListener('click', function (e) {
    var b; if (e.target === TXS || e.target.closest('[data-txclose]')) { TXS.hidden = true; return; }
    if ((b = e.target.closest('[data-txf]'))) { var r = sparse(); TXF[r.type || 'animal'] = b.getAttribute('data-txf'); TXS.hidden = true; location.hash = '#sites/' + r.id + '/' + (r.type || 'animal'); txRoute(true); }
  });
  TXS.addEventListener('submit', function (e) {
    var f = e.target, t = TXCUR; e.preventDefault(); if (!t || !f.hasAttribute('data-txconfirm')) return; if (!f.g.value.trim()) { f.g.focus(); return; }
    var k = f.getAttribute('data-txconfirm'); advance(t, k); var o = TXO[t.id]; if (f.c.value.trim()) { o.comments = (o.comments || []).concat([{ by: f.g.value.trim(), at: nowIso(), text: f.c.value.trim() }]); txSave(); }
    TXS.hidden = true; toast(t.id + (k === 'out' ? ': checked out, now in transit' : ': checked in, transfer completed')); txRoute(true);
  });
  document.getElementById('main').addEventListener('click', function (e) { var b; if ((b = e.target.closest('[data-call]'))) { e.preventDefault(); toast('Calling ' + b.getAttribute('data-call') + ' (demo)'); } else if ((b = e.target.closest('[data-msg]'))) { e.preventDefault(); toast('Message to ' + b.getAttribute('data-msg') + ' (demo)'); } });
  function txRoute(keep) { var r = sparse(); if (r.tab !== 'sites' || !r.id) { document.getElementById('stpanel').hidden = true; TXCUR = null; return false; } r.keep = keep; txPanel(r); return true; }
  matchMedia('(orientation: landscape)').addEventListener('change', function () { if (!document.getElementById('stpanel').hidden) txRoute(true); });
  document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; if (TXTL && TXS.hidden) { TXTL = false; e.stopImmediatePropagation(); if (!document.getElementById('gtpanel').hidden) gtRe(); else txRoute(true); return; } if (!TXS.hidden) TXS.hidden = true; else if (!document.getElementById('stpanel').hidden && RS.hidden) location.hash = '#sites'; });
"""
