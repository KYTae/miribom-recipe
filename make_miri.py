"""Generate pixel-art SVG poses of 미리 from the reel character module -> miri.py (inline SVG strings)."""
import sys, json
sys.argv = ["x"]; sys.path.insert(0, "/home/claude/reel"); sys.path.insert(0, "/home/claude/char")
import numpy as np
from scipy import ndimage
import reel40f as R
from PIL import Image, ImageDraw
import math

# ---------- custom transformation forms (48-grid coords, like reel40f.body_mask) ----------
_orig_mask = R.body_mask
def body_mask(spec, t):
    kind = spec[0]
    if kind not in CUSTOM: return _orig_mask(spec, t)
    im = Image.new("L", (R.HG, R.HG), 0); d = ImageDraw.Draw(im)
    S = lambda v: [(c + (R.OX if i % 2 == 0 else R.OY)) * R.R for i, c in enumerate(v)]
    E = lambda b, f=255: d.ellipse(S(b), fill=f)
    Rr = lambda b, r=0: d.rounded_rectangle(S(b), radius=r * R.R, fill=255)
    L = lambda pts, w: d.line(S(pts), fill=255, width=int(w * R.R), joint="curve")
    Pg = lambda pts: d.polygon([((x + R.OX) * R.R, (y + R.OY) * R.R) for x, y in pts], fill=255)
    if kind == "mega":      # megaphone: round back (face) + cone + rim + handle
        Rr([3, 22, 16, 33]); Pg([(15, 22), (34, 8), (34, 42), (15, 33)]); Rr([33, 7, 37, 43])
    if kind == "cam":       # camera box with viewfinder bump
        Rr([6, 20, 42, 42], 4); Rr([26, 15, 36, 21], 1)
    if kind == "bulb":      # light bulb
        E([12, 13, 36, 37]); Rr([18, 33, 30, 42], 2)
    if kind == "heart":
        E([9, 16, 26, 33]); E([22, 16, 39, 33]); Pg([(10, 27), (38, 27), (24, 42)])
    if kind == "phone":
        Rr([14, 6, 34, 40], 3); L([19, 39, 19, 42], 1.6); L([29, 39, 29, 42], 1.6)
    if kind == "qmark":     # question mark: thick hook (face on top) + stem + dot, no legs
        E([11, 6, 37, 30]); E([19, 14, 29, 22], 0)
        d.rectangle(S([10, 18, 24, 31]), fill=0)            # open the lower-left of the hook
        Rr([21, 26, 28, 34], 2); E([21, 36, 28, 43])
    if kind == "peek":      # hands resting on an edge (body hidden below)
        E([14, 16, 34, 38]); E([10.5, 24.5, 16.5, 30.5]); E([31.5, 24.5, 37.5, 30.5])
    if kind == "arrow":     # arrow pointing right: shaft (face) + head
        Rr([3, 21, 27, 33], 3); Pg([(25, 11), (45, 27), (25, 43)])
    def blob(y0=16, y1=38): E([14, y0, 34, y1])
    def legs(y0=36): L([19.5, y0, 19.5, 41.5], 1.6); L([28.5, y0, 28.5, 41.5], 1.6)
    def arm(sh, ang, Ln, w=2.4):
        tx, ty = R.arm_tip(ang, Ln, sh); L([sh[0], sh[1], tx, ty], w); E([tx - 2.1, ty - 2.1, tx + 2.1, ty + 2.1]); return tx, ty
    if kind == "arms":      # generic body with posed arms (props are drawn as FX)
        if spec[1].get("nolegs"): E([14, 19, 34, 41])
        else: blob(); legs()
        if "ra" in spec[1]: arm(R.SHOULDER_R, spec[1]["ra"], spec[1].get("rl", 12))
        if "la" in spec[1]: arm(R.SHOULDER_L, spec[1]["la"], spec[1].get("ll", 12))
    if kind == "sleepy":    # squashed, sitting, drowsy
        E([12, 21, 36, 42])
    if kind == "shy":       # hands up covering the eyes
        blob(); legs(); L([R.SHOULDER_L[0], R.SHOULDER_L[1], 19, 27], 2.2); L([R.SHOULDER_R[0], R.SHOULDER_R[1], 29, 27], 2.2)
    if kind == "copy":      # front card = body (back card is FX)
        Rr([7, 18, 31, 42], 3)
    if kind == "check":     # the body IS a thick check mark
        L([7, 26, 17, 37], 8.5); L([17, 37, 40, 12], 8.5); E([3, 22, 11, 30]); E([36, 8, 44, 16]); E([12, 32, 22, 42])
    if kind == "play":      # the body IS a play triangle
        Pg([(11, 6), (11, 44), (44, 25)])
    if kind == "star":
        cx, cy = 24, 27; pts = []
        for k in range(10):
            rr = 17 if k % 2 == 0 else 7.5; a = math.radians(-90 + k * 36)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        Pg(pts)
    if kind == "bubble":
        Rr([5, 11, 43, 34], 7); Pg([(13, 32), (22, 32), (11, 42)])
    if kind == "surfer":    # no arms, very short stubby legs standing on the board
        dy = spec[1].get("dy", 0)
        E([14, 17 + dy, 34, 38 + dy]); L([20, 37 + dy, 20, 40.5], 2.2); L([28, 37 + dy, 28, 40.5], 2.2)
    if kind == "magx":      # magnifying glass: lens = face, thick handle, no legs
        E([7, 7, 35, 35]); L([30, 30, 42, 42], 5.5)
    return np.array(im) > 127
CUSTOM = {"surfer", "magx", "mega", "cam", "bulb", "heart", "phone", "qmark", "arrow", "peek", "arms", "sleepy", "shy", "copy", "check", "play", "star", "bubble"}
R.body_mask = body_mask
R.FACE.update({"mega": ((10, 26, 5), (9, 19)), "cam": ((15, 28, 5), (31, 14)), "bulb": ((24, 24, 6), (24, 13)),
               "heart": ((24, 25, 6), (24, 19)), "phone": ((24, 14, 6), (24, 6)),
               "qmark": ((24, 9, 6), (24, 4)), "arrow": ((13, 25, 5), (12, 19)), "peek": ((24, 22, 6), (24, 15)),
               "arms": ((24, 24, 6), (24, 16)), "sleepy": ((24, 29, 6), (24, 21)), "shy": ((24, 24, 6), (24, 16)),
               "copy": ((19, 27, 6), (19, 18)), "check": ((29, 23, 5), (40, 6)), "play": ((21, 24, 6), (14, 8)),
               "star": ((24, 26, 5), (24, 9)), "bubble": ((24, 18, 6), (24, 11)),
               "magx": ((21, 20, 6), (21, 5)), "surfer": ((24, 25, 6), (24, 17))})

def g(x, y): return x + R.OX, y + R.OY   # 48-grid -> 64-grid
WHITE = (255, 255, 255); LIGHT = (255, 160, 210); GOLD = (255, 214, 90); GLASS = (34, 22, 44); DARK = (28, 8, 20); PD = (200, 30, 120)
def ring(cx, cy, r0, r1, a0=-180, a1=180):
    pts = set()
    for y in range(64):
        for x in range(64):
            dx, dy = x + .5 - cx, y + .5 - cy; rr = math.hypot(dx, dy); a = math.degrees(math.atan2(dy, dx))
            if r0 <= rr < r1 and a0 <= a <= a1: pts.add((x, y))
    return pts
def rect(x0, y0, x1, y1): return {(x, y) for x in range(x0, x1) for y in range(y0, y1)}
def FX(name):
    cx, cy = g(30.5, 31.5)
    if name in ("cam", "cam2"):
        out = [(DARK, ring(cx, cy, 6.6, 8.2)), (GLASS, ring(cx, cy, 0, 6.6)), (PD, ring(cx, cy, 2.2, 3.4)), (WHITE, {(int(cx) - 3, int(cy) - 3), (int(cx) - 2, int(cy) - 3), (int(cx) - 3, int(cy) - 2)})]
        fx0, fy0 = g(9, 22)
        out.append((DARK, rect(fx0, fy0, fx0 + 5, fy0 + 3)))
        if name == "cam2":
            out[-1] = (WHITE, rect(fx0, fy0, fx0 + 5, fy0 + 3))
            for (a, b) in [(-2, -2), (-3, -3), (6, -2), (7, -3), (2, -3), (2, -4), (-2, 4), (-3, 5)]: out.append((WHITE, {(fx0 + a, fy0 + b)}))
        return out
    if name in ("mega", "mega2"):
        rim = {(x, y) for x in range(g(34, 0)[0], g(37, 0)[0]) for y in range(g(0, 8)[1], g(0, 43)[1])}
        sh = 2 if name == "mega2" else 0; ln = 3 if name == "mega2" else 2
        dash = set()
        for (dx, dy) in ((40, 12), (41, 25), (40, 38)):
            x0, y0 = g(dx + sh, dy); dash |= {(x0 + i, y0) for i in range(ln)}
        return [(PD, rim), ((170, 170, 176), dash)]
    if name in ("bulb", "bulb2"):
        bx, by = g(18, 35); out = [(PD, rect(bx, by + 1, bx + 13, by + 2) | rect(bx, by + 4, bx + 13, by + 5))]
        if name == "bulb2":
            c0x, c0y = g(24, 25)
            for ang in range(-180, 1, 30):
                a = math.radians(ang)
                out.append((GOLD, {(int(round(c0x + math.cos(a) * r_)), int(round(c0y + math.sin(a) * r_))) for r_ in (14.5, 15.5, 16.5)}))
        return out
    if name in ("phone",):
        sx, sy = g(16, 9); return [(GLASS, rect(sx, sy + 13, sx + 17, sy + 27)), (LIGHT, rect(sx + 3, sy + 16, sx + 14, sy + 17) | rect(sx + 3, sy + 19, sx + 11, sy + 20)), (PINKC, rect(sx + 3, sy + 22, sx + 9, sy + 25))]
    if name == "heart2":
        return [(LIGHT, {g(9, 14), g(8, 13), g(10, 13), g(40, 14), g(39, 13), g(41, 13)})]
    return []
PINKC = R.P
METAL = (58, 58, 68); METAL2 = (120, 120, 132); PAPER = (240, 238, 232); SKY = (120, 184, 255)
def G(x, y): return (x + R.OX, y + R.OY)
def heart_px(x, y, col):
    pat = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
    return (col, {(x + i, y + j) for j, row in enumerate(pat) for i, ch in enumerate(row) if ch == "#"})
def z_px(x, y, n, col):
    pats = {3: ["###", "..#", ".#.", "#..", "###"], 4: ["####", "...#", "..#.", ".#..", "####"]}
    return (col, {(x + i, y + j) for j, row in enumerate(pats[n]) for i, ch in enumerate(row) if ch == "#"})
def PROP(name):
    """props drawn in front of the body: list of (color, draw-fn(ImageDraw)) — outlined automatically"""
    hand = lambda ang, Ln, sh=R.SHOULDER_R: G(*R.arm_tip(ang, Ln, sh))
    out = []
    if name in ("stir", "stir2"):
        hx, hy = hand(20 if name == "stir" else 40, 9)
        out.append((METAL2, lambda d, hx=hx, hy=hy: d.line([hx, hy - 4, G(40, 36)[0], G(40, 36)[1]], width=1)))
        out.append((METAL, lambda d: d.rectangle([G(31, 34)[0], G(31, 34)[1], G(47, 42)[0], G(47, 42)[1]])))
        out.append((METAL2, lambda d: d.rectangle([G(30, 33)[0], G(30, 33)[1], G(48, 34)[0], G(48, 34)[1]])))
    if name in ("flip", "flip2"):
        hx, hy = hand(-5, 12)
        out.append((METAL, lambda d, hx=hx, hy=hy: d.ellipse([hx + 1, hy - 1, hx + 13, hy + 2])))
        py = hy - (6 if name == "flip" else 13)
        out.append((PAPER, lambda d, hx=hx, py=py: d.rectangle([hx + 4, py, hx + 9, py + 3])))
        out.append((PD, lambda d, hx=hx, py=py: d.line([hx + 5, py + 1, hx + 8, py + 1], width=1)))
    if name == "taste":
        hx, hy = hand(-50, 10)
        out.append((METAL2, lambda d, hx=hx, hy=hy: d.line([hx, hy, hx + 4, hy + 7], width=1)))
        out.append((METAL, lambda d, hx=hx, hy=hy: d.ellipse([hx - 6, hy - 2, hx - 1, hy + 2])))
    if name in ("pour", "pour2"):
        hx, hy = hand(-40, 11)
        out.append((PAPER, lambda d, hx=hx, hy=hy: d.polygon([(hx - 1, hy - 4), (hx + 6, hy - 6), (hx + 8, hy + 1), (hx + 1, hy + 3)])))
        out.append((SKY, lambda d, hx=hx, hy=hy: d.line([hx + 1, hy - 3, hx + 6, hy - 5], width=1)))
        for k in range(2 if name == "pour" else 3):
            out.append((LIGHT, lambda d, hx=hx, hy=hy, k=k: d.point((hx + 9, hy + 4 + k * 3))))
    if name == "shy":
        for (x, y) in ((19.5, 26.5), (28.5, 26.5)):
            out.append((PINKC, lambda d, x=x, y=y: d.ellipse([G(x - 2.6, y - 2.6)[0], G(x - 2.6, y - 2.6)[1], G(x + 2.6, y + 2.6)[0], G(x + 2.6, y + 2.6)[1]])))
    if name == "reporter":
        lx, ly = hand(150, 9, R.SHOULDER_L)
        out.append((PAPER, lambda d, lx=lx, ly=ly: d.rectangle([lx - 7, ly - 8, lx + 1, ly + 3])))
        out.append((METAL2, lambda d, lx=lx, ly=ly: [d.line([lx - 5, ly - 5 + 3 * k, lx - 1, ly - 5 + 3 * k], width=1) for k in range(3)]))
        rx, ry = hand(-20, 9)
        out.append((METAL, lambda d, rx=rx, ry=ry: d.line([rx, ry + 1, rx + 3, ry - 6], width=1)))
    if name == "anchor":
        out.append((METAL, lambda d: d.rectangle([G(4, 32)[0], G(4, 32)[1], G(44, 42)[0], G(44, 42)[1]])))
        out.append((PD, lambda d: d.rectangle([G(4, 32)[0], G(4, 32)[1], G(44, 33)[0], G(44, 33)[1]])))
        out.append((METAL2, lambda d: d.line([G(39, 31)[0], G(39, 31)[1], G(37, 25)[0], G(37, 25)[1]], width=1)))
        out.append((METAL, lambda d: d.ellipse([G(35, 22)[0], G(35, 22)[1], G(38, 25)[0], G(38, 25)[1]])))
    if name in ("laptop", "laptop2"):
        out.append((METAL, lambda d: d.rectangle([G(14, 29)[0], G(14, 29)[1], G(34, 38)[0], G(34, 38)[1]])))
        out.append((METAL2, lambda d: d.rectangle([G(11, 38)[0], G(11, 38)[1], G(37, 40)[0], G(37, 40)[1]])))
        out.append((PD, lambda d: d.point(G(24, 33))))
    if name in ("surf", "surf2"):
        dy = 0 if name == "surf" else 1
        out.append((PAPER, lambda d, dy=dy: d.ellipse([G(5, 41 + dy)[0], G(5, 41 + dy)[1], G(43, 44 + dy)[0], G(43, 44 + dy)[1]])))
        out.append((SKY, lambda d, dy=dy: [d.arc([G(-2 + 12 * k, 43 - dy)[0], G(-2 + 12 * k, 43 - dy)[1], G(10 + 12 * k, 50 - dy)[0], G(10 + 12 * k, 50 - dy)[1]], 180, 360, width=2) for k in range(5)]))
    return out
def PIX(name):
    """extra free pixels (no outline): hearts, zzz, check mark, play triangle, dots, back card"""
    if name in ("sleepy", "sleepy2"):
        return [z_px(*G(35, 12), 3, PAPER)] + ([z_px(*G(39, 5), 4, PAPER)] if name == "sleepy2" else [])
    if name in ("hearts", "hearts2"):
        return [heart_px(*G(37, 10 if name == "hearts" else 7), LIGHT), heart_px(*G(42, 18 if name == "hearts" else 14), PINKC)]
    if name == "check":
        pts = set()
        for (x0, y0, x1, y1) in ((15, 30, 21, 36), (21, 36, 33, 23)):
            n = 24
            for k in range(n + 1):
                x = x0 + (x1 - x0) * k / n; y = y0 + (y1 - y0) * k / n
                for ox in (0, 1):
                    for oy in (0, 1): pts.add(G(int(round(x)) + ox, int(round(y)) + oy))
        return [(WHITE, pts)]
    if name == "play":
        pts = set()
        for y in range(21, 37):
            half = (36 - y) if y > 28.5 else (y - 21)
            for x in range(19, 19 + int(half * 1.5) + 1): pts.add(G(x, y))
        return [(WHITE, pts)]
    if name == "bubble":
        return [(WHITE, {G(x + dx, 26 + dy) for x in (16, 23, 30) for dx in (0, 1) for dy in (0, 1)})]
    if name == "copy":
        return [(PD, {G(x, y) for x in range(15, 41) for y in range(10, 34) if (x in (15, 16, 39, 40) or y in (10, 11)) and not (x < 31 and y >= 18)})]
    if name == "magx":
        rim = ring(*G(21, 21), 11.2, 14.2)
        return [(PD, rim), (WHITE, {G(13, 14), G(14, 13), G(13, 15), G(15, 12)})]
    if name == "surprise":
        return [(WHITE, {G(37 + dx, y) for y in range(2, 8) for dx in (0, 1)} | {G(37 + dx, 9 + dy) for dx in (0, 1) for dy in (0, 1)})]
    return []

OUTL = (28, 8, 20)

def grid(spec, t=0.0, eyes=None):
    mask = R.body_mask(spec, t)
    m = R.sdf_of(mask)[R.R // 2::R.R, R.R // 2::R.R] < 0
    G = R.G; px = np.zeros((G, G, 3), np.uint8); al = np.zeros((G, G), np.uint8)
    px[m] = R.P; al[m] = 1
    (ex, ey, gap), (sx, sy) = R.FACE[spec[0]]
    if eyes: R.draw_face(px, al, ex, ey, gap, eyes)
    R.draw_sprout(px, al, sx, sy)
    ol = ndimage.binary_dilation(al > 0, iterations=1) & (al == 0)
    px[ol] = OUTL; al[ol] = 1
    return px, al

def path_of(sel):
    """sel: bool GxG -> svg path of horizontal runs"""
    d = []
    for y in range(sel.shape[0]):
        x = 0; row = sel[y]
        while x < len(row):
            if row[x]:
                s = x
                while x < len(row) and row[x]: x += 1
                d.append(f"M{s} {y}h{x - s}v1h{s - x}z")
            else: x += 1
    return "".join(d)

def hexc(c): return "#%02x%02x%02x" % tuple(int(v) for v in c)

class _Fill:
    """ImageDraw proxy that always paints with value 255"""
    def __init__(self, d): self.d = d
    def rectangle(self, xy, **k): self.d.rectangle(xy, fill=255)
    def ellipse(self, xy, **k): self.d.ellipse(xy, fill=255)
    def polygon(self, xy, **k): self.d.polygon(xy, fill=255)
    def line(self, xy, width=1, **k): self.d.line(xy, fill=255, width=width)
    def point(self, xy, **k): self.d.point(xy, fill=255)
    def arc(self, xy, a0, a1, width=1, **k): self.d.arc(xy, a0, a1, fill=255, width=width)

def decorate(px, al, fx):
    if not fx: return
    for col, pts in FX(fx):
        for x, y in pts:
            if 0 <= x < 64 and 0 <= y < 64: px[y, x] = col; al[y, x] = 1
    for col, fn in PROP(fx):
        im = Image.new("L", (64, 64), 0); fn(_Fill(ImageDraw.Draw(im))); m = np.array(im) > 0
        ol = ndimage.binary_dilation(m, iterations=1) & ~m
        if col != PINKC: ol &= (al == 0)      # pink props (hands) keep a full outline so they read on the body
        px[ol] = OUTL; al[ol] = 1; px[m] = col; al[m] = 1
    for col, pts in PIX(fx):
        for x, y in pts:
            if 0 <= x < 64 and 0 <= y < 64: px[y, x] = col; al[y, x] = 1

def pose(spec, t=0.0, eyesets=("idle", "blink", "happy", "look"), fx=None):
    base, al = grid(spec, t, None)
    decorate(base, al, fx)
    layers = []
    colors = {}
    for y in range(64):
        for x in range(64):
            if al[y, x]: colors.setdefault(tuple(base[y, x]), []).append((y, x))
    for c, pts in colors.items():
        sel = np.zeros((64, 64), bool)
        for y, x in pts: sel[y, x] = True
        layers.append(f'<path fill="{hexc(c)}" d="{path_of(sel)}"/>')
    faces = []
    for e in eyesets:
        p2, a2 = grid(spec, t, e)
        decorate(p2, a2, fx)
        diff = np.any(p2 != base, axis=2) & (a2 > 0)
        faces.append(f'<path class="e e-{e}" fill="#140c12" d="{path_of(diff)}"/>')
    ys, xs = np.nonzero(al)
    return {"body": "".join(layers), "face": "".join(faces), "bbox": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]}

POSES = {
    "idle": (("idle", {}), 0.0),
    "wave": (("wave", {}), 0.12),
    "wave2": (("wave", {}), 0.42),
    "cheer": (("cheer", {}), 0.0),
    "cheer2": (("cheer", {}), 0.11),
    "sit": (("sit", {}), 0.2618), "sit2": (("sit", {}), 0.0), "sit3": (("sit", {}), -0.2618),
    "melt": (("melt", {}), 0.0),
    "hop": (("hop", {}), 0.0),
    "point": (("point", {"ang": -35}), 0.0),
    "think": (("think", {}), 0.0),
    "mag": (("mag", {"ang": -40}), 0.0),
    "ball": (("ball", {}), 0.0),
}
POSES.update({
    "mega": (("mega", {}), 0.0, "mega"), "mega2": (("mega", {}), 0.0, "mega2"),
    "cam": (("cam", {}), 0.0, "cam"), "cam2": (("cam", {}), 0.0, "cam2"),
    "bulb": (("bulb", {}), 0.0, "bulb"), "bulb2": (("bulb", {}), 0.0, "bulb2"),
    "heart": (("heart", {}), 0.0, None), "heart2": (("heart", {}), 0.0, "heart2"),
    "phone": (("phone", {}), 0.0, "phone"),
    "clap": (("clap", {}), 0.0, None), "clap2": (("clap", {}), 0.17, None),
    "tall": (("tall", {}), 0.0, None),
    "qmark": (("qmark", {}), 0.0, None), "bang": (("bang", {}), 0.0, None), "arrow": (("arrow", {}), 0.0, None),
    "edge": (("peek", {}), 0.0, None),
    # chef
    "stir": (("arms", {"ra": 20, "rl": 9, "la": 110, "ll": 9}), 0.0, "stir"), "stir2": (("arms", {"ra": 40, "rl": 9, "la": 110, "ll": 9}), 0.0, "stir2"),
    "flip": (("arms", {"ra": -5, "rl": 12, "la": 110, "ll": 9}), 0.0, "flip"), "flip2": (("arms", {"ra": -5, "rl": 12, "la": 110, "ll": 9}), 0.0, "flip2"),
    "taste": (("arms", {"ra": -50, "rl": 10, "la": 110, "ll": 9}), 0.0, "taste"),
    "pour": (("arms", {"ra": -40, "rl": 11, "la": 110, "ll": 9}), 0.0, "pour"), "pour2": (("arms", {"ra": -40, "rl": 11, "la": 110, "ll": 9}), 0.0, "pour2"),
    # icon transforms (legless)
    "copy": (("copy", {}), 0.0, "copy"), "check": (("check", {}), 0.0, None), "play": (("play", {}), 0.0, None),
    "star": (("star", {}), 0.0, None), "bubble": (("bubble", {}), 0.0, "bubble"),
    # magazine jobs
    "reporter": (("arms", {"la": 150, "ll": 9, "ra": -20, "rl": 9}), 0.0, "reporter"),
    "anchor": (("arms", {"ra": 125, "rl": 7, "la": 55, "ll": 7}), 0.0, "anchor"),
    "laptop": (("type", {}), 0.0, "laptop"), "laptop2": (("type", {}), 0.07, "laptop2"),
    "surf": (("surfer", {}), 0.0, "surf"), "surf2": (("surfer", {"dy": 1}), 0.0, "surf2"),
    "magx": (("magx", {}), 0.0, "magx"),
    # emotions
    "sleepy": (("sleepy", {}), 0.0, "sleepy"), "sleepy2": (("sleepy", {}), 0.0, "sleepy2"),
    "hearts": (("wave", {}), 0.12, "hearts"), "hearts2": (("wave", {}), 0.42, "hearts2"),
    "surprise": (("tall", {}), 0.0, "surprise"),
})
out = {k: pose(v[0], v[1], fx=(v[2] if len(v) > 2 else None)) for k, v in POSES.items()}
with open("/home/claude/site/miri.py", "w") as f:
    f.write("# generated by make_miri.py\nMIRI = " + json.dumps(out, ensure_ascii=False) + "\n")
print({k: v["bbox"] for k, v in out.items()}, sum(len(v["body"]) + len(v["face"]) for v in out.values()))
