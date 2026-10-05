"""favicon set + OG images. python3 make_icons.py (needs /home/claude/ogf fonts, cairosvg)"""
import io, os, json, sys
import numpy as np, cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.abspath(__file__))
F = '/home/claude/ogf/'
BG = (11, 11, 12); PINK = (255, 59, 160); INK = (245, 243, 240); DIM = (160, 156, 160)

def logo(h):
    png = cairosvg.svg2png(url=os.path.join(ROOT, 'assets/logo.svg'), output_height=h)
    return Image.open(io.BytesIO(png)).convert('RGBA')

def icon(size, pad=0.1, radius=0.22):
    S = size * 4
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * radius), fill=BG + (255,))
    lg = logo(int(S * (1 - 2 * pad)))
    im.alpha_composite(lg, ((S - lg.width) // 2, (S - lg.height) // 2))
    return im.resize((size, size), Image.LANCZOS)


from miri import MIRI
from data import VOLUMES
TYPE = {'guide': '따라하기', 'tools': '툴 추천', 'volume': '프롬프트'}
TCOL = {'guide': (79, 227, 180), 'tools': (120, 184, 255), 'volume': (255, 108, 185)}
def pf(w, s): return ImageFont.truetype(F + f'Pretendard-{w}.otf', s)
def serif(s): return ImageFont.truetype(F + 'InstrumentSerif-Italic.ttf', s)

def miri_img(pose, h, eyes='idle', crop=None):
    m = MIRI[pose]; x0, y0, x1, y1 = crop or m['bbox']
    face = m['face'].replace('class="e e-' + eyes + '"', 'class="SHOW"')
    import re
    face = re.sub(r'<path class="e [^"]*"[^>]*/>', '', face)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}" shape-rendering="crispEdges">{m["body"]}{face}</svg>'
    png = cairosvg.svg2png(bytestring=svg.encode(), output_height=h)
    return Image.open(io.BytesIO(png)).convert('RGBA')

def glow(im, cx, cy, r, col, a):
    g = Image.new('L', im.size, 0); ImageDraw.Draw(g).ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
    g = g.filter(ImageFilter.GaussianBlur(r * .45))
    im.paste(Image.new('RGBA', im.size, col + (255,)), (0, 0), g)

def rounded(img, r):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radius=r, fill=255)
    out = img.convert('RGBA'); out.putalpha(m); return out

def cover_fit(img, w, h):
    s = max(w / img.width, h / img.height); img = img.resize((int(img.width * s + .5), int(img.height * s + .5)), Image.LANCZOS)
    return img.crop(((img.width - w) // 2, (img.height - h) // 2, (img.width - w) // 2 + w, (img.height - h) // 2 + h))

def wrap(d, text, font, maxw):
    lines, cur = [], ''
    for word in text.split(' '):
        t = (cur + ' ' + word).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = word
    lines.append(cur); return lines

def brand(im, x, y):
    lg = logo(46); im.alpha_composite(lg, (x, y))
    d = ImageDraw.Draw(im); d.text((x + lg.width + 12, y + 23), '미리봄 레시피', font=pf('Bold', 26), fill=INK, anchor='lm')

def og_home():
    W, H = 1200, 630
    im = Image.new('RGBA', (W, H), BG + (255,)); glow(im, 1020, 60, 420, PINK, 70)
    d = ImageDraw.Draw(im)
    # right: 3 latest heroes fanned + 미리
    for k, v in reversed(list(enumerate(VOLUMES[:3]))):
        src = Image.open(os.path.join(ROOT, 'assets/clips', v['hero'] + '.jpg')).convert('RGB')
        c = rounded(cover_fit(src, 230, 300), 22)
        c = c.rotate([-8, 4, 14][k], resample=Image.BICUBIC, expand=True)
        im.alpha_composite(c, ([840, 700, 930][k], [110, 150, 210][k]))
    mi = miri_img('wave', 250, 'happy'); im.alpha_composite(mi, (690, H - 40 - mi.height))
    d = ImageDraw.Draw(im)
    brand(im, 72, 64)
    f = pf('ExtraBold', 70); y = 196
    d.text((72, y), '릴스에서 본 그 AI,', font=f, fill=INK)
    d.text((72, y + 88), '그대로 따라', font=f, fill=PINK); w = d.textlength('그대로 따라 ', font=f)
    d.text((72 + w, y + 88), '만들어요', font=f, fill=INK)
    d.text((72, y + 210), '프롬프트 복사 · 단계별 따라하기 · 매주 업데이트', font=pf('Medium', 27), fill=DIM)
    d.text((72, H - 64), 'recipe.mirispring.com', font=pf('Medium', 22), fill=(117, 114, 122))
    im.convert('RGB').save(os.path.join(ROOT, 'og/home.jpg'), quality=88)

def og_recipe(v):
    W, H = 1200, 630; t = {'pack': 'volume', 'how': 'guide', 'kit': 'tools'}.get(v.get('type', 'volume'), v.get('type', 'volume'))
    im = Image.new('RGBA', (W, H), BG + (255,)); glow(im, 1100, 80, 380, PINK, 55)
    src = Image.open(os.path.join(ROOT, 'assets/clips', v['hero'] + '.jpg')).convert('RGB')
    mw, mh = 430, 496; mx, my = W - 48 - mw, 86
    # peeking 미리 behind the media
    pk = miri_img('idle', 150, 'idle'); im.alpha_composite(pk, (mx + mw - 200, my - 80))
    im.alpha_composite(rounded(cover_fit(src, mw, mh), 28), (mx, my))
    d = ImageDraw.Draw(im)
    brand(im, 64, 56)
    y = 168
    d.text((64, y), f"No.{v['reel']}", font=serif(64), fill=PINK, anchor='ls')
    nx = 64 + d.textlength(f"No.{v['reel']}", font=serif(64)) + 18
    lab = TYPE[t]; fp = pf('Bold', 22); pw = d.textlength(lab, font=fp) + 32
    col = TCOL[t]
    d.rounded_rectangle([nx, y - 38, nx + pw, y - 2], radius=18, fill=tuple(int(c * .18 + 11 * .82) for c in col))
    d.text((nx + pw / 2, y - 20), lab, font=fp, fill=col, anchor='mm')
    maxw = mx - 64 - 48
    for size in (60, 54, 48, 42):
        ft = pf('ExtraBold', size); lines = wrap(d, v['title'], ft, maxw)
        if len(lines) <= 3: break
    ty = y + 40
    for ln in lines:
        d.text((64, ty), ln, font=ft, fill=INK); ty += int(size * 1.24)
    for ln in wrap(d, v['short'], pf('Medium', 27), maxw)[:2]:
        d.text((64, ty + 18), ln, font=pf('Medium', 27), fill=DIM); ty += 40
    unit = {'tools': '사이트', 'guide': '단계', 'volume': '프롬프트'}[t]
    from build import count as _count
    n = _count(v)
    cta = {'guide': f'{n}단계 바로 따라 하기 →', 'tools': (f'툴 {n}개 가격 한눈에 →' if v.get('type') == 'kit' else f'사이트 {n}개 바로 보기 →'), 'volume': f'프롬프트 {n}개 바로 복사 →'}[t]
    cw = d.textlength(cta, font=pf('Bold', 24)) + 56
    d.rounded_rectangle([64, H - 112, 64 + cw, H - 56], radius=28, fill=PINK)
    d.text((64 + cw / 2, H - 84), cta, font=pf('Bold', 24), fill=(255, 255, 255), anchor='mm')
    im.convert('RGB').save(os.path.join(ROOT, f"og/{v['slug']}.jpg"), quality=88)

if __name__ == '__main__':
    os.makedirs(os.path.join(ROOT, 'og'), exist_ok=True)
    og_home()
    for v in VOLUMES: og_recipe(v)
    print('og ok')
    for s, name in [(48, 'favicon-48.png'), (96, 'favicon-96.png'), (180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
        im = icon(s, radius=0 if name == 'apple-touch-icon.png' else 0.22)
        if name == 'apple-touch-icon.png': im = im.convert('RGB')
        im.save(os.path.join(ROOT, name))
    icon(256).save(os.path.join(ROOT, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
    print('icons ok')
