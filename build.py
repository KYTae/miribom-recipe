"""미리봄 레시피 사이트 빌더: python3 build.py → index.html, <slug>/index.html 생성."""
import html, os
from data import VOLUMES, TEMPLATE

IG = 'https://www.instagram.com/ai.miribom/'
YT = 'https://www.youtube.com/@ai.miribom'
e = html.escape


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
<meta name="theme-color" content="#050507">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@500;600;700&family=Noto+Sans+KR:wght@400;500;700;900&display=swap">
<link rel="stylesheet" href="{base}assets/style.css">
</head>
<body>
<header class="bar"><div class="wrap">
  <a class="logo" href="{base}"><i></i>miribom<span style="color:var(--muted);font-weight:500">&nbsp;/ recipe</span></a>
  <a class="ig" href="{IG}" target="_blank" rel="noopener">@ai.miribom</a>
</div></header>
'''


def foot(base):
    return f'''<footer>
  <div class="big">남들보다 먼저 보는 AI 소식, <em>@ai.miribom</em></div>
  <p>새 레시피는 인스타그램 릴스와 유튜브 쇼츠에 먼저 올라와요.</p>
  <div class="ctas"><a class="btn primary" href="{IG}" target="_blank" rel="noopener">인스타그램 팔로우</a><a class="btn" href="{YT}" target="_blank" rel="noopener">유튜브 쇼츠</a></div>
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


def vol_card(v, base):
    n = sum(len(g['items']) for g in v['groups'])
    return f'''<a class="vol" href="{base}{v['slug']}/">
  {video(v['hero'], base)}
  <div class="shade"></div>
  <span class="chip"><b>No.{v['reel']}</b> · {v['part']}</span>
  <div class="meta"><b>{e(v['title'])}</b><span>{e(v['short'])} · 핵심 문장 {n}개</span><span class="go">레시피 열기 →</span></div>
</a>'''


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
    n = sum(len(g['items']) for g in v['groups'])
    phrases = [it[3].split('\n')[0] for g in v['groups'] for it in g['items']]
    tick = ''.join(f'<span>{e(p)}</span>' for p in phrases * 2)
    title_html = e(v['title']).replace('치트키', '<em>치트키</em>', 1)
    groups_html = []
    for gi, g in enumerate(v['groups']):
        cards = []
        for num, clip, ttl, phrase, desc in g['items']:
            cards.append(f'''<article class="card">
  <div class="clip {g['shape']}">{video(clip, base)}<span class="num">{num}</span><span class="credit">Video · X {e(g['who'])}</span></div>
  <div class="card-body">
    <h3>{e(ttl)}</h3>
    <div class="phrase"><code>{e(phrase)}</code><button class="copy" type="button">복사</button></div>
    <p class="desc">{desc}</p>
  </div>
</article>''')
        one = ' one' if len(cards) == 1 else ''
        groups_html.append(f'''<section class="group" id="g{gi+1}">
  <div class="group-head"><div><h2>{e(g['who'])}</h2><p>{e(g['what'])} · {e(g['tool'])}</p></div><a href="{g['url']}" target="_blank" rel="noopener">원작 보기 ↗</a></div>
  <div class="cards{one}">{''.join(cards)}</div>
</section>''')
    tpl = ''
    tpl_btn = ''
    if v['template']:
        tpl = f'''<section class="tpl" id="template">
  <span class="kicker">full recipe</span>
  <h2>한 번에 쓰는 완성 레시피</h2>
  <p>위 문장들을 미리봄이 하나로 묶은 뼈대예요. 회색 괄호 안만 내 장면으로 바꾸세요. 첫 장면 이미지를 먼저 만들어 참조로 넣으면 더 좋아요.</p>
  <pre id="tpl">{tpl_html()}</pre>
  <div><button class="btn primary" type="button" data-copy="tpl">레시피 전체 복사</button></div>
</section>'''
        tpl_btn = '<a class="btn primary" href="#template">완성 레시피 바로가기</a>'
    others = [o for o in VOLUMES if o['slug'] != v['slug']]
    more = ''
    if others:
        more = f'''<section class="more"><h2>다른 레시피도 저장해두세요</h2><div class="vols">{''.join(vol_card(o, base) for o in others)}</div></section>'''
    authors = len(v['groups'])
    stat_k, stat_v = v['stat']
    return head(f"{v['title']} | 미리봄 레시피", v['lede'], base) + f'''<main class="wrap">
<section class="hero"><div class="hero-grid">
  <div class="frame {v['hero_shape']}">{video(v['hero'], base, eager=True)}<span class="chip"><b>RECIPE No.{v['reel']}</b> · 릴스 #{v['reel']}</span></div>
  <div>
    <span class="kicker">miribom recipe · No.{v['reel']}</span>
    <h1>{title_html}</h1>
    <p class="lede">{e(v['lede'])} 영어 문장은 그대로 복사해서 쓰세요.</p>
    <ul class="stats"><li><b>{n}</b><span>핵심 문장</span></li><li><b>{authors}</b><span>원작자</span></li><li><b>{e(stat_v)}</b><span>{e(stat_k)}</span></li></ul>
    <div class="ctas">{tpl_btn}<a class="btn" href="#g1">문장 보기</a></div>
  </div>
</div></section>
<div class="ticker" aria-hidden="true"><div class="ticker-track">{tick}</div></div>
{''.join(groups_html)}
{tpl}
<ul class="notes">
  <li>같은 문장을 넣어도 결과는 매번 달라요. 여러 번 돌려보고 고르세요.</li>
  <li>영상 AI는 서비스마다 유료 크레딧이 필요할 수 있어요.</li>
  <li>영상과 문장의 출처는 모두 원작자에게 있어요. 프롬프트 전문은 원작자 게시물에서 볼 수 있어요.</li>
</ul>
{more}
''' + foot(base)


def index_page():
    base = ''
    total = sum(len(g['items']) for v in VOLUMES for g in v['groups'])
    vols = ''.join(vol_card(v, base) for v in VOLUMES)
    soon = '<div class="vol soon"><div><b>다음 레시피 준비 중</b>릴스로 먼저 공개돼요</div></div>' if len(VOLUMES) % 2 else ''
    return head('미리봄 레시피', '따라 하면 나오는 AI 영상 레시피. 원작자가 공개한 프롬프트에서 핵심 문장만 뽑아 편마다 정리했어요.', base) + f'''<main class="wrap">
<section class="hero">
  <span class="kicker">miribom recipe</span>
  <h1>따라 하면 나오는<br><em>AI 영상 레시피</em></h1>
  <p class="lede">미리봄 릴스에서 소개한 프롬프트를 편마다 레시피로 모아뒀어요. 원작 영상을 보면서, 핵심 문장 {total}개를 그대로 복사해서 쓰세요.</p>
</section>
<section class="more" style="margin-top:24px"><div class="vols">{vols}{soon}</div></section>
''' + foot(base)


if __name__ == '__main__':
    root = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(root, 'index.html'), 'w') as f:
        f.write(index_page())
    for v in VOLUMES:
        d = os.path.join(root, v['slug']); os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(volume_page(v))
    open(os.path.join(root, '.nojekyll'), 'w').close()
    print('built', [v['slug'] for v in VOLUMES])
