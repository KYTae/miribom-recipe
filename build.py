"""미리봄 레시피 사이트 빌더: python3 build.py → index.html, <slug>/index.html 생성."""
import html, os
from data import VOLUMES, TEMPLATE

IG = 'https://www.instagram.com/ai.miribom/'
YT = 'https://www.youtube.com/@ai.miribom'
e = html.escape
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hahmlet:wght@500;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=Instrument+Serif:ital@0;1&display=swap">'
         '<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">')


def head(title, desc, base):
    return f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta name="theme-color" content="#000000">
<link rel="icon" href="{base}assets/logo.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<header class="bar"><div class="wrap">
  <a class="brand" href="{base}" aria-label="미리봄 레시피 홈"><img src="{base}assets/wordmark.svg" alt="miribom"><span>recipe</span></a>
  <nav><a href="{base}">레시피</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a></nav>
</div></header>
'''


def foot(base):
    return f'''<footer>
  <div><div class="big">남들보다 먼저 보는 AI 소식,<br><em>@ai.miribom</em></div><p>새 레시피는 인스타그램 릴스와 유튜브 쇼츠에 먼저 올라와요.</p></div>
  <div class="ctas"><a class="btn solid" href="{IG}" target="_blank" rel="noopener">인스타그램 팔로우</a><a class="btn" href="{YT}" target="_blank" rel="noopener">유튜브 쇼츠</a></div>
</footer>
</main>
<div class="toast" role="status" aria-live="polite"></div>
<script src="{base}assets/app.js"></script>
</body>
</html>
'''


def video(name, base, eager=False):
    src = f'{base}assets/clips/{name}.mp4'
    poster = f'{base}assets/clips/{name}.jpg'
    if eager:
        return f'<video src="{src}" poster="{poster}" muted loop playsinline autoplay preload="auto"></video>'
    return f'<video data-lazy data-src="{src}" poster="{poster}" muted loop playsinline preload="none"></video>'


def count(v):
    if v.get('type') == 'tools':
        return len(v['tools'])
    return sum(len(g['items']) for g in v['groups'])


def issue_row(v, base):
    return f'''<li class="issue"><a href="{base}{v['slug']}/">
  <div class="no"><small>No.</small>{v['reel']}</div>
  <div class="tt"><b>{e(v['title'])}</b><span>{e(v['short'])} · {'사이트' if v.get('type') == 'tools' else '핵심 문장'} {count(v)}개 · 릴스 #{v['reel']}</span><em>레시피 열기</em></div>
  <div class="pic">{video(v['hero'], base)}</div>
</a></li>'''


def tpl_html():
    out = []
    for line in TEMPLATE.split('\n'):
        s = e(line)
        if line.startswith('['):
            s = f'<span class="k">{s}</span>'
        elif line.startswith('('):
            s = f'<span class="ko">{s}</span>'
        else:
            for tag in ('(인물', '(장소', '(나오면', '(첫 장면', '(전개)', '(클라이맥스)'):
                i = line.find(tag)
                if i > 0:
                    s = e(line[:i]) + f'<span class="ko">{e(line[i:])}</span>'
                    break
        out.append(s)
    return '\n'.join(out)


def volume_page(v):
    base = '../'
    n = count(v)
    # 재료 (ingredients)
    ings = []
    for g in v['groups']:
        ings.append(f'<div class="ing-who">X {e(g["who"])} · {e(g["what"])}</div>')
        for num, clip, ttl, phrase, desc in g['items']:
            ings.append(f'<button class="ing" type="button" aria-label="{num}번 문장 복사"><span class="n">{num}</span><code>{e(phrase)}</code><span class="c">복사</span></button>')
    # 만드는 법 (steps)
    steps, k = [], 0
    for gi, g in enumerate(v['groups']):
        steps.append(f'<div class="src" id="g{gi+1}"><div><b>X {e(g["who"])}</b><br><span>{e(g["what"])} · {e(g["tool"])}</span></div><a href="{g["url"]}" target="_blank" rel="noopener">원작 보기 ↗</a></div>')
        for num, clip, ttl, phrase, desc in g['items']:
            cls = 'step' + (' flip' if k % 2 else '') + (' wide-clip' if g['shape'] == 'wide' else '')
            k += 1
            steps.append(f'''<article class="{cls}">
  <div class="clip {g['shape']}">{video(clip, base)}<span class="tag">X {e(g['who'])}</span></div>
  <div class="txt">
    <div class="num">{num}</div>
    <h3>{e(ttl)}</h3>
    <p>{desc}</p>
    <div class="quote"><code>{e(phrase)}</code><button class="copy" type="button">복사</button></div>
  </div>
</article>''')
    full = ''
    full_btn = ''
    if v['template']:
        full = f'''<section class="sec" id="full">
  <div class="sec-h"><h2>완성 레시피</h2><span class="it">all in one</span><p>회색 괄호 안만 내 장면으로 바꾸세요</p></div>
  <div class="full">
    <div class="full-h"><span>위 문장들을 미리봄이 하나로 묶은 프롬프트 뼈대</span><button class="btn solid" type="button" data-copy="tpl" style="padding:8px 14px;font-size:13px">전체 복사</button></div>
    <pre id="tpl">{tpl_html()}</pre>
  </div>
  <p class="tip">팁: 01번처럼 첫 장면을 이미지로 먼저 만들어 참조로 넣으면 결과가 더 안정돼요.</p>
</section>'''
        full_btn = '<a class="btn" href="#full">완성 레시피</a>'
    others = [o for o in VOLUMES if o['slug'] != v['slug']]
    more = ''
    if others:
        more = f'''<section class="sec"><div class="sec-h"><h2>다른 레시피</h2><span class="it">more</span></div><ul class="index">{''.join(issue_row(o, base) for o in others)}</ul></section>'''
    stat_k, stat_v = v['stat']
    return head(f"{v['title']} | 미리봄 레시피", v['lede'], base) + f'''<main class="wrap">
<section class="cover">
  <div>
    <div class="kicker"><span class="it">Recipe No.{v['reel']}</span><span>릴스 #{v['reel']} · {v['part']}</span></div>
    <h1>{e(v['title'])}</h1>
    <p class="lede">{e(v['lede'])}</p>
    <ul class="facts"><li><b>{n}</b><span>핵심 문장</span></li><li><b>{len(v['groups'])}</b><span>원작자</span></li><li><b>{e(stat_v)}</b><span>{e(stat_k)}</span></li></ul>
    <div class="ctas"><a class="btn solid" href="#ingredients">재료부터 보기</a>{full_btn}</div>
  </div>
  <div class="hero-clip {v['hero_shape']}">{video(v['hero'], base, eager=True)}<span class="tag">X {e(v['groups'][0]['who'])}</span></div>
</section>

<section class="sec" id="ingredients">
  <div class="sec-h"><h2>재료</h2><span class="it">ingredients</span><p>누르면 바로 복사돼요</p></div>
  <div class="ings">{''.join(ings)}</div>
</section>

<section class="sec" id="steps">
  <div class="sec-h"><h2>만드는 법</h2><span class="it">method</span><p>원작 영상과 함께 보기</p></div>
  {''.join(steps)}
</section>
{full}
<ul class="notes">
  <li>같은 문장을 넣어도 결과는 매번 달라요. 여러 번 돌려보고 고르세요.</li>
  <li>영상 AI는 서비스마다 유료 크레딧이 필요할 수 있어요.</li>
  <li>영상과 문장의 출처는 모두 원작자에게 있어요. 프롬프트 전문은 원작자 게시물에서 볼 수 있어요.</li>
</ul>
{more}
''' + foot(base)


def tools_page(v):
    base = '../'
    n = count(v)
    rows = []
    for i, (cat, beg, pro, why, url, clip, cred) in enumerate(v['tools']):
        cls = 'step' + (' flip' if i % 2 else '') + ' wide-clip'
        host = url.replace('https://', '').replace('www.', '')
        rows.append(f'''<article class="{cls}">
  <div class="clip wide">{video(clip, base)}<span class="tag">{e(cred)}</span></div>
  <div class="txt">
    <div class="num">{i+1:02d}</div>
    <div class="cat">{e(cat)}</div>
    <h3>{e(pro)}</h3>
    <div class="vs"><span class="lab">초보</span><span>{e(beg)}</span></div>
    <p>{e(why)}</p>
    <a class="go" href="{url}" target="_blank" rel="noopener">{e(host)} 바로가기 ↗</a>
  </div>
</article>''')
    idx = ''.join(f'<a class="ing" href="#t{i+1}" style="text-decoration:none"><span class="n">{i+1:02d}</span><code>{e(t[2])}</code><span class="c">{e(t[0])}</span></a>' for i, t in enumerate(v['tools']))
    rows = [r.replace('<article class="', f'<article id="t{i+1}" class="', 1) for i, r in enumerate(rows)]
    others = [o for o in VOLUMES if o['slug'] != v['slug']]
    more = f'''<section class="sec"><div class="sec-h"><h2>다른 레시피</h2><span class="it">more</span></div><ul class="index">{''.join(issue_row(o, base) for o in others)}</ul></section>''' if others else ''
    return head(f"{v['title']} | 미리봄 레시피", v['lede'], base) + f'''<main class="wrap">
<section class="cover">
  <div>
    <div class="kicker"><span class="it">Recipe No.{v['reel']}</span><span>릴스 #{v['reel']} · {v['part']}</span></div>
    <h1>{e(v['title'])}</h1>
    <p class="lede">{e(v['lede'])}</p>
    <ul class="facts"><li><b>{n}</b><span>분야</span></li><li><b>{n}</b><span>사이트</span></li><li><b>26.10</b><span>기준</span></li></ul>
    <div class="ctas"><a class="btn solid" href="#list">한눈에 보기</a><a class="btn" href="#t1">하나씩 보기</a></div>
  </div>
  <div class="hero-clip wide">{video(v['hero'], base, eager=True)}<span class="tag">{e(v['tools'][0][6])}</span></div>
</section>
<section class="sec" id="list">
  <div class="sec-h"><h2>한눈에 보기</h2><span class="it">index</span><p>누르면 설명으로 이동해요</p></div>
  <div class="ings">{idx}</div>
</section>
<section class="sec" id="steps">
  <div class="sec-h"><h2>분야별 고수 픽</h2><span class="it">picks</span><p>공식 영상과 함께 보기</p></div>
  {''.join(rows)}
</section>
<ul class="notes">
  <li>2026년 10월 기준이에요. 기능과 요금제는 자주 바뀌니 공식 사이트에서 확인하세요.</li>
  <li>"초보" 칸은 틀렸다는 뜻이 아니라, 대부분 처음 쓰는 기본 선택지라는 뜻이에요.</li>
  <li>영상은 각 회사 공식 계정과 크리에이터가 올린 영상이에요. 출처는 영상 위에 표시했어요.</li>
</ul>
{more}
''' + foot(base)


def index_page():
    base = ''
    total = sum(count(v) for v in VOLUMES)
    rows = ''.join(issue_row(v, base) for v in VOLUMES)
    soon = '<li class="issue soon"><div><div class="no" style="color:var(--dim)"><small>No.</small>?</div><div class="tt"><b>다음 레시피 준비 중</b><span>릴스로 먼저 공개돼요</span></div></div></li>'
    return head('미리봄 레시피', '따라 하면 나오는 AI 영상 레시피. 원작자가 공개한 프롬프트에서 핵심 문장만 뽑아 편마다 정리했어요.', base) + f'''<main class="wrap">
<section class="mast">
  <div class="over">miribom · AI video cookbook</div>
  <h1>Recipe<b>.</b></h1>
  <div class="sub">
    <h2>따라 하면 나오는 AI 영상 레시피</h2>
    <p>미리봄 릴스에서 소개한 프롬프트를 편마다 정리했어요. 원작 영상을 보면서 핵심 문장 {total}개를 그대로 복사해 쓰세요.</p>
  </div>
</section>
<ul class="index">{rows}{soon}</ul>
''' + foot(base)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root, 'index.html'), 'w') as f:
        f.write(index_page())
    for v in VOLUMES:
        d = os.path.join(root, v['slug']); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(tools_page(v) if v.get('type') == 'tools' else volume_page(v))
    open(os.path.join(root, '.nojekyll'), 'w').close()
    print('built', [v['slug'] for v in VOLUMES])
