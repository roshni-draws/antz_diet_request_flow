# sp3.py: exec'd inside home2.py. Diet by Species tab v3: species records + detail from the
# Dev system local screens diet/by-species (by-species.data.js resolved through diet-model.js).
_bs = open(os.path.join(HERE, 'bsdata.json')).read().replace(' – ', ' to ').replace('–', '-').replace('—', '-')
BS = json.loads(_bs)
for _k, _p in BS['plans'].items():
    _p['sharers'] = [[x['tsn'], x['plan']] for x in _p.get('sharers', [])]
exec(open(os.path.join(HERE, 'sample.py')).read())
_spl = []
for _s in BS['species']:
    _spl.append({k: _s[k] for k in ('tsn', 'name', 'sci', 'cls', 'animals', 'diet', 'verified', 'enclosures', 'animalList', 'plans', 'photos')})
BS_EMBED = json.dumps({'species': _spl, 'plans': BS['plans']}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
N_SP = len(_spl)

SP3_CSS = '''    /* =========================================================
       12. SPECIES DETAIL  (Dev system by-species detail in Antz app style)
       landscape: list 40% + detail 60%; portrait: detail opens as a panel
       ========================================================= */
    .sp-split { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--sp-16); align-items: start; }
    .sp-detail { display: none; }
    .spcard[aria-current="true"] { box-shadow: inset 0 0 0 2px var(--md3-primary); border-radius: var(--radius); }
    .spcard .go { color: var(--md3-on-primary-container); transform: rotate(-90deg); }
    .spcard .tagc { margin-top: 4px; }
    /* species header card: name + primary action / stats + secondary actions (container-query layout) */
    .sreqs__h { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
    .sreqs__h h3 { color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
    .sreqs__need { display: flex; align-items: center; gap: 8px; color: #8A5A00; background: var(--moderate-a10); padding: 8px 12px; border-radius: 8px; }
    .sreqs__sub { color: var(--md3-neutral-secondary); }
    .sreq { display: flex; align-items: center; gap: 12px; width: 100%; min-height: 64px; padding: 10px 12px 10px 0; text-align: left; border-radius: 8px; background: var(--md3-background); overflow: hidden; }
    .sreq .ribbon { margin: 0; min-width: 48px; height: 36px; font-size: 16px; padding: 0 8px 0 16px; }
    .sreq .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .sreq .grow b { color: var(--head); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .sreq .grow span, .sreq .grow small { color: var(--ink); }
    .sreq .grow small { color: var(--md3-neutral-secondary); }
    .sreq .grow small.nx { color: var(--md3-on-primary-container); }
    .sreq .grow small.dx { display: inline-flex; align-items: center; gap: 4px; color: var(--head); }
    .hist .hcount { min-width: 22px; height: 22px; padding: 0 7px; border-radius: 11px; display: inline-grid; place-items: center; font-size: 12px; font-weight: 700; background: var(--md3-displaybg-primary); color: var(--md3-on-primary-container); }
    .hero__sec .hist.due { border-color: #E2B33C; background: #FFF6DB; color: #6B4E00; }
    .hero__sec .hist.due svg { color: #8A5A00; }
    .hist.due .hcount { background: #8A5A00; color: var(--white); }
    .hseg { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .hseg .n { margin-left: 4px; opacity: .75; font-variant-numeric: tabular-nums; }
    .hseg .hdot { margin-left: 8px; min-width: 20px; height: 20px; padding: 0 6px; border-radius: 10px; display: inline-grid; place-items: center; font-size: 12px; font-weight: 700; background: #8A5A00; color: var(--white); }
    .hreqs { display: grid; gap: 8px; }
    .hreqs__tab { justify-self: start; min-height: 44px; display: inline-flex; align-items: center; padding: 0 4px; margin-top: 4px; }
    .hfrom { white-space: nowrap; display: inline-flex; align-items: center; gap: 4px; min-height: 44px; margin-top: 4px; padding: 0 8px; border-radius: 6px; background: var(--moderate-a10); color: #6B4E00; font-size: 13px; }
    @media (hover: hover) { .sreq:hover { background: var(--md3-displaybg-primary); } }
    .hero { background: var(--white); border-radius: var(--radius); padding: var(--sp-20) var(--sp-24); container-type: inline-size; container-name: hero; }
    .hero__in { display: grid; grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: "top top" "row row"; column-gap: var(--sp-16); row-gap: var(--sp-16); align-items: center; }
    .hero__top { grid-area: top; display: flex; gap: var(--sp-16); align-items: center; min-width: 0; }
    .hero__nm { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .hero__nm h2 { color: var(--md3-on-primary-container); line-height: 1.2; overflow-wrap: anywhere; }
    .hero__nm i { color: var(--ink); }
    .hero__meta { color: var(--ink); display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
    .hero__nm i + .hero__meta { margin-top: 4px; }
    .hero__row { grid-area: row; display: flex; align-items: center; justify-content: space-between; gap: var(--sp-16); }
    .hero__stats { display: flex; align-items: stretch; }
    .hero__stats { gap: var(--sp-32); }
    .hero__stats .stx { display: grid; gap: 2px; align-content: center; min-width: 72px; }
    .hero__stats .stx .v { color: var(--md3-on-secondary-container); line-height: 1.1; }
    .hero__stats .stx.ok .v { color: var(--md3-on-surface); }
    .hero__stats .stx .l { color: var(--ink); white-space: nowrap; }
    .hero__sec { display: flex; gap: var(--sp-8); flex: none; }
    .hero__sec .chip { height: 48px; border-radius: 8px; }
    @container hero (max-width: 640px) {
      .hero__row { flex-direction: column; align-items: stretch; gap: var(--sp-16); }
      .hero__stats .stx { flex: 1; min-width: 0; }
      .hero__sec .chip { flex: 1; justify-content: center; }
    }
    @container hero (max-width: 520px) {
      .hero__in { grid-template-columns: minmax(0, 1fr); grid-template-areas: "top" "row"; }
    }
    .card2 { background: var(--white); border-radius: var(--radius); padding: var(--sp-16) var(--sp-20); display: grid; gap: var(--sp-12); margin-top: var(--sp-16); }
    .card2 > h3, .cap3 { color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
    .scopes { display: flex; flex-wrap: wrap; gap: var(--sp-8); }
    .scopes .spchip { flex-direction: column; align-items: flex-start; justify-content: center; height: auto; min-height: 52px; padding: 6px 14px; gap: 0; }
    .scopes .spchip small { font-size: 13px; font-weight: 400; }
    .targets { display: grid; gap: var(--sp-8); align-content: start; }
    .ttools { display: grid; gap: var(--sp-8); }
    .tsearchrow { position: relative; display: flex; gap: var(--sp-8); }
    .ttools .spsearch { height: 48px; flex: 1; min-width: 0; }
    .ttools .spsearch input:focus-visible { outline: none; }
    .tfilterbtn { position: relative; width: 48px; height: 48px; flex: none; display: grid; place-items: center; border: 1px solid var(--md3-outline-variant); border-radius: var(--radius); color: var(--md3-on-primary-container); background: var(--white); }
    .tfilterbtn.on { color: var(--white); border-color: var(--md3-on-primary-container); background: var(--md3-on-primary-container); }
    .tfilterbtn .n { position: absolute; top: 3px; right: 3px; min-width: 18px; height: 18px; padding: 0 5px; display: grid; place-items: center; border-radius: 999px; background: var(--md3-primary); color: var(--white); font-size: 11px; font-weight: 700; }
    .tfiltermenu { position: absolute; z-index: 6; top: calc(100% + var(--sp-8)); right: 0; width: min(300px, calc(100vw - var(--sp-32))); display: grid; gap: var(--sp-16); padding: var(--sp-16); border: 1px solid var(--md3-outline-variant); border-radius: 12px; background: var(--white); box-shadow: 0 12px 32px rgba(18,52,59,.16); }
    .tfiltergroup { display: grid; gap: var(--sp-8); }
    .tfiltergroup > span { color: var(--ink); font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
    .tfilteropts { display: flex; flex-wrap: wrap; gap: var(--sp-8); }
    .tfilteropts .spchip { min-height: 48px; }
    .tfilterclear { justify-self: start; min-height: 48px; padding: 0 var(--sp-8); color: var(--md3-on-primary-container); }
    @media (hover: hover) {
      .tfilterbtn:hover { background: var(--md3-displaybg-primary); }
      .tfilterbtn.on:hover { background: var(--md3-on-primary-container); }
      .tfilterclear:hover { text-decoration: underline; }
    }
    .tcount { color: var(--ink); }
    .tbox { position: relative; border-radius: 8px; }
    .tbox::before, .tbox::after { content: ""; position: absolute; left: 0; right: 0; height: 20px; pointer-events: none; z-index: 2; opacity: 0; transition: opacity 160ms var(--ease); }
    .tbox::before { top: 24px; background: linear-gradient(rgba(31,65,91,.12), rgba(31,65,91,0)); border-radius: 8px 8px 0 0; }
    .tbox::after { bottom: 0; background: linear-gradient(rgba(31,65,91,0), rgba(31,65,91,.12)); border-radius: 0 0 8px 8px; }
    .tbox.ft::before, .tbox.fb::after { opacity: 1; }
    .tscroll { max-height: 360px; overflow-y: auto; overscroll-behavior: contain; padding: 0 4px 4px 0; scrollbar-width: thin; }
    .tscroll .tgh { position: sticky; top: 0; z-index: 1; background: var(--white); padding: 6px 0 4px; margin: 0; }
    .tgt .tid { color: var(--ink); font-weight: 400; }
    .tgt mark, .tgh mark { background: rgba(55,189,105,.22); color: inherit; border-radius: 2px; }
    .tmore { justify-self: center; margin: 6px 0; }
    .tempty { display: grid; justify-items: center; gap: 6px; padding: var(--sp-24) var(--sp-12); text-align: center; color: var(--ink); }
    .tempty b { color: var(--head); }
    .tgh { color: var(--md3-neutral-secondary); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; margin-top: 4px; }
    .tgt { display: flex; align-items: center; gap: var(--sp-12); min-height: 52px; padding: 8px 12px; border-radius: 8px; background: var(--md3-background); text-align: left; width: 100%; }
    .tgt[aria-pressed="true"] { box-shadow: inset 0 0 0 2px var(--md3-primary); background: var(--white); }
    .tgt .grow { flex: 1; min-width: 0; display: grid; gap: 2px; }
    .tgt .grow b { color: var(--head); }
    .tgt .grow span { color: var(--ink); }
    .tgt .d { color: var(--md3-on-surface); white-space: nowrap; }
    .tgt .d.none { color: var(--ink); font-weight: 400; }
    .pchips { display: flex; flex-wrap: wrap; gap: var(--sp-8); align-items: center; }
    .pchip { display: grid; gap: 2px; padding: 8px 12px; min-height: 48px; border-radius: 8px; border: 1px solid var(--md3-outline-variant); background: var(--white); text-align: left; }
    .pchip[aria-pressed="true"] { border-color: var(--md3-primary); box-shadow: 0 0 0 1px var(--md3-primary); background: rgba(55,189,105,.05); }
    .pchip.off { opacity: .6; }
    .pchip .l1 { display: flex; align-items: center; gap: 8px; color: var(--head); font-weight: 600; }
    .pchip .l2 { color: var(--md3-neutral-secondary); font-size: 12px; }
    .addchip { width: 48px; height: 48px; border-radius: 8px; border: 1px dashed var(--md3-outline-variant); display: grid; place-items: center; color: var(--md3-on-primary-container); }
    .switch { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; color: var(--ink); }
    .switch .trk { width: 36px; height: 20px; border-radius: 10px; background: var(--md3-outline-variant); position: relative; transition: background-color 200ms var(--ease); }
    .switch .trk::after { content: ""; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; border-radius: 50%; background: var(--white); transition: transform 200ms var(--ease); }
    .switch[aria-pressed="true"] .trk { background: var(--md3-primary); }
    .switch[aria-pressed="true"] .trk::after { transform: translateX(16px); }
    .callout { background: var(--white); border-radius: var(--radius); padding: var(--sp-32) var(--sp-24); margin-top: var(--sp-16); display: grid; justify-items: center; gap: var(--sp-8); text-align: center; }
    .callout .ei { width: 56px; height: 56px; border-radius: 50%; display: grid; place-items: center; background: var(--md3-background); color: var(--md3-on-primary-container); margin-bottom: 4px; }
    .callout b { color: var(--head); }
    .callout p { color: var(--ink); max-width: 56ch; }
    .callout .btn { flex: none; padding: 0 var(--sp-20); margin-top: var(--sp-8); text-decoration: none; }
    .menu { position: fixed; z-index: 35; min-width: 220px; background: var(--white); border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,.16); padding: 6px; display: grid; }
    .menu[hidden] { display: none; }
    .menu button { display: flex; align-items: center; gap: 10px; min-height: 44px; padding: 0 12px; border-radius: 6px; text-align: left; color: var(--head); }
    @media (hover: hover) { .menu button:hover { background: var(--md3-background); } }
    .menu button.danger { color: var(--md3-error); }
    .htab { width: 100%; border-collapse: collapse; }
    .htab th { text-align: left; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; color: var(--ink); background: var(--md3-surface-variant); padding: 8px 10px; }
    .htab td { padding: 10px; border-top: 1px solid var(--md3-surface-variant); vertical-align: top; color: var(--head); }
    .htab td small { display: block; color: var(--md3-neutral-secondary); }
    /* plan card: plan chips, then the selected plan (one surface instead of two) */
    .dpane.plan { margin-top: var(--sp-16); }
    .dp-top { display: flex; align-items: center; justify-content: space-between; gap: var(--sp-12); flex-wrap: wrap; }
    .dp-top h3 { color: var(--head); }
    /* the diet's actions stay in reach while the items table scrolls (tablet) */
    .dpane.plan .dp-head { position: sticky; top: 0; z-index: 3; background: var(--white); margin: -8px 0; padding: 8px 0; }
    .dp-btns { display: flex; flex-wrap: wrap; justify-content: flex-end; gap: var(--sp-12); flex: none; max-width: 50%; }
    .cobtns { display: flex; flex-wrap: wrap; justify-content: center; gap: var(--sp-12); }
    /* touch targets: 48px on the species views (shared components keep their size elsewhere) */
    #p-species .seg3 button, #spanel .dseg button, #p-species .dseg button { min-height: 48px; }
    #p-species .list-bar .chip { height: 48px; }
    #spanel > .bar .iconbtn, #rqf .iconbtn { width: 48px; height: 48px; }
    #spanel > .bar .asbtn { min-height: 48px; }
    #spanel .tag, .sp-detail .tag { font-size: 13px; height: 26px; }
    .dp-head .tags + .dp-applies { margin-top: 4px; }
    .dp-applies { color: var(--head); }
    .dp-meta, .dp-none { color: var(--ink); }
    .dp-edit { flex: none; min-height: 44px; padding: 0 var(--sp-16); gap: 6px; }
    .sp-detail .tag.grey, #spanel .tag.grey { color: var(--ink); }
    /* "Also used by" species list: collapsed by default */
    .shared summary { display: flex; align-items: center; gap: var(--sp-8); min-height: 44px; margin: -8px 0; cursor: pointer; list-style: none; color: var(--head); border-radius: 8px; }
    .shared summary::-webkit-details-marker { display: none; }
    .shared summary svg { flex: none; transform: rotate(-90deg); color: var(--md3-on-primary-container); }
    .shared[open] summary svg { transform: none; }
    @media (prefers-reduced-motion: no-preference) { .shared summary svg { transition: transform 150ms var(--ease); } }
    .shlist { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 4px var(--sp-12); }
    .shrow { width: 100%; min-height: 44px; display: grid; gap: 2px; padding: 6px 8px; border-radius: 8px; text-align: left; }
    a.shrow { text-decoration: none; }
    .shrow span { color: var(--md3-on-surface); }
    .shrow i { color: var(--ink); }
    @media (hover: hover) { .shrow:hover { background: var(--md3-background); } }
    /* species detail as one section: summary, scope and diet share one surface, separated by space and headings */
    .spsheet { background: var(--white); border-radius: var(--radius); padding: var(--sp-20) var(--sp-24) var(--sp-24); display: grid; gap: var(--sp-32); }
    .spsheet > .hero, .spsheet > .card2, .spsheet > .dpane, .spsheet > .callout { background: none; border-radius: 0; padding: 0; margin: 0; }
    .spsheet > .callout { padding: var(--sp-8) 0; }
    @media (orientation: landscape) {
      .tscroll { max-height: 296px; }
      .sp-split { grid-template-columns: minmax(0, 2fr) minmax(0, 3fr); }
      .sp-split .spcards { grid-template-columns: minmax(0, 1fr); }
      .sp-detail { display: block; position: sticky; top: var(--sp-16); max-height: calc(100dvh - var(--status-h) - 138px - 32px); overflow-y: auto; border-radius: var(--radius); }
    }
'''

exec(open(os.path.join(HERE, 'wiz.py')).read())

SP_JS = '''  /* ---------------- Diet by Species (Dev system diet/by-species: data, scopes, plans, detail) ---------------- */
  var BSD = ''' + BS_EMBED + ''';
  function SpModule(root) {
    var SPECIES = BSD.species, PLANS = BSD.plans, BY = {};
    SPECIES.forEach(function (s) { BY[s.tsn] = s; });
    RQ.restorePlans(PLANS, BY);
    /* locked DEC-11: time-bound diets switch back to the base diet automatically once their end date has passed */
    Object.keys(PLANS).forEach(function (k) { var p = PLANS[k]; if (p.active && p.to && !p.recurring && p.kind !== 'base' && p.to < RQ.today()) { p.active = false; p.ended = true; } });
    /* a scheduled request goes live on its effective date: the proposed diet becomes active (and replaces the diet it changes) */
    HOOKS.golive = function (r) { var p = PLANS[r.proposedId]; if (!p || !p.proposed) return; p.proposed = false; p.active = true; p.verified = true; p.fromReq = r.id;
      if (r.end) { p.from = RQ.effStart(r); p.to = r.end; if (p.kind === 'base') p.kind = 'time-bound'; } if (p.editOf && PLANS[p.editOf] && !(p.from || p.to)) PLANS[p.editOf].active = false; RQ.keepPlan(p); };
    REQS_ALL.filter(function (r) { return r.status === 'live'; }).forEach(HOOKS.golive);
    /* Dieticians with diet write permission can edit any active diet. Read-only roles still use the request flow. */
    function mayEdit(s) { return !!s && RQ.can('write'); }
    HOOKS.planOf = function (id) { return id ? PLANS[id] || null : null; };
    HOOKS.currentOf = function (r) { var s = BY[r.tsn]; if (!s) return null; if (r.planId && PLANS[r.planId]) return PLANS[r.planId]; return scopePlansFor(s, r.scope, r.scope === 'species' ? null : r.scopeRef).filter(isDefault)[0] || basePlan(s); };
    HOOKS.editPlan = function (tsn, id) { var p = PLANS[id]; if (!p || !p.active || !BY[tsn]) return; if (!mayEdit(BY[tsn])) { toast('You do not have permission to edit diets.'); return; } st.seg = 'all'; st.tsn = tsn; resetScope(); st.plan = id; applyPlan(BY[tsn]); openEdit(p); };   /* Directory Edit */
    var CLS = [['mammalia', 'Mammalia'], ['aves', 'Aves'], ['reptilia', 'Reptilia'], ['other', 'Other']];
    var SCOPES = [['species', 'Species-wide'], ['site', 'Site-wide'], ['section', 'Section-wide'], ['enclosure', 'Enclosure-wide'], ['animal', 'Animal-wide']];
    var KIND = { base: ['yearround', 'Year-round'], seasonal: ['seasonal', 'Seasonal'], 'time-bound': ['timebound', 'Time-bound'], 'sex-based': ['yearround', 'Sex-based'], combined: ['seasonal', 'Combined'] };
    var KICON = { yearround: 'time', seasonal: 'star', timebound: 'calendar' };
    var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    var NUT = [['Macros', [['energy', 'Energy', 'kcal'], ['protein', 'Protein', 'g'], ['fat', 'Fat', 'g'], ['carbohydrate', 'Carbohydrate', 'g'], ['fiber', 'Fiber', 'g'], ['moisture', 'Moisture', '%']]],
      ['Minerals', [['calcium', 'Calcium', 'mg'], ['phosphorus', 'Phosphorus', 'mg']]],
      ['Vitamins', [['vitaminA', 'Vitamin A', 'IU'], ['vitaminD', 'Vitamin D', 'IU'], ['vitaminE', 'Vitamin E', 'mg'], ['vitaminC', 'Vitamin C', 'mg']]]];
    var SEGS = [['all', 'All'], ['with', 'Species with diet'], ['without', 'Species without diet']];
    var st = { seg: 'all', q: '', cls: [], ver: '', sort: 'count', tsn: null, plan: null, scope: 'species', ref: null, tab: 'items', showInactive: false, shOpen: false, tFiltersOpen: false, hist: { scope: 'all', kind: 'all', seg: 'diets' } };

    function plansOf(s) { return (s.plans || []).map(function (id) { return PLANS[id]; }).filter(Boolean); }
    function activeN(s) { return plansOf(s).filter(function (p) { return p.active; }).length; }
    function hasDiet(s) { return !!s.diet; }
    function clsOf(s) { var c = (s.cls || '').toLowerCase(); return ['mammalia', 'aves', 'reptilia'].indexOf(c) !== -1 ? c : 'other'; }
    function clsName(s) { var c = clsOf(s); for (var i = 0; i < CLS.length; i++) if (CLS[i][0] === c) return CLS[i][1]; return 'Other'; }
    function shownId(p) { return 'D-' + (p.sharedFrom || p.id); }
    function ddmmyy(iso) { return iso ? iso.slice(8, 10) + '-' + iso.slice(5, 7) + '-' + iso.slice(2, 4) : '-'; }
    function ddmm(iso) { return iso ? iso.slice(8, 10) + '-' + iso.slice(5, 7) : '-'; }
    function compact(iso) { return iso ? Number(iso.slice(8, 10)) + ' ' + MON[Number(iso.slice(5, 7)) - 1] : ''; }
    function initials(n) { return n.split(/[\\s-]+/).filter(Boolean).slice(0, 2).map(function (w) { return w[0]; }).join('').toUpperCase(); }
    function uniq(a, k) { var s = {}; return a.filter(function (x) { var v = k(x); if (s[v]) return false; s[v] = 1; return true; }); }
    function locOf(s) {
      var e = s.enclosures || [];
      return { sites: uniq(e, function (x) { return x.siteId; }).map(function (x) { return { id: x.siteId, name: x.site }; }),
        sections: uniq(e, function (x) { return x.sectionId; }).map(function (x) { return { id: x.sectionId, name: x.section, site: x.site, siteId: x.siteId }; }), enclosures: e };
    }
    function isBase(p) { return p.active && p.scope === 'species' && p.kind === 'base'; }
    function kindTag(p) { var k = KIND[p.kind] || KIND.base; return '<span class="ttag ' + k[0] + ' t-body-medium">' + ic(KICON[k[0]], 16) + k[1] + '</span>'; }
    function windowText(p) {
      if (p.proposed) return ['off', 'Proposed · not active'];
      if (!p.active) return ['inactive', 'Inactive'];
      var f = p.recurring ? ddmm : ddmmyy;
      if (p.from || p.to) return ['current', (p.from ? f(p.from) : '...') + ' → ' + (p.to ? f(p.to) : 'open') + (p.recurring ? ' · yearly' : '')];
      return ['current', 'all year · Since ' + ddmmyy(p.created)];
    }
    function animalLabel(a) { return a.label || ((a.group ? 'Group of ' + a.group : 'Animal') + ' #' + a.id); }
    function encById(s, id) { return (s.enclosures || []).filter(function (e) { return e.id === id; })[0]; }
    function dmy(iso) { return iso ? compact(iso) + ' ' + iso.slice(0, 4) : ''; }
    /* the year-round diet that feeds a target: its own override, else the nearest parent override, else the species base */
    var SCN = { site: 'Site', section: 'Section', enclosure: 'Enclosure', animal: 'Animal' };
    function yrAt(s, scope, ref) { return ref == null ? null : plansOf(s).filter(function (p) { return p.active && p.kind === 'base' && p.scope === scope && p.ref === ref; })[0] || null; }
    function parentsOf(s, scope, ref) {
      if (scope === 'animal') { var a = (s.animalList || []).filter(function (x) { return x.id === ref; })[0], e = a && encById(s, a.enclosure); return e ? [['enclosure', e.id], ['section', e.sectionId], ['site', e.siteId]] : []; }
      if (scope === 'enclosure') { var en = encById(s, ref); return en ? [['section', en.sectionId], ['site', en.siteId]] : []; }
      if (scope === 'section') { var sc = locOf(s).sections.filter(function (x) { return x.id === ref; })[0]; return sc ? [['site', sc.siteId]] : []; }
      return [];
    }
    function inherited(s, scope, ref) { var l = parentsOf(s, scope, ref); for (var i = 0; i < l.length; i++) { var p = yrAt(s, l[i][0], l[i][1]); if (p) return p; } return basePlan(s); }
    function effOf(s, scope, ref) { return (scope !== 'species' && yrAt(s, scope, ref)) || inherited(s, scope, ref); }
    function rowLabel(s, scope, ref, n) { var y = yrAt(s, scope, ref); if (!n) return srcLabel(inherited(s, scope, ref)); return y ? srcLabel(y) + (n > 1 ? ' + ' + plural(n - 1, 'dated plan') : '') : plural(n, 'dated plan'); }
    function srcLabel(p) { return !p ? 'No diet' : p.scope === 'species' ? 'Species diet ' + shownId(p) : SCN[p.scope] + ' diet ' + shownId(p); }
    function match(s) {
      var q = st.q.trim().toLowerCase();
      return (!q || (s.name + ' ' + s.sci + ' ' + s.tsn).toLowerCase().indexOf(q) !== -1) && (!st.cls.length || st.cls.indexOf(clsOf(s)) !== -1) &&
        (!st.ver || (st.ver === 'certified' ? s.verified : !s.verified));
    }
    function inSeg(s, t) { return t === 'all' || (t === 'with' ? hasDiet(s) : !hasDiet(s)); }

    root.innerHTML =
      '<div class="segwrap"><div class="seg3" role="tablist" aria-label="Diet coverage" data-seg></div></div>' +
      '<div class="spband"><label class="spsearch">' + ic('search', 20) + '<span class="sr-only">Search species</span><input class="t-body-regular" type="search" data-q placeholder="Search species or taxonomy ID" autocomplete="off"></label>' +
      '<button class="spfilter" type="button" data-fbtn aria-pressed="false" aria-label="Filters">' + ic('filter-2', 24) + '<span class="t-minor-medium" data-fn hidden></span></button></div>' +
      '<div data-chips hidden><div class="segrow" role="group" aria-label="Class" data-clsrow></div><div class="segrow" role="group" aria-label="Certification" data-verrow></div></div>' +
      '<div class="list-bar"><h2 class="t-minor-medium" data-count aria-live="polite"></h2><button class="chip t-body-medium" type="button" data-sort>' + ic('sort', 18) + '<span data-sortl></span></button></div>' +
      '<div class="sp-split"><div data-list></div><div class="sp-detail" data-detail></div></div>';
    var $ = function (s) { return root.querySelector(s); };

    /* ---------- list ---------- */
    function card(s) {
      var n = activeN(s), on = LAND.matches && s.tsn === st.tsn;
      var right = hasDiet(s) ? '<span class="spn"><span class="v t-stat-title">' + n + '</span><span class="l t-body-regular">' + (n === 1 ? 'Active diet' : 'Active diets') + '</span></span>' : '<span class="spn"><span class="gap t-body-medium">No diet yet</span></span>';
      return '<div class="spwrap"><button class="spcard" type="button" data-tsn="' + s.tsn + '"' + (on ? ' aria-current="true"' : '') + ' aria-label="Open ' + esc(s.name) + '"><span class="spav t-minor-title" aria-hidden="true">' + initials(s.name) + '</span>' +
        '<span class="grow"><span class="n t-minor-title">' + esc(s.name) + '</span><span class="m t-minor-italic">' + esc(s.sci) + '</span><span class="c t-body-regular">' + clsName(s) + ' • ' + plural(s.animals || 0, 'animal') + (s.verified ? ' • Certified' : '') + '</span></span>' +
        right + '<span class="go">' + ic('dropdown', 24) + '</span></button></div>';
    }
    function sortL(list) { list.sort(function (a, b) { return st.sort === 'name' ? a.name.localeCompare(b.name) : (activeN(b) - activeN(a)) || a.name.localeCompare(b.name); }); return list; }
    function visibleList() { return sortL(SPECIES.filter(match).filter(function (s) { return inSeg(s, st.seg); })); }
    function drawList() {
      var base = SPECIES.filter(match);
      $('[data-seg]').innerHTML = SEGS.map(function (t) { return '<button type="button" role="tab" class="t-body-medium" data-s="' + t[0] + '" aria-selected="' + (st.seg === t[0]) + '">' + t[1] + ' - ' + base.filter(function (s) { return inSeg(s, t[0]); }).length + '</button>'; }).join('');
      var list = visibleList(), L = $('[data-list]');
      $('[data-count]').textContent = 'Species (' + list.length + ')';
      if (LAND.matches && list.length && !list.some(function (s) { return s.tsn === st.tsn; })) { st.tsn = list[0].tsn; st.plan = null; resetScope(); }
      var empty = '<div class="empty"><span class="ei">' + ic('search', 24) + '</span><b class="t-minor-title">No species match</b><span class="t-body-regular">Try a common or scientific name, a taxonomy ID, or clear the filters.</span></div>';
      if (st.seg === 'all') {
        var w = list.filter(hasDiet), wo = list.filter(function (s) { return !hasDiet(s); });
        L.className = 'spgroups';
        L.innerHTML = !list.length ? empty : [['Species with diet', w], ['Species without diet', wo]].map(function (g) {
          return '<section class="spgroup" aria-label="' + g[0] + '"><h3 class="spgroup__h t-minor-title">' + g[0] + ' (' + g[1].length + ')</h3>' +
            (g[1].length ? '<div class="spcards">' + g[1].map(card).join('') + '</div>' : '<p class="spgroup__none t-body-regular">None match the search or filter.</p>') + '</section>';
        }).join('');
      } else { L.className = 'spcards'; L.innerHTML = list.length ? list.map(card).join('') : empty; }
      var nf = st.cls.length + (st.ver ? 1 : 0);
      $('[data-fn]').hidden = !nf; $('[data-fn]').textContent = nf; $('[data-fbtn]').classList.toggle('on', nf > 0);
      $('[data-clsrow]').innerHTML = '<span class="rowlabel t-body-medium">Class</span>' + CLS.map(function (c) { return '<button type="button" class="spchip t-body-medium" data-cl="' + c[0] + '" aria-pressed="' + (st.cls.indexOf(c[0]) !== -1) + '">' + c[1] + '</button>'; }).join('');
      $('[data-verrow]').innerHTML = '<span class="rowlabel t-body-medium">Certification</span>' + [['', 'All'], ['certified', 'Certified'], ['uncertified', 'Uncertified']].map(function (v) { return '<button type="button" class="spchip t-body-medium" data-vr="' + v[0] + '" aria-pressed="' + (st.ver === v[0]) + '">' + v[1] + '</button>'; }).join('');
      $('[data-sortl]').textContent = st.sort === 'name' ? 'Name A-Z' : 'Most diets';
    }

    /* ---------- detail ---------- */
    function resetScope() { st.scope = 'species'; st.ref = null; st.tab = 'items'; st.showInactive = false; st.tq = ''; st.tf = ''; st.tsx = ''; st.tlimit = 40; }
    function applyPlan(s) {
      var p = st.plan != null ? PLANS[st.plan] : null;
      if (p && p.species === s.tsn) { st.scope = p.scope; st.ref = p.scope === 'species' ? null : p.ref; if (!p.active) st.showInactive = true; }
      else st.plan = null;
    }
    function plansHere(s) { return plansOf(s).filter(function (p) { return p.scope === st.scope && (st.scope === 'species' || p.ref === st.ref); }); }
    function activeAt(s, scope, ref) { return plansOf(s).filter(function (p) { return p.active && p.scope === scope && (ref == null || p.ref === ref); }).length; }
    /* requests for this species: rows shared by the Diet history "Requests" segment */
    var REQ_TL = { temporary: 'Temporary', base: 'Base diet change', site: 'Site / Section', animal: 'Animal' };
    var REQ_SUBTAG = { review: 'orange', configuring: 'teal', sentback: 'red', kitchen: 'orange', delayed: 'orange', done: 'green' };
    function spReqs(s) { return RQ.visible().filter(function (r) { return r.tsn === s.tsn; }); }
    function reqRow(r) {
      RQ.decorate(r);
      var hd = RQ.can('configure'), sb = RQ.hdSub(r), nx = hd ? RQ.hdNext(r) : null, pt = RQ.propText(r);
      var tag = hd && RQ.isOpen(r) ? '<span class="tag ' + (REQ_SUBTAG[sb] || 'grey') + '">' + esc(sb === 'delayed' ? RQ.downLabel(r) : RQ.SUBL[sb] || r.label) + '</span>' : '<span class="tag ' + (r.tone === 'ok' ? 'green' : r.tone === 'bad' ? 'red' : 'orange') + '">' + esc(r.label) + '</span>';
      return '<button type="button" class="sreq" data-rqopen="' + r.id + '"><span class="ribbon ' + r.prio + '" aria-label="' + RQ.PRI[r.prio][1] + ' priority">' + RQ.PRI[r.prio][0] + '</span><span class="grow"><b class="t-body-title">' + esc(r.id + ' · ' + r.title) + '</b>' +
        '<span class="t-body-regular">' + esc((REQ_TL[r.type] || r.type) + ' · ' + (r.scopeText || 'Whole species') + (r.season ? ' · every year ' + r.season.from.split('-').reverse().join('-') + ' to ' + r.season.to.split('-').reverse().join('-') : r.start ? ' · ' + RQ.fmt(r.start) + (r.end ? ' to ' + RQ.fmt(r.end) : ' onwards') : '')) + '</span><small class="t-body-regular">' + esc(r.by.name + ', ' + r.by.role) + '</small>' +
        (nx ? '<small class="t-body-medium nx">' + esc(nx[1]) + '</small>' : '') + (pt ? '<small class="t-body-medium dx">' + ic('book', 14) + esc(pt) + (r.proposedId ? ' (Proposed)' : '') + '</small>' : '') + '</span>' + tag + '</button>';
    }
    function reqGroups(s) {
      var list = spReqs(s), open = list.filter(RQ.isOpen), closed = list.filter(function (r) { return !RQ.isOpen(r); }), g = [];
      var byPri = function (a, b) { return ({ high: 0, medium: 1, low: 2 }[a.prio] - { high: 0, medium: 1, low: 2 }[b.prio]) || a.iso.localeCompare(b.iso); };
      if (RQ.can('configure')) {
        var todo = open.filter(function (r) { return RQ.hdBucket(r) === 'todo'; }), mine = open.filter(function (r) { return RQ.hdBucket(r) === 'mine'; }), other = open.filter(function (r) { return todo.indexOf(r) === -1 && mine.indexOf(r) === -1; });
        if (todo.length) g.push(['To configure', todo.sort(byPri), true]); if (mine.length) g.push(['Configured by me', mine.sort(byPri)]); if (other.length) g.push(['Other', other.sort(byPri)]);
      } else if (open.length) g.push(['Open', open.sort(byPri)]);
      if (closed.length) g.push(['Closed', closed.sort(function (a, b) { return b.iso.localeCompare(a.iso); })]);
      return { n: list.length, open: open.length, todo: RQ.can('configure') ? open.filter(function (r) { return RQ.hdBucket(r) === 'todo'; }).length : 0, groups: g };
    }
    function hero(s) {
      var L = locOf(s), n = activeN(s), rg = reqGroups(s);
      var meta = '<span class="hero__meta t-body-regular">Taxonomy ID ' + s.tsn + ' <span class="tag teal">' + clsName(s) + '</span>' + (s.verified ? '<span class="tag green">Certified</span>' : '') + '</span>';
      var name = LAND.matches ? '<h2 class="t-major-title">' + esc(s.name) + '</h2><i class="t-minor-italic">' + esc(s.sci) + '</i>' : '';
      return '<section class="hero" aria-label="Species summary"><div class="hero__in">' +
        '<div class="hero__top"><span class="hero__nm">' + name + meta + '</span></div>' +
        '<div class="hero__row"><div class="hero__stats" role="group" aria-label="Summary">' +
        '<span class="stx"><span class="v t-stat-title">' + (s.animals || 0) + '</span><span class="l t-body-regular">' + (s.animals === 1 ? 'Animal' : 'Animals') + '</span></span>' +
        '<span class="stx"><span class="v t-stat-title">' + L.sites.length + '</span><span class="l t-body-regular">' + (L.sites.length === 1 ? 'Site' : 'Sites') + '</span></span>' +
        '<span class="stx ok"><span class="v t-stat-title">' + n + '</span><span class="l t-body-regular">' + (n === 1 ? 'Active diet' : 'Active diets') + '</span></span></div>' +
        '<div class="hero__sec"><button type="button" class="chip t-body-medium hist' + (rg.todo ? ' due' : '') + '" data-history aria-label="Diet history' + (rg.open ? ', ' + plural(rg.open, 'open request') + (rg.todo ? ', ' + rg.todo + ' to configure' : '') : '') + '">' + ic('history', 18) + 'Diet history' + (rg.open ? '<span class="hcount">' + rg.open + '</span>' : '') + '</button></div></div>' +
        '</div></section>';
    }
    /* ---------- scope target list: search, quick filters, scroll area, capped rendering ---------- */
    var NOUN = { site: ['site', 'sites'], section: ['section', 'sections'], enclosure: ['enclosure', 'enclosures'], animal: ['animal', 'animals'] };
    var PH = { site: 'Search sites', section: 'Search sections', enclosure: 'Search enclosures', animal: 'Search by animal ID, name, sex or enclosure' };
    function hlq(t, q) { t = String(t); if (!q) return esc(t); var i = t.toLowerCase().indexOf(q); return i < 0 ? esc(t) : esc(t.slice(0, i)) + '<mark>' + esc(t.slice(i, i + q.length)) + '</mark>' + esc(t.slice(i + q.length)); }
    function targetRows(s) {
      var L = locOf(s), out = [];
      if (st.scope === 'site') L.sites.forEach(function (x) { var n = activeAt(s, 'site', x.id); out.push({ g: '', ref: x.id, name: x.name, where: '', n: n, has: n > 0, extra: rowLabel(s, 'site', x.id, n), find: x.name }); });
      if (st.scope === 'section') L.sections.slice().sort(function (a, b) { return L.sites.map(function (z) { return z.name; }).indexOf(a.site) - L.sites.map(function (z) { return z.name; }).indexOf(b.site); }).forEach(function (x) { var n = activeAt(s, 'section', x.id); out.push({ g: x.site, ref: x.id, name: x.name, where: plural(L.enclosures.filter(function (e) { return e.sectionId === x.id; }).length, 'enclosure'), n: n, has: n > 0, extra: rowLabel(s, 'section', x.id, n), find: x.name + ' ' + x.site }); });
      if (st.scope === 'enclosure') L.sections.forEach(function (sec) { L.enclosures.filter(function (e) { return e.sectionId === sec.id; }).forEach(function (e) { var n = activeAt(s, 'enclosure', e.id); out.push({ g: sec.site + ' › ' + sec.name, ref: e.id, name: e.name, where: plural(e.animals || 0, 'animal'), n: n, has: n > 0, extra: rowLabel(s, 'enclosure', e.id, n), find: e.name + ' ' + sec.name + ' ' + sec.site }); }); });
      if (st.scope === 'animal') {
        var own = plansOf(s).filter(function (p) { return p.active && p.scope === 'animal'; });
        (s.animalList || []).forEach(function (a) { var e = encById(s, a.enclosure), sx = a.sex === 'm' ? 'Male' : a.sex === 'f' ? 'Female' : 'Undetermined', eff = effOf(s, 'animal', a.id),
          more = own.filter(function (p) { return p.ref === a.id && p !== eff; }).length, c = !!(eff && eff.scope !== 'species') || more > 0;
          out.push({ o: e ? (s.enclosures || []).indexOf(e) : 999, so: e ? L.sections.map(function (x) { return x.id; }).indexOf(e.sectionId) : 999, g: e ? e.site + ' › ' + e.section : '', ref: a.id, name: animalLabel(a), sub: a.label ? '#' + a.id : '', where: sx + (e ? ' · ' + e.name : ''), sex: a.sex, custom: c, extra: srcLabel(eff) + (more ? ' + ' + plural(more, 'dated plan') : ''), has: c,
            find: [a.id, '#' + a.id, a.label || '', sx, e ? e.name : '', e ? e.section : ''].join(' ') }); });
        out.sort(function (a, b) { return (a.so - b.so) || (b.custom - a.custom) || (a.o - b.o) || String(a.name).localeCompare(String(b.name)); });
      }
      return out;
    }
    function filteredTargets(s) {
      var all = targetRows(s), q = (st.tq || '').trim().toLowerCase();
      var rows = all.filter(function (r) {
        if (q && r.find.toLowerCase().indexOf(q) === -1) return false;
        if (st.tf === 'has' && !r.has) return false; if (st.tf === 'none' && r.has) return false;
        if (st.tf === 'custom' && !r.custom) return false; if (st.tf === 'species' && r.custom) return false;
        if (st.tsx && r.sex !== st.tsx) return false;
        return true;
      });
      return { all: all, rows: rows, q: q };
    }
    function targetsShell() {
      var menu = '', filterable = st.scope === 'enclosure' || st.scope === 'animal', nf = (st.tf ? 1 : 0) + (st.tsx ? 1 : 0);
      if (filterable) {
        var dietOpts = (st.scope === 'enclosure' ? [['', 'All'], ['has', 'Own diet'], ['none', 'Inherited']] : [['', 'All'], ['custom', 'Own diet'], ['species', 'Species diet']]).map(function (c) {
          return '<button type="button" class="spchip t-body-medium" data-tf="' + c[0] + '" aria-pressed="' + ((st.tf || '') === c[0]) + '">' + c[1] + '</button>';
        }).join('');
        menu = '<button type="button" class="tfilterbtn' + (nf ? ' on' : '') + '" data-tfilters aria-label="Filters' + (nf ? ', ' + nf + ' active' : '') + '" aria-haspopup="dialog" aria-expanded="' + st.tFiltersOpen + '">' +
          ic('filter-2', 24) + (nf ? '<span class="n" aria-hidden="true">' + nf + '</span>' : '') + '</button>' +
          '<div class="tfiltermenu" data-tfiltermenu role="dialog" aria-label="Filters"' + (st.tFiltersOpen ? '' : ' hidden') + '><div class="tfiltergroup"><span>Diet source</span><div class="tfilteropts" role="group" aria-label="Diet source">' + dietOpts + '</div></div>' +
          (st.scope === 'animal' ? '<div class="tfiltergroup"><span>Sex</span><div class="tfilteropts" role="group" aria-label="Sex">' + [['m', 'Male'], ['f', 'Female']].map(function (c) { return '<button type="button" class="spchip t-body-medium" data-tsx="' + c[0] + '" aria-pressed="' + (st.tsx === c[0]) + '">' + c[1] + '</button>'; }).join('') + '</div></div>' : '') +
          (nf ? '<button type="button" class="tfilterclear t-body-medium" data-tclearfilters>Clear filters</button>' : '') + '</div>';
      }
      return '<div class="ttools"><div class="tsearchrow"><label class="spsearch">' + ic('search', 20) + '<span class="sr-only">' + PH[st.scope] + '</span><input class="t-body-regular" type="search" data-tq placeholder="' + PH[st.scope] + '" value="' + esc(st.tq || '') + '" autocomplete="off"></label>' + menu + '</div>' +
        '<p class="tcount t-body-regular" data-tcount aria-live="polite"></p></div>' +
        '<div class="tbox" data-tbox><div class="tscroll targets" data-tscroll></div></div>';
    }
    function drawTargets() {
      var box = host() && host().querySelector('[data-tscroll]'); if (!box) return;
      var s = BY[st.tsn], f = filteredTargets(s), N = NOUN[st.scope], lim = st.tlimit || 40, rows = f.rows.slice(0, lim), html = '', lastG = null;
      host().querySelector('[data-tcount]').textContent = f.rows.length === f.all.length ? plural(f.all.length, N[0], N[1]) : 'Showing ' + f.rows.length + ' of ' + f.all.length + ' ' + N[1];
      rows.forEach(function (r) {
        if (r.g && r.g !== lastG) { html += '<p class="tgh">' + esc(r.g) + '</p>'; lastG = r.g; }
        html += '<button type="button" class="tgt" data-ref="' + r.ref + '" aria-pressed="' + (st.ref === r.ref) + '"><span class="grow"><b class="t-body-title">' + hlq(r.name, f.q) + (r.sub ? ' <span class="tid">' + hlq(r.sub, f.q) + '</span>' : '') + '</b>' + (r.where ? '<span class="t-body-regular">' + hlq(r.where, f.q) + '</span>' : '') + '</span>' +
          (openReqs(s, st.scope, r.ref).length ? '<span class="rqb">' + ic('time', 14) + plural(openReqs(s, st.scope, r.ref).length, 'open request') + '</span>' : '') +
          '<span class="d t-body-medium' + (r.has ? '' : ' none') + '">' + esc(r.extra || plural(r.n, 'diet')) + '</span></button>';
      });
      if (f.rows.length > lim) html += '<button type="button" class="chip t-body-medium tmore" data-tmore>Show ' + Math.min(40, f.rows.length - lim) + ' more (' + (f.rows.length - lim) + ' left)</button>';
      if (!f.rows.length) html = '<div class="tempty"><b class="t-body-title">No ' + N[1] + ' match' + (f.q ? ' "' + esc(st.tq.trim()) + '"' : ' these filters') + '</b><span class="t-body-regular">Try another ' + (st.scope === 'animal' ? 'ID, name, sex or enclosure' : 'name') + ', or clear the filters.</span><button type="button" class="chip t-body-medium" data-tclear>Clear search and filters</button></div>';
      box.innerHTML = html; fades();
    }
    function fades() { var h = host(), b = h && h.querySelector('[data-tscroll]'); if (!b) return; var p = b.parentNode; p.classList.toggle('ft', b.scrollTop > 2); p.classList.toggle('fb', b.scrollTop + b.clientHeight < b.scrollHeight - 2); }
    function resetTargets() { st.tq = ''; st.tf = ''; st.tsx = ''; st.tlimit = 40; st.tFiltersOpen = false; }
    function scopeCard(s) {
      var L = locOf(s), all = plansOf(s), cnt = function (sc) { return all.filter(function (p) { return p.active && p.scope === sc; }).length; };
      var custom = (s.animalList || []).filter(function (a) { var e = effOf(s, 'animal', a.id); return (e && e.scope !== 'species') || all.some(function (p) { return p.active && p.scope === 'animal' && p.ref === a.id; }); }).length;
      var siteHidden = L.sites.length <= 1 && cnt('site') === 0;
      var sub = { species: plural(cnt('species'), 'diet'), site: plural(cnt('site'), 'diet') + ' · ' + plural(L.sites.length, 'site'), section: plural(cnt('section'), 'diet') + ' · ' + plural(L.sections.length, 'section'),
        enclosure: plural(cnt('enclosure'), 'diet') + ' · ' + plural(L.enclosures.length, 'enclosure'), animal: custom ? custom + ' with own diet' : basePlan(s) ? 'All on species diet' : 'No diet yet' };
      var h = '<section class="card2"><h3>Scope</h3><div class="scopes" role="group" aria-label="Scope">' + SCOPES.filter(function (x) { return !(x[0] === 'site' && siteHidden); }).map(function (x) {
        return '<button type="button" class="spchip t-body-medium" data-scope="' + x[0] + '" aria-pressed="' + (st.scope === x[0]) + '">' + x[1] + '<small>' + sub[x[0]] + '</small></button>';
      }).join('') + '</div>';
      if (st.scope !== 'species') h += targetsShell();
      return h + '</section>';
    }
    function refName(s, scope, ref) {
      var L = locOf(s), hit = function (l) { return (l.filter(function (x) { return x.id === ref; })[0] || {}).name; };
      if (scope === 'site') return hit(L.sites); if (scope === 'section') return hit(L.sections); if (scope === 'enclosure') return (encById(s, ref) || {}).name;
      var a = (s.animalList || []).filter(function (x) { return x.id === ref; })[0]; return a ? animalLabel(a) : '';
    }
    function planChips(s, here) {
      var inactive = here.filter(function (p) { return !p.active && !p.proposed; }), list = here.filter(function (p) { return p.active || p.proposed || st.showInactive; });
      var head = st.scope === 'species' ? 'Species-wide diets' : 'Diets for ' + (refName(s, st.scope, st.ref) || SCN[st.scope]);
      return '<div class="dp-top"><h3 class="t-minor-title" id="plansH">' + esc(head) + '</h3>' +
        (inactive.length ? '<button type="button" class="switch t-body-medium" data-showinactive aria-pressed="' + st.showInactive + '"><span class="trk" aria-hidden="true"></span>Show inactive (' + inactive.length + ')</button>' : '') + '</div>' +
        '<div class="pchips" role="group" aria-labelledby="plansH">' + list.map(function (p) {
          var parts = [];
          if (p.proposed) parts.push((p.editOf ? 'Change to ' + p.editOfLabel : 'Proposed') + ' · ' + p.fromReq);
          if (p.from || p.to) parts.push((p.from ? compact(p.from) : '…') + ' to ' + (p.to ? compact(p.to) : 'open'));
          if (p.sex) parts.push(p.sex === 'male' ? 'Male' : p.sex === 'female' ? 'Female' : 'Undetermined');
          if (!p.active && !p.proposed) parts.push('Inactive');
          return '<button type="button" class="pchip' + (p.active || p.proposed ? '' : ' off') + '" data-plan="' + p.id + '" aria-pressed="' + (p.id === st.plan) + '"><span class="l1">' + shownId(p) + kindTag(p) + '</span>' + (parts.length ? '<span class="l2">' + esc(parts.join(' · ')) + '</span>' : '') + '</button>';
        }).join('') + '<button type="button" class="addchip" data-newplan aria-label="Add seasonal or time-bound diet">' + ic('add', 24) + '</button></div>';
    }
    function fmt(v) { v = Number(v) || 0; return v.toLocaleString('en-IN', { maximumFractionDigits: 2 }); }
    function itemCell(it) {
      var m = it.mix, h = '<div class="it-n">' + esc(it.name) + (m ? '<span class="it-k">' + esc(m.label || 'MIX') + '</span>' : '') + '</div>';
      if (it.prep) h += '<div class="it-p t-body-regular">(' + esc(it.prep) + ')</div>';
      if (m && m.meta) h += '<div class="it-ex t-body-regular">' + esc(m.meta) + '</div>';
      if (m && m.parts && m.parts.length) h += '<div class="it-parts t-body-regular">' + m.parts.map(function (q) { q = typeof q === 'string' ? { name: q } : q; return '<span>' + esc(q.name) + (q.note ? ' <em>' + esc(q.note) + '</em>' : '') + '</span>'; }).join('') + '</div>';
      if (it.cut) h += '<div class="it-ex t-body-regular">' + esc(it.cut) + '</div>';
      (it.alts || []).forEach(function (a) { a = typeof a === 'string' ? { name: a } : a; var q = a.amount || a.ratio; h += '<div class="it-alt t-body-regular">or <b>' + esc(a.name) + '</b>' + (a.prep ? ' (' + esc(a.prep) + ')' : '') + (q ? ' · ' + esc(q) : '') + '</div>'; });
      if (it.notes) h += '<div class="it-ex t-body-regular">' + esc(it.notes) + '</div>';
      return h;
    }
    function table(p) {
      var sch = p.schedule || [], cols = p.columns || [];
      if (!sch.length) return '<div class="empty"><b class="t-minor-title">No items in this plan yet</b></div>';
      var rows = '';
      sch.forEach(function (b) {
        var n = 0; (b.days || []).forEach(function (g) { n += Math.max(1, (g.items || []).length); }); var first = true;
        (b.days || []).forEach(function (g) {
          var its = g.items && g.items.length ? g.items : [null];
          its.forEach(function (it, i) {
            rows += '<tr>' + (first ? '<td class="time" rowspan="' + n + '">' + esc(b.time) + '</td>' : '') + (i === 0 ? '<td class="day t-body-regular" rowspan="' + its.length + '">' + esc(g.day) + '</td>' : '') +
              (it ? '<td>' + itemCell(it) + '</td><td class="amt">' + esc(it.amount || '-') + '</td>' + cols.map(function (c, k) { return '<td class="amt">' + esc((it.extra || [])[k] || '-') + '</td>'; }).join('') : '<td colspan="' + (2 + cols.length) + '">No items</td>') + '</tr>';
            first = false;
          });
        });
      });
      return '<div class="dtab-wrap"><table class="dtab t-body-regular"><thead><tr><th>Time</th><th>Day</th><th>Item</th><th class="amt">Daily amt</th>' + cols.map(function (c) { return '<th class="amt">' + esc(c) + '</th>'; }).join('') + '</tr></thead><tbody>' + rows + '</tbody></table></div>';
    }
    function nutrition(p) {
      var nv = p.nutrition || {};
      return '<div class="nut"><p class="nut__help t-body-regular">' + ic('info', 20) + 'Per animal, per day. Totals across every item in this plan.</p>' + NUT.map(function (s) {
        return '<div class="nut__sec"><h4>' + s[0] + '</h4>' + s[1].map(function (r) { var v = Number(nv[r[0]]) || 0; return '<div class="nut__row t-body-regular"><span>' + r[1] + '</span><b class="' + (v === 0 ? 'zero' : '') + '">' + fmt(v) + ' <small>' + r[2] + '</small></b></div>'; }).join('') + '</div>';
      }).join('') + '</div>';
    }
    function whenText(p) {
      if (p.recurring && (p.from || p.to)) return compact(p.from) + ' to ' + compact(p.to) + ', every year';
      if (p.from || p.to) return (p.from ? dmy(p.from) : '…') + ' to ' + (p.to ? dmy(p.to) : 'open');
      return 'Year-round since ' + dmy(p.created);
    }
    function appliesText(s, p) {
      if (p.proposed) return p.editOf ? 'Proposed change to ' + p.editOfLabel + '. ' + p.editOfLabel + ' stays active until the change is applied.' : 'Proposed for ' + p.fromReq + '. The active diet does not change.';
      var b = basePlan(s);
      if (p.kind === 'base' && p.scope === 'species') return 'Base diet. Every site, section, enclosure and animal of this species gets it.';
      if (p.kind === 'base') return 'Replaces ' + (b ? shownId(b) : 'the base diet') + ' for ' + (p.scopeName || SCN[p.scope]) + '.';
      return 'Runs on top of the year-round diet for these dates.';
    }
    function retNote(s, p) { if (!p.to || p.kind === 'base') return ''; var b = basePlan(s);
      return '<p class="dp-meta t-body-regular">' + ic('history', 16) + ' ' + esc((p.recurring ? 'Each year after ' + compact(p.to) : 'After ' + dmy(p.to)) + ', automatically returns to ' + (b && b !== p ? 'base diet ' + shownId(b) : 'the base diet') + '.') + '</p>'; }
    function planCard(s, p, here) {
      var QM = { sex: 'By sex', weight: 'By weight', age: 'By age' };
      var h = '<section class="dpane plan" aria-labelledby="plansH">' + planChips(s, here);
      if (!p) return h + '<p class="t-body-regular dp-none">No active diet here. Turn on Show inactive to see earlier diets.</p></section>';
      var tags = (p.active || p.proposed ? '' : '<span class="tag grey">Inactive</span>') + (p.override ? '<span class="tag blue">Own diet</span>' : '') +
        '<span class="tag ' + (p.verified ? 'green' : 'grey') + '">' + (p.verified ? 'Verified' : 'Unverified') + '</span>' + (p.update === 'pending' ? '<span class="tag orange">Update pending</span>' : '') +
        (p.name ? '<span class="tag teal">' + esc(p.name) + '</span>' : '') + (QM[p.quantityMode] ? '<span class="tag teal">' + QM[p.quantityMode] + '</span>' : '');
      var meta = [whenText(p), 'Created by ' + (p.by || 'unknown'), p.dietitian ? 'Certified by ' + p.dietitian : 'Not certified'].join(' · ');
      var n = p.notes || {}, kv = '';
      if (st.tab === 'items' && n.kitchen) kv += '<dt>Kitchen</dt><dd>' + esc(n.kitchen) + '</dd>';
      if (st.tab === 'items' && n.site) kv += '<dt>Site</dt><dd>' + esc(n.site) + '</dd>';
      var reqs = RQ.visible().filter(function (r) { return RQ.isOpen(r) && r.tsn === p.species && (r.planId === p.id || (r.scope === p.scope && (p.scope === 'species' || r.scopeRef === p.ref))); });
      return h + '<div class="dp-head"><div class="grow"><div class="tags">' + tags + '</div>' +
        '<p class="dp-applies t-body-medium">' + esc(appliesText(s, p)) + '</p><p class="dp-meta t-body-regular">' + esc(meta) + '</p>' + retNote(s, p) + '</div>' +
        '<div class="dp-btns"><button type="button" class="btn teal dp-edit" data-rqnew="plan">' + ic('reason-or-list', 20) + 'Request diet change</button>' +
        (p.active ? '<button type="button" class="btn sec dp-edit" data-act="edit" aria-label="Edit ' + shownId(p) + '">' + ic('pencil', 20) + 'Edit</button>' : '') + '</div></div>' +
        (p.fromReq ? '<div class="rqline"><button type="button" class="rqb" data-rqopen="' + p.fromReq + '">' + ic('reason-or-list', 16) + 'Open request ' + p.fromReq + '</button></div>' : reqs.length ? '<div class="rqline">' + reqBadge(reqs) + '</div>' : '') +
        '<div class="dseg" role="group" aria-label="Diet view"><button type="button" data-dtab="items" aria-pressed="' + (st.tab === 'items') + '" class="t-body-medium">Items</button><button type="button" data-dtab="nutrition" aria-pressed="' + (st.tab === 'nutrition') + '" class="t-body-medium">Nutrition</button></div>' +
        (st.tab === 'nutrition' ? nutrition(p) : table(p)) +
        (kv ? '<div class="sub"><h4 class="t-minor-title">Notes</h4><dl class="kv t-body-regular">' + kv + '</dl></div>' : '') +
        (p.remark ? '<div class="remark t-body-regular">' + ic('info', 20) + '<div><b class="t-body-title">Remark</b><br>' + esc(p.remark) + '</div></div>' : '') +
        (p.reason ? '<p class="reason t-body-regular">' + ic('history', 20) + 'Reason <span class="tag orange">' + esc(p.reason) + '</span>' + (p.reasonDetail ? '<span>' + esc(p.reasonDetail) + '</span>' : '') + '</p>' : '') + '</section>';
    }
    /* a target with no plan of its own: show the diet it inherits, with a request path */
    function inheritedCard(s, p) {
      var nm = refName(s, st.scope, st.ref) || SCN[st.scope], from = p.scope === 'species' ? 'species' : SCN[p.scope].toLowerCase() + (p.scopeName ? ' ' + p.scopeName : '');
      var meta = [whenText(p), 'Created by ' + (p.by || 'unknown'), p.dietitian ? 'Certified by ' + p.dietitian : 'Not certified'].join(' · ');
      var reqs = openReqs(s, st.scope, st.ref);
      return '<section class="dpane plan" aria-labelledby="plansH"><div class="dp-top"><h3 class="t-minor-title" id="plansH">' + esc('Diet for ' + nm) + '</h3></div>' +
        '<div class="dp-head"><div class="grow"><div class="dp-id"><b class="t-medium-medium">' + shownId(p) + '</b>' + kindTag(p) + '</div>' +
        '<div class="tags"><span class="tag teal">' + esc((p.kind === 'base' && p.scope === 'species' ? 'Base diet · ' : '') + 'Inherited from ' + from) + '</span></div>' +
        '<p class="dp-meta t-body-regular">' + esc(meta) + '</p></div>' +
        '<div class="dp-btns"><button type="button" class="btn teal dp-edit" data-rqnew="scope">' + ic('reason-or-list', 20) + 'Request new diet</button>' +
        '<button type="button" class="addchip" data-newplan aria-label="Add seasonal or time-bound diet for ' + esc(nm) + '">' + ic('add', 24) + '</button></div></div>' +
        (reqs.length ? '<div class="rqline">' + reqBadge(reqs) + '</div>' : '') +
        '<div class="dseg" role="group" aria-label="Diet view"><button type="button" data-dtab="items" aria-pressed="' + (st.tab === 'items') + '" class="t-body-medium">Items</button><button type="button" data-dtab="nutrition" aria-pressed="' + (st.tab === 'nutrition') + '" class="t-body-medium">Nutrition</button></div>' +
        (st.tab === 'nutrition' ? nutrition(p) : table(p)) + '</section>';
    }
    function shared(s, p) {
      var others = uniq((p.sharers || []).filter(function (x) { return x[0] !== s.tsn; }), function (x) { return x[0]; });
      if (!others.length) return '';
      var key = p.sharedFrom || p.id;
      var list = others.map(function (x) { return { s: BY[x[0]] || { tsn: x[0], name: 'TSN ' + x[0] }, plan: x[1] }; }).sort(function (a, b) { return ((a.plan === key) ? 0 : 1) - ((b.plan === key) ? 0 : 1) || String(a.s.name).localeCompare(String(b.s.name)); });
      return '<details class="dpane shared" data-shared' + (st.shOpen ? ' open' : '') + '><summary class="t-minor-title">' + ic('dropdown', 20) + 'Also used by ' + plural(others.length, 'other species', 'other species') + '</summary>' +
        '<ul class="shlist">' + list.map(function (o) { return '<li><button type="button" class="shrow" data-goto="' + o.s.tsn + '" data-goplan="' + o.plan + '"><span class="t-body-title">' + esc(o.s.name) + '</span>' + (o.s.sci ? '<i class="t-body-regular">' + esc(o.s.sci) + '</i>' : '') + '</button></li>'; }).join('') + '</ul></details>';
    }
    function callout(icon, title, text, btn) {
      return '<section class="callout"><span class="ei">' + ic(icon, 28) + '</span><b class="t-minor-title">' + esc(title) + '</b><p class="t-body-regular">' + esc(text) + '</p>' + (btn || '') + '</section>';
    }
    function detailHtml(s) {
      if (!s) return '<section class="callout"><span class="ei">' + ic('paw', 28) + '</span><b class="t-minor-title">Pick a species to view its diet</b><p class="t-body-regular">Choose a species from the list to see its plans.</p></section>';
      var all = plansOf(s);
      if (!all.filter(function (p) { return p.active; }).length) {
        if (st.scope !== 'species') {   /* no diet anywhere yet: pick a target, then request one for it */
          var noun = { site: 'a site', section: 'a section', enclosure: 'an enclosure', animal: 'an animal' }[st.scope];
          if (st.ref == null) return hero(s) + scopeCard(s) + callout(st.scope === 'animal' ? 'paw' : 'location-icon', 'Pick ' + noun + ' to see its diet', 'Choose ' + noun + ' above.', '');
          return hero(s) + scopeCard(s) + callout('reason-or-list', 'No diet yet', 'No diet applies to ' + (refName(s, st.scope, st.ref) || noun) + ' yet. Request one and the dietician configures it.',
            '<button type="button" class="btn teal" data-rqnew="scope">' + ic('reason-or-list', 20) + 'Request new diet</button>' + reqBadge(openReqs(s, st.scope, st.ref)));
        }
        return hero(s) + scopeCard(s) + callout('reason-or-list', 'No base diet yet', 'Create the base diet first. It is the always-on default for everyday feeding. Seasonal, sex-based, site, section, enclosure and animal plans all build on it, so they cannot be added until the base diet exists.',
          '<div class="cobtns"><button type="button" class="btn teal" data-createbase>' + ic('add', 20) + 'Create base diet</button><button type="button" class="btn sec" data-rqnew="base">' + ic('reason-or-list', 20) + 'Request a base diet</button></div><p class="ro-note t-body-regular">Only dieticians with write access can create diets.</p>' + reqBadge(openReqs(s)));
      }
      var body = scopeCard(s);
      if (st.scope !== 'species' && st.ref == null) {
        var what = { site: 'a site', section: 'a section', enclosure: 'an enclosure', animal: 'an animal' }[st.scope];
        return hero(s) + body + callout(st.scope === 'animal' ? 'paw' : 'location-icon', 'Pick ' + what + ' to see its diets', 'Choose ' + what + ' above. Each row shows the diet it gets today.', '');
      }
      var here = plansHere(s), vis = here.filter(function (p) { return p.active || p.proposed || st.showInactive; });
      if (!here.length) { st.plan = null; var inh = inherited(s, st.scope, st.ref);
        if (inh) return hero(s) + body + inheritedCard(s, inh);
        return hero(s) + body + callout('reason-or-list', 'No ' + SCN[st.scope].toLowerCase() + ' diet here yet', (inh ? srcLabel(inh) + ' applies here.' : 'No diet applies here yet.'), '<div class="cobtns"><button type="button" class="btn teal" data-rqnew="scope">' + ic('reason-or-list', 20) + 'Request new diet</button><button type="button" class="addchip" data-newplan aria-label="Add seasonal or time-bound diet">' + ic('add', 24) + '</button></div>' + reqBadge(openReqs(s, st.scope, st.ref))); }
      if (st.plan == null || !vis.some(function (p) { return p.id === st.plan; })) { var d = vis.filter(function (p) { return p.active; })[0] || vis[0]; st.plan = d ? d.id : null; }
      var sel = st.plan != null ? PLANS[st.plan] : null;
      return hero(s) + body + planCard(s, sel, here) + (sel ? shared(s, sel) : '');
    }
    function host() { return LAND.matches ? $('[data-detail]') : (st.panel ? document.querySelector('#spanel .dpanel__body') : null); }
    function drawDetail() { var h = host(); if (h) { var top = h.scrollTop, ts = h.querySelector('[data-tscroll]'), tt = ts ? ts.scrollTop : 0; h.innerHTML = '<div class="spsheet">' + detailHtml(BY[st.tsn]) + '</div>'; if (!mayEdit(BY[st.tsn])) [].forEach.call(h.querySelectorAll('[data-createbase], [data-newplan], [data-act="edit"], .addchip'), function (b) { b.remove(); }); drawTargets(); var ns = h.querySelector('[data-tscroll]'); if (ns) { ns.scrollTop = tt; fades(); } h.scrollTop = top; } }
    function openPanel() {
      var s = BY[st.tsn], p = document.getElementById('spanel'); if (!s) return;
      st.panel = true; p.querySelector('[data-ptitle]').textContent = s.name; p.querySelector('[data-psub]').textContent = s.sci; var was = !p.hidden; p.hidden = false; drawDetail(); p.querySelector('.dpanel__body').scrollTop = 0; if (!was) { var hd = p.querySelector('#spT'); hd.setAttribute('tabindex', '-1'); hd.focus({ preventScroll: true }); }
    }
    function closePanel() { st.panel = false; document.getElementById('spanel').hidden = true; }
    function hashFor() { return '#species/' + st.seg + (st.tsn ? '/' + st.tsn + (st.plan ? '/' + st.plan : '') : ''); }
    function setHash(push) { var h = hashFor(); if (location.hash === h) return; if (push) location.hash = h; else { try { history.replaceState(null, '', h); } catch (x) {} } }

    /* ---------- history sheet (Diet history drawer) ---------- */
    function historyHtml() {
      var s = BY[st.tsn], all = plansOf(s), H = st.hist;
      var scopeOf = function (p) { return p.scope === 'species' ? 'species' : p.scope === 'animal' ? 'animal' : 'site'; };
      var rows = all.filter(function (p) {
        if (H.scope !== 'all' && scopeOf(p) !== H.scope) return false;
        var k = p.kind; if (H.kind === 'year-round' && !(k === 'base' || k === 'sex-based')) return false;
        if (H.kind === 'seasonal' && !(k === 'seasonal' || k === 'combined')) return false; if (H.kind === 'time-bound' && k !== 'time-bound') return false; return true;
      }).sort(function (a, b) { return b.id - a.id; });
      var SL = { site: 'Site-wide', section: 'Section-wide', enclosure: 'Enclosure-wide', animal: 'Animal-wide' };
      var rg = reqGroups(s), seg = H.seg === 'requests' ? 'requests' : 'diets';
      var head = '<div class="grab"></div><div class="sheet__h" data-histsheet><div><h2 class="t-major-title" id="sheetT">Diet history</h2><p class="t-body-regular" style="color:var(--ink)">' + esc(s.name) + '. ' + (seg === 'diets' ? 'All diets across species, site and animal scopes.' : 'Diet change requests for this species.') + '</p></div><button type="button" class="iconbtn" data-sclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
        '<div class="seg3 hseg" role="tablist" aria-label="Diet history view"><button type="button" role="tab" class="t-body-medium" data-hseg="diets" aria-selected="' + (seg === 'diets') + '">Diets <span class="n">' + all.length + '</span></button><button type="button" role="tab" class="t-body-medium" data-hseg="requests" aria-selected="' + (seg === 'requests') + '">Requests <span class="n">' + rg.n + '</span>' + (rg.todo ? '<span class="hdot" aria-label="' + rg.todo + ' to configure">' + rg.todo + '</span>' : '') + '</button></div>';
      if (seg === 'requests') {
        return head + '<div class="hreqs">' + (rg.groups.length ? rg.groups.map(function (g) { return '<p class="' + (g[2] ? 'sreqs__need' : 'sreqs__sub') + ' t-body-medium">' + (g[2] ? ic('alert', 18) : '') + esc(g[0]) + ' (' + g[1].length + ')</p>' + g[1].map(reqRow).join(''); }).join('') :
          '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">' + esc(RQ.can('seeAll') ? 'No diet change requests for this species yet.' : 'You have not raised any requests for this species.') + '</p>') +
          '<a class="linkbtn t-body-medium hreqs__tab" href="#request" data-tabgo>Open Diet Request tab</a></div>';
      }
      return head +
        '<div class="segrow" style="padding:0">' + [['all', 'All'], ['species', 'Species'], ['site', 'Site'], ['animal', 'Animal']].map(function (t) { var n = t[0] === 'all' ? all.length : all.filter(function (p) { return scopeOf(p) === t[0]; }).length; return '<button type="button" class="spchip t-body-medium" data-hs="' + t[0] + '" aria-pressed="' + (H.scope === t[0]) + '">' + t[1] + ' <span class="n">' + n + '</span></button>'; }).join('') + '</div>' +
        '<div class="segrow" style="padding:0">' + [['all', 'All kinds'], ['year-round', 'Year-round'], ['seasonal', 'Seasonal'], ['time-bound', 'Time-bound']].map(function (t) { return '<button type="button" class="spchip t-body-medium" data-hk="' + t[0] + '" aria-pressed="' + (H.kind === t[0]) + '">' + t[1] + '</button>'; }).join('') + '</div>' +
        (rows.length ? '<div class="dtab-wrap"><table class="htab t-body-regular"><thead><tr><th>Diet</th><th>Scope</th><th>Reason</th><th>Validity</th><th>Status</th></tr></thead><tbody>' + rows.map(function (p) {
          var valid = (p.from || p.to) ? (p.from ? ddmmyy(p.from) : '...') + ' → ' + (p.to ? ddmmyy(p.to) : 'open') + (p.recurring ? ' · yearly' : '') : 'Year-round';
          return '<tr><td><b>' + shownId(p) + '</b><br>' + kindTag(p) + (p.fromReq ? '<button type="button" class="hfrom t-body-medium" data-rqopen="' + p.fromReq + '">' + ic('reason-or-list', 14) + 'From ' + p.fromReq + '</button>' : '') + '</td><td>' + esc(p.scope === 'species' ? 'Species-wide' : SL[p.scope] + (p.scopeName ? ' · ' + p.scopeName : '')) + '</td><td>' + (p.reason ? '<span class="tag orange">' + esc(p.reason) + '</span>' : '-') + '</td>' +
            '<td>' + esc(valid) + '<small>Created ' + ddmmyy(p.created) + (p.by ? ' by ' + esc(p.by) : '') + '</small></td><td>' + (p.proposed ? '<span class="pill inactive t-body-medium">Proposed</span>' : p.active ? '<span class="pill active t-body-medium">Active</span>' : '<span class="pill inactive t-body-medium">Inactive</span>') + '</td></tr>';
        }).join('') + '</tbody></table></div>' : '<p class="t-body-regular" style="color:var(--md3-neutral-secondary)">' + (all.length ? 'No diets match the current filters.' : 'No diets have been created for this species yet.') + '</p>');
    }
    var sheetMode = null;
    function openHistory(seg) { sheetMode = 'hist'; st.hist.seg = seg || 'diets'; document.getElementById('sheet').innerHTML = historyHtml(); document.getElementById('scrim').hidden = false; }
    document.getElementById('scrim').addEventListener('click', function (e) {
      if (!document.querySelector('#sheet [data-histsheet]')) return; var t;
      if (e.target === this || e.target.closest('[data-sclose]')) { this.hidden = true; sheetMode = null; return; }
      if ((t = e.target.closest('[data-hseg]'))) { st.hist.seg = t.getAttribute('data-hseg'); document.getElementById('sheet').innerHTML = historyHtml(); return; }
      if ((t = e.target.closest('[data-rqopen]'))) { this.hidden = true; sheetMode = null; location.hash = '#request/' + t.getAttribute('data-rqopen'); return; }
      if (e.target.closest('[data-tabgo]')) { this.hidden = true; sheetMode = null; return; }
      if ((t = e.target.closest('[data-hs]'))) { st.hist.scope = t.getAttribute('data-hs'); document.getElementById('sheet').innerHTML = historyHtml(); return; }
      if ((t = e.target.closest('[data-hk]'))) { st.hist.kind = t.getAttribute('data-hk'); document.getElementById('sheet').innerHTML = historyHtml(); }
    }, true);

''' + WIZ_JS + REQ_FORM_JS + '''
    /* ---------- events ---------- */
    function onDetail(e) {
      var t, s = BY[st.tsn]; if (!s) return;
      if ((t = e.target.closest('[data-tfilters]'))) { st.tFiltersOpen = !st.tFiltersOpen; t.setAttribute('aria-expanded', String(st.tFiltersOpen)); host().querySelector('[data-tfiltermenu]').hidden = !st.tFiltersOpen; return; }
      if ((t = e.target.closest('[data-tf]'))) { st.tf = t.getAttribute('data-tf'); st.tlimit = 40; drawDetail(); return; }
      if ((t = e.target.closest('[data-tsx]'))) { var sx = t.getAttribute('data-tsx'); st.tsx = st.tsx === sx ? '' : sx; st.tlimit = 40; drawDetail(); return; }
      if (e.target.closest('[data-tclearfilters]')) { st.tf = ''; st.tsx = ''; st.tlimit = 40; drawDetail(); return; }
      if (e.target.closest('[data-tmore]')) { var sc = host().querySelector('[data-tscroll]'), keep = sc.scrollTop; st.tlimit = (st.tlimit || 40) + 40; drawTargets(); sc.scrollTop = keep; return; }
      if (e.target.closest('[data-tclear]')) { resetTargets(); drawDetail(); return; }
      if ((t = e.target.closest('[data-scope]'))) { resetTargets(); st.scope = t.getAttribute('data-scope'); st.ref = null; st.plan = null; st.showInactive = false; if (st.scope !== 'species') { var L = locOf(s); var first = st.scope === 'site' ? L.sites[0] : st.scope === 'section' ? L.sections[0] : null; if (first && L[st.scope === 'site' ? 'sites' : 'sections'].length === 1) st.ref = first.id; } drawDetail(); setHash(false); return; }
      if ((t = e.target.closest('[data-ref]'))) { st.ref = Number(t.getAttribute('data-ref')); st.plan = null; st.showInactive = false; drawDetail(); setHash(false); return; }
      if ((t = e.target.closest('[data-plan]'))) { st.plan = Number(t.getAttribute('data-plan')); st.tab = 'items'; drawDetail(); setHash(false); return; }
      if (e.target.closest('[data-showinactive]')) { st.showInactive = !st.showInactive; drawDetail(); return; }
      if ((t = e.target.closest('[data-dtab]'))) { st.tab = t.getAttribute('data-dtab'); drawDetail(); return; }
      if ((t = e.target.closest('[data-goto]'))) { st.tsn = Number(t.getAttribute('data-goto')); st.plan = Number(t.getAttribute('data-goplan')) || null; resetScope(); applyPlan(BY[st.tsn]); if (!inSeg(BY[st.tsn], st.seg)) st.seg = 'all'; setHash(true); return; }
      if (e.target.closest('[data-history]')) { openHistory(reqGroups(s).open ? 'requests' : 'diets'); return; }
      if (e.target.closest('[data-createbase]')) { openWizard('year-round', true); return; }
      if ((t = e.target.closest('[data-rqopen]'))) { location.hash = '#request/' + t.getAttribute('data-rqopen'); return; }
      if ((t = e.target.closest('[data-rqnew]'))) { var kind = t.getAttribute('data-rqnew');
        if (kind === 'plan') openRequest({ scope: st.scope, ref: st.ref, plan: st.plan, from: 'plan' }); else if (kind === 'scope') openRequest({ scope: st.scope, ref: st.ref, from: 'scope' }); else openRequest({ scope: 'species', from: kind }); return; }
      if ((t = e.target.closest('[data-newplan]'))) { openKindMenu(t); return; }
      if (e.target.closest('[data-act="edit"]')) { var ep = PLANS[st.plan]; if (ep && ep.active) openEdit(ep); }
    }
    $('[data-detail]').addEventListener('click', onDetail);
    document.querySelector('#spanel .dpanel__body').addEventListener('click', onDetail);
    document.addEventListener('click', function (e) {
      if (!st.tFiltersOpen || e.target.closest('[data-tfilters], [data-tfiltermenu]')) return;
      st.tFiltersOpen = false; var h = host(), m = h && h.querySelector('[data-tfiltermenu]'), b = h && h.querySelector('[data-tfilters]');
      if (m) m.hidden = true; if (b) b.setAttribute('aria-expanded', 'false');
    });
    [$('[data-detail]'), document.querySelector('#spanel .dpanel__body')].forEach(function (el) {
      el.addEventListener('input', function (e) { if (e.target.matches('[data-tq]')) { st.tq = e.target.value; st.tlimit = 40; var b = el.querySelector('[data-tscroll]'); drawTargets(); if (b) b.scrollTop = 0; fades(); } });
      el.addEventListener('scroll', function (e) { if (e.target.matches && e.target.matches('[data-tscroll]')) fades(); }, true);
      el.addEventListener('toggle', function (e) { if (e.target.matches && e.target.matches('[data-shared]')) st.shOpen = e.target.open; }, true);
    });
    root.addEventListener('input', function (e) { if (e.target.matches('[data-q]')) { st.q = e.target.value; drawList(); if (LAND.matches) drawDetail(); } });
    root.addEventListener('click', function (e) {
      var t;
      if (e.target.closest('[data-detail]')) return;
      if ((t = e.target.closest('[data-s]'))) { var k = t.getAttribute('data-s'); if (k !== st.seg) { st.seg = k; if (!LAND.matches) st.tsn = null; setHash(true); } return; }
      if ((t = e.target.closest('[data-fbtn]'))) { var c = $('[data-chips]'); c.hidden = !c.hidden; t.setAttribute('aria-pressed', String(!c.hidden)); return; }
      if ((t = e.target.closest('[data-cl]'))) { var i = st.cls.indexOf(t.getAttribute('data-cl')); if (i === -1) st.cls.push(t.getAttribute('data-cl')); else st.cls.splice(i, 1); drawList(); drawDetail(); return; }
      if ((t = e.target.closest('[data-vr]'))) { st.ver = t.getAttribute('data-vr'); drawList(); drawDetail(); return; }
      if (e.target.closest('[data-sort]')) { st.sort = st.sort === 'count' ? 'name' : 'count'; drawList(); return; }
      if ((t = e.target.closest('[data-tsn]'))) { var ts = Number(t.getAttribute('data-tsn')); if (ts !== st.tsn) { st.tsn = ts; st.plan = null; resetScope(); } if (LAND.matches) { drawList(); drawDetail(); setHash(false); } else setHash(true); }
    });
    LAND.addEventListener('change', function () { if (LAND.matches) closePanel(); else if (st.tsn && /#species\\/[a-z]+\\/\\d+/.test(location.hash)) openPanel(); drawList(); drawDetail(); });
    drawList();
    RQ.listeners.push(function () { drawList(); drawDetail(); });
    return {
      count: SPECIES.length,
      show: function (seg, tsn, plan, nk, nstep, rq) {
        st.seg = SEGS.some(function (x) { return x[0] === seg; }) ? seg : 'all';
        if (rq && tsn && BY[tsn]) { if (tsn !== st.tsn) { st.tsn = tsn; resetScope(); } drawList(); if (LAND.matches) drawDetail(); else if (!st.panel) openPanel(); rfRoute(tsn, rq); return; }
        if (RF) closeRF();
        if (nk && tsn && BY[tsn]) { if (tsn !== st.tsn) { st.tsn = tsn; resetScope(); } drawList(); if (LAND.matches) drawDetail(); else if (!st.panel) openPanel(); wizRoute(st.seg, tsn, nk, nstep); return; }
        if (W) closeWizard();
        if (tsn && BY[tsn]) {
          if (tsn !== st.tsn) { st.tsn = tsn; resetScope(); }
          st.plan = plan || null; applyPlan(BY[tsn]);
          drawList(); if (LAND.matches) { closePanel(); drawDetail(); } else openPanel();
        } else { if (!LAND.matches) { st.tsn = null; } closePanel(); drawList(); drawDetail(); }
      },
      hasPanel: function () { return !!st.panel; },
      hasWizard: function () { return !!W; },
      escape: function () { if (st.tFiltersOpen) { st.tFiltersOpen = false; var h = host(), m = h && h.querySelector('[data-tfiltermenu]'), b = h && h.querySelector('[data-tfilters]'); if (m) m.hidden = true; if (b) { b.setAttribute('aria-expanded', 'false'); b.focus(); } return true; } if (RF) { document.querySelector('#rqf [data-rfclose]').click(); return true; } if (!document.getElementById('wsheet').hidden) { var c = document.querySelector('#wsheet [data-isclose]'); if (c) c.click(); return true; } if (W) { document.querySelector('#wiz [data-wcancel]').click(); return true; } return false; },
    };
  }
'''
