# -*- coding: utf-8 -*-
"""
Pure-Python PNG generatsiya va chizish kutubxonasi.
Faqat standart kutubxonalar (zlib, struct) ishlatiladi.
Word fayl uchun ilmiy diagramma/grafiklarni yaratishda foydalaniladi.
"""
import zlib
import struct
import math

# ---------------------------------------------------------------------------
# 8x8 bitmap shrift (faqat kerakli belgilar). Har bir glif - 8 ta qator.
# '#' = yoqilgan piksel, ' ' = bo'sh.
# ---------------------------------------------------------------------------
_GLYPHS = {
    ' ': ["        "] * 8,
    'A': [
        "  ###   ",
        " #   #  ",
        "#     # ",
        "#     # ",
        "####### ",
        "#     # ",
        "#     # ",
        "        ",
    ],
    'B': [
        "######  ",
        "#     # ",
        "#     # ",
        "######  ",
        "#     # ",
        "#     # ",
        "######  ",
        "        ",
    ],
    'C': [
        " #####  ",
        "#     # ",
        "#       ",
        "#       ",
        "#       ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    'D': [
        "######  ",
        "#     # ",
        "#     # ",
        "#     # ",
        "#     # ",
        "#     # ",
        "######  ",
        "        ",
    ],
    'E': [
        "####### ",
        "#       ",
        "#       ",
        "#####   ",
        "#       ",
        "#       ",
        "####### ",
        "        ",
    ],
    'F': [
        "####### ",
        "#       ",
        "#       ",
        "#####   ",
        "#       ",
        "#       ",
        "#       ",
        "        ",
    ],
    'G': [
        " #####  ",
        "#     # ",
        "#       ",
        "#   ### ",
        "#     # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    'H': [
        "#     # ",
        "#     # ",
        "#     # ",
        "####### ",
        "#     # ",
        "#     # ",
        "#     # ",
        "        ",
    ],
    'I': [
        " #####  ",
        "   #    ",
        "   #    ",
        "   #    ",
        "   #    ",
        "   #    ",
        " #####  ",
        "        ",
    ],
    'J': [
        "  ##### ",
        "     #  ",
        "     #  ",
        "     #  ",
        "#    #  ",
        "#    #  ",
        " ####   ",
        "        ",
    ],
    'K': [
        "#     # ",
        "#    #  ",
        "#   #   ",
        "####    ",
        "#   #   ",
        "#    #  ",
        "#     # ",
        "        ",
    ],
    'L': [
        "#       ",
        "#       ",
        "#       ",
        "#       ",
        "#       ",
        "#       ",
        "####### ",
        "        ",
    ],
    'M': [
        "#     # ",
        "##   ## ",
        "# # # # ",
        "#  #  # ",
        "#     # ",
        "#     # ",
        "#     # ",
        "        ",
    ],
    'N': [
        "#     # ",
        "##    # ",
        "# #   # ",
        "#  #  # ",
        "#   # # ",
        "#    ## ",
        "#     # ",
        "        ",
    ],
    'O': [
        " #####  ",
        "#     # ",
        "#     # ",
        "#     # ",
        "#     # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    'P': [
        "######  ",
        "#     # ",
        "#     # ",
        "######  ",
        "#       ",
        "#       ",
        "#       ",
        "        ",
    ],
    'Q': [
        " #####  ",
        "#     # ",
        "#     # ",
        "#     # ",
        "#   # # ",
        "#    #  ",
        " #### # ",
        "        ",
    ],
    'R': [
        "######  ",
        "#     # ",
        "#     # ",
        "######  ",
        "#   #   ",
        "#    #  ",
        "#     # ",
        "        ",
    ],
    'S': [
        " #####  ",
        "#     # ",
        "#       ",
        " #####  ",
        "      # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    'T': [
        "####### ",
        "   #    ",
        "   #    ",
        "   #    ",
        "   #    ",
        "   #    ",
        "   #    ",
        "        ",
    ],
    'U': [
        "#     # ",
        "#     # ",
        "#     # ",
        "#     # ",
        "#     # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    'V': [
        "#     # ",
        "#     # ",
        "#     # ",
        "#     # ",
        " #   #  ",
        "  # #   ",
        "   #    ",
        "        ",
    ],
    'W': [
        "#     # ",
        "#     # ",
        "#     # ",
        "#  #  # ",
        "# # # # ",
        "##   ## ",
        "#     # ",
        "        ",
    ],
    'X': [
        "#     # ",
        " #   #  ",
        "  # #   ",
        "   #    ",
        "  # #   ",
        " #   #  ",
        "#     # ",
        "        ",
    ],
    'Y': [
        "#     # ",
        " #   #  ",
        "  # #   ",
        "   #    ",
        "   #    ",
        "   #    ",
        "   #    ",
        "        ",
    ],
    'Z': [
        "####### ",
        "     #  ",
        "    #   ",
        "   #    ",
        "  #     ",
        " #      ",
        "####### ",
        "        ",
    ],
    '0': [
        " #####  ",
        "#     # ",
        "#    ## ",
        "#   # # ",
        "#  #  # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    '1': [
        "   #    ",
        "  ##    ",
        " # #    ",
        "   #    ",
        "   #    ",
        "   #    ",
        " ###### ",
        "        ",
    ],
    '2': [
        " #####  ",
        "#     # ",
        "      # ",
        "    ##  ",
        "  ##    ",
        " #      ",
        "####### ",
        "        ",
    ],
    '3': [
        "####### ",
        "     #  ",
        "    #   ",
        "  ###   ",
        "      # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    '4': [
        "    ##  ",
        "   # #  ",
        "  #  #  ",
        " #   #  ",
        "####### ",
        "     #  ",
        "     #  ",
        "        ",
    ],
    '5': [
        "####### ",
        "#       ",
        "#       ",
        "######  ",
        "      # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    '6': [
        "  ####  ",
        " #      ",
        "#       ",
        "######  ",
        "#     # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    '7': [
        "####### ",
        "     #  ",
        "    #   ",
        "   #    ",
        "  #     ",
        "  #     ",
        "  #     ",
        "        ",
    ],
    '8': [
        " #####  ",
        "#     # ",
        "#     # ",
        " #####  ",
        "#     # ",
        "#     # ",
        " #####  ",
        "        ",
    ],
    '9': [
        " #####  ",
        "#     # ",
        "#     # ",
        " ###### ",
        "      # ",
        "     #  ",
        " ####   ",
        "        ",
    ],
    '.': [
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "  ##    ",
        "  ##    ",
        "        ",
    ],
    ',': [
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "  ##    ",
        "  ##    ",
        " #      ",
    ],
    '-': [
        "        ",
        "        ",
        "        ",
        " #####  ",
        "        ",
        "        ",
        "        ",
        "        ",
    ],
    '+': [
        "        ",
        "   #    ",
        "   #    ",
        " #####  ",
        "   #    ",
        "   #    ",
        "        ",
        "        ",
    ],
    '%': [
        "##    # ",
        "##   #  ",
        "    #   ",
        "   #    ",
        "  #     ",
        " #   ## ",
        "#    ## ",
        "        ",
    ],
    '(': [
        "    #   ",
        "   #    ",
        "  #     ",
        "  #     ",
        "  #     ",
        "   #    ",
        "    #   ",
        "        ",
    ],
    ')': [
        "  #     ",
        "   #    ",
        "    #   ",
        "    #   ",
        "    #   ",
        "   #    ",
        "  #     ",
        "        ",
    ],
    '/': [
        "      # ",
        "     #  ",
        "    #   ",
        "   #    ",
        "  #     ",
        " #      ",
        "#       ",
        "        ",
    ],
    ':': [
        "        ",
        "  ##    ",
        "  ##    ",
        "        ",
        "  ##    ",
        "  ##    ",
        "        ",
        "        ",
    ],
    '=': [
        "        ",
        "        ",
        " #####  ",
        "        ",
        " #####  ",
        "        ",
        "        ",
        "        ",
    ],
    '*': [
        "        ",
        "#  #  # ",
        " # # #  ",
        "  ###   ",
        " # # #  ",
        "#  #  # ",
        "        ",
        "        ",
    ],
    '_': [
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
        "####### ",
        "        ",
    ],
    "'": [
        "   #    ",
        "   #    ",
        "  #     ",
        "        ",
        "        ",
        "        ",
        "        ",
        "        ",
    ],
}


def _norm_char(ch):
    if ch in _GLYPHS:
        return ch
    up = ch.upper()
    if up in _GLYPHS:
        return up
    return '*'  # noma'lum belgi


class Canvas:
    """Oddiy RGB rastr; piksellar bo'yicha chizish va PNG saqlash."""

    def __init__(self, w, h, bg=(255, 255, 255)):
        self.w = w
        self.h = h
        self.px = [[bg for _ in range(w)] for _ in range(h)]

    # ---- asosiy piksel ----
    def set(self, x, y, c):
        xi = int(x)
        yi = int(y)
        if 0 <= xi < self.w and 0 <= yi < self.h:
            self.px[yi][xi] = c

    # ---- to'rtburchaklar ----
    def fill_rect(self, x0, y0, x1, y1, c):
        x0, x1 = sorted((int(x0), int(x1)))
        y0, y1 = sorted((int(y0), int(y1)))
        for y in range(max(0, y0), min(self.h, y1 + 1)):
            row = self.px[y]
            for x in range(max(0, x0), min(self.w, x1 + 1)):
                row[x] = c

    def rect(self, x0, y0, x1, y1, c, t=1):
        for i in range(t):
            self.line(x0, y0 + i, x1, y0 + i, c)
            self.line(x0, y1 - i, x1, y1 - i, c)
            self.line(x0 + i, y0, x0 + i, y1, c)
            self.line(x1 - i, y0, x1 - i, y1, c)

    def round_panel(self, x0, y0, x1, y1, fill, border=None, t=1):
        """Yumaloq burchakli emas, oddiy panel (fon + ramka)."""
        self.fill_rect(x0, y0, x1, y1, fill)
        if border:
            self.rect(x0, y0, x1, y1, border, t)

    # ---- chiziq (Bresenham + qalinlik) ----
    def line(self, x0, y0, x1, y1, c, t=1):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        half = t // 2
        while True:
            if t <= 1:
                self.set(x0, y0, c)
            else:
                for ax in range(-half, half + 1):
                    for ay in range(-half, half + 1):
                        self.set(x0 + ax, y0 + ay, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def dashed_line(self, x0, y0, x1, y1, c, dash=6, gap=4, t=1):
        dist = math.hypot(x1 - x0, y1 - y0)
        if dist == 0:
            return
        steps = int(dist)
        on = True
        cnt = 0
        for i in range(steps + 1):
            tt = i / dist
            x = x0 + (x1 - x0) * tt
            y = y0 + (y1 - y0) * tt
            if on:
                half = t // 2
                for ax in range(-half, half + 1):
                    for ay in range(-half, half + 1):
                        self.set(x + ax, y + ay, c)
            cnt += 1
            if on and cnt >= dash:
                on = False
                cnt = 0
            elif not on and cnt >= gap:
                on = True
                cnt = 0

    # ---- aylanalar ----
    def fill_circle(self, cx, cy, r, c):
        cx, cy, r = int(cx), int(cy), int(r)
        for y in range(-r, r + 1):
            for x in range(-r, r + 1):
                if x * x + y * y <= r * r:
                    self.set(cx + x, cy + y, c)

    def circle(self, cx, cy, r, c, t=1):
        cx, cy, r = int(cx), int(cy), int(r)
        for ang in range(0, 360, 1):
            a = math.radians(ang)
            for tt in range(t):
                self.set(cx + (r - tt) * math.cos(a), cy + (r - tt) * math.sin(a), c)

    def ellipse(self, cx, cy, rx, ry, c, fill=None, t=1):
        cx, cy, rx, ry = int(cx), int(cy), int(rx), int(ry)
        if fill is not None:
            for y in range(-ry, ry + 1):
                for x in range(-rx, rx + 1):
                    if (x * x) / (rx * rx + 0.0001) + (y * y) / (ry * ry + 0.0001) <= 1.0:
                        self.set(cx + x, cy + y, fill)
        for ang in range(0, 361):
            a = math.radians(ang)
            for tt in range(t):
                self.set(cx + (rx - tt) * math.cos(a), cy + (ry - tt) * math.sin(a), c)

    # ---- strelka ----
    def arrow(self, x0, y0, x1, y1, c, t=2, head=8):
        self.line(x0, y0, x1, y1, c, t)
        ang = math.atan2(y1 - y0, x1 - x0)
        for da in (math.radians(150), math.radians(-150)):
            hx = x1 + head * math.cos(ang + da)
            hy = y1 + head * math.sin(ang + da)
            self.line(x1, y1, hx, hy, c, t)

    # ---- matn ----
    def char(self, x, y, ch, c, scale=2):
        glyph = _GLYPHS[_norm_char(ch)]
        for ry, row in enumerate(glyph):
            for rx, p in enumerate(row):
                if p != ' ':
                    self.fill_rect(
                        x + rx * scale, y + ry * scale,
                        x + rx * scale + scale - 1, y + ry * scale + scale - 1, c
                    )

    def text(self, x, y, s, c=(0, 0, 0), scale=2, spacing=1):
        cw = (8 + spacing) * scale
        cx = x
        for ch in s:
            self.char(cx, y, ch, c, scale)
            cx += cw

    def text_w(self, s, scale=2, spacing=1):
        return len(s) * (8 + spacing) * scale

    def text_center(self, cx, y, s, c=(0, 0, 0), scale=2, spacing=1):
        w = self.text_w(s, scale, spacing)
        self.text(cx - w // 2, y, s, c, scale, spacing)

    # ---- PNG saqlash ----
    def save_png(self, path):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)  # filter type 0
            row = self.px[y]
            for x in range(self.w):
                r, g, b = row[x]
                raw.append(r & 255)
                raw.append(g & 255)
                raw.append(b & 255)
        compressed = zlib.compress(bytes(raw), 9)

        def chunk(typ, data):
            payload = typ + data
            return (struct.pack(">I", len(data)) + payload +
                    struct.pack(">I", zlib.crc32(payload) & 0xffffffff))

        out = b'\x89PNG\r\n\x1a\n'
        out += chunk(b'IHDR', struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0))
        out += chunk(b'IDAT', compressed)
        out += chunk(b'IEND', b'')
        with open(path, 'wb') as f:
            f.write(out)


# ---------------------------------------------------------------------------
# Ranglar palitrasi (dissertatsiya uchun yumshoq, professional ohang)
# ---------------------------------------------------------------------------
COL = {
    'bg': (255, 255, 255),
    'ink': (30, 40, 55),
    'gray': (120, 130, 145),
    'lgray': (225, 230, 236),
    'blue': (41, 98, 168),
    'lblue': (210, 226, 246),
    'green': (46, 139, 87),
    'lgreen': (210, 238, 220),
    'teal': (32, 150, 160),
    'lteal': (205, 236, 238),
    'orange': (224, 138, 40),
    'lorange': (250, 228, 200),
    'red': (200, 60, 60),
    'lred': (250, 215, 215),
    'purple': (120, 80, 170),
    'lpurple': (228, 218, 244),
    'yellow': (235, 195, 60),
    'lyellow': (250, 240, 200),
    'dark': (55, 65, 80),
}


def box(cv, x0, y0, x1, y1, text, fill, border, tcol=None, scale=2, t=2, lines=None):
    """Markazida matnli to'rtburchak blok. lines berilsa, ko'p qatorli."""
    cv.round_panel(x0, y0, x1, y1, fill, border, t)
    tcol = tcol or COL['ink']
    cx = (x0 + x1) // 2
    if lines is None:
        lines = [text] if text else []
    total_h = len(lines) * (8 * scale + 4) - 4
    cy = (y0 + y1) // 2 - total_h // 2
    for ln in lines:
        cv.text_center(cx, cy, ln, tcol, scale)
        cy += 8 * scale + 4


def title_block(cv, title, scale=3):
    """Yuqori sarlavha chizig'i."""
    cv.text_center(cv.w // 2, 14, title, COL['ink'], scale)
    cv.line(40, 14 + 8 * scale + 8, cv.w - 40, 14 + 8 * scale + 8, COL['blue'], 2)
