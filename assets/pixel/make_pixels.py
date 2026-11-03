"""Pixel-art animated icons for the profile's projects: 32 x 32 grid, exported 4x with nearest-neighbour, looping GIFs."""
import math
import os
from PIL import Image

N = 32
SCALE = 4
OUT = os.path.join(os.path.dirname(__file__), "out")  # run with Pillow installed: python3 assets/pixel/make_pixels.py
CLEAR = None


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Frame:
    def __init__(self):
        self.p = [[CLEAR] * N for _ in range(N)]

    def px(self, x, y, c):
        if 0 <= x < N and 0 <= y < N and c is not None:
            self.p[y][x] = hexc(c) if isinstance(c, str) else c

    def rect(self, x, y, w, h, c):
        for j in range(y, y + h):
            for i in range(x, x + w):
                self.px(i, j, c)

    def disc(self, cx, cy, r, c):
        for j in range(N):
            for i in range(N):
                if (i - cx) ** 2 + (j - cy) ** 2 <= r * r + r * 0.6:
                    self.px(i, j, c)

    def ellipse(self, cx, cy, rx, ry, c):
        for j in range(N):
            for i in range(N):
                if ((i - cx) / rx) ** 2 + ((j - cy) / ry) ** 2 <= 1.0:
                    self.px(i, j, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.px(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def tile(self, top, bottom=None, radius=6, edge="#4b5260"):
        """Rounded tile. A gradient is drawn as four flat bands, the pixel-art way. The 1 px edge in a mid-tone keeps a
        dark tile visible on GitHub's dark theme (#0d1117) and a light tile visible on white."""
        bottom = bottom or top
        t, b = hexc(top), hexc(bottom)
        for j in range(N):
            k = min(3, j * 4 // N) / 3
            row = tuple(round(t[i] + (b[i] - t[i]) * k) for i in range(3))
            for i in range(N):
                if self.inside(i, j, radius):
                    self.p[j][i] = row
        if edge:
            e = hexc(edge)
            inside = [[self.p[j][i] is not None for i in range(N)] for j in range(N)]
            for j in range(N):
                for i in range(N):
                    if inside[j][i] and any(not (0 <= i + di < N and 0 <= j + dj < N and inside[j + dj][i + di])
                                            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                        self.p[j][i] = e

    @staticmethod
    def inside(i, j, r):
        for cx, cy in ((r, r), (N - 1 - r, r), (r, N - 1 - r), (N - 1 - r, N - 1 - r)):
            if (i < r and j < r and cx == r and cy == r) or (i > N - 1 - r and j < r and cx == N - 1 - r and cy == r) \
               or (i < r and j > N - 1 - r and cx == r and cy == N - 1 - r) or (i > N - 1 - r and j > N - 1 - r and cx == N - 1 - r and cy == N - 1 - r):
                return (i - cx) ** 2 + (j - cy) ** 2 <= r * r + 1
        return True


def save(name, frames, ms):
    colors = sorted({c for f in frames for row in f.p for c in row if c is not None})
    assert len(colors) <= 255, (name, len(colors))
    palette = [0, 0, 0]  # index 0 is the transparent corner colour
    for c in colors:
        palette += list(c)
    index = {c: i + 1 for i, c in enumerate(colors)}
    imgs = []
    for f in frames:
        im = Image.new("P", (N, N))
        im.putpalette(palette + [0] * (768 - len(palette)))
        im.putdata([index[c] if c is not None else 0 for row in f.p for c in row])
        imgs.append(im.resize((N * SCALE, N * SCALE), Image.NEAREST))
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{name}.gif")
    imgs[0].save(path, save_all=True, append_images=imgs[1:], duration=ms, loop=0, disposal=2, transparency=0, optimize=False)
    return path, imgs


def stamp(F, art, x0, y0, colors):
    """Draws a character map: each character is a colour key, '.' is left as it is."""
    for j, line in enumerate(art.strip("\n").split("\n")):
        for i, ch in enumerate(line):
            if ch != "." and ch in colors:
                F.px(x0 + i, y0 + j, colors[ch])


# ------------------------------------------------------------------ projects
CAR = """
......MMMMMMMMMMMM......
....MMTTTTTTTTTTTTMM....
...MTTTTTTTTTTTTTTTTM...
..MTTTTTTTTCCTTTTTTTTM..
..MTTTTMMMMCCMMMMTTTTM..
.MMMMMMMMMMMMMMMMMMMMMM.
MMMMMMMMMMMMMMMMMMMMMMMM
.MLLLLMMMMMMMMMMMMLLLLM.
.MLLLLMMMMMMMMMMMMLLLLM.
.MMMMMMMMMMMMMMMMMMMMMM.
.MMMMMMGGGGGGGGGGMMMMMM.
.MMMMMMMMMMMMMMMMMMMMMM.
..MMMM............MMMM..
..MMMM............MMMM..
"""


def opencarmind():
    out = []
    for f in range(12):
        F = Frame(); F.tile("#14917f", "#0b5f58", edge=None)
        for k in range(16):                                   # road edges converge toward the horizon
            F.px(15 - k // 2 - 1, 30 - k, "#0a4b45" if k < 9 else None)
            F.px(16 + k // 2 + 1, 30 - k, "#0a4b45" if k < 9 else None)
        for k in range(2):                                    # centre dashes flow toward the viewer
            dy = 22 + ((f + 6 * k) % 12) * 9 // 12
            F.rect(15, dy, 2, 1 + (dy - 22) // 4, "#9fd9cf")
        bob = 1 if f % 4 in (1, 2) else 0
        on = f % 6 < 3
        stamp(F, CAR, 4, 5 + bob, {"M": "#e8f5f2", "T": "#0f766e", "C": "#f59e0b" if on else "#b45309",
                                   "L": "#fde68a" if on else "#bfe9e1", "G": "#0f766e"})
        out.append(F)
    return out, 110


HOUND = """
.....AAAAA..........
...AAAAAAAAA........
..DAAAAAAAAAA.......
.DDAAAAAAAAAAA......
.DDAAAKKAAAAAAA.....
DDDAAAKKAAAAAAAAAA..
DDDAAAAAAAAAAAAAAAAK
DDDAAAAAAAAAAAAAAAKK
DDDDAAAAAAAAAAAAAA..
DDDDAAAAAAAAAAAAA...
.DDDDAAAAAAAA.......
..DDDAAAAAAA........
...DDAAAAAA.........
.....AAAAAA.........
.....AAAAAA.........
"""
PAGE = """
WWWWWWWFF.
WWWWWWWFFF
WWWWWWWWWW
WWWWWWWWWW
WWWWWWWWWW
WWWWWWWWWW
WWWWWWWWWW
WWWWWWWWWW
WWWWWWWWWW
WWWWWWWWWW
"""


def research_hound():
    out = []
    for f in range(12):
        F = Frame(); F.tile("#191919")
        sniff = 1 if f % 4 in (1, 2) else 0
        stamp(F, HOUND, 3 + sniff, 6, {"A": "#eca208", "D": "#b97c06", "K": "#191919"})
        if sniff:
            F.px(24 + sniff, 10, "#8a8a8a"); F.px(25 + sniff, 12, "#8a8a8a")
        stamp(F, PAGE, 19, 19, {"W": "#fdfefd", "F": "#c9c9c9"})
        for k, yy in enumerate((22, 24, 26)):
            if f >= 6 + 2 * k:
                F.px(20, yy, "#16a34a"); F.px(21, yy + 1, "#16a34a"); F.px(22, yy, "#16a34a"); F.px(23, yy - 1, "#16a34a")
                F.rect(24, yy, 3, 1, "#b8b8b8")
            else:
                F.rect(20, yy, 7, 1, "#b8b8b8")
        out.append(F)
    return out, 140


def skill_vision():
    out = []
    look = [0, 0, 1, 1, 1, 0, 0, -1, -1, -1, 0, 0]
    for f in range(12):
        F = Frame(); F.tile("#191919")
        blink = f == 5
        for cx in (10, 21):
            if blink:
                F.rect(cx - 5, 13, 11, 1, "#f5f5f5")
            else:
                F.disc(cx, 13, 5, "#f5f5f5")
                F.disc(cx + look[f], 13, 3, "#4cc9f0")
                F.disc(cx + look[f], 13, 1, "#0b0b0b")
                F.px(cx + look[f] - 1, 11, "#ffffff")
        ck = "#38bdf8" if f % 6 < 4 else "#7dd3fc"
        F.line(12, 23, 14, 25, ck); F.line(14, 25, 20, 19, ck)
        F.line(12, 24, 14, 26, ck); F.line(14, 26, 20, 20, ck)
        out.append(F)
    return out, 130


def agent_oracle():
    out = []
    for f in range(12):
        F = Frame(); F.tile("#191919")
        F.rect(10, 24, 12, 2, "#fdf9ec"); F.rect(8, 26, 16, 2, "#e8dfc4")         # base
        F.disc(16, 14, 9, "#ccbae4")
        F.disc(16, 14, 7, "#d9cbee")
        a = f / 12 * 2 * math.pi
        nodes = [(16 + round(5 * math.cos(a + k * 2.094)), 14 + round(4 * math.sin(a + k * 2.094))) for k in range(3)]
        hub = (16, 14)
        for n in nodes:
            F.line(hub[0], hub[1], n[0], n[1], "#ffffff")
        for n in nodes + [hub]:
            F.rect(n[0], n[1], 2, 2, "#ffffff")
        if f % 4 == 0:
            F.px(21, 8, "#ffffff"); F.px(22, 7, "#ffffff"); F.px(20, 7, "#e9e0f7"); F.px(21, 6, "#e9e0f7")   # sparkle
        out.append(F)
    return out, 120


def mr_usage():
    out = []
    for f in range(16):
        F = Frame(); F.tile("#191919")
        tracks = [(9, "#3b82f6", 0.0), (15, "#3b82f6", 2.1), (21, "#f5b014", 4.2)]
        for y, c, ph in tracks:
            F.rect(6, y, 20, 3, "#1e2a44")
            base = 0.25 if c == "#f5b014" else 0.65
            w = max(2, round(20 * (base + 0.25 * math.sin(f / 16 * 2 * math.pi + ph))))
            F.rect(6, y, w, 3, c)
            F.px(6 + w - 1, y, "#93c5fd" if c != "#f5b014" else "#fde68a")
        out.append(F)
    return out, 110


def llm_dogfight():
    out = []
    for f in range(12):
        F = Frame(); F.tile("#191918")
        b1 = round(math.sin(f / 12 * 2 * math.pi))
        b2 = -b1

        def saucer(cx, cy, body, dome):
            F.ellipse(cx, cy, 6, 2, body)
            F.ellipse(cx, cy - 2, 3, 2, dome)
            F.px(cx - 4, cy, "#ffffff"); F.px(cx, cy + 1, "#ffffff"); F.px(cx + 4, cy, "#ffffff")
        saucer(10, 10 + b1, "#5ad1c5", "#bdeee9")
        saucer(22, 21 + b2, "#c4336b", "#f2a7c3")
        if f in (3, 4):
            F.line(14, 12 + b1, 19, 18 + b2, "#5ad1c5")
        if f in (9, 10):
            F.line(18, 19 + b2, 13, 13 + b1, "#c4336b")
        if f in (5, 11):
            hx, hy = (20, 19 + b2) if f == 5 else (12, 12 + b1)
            F.px(hx, hy, "#ffffff"); F.px(hx + 1, hy, "#fff3b0"); F.px(hx - 1, hy, "#fff3b0"); F.px(hx, hy - 1, "#fff3b0"); F.px(hx, hy + 1, "#fff3b0")
        out.append(F)
    return out, 120


def tigerocr():
    out = []
    for f in range(12):
        F = Frame(); F.tile("#e79e26", "#cf6215", edge=None)
        for j in range(N):
            for i in range(N):
                if F.p[j][i] is not None and ((i + j + f) % 16) in (0, 1, 2, 3):
                    F.p[j][i] = hexc("#17140d")
        y = 4 + f * 2
        if y < 28:
            for i in range(N):
                if F.p[y][i] is not None:
                    F.p[y][i] = hexc("#fff3d6")
                if y + 1 < N and F.p[y + 1][i] is not None and F.p[y + 1][i] != hexc("#17140d"):
                    F.p[y + 1][i] = hexc("#f7c56a")
        out.append(F)
    return out, 110


def murasaki():
    """Blue is pushed out from the core and red is pulled in. Where they cross, the orb glows purple."""
    out = []
    frames = 16
    for f in range(frames):
        F = Frame(); F.tile("#07050c", edge="#3b2a55")
        cx, cy = 16, 16
        pulse = 1 if f % 8 < 4 else 0
        F.disc(cx, cy, 6 + pulse, "#2f104c")
        F.disc(cx, cy, 5, "#5b2a86")
        F.disc(cx, cy, 3 + pulse, "#8b3fd1")
        F.disc(cx, cy, 1, "#c37af0")
        F.px(cx - 2, cy - 2, "#f3e3ff")
        for k in range(6):
            # blue: repelled outward along six spokes, each spoke a little behind the last
            ph = ((f + 3 * k) % frames) / frames
            a = k * math.pi / 3 + 0.25
            r = 4 + ph * 10
            x, y = round(cx + r * math.cos(a)), round(cy + r * math.sin(a))
            tx, ty = round(cx + (r - 1.6) * math.cos(a)), round(cy + (r - 1.6) * math.sin(a))
            if r < 13:
                F.px(tx, ty, "#1e3a8a"); F.rect(x, y, 2, 2, "#38bdf8" if ph < 0.6 else "#60a5fa")
            # red: pulled inward along the spokes in between
            a2 = a + math.pi / 6
            r2 = 13 - ph * 9
            x2, y2 = round(cx + r2 * math.cos(a2)), round(cy + r2 * math.sin(a2))
            tx2, ty2 = round(cx + (r2 + 1.6) * math.cos(a2)), round(cy + (r2 + 1.6) * math.sin(a2))
            if r2 > 5:
                F.px(tx2, ty2, "#7f1d1d"); F.rect(x2, y2, 2, 2, "#ef4444" if ph < 0.6 else "#f87171")
        out.append(F)
    return out, 90


ALL = {
    "opencarmind": opencarmind, "research-hound": research_hound, "skill-vision": skill_vision,
    "agent-oracle": agent_oracle, "mr-usage": mr_usage, "llm-dogfight": llm_dogfight,
    "tigerocr": tigerocr, "murasaki": murasaki,
}

if __name__ == "__main__":
    sheet_rows = []
    for name, fn in ALL.items():
        frames, ms = fn()
        path, imgs = save(name, frames, ms)
        print(f"{name}: {len(frames)} frames, {ms} ms, {os.path.getsize(path)} bytes")
        sheet_rows.append([im.convert("RGBA") for im in imgs[:12]])
    # contact sheet for review: every frame, on GitHub's light page (left) and dark page (right)
    cell = N * SCALE // 2
    cols = 12
    sheet = Image.new("RGBA", (2 * cols * (cell + 4) + 16, len(sheet_rows) * (cell + 4)), (255, 255, 255, 255))
    sheet.paste((13, 17, 23, 255), (cols * (cell + 4) + 16, 0, sheet.width, sheet.height))
    for r, row in enumerate(sheet_rows):
        for c, im in enumerate(row[:cols]):
            small = im.resize((cell, cell), Image.NEAREST)
            for off in (0, cols * (cell + 4) + 16):
                sheet.paste(small, (off + c * (cell + 4), r * (cell + 4)), small)
    sheet.save(os.path.join(OUT, "contact_sheet.png"))
