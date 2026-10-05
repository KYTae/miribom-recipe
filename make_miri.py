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
    return np.array(im) > 127
CUSTOM = {"mega", "cam", "bulb", "heart", "phone", "qmark", "arrow", "peek"}
R.body_mask = body_mask
R.FACE.update({"mega": ((10, 26, 5), (9, 19)), "cam": ((15, 28, 5), (31, 14)), "bulb": ((24, 24, 6), (24, 13)),
               "heart": ((24, 25, 6), (24, 19)), "phone": ((24, 14, 6), (24, 6)),
               "qmark": ((24, 9, 6), (24, 4)), "arrow": ((13, 25, 5), (12, 19)), "peek": ((24, 22, 6), (24, 15))})

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

def pose(spec, t=0.0, eyesets=("idle", "blink", "happy", "look"), fx=None):
    base, al = grid(spec, t, None)
    for col, pts in (FX(fx) if fx else []):
        for x, y in pts:
            if 0 <= x < 64 and 0 <= y < 64: base[y, x] = col; al[y, x] = 1
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
        for col, pts in (FX(fx) if fx else []):
            for x, y in pts:
                if 0 <= x < 64 and 0 <= y < 64: p2[y, x] = col; a2[y, x] = 1
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
})
out = {k: pose(v[0], v[1], fx=(v[2] if len(v) > 2 else None)) for k, v in POSES.items()}
with open("/home/claude/site/miri.py", "w") as f:
    f.write("# generated by make_miri.py\nMIRI = " + json.dumps(out, ensure_ascii=False) + "\n")
print({k: v["bbox"] for k, v in out.items()}, sum(len(v["body"]) + len(v["face"]) for v in out.values()))
