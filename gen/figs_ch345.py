# -*- coding: utf-8 -*-
"""
Генерация иллюстраций к Главам 3, 4, 5.
Подписи на русском языке выносятся в Word; на рисунках — латинские теги,
цифровые позиции и числовые шкалы (ограничение растрового шрифта 5x7).
"""
import os
import math
import random
from drawlib import (Canvas, BLACK, WHITE, GRAY, LGRAY, BLUE, LBLUE, STEEL,
                     ORANGE, GREEN, RED, DARK, SAND)

OUT = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(OUT, exist_ok=True)


def p(name):
    return os.path.join(OUT, name)


def box(c, x0, y0, x1, y1, t1, t2=None, fill=(225, 232, 240), tcol=BLACK, w=3):
    c.rect(x0, y0, x1, y1, color=DARK, fill=fill, w=w)
    cx = (x0 + x1) // 2
    if t2:
        c.ctext(cx, (y0 + y1) // 2 - 16, t1, tcol, 2)
        c.ctext(cx, (y0 + y1) // 2 + 4, t2, GRAY, 2)
    else:
        c.ctext(cx, (y0 + y1) // 2 - 7, t1, tcol, 2)


def diamond(c, cx, cy, w, h, t1, fill=(245, 226, 150)):
    pts = [(cx, cy - h // 2), (cx + w // 2, cy), (cx, cy + h // 2), (cx - w // 2, cy)]
    if fill:
        for yy in range(cy - h // 2, cy + h // 2 + 1):
            t = 1 - abs(yy - cy) / (h / 2)
            half = int(w / 2 * t)
            for xx in range(cx - half, cx + half + 1):
                c.set(xx, yy, fill)
    for i in range(4):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % 4]
        c.line(x0, y0, x1, y1, DARK, 3)
    c.ctext(cx, cy - 7, t1, BLACK, 2)


def instr(c, cx, cy, tag, r=26):
    c.circle(cx, cy, r, color=BLUE, fill=WHITE, w=2)
    c.line(cx - r, cy, cx + r, cy, BLUE, 1)
    c.ctext(cx, cy - 18, tag, BLUE, 2)


# ==========================================================================
# ГЛАВА 3
# ==========================================================================
def fig_3_1_object():
    c = Canvas(960, 460)
    box(c, 360, 160, 620, 320, "MShTs", "OBJECT", fill=LBLUE)
    c.arrow(120, 210, 360, 210, GREEN, 2)
    c.text(120, 182, "QR-RUDA", GREEN, 2)
    c.arrow(120, 280, 360, 280, GREEN, 2)
    c.text(120, 252, "QW-VODA", GREEN, 2)
    c.arrow(430, 60, 430, 160, RED, 2)
    c.text(360, 35, "TVERDOST", RED, 2)
    c.arrow(560, 60, 560, 160, RED, 2)
    c.text(500, 35, "KRUPNOST", RED, 2)
    c.arrow(620, 200, 860, 200, BLUE, 2)
    c.text(700, 172, "PLOTNOST", BLUE, 2)
    c.arrow(620, 245, 860, 245, BLUE, 2)
    c.text(700, 248, "KRUPNOST P", BLUE, 2)
    c.arrow(620, 290, 860, 290, BLUE, 2)
    c.text(700, 293, "ZAGRUZKA", BLUE, 2)
    c.save_png(p("fig_3_1_object.png"))


def fig_3_2_fsa():
    c = Canvas(980, 540)
    midy = 380
    c.rect(300, 320, 700, 460, color=DARK, fill=(232, 236, 240), w=3)
    c.rect(220, midy - 28, 300, midy + 28, color=DARK, fill=STEEL, w=2)
    c.rect(700, midy - 28, 780, midy + 28, color=DARK, fill=STEEL, w=2)
    c.line(60, 150, 920, 150, GRAY, 2)
    c.text(70, 120, "SHCHIT / PLC", GRAY, 2)
    points = [(250, "FT"), (360, "WT"), (500, "AT"), (640, "DT"), (760, "TT")]
    for x, low in points:
        c.line(x, 320 if 300 < x < 700 else midy, x, 220, GRAY, 1)
        instr(c, x, 195, low)
        instr(c, x, 100, low[0] + "C")
        c.line(x, 169, x, 124, GRAY, 1)
    box(c, 120, 240, 210, 300, "FV", fill=(225, 232, 240))
    c.arrow(165, 240, 165, 124, GREEN, 1)
    c.text(120, 312, "VODA", GREEN, 2)
    c.save_png(p("fig_3_2_fsa.png"))


def fig_3_3_asutp():
    c = Canvas(900, 560)
    box(c, 250, 40, 650, 140, "SCADA / APM", "VERHNIY UROVEN", fill=(245, 226, 150))
    box(c, 250, 230, 650, 330, "PLC", "SREDNIY UROVEN", fill=LBLUE)
    box(c, 80, 440, 300, 520, "DATCHIKI", "FT DT WT")
    box(c, 360, 440, 540, 520, "IM/KLAPAN", "MEO")
    box(c, 600, 440, 820, 520, "PRIVOD", "DVIGATEL")
    c.arrow(450, 140, 450, 230, BLACK, 2)
    c.text(460, 175, "ETHERNET", GRAY, 2)
    for bx in (190, 450, 710):
        c.arrow(450, 330, bx, 440, BLACK, 2)
    c.text(300, 385, "FIELDBUS / 4-20 MA", GRAY, 2)
    c.save_png(p("fig_3_3_asutp.png"))


def fig_3_4_plc():
    c = Canvas(980, 360)
    mods = [("PS", "220V"), ("CPU", "PROC"), ("AI", "4-20"),
            ("AO", "4-20"), ("DI", "DISCR"), ("DO", "RELE"), ("COM", "NET")]
    x = 60
    w = 120
    for t1, t2 in mods:
        fill = LBLUE if t1 == "CPU" else (225, 232, 240)
        box(c, x, 110, x + w, 250, t1, t2, fill=fill)
        x += w + 10
    c.rect(60, 95, x - 10, 110, color=DARK, fill=LGRAY, w=1)
    c.arrow(180, 300, 300, 252, GREEN, 2)
    c.text(120, 305, "VHOD 4-20 MA", GREEN, 2)
    c.arrow(560, 252, 680, 300, ORANGE, 2)
    c.text(600, 305, "VYHOD", ORANGE, 2)
    c.save_png(p("fig_3_4_plc.png"))


def fig_3_5_electrical():
    c = Canvas(960, 460)
    c.line(120, 60, 860, 60, DARK, 3)
    c.text(120, 30, "6 KV", DARK, 2)
    c.line(300, 60, 300, 110, DARK, 2)
    box(c, 270, 110, 330, 160, "QF", fill=(225, 232, 240))
    c.line(300, 160, 300, 210, DARK, 2)
    box(c, 250, 210, 350, 260, "TR", "6/0.4")
    c.line(300, 260, 300, 320, DARK, 2)
    c.circle(300, 360, 40, color=DARK, fill=(245, 226, 150), w=3)
    c.ctext(300, 352, "M", BLACK, 3)
    c.text(250, 410, "DVIGATEL", GRAY, 2)
    c.line(560, 60, 560, 110, DARK, 2)
    box(c, 520, 110, 600, 160, "QF2", fill=(225, 232, 240))
    c.line(560, 160, 560, 200, DARK, 2)
    box(c, 480, 200, 640, 270, "PLC", fill=LBLUE)
    c.arrow(640, 235, 760, 235, BLACK, 2)
    box(c, 760, 200, 860, 270, "KM", "PUSK")
    c.line(810, 270, 810, 320, DARK, 2)
    c.arrow(810, 320, 340, 350, ORANGE, 1)
    c.text(560, 300, "UPRAVLENIE", GRAY, 2)
    c.save_png(p("fig_3_5_electrical.png"))


def fig_3_6_algorithm():
    c = Canvas(720, 720)
    cx = 360
    box(c, cx - 90, 30, cx + 90, 90, "START", fill=GREEN)
    c.arrow(cx, 90, cx, 130, BLACK, 2)
    box(c, cx - 130, 130, cx + 130, 195, "IZMER PV (DT)")
    c.arrow(cx, 195, cx, 235, BLACK, 2)
    box(c, cx - 130, 235, cx + 130, 300, "E = SP - PV")
    c.arrow(cx, 300, cx, 345, BLACK, 2)
    diamond(c, cx, 405, 230, 130, "E > 0 ?")
    c.arrow(cx + 115, 405, cx + 230, 405, BLACK, 2)
    c.text(cx + 130, 378, "DA", GREEN, 2)
    box(c, cx + 230, 372, cx + 360, 438, "+ VODA")
    c.arrow(cx - 115, 405, cx - 230, 405, BLACK, 2)
    c.text(cx - 200, 378, "NET", RED, 2)
    box(c, cx - 360, 372, cx - 230, 438, "- VODA")
    c.arrow(cx + 295, 438, cx + 295, 520, BLACK, 2)
    c.arrow(cx - 295, 438, cx - 295, 520, BLACK, 2)
    c.line(cx - 295, 520, cx + 295, 520, BLACK, 2)
    c.arrow(cx, 520, cx, 560, BLACK, 2)
    diamond(c, cx, 615, 230, 110, "PREDEL ?")
    c.text(cx + 130, 600, "ALARM", RED, 2)
    c.arrow(cx + 115, 615, cx + 250, 615, RED, 2)
    c.line(cx - 295, 520, cx - 330, 520, BLACK, 2)
    c.line(cx - 330, 520, cx - 330, 162, BLACK, 2)
    c.arrow(cx - 330, 162, cx - 130, 162, BLACK, 2)
    c.save_png(p("fig_3_6_algorithm.png"))


def fig_3_7_hmi():
    c = Canvas(960, 560)
    c.rect(40, 40, 920, 520, color=DARK, fill=(245, 247, 250), w=3)
    c.rect(40, 40, 920, 90, color=DARK, fill=(70, 95, 130), w=2)
    c.text(60, 55, "ARM OPERATORA - MShTs", WHITE, 2)
    c.rect(120, 170, 460, 300, color=DARK, fill=(232, 236, 240), w=3)
    c.rect(80, 205, 120, 265, color=DARK, fill=STEEL, w=2)
    c.rect(460, 205, 500, 265, color=DARK, fill=STEEL, w=2)
    c.ctext(290, 225, "MILL", GRAY, 2)
    vals = [("PLOTNOST", "1560"), ("RUDA T/H", "92"), ("VODA M3/H", "71"),
            ("MOSCH KW", "1180")]
    yy = 130
    for lab, v in vals:
        box(c, 560, yy, 760, yy + 60, v, lab, fill=WHITE)
        yy += 80
    c.rect(120, 340, 760, 470, color=DARK, fill=WHITE, w=2)
    c.text(130, 318, "TREND", GRAY, 2)
    prev = None
    random.seed(2)
    yv = 405
    for i in range(0, 64):
        x = 130 + i * 9.8
        yv += random.randint(-8, 8)
        yv = max(355, min(455, yv))
        if prev:
            c.line(prev[0], prev[1], x, yv, GREEN, 2)
        prev = (x, yv)
    c.rect(120, 485, 760, 510, color=DARK, fill=(245, 226, 150), w=1)
    c.text(130, 490, "NORMA: PARAMETRY V PREDELAH", BLACK, 2)
    c.save_png(p("fig_3_7_hmi.png"))


def fig_3_8_loops():
    c = Canvas(980, 480)
    box(c, 60, 60, 220, 130, "DC", "PLOTNOST", fill=LBLUE)
    c.arrow(220, 95, 360, 95, BLACK, 2)
    box(c, 360, 60, 520, 130, "FV", "VODA")
    c.arrow(520, 95, 700, 95, BLACK, 2)
    box(c, 700, 60, 900, 200, "MShTs", "OBJECT", fill=(232, 236, 240))
    c.line(800, 200, 800, 250, BLACK, 2)
    c.line(800, 250, 140, 250, BLACK, 2)
    c.arrow(140, 250, 140, 130, BLACK, 2)
    box(c, 60, 300, 220, 370, "WC", "ZAGRUZKA", fill=LBLUE)
    c.arrow(220, 335, 360, 335, BLACK, 2)
    box(c, 360, 300, 520, 370, "PITATEL", "ChRP")
    c.arrow(520, 335, 700, 200, BLACK, 2)
    box(c, 560, 300, 760, 440, "ZASCHITA", "BLOKIROVKA", fill=(245, 200, 200))
    c.arrow(800, 200, 760, 360, RED, 2)
    c.text(560, 455, "TT PT - AVARIYA -> STOP", RED, 2)
    c.save_png(p("fig_3_8_loops.png"))


# ==========================================================================
# ГЛАВА 4
# ==========================================================================
def fig_4_1_factors():
    c = Canvas(980, 320)
    box(c, 360, 30, 620, 100, "FAKTORY", "OVPF", fill=(245, 226, 150))
    groups = [("FIZICH", "SHUM VIBR", 70), ("HIMICH", "CIANIDY", 310),
              ("PYL", "AEROZOL", 550), ("ELEKTRO", "TOK", 790)]
    for t1, t2, x in groups:
        c.arrow(490, 100, x + 75, 200, BLACK, 2)
        box(c, x, 200, x + 150, 290, t1, t2)
    c.save_png(p("fig_4_1_factors.png"))


def fig_4_3_grounding():
    c = Canvas(960, 460)
    c.circle(150, 130, 40, color=DARK, fill=WHITE, w=2)
    c.ctext(150, 122, "TR", BLACK, 2)
    c.line(150, 170, 150, 380, DARK, 3)
    c.line(60, 380, 900, 380, DARK, 3)
    for gx in range(80, 900, 40):
        c.line(gx, 380, gx - 12, 400, DARK, 1)
    box(c, 600, 120, 760, 240, "EO", "KORPUS", fill=(232, 236, 240))
    c.line(680, 240, 680, 380, GREEN, 3)
    c.text(690, 290, "PE", GREEN, 2)
    c.line(150, 130, 600, 130, RED, 2)
    c.text(330, 100, "FAZA L", RED, 2)
    c.line(600, 160, 600, 130, RED, 2)
    c.text(770, 170, "ZAMYKANIE", GRAY, 2)
    c.save_png(p("fig_4_3_grounding.png"))


def fig_4_4_noise():
    c = Canvas(860, 520)
    ox, oy = 110, 430
    ax, ay = 800, 70
    c.arrow(ox, oy, ax, oy, BLACK, 2)
    c.arrow(ox, oy, ox, ay, BLACK, 2)
    c.text(ox - 50, ay - 10, "DBA", BLACK, 2)
    for v in (0, 40, 60, 80, 100, 120):
        y = oy - (oy - ay - 10) * v / 120.0
        c.line(ox - 5, y, ox, y, BLACK, 1)
        c.text(ox - 55, y - 7, str(v), BLACK, 2)
        c.line(ox, y, ax - 10, y, LGRAY, 1)
    yn = oy - (oy - ay - 10) * 80 / 120.0
    c.line(ox, yn, ax - 10, yn, RED, 2)
    c.text(ax - 130, yn - 24, "PDU 80", RED, 2)
    bars = [("MELNICA", 95), ("NASOS", 82), ("OPER", 60), ("KABINA", 50)]
    gw = (ax - ox - 60) / len(bars)
    for i, (lab, v) in enumerate(bars):
        gx = ox + 40 + i * gw
        y = oy - (oy - ay - 10) * v / 120.0
        col = RED if v > 80 else GREEN
        c.rect(gx, y, gx + 60, oy, color=DARK, fill=col, w=2)
        c.ctext(gx + 30, oy + 12, lab, BLACK, 2)
    c.save_png(p("fig_4_4_noise.png"))


def fig_4_5_fire():
    c = Canvas(720, 560)
    cx, cy, R = 360, 330, 230
    pts = [(cx, cy - R), (cx + int(R * 0.87), cy + R // 2),
           (cx - int(R * 0.87), cy + R // 2)]
    for i in range(3):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % 3]
        c.line(x0, y0, x1, y1, RED, 4)
    c.ctext(cx, 50, "TREUGOLNIK GORENIYA", BLACK, 2)
    c.text(cx - 60, cy - R - 30, "TOPLIVO", BLACK, 2)
    c.text(cx + 95, cy + R // 2 + 12, "OKISLITEL", BLACK, 2)
    c.text(cx - 255, cy + R // 2 + 12, "ISTOCHNIK", BLACK, 2)
    c.ctext(cx, cy, "OGON", RED, 3)
    c.save_png(p("fig_4_5_fire.png"))


def fig_4_7_groundcontour():
    c = Canvas(960, 420)
    gy = 150
    c.line(120, gy, 840, gy, DARK, 3)
    c.text(120, gy - 30, "GORIZONT ZAZEMLITEL", GRAY, 2)
    n = 6
    for i in range(n):
        x = 160 + i * 120
        c.line(x, gy, x, gy + 200, STEEL, 4)
        c.line(x, gy + 200, x - 8, gy + 180, STEEL, 2)
        c.line(x, gy + 200, x + 8, gy + 180, STEEL, 2)
    c.line(160, gy + 230, 280, gy + 230, BLUE, 1)
    c.text(200, gy + 235, "A", BLUE, 2)
    c.line(160, gy, 160, gy - 60, BLUE, 1)
    c.text(120, gy - 90, "L=3M", BLUE, 2)
    c.line(80, gy + 20, 880, gy + 20, GREEN, 1)
    for gx in range(90, 880, 30):
        c.line(gx, gy + 20, gx - 8, gy + 32, GREEN, 1)
    c.text(820, gy - 5, "PE", DARK, 2)
    c.save_png(p("fig_4_7_groundcontour.png"))


# ==========================================================================
# ГЛАВА 5
# ==========================================================================
def _bars(c, title_tags, values, colors, ymax, unit_tag):
    ox, oy = 120, 430
    ax, ay = 820, 70
    c.arrow(ox, oy, ax, oy, BLACK, 2)
    c.arrow(ox, oy, ox, ay, BLACK, 2)
    c.text(ox - 60, ay - 10, unit_tag, BLACK, 2)
    steps = 5
    for s in range(steps + 1):
        v = ymax * s / steps
        y = oy - (oy - ay - 10) * s / steps
        c.line(ox - 5, y, ox, y, BLACK, 1)
        c.text(ox - 75, y - 7, str(int(v)), BLACK, 2)
        c.line(ox, y, ax - 10, y, LGRAY, 1)
    gw = (ax - ox - 60) / len(values)
    for i, (lab, v) in enumerate(zip(title_tags, values)):
        gx = ox + 40 + i * gw
        y = oy - (oy - ay - 10) * v / ymax
        col = colors[i % len(colors)]
        c.rect(gx, y, gx + 70, oy, color=DARK, fill=col, w=2)
        c.ctext(gx + 35, oy + 12, lab, BLACK, 2)
        c.ctext(gx + 35, y - 22, str(v), BLACK, 2)


def fig_5_1_capital():
    c = Canvas(900, 500)
    _bars(c, ["PLC", "DATCHIKI", "SCADA", "MONTAZH", "PNR"],
          [120, 180, 90, 110, 60], [BLUE, GREEN, ORANGE, STEEL, SAND],
          200, "TYS USD")
    c.save_png(p("fig_5_1_capital.png"))


def fig_5_2_opex():
    c = Canvas(900, 500)
    _bars(c, ["ENERGO", "REMONT", "ZP", "AMORT", "PROCH"],
          [60, 35, 45, 40, 20], [ORANGE, STEEL, BLUE, GREEN, SAND],
          80, "TYS USD G")
    c.save_png(p("fig_5_2_opex.png"))


def fig_5_3_savings():
    c = Canvas(900, 500)
    _bars(c, ["ENERGO", "PROIZV", "POTERI"],
          [85, 140, 75], [GREEN, BLUE, ORANGE], 160, "TYS USD G")
    c.save_png(p("fig_5_3_savings.png"))


def fig_5_4_payback():
    c = Canvas(880, 520)
    ox, oy = 130, 300
    ax, ay = 820, 60
    aybot = 470
    c.arrow(ox, oy, ax, oy, BLACK, 2)
    c.line(ox, ay, ox, aybot, BLACK, 2)
    c.text(ax - 60, oy - 26, "GOD", BLACK, 2)
    c.text(ox - 90, ay, "USD", BLACK, 2)
    flow = [-560, -260, 40, 340, 640, 940]

    def ypix(v):
        return oy - v / 1000.0 * (oy - ay)
    prev = None
    for i, v in enumerate(flow):
        x = ox + 40 + i * 120
        y = ypix(v)
        c.line(x, oy, x, oy + 6, BLACK, 1)
        c.ctext(x, oy + 12, str(i), BLACK, 2)
        c.circle(x, y, 5, color=RED, fill=RED, w=1)
        if prev:
            c.line(prev[0], prev[1], x, y, BLUE, 3)
        prev = (x, y)
    c.text(ox + 150, oy - 40, "OKUP ~ 1.9 G", GREEN, 2)
    c.save_png(p("fig_5_4_payback.png"))


def fig_5_5_tep():
    c = Canvas(920, 520)
    ox, oy = 130, 430
    ax, ay = 860, 70
    c.arrow(ox, oy, ax, oy, BLACK, 2)
    c.arrow(ox, oy, ox, ay, BLACK, 2)
    c.text(ox - 60, ay - 10, "PROC", BLACK, 2)
    for v in (0, 25, 50, 75, 100, 140):
        y = oy - (oy - ay - 10) * v / 140.0
        c.line(ox - 5, y, ox, y, BLACK, 1)
        c.text(ox - 75, y - 7, str(v), BLACK, 2)
        c.line(ox, y, ax - 10, y, LGRAY, 1)
    groups = [("PROIZV", 100, 112), ("ENERGO", 100, 91),
              ("SEBEST", 100, 88), ("IZVLECH", 100, 103)]
    gw = (ax - ox - 60) / len(groups)
    bw = 42
    for gi, (lab, b, a) in enumerate(groups):
        gx = ox + 30 + gi * gw
        yb = oy - (oy - ay - 10) * b / 140.0
        ya = oy - (oy - ay - 10) * a / 140.0
        c.rect(gx, yb, gx + bw, oy, color=DARK, fill=LGRAY, w=2)
        c.rect(gx + bw + 10, ya, gx + 2 * bw + 10, oy, color=DARK, fill=GREEN, w=2)
        c.ctext(gx + bw + 5, oy + 12, lab, BLACK, 2)
    c.rect(620, 90, 650, 115, color=DARK, fill=LGRAY, w=2)
    c.text(660, 95, "DO", BLACK, 2)
    c.rect(620, 130, 650, 155, color=DARK, fill=GREEN, w=2)
    c.text(660, 135, "POSLE", BLACK, 2)
    c.save_png(p("fig_5_5_tep.png"))


if __name__ == "__main__":
    funcs = [
        fig_3_1_object, fig_3_2_fsa, fig_3_3_asutp, fig_3_4_plc,
        fig_3_5_electrical, fig_3_6_algorithm, fig_3_7_hmi, fig_3_8_loops,
        fig_4_1_factors, fig_4_3_grounding, fig_4_4_noise, fig_4_5_fire,
        fig_4_7_groundcontour,
        fig_5_1_capital, fig_5_2_opex, fig_5_3_savings, fig_5_4_payback,
        fig_5_5_tep,
    ]
    for f in funcs:
        f()
    print("Создано изображений:", len(funcs))
    for fn in sorted(os.listdir(OUT)):
        if fn.startswith("fig_") and fn[4] in "345":
            print("  ", fn, os.path.getsize(os.path.join(OUT, fn)), "bytes")
