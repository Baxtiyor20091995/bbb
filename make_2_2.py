# -*- coding: utf-8 -*-
"""
2.2. Kesish jarayonini boshqarish tizimining vaqt va chastotaviy
xarakteristikalarini aniqlash.

- 2.1-modeldan uzatish funksiyasi tuziladi (boshqaruv obyekti).
- Yopiq tizimning o'tish h(t) va impuls g(t) xarakteristikalari (RK4).
- Ochiq tizimning Bode diagrammasi + zapas (gain/phase margin).
- Grafiklar MATLAB uslubida PNG sifatida chiziladi va Word'ga joylashtiriladi.

Sof Python (zlib + plotlib), tashqi kutubxonalarsiz.
"""
import zipfile
import math
from xml.sax.saxutils import escape
from plotlib import Canvas, draw_plot, BLUE, BLACK, RED, DKGRID

OUT = "2.2_Vaqt_va_chastotaviy_xarakteristikalar.docx"

# ===========================================================================
# 1) MODEL VA UZATISH FUNKSIYASI
# ===========================================================================
# Ochiq tizim (boshqaruv obyekti): yuritma (integrator + lag) * kesish (lag)
#   W(s) = K / [ s (T1 s + 1)(T2 s + 1) ]
K = 18.0       # ochiq tizim kuchaytirish koeffitsiyenti (dobrotnost), 1/s
T1 = 0.05      # yuritma elektromexanik doimiysi, s
T2 = 0.02      # kesish jarayoni (qirindi hosil bo'lishi) doimiysi, s

# Yopiq tizim (birlik teskari aloqa): Phi(s) = W/(1+W)
#   maxraj: s(T1 s+1)(T2 s+1) + K = T1T2 s^3 + (T1+T2) s^2 + s + K
# Normallash (T1T2 ga bo'lish): s^3 + a2 s^2 + a1 s + a0,  surat = b0
a2 = (T1 + T2) / (T1 * T2)        # 70.0
a1 = 1.0 / (T1 * T2)              # 1000.0
a0 = K / (T1 * T2)                # 18000.0
b0 = a0                           # birlik statik kuchaytirish (Phi(0)=1)

# ===========================================================================
# 2) VAQT XARAKTERISTIKALARI (RK4 integrallash)
# ===========================================================================
# Holat fazosi (boshqariluvchi kanonik forma):
#   x1'=x2, x2'=x3, x3'=-a0 x1 -a1 x2 -a2 x3 + u ;  y = b0 x1


def deriv(x, u):
    return [x[1],
            x[2],
            -a0 * x[0] - a1 * x[1] - a2 * x[2] + u]


def simulate(x0, u_const, tmax, dt):
    x = list(x0)
    ts, ys = [0.0], [b0 * x[0]]
    n = int(tmax / dt)
    t = 0.0
    for _ in range(n):
        k1 = deriv(x, u_const)
        x2 = [x[i] + 0.5 * dt * k1[i] for i in range(3)]
        k2 = deriv(x2, u_const)
        x3 = [x[i] + 0.5 * dt * k2[i] for i in range(3)]
        k3 = deriv(x3, u_const)
        x4 = [x[i] + dt * k3[i] for i in range(3)]
        k4 = deriv(x4, u_const)
        x = [x[i] + dt / 6.0 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
             for i in range(3)]
        t += dt
        ts.append(t)
        ys.append(b0 * x[0])
    return ts, ys


DT = 0.0002
TMAX = 0.8
# o'tish (step) xarakteristikasi
t_h, h = simulate([0, 0, 0], 1.0, TMAX, DT)
# impuls xarakteristikasi g(t) = C e^{At} B  -> x0=B=[0,0,1], u=0
t_g, g = simulate([0, 0, 1.0], 0.0, TMAX, DT)

# o'tish jarayoni sifat ko'rsatkichlari
# yopiq tizimning aniq statik kuchaytirishi Phi(0) = b0/a0 = 1.0
h_ss = b0 / a0
h_peak = max(h)
i_peak = h.index(h_peak)
t_peak = t_h[i_peak]
overshoot = (h_peak - h_ss) / h_ss * 100.0
# o'rnashish vaqti (±5%)
band = 0.05 * h_ss
t_settle = t_h[-1]
for i in range(len(h) - 1, -1, -1):
    if abs(h[i] - h_ss) > band:
        t_settle = t_h[min(i + 1, len(h) - 1)]
        break
# ko'tarilish vaqti (0.1 -> 0.9)
def cross(level):
    for i in range(len(h)):
        if h[i] >= level * h_ss:
            return t_h[i]
    return t_h[-1]
t_rise = cross(0.9) - cross(0.1)

# ===========================================================================
# 3) CHASTOTAVIY XARAKTERISTIKA (Bode) + ZAPASLAR
# ===========================================================================
def L_mag(w):
    return K / (w * math.sqrt(1 + (T1 * w) ** 2) * math.sqrt(1 + (T2 * w) ** 2))


def L_phase_deg(w):
    return -90.0 - math.degrees(math.atan(T1 * w)) - math.degrees(math.atan(T2 * w))


W = []
MAG = []
PHA = []
N = 800
w_lo, w_hi = 0.1, 1000.0
for i in range(N + 1):
    w = 10 ** (math.log10(w_lo) + (math.log10(w_hi) - math.log10(w_lo)) * i / N)
    W.append(w)
    MAG.append(20 * math.log10(L_mag(w)))
    PHA.append(L_phase_deg(w))

# kesishish chastotalari (interpolyatsiya bilan)
def find_cross_x(xs, ys, target):
    for i in range(len(xs) - 1):
        y0, y1 = ys[i] - target, ys[i + 1] - target
        if y0 == 0:
            return xs[i]
        if y0 * y1 < 0:
            f = y0 / (y0 - y1)
            # logarifmik interpolyatsiya x bo'yicha
            lx = math.log10(xs[i]) + f * (math.log10(xs[i + 1]) - math.log10(xs[i]))
            return 10 ** lx
    return None


wc = find_cross_x(W, MAG, 0.0)          # kuchaytirish kesishishi (0 dB)
w180 = find_cross_x(W, PHA, -180.0)     # faza kesishishi (-180 deg)
PM = 180.0 + L_phase_deg(wc) if wc else float("nan")
GM_dB = -20 * math.log10(L_mag(w180)) if w180 else float("inf")

print("== Yopiq tizim (vaqt) ==")
print("  Statik qiymat h_inf = %.4f" % h_ss)
print("  Overshoot sigma = %.1f %%, t_peak=%.4f s" % (overshoot, t_peak))
print("  t_rise(0.1-0.9)=%.4f s, t_settle(5%%)=%.4f s" % (t_rise, t_settle))
print("  g(t) max = %.2f at t=%.4f" % (max(g), t_g[g.index(max(g))]))
print("== Ochiq tizim (Bode) ==")
print("  wc=%.3f rad/s, PM=%.2f deg" % (wc, PM))
print("  w180=%.3f rad/s, GM=%.2f dB" % (w180, GM_dB))

# ===========================================================================
# 4) GRAFIKLARNI CHIZISH (PNG)
# ===========================================================================
# --- h(t): o'tish xarakteristikasi ---
cv1 = Canvas(820, 470)
y_top = math.ceil(h_peak * 10) / 10 + 0.1
area = (95, 45, 790, 400)
def extra_h(cv, mx, my):
    # statik daraja chizig'i
    yy = int(round(my(h_ss)))
    cv.dashed_hline(area[0], area[2], yy, DKGRID)
draw_plot(cv1, area, t_h, h, (0, TMAX), (0, y_top),
          title="OTISH XARAKTERISTIKASI  H(T)", xlabel="T, S", ylabel="H(T)",
          xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
          color=BLUE, extra=extra_h)
png_h = cv1.to_png()

# --- g(t): impuls xarakteristikasi ---
cv2 = Canvas(820, 470)
g_max = max(g)
g_min = min(g)
gy_hi = math.ceil(g_max / 10) * 10
gy_lo = math.floor(g_min / 10) * 10
area2 = (110, 45, 790, 400)
def extra_g(cv, mx, my):
    yy = int(round(my(0)))
    cv.dashed_hline(area2[0], area2[2], yy, DKGRID)
draw_plot(cv2, area2, t_g, g, (0, TMAX), (gy_lo, gy_hi),
          title="IMPULS XARAKTERISTIKASI  G(T)", xlabel="T, S", ylabel="G(T)",
          xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
          color=(180, 40, 0), extra=extra_g)
png_g = cv2.to_png()

# --- Bode (magnitude + phase) ---
cvb = Canvas(820, 660)
xticks_b = [0.1, 1, 10, 100, 1000]
xlabels_b = ["0.1", "1", "10", "100", "1000"]
mag_lo = math.floor(min(MAG) / 20) * 20
mag_hi = math.ceil(max(MAG) / 20) * 20
area_m = (95, 45, 790, 300)
area_p = (95, 360, 790, 600)

def extra_mag(cv, mx, my):
    # 0 dB chizig'i
    cv.dashed_hline(area_m[0], area_m[2], int(round(my(0.0))), DKGRID)
    # wc va w180 vertikal chiziqlari
    if wc:
        cv.dashed_vline(int(round(mx(wc))), area_m[1], area_m[3], RED)
    if w180:
        cv.dashed_vline(int(round(mx(w180))), area_m[1], area_m[3], (0, 150, 0))

draw_plot(cvb, area_m, W, MAG, (w_lo, w_hi), (mag_lo, mag_hi),
          title="BODE DIAGRAMMASI", ylabel="MAGNITUDE (DB)",
          xticks=xticks_b, xticklabels=xlabels_b, xlog=True,
          yticks=list(range(int(mag_lo), int(mag_hi) + 1, 20)),
          color=BLUE, extra=extra_mag)

def extra_pha(cv, mx, my):
    cv.dashed_hline(area_p[0], area_p[2], int(round(my(-180.0))), DKGRID)
    if wc:
        cv.dashed_vline(int(round(mx(wc))), area_p[1], area_p[3], RED)
    if w180:
        cv.dashed_vline(int(round(mx(w180))), area_p[1], area_p[3], (0, 150, 0))

draw_plot(cvb, area_p, W, PHA, (w_lo, w_hi), (-270, -90),
          xlabel="FREQUENCY (RAD/S)", ylabel="PHASE (DEG)",
          xticks=xticks_b, xticklabels=xlabels_b, xlog=True,
          yticks=[-90, -135, -180, -225, -270],
          color=BLUE, extra=extra_pha)
# zapaslar yozuvi
cvb.text(area_m[0] + 8, area_m[1] + 6,
         "GM = %.1f DB    PM = %.0f DEG" % (GM_dB, PM), BLACK, 2)
png_bode = cvb.to_png()

# ===========================================================================
# 5) WORD HUJJATI
# ===========================================================================
NSDECL = (
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
)
TXT_W = 9355


def esc(t):
    return escape(str(t))


def run(text, bold=False, italic=False, size=28, sub=False, sup=False):
    rpr = ['<w:rPr><w:rFonts w:ascii="Times New Roman" '
           'w:hAnsi="Times New Roman" w:cs="Times New Roman"/>']
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if sub:
        rpr.append('<w:vertAlign w:val="subscript"/>')
    if sup:
        rpr.append('<w:vertAlign w:val="superscript"/>')
    rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (size, size))
    return ("<w:r>" + "".join(rpr) +
            '<w:t xml:space="preserve">' + esc(text) + "</w:t></w:r>")


def runs_from_parts(parts):
    out = []
    for p in parts:
        if isinstance(p, str):
            out.append(run(p))
        else:
            out.append(run(p[0], **p[1]))
    return "".join(out)


def para(content, align="both", after=120, before=0, line=360,
         first=709, left=0, keep=False):
    ppr = ["<w:pPr>"]
    jc = {"left": "left", "center": "center", "right": "right", "both": "both"}[align]
    ppr.append('<w:jc w:val="%s"/>' % jc)
    ind = []
    if left:
        ind.append('w:left="%d"' % left)
    if first:
        ind.append('w:firstLine="%d"' % first)
    if ind:
        ppr.append('<w:ind %s/>' % " ".join(ind))
    ppr.append('<w:spacing w:before="%d" w:after="%d" w:line="%d" '
               'w:lineRule="auto"/>' % (before, after, line))
    if keep:
        ppr.append("<w:keepNext/>")
    ppr.append("</w:pPr>")
    if isinstance(content, list):
        body = runs_from_parts(content)
    elif content.startswith("<w:r") or content.startswith("<w:fldSimple"):
        body = content
    else:
        body = run(content)
    return "<w:p>" + "".join(ppr) + body + "</w:p>"


def h_section(text):
    return para([(text, {"bold": True, "size": 28})], align="left",
                before=160, after=120, first=0, keep=True)


def h_sub(text):
    return para([(text, {"bold": True, "italic": True, "size": 28})],
                align="left", before=120, after=80, first=0, keep=True)


def formula(expr_runs, number=None):
    center = TXT_W // 2
    ppr = ('<w:pPr><w:tabs><w:tab w:val="center" w:pos="%d"/>'
           '<w:tab w:val="right" w:pos="%d"/></w:tabs>'
           '<w:spacing w:before="80" w:after="80" w:line="360" '
           'w:lineRule="auto"/><w:ind w:firstLine="0"/></w:pPr>' % (center, TXT_W))
    tab = '<w:r><w:tab/></w:r>'
    num = (tab + run(number) if number else "")
    return "<w:p>" + ppr + tab + expr_runs + num + "</w:p>"


def caption(text):
    return para([(text, {"italic": True, "size": 24})], align="center",
                after=60, before=40, first=0)


def cell(text, bold=False, align="left", w=None, shade=None, size=26):
    tcpr = ["<w:tcPr>"]
    if w:
        tcpr.append('<w:tcW w:w="%d" w:type="dxa"/>' % w)
    if shade:
        tcpr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
    tcpr.append('<w:vAlign w:val="center"/></w:tcPr>')
    p = ('<w:p><w:pPr><w:jc w:val="%s"/><w:spacing w:before="20" w:after="20" '
         'w:line="240" w:lineRule="auto"/><w:ind w:firstLine="0"/></w:pPr>%s</w:p>'
         % (align, run(text, bold=bold, size=size)))
    return "<w:tc>" + "".join(tcpr) + p + "</w:tc>"


def table(rows, widths, aligns=None):
    if aligns is None:
        aligns = ["left"] * len(widths)
    borders = ('<w:tblBorders>'
               '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
               '</w:tblBorders>')
    tblpr = ('<w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/>%s</w:tblPr>'
             % (sum(widths), borders))
    grid = "<w:tblGrid>" + "".join('<w:gridCol w:w="%d"/>' % w for w in widths) + "</w:tblGrid>"
    trs = []
    for ri, rowcells in enumerate(rows):
        head = ri == 0
        tcs = [cell(c, bold=head, align=aligns[ci], w=widths[ci],
                    shade="D9D9D9" if head else None) for ci, c in enumerate(rowcells)]
        trs.append("<w:tr>" + "".join(tcs) + "</w:tr>")
    return ("<w:tbl>" + tblpr + grid + "".join(trs) + "</w:tbl>"
            '<w:p><w:pPr><w:spacing w:after="80" w:line="240" w:lineRule="auto"/></w:pPr></w:p>')


def image_par(relid, did, name, w_px, h_px, disp_cm=15.0):
    cx = int(disp_cm * 360000)
    cy = int(cx * h_px / w_px)
    drawing = (
        '<w:r><w:drawing>'
        '<wp:inline distT="0" distB="0" distL="0" distR="0" '
        'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
        '<wp:extent cx="%d" cy="%d"/>' % (cx, cy) +
        '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
        '<wp:docPr id="%d" name="%s"/>' % (did, esc(name)) +
        '<wp:cNvGraphicFramePr>'
        '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
        '</wp:cNvGraphicFramePr>'
        '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
        '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>' % (did, esc(name)) +
        '<pic:blipFill><a:blip r:embed="%s"/>' % relid +
        '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>' % (cx, cy) +
        '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
        '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
    )
    return ('<w:p><w:pPr><w:jc w:val="center"/>'
            '<w:spacing w:before="60" w:after="40" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:firstLine="0"/></w:pPr>' + drawing + '</w:p>')


def num(x, nd=1):
    s = ("%." + str(nd) + "f") % x
    return s.replace(".", ",")


# --------------------------- MATN -----------------------------------------
B = []
B.append(h_section("2.2. Kesish jarayonini boshqarish tizimining vaqt va "
                   "chastotaviy xarakteristikalarini aniqlash"))

B.append(para(
    "2.1-bo‘limda tuzilgan statik matematik model kesish rejimlari va "
    "kuchlari orasidagi bog‘lanishni beradi, lekin avtomatik boshqaruv "
    "tizimini loyihalash uchun jarayonning dinamik (vaqt bo‘yicha) xulqini "
    "ham bilish zarur. Shu maqsadda boshqaruv obyektining uzatish funksiyasi "
    "tuziladi hamda tizimning o‘tish h(t), impuls g(t) va chastotaviy (Bode) "
    "xarakteristikalari aniqlanadi."))

B.append(h_sub("2.2.1. Boshqaruv obyektining uzatish funksiyasini tuzish"))
B.append(para(
    "Kesish kuchini barqaror ushlab turuvchi boshqaruv konturi quyidagi "
    "bo‘g‘inlardan iborat: surilish yuritmasi (servoyuritma) va kesish "
    "jarayonining o‘zi. Surilish yuritmasi holat (siljish) bo‘yicha "
    "integrallovchi xususiyatga ega bo‘lib, elektromexanik kechikish doimiysi "
    "T₁ bilan, kesish jarayoni esa qirindi hosil bo‘lishi inersiyasini "
    "ifodalovchi T₂ doimiysi bilan birinchi tartibli aperiodik bo‘g‘in "
    "sifatida tavsiflanadi. Natijada ochiq (uzilgan) tizimning uzatish "
    "funksiyasi quyidagi ko‘rinishni oladi:"))

f_w = (run("W", italic=True) + run("(") + run("s", italic=True) + run(") = ") +
       run("K", italic=True) + run(" / [ ") + run("s", italic=True) +
       run(" ( ") + run("T", italic=True) + run("1", sub=True) + run(" ") +
       run("s", italic=True) + run(" + 1 )( ") + run("T", italic=True) +
       run("2", sub=True) + run(" ") + run("s", italic=True) + run(" + 1 ) ]"))
B.append(formula(f_w, "(2.11)"))

B.append(para([
    ("bu yerda ", {}), ("K", {"italic": True}),
    (" — tizimning kuchaytirish (dobrotnost) koeffitsiyenti; ", {}),
    ("T", {"italic": True}), ("1", {"sub": True}),
    (" — surilish yuritmasining, ", {}),
    ("T", {"italic": True}), ("2", {"sub": True}),
    (" — kesish jarayonining vaqt doimiylari. 2.1-bo‘limdagi ish nuqtasi va "
     "HT-250 yuritmasi parametrlaridan kelib chiqib quyidagi qiymatlar qabul "
     "qilinadi: ", {}),
    ("K", {"italic": True}), (" = %s 1/s; " % num(K, 0), {}),
    ("T", {"italic": True}), ("1", {"sub": True}),
    (" = %s s; " % num(T1, 2), {}),
    ("T", {"italic": True}), ("2", {"sub": True}),
    (" = %s s." % num(T2, 2), {}),
], first=0))

B.append(para("Boshqaruv tizimi birlik teskari aloqa bilan yopilganda, "
              "yopiq tizimning uzatish funksiyasi:"))
f_phi = (run("Φ", italic=True) + run("(") + run("s", italic=True) + run(") = ") +
         run("W", italic=True) + run("(") + run("s", italic=True) + run(") / [1 + ") +
         run("W", italic=True) + run("(") + run("s", italic=True) + run(")]"))
B.append(formula(f_phi, "(2.12)"))
B.append(para("(2.11) ni (2.12) ga qo‘yib, maxrajni soddalashtirgach, yopiq "
              "tizimning xarakteristik tenglamasi uchinchi tartibli ko‘rinishga "
              "keladi:"))
f_char = (run("T", italic=True) + run("1", sub=True) + run("T", italic=True) +
          run("2", sub=True) + run(" ") + run("s", italic=True) + run("3", sup=True) +
          run(" + (") + run("T", italic=True) + run("1", sub=True) + run("+") +
          run("T", italic=True) + run("2", sub=True) + run(") ") +
          run("s", italic=True) + run("2", sup=True) + run(" + ") +
          run("s", italic=True) + run(" + ") + run("K", italic=True) + run(" = 0"))
B.append(formula(f_char, "(2.13)"))
B.append(para([
    ("Qiymatlarni qo‘yganda xarakteristik ko‘phad ", {}),
    ("0,001·s³ + 0,07·s² + s + 18 = 0", {"italic": True}),
    (" ko‘rinishini oladi. Raus–Gurvits mezoni bo‘yicha barcha koeffitsiyentlar "
     "musbat va Raus jadvalining birinchi ustuni ishorasini saqlaydi "
     "(742,9 > 0), demak yopiq tizim turg‘un.", {}),
], first=0))

B.append(h_sub("2.2.2. Vaqt xarakteristikalari: o‘tish h(t) va impuls g(t)"))
B.append(para(
    "Yopiq tizimning uzatish funksiyasi (2.12) holat fazosi shakliga "
    "keltirilib, differensial tenglamalar tizimi Runge–Kutta (4-tartib) usuli "
    "bilan integrallandi. Birlik sakrash (1(t)) ta’siriga tizim javobi — "
    "o‘tish xarakteristikasi h(t) — 2.1-rasmda, birlik impuls ta’siriga javob "
    "— impuls (vazn) funksiyasi g(t) — 2.2-rasmda keltirilgan."))

B.append(image_par("rId2", 101, "h(t)", 820, 470))
B.append(caption("2.1-rasm. Boshqaruv tizimining o‘tish xarakteristikasi h(t)"))

B.append(image_par("rId3", 102, "g(t)", 820, 470))
B.append(caption("2.2-rasm. Boshqaruv tizimining impuls xarakteristikasi g(t)"))

B.append(para("O‘tish xarakteristikasidan olingan asosiy sifat ko‘rsatkichlari "
              "2.4-jadvalda berilgan."))
B.append(caption("2.4-jadval. O‘tish jarayonining sifat ko‘rsatkichlari"))
B.append(table(
    [["Ko‘rsatkich", "Belgisi", "Qiymati"],
     ["Turg‘unlashgan qiymat", "h(∞)", num(h_ss, 2)],
     ["Maksimal qiymat", "hmax", num(h_peak, 2)],
     ["O‘tib ketish (overshoot)", "σ, %", num(overshoot, 1)],
     ["Maksimumga chiqish vaqti", "tp, s", num(t_peak, 3)],
     ["Ko‘tarilish vaqti (0,1–0,9)", "tk, s", num(t_rise, 3)],
     ["O‘rnashish vaqti (±5%)", "tt, s", num(t_settle, 3)]],
    widths=[5000, 1800, 2555],
    aligns=["left", "center", "center"]))

B.append(para([
    ("Grafiklardan ko‘rinadiki, o‘tish xarakteristikasi h(t) so‘nuvchi "
     "tebranish ko‘rinishida bo‘lib, taxminan ", {}),
    (num(t_settle, 2) + " s", {"italic": True}),
    (" da turg‘un qiymatga (birlikka) o‘rnashadi; o‘tib ketish ", {}),
    (num(overshoot, 0) + "%", {"italic": True}),
    (" ni tashkil etadi, bu sanoat boshqaruv tizimlari uchun maqbul "
     "(odatda 30% gacha) hisoblanadi. Impuls xarakteristikasi g(t) o‘tish "
     "xarakteristikasining hosilasi bo‘lib (g(t)=dh/dt), uning musbat va "
     "manfiy qiymatlari h(t) dagi tebranishlarga mos keladi va vaqt o‘tishi "
     "bilan nolga intiladi — bu ham tizim turg‘unligini tasdiqlaydi.", {}),
], first=0))

B.append(h_sub("2.2.3. Chastotaviy xarakteristika va turg‘unlik zapaslari "
               "(Bode diagrammasi)"))
B.append(para(
    "Ochiq tizimning (2.11) chastotaviy xususiyatlarini baholash uchun "
    "Bode diagrammasi qurildi: logarifmik amplituda-chastota (LACHX) va "
    "faza-chastota (FCHX) xarakteristikalari. Diagramma turg‘unlik zapaslarini "
    "— amplituda bo‘yicha zapas (Gain Margin, GM) va faza bo‘yicha zapas "
    "(Phase Margin, PM) ni aniqlash imkonini beradi."))

B.append(image_par("rId4", 103, "Bode", 820, 660))
B.append(caption("2.3-rasm. Ochiq tizimning Bode diagrammasi va turg‘unlik "
                 "zapaslari (GM, PM)"))

B.append(caption("2.5-jadval. Chastotaviy xarakteristikaning ko‘rsatkichlari"))
B.append(table(
    [["Ko‘rsatkich", "Belgisi", "Qiymati"],
     ["Kuchaytirish kesishish chastotasi", "ωc, rad/s", num(wc, 1)],
     ["Faza kesishish chastotasi", "ωπ, rad/s", num(w180, 1)],
     ["Faza bo‘yicha zapas", "PM, deg", num(PM, 0)],
     ["Amplituda bo‘yicha zapas", "GM, dB", num(GM_dB, 1)]],
    widths=[5000, 1800, 2555],
    aligns=["left", "center", "center"]))

B.append(para([
    ("Bode diagrammasidan olingan natijalar: kuchaytirish kesishish "
     "chastotasi ωc ≈ %s rad/s, unga mos faza zapasi PM ≈ %s°; faza "
     "kesishish chastotasi ωπ ≈ %s rad/s da amplituda zapasi "
     "GM ≈ %s dB. " % (num(wc, 1), num(PM, 0), num(w180, 1), num(GM_dB, 1)), {}),
    ("Ikkala zapas ham musbat bo‘lganligi sababli (Naykvist–Bode mezoni "
     "bo‘yicha) yopiq tizim turg‘un. ", {}),
    ("Bundan tashqari, PM ≈ %s° qiymati 30–60° tavsiya etilgan oraliqda "
     "yotadi, GM ≈ %s dB esa 6 dB dan katta — bu tizim yetarli barqarorlik "
     "zapasiga ega ekanini va parametrlar o‘zgarishiga (masalan, material "
     "qattiqligi yoki kesish kuchining tebranishiga) chidamli ekanini "
     "ko‘rsatadi." % (num(PM, 0), num(GM_dB, 1)), {}),
], first=0))

B.append(h_sub("2.2.4. Xulosa"))
B.append(para(
    "Ushbu bo‘limda kesish jarayonini boshqarish tizimining matematik modeli "
    "asosida uzatish funksiyasi (2.11) tuzildi va uning vaqt hamda chastotaviy "
    "xarakteristikalari aniqlandi. O‘tish xarakteristikasi h(t) tizim "
    "turg‘unligini va maqbul sifat ko‘rsatkichlarini (σ ≈ %s%%, "
    "tt ≈ %s s), Bode diagrammasi esa yetarli turg‘unlik zapaslarini "
    "(PM ≈ %s°, GM ≈ %s dB) ko‘rsatdi. Olingan natijalar boshqaruv tizimi "
    "to‘g‘ri loyihalanganini tasdiqlaydi va 2.3-bo‘limda tizim turg‘unligini "
    "hamda o‘tkinchi jarayonlarni chuqurroq tahlil qilish va rostlagichni "
    "sozlash uchun asos bo‘ladi."
    % (num(overshoot, 0), num(t_settle, 2), num(PM, 0), num(GM_dB, 1))))

# --------------------------- HUJJATNI YIG'ISH -----------------------------
sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" '
        'w:left="1701" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:pgNumType w:start="27"/></w:sectPr>')

document_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<w:document ' + NSDECL + '><w:body>' + "".join(B) + sect +
                '</w:body></w:document>')

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Default Extension="png" ContentType="image/png"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    '</Types>')

rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    '</Relationships>')

doc_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image2.png"/>'
    '<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image3.png"/>'
    '</Relationships>')

styles_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:styles ' + NSDECL + '><w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="uz-Latn-UZ"/>'
    '</w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/><w:qFormat/></w:style></w:styles>')

core_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<cp:coreProperties '
    'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/">'
    '<dc:title>2.2 Vaqt va chastotaviy xarakteristikalar</dc:title>'
    '<dc:creator>Bakalavr dissertatsiyasi</dc:creator>'
    '<cp:lastModifiedBy>Kiro</cp:lastModifiedBy></cp:coreProperties>')

app_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    '<Application>Kiro OOXML Generator</Application></Properties>')

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("word/media/image1.png", png_h)
    z.writestr("word/media/image2.png", png_g)
    z.writestr("word/media/image3.png", png_bode)
    z.writestr("docProps/core.xml", core_xml)
    z.writestr("docProps/app.xml", app_xml)

print("Yaratildi:", OUT)
