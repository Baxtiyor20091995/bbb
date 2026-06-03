# -*- coding: utf-8 -*-
"""
Minimal sof-Python grafik kutubxona: piksel buferiga chizish va PNG eksport.
Tashqi kutubxonalarsiz (faqat zlib). MATLAB uslubidagi XY-grafiklar:
chiziqli/logarifmik o'q, ko'p egri chiziq, afsona (legend), markerlar.
"""
import zlib
import struct
import math

FONT = {
    '0': [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    '1': ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    '2': [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    '3': ["#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "],
    '4': ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    '5': ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    '6': ["  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "],
    '7': ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    '8': [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    '9': [" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "],
    'A': [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    'C': [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    'D': ["###  ", "#  # ", "#   #", "#   #", "#   #", "#  # ", "###  "],
    'E': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    'F': ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    'G': [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ### "],
    'H': ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    'I': [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    'J': ["  ###", "   # ", "   # ", "   # ", "#  # ", "#  # ", " ##  "],
    'K': ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    'R': ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    'S': [" ### ", "#   #", "#    ", " ### ", "    #", "#   #", " ### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    'W': ["#   #", "#   #", "#   #", "#   #", "# # #", "## ##", "#   #"],
    'X': ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    'Y': ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    ' ': ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
    '-': ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    '.': ["     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "],
    ',': ["     ", "     ", "     ", "     ", " ##  ", " ##  ", " #   "],
    '/': ["    #", "    #", "   # ", "  #  ", " #   ", "#    ", "#    "],
    '(': ["  ## ", " #   ", "#    ", "#    ", "#    ", " #   ", "  ## "],
    ')': [" ##  ", "   # ", "    #", "    #", "    #", "   # ", " ##  "],
    ':': ["     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "],
    '+': ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    '=': ["     ", "     ", "#####", "     ", "#####", "     ", "     "],
    '%': ["##  #", "##  #", "   # ", "  #  ", " #   ", "#  ##", "#  ##"],
}

BLUE = (0, 60, 200)
RED = (200, 30, 30)
GREEN = (0, 140, 40)
ORANGE = (210, 110, 0)
BLACK = (0, 0, 0)
GRID = (205, 205, 205)
DKGRID = (165, 165, 165)


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.buf = bytearray(bg * (w * h))

    def px(self, x, y, c):
        x = int(x); y = int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = c[0]; self.buf[i + 1] = c[1]; self.buf[i + 2] = c[2]

    def hline(self, x0, x1, y, c):
        if x1 < x0:
            x0, x1 = x1, x0
        for x in range(int(x0), int(x1) + 1):
            self.px(x, y, c)

    def vline(self, x, y0, y1, c):
        if y1 < y0:
            y0, y1 = y1, y0
        for y in range(int(y0), int(y1) + 1):
            self.px(x, y, c)

    def fill_rect(self, x0, y0, x1, y1, c):
        for y in range(int(y0), int(y1) + 1):
            self.hline(x0, x1, y, c)

    def line(self, x0, y0, x1, y1, c, width=1):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx = abs(x1 - x0); dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            if width <= 1:
                self.px(x0, y0, c)
            else:
                r = width // 2
                for ax in range(-r, r + 1):
                    for ay in range(-r, r + 1):
                        self.px(x0 + ax, y0 + ay, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def dashed_vline(self, x, y0, y1, c, dash=6, gap=5):
        if y1 < y0:
            y0, y1 = y1, y0
        y = int(y0); on = True
        while y <= y1:
            if on:
                for yy in range(y, min(y + dash, int(y1) + 1)):
                    self.px(x, yy, c)
            y += dash if on else gap
            on = not on

    def dashed_hline(self, x0, x1, y, c, dash=6, gap=5):
        if x1 < x0:
            x0, x1 = x1, x0
        x = int(x0); on = True
        while x <= x1:
            if on:
                for xx in range(x, min(x + dash, int(x1) + 1)):
                    self.px(xx, y, c)
            x += dash if on else gap
            on = not on

    def polyline(self, pts, c, width=2):
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], c, width)

    def fill_disc(self, x, y, r, c):
        for ay in range(-r, r + 1):
            for ax in range(-r, r + 1):
                if ax * ax + ay * ay <= r * r:
                    self.px(x + ax, y + ay, c)

    def mark_x(self, x, y, r, c):
        for d in range(-r, r + 1):
            self.px(x + d, y + d, c)
            self.px(x + d, y - d, c)
            self.px(x + d + 1, y + d, c)
            self.px(x + d + 1, y - d, c)

    def _glyph(self, ch, scale):
        g = FONT.get(ch.upper(), FONT[' '])
        out = []
        for r in range(7):
            for col in range(5):
                if g[r][col] == '#':
                    for sx in range(scale):
                        for sy in range(scale):
                            out.append((col * scale + sx, r * scale + sy))
        return out

    def text(self, x, y, s, c=(0, 0, 0), scale=2, spacing=1):
        cx = x
        for ch in s:
            for (gx, gy) in self._glyph(ch, scale):
                self.px(cx + gx, y + gy, c)
            cx += (5 + spacing) * scale

    def text_w(self, s, scale=2, spacing=1):
        return len(s) * (5 + spacing) * scale

    def text_vertical(self, x, y_bottom, s, c=(0, 0, 0), scale=2, spacing=1):
        cx = 0; pts = []
        for ch in s:
            for (gx, gy) in self._glyph(ch, scale):
                pts.append((cx + gx, gy))
            cx += (5 + spacing) * scale
        for (gx, gy) in pts:
            self.px(x + gy, y_bottom - gx, c)
        return self.text_w(s, scale, spacing)

    def to_png(self):
        raw = bytearray(); row = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw += self.buf[y * row:(y + 1) * row]
        comp = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            c = typ + data
            return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
                chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def nice_ticks(lo, hi, n=5):
    if hi <= lo:
        hi = lo + 1
    raw = (hi - lo) / n
    mag = 10 ** math.floor(math.log10(raw))
    step = 10 * mag
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    start = math.ceil(lo / step) * step
    ticks = []; v = start
    while v <= hi + step * 1e-6:
        ticks.append(round(v, 10)); v += step
    return ticks


def fmt(v):
    if v == 0:
        return "0"
    if abs(v) >= 1000 or abs(v) < 0.01:
        return "%.0e" % v
    if abs(v - round(v)) < 1e-9:
        return "%d" % round(v)
    return ("%.3f" % v).rstrip("0").rstrip(".")


def draw_axes(cv, area, xr, yr, *, xticks=None, yticks=None, xlog=False,
              xticklabels=None, title="", xlabel="", ylabel="",
              x0line=False, y0line=False):
    L, T, R, Bt = area

    def mapx(x):
        if xlog:
            x = math.log10(x); a = math.log10(xr[0]); b = math.log10(xr[1])
        else:
            a, b = xr
        return L + (x - a) / (b - a) * (R - L)

    def mapy(y):
        return Bt - (y - yr[0]) / (yr[1] - yr[0]) * (Bt - T)

    if yticks is None:
        yticks = nice_ticks(yr[0], yr[1])
    if xticks is None:
        xticks = nice_ticks(xr[0], xr[1])
    for yt in yticks:
        if yr[0] - 1e-9 <= yt <= yr[1] + 1e-9:
            cv.hline(L, R, int(round(mapy(yt))), GRID)
    for xt in xticks:
        if xr[0] - 1e-9 <= xt <= xr[1] + 1e-9:
            cv.vline(int(round(mapx(xt))), T, Bt, GRID)
    # nol o'qlari (root locus uchun)
    if y0line and yr[0] < 0 < yr[1]:
        cv.hline(L, R, int(round(mapy(0))), DKGRID)
    if x0line and xr[0] < 0 < xr[1]:
        cv.vline(int(round(mapx(0))), T, Bt, DKGRID)
    # ramka
    cv.line(L, T, R, T, BLACK); cv.line(L, Bt, R, Bt, BLACK)
    cv.line(L, T, L, Bt, BLACK); cv.line(R, T, R, Bt, BLACK)
    # belgilar
    for i, xt in enumerate(xticks):
        if xr[0] - 1e-9 <= xt <= xr[1] + 1e-9:
            xx = int(round(mapx(xt)))
            cv.vline(xx, Bt, Bt + 5, BLACK)
            lab = xticklabels[i] if xticklabels else fmt(xt)
            cv.text(xx - cv.text_w(lab, 2) // 2, Bt + 9, lab, BLACK, 2)
    for yt in yticks:
        if yr[0] - 1e-9 <= yt <= yr[1] + 1e-9:
            yy = int(round(mapy(yt)))
            cv.hline(L - 5, L, yy, BLACK)
            lab = fmt(yt)
            cv.text(L - 9 - cv.text_w(lab, 2), yy - 7, lab, BLACK, 2)
    if title:
        cv.text(L + (R - L) // 2 - cv.text_w(title, 2) // 2, T - 24, title, BLACK, 2)
    if xlabel:
        cv.text(L + (R - L) // 2 - cv.text_w(xlabel, 2) // 2, Bt + 26, xlabel, BLACK, 2)
    if ylabel:
        h = cv.text_w(ylabel, 2)
        cv.text_vertical(16, T + (Bt - T) // 2 + h // 2, ylabel, BLACK, 2)
    return mapx, mapy


def draw_plot(cv, area, xdata, ydata, xr, yr, *, color=BLUE, extra=None, **kw):
    mapx, mapy = draw_axes(cv, area, xr, yr, **kw)
    if extra:
        extra(cv, mapx, mapy)
    cv.polyline([(mapx(x), mapy(y)) for x, y in zip(xdata, ydata)], color, 2)
    return mapx, mapy


def draw_legend(cv, x, y, entries, scale=2):
    """entries: list of (color, label). Yuqori-o'ng burchakda afsona."""
    lh = 7 * scale + 6
    bw = max(cv.text_w(lab, scale) for _, lab in entries) + 40
    bh = lh * len(entries) + 6
    cv.fill_rect(x, y, x + bw, y + bh, (255, 255, 255))
    cv.line(x, y, x + bw, y, BLACK); cv.line(x, y + bh, x + bw, y + bh, BLACK)
    cv.line(x, y, x, y + bh, BLACK); cv.line(x + bw, y, x + bw, y + bh, BLACK)
    for i, (color, lab) in enumerate(entries):
        cy = y + 6 + i * lh + 7 * scale // 2
        cv.line(x + 6, cy, x + 30, cy, color, 3)
        cv.text(x + 36, cy - 7 * scale // 2, lab, BLACK, scale)


def draw_multi(cv, area, curves, xr, yr, *, legend_pos="tr", **kw):
    """curves: list of dict(x=, y=, color=, label=)."""
    mapx, mapy = draw_axes(cv, area, xr, yr, **kw)
    for cu in curves:
        cv.polyline([(mapx(x), mapy(y)) for x, y in zip(cu["x"], cu["y"])],
                    cu["color"], 2)
    entries = [(cu["color"], cu["label"]) for cu in curves if cu.get("label")]
    if entries:
        L, T, R, Bt = area
        bw = max(cv.text_w(lab, 2) for _, lab in entries) + 40
        if legend_pos == "tr":
            draw_legend(cv, R - bw - 10, T + 8, entries)
        else:
            draw_legend(cv, L + 12, T + 8, entries)
    return mapx, mapy


# --------------------------------------------------------------------------
# Ko'phad ildizlarini topish (Durand-Kerner) — ildiz godografi uchun
# --------------------------------------------------------------------------
def poly_roots(coeffs):
    """coeffs: kamayuvchi tartibda [a_n,...,a0]. Kompleks ildizlar ro'yxati."""
    a = [complex(c) for c in coeffs]
    while len(a) > 1 and abs(a[0]) < 1e-14:
        a = a[1:]
    n = len(a) - 1
    if n <= 0:
        return []
    a = [c / a[0] for c in a]  # monik
    roots = [(0.4 + 0.9j) ** k for k in range(n)]
    for _ in range(200):
        maxd = 0.0
        new = []
        for i in range(n):
            num = a[0]
            for c in a[1:]:
                num = num * roots[i] + c
            den = 1 + 0j
            for j in range(n):
                if j != i:
                    den *= (roots[i] - roots[j])
            if abs(den) < 1e-30:
                den = 1e-30
            delta = num / den
            new.append(roots[i] - delta)
            maxd = max(maxd, abs(delta))
        roots = new
        if maxd < 1e-12:
            break
    return roots
