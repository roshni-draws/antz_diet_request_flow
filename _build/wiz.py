# wiz.py: exec'd by sp3.py. "Add a diet" flows (create wizard) from the Dev system diet-editor.js,
# rendered in the Antz app style. Inserted into SpModule's closure.
LOOK = json.load(open(os.path.join(HERE, 'lookups.json')))
LOOK['items'] = LOOK['items'] + SAMPLE_ITEMS   # SAMPLE DATA citrus items for the kitchen auto-resolution demo
LOOK_EMBED = json.dumps({'items': [i for i in LOOK['items']], 'mixes': LOOK['mixes'], 'timeBands': LOOK['timeBands'],
                         'reasons': LOOK['reasons'], 'dietitians': LOOK['dietitians']}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')

WIZ_CSS = '''    /* =========================================================
       13. ADD A DIET  (create wizard, item sheet, diet picker, kind menu)
       ========================================================= */
    .wiz { position: fixed; inset: var(--status-h) 0 0 0; z-index: 25; display: grid; grid-template-rows: auto auto 1fr auto; background: var(--md3-background); }
    .wiz[hidden] { display: none; }
    .wiz .bar__hd small { color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
    .steps { display: flex; gap: 6px; padding: 10px var(--sp-16); background: var(--white); border-bottom: 1px solid var(--line); overflow-x: auto; scrollbar-width: none; }
    .steps span { display: inline-flex; align-items: center; gap: 6px; height: 32px; padding: 0 12px; border-radius: 999px; background: var(--neutral05); color: var(--md3-neutral-secondary); white-space: nowrap; font-size: 13px; font-weight: 500; }
    .steps span.on { background: var(--md3-on-primary-container); color: var(--white); }
    .steps span.done { background: var(--md3-on-background); color: var(--md3-on-surface); }
    .wiz__body { overflow-y: auto; padding: var(--sp-16) var(--sp-16) var(--sp-32); }
    .wiz__inner { max-width: 880px; margin: 0 auto; display: grid; gap: var(--sp-16); }
    .wiz__foot { display: flex; align-items: center; gap: var(--sp-12); padding: var(--sp-12) var(--sp-16); background: var(--white); border-top: 1px solid var(--line); }
    .wiz__foot .sp { flex: 1; }
    .wiz__foot .btn { flex: none; min-width: 120px; padding: 0 var(--sp-20); }
    .btn[disabled] { opacity: .45; cursor: not-allowed; }
    .btn.ghost { color: var(--md3-on-primary-container); }
    .wcard { background: var(--white); border-radius: var(--radius); padding: var(--sp-20); display: grid; gap: var(--sp-16); }
    .wcard h2 { color: var(--head); }
    .wcard > p.sub { color: var(--ink); margin-top: -10px; }
    .ocards { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--sp-12); }
    .ocard { position: relative; display: grid; gap: 8px; align-content: start; text-align: left; padding: var(--sp-16); min-height: 120px; border-radius: var(--radius); border: 1px solid var(--md3-outline-variant); background: var(--white); transition: border-color 200ms var(--ease), box-shadow 200ms var(--ease); }
    .ocard[aria-pressed="true"] { border-color: var(--md3-primary); box-shadow: 0 0 0 1px var(--md3-primary); background: rgba(55,189,105,.04); }
    .ocard .oi { width: 40px; height: 40px; border-radius: 8px; display: grid; place-items: center; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .ocard b { color: var(--head); }
    .ocard span.s { color: var(--ink); }
    .ocard ul { list-style: none; display: grid; gap: 4px; color: var(--md3-on-surface); }
    .ocard ul li { display: flex; gap: 6px; align-items: center; }
    .ocard .rec { position: absolute; top: 12px; right: 12px; }
    .fld { display: grid; gap: 6px; min-width: 0; }
    .fld > span { color: var(--ink); font-size: 14px; font-weight: 500; }
    .fld > span .req { color: var(--md3-error); }
    .fld input, .fld select, .fld textarea { width: 100%; min-height: 48px; padding: 10px 12px; border: 1px solid var(--md3-outline-variant); border-radius: 8px; background: var(--white); color: var(--head); font: inherit; font-size: 15px; }
    .fld textarea { min-height: 80px; resize: vertical; }
    .fld select { appearance: none; background-image: linear-gradient(45deg, transparent 50%, #44544A 50%), linear-gradient(135deg, #44544A 50%, transparent 50%); background-position: calc(100% - 18px) 21px, calc(100% - 13px) 21px; background-size: 5px 5px; background-repeat: no-repeat; padding-right: 36px; }
    .fld input:focus, .fld select:focus, .fld textarea:focus { outline: none; border-color: var(--md3-on-primary-container); box-shadow: 0 0 0 2px rgba(31,81,91,.15); }
    .fld.err input, .fld.err select { border-color: var(--md3-error); }
    .fld .help { color: var(--md3-neutral-secondary); font-size: 12px; }
    .fld .help.err { color: var(--md3-error); }
    .adorn { position: relative; }
    .adorn em { position: absolute; right: 12px; top: 50%; transform: translateY(-50%); color: var(--md3-neutral-secondary); font-style: normal; pointer-events: none; }
    .g2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--sp-12); }
    .g4 { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--sp-12); }
    .mdrow { display: grid; grid-template-columns: 1fr auto 1fr; gap: var(--sp-12); align-items: end; }
    .mdrow .arr { padding-bottom: 12px; color: var(--md3-neutral-secondary); }
    .yearbar { position: relative; height: 12px; border-radius: 6px; background: var(--neutral05); overflow: hidden; }
    .yearbar i { position: absolute; top: 0; bottom: 0; background: var(--md3-primary); border-radius: 6px; }
    .ticks { position: relative; height: 16px; color: var(--md3-neutral-secondary); font-size: 11px; }
    .ticks span { position: absolute; transform: translateX(-50%); }
    .alert { display: flex; gap: 10px; align-items: flex-start; padding: var(--sp-12) var(--sp-16); border-radius: 8px; background: var(--error-a5); color: var(--md3-error); }
    .alert.info { background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .winbox { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; padding: var(--sp-12) var(--sp-16); border-radius: 8px; background: var(--md3-on-background); color: var(--md3-on-surface); }
    .winbox span { color: var(--md3-neutral-secondary); }
    .bhead { display: flex; align-items: center; flex-wrap: wrap; gap: var(--sp-8); }
    .bhead h3 { flex: 1; color: var(--head); min-width: 160px; }
    /* bands header: title left, one action group right; the group drops below the title as a unit, never splits */
    .bhead2 { display: flex; flex-wrap: wrap; align-items: center; column-gap: 16px; row-gap: 8px; }
    .bhead2 h3 { flex: 1 1 auto; color: var(--head); white-space: nowrap; }
    .bh-acts { display: flex; align-items: center; gap: 8px; margin-left: auto; flex: none; }
    .bh-acts .chip { height: 44px; padding: 0 14px; gap: 8px; }
    .bh-acts .chip svg { width: 18px; height: 18px; flex: none; }
    .bh-acts .chip .caret { margin-right: -4px; transition: transform 160ms var(--ease); }
    .bh-acts [aria-expanded="true"] .caret { transform: rotate(180deg); }
    .bh-acts [aria-expanded="true"] { border-color: var(--md3-on-primary-container); }
    .pfwrap { position: relative; }
    .pfmenu { position: absolute; right: 0; top: calc(100% + 6px); z-index: 5; width: 300px; padding: 6px; border-radius: 12px; background: var(--white); border: 1px solid var(--md3-outline-variant); box-shadow: 0 12px 32px rgba(18, 52, 59, .16); display: grid; gap: 2px; }
    .pfmenu button { display: grid; gap: 2px; text-align: left; min-height: 56px; padding: 8px 12px; border-radius: 8px; }
    .pfmenu button b { color: var(--head); }
    .pfmenu button small { color: var(--md3-on-surface-variant); }
    .pfmenu button:hover, .pfmenu button:focus-visible { background: var(--md3-displaybg-primary); outline: none; }
    .addband { display: flex; align-items: center; justify-content: center; gap: 8px; width: 100%; min-height: 48px; margin-top: 12px; border-radius: 8px; border: 1px dashed var(--md3-outline-variant); color: var(--md3-on-primary-container); background: transparent; }
    .addband:hover { background: var(--md3-displaybg-primary); }
    .addband:active { transform: scale(.995); }
    .wband { border: 1px solid var(--md3-surface-variant); border-radius: var(--radius); overflow: hidden; background: var(--white); }
    .wband__hd { display: flex; align-items: center; gap: var(--sp-12); padding: 8px 12px; background: var(--md3-displaybg-primary); flex-wrap: wrap; }
    .wband__hd b { color: var(--md3-on-primary-container); }
    .wband__hd .fld { width: 220px; }
    .wband__hd .sp { flex: 1; }
    .wband__bd { padding: var(--sp-12); display: grid; gap: var(--sp-12); }
    .witems { width: 100%; border-collapse: collapse; }
    .witems th { text-align: left; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; color: var(--ink); padding: 8px; border-bottom: 1px solid var(--md3-surface-variant); }
    .witems td { padding: 10px 8px; border-bottom: 1px solid var(--line); vertical-align: top; color: var(--head); }
    .witems tr.it { cursor: pointer; }
    .witems tr.it:hover td { background: #FAFCFB; }
    .witems td.amt, .witems th.amt { text-align: right; white-space: nowrap; }
    .witems td small { display: block; color: var(--md3-neutral-secondary); }
    .witems td.x { width: 48px; text-align: right; padding: 2px; }
    .witems .empty-row td { color: var(--md3-neutral-secondary); text-align: center; padding: 16px; }
    .addrow { display: flex; gap: var(--sp-8); flex-wrap: wrap; }
    .reasons { display: flex; flex-wrap: wrap; gap: var(--sp-8); }
    .qbrow { display: grid; grid-template-columns: 1fr auto 1fr auto 48px; gap: var(--sp-8); align-items: end; }
    .qbrow .to { padding-bottom: 14px; color: var(--md3-neutral-secondary); }
    .daychips { display: flex; gap: var(--sp-8); flex-wrap: wrap; }
    .daychips button { width: 52px; height: 44px; border-radius: 999px; background: var(--neutral05); color: var(--ink); font-weight: 600; }
    .daychips button[aria-pressed="true"] { background: var(--md3-primary); color: var(--white); }
    .presets { display: flex; gap: 4px; flex-wrap: wrap; }
    .sec2 { display: grid; gap: var(--sp-12); padding: var(--sp-16); border: 1px solid var(--md3-surface-variant); border-radius: var(--radius); }
    .sec2 > h4 { display: flex; align-items: center; justify-content: space-between; gap: 8px; color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
    .altbox { display: grid; gap: var(--sp-12); padding: var(--sp-12); border-radius: 8px; background: var(--md3-background); }
    .altbox .top { display: grid; grid-template-columns: 1fr 48px; gap: 8px; align-items: end; }
    .mixsum { color: var(--ink); display: flex; flex-wrap: wrap; gap: 6px; }
    .pick { display: grid; gap: 6px; max-height: 46dvh; overflow-y: auto; }
    .pick button { display: flex; align-items: center; gap: 12px; min-height: 52px; padding: 8px 12px; border-radius: 8px; background: var(--md3-background); text-align: left; width: 100%; }
    .pick button[aria-pressed="true"] { box-shadow: inset 0 0 0 2px var(--md3-primary); background: var(--white); }
    .pick button .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .pick button .grow b { color: var(--head); }
    .pick button .grow span { color: var(--md3-neutral-secondary); }
    .kmenu button { flex-direction: column; align-items: flex-start; justify-content: center; gap: 0; min-height: 56px; }
    .kmenu button small { color: var(--md3-neutral-secondary); font-size: 12px; }
    .kmenu button[disabled] { opacity: .5; cursor: not-allowed; }
    .sheet.wide { width: min(760px, 100%); }
    .sheet__f.end { justify-content: flex-end; }
    .sheet__f.end .btn { flex: none; min-width: 120px; padding: 0 20px; }
    .callout .alt-link { margin-top: 4px; }
    .wiz__inner.wide { max-width: 1180px; }
    .wgrid { display: grid; gap: var(--sp-16); align-items: start; }
    .wmain { display: grid; gap: var(--sp-16); min-width: 0; }
    .wreq { background: var(--white); border-radius: var(--radius); box-shadow: inset 0 0 0 1px var(--md3-surface-variant); overflow: hidden; }
    .wreq summary { list-style: none; display: flex; align-items: center; gap: 12px; min-height: 56px; padding: 8px 12px 8px 0; cursor: pointer; color: var(--md3-on-primary-container); }
    .wreq summary::-webkit-details-marker { display: none; }
    .wreq summary .ribbon { margin: 0; min-width: 44px; height: 32px; font-size: 16px; padding: 0 8px 0 16px; }
    .wreq summary .grow { flex: 1; min-width: 0; display: grid; }
    .wreq summary small { color: var(--ink); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .wreq[open] summary svg { transform: rotate(180deg); }
    .wreq__wrap { display: flex; flex-direction: column; min-height: 0; border-top: 1px solid var(--line); }
    .wreq__sc { flex: 1 1 auto; min-height: 0; overflow-y: auto; overscroll-behavior: contain; padding-top: 12px; }
    .wreq__sc.ft { -webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 24px); mask-image: linear-gradient(to bottom, transparent 0, #000 24px); }
    .wreq__sc.fb { -webkit-mask-image: linear-gradient(to top, transparent 0, #000 24px); mask-image: linear-gradient(to top, transparent 0, #000 24px); }
    .wreq__sc.ft.fb { -webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 24px, #000 calc(100% - 24px), transparent 100%); mask-image: linear-gradient(to bottom, transparent 0, #000 24px, #000 calc(100% - 24px), transparent 100%); }
    .wreq__f { flex: none; padding: 4px 8px; border-top: 1px solid var(--line); background: var(--white); }
    .wreq__f .linkbtn { min-height: 44px; display: inline-flex; align-items: center; padding: 0 8px; }
    .wreq__d { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .wreq__d .linkbtn { min-height: 44px; padding: 0 8px; margin: -10px -8px -10px 0; flex: none; }
    .wreq__d .using { display: inline-flex; align-items: center; gap: 4px; color: var(--md3-on-primary-container); font-size: 13px; flex: none; }
    .aichip { border: 1.5px solid transparent; background: linear-gradient(var(--white), var(--white)) padding-box, linear-gradient(90deg, var(--md3-on-primary-container), var(--md3-primary)) border-box; color: var(--md3-on-primary-container); font-weight: 600; }
    .aichip svg, .aimark svg, .aigo svg, [data-airegen] svg { color: var(--md3-primary); }
    .aigo svg { color: var(--white); }
    .aimark { display: inline-flex; vertical-align: -2px; margin-right: 8px; }
    .aimark svg { width: 22px; height: 22px; }
    .aictx { display: grid; gap: 8px; padding: 12px 14px; border-radius: 8px; background: var(--md3-background); color: var(--ink); margin-bottom: 12px; }
    .aictx b { display: block; color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
    .aictx__g { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; }
    .aispin { width: 18px; height: 18px; border-radius: 50%; border: 2px solid rgba(255,255,255,.4); border-top-color: var(--white); animation: aispin .8s linear infinite; }
    @keyframes aispin { to { transform: rotate(360deg); } }
    @media (prefers-reduced-motion: reduce) { .aispin { animation: none; } }
    .aisrc { color: var(--md3-on-surface-variant); margin-bottom: 8px; }
    .aiband { border: 1px solid var(--md3-outline-variant); border-radius: 8px; margin-bottom: 10px; overflow: hidden; }
    .aiband > b { display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .aiband ul { list-style: none; margin: 0; padding: 0; }
    .aiband li { display: flex; align-items: center; gap: 12px; padding: 8px 12px; border-top: 1px solid var(--line); }
    .aiband li:first-child { border-top: 0; }
    .aiband .grow { flex: 1; min-width: 0; display: grid; }
    .aiband .grow small { color: var(--md3-on-surface-variant); }
    .aiwhy { flex: none; max-width: 48%; text-align: right; font-size: 13px; color: var(--md3-on-primary-container); background: var(--md3-displaybg-primary); border-radius: 6px; padding: 3px 8px; }
    .aiscroll { max-height: calc(100dvh - 400px); min-height: 140px; overflow-y: auto; overscroll-behavior: contain; }
    .aileft { color: var(--md3-on-surface-variant); margin: 4px 0; }
    .ainote { display: flex; align-items: center; gap: 6px; color: var(--md3-neutral-secondary); font-size: 13px; margin-top: 6px; }
    .aitag { display: inline-block; font-size: 11px; font-weight: 700; letter-spacing: .04em; padding: 1px 6px; border-radius: 4px; color: var(--white); background: linear-gradient(90deg, var(--md3-on-primary-container), var(--md3-primary)); vertical-align: 1px; }
    .rqdates { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin: 4px 0 12px; }
    .rqdates .chip { height: 44px; color: var(--md3-on-primary-container); }
    .rqdates .using { display: inline-flex; align-items: center; gap: 6px; min-height: 36px; color: var(--md3-on-primary-container); }
    .wreq__b { display: grid; gap: 10px; padding: 0 16px 16px; color: var(--ink); }
    .wreq__kit { padding: 10px 12px; border-radius: 8px; background: var(--error-a5); color: #B3213F; }
    .wreq__kit b { color: #B3213F !important; }
    .wreq__b b { display: block; color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; margin-bottom: 2px; }
    .wreq__m { display: grid; gap: 8px; }
    .msgmini { padding: 8px 10px; border-radius: 8px; background: var(--md3-background); color: var(--head); display: grid; gap: 2px; }
    .msgmini small { color: var(--md3-neutral-secondary); }
    .msgmini .file { display: inline-flex; align-items: center; gap: 4px; margin-top: 4px; padding: 4px 8px; border-radius: 6px; background: var(--white); color: var(--md3-on-primary-container); font-size: 13px; }
    @media (orientation: landscape) { .wgrid { grid-template-columns: minmax(0, 1fr) 320px; } .wreq { position: sticky; top: 0; } .wreq summary { pointer-events: none; } .wreq summary > svg { display: none; } }
    .cfgs { display: grid; gap: 8px; }
    .cfg { display: flex; gap: 12px; align-items: flex-start; text-align: left; width: 100%; min-height: 72px; padding: 12px 14px; border-radius: var(--radius); border: 1px solid var(--md3-outline-variant); background: var(--white); }
    .cfg[aria-checked="true"] { border-color: var(--md3-on-primary-container); box-shadow: 0 0 0 1px var(--md3-on-primary-container); background: var(--md3-displaybg-primary); }
    .cfg[disabled] { opacity: .62; cursor: not-allowed; background: var(--md3-background); }
    .cfg .oi { width: 40px; height: 40px; border-radius: 8px; display: grid; place-items: center; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); flex: none; }
    .cfg .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .cfg .grow b { color: var(--head); display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .cfg .grow span { color: var(--ink); }
    .cfg .grow small { color: var(--md3-on-surface); }
    .cfg .grow small.note { color: var(--md3-on-primary-container); display: flex; gap: 6px; align-items: flex-start; margin-top: 2px; }
    .cfg .grow small.note svg { flex: none; margin-top: 2px; }
    .cfg .cfg__tail { font-style: normal; font-weight: 500; color: var(--md3-on-primary-container); }
    .cfg.cur .oi { background: var(--md3-on-primary-container); color: var(--white); }
    .alert.warn { background: #FFF4D6; color: #6B4E00; }
    .cfgedit { margin-top: 12px; }
    .cfg .grow small.why { color: var(--md3-error); display: flex; gap: 6px; align-items: center; }
    .sc4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
    .sc4 .tag { white-space: normal; height: auto; min-height: 24px; padding: 3px 8px; }
    .tgt[disabled] { opacity: .55; cursor: not-allowed; }
    .tgt .rd { color: var(--md3-on-primary-container); display: grid; place-items: center; }
    .ssum { display: flex; align-items: center; gap: 8px; color: var(--md3-on-surface); }
    .ctxstrip { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; padding: 10px 16px; border-radius: var(--radius); background: var(--white); color: var(--md3-on-primary-container); box-shadow: inset 0 0 0 1px var(--md3-surface-variant); }
    .ctxstrip span { flex: 1; min-width: 0; }
    .ctxstrip .linkbtn { min-height: 36px; }
    @media (orientation: portrait) {
      .g4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .sc4 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
'''

WIZ_OVERLAY = f'''  <div class="wiz" id="wiz" hidden role="dialog" aria-modal="true" aria-labelledby="wizT">
    <header class="bar"><button class="iconbtn" type="button" data-wclose aria-label="Close">{svg("close", 24)}</button><div class="bar__hd"><small>Diet formulation</small><h1 class="t-medium-medium" id="wizT"></h1><p class="t-body-regular" data-wsub></p></div></header>
    <div class="steps" data-wsteps aria-label="Steps"></div>
    <div class="wiz__body"><div class="wiz__inner" data-wbody></div></div>
    <div class="wiz__foot" data-wfoot></div>
  </div>
  <div class="scrim" id="wsheet" hidden><div class="sheet wide" role="dialog" aria-modal="true" aria-labelledby="wsT"></div></div>
  <div class="menu kmenu" id="kmenu" hidden role="menu"></div>'''

WIZ_JS = '''    /* ======================= ADD A DIET (Dev system diet-editor.js create wizard) ======================= */
    var LK = ''' + LOOK_EMBED + ''';
    var DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var ITEM = {}; LK.items.forEach(function (x) { ITEM[x.id] = x; });
    var MIX = {}; LK.mixes.forEach(function (x) { MIX[x.key] = x; });
    var W = null, wseq = 0;
    function pad(n) { return ('0' + n).slice(-2); }
    function localIso(d) { return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate()); }
    function todayIso() { return localIso(new Date()); }
    function daysIn(m) { return new Date(2024, m, 0).getDate(); }
    function hm12(t) { var h = Number(t.slice(0, 2)), m = t.slice(3, 5); return (h % 12 || 12) + (m === '00' ? '' : ':' + m) + ' ' + (h < 12 ? 'am' : 'pm'); }
    function tbLabel(b) { return b.tb === 'any' ? 'any time' : b.tb === 'adlib' ? 'ad lib' : (function (t) { return hm12(t.timeStart) + ' to ' + hm12(t.timeEnd); })(LK.timeBands.filter(function (t) { return String(t.id) === String(b.tb); })[0]); }
    function emptyItem(kind) { return { kind: kind || 'item', itemId: null, mixKey: null, qty: '', unit: null, prep: null, cut: null, alts: [], qtyF: '', qtyM: '', bandQty: {}, cadence: 'weekly', days: DAYS.slice(), intervalDays: '', anchorDate: '', monthDay: '', notes: '' }; }
    function emptyBand() { return { tb: 'any', items: [], notes: '' }; }
    function scopeKey() { return st.scope + ':' + (st.ref == null ? '' : st.ref); }
    function scopePlansFor(s, scope, ref) { return plansOf(s).filter(function (p) { return p.scope === scope && (scope === 'species' || p.ref === ref); }); }
    function isDefault(p) { return p.active && !p.sex && !p.from && !p.to; }
    function basePlan(s) { return plansOf(s).filter(isBase)[0] || null; }
    function md(iso) { var m = /^\\d{4}-(\\d{2})-(\\d{2})$/.exec(iso || ''); return m ? { m: Number(m[1]), d: Number(m[2]) } : null; }
    function mdContains(sm, sd, em, ed, pm, pd) { var sbe = sm < em || (sm === em && sd <= ed), pas = pm > sm || (pm === sm && pd >= sd), pbe = pm < em || (pm === em && pd <= ed); return sbe ? pas && pbe : pas || pbe; }
    function mdOverlap(a, b, c, d, e, f, g, h) { return mdContains(a, b, c, d, e, f) || mdContains(a, b, c, d, g, h) || mdContains(e, f, g, h, a, b) || mdContains(e, f, g, h, c, d); }
    function smartSeasonal(existing) {
      var seasonal = existing.filter(function (p) { return p.active && p.recurring && p.from && p.to; });
      var today = new Date(), sm = today.getMonth() + 1, em;
      for (var t = 0; t < 12; t++) { em = ((sm - 1 + 2) % 12) + 1; var el = daysIn(em);
        var clash = seasonal.some(function (p) { var a = md(p.from), b = md(p.to); return mdOverlap(sm, 1, em, el, a.m, a.d, b.m, b.d); }); if (!clash) break; sm = (sm % 12) + 1; }
      var y = today.getFullYear(), sy = sm < today.getMonth() + 1 ? y + 1 : y, start = new Date(sy, sm - 1, 1); if (start < today) start = today;
      return { from: localIso(start), to: localIso(new Date(em < sm ? sy + 1 : sy, em, 0)) };
    }
    function smartDated(existing) {
      var dated = existing.filter(function (p) { return p.active && !p.recurring && p.from && p.to; }), start = new Date(), end = new Date(start.getTime() + 30 * 86400000);
      for (var t = 0; t < 8; t++) { var s = localIso(start), e = localIso(end), over = dated.filter(function (p) { return !(e < p.from || s > p.to); }); if (!over.length) break;
        var mx = over.reduce(function (m, p) { return p.to > m ? p.to : m; }, ''), ne = new Date(mx + 'T00:00:00'); ne.setDate(ne.getDate() + 1); start = ne; end = new Date(start.getTime() + 30 * 86400000); }
      return { from: localIso(start), to: localIso(end) };
    }
    function overlap() {
      if (!W || W.kind === 'year-round' || !W.from || !W.to) return null;
      var ex = scopePlansFor(BY[W.tsn], W.scope, W.ref).filter(function (p) { return p.active && p.from && p.to && !!p.recurring === (W.kind === 'seasonal'); });
      for (var i = 0; i < ex.length; i++) { var p = ex[i];
        if (W.kind === 'seasonal') { var a = md(W.from), b = md(W.to), c = md(p.from), d = md(p.to); if (mdOverlap(a.m, a.d, b.m, b.d, c.m, c.d, d.m, d.d)) return p; }
        else if (!(W.to < p.from || W.from > p.to)) return p; }
      return null;
    }
    function dateErr() {
      if (!W.from) return 'Valid from is required'; if (!W.to) return 'Valid to is required';
      if (W.kind === 'seasonal') return W.from.slice(5) === W.to.slice(5) ? 'Season start and end cannot be the same day' : null;
      var t = todayIso(); if (W.from < t) return 'Valid from cannot be in the past'; if (W.to < t) return 'Valid to cannot be in the past'; if (W.from > W.to) return 'Valid from cannot be after Valid to'; return null;
    }
    function F() {
      var s = BY[W.tsn], base = basePlan(s), firstBase = W.scope === 'species' && !base && (W.base || !W.req);
      return { base: base, firstBase: firstBase, isBasePlan: firstBase, skipQuantity: W.scope === 'animal', includeReason: !firstBase, unbounded: W.kind === 'year-round' };
    }
    function stepList() {
      var f = F(), l = [];
      if (W.base && !W.req) l.push(['scope', 'Who is it for']);
      if (W.kind !== 'year-round') l.push(['date', W.kind === 'seasonal' ? 'Season window' : 'Date range']);
      if (!W.src) l.push(['path', 'How to start']);
      if (!f.skipQuantity && W.path !== 'adopt' && !W.src) l.push(['quantity', 'Daily amounts']);
      if (W.path !== 'adopt') l.push(['editor', 'Build diet']);
      if (f.includeReason && W.path !== 'adopt') l.push(['reason', 'Why this change']);
      return l;
    }
    function titleText() {
      var sc = W.scope === 'species' ? (W.kind === 'year-round' ? 'base ' : '') : W.scope === 'site' ? 'site-wide ' : W.scope === 'section' ? 'section-wide ' : W.scope === 'enclosure' ? 'enclosure-wide ' : 'animal ';
      var k = W.kind === 'seasonal' ? 'seasonal ' : W.kind === 'time-bound' ? 'time-bound ' : '';
      if (W.req && W.editOf) return 'Proposed change to ' + eoL() + ' for ' + W.req;
      if (W.req) return 'Proposed ' + ({ base: 'base ', 'year-round': 'year-round ', seasonal: 'seasonal ', 'time-bound': 'time-bound ' }[W.cfgKind] || k) + 'diet for ' + W.req;
      return ('New ' + sc + k + 'diet').replace(/\\s+/g, ' ');
    }
    function scopeLabel() {
      var s = BY[W.tsn]; if (W.scope === 'species') return 'Species-wide';
      var L = locOf(s), nm = '';
      if (W.scope === 'site') nm = (L.sites.filter(function (x) { return x.id === W.ref; })[0] || {}).name;
      if (W.scope === 'section') nm = (L.sections.filter(function (x) { return x.id === W.ref; })[0] || {}).name;
      if (W.scope === 'enclosure') nm = (encById(s, W.ref) || {}).name;
      if (W.scope === 'animal') { var a = (s.animalList || []).filter(function (x) { return x.id === W.ref; })[0]; nm = a ? animalLabel(a) : ''; }
      return { site: 'Site', section: 'Section', enclosure: 'Enclosure', animal: 'Animal' }[W.scope] + (nm ? ' · ' + nm : '');
    }
    function wizHash(step) { return '#species/' + st.seg + '/' + W.tsn + '/new/' + (W.base ? 'base' : W.kind) + (step ? '/' + step : ''); }
    function openWizard(kind, isBase, fromHash, req, cfgKind, opt) {
      var s = BY[st.tsn]; if (!s) return;
      if (!req && !basePlan(s)) { kind = 'year-round'; isBase = true; st.scope = 'species'; st.ref = null; }
      if (!req && kind === 'year-round' && scopePlansFor(s, st.scope, st.ref).some(isDefault)) { toast('A year-round diet already exists here. Edit the current diet to change its items.'); return; }
      W = { tsn: s.tsn, kind: kind, base: !!isBase, scope: st.scope, ref: st.scope === 'species' ? null : st.ref, step: null, path: null, qPick: null, from: '', to: '', error: null, reached: 0, sq: '', ssx: '',
        d: { quantityMode: 'standard', qBands: [], ageUnit: 'years', bands: [emptyBand()], notes: '', siteNotes: '', remark: '', dietitian: '', reason: '', remarks: '' } };
      if (req) { W.cfgKind = cfgKind || (isBase ? 'base' : kind); W.req = req.id; W.d.remarks = req.text; W.d.reason = 'Other'; W.d.notes = req.notes || ''; if (req.proposedId && PLANS[req.proposedId]) W.prevProposed = req.proposedId; }
      var ex = scopePlansFor(s, W.scope, W.ref);
      if (req && kind === 'time-bound' && req.start) { W.from = req.start; if (req.end) W.to = req.end; else { var dt = new Date(req.start + 'T00:00:00'); dt.setDate(dt.getDate() + 30); W.to = localIso(dt); } }
      else if (req && kind === 'seasonal' && req.season) { var yy = new Date().getFullYear(), wrapS = req.season.to < req.season.from; W.from = yy + '-' + req.season.from; W.to = (wrapS ? yy + 1 : yy) + '-' + req.season.to; }
      else if (req && kind === 'seasonal' && req.start && req.end) { W.from = req.start; W.to = req.end; }
      else if (kind === 'seasonal') { var a = smartSeasonal(ex); W.from = a.from; W.to = a.to; }
      if (kind === 'time-bound' && !(req && req.start)) { var b = smartDated(ex); W.from = b.from; W.to = b.to; }
      if (req && opt) {
        W.editOf = opt.editOf || null; W.reopen = !!opt.reopen;
        if (req.scope !== W.scope || (W.scope !== 'species' && req.scopeRef !== W.ref)) W.origTarget = req.scopeText || req.scope;
        var src = opt.source && PLANS[opt.source];
        if (src) { W.src = src.id; W.path = 'configure'; var bs = bandsFrom(src); if (bs.length) W.d.bands = bs;
          W.d.quantityMode = src.quantityMode === 'sex' ? 'sex' : 'standard'; W.qPick = W.d.quantityMode;
          if (src.notes && src.notes.kitchen) W.d.notes = src.notes.kitchen; if (src.notes && src.notes.site) W.d.siteNotes = src.notes.site;
          if (W.reopen) { if (src.from) W.from = src.from; if (src.to) W.to = src.to; if (src.reasonDetail) W.d.remarks = src.reasonDetail; if (src.reason) W.d.reason = src.reason; } }
      }
      W.step = stepList()[0][0];
      var h = wizHash(W.step);
      if (fromHash) { try { history.replaceState(null, '', h); } catch (x) {} } else location.hash = h;
      document.getElementById('wiz').hidden = false; drawWiz();
    }
    function closeWizard(silent) { W = null; document.getElementById('wiz').hidden = true; document.getElementById('wsheet').hidden = true; }
    function goStep(step, push) {
      var l = stepList().map(function (x) { return x[0]; }), i = l.indexOf(step); if (i === -1) return;
      W.step = step; W.error = null; W.reached = Math.max(W.reached, i);
      if (push) location.hash = wizHash(step); else { try { history.replaceState(null, '', wizHash(step)); } catch (x) {} }
      drawWiz(); document.querySelector('#wiz .wiz__body').scrollTop = 0;
    }
    function stepValid() {
      if (W.step === 'scope') return W.scope === 'species' || (W.ref != null && !refTaken(W.scope, W.ref));
      if (W.step === 'date') return !dateErr() && (W.req || !overlap());
      if (W.step === 'path') return W.path != null;
      if (W.step === 'quantity') return W.qPick != null;
      if (W.step === 'reason') return !!W.d.reason;
      return true;
    }
    function fld(label, inner, o) { o = o || {}; return '<label class="fld' + (o.err ? ' err' : '') + '"' + (o.style ? ' style="' + o.style + '"' : '') + '><span>' + label + (o.req ? ' <b class="req">*</b>' : '') + '</span>' + inner + (o.help ? '<em class="help' + (o.err ? ' err' : '') + '" style="font-style:normal">' + esc(o.help) + '</em>' : '') + '</label>'; }
    function opts(list, cur, ph) { return (ph != null ? '<option value="">' + esc(ph) + '</option>' : '') + list.map(function (o) { if (typeof o !== 'object') o = { v: o, t: o }; return '<option value="' + esc(o.v) + '"' + (String(o.v) === String(cur) ? ' selected' : '') + (o.dis ? ' disabled' : '') + '>' + esc(o.t) + '</option>'; }).join(''); }
    function dtx(iso, md0) { var m = /^(\\d{4})-(\\d{2})-(\\d{2})$/.exec(iso || ''); if (!m) return iso || ''; return Number(m[3]) + ' ' + MONTHS[Number(m[2]) - 1].slice(0, 3) + (md0 ? '' : ' ' + m[1]); }
    function alertBox(t, info) { return '<div class="alert' + (info === 'warn' ? ' warn' : info ? ' info' : '') + ' t-body-regular">' + ic(info && info !== 'warn' ? 'info' : 'alert', 20) + '<div>' + esc(t) + '</div></div>'; }
    function yfrac(m, d) { var t = 0; for (var i = 1; i < m; i++) t += daysIn(i); return Math.min(1, Math.max(0, (t + d - 1) / 365)); }

    function currentAt() { if (!W) return null; var s = BY[W.tsn]; return scopePlansFor(s, W.scope, W.ref).filter(isDefault)[0] || basePlan(s); }
    /* request dates for the current kind (same mapping as the prefill on open) */
    function reqDates() {
      var r = W && W.req && RQ.get(W.req); if (!r || (W.kind !== 'seasonal' && W.kind !== 'time-bound')) return null;
      var yy = new Date().getFullYear(), f, t;
      if (W.kind === 'time-bound') { if (!r.start) return null; f = r.start; if (r.end) t = r.end; else { var dt = new Date(r.start + 'T00:00:00'); dt.setDate(dt.getDate() + 30); t = localIso(dt); } }
      else if (r.season) { f = yy + '-' + r.season.from; t = (r.season.to < r.season.from ? yy + 1 : yy) + '-' + r.season.to; }
      else if (r.start && r.end) { var a = md(r.start), b = md(r.end), wr = b.m < a.m || (b.m === a.m && b.d <= a.d); f = yy + '-' + pad(a.m) + '-' + pad(a.d); t = (wr ? yy + 1 : yy) + '-' + pad(b.m) + '-' + pad(b.d); }
      else return null;
      var same = W.kind === 'seasonal' ? (W.from.slice(5) === f.slice(5) && W.to.slice(5) === t.slice(5)) : (W.from === f && W.to === t);
      var lab = W.kind === 'seasonal' ? dtx(f, true) + ' to ' + dtx(t, true) : (f.slice(0, 4) === t.slice(0, 4) ? dtx(f, true) : dtx(f)) + ' to ' + dtx(t);
      return { from: f, to: t, same: same, label: lab };
    }
    function panelApply() { if (!W || W.step !== 'date') return ''; var q = reqDates(); if (!q) return '';
      return q.same ? '<span class="using">' + ic('just-tick-mark', 16) + 'Using</span>' : '<button type="button" class="linkbtn t-body-medium" data-applydates aria-label="Apply dates from request (' + esc(q.label) + ')">Apply</button>'; }
    function applyBar() { var q = reqDates(); if (!q) return '';
      return '<div class="rqdates">' + (q.same ? '<span class="using t-body-medium">' + ic('just-tick-mark', 18) + 'Using request dates (' + esc(q.label) + ')</span>' : '<button type="button" class="chip t-body-medium" data-applydates>' + ic('calendar', 18) + 'Apply dates from request (' + esc(q.label) + ')</button>') + '</div>'; }
    function fitReq() {
      var p = document.querySelector('#wiz [data-wreq]'), bd = document.querySelector('#wiz .wiz__body'); if (!p || !bd) return;
      var wrap = p.querySelector('.wreq__wrap'), sm = p.querySelector('summary'), sc = p.querySelector('[data-wreqsc]');
      var cap = LAND.matches ? bd.clientHeight - 48 : Math.round(bd.clientHeight * 0.6);
      wrap.style.maxHeight = Math.max(160, cap - sm.offsetHeight) + 'px';
      edge(sc);
    }
    function edge(sc) { if (!sc) return; sc.classList.toggle('ft', sc.scrollTop > 2); sc.classList.toggle('fb', sc.scrollTop + sc.clientHeight < sc.scrollHeight - 2); }
    function reqPanel() {
      var r = RQ.get(W.req); if (!r) return '';
      var msgs = r.events.filter(function (e) { return e.kind === 'comment'; }).slice(-2), open = LAND.matches || W.reqOpen;
      return '<details class="wreq"' + (open ? ' open' : '') + ' data-wreq><summary class="t-body-medium"><span class="ribbon ' + r.prio + '" aria-hidden="true">' + RQ.PRI[r.prio][0] + '</span><span class="grow">Request ' + esc(r.id) + '<small class="t-body-regular">' + esc(r.title) + '</small></span>' + ic('dropdown', 22) + '</summary>' +
        '<div class="wreq__wrap"><div class="wreq__sc" data-wreqsc><div class="wreq__b t-body-regular">' + (r.status === 'adjustment' && r.adjustReason ? '<p class="wreq__kit"><b>Kitchen asked for a readjustment</b>' + esc(r.adjustReason) + '</p>' : '') + '<p><b>Reason</b>' + esc(r.text) + '</p>' + (r.notes ? '<p><b>Notes</b>' + esc(r.notes) + '</p>' : '') +
        '<p><b>Applies to</b>' + esc(r.scopeText || 'Whole species') + '</p>' +
        '<p><b>Dates</b><span class="wreq__d"><span>' + esc(r.season ? 'Every year ' + r.season.from.split('-').reverse().join('-') + ' to ' + r.season.to.split('-').reverse().join('-') : r.start ? RQ.fmt(r.start) + (r.end ? ' to ' + RQ.fmt(r.end) : ' onwards') : 'Not given') + '</span>' + panelApply() + '</span></p>' +
        '<p><b>Priority</b><span class="pribadge ' + r.prio + '">' + RQ.PRI[r.prio][0] + ' ' + RQ.PRI[r.prio][1] + '</span></p>' +
        '<p><b>Requested by</b>' + esc(r.by.name + ', ' + r.by.role + ' · ' + RQ.fmtDT(r.events[0].at)) + '</p>' +
        (msgs.length ? '<div class="wreq__m"><b>Latest messages</b>' + msgs.map(function (m) { return '<div class="msgmini"><small>' + esc(m.by + ' · ' + RQ.ago(m.at)) + '</small>' + esc(m.text || '') + (m.files && m.files.length ? '<span>' + m.files.map(function (f) { return '<span class="file">' + ic('notes-new', 14) + esc(f) + '</span>'; }).join('') + '</span>' : '') + '</div>'; }).join('') + '</div>' : '') +
        '</div></div><div class="wreq__f"><a class="linkbtn t-body-medium" href="#request/' + esc(r.id) + '" data-wreqopen>Open full request</a></div></div></details>';
    }
    /* ---------- step: who is this diet for? (base diet only) ---------- */
    var SC4 = [['species', 'paw', 'Species-wide', 'Every animal of the species, wherever it is housed.'], ['site', 'location-icon', 'Site-wide', 'Animals of the species at one site.'],
      ['section', 'grid', 'Section-wide', 'Animals of the species in one section.'], ['animal', 'user', 'Animal-wide', 'One named animal or group.']];
    function refTaken(scope, ref) { return scopePlansFor(BY[W.tsn], scope, ref).some(isDefault); }
    function animalsAt(s, f) { return (s.enclosures || []).filter(f).reduce(function (n, e) { return n + (e.animals || 0); }, 0); }
    function scopeRows(s) {
      var L = locOf(s), out = [];
      if (W.scope === 'site') L.sites.forEach(function (x) { var n = animalsAt(s, function (e) { return e.siteId === x.id; }); out.push({ g: '', ref: x.id, name: x.name, where: plural(n, 'animal') + ' · ' + plural(L.sections.filter(function (c) { return c.site === x.name; }).length, 'section'), n: n, find: x.name }); });
      if (W.scope === 'section') L.sites.forEach(function (site) { L.sections.filter(function (c) { return c.site === site.name; }).forEach(function (x) { var n = animalsAt(s, function (e) { return e.sectionId === x.id; });
        out.push({ g: site.name, ref: x.id, name: x.name, where: plural(n, 'animal') + ' · ' + plural(L.enclosures.filter(function (e) { return e.sectionId === x.id; }).length, 'enclosure'), n: n, find: x.name + ' ' + site.name }); }); });
      if (W.scope === 'animal') L.sections.forEach(function (sec) { (s.animalList || []).filter(function (a) { var e = encById(s, a.enclosure); return e && e.sectionId === sec.id; }).forEach(function (a) {
        var e = encById(s, a.enclosure), sx = a.sex === 'm' ? 'Male' : a.sex === 'f' ? 'Female' : 'Undetermined';
        out.push({ g: sec.site + ' › ' + sec.name, ref: a.id, name: animalLabel(a), sub: a.label ? '#' + a.id : '', where: sx + ' · ' + e.name, sex: a.sex, n: a.group || 1, find: [a.id, '#' + a.id, a.label || '', sx, e.name, sec.name].join(' ') }); }); });
      return out;
    }
    function scopeSummary(s) {
      if (W.scope === 'species') return 'All ' + plural(s.animals || 0, 'animal') + ' of ' + s.name;
      var r = scopeRows(s).filter(function (x) { return x.ref === W.ref; })[0];
      return r ? r.name + ' selected · ' + plural(r.n, 'animal') : 'Pick ' + ({ site: 'a site', section: 'a section', animal: 'an animal' })[W.scope] + ' to continue';
    }
    function scopeStep() {
      var s = BY[W.tsn], L = locOf(s);
      var cnt = { species: 'All ' + plural(s.animals || 0, 'animal') + ' of ' + s.name, site: plural(L.sites.length, 'site'), section: plural(L.sections.length, 'section'), animal: plural((s.animalList || []).length, 'animal') };
      var h = '<section class="wcard"><h2 class="t-medium-medium">Who is this diet for?</h2><p class="sub t-body-regular">Choose the level this first diet covers. You can add other levels later.</p><div class="ocards sc4">' + SC4.map(function (c) {
        return '<button type="button" class="ocard" data-wscope="' + c[0] + '" aria-pressed="' + (W.scope === c[0]) + '"><span class="oi">' + ic(c[1], 24) + '</span><b class="t-minor-title">' + c[2] + '</b><span class="s t-body-regular">' + c[3] + '</span><span class="tag teal" style="justify-self:start">' + esc(cnt[c[0]]) + '</span></button>';
      }).join('') + '</div>';
      if (W.scope !== 'species') {
        var PHW = { site: 'Search sites', section: 'Search sections', animal: 'Search by animal ID, name, sex or enclosure' };
        h += '<div class="ttools"><label class="spsearch">' + ic('search', 20) + '<span class="sr-only">' + PHW[W.scope] + '</span><input class="t-body-regular" type="search" data-wsq placeholder="' + PHW[W.scope] + '" value="' + esc(W.sq) + '" autocomplete="off"></label>' +
          (W.scope === 'animal' ? '<div class="segrow tchips" role="group" aria-label="Sex">' + [['', 'All'], ['m', 'Male'], ['f', 'Female']].map(function (c) { return '<button type="button" class="spchip t-body-medium" data-wsx="' + c[0] + '" aria-pressed="' + (W.ssx === c[0]) + '">' + c[1] + '</button>'; }).join('') + '</div>' : '') +
          '<p class="tcount t-body-regular" data-wscount aria-live="polite"></p></div><div class="tbox" data-tbox><div class="tscroll targets" data-wslist role="radiogroup" aria-label="' + ({ site: 'Sites', section: 'Sections', animal: 'Animals' })[W.scope] + '"></div></div>';
        if (!basePlan(s)) h += alertBox('In the kitchen system the first diet is always species-wide. ' + (W.scope === 'animal' ? 'Other animals of the species' : 'Animals outside this ' + W.scope) + ' stay without a diet until a species-wide base diet is added.', true);
      }
      h += '<p class="ssum t-body-medium" data-wssum>' + ic(W.scope === 'species' || W.ref != null ? 'just-tick-mark' : 'info', 18) + esc(scopeSummary(s)) + '</p></section>';
      return h;
    }
    function drawScopeList() {
      var box = document.querySelector('#wiz [data-wslist]'); if (!box) return;
      var s = BY[W.tsn], all = scopeRows(s), q = W.sq.trim().toLowerCase(), N = NOUN[W.scope];
      var rows = all.filter(function (r) { return (!q || r.find.toLowerCase().indexOf(q) !== -1) && (!W.ssx || r.sex === W.ssx); }), html = '', lastG = null;
      document.querySelector('#wiz [data-wscount]').textContent = rows.length === all.length ? plural(all.length, N[0], N[1]) : 'Showing ' + rows.length + ' of ' + all.length + ' ' + N[1];
      rows.forEach(function (r) {
        if (r.g && r.g !== lastG) { html += '<p class="tgh">' + esc(r.g) + '</p>'; lastG = r.g; }
        var taken = refTaken(W.scope, r.ref), on = W.ref === r.ref;
        html += '<button type="button" class="tgt" role="radio" data-wsref="' + r.ref + '" aria-checked="' + on + '" aria-pressed="' + on + '"' + (taken ? ' disabled' : '') + '><span class="rd">' + ic(on ? 'checkbox-checked' : 'checkbox-unchecked', 22) + '</span><span class="grow"><b class="t-body-title">' + hlq(r.name, q) + (r.sub ? ' <span class="tid">' + hlq(r.sub, q) + '</span>' : '') + '</b><span class="t-body-regular">' + hlq(r.where, q) + '</span></span>' +
          (taken ? '<span class="d t-body-medium">Has a diet</span>' : '') + '</button>';
      });
      if (!rows.length) html = '<div class="tempty"><b class="t-body-title">No ' + N[1] + ' match' + (q ? ' "' + esc(W.sq.trim()) + '"' : ' this filter') + '</b><span class="t-body-regular">Try another ' + (W.scope === 'animal' ? 'ID, name, sex or enclosure' : 'name') + '.</span></div>';
      box.innerHTML = html;
      var b = box.parentNode; b.classList.toggle('ft', box.scrollTop > 2); b.classList.toggle('fb', box.scrollTop + box.clientHeight < box.scrollHeight - 2);
    }
    function eoL() { return PLANS[W.editOf] ? shownId(PLANS[W.editOf]) : 'D-' + W.editOf; }
    function editNote() {
      if (W.req && !W.src && !W.base && !basePlan(BY[W.tsn])) return '<div class="cfgedit">' + alertBox('No base diet yet. This proposal will also need a base diet before it can go live.', true) + '</div>';
      if (!W.req || !W.src) return '';
      if (W.reopen) return '<div class="cfgedit">' + alertBox('Editing the proposal ' + shownId(PLANS[W.src]) + '. Saving replaces it on ' + W.req + '.' + (W.editOf ? ' It is still a proposed change to ' + eoL() + '.' : ''), true) + '</div>';
      return '<div class="cfgedit">' + alertBox('Prefilled from ' + eoL() + ' in edit mode. ' + eoL() + ' stays active until the change is applied.', true) + '</div>';
    }
    function contextStrip() {
      var s = BY[W.tsn], l = scopeLabel(), parts = [s.name, ({ species: 'Species-wide', site: 'Site-wide', section: 'Section-wide', enclosure: 'Enclosure-wide', animal: 'Animal-wide' })[W.scope]];
      if (W.scope !== 'species' && l.indexOf(' · ') !== -1) parts.push(l.split(' · ')[1]);
      if (W.req) { var rq0 = RQ.get(W.req); parts.push('From request ' + W.req); if (rq0) parts.push(RQ.PRI[rq0.prio][1] + ' priority'); if (W.origTarget) parts.push('Request targeted ' + W.origTarget); }
      return '<div class="ctxstrip t-body-medium">' + ic('paw', 18) + '<span>' + esc(parts.join(' · ')) + '</span>' + (W.base && !W.req && W.step !== 'scope' ? '<button type="button" class="linkbtn t-body-medium" data-wchscope>Change</button>' : '') + '</div>';
    }
    /* ---------- steps ---------- */
    function dateStep() {
      var seasonal = W.kind === 'seasonal', body = '';
      if (seasonal) {
        var f = md(W.from), t = md(W.to), seg = '', pillTxt = '';
        if (f && t) { var s0 = yfrac(f.m, f.d), e0 = yfrac(t.m, t.d), wraps = t.m < f.m || (t.m === f.m && t.d <= f.d);
          seg = (wraps ? [[s0, 1 - s0], [0, e0]] : [[s0, Math.max(0.01, e0 - s0)]]).map(function (x) { return '<i style="left:' + x[0] * 100 + '%;width:' + x[1] * 100 + '%"></i>'; }).join('');
          pillTxt = 'Repeats ' + f.d + ' ' + MONTHS[f.m - 1].slice(0, 3) + ' to ' + t.d + ' ' + MONTHS[t.m - 1].slice(0, 3) + ', every year' + (wraps ? ' (wraps the new year)' : ''); }
        function mdSel(side, v) { var x = md(v) || { m: 0, d: 0 }, dl = []; for (var i = 1; i <= (x.m ? daysIn(x.m) : 31); i++) dl.push(i);
          return '<div class="g2">' + fld((side === 'from' ? 'From' : 'To') + ' day', '<select data-md="' + side + ':d">' + opts(dl, x.d || '') + '</select>', { req: true }) +
            fld((side === 'from' ? 'From' : 'To') + ' month', '<select data-md="' + side + ':m">' + opts(MONTHS.map(function (n, i) { return { v: i + 1, t: n }; }), x.m || '') + '</select>', { req: true }) + '</div>'; }
        body = '<div class="yearbar" aria-hidden="true">' + seg + '</div><div class="ticks" aria-hidden="true">' + [['Jan', 1], ['Mar', 3], ['May', 5], ['Jul', 7], ['Sep', 9], ['Nov', 11]].map(function (x) { return '<span style="left:' + yfrac(x[1], 1) * 100 + '%">' + x[0] + '</span>'; }).join('') + '</div>' +
          '<div class="mdrow">' + mdSel('from', W.from) + '<span class="arr">' + ic('dropdown', 24).replace('<svg', '<svg style="transform:rotate(-90deg)"') + '</span>' + mdSel('to', W.to) + '</div>' +
          (pillTxt ? '<span class="win current">' + ic('calendar', 18) + esc(pillTxt) + '</span>' : '');
      } else {
        var t0 = todayIso();
        body = '<div class="g2">' + fld('Valid from', '<input type="date" data-wd="from" min="' + t0 + '" value="' + W.from + '">', { req: true }) +
          fld('Valid to', '<input type="date" data-wd="to" min="' + (W.from || t0) + '" value="' + W.to + '">', { req: true, help: W.from && !W.to ? 'Pick an end date to continue' : '' }) + '</div>';
      }
      var e = W.from && W.to ? dateErr() : null, o = overlap();
      return '<section class="wcard"><h2 class="t-medium-medium">' + (seasonal ? 'When does this diet apply?' : 'Date range') + '</h2><p class="sub t-body-regular">' + (seasonal ? 'It repeats every year between these dates.' : 'Time-bound span. It applies once between these dates.') + '</p>' + (W.req ? applyBar() : '') + body +
        (e ? alertBox(e) : '') + (o ? (W.req ? alertBox('Overlaps ' + shownId(o) + ' from ' + dtx(o.from, seasonal) + ' to ' + dtx(o.to, seasonal) + '; the proposal will replace it for those dates.', 'warn') : alertBox('Dates overlap with existing plan ' + shownId(o) + '. Two ' + (seasonal ? 'seasonal' : 'time-bound') + ' plans of the same kind cannot cover the same period.')) : '') + '</section>';
    }
    function pathStep() {
      var cards = [['configure', 'add', 'Configure new diet', 'Start with a blank schedule and build feeding bands yourself.', ['Full control', 'Empty time bands'], true],
        ['adopt', 'transfer', 'Adopt an existing diet', 'Follow another species diet schedule. It is shared, not copied.', ['Reuse a proven plan', 'Shares the source schedule'], false]];
      return '<section class="wcard"><h2 class="t-medium-medium">How would you like to start?</h2><p class="sub t-body-regular">Build from scratch, or follow a similar diet.</p><div class="ocards">' + cards.map(function (c) {
        return '<button type="button" class="ocard" data-path="' + c[0] + '" aria-pressed="' + (W.path === c[0]) + '">' + (c[5] ? '<span class="tag green rec">Recommended</span>' : '') + '<span class="oi">' + ic(c[1], 24) + '</span><b class="t-minor-title">' + c[2] + '</b><span class="s t-body-regular">' + c[3] + '</span><ul class="t-body-regular">' + c[4].map(function (x) { return '<li>' + ic('just-tick-mark', 16) + x + '</li>'; }).join('') + '</ul></button>';
      }).join('') + '</div>' + (W.error ? alertBox(W.error) : '') + '</section>';
    }
    var QC = [['standard', 'Standard', 'One quantity per item, applies to every animal in scope.'], ['sex', 'Tailored by Sex', 'Different quantities per sex. The standard ration applies when blank.'], ['age', 'Tailored by Age', 'Different quantities per age band. Set the bands for this diet.'], ['weight', 'Tailored by Weight band', 'Different quantities per weight band. Set the bands for this diet.']];
    function quantityStep() {
      return '<section class="wcard"><h2 class="t-medium-medium">How are daily amounts set?</h2><p class="sub t-body-regular">Pick how this diet tailors the per-animal ration.</p><div class="ocards">' + QC.map(function (c) {
        return '<button type="button" class="ocard" data-qpick="' + c[0] + '" aria-pressed="' + (W.qPick === c[0]) + '"><b class="t-minor-title">' + c[1] + '</b><span class="s t-body-regular">' + c[2] + '</span></button>'; }).join('') + '</div></section>';
    }
    function defBands(k) { return k === 'age' ? [{ k: 'a' + (++wseq), from: '0', to: '1' }, { k: 'a' + (++wseq), from: '1', to: '5' }, { k: 'a' + (++wseq), from: '5', to: '' }] : k === 'weight' ? [{ k: 'w' + (++wseq), from: '0', to: '10' }, { k: 'w' + (++wseq), from: '10', to: '50' }, { k: 'w' + (++wseq), from: '50', to: '' }] : []; }
    function bandName(b) { var u = W.d.quantityMode === 'age' ? (W.d.ageUnit === 'months' ? ' mo' : ' y') : ' kg'; return b.to === '' ? b.from + '+' + u : b.from + '-' + b.to + u; }
    function qbErr() {
      var B = W.d.qBands; if (!B.length) return 'Add at least one band.';
      for (var i = 0; i < B.length; i++) { var f = Number(B[i].from), t = B[i].to === '' ? null : Number(B[i].to);
        if (String(B[i].from).trim() === '' || !isFinite(f)) return 'Band ' + (i + 1) + ': enter a From value.';
        if (t == null && i !== B.length - 1) return 'Only the last band can be open-ended.';
        if (t != null && !(t > f)) return 'Band ' + (i + 1) + ': To must be greater than From.';
        if (i > 0 && B[i - 1].to !== '' && Number(B[i - 1].to) !== f) return 'Band ' + (i + 1) + ' should start where band ' + i + ' ends (' + B[i - 1].to + ').'; }
      return null;
    }
    function itemName(it) { return it.kind === 'item' ? (ITEM[it.itemId] || {}).name : (MIX[it.mixKey] || {}).name; }
    function itemUnit(it) { return it.kind === 'item' ? (it.unit || (ITEM[it.itemId] || {}).unit || '') : (MIX[it.mixKey] || {}).unit || ''; }
    function cadLabel(it) { if (it.cadence === 'every_n_days') return 'Every ' + it.intervalDays + ' days'; if (it.cadence === 'monthly_day') return 'Monthly, ' + (Number(it.monthDay) === -1 ? 'last day' : 'day ' + it.monthDay);
      return it.days.length === 7 ? 'Daily' : it.days.join(', '); }
    function editorStep() {
      var f = F(), d = W.d, h = '<section class="wcard">';
      if (W.kind === 'year-round') h += alertBox(W.scope === 'species' ? 'Base diets are unbounded. Create a Seasonal plan for time-windowed feeding.' : W.scope === 'animal' ? 'This animal-wide default is unbounded. Add a seasonal plan separately if needed.' : 'This default is unbounded. Create a Seasonal plan for time-windowed feeding.', true);
      else { var a = W.from.slice(8, 10) + '-' + W.from.slice(5, 7), b = W.to.slice(8, 10) + '-' + W.to.slice(5, 7); h += '<div class="winbox t-body-medium">' + ic('calendar', 18) + (W.kind === 'seasonal' ? 'Every year ' : 'Time-bound ') + a + ' → ' + b + ' <span class="t-body-regular">Use Back to change</span></div>'; }
      if (!f.isBasePlan && !f.skipQuantity) h += '<div class="bhead"><h3 class="t-minor-title">Quantity mode</h3><div class="dseg" role="group" aria-label="Quantity mode">' + [['standard', 'Standard'], ['sex', 'By sex'], ['age', 'By age'], ['weight', 'By weight']].map(function (q) { return '<button type="button" data-qmode="' + q[0] + '" aria-pressed="' + (d.quantityMode === q[0]) + '" class="t-body-medium">' + q[1] + '</button>'; }).join('') + '</div></div>';
      if (d.quantityMode === 'age' || d.quantityMode === 'weight') {
        var qe = qbErr();
        h += '<div class="sec2"><h4>' + (d.quantityMode === 'age' ? 'Age bands (' + d.ageUnit + ')' : 'Weight bands (kg)') + '<span style="display:flex;gap:8px;align-items:center">' + (d.quantityMode === 'age' ? '<span class="dseg"><button type="button" data-ageunit="years" aria-pressed="' + (d.ageUnit === 'years') + '" class="t-body-medium">Years</button><button type="button" data-ageunit="months" aria-pressed="' + (d.ageUnit === 'months') + '" class="t-body-medium">Months</button></span>' : '') + '<button type="button" class="chip t-body-medium" data-qbadd>' + ic('add', 18) + 'Add band</button></span></h4>' +
          d.qBands.map(function (b, i) { return '<div class="qbrow">' + fld('From', '<input inputmode="decimal" data-qb="' + i + ':from" value="' + esc(b.from) + '">') + '<span class="to">to</span>' + fld('To', '<input inputmode="decimal" data-qb="' + i + ':to" value="' + esc(b.to) + '" placeholder="' + (i === d.qBands.length - 1 ? 'Open (blank)' : '') + '">') + '<span class="to">' + (d.quantityMode === 'age' ? d.ageUnit : 'kg') + '</span><button type="button" class="iconbtn" data-qbrm="' + i + '" aria-label="Remove band"' + (d.qBands.length <= 1 ? ' disabled' : '') + '>' + ic('close', 22) + '</button></div>'; }).join('') +
          (qe ? '<span class="help err t-body-regular" style="color:var(--md3-error)">' + esc(qe) + '</span>' : '') + '</div>';
      }
      var pfItems = [], cp = currentAt();
      if (f.base) pfItems.push(['base', 'Base diet', 'Copy the bands of ' + shownId(f.base) + ', the species base']);
      if (cp && cp !== f.base) pfItems.push(['current', 'Current diet at this scope', 'Copy the bands of ' + shownId(cp)]);
      pfItems.push(['diet', 'Another diet', 'Pick any diet from another species or scope']);
      h += '</section><section class="wcard"><div class="bhead2"><h3 class="t-minor-title">Feeding time bands (' + d.bands.length + ')</h3><div class="bh-acts">' +
        '<button type="button" class="chip t-body-medium aichip" data-aiopen>' + SPARK + 'Prefill with AI</button>' +
        '<div class="pfwrap"><button type="button" class="chip t-body-medium" data-pfmenu aria-haspopup="menu" aria-expanded="' + !!W.pfOpen + '">' + ic('transfer', 18) + 'Prefill from' + ic('dropdown', 18).replace('<svg', '<svg class="caret"') + '</button>' +
        (W.pfOpen ? '<div class="pfmenu" role="menu" aria-label="Prefill from">' + pfItems.map(function (x) { return '<button type="button" role="menuitem" data-prefill="' + x[0] + '"><b class="t-body-title">' + x[1] + '</b><small class="t-body-regular">' + esc(x[2]) + '</small></button>'; }).join('') + '</div>' : '') +
        '</div></div></div>' +
        d.bands.map(function (b, bi) {
          var tbo = [{ v: 'any', t: 'Any time' }, { v: 'adlib', t: 'Ad libitum' }].concat(LK.timeBands.map(function (t) { return { v: String(t.id), t: hm12(t.timeStart) + ' to ' + hm12(t.timeEnd) }; }));
          var rows = b.items.length ? b.items.map(function (it, ii) {
            var alts = it.kind === 'item' ? it.alts.filter(function (a) { return a.itemId; }) : [], meta = it.kind === 'item' ? [it.prep && 'Prep: ' + it.prep, it.cut && 'Cut: ' + it.cut].filter(Boolean).join(' · ') : ((MIX[it.mixKey] || {}).items || []).map(function (x) { return x.name + (it.kind === 'mix' ? ' ' + Math.round(x.share || 0) + '%' : ''); }).slice(0, 4).join(' · ');
            return '<tr class="it" data-edititem="' + bi + ':' + ii + '" tabindex="0"><td>' + esc(cadLabel(it)) + '</td><td><b>' + esc(itemName(it) || '') + '</b>' + (it.kind !== 'item' ? ' <span class="it-k">' + (it.kind === 'recipe' ? 'RECIPE' : 'MIX') + '</span>' : '') + (it.ai ? ' <span class="aitag" title="' + esc(it.ai) + '">AI</span>' : '') +
              (alts.length ? '<small>or ' + esc(alts.map(function (a) { return (ITEM[a.itemId] || {}).name; }).join(', ')) + '</small>' : '') + (meta ? '<small>' + esc(meta) + '</small>' : '') + (it.notes ? '<small>' + esc(it.notes) + '</small>' : '') + '</td>' +
              '<td class="amt"><b>' + esc(it.qty + ' ' + itemUnit(it)) + '</b></td><td class="x"><button type="button" class="iconbtn" data-rmitem="' + bi + ':' + ii + '" aria-label="Remove ' + esc(itemName(it) || 'item') + '">' + ic('close', 20) + '</button></td></tr>';
          }).join('') : '<tr class="empty-row"><td colspan="4">No items yet. Add the first one below.</td></tr>';
          return '<div class="wband"><div class="wband__hd">' + ic('time', 20) + '<b class="t-body-title">Band ' + (bi + 1) + '</b><label class="fld"><span class="sr-only">Time band</span><select data-tb="' + bi + '">' + opts(tbo, b.tb) + '</select></label><span class="sp"></span>' +
            '<button type="button" class="iconbtn" data-tbclone="' + bi + '" aria-label="Clone this band">' + ic('transfer', 22) + '</button><button type="button" class="iconbtn" data-tbrm="' + bi + '" aria-label="Remove band">' + ic('close', 22) + '</button></div>' +
            '<div class="wband__bd"><table class="witems t-body-regular"><thead><tr><th>Day</th><th>Item</th><th class="amt">Daily amt</th><th></th></tr></thead><tbody>' + rows + '</tbody></table>' +
            '<div class="addrow">' + [['item', 'Ingredient'], ['mix', 'Mix'], ['recipe', 'Recipe']].map(function (k) { return '<button type="button" class="chip t-body-medium" data-additem="' + bi + ':' + k[0] + '">' + ic('add', 18) + k[1] + '</button>'; }).join('') + '</div>' +
            fld('Notes for this time band (optional)', '<input data-bnote="' + bi + '" value="' + esc(b.notes) + '" placeholder="e.g. warm before serving, scatter for foraging">') + '</div></div>';
        }).join('') + '<button type="button" class="addband t-body-medium" data-addband>' + ic('add', 20) + 'Add time band</button></section>' +
        '<section class="wcard">' + fld('Notes for the kitchen', '<textarea data-dv="notes" placeholder="Extra instructions for the kitchen (optional), e.g. thaw fish overnight">' + esc(d.notes) + '</textarea>') +
        fld('Notes for site', '<textarea data-dv="siteNotes" placeholder="Extra instructions for the keepers (optional), e.g. scatter for foraging">' + esc(d.siteNotes) + '</textarea>') +
        fld('Remark', '<textarea data-dv="remark" placeholder="A remark shown highlighted in the plan view (optional), e.g. vet: monitor weight weekly">' + esc(d.remark) + '</textarea>') +
        fld('Dietician', '<select data-dv="dietitian">' + opts(LK.dietitians, d.dietitian, 'Assign a diet owner (optional)') + '</select>') + '</section>' + (W.error ? alertBox(W.error) : '');
      return h;
    }
    function reasonStep() {
      return '<section class="wcard"><h2 class="t-medium-medium">Why this change?</h2><p class="sub t-body-regular">Pick a reason. It is kept in the diet history.</p><div class="reasons" role="radiogroup" aria-label="Reason for this change">' +
        LK.reasons.map(function (r) { return '<button type="button" role="radio" class="spchip t-body-medium" data-reason="' + esc(r) + '" aria-pressed="' + (W.d.reason === r) + '" aria-checked="' + (W.d.reason === r) + '">' + esc(r) + '</button>'; }).join('') + '</div>' +
        fld('Remarks (optional)', '<textarea data-dv="remarks" placeholder="What changed and why? Context for the keeper or vet.">' + esc(W.d.remarks) + '</textarea>') + (W.error ? alertBox(W.error) : '') + '</section>';
    }
    function drawWiz() {
      if (!W) return;
      var l = stepList(), idx = l.map(function (x) { return x[0]; }).indexOf(W.step), f = F(), s = BY[W.tsn];
      document.getElementById('wizT').textContent = titleText();
      document.querySelector('#wiz [data-wsub]').textContent = s.name + ' · ' + scopeLabel();
      document.querySelector('#wiz [data-wsteps]').innerHTML = l.map(function (x, i) { return '<span class="' + (i === idx ? 'on' : i < idx ? 'done' : '') + '">' + (i < idx ? ic('just-tick-mark', 16) : (i + 1) + '.') + ' ' + x[1] + '</span>'; }).join('');
      var body = W.step === 'scope' ? scopeStep() : W.step === 'date' ? dateStep() : W.step === 'path' ? pathStep() : W.step === 'quantity' ? quantityStep() : W.step === 'editor' ? editorStep() : reasonStep();
      var inner = (W.step !== 'scope' ? contextStrip() + editNote() : '') + body;
      document.querySelector('#wiz .wiz__inner').classList.toggle('wide', !!W.req);
      var osc = document.querySelector('#wiz [data-wreqsc]'), oscT = osc ? osc.scrollTop : 0;
      document.querySelector('#wiz [data-wbody]').innerHTML = W.req ? '<div class="wgrid"><div class="wmain">' + inner + '</div>' + reqPanel() + '</div>' : inner;
      if (W.step === 'scope') drawScopeList();
      var foot = '<button type="button" class="btn ghost" data-wcancel>Cancel</button><span class="sp"></span>';
      if (idx > 0) foot += '<button type="button" class="btn sec" data-wback>Back</button>';
      var last = idx === l.length - 1;
      var saveL = W.req ? 'Save proposed diet' : 'Create plan';
      if (W.step === 'editor' && !f.includeReason) foot += '<button type="button" class="btn pri" data-wsave>' + saveL + '</button>';
      else if (last && W.step === 'reason') foot += '<button type="button" class="btn pri" data-wsave' + (W.d.reason ? '' : ' disabled') + '>' + saveL + '</button>';
      else if (W.step === 'editor') foot += '<button type="button" class="btn pri" data-wnext>Next</button>';
      else foot += '<button type="button" class="btn pri" data-wnext' + (stepValid() ? '' : ' disabled') + '>Continue</button>';
      document.querySelector('#wiz [data-wfoot]').innerHTML = foot;
      if (W.req) { fitReq(); var nsc = document.querySelector('#wiz [data-wreqsc]'); if (nsc) { nsc.scrollTop = oscT; edge(nsc); } }
    }

    /* ---------- validation of the built diet (diet-editor.js validateBands) ---------- */
    function bandsErr() {
      var B = W.d.bands, seen = {};
      for (var bi = 0; bi < B.length; bi++) {
        if (!B[bi].items.length) return 'Band ' + (bi + 1) + ': add at least one item';
        var key = B[bi].tb; if (seen[key]) return 'Band ' + (bi + 1) + ' (' + tbLabel(B[bi]) + ') is already used. Each time band can only be added once. Put its items in the existing band instead.'; seen[key] = 1;
      }
      if (W.d.quantityMode === 'age' || W.d.quantityMode === 'weight') { var q = qbErr(); if (q) return q; }
      return null;
    }
    function itemErr(it) {
      if (it.kind === 'item' && !it.itemId) return 'Pick a diet item.';
      if (it.kind !== 'item' && !it.mixKey) return it.kind === 'recipe' ? 'Pick a diet recipe.' : 'Pick a diet mix.';
      if (!(Number(it.qty) > 0)) return 'Enter a quantity greater than zero.';
      if (it.cadence === 'weekly' && !it.days.length) return 'Pick at least one day for this item.';
      if (it.cadence === 'every_n_days') { var n = Number(it.intervalDays); if (!Number.isInteger(n) || n < 1 || n > 365 || !it.anchorDate) return 'Complete the cadence: interval (1 to 365 days) and first feed date.'; }
      if (it.cadence === 'monthly_day' && it.monthDay === '') return 'Complete the cadence: pick the day of the month.';
      for (var i = 0; i < it.alts.length; i++) { var a = it.alts[i]; if (!a.itemId) continue; if (!(Number(a.qty) > 0)) return 'Enter a quantity greater than zero for each alternative.'; }
      return null;
    }

    /* ---------- item sheet ---------- */
    var IS = null;
    function sheetEl() { return document.querySelector('#wsheet .sheet'); }
    function openItem(bi, ii, kind) {
      var it = ii == null ? emptyItem(kind) : JSON.parse(JSON.stringify(W.d.bands[bi].items[ii]));
      IS = { mode: 'item', bi: bi, ii: ii, it: it, error: null }; drawItem(); document.getElementById('wsheet').hidden = false;
    }
    function usedInBand(kindItem) { var b = W.d.bands[IS.bi]; return b.items.filter(function (x, j) { return j !== IS.ii && (kindItem ? x.kind === 'item' : x.kind !== 'item'); }).map(function (x) { return String(kindItem ? x.itemId : x.mixKey); }); }
    function drawItem() {
      var it = IS.it, qm = W.d.quantityMode, isItem = it.kind === 'item', mi = ITEM[it.itemId], mx = MIX[it.mixKey], used = usedInBand(isItem);
      var h = '<div class="grab"></div><div class="sheet__h"><div><h2 class="t-major-title" id="wsT">' + (IS.ii == null ? 'New item' : 'Edit item') + '</h2><p class="t-body-regular" style="color:var(--ink)">Band ' + (IS.bi + 1) + ' · ' + esc(tbLabel(W.d.bands[IS.bi])) + '</p></div><button type="button" class="iconbtn" data-isclose aria-label="Close">' + ic('close', 24) + '</button></div>';
      h += '<div class="sec2"><h4>Selection<span class="dseg" role="group" aria-label="Kind">' + [['item', 'Item'], ['mix', 'Mix'], ['recipe', 'Recipe']].map(function (k) { return '<button type="button" data-ikind="' + k[0] + '" aria-pressed="' + (it.kind === k[0]) + '" class="t-body-medium">' + k[1] + '</button>'; }).join('') + '</span></h4>';
      if (isItem) {
        h += fld('Diet item', '<select data-iv="itemId">' + opts(LK.items.filter(function (x) { return x.isActive && (used.indexOf(String(x.id)) === -1 || String(x.id) === String(it.itemId)); }).map(function (x) { return { v: x.id, t: x.name }; }), it.itemId || '', 'Pick a diet item') + '</select>', { req: true });
        h += '<div class="g4">' + fld('Qty', '<input inputmode="decimal" data-iv="qty" value="' + esc(it.qty) + '">', { req: true }) +
          fld('Unit', '<select data-iv="unit"' + (mi ? '' : ' disabled') + '>' + opts(mi ? mi.units : [], it.unit || (mi && mi.unit) || '') + '</select>') +
          fld('Prep', '<select data-iv="prep"' + (mi ? '' : ' disabled') + '>' + opts(mi ? mi.preps : [], it.prep || '', '') + '</select>') +
          (mi && mi.cuts.length ? fld('Cut', '<select data-iv="cut">' + opts(mi.cuts, it.cut || '', '') + '</select>') : '') + '</div>';
        if (mi) {
          h += '<div class="bhead"><h3 class="t-body-title">Alternatives</h3><button type="button" class="chip t-body-medium" data-addalt>' + ic('add', 18) + 'Add alternative</button></div><p class="t-body-regular" style="color:var(--md3-neutral-secondary);margin-top:-6px">Substitutes the kitchen may feed when ' + esc(mi.name) + ' is short. The forecast always uses the primary.</p>' +
            it.alts.map(function (a, ai) { var am = ITEM[a.itemId], ex = used.concat([String(it.itemId)]).concat(it.alts.filter(function (x, j) { return j !== ai && x.itemId; }).map(function (x) { return String(x.itemId); }));
              return '<div class="altbox"><div class="top">' + fld('Alternative item', '<select data-alt="' + ai + ':itemId">' + opts(LK.items.filter(function (x) { return x.isActive && (ex.indexOf(String(x.id)) === -1 || String(x.id) === String(a.itemId)); }).map(function (x) { return { v: x.id, t: x.name }; }), a.itemId || '', 'Pick an item') + '</select>') +
                '<button type="button" class="iconbtn" data-rmalt="' + ai + '" aria-label="Remove alternative">' + ic('close', 22) + '</button></div><div class="g4">' + fld('Qty', '<input inputmode="decimal" data-alt="' + ai + ':qty" value="' + esc(a.qty) + '">') +
                fld('Unit', '<select data-alt="' + ai + ':unit"' + (am ? '' : ' disabled') + '>' + opts(am ? am.units : [], a.unit || (am && am.unit) || '') + '</select>') + fld('Prep', '<select data-alt="' + ai + ':prep"' + (am ? '' : ' disabled') + '>' + opts(am ? am.preps : [], a.prep || '', '') + '</select>') + '</div></div>'; }).join('');
        }
      } else {
        var list = LK.mixes.filter(function (x) { return x.kind === it.kind && (x.isActive || x.key === it.mixKey) && (used.indexOf(x.key) === -1 || x.key === it.mixKey); });
        h += fld(it.kind === 'recipe' ? 'Diet recipe' : 'Diet mix', '<select data-iv="mixKey">' + opts(list.map(function (x) { return { v: x.key, t: x.name }; }), it.mixKey || '', it.kind === 'recipe' ? 'Pick a recipe' : 'Pick a mix') + '</select>', { req: true }) +
          (mx ? '<div class="mixsum t-body-regular">' + mx.items.map(function (x) { return '<span class="tag teal">' + esc(x.name + (it.kind === 'mix' ? ' ' + Math.round(x.share || 0) + '%' : '')) + '</span>'; }).join('') + '</div>' : '') +
          '<div class="g2">' + fld('Qty', '<span class="adorn"><input inputmode="decimal" data-iv="qty" value="' + esc(it.qty) + '"><em>' + esc(mx ? mx.unit : '') + '</em></span>', { req: true, help: 'Unit follows the ' + (it.kind === 'recipe' ? 'recipe' : 'mix') + '.' }) + '</div>';
      }
      h += '</div>';
      if (qm === 'sex') h += '<div class="sec2"><h4>By sex</h4><p class="t-body-regular" style="color:var(--md3-neutral-secondary)">Leave blank to use the standard ration. Undetermined-sex animals always use the standard ration.</p><div class="g2">' + fld('Female', '<input inputmode="decimal" data-iv="qtyF" value="' + esc(it.qtyF) + '" placeholder="' + esc(it.qty || '') + '">') + fld('Male', '<input inputmode="decimal" data-iv="qtyM" value="' + esc(it.qtyM) + '" placeholder="' + esc(it.qty || '') + '">') + '</div></div>';
      if (qm === 'age' || qm === 'weight') h += '<div class="sec2"><h4>By ' + (qm === 'age' ? 'age (' + W.d.ageUnit + ')' : 'weight (kg)') + '</h4><p class="t-body-regular" style="color:var(--md3-neutral-secondary)">Leave blank to use the standard ration.</p><div class="g4">' + W.d.qBands.map(function (b) { return fld(esc(bandName(b)), '<input inputmode="decimal" data-bq="' + b.k + '" value="' + esc(it.bandQty[b.k] || '') + '" placeholder="' + esc(it.qty || '') + '">'); }).join('') + '</div></div>';
      if (it.cadence === 'weekly') {
        h += '<div class="sec2"><h4>Schedule<span class="presets">' + ['All', 'None', 'Weekdays', 'Weekend'].map(function (p) { return '<button type="button" class="linkbtn t-body-medium" data-preset="' + p + '">' + p + '</button>'; }).join('') + '</span></h4><div class="daychips" role="group" aria-label="Days">' +
          DAYS.map(function (d) { return '<button type="button" data-day="' + d + '" aria-pressed="' + (it.days.indexOf(d) !== -1) + '">' + d.slice(0, 2) + '</button>'; }).join('') + '</div><button type="button" class="linkbtn t-body-medium" data-cad="every_n_days" style="justify-self:start">Longer frequency</button></div>';
      } else {
        var mdl = []; for (var i = 1; i <= 28; i++) mdl.push({ v: i, t: 'Day ' + i }); mdl.push({ v: -1, t: 'Last day' });
        h += '<div class="sec2"><h4>Schedule<button type="button" class="linkbtn t-body-medium" data-cad="weekly">Back to weekly</button></h4><p class="t-body-regular" style="color:var(--md3-neutral-secondary)">The cadence runs on this schedule. Weekday selection does not apply.</p><div class="g2">' +
          fld('Cadence', '<select data-iv="cadence">' + opts([{ v: 'every_n_days', t: 'Every N days' }, { v: 'monthly_day', t: 'Monthly on day' }], it.cadence) + '</select>') +
          (it.cadence === 'every_n_days' ? fld('Interval (days)', '<input inputmode="numeric" data-iv="intervalDays" value="' + esc(it.intervalDays) + '" placeholder="10">') + fld('First feed', '<input type="date" data-iv="anchorDate" value="' + esc(it.anchorDate) + '">') : fld('Day of month', '<select data-iv="monthDay">' + opts(mdl, it.monthDay, '') + '</select>')) + '</div></div>';
      }
      h += fld('Notes', '<textarea data-iv="notes" placeholder="Optional">' + esc(it.notes) + '</textarea>');
      if (IS.error) h += alertBox(IS.error);
      h += '<div class="sheet__f end">' + (IS.ii != null ? '<button type="button" class="btn ghost" data-isdel style="margin-right:auto;color:var(--md3-error)">Remove item</button>' : '') + '<button type="button" class="btn sec" data-isclose>Cancel</button><button type="button" class="btn pri" data-issave>Save item</button></div>';
      sheetEl().innerHTML = h;
    }

    /* ---------- diet picker (Adopt / Prefill from diet) ---------- */
    function openPicker(purpose) {
      IS = { mode: 'pick', purpose: purpose, q: '', tsn: null, plan: null };
      drawPicker(); document.getElementById('wsheet').hidden = false;
    }
    function drawPicker() {
      var q = IS.q.trim().toLowerCase();
      var sp = SPECIES.filter(function (s) { return s.tsn !== W.tsn && plansOf(s).some(function (p) { return p.active; }) && (!q || (s.name + ' ' + s.sci).toLowerCase().indexOf(q) !== -1); }).sort(function (a, b) { return a.name.localeCompare(b.name); });
      var h = '<div class="grab"></div><div class="sheet__h"><div><h2 class="t-major-title" id="wsT">' + (IS.purpose === 'adopt' ? 'Adopt an existing diet' : 'Prefill from a diet') + '</h2><p class="t-body-regular" style="color:var(--ink)">' + (IS.purpose === 'adopt' ? 'Pick a species, then the diet this new slot should follow. It is shared, not copied.' : 'Pick a species, then the diet whose time bands and items to copy into this draft.') + '</p></div><button type="button" class="iconbtn" data-isclose aria-label="Close">' + ic('close', 24) + '</button></div>';
      if (!IS.tsn) {
        h += '<label class="spsearch">' + ic('search', 20) + '<span class="sr-only">Search species</span><input class="t-body-regular" type="search" data-pq placeholder="Search species" value="' + esc(IS.q) + '"></label><div class="pick">' +
          sp.map(function (s) { return '<button type="button" data-ptsn="' + s.tsn + '"><span class="spav t-body-title" style="width:40px;height:40px">' + initials(s.name) + '</span><span class="grow"><b class="t-body-title">' + esc(s.name) + '</b><span class="t-body-regular">' + plural(plansOf(s).filter(function (p) { return p.active; }).length, 'active diet') + '</span></span>' + ic('dropdown', 22).replace('<svg', '<svg style="transform:rotate(-90deg)"') + '</button>'; }).join('') + '</div>';
      } else {
        var s2 = BY[IS.tsn];
        h += '<button type="button" class="linkbtn t-body-medium" data-pback2 style="justify-self:start">' + ic('back', 20) + esc(s2.name) + '</button><div class="pick">' + plansOf(s2).filter(function (p) { return p.active; }).map(function (p) {
          var n = (p.schedule || []).reduce(function (a, b) { return a + (b.days || []).reduce(function (c, g) { return c + (g.items || []).length; }, 0); }, 0);
          return '<button type="button" data-pplan="' + p.id + '" aria-pressed="' + (IS.plan === p.id) + '"><span class="grow"><b class="t-body-title">' + shownId(p) + ' ' + kindTag(p) + '</b><span class="t-body-regular">' + esc(p.scope === 'species' ? 'Species-wide' : ({ site: 'Site', section: 'Section', enclosure: 'Enclosure', animal: 'Animal' })[p.scope] + (p.scopeName ? ' · ' + p.scopeName : '')) + ' · ' + plural(n, 'item') + '</span></span></button>';
        }).join('') + '</div><div class="sheet__f end"><button type="button" class="btn sec" data-isclose>Cancel</button><button type="button" class="btn pri" data-pconfirm' + (IS.plan ? '' : ' disabled') + '>' + (IS.purpose === 'adopt' ? 'Adopt diet' : 'Prefill') + '</button></div>';
      }
      sheetEl().innerHTML = h;
    }
    function closeSheet2() { IS = null; document.getElementById('wsheet').hidden = true; }

    /* ---------- prefill: plan schedule back into draft bands ---------- */
    function findItemId(name) { var x = LK.items.filter(function (i) { return i.name === name; })[0]; return x ? x.id : null; }
    function findMix(name) { var x = LK.mixes.filter(function (m) { return m.name === name; })[0]; return x || null; }
    function tbFromLabel(t) {
      t = String(t || '').toLowerCase(); if (t === 'any time' || !t) return 'any'; if (t.indexOf('ad lib') === 0) return 'adlib';
      var hit = LK.timeBands.filter(function (b) { return (hm12(b.timeStart) + ' to ' + hm12(b.timeEnd)).toLowerCase() === t; })[0]; return hit ? String(hit.id) : 'any';
    }
    function bandsFrom(p) {
      return (p.schedule || []).map(function (b) {
        var nb = { tb: tbFromLabel(b.time), items: [], notes: '' };
        (b.days || []).forEach(function (g) { (g.items || []).forEach(function (x) {
          var mx = x.mix ? findMix(x.name) : null, it = emptyItem(x.mix ? (mx ? mx.kind : 'mix') : 'item');
          var m = /^([\\d.]+)\\s*(.*)$/.exec(x.amount || ''); it.qty = m ? m[1] : '';
          if (it.kind === 'item') { it.itemId = findItemId(x.name); it.unit = m ? m[2] : null; it.prep = x.prep || null; it.cut = x.cut || null;
            it.alts = (x.alts || []).map(function (a) { a = typeof a === 'string' ? { name: a } : a; var am = /^([\\d.]+)\\s*(.*)$/.exec(a.amount || ''); return { itemId: findItemId(a.name), qty: am ? am[1] : '', unit: am ? am[2] : null, prep: a.prep || null }; }).filter(function (a) { return a.itemId; }); }
          else it.mixKey = mx ? mx.key : null;
          if (g.day && g.day !== 'Daily') { var ds = g.day.split(/,\\s*/).filter(function (d) { return DAYS.indexOf(d) !== -1; }); if (ds.length) it.days = ds; }
          if ((it.kind === 'item' && it.itemId) || (it.kind !== 'item' && it.mixKey)) nb.items.push(it);
        }); });
        return nb;
      }).filter(function (b) { return b.items.length; });
    }
    function prefillFrom(p) {
      var bands = bandsFrom(p);
      if (!bands.length) { toast('That diet has no items that match the current masters.'); return; }
      W.d.bands = bands; W.error = null; drawWiz(); toast('Time bands copied from ' + shownId(p) + '.');
    }

    /* ---------- save (diet-editor.js doSave / adoptAndClose, kept in memory) ---------- */
    function nextId() { return Math.max.apply(null, Object.keys(PLANS).map(Number)) + 1; }
    function amountTxt(q, u) { return q + (u ? ' ' + u : ''); }
    function toPlanItem(it) {
      var o = { name: itemName(it), amount: amountTxt(it.qty, itemUnit(it)) };
      if (it.kind === 'item') { if (it.prep) o.prep = it.prep; if (it.cut) o.cut = it.cut;
        var alts = it.alts.filter(function (a) { return a.itemId && Number(a.qty) > 0; }).map(function (a) { var am = ITEM[a.itemId]; var r = { name: am.name, amount: amountTxt(a.qty, a.unit || am.unit) }; if (a.prep) r.prep = a.prep; return r; }); if (alts.length) o.alts = alts; }
      else { var mx = MIX[it.mixKey]; o.mix = { label: it.kind === 'recipe' ? 'RECIPE' : 'MIX', meta: plural(mx.items.length, 'item') + (it.kind === 'mix' ? ' · ' + mx.items.map(function (x) { return Math.round(x.share || 0) + '%'; }).join(' / ') : ''), parts: mx.items.map(function (x) { return { name: x.name }; }) }; }
      var qm = W.d.quantityMode, u = itemUnit(it);
      if (qm === 'sex') o.extra = [it.qtyF ? amountTxt(it.qtyF, u) : amountTxt(it.qty, u), it.qtyM ? amountTxt(it.qtyM, u) : amountTxt(it.qty, u)];
      if (qm === 'age' || qm === 'weight') o.extra = W.d.qBands.map(function (b) { return it.bandQty[b.k] ? amountTxt(it.bandQty[b.k], u) : amountTxt(it.qty, u); });
      if (it.notes) o.notes = it.notes;
      return o;
    }
    function scopeName() { var l = scopeLabel(); return W.scope === 'species' ? undefined : l.split(' · ')[1]; }
    function addProposed(p) {
      var rec = RQ.get(W.req), s = BY[W.tsn];
      if (W.prevProposed && PLANS[W.prevProposed]) { delete PLANS[W.prevProposed]; s.plans = (s.plans || []).filter(function (x) { return x !== W.prevProposed; }); RQ.dropPlan(W.prevProposed); }
      p.active = false; p.proposed = true; p.fromReq = rec.id; p.sharers = []; if (W.editOf) { p.editOf = W.editOf; p.editOfLabel = eoL(); } PLANS[p.id] = p; s.plans = [p.id].concat(s.plans || []); RQ.keepPlan(p);
      rec.editOf = W.editOf || null; rec.configuredBy = { id: RQ.viewer.id, name: RQ.viewer.name }; rec.editOfLabel = W.editOf ? eoL() : null;
      rec.proposedId = p.id; rec.cfgKind = W.cfgKind; rec.cfgLabel = { base: 'Base diet', 'year-round': 'Year-round diet', seasonal: 'Seasonal diet', 'time-bound': 'Time-bound diet' }[W.cfgKind] || 'Proposed diet';
      RQ.ev(rec, 'draft', 'Configured as ' + rec.cfgLabel + ' D-' + p.id + (W.editOf ? ' (Proposed change to ' + eoL() + ')' : ' (Proposed)')); RQ.changed();
      var id = rec.id; closeWizard();
      try { history.replaceState(null, '', '#request/' + id); } catch (x) {} window.dispatchEvent(new HashChangeEvent('hashchange'));
      toast('Proposed diet D-' + p.id + ' saved to ' + id + '. It is not active.');
    }
    function addPlan(p) {
      if (W.req) { addProposed(p); return; }
      var s = BY[W.tsn]; PLANS[p.id] = p; s.plans = [p.id].concat(s.plans || []); s.diet = true;
      var key = p.sharedFrom || p.id; Object.keys(PLANS).forEach(function (k) { var x = PLANS[k]; if ((x.sharedFrom || x.id) === key && x.active) { x.sharers = x.sharers || []; if (!x.sharers.some(function (y) { return y[1] === p.id; })) x.sharers.push([p.species, p.id]); } });
      p.sharers = Object.keys(PLANS).map(function (k) { return PLANS[k]; }).filter(function (x) { return (x.sharedFrom || x.id) === key && x.active; }).map(function (x) { return [x.species, x.id]; });
      var isFirst = W.base, kindTxt = p.kind === 'seasonal' ? 'Seasonal diet' : p.kind === 'time-bound' ? 'Time-bound diet' : isFirst ? 'Base diet' : 'Year-round diet';
      st.scope = p.scope; st.ref = p.scope === 'species' ? null : p.ref; st.plan = p.id; st.tab = 'items'; st.showInactive = false;
      var msg = kindTxt + ' ' + shownId(p) + ' created for ' + s.name + (p.scope !== 'species' ? ' (' + scopeLabel() + ')' : '') + '.';
      closeWizard();
      if (st.seg === 'without') st.seg = 'with';
      try { history.replaceState(null, '', '#species/' + st.seg + '/' + s.tsn + '/' + p.id); } catch (x) {}
      drawList(); if (LAND.matches) drawDetail(); else openPanel();
      toast(msg);
    }
    function windowFields() { var o = {}; if (W.kind !== 'year-round') { o.from = W.from; o.to = W.to; if (W.kind === 'seasonal') o.recurring = true; } return o; }
    function doSave() {
      var e = bandsErr(); if (e) { W.error = e; W.step = 'editor'; drawWiz(); return; }
      if (F().includeReason && !W.d.reason) { W.error = 'Pick a change reason before saving.'; drawWiz(); return; }
      var d = W.d, cols = d.quantityMode === 'sex' ? ['Female', 'Male'] : (d.quantityMode === 'age' || d.quantityMode === 'weight') ? d.qBands.map(bandName) : undefined;
      var schedule = d.bands.map(function (b) {
        var groups = [], by = {};
        b.items.forEach(function (it) { var dl = cadLabel(it); if (!by[dl]) { by[dl] = { day: dl, items: [] }; groups.push(by[dl]); } by[dl].items.push(toPlanItem(it)); });
        return { time: tbLabel(b), days: groups, notes: b.notes || undefined };
      });
      var notes = {}; if (d.notes) notes.kitchen = d.notes; if (d.siteNotes) notes.site = d.siteNotes;
      var p = Object.assign({ id: nextId(), species: W.tsn, scope: W.scope, active: true, verified: false, update: 'none', dietitian: d.dietitian || null, created: todayIso(), by: 'You', schedule: schedule,
        kind: W.kind === 'seasonal' ? 'seasonal' : W.kind === 'time-bound' ? 'time-bound' : 'base' }, windowFields());
      if (W.scope !== 'species') { p.ref = W.ref; p.scopeName = scopeName(); }
      if (d.reason) p.reason = d.reason; if (d.remarks) p.reasonDetail = d.remarks; if (d.remark) p.remark = d.remark; if (notes.kitchen || notes.site) p.notes = notes;
      if (d.quantityMode !== 'standard') { p.quantityMode = d.quantityMode; p.columns = cols; }
      addPlan(p);
    }
    function adopt(srcId) {
      var src = PLANS[srcId]; if (!src) return;
      if (W.kind === 'year-round' && scopePlansFor(BY[W.tsn], W.scope, W.ref).some(isDefault)) { W.path = null; W.error = 'A year-round diet already exists here. Edit the current diet to change its items.'; drawWiz(); return; }
      var p = Object.assign({ id: nextId(), species: W.tsn, scope: W.scope, sharedFrom: src.sharedFrom || src.id, active: true, verified: false, update: 'none', dietitian: src.dietitian || null, created: todayIso(), by: 'You',
        schedule: JSON.parse(JSON.stringify(src.schedule || [])), nutrition: src.nutrition, columns: src.columns, quantityMode: src.quantityMode,
        kind: W.kind === 'seasonal' ? 'seasonal' : W.kind === 'time-bound' ? 'time-bound' : 'base' }, windowFields());
      if (W.scope !== 'species') { p.ref = W.ref; p.scopeName = scopeName(); }
      addPlan(p);
    }

    /* ---------- Prefill with AI ----------
       SIMULATED: no network call. The "recommendation" is a few in-page rules over the request text and the
       masters (LK.items / LK.mixes). A real version would send the request (title, reason, notes, scope, kind,
       dates) plus the masters to a model and get back bands that use only those master ids. */
    var AIS = null, SPARK = '<svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2l1.9 5.6L19.5 9.5l-5.6 1.9L12 17l-1.9-5.6L4.5 9.5l5.6-1.9zM19 14l.9 2.6 2.6.9-2.6.9L19 21l-.9-2.6-2.6-.9 2.6-.9zM5 15l.7 1.8 1.8.7-1.8.7L5 20l-.7-1.8-1.8-.7 1.8-.7z"/></svg>';
    var SOFT_WORDS = ['soft', 'chopped', 'minced', 'mashed', 'mash'], SOFT_PREPS = ['Chopped', 'Steamed', 'Cooked'];
    var SWAPS = ['Sweet Potato', 'Carrot', 'Ragi', 'Bannana', 'Papaya', 'Spinach'];
    function aiText() { var r = W.req && RQ.get(W.req); return ((r ? r.title + '. ' + r.text + '. ' + (r.notes || '') : '') + '. ' + (AIS && AIS.extra || '')).toLowerCase(); }
    function stem(w) { return w.replace(/(es|s)$/, ''); }
    function words(t) { return t.split(/[^a-z]+/).filter(Boolean); }
    function masterIn(ws) { /* master items or mixes named inside a short run of words */
      var run = ' ' + ws.map(stem).join(' ') + ' ', hit = [];
      LK.items.forEach(function (x) { if (x.isActive && run.indexOf(' ' + words(x.name.toLowerCase()).map(stem).join(' ') + ' ') !== -1) hit.push({ kind: 'item', id: x.id, name: x.name }); });
      LK.mixes.forEach(function (x) { if (x.isActive && run.indexOf(' ' + words(x.name.toLowerCase()).map(stem).join(' ') + ' ') !== -1) hit.push({ kind: x.kind, key: x.key, name: x.name }); });
      return hit;
    }
    function aiRules(t) {
      var w = words(t), ex = [], add = [], soft = SOFT_WORDS.some(function (k) { return w.indexOf(k) !== -1; });
      w.forEach(function (x, i) {
        if (x === 'no' || x === 'avoid' || x === 'without') masterIn(w.slice(i + 1, i + 4)).forEach(function (m) { ex.push(m.name); });
        if (x === 'add' || x === 'include' || x === 'extra' || x === 'more') masterIn(w.slice(i + 1, i + 4)).forEach(function (m) { add.push(m); });
      });
      return { soft: soft, ex: ex, add: add.filter(function (m) { return ex.indexOf(m.name) === -1; }) };
    }
    function scopeAnimals(s, scope, ref) {
      if (scope === 'species') return s.animals || 1; if (scope === 'animal') return 1;
      var k = scope === 'site' ? 'siteId' : scope === 'section' ? 'sectionId' : 'id';
      return animalsAt(s, function (e) { return e[k] === ref; }) || 1;
    }
    function similarPlan(s) { /* same class, an active species-wide base whose items map to the masters */
      var best = null;
      SPECIES.forEach(function (o) { if (o.tsn === s.tsn || o.cls !== s.cls) return; var b = basePlan(o); if (!b) return; var n = bandsFrom(b).reduce(function (a, x) { return a + x.items.length; }, 0);
        if (n && (!best || Math.abs(o.animals - s.animals) < Math.abs(best.s.animals - s.animals))) best = { s: o, p: b }; });
      return best;
    }
    function roundQ(q, unit) { if (unit === 'g' || unit === 'pcs') return String(Math.max(1, Math.round(q))); var v = Math.max(0.1, Math.round(q * 10) / 10); return String(v); }
    function aiGenerate() {
      var s = BY[W.tsn], cur = currentAt(), src, srcName, factor = 1, why0;
      if (cur) { src = cur; srcName = shownId(cur); why0 = cur === basePlan(s) ? 'From base diet' : 'From current diet';
        factor = scopeAnimals(s, W.scope, W.ref) / scopeAnimals(s, cur.scope, cur.ref); }
      else { var sim = similarPlan(s); if (sim) { src = sim.p; srcName = sim.s.name + ' ' + shownId(sim.p); why0 = 'From ' + sim.s.name + ' diet'; factor = scopeAnimals(s, W.scope, W.ref) / (sim.s.animals || 1); } }
      factor = Math.min(20, Math.max(0.05, factor));
      var R = W.req ? aiRules(aiText()) : { soft: false, ex: [], add: [] }, out = [], left = [], seed = AIS.round;
      var bands = src ? bandsFrom(src) : [emptyBand()]; if (!bands.length) bands = [emptyBand()];
      var used = {};
      bands.forEach(function (b) { b.items.forEach(function (it) { if (it.kind === 'item') used[it.itemId] = 1; }); });
      bands.forEach(function (b) {
        var nb = { tb: b.tb, items: [], notes: '' };
        b.items.forEach(function (it) {
          var mi = it.kind === 'item' ? ITEM[it.itemId] : MIX[it.mixKey], nm = mi ? mi.name : '', unit = itemUnit(it);
          var q = Number(it.qty) || 0, qty = roundQ(q * factor, unit), why = why0 + (Math.abs(factor - 1) > 0.05 ? ', scaled to ' + plural(scopeAnimals(s, W.scope, W.ref), 'animal') : '');
          var mixHas = it.kind !== 'item' && mi && mi.items.some(function (x) { return R.ex.indexOf(x.name) !== -1; });
          var hard = it.kind === 'item' && R.soft && mi && !mi.preps.some(function (p) { return SOFT_PREPS.indexOf(p) !== -1; }) && mi.preps.indexOf('Whole') !== -1;
          if (R.ex.indexOf(nm) !== -1 || mixHas || hard) {
            var reasonOut = R.ex.indexOf(nm) !== -1 || mixHas ? 'excluded by request' : 'whole, request asks for soft food';
            left.push(nm + ' (' + reasonOut + ')');
            if (it.kind === 'item') { /* swap in a soft master item not already in the diet */
              var pool = SWAPS.slice(seed % SWAPS.length).concat(SWAPS.slice(0, seed % SWAPS.length));
              for (var k = 0; k < pool.length; k++) { var sw = LK.items.filter(function (x) { return x.name === pool[k] && x.isActive; })[0];
                if (sw && !used[sw.id] && R.ex.indexOf(sw.name) === -1) { used[sw.id] = 1; var ni = emptyItem('item'); ni.itemId = sw.id; ni.unit = sw.unit; ni.qty = qty; ni.days = it.days.slice(); ni.cadence = it.cadence;
                  if (R.soft) ni.prep = SOFT_PREPS.filter(function (p) { return sw.preps.indexOf(p) !== -1; })[0] || null; else ni.prep = sw.preps[0] || null;
                  ni.ai = 'Replaces ' + (mi.preps.indexOf('Whole') !== -1 ? 'whole ' : '') + nm.toLowerCase() + ' (' + reasonOut + ')'; nb.items.push(ni); break; } }
            }
            return;
          }
          var n = JSON.parse(JSON.stringify(it)); n.qty = qty; n.ai = why;
          if (n.alts) n.alts.forEach(function (a) { var au = a.unit || (ITEM[a.itemId] || {}).unit; a.qty = Number(a.qty) > 0 ? roundQ(Number(a.qty) * factor, au) : qty; });
          if (it.kind === 'item' && R.soft && mi) { var sp = SOFT_PREPS.filter(function (p) { return mi.preps.indexOf(p) !== -1; })[0]; if (sp && sp !== n.prep) { n.prep = sp; n.ai = sp + ' per request'; } else if (sp) n.ai = why + ', ' + sp.toLowerCase(); }
          nb.items.push(n);
        });
        out.push(nb);
      });
      R.add.forEach(function (m) {
        var have = null; out.forEach(function (b) { b.items.forEach(function (x) { if ((m.kind === 'item' && x.itemId === m.id) || (m.kind !== 'item' && x.mixKey === m.key)) have = x; }); });
        if (have) { have.qty = roundQ(Number(have.qty) * 1.25, itemUnit(have)); have.ai = 'Increased per request'; return; }
        var ni = emptyItem(m.kind); if (m.kind === 'item') { var mi = ITEM[m.id]; ni.itemId = m.id; ni.unit = mi.unit; ni.prep = R.soft ? (SOFT_PREPS.filter(function (p) { return mi.preps.indexOf(p) !== -1; })[0] || mi.preps[0] || null) : (mi.preps[0] || null); } else ni.mixKey = m.key;
        var unit = m.kind === 'item' ? ITEM[m.id].unit : MIX[m.key].unit; ni.qty = roundQ((unit === 'g' ? 50 : 0.5) * Math.max(1, scopeAnimals(s, W.scope, W.ref) / 4), unit); ni.ai = 'Added per request'; out[0].items.push(ni);
      });
      return { bands: out.filter(function (b) { return b.items.length; }), left: left, src: srcName, rules: R };
    }
    function aiOpen() { AIS = { step: 'ask', extra: (AIS && AIS.extra) || '', round: 0, res: null }; aiDraw(); document.getElementById('wsheet').hidden = false; }
    function aiDraw() {
      var r = W.req && RQ.get(W.req), s = BY[W.tsn], h = '<div class="grab"></div><div class="sheet__h"><div><h2 class="t-major-title" id="wsT"><span class="aimark">' + SPARK + '</span>' + (r ? 'Recommend from request' : 'Recommend a starting diet') + '</h2><p class="t-body-regular" style="color:var(--ink)">Uses only items, mixes and recipes in the masters.</p></div><button type="button" class="iconbtn" data-aiclose aria-label="Close">' + ic('close', 24) + '</button></div>';
      var ctx = [['Species', s.name], ['Scope', scopeLabel()], ['Kind', { 'year-round': W.base ? 'Base diet' : 'Year-round', seasonal: 'Seasonal', 'time-bound': 'Time-bound' }[W.kind]]];
      if (W.from && W.to && W.kind !== 'year-round') ctx.push(['Dates', W.kind === 'seasonal' ? dtx(W.from, true) + ' to ' + dtx(W.to, true) : dtx(W.from) + ' to ' + dtx(W.to)]);
      if (AIS.step !== 'preview') {
        h += '<div class="aictx t-body-regular">' + (r ? '<p><b>Request</b>' + esc(r.id + ' · ' + r.title) + '</p><p><b>Reason</b>' + esc(r.text) + '</p>' + (r.notes ? '<p><b>Notes</b>' + esc(r.notes) + '</p>' : '') : '') +
          '<div class="aictx__g">' + ctx.map(function (c) { return '<p><b>' + c[0] + '</b>' + esc(c[1]) + '</p>'; }).join('') + '</div></div>' +
          '<label class="fld"><span>Anything to add? <span style="color:var(--md3-neutral-secondary);font-weight:400">(optional)</span></span><input type="text" data-aiextra value="' + esc(AIS.extra) + '" placeholder="e.g. add papaya" autocomplete="off"' + (AIS.step === 'load' ? ' disabled' : '') + '></label>';
        h += '<div class="sheet__f end"><button type="button" class="btn sec" data-aiclose>Cancel</button><button type="button" class="btn teal aigo" data-aigen' + (AIS.step === 'load' ? ' disabled aria-busy="true"' : '') + '>' + (AIS.step === 'load' ? '<span class="aispin" aria-hidden="true"></span>Reading the request and masters' : SPARK + 'Generate') + '</button></div>';
      } else {
        var res = AIS.res, n = res.bands.reduce(function (a, b) { return a + b.items.length; }, 0);
        h += '<p class="t-body-regular aisrc">' + (res.src ? 'Started from ' + esc(res.src) + '.' : 'No diet to start from, so the lines are new.') + ' ' + plural(n, 'line') + ' in ' + plural(res.bands.length, 'time band') + '.</p>' +
          '<div class="aiscroll">' + res.bands.map(function (b) { return '<div class="aiband"><b class="t-body-title">' + ic('time', 18) + esc(tbLabel(b).replace(/^./, function (c) { return c.toUpperCase(); })) + '</b><ul>' + b.items.map(function (it) {
            return '<li><span class="grow"><span><b>' + esc(itemName(it)) + '</b>' + (it.kind !== 'item' ? ' <span class="it-k">' + (it.kind === 'recipe' ? 'RECIPE' : 'MIX') + '</span>' : '') + '</span><small>' + esc([it.qty + ' ' + itemUnit(it), it.prep, cadLabel(it)].filter(Boolean).join(' · ')) + '</small></span><span class="aiwhy">' + esc(it.ai) + '</span></li>'; }).join('') + '</ul></div>'; }).join('') + '</div>' +
          (res.left.length ? '<p class="t-body-regular aileft">Left out: ' + esc(res.left.join(', ')) + '</p>' : '') +
          '<p class="t-body-regular ainote">' + ic('info', 16) + 'AI suggestions are a starting point. Review before saving.</p>' +
          '<div class="sheet__f end"><button type="button" class="btn ghost" data-aiclose>Cancel</button><button type="button" class="btn sec" data-airegen>' + SPARK + 'Regenerate</button><button type="button" class="btn teal" data-aiapply>Apply</button></div>';
      }
      sheetEl().innerHTML = h;
    }
    function aiRun() { AIS.step = 'load'; aiDraw(); setTimeout(function () { if (!AIS) return; AIS.res = aiGenerate(); AIS.step = 'preview'; aiDraw(); }, 1500); }
    function closeAi() { AIS = null; document.getElementById('wsheet').hidden = true; }

    /* ---------- events ---------- */
    var wiz = document.getElementById('wiz');
    wiz.addEventListener('click', function (e) {
      if (!W) return; var t, d = W.d, l;
      if (e.target.closest('[data-pfmenu]')) { W.pfOpen = !W.pfOpen; drawWiz(); if (W.pfOpen) { var fm = document.querySelector('#wiz .pfmenu button'); if (fm) fm.focus(); } return; }
      if (W.pfOpen && !e.target.closest('.pfmenu')) { W.pfOpen = false; drawWiz(); }
      if (W.pfOpen && e.target.closest('.pfmenu [data-prefill]')) { W.pfOpen = false; var mm = document.querySelector('#wiz .pfmenu'), tb = document.querySelector('#wiz [data-pfmenu]'); if (mm) mm.remove(); if (tb) tb.setAttribute('aria-expanded', 'false'); }
      if (e.target.closest('[data-aiopen]')) { aiOpen(); return; }
      if (e.target.closest('[data-applydates]')) { var q = reqDates(); if (q) { W.from = q.from; W.to = q.to; W.error = null; drawWiz(); toast('Dates applied from ' + W.req + '.'); } return; }
      if (e.target.closest('[data-wreqopen]')) { if (!window.confirm('Leave the configuration? Your draft is not kept.')) { e.preventDefault(); return; } closeWizard(); return; }
      if (e.target.closest('[data-wclose], [data-wcancel]')) { var back = W.req ? '#request/' + W.req : '#species/' + st.seg + '/' + W.tsn + (st.plan ? '/' + st.plan : ''); closeWizard(); try { history.replaceState(null, '', back); } catch (x) {} window.dispatchEvent(new HashChangeEvent('hashchange')); return; }
      if (e.target.closest('[data-wback]')) { l = stepList().map(function (x) { return x[0]; }); var i = l.indexOf(W.step); if (i > 0) history.back(); return; }
      if (e.target.closest('[data-wnext]')) {
        if (W.step === 'editor') { var be = bandsErr(); if (be) { W.error = be; drawWiz(); return; } }
        if (!stepValid()) return; l = stepList().map(function (x) { return x[0]; }); var j = l.indexOf(W.step); if (j < l.length - 1) goStep(l[j + 1], true); return;
      }
      if (e.target.closest('[data-wsave]')) { doSave(); return; }
      if ((t = e.target.closest('[data-wscope]'))) { var ns = t.getAttribute('data-wscope'); if (ns !== W.scope) { W.scope = ns; W.ref = null; W.sq = ''; W.ssx = ''; W.qPick = null; W.path = null; } drawWiz(); return; }
      if ((t = e.target.closest('[data-wsref]'))) { if (t.disabled) return; W.ref = Number(t.getAttribute('data-wsref')); var keep = document.querySelector('#wiz [data-wslist]').scrollTop; drawWiz(); document.querySelector('#wiz [data-wslist]').scrollTop = keep; drawScopeList(); return; }
      if ((t = e.target.closest('[data-wsx]'))) { W.ssx = t.getAttribute('data-wsx'); drawWiz(); return; }
      if (e.target.closest('[data-wchscope]')) { goStep('scope', true); return; }
      if ((t = e.target.closest('[data-path]'))) { W.path = t.getAttribute('data-path'); W.error = null; if (W.path === 'adopt') { drawWiz(); openPicker('adopt'); } else drawWiz(); return; }
      if ((t = e.target.closest('[data-qpick]'))) { W.qPick = t.getAttribute('data-qpick'); d.quantityMode = F().skipQuantity ? 'standard' : W.qPick; d.qBands = defBands(d.quantityMode); drawWiz(); return; }
      if ((t = e.target.closest('[data-qmode]'))) { var qm = t.getAttribute('data-qmode'); if (qm !== d.quantityMode) { d.quantityMode = qm; d.qBands = defBands(qm); if (qm !== 'age') d.ageUnit = 'years'; } drawWiz(); return; }
      if ((t = e.target.closest('[data-ageunit]'))) { var u = t.getAttribute('data-ageunit'); if (u !== d.ageUnit) { var fac = u === 'months' ? 12 : 1 / 12; d.qBands.forEach(function (b) { ['from', 'to'].forEach(function (k) { if (String(b[k]).trim() !== '' && isFinite(Number(b[k]))) b[k] = String(Math.round(Number(b[k]) * fac * 100) / 100); }); }); d.ageUnit = u; } drawWiz(); return; }
      if (e.target.closest('[data-qbadd]')) { var lastB = d.qBands[d.qBands.length - 1]; d.qBands.push({ k: 'q' + (++wseq), from: lastB && lastB.to !== '' ? lastB.to : '', to: '' }); drawWiz(); return; }
      if ((t = e.target.closest('[data-qbrm]'))) { if (d.qBands.length > 1) d.qBands.splice(Number(t.getAttribute('data-qbrm')), 1); drawWiz(); return; }
      if (e.target.closest('[data-addband]')) { var usedTb = d.bands.map(function (b) { return b.tb; }), free = ['any', 'adlib'].concat(LK.timeBands.map(function (x) { return String(x.id); })).filter(function (x) { return usedTb.indexOf(x) === -1; })[0]; var nb = emptyBand(); nb.tb = free || 'any'; d.bands.push(nb); drawWiz(); return; }
      if ((t = e.target.closest('[data-tbclone]'))) { var bi = Number(t.getAttribute('data-tbclone')), cp = JSON.parse(JSON.stringify(d.bands[bi])); var usedT = d.bands.map(function (b) { return b.tb; }); cp.tb = LK.timeBands.map(function (x) { return String(x.id); }).filter(function (x) { return usedT.indexOf(x) === -1; })[0] || 'any'; d.bands.splice(bi + 1, 0, cp); drawWiz(); return; }
      if ((t = e.target.closest('[data-tbrm]'))) { d.bands.splice(Number(t.getAttribute('data-tbrm')), 1); if (!d.bands.length) d.bands.push(emptyBand()); drawWiz(); return; }
      if ((t = e.target.closest('[data-rmitem]'))) { e.stopPropagation(); var p2 = t.getAttribute('data-rmitem').split(':').map(Number); d.bands[p2[0]].items.splice(p2[1], 1); drawWiz(); return; }
      if ((t = e.target.closest('[data-additem]'))) { var p3 = t.getAttribute('data-additem').split(':'); openItem(Number(p3[0]), null, p3[1]); return; }
      if ((t = e.target.closest('[data-edititem]'))) { var p4 = t.getAttribute('data-edititem').split(':').map(Number); openItem(p4[0], p4[1]); return; }
      if ((t = e.target.closest('[data-prefill="current"]'))) { var cp = currentAt(); if (cp && (!d.bands.some(function (b) { return b.items.length; }) || window.confirm('Replace the current feeding time bands with ' + shownId(cp) + '? Dates stay the same.'))) prefillFrom(cp); return; }
      if ((t = e.target.closest('[data-prefill]'))) { if (t.getAttribute('data-prefill') === 'base') { var bp = F().base; if (bp && (!d.bands.some(function (b) { return b.items.length; }) || window.confirm('Replace the current feeding time bands with the base diet? Dates stay the same.'))) prefillFrom(bp); } else openPicker('prefill'); return; }
      if ((t = e.target.closest('[data-reason]'))) { d.reason = t.getAttribute('data-reason'); W.error = null; drawWiz(); return; }
    });
    wiz.addEventListener('change', function (e) {
      if (!W) return; var t = e.target, d = W.d;
      if (t.matches('[data-md]')) { var k = t.getAttribute('data-md').split(':'), side = k[0], x = md(W[side]) || { m: 1, d: 1 }; if (k[1] === 'm') { x.m = Number(t.value); x.d = Math.min(x.d, daysIn(x.m)); } else x.d = Number(t.value);
        var y = new Date().getFullYear(), other = md(W[side === 'from' ? 'to' : 'from']) || x; W[side] = y + '-' + pad(x.m) + '-' + pad(x.d);
        var f = md(W.from), to = md(W.to); if (f && to) { var wraps = to.m < f.m || (to.m === f.m && to.d <= f.d); W.from = y + '-' + pad(f.m) + '-' + pad(f.d); W.to = (wraps ? y + 1 : y) + '-' + pad(to.m) + '-' + pad(to.d); } drawWiz(); return; }
      if (t.matches('[data-wd]')) { W[t.getAttribute('data-wd')] = t.value; drawWiz(); return; }
      if (t.matches('[data-tb]')) { d.bands[Number(t.getAttribute('data-tb'))].tb = t.value; W.error = null; drawWiz(); return; }
      if (t.matches('[data-dietitian], [data-dv="dietitian"]')) { d.dietitian = t.value; return; }
    });
    wiz.addEventListener('input', function (e) {
      if (!W) return; var t = e.target, d = W.d;
      if (t.matches('[data-wsq]')) { W.sq = t.value; var bx = document.querySelector('#wiz [data-wslist]'); drawScopeList(); bx.scrollTop = 0; return; }
      if (t.matches('[data-dv]')) { d[t.getAttribute('data-dv')] = t.value; return; }
      if (t.matches('[data-bnote]')) { d.bands[Number(t.getAttribute('data-bnote'))].notes = t.value; return; }
      if (t.matches('[data-qb]')) { var k = t.getAttribute('data-qb').split(':'); d.qBands[Number(k[0])][k[1]] = t.value.replace(/[^\\d.]/g, ''); return; }
    });
    wiz.addEventListener('toggle', function (e) { if (W && e.target.matches && e.target.matches('[data-wreq]')) { W.reqOpen = e.target.open; fitReq(); } }, true);
    wiz.addEventListener('keydown', function (e) { if (W && W.pfOpen && e.key === 'Escape') { e.stopPropagation(); W.pfOpen = false; drawWiz(); var b = document.querySelector('#wiz [data-pfmenu]'); if (b) b.focus(); } });
    wiz.addEventListener('scroll', function (e) { if (e.target.matches && e.target.matches('[data-wreqsc]')) edge(e.target); }, true);
    window.addEventListener('resize', function () { if (W && W.req) fitReq(); });
    wiz.addEventListener('scroll', function (e) { if (e.target.matches && e.target.matches('[data-wslist]')) { var b = e.target.parentNode; b.classList.toggle('ft', e.target.scrollTop > 2); b.classList.toggle('fb', e.target.scrollTop + e.target.clientHeight < e.target.scrollHeight - 2); } }, true);
    wiz.addEventListener('focusout', function (e) { if (W && e.target.matches('[data-qb]')) drawWiz(); });
    var ws = document.getElementById('wsheet');
    ws.addEventListener('click', function (e) {
      if (!AIS) return;
      if (e.target === ws || e.target.closest('[data-aiclose]')) { closeAi(); return; }
      if (e.target.closest('[data-aigen]') && AIS.step === 'ask') { var x = sheetEl().querySelector('[data-aiextra]'); AIS.extra = x ? x.value.trim() : ''; aiRun(); return; }
      if (e.target.closest('[data-airegen]')) { AIS.round++; aiRun(); return; }
      if (e.target.closest('[data-aiapply]')) { var res = AIS.res; if (W.d.bands.some(function (b) { return b.items.length; }) && !window.confirm('Replace the current feeding time bands with the AI suggestion?')) return;
        W.d.bands = res.bands.length ? res.bands : [emptyBand()]; W.error = null; closeAi(); drawWiz(); toast('AI suggestion applied. Review each line before saving.'); return; }
    });
    ws.addEventListener('keydown', function (e) { if (AIS && e.target.matches('[data-aiextra]') && e.key === 'Enter') { e.preventDefault(); AIS.extra = e.target.value.trim(); aiRun(); } });
    ws.addEventListener('click', function (e) {
      if (!IS) return; var t, it = IS.it;
      if (e.target === ws || e.target.closest('[data-isclose]')) { if (IS.mode === 'pick' && IS.purpose === 'adopt') { W.path = null; drawWiz(); } closeSheet2(); return; }
      if (IS.mode === 'pick') {
        if ((t = e.target.closest('[data-ptsn]'))) { IS.tsn = Number(t.getAttribute('data-ptsn')); IS.plan = null; drawPicker(); return; }
        if (e.target.closest('[data-pback2]')) { IS.tsn = null; drawPicker(); return; }
        if ((t = e.target.closest('[data-pplan]'))) { IS.plan = Number(t.getAttribute('data-pplan')); drawPicker(); return; }
        if (e.target.closest('[data-pconfirm]') && IS.plan) { var pid = IS.plan, pur = IS.purpose; closeSheet2(); if (pur === 'adopt') adopt(pid); else { var src = PLANS[pid]; if (!W.d.bands.some(function (b) { return b.items.length; }) || window.confirm('Replace the current feeding time bands with the selected diet? Dates stay the same.')) prefillFrom(src); } }
        return;
      }
      if ((t = e.target.closest('[data-ikind]'))) { var k = t.getAttribute('data-ikind'); if (k !== it.kind) { var keep = { qty: it.qty, cadence: it.cadence, days: it.days, notes: it.notes }; IS.it = Object.assign(emptyItem(k), keep); IS.error = null; drawItem(); } return; }
      if (e.target.closest('[data-addalt]')) { it.alts.push({ itemId: null, qty: '', unit: null, prep: null }); drawItem(); return; }
      if ((t = e.target.closest('[data-rmalt]'))) { it.alts.splice(Number(t.getAttribute('data-rmalt')), 1); drawItem(); return; }
      if ((t = e.target.closest('[data-preset]'))) { var p = t.getAttribute('data-preset'); it.days = p === 'All' ? DAYS.slice() : p === 'None' ? [] : p === 'Weekdays' ? DAYS.slice(0, 5) : DAYS.slice(5); drawItem(); return; }
      if ((t = e.target.closest('[data-day]'))) { var dd = t.getAttribute('data-day'), i = it.days.indexOf(dd); if (i === -1) it.days.push(dd); else it.days.splice(i, 1); it.days.sort(function (a, b) { return DAYS.indexOf(a) - DAYS.indexOf(b); }); drawItem(); return; }
      if ((t = e.target.closest('[data-cad]'))) { it.cadence = t.getAttribute('data-cad'); drawItem(); return; }
      if (e.target.closest('[data-isdel]')) { if (window.confirm('Remove this item from the band?')) { W.d.bands[IS.bi].items.splice(IS.ii, 1); closeSheet2(); drawWiz(); } return; }
      if (e.target.closest('[data-issave]')) { var er = itemErr(it); if (er) { IS.error = er; drawItem(); return; } it.ai = null; it.alts = it.kind === 'item' ? it.alts.filter(function (a) { return a.itemId; }) : [];
        var band = W.d.bands[IS.bi]; if (IS.ii == null) band.items.push(it); else band.items[IS.ii] = it; W.error = null; closeSheet2(); drawWiz(); }
    });
    ws.addEventListener('change', function (e) {
      if (!IS || IS.mode !== 'item') return; var t = e.target, it = IS.it;
      if (t.matches('[data-iv]')) { var k = t.getAttribute('data-iv'); it[k] = k === 'itemId' ? (t.value ? Number(t.value) : null) : (t.value || (k === 'unit' || k === 'prep' || k === 'cut' || k === 'mixKey' ? null : ''));
        if (k === 'itemId') { var mi = ITEM[it.itemId]; it.unit = mi ? mi.unit : null; it.prep = null; it.cut = null; it.alts = []; }
        if (k === 'itemId' || k === 'mixKey' || k === 'cadence') drawItem(); return; }
      if (t.matches('[data-alt]')) { var a = t.getAttribute('data-alt').split(':'), al = it.alts[Number(a[0])]; al[a[1]] = a[1] === 'itemId' ? (t.value ? Number(t.value) : null) : t.value || null; if (a[1] === 'itemId') { var am = ITEM[al.itemId]; al.unit = am ? am.unit : null; al.prep = null; drawItem(); } return; }
    });
    ws.addEventListener('input', function (e) {
      if (!IS) return; var t = e.target;
      if (IS.mode === 'pick' && t.matches('[data-pq]')) { IS.q = t.value; var pos = t.selectionStart; drawPicker(); var n = sheetEl().querySelector('[data-pq]'); n.focus(); n.setSelectionRange(pos, pos); return; }
      if (IS.mode !== 'item') return; var it = IS.it;
      if (t.matches('[data-iv="qty"], [data-iv="qtyF"], [data-iv="qtyM"], [data-iv="intervalDays"]')) { t.value = t.value.replace(t.getAttribute('data-iv') === 'intervalDays' ? /[^\\d]/g : /[^\\d.]/g, ''); it[t.getAttribute('data-iv')] = t.value; return; }
      if (t.matches('[data-iv="notes"]')) { it.notes = t.value; return; }
      if (t.matches('[data-alt]')) { var a = t.getAttribute('data-alt').split(':'); if (a[1] === 'qty') { t.value = t.value.replace(/[^\\d.]/g, ''); it.alts[Number(a[0])].qty = t.value; } return; }
      if (t.matches('[data-bq]')) { t.value = t.value.replace(/[^\\d.]/g, ''); it.bandQty[t.getAttribute('data-bq')] = t.value; }
    });

    /* kind menu on the plan "+" (Year-round / Seasonal / Time-bound) */
    var km = document.getElementById('kmenu');
    function openKindMenu(btn) {
      var s = BY[st.tsn], taken = scopePlansFor(s, st.scope, st.ref).some(isDefault);
      km.innerHTML = [['year-round', 'Year-round', taken ? 'Already set here. Edit the current diet instead.' : 'Always-on daily default'], ['seasonal', 'Seasonal', 'Repeats every year'], ['time-bound', 'Time-bound', 'Applies once between fixed dates']].map(function (k) {
        return '<button type="button" role="menuitem" data-kind="' + k[0] + '"' + (k[0] === 'year-round' && taken ? ' disabled' : '') + '><b class="t-body-title">' + k[1] + '</b><small>' + k[2] + '</small></button>'; }).join('');
      var r = btn.getBoundingClientRect(); km.hidden = false; km.style.top = Math.min(innerHeight - 200, r.bottom + 6) + 'px'; km.style.left = Math.max(8, Math.min(innerWidth - 268, r.left)) + 'px'; km.style.minWidth = '260px';
    }
    document.addEventListener('click', function (e) { if (!km.hidden && !e.target.closest('#kmenu') && !e.target.closest('[data-newplan]')) km.hidden = true; });
    km.addEventListener('click', function (e) { var b = e.target.closest('[data-kind]'); if (!b || b.disabled) return; km.hidden = true; openWizard(b.getAttribute('data-kind'), false); });
    function wizRoute(seg, tsn, kindSeg, step) {
      if (!tsn || !BY[tsn]) return;
      var kind = kindSeg === 'base' ? 'year-round' : kindSeg, isBase = kindSeg === 'base';
      if (W && W.tsn === tsn && (W.kind === kind || W.req)) {
        var l = stepList().map(function (x) { return x[0]; }), i = l.indexOf(step || l[0]);
        if (i !== -1 && i <= W.reached) { W.step = l[i]; W.error = null; drawWiz(); document.getElementById('wiz').hidden = false; } else { try { history.replaceState(null, '', wizHash(W.step)); } catch (x) {} }
        return;
      }
      st.tsn = tsn; if (!BY[tsn] || !plansOf(BY[tsn]).filter(isBase).length) isBase = true;
      openWizard(isBase ? 'year-round' : kind, isBase, true);
    }
'''
