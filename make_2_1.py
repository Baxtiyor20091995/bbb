# -*- coding: utf-8 -*-
"""
II BOB. HISOBIY QISM — 2.1-bo'lim to'liq matni (Word .docx).

"2.1. Kesish rejimlari, kesish kuchlari va quvvatini hisoblash.
Kesish jarayonining matematik modelini tuzish va tahlil qilish
(HT-250 stanogi ma'lumotlari hisobga olingan holda)."

.docx fayl faqat Python standart kutubxonasi (zipfile + OOXML) yordamida
yaratiladi. MS Word, LibreOffice, Google Docs'da ochiladi.
"""

import zipfile
from xml.sax.saxutils import escape

OUT = "2.1_Kesish_rejimlari_va_matematik_model.docx"

NSDECL = (
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
)

# Sahifaning foydali kengligi (twip): 11906 - 1701(chap) - 850(o'ng) = 9355
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
    """parts: list of (text, {opts}) yoki oddiy str."""
    out = []
    for p in parts:
        if isinstance(p, str):
            out.append(run(p))
        else:
            txt, opts = p
            out.append(run(txt, **opts))
    return "".join(out)


def para(content, align="both", after=120, before=0, line=360,
         first=709, left=0, keep=False):
    ppr = ["<w:pPr>"]
    jc = {"left": "left", "center": "center", "right": "right",
          "both": "both"}[align]
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
    if isinstance(content, list) and content and isinstance(content[0], (tuple, str)):
        body = runs_from_parts(content)
    elif isinstance(content, str):
        body = content if content.startswith("<w:r") else run(content)
    else:
        body = "".join(content)
    return "<w:p>" + "".join(ppr) + body + "</w:p>"


def h_chapter(text):
    return para([(text, {"bold": True, "size": 32})], align="center",
                before=120, after=200, first=0)


def h_section(text):
    return para([(text, {"bold": True, "size": 28})], align="left",
                before=160, after=120, first=0, keep=True)


def h_sub(text):
    return para([(text, {"bold": True, "italic": True, "size": 28})],
                align="left", before=120, after=80, first=0, keep=True)


def formula(expr_runs, number=None):
    """Markazlashtirilgan formula + o'ngda raqami. expr_runs: runs str."""
    center = TXT_W // 2
    ppr = ('<w:pPr><w:tabs>'
           '<w:tab w:val="center" w:pos="%d"/>'
           '<w:tab w:val="right" w:pos="%d"/>'
           '</w:tabs><w:spacing w:before="80" w:after="80" w:line="360" '
           'w:lineRule="auto"/><w:ind w:firstLine="0"/></w:pPr>' %
           (center, TXT_W))
    tab = '<w:r><w:tab/></w:r>'
    num = (tab + run(number) if number else "")
    return "<w:p>" + ppr + tab + expr_runs + num + "</w:p>"


def empty(n=1):
    return "".join('<w:p><w:pPr><w:spacing w:after="0" w:line="360" '
                   'w:lineRule="auto"/></w:pPr></w:p>' for _ in range(n))


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


# ----- Jadval -----
def cell(text_or_runs, bold=False, align="left", w=None, shade=None, size=26):
    tcpr = ["<w:tcPr>"]
    if w:
        tcpr.append('<w:tcW w:w="%d" w:type="dxa"/>' % w)
    if shade:
        tcpr.append('<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade)
    tcpr.append('<w:vAlign w:val="center"/></w:tcPr>')
    if isinstance(text_or_runs, str):
        rr = run(text_or_runs, bold=bold, size=size)
    else:
        rr = text_or_runs
    p = ('<w:p><w:pPr><w:jc w:val="%s"/>'
         '<w:spacing w:before="20" w:after="20" w:line="240" '
         'w:lineRule="auto"/><w:ind w:firstLine="0"/></w:pPr>%s</w:p>' %
         (align, rr))
    return "<w:tc>" + "".join(tcpr) + p + "</w:tc>"


def table(rows, widths, header=True, aligns=None):
    """rows: list of list (str yoki runs). widths: list[int] (twip)."""
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
    tblpr = ('<w:tblPr><w:tblW w:w="%d" w:type="dxa"/>'
             '<w:jc w:val="center"/>%s</w:tblPr>' % (sum(widths), borders))
    grid = "<w:tblGrid>" + "".join('<w:gridCol w:w="%d"/>' % w for w in widths) + "</w:tblGrid>"
    trs = []
    for ri, rowcells in enumerate(rows):
        is_head = header and ri == 0
        tcs = []
        for ci, c in enumerate(rowcells):
            tcs.append(cell(c, bold=is_head, align=aligns[ci],
                            w=widths[ci],
                            shade="D9D9D9" if is_head else None,
                            size=26))
        trs.append("<w:tr>" + "".join(tcs) + "</w:tr>")
    return "<w:tbl>" + tblpr + grid + "".join(trs) + "</w:tbl>" + \
        '<w:p><w:pPr><w:spacing w:after="80" w:line="240" w:lineRule="auto"/></w:pPr></w:p>'


def caption(text):
    return para([(text, {"italic": True, "size": 24})], align="right",
                after=40, first=0)


# ============================================================================
# MATN
# ============================================================================
B = []

B.append(h_chapter("II BOB. HISOBIY QISM"))
B.append(h_section("2.1. Kesish rejimlari, kesish kuchlari va quvvatini "
                   "hisoblash. Kesish jarayonining matematik modelini tuzish"))

# --- Kirish ---
B.append(para(
    "Kesish rejimlari — kesish chuqurligi t, surilish S va kesish tezligi V — "
    "metallni kesib ishlash jarayonining asosiy boshqariluvchi parametrlari "
    "hisoblanadi. Ushbu parametrlar detal sifatini (o‘lchamlar aniqligi va "
    "yuza g‘adir-budurligi), mehnat unumdorligini, asbobning bardoshliligini "
    "va energiya sarfini bevosita belgilaydi. Jarayonni avtomatlashtirish, "
    "ya’ni uni raqamli dasturiy boshqaruv (ChPU) tizimi orqali boshqarish "
    "uchun avvalo kesish jarayonining matematik modelini tuzish, rejimlarni "
    "tahliliy hisoblash va olingan natijalarni HT-250 stanogining texnik "
    "imkoniyatlari bilan moslashtirish talab etiladi."))

B.append(para(
    "Mazkur bo‘limda kesish jarayonining matematik modeli statik (rejimlar) "
    "ko‘rinishida tuziladi: kirish ta’sirlari (t, S, V), chiqish kattaliklari "
    "(kesish kuchi Pz, kesish quvvati Ne, buramomant Mkr) va stanok "
    "imkoniyatlaridan kelib chiqadigan cheklovlar o‘zaro bog‘lanadi. Bu model "
    "keyinchalik 2.3-bo‘limda boshqaruv tizimini avtomatik boshqarish "
    "nazariyasi (control theory) asosida hisoblashda ish nuqtasi atrofida "
    "chiziqlilashtirish uchun asos bo‘lib xizmat qiladi."))

# --- 2.1.1 Matematik model ---
B.append(h_sub("2.1.1. Kesish jarayonining matematik modeli"))
B.append(para(
    "Yo‘nish (tokarlik) jarayonining matematik modeli quyidagi tenglamalar "
    "tizimi ko‘rinishida ifodalanadi. Kinematik bog‘lanish kesish tezligi V "
    "(m/min), zagotovka diametri D (mm) va shpindel aylanish chastotasi n "
    "(ayl/min) orasidagi munosabatni beradi:"))

# Formula (2.1): V = pi*D*n/1000
f21 = (run("V", italic=True) + run(" = ") +
       run("π·D·n", italic=True) + run(" / 1000"))
B.append(formula(f21, "(2.1)"))
f22 = (run("n", italic=True) + run(" = 1000·") + run("V", italic=True) +
       run(" / (π·") + run("D", italic=True) + run(")"))
B.append(formula(f22, "(2.2)"))

B.append(para(
    "Iqtisodiy jihatdan maqbul kesish tezligi asbob bardoshliligi T (min) "
    "bo‘yicha empirik (eksponensial) model orqali aniqlanadi:"))
# (2.3) V = Cv/(T^m * t^xv * S^yv) * Kv
f23 = (run("V", italic=True) + run(" = ") + run("C", italic=True) +
       run("v", italic=True, sub=True) +
       run(" / ( ") + run("T", italic=True) + run("m", sup=True) +
       run(" · ") + run("t", italic=True) + run("xv", sup=True) +
       run(" · ") + run("S", italic=True) + run("yv", sup=True) +
       run(" ) · ") + run("K", italic=True) + run("v", italic=True, sub=True))
B.append(formula(f23, "(2.3)"))
B.append(para([
    ("bu yerda ", {}),
    ("Cv", {"italic": True}),
    (" — material va ishlov sharoitiga bog‘liq koeffitsiyent; ", {}),
    ("m, xv, yv", {"italic": True}),
    (" — darajalar ko‘rsatkichlari; ", {}),
    ("Kv", {"italic": True}),
    (" — umumiy tuzatish koeffitsiyenti (material, asbob va yuza holatini "
     "hisobga oluvchi koeffitsiyentlar ko‘paytmasi).", {}),
], first=0))

B.append(para(
    "Kesishning bosh (urinma) tashkil etuvchisi — kesish kuchi Pz (N) "
    "eksponensial model bilan hisoblanadi:"))
# (2.4) Pz = 10*Cp*t^xp*S^yp*V^np*Kp
f24 = (run("P", italic=True) + run("z", italic=True, sub=True) +
       run(" = 10·") + run("C", italic=True) + run("p", italic=True, sub=True) +
       run(" · ") + run("t", italic=True) + run("xp", sup=True) +
       run(" · ") + run("S", italic=True) + run("yp", sup=True) +
       run(" · ") + run("V", italic=True) + run("np", sup=True) +
       run(" · ") + run("K", italic=True) + run("p", italic=True, sub=True))
B.append(formula(f24, "(2.4)"))
B.append(para(
    "Kesish kuchining radial Py va o‘qiy Px tashkil etuvchilari ham shunga "
    "o‘xshash ko‘rinishda, o‘z koeffitsiyentlari bilan aniqlanadi. Hisoblashda "
    "asosiy e’tibor Pz ga qaratiladi, chunki aynan u kesish quvvati va "
    "buramomantni belgilaydi."))

B.append(para("Kesish quvvati Ne (kVt) va shpindeldagi buramomant Mkr (N·m):"))
# (2.5) Ne = Pz*V/(60*1000)
f25 = (run("N", italic=True) + run("e", italic=True, sub=True) +
       run(" = ") + run("P", italic=True) + run("z", italic=True, sub=True) +
       run(" · ") + run("V", italic=True) + run(" / (60 · 1000)"))
B.append(formula(f25, "(2.5)"))
# (2.6) Mkr = Pz*D/(2*1000)
f26 = (run("M", italic=True) + run("kr", italic=True, sub=True) +
       run(" = ") + run("P", italic=True) + run("z", italic=True, sub=True) +
       run(" · ") + run("D", italic=True) + run(" / (2 · 1000)"))
B.append(formula(f26, "(2.6)"))

B.append(para("Mehnat unumdorligini baholash uchun material olib tashlash "
              "tezligi Q (mm³/min) va bir o‘tishdagi asosiy (mashina) vaqt "
              "To (min) hisoblanadi:"))
# (2.7) Q = 1000*V*S*t
f27 = (run("Q", italic=True) + run(" = 1000·") + run("V", italic=True) +
       run(" · ") + run("S", italic=True) + run(" · ") + run("t", italic=True))
B.append(formula(f27, "(2.7)"))
# (2.8) To = L/(n*S)
f28 = (run("T", italic=True) + run("o", italic=True, sub=True) +
       run(" = ") + run("L", italic=True) + run(" / (") + run("n", italic=True) +
       run(" · ") + run("S", italic=True) + run("),   ") +
       run("L", italic=True) + run(" = ") + run("l", italic=True) +
       run(" + ") + run("l", italic=True) + run("1", sub=True) +
       run(" + ") + run("l", italic=True) + run("2", sub=True))
B.append(formula(f28, "(2.8)"))

B.append(para(
    "Matematik modelning chegaraviy (cheklov) shartlari aynan HT-250 "
    "stanogining texnik xususiyatlaridan kelib chiqadi va hisoblangan rejim "
    "amalda bajarilishi mumkinligini kafolatlaydi:"))
# Cheklovlar
fc1 = (run("n", italic=True) + run("min", sub=True) + run(" ≤ ") +
       run("n", italic=True) + run(" ≤ ") + run("n", italic=True) +
       run("max", sub=True))
B.append(formula(fc1, "(2.9)"))
fc2 = (run("N", italic=True) + run("e", italic=True, sub=True) + run(" ≤ ") +
       run("N", italic=True) + run("shp", sub=True) + run(" = ") +
       run("N", italic=True) + run("dv", sub=True) + run(" · η"))
B.append(formula(fc2, "(2.10)"))
B.append(para([
    ("ya’ni hisoblangan aylanishlar chastotasi stanok shpindeli "
     "diapazonida bo‘lishi (2.9), kesish quvvati esa shpindeldagi mavjud "
     "quvvatdan (yuritma quvvati ", {}),
    ("Ndv", {"italic": True}),
    (" va FIK ", {}),
    ("η", {"italic": True}),
    (" ko‘paytmasi) oshmasligi shart (2.10).", {}),
], first=0))

# --- 2.1.2 Kirish ma'lumotlari ---
B.append(h_sub("2.1.2. Hisoblash uchun dastlabki ma’lumotlar"))
B.append(para(
    "Hisoblashga misol sifatida HT-250 stanogida po‘lat 45 (GOST 1050) "
    "materialidan tayyorlangan val tipidagi detalga bo‘ylama yo‘nish "
    "(qora ishlov) operatsiyasi qabul qilinadi. Kesuvchi asbob — T15K6 "
    "qattiq qotishmali yo‘nish keskichi. Stanokning texnik ko‘rsatkichlari "
    "1.3-bo‘limda keltirilgan bo‘lib, hisob uchun zarur qismi 2.1-jadvalda "
    "berilgan."))

B.append(caption("2.1-jadval. HT-250 stanogining hisob uchun zarur texnik "
                 "ko‘rsatkichlari"))
B.append(table(
    [["Ko‘rsatkich", "Belgisi", "Qiymati"],
     ["Stanina ustida ishlov beriladigan eng katta diametr", "—", "400 mm"],
     ["Markazlar orasidagi eng katta masofa", "—", "750 mm"],
     ["Shpindel aylanishlari diapazoni", "n", "20…2000 ayl/min"],
     ["Surilishlar diapazoni (bo‘ylama)", "S", "0,05…2,8 mm/ayl"],
     ["Bosh harakat yuritmasi quvvati", "Ndv", "7,5 kVt"],
     ["Stanok foydali ish koeffitsiyenti (FIK)", "η", "0,80"]],
    widths=[5400, 1400, 2555],
    aligns=["left", "center", "center"]))
B.append(para([
    ("Eslatma: ", {"bold": True, "italic": True}),
    ("2.1-jadvaldagi qiymatlar ushbu sinf stanoklari uchun xos bo‘lib, yakuniy "
     "ishda HT-250 stanogining texnik pasporti bo‘yicha aniqlashtirilishi "
     "shart.", {"italic": True}),
], first=0, after=120))

B.append(caption("2.2-jadval. Detal materiali, asbob va kesish rejimi "
                 "bo‘yicha dastlabki ma’lumotlar"))
B.append(table(
    [["Parametr", "Belgisi", "Qiymati"],
     ["Detal materiali", "—", "Po‘lat 45 (σв ≈ 750 MPa, HB ≈ 207)"],
     ["Kesuvchi asbob", "—", "T15K6 qattiq qotishma; φ = 45°"],
     ["Zagotovka (boshlang‘ich) diametri", "D", "60 mm"],
     ["Ishlov uzunligi", "l", "200 mm"],
     ["Kesish chuqurligi", "t", "2,0 mm"],
     ["Surilish", "S", "0,3 mm/ayl"],
     ["Asbob bardoshliligi", "T", "60 min"]],
    widths=[3800, 1400, 4155],
    aligns=["left", "center", "left"]))

# --- 2.1.3 Hisoblash ---
B.append(h_sub("2.1.3. Kesish rejimlari, kuch va quvvatni hisoblash"))
B.append(para([
    ("1) Kesish tezligi (2.3-formula). Koeffitsiyentlar mashinasozlik "
     "texnologi ma’lumotnomasidan qabul qilinadi: ", {}),
    ("Cv", {"italic": True}), (" = 350; ", {}),
    ("m", {"italic": True}), (" = 0,20; ", {}),
    ("xv", {"italic": True}), (" = 0,15; ", {}),
    ("yv", {"italic": True}), (" = 0,35; ", {}),
    ("Kv", {"italic": True}), (" = 1,0:", {}),
]))
f_v = (run("V", italic=True) + run(" = 350 / (60") + run("0,20", sup=True) +
       run(" · 2") + run("0,15", sup=True) + run(" · 0,3") +
       run("0,35", sup=True) + run(") = 350 / (2,268·1,110·0,656) ≈ 212 m/min"))
B.append(formula(f_v))

B.append(para("2) Shpindel aylanish chastotasi (2.2-formula):"))
f_n = (run("n", italic=True) + run(" = 1000·212 / (π·60) ≈ 1125 ayl/min"))
B.append(formula(f_n))
B.append(para([
    ("Stanokda mavjud diskret qatordan eng yaqin qiymat qabul qilinadi: ", {}),
    ("n", {"italic": True}),
    ("d", {"italic": True, "sub": True}),
    (" = 1000 ayl/min. Bu qiymat 2.9-cheklov shartini qanoatlantiradi "
     "(20 ≤ 1000 ≤ 2000). Qabul qilingan chastota bo‘yicha haqiqiy kesish "
     "tezligi qayta hisoblanadi:", {}),
]))
f_vr = (run("V", italic=True) + run("haq", sub=True) +
        run(" = π·60·1000 / 1000 ≈ 188,5 m/min"))
B.append(formula(f_vr))

B.append(para([
    ("3) Kesish kuchi (2.4-formula). Koeffitsiyentlar: ", {}),
    ("Cp", {"italic": True}), (" = 300; ", {}),
    ("xp", {"italic": True}), (" = 1,0; ", {}),
    ("yp", {"italic": True}), (" = 0,75; ", {}),
    ("np", {"italic": True}), (" = −0,15; ", {}),
    ("Kp", {"italic": True}), (" ≈ 1,0:", {}),
]))
f_pz = (run("P", italic=True) + run("z", italic=True, sub=True) +
        run(" = 10·300·2,0") + run("1,0", sup=True) + run(" · 0,3") +
        run("0,75", sup=True) + run(" · 188,5") + run("−0,15", sup=True) +
        run(" ≈ 1108 N"))
B.append(formula(f_pz))

B.append(para("4) Kesish quvvati (2.5-formula):"))
f_ne = (run("N", italic=True) + run("e", italic=True, sub=True) +
        run(" = 1108 · 188,5 / (60·1000) ≈ 3,48 kVt"))
B.append(formula(f_ne))

B.append(para("5) Shpindeldagi buramomant (2.6-formula):"))
f_m = (run("M", italic=True) + run("kr", italic=True, sub=True) +
       run(" = 1108 · 60 / (2·1000) ≈ 33,3 N·m"))
B.append(formula(f_m))

B.append(para("6) Material olib tashlash tezligi (2.7) va bir o‘tishdagi "
              "asosiy vaqt (2.8); o‘tish uzunligi L = 200 + 5 = 205 mm:"))
f_q = (run("Q", italic=True) + run(" = 1000·188,5·0,3·2,0 ≈ 113 100 mm³/min "
                                   "≈ 113 sm³/min"))
B.append(formula(f_q))
f_to = (run("T", italic=True) + run("o", italic=True, sub=True) +
        run(" = 205 / (1000·0,3) ≈ 0,68 min ≈ 41 s"))
B.append(formula(f_to))

# --- Natijalar jadvali ---
B.append(caption("2.3-jadval. Kesish rejimlari va hisob natijalari"))
B.append(table(
    [["Kattalik", "Belgisi", "Qiymati", "O‘lchami"],
     ["Kesish chuqurligi", "t", "2,0", "mm"],
     ["Surilish", "S", "0,3", "mm/ayl"],
     ["Hisobiy kesish tezligi", "V", "212", "m/min"],
     ["Qabul qilingan shpindel chastotasi", "nd", "1000", "ayl/min"],
     ["Haqiqiy kesish tezligi", "Vhaq", "188,5", "m/min"],
     ["Kesish kuchi", "Pz", "1108", "N"],
     ["Kesish quvvati", "Ne", "3,48", "kVt"],
     ["Buramomant", "Mkr", "33,3", "N·m"],
     ["Material olib tashlash tezligi", "Q", "113", "sm³/min"],
     ["Bir o‘tish asosiy vaqti", "To", "0,68", "min"]],
    widths=[4200, 1300, 2155, 1700],
    aligns=["left", "center", "center", "center"]))

# --- 2.1.4 Tahlil ---
B.append(h_sub("2.1.4. Natijalarning tahlili"))
B.append(para([
    ("1. Quvvat bo‘yicha tekshirish (2.10-cheklov). Stanok shpindelidagi "
     "foydali quvvat ", {}),
    ("Nshp", {"italic": True}),
    (" = Ndv·η = 7,5·0,80 = 6,0 kVt. Hisoblangan kesish quvvati Ne = 3,48 kVt "
     "shu chegaradan kichik, demak shart bajariladi: 3,48 < 6,0 kVt. "
     "Quvvatdan foydalanish koeffitsiyenti η_N = Ne/Nshp = 0,58, ya’ni stanok "
     "quvvatining 58% i ishlatiladi. Bu zaxira surilish yoki kesish "
     "chuqurligini oshirish hisobiga unumdorlikni yana ko‘tarish mumkinligini "
     "ko‘rsatadi.", {}),
], first=0))

B.append(para(
    "2. Tezlik va chastota bo‘yicha. Hisobiy tezlik (212 m/min) stanokning "
    "diskret aylanishlar qatoriga moslab 188,5 m/min gacha kamaytirildi. "
    "Bu tafovut (≈11%) asbob bardoshliligini biroz oshiradi, ammo iqtisodiy "
    "rejimdan jiddiy chetlanish hisoblanmaydi. ChPU bilan jihozlangan HT-250 "
    "da uzluksiz tezlik rostlash imkoni bo‘lsa, aynan hisobiy qiymat (212 "
    "m/min) o‘rnatilishi mumkin."))

B.append(para([
    ("3. Modelning sezgirligi (tahliliy baho). (2.4) modeldan ko‘rinadiki, "
     "kesish kuchi Pz kesish chuqurligiga deyarli to‘g‘ri proporsional "
     "(daraja ko‘rsatkichi xp = 1,0), surilishga kuchsizroq (yp = 0,75), "
     "tezlikka esa teskari va juda sust bog‘langan (np = −0,15). Shu sababli "
     "unumdorlikni (Q) oshirishda ", {}),
    ("t", {"italic": True}),
    (" va ", {}),
    ("S", {"italic": True}),
    (" ni oshirish quvvat va kuchni sezilarli ko‘taradi, ", {}),
    ("V", {"italic": True}),
    (" ni oshirish esa kuchga kam ta’sir qiladi, lekin asbob bardoshligini "
     "keskin kamaytiradi. Bu xulosa avtomatik boshqaruvda rejim "
     "optimallashtirish mezonini tanlashda hisobga olinadi.", {}),
], first=0))

B.append(para([
    ("4. Avtomatlashtirish bilan bog‘liqlik. Hisoblangan ish nuqtasi "
     "(V₀ = 188,5 m/min, S₀ = 0,3 mm/ayl, t₀ = 2,0 mm, Pz₀ ≈ 1108 N) kesish "
     "jarayonini avtomatik boshqarish tizimi uchun nominal (statik) rejim "
     "bo‘lib xizmat qiladi. 2.3-bo‘limda aynan shu nuqta atrofida (2.3) va "
     "(2.4) bog‘lanishlar chiziqlilashtirilib, jarayonning uzatish funksiyasi "
     "olinadi va PID-rostlagich sozlanadi. Shunday qilib, statik model "
     "dinamik (control theory) model uchun zarur boshlang‘ich ma’lumotlarni "
     "beradi.", {}),
], first=0))

B.append(para(
    "Xulosa qilib aytganda, tuzilgan matematik model kesish rejimlarini "
    "tahliliy aniqlash va ularni HT-250 stanogining quvvat hamda kinematika "
    "cheklovlari bilan moslashtirish imkonini berdi. Olingan rejim "
    "(t = 2,0 mm, S = 0,3 mm/ayl, n = 1000 ayl/min) stanok imkoniyatlariga "
    "to‘liq mos keladi, quvvat zaxirasini saqlaydi va jarayonni "
    "avtomatlashtirish uchun ishonchli asos yaratadi."))

# ----------------------------------------------------------------------------
# Hujjatni yig'ish
# ----------------------------------------------------------------------------
sect = (
    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" '
    'w:left="1701" w:header="708" w:footer="708" w:gutter="0"/>'
    '<w:pgNumType w:start="22"/></w:sectPr>'
)

document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document ' + NSDECL + '><w:body>' + "".join(B) + sect +
    '</w:body></w:document>'
)

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
    '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
    '</Types>'
)

rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
    '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
    '</Relationships>'
)

doc_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '</Relationships>'
)

styles_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:styles ' + NSDECL + '><w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="uz-Latn-UZ"/>'
    '</w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/><w:qFormat/></w:style></w:styles>'
)

core_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<cp:coreProperties '
    'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/">'
    '<dc:title>2.1. Kesish rejimlari va matematik model</dc:title>'
    '<dc:creator>Bakalavr dissertatsiyasi</dc:creator>'
    '<cp:lastModifiedBy>Kiro</cp:lastModifiedBy></cp:coreProperties>'
)

app_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    '<Application>Kiro OOXML Generator</Application></Properties>'
)

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("docProps/core.xml", core_xml)
    z.writestr("docProps/app.xml", app_xml)

print("Yaratildi:", OUT)
