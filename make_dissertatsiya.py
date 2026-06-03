# -*- coding: utf-8 -*-
"""
Bakalavr dissertatsiyasi MUNDARIJA-sini Word (.docx) hujjati sifatida
yaratuvchi generator.

Mavzu: "Metallni kesish jarayonini avtomatlashtirish" (HT-250 stanogi).

python-docx / pandoc / libreoffice mavjud emasligi sababli, .docx fayl
to'g'ridan-to'g'ri OOXML (Office Open XML) ZIP arxivi sifatida, faqat
Python standart kutubxonasi yordamida yaratiladi. Hosil bo'lgan fayl
Microsoft Word, LibreOffice va Google Docs'da ochiladi.
"""

import zipfile
from xml.sax.saxutils import escape

OUT = "Metallni_kesish_avtomatlashtirish_MUNDARIJA.docx"

# ----------------------------------------------------------------------------
# Yordamchi funksiyalar (OOXML paragraflarini hosil qilish)
# ----------------------------------------------------------------------------

NSDECL = (
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
)


def esc(text):
    return escape(str(text))


def run(text, bold=False, italic=False, size=28, caps=False, color=None):
    """Bitta matn 'run' (w:r) hosil qiladi. size = yarim-punktlar (28 = 14pt)."""
    rpr = ["<w:rPr>"]
    rpr.append('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
               'w:cs="Times New Roman"/>')
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    if caps:
        rpr.append("<w:caps/>")
    if color:
        rpr.append('<w:color w:val="%s"/>' % color)
    rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size))
    rpr.append("</w:rPr>")
    return ("<w:r>" + "".join(rpr) +
            '<w:t xml:space="preserve">' + esc(text) + "</w:t></w:r>")


def para(runs, align="left", spacing_after=120, spacing_before=0,
         line=360, indent_left=0, indent_first=0, keep=False):
    """Paragraf (w:p). line=360 -> 1.5 qatorlar oralig'i (240 = 1.0)."""
    ppr = ["<w:pPr>"]
    jc = {"left": "left", "center": "center", "right": "right",
          "both": "both", "justify": "both"}[align]
    ppr.append('<w:jc w:val="%s"/>' % jc)
    ind = []
    if indent_left:
        ind.append('w:left="%d"' % indent_left)
    if indent_first:
        ind.append('w:firstLine="%d"' % indent_first)
    if ind:
        ppr.append('<w:ind %s/>' % " ".join(ind))
    ppr.append('<w:spacing w:before="%d" w:after="%d" w:line="%d" '
               'w:lineRule="auto"/>' % (spacing_before, spacing_after, line))
    if keep:
        ppr.append("<w:keepNext/>")
    ppr.append("</w:pPr>")
    if isinstance(runs, str):
        runs = [runs]
    return "<w:p>" + "".join(ppr) + "".join(runs) + "</w:p>"


def toc_line(text, page, level=0, bold=False, size=28, caps=False,
             spacing_after=80):
    """
    Mundarija qatori: matn ..... (nuqtali leader) sahifa raqami.
    O'ng tabulyatsiya 9639 twip (~16.8 sm) da, nuqtali to'ldiruvchi bilan.
    """
    left_ind = 0 if level == 0 else 360 + (level - 1) * 360
    ppr = ["<w:pPr>"]
    ppr.append('<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9639"/></w:tabs>')
    if left_ind:
        ppr.append('<w:ind w:left="%d"/>' % left_ind)
    ppr.append('<w:spacing w:before="0" w:after="%d" w:line="276" '
               'w:lineRule="auto"/>' % spacing_after)
    ppr.append("</w:pPr>")
    r_text = run(text, bold=bold, size=size, caps=caps)
    r_tab = '<w:r><w:tab/></w:r>'
    r_page = run(str(page), bold=bold, size=size)
    return "<w:p>" + "".join(ppr) + r_text + r_tab + r_page + "</w:p>"


def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'


def empty(n=1):
    return "".join('<w:p><w:pPr><w:spacing w:after="0" w:line="360" '
                   'w:lineRule="auto"/></w:pPr></w:p>' for _ in range(n))


# ----------------------------------------------------------------------------
# Hujjat tarkibi
# ----------------------------------------------------------------------------

body = []

# ===== TITUL VARAQ =====
body.append(para([run("O‘ZBEKISTON RESPUBLIKASI", bold=True, size=24)],
                 align="center", spacing_after=0))
body.append(para([run("OLIY TA’LIM, FAN VA INNOVATSIYALAR VAZIRLIGI",
                      bold=True, size=24)], align="center", spacing_after=0))
body.append(para([run("___________________ TEXNIKA UNIVERSITETI",
                      bold=True, size=24)], align="center", spacing_after=240))
body.append(para([run("“Mashinasozlik texnologiyasi” kafedrasi", size=24)],
                 align="center", spacing_after=0))
body.append(empty(4))
body.append(para([run("BAKALAVR BITIRUV MALAKAVIY ISHI", bold=True, size=32)],
                 align="center", spacing_after=120))
body.append(para([run("(DISSERTATSIYA)", bold=True, size=24)],
                 align="center", spacing_after=360))
body.append(para([run("Mavzu:", bold=True, size=28)],
                 align="center", spacing_after=60))
body.append(para([run("“METALLNI KESISH JARAYONINI AVTOMATLASHTIRISH",
                      bold=True, size=30)], align="center", spacing_after=0))
body.append(para([run("(HT-250 stanogi misolida)”", bold=True, size=30)],
                 align="center", spacing_after=360))
body.append(empty(3))
body.append(para([run("Bajardi: ______________________________", size=28)],
                 align="right", indent_left=0, spacing_after=60))
body.append(para([run("Ilmiy rahbar: __________________________", size=28)],
                 align="right", spacing_after=60))
body.append(para([run("“Himoyaga ruxsat etildi”", size=24)],
                 align="right", spacing_after=0))
body.append(para([run("Kafedra mudiri: ________________________", size=28)],
                 align="right", spacing_after=360))
body.append(empty(3))
body.append(para([run("Toshkent — 2026", bold=True, size=28)],
                 align="center", spacing_after=0))
body.append(page_break())

# ===== MUNDARIJA SARLAVHASI =====
body.append(para([run("MUNDARIJA", bold=True, size=32)],
                 align="center", spacing_after=240, spacing_before=120))

# Mundarija tuzilishi: (matn, sahifa, daraja, bold, caps)
toc = [
    ("KIRISH", 4, 0, True, False),

    ("I BOB. TEXNOLOGIK QISM", 7, 0, True, False),
    ("1.1. Detalning xizmat vazifasi va texnik tavsifi", 7, 1, False, False),
    ("1.2. Material tanlash va uning mexanik xossalari", 9, 1, False, False),
    ("1.3. HT-250 stanogi: tuzilishi, texnik tavsifi va imkoniyatlari",
     11, 1, False, False),
    ("1.4. Zagotovka turini tanlash va asoslash", 14, 1, False, False),
    ("1.5. Metallni kesishning texnologik jarayoni (marshrut)", 16, 1, False, False),
    ("1.6. Kesuvchi asbob va texnologik jihozlarni tanlash", 19, 1, False, False),

    ("II BOB. HISOBIY QISM", 22, 0, True, False),
    ("2.1. Kesish rejimlari, kesish kuchlari va quvvatini hisoblash",
     22, 1, False, False),
    ("2.2. Kesish jarayonining matematik modelini tuzish", 27, 1, False, False),
    ("2.3. Boshqaruv tizimini avtomatik boshqarish nazariyasi "
     "(control theory) asosida hisoblash", 32, 1, False, False),
    ("2.4. Tizim turg‘unligini va o‘tkinchi jarayonlarni tahlil qilish "
     "(PID-rostlagichni sozlash)", 38, 1, False, False),

    ("III BOB. AVTOMATLASHTIRISH SXEMALARINI LOYIHALASH", 43, 0, True, False),
    ("3.1. Avtomatlashtirish darajasi va tamoyillari", 43, 1, False, False),
    ("3.2. Boshqaruv tizimi tarkibi (ChPU/CNC, PLK)", 45, 1, False, False),
    ("3.3. Datchiklar va o‘lchash-nazorat tizimlari", 48, 1, False, False),
    ("3.4. Yuritmalarni (servo, qadamli dvigatel) tanlash", 51, 1, False, False),
    ("3.5. Funksional va prinsipial sxemalarni ishlab chiqish", 54, 1, False, False),
    ("3.6. Boshqaruv dasturi algoritmi (G-kod) va modellashtirish", 57, 1, False, False),

    ("IV BOB. HAYOT FAOLIYATI XAVFSIZLIGI", 61, 0, True, False),
    ("4.1. Ish joyini tashkil etish va ergonomika", 61, 1, False, False),
    ("4.2. Elektr xavfsizligi", 63, 1, False, False),
    ("4.3. Mexanik xavfsizlik va himoya vositalari", 65, 1, False, False),
    ("4.4. Sanitariya-gigiyena sharoitlari (yoritish, shovqin, mikroiqlim)",
     67, 1, False, False),
    ("4.5. Yong‘in xavfsizligi va atrof-muhitni muhofaza qilish", 69, 1, False, False),

    ("V BOB. IQTISODIY SAMARADORLIK", 72, 0, True, False),
    ("5.1. Loyihaning kapital xarajatlarini hisoblash", 72, 1, False, False),
    ("5.2. Mahsulot tannarxini hisoblash", 74, 1, False, False),
    ("5.3. Avtomatlashtirishdan olinadigan iqtisodiy samara", 76, 1, False, False),
    ("5.4. Loyihaning o‘zini oqlash (qoplanish) muddati", 78, 1, False, False),
    ("5.5. Asosiy texnik-iqtisodiy ko‘rsatkichlar", 80, 1, False, False),

    ("XULOSA VA TAKLIFLAR", 82, 0, True, False),
    ("FOYDALANILGAN ADABIYOTLAR", 84, 0, True, False),
    ("ILOVALAR", 87, 0, True, False),
]

for text, page, level, bold, caps in toc:
    body.append(toc_line(text, page, level=level, bold=bold,
                         size=28 if level == 0 else 28,
                         caps=False,
                         spacing_after=120 if level == 0 else 60))

# ----------------------------------------------------------------------------
# document.xml
# ----------------------------------------------------------------------------

sect = (
    '<w:sectPr>'
    '<w:pgSz w:w="11906" w:h="16838"/>'                      # A4
    '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" '   # 2/1.5/2/3 sm
    'w:left="1701" w:header="708" w:footer="708" w:gutter="0"/>'
    '<w:pgNumType w:start="1"/>'
    '</w:sectPr>'
)

document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<w:document ' + NSDECL + '>'
    '<w:body>' + "".join(body) + sect + '</w:body></w:document>'
)

# ----------------------------------------------------------------------------
# Statik OOXML qismlar
# ----------------------------------------------------------------------------

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
    '<w:styles ' + NSDECL + '>'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="uz-Latn-UZ"/>'
    '</w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/><w:qFormat/></w:style>'
    '</w:styles>'
)

core_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<cp:coreProperties '
    'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" '
    'xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:title>Metallni kesish jarayonini avtomatlashtirish - Mundarija</dc:title>'
    '<dc:creator>Bakalavr dissertatsiyasi</dc:creator>'
    '<cp:lastModifiedBy>Kiro</cp:lastModifiedBy>'
    '</cp:coreProperties>'
)

app_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
    '<Application>Kiro OOXML Generator</Application></Properties>'
)

# ----------------------------------------------------------------------------
# ZIP (.docx) yozish
# ----------------------------------------------------------------------------

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("docProps/core.xml", core_xml)
    z.writestr("docProps/app.xml", app_xml)

print("Yaratildi:", OUT)
