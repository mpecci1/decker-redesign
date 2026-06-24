/* Decker Tape — interactions: mobile nav, scroll reveal, form, year */
(function () {
  'use strict';

  // current year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // mobile menu
  var toggle = document.querySelector('.nav-toggle');
  var panel = document.querySelector('.mobile-panel');
  if (toggle && panel) {
    var setOpen = function (open) {
      panel.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
    };
    toggle.addEventListener('click', function () {
      setOpen(!panel.classList.contains('open'));
    });
    panel.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { setOpen(false); });
    });
    window.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
  }

  // scroll reveal
  var reveals = document.querySelectorAll('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('in'); });
  }

  // quote form — submits to Web3Forms (https://web3forms.com).
  // Until a real access key is pasted into the hidden access_key field,
  // it runs in "demo mode" and just shows the success state.
  var form = document.querySelector('form[data-quote]');
  if (form) {
    var ok = form.querySelector('.form__ok');
    var err = form.querySelector('.form__err');
    var btn = form.querySelector('button[type="submit"]');
    var btnHTML = btn ? btn.innerHTML : '';

    var lock = function () {
      form.querySelectorAll('input, textarea, select, button').forEach(function (el) {
        el.setAttribute('disabled', 'disabled');
      });
    };
    var show = function (el) { if (el) el.classList.add('show'); };
    var hide = function (el) { if (el) el.classList.remove('show'); };

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      hide(err);

      // honeypot — bots tick the hidden checkbox; silently drop.
      var hp = form.querySelector('[name="botcheck"]');
      if (hp && hp.checked) return;

      // native validation (required name + email)
      if (!form.checkValidity()) { form.reportValidity(); return; }

      var keyEl = form.querySelector('[name="access_key"]');
      var key = keyEl ? keyEl.value : '';
      var configured = key && key.indexOf('YOUR_') !== 0;

      if (!configured) { show(ok); lock(); return; } // demo mode

      if (btn) { btn.disabled = true; btn.textContent = 'Sending…'; }
      fetch(form.action, { method: 'POST', body: new FormData(form) })
        .then(function (r) { return r.json(); })
        .then(function (data) {
          if (data && data.success) { show(ok); lock(); }
          else { throw new Error((data && data.message) || 'send failed'); }
        })
        .catch(function () {
          show(err);
          if (btn) { btn.disabled = false; btn.innerHTML = btnHTML; }
        });
    });
  }

  // ---- catalog (catalog.html): client-side search/filter over real products ----
  var grid = document.getElementById('cat-grid');
  if (grid) {
    var search = document.getElementById('cat-search');
    var filters = document.getElementById('cat-filters');
    var countEl = document.getElementById('cat-count');
    var moreBtn = document.getElementById('cat-more');
    var PAGE = 48;
    var data = [], active = 'All', shown = 0, matches = [], sprites = null;

    var sectionOf = function (p) {
      var c = ((p.cats || []).join(' ') + ' ' + p.name).toLowerCase();
      if (/handle|tape pad|\bpads?\b/.test(c)) return 'Handles & Pads';
      if (/label|fragile|pictograph|d\.?o\.?t|regulated|hazard|arrow|circle|fluorescent|color coded|inventory|control label|\bmonths?\b|\bnumbers?\b|handling|pallet|blank label|wafer/.test(c)) return 'Labels';
      if (/printed|stock print|custom print/.test(c)) return 'Printed Tape';
      return 'Tape';
    };
    var SECTIONS = ['All', 'Tape', 'Printed Tape', 'Labels', 'Handles & Pads'];

    var esc = function (s) { return (s || '').replace(/[&<>"]/g, function (m) { return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[m]; }); };

    var render = function (reset) {
      if (reset) { grid.innerHTML = ''; shown = 0; }
      var slice = matches.slice(shown, shown + PAGE);
      var html = slice.map(function (p) {
        var thumb;
        if (p.sp && sprites && sprites[p.sp[0]]) {
          var sh = sprites[p.sp[0]], c = p.sp[1], r = p.sp[2];
          var bx = sh.cols > 1 ? (c / (sh.cols - 1) * 100) : 0;
          var by = sh.rows > 1 ? (r / (sh.rows - 1) * 100) : 0;
          thumb = '<div class="cat-item__thumb sprite" role="img" aria-label="' + esc(p.disp) +
            '" style="background-image:url(' + sh.src + ');background-size:' + (sh.cols * 100) + '% ' +
            (sh.rows * 100) + '%;background-position:' + bx.toFixed(3) + '% ' + by.toFixed(3) + '%"></div>';
        } else {
          thumb = '<div class="cat-item__thumb noimg"></div>';
        }
        return '<article class="cat-item">' + thumb +
          '<div class="cat-item__body"><span class="cat-item__code">' + esc(p.code) +
          '</span><span class="cat-item__name">' + esc(p.disp) +
          '</span><span class="cat-item__sect">' + esc(p.sect) + '</span></div></article>';
      }).join('');
      grid.insertAdjacentHTML('beforeend', html);
      shown += slice.length;
      moreBtn.hidden = shown >= matches.length;
      if (!matches.length) grid.innerHTML = '<p class="catalog-empty">No products match that search. Try a part number like <strong>150X</strong> or a word like <strong>fragile</strong>.</p>';
      countEl.textContent = matches.length + ' product' + (matches.length === 1 ? '' : 's') +
        (active === 'All' ? '' : ' in ' + active) + (search.value ? ' matching “' + search.value + '”' : '');
    };

    var apply = function () {
      var q = search.value.trim().toLowerCase();
      matches = data.filter(function (p) {
        if (active !== 'All' && p.sect !== active) return false;
        if (!q) return true;
        return p.hay.indexOf(q) !== -1;
      });
      render(true);
    };

    fetch('catalog.json').then(function (r) { return r.json(); }).then(function (json) {
      sprites = json.sprites || null;
      data = (json.products || json).map(function (p) {
        // strip leading "CODE - " from the name for a cleaner display label
        var disp = (p.name || '').replace(/^[A-Z0-9./-]+\s*[-–]\s*/i, '').trim() || p.name;
        var sect = sectionOf(p);
        return { code: p.code, disp: disp, sect: sect, sp: p.sp || null, hay: (p.code + ' ' + p.name).toLowerCase() };
      });
      // build filter buttons with counts
      filters.innerHTML = SECTIONS.map(function (s) {
        var n = s === 'All' ? data.length : data.filter(function (p) { return p.sect === s; }).length;
        return '<button class="cat-filter" role="tab" data-sect="' + s + '" aria-selected="' + (s === 'All') + '">' + s + '<span class="n">' + n + '</span></button>';
      }).join('');
      filters.addEventListener('click', function (e) {
        var b = e.target.closest('.cat-filter'); if (!b) return;
        active = b.getAttribute('data-sect');
        filters.querySelectorAll('.cat-filter').forEach(function (x) { x.setAttribute('aria-selected', x === b); });
        apply();
      });
      var t; search.addEventListener('input', function () { clearTimeout(t); t = setTimeout(apply, 120); });
      moreBtn.addEventListener('click', function () { render(false); });
      apply();
    }).catch(function () {
      countEl.textContent = 'Catalog could not be loaded.';
      grid.innerHTML = '<p class="catalog-empty">Couldn\'t load the catalog right now. Please <a href="contact.html">contact us</a> for the full product list.</p>';
    });
  }
})();
