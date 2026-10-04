/* 미리봄 레시피 v2 — interactions */
(function () {
  'use strict';
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- toast ---------- */
  var toastEl = $('.toast'), toastT;
  function toast(msg) {
    if (!toastEl) return;
    var tt = $('.toast-t', toastEl) || toastEl;
    tt.textContent = msg;
    toastEl.classList.add('on');
    clearTimeout(toastT);
    toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 1800);
  }

  /* ---------- clipboard ---------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(function () { return legacy(text); });
    }
    return legacy(text);
  }
  function legacy(text) {
    return new Promise(function (ok, no) {
      var ta = document.createElement('textarea');
      ta.value = text; ta.setAttribute('readonly', '');
      ta.style.cssText = 'position:fixed;top:-1000px;opacity:0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy') ? ok() : no(); } catch (e) { no(e); }
      document.body.removeChild(ta);
    });
  }
  function flash(btn, cls, labelSel, doneLabel) {
    var lab = labelSel ? $(labelSel, btn) : null, old = lab ? lab.textContent : '';
    btn.classList.add(cls);
    if (lab) lab.textContent = doneLabel;
    clearTimeout(btn._t);
    btn._t = setTimeout(function () { btn.classList.remove(cls); if (lab) lab.textContent = old; }, 1600);
  }

  document.addEventListener('click', function (ev) {
    var t = ev.target;
    var cp = t.closest && t.closest('.copy');
    if (cp) {
      var id = cp.getAttribute('data-target');
      var box = id ? document.getElementById(id) : null;
      if (!box) { var p = cp.closest('.prompt'); box = p && $('pre', p); }
      if (!box) return;
      copyText(box.innerText.trim()).then(function () {
        flash(cp, 'done', 'span', '복사됨'); toast('프롬프트를 복사했어요');
      }, function () { toast('복사하지 못했어요. 길게 눌러 선택해 주세요'); });
      return;
    }
    var ing = t.closest && t.closest('.ing');
    if (ing) {
      var code = $('code', ing);
      copyText(code ? code.innerText.trim() : '').then(function () {
        flash(ing, 'done', 'em', '복사됨'); toast('문장을 복사했어요');
      });
      return;
    }
    var sh = t.closest && t.closest('[data-share]');
    if (sh) {
      var data = { title: document.title, url: location.href.split('#')[0] };
      if (navigator.share) { navigator.share(data).catch(function () {}); }
      else copyText(data.url).then(function () { toast('링크를 복사했어요'); });
      return;
    }
    var cl = t.closest && t.closest('[data-copylink]');
    if (cl) {
      copyText(location.href.split('#')[0]).then(function () { toast('링크를 복사했어요'); });
      return;
    }
    var fs = t.closest && t.closest('[data-focus-search]');
    if (fs) {
      var inp = $('.search input');
      if (inp) { ev.preventDefault(); $('#search').scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' }); setTimeout(function () { inp.focus({ preventScroll: true }); }, reduce ? 0 : 450); }
      return;
    }
    var top = t.closest && t.closest('.totop');
    if (top) { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); }
  });

  /* ---------- index: search + filter ---------- */
  var grid = $('.cards.grid');
  if (grid) {
    var input = $('.search input'), chips = $$('.chip[data-filter]'), empty = $('.empty'), filter = 'all';
    var norm = function (s) { return (s || '').toLowerCase().replace(/\s+/g, ''); };
    var cards = $$('.card', grid);
    var apply = function () {
      var q = norm(input ? input.value : ''), shown = 0;
      cards.forEach(function (c) {
        var okT = filter === 'all' || c.getAttribute('data-type') === filter;
        var okQ = !q || norm(c.getAttribute('data-kw') + ' ' + c.textContent).indexOf(q) > -1;
        var on = okT && okQ; c.hidden = !on; if (on) shown++;
      });
      if (empty) empty.hidden = shown > 0;
    };
    chips.forEach(function (ch) {
      ch.addEventListener('click', function () {
        filter = ch.getAttribute('data-filter');
        chips.forEach(function (o) { var on = o === ch; o.classList.toggle('on', on); o.setAttribute('aria-pressed', on ? 'true' : 'false'); });
        apply();
      });
    });
    if (input) {
      input.addEventListener('input', apply);
      input.addEventListener('keydown', function (e) { if (e.key === 'Escape') { input.value = ''; apply(); } });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === '/' && input && document.activeElement !== input && !/INPUT|TEXTAREA/.test((document.activeElement || {}).tagName)) { e.preventDefault(); input.focus(); }
    });
  }

  /* ---------- checklist (guide steps) ---------- */
  var KEY = 'mr-done-' + location.pathname;
  var doneBtns = $$('.done-btn[data-step]'), prog = $('.toc-prog');
  function load() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; } }
  function save(a) { try { localStorage.setItem(KEY, JSON.stringify(a)); } catch (e) {} }
  function renderProg() {
    if (!prog) return;
    var total = +prog.getAttribute('data-total') || doneBtns.length;
    var n = doneBtns.filter(function (b) { return b.getAttribute('aria-pressed') === 'true'; }).length;
    var i = $('i', prog), b = $('b', prog);
    if (i) i.style.setProperty('--p', (total ? Math.round(n / total * 100) : 0) + '%');
    if (b) b.textContent = n + '/' + total;
    prog.classList.toggle('all', n === total && total > 0);
  }
  if (doneBtns.length) {
    var st = load();
    doneBtns.forEach(function (b) {
      var k = b.getAttribute('data-step'), lab = $('span', b);
      var set = function (on) { b.setAttribute('aria-pressed', on ? 'true' : 'false'); if (lab) lab.textContent = on ? '완료했어요' : '이 단계 했어요'; };
      set(st.indexOf(k) > -1);
      b.addEventListener('click', function () {
        var on = b.getAttribute('aria-pressed') !== 'true', a = load().filter(function (x) { return x !== k; });
        if (on) a.push(k);
        save(a); set(on); renderProg();
        if (on && a.length === doneBtns.length) toast('모든 단계를 끝냈어요 🎉');
      });
    });
    renderProg();
  }

  /* ---------- toc active section ---------- */
  var tocLinks = $$('.toc-links a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    tocLinks.forEach(function (a) { var s = document.getElementById(a.getAttribute('href').slice(1)); if (s) map[s.id] = a; });
    var setOn = function (id) {
      tocLinks.forEach(function (a) { a.classList.toggle('on', a === map[id]); });
      var a = map[id], box = a && a.parentNode;
      if (a && box && box.scrollWidth > box.clientWidth) box.scrollTo({ left: a.offsetLeft - 16, behavior: reduce ? 'auto' : 'smooth' });
    };
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) setOn(en.target.id); });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  /* ---------- scroll-driven chrome ---------- */
  var bar = $('.readbar i'), fab = $('.fab'), totop = $('.totop'), cover = $('.cover'),
      pr = $('#prompts'), foot = $('.foot'), ticking = false;
  function onScroll() {
    ticking = false;
    var y = window.scrollY, h = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    if (totop) totop.classList.toggle('on', y > 600);
    if (fab) {
      var past = cover ? cover.getBoundingClientRect().bottom < 0 : y > 400;
      var near = false;
      [pr, foot].forEach(function (el) { if (el) { var r = el.getBoundingClientRect(); if (r.top < innerHeight && r.bottom > 0) near = true; } });
      var on = past && !near;
      fab.classList.toggle('on', on);
      fab.setAttribute('aria-hidden', on ? 'false' : 'true');
      var a = $('a', fab); if (a) a.tabIndex = on ? 0 : -1;
    }
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  window.addEventListener('resize', onScroll);
  onScroll();

  /* ---------- lazy autoplay video ---------- */
  var vids = $$('video[data-lazy]');
  if ('IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        var v = en.target;
        if (en.isIntersecting) {
          if (!v.src && v.dataset.src) { v.src = v.dataset.src; v.preload = 'auto'; }
          if (!reduce) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        } else if (!v.paused) v.pause();
      });
    }, { rootMargin: '200px 0px' });
    vids.forEach(function (v) { vio.observe(v); });
    // eager videos: pause off-screen to save battery
    $$('video:not([data-lazy])').forEach(function (v) {
      if (reduce) { v.removeAttribute('autoplay'); v.pause(); }
      vio.observe(v);
    });
  } else {
    vids.forEach(function (v) { v.src = v.dataset.src; });
  }
  // reduced motion: tap a video to play/pause
  if (reduce) $$('video').forEach(function (v) { v.addEventListener('click', function () { v.paused ? v.play() : v.pause(); }); });

  /* ---------- hero 미리: rotating tips + tap to hop ---------- */
  var tipEl = $('.bubble span[data-tips]'), mb = $('.miri-btn');
  if (tipEl) {
    var tips = []; try { tips = JSON.parse(tipEl.getAttribute('data-tips')); } catch (e) {}
    var ti = -1;
    var nextTip = function () {
      if (!tips.length) return;
      ti = (ti + 1) % tips.length;
      tipEl.classList.add('swap');
      setTimeout(function () { tipEl.textContent = tips[ti]; tipEl.classList.remove('swap'); }, 250);
    };
    if (!reduce) setInterval(function () { if (!document.hidden) nextTip(); }, 4200);
    if (mb) mb.addEventListener('click', function () {
      nextTip();
      if (reduce) return;
      mb.classList.remove('hop', 'b'); void mb.offsetWidth; mb.classList.add('hop');
      var k = 0, iv = setInterval(function () { mb.classList.toggle('b'); if (++k > 4) clearInterval(iv); }, 120);
      clearTimeout(mb._t); mb._t = setTimeout(function () { mb.classList.remove('hop', 'b'); }, 720);
    });
  }

  /* ---------- entrance motion (only when JS runs) ---------- */
  if (!reduce && 'IntersectionObserver' in window) {
    var targets = $$('.cards.grid .card, .tip, .tidx, .ing');
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); rio.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    targets.forEach(function (el) {
      if (el.getBoundingClientRect().top > innerHeight) { el.classList.add('rise'); rio.observe(el); }
    });
  }
})();
