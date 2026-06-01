# -*- coding: utf-8 -*-
"""
Генерация иллюстраций к Главе 2 (Расчётная часть).
Все подписи на русском языке добавляются в Word; на самих рисунках —
цифровые позиции (выноски), латинские теги КИПиА и числовые шкалы.
"""
import os
import math
from drawlib import (Canvas, BLACK, WHITE, GRAY, LGRAY, BLUE, LBLUE, STEEL,
                     ORANGE, GREEN, RED, DARK, SAND)

OUT = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(OUT, exist_ok=True)


def p(name):
    return os.path.join(OUT, name)


# ==========================================================================
# Рис. 2.1 — Продольный разрез шаровой мельницы МШЦ
# ==========================================================================
def fig_mill():
    c = Canvas(960, 460)
    cx0, cx1 = 200, 760           # барабан
    cy0, cy1 = 90, 360
    midy = (cy0 + cy1) // 2
    # цапфы (загрузочная слева, разгрузочная справа)
    c.rect(110, midy - 40, 210, midy + 40, color=DARK, fill=STEEL, w=2)
    c.rect(750, midy - 40, 850, midy + 40, color=DARK, fill=STEEL, w=2)
    # корпус барабана
    c.rect(cx0, cy0, cx1, cy1, color=DARK, fill=(232, 236, 240), w=3)
    # футеровка (броневые плиты) — двойная линия
    c.rect(cx0 + 14, cy0 + 14, cx1 - 14, cy1 - 14, color=GRAY, fill=None, w=2)
    # пульпа (уровень)
    pulp_top = midy + 35
    c.rect(cx0 + 15, pulp_top, cx1 - 15, cy1 - 15, color=None, fill=LBLUE, w=1)
    # шары
    import random
    random.seed(7)
    for _ in range(120):
        rr = random.randint(8, 15)
        rx = random.randint(cx0 + 30, cx1 - 30)
        ry = random.randint(pulp_top - 10, cy1 - 25)
        c.circle(rx, ry, rr, color=STEEL, fill=(150, 165, 180), w=1)
    # ось вращения
    c.line(90, midy, 870, midy, GRAY, 1)
    # стрелка вращения
    c.circle(480, midy, 0, color=None)
    c.arrow(560, 70, 600, 95, BLACK, 2, head=8)
    c.text(545, 45, "N", BLACK, 2)
    # выноски (позиции)
    def callout(x, y, num, tx, ty):
        c.line(x, y, tx, ty, BLACK, 1)
        c.circle(tx, ty, 12, color=BLACK, fill=WHITE, w=2)
        c.ctext(tx, ty - 6, num, BLACK, 2)
    callout(160, midy, "1", 150, 40)
    callout(cx0 + 60, cy0 + 8, "2", 300, 40)
    callout(cx0 + 20, midy + 5, "3", 250, 415)
    callout(480, cy1 - 40, "4", 480, 415)
    callout(800, midy, "5", 810, 40)
    callout(600, pulp_top + 30, "6", 640, 415)
    c.save_png(p("fig_2_1_mill.png"))


# ==========================================================================
# Рис. 2.2 — Режим движения шаровой загрузки (поперечное сечение)
# ==========================================================================
def fig_motion():
    c = Canvas(720, 600)
    cx, cy, R = 360, 280, 230
    c.circle(cx, cy, R, color=DARK, fill=(238, 240, 244), w=3)
    c.circle(cx, cy, R - 12, color=GRAY, fill=None, w=2)
    # центр
    c.dot(cx, cy, BLACK, 3)
    # шары: сегмент, поднятый под углом (водопадно-каскадный режим)
    import random
    random.seed(3)
    a_lift = math.radians(35)   # угол подъёма "пяты"
    for _ in range(260):
        a = random.uniform(math.pi/2 + 0.15, math.pi*1.5 + a_lift)
        rr = random.uniform(0, R - 35)
        # держим массу в нижне-боковом секторе
        x = cx + rr * math.cos(a)
        y = cy + rr * math.sin(a)
        if y > cy - R*0.2 or (x < cx and y > cy - R*0.55):
            c.circle(x, y, random.randint(7, 12), color=STEEL,
                     fill=(150, 165, 180), w=1)
    # траектория полёта одного шара (водопадный режим)
    pts = []
    for i in range(40):
        t = i / 39
        bx = cx - (R - 30) + t * (1.4 * R)
        by = cy - (R - 40) + (t * 2 - 1) ** 2 * (R - 30) - (R - 40)
        pts.append((bx, by))
    for i in range(len(pts) - 1):
        c.line(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1], ORANGE, 2)
    # стрелка вращения
    c.arrow(cx + 150, cy - 150, cx + 185, cy - 110, BLACK, 2, head=9)
    c.text(cx + 150, cy - 185, "N", BLACK, 2)
    # обозначение угла
    c.line(cx, cy, cx - (R-20)*math.cos(a_lift), cy + (R-20)*math.sin(a_lift), RED, 1)
    c.line(cx, cy, cx - (R-20), cy, RED, 1)
    c.text(cx - 120, cy + 30, "A", RED, 2)
    c.save_png(p("fig_2_2_motion.png"))


# ==========================================================================
# Рис. 2.3 — Зависимость мощности от относительной частоты вращения
# ==========================================================================
def fig_power_curve():
    c = Canvas(820, 560)
    ox, oy = 110, 470          # начало координат
    ax, ay = 760, 90           # концы осей
    c.arrow(ox, oy, ax, oy, BLACK, 2)      # X
    c.arrow(ox, oy, ox, ay, BLACK, 2)      # Y
    c.text(ax - 60, oy + 18, "PSI", BLACK, 2)
    c.text(ox - 30, ay - 8, "N", BLACK, 2)
    # сетка и метки X (psi = доля критической частоты 0..1)
    for k in range(0, 11, 2):
        x = ox + (ax - ox - 20) * k / 10.0
        c.line(x, oy, x, oy + 5, BLACK, 1)
        c.ctext(x, oy + 12, "0." + str(k) if k else "0", BLACK, 2)
    # кривая N(psi) ~ psi*(1-psi)^? с максимумом около 0.8 (упрощённо)
    def Nval(psi):
        return max(0.0, math.sin(math.pi * min(psi, 1.0) ** 0.9))
    prev = None
    for i in range(0, 101):
        psi = i / 100.0
        x = ox + (ax - ox - 20) * psi
        y = oy - (oy - ay - 10) * Nval(psi)
        if prev:
            c.line(prev[0], prev[1], x, y, BLUE, 3)
        prev = (x, y)
    # рабочая точка psi=0.75..0.78
    psw = 0.76
    xw = ox + (ax - ox - 20) * psw
    yw = oy - (oy - ay - 10) * Nval(psw)
    c.line(xw, oy, xw, yw, RED, 1)
    c.line(ox, yw, xw, yw, RED, 1)
    c.circle(xw, yw, 6, color=RED, fill=RED, w=1)
    c.text(xw + 8, yw - 24, "RAB", RED, 2)
    c.save_png(p("fig_2_3_power.png"))


# ==========================================================================
# Рис. 2.4 — Материальный баланс процесса измельчения (блок-схема)
# ==========================================================================
def fig_balance():
    c = Canvas(960, 420)
    # блок мельницы
    c.rect(360, 150, 600, 290, color=DARK, fill=(225, 232, 240), w=3)
    c.ctext(480, 195, "MShTs", BLACK, 3)
    c.ctext(480, 235, "MILL", GRAY, 2)
    # входы слева
    c.arrow(120, 120, 360, 180, BLACK, 2)
    c.text(130, 95, "RUDA", BLACK, 2)
    c.text(130, 118, "100 T/H", GRAY, 2)
    c.arrow(120, 250, 360, 230, BLACK, 2)
    c.text(130, 258, "VODA", BLACK, 2)
    c.text(130, 281, "67 T/H", GRAY, 2)
    c.arrow(120, 340, 360, 270, BLACK, 2)
    c.text(130, 348, "SHARY", BLACK, 2)
    # выход справа
    c.arrow(600, 220, 860, 220, BLACK, 2)
    c.text(700, 185, "SLIV", BLACK, 2)
    c.text(660, 240, "PULPA 167 T/H", GRAY, 2)
    c.save_png(p("fig_2_4_balance.png"))


# ==========================================================================
# Рис. 2.5 — Функциональная схема одноконтурной АСР
# ==========================================================================
def fig_loop():
    c = Canvas(980, 360)
    y = 150
    # сумматор
    sx, sy = 150, y
    c.circle(sx, sy, 26, color=BLACK, fill=WHITE, w=2)
    c.line(sx - 14, sy, sx + 14, sy, BLACK, 1)
    c.line(sx, sy - 14, sx, sy + 14, BLACK, 1)
    c.text(sx - 80, sy - 36, "SP", BLACK, 2)
    c.arrow(60, sy, sx - 26, sy, BLACK, 2)
    c.text(sx - 18, sy - 40, "+", BLACK, 2)
    c.text(sx - 40, sy + 28, "-", BLACK, 2)
    # регулятор
    def block(x0, y0, x1, y1, t1, t2=None):
        c.rect(x0, y0, x1, y1, color=DARK, fill=(225, 232, 240), w=3)
        c.ctext((x0+x1)//2, (y0+y1)//2 - (14 if t2 else 7), t1, BLACK, 3)
        if t2:
            c.ctext((x0+x1)//2, (y0+y1)//2 + 8, t2, GRAY, 2)
    c.arrow(sx + 26, sy, 290, sy, BLACK, 2)
    c.text(220, sy - 26, "E", BLACK, 2)
    block(290, y - 45, 440, y + 45, "PID")
    c.arrow(440, sy, 560, sy, BLACK, 2)
    c.text(480, sy - 26, "U", BLACK, 2)
    block(560, y - 45, 700, y + 45, "IM")          # исполнительный механизм
    c.arrow(700, sy, 820, sy, BLACK, 2)
    block(820, y - 45, 950, y + 45, "OB")          # объект (мельница)
    c.arrow(950, sy, 950, 300, BLACK, 2)
    c.line(950, 300, 470, 300, BLACK, 2)
    # датчик
    block(360, 270, 470, 330, "FT")
    c.arrow(360, 300, sx, 300, BLACK, 2)
    c.arrow(sx, 300, sx, sy + 26, BLACK, 2)
    c.text(150, 312, "PV", BLACK, 2)
    c.save_png(p("fig_2_5_loop.png"))


# ==========================================================================
# Рис. 2.6 — Структурная схема ПИД-регулятора
# ==========================================================================
def fig_pid():
    c = Canvas(900, 420)
    c.arrow(60, 210, 180, 210, BLACK, 2)
    c.text(70, 184, "E(T)", BLACK, 2)
    c.line(180, 210, 180, 90, BLACK, 2)
    c.line(180, 210, 180, 330, BLACK, 2)
    def blk(y0, t):
        c.rect(220, y0, 440, y0 + 60, color=DARK, fill=(225, 232, 240), w=3)
        c.ctext(330, y0 + 22, t, BLACK, 3)
    blk(60, "KP")
    blk(180, "KI / S")
    blk(300, "KD * S")
    for yy in (90, 210, 330):
        c.arrow(180, yy, 220, yy, BLACK, 2)
        c.arrow(440, yy, 560, yy, BLACK, 2)
    # сумматор
    c.circle(590, 210, 30, color=BLACK, fill=WHITE, w=2)
    c.text(575, 198, "S", BLACK, 3)
    for yy in (90, 330):
        c.line(560, yy, 560, 210, BLACK, 2)
    c.line(560, 90, 560, 90, BLACK, 1)
    c.arrow(620, 210, 760, 210, BLACK, 2)
    c.text(680, 184, "U(T)", BLACK, 2)
    c.save_png(p("fig_2_6_pid.png"))


# ==========================================================================
# Рис. 2.7 — Переходные характеристики (P, PI, PID)
# ==========================================================================
def fig_transient():
    c = Canvas(820, 540)
    ox, oy = 100, 450
    ax, ay = 760, 80
    c.arrow(ox, oy, ax, oy, BLACK, 2)
    c.arrow(ox, oy, ox, ay, BLACK, 2)
    c.text(ax - 40, oy + 16, "T", BLACK, 2)
    c.text(ox - 40, ay, "PV", BLACK, 2)
    # уставка
    sp_y = ay + 60
    c.line(ox, sp_y, ax - 10, sp_y, GRAY, 1)
    c.text(ax - 70, sp_y - 22, "SP", GRAY, 2)
    span = oy - sp_y

    def curve(color, zeta, wn, label, ly):
        prev = None
        for i in range(0, 200):
            t = i / 18.0
            if zeta < 1:
                wd = wn * math.sqrt(1 - zeta**2)
                val = 1 - math.exp(-zeta*wn*t) * (math.cos(wd*t) +
                        (zeta*wn/wd)*math.sin(wd*t))
            else:
                val = 1 - math.exp(-wn*t)*(1 + wn*t)
            x = ox + (ax - ox - 12) * (i / 199.0)
            y = oy - span * val
            if prev:
                c.line(prev[0], prev[1], x, y, color, 2)
            prev = (x, y)
        c.text(ax - 150, ly, label, color, 2)
    curve(GREEN, 1.2, 1.1, "PID", ay + 90)
    curve(BLUE, 0.5, 1.3, "PI", ay + 120)
    curve(ORANGE, 0.22, 1.6, "P", ay + 150)
    c.save_png(p("fig_2_7_transient.png"))


# ==========================================================================
# Рис. 2.8 — Размещение датчиков КИПиА на мельнице
# ==========================================================================
def fig_sensors():
    c = Canvas(980, 480)
    midy = 250
    # барабан
    c.rect(260, 150, 700, 350, color=DARK, fill=(232, 236, 240), w=3)
    c.rect(170, midy - 35, 260, midy + 35, color=DARK, fill=STEEL, w=2)
    c.rect(700, midy - 35, 790, midy + 35, color=DARK, fill=STEEL, w=2)
    c.rect(275, midy + 5, 685, 335, color=None, fill=LBLUE, w=1)
    import random
    random.seed(11)
    for _ in range(70):
        c.circle(random.randint(290, 670), random.randint(midy+15, 320),
                 random.randint(7, 12), color=STEEL, fill=(150,165,180), w=1)

    def sensor(x, y, tag, tx, ty):
        c.line(x, y, tx, ty, BLACK, 1)
        c.circle(tx, ty, 24, color=BLUE, fill=WHITE, w=2)
        c.ctext(tx, ty - 6, tag, BLUE, 2)

    sensor(120, midy, "WT", 90, 80)        # вес (загрузка)
    sensor(215, midy - 20, "FT", 215, 70)  # расход воды/руды на входе
    sensor(480, 160, "AT", 480, 70)        # анализатор/уровень шума
    sensor(745, midy - 10, "DT", 760, 70)  # плотность пульпы
    sensor(745, midy + 15, "TT", 870, 150) # температура подшипника
    sensor(745, midy + 25, "PT", 880, 360) # давление масла
    sensor(480, 345, "LT", 480, 440)       # уровень в зумпфе/мельнице
    c.save_png(p("fig_2_8_sensors.png"))


if __name__ == "__main__":
    fig_mill()
    fig_motion()
    fig_power_curve()
    fig_balance()
    fig_loop()
    fig_pid()
    fig_transient()
    fig_sensors()
    print("Изображения созданы в:", os.path.abspath(OUT))
    for f in sorted(os.listdir(OUT)):
        print("  ", f, os.path.getsize(os.path.join(OUT, f)), "bytes")
