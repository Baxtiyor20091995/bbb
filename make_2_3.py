# -*- coding: utf-8 -*-
"""
2.3. Tizim turg'unligini va o'tkinchi jarayonlarni tahlil qilish
     (rostlagichni sozlash; ilmiy tadqiqotlar natijalari bilan).

- Raus-Gurvits mezoni bo'yicha turg'unlik va kritik kuchaytirish.
- Ziegler-Nichols usuli; astatik obyekt uchun PD-rostlagichni sozlash.
- O'tkinchi jarayonlarni taqqoslash (step) va ildiz godografi (root locus).
Sof Python (zlib + plotlib).
"""
import zipfile
import math
import cmath
from xml.sax.saxutils import escape
from plotlib import (Canvas, draw_multi, draw_axes, poly_roots,
                     BLUE, RED, GREEN, ORANGE, BLACK, DKGRID)

OUT = "2.3_Turgunlik_va_otkinchi_jarayonlar.docx"

# ===========================================================================
# 1) MODEL VA TURG'UNLIK
# ===========================================================================
Kob, T1, T2 = 18.0, 0.05, 0.02
# Yopiq tizim (P, 2.2): 0.001 s^3 + 0.07 s^2 + s + 18 = 0
c3, c2, c1, c0 = T1 * T2, (T1 + T2), 1.0, Kob   # 0.001,0.07,1,18

# Raus jadvali (uncorrected, kuchaytirish = 18)
r_s1 = (c2 * c1 - c3 * c0) / c2                  # 0.0528.../0.07
# Kritik kuchaytirish: c2*c1 = c3*(Kob*Kc) -> Kob*Kc = c2*c1/c3
loop_cr = c2 * c1 / c3                            # 70
Kcu = loop_cr / Kob                               # 3.8889 (rostlagich)
wcr = math.sqrt(loop_cr / c2)                     # 31.6228
Tcr = 2 * math.pi / wcr                           # 0.19869

# ZN klassik PID
Kp_z = 0.6 * Kcu; Ti_z = 0.5 * Tcr; Td_z = 0.125 * Tcr
Ki_z = Kp_z / Ti_z; Kd_z = Kp_z * Td_z

# Tanlangan PD-rostlagich (astatik obyekt uchun)
Kp_d, Kd_d = 1.5, 0.08

# ===========================================================================
# 2) SIMULYATSIYA (RK4)
# ===========================================================================
def step_tf(num, den, tmax=0.8, dt=0.0002):
    n = len(den) - 1
    alpha = [c / den[0] for c in den[1:]]
    b = [0.0] * (n + 1)
    for i, c in enumerate(reversed(num)):
        b[n - i] = c / den[0]
    C = [b[n - i] for i in range(n)]

    def deriv(x, u):
        d = [0.0] * n
        for i in range(n - 1):
            d[i] = x[i + 1]
        s = u
        for i in range(n):
            s -= alpha[n - 1 - i] * x[i]
        d[n - 1] = s
        return d
    x = [0.0] * n; ts = [0.0]; ys = [0.0]; t = 0.0
    for _ in range(int(tmax / dt)):
        k1 = deriv(x, 1.0); x2 = [x[i] + 0.5 * dt * k1[i] for i in range(n)]
        k2 = deriv(x2, 1.0); x3 = [x[i] + 0.5 * dt * k2[i] for i in range(n)]
        k3 = deriv(x3, 1.0); x4 = [x[i] + dt * k3[i] for i in range(n)]
        k4 = deriv(x4, 1.0)
        x = [x[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) for i in range(n)]
        t += dt; ts.append(t); ys.append(sum(C[i] * x[i] for i in range(n)))
    return ts, ys


def metrics(ts, ys, ss=1.0):
    peak = max(ys); tp = ts[ys.index(peak)]
    over = (peak - ss) / ss * 100
    band = 0.05 * ss; tset = ts[-1]
    for i in range(len(ys) - 1, -1, -1):
        if abs(ys[i] - ss) > band:
            tset = ts[min(i + 1, len(ys) - 1)]; break
    # ko'tarilish vaqti 0.1-0.9
    def cr(l):
        for i in range(len(ys)):
            if ys[i] >= l * ss:
                return ts[i]
        return ts[-1]
    return over, tp, tset, cr(0.9) - cr(0.1)


# uncorrected
t_u, y_u = step_tf([Kob], [c3, c2, c1, c0])
m_u = metrics(t_u, y_u)
# ZN-PID:  num=18[Kd,Kp,Ki]; den=[c3,c2,1+18Kd,18Kp,18Ki]
t_z, y_z = step_tf([Kob * Kd_z, Kob * Kp_z, Kob * Ki_z],
                   [c3, c2, 1 + Kob * Kd_z, Kob * Kp_z, Kob * Ki_z])
m_z = metrics(t_z, y_z)
# PD: num=18[Kd,Kp]; den=[c3,c2,1+18Kd,18Kp]
t_d, y_d = step_tf([Kob * Kd_d, Kob * Kp_d], [c3, c2, 1 + Kob * Kd_d, Kob * Kp_d])
m_d = metrics(t_d, y_d)


def pd_margin(Kp, Kd):
    prev = None
    for i in range(8001):
        w = 10 ** (-1 + 4 * i / 8000)
        jw = complex(0, w)
        C = Kp + Kd * jw
        Wp = Kob / (jw * (1 + T1 * jw) * (1 + T2 * jw))
        L = C * Wp
        mag = 20 * math.log10(abs(L)); ph = math.degrees(cmath.phase(L))
        if ph > 0:
            ph -= 360
        if prev and ((prev[0] >= 0 >= mag) or (prev[0] <= 0 <= mag)):
            return w, 180 + ph
        prev = (mag, ph)
    return None, None


wc_d, PM_d = pd_margin(Kp_d, Kd_d)

print("Raus s^1=%.4f  loop_cr=%.1f  Kcu=%.4f  wcr=%.3f  Tcr=%.5f"
      % (r_s1, loop_cr, Kcu, wcr, Tcr))
print("ZN: Kp=%.3f Ki=%.3f Kd=%.5f" % (Kp_z, Ki_z, Kd_z))
print("UNCORR  over=%.1f tp=%.3f tset=%.3f tr=%.3f" % m_u)
print("ZN-PID  over=%.1f tp=%.3f tset=%.3f tr=%.3f" % m_z)
print("PD      over=%.1f tp=%.3f tset=%.3f tr=%.3f" % m_d)
print("PD margin: wc=%.2f PM=%.1f" % (wc_d, PM_d))

# ===========================================================================
# 3) GRAFIKLAR
# ===========================================================================
# --- 2.4-rasm: o'tkinchi jarayonlarni taqqoslash ---
cv1 = Canvas(840, 480)
area = (95, 50, 810, 405)
peak_all = max(max(y_u), max(y_z), max(y_d))
y_hi = math.ceil(peak_all * 10) / 10 + 0.05
curves = [
    {"x": t_u, "y": y_u, "color": ORANGE, "label": "1 - ROSTLAGICHSIZ (P)"},
    {"x": t_z, "y": y_z, "color": RED, "label": "2 - ZN-PID"},
    {"x": t_d, "y": y_d, "color": BLUE, "label": "3 - PD (TANLANGAN)"},
]


draw_multi(cv1, area, curves, (0, 0.8), (0, y_hi),
           title="OTKINCHI JARAYONLAR (OTISH XARAKTERISTIKASI)",
           xlabel="T, S", ylabel="H(T)",
           xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], legend_pos="tr")
# h=1,0 ko'rsatkich chizig'i (turg'unlashgan qiymat)
y1_px = int(round(area[3] - (1.0 / y_hi) * (area[3] - area[1])))
cv1.dashed_hline(area[0], area[2], y1_px, DKGRID)
png_step = cv1.to_png()

# --- 2.5-rasm: ildiz godografi (root locus) ---
cvb = Canvas(800, 560)
areab = (95, 50, 770, 490)
re_r = (-75, 15); im_r = (-45, 45)
mapx, mapy = draw_axes(cvb, areab, re_r, im_r,
                       title="ILDIZ GODOGRAFI (ROOT LOCUS)",
                       xlabel="RE", ylabel="IM",
                       xticks=[-75, -60, -45, -30, -15, 0, 15],
                       yticks=[-45, -30, -15, 0, 15, 30, 45],
                       x0line=True, y0line=True)
# turg'unlik chegarasi (mavhum o'q) qizil punktir
cvb.dashed_vline(int(round(mapx(0))), areab[1], areab[3], RED)
# godograf nuqtalari
Kc_vals = [i / 400.0 * 6.0 for i in range(401)]
for Kc in Kc_vals:
    for r in poly_roots([c3, c2, c1, Kob * Kc]):
        if re_r[0] <= r.real <= re_r[1] and im_r[0] <= r.imag <= im_r[1]:
            cvb.fill_disc(int(round(mapx(r.real))), int(round(mapy(r.imag))), 1, BLUE)
# ochiq tizim qutblari (Kc->0): 0, -20, -50
for p in (0.0, -20.0, -50.0):
    cvb.mark_x(int(round(mapx(p))), int(round(mapy(0))), 5, BLACK)
# kritik nuqtalar (Kc=Kcu): +-j wcr
for sgn in (1, -1):
    cvb.fill_disc(int(round(mapx(0))), int(round(mapy(sgn * wcr))), 4, RED)
cvb.text(mapx(0) + 8, mapy(wcr) - 8, "KCR", RED, 2)
png_rl = cvb.to_png()

# ===========================================================================
# 4) WORD HUJJATI
# ===========================================================================
NSDECL = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
          'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"')
TXT_W = 9355


def esc(t):
    return escape(str(t))


def run(text, bold=False, italic=False, size=28, sub=False, sup=False):
    rpr = ['<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>']
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if sub:
        rpr.append('<w:vertAlign w:val="subscript"/>')
    if sup:
        rpr.append('<w:vertAlign w:val="superscript"/>')
    rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (size, size))
    return "<w:r>" + "".join(rpr) + '<w:t xml:space="preserve">' + esc(text) + "</w:t></w:r>"


def runs_from_parts(parts):
    out = []
    for p in parts:
        out.append(run(p) if isinstance(p, str) else run(p[0], **p[1]))
    return "".join(out)


def para(content, align="both", after=120, before=0, line=360, first=709, left=0, keep=False):
    ppr = ["<w:pPr>"]
    ppr.append('<w:jc w:val="%s"/>' % {"left": "left", "center": "center", "right": "right", "both": "both"}[align])
    ind = []
    if left:
        ind.append('w:left="%d"' % left)
    if first:
        ind.append('w:firstLine="%d"' % first)
    if ind:
        ppr.append('<w:ind %s/>' % " ".join(ind))
    ppr.append('<w:spacing w:before="%d" w:after="%d" w:line="%d" w:lineRule="auto"/>' % (before, after, line))
    if keep:
        ppr.append("<w:keepNext/>")
    ppr.append("</w:pPr>")
    body = runs_from_parts(content) if isinstance(content, list) else (content if content.startswith("<w:") else run(content))
    return "<w:p>" + "".join(ppr) + body + "</w:p>"


def h_section(text):
    return para([(text, {"bold": True, "size": 28})], align="left", before=160, after=120, first=0, keep=True)


def h_sub(text):
    return para([(text, {"bold": True, "italic": True, "size": 28})], align="left", before=120, after=80, first=0, keep=True)


def formula(expr, number=None):
    center = TXT_W // 2
    ppr = ('<w:pPr><w:tabs><w:tab w:val="center" w:pos="%d"/><w:tab w:val="right" w:pos="%d"/></w:tabs>'
           '<w:spacing w:before="80" w:after="80" w:line="360" w:lineRule="auto"/><w:ind w:firstLine="0"/></w:pPr>' % (center, TXT_W))
    num = ('<w:r><w:tab/></w:r>' + run(number)) if number else ""
    return "<w:p>" + ppr + '<w:r><w:tab/></w:r>' + expr + num + "</w:p>"


def caption(text):
    return para([(text, {"italic": True, "size": 24})], align="center", after=60, before=40, first=0)


def cell(text, bold=False, align="left", w=None, shade=None, size=26):
    tcpr = ["<w:tcPr>"]
    if w:
        tcpr.append('<w:tcW w:w="%d" w:type="dxa"/>' % w)
    if shade:
        tcpr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
    tcpr.append('<w:vAlign w:val="center"/></w:tcPr>')
    p = ('<w:p><w:pPr><w:jc w:val="%s"/><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'
         '<w:ind w:firstLine="0"/></w:pPr>%s</w:p>' % (align, run(text, bold=bold, size=size)))
    return "<w:tc>" + "".join(tcpr) + p + "</w:tc>"


def table(rows, widths, aligns=None):
    if aligns is None:
        aligns = ["left"] * len(widths)
    borders = ('<w:tblBorders>' + "".join(
        '<w:%s w:val="single" w:sz="4" w:space="0" w:color="000000"/>' % s
        for s in ("top", "left", "bottom", "right", "insideH", "insideV")) + '</w:tblBorders>')
    tblpr = '<w:tblPr><w:tblW w:w="%d" w:type="dxa"/><w:jc w:val="center"/>%s</w:tblPr>' % (sum(widths), borders)
    grid = "<w:tblGrid>" + "".join('<w:gridCol w:w="%d"/>' % w for w in widths) + "</w:tblGrid>"
    trs = []
    for ri, rc in enumerate(rows):
        head = ri == 0
        trs.append("<w:tr>" + "".join(
            cell(c, bold=head, align=aligns[ci], w=widths[ci], shade="D9D9D9" if head else None)
            for ci, c in enumerate(rc)) + "</w:tr>")
    return ("<w:tbl>" + tblpr + grid + "".join(trs) + "</w:tbl>"
            '<w:p><w:pPr><w:spacing w:after="80" w:line="240" w:lineRule="auto"/></w:pPr></w:p>')


def image_par(relid, did, name, w_px, h_px, disp_cm=14.5):
    cx = int(disp_cm * 360000); cy = int(cx * h_px / w_px)
    d = ('<w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0" '
         'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing">'
         '<wp:extent cx="%d" cy="%d"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
         '<wp:docPr id="%d" name="%s"/><wp:cNvGraphicFramePr>'
         '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
         '</wp:cNvGraphicFramePr><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
         '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
         '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
         '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>'
         '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
         '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
         '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
         '</a:graphicData></a:graphic></wp:inline></w:drawing></w:r>'
         % (cx, cy, did, esc(name), did, esc(name), relid, cx, cy))
    return ('<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="40" w:line="240" w:lineRule="auto"/>'
            '<w:ind w:firstLine="0"/></w:pPr>' + d + '</w:p>')


def num(x, nd=1):
    return (("%." + str(nd) + "f") % x).replace(".", ",")


# --------------------------- MATN -----------------------------------------
B = []
B.append(h_section("2.3. Tizim turg‘unligini va o‘tkinchi jarayonlarni tahlil "
                   "qilish"))
B.append(para(
    "2.2-bo‘limda olingan uzatish funksiyasi asosida boshqaruv tizimining "
    "turg‘unligini baholash, o‘tkinchi jarayonlar sifatini tahlil qilish va "
    "uni yaxshilash uchun rostlagichni sozlash masalalari ko‘rib chiqiladi. "
    "Avval mavzu bo‘yicha ilmiy tadqiqotlar natijalari umumlashtiriladi, "
    "so‘ng Raus–Gurvits mezoni qo‘llaniladi va rostlagich loyihalanadi."))

# 2.3.1 Ilmiy tadqiqotlar
B.append(h_sub("2.3.1. Mavzu bo‘yicha ilmiy tadqiqotlar natijalarining tahlili"))
B.append(para([
    ("Avtomatik boshqaruv tizimlarini sozlashda eng keng tarqalgan usul — "
     "proporsional-integral-differensial (PID) qonuni bo‘lib, uning klassik "
     "sozlash uslubi J. Ziegler va N. Nichols tomonidan 1942-yilda taklif "
     "etilgan [1]. Ushbu usulda rostlagich parametrlari tizimning kritik "
     "kuchaytirishi va avtotebranish davri orqali empirik aniqlanadi. "
     "Tadqiqotlar shuni ko‘rsatadiki, Ziegler–Nichols sozlamasi sodda va "
     "universal bo‘lsa-da, odatda 20–25% atrofida (ba’zan undan ko‘proq) "
     "o‘tib ketish (overshoot) beradi va agressiv hisoblanadi [1, 2].", {}),
]))
B.append(para([
    ("K. Åström va T. Hägglund ishlarida [2] PID-rostlagichni sozlashning "
     "takomillashtirilgan uslublari (rele asosida avtosozlash, robastlik "
     "mezonlari) keltirilgan hamda amaliy loyihalashda faza bo‘yicha zapas "
     "30–60° va amplituda bo‘yicha zapas 6 dB dan katta bo‘lishi tavsiya "
     "etiladi. Astatik (integrallovchi) obyektlar uchun esa V.A. Besekerskiy "
     "va E.P. Popovning klassik ishlarida [3] integral ta’sir tizim "
     "turg‘unligini yomonlashtirishi, differensial ta’sir (PD-qonun) esa "
     "dempflashni oshirib, o‘tib ketishni kamaytirishi ko‘rsatilgan.", {}),
]))
B.append(para([
    ("Metall kesish jarayonini boshqarishga oid tadqiqotlarda Y. Koren [4] "
     "kesish kuchini doimiy darajada ushlab turuvchi adaptiv boshqaruv "
     "tizimlari (Adaptive Control with Constraints) mehnat unumdorligini va "
     "asbob bardoshliligini oshirishini asoslagan. Y. Altintas [5] esa "
     "regenerativ tebranishlar (chatter) va turg‘unlik “loblari” "
     "diagrammasini tahlil qilib, shpindel aylanishi va kesish chuqurligini "
     "tanlashda turg‘unlikni hisobga olish zarurligini ko‘rsatgan. "
     "Ushbu natijalardan kelib chiqib, mazkur ishda turg‘unlik Raus–Gurvits "
     "mezoni bilan baholanadi, rostlagich esa Ziegler–Nichols usuli asosida "
     "boshlang‘ich sozlanib, astatik obyekt xususiyatini hisobga olgan holda "
     "[3] PD-qonun bo‘yicha takomillashtiriladi.", {}),
]))

# 2.3.2 Raus-Gurvits
B.append(h_sub("2.3.2. Turg‘unlikni Raus–Gurvits mezoni bo‘yicha tahlil qilish"))
B.append(para("2.2-bo‘limdagi yopiq tizimning xarakteristik tenglamasi:"))
f1 = (run("0,001·") + run("s", italic=True) + run("3", sup=True) + run(" + 0,07·") +
      run("s", italic=True) + run("2", sup=True) + run(" + ") + run("s", italic=True) +
      run(" + 18 = 0"))
B.append(formula(f1, "(2.14)"))
B.append(para("Uchinchi tartibli tizim uchun Raus jadvali quyidagicha tuziladi "
              "(2.6-jadval). Turg‘unlik sharti — birinchi ustundagi barcha "
              "elementlar musbat bo‘lishi."))
B.append(caption("2.6-jadval. Raus jadvali"))
B.append(table(
    [["Qator", "1-ustun", "2-ustun"],
     ["s³", "0,001", "1"],
     ["s²", "0,07", "18"],
     ["s¹", num(r_s1, 4), "0"],
     ["s⁰", "18", "—"]],
    widths=[2200, 3600, 3555], aligns=["center", "center", "center"]))
B.append(para([
    ("Birinchi ustun elementlari (0,001; 0,07; %s; 18) musbat bo‘lganligi "
     "sababli yopiq tizim turg‘un. Tizim turg‘unligi chegarasida bo‘lishi "
     "uchun s¹ qatori nolga teng bo‘lishi kerak; bundan kontur (halqa) "
     "kuchaytirishining kritik qiymati " % num(r_s1, 4), {}),
    ("K", {"italic": True}),
    ("halqa.kr", {"italic": True, "sub": True}),
    (" = %s, rostlagichning kritik kuchaytirishi esa " % num(loop_cr, 0), {}),
    ("K", {"italic": True}),
    ("kr", {"italic": True, "sub": True}),
    (" = %s kelib chiqadi. Bunga mos avtotebranish chastotasi yordamchi "
     "tenglamadan ω" % num(Kcu, 2), {}),
    ("kr", {"italic": True, "sub": True}),
    (" = %s rad/s, davri esa T" % num(wcr, 1), {}),
    ("kr", {"italic": True, "sub": True}),
    (" = 2π/ω", {}),
    ("kr", {"italic": True, "sub": True}),
    (" = %s s ga teng." % num(Tcr, 3), {}),
]))

# 2.3.3 Rostlagichni sozlash
B.append(h_sub("2.3.3. Rostlagichni sozlash (Ziegler–Nichols va PD-qonun)"))
B.append(para([
    ("Ziegler–Nichols klassik usuli bo‘yicha PID-rostlagich parametrlari "
     "kritik qiymatlar orqali aniqlanadi: ", {}),
    ("K", {"italic": True}), ("p", {"italic": True, "sub": True}),
    (" = 0,6·", {}), ("K", {"italic": True}), ("kr", {"italic": True, "sub": True}),
    ("; T", {"italic": True}), ("i", {"italic": True, "sub": True}),
    (" = 0,5·T", {}), ("kr", {"italic": True, "sub": True}),
    ("; T", {"italic": True}), ("d", {"italic": True, "sub": True}),
    (" = 0,125·T", {}), ("kr", {"italic": True, "sub": True}),
    (". Hisob natijalari 2.7-jadvalda keltirilgan.", {}),
]))
B.append(caption("2.7-jadval. Ziegler–Nichols bo‘yicha PID parametrlari"))
B.append(table(
    [["Parametr", "Formula", "Qiymati"],
     ["Kp", "0,6·Kkr", num(Kp_z, 3)],
     ["Ki = Kp/Ti", "—", num(Ki_z, 2)],
     ["Kd = Kp·Td", "—", num(Kd_z, 4)]],
    widths=[3000, 3000, 3355], aligns=["center", "center", "center"]))
B.append(para([
    ("Biroq boshqaruv obyekti astatik (uzatish funksiyasida integrallovchi "
     "bo‘g‘in — 1/s mavjud) bo‘lganligi sababli, integral ta’sirning "
     "qo‘shilishi tizimni ikkinchi tartibli astatik tizimga aylantiradi va "
     "o‘tib ketishni keskin oshiradi. Simulyatsiya shuni tasdiqladi: "
     "Ziegler–Nichols PID sozlamasida o‘tib ketish σ ≈ %s%% ga yetadi, bu "
     "esa amaliyot uchun ortiqcha. Shu sababli [3] tavsiyalariga muvofiq "
     "differensial ta’sir ustun bo‘lgan PD-rostlagich tanlandi:" % num(m_z[0], 0), {}),
]))
f2 = (run("W", italic=True) + run("r", italic=True, sub=True) + run("(") +
      run("s", italic=True) + run(") = ") + run("K", italic=True) +
      run("p", italic=True, sub=True) + run(" + ") + run("K", italic=True) +
      run("d", italic=True, sub=True) + run("·") + run("s", italic=True) +
      run(" = %s + %s·" % (num(Kp_d, 1), num(Kd_d, 2))) + run("s", italic=True))
B.append(formula(f2, "(2.15)"))

# 2.3.4 O'tkinchi jarayonlar
B.append(h_sub("2.3.4. O‘tkinchi jarayonlarni tahlil qilish"))
B.append(para(
    "Uchala variant — rostlagichsiz (proporsional, 2.2-bo‘lim), "
    "Ziegler–Nichols PID va tanlangan PD-rostlagich — uchun yopiq tizimning "
    "o‘tish xarakteristikalari hisoblanib, 2.4-rasmda taqqoslangan."))
B.append(image_par("rId2", 201, "Otkinchi jarayonlar", 840, 480))
B.append(caption("2.4-rasm. O‘tkinchi jarayonlarni taqqoslash: 1 — rostlagichsiz; "
                 "2 — Ziegler–Nichols PID; 3 — tanlangan PD-rostlagich"))
B.append(caption("2.8-jadval. O‘tkinchi jarayon sifat ko‘rsatkichlarini taqqoslash"))
B.append(table(
    [["Ko‘rsatkich", "Rostlagichsiz", "ZN-PID", "PD (tanlangan)"],
     ["O‘tib ketish σ, %", num(m_u[0], 1), num(m_z[0], 1), num(m_d[0], 1)],
     ["Maksimum vaqti tp, s", num(m_u[1], 3), num(m_z[1], 3), num(m_d[1], 3)],
     ["Ko‘tarilish vaqti tk, s", num(m_u[3], 3), num(m_z[3], 3), num(m_d[3], 3)],
     ["O‘rnashish vaqti tt, s", num(m_u[2], 3), num(m_z[2], 3), num(m_d[2], 3)],
     ["Faza zapasi PM, deg", "39", "—", num(PM_d, 0)]],
    widths=[3400, 2050, 1900, 2005],
    aligns=["left", "center", "center", "center"]))
B.append(para([
    ("Taqqoslashdan ko‘rinadiki, tanlangan PD-rostlagich o‘tib ketishni "
     "rostlagichsiz holatdagi %s%% dan %s%% gacha kamaytirdi va o‘rnashish "
     "vaqtini %s s dan %s s gacha qisqartirdi, faza zapasini esa 39° dan "
     "%s° gacha oshirdi. Ziegler–Nichols PID esa tezkor bo‘lsa-da, %s%% "
     "o‘tib ketish bilan astatik obyekt uchun nomaqbuldir. Demak, PD-qonun "
     "ushbu tizim uchun optimal hisoblanadi."
     % (num(m_u[0], 0), num(m_d[0], 0), num(m_u[2], 2), num(m_d[2], 2),
        num(PM_d, 0), num(m_z[0], 0)), {}),
]))

B.append(para(
    "Tizim turg‘unligining kuchaytirishga bog‘liqligini ko‘rsatish uchun "
    "ildiz godografi (root locus) qurildi (2.5-rasm). Unda kontur "
    "kuchaytirishi 0 dan oshib borishi bilan yopiq tizim qutblarining "
    "kompleks tekislikdagi harakati tasvirlangan."))
B.append(image_par("rId3", 202, "Ildiz godografi", 800, 560))
B.append(caption("2.5-rasm. Tizimning ildiz godografi (× — ochiq tizim "
                 "qutblari; qizil punktir — turg‘unlik chegarasi; "
                 "Kkr — kritik kuchaytirishdagi nuqtalar)"))
B.append(para([
    ("Godografdan ko‘rinadiki, ochiq tizim qutblari (0; −20; −50) dan "
     "boshlangan shoxlar kuchaytirish ortishi bilan harakatlanadi va kritik "
     "kuchaytirish K", {}),
    ("kr", {"italic": True, "sub": True}),
    (" = %s da ikkita shox mavhum o‘qni ±j%s nuqtalarda kesib o‘tadi — bu "
     "turg‘unlik chegarasi. Ish rejimida (kuchaytirish kritikdan kichik) "
     "barcha qutblar chap yarim tekislikda joylashgan, demak tizim turg‘un. "
     "Bu natija Raus–Gurvits mezoni va 2.2-bo‘limdagi amplituda zapasi "
     "(GM ≈ 11,8 dB) bilan to‘liq mos keladi." % (num(Kcu, 2), num(wcr, 1)), {}),
]))

# 2.3.5 Xulosa
B.append(h_sub("2.3.5. Xulosa"))
B.append(para(
    "Bo‘limda tizim turg‘unligi Raus–Gurvits mezoni va ildiz godografi bilan "
    "tahlil qilinib, uning ish rejimida turg‘un ekani (kritik kuchaytirish "
    "Kkr = %s) tasdiqlandi. Ilmiy tadqiqotlar natijalariga [1–3] tayanib "
    "rostlagich sozlandi: astatik obyekt uchun PD-qonun optimal bo‘lib, u "
    "o‘tib ketishni %s%% gacha kamaytirdi, faza zapasini %s° gacha oshirdi "
    "va o‘tkinchi jarayonni sezilarli yaxshiladi. Olingan natijalar boshqaruv "
    "tizimini amaliy joriy etish (3-bobda avtomatlashtirish sxemalarini "
    "loyihalash) uchun asos bo‘ladi."
    % (num(Kcu, 2), num(m_d[0], 0), num(PM_d, 0))))

# Adabiyotlar
B.append(h_sub("Foydalanilgan adabiyotlar (2-bob bo‘yicha)"))
refs = [
    "Ziegler J.G., Nichols N.B. Optimum Settings for Automatic Controllers // "
    "Transactions of the ASME. — 1942. — Vol. 64. — P. 759–768.",
    "Åström K.J., Hägglund T. PID Controllers: Theory, Design, and Tuning. "
    "2nd ed. — Research Triangle Park, NC: ISA, 1995. — 343 p.",
    "Бесекерский В.А., Попов Е.П. Теория систем автоматического "
    "регулирования. — СПб.: Профессия, 2003. — 752 с.",
    "Koren Y. Computer Control of Manufacturing Systems. — New York: "
    "McGraw-Hill, 1983. — 287 p.",
    "Altintas Y. Manufacturing Automation: Metal Cutting Mechanics, Machine "
    "Tool Vibrations, and CNC Design. 2nd ed. — Cambridge: Cambridge "
    "University Press, 2012. — 366 p.",
]
for i, rf in enumerate(refs, 1):
    B.append(para([("%d. " % i, {}), (rf, {})], first=0, left=360, after=60))

# --------------------------- HUJJAT -----------------------------
sect = ('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" '
        'w:left="1701" w:header="708" w:footer="708" w:gutter="0"/>'
        '<w:pgNumType w:start="38"/></w:sectPr>')
document_xml = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<w:document ' + NSDECL + '><w:body>' + "".join(B) + sect + '</w:body></w:document>')

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Default Extension="png" ContentType="image/png"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>')
rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>')
doc_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image1.png"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image2.png"/></Relationships>')
styles_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:styles ' + NSDECL + '><w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="uz-Latn-UZ"/></w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/></w:style></w:styles>')
core_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>2.3 Turgunlik va otkinchi jarayonlar</dc:title>'
    '<dc:creator>Bakalavr dissertatsiyasi</dc:creator><cp:lastModifiedBy>Kiro</cp:lastModifiedBy></cp:coreProperties>')
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
    z.writestr("word/media/image1.png", png_step)
    z.writestr("word/media/image2.png", png_rl)
    z.writestr("docProps/core.xml", core_xml)
    z.writestr("docProps/app.xml", app_xml)

print("Yaratildi:", OUT)
