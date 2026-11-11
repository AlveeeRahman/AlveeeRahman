"""DS-style animated pixel icons: 64 x 64 sprites with cel shading, coloured outlines, glints and eased motion.

Run with numpy, scipy and Pillow installed: python3 assets/pixel/make_pixels.py. The car is traced from logo_car.png (the OpenCarMind logo cut-out).
"""
import math
import os

import numpy as np
from PIL import Image

N = 64
SCALE = 2
FRAMES = 24
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out_hd")
LIGHT = np.array([-0.55, -0.65, 0.52])
LIGHT = LIGHT / np.linalg.norm(LIGHT)
YY, XX = np.mgrid[0:N, 0:N].astype(float) + 0.5


def rgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)


def mix(a, b, t):
    return a + (b - a) * t


def ease(t):
    """Smooth in and out, so motion slows at its ends like hand-animated sprites."""
    return 0.5 - 0.5 * math.cos(math.pi * t)


def wave(f, period=FRAMES, phase=0.0):
    return math.sin(2 * math.pi * (f / period + phase))


class Canvas:
    def __init__(self):
        self.c = np.zeros((N, N, 3))
        self.a = np.zeros((N, N))

    def put(self, mask, color, alpha=1.0):
        col = color if isinstance(color, np.ndarray) and color.ndim == 3 else np.broadcast_to(np.asarray(color, float), (N, N, 3))
        al = np.where(mask, alpha, 0.0) if np.isscalar(alpha) else np.where(mask, alpha, 0.0)
        self.c = self.c * (1 - al[..., None]) + col * al[..., None]
        self.a = np.maximum(self.a, np.where(mask, 1.0, self.a) if np.isscalar(alpha) and alpha >= 1 else self.a + (1 - self.a) * al)

    # ---------------------------------------------------------------- shapes with normals
    @staticmethod
    def ellipsoid(cx, cy, rx, ry):
        u, v = (XX - cx) / rx, (YY - cy) / ry
        d = u * u + v * v
        mask = d <= 1.0
        z = np.sqrt(np.clip(1 - d, 0, 1))
        n = np.stack([u, v, z], -1)
        n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-9
        return mask, n

    @staticmethod
    def rbox(x, y, w, h, r, bevel=2.5):
        # distance to a rounded rectangle, then a normal that tilts only near the edge (a bevel)
        qx = np.abs(XX - (x + w / 2)) - (w / 2 - r)
        qy = np.abs(YY - (y + h / 2)) - (h / 2 - r)
        outside = np.hypot(np.maximum(qx, 0), np.maximum(qy, 0)) + np.minimum(np.maximum(qx, qy), 0) - r
        mask = outside <= 0
        inner = -outside
        t = np.clip(1 - inner / bevel, 0, 1)
        gx = np.sign(XX - (x + w / 2)) * (qx > qy) * 1.0
        gy = np.sign(YY - (y + h / 2)) * (qy >= qx) * 1.0
        n = np.stack([gx * t, gy * t, np.ones_like(t)], -1)
        n /= np.linalg.norm(n, axis=-1, keepdims=True)
        return mask, n

    def shade(self, mask, n, base, outline=True, spec=True, tones=(0.18, 0.5, 0.82), out_k=0.42, alpha=1.0):
        """Cel shading: four flat tones from the light direction, a specular glint, a darker outline of the same hue."""
        base = rgb(base) if isinstance(base, str) else base
        lam = np.clip(n @ LIGHT, 0, 1)
        dark, mid, light, hi = mix(base, base * 0.55, 0.85), base, mix(base, np.array([255, 255, 255.0]), 0.28), mix(base, np.array([255, 255, 255.0]), 0.62)
        col = np.where((lam < tones[0])[..., None], dark, mid)
        col = np.where((lam >= tones[1])[..., None], light, col)
        if spec:
            r = 2 * lam[..., None] * n - LIGHT
            s = np.clip(r[..., 2], 0, 1)
            col = np.where(((s > 0.93) & (lam > tones[2]))[..., None], hi, col)
        self.put(mask, col, alpha)
        if outline:
            edge = mask & ~erode(mask)
            self.put(edge, base * out_k, alpha)

    def flat(self, mask, color, alpha=1.0):
        self.put(mask, rgb(color) if isinstance(color, str) else color, alpha)

    def glow(self, cx, cy, r, color, strength=0.8):
        d = np.hypot(XX - cx, YY - cy)
        al = np.clip(1 - d / r, 0, 1) ** 2 * strength
        # posterise the glow into three steps: soft light still reads as pixel art
        al = np.round(al * 3) / 3
        self.put(al > 0, rgb(color), al)

    def line(self, x0, y0, x1, y1, color, width=1.0, alpha=1.0):
        px, py = XX - x0, YY - y0
        dx, dy = x1 - x0, y1 - y0
        L2 = dx * dx + dy * dy or 1
        t = np.clip((px * dx + py * dy) / L2, 0, 1)
        d = np.hypot(px - t * dx, py - t * dy)
        self.put(d <= width / 2 + 0.25, rgb(color) if isinstance(color, str) else color, alpha)

    def shadow(self, cx, cy, rx, ry, k=0.35):
        u, v = (XX - cx) / rx, (YY - cy) / ry
        self.put(u * u + v * v <= 1, np.zeros(3), k)


def erode(m):
    e = m.copy()
    e[1:, :] &= m[:-1, :]; e[:-1, :] &= m[1:, :]; e[:, 1:] &= m[:, :-1]; e[:, :-1] &= m[:, 1:]
    return e


def tile(cv, top, bottom=None, edge="#4b5260", radius=12):
    """Rounded tile with a bevel: lighter top rim, darker bottom rim, banded gradient."""
    t, b = rgb(top), rgb(bottom or top)
    mask, _ = Canvas.rbox(0, 0, N, N, radius, bevel=1)
    band = np.minimum(3, (YY * 4 // N)) / 3
    col = t + (b - t) * band[..., None]
    cv.put(mask, col)
    inner = erode(mask)
    rim = inner & ~erode(inner)
    cv.put(rim & (YY < N / 2), np.minimum(t * 1.25 + 18, 255))
    cv.put(rim & (YY >= N / 2), b * 0.7)
    if edge:
        cv.put(mask & ~inner, rgb(edge))
    cv.tile_mask = mask
    return mask


# ===================================================================== the eight projects
# The car is traced from the OpenCarMind logo cut-out at pixel size, so the sprite keeps the logo's shape.
LOGO_CAR = os.environ.get("OCM_LOGO_CAR", os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_car.png"))


def _car_parts(width=46):
    from scipy import ndimage
    src = np.array(Image.open(LOGO_CAR).convert("RGBA")).astype(float)
    amber = (src[..., 0] > 150) & (src[..., 2] < 140) & (src[..., 3] > 40)
    alpha = src[..., 3] / 255
    ys, xs = np.where(alpha > 0.05)
    box = (slice(ys.min(), ys.max() + 1), slice(xs.min(), xs.max() + 1))
    h = round(width * (ys.max() - ys.min()) / (xs.max() - xs.min()))

    def small(a):
        im = Image.fromarray((np.clip(a[box], 0, 1) * 255).astype(np.uint8)).resize((width, h), Image.LANCZOS)
        return np.array(im) > 127
    body, chip = small(np.where(amber, 0, alpha)), small(amber.astype(float))
    filled = ndimage.binary_fill_holes(body | chip)
    holes = filled & ~body & ~chip
    lab, k = ndimage.label(holes)
    parts = {"windshield": np.zeros_like(holes), "lights": np.zeros_like(holes), "grille": np.zeros_like(holes)}
    for i in range(1, k + 1):
        m = lab == i
        cy, cx = np.argwhere(m).mean(0)
        if cy < h * 0.42:
            parts["windshield"] |= m
        elif abs(cx - width / 2) > width * 0.2:
            parts["lights"] |= m
        else:
            parts["grille"] |= m
    d = ndimage.distance_transform_edt(body)
    gy, gx = np.gradient(np.minimum(d, 2.5))
    return body, chip, parts, gx, gy


_CAR = None


def opencarmind(f):
    global _CAR
    if _CAR is None:
        _CAR = _car_parts()
    body, chip, parts, gx, gy = _CAR
    h, w = body.shape
    cv = Canvas(); tile(cv, "#16a08d", "#0a554f", edge=None)
    t = f / FRAMES
    for k in range(18):                                                          # road in perspective
        y = 63 - k
        half = 3 + (18 - k) * 1.1
        cv.flat((YY >= y) & (YY < y + 1) & (np.abs(XX - 32) <= half), "#0b4842")
        cv.flat((YY >= y) & (YY < y + 1) & (np.abs(np.abs(XX - 32) - half) < 0.8), "#5fb8ac")
    for k in range(3):                                                           # dashes flow toward the viewer
        p = (t + k / 3) % 1.0
        y = 47 + ease(p) * 16
        cv.flat((YY >= y) & (YY < y + 1 + p * 3) & (np.abs(XX - 32) <= 0.6 + p * 0.9), "#e6fbf6")
    bob = 1 if 0.25 < (t * 2) % 1 < 0.75 else 0
    x0, y0 = (N - w) // 2, 12 + bob
    cv.shadow(32, y0 + h + 1, w / 2 - 2, 2.5, 0.4)

    def place(m):
        out = np.zeros((N, N), bool)
        out[y0:y0 + h, x0:x0 + w] = m
        return out

    def place_f(a):
        out = np.zeros((N, N))
        out[y0:y0 + h, x0:x0 + w] = a
        return out
    n = np.stack([-place_f(gx), -place_f(gy), np.ones((N, N))], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    cv.shade(place(body), n, "#eaf8f4")
    flat_n = np.dstack([np.zeros((N, N)), np.zeros((N, N)), np.ones((N, N))])
    ws = place(parts["windshield"])
    cv.shade(ws, flat_n, "#0f6a63", outline=False, spec=False)
    sweep = (t * 1.5) % 1.5 - 0.25                                                # shine sweeps over the glass
    sx = x0 + sweep * w
    cv.put(ws & (np.abs((XX - sx) + (YY - y0) * 0.6) < 1.4), rgb("#9de6da"), 0.8)
    on = (f // 6) % 2 == 0
    lights = place(parts["lights"])
    cv.shade(lights, flat_n, "#ffe7a1" if on else "#7cc9bd", outline=False, spec=False)
    if on:
        for cx in (x0 + w * 0.2, x0 + w * 0.8):
            cv.glow(cx, y0 + h * 0.58, 9, "#fff2b8", 0.45)
    cv.shade(place(parts["grille"]), flat_n, "#0e5f59", outline=False, spec=False)
    m = place(chip)
    cv.shade(m, flat_n, "#f7a21b" if on else "#c2630a", outline=False, spec=False)
    if on:
        cy, cx = np.argwhere(m).mean(0)
        cv.glow(cx, cy, 5, "#ffd27a", 0.5)
    return cv


def research_hound(f):
    cv = Canvas(); tile(cv, "#232323", "#141414")
    t = f / FRAMES
    sniff = ease((t * 4) % 1) if (t * 4) % 2 < 1 else ease(1 - (t * 4) % 1)
    sx = sniff * 2
    cv.shadow(22, 52, 14, 3, 0.45)
    m, n = Canvas.ellipsoid(13 + sx * 0.3, 30, 6, 13); cv.shade(m, n, "#b4760a")              # ear behind
    m, n = Canvas.ellipsoid(22 + sx * 0.5, 26, 13, 12); cv.shade(m, n, "#efa514")             # skull
    m, n = Canvas.ellipsoid(35 + sx, 31, 11, 7); cv.shade(m, n, "#efa514")                    # muzzle
    m, n = Canvas.ellipsoid(45 + sx, 29, 3.4, 3.0); cv.shade(m, n, "#2a1a10")                 # nose
    m, n = Canvas.ellipsoid(15 + sx * 0.3, 33, 5, 11); cv.shade(m, n, "#c4800c")              # ear front
    m, n = Canvas.ellipsoid(27 + sx * 0.6, 22, 2.6, 2.8); cv.shade(m, n, "#1c120a", outline=False)   # eye
    cv.flat((np.hypot(XX - 26.4 - sx * 0.6, YY - 21) < 0.9), "#ffffff")
    m, n = Canvas.rbox(17, 37, 13, 9, 4, 2); cv.shade(m, n, "#e19b12")                         # neck
    if sniff > 0.6:
        for k, (dx, dy) in enumerate(((5, -4), (7, -1), (6, 3))):
            cv.flat(np.hypot(XX - 49 - sx - dx * 0.4, YY - 29 - dy) < 0.9, "#9aa0a6", 0.8)
    # page with a folded corner, lines turning into checks one by one
    m, n = Canvas.rbox(38, 36, 20, 22, 2, 1.5); cv.shade(m, n, "#fbfbf8", spec=False)
    cv.flat((XX >= 52) & (YY < 42) & (XX - 52 > YY - 36), "#141414")
    cv.flat((XX >= 52) & (YY < 42) & (XX - 52 <= YY - 36) & (XX < 58) & (YY >= 36), "#cfcfca")
    for k, y in enumerate((43, 47, 51)):
        done = t > 0.35 + k * 0.17
        cv.flat((YY >= y) & (YY < y + 1.5) & (XX >= (47 if done else 41)) & (XX <= 54), "#b9b9b4")
        if done:
            pop = min(1.0, (t - (0.35 + k * 0.17)) * 10)
            cv.line(41, y + 0.5, 42.5, y + 2 * pop, "#16a34a", 1.4)
            cv.line(42.5, y + 2 * pop, 45, y - 1.5 * pop, "#16a34a", 1.4)
    return cv


def skill_vision(f):
    """Friendly, flat eyes like the original icon: no bulge and no shadow, a gentle glance and a sliding blink."""
    cv = Canvas(); tile(cv, "#232323", "#141414")
    t = f / FRAMES
    look = 2.2 * math.sin(2 * math.pi * t)
    lid = 0.0
    if 0.56 < t < 0.72:                                                             # lid slides down and back up
        lid = ease(1 - abs(t - 0.64) / 0.08)
    for cx in (21, 43):
        cy, rx = 25, 8.5
        ry = 9.5 * (1 - 0.92 * lid)                                               # the eye squashes as it closes
        if lid > 0.8:                                                              # closed: a soft curved lid line
            for dx in np.linspace(-rx + 1, rx - 1, 40):
                y = cy + 1.5 - 2.6 * (1 - (dx / rx) ** 2)
                cv.flat(np.hypot(XX - (cx + dx), YY - y) < 0.9, "#d4dbe4")
            continue
        u, v = (XX - cx) / rx, (YY - cy) / ry
        oval = u * u + v * v <= 1
        cv.flat(oval, "#f4f6f8")
        u2, v2 = (XX - cx) / rx, (YY - cy + 2.2 * ry / 9.5) / ry
        cv.flat(oval & ~(u2 * u2 + v2 * v2 <= 1), "#d4dbe4")                        # soft shade along the bottom
        iris = np.hypot(XX - cx - look, YY - cy - 0.8) <= 4.6
        cv.flat(iris & oval, "#3cb8ec")
        cv.flat(iris & oval & ~(np.hypot(XX - cx - look, YY - cy - 0.8) <= 3.6), "#2a8fc4")
        cv.flat(oval & (np.hypot(XX - cx - look, YY - cy - 0.8) <= 2.1), "#10202e")
        cv.flat(oval & (np.hypot(XX - cx - look + 1.7, YY - cy + 1.2) <= 1.3), "#ffffff")   # one catch-light
        cv.put(oval & ~erode(oval), rgb("#aeb8c4"))                                     # light outline, not a dark ring
    pulse = 0.5 + 0.5 * wave(f)
    col = mix(rgb("#2c9be0"), rgb("#7fd4ff"), pulse)
    cv.line(25, 47, 30, 52, col * 0.5, 3.6); cv.line(30, 52, 40, 42, col * 0.5, 3.6)
    cv.line(25, 47, 30, 52, col, 2.2); cv.line(30, 52, 40, 42, col, 2.2)
    return cv


def agent_oracle(f):
    cv = Canvas(); tile(cv, "#232323", "#141414")
    t = f / FRAMES
    cv.shadow(32, 55, 16, 3, 0.45)
    m, n = Canvas.rbox(17, 46, 30, 6, 3, 2); cv.shade(m, n, "#e8dcc0")                          # stand
    m, n = Canvas.rbox(21, 42, 22, 6, 2.5, 2); cv.shade(m, n, "#fbf5e3")
    cv.glow(32, 26, 24, "#c9b4ef", 0.35)
    m, n = Canvas.ellipsoid(32, 26, 18, 18); cv.shade(m, n, "#c8b4e6", spec=False)               # glass
    # the network inside turns in 3D: nodes on a tilted ring, nearer ones larger and brighter
    a0 = 2 * math.pi * t
    pts = []
    for k in range(4):
        a = a0 + k * math.pi / 2
        x, z = math.cos(a) * 12, math.sin(a)
        y = math.sin(a) * 5
        pts.append((32 + x, 26 + y - 1, z))
    for x, y, z in pts:
        cv.line(32, 25, x, y, mix(rgb("#5b4a86"), rgb("#8d7bb8"), 0.5 + 0.5 * z), 2.4)
        cv.line(32, 25, x, y, mix(rgb("#ffffff"), rgb("#d9cdf2"), 0.5 - 0.5 * z), 1.1)
    for x, y, z in sorted(pts, key=lambda p: p[2]):
        r = 2.6 + z * 0.9
        m, n = Canvas.ellipsoid(x, y, r, r); cv.shade(m, n, "#ffffff" if z > 0 else "#ece6fa", out_k=0.45)
    m, n = Canvas.ellipsoid(32, 25, 3.2, 3.2); cv.shade(m, n, "#ffffff", out_k=0.45)
    cv.line(21, 18, 26, 12, "#f4efff", 1.6, 0.9)                                                  # glass reflection
    cv.flat(np.hypot(XX - 24, YY - 20) < 1.2, "#ffffff")
    m, _ = Canvas.ellipsoid(32, 26, 18, 18); cv.put(m & ~erode(m), rgb("#6d5a94"))
    if (f // 3) % 4 == 0:                                                                          # twinkle
        for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            cv.flat((np.abs(XX - 46.5 - dx) < 0.5) & (np.abs(YY - 11.5 - dy) < 0.5), "#ffffff")
    return cv


def mr_usage(f):
    cv = Canvas(); tile(cv, "#232323", "#141414")
    rows = [(17, "#3b82f6", 0.72, 0.0), (31, "#3b82f6", 0.58, 0.33), (45, "#f5b014", 0.22, 0.66)]
    for y, c, base, ph in rows:
        m, n = Canvas.rbox(10, y - 4, 44, 9, 4.5, 2); cv.shade(m, n, "#1d2940", spec=False)     # track
        w = 44 * (base + 0.16 * wave(f, phase=ph))
        m, n = Canvas.rbox(10, y - 4, max(9, w), 9, 4.5, 2.5); cv.shade(m, n, c)
        g = (f / FRAMES + ph) % 1
        gx = 12 + g * (max(9, w) - 6)
        cv.line(gx, y - 2, gx + 3, y - 2, "#ffffff", 1, 0.75)                                       # glint runs along the bar
    return cv


def llm_dogfight(f):
    cv = Canvas(); tile(cv, "#1f1f22", "#121214")
    t = f / FRAMES
    rng = np.random.default_rng(7)
    for sx, sy in rng.integers(4, 60, size=(14, 2)):                                               # starfield twinkle
        if (sx + sy + f) % 6:
            cv.flat((np.abs(XX - sx - 0.5) < 0.5) & (np.abs(YY - sy - 0.5) < 0.5), "#6b7280" if (sx + f) % 5 else "#e5e7eb")
    b1, b2 = 2.2 * wave(f), -2.2 * wave(f)

    def saucer(cx, cy, body, dome):
        cv.shadow(cx, cy + 9, 9, 1.6, 0.25)
        m, n = Canvas.ellipsoid(cx, cy - 3, 6, 5); cv.shade(m, n, dome)
        m, n = Canvas.ellipsoid(cx, cy + 1, 14, 4.2); cv.shade(m, n, body)
        for k in (-8, 0, 8):
            on = (f // 3 + k) % 2 == 0
            cv.flat(np.hypot(XX - cx - k, YY - cy - 2) < 1.1, "#ffffff" if on else "#fff3b0")
    saucer(20, 18 + b1, "#53cfc2", "#bdf0ea")
    saucer(44, 42 + b2, "#d23d76", "#f6b0cb")
    if 0.15 < t < 0.3:
        cv.line(27, 22 + b1, 37, 37 + b2, "#5ad1c5", 3, 0.5); cv.line(27, 22 + b1, 37, 37 + b2, "#e6fffb", 1.2)
    if 0.65 < t < 0.8:
        cv.line(37, 38 + b2, 27, 23 + b1, "#e0457f", 3, 0.5); cv.line(37, 38 + b2, 27, 23 + b1, "#ffe4ef", 1.2)
    for hit, (hx, hy) in ((0.3 < t < 0.4, (38, 37 + b2)), (0.8 < t < 0.9, (26, 23 + b1))):
        if hit:
            cv.glow(hx, hy, 8, "#fff3b0", 0.9)
            for dx, dy in ((3, 0), (-3, 0), (0, 3), (0, -3)):
                cv.line(hx, hy, hx + dx, hy + dy, "#ffffff", 1)
    return cv


def tigerocr(f):
    cv = Canvas(); tile(cv, "#f2b03a", "#c95511", edge=None)
    t = f / FRAMES
    phase = t * 16
    stripe = ((XX + YY + phase) % 22) < 6
    inside = cv.tile_mask & erode(erode(cv.tile_mask))
    cv.flat(stripe & inside, "#1a140c")
    cv.flat(stripe & inside & ((((XX + YY + phase) % 22) < 1.2)), "#3a2a14")
    y = 6 + ease(t) * 50                                                                          # scan beam with glow
    for dy, a in ((-3, 0.25), (-2, 0.4), (-1, 0.7), (0, 1.0), (1, 0.55), (2, 0.25)):
        cv.put(inside & (np.abs(YY - (y + dy)) < 0.5), rgb("#fff4d6"), a)
    return cv


def murasaki(f):
    """Blue is pushed out of the core, red is pulled in, and the purple orb glows where they cross."""
    cv = Canvas(); tile(cv, "#0d0918", "#05030a", edge="#3b2a55")
    t = f / FRAMES
    pulse = 0.5 + 0.5 * wave(f, phase=0.25)
    cv.glow(32, 32, 22 + 3 * pulse, "#6d28d9", 0.55)
    for k in range(8):
        ph = (t + k / 8) % 1
        a = k * math.pi / 4 + 0.3
        r = 9 + ease(ph) * 20                                       # blue: repelled outward
        x, y = 32 + r * math.cos(a), 32 + r * math.sin(a)
        if r < 28:
            cv.line(32 + (r - 5) * math.cos(a), 32 + (r - 5) * math.sin(a), x, y, "#1e3a8a", 1.4, 0.8)
            cv.glow(x, y, 4, "#60a5fa", 0.9)
            cv.flat(np.hypot(XX - x, YY - y) < 1.1, "#e0f2ff")
        a2 = a + math.pi / 8
        r2 = 29 - ease(ph) * 19                                     # red: pulled inward
        x2, y2 = 32 + r2 * math.cos(a2), 32 + r2 * math.sin(a2)
        if r2 > 11:
            cv.line(32 + (r2 + 5) * math.cos(a2), 32 + (r2 + 5) * math.sin(a2), x2, y2, "#7f1d1d", 1.4, 0.8)
            cv.glow(x2, y2, 4, "#f87171", 0.9)
            cv.flat(np.hypot(XX - x2, YY - y2) < 1.1, "#ffe4e4")
    rr = 10 + 1.2 * pulse
    m, n = Canvas.ellipsoid(32, 32, rr, rr); cv.shade(m, n, mix(rgb("#7c3aed"), rgb("#a855f7"), pulse))
    m, n = Canvas.ellipsoid(32, 32, rr * 0.5, rr * 0.5); cv.shade(m, n, "#d8b4fe", outline=False)
    cv.flat(np.hypot(XX - 28.5, YY - 28.5) < 1.6, "#ffffff")
    return cv


def liteeda(f):
    """The LiteEDA Pulse mark on its green tile, with the pulse sliding sideways like a trace on a scope."""
    cv = Canvas(); tile(cv, "#44d9a2", "#0c7f53", edge=None)
    # the period is longer than the trace plus the pulse, so the pulse is never split across both ends
    x0, x1, period, width = 6, 58, 72, 16
    lo, hi = 40, 24                                                            # the logo's low and high levels
    s = 3 * f + 32                                                             # 3 px a frame; frame 0 is centred like the logo

    def level(x):
        return hi if (x - x0 - s) % period >= period - width else lo
    pts, y = [(x0, level(x0))], level(x0)
    for x in range(x0 + 1, x1 + 1):
        if level(x) != y:                                                      # an edge: a vertical step
            pts += [(x, y), (x, level(x))]
            y = level(x)
    pts.append((x1, y))
    segs = list(zip(pts, pts[1:]))

    def near(r, dy=0.0):
        m = np.zeros((N, N), bool)
        for (ax, ay), (bx, by) in segs:
            px, py, dx, dy2 = XX - ax, YY - ay - dy, bx - ax, by - ay
            t = np.clip((px * dx + py * dy2) / (dx * dx + dy2 * dy2 or 1), 0, 1)
            m |= np.hypot(px - t * dx, py - t * dy2) <= r
        return m
    fade = np.ceil(np.clip((np.minimum(XX - x0, x1 - XX) + 1) / 12, 0, 1) * 4) / 4   # the trace fades in and out at its ends
    cv.put(near(3.2, 2), np.zeros(3) + rgb("#03341f"), fade * 0.35)          # soft drop shadow, as on the app icon
    cv.put(near(3.6), np.zeros(3) + rgb("#0a6644"), fade)                    # darker rim of the same green
    band = np.clip((YY - hi + 2) / (lo - hi + 4), 0, 1)                       # white at the top, mint at the bottom
    col = mix(rgb("#ffffff"), rgb("#dcf4e9"), np.round(band * 3)[..., None] / 3)
    cv.put(near(2.75), col, fade)
    for x, y in pts[1:-1]:                                                     # glint on the high plateau's corners
        if y == hi:
            cv.put(np.hypot(XX - x, YY - y + 1) < 1.0, rgb("#ffffff"), fade)
    return cv


ALL = {
    "opencarmind": opencarmind, "research-hound": research_hound, "skill-vision": skill_vision,
    "agent-oracle": agent_oracle, "mr-usage": mr_usage, "llm-dogfight": llm_dogfight,
    "tigerocr": tigerocr, "murasaki": murasaki, "liteeda": liteeda,
}


def to_gif(name, canvases, ms=70):
    """One shared palette for all frames (no flicker), hard transparency only at the rounded corners."""
    rgbs = [np.clip(cv.c, 0, 255).astype(np.uint8) for cv in canvases]
    alpha = [cv.a > 0.5 for cv in canvases]
    stack = np.concatenate([r[a] for r, a in zip(rgbs, alpha)])
    sample = Image.fromarray(stack.reshape(-1, 1, 3))
    pal_img = sample.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    pal = np.array(pal_img.getpalette()[:255 * 3], float).reshape(-1, 3)
    frames = []
    for r, a in zip(rgbs, alpha):
        flat = r.reshape(-1, 3).astype(float)
        idx = np.argmin(((flat[:, None, :] - pal[None, :, :]) ** 2).sum(-1), axis=1) + 1
        idx[~a.reshape(-1)] = 0
        im = Image.fromarray(idx.reshape(N, N).astype(np.uint8), "P")
        im.putpalette([0, 0, 0] + pal.astype(int).flatten().tolist())
        frames.append(im.resize((N * SCALE, N * SCALE), Image.NEAREST))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{name}.gif")
    frames[0].save(path, save_all=True, append_images=frames[1:], duration=ms, loop=0, disposal=2, transparency=0, optimize=False)
    return path, frames


if __name__ == "__main__":
    import sys
    pick = sys.argv[1:] or list(ALL)
    sheets = []
    for name in pick:
        canvases = [ALL[name](f) for f in range(FRAMES)]
        path, frames = to_gif(name, canvases)
        print(f"{name}: {len(frames)} frames, {os.path.getsize(path) // 1024} KB")
        sheets.append(frames)
    # review: frames 0, 6, 12, 18 of each, on GitHub's light and dark page colours
    cell = N * SCALE
    sheet = Image.new("RGB", (8 * (cell + 6) + 12, len(sheets) * (cell + 6)), (255, 255, 255))
    sheet.paste((13, 17, 23), (4 * (cell + 6) + 12, 0, sheet.width, sheet.height))
    for r, frames in enumerate(sheets):
        for c, fi in enumerate((0, 6, 12, 18)):
            im = frames[fi].convert("RGBA")
            for off in (0, 4 * (cell + 6) + 12):
                sheet.paste(im, (off + c * (cell + 6), r * (cell + 6)), im)
    sheet.save(os.path.join(OUT, "review.png"))
