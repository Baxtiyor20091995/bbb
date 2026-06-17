# -*- coding: utf-8 -*-
"""
Генерация иллюстраций к Главе 1 (Технологическая часть).
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


def box(c, x0, y0, x1, y1, t1, t2=None, fill=(225, 232, 240), tcol=BLACK):
    c.rect(x0, y0, x1, y1, color=DARK, fill=fill, w=3)
    cx = (x0 + x1) // 2
    if t2:
        c.ctext(cx, (y0 + y1) // 2 - 16, t1, tcol, 2)
        c.ctext(cx, (y0 + y1) // 2 + 4, t2, GRAY, 2)
    else:
        c.ctext(cx, (y0 + y1) // 2 - 7, t1, tcol, 2)


# ==========================================================================
# Рис. 1.1 — Принципиальная технологическая схема ГМЗ-7 (блок-схема)
# ==========================================================================
def fig_flowsheet():
    c = Canvas(980, 520)
    bw, bh = 190, 70
    y1, y2, y3 = 60, 250, 430
    xs = [40, 290, 540, 790]
    box(c, xs[0], y1, xs[0]+bw, y1+bh, "ORE", "RUDA", fill=SAND)
    box(c, xs[1], y1, xs[1]+bw, y1+bh, "CRUSH", "DROBL")
    box(c, xs[2], y1, xs[2]+bw, y1+bh, "GRIND", "MShTs", fill=LBLUE)
    box(c, xs[3], y1, xs[3]+bw, y1+bh, "CLASS", "KLASS")
    for i in range(3):
        c.arrow(xs[i]+bw, y1+bh//2, xs[i+1], y1+bh//2, BLACK, 2)
    c.arrow(xs[3]+bw//2, y1+bh, xs[3]+bw//2, y2, BLACK, 2)
    box(c, xs[3], y2, xs[3]+bw, y2+bh, "THICK", "SGUSCH")
    box(c, xs[2], y2, xs[2]+bw, y2+bh, "LEACH", "VYSCHEL")
    box(c, xs[1], y2, xs[1]+bw, y2+bh, "CIP", "SORBCIYA")
    box(c, xs[0], y2, xs[0]+bw, y2+bh, "ELU-EW", "DESORB")
    for i in (3, 2, 1):
        c.arrow(xs[i], y2+bh//2, xs[i-1]+bw, y2+bh//2, BLACK, 2)
    c.arrow(xs[0]+bw//2, y2+bh, xs[0]+bw//2, y3, BLACK, 2)
    box(c, xs[0], y3, xs[0]+bw, y3+bh, "AU", "ZOLOTO", fill=(245, 226, 150))
    box(c, xs[2], y3, xs[2]+bw, y3+bh, "TAIL", "HVOSTY", fill=(225, 215, 205))
    c.arrow(xs[3]+bw//2, y2+bh, xs[2]+bw, y3+bh//2, RED, 2)
    c.save_png(p("fig_1_1_flowsheet.png"))


# ==========================================================================
# Рис. 1.2 — Замкнутый цикл измельчения (мельница + гидроциклон)
# ==========================================================================
def fig_circuit():
    c = Canvas(960, 480)
    c.arrow(40, 150, 180, 150, BLACK, 2)
    c.text(45, 120, "RUDA+VODA", BLACK, 2)
    box(c, 180, 110, 420, 200, "MShTs", "MILL", fill=LBLUE)
    c.arrow(300, 200, 300, 300, BLACK, 2)
    box(c, 200, 300, 400, 380, "PUMP", "ZUMPF")
    c.arrow(400, 340, 560, 340, BLACK, 2)
    cx0, cy0, cx1 = 560, 250, 700
    c.rect(cx0, cy0, cx1, cy0+60, color=DARK, fill=(225, 232, 240), w=3)
    c.line(cx0, cy0+60, (cx0+cx1)//2, cy0+170, DARK, 3)
    c.line(cx1, cy0+60, (cx0+cx1)//2, cy0+170, DARK, 3)
    c.ctext((cx0+cx1)//2, cy0+25, "CYCLON", BLACK, 2)
    c.arrow(540, 320, cx0, cy0+30, BLACK, 2)
    c.arrow(cx1, cy0+20, 860, cy0+20, GREEN, 2)
    c.text(740, cy0-15, "SLIV", GREEN, 2)
    c.text(720, cy0+35, "GOTOVYY", GRAY, 2)
    c.arrow((cx0+cx1)//2, cy0+170, (cx0+cx1)//2, 430, ORANGE, 2)
    c.line((cx0+cx1)//2, 430, 300, 430, ORANGE, 2)
    c.arrow(300, 430, 300, 200, ORANGE, 2)
    c.text(360, 440, "PESKI (VOZVRAT)", ORANGE, 2)
    c.save_png(p("fig_1_2_circuit.png"))


# ==========================================================================
# Рис. 1.3 — Общий вид мельницы МШЦ с приводом
# ==========================================================================
def fig_general():
    c = Canvas(980, 460)
    midy = 230
    c.rect(60, 360, 920, 410, color=DARK, fill=(220, 215, 205), w=2)
    c.rect(150, 250, 230, 360, color=DARK, fill=STEEL, w=2)
    c.rect(660, 250, 740, 360, color=DARK, fill=STEEL, w=2)
    c.rect(230, 150, 660, 320, color=DARK, fill=(232, 236, 240), w=3)
    c.ctext(445, 225, "BARABAN", GRAY, 2)
    c.rect(120, midy-25, 230, midy+25, color=DARK, fill=STEEL, w=2)
    c.rect(660, midy-25, 770, midy+25, color=DARK, fill=STEEL, w=2)
    c.circle(630, midy, 95, color=DARK, fill=None, w=3)
    for i in range(40):
        a = 2*math.pi*i/40
        x0 = 630 + 95*math.cos(a); y0 = midy + 95*math.sin(a)
        x1 = 630 + 105*math.cos(a); y1 = midy + 105*math.sin(a)
        c.line(x0, y0, x1, y1, DARK, 1)
    c.circle(770, 360, 28, color=DARK, fill=STEEL, w=2)
    box(c, 800, 320, 940, 400, "MOTOR", "DVIG.")
    c.line(798, 360, 880, 360, DARK, 3)

    def callout(x, y, num, tx, ty):
        c.line(x, y, tx, ty, BLACK, 1)
        c.circle(tx, ty, 12, color=BLACK, fill=WHITE, w=2)
        c.ctext(tx, ty-6, num, BLACK, 2)
    callout(445, 160, "1", 445, 60)
    callout(170, midy, "2", 150, 80)
    callout(700, midy, "3", 700, 80)
    callout(630, midy-95, "4", 560, 60)
    callout(770, 360, "5", 820, 285)
    callout(870, 360, "6", 905, 290)
    c.save_png(p("fig_1_3_general.png"))


# ==========================================================================
# Рис. 1.4 — Принцип центральной загрузки и разгрузки
# ==========================================================================
def fig_principle():
    c = Canvas(960, 420)
    midy = 210
    c.rect(250, 100, 710, 320, color=DARK, fill=(232, 236, 240), w=3)
    c.rect(160, midy-30, 250, midy+30, color=DARK, fill=STEEL, w=2)
    c.rect(710, midy-30, 800, midy+30, color=DARK, fill=STEEL, w=2)
    c.rect(265, midy+10, 695, 305, color=None, fill=LBLUE, w=1)
    random.seed(5)
    for _ in range(80):
        c.circle(random.randint(280, 680), random.randint(midy+20, 295),
                 random.randint(7, 12), color=STEEL, fill=(150, 165, 180), w=1)
    c.arrow(70, midy, 160, midy, BLUE, 3)
    c.text(60, midy-35, "PITANIE", BLUE, 2)
    c.text(70, midy+30, "RUDA+VODA", GRAY, 2)
    c.arrow(800, midy, 900, midy, GREEN, 3)
    c.text(805, midy-35, "RAZGRUZKA", GREEN, 2)
    c.text(820, midy+30, "PULPA", GRAY, 2)
    c.arrow(360, 150, 420, 150, BLACK, 2, head=7)
    c.arrow(540, 150, 600, 150, BLACK, 2, head=7)
    c.text(440, 120, "N", BLACK, 2)
    c.save_png(p("fig_1_4_principle.png"))


# ==========================================================================
# Рис. 1.5 — Схема процесса мокрого измельчения (потоки)
# ==========================================================================
def fig_wet():
    c = Canvas(960, 420)
    box(c, 360, 150, 600, 270, "MShTs", "MILL", fill=LBLUE)
    c.arrow(120, 110, 360, 180, BLACK, 2)
    c.text(120, 85, "RUDA Q", BLACK, 2)
    c.arrow(120, 230, 360, 210, BLUE, 2)
    c.text(120, 240, "VODA W", BLUE, 2)
    c.arrow(120, 330, 360, 250, BLACK, 2)
    c.text(120, 340, "SHARY G", BLACK, 2)
    c.arrow(600, 210, 860, 210, GREEN, 2)
    c.text(700, 175, "PULPA", GREEN, 2)
    c.text(640, 235, "NA KLASSIFIKACIYU", GRAY, 2)
    c.save_png(p("fig_1_5_wet.png"))


# ==========================================================================
# Рис. 1.6 — Гранулометрические характеристики (питание / продукт)
# ==========================================================================
def fig_grain():
    c = Canvas(840, 560)
    ox, oy = 110, 470
    ax, ay = 780, 90
    c.arrow(ox, oy, ax, oy, BLACK, 2)
    c.arrow(ox, oy, ox, ay, BLACK, 2)
    c.text(ax-160, oy+16, "RAZMER MM", BLACK, 2)
    c.text(ox-30, ay-10, "PROHOD PROC", BLACK, 2)
    decades = [(-2, "0.01"), (-1, "0.1"), (0, "1"), (1, "10"), (2, "100")]

    def xpix(log10v):
        return ox + (ax - ox - 20) * (log10v - (-2)) / 4.0
    for lv, lab in decades:
        x = xpix(lv)
        c.line(x, oy, x, oy+5, BLACK, 1)
        c.ctext(x, oy+12, lab, BLACK, 2)
    for pct in (0, 20, 40, 60, 80, 100):
        y = oy - (oy - ay - 10) * pct / 100.0
        c.line(ox-5, y, ox, y, BLACK, 1)
        c.text(ox-55, y-7, str(pct), BLACK, 2)
        c.line(ox, y, ax-10, y, LGRAY, 1)

    def curve(center_log, color):
        prev = None
        for i in range(0, 121):
            lv = -2 + 4*i/120.0
            val = 100.0/(1.0 + math.exp(-2.6*(lv - center_log)))
            x = xpix(lv)
            y = oy - (oy - ay - 10) * val/100.0
            if prev:
                c.line(prev[0], prev[1], x, y, color, 3)
            prev = (x, y)
    curve(math.log10(8.0), ORANGE)
    curve(math.log10(0.12), BLUE)
    c.text(ax-190, ay+40, "F-PITANIE", ORANGE, 2)
    c.text(ax-190, ay+66, "P-PRODUKT", BLUE, 2)
    c.save_png(p("fig_1_6_grain.png"))


# ==========================================================================
# Рис. 1.7 — Существующая (ручная/локальная) система управления
# ==========================================================================
def fig_manual():
    c = Canvas(960, 440)
    box(c, 360, 60, 600, 150, "MShTs", "MILL", fill=LBLUE)
    box(c, 120, 70, 280, 140, "PI", "MESTNYY")
    box(c, 680, 70, 840, 140, "FI", "MESTNYY")
    c.arrow(360, 105, 280, 105, BLACK, 2)
    c.arrow(680, 105, 600, 105, BLACK, 2)
    cxo = 480
    c.circle(cxo, 300, 26, color=DARK, fill=(245, 226, 150), w=2)
    c.line(cxo, 326, cxo, 380, DARK, 3)
    c.line(cxo, 345, cxo-30, 370, DARK, 3)
    c.line(cxo, 345, cxo+30, 370, DARK, 3)
    c.line(cxo, 380, cxo-22, 415, DARK, 3)
    c.line(cxo, 380, cxo+22, 415, DARK, 3)
    c.text(cxo-60, 250, "OPERATOR", BLACK, 2)
    c.arrow(200, 140, cxo-40, 290, GRAY, 2)
    c.arrow(760, 140, cxo+40, 290, GRAY, 2)
    box(c, 300, 330, 470, 400, "RUCH.", "VENTIL")
    c.arrow(cxo-20, 365, 470, 365, RED, 2)
    c.arrow(385, 330, 420, 150, BLACK, 2)
    c.text(250, 305, "RUCHNOE UPRAVLENIE", RED, 2)
    c.save_png(p("fig_1_7_manual.png"))


# ==========================================================================
# Рис. 1.8 — Технико-экономический эффект автоматизации (диаграмма)
# ==========================================================================
def fig_effect():
    c = Canvas(860, 540)
    ox, oy = 110, 450
    ax, ay = 800, 80
    c.arrow(ox, oy, ax, oy, BLACK, 2)
    c.arrow(ox, oy, ox, ay, BLACK, 2)
    c.text(ox-40, ay-10, "PROC", BLACK, 2)
    for pct in (0, 25, 50, 75, 100, 115):
        y = oy - (oy-ay-10)*pct/115.0
        c.line(ox-5, y, ox, y, BLACK, 1)
        c.text(ox-55, y-7, str(pct), BLACK, 2)
    groups = [("PROIZV", 100, 112), ("ENERGO", 100, 92), ("STABIL", 100, 135)]
    gw = (ax - ox - 60) / len(groups)
    bw = 48
    for gi, (lab, b, a) in enumerate(groups):
        gx = ox + 40 + gi*gw
        yb = oy - (oy-ay-10)*b/115.0
        ya = oy - (oy-ay-10)*a/115.0
        c.rect(gx, yb, gx+bw, oy, color=DARK, fill=LGRAY, w=2)
        c.rect(gx+bw+12, ya, gx+2*bw+12, oy, color=DARK, fill=GREEN, w=2)
        c.ctext(gx+bw+6, oy+12, lab, BLACK, 2)
    c.rect(560, 95, 590, 120, color=DARK, fill=LGRAY, w=2)
    c.text(600, 100, "DO", BLACK, 2)
    c.rect(560, 135, 590, 160, color=DARK, fill=GREEN, w=2)
    c.text(600, 140, "POSLE", BLACK, 2)
    c.save_png(p("fig_1_8_effect.png"))


if __name__ == "__main__":
    fig_flowsheet()
    fig_circuit()
    fig_general()
    fig_principle()
    fig_wet()
    fig_grain()
    fig_manual()
    fig_effect()
    print("Изображения Главы 1 созданы.")
    for f in sorted(os.listdir(OUT)):
        if f.startswith("fig_1_"):
            print("  ", f, os.path.getsize(os.path.join(OUT, f)), "bytes")
