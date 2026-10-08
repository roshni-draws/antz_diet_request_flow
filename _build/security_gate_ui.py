# security_gate_ui.py: exec'd by security.py. Security role: the gate screen opened from the Gates tab (#gates/G01).
# Layout from the user's 8 Oct gate screenshots, built with the site page's parts (hero band, tab bar, search band, cards):
# hero with the building and a gate switcher, tabs All | Checked in | Checked out (no transfers: gate departments are not animal related),
# search (vendor, DC number, vehicle) with a scan button and a Sealed DC filter, vehicle cards, and a + button with
# Log Entry, Log Exit and Upload Sealed DC. Changes are kept in localStorage 'antz.security.gate'.
GATE_CSS = """    /* =========================================================
       19. GATE SCREEN  (Security: Gates tab > a gate)
       ========================================================= */
    .gtpanel { grid-template-rows: auto auto 1fr; }
    .gthero { position: relative; overflow: hidden; display: grid; gap: 10px; padding: 56px var(--sp-20) var(--sp-16); background: var(--stc, #2C4F5A); color: var(--white); }
    .gthero .iconbtn { position: absolute; left: 8px; top: 8px; color: var(--white); }
    .gthero .asbtn { position: absolute; right: 12px; top: 10px; }
    .gthero .stcard__art { width: 220px; height: 220px; right: 24px; top: -30px; }
    .gthero__loc { position: relative; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; opacity: .9; }
    .gthero__loc i { width: 4px; height: 4px; border-radius: 50%; background: currentColor; }
    .gtpick { position: relative; justify-self: start; display: flex; align-items: center; gap: 12px; min-height: 56px; padding: 6px 14px 6px 6px; border-radius: var(--radius); background: rgba(0,0,0,.22); border: 1px solid rgba(255,255,255,.3); color: var(--white); text-align: left; }
    .gtpick .gico { width: 44px; height: 44px; border-radius: 6px; display: grid; place-items: center; background: var(--white); color: var(--md3-on-primary-container); }
    .gtpick b { display: flex; align-items: center; gap: 4px; font-size: 20px; font-weight: 600; }
    .gtpick small { opacity: .85; }
    .gtbody { min-height: 0; overflow-y: auto; padding: 0 var(--sp-16) 120px; background: var(--md3-surface-variant); }
    .gtband { position: sticky; top: 0; z-index: 1; display: flex; gap: var(--sp-12); padding: var(--sp-16) 0 var(--sp-12); background: var(--md3-surface-variant); }
    .gtband .spsearch { background: var(--white); border-color: var(--md3-outline-variant); }
    .gtband .spsearch .ricon { width: 40px; height: 40px; color: var(--md3-on-primary-container); margin-right: -6px; }
    .gtband .spfilter { background: var(--white); border-color: var(--md3-outline-variant); }
    .gtband .spfilter.on { background: var(--md3-on-primary-container); color: var(--white); }
    .gvc { display: flex; align-items: center; gap: var(--sp-16); width: 100%; padding: var(--sp-16) var(--sp-20); border-radius: var(--radius); background: var(--white); box-shadow: var(--card-shadow); text-align: left; }
    .gvc + .gvc { margin-top: var(--sp-12); }
    .gvc .grow { flex: 1; min-width: 0; display: grid; gap: 6px; }
    .gvc__no { color: #11823B; font-size: 18px; font-weight: 600; font-variant-numeric: tabular-nums; }
    .gvc__ln { display: flex; align-items: center; flex-wrap: wrap; gap: 6px 16px; color: var(--ink); }
    .gvc__ln > span { display: inline-flex; align-items: center; gap: 6px; }
    .gvc__ln svg.si { color: var(--md3-on-primary-container); }
    .gvc__ln .ven { color: var(--head); font-weight: 500; }
    .gvc__side { flex: none; display: grid; justify-items: end; gap: 10px; }
    .gst { display: inline-flex; align-items: center; gap: 6px; font-weight: 600; font-size: 14px; }
    .gst.in { color: #11823B; } .gst.out { color: #C3213F; } .gst.draft { height: 36px; padding: 0 12px; border-radius: 6px; background: var(--neutral05); color: var(--head); }
    .btn.exit { flex: none; height: 44px; padding: 0 18px; background: #D93A55; color: var(--white); font-size: 15px; font-weight: 500; }
    .dctag { display: inline-flex; align-items: center; height: 26px; padding: 0 10px; border-radius: 4px; font-size: 13px; font-weight: 500; }
    .dctag.up { background: #C9F5D6; color: #11823B; } .dctag.pend { background: #FBD9D3; color: #C3213F; }
    button.dctag { min-height: 26px; }
    .seal { display: block; width: 60px; height: 60px; color: #11823B; transform: rotate(-10deg); opacity: .9; }
    .seal svg { width: 100%; height: 100%; }
    .gtsplit { min-height: 0; }
    .gtsplit .txlist { padding-bottom: 120px; }
    .gtsplit .gvc { padding: var(--sp-16); gap: var(--sp-12); align-items: flex-start; cursor: pointer; border: 2px solid transparent; }
    .gtsplit .gvc[aria-current="true"] { border-color: var(--md3-on-primary-container); }
    .gtsplit .gvc__ln { gap: 4px 12px; }
    .gtsplit .gvc .seal { width: 48px; height: 48px; }
    .gtsplit .btn.exit { height: 40px; padding: 0 14px; font-size: 14px; }
    .gtdh { background: var(--md3-on-primary-container); }
    .gtdh h3 { font-size: 20px; }
    .gtdh__m { display: flex; flex-wrap: wrap; gap: 8px; }
    .gtdh__m > span { display: inline-flex; align-items: center; gap: 6px; height: 30px; padding: 0 10px; border-radius: 6px; background: rgba(255,255,255,.14); color: var(--white); }
    .gtdh__m b { font-weight: 600; font-size: 14px; }
    .gchip { justify-self: start; display: inline-flex; align-items: center; gap: 6px; height: 26px; padding: 0 10px; border-radius: 6px; font-size: 13px; font-weight: 600; }
    .gchip.in { background: #C9F5D6; color: #11823B; } .gchip.out { background: #FBD9D3; color: #C3213F; } .gchip.draft { background: rgba(255,255,255,.85); color: var(--head); }
    .gfl { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px var(--sp-16); padding: 4px var(--sp-20) var(--sp-12); }
    .gfl.two { grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 0; }
    .gfl div { display: grid; gap: 2px; min-width: 0; }
    .gfl small { color: var(--ink); font-size: 12px; }
    .gfl b { color: var(--head); font-weight: 500; font-size: 16px; overflow-wrap: anywhere; }
    .gfl .nil { color: var(--md3-neutral-secondary); font-weight: 400; }
    .gthumbs { display: flex; flex-wrap: wrap; align-items: center; gap: 10px; padding: 0 var(--sp-20) var(--sp-16); }
    .gsecs > .txsec { margin-top: var(--sp-8); padding-top: var(--sp-16); }
    .gsecs > .txsec ~ .txsec { border-top: 1px solid var(--md3-surface-variant); }
    .gsecs .txsec .cnt { display: inline-grid; place-items: center; min-width: 24px; height: 22px; padding: 0 7px; border-radius: 11px; background: var(--neutral05); color: var(--ink); font-size: 12px; font-weight: 600; }
    .gsecs .txcom { padding-bottom: var(--sp-24); }
    .gthumb { width: 64px; height: 64px; border-radius: var(--radius); display: grid; place-items: center; background: linear-gradient(135deg, #C9DCD5, #9DBDB2); color: rgba(255,255,255,.95); }
    .gthumb.sec { background: linear-gradient(135deg, #D7E3EA, #AFC3CF); }
    .gthumb.doc { background: linear-gradient(135deg, #E8EEF2, #C7D3DB); color: var(--md3-on-primary-container); }
    .gaddph { width: 64px; height: 64px; display: grid; place-items: center; align-content: center; gap: 2px; border-radius: var(--radius); border: 1px dashed var(--md3-outline-variant); background: var(--white); color: var(--md3-on-primary-container); font-size: 12px; font-weight: 500; }
    @media (hover: hover) { .gaddph:hover { border-color: var(--md3-on-primary-container); background: var(--md3-displaybg-primary); } }
    .gaddph svg.si { color: var(--md3-on-primary-container); }
    .txsec .gedit { width: 44px; height: 44px; color: var(--md3-on-primary-container); }
    .txsec .gadd { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; color: var(--md3-on-surface); font-weight: 600; }
    .txsec .cnt { display: inline-grid; place-items: center; min-width: 24px; height: 22px; margin-left: 6px; padding: 0 7px; border-radius: 11px; background: var(--neutral05); color: var(--ink); font-size: 12px; font-weight: 600; vertical-align: middle; }
    .gacc { display: grid; gap: 10px; padding: 0 var(--sp-20) var(--sp-16); }
    .gacc__i { border-radius: var(--radius); border: 1px solid var(--md3-surface-variant); background: var(--white); overflow: hidden; }
    .gacc__i.open { border-color: var(--md3-outline-variant); background: var(--md3-background); }
    .gacc__h { display: flex; align-items: center; gap: 12px; width: 100%; min-height: 56px; padding: 8px 14px; text-align: left; color: var(--head); }
    .gacc__h svg.si { flex: none; color: var(--md3-neutral-secondary); transition: transform 200ms var(--ease); }
    .gacc__i.open .gacc__h svg.si { transform: rotate(180deg); }
    .gacc__n { flex: none; color: var(--ink); font-size: 13px; font-weight: 500; }
    .gacc__h b { font-size: 15px; font-weight: 600; }
    .gacc__m { flex: 1; min-width: 0; text-align: right; color: var(--md3-neutral-secondary); font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .gacc__b { border-top: 1px solid var(--md3-surface-variant); padding-top: 12px; }
    .gacc__b .gfl { padding: 0 14px 12px; }
    .gacc__b .gthumbs { padding: 0 14px 12px; }
    .gacc__a { display: flex; gap: 8px; justify-content: flex-end; padding: 0 8px 6px; }
    .gacc__a .linkbtn { display: inline-flex; align-items: center; gap: 6px; min-height: 44px; padding: 0 10px; color: var(--md3-on-primary-container); font-weight: 500; }
    .gacc__a .gdelt { color: #C3213F; }
    .gvch { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; padding: 0 14px 12px; }
    .gvch small { width: 100%; color: var(--ink); font-size: 12px; }
    .gvch .spchip { height: 36px; }
    .gvch .nil { color: var(--md3-neutral-secondary); }
    .gdig { display: inline-flex; align-items: center; height: 22px; padding: 0 8px; margin-right: 8px; border-radius: 11px; background: #E3F8EA; color: #11823B; font-size: 12px; font-weight: 600; }
    .glines { display: grid; gap: 8px; margin: 0 14px 12px; }
    .gl__r { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 1.6fr); gap: 8px; }
    .gl__r > span { display: grid; align-content: center; padding: 12px 14px; border-radius: var(--radius); background: var(--white); color: var(--md3-on-primary-container); }
    .gl__q { grid-template-columns: .8fr 1fr 1.1fr; align-items: center; gap: 8px; }
    .gl__h > span { background: var(--md3-on-primary-container); color: var(--white); font-size: 13px; font-weight: 600; padding: 12px 14px; }
    .gl__h .gl__q span { color: var(--white); }
    .gl__i b { font-weight: 500; }
    .gl__i small { color: var(--ink); font-size: 13px; }
    .gl__r.bad > span { background: #FCF3F4; }
    .gl__r.bad .gl__i b { color: #4D0A1F; }
    .gl__ret { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; margin-top: 6px; color: #C3213F; font-size: 14px; }
    .tag.ret { background: #FBD9DE; color: #C3213F; height: 24px; }
    .gl__c { color: var(--md3-on-primary-container); }
    .gcond { display: inline-flex; align-items: center; height: 24px; padding: 0 8px; border-radius: 6px; font-size: 12px; font-weight: 600; }
    .gcond.good { background: #E3F8EA; color: #11823B; } .gcond.damaged { background: #FBE3E7; color: #C3213F; } .gcond.short { background: #FFF3D6; color: #8A5A00; }
    .gexp { display: inline-flex; align-items: center; height: 24px; padding: 0 8px; border-radius: 6px; background: var(--neutral05); color: var(--ink); font-size: 12px; }
    .gwait { display: flex; align-items: flex-start; gap: 8px; margin: 0 14px 12px; padding: 10px 12px; border-radius: var(--radius); background: var(--white); border: 1px dashed var(--md3-outline-variant); color: var(--ink); }
    .gwait svg.si { margin-top: 2px; color: var(--md3-on-primary-container); }
    .gvrow { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
    .gvrow small { width: 100%; color: rgba(255,255,255,.75); font-size: 12px; }
    .gvrow > span { display: inline-flex; align-items: center; height: 28px; padding: 0 10px; border-radius: 6px; background: rgba(255,255,255,.14); color: var(--white); font-size: 13px; }
    .gplus { display: inline-flex; align-items: center; height: 22px; padding: 0 8px; margin-left: 4px; border-radius: 11px; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); font-size: 12px; font-weight: 600; vertical-align: middle; font-variant-numeric: normal; }
    .gplus.ok { background: #E3F8EA; color: #11823B; } .gplus.wait { background: #FFF3D6; color: #8A5A00; }
    .gchal { margin: 0 var(--sp-20) var(--sp-12); padding: var(--sp-12) var(--sp-16) 0; border-radius: var(--radius); background: var(--md3-background); }
    .gchal .gthumbs { padding: var(--sp-12) 0 var(--sp-12); }
    .gchal__h { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
    .gnum { width: 24px; height: 24px; border-radius: 50%; display: grid; place-items: center; background: var(--md3-on-primary-container); color: var(--white); font-size: 12px; font-weight: 600; }
    .gdel { width: 40px; height: 40px; color: #C3213F; }
    .gchal__h b { color: var(--head); }
    .gchal__h .grow { flex: 1; }
    .gnote { padding: 0 var(--sp-20) var(--sp-16); color: var(--ink); }
    .txdet .dcdrop { margin: 0 var(--sp-20) var(--sp-16); width: calc(100% - 40px); min-height: 104px; background: var(--md3-background); border-color: var(--md3-outline-variant); color: var(--md3-on-primary-container); }
    .txdet .dcdrop small { color: var(--md3-neutral-secondary); }
    .gdcok { display: flex; align-items: center; gap: var(--sp-16); margin: 0 var(--sp-20) var(--sp-16); padding: var(--sp-12) var(--sp-16); border-radius: var(--radius); background: #EAFBEF; }
    .gdcok .seal { width: 48px; height: 48px; }
    .gdcok .grow { flex: 1; display: grid; gap: 2px; } .gdcok b { color: var(--head); } .gdcok small { color: #11823B; }
    .gsteps { padding: 4px var(--sp-20) var(--sp-8); }
    .gsec { display: flex; align-items: center; gap: var(--sp-12); padding: 0 var(--sp-20) var(--sp-12); }
    .gsec .grow { flex: 1; min-width: 160px; display: grid; gap: 2px; } .gsec b { color: var(--head); } .gsec small { color: var(--ink); }
    .gsec .gthumbs { padding: 0; }
    .txfoot .sheet__f .btn { height: 56px; }
    /* the + button lives over the list, never over the detail footer */
    @media (orientation: landscape) { .gfab { right: auto; left: calc(min(400px, 100vw) - 88px); } #gmenu ul { right: auto; left: calc(min(400px, 100vw) - 28px); transform: translateX(-100%); justify-items: end; } }
    @media (orientation: portrait) { .gfab.hide-p { display: none; } .gtpanel.det .txtabs { display: none; } }   /* a vehicle open full width: no list tabs */
    @media (orientation: portrait) { .gfl { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    .ginputs { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px var(--sp-12); padding: 0 14px 12px; }
    .ginputs.one { grid-template-columns: minmax(0, 1fr); }
    .ginputs.gpad { padding: 0 var(--sp-20) var(--sp-12); }
    @media (orientation: portrait) { .ginputs { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
    .gin { display: grid; gap: 6px; min-width: 0; }
    .gin > span { color: var(--ink); font-size: 13px; }
    .gin > span i { color: #C3213F; font-style: normal; }
    .gin input { height: 48px; padding: 0 12px; border-radius: var(--radius); border: 1px solid var(--md3-outline-variant); background: var(--white); color: var(--head); font: inherit; min-width: 0; }
    .gin input::placeholder { color: var(--md3-neutral-secondary); }
    .gin input:focus { outline: none; border-color: var(--md3-on-primary-container); box-shadow: 0 0 0 3px rgba(31,81,91,.12); }
    .gin.bad input { border-color: #C3213F; background: #FFF8F9; }
    .gin small { color: #C3213F; font-size: 12px; }
    .gin.ro b { display: flex; align-items: center; height: 48px; padding: 0 12px; border-radius: var(--radius); background: var(--neutral05); color: var(--ink); font-weight: 400; }
    .gacc__i.err { border-color: #E9A3AF; }
    .gin.ro.now b { background: #FBE3E7; color: #C3213F; font-weight: 500; }
    .gnform > .gnfull { margin: 0 var(--sp-20) var(--sp-16) !important; width: calc(100% - 40px) !important; }
    .gerr { color: #C3213F; font-weight: 500; }
    .gnform .gacc__h b { color: var(--head); }
    .gndrop { margin: 0 14px 12px !important; width: calc(100% - 28px) !important; min-height: 96px !important; }
    .gnform > .gndrop { margin: 0 var(--sp-20) var(--sp-16) !important; width: calc(100% - 40px) !important; }
    .gthumb { position: relative; }
    .gthx { position: absolute; top: -8px; right: -8px; width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center; background: var(--head); color: var(--white); box-shadow: 0 0 0 2px var(--white); }
    .gthx svg { width: 14px; height: 14px; }
    .btn.dark[aria-disabled="true"] { background: var(--md3-surface-variant); color: var(--md3-neutral-secondary); }
    .gfab { position: fixed; right: 28px; bottom: 28px; z-index: 22; width: 60px; height: 60px; border-radius: 50%; display: grid; place-items: center; background: var(--md3-primary); color: var(--white); box-shadow: 0 6px 18px rgba(31,65,91,.25); transition: transform 160ms var(--ease); }
    .gfab svg { fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linecap: round; }
    .gfab[aria-expanded="true"] { transform: rotate(45deg); background: var(--md3-on-primary-container); }
    .gmenu { position: fixed; inset: 0; z-index: 21; background: rgba(0,0,0,.45); }
    .gmenu[hidden] { display: none; }
    .gmenu ul { position: absolute; right: 28px; bottom: 104px; list-style: none; display: grid; justify-items: end; gap: 14px; }
    .gmenu button { display: flex; align-items: center; gap: 16px; min-height: 64px; padding: 6px 6px 6px 28px; border-radius: 32px; background: var(--white); color: var(--head); font-size: 18px; font-weight: 500; box-shadow: 0 4px 14px rgba(0,0,0,.18); }
    .gmenu button span:last-child { width: 52px; height: 52px; border-radius: 50%; display: grid; place-items: center; background: #C9F5D6; color: var(--md3-on-primary-container); }
    .gmenu button:active { transform: scale(.98); }
    .toast { bottom: auto; top: 96px; transform: translate(-50%, -16px); }   /* clear of sheet buttons and the + button */
    .toast.on { transform: translate(-50%, 0); }
    .gpick { display: grid; gap: 8px; max-height: 44dvh; overflow-y: auto; }
    .gpick button { display: flex; align-items: center; gap: 12px; min-height: 60px; padding: 8px 14px; border-radius: var(--radius); border: 1px solid var(--md3-outline-variant); background: var(--white); text-align: left; width: 100%; }
    .gpick button[aria-pressed="true"] { border-color: var(--md3-on-primary-container); background: var(--md3-displaybg-primary); }
    .gpick .grow { flex: 1; min-width: 0; display: grid; }
    .gpick b { color: var(--head); } .gpick small { color: var(--ink); }
    .dcdrop { display: grid; place-items: center; gap: 6px; min-height: 120px; padding: var(--sp-16); border-radius: var(--radius); border: 1px dashed var(--md3-outline-variant); background: var(--md3-background); color: var(--ink); text-align: center; width: 100%; }
    .dcdrop.done { border-style: solid; border-color: #11823B; background: #EAFBEF; color: #11823B; }
    .dcdrop svg { width: 32px; height: 32px; }
"""

GATE_HTML = '''  <div class="ddrawer" id="ddrawer" hidden role="dialog" aria-modal="true" aria-label="Vehicle detail"><div class="ddrawer__p"></div></div>
  <div class="dpanel gtpanel" id="gtpanel" hidden role="dialog" aria-modal="true" aria-labelledby="gtT"></div>
  <button type="button" class="gfab" id="gfab" hidden aria-label="Gate actions" aria-expanded="false" aria-controls="gmenu"><svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></button>
  <div class="gmenu" id="gmenu" hidden><ul><li><button type="button" data-gact="entry"><span>Log Entry</span><span><svg class="si" width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M13 4h5a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1h-5M4 12h10M11 9l3 3-3 3"/></svg></span></button></li>
    <li><button type="button" data-gact="exit"><span>Log Exit</span><span><svg class="si" width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M11 4H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h5M10 12h10M17 9l3 3-3 3"/></svg></span></button></li>
    <li><button type="button" data-gact="dc"><span>Upload Sealed DC</span><span><svg class="si" width="26" height="26" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 15h6M9 18h4"/></svg></span></button></li></ul></div>'''

GATE_JS = r"""  /* ---------------- Security: gate screen ---------------- */
  var GT_KEY = 'antz.security.gate', GT = (function () { var s = lsGet(GT_KEY); var g = s && s.v === CFG_V ? s : { v: CFG_V, add: [], ov: {} }; g.seq = g.seq || 0; return g; })();
  function gtSave() { lsSet(GT_KEY, GT); }
  var GTQ = '', GTDC = '', GTCUR = null, GTSEL = '';
  var SV = { pin: '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>', bld: '<rect x="4" y="3" width="10" height="18" rx="1"/><path d="M14 9h6v12h-6M7 7h4M7 11h4M7 15h4"/>',
    door: '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M12 3v18M9.5 12h.01M14.5 12h.01"/>', pen: '<path d="M4 20l1-4L16 5l3 3L8 19z"/>', qr: '<path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h2v2h-2zM18 18h2v2h-2zM14 18h2M18 14h2"/>',
    sliders: '<path d="M4 7h10M18 7h2M4 17h4M12 17h8"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="17" r="2"/>', loc: '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>',
    outi: '<path d="M11 4H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h5M10 12h10M17 9l3 3-3 3"/>', badge: '<path d="M12 3l2.2 1.6 2.7-.2.9 2.6 2.3 1.4-.8 2.6.8 2.6-2.3 1.4-.9 2.6-2.7-.2L12 21l-2.2-1.6-2.7.2-.9-2.6-2.3-1.4.8-2.6-.8-2.6 2.3-1.4.9-2.6 2.7.2z"/><path d="m9 12 2 2 4-4"/>',
    upload: '<path d="M12 16V4M7 9l5-5 5 5M5 20h14"/>', undo: '<path d="M9 14 4 9l5-5"/><path d="M4 9h10a6 6 0 0 1 0 12h-2"/>', timer: '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2M9.5 2.5h5"/>', truck: '<path d="M3 6h11v10H3zM14 9h4l3 3v4h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>', cam: '<rect x="3" y="6" width="18" height="14" rx="2"/><circle cx="12" cy="13" r="3.5"/><path d="M8.5 6 10 3.5h4L15.5 6"/>', chev: '<path d="m6 9 6 6 6-6"/>' };
  var SEAL = '<span class="seal" role="img" aria-label="Sealed DC uploaded"><svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="29" fill="none" stroke="currentColor" stroke-width="2.5"/><circle cx="32" cy="32" r="23.5" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2.2 2.2"/>' +
    '<path d="m24 27 5.5 5.5 10.5-11" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><text x="32" y="44.5" text-anchor="middle" font-size="6.8" font-weight="700" letter-spacing="1" fill="currentColor" font-family="Inter, system-ui, sans-serif">SEALED</text></svg></span>';
  function sv(k, s) { return '<svg class="si" width="' + (s || 18) + '" height="' + (s || 18) + '" viewBox="0 0 24 24" aria-hidden="true">' + SV[k] + '</svg>'; }
  function dtl(iso) { var p = iso.split(/[-T:]/).map(Number), h = p[3] % 12 || 12; return p[2] + ' ' + MON[p[1] - 1] + ', ' + h + ':' + ('0' + p[4]).slice(-2) + (p[3] < 12 ? ' AM' : ' PM'); }
  /* a gate's visits: today and yesterday, plus anything security logged here; state is checked-in, draft or checked-out */
  /* the gate screen shows exactly the QA cases (user list, 8 Oct): checked in, not processed and processed, and
     checked out without and with the sealed DC, each for 1v1c, 1v2c, 2v2c and 2v1c (vehicles v, challans c). SAMPLE DATA */
  var GSC = [['in', 0, 1, 1], ['in', 0, 1, 2], ['in', 0, 2, 2], ['in', 0, 2, 1], ['in', 1, 1, 1], ['in', 1, 1, 2], ['in', 1, 2, 2], ['in', 1, 2, 1],
    ['out', 0, 1, 1], ['out', 0, 1, 2], ['out', 0, 2, 2], ['out', 0, 2, 1], ['out', 1, 1, 1], ['out', 1, 1, 2], ['out', 1, 2, 2], ['out', 1, 2, 1]];
  var GVEN = ['Jamnagar Fresh Farms', 'Saurashtra Meat Suppliers', 'AquaLive Feeders', 'GreenLeaf Fodder Co-op', 'Coastal Cold Chain', 'Patel Grain Traders', 'Shree Gas Agency', 'City Linen Services'];
  var GDRV2 = ['Hitesh Parmar', 'Imran Shaikh', 'Prakash Menon', 'Devji Bhai', 'Suresh Rana', 'Nitin Bhatt', 'Kalpesh Joshi', 'Bharat Solanki'];
  var GSCV = {};
  function gtScen(g) {
    if (GSCV[g.id]) return GSCV[g.id];
    var gi = Number(g.id.replace(/\D/g, '')) || 1, L = 'ABCDEFGHKMNPRTXY', p2 = function (n) { return ('0' + n).slice(-2); };
    return (GSCV[g.id] = GSC.map(function (c, k) {
      var n = gi * 31 + k * 7, plate = 'GJ-' + ['10', '03', '12', '01'][n % 4] + '-' + L[n % 16] + L[(n * 3) % 16] + '-' + (1000 + (n * 137) % 9000);
      var inMin = c[0] === 'in' ? (c[1] ? 600 + k * 35 : 920 + k * 4) : 480 + (k - 8) * 25, inAt = '2026-09-30T' + p2(Math.floor(inMin / 60)) + ':' + p2(inMin % 60), outMin = inMin + 45 + (k % 3) * 20;
      var v = { id: 'GS-' + g.id + '-' + (k + 1), gate: g.id, state: c[0] === 'in' ? 'INSIDE' : 'EXITED', vehicleNo: plate, vendor: GVEN[k % GVEN.length], driver: GDRV2[k % GDRV2.length], enteredAt: inAt,
        challanNo: 'DC-' + ['JFF', 'SMS', 'AQL', 'GLF', 'CCC', 'PGT', 'SGA', 'CLS'][k % 8] + '-' + (4400 + gi * 50 + k), lines: 3, scen: { st: c[0], proc: c[0] === 'out' ? true : !!c[1], seal: c[0] === 'out' && !!c[1], nv: c[2], nc: c[3], k: k } };
      if (c[0] === 'out') { v.exitedAt = '2026-09-30T' + p2(Math.floor(outMin / 60)) + ':' + p2(outMin % 60); v.exitGate = g.id; v.exitChallan = !!c[1]; }
      return v;
    }));
  }
  function gtVisits(g) {
    return gtScen(g).concat(GT.add.filter(function (v) { return v.gate === g.id; })).map(gtMap)
      .sort(function (a, b) { var ka = a.outAt || a.inAt || a.editAt, kb = b.outAt || b.inAt || b.editAt; return ka === kb ? b.seq - a.seq : ka < kb ? 1 : -1; });
  }
  function gtTabs(g) { var t = ['all'], c = gTabs(g); if (c.indexOf('entry') !== -1) t.push('in'); if (c.indexOf('exit') !== -1) t.push('out'); return t; }
  var GTL = { all: 'All', in: 'Checked in', out: 'Checked out' };
  function gtCard(x, b, g) {
    var where = '<span>' + sv('loc') + esc(b.name) + ' • ' + esc(gname(x.v.gate)) + '</span>', side = '', lines = '';
    if (x.st === 'in') { lines = '<span><span class="mk fr"></span>In ' + dtl(x.inAt) + '</span>'; side = '<span class="gst in">' + sv('loc', 16) + 'Checked-in</span><button type="button" class="btn exit" data-gexit="' + x.id + '">Record Exit</button>'; }
    else if (x.st === 'draft') { lines = '<span>' + sv('pen', 16) + 'Edited ' + dtl(x.editAt) + '</span>'; side = '<span class="gst draft">' + sv('pen', 16) + 'Draft</span>'; }
    else { lines = '<span><span class="mk fr"></span>In ' + dtl(x.inAt) + '</span><span><span class="mk to"></span>Out ' + dtl(x.outAt) + '</span>';
      side = '<span class="gst out">' + sv('outi', 16) + 'Checked-Out</span>' + (x.dc === 'up' ? SEAL : ''); }
    var dc = x.st === 'out' ? '<span class="gvc__ln"><span>' + sv('badge', 16) + '<b style="color:var(--head)">Sealed DC:</b>' + (x.dc === 'up' ? '<span class="dctag up">Uploaded</span>' : '<button type="button" class="dctag pend" data-gdc="' + x.id + '">Pending</button>') + '</span></span>' : '';
    return '<div class="gvc" role="link" tabindex="0" data-gopen="' + x.id + '" aria-current="' + (x.id === GTSEL) + '" aria-label="' + esc(x.vehicleNo) + ', ' + esc(x.vendor) + '"><span class="grow"><b class="gvc__no">' + esc(x.vehicleNo) + (function () { var en = gEnt(x); return (en.veh.length > 1 ? ' <span class="gplus">+' + (en.veh.length - 1) + ' vehicle' + (en.veh.length > 2 ? 's' : '') + '</span>' : '') + (en.chal.length > 1 ? ' <span class="gplus">' + en.chal.length + ' challans</span>' : '') + (x.st === 'in' && x.v.scen ? ' <span class="gplus ' + (x.v.scen.proc ? 'ok' : 'wait') + '">' + (x.v.scen.proc ? 'Processed' : 'Not processed') + '</span>' : ''); })() + '</b><span class="gvc__ln"><span class="ven">' + esc(x.vendor) + '</span>' + (x.challanNo ? '<span>DC ' + esc(x.challanNo) + '</span>' : '') + '</span><span class="gvc__ln">' + where + '</span><span class="gvc__ln">' + lines + '</span>' + dc + '</span><span class="gvc__side">' + side + '</span></div>';
  }
  /* ---- vehicle detail (same parts as the transfer detail: coloured header, label/value rows, sections, status footer) ---- */
  function addMin(iso, m) { var p = iso.split(/[-T:]/).map(Number), t = p[3] * 60 + p[4] + m, h = Math.floor(t / 60), mm = t % 60; return iso.slice(0, 11) + ('0' + Math.min(h, 23)).slice(-2) + ':' + ('0' + mm).slice(-2); }
  function phone(id) { var n = String(id).replace(/\D/g, '') || '7'; return '+91 98' + ('0000000' + (Number(n) * 7919 % 100000000)).slice(-8).replace(/(\d{3})(\d{5})/, '$1 $2'); }
  /* one gate entry can carry several vehicles and several challans, linked both ways:
     one vehicle with several challans, one challan split across several vehicles, or a mix. SAMPLE DATA picks a case per visit. */
  var GITEMS = ['Tomato, 40 kg', 'Onion, 25 kg', 'Carrot, 18 kg', 'Chicken, 30 kg', 'Fish, 12 kg', 'Rice, 50 kg', 'Banana, 22 kg', 'Spinach, 9 kg'];
  var GDRV = ['Sunil Patel', 'Rakesh Jadeja', 'Mohan Lal', 'Vijay Rathod'];
  var GOPEN = { id: '', v: 0, c: 0 }, GANCH = null;
  /* digitised challan lines (Receiving reads the DC at the kiosk): the matched master item, the DC wording, qty, condition, expiry. SAMPLE DATA */
  var GCAT = [['Tomato (Hybrid)', 'Tomato', 'kg'], ['Onion (Red)', 'Onion', 'kg'], ['Carrot (Ooty)', 'Carrot', 'kg'], ['Chicken, broiler whole', 'Chicken', 'kg'], ['Rohu fish', 'Fish', 'kg'], ['Rice (Sona Masoori)', 'Rice', 'kg'], ['Banana (Robusta)', 'Banana', 'doz'], ['Spinach (Palak)', 'Palak', 'bunch'], ['Apple (Shimla)', 'Apple', 'kg'], ['Papaya', 'Papaya', 'nos']];
  function gLines(c, ci, x) {
    if (c.lines) return c.lines;
    var n = (Number(String(x.id).replace(/\D/g, '')) || 1) + ci * 7, k = 2 + n % 3, out = [];
    /* line 1 is what the challan says (e.g. "Fish, 12 kg" becomes Rohu fish 12 kg); the rest come from the DC */
    var w = String(c.items || '').split(/[ ,(]/)[0].toLowerCase(), m = String(c.items || '').match(/(\d+)\s*kg/), b0 = 0;
    GCAT.forEach(function (g, gi) { if (g[1].toLowerCase() === w || g[0].toLowerCase().indexOf(w) === 0) b0 = gi; });
    for (var i = 0; i < k; i++) { var it = i === 0 ? GCAT[b0] : GCAT[(b0 + i * 3) % GCAT.length], q = i === 0 && m ? Number(m[1]) : 5 + (n * (i + 3)) % 46, cond = (n + i) % 9 === 0 ? 'Damaged' : (n + i) % 7 === 0 ? 'Short' : 'Good';
      if (x.v && x.v.scen) cond = c.dmg && i === k - 1 ? 'Damaged' : 'Good';
      out.push({ item: it[0], dc: it[1], qty: q + ' ' + it[2], cond: cond, ret: cond === 'Damaged' ? (2 + n % 4) + ' ' + it[2] : '', exp: ('0' + (2 + (n + i * 5) % 26)).slice(-2) + '/10/2026' }); }
    return out;
  }
  function gEnt(x) {
    var o = GT.ov[x.id] || {}; if (o.ent) return JSON.parse(JSON.stringify(o.ent));
    var n = Number(String(x.id).replace(/\D/g, '')) || 1, sc = x.id === 'GV-9004' ? 2 : n % 4, L = 'ABCDEFGHKMNPRTXY', S = x.v && x.v.scen;
    var plate = function (k) { return 'GJ-' + ['10', '03', '12'][(n + k) % 3] + '-' + L[(n * 3 + k) % 16] + L[(n + k * 5) % 16] + '-' + (1000 + (n * 37 + k * 911) % 9000); };
    var veh = [{ no: x.vehicleNo, driver: x.driver, vendor: x.vendor, ph: x.st === 'draft' ? 0 : 2 }], chal = [];
    var item = function (k) { return GITEMS[(n + k) % GITEMS.length]; };
    if (!x.challanNo) return { veh: veh, chal: chal };
    if (S) {   /* QA cases: v vehicles, c challans; with 2 and 2 each vehicle has its own challan, with 2 and 1 the challan is split */
      if (S.nv === 2) veh.push({ no: plate(1), driver: GDRV[n % 4], vendor: x.vendor, ph: 1 });
      var dmg = (S.st === 'in' && S.proc && S.nv === 1 && S.nc === 2) || (S.st === 'out' && !S.seal && S.nv === 2 && S.nc === 2) || (S.st === 'out' && S.seal && S.nv === 1 && S.nc === 1);
      chal.push({ no: x.challanNo, items: item(0), ph: 1, veh: S.nv === 2 && S.nc === 1 ? [0, 1] : [0], dmg: dmg && S.nc === 1 });
      if (S.nc === 2) chal.push({ no: x.challanNo + '-B', items: item(1), ph: 1, veh: [S.nv === 2 ? 1 : 0], dmg: dmg });
      return { veh: veh, chal: chal };
    }
    if (sc === 0) {          /* one challan, several vehicles */
      veh.push({ no: plate(1), driver: GDRV[n % 4], vendor: x.vendor, ph: 1 }, { no: plate(2), driver: GDRV[(n + 1) % 4], vendor: x.vendor, ph: 1 });
      chal.push({ no: x.challanNo, items: item(0) + ' (split load)', ph: 1, veh: [0, 1, 2] });
    } else if (sc === 1) {   /* one vehicle, several challans */
      chal.push({ no: x.challanNo, items: item(0), ph: 1, veh: [0] }, { no: x.challanNo + '-B', items: item(1), ph: 1, veh: [0] }, { no: x.challanNo + '-C', items: item(2), ph: 0, veh: [0] });
    } else if (sc === 2) {   /* a mix: two vehicles, one challan on both, one on the second */
      veh.push({ no: plate(1), driver: GDRV[n % 4], vendor: x.vendor, ph: 1 });
      chal.push({ no: x.challanNo, items: item(0), ph: 1, veh: [0, 1] }, { no: x.challanNo + '-B', items: item(3), ph: 1, veh: [1] });
    } else chal.push({ no: x.challanNo, items: (x.v.lines || 1) + (x.v.lines === 1 ? ' line' : ' lines'), ph: 1, veh: [0] });
    return { veh: veh, chal: chal };
  }
  function gEntSave(x, ent) { var o = GT.ov[x.id] = GT.ov[x.id] || {}; o.ent = ent; o.vehicleNo = ent.veh[0].no; o.vendor = ent.veh[0].vendor || o.vendor; o.driver = ent.veh[0].driver; o.challanNo = ent.chal[0] ? ent.chal[0].no : ''; gtSave(); }
  function plural2(n, w) { return n + ' ' + w + (n === 1 ? '' : 's'); }
  function vehSheet(i) {
    var x = gfind(GTSEL), ent = gEnt(x), v = i == null ? { vendor: x.vendor } : ent.veh[i];
    sheet2(sheetHead(i == null ? 'Add vehicle' : 'Edit vehicle ' + (i + 1), esc(x.vendor) + ' · ' + esc(GTCUR.g.name)) + '<form class="fgrid" data-gvehf="' + (i == null ? '' : i) + '">' + field('Vehicle number*', 'vno', v.no, 'e.g. GJ-10-AB-1234') + '<div class="fcols">' + field('Driver name', 'drv', v.driver, 'Name') + field('Vendor', 'ven', v.vendor, 'Company') + '</div><p class="ferr" hidden></p>' +
      '<div class="sheet__f"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">' + (i == null ? 'Add vehicle' : 'Save') + '</button></div></form>');
  }
  function chalSheet() {
    var x = gfind(GTSEL), ent = gEnt(x);
    sheet2(sheetHead('Add challan', esc(x.vendor)) + '<form class="fgrid" data-gchalf>' + field('Challan number*', 'no', '', 'e.g. DC-JFF-4488') + field('Challan items*', 'items', '', 'e.g. Tomato, 40 kg') +
      '<div class="sheet__g"><h3 class="t-minor-medium">Vehicles carrying this challan</h3><div class="pchips">' + ent.veh.map(function (v, i) { return '<label class="pchip t-body-medium"><input type="checkbox" name="cv" value="' + i + '" checked>' + esc(v.no) + '</label>'; }).join('') + '</div></div>' +
      '<p class="ferr" hidden></p><div class="sheet__f"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">Add challan</button></div></form>');
  }
  /* ---- Security Admin: vehicle detail drawer (read only, the same detail security sees) ---- */
  var GRO = false;
  function gtMap(v) {
    var o = GT.ov[v.id] || {}, st = o.st || (v.state === 'EXITED' ? 'out' : v.state === 'AT_GATE' ? 'draft' : v.state === 'DRAFT' ? 'draft' : v.state === 'UPCOMING' ? 'up' : 'in');
    return { id: v.id, v: v, st: st, vehicleNo: o.vehicleNo || v.vehicleNo, vendor: o.vendor || v.vendor, challanNo: o.challanNo || v.challanNo || '', driver: o.driver || v.driver || '',
      inAt: o.inAt || v.enteredAt || '', outAt: o.outAt || v.exitedAt || '', editAt: o.editAt || v.atGateAt || v.enteredAt || '', dc: o.dc || (v.state === 'EXITED' ? (v.exitChallan ? 'up' : 'pend') : ''), seq: o.seq || 0 };
  }
  var DRID = '';
  function drawerOpen(id, anim) {
    var v = VISITS.filter(function (q) { return q.id === id; })[0]; if (!v) return; DRID = id;
    var x = gtMap(v), g = sby(SD.gates, v.gate), b = sby(SD.buildings, v.bld), D = document.getElementById('ddrawer'), body;
    if (x.st === 'up') {
      body = '<div class="txdh gtdh"><div class="txdh__r"><div class="grow"><span class="gchip draft">' + sv('timer', 14) + 'Expected</span><h3 id="ddT">' + esc(v.vendor) + '</h3><span class="gtdh__m"><span>' + sv('truck', 16) + '<b class="mono">' + esc(v.vehicleNo) + '</b></span><span>' + sv('door', 16) + esc(g.name || '') + '</span></span><span class="sub t-body-regular">Due ' + dt(v.eta) + '</span>' +
        (v.driver ? '<span class="txby">' + avi(v.driver) + esc(v.driver) + '</span>' : '') + '</div></div></div><div class="gsecs"><div class="txsec">' + sv('truck', 20) + '<span class="grow">Expected vehicle</span></div><div class="gfl" style="padding-bottom:16px">' +
        [['Vehicle number', v.vehicleNo], ['Driver name', v.driver], ['Vendor', v.vendor], ['Gate', g.name], ['Expected at', hm(v.eta)], ['Challan', v.challanNo ? v.challanNo + ' · ' + plural2(v.lines || 1, 'line') : '']].map(function (r) { return '<div><small>' + r[0] + '</small><b>' + (r[1] ? esc(r[1]) : '<span class="nil">Not shared yet</span>') + '</b></div>'; }).join('') + '</div>' +
        (v.note ? '<p class="gnote t-body-regular">' + esc(v.note) + '</p>' : '') + '<p class="gwait t-body-regular" style="margin:0 20px 20px">' + sv('timer', 16) + 'Not at the gate yet. Security logs the entry when it arrives.</p></div>';
      body = '<div class="txdb">' + body + '</div>';
    } else { GRO = true; body = gtDetail(x, g, b, 'all'); GRO = false; }
    D.querySelector('.ddrawer__p').innerHTML = '<div class="ddrawer__h"><b class="t-minor-title">' + esc(x.vehicleNo) + '</b><span class="t-body-regular">' + esc(g.name || '') + ' · ' + esc(b.name || '') + '</span><button type="button" class="iconbtn" data-ddclose aria-label="Close">' + ic('close', 24) + '</button></div><div class="ddrawer__b">' + body + '</div>';
    D.hidden = false; if (anim) { D.classList.remove('anim'); void D.offsetWidth; D.classList.add('anim'); }
  }
  function drawerClose() { var D = document.getElementById('ddrawer'); D.hidden = true; DRID = ''; }
  document.getElementById('ddrawer').addEventListener('click', function (e) {
    var b, D = this;
    if (e.target === D || e.target.closest('[data-ddclose]')) { drawerClose(); return; }
    if ((b = e.target.closest('[data-gvopen]'))) { var i = Number(b.getAttribute('data-gvopen')); GOPEN.v = GOPEN.v === i ? -1 : i; drawerOpen(DRID); return; }
    if ((b = e.target.closest('[data-gcopen]'))) { var j = Number(b.getAttribute('data-gcopen')); GOPEN.c = GOPEN.c === j ? -1 : j; drawerOpen(DRID); return; }
    if (e.target.closest('[data-txsteps]')) { TXTL = !TXTL; TXTLA = TXTL; drawerOpen(DRID); return; }
    if ((b = e.target.closest('[data-call]')) || (b = e.target.closest('[data-msg]'))) { toast((b.hasAttribute('data-call') ? 'Calling ' : 'Message to ') + (b.getAttribute('data-call') || b.getAttribute('data-msg')) + ' (demo)'); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !document.getElementById('ddrawer').hidden) { if (TXTL) { TXTL = false; drawerOpen(DRID); } else drawerClose(); e.stopImmediatePropagation(); } }, true);
  function gtDetail(x, g, b, cur) {
    var o = GT.ov[x.id] || {};
    var guard = o.guard || (!GRO && (x.st === 'in' || x.st === 'draft') ? VIEWER.name : 'Mahesh Rathod'), dcReady = o.dcReady, back = '#gates/' + g.id + '/' + cur;
    var stc = x.st === 'in' ? ['Checked-in', 'pend'] : x.st === 'draft' ? ['Draft', 'muted'] : ['Checked-out', 'done'];
    var head = '<div class="txdh gtdh"><div class="txdh__r"><div class="grow"><span class="gchip ' + x.st + '">' + (x.st === 'out' ? sv('outi', 14) : x.st === 'draft' ? sv('pen', 14) : sv('loc', 14)) + stc[0] + '</span>' +
      '<h3 id="txT">' + esc(x.vendor) + '</h3><span class="gtdh__m"><span>' + sv('truck', 16) + '<b class="mono">' + esc(x.vehicleNo) + '</b></span><span>' + sv('door', 16) + esc(gname(x.v.gate)) + '</span></span>' +
      (gEnt(x).veh.length > 1 ? '<span class="gvrow"><small>Vehicle entries</small>' + gEnt(x).veh.slice(0, 3).map(function (v) { return '<span class="mono">' + esc(v.no) + '</span>'; }).join('') + (gEnt(x).veh.length > 3 ? '<span>+' + (gEnt(x).veh.length - 3) + ' more</span>' : '') + '</span>' : '') + '<span class="sub t-body-regular">' + (x.inAt ? 'Entered ' + dt(x.inAt) : 'Not checked in yet') + (x.outAt ? ' · Left ' + hm(x.outAt) : '') + '</span>' +
      (x.driver ? '<span class="txby">' + avi(x.driver) + esc(x.driver) + '<button type="button" class="ricon" data-call="' + esc(x.driver) + '" aria-label="Call ' + esc(x.driver) + '">' + si('phone', 18) + '</button><button type="button" class="ricon" data-msg="' + esc(x.driver) + '" aria-label="Message ' + esc(x.driver) + '">' + si('chat', 18) + '</button></span>' : '') + '</div>' + QR + '</div></div>';
    var f = function (l, v) { return '<div><small>' + l + '</small><b>' + (v ? esc(v) : '<span class="nil">Not added</span>') + '</b></div>'; };
    var thumbs = function (n, kind, id) { var h = ''; for (var i = 0; i < n; i++) h += '<span class="gthumb ' + kind + '" role="img" aria-label="' + (kind === 'dc' ? 'Challan' : kind === 'sec' ? 'Guard' : 'Vehicle') + ' photo ' + (i + 1) + '">' + (kind === 'sec' ? si('user', 22) : si(kind === 'veh' ? 'image' : 'note', 22)) + '</span>'; return '<div class="gthumbs">' + h + (x.st === 'out' || GRO ? '' : '<button type="button" class="gaddph" data-gph="' + kind + '"' + (id != null ? ' data-i="' + id + '"' : '') + ' aria-label="Add photo">' + sv('cam', 20) + '<span>Add</span></button>') + '</div>'; };
    var ent = gEnt(x), chal = ent.chal, ro = x.st === 'out' || GRO, digi = x.v && x.v.scen ? x.v.scen.proc : x.st === 'out' || (x.st === 'in' && !!x.inAt && addMin(x.inAt, 12) <= '2026-09-30T15:42');
    if (GOPEN.id !== x.id) GOPEN = { id: x.id, v: 0, c: 0 };
    var vchal = function (vi) { return chal.filter(function (c) { return c.veh.indexOf(vi) !== -1; }).length; };
    var entry = '<div class="txsec">' + sv('truck', 20) + '<span class="grow">Vehicle entries <span class="cnt">' + ent.veh.length + '</span></span>' + (ro ? '' : '<button type="button" class="linkbtn t-body-medium gadd" data-gvadd>' + si('plus', 18) + 'Add vehicle</button>') + '</div>' +
      '<div class="gacc">' + ent.veh.map(function (v, i) { var open = GOPEN.v === i, nc = vchal(i);
        return '<div class="gacc__i' + (open ? ' open' : '') + '"><button type="button" class="gacc__h" data-gvopen="' + i + '" aria-expanded="' + open + '"><span class="gacc__n">Vehicle ' + (i + 1) + '</span><b class="mono">' + esc(v.no) + '</b><span class="gacc__m">' + plural2(nc, 'challan') + '</span>' + sv('chev', 20) + '</button>' +
          (open ? '<div class="gacc__b"><div class="gfl">' + f('Vehicle number', v.no) + f('Driver name', v.driver) + f('Driver phone', v.driver ? phone(x.id + i) : '') + f('Vendor', v.vendor) + f('Entry gate', x.inAt ? gname(x.v.gate) + ', ' + hm(x.inAt) : gname(x.v.gate)) + f('Exit gate', x.outAt ? gname(o.exitGate || x.v.exitGate || g.id) + ', ' + hm(x.outAt) : 'Decide at the gate') + '</div>' +
            '<div class="gvch"><small>Challans on this vehicle</small>' + (nc ? chal.map(function (c, ci) { return c.veh.indexOf(i) !== -1 ? '<span class="gtab">' + esc(c.no) + '</span>' : ''; }).join('') : '<span class="nil t-body-regular">None yet</span>') + '</div>' +
            thumbs(v.ph || 0, 'veh', i) + (ro ? '' : '<div class="gacc__a"><button type="button" class="linkbtn t-body-medium" data-gvedit="' + i + '">' + sv('pen', 16) + 'Edit</button>' + (ent.veh.length > 1 ? '<button type="button" class="linkbtn t-body-medium gdelt" data-gvdel="' + i + '">' + si('bin', 16) + 'Remove</button>' : '') + '</div>') + '</div>' : '') + '</div>'; }).join('') + '</div>';
    var ch = '<div class="txsec">' + si('note', 20) + '<span class="grow">Challan details <span class="cnt">' + chal.length + '</span></span>' + (ro ? '' : '<button type="button" class="linkbtn t-body-medium gadd" data-gchal>' + si('plus', 18) + 'Add challan</button>') + '</div>' +
      (chal.length ? '<div class="gacc">' + chal.map(function (c, i) { var open = GOPEN.c === i;
        return '<div class="gacc__i' + (open ? ' open' : '') + '"><button type="button" class="gacc__h" data-gcopen="' + i + '" aria-expanded="' + open + '"><span class="gacc__n">Challan ' + (i + 1) + '</span><b class="mono">' + esc(c.no) + '</b><span class="gacc__m">' + (digi ? '<span class="gdig">Digitised \u00b7 ' + plural2(gLines(c, i, x).length, 'line') + '</span>' : '') + (c.veh.length > 1 ? 'Split across ' + c.veh.length + ' vehicles' : 'On ' + esc(ent.veh[c.veh[0]] ? ent.veh[c.veh[0]].no : '')) + '</span>' + sv('chev', 20) + '</button>' +
          (open ? '<div class="gacc__b"><div class="gfl two">' + f('Challan number', c.no) + f('Challan items', c.items) + '</div>' +
            (digi ? '<div class="glines" role="table" aria-label="Challan items"><div class="gl__r gl__h" role="row"><span role="columnheader">Item</span><span class="gl__q"><span role="columnheader">Qty</span><span role="columnheader">Condition</span><span role="columnheader">Expiry</span></span></div>' + gLines(c, i, x).map(function (l) { var bad = l.cond !== 'Good';
              return '<div class="gl__r' + (bad ? ' bad' : '') + '" role="row"><span class="gl__i" role="cell"><b>' + esc(l.item) + '</b><small>On DC \u201c' + esc(l.dc) + '\u201d</small>' + (l.ret ? '<span class="gl__ret"><span class="tag ret">Returned</span>' + sv('undo', 14) + esc(l.ret) + ' returned</span>' : '') + '</span><span class="gl__q" role="cell"><span>' + esc(l.qty) + '</span><span class="gl__c">' + l.cond + '</span><span><span class="gexp">' + l.exp + '</span></span></span></div>'; }).join('') + '</div>'
              : '<p class="gwait t-body-regular">' + sv('timer', 16) + 'Waiting to be digitised. Receiving reads this challan at the kiosk and the lines show here.</p>') +
            '<div class="gvch"><small>Vehicles carrying this challan</small>' + ent.veh.map(function (v, vi) { var on = c.veh.indexOf(vi) !== -1; return ro ? (on ? '<span class="gtab">' + esc(v.no) + '</span>' : '') : '<button type="button" class="spchip t-body-medium" data-gcveh="' + i + '" data-vi="' + vi + '" aria-pressed="' + on + '">' + esc(v.no) + '</button>'; }).join('') + '</div>' +
            thumbs(c.ph || 0, 'dc', i) + (ro ? '' : '<div class="gacc__a"><button type="button" class="linkbtn t-body-medium gdelt" data-gcdel="' + i + '">' + si('bin', 16) + 'Delete challan</button></div>') + '</div>' : '') + '</div>'; }).join('') + '</div>'
        : '<p class="gnote t-body-regular">No challan yet. Add one for each delivery note the driver hands over.</p>');
    var dcDone = x.dc === 'up' || (x.st === 'in' && dcReady);
    var dc = '<div class="txsec">' + sv('badge', 20) + '<span class="grow">Sealed DC</span>' + (x.dc === 'up' ? '<span class="dctag up">Uploaded</span>' : x.st === 'out' ? '<span class="dctag pend">Pending</span>' : '') + '</div>' +
      (dcDone ? '<div class="gdcok">' + SEAL + '<span class="grow"><b class="t-body-medium">sealed-dc-photo.jpg</b><small class="t-body-regular">' + (x.dc === 'up' ? 'Uploaded' : 'Attached, saved when the exit is marked') + '</small></span></div>'
        : (GRO ? '<p class="gnote t-body-regular">No sealed DC yet.</p>' : x.st === 'draft' ? '<p class="gnote t-body-regular">Attach the sealed DC once the vehicle is checked in.</p>' : '<button type="button" class="dcdrop" data-gdcz>' + sv('cam', 30) + '<b class="t-body-medium">Take photo or upload image</b><small class="t-body-regular">JPEG or PNG, up to 50 MB</small></button>'));
    /* receiving sits inside the stay: started a third of the way in, completed just before the exit */
    var mins = function (iso) { var p = iso.split(/[-T:]/).map(Number); return Date.UTC(p[0], p[1] - 1, p[2], p[3], p[4]) / 60000; }, dwell = x.inAt && x.outAt ? mins(x.outAt) - mins(x.inAt) : 0;
    var rs = x.inAt ? (x.outAt ? addMin(x.inAt, Math.max(1, Math.round(dwell / 3))) : addMin(x.inAt, 12) <= '2026-09-30T15:42' ? addMin(x.inAt, 12) : '') : '';
    var tl = [['Entry marked', x.inAt], ['Receiving started', rs], ['Receiving completed', x.outAt ? addMin(x.outAt, -Math.max(1, Math.round(dwell / 6))) : ''], ['Exit marked', x.outAt]];
    var at = tl.filter(function (s) { return s[1]; }).length;
    var steps = '<div class="txsec">' + si('check', 20) + '<span class="grow">Timeline</span></div><ol class="txsteps gsteps">' + tl.map(function (s, i) { var cls = s[1] ? (i === at - 1 ? 'now done' : 'done') : 'next'; return '<li class="' + cls + '"><span class="dot">' + (s[1] && i < at - 1 ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" aria-hidden="true"><path d="m5 12 5 5 9-10"/></svg>' : '') + '</span><span><b>' + s[0] + '</b><small>' + (s[1] ? dt(s[1]) : 'Waiting') + '</small></span></li>'; }).join('') + '</ol>';
    var sec = '<div class="txsec">' + si('user', 20) + '<span class="grow">Security details</span></div><div class="gsec">' + avi(guard) + '<span class="grow"><b>' + esc(guard) + '</b><small class="t-body-regular">' + (x.st === 'out' ? 'Checked the vehicle out' : 'On duty at ' + esc(g.name)) + '</small></span></div>' + thumbs(o.sph == null ? 1 : o.sph, 'sec');
    /* comments, same as the transfer detail */
    var cms = o.comments || [];
    var com = '<div class="txsec">' + si('comment', 20) + '<span class="grow">Comments</span><span class="cnt">' + cms.length + '</span></div><div class="txcom">' + cms.map(function (c) { return '<div class="txcm">' + avi(c.by) + '<div><b>' + esc(c.by) + '</b> <small>' + dt(c.at) + '</small><p>' + esc(c.text) + '</p></div></div>'; }).join('') +
      (GRO ? '' : '<form data-gcom>' + avi(VIEWER.name).replace('class="av"', 'class="av" style="width:32px;height:32px;font-size:12px"') + '<input type="text" name="c" placeholder="Add a comment" aria-label="Add a comment" autocomplete="off"><button type="submit" class="send" aria-label="Send comment"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 20.5 21 12 3 3.5l2.5 8.5zm2.5-8.5H13"/></svg></button></form>') + '</div>';
    var pct = x.st === 'draft' ? 0 : Math.round((at - 1) / 3 * 100);
    var act = GRO ? '' : x.st === 'in' ? '<div class="sheet__f"><a class="btn sec" href="' + back + '">Cancel</a><button type="button" class="btn dark" data-gexit="' + x.id + '">Mark exit</button></div>'
      : x.st === 'draft' ? '<button type="button" class="btn dark" data-gfinish>Check in</button>' : x.dc === 'pend' ? '<button type="button" class="btn dark" data-gdc="' + x.id + '">Upload sealed DC</button>' : '';
    var ev = [];
    if (x.st === 'draft') ev.push({ at: x.editAt, title: 'Entry saved as draft', by: guard });
    tl.forEach(function (st, i) { if (!st[1]) return; ev.push({ at: st[1], title: st[0], by: i === 0 || i === 3 ? guard : '' });
      if (i === 0) ev.push({ at: addMin(st[1], 2), title: 'Challans checked', val: chal.length + (chal.length === 1 ? ' challan' : ' challans') });
      if (i === 1 && chal.length) ev.push({ at: addMin(st[1], 3), title: 'Challans digitised', val: chal.reduce(function (n, c, ci) { return n + gLines(c, ci, x).length; }, 0) + ' lines' }); });
    if (x.st === 'out') ev.push({ at: addMin(x.outAt, 1), title: 'Sealed DC', val: x.dc === 'up' ? 'Uploaded' : 'Pending' }); else if (dcReady) ev.push({ at: '2026-09-30T15:42', title: 'Sealed DC', val: 'Attached' });
    ev.sort(function (a, c) { return a.at < c.at ? -1 : 1; }); if (ev.length) ev[ev.length - 1].now = true; ev.reverse();
    var foot = tlFoot(ev, (x.st === 'in' ? (digi ? 'Inside, receiving in progress' : 'Inside, waiting for receiving') : x.st === 'draft' ? 'Entry not finished' : x.dc === 'up' ? 'Left with the sealed DC' : 'Left, sealed DC pending'), 'Current status', '<div class="txprog" aria-hidden="true"><i style="width:' + Math.max(pct, 4) + '%"></i></div>' + act);
    return '<div style="min-height:0;display:grid;grid-template-rows:auto 1fr auto;overflow:hidden"><a class="txback t-body-medium" href="' + back + '">' + ic('back', 20) + 'All vehicles</a><div class="txdb" style="min-height:0">' + head + '<div class="gsecs">' + entry + ch + dc + sec + com + '</div></div>' + foot + '</div>';
  }
  /* ---- Log entry (concept screens 8 Oct): same parts as the entry detail; fields edit a draft in memory, Mark entry saves it ---- */
  var GN = null;
  function gnReset() { GN = { veh: [{ no: '', driver: '', phone: '', vendor: '', ph: 0 }], chal: [{ no: '', ph: 0, veh: [0] }], guard: VIEWER.name, gph: 0, v: 0, c: 0, tried: false }; }
  function gnFromEntry(x) {   /* Record exit: the entry's log entry form, already filled */
    var ent = gEnt(x), o = GT.ov[x.id] || {};
    GN = { mode: 'exit', id: x.id, inAt: x.inAt, entryGate: x.v.gate, veh: ent.veh.map(function (v, i) { return { no: v.no || '', driver: v.driver || '', phone: v.driver ? phone(x.id + i).replace('+91 ', '') : '', vendor: v.vendor || x.vendor || '', ph: v.ph || 0 }; }),
      chal: ent.chal.map(function (c) { return JSON.parse(JSON.stringify(c)); }), guard: VIEWER.name, gph: o.sph == null ? 1 : o.sph, v: 0, c: 0, tried: false, dc: !!o.dcReady };
  }
  function gnOk() { return GN.veh.every(function (v) { return v.no.trim() && v.vendor.trim(); }) && GN.chal.every(function (c) { return c.no.trim(); }) && GN.guard.trim(); }
  function gnInput(path, val, lab, ph, req, type) {
    var bad = GN.tried && req && !String(val || '').trim();
    return '<label class="gin' + (bad ? ' bad' : '') + '"><span>' + lab + (req ? ' <i aria-hidden="true">*</i>' : '') + '</span><input type="' + (type || 'text') + '" data-gn="' + path + '" value="' + esc(val || '') + '" placeholder="' + ph + '"' + (req ? ' aria-required="true"' : '') + (bad ? ' aria-invalid="true"' : '') + ' autocomplete="off">' + (bad ? '<small>Required</small>' : '') + '</label>';
  }
  function gnPhotos(n, kind, i, empty) {
    if (!n) return '<button type="button" class="dcdrop gndrop" data-gnph="' + kind + '"' + (i != null ? ' data-i="' + i + '"' : '') + '>' + sv('cam', 26) + '<b class="t-body-medium">Take photo or upload image</b><small class="t-body-regular">JPEG or PNG, up to 50 MB</small></button>';
    var h = ''; for (var k = 0; k < n; k++) h += '<span class="gthumb ' + kind + '" role="img" aria-label="Photo ' + (k + 1) + '">' + (kind === 'sec' ? si('user', 22) : si(kind === 'veh' ? 'image' : 'note', 22)) + '<button type="button" class="gthx" data-gnphx="' + kind + '"' + (i != null ? ' data-i="' + i + '"' : '') + ' aria-label="Remove photo">' + ic('close', 14) + '</button></span>';
    return '<div class="gthumbs">' + h + '<button type="button" class="gaddph" data-gnph="' + kind + '"' + (i != null ? ' data-i="' + i + '"' : '') + ' aria-label="Add photo">' + sv('cam', 20) + '<span>Add</span></button></div>';
  }
  function gtNewForm(g, b, cur) {
    if (!GN) gnReset();
    var back = '#gates/' + g.id + '/' + cur, now = '2026-09-30T15:42';
    var ex = GN.mode === 'exit';
    var head = ex ? '<div class="txdh gtdh"><div class="txdh__r"><div class="grow"><span class="gchip out">' + sv('outi', 14) + 'Recording exit</span><h3 id="txT">Log exit</h3><span class="sub t-body-regular">' + esc(GN.veh[0].vendor) + ' · entered ' + dt(GN.inAt) + ' · leaving by ' + esc(g.name) + '</span></div>' + QR + '</div></div>'
      : '<div class="txdh gtdh"><div class="txdh__r"><div class="grow"><span class="gchip draft">' + sv('pen', 14) + 'New entry</span><h3 id="txT">Log entry</h3><span class="sub t-body-regular">' + esc(g.name) + ' · ' + esc(b.name) + ' · ' + dt(now) + '</span></div></div></div>';
    var veh = '<div class="txsec">' + sv('truck', 20) + '<span class="grow">Vehicle entries <span class="cnt">' + GN.veh.length + '</span></span><button type="button" class="linkbtn t-body-medium gadd" data-gnadd="veh">' + si('plus', 18) + 'Add vehicle</button></div><div class="gacc">' +
      GN.veh.map(function (v, i) { var open = GN.v === i, bad = GN.tried && (!v.no.trim() || !v.vendor.trim());
        return '<div class="gacc__i' + (open ? ' open' : '') + (bad ? ' err' : '') + '"><button type="button" class="gacc__h" data-gnopen="v' + i + '" aria-expanded="' + open + '"><span class="gacc__n">Vehicle ' + (i + 1) + '</span><b class="mono">' + esc(v.no || 'Not filled yet') + '</b><span class="gacc__m">' + (bad ? '<span class="gerr">Needs details</span>' : esc(v.vendor || '')) + '</span>' + sv('chev', 20) + '</button>' +
          (open ? '<div class="gacc__b"><div class="ginputs">' + gnInput('veh.' + i + '.no', v.no, 'Vehicle number', 'e.g. GJ-10-AB-1234', true) + gnInput('veh.' + i + '.driver', v.driver, 'Driver name', 'Name') + gnInput('veh.' + i + '.phone', v.phone, 'Driver phone', '10 digit number', false, 'tel') + gnInput('veh.' + i + '.vendor', v.vendor, 'Vendor', 'Company or person', true) +
            '<div class="gin ro"><span>Entry gate</span><b>' + (ex ? esc(gname(GN.entryGate)) + ', ' + hm(GN.inAt) : esc(g.name) + ', 3:42 PM') + '</b></div><div class="gin ro' + (ex ? ' now' : '') + '"><span>Exit gate</span><b>' + (ex ? esc(g.name) + ', 3:42 PM' : 'Decide at the gate') + '</b></div></div>' + gnPhotos(v.ph, 'veh', i) +
            (GN.veh.length > 1 ? '<div class="gacc__a"><button type="button" class="linkbtn t-body-medium gdelt" data-gndel="v' + i + '">' + si('bin', 16) + 'Remove vehicle</button></div>' : '') + '</div>' : '') + '</div>'; }).join('') + '</div>';
    var ch = '<div class="txsec">' + si('note', 20) + '<span class="grow">Challan details <span class="cnt">' + GN.chal.length + '</span></span><button type="button" class="linkbtn t-body-medium gadd" data-gnadd="chal">' + si('plus', 18) + 'Add challan</button></div><div class="gacc">' +
      GN.chal.map(function (c, i) { var open = GN.c === i, bad = GN.tried && !c.no.trim();
        return '<div class="gacc__i' + (open ? ' open' : '') + (bad ? ' err' : '') + '"><button type="button" class="gacc__h" data-gnopen="c' + i + '" aria-expanded="' + open + '"><span class="gacc__n">Challan ' + (i + 1) + '</span><b class="mono">' + esc(c.no || 'Not filled yet') + '</b><span class="gacc__m">' + (bad ? '<span class="gerr">Needs a number</span>' : GN.veh.length > 1 ? (c.veh.length > 1 ? 'Split across ' + c.veh.length + ' vehicles' : 'On vehicle ' + (c.veh[0] + 1)) : '') + '</span>' + sv('chev', 20) + '</button>' +
          (open ? '<div class="gacc__b"><div class="ginputs one">' + gnInput('chal.' + i + '.no', c.no, 'Challan number', 'e.g. DC-JFF-4488', true) + '</div>' +
            (GN.veh.length > 1 ? '<div class="gvch"><small>Vehicles carrying this challan</small>' + GN.veh.map(function (v, vi) { return '<button type="button" class="spchip t-body-medium" data-gnveh="' + i + '" data-vi="' + vi + '" aria-pressed="' + (c.veh.indexOf(vi) !== -1) + '">' + esc(v.no || 'Vehicle ' + (vi + 1)) + '</button>'; }).join('') + '</div>' : '') +
            gnPhotos(c.ph, 'dc', i) + (GN.chal.length > 1 ? '<div class="gacc__a"><button type="button" class="linkbtn t-body-medium gdelt" data-gndel="c' + i + '">' + si('bin', 16) + 'Delete challan</button></div>' : '') + '</div>' : '') + '</div>'; }).join('') + '</div>';
    var sec = '<div class="txsec">' + si('user', 20) + '<span class="grow">Security details</span></div><div class="ginputs one gpad">' + gnInput('guard', GN.guard, 'Security name', 'Your name', true) + '</div>' + gnPhotos(GN.gph, 'sec');
    var dcs = ex ? '<div class="txsec">' + sv('badge', 20) + '<span class="grow">Sealed DC</span>' + (GN.dc ? '<span class="dctag up">Attached</span>' : '<span class="dctag pend">Not attached</span>') + '</div>' +
      (GN.dc ? '<div class="gdcok">' + SEAL + '<span class="grow"><b class="t-body-medium">sealed-dc-photo.jpg</b><small class="t-body-regular">Saved as uploaded when you mark the exit</small></span><button type="button" class="ricon gdel" data-gndc="0" aria-label="Remove sealed DC">' + si('bin', 18) + '</button></div>'
        : '<button type="button" class="dcdrop gndrop gnfull" data-gndc="1">' + sv('cam', 26) + '<b class="t-body-medium">Take photo of the sealed DC</b><small class="t-body-regular">Skip it and the exit is saved with the sealed DC pending</small></button>') : '';
    var foot = '<div class="txfoot"><div class="txfoot__h"><span class="grow"><small>Current status</small><b>' + gnMsg() + '</b></span></div><div class="sheet__f"><a class="btn sec" href="' + back + '" data-gncancel>Cancel</a><button type="button" class="btn dark" data-gnsave' + (gnOk() ? '' : ' aria-disabled="true"') + '>' + (ex ? 'Mark exit' : 'Mark entry') + '</button></div></div>';
    return '<div style="min-height:0;display:grid;grid-template-rows:auto 1fr auto;overflow:hidden"><a class="txback t-body-medium" href="' + back + '" data-gncancel>' + ic('back', 20) + 'All vehicles</a><div class="txdb" style="min-height:0">' + head + '<div class="gsecs gnform">' + veh + ch + dcs + sec + '</div></div>' + foot + '</div>';
  }
  function gnFoot() { var b = document.querySelector('#gtpanel [data-gnsave]'), t = document.querySelector('#gtpanel .txfoot__h b'); if (!b) return; if (gnOk()) b.removeAttribute('aria-disabled'); else b.setAttribute('aria-disabled', 'true'); if (t) t.textContent = gnMsg(); }
  function gnMsg() { return !gnOk() ? 'Fill the vehicle, vendor and challan number' : GN.mode === 'exit' ? (GN.dc ? 'Ready to mark the exit' : 'Ready to mark the exit, sealed DC pending') : 'Ready to mark the entry'; }
  function gatePanel(g, b, tab, vid) {
    /* keep the reader where they were: a re-render of the same vehicle (open a row, add a photo, comment) must not jump to the top */
    var P0 = document.getElementById('gtpanel'), db0 = P0.querySelector('.txdb'), ls0 = P0.querySelector('.txlist'), keepId = GTSEL, keepDb = db0 ? db0.scrollTop : 0, keepLs = ls0 ? ls0.scrollTop : 0;
    var P = document.getElementById('gtpanel'), tabs = gtTabs(g), cur = tabs.indexOf(tab) !== -1 ? tab : 'all', all = gtVisits(g), gsAll = sgates(b.id).filter(function (x) { return x.active && onTab(x); });
    GTCUR = { g: g, b: b };
    var q = GTQ.toLowerCase(), match = function (x) { return (!q || [x.vehicleNo, x.vendor, x.challanNo].join(' ').toLowerCase().indexOf(q) !== -1) && (!GTDC || (x.st === 'out' && x.dc === GTDC)); };
    var n = { all: all.length, in: all.filter(function (x) { return x.st === 'in'; }).length, out: all.filter(function (x) { return x.st === 'out'; }).length };
    var body;
    {
      var l = all.filter(function (x) { return (cur === 'all' || x.st === cur) && match(x); }), land = matchMedia('(orientation: landscape)').matches;
      var isExit = /^exit-/.test(vid || ''), exX = isExit ? all.filter(function (x) { return x.id === vid.slice(5) && x.st === 'in'; })[0] : null;
      if (isExit && (!GN || GN.mode !== 'exit' || GN.id !== (exX && exX.id))) { if (exX) gnFromEntry(exX); }
      var isNew = vid === 'new' || !!exX, selx = isNew ? null : vid ? all.filter(function (x) { return x.id === vid; })[0] : (land ? l[0] : null); GTSEL = selx ? selx.id : ''; if (!isNew) GN = null; if (vid === 'new' && GN && GN.mode === 'exit') GN = null;
      body = '<div class="txbody gtsplit' + ((vid && selx) || isNew ? ' sel' : '') + '"><div class="txlist"><div class="gtband"><div class="spsearch">' + ic('search', 22) + '<input type="search" id="gtq" value="' + esc(GTQ) + '" placeholder="Search vendor, DC number or vehicle" aria-label="Search vendor, DC number or vehicle" autocomplete="off"><button type="button" class="ricon" data-gscan aria-label="Scan a gate pass">' + sv('qr', 22) + '</button></div><button type="button" class="spfilter' + (GTDC ? ' on' : '') + '" data-gfilter aria-label="Filter" aria-haspopup="dialog">' + sv('sliders', 22) + '</button></div>' +
        (l.length ? l.map(function (x) { return gtCard(x, b, g); }).join('') : '<div class="empty"><b class="t-minor-title">' + (q || GTDC ? 'No vehicles match' : 'No vehicles yet') + '</b><span class="t-body-regular">' + (q || GTDC ? 'Try another search or clear the filter.' : 'Use + to log an entry at ' + esc(g.name) + '.') + '</span></div>') + '</div><section class="txdet" aria-labelledby="txT">' + (isNew ? gtNewForm(g, b, cur) : selx ? gtDetail(selx, g, b, cur) : '<div class="txempty t-body-regular" style="align-self:center">Pick a vehicle to see its entry.</div>') + '</section></div>';

    }
    P.innerHTML = '<div class="gthero" style="--stc:' + STC[b.site] + '"><a class="iconbtn" href="#gates" aria-label="Back to Gates">' + ic('back', 24) + '</a><span class="stcard__art">' + si('art', 220, '0 0 64 64') + '</span>' +
      '<button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button>' +
      '<div class="gthero__loc t-body-medium">' + sv('pin') + esc(b.name) + '<i></i>' + sv('bld') + esc(sby(SD.departments, b.dept).name) + ' · ' + esc(b.code) + '</div>' +
      '<button type="button" class="gtpick" data-gpick' + (gsAll.length > 1 ? '' : ' disabled') + ' aria-haspopup="dialog" aria-label="Gate: ' + esc(g.name) + (gsAll.length > 1 ? ', switch gate' : '') + '"><span class="gico">' + sv('door', 24) + '</span><span><b id="gtT">' + esc(g.name) + (gsAll.length > 1 ? sv('chev', 20) : '') + '</b><small class="t-body-regular">' + esc(g.purposes.join(' + ')) + '</small></span></button></div>' +
      '<nav class="txtabs" role="tablist" aria-label="' + esc(g.name) + '" style="grid-template-columns:repeat(' + tabs.length + ', minmax(0, 1fr))">' + tabs.map(function (k) { return '<a class="txtab t-body-medium" role="tab" href="#gates/' + g.id + '/' + k + '" aria-selected="' + (k === cur) + '">' + (GTL[k] || GTAB[k]) + (n[k] != null ? '<span class="n">' + n[k] + '</span>' : '') + '</a>'; }).join('') + '</nav>' +
      body;
    var db1 = P.querySelector('.txdb'), ls1 = P.querySelector('.txlist');
    if (ls1) ls1.scrollTop = keepLs;
    if (db1 && keepId && keepId === GTSEL) db1.scrollTop = keepDb;
    /* the row that was tapped stays where the finger is, even when the row above it closes */
    if (GANCH && db1) { var a1 = db1.querySelector(GANCH.sel); if (a1) db1.scrollTop += a1.getBoundingClientRect().top - GANCH.top; } GANCH = null;
    gmenu(false); P.hidden = false; var fab = document.getElementById('gfab'); fab.hidden = false; fab.classList.toggle('hide-p', !!((vid && selx) || vid === 'new')); P.classList.toggle('det', !!((vid && selx) || vid === 'new'));
    [].forEach.call(P.querySelectorAll('.asbtn'), function (x) { x.innerHTML = ic('user', 20) + '<span class="t-body-medium">Viewing as: ' + esc(VIEWER.name) + ' <small>· ' + esc(VIEWER.title) + '</small></span>' + ic('dropdown', 18); });
  }
  function gateClose() { document.getElementById('gtpanel').hidden = true; document.getElementById('gfab').hidden = true; gmenu(false); GTCUR = null; }
  function gmenu(o) { document.getElementById('gmenu').hidden = !o; document.getElementById('gfab').setAttribute('aria-expanded', String(!!o)); }
  function gtRe() { var r = sparse(); if (GTCUR) gatePanel(GTCUR.g, GTCUR.b, r.type, r.tx); }
  function gfind(id) { return GTCUR ? gtVisits(GTCUR.g).filter(function (x) { return x.id === id; })[0] : null; }
  function entrySheet(x) {
    sheet2(sheetHead(x ? 'Finish entry' : 'Log entry', esc(GTCUR.g.name) + ' · ' + esc(GTCUR.b.name)) + '<form class="fgrid" data-gentry="' + (x ? x.id : '') + '">' + field('Vehicle number*', 'vno', x && x.vehicleNo, 'e.g. GJ-10-AB-1234') + field('Vendor*', 'ven', x && x.vendor, 'Company or person') +
      '<div class="fcols">' + field('DC number', 'dc', x && x.challanNo, 'e.g. DC-JFF-4488') + field('Driver', 'drv', x && x.driver, 'Name') + '</div><p class="ferr" hidden></p>' +
      '<div class="sheet__f"><button type="submit" class="btn sec" name="draft" value="1">Save draft</button><button type="submit" class="btn pri">Check in</button></div></form>');
  }
  function exitSheet() {   /* + then Log exit: pick the vehicle, then its filled log entry form opens */
    var ins = gtVisits(GTCUR.g).filter(function (x) { return x.st === 'in'; });
    sheet2(sheetHead('Log exit', 'Pick the vehicle that is leaving ' + esc(GTCUR.g.name)) + (ins.length ? '<form class="fgrid" data-gexitf><div class="gpick" role="radiogroup" aria-label="Vehicle">' + ins.map(function (x, i) { var en = gEnt(x); return '<button type="button" role="radio" data-gpv="' + x.id + '" aria-pressed="' + (i === 0) + '"><span class="grow"><b>' + esc(x.vehicleNo) + (en.veh.length > 1 ? ' +' + (en.veh.length - 1) : '') + '</b><small>' + esc(x.vendor) + ' · in ' + dtl(x.inAt) + ' · ' + plural2(en.chal.length, 'challan') + '</small></span></button>'; }).join('') + '</div>' +
      '<div class="sheet__f"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">Continue</button></div></form>' : '<p class="t-body-regular" style="color:var(--ink)">No vehicle is checked in at ' + esc(GTCUR.g.name) + '.</p>'));
  }
  function dcSheet(only) {
    var pend = gtVisits(GTCUR.g).filter(function (x) { return x.st === 'out' && x.dc === 'pend' && (!only || x.id === only); });
    sheet2(sheetHead('Upload sealed DC', esc(GTCUR.g.name)) + (pend.length ? '<form class="fgrid" data-gdcf><div class="gpick" role="radiogroup" aria-label="Vehicle">' + pend.map(function (x, i) { return '<button type="button" role="radio" data-gpv="' + x.id + '" aria-pressed="' + (i === 0) + '"><span class="grow"><b>' + esc(x.vehicleNo) + '</b><small>' + esc(x.vendor) + ' · out ' + dtl(x.outAt) + '</small></span></button>'; }).join('') + '</div>' +
      '<button type="button" class="dcdrop" data-gphoto>' + sv('upload', 32) + '<b class="t-body-medium">Take a photo of the sealed DC</b><small class="t-body-regular">Demo: tap to attach a sample photo</small></button><p class="ferr" hidden></p>' +
      '<div class="sheet__f"><button type="button" class="btn sec" data-txclose>Cancel</button><button type="submit" class="btn pri">Upload</button></div></form>' : '<p class="t-body-regular" style="color:var(--ink)">No sealed DC is pending at ' + esc(GTCUR.g.name) + '.</p>'));
  }
  document.getElementById('gfab').addEventListener('click', function () { gmenu(document.getElementById('gmenu').hidden); });
  document.getElementById('gmenu').addEventListener('click', function (e) { var b = e.target.closest('[data-gact]'); gmenu(false); if (!b || !GTCUR) return; var k = b.getAttribute('data-gact'); if (k === 'entry') { GN = null; location.hash = '#gates/' + GTCUR.g.id + '/' + (sparse().type || 'all') + '/new'; } else if (k === 'exit') exitSheet(); else dcSheet(); });
  document.getElementById('gtpanel').addEventListener('input', function (e) {
    var pth = e.target.getAttribute && e.target.getAttribute('data-gn');
    if (pth && GN) { var q = pth.split('.'); if (q.length === 1) GN[q[0]] = e.target.value; else GN[q[0]][Number(q[1])][q[2]] = e.target.value;
      var h = e.target.closest('.gacc__i'); if (h && (q[2] === 'no')) { var m = h.querySelector('.gacc__h b'); if (m) m.textContent = e.target.value || 'Not filled yet'; }
      var lab = e.target.closest('.gin'); if (lab && lab.classList.contains('bad') && e.target.value.trim()) { lab.classList.remove('bad'); e.target.removeAttribute('aria-invalid'); var sm = lab.querySelector('small'); if (sm) sm.remove(); }
      if (h && h.classList.contains('err') && q.length === 3) { var it = GN[q[0]][Number(q[1])], okk = q[0] === 'veh' ? it.no.trim() && it.vendor.trim() : it.no.trim();
        if (okk) { h.classList.remove('err'); var ge = h.querySelector('.gerr'); if (ge) ge.outerHTML = q[0] === 'veh' ? esc(it.vendor) : ''; } }
      gnFoot(); return; } if (e.target.id === 'gtq') { GTQ = e.target.value; var pos = e.target.selectionStart; gtRe(); var i = document.getElementById('gtq'); if (i) { i.focus(); i.setSelectionRange(pos, pos); } } });
  document.getElementById('gtpanel').addEventListener('click', function (e) {
    var b;
    if ((b = e.target.closest('[data-gexit]'))) { GN = null; location.hash = '#gates/' + GTCUR.g.id + '/' + (sparse().type || 'all') + '/exit-' + b.getAttribute('data-gexit'); return; }
    if ((b = e.target.closest('[data-gdc]'))) { dcSheet(b.getAttribute('data-gdc')); return; }
    if ((b = e.target.closest('[data-gnopen]'))) { var k0 = b.getAttribute('data-gnopen'), ix0 = Number(k0.slice(1)); GANCH = { sel: '[data-gnopen="' + k0 + '"]', top: b.getBoundingClientRect().top }; if (k0[0] === 'v') GN.v = GN.v === ix0 ? -1 : ix0; else GN.c = GN.c === ix0 ? -1 : ix0; gtRe(); return; }
    if ((b = e.target.closest('[data-gnadd]'))) { if (b.getAttribute('data-gnadd') === 'veh') { GN.veh.push({ no: '', driver: '', phone: '', vendor: GN.veh[0].vendor, ph: 0 }); GN.v = GN.veh.length - 1; } else { GN.chal.push({ no: '', ph: 0, veh: GN.veh.map(function (_, i) { return i; }) }); GN.c = GN.chal.length - 1; } gtRe(); var f0 = document.querySelector('#gtpanel .gacc__i.open input'); if (f0 && b.getAttribute('data-gnadd') === 'veh') f0.focus(); return; }
    if ((b = e.target.closest('[data-gndel]'))) { var k1 = b.getAttribute('data-gndel'), ix1 = Number(k1.slice(1));
      if (k1[0] === 'v') { GN.veh.splice(ix1, 1); GN.chal.forEach(function (c) { c.veh = c.veh.filter(function (q) { return q !== ix1; }).map(function (q) { return q > ix1 ? q - 1 : q; }); if (!c.veh.length) c.veh = [0]; }); GN.v = 0; } else { GN.chal.splice(ix1, 1); GN.c = 0; } gtRe(); return; }
    if ((b = e.target.closest('[data-gnveh]'))) { var c1 = GN.chal[Number(b.getAttribute('data-gnveh'))], vi1 = Number(b.getAttribute('data-vi')), at1 = c1.veh.indexOf(vi1); if (at1 !== -1 && c1.veh.length === 1) { toast('A challan needs at least one vehicle'); return; } if (at1 !== -1) c1.veh.splice(at1, 1); else { c1.veh.push(vi1); c1.veh.sort(); } gtRe(); return; }
    if ((b = e.target.closest('[data-gnph]'))) { var kd = b.getAttribute('data-gnph'), ii = Number(b.getAttribute('data-i')); if (kd === 'sec') GN.gph++; else (kd === 'veh' ? GN.veh : GN.chal)[ii].ph++; toast('Photo added (demo)'); gtRe(); return; }
    if ((b = e.target.closest('[data-gnphx]'))) { var kx = b.getAttribute('data-gnphx'), ix2 = Number(b.getAttribute('data-i')); if (kx === 'sec') GN.gph = Math.max(0, GN.gph - 1); else { var it2 = (kx === 'veh' ? GN.veh : GN.chal)[ix2]; it2.ph = Math.max(0, it2.ph - 1); } gtRe(); return; }
    if ((b = e.target.closest('[data-gndc]'))) { GN.dc = b.getAttribute('data-gndc') === '1'; if (GN.dc) toast('Sealed DC attached (demo)'); gtRe(); return; }
    if (e.target.closest('[data-gncancel]')) { GN = null; return; }
    if (e.target.closest('[data-gnsave]')) {
      if (!gnOk()) { GN.tried = true; var bad0 = GN.veh.findIndex(function (v) { return !v.no.trim() || !v.vendor.trim(); }); if (bad0 !== -1) GN.v = bad0; else { var bc = GN.chal.findIndex(function (c) { return !c.no.trim(); }); if (bc !== -1) GN.c = bc; } gtRe(); var fi = document.querySelector('#gtpanel .gin.bad input'); if (fi) { fi.focus(); fi.scrollIntoView({ block: 'center' }); } return; }
      if (GN.mode === 'exit') { var xo = gfind(GN.id), eo = gEnt(xo), oo = GT.ov[GN.id] = GT.ov[GN.id] || {};
        eo.veh = GN.veh.map(function (v) { return { no: v.no.trim().toUpperCase(), driver: v.driver.trim(), vendor: v.vendor.trim(), ph: v.ph }; });
        eo.chal = GN.chal.map(function (c, ci) { var k = JSON.parse(JSON.stringify(c)); k.no = String(c.no).trim().toUpperCase(); if (!k.lines && xo.v.scen) k.lines = gLines(c, ci, xo); return k; });
        gEntSave(xo, eo); Object.assign(oo, { st: 'out', outAt: '2026-09-30T15:42', exitGate: GTCUR.g.id, dc: GN.dc ? 'up' : 'pend', guard: GN.guard.trim(), sph: GN.gph, seq: ++GT.seq }); gtSave();
        toast(eo.veh[0].no + (eo.veh.length > 1 ? ' and ' + (eo.veh.length - 1) + ' more' : '') + ' checked out' + (GN.dc ? ' with the sealed DC' : ', sealed DC pending')); GN = null; location.hash = '#gates/' + GTCUR.g.id + '/out/' + xo.id; return; }
      var now = '2026-09-30T15:42', id = 'GV-T' + (GT.add.length + 1), v0 = GN.veh[0];
      var ent = { veh: GN.veh.map(function (v) { return { no: v.no.trim().toUpperCase(), driver: v.driver.trim(), vendor: v.vendor.trim(), ph: v.ph }; }), chal: GN.chal.map(function (c) { return { no: c.no.trim().toUpperCase(), items: 'Not digitised yet', ph: c.ph, veh: c.veh.slice() }; }) };
      GT.add.push({ id: id, gate: GTCUR.g.id, bld: GTCUR.b.id, state: 'INSIDE', vehicleNo: ent.veh[0].no, vendor: ent.veh[0].vendor, driver: ent.veh[0].driver, enteredAt: now, challanNo: ent.chal[0].no });
      GT.ov[id] = { ent: ent, vehicleNo: ent.veh[0].no, vendor: ent.veh[0].vendor, driver: ent.veh[0].driver, challanNo: ent.chal[0].no, st: 'in', inAt: now, seq: ++GT.seq, guard: GN.guard.trim(), sph: GN.gph };
      gtSave(); GN = null; toast(ent.veh[0].no + (ent.veh.length > 1 ? ' and ' + (ent.veh.length - 1) + ' more' : '') + ' checked in at ' + GTCUR.g.name); location.hash = '#gates/' + GTCUR.g.id + '/in/' + id; return; }
    if (e.target.closest('[data-txsteps]')) { TXTL = !TXTL; TXTLA = TXTL; gtRe(); return; }
    if ((b = e.target.closest('[data-gfinish], [data-gedit]'))) { entrySheet(gfind(GTSEL)); return; }
    if (e.target.closest('[data-gchal]')) { chalSheet(); return; }
    if (e.target.closest('[data-gvadd]')) { vehSheet(); return; }
    if ((b = e.target.closest('[data-gvedit]'))) { vehSheet(Number(b.getAttribute('data-gvedit'))); return; }
    if ((b = e.target.closest('[data-gvopen], [data-gcopen]'))) GANCH = { sel: b.hasAttribute('data-gvopen') ? '[data-gvopen="' + b.getAttribute('data-gvopen') + '"]' : '[data-gcopen="' + b.getAttribute('data-gcopen') + '"]', top: b.getBoundingClientRect().top };
    if ((b = e.target.closest('[data-gvopen]'))) { var vi0 = Number(b.getAttribute('data-gvopen')); GOPEN.v = GOPEN.v === vi0 ? -1 : vi0; gtRe(); return; }
    if ((b = e.target.closest('[data-gcopen]'))) { var ci0 = Number(b.getAttribute('data-gcopen')); GOPEN.c = GOPEN.c === ci0 ? -1 : ci0; gtRe(); return; }
    if ((b = e.target.closest('[data-gcveh]'))) { var xx = gfind(GTSEL), en = gEnt(xx), c = en.chal[Number(b.getAttribute('data-gcveh'))], vi = Number(b.getAttribute('data-vi')), at = c.veh.indexOf(vi);
      if (at !== -1 && c.veh.length === 1) { toast('A challan needs at least one vehicle'); return; } if (at !== -1) c.veh.splice(at, 1); else { c.veh.push(vi); c.veh.sort(); } gEntSave(xx, en); gtRe(); return; }
    if ((b = e.target.closest('[data-gvdel]'))) { var xd = gfind(GTSEL), ed = gEnt(xd), di = Number(b.getAttribute('data-gvdel')), gone = ed.veh[di].no; ed.veh.splice(di, 1);
      ed.chal.forEach(function (c) { c.veh = c.veh.filter(function (k) { return k !== di; }).map(function (k) { return k > di ? k - 1 : k; }); if (!c.veh.length) c.veh = [0]; }); GOPEN.v = 0; gEntSave(xd, ed); toast(gone + ' removed from this entry'); gtRe(); return; }
    if ((b = e.target.closest('[data-gcdel]'))) { var x0 = gfind(GTSEL), e0 = gEnt(x0); e0.chal.splice(Number(b.getAttribute('data-gcdel')), 1); GOPEN.c = 0; gEntSave(x0, e0); toast('Challan removed'); gtRe(); return; }
    if ((b = e.target.closest('[data-gph]'))) { var x1 = gfind(GTSEL), o1 = GT.ov[x1.id] = GT.ov[x1.id] || {}, k = b.getAttribute('data-gph');
      if (k === 'sec') { o1.sph = (o1.sph == null ? 1 : o1.sph) + 1; gtSave(); } else { var e1 = gEnt(x1), it = (k === 'veh' ? e1.veh : e1.chal)[Number(b.getAttribute('data-i'))]; it.ph = (it.ph || 0) + 1; gEntSave(x1, e1); }
      toast('Photo added (demo)'); gtRe(); return; }
    if (e.target.closest('[data-gdcz]')) { var x2 = gfind(GTSEL), o2 = GT.ov[x2.id] = GT.ov[x2.id] || {}; if (x2.st === 'out') o2.dc = 'up'; else o2.dcReady = true; gtSave(); toast(x2.st === 'out' ? 'Sealed DC uploaded for ' + x2.vehicleNo : 'Sealed DC attached'); gtRe(); return; }
    if (e.target.closest('[data-call]') || e.target.closest('[data-msg]')) { var c = e.target.closest('[data-call]') || e.target.closest('[data-msg]'); toast((c.hasAttribute('data-call') ? 'Calling ' : 'Message to ') + (c.getAttribute('data-call') || c.getAttribute('data-msg')) + ' (demo)'); return; }
    if ((b = e.target.closest('[data-gopen]'))) { location.hash = '#gates/' + GTCUR.g.id + '/' + (sparse().type || 'all') + '/' + b.getAttribute('data-gopen'); return; }
    if (e.target.closest('[data-gscan]')) { toast('Point the camera at the gate pass QR (demo)'); return; }
    if (e.target.closest('[data-gfilter]')) { sheet2(sheetHead('Filter') + '<div class="sheet__g"><h3 class="t-minor-medium">Sealed DC</h3><div class="chips">' + [['', 'All'], ['pend', 'Pending'], ['up', 'Uploaded']].map(function (o) { return '<button type="button" class="spchip t-body-medium" data-gfdc="' + o[0] + '" aria-pressed="' + (o[0] === GTDC) + '">' + o[1] + '</button>'; }).join('') + '</div></div>'); return; }
    if (e.target.closest('[data-gpick]')) { var gs = sgates(GTCUR.b.id).filter(function (x) { return x.active && onTab(x); }); sheet2(sheetHead('Switch gate', esc(GTCUR.b.name)) + '<div class="gpick">' + gs.map(function (x) { return '<button type="button" data-gto="' + x.id + '" aria-pressed="' + (x.id === GTCUR.g.id) + '"><span class="gico">' + GICO + '</span><span class="grow"><b>' + esc(x.name) + '</b><small>' + esc(x.purposes.join(' + ')) + '</small></span></button>'; }).join('') + '</div>'); return; }
  });
  document.getElementById('gtpanel').addEventListener('submit', function (e) {
    var f = e.target; if (!f.hasAttribute('data-gcom')) return; e.preventDefault(); var v = f.c.value.trim(); if (!v || !GTSEL) return;
    var o = GT.ov[GTSEL] = GT.ov[GTSEL] || {}; o.comments = (o.comments || []).concat([{ by: VIEWER.name, at: '2026-09-30T15:42', text: v }]); gtSave(); gtRe();
    var db = document.querySelector('#gtpanel .txdb'); if (db) db.scrollTop = db.scrollHeight;
  });
  document.getElementById('gtpanel').addEventListener('keydown', function (e) { var b = e.target.closest && e.target.closest('[data-gopen]'); if (b && e.target === b && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); b.click(); } });
  document.getElementById('txsheet').addEventListener('click', function (e) {
    var b, S = document.getElementById('txsheet');
    if ((b = e.target.closest('[data-gfdc]'))) { GTDC = b.getAttribute('data-gfdc'); S.hidden = true; gtRe(); return; }
    if ((b = e.target.closest('[data-gto]'))) { S.hidden = true; location.hash = '#gates/' + b.getAttribute('data-gto'); return; }
    if ((b = e.target.closest('[data-gpv], [data-gsdc]'))) { [].forEach.call(b.parentNode.children, function (x) { x.setAttribute('aria-pressed', String(x === b)); }); return; }
    if ((b = e.target.closest('[data-gphoto]'))) { b.classList.add('done'); b.innerHTML = sv('badge', 32) + '<b class="t-body-medium">sealed-dc-photo.jpg attached</b><small class="t-body-regular">Tap Upload to save it</small>'; return; }
  });
  document.getElementById('txsheet').addEventListener('submit', function (e) {
    var f = e.target, S = document.getElementById('txsheet'), now = '2026-09-30T15:42',   /* the mock clock */ sel = function () { var p = f.querySelector('[data-gpv][aria-pressed="true"]'); return p && p.getAttribute('data-gpv'); };
    if (f.hasAttribute('data-gchalf')) { e.preventDefault(); var er0 = f.querySelector('.ferr'); if (!f.no.value.trim() || !f.items.value.trim()) { er0.textContent = 'Enter the challan number and items.'; er0.hidden = false; return; }
      var cv = [].map.call(f.querySelectorAll('input[name=cv]:checked'), function (q) { return Number(q.value); }); if (!cv.length) { er0.textContent = 'Pick at least one vehicle.'; er0.hidden = false; return; }
      var x3 = gfind(GTSEL), e3 = gEnt(x3); e3.chal.push({ no: f.no.value.trim().toUpperCase(), items: f.items.value.trim(), ph: 0, veh: cv }); GOPEN.c = e3.chal.length - 1; gEntSave(x3, e3); S.hidden = true; toast('Challan added'); gtRe(); return; }
    if (f.hasAttribute('data-gvehf')) { e.preventDefault(); var er1 = f.querySelector('.ferr'); if (!f.vno.value.trim()) { er1.textContent = 'Enter the vehicle number.'; er1.hidden = false; return; }
      var x4 = gfind(GTSEL), e4 = gEnt(x4), ix = f.getAttribute('data-gvehf'), rec = { no: f.vno.value.trim().toUpperCase(), driver: f.drv.value.trim(), vendor: f.ven.value.trim() || x4.vendor };
      if (ix === '') { rec.ph = 0; e4.veh.push(rec); GOPEN.v = e4.veh.length - 1; toast(rec.no + ' added to this entry'); } else { Object.assign(e4.veh[Number(ix)], rec); toast('Vehicle saved'); }
      gEntSave(x4, e4); S.hidden = true; gtRe(); return; }
    if (f.hasAttribute('data-gentry')) { e.preventDefault(); var err = f.querySelector('.ferr'), draft = e.submitter && e.submitter.name === 'draft';
      if (!f.vno.value.trim() || !f.ven.value.trim()) { err.textContent = 'Enter the vehicle number and vendor.'; err.hidden = false; return; }
      var id = f.getAttribute('data-gentry'), rec = { vehicleNo: f.vno.value.trim().toUpperCase(), vendor: f.ven.value.trim(), challanNo: f.dc.value.trim(), driver: f.drv.value.trim(), st: draft ? 'draft' : 'in', editAt: now };
      var prev = id && gfind(id); if (prev && prev.st === 'in') { rec.st = 'in'; } else if (!draft) rec.inAt = now;
      if (!id) { id = 'GV-T' + (GT.add.length + 1); GT.add.push({ id: id, gate: GTCUR.g.id, bld: GTCUR.b.id, state: draft ? 'DRAFT' : 'INSIDE', vehicleNo: rec.vehicleNo, vendor: rec.vendor, enteredAt: draft ? '' : now, atGateAt: now }); }
      rec.seq = ++GT.seq; GT.ov[id] = Object.assign(GT.ov[id] || {}, rec); gtSave(); S.hidden = true; toast(rec.vehicleNo + (draft ? ' saved as draft' : ' checked in at ' + GTCUR.g.name)); gtRe(); return; }
    if (f.hasAttribute('data-gexitf')) { e.preventDefault(); var id2 = sel(); if (!id2) return; S.hidden = true; GN = null; location.hash = '#gates/' + GTCUR.g.id + '/' + (sparse().type || 'all') + '/exit-' + id2; return; }
    if (f.hasAttribute('data-gdcf')) { e.preventDefault(); var id3 = sel(), ph = f.querySelector('[data-gphoto]'), er = f.querySelector('.ferr'); if (!ph.classList.contains('done')) { er.textContent = 'Attach the sealed DC photo first.'; er.hidden = false; return; }
      GT.ov[id3] = Object.assign(GT.ov[id3] || {}, { dc: 'up' }); gtSave(); S.hidden = true; toast('Sealed DC uploaded for ' + gfind(id3).vehicleNo); gtRe(); return; }
  });
  document.addEventListener('keydown', function (e) { if (e.key !== 'Escape') return; if (!document.getElementById('gmenu').hidden) { gmenu(false); return; } if (!document.getElementById('gtpanel').hidden && document.getElementById('txsheet').hidden && RS.hidden) location.hash = '#gates'; });
"""
