# modules.py: exec'd by build.py after kitchen.py. Security and Inventory module homes (blank for now, content to come).
# Same shell, Viewing as sheet and No access guard as kitchen-home.html. Roles and module access live in roles.py (MODS).
MOD_USERS_JS = '''  var USERS = [
    { key: 'dietician', name: 'Hydar Ali', title: 'Dietician', what: 'Diet module. Raises requests and sees My requests.' },
    { key: 'head-dietician', name: 'Dr. Meera Iyer', title: 'Head Dietician', what: 'Diet module. Reviews and configures requests, edits diets.' },
    { key: 'kitchen-head', name: 'Suresh Gowda', title: 'Kitchen Head', what: 'Diet, Kitchen and Inventory.' },
    { key: 'kitchen-operator', name: 'Anil Kumar', title: 'Kitchen Operator', what: 'Kitchen only.' },
    { key: 'receiving-manager', name: 'Farhan Shaikh', title: 'Receiving Manager', what: 'Inventory and Kitchen.' },
    { key: 'security', name: 'Ravi Naik', title: 'Security', what: 'Security module only.' },
    { key: 'security-admin', name: 'Priya Desai', title: 'Security Admin', what: 'Security module only.' } ];
'''

def mod_page(slug, title, default_role, tabs='', css='', js_extra='', extra_html=''):
    body = f'''  <div class="app">
{STATUS_HTML}
    <div class="head">
      <header class="bar">
        <a class="iconbtn" href="diet-module-flow.html" data-aslink="diet-module-flow.html" aria-label="Back to Modules">{svg("back", 24)}</a>
        <div class="bar__hd"><h1 class="t-medium-medium">{title}</h1></div>
        <button class="asbtn" type="button" aria-haspopup="dialog" aria-label="Viewing as, switch role"></button>
        {SITE_BTN}
      </header>
{tabs}
    </div>
    <main class="main" id="main"></main>
  </div>
{extra_html}
{ROLE_OVERLAY}'''
    js = (icon_js(['back', 'user', 'dropdown', 'close', 'just-tick-mark', 'location-icon', 'search', 'calendar']) +
          "  function esc(s) { return String(s == null ? '' : s).replace(/[&<>\"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;' }[c]; }); }\n" +
          STORE_JS + MOD_USERS_JS + '''  var MOD = '__MOD__';
  var VIEWER = (function () { var a = new URLSearchParams(location.search).get('as'), sv = savedViewer(), ok = function (k) { return USERS.some(function (u) { return u.key === k; }); }; return USERS.filter(function (u) { return u.key === (ok(a) ? a : ok(sv) ? sv : '__DEF__'); })[0]; })();
  function initials(n) { return String(n).replace(/^Dr\\.?\\s+/i, '').split(/\\s+/).slice(0, 2).map(function (w) { return w[0].toUpperCase(); }).join(''); }
  var RS = document.getElementById('rqsheet');
  function applyViewer() {
    saveViewer(VIEWER.key); guardModule(MOD, VIEWER);
    try { var q = new URLSearchParams(location.search); q.set('as', VIEWER.key); history.replaceState(null, '', location.pathname + '?' + q.toString() + location.hash); } catch (x) {}
    [].forEach.call(document.querySelectorAll('a[data-aslink]'), function (a) { a.setAttribute('href', a.getAttribute('data-aslink') + '?as=' + VIEWER.key); });
    [].forEach.call(document.querySelectorAll('.asbtn'), function (b) { b.innerHTML = ic('user', 20) + '<span class="t-body-medium">Viewing as: ' + esc(VIEWER.name) + ' <small>· ' + esc(VIEWER.title) + '</small></span>' + ic('dropdown', 18); });
    if (typeof onViewer === 'function') onViewer();
  }
  function openRoles() {
    RS.querySelector('.sheet').innerHTML = '<div class="grab"></div><div class="sheet__h"><div><h2 class="t-major-title" id="rsT">Viewing as</h2><p class="t-body-regular" style="color:var(--ink)">Demo only. Switch role to see what each one can do.</p></div><button type="button" class="iconbtn" data-rsclose aria-label="Close">' + ic('close', 24) + '</button></div>' +
      '<div class="roles" role="radiogroup" aria-label="Role">' + USERS.map(function (u) { return '<button type="button" class="role" role="radio" data-as="' + u.key + '" aria-checked="' + (u === VIEWER) + '"><span class="av">' + initials(u.name) + '</span><span class="grow"><b class="t-minor-title">' + esc(u.title) + '</b><span class="t-body-regular">' + esc(u.name) + '</span><small class="t-body-regular">' + esc(u.what) + '</small></span>' + (u === VIEWER ? ic('just-tick-mark', 22) : '') + '</button>'; }).join('') + '</div>';
    RS.hidden = false;
  }
  RS.addEventListener('click', function (e) { var t; if (e.target === RS || e.target.closest('[data-rsclose]')) { RS.hidden = true; return; } if ((t = e.target.closest('[data-as]'))) { VIEWER = USERS.filter(function (u) { return u.key === t.getAttribute('data-as'); })[0]; RS.hidden = true; applyViewer(); } });
  document.addEventListener('click', function (e) { if (e.target.closest('.asbtn')) openRoles(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') RS.hidden = true; });
  applyViewer();
''' + js_extra).replace('__MOD__', slug).replace('__DEF__', default_role)
    page(f'{slug}-home.html', title,
         f'{title} home: blank for now, content to come. Target of the {title} tile on diet-module-flow.html. Generated by _build/modules.py, do not hand-edit.',
         HEAD_CSS + DIR_CSS2 + ROLE_CSS + css, body, js)

exec(open(os.path.join(HERE, 'security.py')).read())
mod_page('inventory', 'Inventory', 'receiving-manager')
