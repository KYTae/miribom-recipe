"""미리봄 레시피 사이트 빌더 v2 — python3 build.py → index.html, <slug>/index.html 생성.
새 릴스가 나오면 data.py의 VOLUMES 맨 앞에 한 편을 추가하고 이 파일을 실행하세요."""
import html, os, re, json
from data import VOLUMES, TEMPLATE
from miri import MIRI

SITE = 'https://kytae.github.io/miribom-recipe/'
IG = 'https://www.instagram.com/ai.miribom/'
YT = 'https://www.youtube.com/@ai.miribom'
VER = '4'
e = html.escape

TYPE = {'guide': ('따라하기', 'HOW TO', 'guide'), 'tools': ('툴 추천', 'AI TOOLS', 'tools'), 'volume': ('프롬프트', 'PROMPT', 'prompt')}
def vtype(v): return v.get('type', 'volume')

FONTS = ('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>'
         '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500;600&display=swap">')

ICON = {
    'search': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    'back': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 18l-6-6 6-6"/></svg>',
    'next': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18l6-6-6-6"/></svg>',
    'copy': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M5 15V6a2 2 0 0 1 2-2h8"/></svg>',
    'share': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v12"/><path d="M7 8l5-5 5 5"/><path d="M5 13v5a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-5"/></svg>',
    'ig': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" class="dot"/></svg>',
    'yt': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="2.5" y="5.5" width="19" height="13" rx="4"/><path d="M10 9.5v5l4.5-2.5z" class="dot"/></svg>',
    'up': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 15l6-6 6 6"/></svg>',
    'ext': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6"/><path d="M20 4l-9 9"/><path d="M19 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h4"/></svg>',
    'check': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    'play': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z" class="dot"/></svg>',
}


def miri(poses, cls='', vb=None, label=''):
    """inline pixel 미리. poses: list of pose keys (first = default visible). CSS animates .pz groups / eyes."""
    if vb is None:
        bb = [MIRI[p]['bbox'] for p in poses]
        x0 = min(b[0] for b in bb) - 1; y0 = min(b[1] for b in bb) - 1; x1 = max(b[2] for b in bb) + 1; y1 = max(b[3] for b in bb)
        vb = f'{x0} {y0} {x1 - x0} {y1 - y0}'
    gs = ''.join(f'<g class="pz pz-{p}">{MIRI[p]["body"]}{MIRI[p]["face"]}</g>' for p in poses)
    aria = f' role="img" aria-label="{e(label)}"' if label else ' aria-hidden="true"'
    return f'<svg class="miri {cls}" viewBox="{vb}" shape-rendering="crispEdges"{aria}>{gs}</svg>'


def strip_tags(s): return re.sub(r'<[^>]+>', '', s)


def head(title, desc, base, page='home', og_img=None, url='', og_title=None, og_alt=''):
    img = og_img or f'{SITE}og/home.jpg'
    ogt = og_title or title
    alt = og_alt or ogt
    ld = ''
    if page == 'home':
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "WebSite", "name": "미리봄 레시피", "alternateName": ["miribom recipe", "미리봄"],
            "url": SITE, "inLanguage": "ko-KR", "description": desc,
            "publisher": {"@type": "Organization", "name": "미리봄 AI 매거진", "url": SITE, "logo": f"{SITE}icon-512.png", "sameAs": [IG]}}, ensure_ascii=False) + '</script>'
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{url}">
<meta name="application-name" content="미리봄 레시피">
<meta name="apple-mobile-web-app-title" content="미리봄 레시피">
<meta property="og:type" content="{'website' if page == 'home' else 'article'}">
<meta property="og:site_name" content="미리봄 레시피">
<meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{e(ogt)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:secure_url" content="{img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(ogt)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#0b0b0c">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="{base}favicon.ico" sizes="48x48">
<link rel="icon" href="{base}favicon-96.png" type="image/png" sizes="96x96">
<link rel="icon" href="{base}icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{base}apple-touch-icon.png">
<link rel="manifest" href="{base}site.webmanifest">
{ld}
{FONTS}
<link rel="stylesheet" href="{base}assets/style.css?v={VER}">
</head>
<body class="p-{page}">
<a class="skip" href="#main">본문으로 건너뛰기</a>
<div class="readbar" aria-hidden="true"><i></i></div>
<header class="bar"><div class="wrap bar-in">
  {'<a class="back" href="' + base + '" aria-label="전체 레시피로">' + ICON['back'] + '<span>전체 레시피</span></a>' if page != 'home' else ''}
  <a class="brand" href="{base}" aria-label="미리봄 레시피 홈"><img src="{base}assets/wordmark.svg" alt="miribom" width="104" height="29"><em>recipe</em></a>
  <nav class="bar-r">
    {'<button class="icon-btn" type="button" data-share aria-label="이 레시피 공유">' + ICON['share'] + '</button>' if page != 'home' else '<a class="icon-btn" href="#search" data-focus-search aria-label="레시피 검색">' + ICON['search'] + '</a>'}
    <a class="icon-btn" href="{IG}" target="_blank" rel="noopener" aria-label="인스타그램 @ai.miribom">{ICON['ig']}</a>
  </nav>
</div></header>
'''


def foot(base):
    return f'''<footer class="foot"><div class="wrap">
  <div class="foot-top">
    <div class="foot-miri">{miri(['sit'], 'm-sit')}</div>
    <img src="{base}assets/logo.svg" alt="" width="40" height="58">
    <p class="foot-big">남들보다 먼저 보는 AI 소식,<br><a href="{IG}" target="_blank" rel="noopener">{ICON['ig']}@ai.miribom</a></p>
    <p class="foot-sub">새 레시피는 인스타그램 릴스에 먼저 올라와요. 릴스 댓글에 키워드를 남기면 이 페이지 링크를 DM으로 보내드려요.</p>
    <div class="foot-cta"><a class="btn solid" href="{IG}" target="_blank" rel="noopener">{ICON['ig']}인스타그램 팔로우</a></div>
  </div>
  <p class="foot-legal">영상·프롬프트의 저작권은 각 원작자에게 있어요. 출처는 영상마다 표시했어요. 삭제 요청은 인스타그램 DM으로 주세요.<br>© <a href="{IG}" target="_blank" rel="noopener">@ai.miribom</a> · AI 매거진 미리봄</p>
</div></footer>
<button class="totop" type="button" aria-label="맨 위로">{ICON['up']}</button>
<div class="toast" role="status" aria-live="polite">{miri(["ball"], "m-toast")}<span class="toast-t"></span></div>
<script src="{base}assets/app.js?v={VER}" defer></script>
</body>
</html>
'''


def video(name, base, eager=False, label=''):
    src = f'{base}assets/clips/{name}.mp4'; poster = f'{base}assets/clips/{name}.jpg'
    al = f' aria-label="{e(label)}"' if label else ' aria-hidden="true"'
    if eager:
        return f'<video src="{src}" poster="{poster}" muted loop playsinline autoplay preload="metadata"{al}></video>'
    return f'<video data-lazy data-src="{src}" poster="{poster}" muted loop playsinline preload="none"{al}></video>'


def count(v):
    t = vtype(v)
    if t == 'tools': return len(v['tools'])
    if t == 'guide': return len(v['steps'])
    return sum(len(g['items']) for g in v['groups'])


def unit(v): return {'tools': '사이트', 'guide': '단계', 'volume': '프롬프트'}[vtype(v)]


def count_label(v):
    n = count(v); t = vtype(v)
    return f'{n}단계' if t == 'guide' else f'{unit(v)} {n}개'


def prompts_in(v):
    """every copyable prompt on the page (for the floating 'copy prompt' action + counts)"""
    t = vtype(v); out = []
    if t == 'volume':
        for g in v['groups']:
            for it in g['items']: out.append(it[3])
    if t == 'guide':
        for st in v['steps']:
            for p in st[3]:
                q = quoted(p)
                if q: out.append(q)
    return out


def quoted(s):
    m = re.search(r'"([^"]{40,})"', s)
    return m.group(1) if m else None


def tag_line(v):
    t = vtype(v)
    if t == 'volume': return 'X ' + v['groups'][0]['who']
    if t == 'tools': return v['tools'][0][6]
    return v.get('hero_tag', '')


def keywords(v):
    bits = [v['title'], v['short'], v['lede'], TYPE[vtype(v)][0]]
    t = vtype(v)
    if t == 'tools': bits += [x[2] + ' ' + x[0] for x in v['tools']]
    if t == 'guide': bits += [s[2] for s in v['steps']]
    if t == 'volume': bits += [it[2] for g in v['groups'] for it in g['items']] + [g['tool'] for g in v['groups']]
    return ' '.join(bits).lower()


def card(v, base, feat=False, idx=0):
    t = vtype(v); lab = TYPE[t]
    new = '<span class="new">NEW</span>' if v is VOLUMES[0] else ''
    shape = 'feat' if feat else 'std'
    return f'''<li class="card {shape}" data-type="{lab[2]}" data-kw="{e(keywords(v))}" style="--i:{idx}">
  <a href="{base}{v['slug']}/">
    <div class="card-media">{video(v['hero'], base)}<span class="card-no"><i>No.</i>{v['reel']}</span>{new}</div>
    <div class="card-body">
      <div class="card-kick"><span class="pill t-{lab[2]}">{lab[0]}</span><span>{count_label(v)}</span></div>
      <h3>{e(v['title'])}</h3>
      <p>{e(v['short'])}</p>
      {'<span class="card-go">레시피 열기' + ICON['next'] + '</span>' if feat else ''}
    </div>
  </a>
</li>'''


def index_page():
    base = ''
    n_prompt = sum(len(prompts_in(v)) for v in VOLUMES)
    chips = ''.join(f'<button type="button" class="chip{" on" if k == "all" else ""}" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{n}<b>{c}</b></button>'
                    for k, n, c in [('all', '전체', len(VOLUMES)), ('guide', '따라하기', sum(vtype(v) == 'guide' for v in VOLUMES)),
                                    ('prompt', '프롬프트', sum(vtype(v) == 'volume' for v in VOLUMES)), ('tools', '툴 추천', sum(vtype(v) == 'tools' for v in VOLUMES))])
    cards = ''.join(card(v, base, idx=i) for i, v in enumerate(VOLUMES))
    return head('미리봄 레시피', '미리봄 릴스에서 소개한 AI 영상·이미지 만드는 법과 프롬프트를 편마다 정리했어요. 누르면 바로 복사돼요.', base, og_title='미리봄 레시피 — 릴스에서 본 그 AI, 그대로 따라 만들어요', og_alt='미리봄 레시피: 릴스에서 본 그 AI, 그대로 따라 만들어요') + f'''<main id="main">
<section class="mast"><div class="wrap mast-in">
  <div class="mast-txt">
    <p class="eyebrow"><span class="dot-live"></span>미리봄 레시피 <span class="serif">Recipe</span> · No.{VOLUMES[0]['reel']}까지 업데이트</p>
    <h1 class="mast-h">릴스에서 본 그 AI,<br><mark>그대로 따라</mark> 만들어요</h1>
    <p class="mast-lede">미리봄 릴스에 나온 영상·이미지 제작법을 편마다 정리했어요. 프롬프트는 누르면 복사되고, 단계는 체크하며 따라가면 돼요.</p>
    <div class="mast-cta"><a class="btn solid" href="{VOLUMES[0]['slug']}/">최신 레시피 No.{VOLUMES[0]['reel']} 보기{ICON['next']}</a><a class="btn" href="#search" data-focus-search>{ICON['search']}레시피 찾기</a></div>
    <dl class="mast-stats"><div><dt>레시피</dt><dd>{len(VOLUMES)}</dd></div><div><dt>복사용 프롬프트</dt><dd>{n_prompt}</dd></div><div><dt>업데이트</dt><dd>매주</dd></div></dl>
  </div>
  <div class="stage" aria-label="미리봄 캐릭터 미리">
    <div class="stage-grid" aria-hidden="true"></div>
    <span class="floaty f1" aria-hidden="true"><b>/</b>prompt</span>
    <span class="floaty f2" aria-hidden="true">copy <b>✓</b></span>
    <span class="floaty f3" aria-hidden="true">720p <b>●</b></span>
    <p class="bubble" aria-live="off"><span data-tips='["프롬프트는 누르면 바로 복사돼요","릴스 댓글에 키워드 남기면 DM으로 링크가 와요","따라하기 단계는 체크해두면 기억돼요","새 레시피는 매주 올라와요"]'>안녕하세요, 미리예요!</span></p>
    <button class="miri-btn" type="button" aria-label="미리 누르기">
      <span class="miri-drop"><span class="miri-bob">{miri(['idle', 'wave', 'wave2', 'hop', 'cheer', 'cheer2'], 'm-hero')}</span></span>
      <span class="miri-shadow" aria-hidden="true"></span>
    </button>
  </div>
</div></section>

<section class="wrap how" aria-label="이용 방법">
  <ol>
    <li><span>01</span><div><b>릴스 보기</b><small>인스타그램 @ai.miribom</small></div></li>
    <li><span>02</span><div><b>댓글에 키워드</b><small>DM으로 이 사이트 링크 도착</small></div></li>
    <li><span>03</span><div><b>복사해서 따라 하기</b><small>프롬프트 한 번에 복사</small></div></li>
  </ol>
</section>

<section class="wrap latest" aria-label="최신 레시피">
  <div class="sec-h"><h2>최신 레시피</h2><span class="serif">latest</span></div>
  <ul class="cards one">{card(VOLUMES[0], base, feat=True)}</ul>
</section>

<section class="wrap all" id="search" aria-label="전체 레시피">
  <div class="sec-h"><h2>전체 레시피</h2><span class="serif">all recipes</span></div>
  <div class="tools-row">
    <label class="search">{ICON['search']}<input type="search" placeholder="Kling, 강아지, 프롬프트…" aria-label="레시피 검색" autocomplete="off" enterkeyhint="search"></label>
    <div class="chips" role="group" aria-label="종류">{chips}</div>
  </div>
  <ul class="cards grid">{cards}</ul>
  <div class="empty" hidden>{miri(["melt"], "m-melt")}<p><b>찾는 레시피가 없어요</b>다른 단어로 검색하거나 전체 보기를 눌러보세요.</p></div>
</section>
''' + foot(base)


# ---------- recipe page parts ----------
def cover(v, base, ctas, facts):
    t = vtype(v); lab = TYPE[t]
    shape = v.get('hero_shape', 'tall')
    fact = ''.join(f'<li><b>{e(str(a))}</b><span>{e(b)}</span></li>' for a, b in facts)
    btns = ''.join(f'<a class="btn{" solid" if i == 0 else ""}" href="{h}">{e(tx)}</a>' for i, (tx, h) in enumerate(ctas))
    return f'''<section class="cover wrap">
  <div class="cover-txt">
    <div class="kicker"><span class="serif">No.{v['reel']}</span><span class="pill t-{lab[2]}">{lab[0]}</span><span>릴스 #{v['reel']}</span></div>
    <h1>{e(v['title'])}</h1>
    <p class="lede">{e(v['lede'])}</p>
    <ul class="facts">{fact}</ul>
    <div class="ctas">{btns}</div>
  </div>
  <div class="cover-fig">
    <span class="peek" aria-hidden="true">{miri(['idle'], 'm-peek', vb='20 27 24 16')}</span>
    <figure class="cover-media {shape}">{video(v['hero'], base, eager=True, label=v['title'] + ' 예시 영상')}<figcaption class="tag">{e(tag_line(v))}</figcaption></figure>
  </div>
</section>'''


def toc(items, checklist=0):
    links = ''.join(f'<a href="#{i}">{e(n)}</a>' for i, n in items)
    prog = f'<span class="toc-prog" data-total="{checklist}"><i></i><b>0/{checklist}</b></span>' if checklist else ''
    return f'<nav class="toc" aria-label="이 페이지 목차"><div class="wrap toc-in"><div class="toc-links">{links}</div>{prog}</div></nav>'


def sec_h(title, serif, sub=''):
    return f'<div class="sec-h"><h2>{e(title)}</h2><span class="serif">{e(serif)}</span>{f"<p>{e(sub)}</p>" if sub else ""}</div>'


def prompt_block(text, label='프롬프트', pid=None):
    idattr = f' id="{pid}"' if pid else ''
    return f'''<div class="prompt"><div class="prompt-h"><span>{e(label)}</span><button class="copy" type="button">{ICON['copy']}<span>복사</span></button></div><pre{idattr}><code>{e(text)}</code></pre></div>'''


def more(v, base):
    i = VOLUMES.index(v)
    prev = VOLUMES[i + 1] if i + 1 < len(VOLUMES) else None   # older
    nxt = VOLUMES[i - 1] if i > 0 else None                    # newer
    pn = ''
    if prev: pn += f'<a class="pn prev" href="{base}{prev["slug"]}/"><small>{ICON["back"]}이전 레시피 · No.{prev["reel"]}</small><b>{e(prev["title"])}</b></a>'
    if nxt: pn += f'<a class="pn next" href="{base}{nxt["slug"]}/"><small>다음 레시피 · No.{nxt["reel"]}{ICON["next"]}</small><b>{e(nxt["title"])}</b></a>'
    others = [o for o in VOLUMES if o is not v][:6]
    return f'''<section class="wrap sec more" aria-label="다른 레시피">
  <div class="pns">{pn}</div>
  {sec_h('다른 레시피', 'more recipes')}
  <ul class="cards rail">{''.join(card(o, base, idx=k) for k, o in enumerate(others))}</ul>
  <div class="center"><a class="btn" href="{base}">전체 레시피 보기</a></div>
</section>'''


def share_band(v):
    return f'''<section class="wrap share-band" aria-label="공유">
  <div><b>도움이 됐다면 저장·공유해주세요</b><span>친구에게 보내면 같이 만들어볼 수 있어요</span></div>
  <div class="ctas"><button class="btn solid" type="button" data-share>{ICON['share']}공유하기</button><button class="btn" type="button" data-copylink>{ICON['copy']}링크 복사</button></div>
</section>'''


def notes_html(lines):
    return '<ul class="notes wrap">' + ''.join(f'<li>{e(x)}</li>' for x in lines) + '</ul>'


def fab(v):
    ps = prompts_in(v)
    if not ps: return ''
    return f'''<div class="fab" aria-hidden="false"><a class="fab-btn" href="#prompts">{ICON['copy']}<span>프롬프트 {len(ps)}개 바로 보기</span></a></div>'''


# ---------- page types ----------
def volume_page(v):
    base = '../'
    n = count(v)
    ing = []
    for g in v['groups']:
        ing.append(f'<div class="ing-who">X {e(g["who"])} <span>· {e(g["what"])} · {e(g["tool"])}</span></div>')
        for num, clip, ttl, phrase, desc in g['items']:
            ing.append(f'<button class="ing" type="button" aria-label="{num}번 문장 복사"><span class="n">{num}</span><span class="ing-t"><small>{e(ttl)}</small><code>{e(phrase)}</code></span><span class="c">{ICON["copy"]}<em>복사</em></span></button>')
    steps, k = [], 0
    for gi, g in enumerate(v['groups']):
        steps.append(f'<div class="src"><div><b>X {e(g["who"])}</b><span>{e(g["what"])} · {e(g["tool"])}</span></div><a href="{g["url"]}" target="_blank" rel="noopener">원작 보기{ICON["ext"]}</a></div>')
        for num, clip, ttl, phrase, desc in g['items']:
            steps.append(f'''<article class="step{' rev' if k % 2 else ''}" id="s{k+1}">
  <figure class="step-media {g['shape']}">{video(clip, base, label=ttl)}<figcaption class="tag">X {e(g['who'])}</figcaption></figure>
  <div class="step-txt">
    <div class="step-no"><span class="serif">{num}</span></div>
    <h3>{e(ttl)}</h3>
    <p>{desc}</p>
    {prompt_block(phrase, '이 문장을 프롬프트에')}
  </div>
</article>''')
            k += 1
    full = ''
    if v['template']:
        full = f'''<section class="wrap sec" id="full">{sec_h('완성 레시피', 'all in one', '회색 괄호 안만 내 장면으로 바꾸세요')}
  <div class="prompt big"><div class="prompt-h"><span>미리봄이 하나로 묶은 프롬프트 뼈대</span><button class="copy" type="button" data-target="tpl">{ICON['copy']}<span>전체 복사</span></button></div><pre id="tpl"><code>{tpl_html()}</code></pre></div>
  <p class="tip">팁: 01번처럼 첫 장면을 이미지로 먼저 만들어 참조로 넣으면 결과가 더 안정돼요.</p>
</section>'''
    stat_k, stat_v = v['stat']
    items = [('prompts', '재료'), ('steps', '만드는 법')] + ([('full', '완성 레시피')] if v['template'] else [])
    return head(f"{v['title']} | 미리봄 레시피", v['lede'], base, 'recipe', f'{SITE}og/{v["slug"]}.jpg', v['slug'] + '/', og_alt=f"미리봄 레시피 No.{v['reel']} {v['title']}") + f'''<main id="main">
{cover(v, base, [('재료부터 복사하기', '#prompts')] + ([('완성 레시피', '#full')] if v['template'] else []), [(n, '핵심 문장'), (len(v['groups']), '원작자'), (stat_v, stat_k)])}
{toc(items)}
<section class="wrap sec" id="prompts">{sec_h('재료', 'ingredients', '누르면 바로 복사돼요')}<div class="ings">{''.join(ing)}</div></section>
<section class="wrap sec" id="steps">{sec_h('만드는 법', 'method', '원작 영상과 함께 보기')}{''.join(steps)}</section>
{full}
{notes_html(['같은 문장을 넣어도 결과는 매번 달라요. 여러 번 돌려보고 고르세요.', '영상 AI는 서비스마다 유료 크레딧이 필요할 수 있어요.', '영상과 문장의 출처는 모두 원작자에게 있어요. 프롬프트 전문은 원작자 게시물에서 볼 수 있어요.'])}
{share_band(v)}
{more(v, base)}
</main>
''' + fab(v) + foot(base)


def tools_page(v):
    base = '../'
    n = count(v)
    rows, idx = [], []
    for i, (cat, beg, pro, why, url, clip, cred) in enumerate(v['tools']):
        host = url.replace('https://', '').replace('www.', '').rstrip('/')
        idx.append(f'<a class="tidx" href="#t{i+1}"><span class="n">{i+1:02d}</span><span class="tidx-t"><small>{e(cat)}</small><b>{e(pro)}</b></span>{ICON["next"]}</a>')
        rows.append(f'''<article class="step wide{' rev' if i % 2 else ''}" id="t{i+1}">
  <figure class="step-media wide">{video(clip, base, label=pro)}<figcaption class="tag">{e(cred)}</figcaption></figure>
  <div class="step-txt">
    <div class="step-no"><span class="serif">{i+1:02d}</span><span class="pill">{e(cat)}</span></div>
    <h3>{e(pro)}</h3>
    <div class="vs"><span class="lab">초보</span><span>{e(beg)}</span></div>
    <div class="vs pro"><span class="lab">고수</span><span>{e(why)}</span></div>
    <a class="btn go" href="{url}" target="_blank" rel="noopener">{e(host)} 바로가기{ICON['ext']}</a>
  </div>
</article>''')
    return head(f"{v['title']} | 미리봄 레시피", v['lede'], base, 'recipe', f'{SITE}og/{v["slug"]}.jpg', v['slug'] + '/', og_alt=f"미리봄 레시피 No.{v['reel']} {v['title']}") + f'''<main id="main">
{cover(v, base, [('한눈에 보기', '#list'), ('하나씩 보기', '#t1')], [(n, '분야'), (n, '사이트'), ('26.10', '기준')])}
{toc([('list', '한눈에 보기'), ('steps', '분야별 고수 픽')])}
<section class="wrap sec" id="list">{sec_h('한눈에 보기', 'index', '누르면 설명으로 이동해요')}<div class="tidxs">{''.join(idx)}</div></section>
<section class="wrap sec" id="steps">{sec_h('분야별 고수 픽', 'picks', '공식 영상과 함께 보기')}{''.join(rows)}</section>
{notes_html(['2026년 10월 기준이에요. 기능과 요금제는 자주 바뀌니 공식 사이트에서 확인하세요.', '"초보" 칸은 틀렸다는 뜻이 아니라, 대부분 처음 쓰는 기본 선택지라는 뜻이에요.', '영상은 각 회사 공식 계정과 크리에이터가 올린 영상이에요. 출처는 영상 위에 표시했어요.'])}
{share_band(v)}
{more(v, base)}
</main>
''' + foot(base)


def guide_point(p):
    q = quoted(p)
    if q:
        before = p[:p.find('"')].strip().rstrip(':').strip()
        lab = before if before else '프롬프트'
        return f'<li class="has-prompt">{prompt_block(q, lab)}</li>'
    return f'<li>{e(p)}</li>'


def guide_page(v):
    base = '../'
    steps = []
    for i, st in enumerate(v['steps']):
        clip, cred, ttl, pts = st[:4]
        shape = st[4] if len(st) > 4 else ('stack' if '17-3' in clip else 'tall')
        lis = ''.join(guide_point(x) for x in pts)
        steps.append(f'''<article class="step{' rev' if i % 2 else ''}" id="s{i+1}">
  <figure class="step-media {shape}">{video(clip, base, label=ttl)}<figcaption class="tag">{e(cred)}</figcaption></figure>
  <div class="step-txt">
    <div class="step-no"><span class="serif">{i+1:02d}</span><span class="pill">STEP {i+1}</span></div>
    <h3>{e(ttl)}</h3>
    <ul class="pts">{lis}</ul>
    <button class="done-btn" type="button" data-step="{i}" aria-pressed="false">{ICON['check']}<span>이 단계 했어요</span></button>
  </div>
</article>''')
    rows = ''.join(f'<div class="prow"><span>{e(a)}</span><b>{e(b)}</b></div>' for a, b in v['price'])
    alts = ''.join(f'''<a class="alt" href="{u}" target="_blank" rel="noopener"><img src="{base}assets/logo_{k}.png" alt="" width="48" height="48" loading="lazy"><div><b>{e(n)}</b><span>{e(d)}</span></div>{ICON['ext']}</a>''' for k, n, d, u in v['alts'])
    tips = ''.join(f'<li><span>{i+1}</span><p>{e(t)}</p></li>' for i, t in enumerate(v['tips']))
    ps = prompts_in(v)
    prompts_sec = ''
    if ps:
        blocks = ''.join(prompt_block(p, f'프롬프트 {i+1}') for i, p in enumerate(ps))
        prompts_sec = f'<section class="wrap sec" id="prompts">{sec_h("프롬프트 모아보기", "copy & paste", "단계에 나온 프롬프트를 한곳에 모았어요")}{blocks}</section>'
    items = [('steps', v.get('steps_title', '만드는 법'))] + ([('prompts', '프롬프트')] if ps else []) + [('price', v.get('price_title', '가격')), ('tips', '꿀팁')]
    facts = v.get('facts', [('3', '단계'), ('~10', '분'), ('$2~', '15초 1개')])
    ctas = v.get('ctas', [('만드는 법 보기', '#s1'), ('가격·무료 방법', '#price')])
    return head(f"{v['title']} | 미리봄 레시피", v['lede'], base, 'recipe', f'{SITE}og/{v["slug"]}.jpg', v['slug'] + '/', og_alt=f"미리봄 레시피 No.{v['reel']} {v['title']}") + f'''<main id="main">
{cover(v, base, ctas, facts)}
{toc(items, checklist=len(v['steps']))}
<section class="wrap sec" id="steps">{sec_h(v.get('steps_title', '만드는 법'), 'method', v.get('steps_sub', ''))}{''.join(steps)}</section>
{prompts_sec}
<section class="wrap sec" id="price">{sec_h(v.get('price_title', '가격'), v.get('price_it', 'price'), v.get('price_sub', ''))}
  <div class="table">{rows}</div>
  {f'<h3 class="sub3">무료로 해보려면</h3><div class="alts">{alts}</div>' if alts else ''}
</section>
<section class="wrap sec" id="tips">{sec_h('꿀팁', 'tips')}<ol class="tips">{tips}</ol></section>
{notes_html(v['notes'])}
{share_band(v)}
{more(v, base)}
</main>
''' + fab(v) + foot(base)


def tpl_html():
    out = []
    for line in TEMPLATE.split('\n'):
        s = e(line)
        if line.startswith('['): s = f'<span class="k">{s}</span>'
        elif line.startswith('('): s = f'<span class="ko">{s}</span>'
        else:
            for tg in ('(인물', '(장소', '(나오면', '(첫 장면', '(전개)', '(클라이맥스)'):
                i = line.find(tg)
                if i > 0: s = e(line[:i]) + f'<span class="ko">{e(line[i:])}</span>'; break
        out.append(s)
    return '\n'.join(out)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root, 'index.html'), 'w') as f: f.write(index_page())
    for v in VOLUMES:
        d = os.path.join(root, v['slug']); os.makedirs(d, exist_ok=True)
        t = vtype(v)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(tools_page(v) if t == 'tools' else (guide_page(v) if t == 'guide' else volume_page(v)))
    open(os.path.join(root, '.nojekyll'), 'w').close()
    with open(os.path.join(root, 'site.webmanifest'), 'w') as f:
        json.dump({"name": "미리봄 레시피", "short_name": "미리봄 레시피", "start_url": "/miribom-recipe/", "scope": "/miribom-recipe/", "display": "standalone",
                   "background_color": "#0b0b0c", "theme_color": "#0b0b0c", "lang": "ko",
                   "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
                             {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]}, f, ensure_ascii=False)
    with open(os.path.join(root, 'robots.txt'), 'w') as f: f.write(f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
    with open(os.path.join(root, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{p}</loc></url>' for p in [''] + [v['slug'] + '/' for v in VOLUMES]) + '</urlset>\n')
    with open(os.path.join(root, '404.html'), 'w') as f:
        f.write(head('페이지를 찾을 수 없어요 | 미리봄 레시피', '', '/miribom-recipe/', 'recipe') + '<main id="main" class="wrap nf">' + miri(['melt'], 'm-melt m-nf') + '<p class="serif nf-big">404</p><h1>레시피를 찾을 수 없어요</h1><p>주소가 바뀌었거나 아직 올라오지 않은 레시피예요.</p><a class="btn solid" href="/miribom-recipe/">전체 레시피 보기</a></main>' + foot('/miribom-recipe/'))
    print('built', [v['slug'] for v in VOLUMES])
