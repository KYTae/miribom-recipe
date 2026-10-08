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

  /* ---------- hero 미리: pose show (transforms + bubble lines) ---------- */
  var hero = $('.m-hero'), mb = $('.miri-btn'), tipEl = $('.bubble .bubble-t');
  if (hero && mb) {
    var SCENES = [
      { p: ['wave', 'wave2'], ms: 300, eyes: 'happy', t: '안녕하세요, 미리예요!' },
      { p: ['mega', 'mega2'], ms: 380, badge: '속보!', t: '새 레시피가 매주 올라와요!' },
      { p: ['stir', 'stir2'], ms: 420, t: '오늘의 프롬프트, 보글보글 끓이는 중' },
      { p: ['qmark'], anim: 'tilt', badge: '?', t: '오늘은 뭘 만들어볼까요?' },
      { p: ['copy'], anim: 'shake', t: '누르면 바로 복사! 붙여넣기만 하면 돼요' },
      { p: ['reporter'], t: '새 AI 소식, 제가 먼저 취재해요' },
      { p: ['flip', 'flip2'], ms: 450, t: '프롬프트 한 장 뒤집기!' },
      { p: ['bulb', 'bulb2'], ms: 520, t: '아하! 이런 방법이 있었네요' },
      { p: ['surf', 'surf2'], ms: 500, eyes: 'happy', t: '요즘 AI 트렌드, 같이 타요!' },
      { p: ['check'], anim: 'shake', t: '따라 한 단계는 체크해두면 기억돼요' },
      { p: ['cam', 'cam', 'cam', 'cam2'], ms: 260, t: '원작 영상과 출처까지 같이 정리했어요' },
      { p: ['taste'], eyes: 'happy', t: '음~ 이 프롬프트 맛있다!' },
      { p: ['bang'], anim: 'shake', t: '새 AI 기능은 나오자마자 정리해요' },
      { p: ['laptop', 'laptop2'], ms: 160, t: '레시피 열심히 정리 중…' },
      { p: ['play'], anim: 'tilt', t: '영상 보면서 그대로 따라 해요' },
      { p: ['magx'], anim: 'tilt', t: '검색창에 툴 이름을 넣어보세요' },
      { p: ['pour', 'pour2'], ms: 360, t: '설정값은 계량컵처럼 정확하게' },
      { p: ['anchor'], t: '오늘의 AI 뉴스, 미리가 전해드려요' },
      { p: ['surprise'], anim: 'shake', t: '이게 된다고?!' },
      { p: ['arrow'], anim: 'shake', t: '릴스 댓글에 키워드 → DM으로 링크가 와요' },
      { p: ['star'], anim: 'tilt', t: '마음에 들면 저장해두세요' },
      { p: ['ball'], anim: 'roll', t: '데굴데굴~ 다음 레시피로!' },
      { p: ['sleepy', 'sleepy2'], ms: 900, eyes: 'blink', t: '밤새 AI 뉴스 보느라… 쿨쿨' },
      { p: ['bubble'], anim: 'tilt', t: '궁금한 건 인스타 DM으로 물어보세요' },
      { p: ['cheer', 'cheer2'], ms: 260, eyes: 'happy', t: '오늘도 하나 만들어봐요!' },
      { p: ['hearts', 'hearts2'], ms: 450, eyes: 'happy', t: '도움이 됐다면 친구에게 공유해 주세요' }
    ];
    var groups = {};
    $$('.pz', hero).forEach(function (g) { var k = (g.getAttribute('class').match(/pz-(\S+)/) || [])[1]; if (k) groups[k] = g; });
    var bob = $('.miri-bob'), badge = $('.shout'), cur = null, si = -1, fi = 0, frameT, sceneT, morphT, sayT, badgeT, animT, lastTap = 0;
    var show = function (k) { if (cur) cur.classList.remove('on'); cur = groups[k] || groups.idle; cur.classList.add('on'); };
    var say = function (txt) {
      if (!tipEl) return;
      clearTimeout(sayT); tipEl.classList.add('swap');
      sayT = setTimeout(function () { tipEl.textContent = txt; tipEl.classList.remove('swap'); }, 200);
    };
    var puff = function () {
      if (reduce || $$('.puff', mb.parentNode).length > 6) return;
      for (var i = 0; i < 6; i++) {
        var d = document.createElement('i'); d.className = 'puff';
        var a = Math.PI * (1.05 + i * 0.18);
        d.style.setProperty('--dx', Math.cos(a) * 46 + 'px'); d.style.setProperty('--dy', Math.sin(a) * 34 + 'px');
        mb.parentNode.appendChild(d); void d.offsetWidth; d.classList.add('go');
        setTimeout(function (n) { return function () { n.remove(); }; }(d), 600);
      }
    };
    var play = function (n, cls) {
      // cancel everything from the previous scene so timers never stack up (rapid taps used to leave
      // several frame intervals running at once → poses flickering forever)
      clearInterval(frameT); clearTimeout(sceneT); clearTimeout(morphT); clearTimeout(badgeT); clearTimeout(animT);
      si = (n + SCENES.length) % SCENES.length; var sc = SCENES[si]; fi = 0;
      // morph: squash through a ball, then pop into the new form
      show('ball'); hero.removeAttribute('data-eyes');
      bob.classList.remove('poof', 'hop', 'a-tilt', 'a-shake', 'a-roll'); void bob.offsetWidth; bob.classList.add(cls || 'poof'); puff();
      morphT = setTimeout(function () {
        show(sc.p[0]);
        if (sc.eyes) hero.setAttribute('data-eyes', sc.eyes); else hero.removeAttribute('data-eyes');
        if (sc.anim && !reduce) animT = setTimeout(function () { bob.classList.remove('poof', 'hop'); bob.classList.add('a-' + sc.anim); }, 420);
        if (sc.p.length > 1) frameT = setInterval(function () { fi = (fi + 1) % sc.p.length; show(sc.p[fi]); }, sc.ms || 300);
      }, 140);
      say(sc.t);
      if (badge) { badge.classList.remove('on'); if (sc.badge) { badge.textContent = sc.badge; badgeT = setTimeout(function () { badge.classList.add('on'); }, 220); } }
      if (!reduce) sceneT = setTimeout(function next() { if (document.hidden) { sceneT = setTimeout(next, 1000); return; } play(si + 1); }, 3800);
    };
    hero.classList.add('js'); show('idle');
    if (reduce) { mb.addEventListener('click', function () { si = (si + 1) % SCENES.length; say(SCENES[si].t); }); }
    else {
      setTimeout(function () { play(0); }, 1500);   // after the drop-in landing
      mb.addEventListener('click', function () {
        var now = Date.now(); if (now - lastTap < 700) return;   // one morph at a time
        lastTap = now; play(si + 1, 'hop');
      });
      bob.addEventListener('animationend', function (e) { if (e.animationName === 'poof' || e.animationName === 'hop') bob.classList.remove('poof', 'hop'); });
    }
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

/* ---------- 2026-10-09: prompt maker + glossary search ---------- */
(function () {
  var mk = document.getElementById('maker');
  if (mk) {
    var out = document.getElementById('mk-out');
    var tip = document.getElementById('mk-tip');
    var cur = 'text';
    function val(form, n) { var el = form.querySelector('[name="' + n + '"]'); return el ? el.value.trim() : ''; }
    function parts(v) { return v ? v.split('|') : []; }
    function lines(v) { return v.split('\n').map(function (s) { return s.trim(); }).filter(Boolean); }
    function build() {
      var f = mk.querySelector('[data-mk-form="' + cur + '"]'); var t = '';
      if (cur === 'text') {
        var task = val(f, 'task'); if (!task) { out.textContent = '“무엇을 해달라고 할까요?” 칸을 먼저 채워주세요.'; return; }
        var role = val(f, 'role'), who = val(f, 'who'), ctx = val(f, 'ctx'), rules = lines(val(f, 'rules')), fmt = val(f, 'fmt');
        if (role) t += '너는 ' + role + '야.\n';
        t += task.replace(/[.。]?$/, '') + '.\n';
        if (who) t += '\n[읽는 사람 / 쓰는 곳]\n' + who + '\n';
        if (ctx) t += '\n[내 상황·재료]\n' + ctx + '\n';
        if (rules.length) t += '\n[꼭 지킬 조건]\n' + rules.map(function (r) { return '- ' + r; }).join('\n') + '\n';
        if (fmt) t += '\n[결과 모양]\n' + fmt + '\n';
        t += '\n모르는 정보는 지어내지 말고 [확인 필요]로 표시하거나 먼저 질문해줘.';
        tip.textContent = '팁: 결과가 길면 “핵심만 3줄로”, 엉뚱하면 “질문 3개를 먼저 해줘”라고 이어서 보내세요.';
      } else if (cur === 'image') {
        var subj = val(f, 'subj'); if (!subj) { out.textContent = '“무엇을 그릴까요?” 칸을 먼저 채워주세요.'; return; }
        var st = parts(val(f, 'style')), li = parts(val(f, 'light')), co = parts(val(f, 'comp')), ra = parts(val(f, 'ratio'));
        var scene = val(f, 'scene'), keep = val(f, 'keep'), text = val(f, 'text');
        t = subj + (scene ? ', 배경은 ' + scene : '') + '.\n';
        t += '스타일: ' + (st[1] || '') + (li[0] ? ', ' + li[0] : '') + (co[0] ? ', ' + co[0] : '') + '.\n';
        if (keep) t += '첨부한 사진의 ' + keep + '은(는) 절대 바꾸지 마.\n';
        if (text) t += '이미지 안에 “' + text + '” 글자를 또렷하게 넣어줘.\n';
        t += '비율: ' + (ra[0] || '') + '.\n';
tip.textContent = '팁: 사진을 바꾸는 거라면 사진을 꼭 첨부하고 “바꾸면 안 되는 것”을 채우세요. Midjourney처럼 영어가 더 잘 먹히는 곳이라면 ChatGPT에 이 프롬프트와 함께 “영어 이미지 프롬프트로 바꿔줘”라고 하세요.';
      } else if (cur === 'video') {
        var vs = val(f, 'subj'); if (!vs) { out.textContent = '“누가 무엇을 해요?” 칸을 먼저 채워주세요.'; return; }
        var cam = parts(val(f, 'cam')), sty = parts(val(f, 'style')), len = parts(val(f, 'len')), sc = val(f, 'scene'), kp = val(f, 'keep');
        t = '장면: ' + vs + (sc ? ' (장소: ' + sc + ')' : '') + '\n카메라: ' + cam[0] + '\n느낌: ' + sty[0] + '\n길이: ' + len[0] + '\n';
        if (kp) t += '첨부한 이미지의 ' + kp + '은(는) 처음부터 끝까지 그대로 유지.\n';
tip.textContent = '팁: 처음엔 5초로 테스트하세요. 영상 AI는 영어를 더 정확히 알아들어요. ChatGPT에 이 프롬프트를 붙이고 “영상 AI용 영어 프롬프트로 바꿔줘”라고 하면 돼요.';
      } else {
        var what = val(f, 'what'); if (!what) { out.textContent = '“무엇을 만들까요?” 칸을 먼저 채워주세요.'; return; }
        var who2 = val(f, 'who'), must = lines(val(f, 'must')), look = val(f, 'look'), wh = parts(val(f, 'where'));
        t = what.replace(/[.。]?$/, '') + '을(를) 만들어줘.\n';
        if (who2) t += '쓰는 사람: ' + who2 + '\n';
        if (must.length) t += '\n[꼭 있어야 할 기능]\n' + must.map(function (r, i) { return (i + 1) + '. ' + r; }).join('\n') + '\n';
        if (look) t += '\n[화면 느낌]\n' + look + '\n';
        if (wh[0] === 'app') t += '\n[만드는 방식]\nHTML 파일 하나로 만들어서 바로 미리보기로 볼 수 있게 해줘. 모바일 화면에서도 보기 좋게.\n';
        else if (wh[0] === 'roblox') t += '\n[만드는 방식]\n지금 열려 있는 로블록스 스튜디오에 직접 만들어줘. 스크립트는 역할별로 나눠 넣고, 다 만들면 플레이 모드로 테스트해서 오류를 고쳐줘.\n';
        else t += '\n[만드는 방식]\n먼저 계획(화면·파일 구조)을 짧게 보여주고 시작해. 단계마다 실행해서 스크린샷으로 확인하고, 마지막에 실행 방법을 알려줘.\n';
        t += '\n처음엔 핵심 기능만 되는 작은 버전부터 만들고, 내가 써본 뒤 하나씩 늘려가자.';
        tip.textContent = '팁: 만든 뒤엔 “[증상] → [원하는 느낌]” 형식으로 고칠 점을 하나씩 말하세요. 27번 레시피에 고치는 문장이 더 있어요.';
      }
      out.textContent = t;
    }
    mk.addEventListener('input', build);
    mk.addEventListener('change', build);
    mk.addEventListener('click', function (ev) {
      var tb = ev.target.closest('[data-mk]');
      if (tb) {
        cur = tb.getAttribute('data-mk');
        mk.querySelectorAll('[data-mk]').forEach(function (b) { var on = b === tb; b.classList.toggle('on', on); b.setAttribute('aria-pressed', on ? 'true' : 'false'); });
        mk.querySelectorAll('[data-mk-form]').forEach(function (fm) { fm.hidden = fm.getAttribute('data-mk-form') !== cur; });
        build(); return;
      }
      var ex = ev.target.closest('[data-fill]');
      if (ex) {
        var fm = ex.closest('form'); var el = fm.querySelector('[name="' + ex.getAttribute('data-fill') + '"]');
        if (el) { if (el.tagName === 'TEXTAREA' && el.name === 'rules' && el.value) el.value += '\n' + ex.getAttribute('data-v'); else el.value = ex.getAttribute('data-v'); }
        build();
      }
    });
  }
  var gs = document.querySelector('[data-gl-search]');
  if (gs) {
    gs.addEventListener('input', function () {
      var q = gs.value.trim().toLowerCase();
      document.querySelectorAll('.gl-list > div').forEach(function (d) { d.hidden = q && d.getAttribute('data-term').indexOf(q) < 0; });
      document.querySelectorAll('.gl-sec').forEach(function (s) { s.hidden = !s.querySelector('.gl-list > div:not([hidden])'); });
    });
  }
})();
