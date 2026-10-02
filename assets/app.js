(function () {
  var toast = document.querySelector('.toast');
  var tt;
  function say(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('on');
    clearTimeout(tt);
    tt = setTimeout(function () { toast.classList.remove('on'); }, 1600);
  }
  function selectEl(el) {
    try {
      var r = document.createRange(); r.selectNodeContents(el);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      say('선택됐어요. 길게 눌러 복사하세요');
    } catch (e) {}
  }
  function copyFrom(el, btn, label) {
    var text = el.textContent;
    var ok = function () {
      say('복사됐어요');
      if (btn) {
        btn.textContent = '복사됨'; btn.classList.add('done');
        setTimeout(function () { btn.textContent = label; btn.classList.remove('done'); }, 1400);
      }
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(ok, function () { selectEl(el); });
    } else { selectEl(el); }
  }
  document.querySelectorAll('.copy').forEach(function (b) {
    b.addEventListener('click', function () { copyFrom(b.parentElement.querySelector('code'), b, '복사'); });
  });
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () { copyFrom(document.getElementById(b.getAttribute('data-copy')), null, ''); });
  });

  // play clips only while on screen (saves data in Instagram's in-app browser)
  var vids = [].slice.call(document.querySelectorAll('video[data-lazy]'));
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;
  if (!('IntersectionObserver' in window)) {
    vids.forEach(function (v) { v.src = v.getAttribute('data-src'); v.play && v.play().catch(function () {}); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      var v = e.target;
      if (e.isIntersecting) {
        if (!v.src) { v.src = v.getAttribute('data-src'); }
        var p = v.play(); if (p && p.catch) p.catch(function () {});
      } else { v.pause(); }
    });
  }, { rootMargin: '200px 0px' });
  vids.forEach(function (v) { io.observe(v); });
})();
