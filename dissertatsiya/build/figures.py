# -*- coding: utf-8 -*-
"""
Dissertatsiya uchun barcha ilmiy diagramma/grafiklarni generatsiya qiladi.
Natija: dissertatsiya/rasmlar/*.png
"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from draw import Canvas, COL, box  # noqa: E402

OUT = os.path.normpath(os.path.join(HERE, '..', 'rasmlar'))
os.makedirs(OUT, exist_ok=True)


# ===========================================================================
#  YORDAMCHI GRAFIK FUNKSIYALAR
# ===========================================================================
def _axes(cv, ox, oy, w, h, title=None):
    if title:
        cv.text_center(ox + w // 2, 12, title, COL['ink'], 3)
    # o'qlar
    cv.line(ox, oy, ox, oy - h, COL['dark'], 2)        # Y
    cv.line(ox, oy, ox + w, oy, COL['dark'], 2)        # X


def bar_chart(cv, ox, oy, w, h, data, ymax, ytitle="", title=None, value_suffix=""):
    """data: [(label, value, color)]. Vertikal ustunli diagramma."""
    _axes(cv, ox, oy, w, h, title)
    # y to'r va belgilar
    steps = 5
    for s in range(steps + 1):
        val = ymax * s / steps
        yy = oy - h * s / steps
        cv.dashed_line(ox, yy, ox + w, yy, COL['lgray'], 5, 5, 1)
        lbl = ("%g" % round(val, 1))
        cv.text(ox - cv.text_w(lbl, 1) - 8, yy - 6, lbl, COL['gray'], 1)
    if ytitle:
        cv.text(ox - 30, oy - h - 26, ytitle, COL['gray'], 1)
    # ustunlar
    n = len(data)
    gap = w / (n * 2 + 1)
    bw = gap
    for i, (label, val, col) in enumerate(data):
        x0 = ox + gap * (2 * i + 1)
        x1 = x0 + bw
        bh = h * (val / ymax)
        cv.fill_rect(x0, oy - bh, x1, oy - 1, col)
        cv.rect(x0, oy - bh, x1, oy - 1, COL['dark'], 1)
        # qiymat
        vtxt = ("%g" % val) + value_suffix
        cv.text_center((x0 + x1) // 2, oy - bh - 20, vtxt, COL['ink'], 1)
        # label (qisqa)
        cv.text_center((x0 + x1) // 2, oy + 8, label, COL['ink'], 1)


def line_chart(cv, ox, oy, w, h, series, xmax, ymax, xtitle="", ytitle="",
               title=None, xticks=None):
    """series: [(name, [(x,y)...], color)]."""
    _axes(cv, ox, oy, w, h, title)
    steps = 5
    for s in range(steps + 1):
        val = ymax * s / steps
        yy = oy - h * s / steps
        cv.dashed_line(ox, yy, ox + w, yy, COL['lgray'], 5, 5, 1)
        lbl = "%g" % round(val, 1)
        cv.text(ox - cv.text_w(lbl, 1) - 8, yy - 6, lbl, COL['gray'], 1)
    # x belgilari
    if xticks is None:
        xticks = [xmax * s / steps for s in range(steps + 1)]
    for xv in xticks:
        xx = ox + w * (xv / xmax)
        cv.line(xx, oy, xx, oy + 5, COL['dark'], 1)
        lbl = "%g" % round(xv, 1)
        cv.text_center(xx, oy + 10, lbl, COL['gray'], 1)
    if xtitle:
        cv.text_center(ox + w // 2, oy + 30, xtitle, COL['gray'], 1)
    if ytitle:
        cv.text(ox - 36, oy - h - 26, ytitle, COL['gray'], 1)

    def px(xv, yv):
        return (ox + w * (xv / xmax), oy - h * (yv / ymax))

    for name, pts, col in series:
        prev = None
        for (xv, yv) in pts:
            p = px(xv, yv)
            if prev:
                cv.line(prev[0], prev[1], p[0], p[1], col, 3)
            prev = p
        for (xv, yv) in pts:
            p = px(xv, yv)
            cv.fill_circle(p[0], p[1], 4, col)
            cv.circle(p[0], p[1], 4, COL['bg'], 1)


def legend(cv, x, y, items, scale=1):
    """items: [(text, color)]."""
    cy = y
    for text, col in items:
        cv.fill_rect(x, cy, x + 16, cy + 12, col)
        cv.rect(x, cy, x + 16, cy + 12, COL['dark'], 1)
        cv.text(x + 24, cy, text, COL['ink'], scale)
        cy += 22


def save(cv, name):
    path = os.path.join(OUT, name)
    cv.save_png(path)
    return path


# ===========================================================================
#  KIRISH
# ===========================================================================
def fig_kirish_overview():
    cv = Canvas(940, 470)
    cv.text_center(470, 14, "HAVO IFLOSLANISHI VA UNI TOZALASH YONDASHUVLARI", COL['ink'], 3)
    cv.line(40, 50, 900, 50, COL['blue'], 2)

    # manbalar
    cv.text_center(180, 70, "IFLOSLANTIRUVCHI MANBALAR", COL['gray'], 1)
    box(cv, 40, 95, 320, 135, "TRANSPORT (NOX, CO)", COL['lred'], COL['red'], scale=1)
    box(cv, 40, 150, 320, 190, "SANOAT (VOC, SO2)", COL['lred'], COL['red'], scale=1)
    box(cv, 40, 205, 320, 245, "MAISHIY (FORMALDEGID)", COL['lred'], COL['red'], scale=1)
    box(cv, 40, 260, 320, 300, "CHANG VA PM2.5", COL['lred'], COL['red'], scale=1)

    # markaziy: qoplama
    box(cv, 390, 150, 560, 245, "", COL['lgreen'], COL['green'], t=3,
        lines=["FAOL", "QOPLAMA"])
    cv.text_center(475, 120, "TiO2 / ZnO + ADSORBENT", COL['green'], 1)

    # natija
    cv.text_center(760, 70, "NATIJA", COL['gray'], 1)
    box(cv, 620, 110, 900, 150, "ZARARSIZ CO2 + H2O", COL['lblue'], COL['blue'], scale=1)
    box(cv, 620, 165, 900, 205, "TOZALANGAN HAVO", COL['lblue'], COL['blue'], scale=1)
    box(cv, 620, 220, 900, 260, "ANTIBAKTERIAL TASIR", COL['lblue'], COL['blue'], scale=1)

    for y in (115, 170, 225, 280):
        cv.arrow(320, y, 388, 197, COL['gray'], 1, 6)
    cv.arrow(560, 197, 618, 130, COL['green'], 2, 8)
    cv.arrow(560, 197, 618, 185, COL['green'], 2, 8)
    cv.arrow(560, 197, 618, 240, COL['green'], 2, 8)

    # quyosh
    cv.fill_circle(475, 380, 26, COL['yellow'])
    for a in range(0, 360, 30):
        import math
        rad = math.radians(a)
        cv.line(475 + 30 * math.cos(rad), 380 + 30 * math.sin(rad),
                475 + 42 * math.cos(rad), 380 + 42 * math.sin(rad), COL['yellow'], 2)
    cv.arrow(475, 422, 475, 250, COL['orange'], 2, 9)
    cv.text_center(475, 435, "QUYOSH / UV NURI", COL['orange'], 1)
    return save(cv, 'kirish_overview.png')


# ===========================================================================
#  1-BOB
# ===========================================================================
def fig_adsorbent_klassifikatsiya():
    cv = Canvas(940, 430)
    cv.text_center(470, 14, "ADSORBENT MODDALAR KLASSIFIKATSIYASI", COL['ink'], 3)
    cv.line(40, 50, 900, 50, COL['blue'], 2)
    box(cv, 340, 70, 600, 115, "ADSORBENTLAR", COL['lblue'], COL['blue'], t=3)

    cats = [
        (70, "UGLEROD ASOSLI", COL['ldark'] if 'ldark' in COL else COL['lgray'], COL['dark'],
         ["Aktiv ko'mir", "Grafen, nanotuba"]),
        (310, "OKSID ASOSLI", COL['lteal'], COL['teal'],
         ["Silikagel (SiO2)", "Al2O3, zeolit"]),
        (550, "FOTOFAOL OKSIDLAR", COL['lgreen'], COL['green'],
         ["TiO2 (anataz)", "ZnO, WO3"]),
        (790, "TABIIY/BIO", COL['lorange'], COL['orange'],
         ["Mikrosuvo'tlar", "Tuproq, gil"]),
    ]
    for cx, title, fill, border, items in cats:
        box(cv, cx - 100, 175, cx + 100, 215, title, fill, border, scale=1)
        cv.arrow(470, 117, cx, 173, COL['gray'], 1, 6)
        yy = 235
        for it in items:
            box(cv, cx - 100, yy, cx + 100, yy + 36, it, COL['bg'], COL['gray'], scale=1)
            yy += 46
    return save(cv, 'adsorbent_klassifikatsiya.png')


def fig_silikagel_jarayon():
    cv = Canvas(940, 300)
    cv.text_center(470, 14, "SILIKAGEL OLINISHI TEXNOLOGIK JARAYONI", COL['ink'], 3)
    cv.line(40, 50, 900, 50, COL['blue'], 2)
    steps = [
        ("SUYUQ SHISHA", "Na2SiO3", COL['lteal'], COL['teal']),
        ("KISLOTA BILAN", "+ H2SO4", COL['lteal'], COL['teal']),
        ("GEL HOSIL", "SiO2 * nH2O", COL['lblue'], COL['blue']),
        ("YUVISH", "Na+ chiqarish", COL['lblue'], COL['blue']),
        ("QURITISH", "100-200 C", COL['lorange'], COL['orange']),
        ("SILIKAGEL", "donador", COL['lgreen'], COL['green']),
    ]
    n = len(steps)
    bw = 130
    gap = (900 - 40 - bw * n) / (n - 1)
    x = 40
    for i, (t1, t2, fill, border) in enumerate(steps):
        box(cv, x, 120, x + bw, 200, "", fill, border, t=2, lines=[t1, t2])
        if i < n - 1:
            cv.arrow(x + bw, 160, x + bw + gap, 160, COL['gray'], 2, 8)
        x += bw + gap
    cv.text_center(470, 240, "Mezagovakli struktura: solishtirma yuza 500-800 m2/g, govak diametri 2-10 nm", COL['gray'], 1)
    return save(cv, 'silikagel_jarayon.png')


def fig_aktiv_komir():
    cv = Canvas(940, 430)
    cv.text_center(470, 14, "AKTIV KO'MIR: OLINISHI VA G'OVAK TUZILISHI", COL['ink'], 3)
    cv.line(40, 50, 900, 50, COL['blue'], 2)
    # jarayon (chap)
    steps = [
        ("XOMASHYO", "yong'oq po'sti,\nyog'och, torf", COL['lorange'], COL['orange']),
        ("KARBONIZATSIYA", "400-600 C\nkislorodsiz", COL['lgray'], COL['dark']),
        ("AKTIVATSIYA", "800-1000 C\nbug'/KOH", COL['ldark'] if 'ldark' in COL else COL['lgray'], COL['dark']),
        ("AKTIV KO'MIR", "900-1500 m2/g", COL['lgreen'], COL['green']),
    ]
    y = 80
    for t1, t2, fill, border in steps:
        lines = [t1] + t2.split('\n')
        box(cv, 40, y, 360, y + 70, "", fill, border, scale=1, lines=lines)
        if border != COL['green']:
            cv.arrow(200, y + 70, 200, y + 80, COL['gray'], 2, 7)
        y += 82
    # g'ovak struktura (o'ng)
    cv.text_center(680, 70, "MIKRO/MEZO-G'OVAK TUZILISHI", COL['gray'], 1)
    cv.rect(470, 95, 900, 410, COL['dark'], 2)
    cv.fill_rect(471, 96, 899, 409, (245, 243, 238))
    import random
    random.seed(7)
    for _ in range(420):
        x = random.randint(478, 892)
        y = random.randint(102, 402)
        r = random.choice([2, 2, 3, 4, 6])
        cv.fill_circle(x, y, r, (60, 55, 50))
    cv.text_center(685, 420 - 0, "", COL['gray'], 1)
    return save(cv, 'aktiv_komir.png')


def fig_yuza_solishtirma():
    cv = Canvas(820, 430)
    bar_chart(cv, 110, 360, 640, 270,
              data=[("AKTIV KOMIR", 1200, COL['dark']),
                    ("SILIKAGEL", 700, COL['teal']),
                    ("ZEOLIT", 600, COL['blue']),
                    ("ZnO (NANO)", 50, COL['orange']),
                    ("TiO2 (NANO)", 55, COL['green'])],
              ymax=1400, ytitle="m2/g",
              title="SOLISHTIRMA YUZA (BET), m2/g")
    return save(cv, 'yuza_solishtirma.png')


def fig_bandgap():
    cv = Canvas(900, 420)
    cv.text_center(450, 14, "TiO2 VA ZnO YARIMO'TKAZGICH TAQIQLANGAN ZONA (Eg)", COL['ink'], 3)
    cv.line(40, 50, 860, 50, COL['blue'], 2)
    mats = [
        (150, "TiO2 (ANATAZ)", 3.2, COL['green']),
        (350, "TiO2 (RUTIL)", 3.0, COL['teal']),
        (550, "ZnO", 3.37, COL['orange']),
        (750, "WO3", 2.8, COL['purple']),
    ]
    base = 380
    top = 90
    scale = (base - top) / 4.0  # 0..4 eV
    cv.line(80, base, 820, base, COL['dark'], 2)
    cv.text(60, base + 10, "VB (valent zona)", COL['gray'], 1)
    for cx, name, eg, col in mats:
        cb_y = base - eg * scale
        cv.fill_rect(cx - 70, base, cx + 70, base + 14, COL['lgray'])  # VB
        cv.fill_rect(cx - 70, cb_y - 14, cx + 70, cb_y, col)           # CB
        cv.dashed_line(cx - 70, cb_y, cx + 70, cb_y, col, 4, 3, 1)
        cv.arrow(cx, base, cx, cb_y, COL['dark'], 1, 6)
        cv.text_center(cx, (base + cb_y) // 2 - 6, ("%g eV" % eg), COL['ink'], 1)
        cv.text_center(cx, base + 24, name, COL['ink'], 1)
        cv.text_center(cx, cb_y - 30, "CB", col, 1)
    cv.text_center(450, 400, "Eg qancha kichik bo'lsa, fotofaollik uchun shuncha kam energiyali nur yetarli", COL['gray'], 1)
    return save(cv, 'bandgap.png')


def fig_qollanish_1bob():
    cv = Canvas(900, 360)
    cv.text_center(450, 14, "ADSORBENT VA OKSIDLARNING QO'LLANISH SOHALARI", COL['ink'], 3)
    cv.line(40, 50, 860, 50, COL['blue'], 2)
    items = [
        ("HAVO TOZALASH", COL['lgreen'], COL['green']),
        ("SUV TOZALASH", COL['lblue'], COL['blue']),
        ("O'ZINI TOZALOVCHI YUZA", COL['lteal'], COL['teal']),
        ("ANTIBAKTERIAL", COL['lred'], COL['red']),
        ("QUYOSH ENERGETIKASI", COL['lorange'], COL['orange']),
        ("DEZODORATSIYA", COL['lpurple'], COL['purple']),
    ]
    x0 = 60
    y0 = 90
    bw = 250
    bh = 90
    gx = 30
    gy = 30
    for i, (t, fill, border) in enumerate(items):
        r = i // 3
        c = i % 3
        x = x0 + c * (bw + gx)
        y = y0 + r * (bh + gy)
        box(cv, x, y, x + bw, y + bh, t, fill, border, scale=1)
    return save(cv, 'qollanish_1bob.png')


# ===========================================================================
#  2-BOB
# ===========================================================================
def fig_fotosintez_taqqos():
    cv = Canvas(940, 470)
    cv.text_center(470, 14, "TABIIY FOTOSINTEZ VA SUN'IY FOTOKATALIZ TAQQOSI", COL['ink'], 3)
    cv.line(40, 50, 900, 50, COL['blue'], 2)
    # chap - tabiiy
    cv.fill_rect(40, 70, 460, 450, COL['lgreen'])
    cv.rect(40, 70, 460, 450, COL['green'], 2)
    cv.text_center(250, 82, "TABIIY FOTOSINTEZ (O'SIMLIK)", COL['green'], 2)
    box(cv, 90, 130, 410, 170, "QUYOSH NURI (FOTON)", COL['lyellow'], COL['orange'], scale=1)
    box(cv, 90, 195, 410, 235, "XLOROFILL NURNI YUTADI", COL['bg'], COL['green'], scale=1)
    box(cv, 90, 260, 410, 300, "H2O VA CO2 PARCHALANADI", COL['bg'], COL['green'], scale=1)
    box(cv, 90, 325, 410, 365, "GLYUKOZA + O2 AJRALADI", COL['lgreen'], COL['green'], scale=1)
    box(cv, 90, 390, 410, 430, "NATIJA: HAVO BOYIYDI (O2)", COL['lblue'], COL['blue'], scale=1)
    for y in (170, 235, 300, 365):
        cv.arrow(250, y, 250, y + 25, COL['green'], 2, 7)
    # o'ng - sun'iy
    cv.fill_rect(480, 70, 900, 450, COL['lteal'])
    cv.rect(480, 70, 900, 450, COL['teal'], 2)
    cv.text_center(690, 82, "SUN'IY FOTOKATALIZ (TiO2)", COL['teal'], 2)
    box(cv, 530, 130, 850, 170, "UV / QUYOSH NURI (FOTON)", COL['lyellow'], COL['orange'], scale=1)
    box(cv, 530, 195, 850, 235, "TiO2 e- / h+ HOSIL QILADI", COL['bg'], COL['teal'], scale=1)
    box(cv, 530, 260, 850, 300, "OH* VA O2-* RADIKALLAR", COL['bg'], COL['teal'], scale=1)
    box(cv, 530, 325, 850, 365, "IFLOSLANTIRUVCHI OKSIDLANADI", COL['bg'], COL['teal'], scale=1)
    box(cv, 530, 390, 850, 430, "NATIJA: CO2 + H2O (ZARARSIZ)", COL['lblue'], COL['blue'], scale=1)
    for y in (170, 235, 300, 365):
        cv.arrow(690, y, 690, y + 25, COL['teal'], 2, 7)
    return save(cv, 'fotosintez_taqqos.png')


def fig_fotokataliz_mexanizm():
    cv = Canvas(940, 470)
    cv.text_center(470, 14, "TiO2 FOTOKATALIZ MEXANIZMI (ENERGIYA DIAGRAMMASI)", COL['ink'], 3)
    cv.line(40, 50, 900, 50, COL['blue'], 2)
    # zonalar
    cbx0, cbx1 = 120, 470
    cb_y = 130
    vb_y = 380
    cv.fill_rect(cbx0, cb_y - 30, cbx1, cb_y, COL['lblue'])
    cv.rect(cbx0, cb_y - 30, cbx1, cb_y, COL['blue'], 1)
    cv.text_center((cbx0 + cbx1) // 2, cb_y - 24, "O'TKAZUVCHANLIK ZONASI (CB)", COL['blue'], 1)
    cv.fill_rect(cbx0, vb_y, cbx1, vb_y + 30, COL['lorange'])
    cv.rect(cbx0, vb_y, cbx1, vb_y + 30, COL['orange'], 1)
    cv.text_center((cbx0 + cbx1) // 2, vb_y + 8, "VALENT ZONASI (VB)", COL['orange'], 1)
    # bandgap o'q
    cv.arrow(150, vb_y, 150, cb_y, COL['dark'], 2, 8)
    cv.arrow(150, cb_y, 150, vb_y, COL['dark'], 2, 8)
    cv.text(160, (cb_y + vb_y) // 2 - 10, "Eg = 3.2 eV", COL['ink'], 1)
    # foton
    import math
    cv.fill_circle(300, 60, 0, COL['yellow'])
    cv.text_center(300, 60, "h*v (UV FOTON)", COL['orange'], 1)
    cv.arrow(300, 78, 300, vb_y - 2, COL['orange'], 2, 8)
    # e- va h+
    cv.fill_circle(380, cb_y + 4, 9, COL['blue'])
    cv.text_center(380, cb_y + 1, "e-", COL['bg'], 1)
    cv.fill_circle(380, vb_y - 4, 9, COL['orange'])
    cv.text_center(380, vb_y - 7, "h+", COL['bg'], 1)
    cv.arrow(380, vb_y - 14, 380, cb_y + 16, COL['gray'], 1, 6)
    # reaksiyalar (o'ng)
    box(cv, 560, 110, 900, 155, "e- + O2  ->  O2-* (superoksid)", COL['lblue'], COL['blue'], scale=1)
    box(cv, 560, 175, 900, 220, "h+ + H2O  ->  OH* + H+", COL['lorange'], COL['orange'], scale=1)
    box(cv, 560, 250, 900, 320, "", COL['lgreen'], COL['green'], scale=1,
        lines=["OH* / O2-* + IFLOSLANTIRUVCHI", "(VOC, NOx, formaldegid)"])
    box(cv, 560, 350, 900, 410, "CO2 + H2O (ZARARSIZ)", COL['lgreen'], COL['green'], t=2, scale=1)
    cv.arrow(470, 120, 558, 132, COL['gray'], 1, 6)
    cv.arrow(470, 370, 558, 197, COL['gray'], 1, 6)
    cv.arrow(730, 220, 730, 248, COL['green'], 2, 7)
    cv.arrow(730, 320, 730, 348, COL['green'], 2, 7)
    return save(cv, 'fotokataliz_mexanizm.png')


def fig_mono_struktura():
    cv = Canvas(940, 360)
    cv.text_center(470, 14, "MONO-STRUKTURALI OKSIDLARNI OLISH USULLARI", COL['ink'], 3)
    cv.line(40, 50, 900, 50, COL['blue'], 2)
    methods = [
        ("ZOL-GEL", "alkoksid gidrolizi,\narzon, bir jinsli", COL['lgreen'], COL['green']),
        ("GIDROTERMAL", "yuqori bosim/harorat,\nyaxshi kristallik", COL['lteal'], COL['teal']),
        ("CVD", "bug' fazasidan,\nyupqa pardalar", COL['lblue'], COL['blue']),
        ("CHO'KTIRISH", "eritmadan,\nyirik miqyos", COL['lorange'], COL['orange']),
        ("ELEKTROKIMYO", "anodlash,\nnanonaycha massiv", COL['lpurple'], COL['purple']),
    ]
    n = len(methods)
    bw = 160
    gap = (900 - 40 - bw * n) / (n - 1)
    x = 40
    for t1, t2, fill, border in methods:
        lines = [t1] + t2.split('\n')
        box(cv, x, 110, x + bw, 230, "", fill, border, scale=1, lines=lines)
        x += bw + gap
    cv.text_center(470, 270, "Olish usuli zarracha o'lchami, govakligi va kristall fazasini belgilaydi", COL['gray'], 1)
    cv.text_center(470, 300, "-> bular esa fotokatalitik faollikka bevosita ta'sir qiladi", COL['gray'], 1)
    return save(cv, 'mono_struktura.png')


def fig_qollanish_sohalari_2bob():
    cv = Canvas(820, 420)
    bar_chart(cv, 150, 350, 620, 250,
              data=[("HAVO TOZALASH", 32, COL['green']),
                    ("SUV TOZALASH", 24, COL['blue']),
                    ("OZINI TOZALASH", 18, COL['teal']),
                    ("ENERGETIKA", 15, COL['orange']),
                    ("TIBBIYOT", 11, COL['purple'])],
              ymax=40, ytitle="%", value_suffix="%",
              title="NANO-G'OVAKLI OKSIDLAR QO'LLANISHI (TAXMINIY ULUSH)")
    return save(cv, 'qollanish_sohalari_2bob.png')


# ===========================================================================
#  3-BOB
# ===========================================================================
def fig_texnologiya_oqim():
    cv = Canvas(940, 320)
    cv.text_center(470, 14, "HAVONI TOZALOVCHI QOPLAMA OLISH TEXNOLOGIYASI", COL['ink'], 3)
    cv.line(40, 50, 900, 50, COL['blue'], 2)
    steps = [
        ("PREKURSOR", "Ti(OBu)4 / TiCl4", COL['lorange'], COL['orange']),
        ("ZOL TAYYORLASH", "gidroliz + barqaror", COL['lteal'], COL['teal']),
        ("QOPLASH", "dip / spray coating", COL['lblue'], COL['blue']),
        ("QURITISH", "60-120 C", COL['lgray'], COL['dark']),
        ("KALSINATSIYA", "400-500 C anataz", COL['lgreen'], COL['green']),
    ]
    n = len(steps)
    bw = 150
    gap = (900 - 40 - bw * n) / (n - 1)
    x = 40
    for i, (t1, t2, fill, border) in enumerate(steps):
        box(cv, x, 110, x + bw, 200, "", fill, border, scale=1, lines=[t1, t2])
        if i < n - 1:
            cv.arrow(x + bw, 155, x + bw + gap, 155, COL['gray'], 2, 8)
        x += bw + gap
    box(cv, 320, 240, 620, 290, "TAYYOR FOTOKATALITIK QOPLAMA", COL['lgreen'], COL['green'], t=2, scale=1)
    cv.arrow(470, 200, 470, 238, COL['green'], 2, 8)
    return save(cv, 'texnologiya_oqim.png')


def fig_qurilma():
    cv = Canvas(900, 460)
    cv.text_center(450, 14, "FOTOKATALITIK HAVO TOZALASH QURILMASI SXEMASI", COL['ink'], 3)
    cv.line(40, 50, 860, 50, COL['blue'], 2)
    # reaktor kamerasi
    cv.fill_rect(250, 120, 650, 360, (235, 244, 250))
    cv.rect(250, 120, 650, 360, COL['blue'], 2)
    cv.text_center(450, 128, "FOTOREAKTOR KAMERA", COL['blue'], 1)
    # UV lampa
    cv.fill_rect(300, 160, 600, 180, COL['lyellow'])
    cv.rect(300, 160, 600, 180, COL['orange'], 1)
    cv.text_center(450, 163, "UV LAMPA (365 nm)", COL['orange'], 1)
    import math
    for x in range(320, 601, 40):
        cv.arrow(x, 182, x, 250, COL['orange'], 1, 5)
    # qoplamali namuna
    cv.fill_rect(300, 300, 600, 330, COL['lgreen'])
    cv.rect(300, 300, 600, 330, COL['green'], 2)
    cv.text_center(450, 306, "TiO2 QOPLAMALI NAMUNA (SUBSTRAT)", COL['green'], 1)
    # gaz kirish/chiqish
    box(cv, 60, 200, 230, 250, "IFLOS HAVO KIRISHI", COL['lred'], COL['red'], scale=1)
    cv.arrow(230, 225, 250, 225, COL['red'], 2, 8)
    box(cv, 670, 200, 840, 250, "TOZA HAVO CHIQISHI", COL['lblue'], COL['blue'], scale=1)
    cv.arrow(650, 225, 670, 225, COL['blue'], 2, 8)
    # datchik
    box(cv, 320, 390, 580, 435, "GAZ ANALIZATORI / DATCHIK (NOx, VOC, CO2)", COL['bg'], COL['gray'], scale=1)
    cv.arrow(450, 360, 450, 388, COL['gray'], 1, 6)
    # ventilyator
    cv.circle(150, 300, 26, COL['dark'], 2)
    cv.text_center(150, 297, "FAN", COL['gray'], 1)
    cv.arrow(150, 274, 150, 252, COL['gray'], 1, 6)
    return save(cv, 'qurilma.png')


def fig_samaradorlik_vaqt():
    cv = Canvas(860, 430)
    series = [
        ("TiO2 + UV", [(0, 0), (30, 28), (60, 52), (90, 70), (120, 84), (150, 93), (180, 97)], COL['green']),
        ("TiO2/aktiv komir", [(0, 0), (30, 35), (60, 60), (90, 78), (120, 90), (150, 96), (180, 99)], COL['blue']),
        ("ZnO + UV", [(0, 0), (30, 22), (60, 41), (90, 58), (120, 71), (150, 80), (180, 86)], COL['orange']),
        ("Faqat adsorbent", [(0, 0), (30, 18), (60, 30), (90, 38), (120, 43), (150, 46), (180, 48)], COL['gray']),
    ]
    line_chart(cv, 110, 350, 600, 270, series, xmax=180, ymax=100,
               xtitle="VAQT (MINUT)", ytitle="%",
               title="IFLOSLANTIRUVCHINING PARCHALANISH DARAJASI",
               xticks=[0, 30, 60, 90, 120, 150, 180])
    legend(cv, 720, 90, [(s[0], s[2]) for s in series], 1)
    return save(cv, 'samaradorlik_vaqt.png')


def fig_solishtirma_bar():
    cv = Canvas(840, 430)
    bar_chart(cv, 120, 360, 640, 270,
              data=[("TiO2/AK", 99, COL['blue']),
                    ("TiO2", 97, COL['green']),
                    ("ZnO", 86, COL['orange']),
                    ("TiO2/SiO2", 92, COL['teal']),
                    ("ADSORBENT", 48, COL['gray'])],
              ymax=100, ytitle="%", value_suffix="%",
              title="180 MIN DAVOMIDA TOZALASH SAMARADORLIGI")
    return save(cv, 'solishtirma_bar.png')


def fig_xrd():
    cv = Canvas(860, 400)
    # XRD difraktogramma (anataz TiO2 cho'qqilari)
    ox, oy, w, h = 90, 330, 700, 250
    cv.text_center(450, 14, "QOPLAMA XRD DIFRAKTOGRAMMASI (ANATAZ TiO2)", COL['ink'], 3)
    cv.line(40, 46, 820, 46, COL['blue'], 2)
    cv.line(ox, oy, ox, oy - h, COL['dark'], 2)
    cv.line(ox, oy, ox + w, oy, COL['dark'], 2)
    cv.text(ox - 30, oy - h - 22, "I (a.b.)", COL['gray'], 1)
    cv.text_center(ox + w // 2, oy + 28, "2-teta (gradus)", COL['gray'], 1)
    peaks = [(25.3, 1.0, "(101)"), (37.8, 0.28, "(004)"), (48.0, 0.38, "(200)"),
             (53.9, 0.22, "(105)"), (55.1, 0.20, "(211)"), (62.7, 0.18, "(204)")]
    xmin, xmax = 20, 70
    import math

    def X(v):
        return ox + w * (v - xmin) / (xmax - xmin)
    # x belgilari
    for tv in range(20, 71, 10):
        cv.line(X(tv), oy, X(tv), oy + 5, COL['dark'], 1)
        cv.text_center(X(tv), oy + 10, str(tv), COL['gray'], 1)
    # bazaviy chiziq + cho'qqilar (gauss)
    prev = None
    step = 1
    for xv in range(xmin * 10, xmax * 10 + 1, step):
        t = xv / 10.0
        y = 0.02
        for (p, amp, _) in peaks:
            y += amp * math.exp(-((t - p) ** 2) / (2 * 0.35 ** 2))
        py = oy - h * min(y, 1.05) / 1.1
        px_ = X(t)
        if prev:
            cv.line(prev[0], prev[1], px_, py, COL['green'], 2)
        prev = (px_, py)
    for (p, amp, idx) in peaks:
        cv.text_center(X(p), oy - h * amp / 1.1 - 18, idx, COL['ink'], 1)
    return save(cv, 'xrd.png')


def fig_karakterizatsiya():
    cv = Canvas(900, 340)
    cv.text_center(450, 14, "QOPLAMALARNI TAHLIL QILISH USULLARI", COL['ink'], 3)
    cv.line(40, 50, 860, 50, COL['blue'], 2)
    items = [
        ("XRD", "kristall faza,\nzarracha o'lchami", COL['lgreen'], COL['green']),
        ("SEM/TEM", "yuza morfologiyasi,\nmikrostruktura", COL['lblue'], COL['blue']),
        ("BET", "solishtirma yuza,\ngovaklik", COL['lteal'], COL['teal']),
        ("FTIR", "kimyoviy bog'lar,\nfunksional guruh", COL['lorange'], COL['orange']),
        ("UV-Vis", "yutilish,\ntaqiqlangan zona", COL['lpurple'], COL['purple']),
        ("KONTAKT BURCHAK", "gidrofillik,\no'zini tozalash", COL['lred'], COL['red']),
    ]
    x0, y0, bw, bh, gx, gy = 60, 90, 250, 90, 30, 30
    for i, (t1, t2, fill, border) in enumerate(items):
        r = i // 3
        c = i % 3
        x = x0 + c * (bw + gx)
        y = y0 + r * (bh + gy)
        lines = [t1] + t2.split('\n')
        box(cv, x, y, x + bw, y + bh, "", fill, border, scale=1, lines=lines)
    return save(cv, 'karakterizatsiya.png')


def fig_qayta_ishlatish():
    cv = Canvas(820, 410)
    bar_chart(cv, 120, 340, 620, 250,
              data=[("1-SIKL", 97, COL['green']),
                    ("2-SIKL", 96, COL['green']),
                    ("3-SIKL", 94, COL['teal']),
                    ("4-SIKL", 92, COL['teal']),
                    ("5-SIKL", 90, COL['blue'])],
              ymax=100, ytitle="%", value_suffix="%",
              title="QOPLAMA BARQARORLIGI (QAYTA ISHLATISH SIKLLARI)")
    return save(cv, 'qayta_ishlatish.png')


# ===========================================================================
def main():
    funcs = [
        fig_kirish_overview,
        fig_adsorbent_klassifikatsiya,
        fig_silikagel_jarayon,
        fig_aktiv_komir,
        fig_yuza_solishtirma,
        fig_bandgap,
        fig_qollanish_1bob,
        fig_fotosintez_taqqos,
        fig_fotokataliz_mexanizm,
        fig_mono_struktura,
        fig_qollanish_sohalari_2bob,
        fig_texnologiya_oqim,
        fig_qurilma,
        fig_samaradorlik_vaqt,
        fig_solishtirma_bar,
        fig_xrd,
        fig_karakterizatsiya,
        fig_qayta_ishlatish,
    ]
    paths = []
    for f in funcs:
        p = f()
        paths.append(p)
        print("OK:", os.path.basename(p))
    print("\nJami:", len(paths), "ta rasm ->", OUT)
    return paths


if __name__ == '__main__':
    main()
