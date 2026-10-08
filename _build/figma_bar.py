# figma_bar.py: exec'd by build.py. Prototype-only "Copy to Figma" toolbar (same idea as antz-diet.pages.dev/prototypes/diet-tablet):
# Figma's html-to-design script exposes window.figma.captureForDesign({ selector }) and copies the element to the clipboard,
# ready to paste into Figma. Collapsed to a small "Figma" pill bottom-left; the bar hides itself while copying so it is never captured.
FIG_HEAD = '  <script src="https://mcp.figma.com/mcp/html-to-design/capture.js" async></script><!-- Figma html-to-design capture; inert unless used from the Figma button -->\n'
FIG_BODY = r'''  <!-- Figma capture toolbar (prototype only, not part of the app) -->
  <style>
    .figbar { position: fixed; left: 12px; bottom: 12px; z-index: 90; display: flex; align-items: center; gap: 6px; padding: 4px; border-radius: 22px; background: rgba(20, 24, 28, .88); color: #fff; font: 500 13px/1 Inter, system-ui, sans-serif; box-shadow: 0 6px 20px rgba(0,0,0,.25); }
    .figbar button { min-height: 36px; padding: 0 12px; border: 0; border-radius: 18px; background: transparent; color: #fff; font: inherit; cursor: pointer; white-space: nowrap; }
    .figbar button:hover:not([disabled]) { background: rgba(255,255,255,.14); }
    .figbar button[disabled] { opacity: .4; cursor: not-allowed; }
    .figbar button[aria-pressed="true"] { background: #fff; color: #14181C; }
    .figbar .figbar__tog { display: inline-flex; align-items: center; gap: 6px; font-weight: 600; }
    .figbar .figbar__tog svg { width: 14px; height: 14px; }
    .figbar .figbar__ipad { display: inline-flex; align-items: center; gap: 6px; font-weight: 600; }
    .figbar .figbar__ipad svg { width: 16px; height: 16px; }
    .figbar .figbar__ui { font-weight: 600; }
    .figbar .figbar__ui[aria-pressed="true"] { background: #37BD69; color: #fff; }
    .figbar__sep { width: 1px; height: 20px; background: rgba(255,255,255,.25); }
    .figbar__acts { display: none; align-items: center; gap: 2px; }
    .figbar.open .figbar__acts { display: flex; }
    .figbar__st { max-width: 260px; padding: 0 10px 0 4px; color: rgba(255,255,255,.75); font-weight: 400; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .figbar__st[data-tone="ok"] { color: #8EF0B4; } .figbar__st[data-tone="error"] { color: #FFB4C0; }
    .figbar__outline { position: absolute; z-index: 89; pointer-events: none; border: 2px solid #0D99FF; background: rgba(13,153,255,.08); border-radius: 4px; }
    body.is-figma-picking, body.is-figma-picking * { cursor: crosshair !important; }
    @media print { .figbar { display: none; } }
  </style>
  <div class="figbar" id="figbar" role="toolbar" aria-label="Copy to Figma, prototype only"></div>
  <script>
  (function () {
    var bar = document.getElementById('figbar'); if (!bar) return;
    var PICK = 'data-figma-pick', open = false, picking = false, busy = false, msg = '', tone = '';
    var LOGO = '<svg viewBox="0 0 38 57" aria-hidden="true"><path fill="#1ABCFE" d="M19 28.5a9.5 9.5 0 1 1 19 0 9.5 9.5 0 0 1-19 0z"/><path fill="#0ACF83" d="M0 47.5A9.5 9.5 0 0 1 9.5 38H19v9.5a9.5 9.5 0 1 1-19 0z"/><path fill="#FF7262" d="M19 0v19h9.5a9.5 9.5 0 1 0 0-19H19z"/><path fill="#F24E1E" d="M0 9.5A9.5 9.5 0 0 0 9.5 19H19V0H9.5A9.5 9.5 0 0 0 0 9.5z"/><path fill="#A259FF" d="M0 28.5A9.5 9.5 0 0 0 9.5 38H19V19H9.5A9.5 9.5 0 0 0 0 28.5z"/></svg>';
    var IPAD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="5" y="2.5" width="14" height="19" rx="2.5"/><path d="M11 18.5h2"/></svg>';
    function ready() { return !!(window.figma && window.figma.captureForDesign); }
    /* the sheet or panel on top right now: a visible bottom sheet, else an open full-screen panel */
    function topSheet() { var s = [].slice.call(document.querySelectorAll('.scrim:not([hidden]) .sheet, .rscrim:not([hidden]) .rsheet, .ddrawer:not([hidden]) .ddrawer__p')).filter(function (e) { return e.offsetParent !== null; }); return s[s.length - 1] || null; }
    function draw() {
      var sh = !!topSheet();
      var cls = 'figbar' + (open ? ' open' : ''); if (bar.className !== cls) bar.className = cls;
      bar.innerHTML = '<button type="button" class="figbar__ui" data-fig="ui" aria-pressed="' + document.documentElement.classList.contains('ui-new') + '" title="Switch between the current UI and the Antz Design Library UI">' + (document.documentElement.classList.contains('ui-new') ? 'New UI on' : 'New UI') + '</button><span class="figbar__sep" aria-hidden="true"></span>' + (window.self === window.top ? '<button type="button" class="figbar__ipad" data-fig="ipad" title="See this screen in an iPad mini frame">' + IPAD + 'iPad view</button><span class="figbar__sep" aria-hidden="true"></span>' : '') + '<button type="button" class="figbar__tog" data-fig="tog" aria-expanded="' + open + '" title="Copy to Figma">' + LOGO + 'Figma</button>' +
        '<span class="figbar__acts"><button type="button" data-fig="screen">Copy screen</button><button type="button" data-fig="sheet"' + (sh ? '' : ' disabled title="Open a sheet or panel first"') + '>Copy sheet</button>' +
        '<button type="button" data-fig="pick" aria-pressed="' + picking + '">' + (picking ? 'Cancel pick' : 'Pick element') + '</button>' +
        '<span class="figbar__st" role="status" data-tone="' + tone + '">' + (msg || (ready() ? (picking ? 'Tap anything to copy it, Esc cancels' : 'Copies to the clipboard, paste into Figma') : 'Loading the Figma script')) + '</span></span>';
    }
    function say(t, k) { msg = t; tone = k || ''; draw(); }
    /* Figma reads each SVG on its own: inline <use> symbols and copy any gradient / mask / clip an SVG points to into that SVG */
    function flatten(root) {
      [].forEach.call((root || document).querySelectorAll('svg'), function (svg, n) {
        if (svg.closest('#figbar') || svg.classList.contains('icon-defs')) return;
        [].forEach.call(svg.querySelectorAll('use'), function (u) {
          var ref = (u.getAttribute('href') || u.getAttribute('xlink:href') || '').replace(/^#/, ''), sym = ref && document.getElementById(ref); if (!sym) return;
          var g = document.createElementNS('http://www.w3.org/2000/svg', 'g'); [].forEach.call(sym.childNodes, function (c) { g.appendChild(c.cloneNode(true)); }); u.parentNode.replaceChild(g, u);
        });
        var defs = svg.querySelector(':scope > defs'), map = {};
        [].forEach.call(svg.querySelectorAll('*'), function (el) {
          ['fill', 'stroke', 'mask', 'clip-path', 'filter'].forEach(function (at) {
            var v = el.getAttribute(at), m = v && v.match(/url\(#([^)]+)\)/); if (!m) return; var id = m[1];
            if (svg.querySelector('[id="' + id + '"]')) return;
            if (!map[id]) { var src = document.getElementById(id); if (!src) return; if (!defs) { defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs'); svg.insertBefore(defs, svg.firstChild); } var c = src.cloneNode(true); map[id] = id + '-f' + n; c.id = map[id]; defs.appendChild(c); }
            el.setAttribute(at, 'url(#' + map[id] + ')');
          });
        });
      });
    }
    function capture(selector, label) {
      if (!ready()) return say('The Figma script has not loaded (it needs internet).', 'error');
      if (busy) return; busy = true; say('Copying ' + label);
      bar.style.visibility = 'hidden'; outline.hidden = true; try { flatten(document); } catch (e) {}
      Promise.resolve().then(function () { return window.figma.captureForDesign({ selector: selector, delayMs: 0 }); })
        .then(function (r) { if (r && r.success === false) say('Could not copy: ' + r.error, 'error'); else say(label.charAt(0).toUpperCase() + label.slice(1) + ' copied. Paste into Figma.', 'ok'); })
        .catch(function (e) { say('Could not copy: ' + (e && e.message || e), 'error'); })
        .then(function () { busy = false; bar.style.visibility = ''; [].forEach.call(document.querySelectorAll('[' + PICK + ']'), function (x) { x.removeAttribute(PICK); }); setTimeout(function () { if (!busy) { msg = ''; tone = ''; draw(); } }, 4000); });
    }
    var outline = document.createElement('div'); outline.className = 'figbar__outline'; outline.hidden = true; document.body.appendChild(outline);
    function inPage(el) { return el && el.closest && !el.closest('#figbar') && el !== outline && el !== document.body && el !== document.documentElement; }
    function show(el) { var r = el.getBoundingClientRect(); outline.style.top = (r.top + scrollY) + 'px'; outline.style.left = (r.left + scrollX) + 'px'; outline.style.width = r.width + 'px'; outline.style.height = r.height + 'px'; outline.hidden = false; }
    function target(el) { return el.closest('.tile, .row, .gvc, .txc, .stcard, .spk, .cfgrow, .gacc__i, .glines, .dkpi, .dsum, .dpan, .dcard, .scard, .kpanel, .card, .sheet, .txdh, .txfoot, .txsec, section, button, a') || el; }
    function stopPick() { picking = false; outline.hidden = true; document.body.classList.remove('is-figma-picking'); draw(); }
    document.addEventListener('mouseover', function (e) { if (picking && inPage(e.target)) show(target(e.target)); }, true);
    document.addEventListener('click', function (e) {
      if (!picking || !inPage(e.target)) return;
      e.preventDefault(); e.stopImmediatePropagation();
      var el = target(e.target), name = (el.className && typeof el.className === 'string' && el.className.split(' ')[0]) || el.tagName.toLowerCase();
      el.setAttribute(PICK, '1'); stopPick(); capture('[' + PICK + '="1"]', 'the ' + name);
    }, true);
    document.addEventListener('keydown', function (e) { if (picking && e.key === 'Escape') { e.stopImmediatePropagation(); stopPick(); } }, true);
    bar.addEventListener('click', function (e) {
      var b = e.target.closest('[data-fig]'); if (!b || b.disabled) return; var a = b.getAttribute('data-fig');
      if (a === 'ui') { var on = !document.documentElement.classList.contains('ui-new'); document.documentElement.classList.toggle('ui-new', on); try { localStorage.setItem('antz.ui', on ? 'new' : 'old'); } catch (e) {} try { if (window.self !== window.top) parent.postMessage({ antzUi: on }, '*'); } catch (e) {} draw(); return; }
      if (a === 'ipad') { var here = location.pathname.split('/').pop() + location.search + location.hash; location.href = 'preview.html?src=' + encodeURIComponent(here); return; }
      if (a === 'tog') { open = !open; if (!open && picking) stopPick(); else draw(); return; }
      if (a === 'screen') return capture('body', 'the screen');
      if (a === 'sheet') { var s = topSheet(); if (!s) return; s.setAttribute(PICK, '1'); return capture('[' + PICK + '="1"]', 'the sheet'); }
      if (a === 'pick') { if (picking) return stopPick(); picking = true; document.body.classList.add('is-figma-picking'); draw(); }
    });
    /* keep Copy sheet in step with sheets opening and closing */
    var lastSh = null; new MutationObserver(function (ms) { if (busy || !open) return; if (ms.every(function (m) { return bar.contains(m.target) || m.target === outline; })) return; var sh = !!topSheet(); if (sh !== lastSh) { lastSh = sh; draw(); } }).observe(document.body, { subtree: true, attributes: true, attributeFilter: ['hidden', 'class'] });
    var wait = setInterval(function () { if (ready()) { clearInterval(wait); draw(); } }, 400); setTimeout(function () { clearInterval(wait); }, 20000);
    draw();
    /* inside the iPad preview frame: tell the preview which screen is showing, so Exit iPad view returns to it */
    if (window.self !== window.top) { var tell = function () { try { parent.postMessage({ antzLoc: location.pathname.split('/').pop() + location.search + location.hash }, '*'); } catch (e) {} }; tell(); addEventListener('hashchange', tell); }
  })();
  </script>
'''
FIG_PAGES = {'diet-home.html', 'kitchen-home.html', 'security-home.html', 'inventory-home.html'}
