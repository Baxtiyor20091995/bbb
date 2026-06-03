# -*- coding: utf-8 -*-
"""
Minimal sof-Python grafik kutubxona: piksel buferiga chizish va PNG eksport.
Tashqi kutubxonalarsiz (faqat zlib standart kutubxonasidan PNG uchun).
MATLAB uslubidagi XY-grafiklar (chiziqli va logarifmik o'q) chizish uchun.
"""
import zlib
import struct
import math

# ---------------------------------------------------------------------------
# 5x7 bitmap shrift (katta harflar, raqamlar, belgilar)
# ---------------------------------------------------------------------------
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


class Canvas:
    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.buf = bytearray(bg * (w * h))

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.buf[i] = c[0]
            self.buf[i + 1] = c[1]
            self.buf[i + 2] = c[2]

    def hline(self, x0, x1, y, c):
        if x1 < x0:
            x0, x1 = x1, x0
        for x in range(x0, x1 + 1):
            self.px(x, y, c)

    def vline(self, x, y0, y1, c):
        if y1 < y0:
            y0, y1 = y1, y0
        for y in range(y0, y1 + 1):
            self.px(x, y, c)

    def line(self, x0, y0, x1, y1, c, width=1):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
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
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def dashed_vline(self, x, y0, y1, c, dash=6, gap=5):
        if y1 < y0:
            y0, y1 = y1, y0
        y = y0
        on = True
        while y <= y1:
            seg = dash if on else gap
            if on:
                for yy in range(y, min(y + seg, y1 + 1)):
                    self.px(x, yy, c)
            y += seg
            on = not on

    def dashed_hline(self, x0, x1, y, c, dash=6, gap=5):
        if x1 < x0:
            x0, x1 = x1, x0
        x = x0
        on = True
        while x <= x1:
            seg = dash if on else gap
            if on:
                for xx in range(x, min(x + seg, x1 + 1)):
                    self.px(xx, y, c)
            x += seg
            on = not on

    def polyline(self, pts, c, width=2):
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], c, width)

    def _glyph_pixels(self, ch, scale):
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
            for (px, py) in self._glyph_pixels(ch, scale):
                self.px(cx + px, y + py, c)
            cx += (5 + spacing) * scale

    def text_w(self, s, scale=2, spacing=1):
        return len(s) * (5 + spacing) * scale

    def text_vertical(self, x, y_bottom, s, c=(0, 0, 0), scale=2, spacing=1):
        """Vertikal yozuv (pastdan yuqoriga o'qiladi), 90° CCW burilgan."""
        # avval gorizontal piksellarni yig'amiz, keyin aylantiramiz
        total_w = self.text_w(s, scale, spacing)
        cx = 0
        pts = []
        for ch in s:
            for (px, py) in self._glyph_pixels(ch, scale):
                pts.append((cx + px, py))
            cx += (5 + spacing) * scale
        ch_h = 7 * scale
        for (px, py) in pts:
            # 90° CCW: yangi_x = py, yangi_y = (total_w-1 - px)
            nx = x + py
            ny = y_bottom - px
            self.px(nx, ny, c)
        return total_w  # vertikal balandlik

    def to_png(self):
        raw = bytearray()
        row = self.w * 3
        for y in range(self.h):
            raw.append(0)  # filter type 0
            raw += self.buf[y * row:(y + 1) * row]
        comp = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            c = typ + data
            return (struct.pack(">I", len(data)) + c +
                    struct.pack(">I", zlib.crc32(c) & 0xffffffff))

        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
                chunk(b"IDAT", comp) + chunk(b"IEND", b""))


# ---------------------------------------------------------------------------
# XY grafik chizuvchi yuqori darajali funksiya
# ---------------------------------------------------------------------------
BLUE = (0, 60, 200)
BLACK = (0, 0, 0)
GRID = (205, 205, 205)
RED = (200, 30, 30)
DKGRID = (170, 170, 170)


def nice_ticks(lo, hi, n=5):
    if hi <= lo:
        hi = lo + 1
    raw = (hi - lo) / n
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    else:
        step = 10 * mag
    start = math.ceil(lo / step) * step
    ticks = []
    v = start
    while v <= hi + step * 1e-6:
        ticks.append(round(v, 10))
        v += step
    return ticks


def fmt(v):
    if v == 0:
        return "0"
    av = abs(v)
    if av >= 1000 or av < 0.01:
        return ("%.0e" % v)
    if abs(v - round(v)) < 1e-9:
        return "%d" % round(v)
    s = ("%.3f" % v).rstrip("0").rstrip(".")
    return s


def draw_plot(cv, area, xdata, ydata, xr, yr, *, title="", xlabel="",
              ylabel="", xticks=None, yticks=None, xlog=False,
              color=BLUE, xticklabels=None, extra=None):
    """
    cv: Canvas. area=(L,T,R,Bt) piksel chegaralar (chizma to'rtburchagi).
    xr=(xmin,xmax), yr=(ymin,ymax). xlog -> x o'qi log10 bo'yicha.
    extra: foydalanuvchi qo'shimcha chizmalari uchun callback(cv, mapx, mapy).
    """
    L, T, R, Bt = area

    def mapx(x):
        xv = math.log10(x) if xlog else x
        x0 = math.log10(xr[0]) if xlog else xr[0]
        x1 = math.log10(xr[1]) if xlog else xr[1]
        return L + (xv - x0) / (x1 - x0) * (R - L)

    def mapy(y):
        return Bt - (y - yr[0]) / (yr[1] - yr[0]) * (Bt - T)

    # to'r chiziqlari
    if yticks is None:
        yticks = nice_ticks(yr[0], yr[1])
    for yt in yticks:
        if yr[0] - 1e-9 <= yt <= yr[1] + 1e-9:
            yy = int(round(mapy(yt)))
            cv.hline(L, R, yy, GRID)
    if xticks is None:
        xticks = nice_ticks(xr[0], xr[1])
    for i, xt in enumerate(xticks):
        if xr[0] - 1e-9 <= xt <= xr[1] + 1e-9:
            xx = int(round(mapx(xt)))
            cv.vline(xx, T, Bt, GRID)

    # qo'shimcha chizmalar (dashed margin chiziqlari va h.k.)
    if extra:
        extra(cv, mapx, mapy)

    # asosiy egri chiziq
    pts = [(mapx(x), mapy(y)) for x, y in zip(xdata, ydata)]
    cv.polyline(pts, color, width=2)

    # ramka
    cv.line(L, T, R, T, BLACK, 1)
    cv.line(L, Bt, R, Bt, BLACK, 1)
    cv.line(L, T, L, Bt, BLACK, 1)
    cv.line(R, T, R, Bt, BLACK, 1)

    # x belgilar
    for i, xt in enumerate(xticks):
        if xr[0] - 1e-9 <= xt <= xr[1] + 1e-9:
            xx = int(round(mapx(xt)))
            cv.vline(xx, Bt, Bt + 5, BLACK)
            lab = xticklabels[i] if xticklabels else fmt(xt)
            cv.text(xx - cv.text_w(lab, 2) // 2, Bt + 9, lab, BLACK, 2)
    # y belgilar
    for yt in yticks:
        if yr[0] - 1e-9 <= yt <= yr[1] + 1e-9:
            yy = int(round(mapy(yt)))
            cv.hline(L - 5, L, yy, BLACK)
            lab = fmt(yt)
            cv.text(L - 9 - cv.text_w(lab, 2), yy - 7, lab, BLACK, 2)

    # sarlavha va o'q nomlari
    if title:
        cv.text(L + (R - L) // 2 - cv.text_w(title, 2) // 2, T - 22,
                title, BLACK, 2)
    if xlabel:
        cv.text(L + (R - L) // 2 - cv.text_w(xlabel, 2) // 2, Bt + 26,
                xlabel, BLACK, 2)
    if ylabel:
        ylab_h = cv.text_w(ylabel, 2)
        cv.text_vertical(14, T + (Bt - T) // 2 + ylab_h // 2, ylabel, BLACK, 2)
    return mapx, mapy
