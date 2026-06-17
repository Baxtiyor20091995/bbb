# -*- coding: utf-8 -*-
"""
Generates a master's-level scientific article (Uzbek) as a .docx file,
with embedded bar charts (PNG) and tables. Uses ONLY the Python standard
library (zlib, zipfile, struct) - no external dependencies.
"""
import os, struct, zlib, zipfile, html

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA = []  # list of (filename, bytes)

# ----------------------------------------------------------------------------
# 5x7 bitmap font (uppercase + digits + symbols) for chart labels
# ----------------------------------------------------------------------------
FONT = {
 'A':[" ### ","#   #","#   #","#####","#   #","#   #","#   #"],
 'B':["#### ","#   #","#   #","#### ","#   #","#   #","#### "],
 'C':[" ### ","#   #","#    ","#    ","#    ","#   #"," ### "],
 'D':["#### ","#   #","#   #","#   #","#   #","#   #","#### "],
 'E':["#####","#    ","#    ","#### ","#    ","#    ","#####"],
 'F':["#####","#    ","#    ","#### ","#    ","#    ","#    "],
 'G':[" ### ","#   #","#    ","# ###","#   #","#   #"," ### "],
 'H':["#   #","#   #","#   #","#####","#   #","#   #","#   #"],
 'I':["#####","  #  ","  #  ","  #  ","  #  ","  #  ","#####"],
 'J':["  ###","   # ","   # ","   # ","#  # ","#  # "," ##  "],
 'K':["#   #","#  # ","# #  ","##   ","# #  ","#  # ","#   #"],
 'L':["#    ","#    ","#    ","#    ","#    ","#    ","#####"],
 'M':["#   #","## ##","# # #","#   #","#   #","#   #","#   #"],
 'N':["#   #","##  #","# # #","#  ##","#   #","#   #","#   #"],
 'O':[" ### ","#   #","#   #","#   #","#   #","#   #"," ### "],
 'P':["#### ","#   #","#   #","#### ","#    ","#    ","#    "],
 'Q':[" ### ","#   #","#   #","#   #","# # #","#  # "," ## #"],
 'R':["#### ","#   #","#   #","#### ","# #  ","#  # ","#   #"],
 'S':[" ####","#    ","#    "," ### ","    #","    #","#### "],
 'T':["#####","  #  ","  #  ","  #  ","  #  ","  #  ","  #  "],
 'U':["#   #","#   #","#   #","#   #","#   #","#   #"," ### "],
 'V':["#   #","#   #","#   #","#   #","#   #"," # # ","  #  "],
 'W':["#   #","#   #","#   #","#   #","# # #","## ##","#   #"],
 'X':["#   #","#   #"," # # ","  #  "," # # ","#   #","#   #"],
 'Y':["#   #","#   #"," # # ","  #  ","  #  ","  #  ","  #  "],
 'Z':["#####","    #","   # ","  #  "," #   ","#    ","#####"],
 '0':[" ### ","#   #","#  ##","# # #","##  #","#   #"," ### "],
 '1':["  #  "," ##  ","  #  ","  #  ","  #  ","  #  ","#####"],
 '2':[" ### ","#   #","    #","   # ","  #  "," #   ","#####"],
 '3':["#####","   # ","  #  ","   # ","    #","#   #"," ### "],
 '4':["   # ","  ## "," # # ","#  # ","#####","   # ","   # "],
 '5':["#####","#    ","#### ","    #","    #","#   #"," ### "],
 '6':[" ### ","#    ","#    ","#### ","#   #","#   #"," ### "],
 '7':["#####","    #","   # ","  #  "," #   "," #   "," #   "],
 '8':[" ### ","#   #","#   #"," ### ","#   #","#   #"," ### "],
 '9':[" ### ","#   #","#   #"," ####","    #","    #"," ### "],
 '%':["##  #","##  #","   # ","  #  "," #   ","#  ##","#  ##"],
 '.':["     ","     ","     ","     ","     "," ##  "," ##  "],
 ',':["     ","     ","     ","     ","  ## ","  ## ","  #  "],
 '-':["     ","     ","     ","#####","     ","     ","     "],
 '(':["   # ","  #  "," #   "," #   "," #   ","  #  ","   # "],
 ')':[" #   ","  #  ","   # ","   # ","   # ","  #  "," #   "],
 '/':["    #","    #","   # ","  #  "," #   ","#    ","#    "],
 '+':["     ","  #  ","  #  ","#####","  #  ","  #  ","     "],
 ':':["     ","  #  ","  #  ","     ","  #  ","  #  ","     "],
 ' ':["     ","     ","     ","     ","     ","     ","     "],
}

# ----------------------------------------------------------------------------
# Simple RGB canvas
# ----------------------------------------------------------------------------
class Canvas:
    def __init__(self, w, h, bg=(255,255,255)):
        self.w, self.h = w, h
        self.buf = bytearray()
        row = bytes(bg) * w
        for _ in range(h):
            self.buf += row

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y*self.w + x)*3
            self.buf[i:i+3] = bytes(c)

    def rect(self, x0, y0, x1, y1, c):
        if x1 < x0: x0, x1 = x1, x0
        if y1 < y0: y0, y1 = y1, y0
        for y in range(int(y0), int(y1)+1):
            for x in range(int(x0), int(x1)+1):
                self.px(x, y, c)

    def hline(self, x0, x1, y, c):
        for x in range(int(x0), int(x1)+1):
            self.px(x, int(y), c)

    def vline(self, x, y0, y1, c):
        for y in range(int(y0), int(y1)+1):
            self.px(int(x), y, c)

    def text(self, x, y, s, c=(0,0,0), scale=2):
        cx = x
        for ch in s.upper():
            g = FONT.get(ch, FONT[' '])
            for ry, rowstr in enumerate(g):
                for rx, p in enumerate(rowstr):
                    if p == '#':
                        for sy in range(scale):
                            for sx in range(scale):
                                self.px(cx+rx*scale+sx, y+ry*scale+sy, c)
            cx += (5*scale + scale)  # 1px spacing scaled

    def text_w(self, s, scale=2):
        return len(s) * (5*scale + scale)

    def to_png(self):
        raw = bytearray()
        for y in range(self.h):
            raw.append(0)  # filter type 0
            i = y*self.w*3
            raw += self.buf[i:i+self.w*3]
        comp = zlib.compress(bytes(raw), 9)
        def chunk(typ, data):
            c = typ + data
            return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xffffffff)
        png = b"\x89PNG\r\n\x1a\n"
        png += chunk(b"IHDR", struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0))
        png += chunk(b"IDAT", comp)
        png += chunk(b"IEND", b"")
        return bytes(png)

# ----------------------------------------------------------------------------
# Vertical grouped bar chart
# ----------------------------------------------------------------------------
def bar_chart(title, categories, series, ymax, colors, ylabel="%"):
    """series: list of (name, [values per category])"""
    W, H = 900, 560
    cv = Canvas(W, H)
    # title
    tw = cv.text_w(title, 3)
    cv.text((W-tw)//2, 18, title, (20,20,20), 3)
    # plot area
    L, R, T, B = 90, W-30, 70, H-110
    # axes
    cv.vline(L, T, B, (60,60,60))
    cv.hline(L, R, B, (60,60,60))
    # y gridlines + labels
    steps = 5
    for s in range(steps+1):
        val = ymax*s/steps
        yy = B - (B-T)*s/steps
        cv.hline(L, R, yy, (220,220,220))
        cv.text(L-70, int(yy)-7, ("%.0f" % val), (90,90,90), 2)
    cv.vline(L, T, B, (60,60,60))
    cv.hline(L, R, B, (60,60,60))
    # bars
    ncat = len(categories)
    nser = len(series)
    group_w = (R-L)/ncat
    bar_w = group_w*0.7/nser
    for ci, cat in enumerate(categories):
        gx = L + group_w*ci + group_w*0.15
        for si,(name,vals) in enumerate(series):
            v = vals[ci]
            bx0 = gx + si*bar_w
            bx1 = bx0 + bar_w*0.9
            bh = (B-T)*v/ymax
            by0 = B - bh
            cv.rect(bx0, by0, bx1, B-1, colors[si])
            lbl = ("%.1f" % v)
            cv.text(int((bx0+bx1)/2 - cv.text_w(lbl,2)/2), int(by0)-18, lbl, (30,30,30), 2)
        # category label
        clbl = cat
        cv.text(int(gx + (group_w*0.7)/2 - cv.text_w(clbl,2)/2), B+12, clbl, (30,30,30), 2)
    # legend
    if nser > 1:
        lx = L+10; ly = T-2
        for si,(name,vals) in enumerate(series):
            cv.rect(lx, ly, lx+22, ly+16, colors[si])
            cv.text(lx+30, ly+1, name, (40,40,40), 2)
            lx += 40 + cv.text_w(name,2)
    # ylabel
    cv.text(8, T-30, ylabel, (90,90,90), 2)
    return cv.to_png()

# ----------------------------------------------------------------------------
# Build charts (REAL data from cited literature)
# ----------------------------------------------------------------------------
# Fig 1: urban vegetation phytoremediation reduction ranges (npj Urban Sust. 2023)
png1 = bar_chart(
    "1-RASM. SHAHAR USIMLIKLARINING IFLOSLANTIRUVCHI MODDALARNI KAMAYTIRISHI",
    ["PM", "NOX", "SO2"],
    [("MIN", [16.5, 13.9, 20.5]), ("MAX", [26.7, 36.2, 47.8])],
    60, [(110,170,90),(40,110,60)], ylabel="%")
MEDIA.append(("chart1.png", png1))

# Fig 2: PM2.5 reduction by green-system type (CFD study, pedestrian level)
png2 = bar_chart(
    "2-RASM. YASHIL TIZIM TURI BOYICHA PM2.5 KAMAYISHI",
    ["DEVOR", "TOM", "TOSIQ"],
    [("PM2.5", [14.6, 4.6, 7.4])],
    20, [(70,130,180)], ylabel="%")
MEDIA.append(("chart2.png", png2))

# Fig 3: active (botanical) green-wall maximum removal efficiency (review 2024)
png3 = bar_chart(
    "3-RASM. FAOL YASHIL DEVOR MAKSIMAL SAMARADORLIGI",
    ["VOC", "PM", "CO2"],
    [("MAX", [96.3, 65.4, 4.8])],
    100, [(200,120,60)], ylabel="%")
MEDIA.append(("chart3.png", png3))

print("charts generated:", [m[0] for m in MEDIA])
print("sizes:", [len(m[1]) for m in MEDIA])



# ============================================================================
# DOCX BUILDER (pure stdlib, OOXML)
# ============================================================================
EMU_PER_PX = 9525
PAGE_W_DXA = 12240   # 8.5in * 1440
MARGIN_DXA = 1440    # 1in
USABLE_DXA = PAGE_W_DXA - 2*MARGIN_DXA  # 9360

def esc(t):
    return html.escape(t, quote=False)

BODY = []          # list of XML strings (paragraphs/tables)
RELS_IMG = []      # (rId, target)
_img_counter = [0]

def run(text, bold=False, italic=False, size=24, font="Times New Roman", color=None):
    rpr = "<w:rPr>"
    rpr += '<w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>' % (font,font,font)
    if bold: rpr += "<w:b/>"
    if italic: rpr += "<w:i/>"
    if color: rpr += '<w:color w:val="%s"/>' % color
    rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size,size)
    rpr += "</w:rPr>"
    return '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, esc(text))

def para(runs_xml, align="both", spacing_after=120, spacing_line=276, indent_first=0, keep=False):
    ppr = "<w:pPr>"
    if keep: ppr += "<w:keepNext/>"
    ppr += '<w:spacing w:after="%d" w:line="%d" w:lineRule="auto"/>' % (spacing_after, spacing_line)
    if indent_first: ppr += '<w:ind w:firstLine="%d"/>' % indent_first
    ppr += '<w:jc w:val="%s"/>' % align
    ppr += "</w:pPr>"
    return "<w:p>%s%s</w:p>" % (ppr, runs_xml)

def p_text(text, **kw):
    align = kw.pop("align","both")
    sa = kw.pop("spacing_after",120)
    indent = kw.pop("indent_first",360)
    BODY.append(para(run(text, **kw), align=align, spacing_after=sa, indent_first=indent))

def heading(text, level=1):
    size = 30 if level==1 else 26
    BODY.append(para(run(text, bold=True, size=size), align="left",
                     spacing_after=120, indent_first=0, keep=True))

def title_block(text):
    BODY.append(para(run(text, bold=True, size=32), align="center",
                     spacing_after=180, indent_first=0))

def caption(text):
    BODY.append(para(run(text, italic=True, size=20), align="center",
                     spacing_after=160, indent_first=0))

def add_image(filename, disp_w_in=6.0):
    # source pixel size 900x560 (charts) -> aspect
    px_w, px_h = 900, 560
    cx = int(disp_w_in * 914400)
    cy = int(cx * px_h / px_w)
    _img_counter[0] += 1
    rid = "rIdImg%d" % _img_counter[0]
    RELS_IMG.append((rid, "media/%s" % filename))
    docpr_id = 100 + _img_counter[0]
    drawing = (
      '<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="60"/></w:pPr><w:r><w:drawing>'
      '<wp:inline distT="0" distB="0" distL="0" distR="0">'
      '<wp:extent cx="%d" cy="%d"/>' % (cx, cy) +
      '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
      '<wp:docPr id="%d" name="Picture %d"/>' % (docpr_id, docpr_id) +
      '<wp:cNvGraphicFramePr><a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/></wp:cNvGraphicFramePr>'
      '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
      '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
      '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
      '<pic:nvPicPr><pic:cNvPr id="%d" name="%s"/><pic:cNvPicPr/></pic:nvPicPr>' % (docpr_id, filename) +
      '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>' % rid +
      '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>' % (cx, cy) +
      '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
      '</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>'
    )
    BODY.append(drawing)

def add_table(headers, rows, col_widths=None, fontsize=20):
    n = len(headers)
    if col_widths is None:
        col_widths = [USABLE_DXA//n]*n
    grid = "".join('<w:gridCol w:w="%d"/>' % w for w in col_widths)
    def cell(text, w, bold=False, shade=None, align="left"):
        tcpr = '<w:tcPr><w:tcW w:w="%d" w:type="dxa"/>' % w
        if shade: tcpr += '<w:shd w:val="clear" w:color="auto" w:fill="%s"/>' % shade
        tcpr += '<w:vAlign w:val="center"/></w:tcPr>'
        rpr = '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
        if bold: rpr += "<w:b/>"
        rpr += '<w:sz w:val="%d"/><w:szCs w:val="%d"/></w:rPr>' % (fontsize,fontsize)
        p = ('<w:p><w:pPr><w:spacing w:after="20" w:line="240" w:lineRule="auto"/>'
             '<w:jc w:val="%s"/></w:pPr>' % align +
             '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>' % (rpr, esc(text)))
        return "<w:tc>%s%s</w:tc>" % (tcpr, p)
    borders = ('<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="666666"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="999999"/>'
        '</w:tblBorders>')
    tblpr = ('<w:tblPr><w:tblW w:w="%d" w:type="dxa"/>' % sum(col_widths) +
             '<w:jc w:val="center"/>%s'
             '<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="80" w:type="dxa"/>'
             '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar>'
             '</w:tblPr>' % borders)
    hrow = "<w:tr><w:trPr><w:tblHeader/></w:trPr>" + "".join(
        cell(h, col_widths[i], bold=True, shade="D9E2D9", align="center") for i,h in enumerate(headers)) + "</w:tr>"
    body_rows = ""
    for r in rows:
        body_rows += "<w:tr>" + "".join(
            cell(str(c), col_widths[i], align=("center" if i>0 and len(str(c))<14 else "left")) for i,c in enumerate(r)) + "</w:tr>"
    BODY.append('<w:tbl>%s<w:tblGrid>%s</w:tblGrid>%s%s</w:tbl>' % (tblpr, grid, hrow, body_rows))
    BODY.append(para(run("", size=8), spacing_after=60, indent_first=0))

# ============================================================================
# ARTICLE CONTENT (Uzbek)
# ============================================================================
title_block("Shahar ekotizimlarida biologik qoplamalar yordamida havo "
            "ifloslanishini kamaytirish usullarini tadqiq etish")

BODY.append(para(run("Magistrlik ilmiy maqolasi", italic=True, size=22), align="center", spacing_after=60, indent_first=0))
BODY.append(para(run("Yo'nalish: Ekologiya va atrof-muhit muhofazasi", size=22), align="center", spacing_after=200, indent_first=0))

# Annotatsiya
heading("Annotatsiya", 2)
p_text("Ushbu maqolada shahar ekotizimlarida havo ifloslanishini kamaytirishda "
       "biologik qoplamalar (moxli biofiltrlar, yashil devorlar va fasadlar, mikroalgali "
       "fotobioreaktorlar hamda lishaynik asosidagi biomonitoring tizimlari)dan foydalanish "
       "usullari tahlil qilingan. Tadqiqotda jahon ilmiy adabiyotidagi dala va laboratoriya "
       "natijalari umumlashtirilib, turli biologik tizimlarning chang (PM), azot oksidlari (NOx), "
       "oltingugurt dioksidi (SO2) va uchuvchan organik birikmalar (VOC)ni yutish samaradorligi "
       "qiyosiy baholangan. Natijalar shuni ko'rsatadiki, shahar o'simliklari ifloslantiruvchi "
       "moddalar konsentratsiyasini 14-48% gacha kamaytirishi, faol (ventilyatsiyali) yashil "
       "devorlar esa ayrim moddalar bo'yicha 90% dan ortiq samaradorlikka erishishi mumkin. "
       "Maqolada bu yondashuvlarning O'zbekiston shaharlari, jumladan Toshkent sharoitida "
       "qo'llanilishi istiqbollari ham muhokama qilingan.", indent_first=0)
p_text("Kalit so'zlar: biologik qoplama, havo ifloslanishi, shahar ekotizimi, yashil devor, "
       "moxli biofiltr, mikroalga, fotobioreaktor, lishaynik, biomonitoring, PM2.5, NOx, "
       "fitoremediatsiya.", bold=False, italic=True, indent_first=0)

# 1. Kirish
heading("1. Kirish", 2)
p_text("Urbanizatsiya jadallashuvi bilan shaharlarda havo sifatining yomonlashuvi jahon "
       "miqyosidagi eng dolzarb ekologik va tibbiy muammolardan biriga aylandi. Jahon sog'liqni "
       "saqlash tashkiloti (JSST) ma'lumotlariga ko'ra, atmosfera havosi ifloslanishi har yili "
       "taxminan 4,2 million erta o'limga sabab bo'lmoqda, dunyo aholisining qariyb 99 foizi esa "
       "JSST belgilagan me'yorlardan oshib ketgan ifloslangan havodan nafas olmoqda. Avtotransport, "
       "sanoat korxonalari, isitish tizimlari va qurilish faoliyati natijasida atmosferaga chiqarilayotgan "
       "qattiq zarrachalar (PM2.5 va PM10), azot oksidlari, oltingugurt dioksidi va uchuvchan organik "
       "birikmalar shahar aholisining nafas olish va yurak-qon tomir kasalliklari xavfini sezilarli "
       "darajada oshiradi.")
p_text("An'anaviy muhandislik yechimlari (filtrlash inshootlari, transportni cheklash, yoqilg'i "
       "standartlarini qattiqlashtirish) zarur, biroq ular ko'pincha qimmat va ifloslanishning "
       "manbasiga yo'naltirilgan bo'ladi. So'nggi yillarda esa tabiatga asoslangan yechimlar "
       "(nature-based solutions), xususan biologik qoplamalar yordamida havoni tozalash yondashuvi "
       "tobora ko'proq e'tibor qozonmoqda. Biologik qoplamalar deganda tirik organizmlar - yuksak "
       "o'simliklar, mox, lishaynik, mikroskopik suvo'tlar (mikroalga) va mikrobiologik "
       "birliklardan tashkil topgan, bino yuzalari, ko'cha infratuzilmasi yoki maxsus qurilmalarga "
       "o'rnatiladigan faol qatlamlar tushuniladi. Ushbu qatlamlar ifloslantiruvchi moddalarni "
       "yuza adsorbtsiyasi, barg/tallom orqali yutilishi (assimilyatsiya) hamda mikrobiologik "
       "parchalanish mexanizmlari orqali ushlab qoladi.")
p_text("Ushbu maqolaning maqsadi - shahar ekotizimlarida biologik qoplamalar yordamida havo "
       "ifloslanishini kamaytirishning zamonaviy usullarini tizimli tahlil qilish, ularning "
       "samaradorligini real ilmiy tadqiqotlar asosida qiyoslash va O'zbekiston shaharlari uchun "
       "amaliy tavsiyalar ishlab chiqishdir.")

# 2. Materiallar va usullar
heading("2. Tadqiqot materiallari va usullari", 2)
p_text("Tadqiqot tahliliy-umumlashtiruvchi (sistematik adabiyot tahlili) usuliga asoslangan. "
       "2008-2025 yillarda nufuzli xalqaro jurnallarda (Nature/npj Urban Sustainability, MDPI "
       "Atmosphere, IJERPH, Buildings, Urban Science, Frontiers in Built Environment, Environmental "
       "Pollution) hamda Yevropa Ittifoqining ilmiy loyihalari hisobotlarida (CORDIS/Horizon 2020) "
       "e'lon qilingan dala va laboratoriya tadqiqotlari to'plandi. Tanlangan manbalarda biologik "
       "qoplamalarning quyidagi ko'rsatkichlari tahlil qilindi: ifloslantiruvchi modda turi, "
       "kamayish samaradorligi (foizda), tizim turi (passiv yoki faol) va o'lchov sharoiti (dala/laboratoriya). "
       "Olingan miqdoriy ma'lumotlar qiyosiy jadvallar va diagrammalar ko'rinishida umumlashtirildi.")



# 3. Biologik qoplamalar turlari
heading("3. Biologik qoplamalar turlari va ta'sir mexanizmlari", 2)
p_text("Shahar sharoitida qo'llaniladigan biologik qoplamalarni ta'sir mexanizmi va konstruksiyasiga "
       "ko'ra besh asosiy guruhga ajratish mumkin. Ularning umumiy tavsifi 1-jadvalda keltirilgan.")

add_table(
    ["Qoplama turi", "Asosiy organizm", "Yutiladigan moddalar", "Asosiy mexanizm"],
    [
     ["Moxli biofiltr", "Mox (Bryophyta)", "PM2.5, PM10, CO2", "Yuza adsorbtsiyasi, IoT bilan faol havo haydash"],
     ["Yashil devor / fasad", "Yuksak o'simliklar", "PM, NOx, VOC, CO2", "Barg yuzasiga cho'kish va assimilyatsiya"],
     ["Mikroalgali fotobioreaktor", "Mikroalga (Chlorella va b.)", "CO2, NOx", "Fotosintez orqali biofiksatsiya"],
     ["Lishaynik tizimi", "Lishaynik (simbioz)", "Og'ir metallar, N, S", "Akkumulyatsiya, biomonitoring"],
     ["Biologik tuproq qatlami", "Mox-suvo't-mikrob", "Chang, ozuqa moddalari", "Yuzani barqarorlashtirish, changni ushlash"],
    ],
    col_widths=[2200, 2200, 2480, 2480])
caption("1-jadval. Shahar ekotizimlarida qo'llaniladigan biologik qoplamalarning asosiy turlari")

heading("3.1. Moxli biofiltrlar", 3)
p_text("Mox o'zining juda katta solishtirma yuzasi va kutikulasiz tuzilishi tufayli havodagi mayda "
       "chang zarralarini samarali ushlab qoladi. Germaniyaning Green City Solutions kompaniyasi "
       "ishlab chiqqan CityTree va MossTree qurilmalari moxni Internet of Things (IoT) texnologiyasi "
       "bilan birlashtirib, havoni faol ravishda qatlam orqali haydaydi va namlikni avtomatik nazorat "
       "qiladi. Yevropa Ittifoqining Horizon 2020 doirasidagi MossTree loyihasi (grant 847744) natijalariga "
       "ko'ra, mox asosidagi filtrlar shahar 'issiq nuqtalari'da mayda changni o'lchanadigan darajada "
       "kamaytirishi mumkin. Qozog'istonda o'tkazilgan dala tadqiqoti ham mox asosidagi biotexnologik "
       "tozalash filtri ochiq havodagi ifloslantiruvchi moddalar miqdorini pasaytirishini tasdiqlagan.")

heading("3.2. Yashil devorlar va fasadlar", 3)
p_text("Yashil devorlar passiv (tabiiy shamollatishga tayanadigan) va faol (havoni majburiy ravishda "
       "o'simlik ildiz-substrat qatlamidan o'tkazadigan) turlarga bo'linadi. Hisoblash gidrodinamikasi "
       "(CFD) modellashtirishi shuni ko'rsatadiki, 25-75% qamrovga ega yashil devorlar piyodalar "
       "darajasidagi PM2.5 konsentratsiyasini taxminan 14-15% ga, yashil tomlar 3,7-5,5% ga, jonli "
       "to'siqlar (hedge) esa 2,7-12% ga kamaytiradi. Faol (botanik biofiltratsiyali) yashil devorlar "
       "ancha yuqori ko'rsatkich beradi: Chlorophytum comosum va Sansevieria trifasciata kabi turlardan "
       "foydalanilganda VOC bo'yicha 96% gacha, chang bo'yicha 65% gacha samaradorlikka erishilgan.")

# Figure 1
add_image("chart1.png")
caption("1-rasm. Shahar o'simliklarining ifloslantiruvchi moddalarni kamaytirish diapazoni "
        "(manba: npj Urban Sustainability, 2023): PM 16,5-26,7%, NOx 13,9-36,2%, SO2 20,5-47,8%.")

# Figure 2
add_image("chart2.png")
caption("2-rasm. Yashil tizim turi bo'yicha PM2.5 ning piyodalar darajasidagi o'rtacha kamayishi "
        "(CFD tadqiqoti asosida): yashil devor ~14,6%, yashil tom ~4,6%, jonli to'siq ~7,4%.")

heading("3.3. Mikroalgali fotobioreaktorli fasadlar", 3)
p_text("Mikroalgalar fotosintez jarayonida atmosferadagi CO2 ni yuqori samaradorlik bilan "
       "biomassaga aylantiradi. Shaffof panellarga (fotobioreaktorlarga) joylangan mikroalga "
       "binoning fasadiga integratsiya qilinadi va bir vaqtning o'zida soyalash, issiqlik izolyatsiyasi "
       "hamda biomassa ishlab chiqarish vazifalarini bajaradi. Gamburgdagi BIQ House (2013) bunday "
       "'jonli fasad'ga ega birinchi turar-joy binosi sifatida tanilgan. Universidad de Alcala (Ispaniya) "
       "tomonidan ishlab chiqilgan mikroalgali fasad yiliga 720 kg gacha CO2 ni biriktirib, 400 kg "
       "biomassa hosil qila olishi qayd etilgan; bunday biomassa keyinchalik o'g'it sifatida ishlatilishi mumkin.")

heading("3.4. Lishaynik va biologik monitoring", 3)
p_text("Lishayniklar (zamburug' va suvo't yoki sianobakteriya simbiozi) havo sifatining tabiiy "
       "ko'rsatkichlari (bioindikatorlari) hisoblanadi. Ular havodagi og'ir metallar, azot va "
       "oltingugurt birikmalarini to'planti tarzida yutadi, shu sababli ularning tarkibi va tur "
       "tarqalishi shahar havosining ifloslanish darajasini arzon va keng qamrovli baholashga imkon "
       "beradi. Lishayniklardagi uglerod, azot va oltingugurt miqdori hamda izotop nisbati shahar "
       "markazlaridagi havo sifatini yuqori fazoviy aniqlikda kartalashtirish uchun ishlatilmoqda. "
       "Shu bilan birga lishayniklar ifloslanishga juda sezgir bo'lganligi tufayli ular bevosita "
       "tozalovchi emas, balki monitoring va erta ogohlantirish vositasi sifatida qiymatga ega.")

# 4. Qiyosiy tahlil
heading("4. Samaradorlikning qiyosiy tahlili", 2)
p_text("To'plangan ma'lumotlar tahlili biologik qoplamalar samaradorligi tizim turiga, qamrov "
       "darajasiga va o'lchov sharoitiga kuchli bog'liqligini ko'rsatadi. 2-jadvalda turli "
       "tizimlarning asosiy ifloslantiruvchi moddalar bo'yicha kamaytirish samaradorligi "
       "umumlashtirilgan.")

add_table(
    ["Tizim turi", "Modda", "Kamayish (%)", "Sharoit", "Manba"],
    [
     ["Shahar o'simliklari (umumiy)", "PM", "16,5-26,7", "Dala/meta-tahlil", "npj Urban Sust., 2023"],
     ["Shahar o'simliklari (umumiy)", "NOx", "13,9-36,2", "Dala/meta-tahlil", "npj Urban Sust., 2023"],
     ["Shahar o'simliklari (umumiy)", "SO2", "20,5-47,8", "Dala/meta-tahlil", "npj Urban Sust., 2023"],
     ["Yashil devor (25-75%)", "PM2.5", "14,2-15,0", "CFD modeli", "HRPub, CFD study"],
     ["Yashil tom", "PM2.5", "3,7-5,5", "CFD modeli", "HRPub, CFD study"],
     ["Jonli to'siq (hedge)", "PM2.5", "2,7-12,0", "CFD modeli", "HRPub, CFD study"],
     ["Faol yashil devor", "VOC", "96,3 gacha", "Laboratoriya", "Preprints review, 2024"],
     ["Faol yashil devor", "PM", "65,4 gacha", "Laboratoriya", "Preprints review, 2024"],
     ["Faol yashil devor", "CO2", "4,8 gacha", "Laboratoriya", "Preprints review, 2024"],
    ],
    col_widths=[2700, 1300, 1700, 1860, 1800], fontsize=18)
caption("2-jadval. Biologik/yashil tizimlarning ifloslantiruvchi moddalarni kamaytirish samaradorligi")

# Figure 3
add_image("chart3.png")
caption("3-rasm. Faol (ventilyatsiyali, botanik) yashil devorning maksimal kamaytirish samaradorligi: "
        "VOC 96,3%, PM 65,4%, CO2 4,8% (manba: Preprints, 2024 sharhi).")

p_text("Tahlil natijalari uch muhim xulosani ko'rsatadi. Birinchidan, passiv tizimlar (an'anaviy yashil "
       "tomlar, jonli to'siqlar) ko'cha darajasida nisbatan kichik, ammo barqaror samara beradi. "
       "Ikkinchidan, faol tizimlar (IoT-li moxli biofiltrlar va ventilyatsiyali yashil devorlar) birlik "
       "yuzaga nisbatan ancha yuqori samaradorlikka ega, biroq energiya va texnik xizmatni talab qiladi. "
       "Uchinchidan, mikroalgali fasadlar birinchi navbatda CO2 ni biriktirish va energiya tejashda "
       "ustun bo'lsa-da, qattiq zarrachalarni bevosita ushlashda yetakchi emas. Real loyihalar ko'rsatkichlari "
       "3-jadvalda jamlangan.")

add_table(
    ["Loyiha / tizim", "Joylashuv", "Asosiy ko'rsatkich"],
    [
     ["CityTree / MossTree", "Yevropa shaharlari", "IoT-li moxli biofiltr, mayda changni ushlash"],
     ["BIQ House (SolarLeaf)", "Gamburg, Germaniya", "Birinchi mikroalgali fasadli bino (2013)"],
     ["Mikroalgali fasad (UAH)", "Ispaniya", "~720 kg CO2/yil, ~400 kg biomassa/yil"],
     ["Botanik biofiltratsiya", "Yo'l yoqasi (dala)", "Yo'l yoqasidagi ifloslanishni sezilarli kamaytirish"],
     ["Lishaynik biomonitoringi", "Shahar markazlari", "Og'ir metall, N, S kartalashtirish"],
    ],
    col_widths=[2700, 2660, 4000], fontsize=19)
caption("3-jadval. Biologik qoplamalardan foydalangan real loyihalar va ularning ko'rsatkichlari")

# 5. Muhokama
heading("5. Muhokama: O'zbekiston shaharlari uchun istiqbollar", 2)
p_text("O'zbekiston shaharlari, ayniqsa Toshkent, qishki mavsumda inversiya hodisalari, avtotransport "
       "zichligi va chang bo'ronlari tufayli yuqori PM2.5 va PM10 darajalari bilan ajralib turadi. "
       "Mintaqaning quruq va issiq iqlimi biologik qoplamalarni tanlashda suv resurslarini tejovchi "
       "yondashuvni taqozo etadi. Shu nuqtai nazardan moxli biofiltrlar va qurg'oqchilikka chidamli "
       "o'simliklarga asoslangan yashil devorlar eng istiqbolli yechim hisoblanadi, chunki ular kichik "
       "maydonda yuqori tozalash samarasini beradi va yopiq suv aylanma tizimi bilan jihozlanishi mumkin.")
p_text("Amaliy joriy etishda quyidagi bosqichlar tavsiya etiladi: (1) eng ifloslangan kesishmalar va "
       "ko'chalarni lishaynik biomonitoringi yordamida aniqlash; (2) shu nuqtalarga moxli biofiltrlar "
       "yoki faol yashil devorlarni pilot tarzda o'rnatish; (3) mahalliy mox, suvo't va qurg'oqchilikka "
       "chidamli o'simlik turlarini sinovdan o'tkazish; (4) samaradorlikni avtomatik havo sifati "
       "sensorlari bilan uzluksiz baholash. Bunday bosqichli yondashuv investitsiyalarni eng katta "
       "ekologik foyda beradigan joylarga yo'naltirishga imkon beradi.")
p_text("Shu bilan birga biologik qoplamalar ifloslanish manbasini bartaraf etmaydi va faqat to'ldiruvchi "
       "chora hisoblanadi. Eng yaxshi natija ularning transportni boshqarish, yashil energiyaga o'tish "
       "va shaharsozlik rejalashtirishi bilan birgalikda qo'llanilishida erishiladi.")

# 6. Xulosa
heading("6. Xulosa", 2)
p_text("Tahlil shuni ko'rsatdiki, biologik qoplamalar shahar ekotizimlarida havo sifatini "
       "yaxshilashning iqtisodiy va ekologik jihatdan istiqbolli vositasidir. Shahar o'simliklari "
       "ifloslantiruvchi moddalarni o'rtacha 14-48% gacha kamaytiradi, faol yashil devorlar ayrim "
       "moddalar bo'yicha 90% dan ortiq samaradorlik beradi, moxli biofiltrlar esa kichik maydonda "
       "yuqori chang ushlash qobiliyatiga ega. Mikroalgali fasadlar CO2 ni biriktirish va energiya "
       "tejashda, lishayniklar esa havo sifatini monitoring qilishda alohida ahamiyatga ega. "
       "O'zbekiston sharoitida bu texnologiyalarni suv resurslarini tejovchi shaklda, bosqichli pilot "
       "loyihalar orqali joriy etish maqsadga muvofiqdir. Kelgusi tadqiqotlar mahalliy turlar tanlovi, "
       "uzoq muddatli samaradorlik va xarajat-foyda tahliliga qaratilishi lozim.")

# References
heading("Foydalanilgan adabiyotlar", 2)
refs = [
 "Diener A., Mudu P. How can vegetation protect us from air pollution? Role of urban vegetation in air phytoremediation. npj Urban Sustainability / Nature, 2023. https://www.nature.com/articles/s42949-023-00105-0",
 "Mitigating Built Environment Air Pollution by Green Systems: An In-Depth Review. Preprints.org, 2024. https://www.preprints.org/manuscript/202406.1855/v1",
 "Reducing Outdoor Air Pollutants through a Moss-Based Biotechnological Purification Filter in Kazakhstan. Urban Science, 2023, 7(4), 104. https://www.mdpi.com/2413-8851/7/4/104",
 "MossTree: A new urban green infrastructure to actively reduce air pollution in urban hotspots. EU Horizon 2020, CORDIS, project 847744. https://cordis.europa.eu/project/id/847744",
 "An Assessment of the Suitability of Active Green Walls for NO2 Reduction in Green Buildings Using a Closed-Loop Flow Reactor. Atmosphere, 2019, 10(12), 801. https://www.mdpi.com/2073-4433/10/12/801",
 "Can Green Walls Reduce Outdoor Ambient Particulate Matter, Noise Pollution and Temperature? IJERPH, 2020, 17(14), 5084. https://www.mdpi.com/1660-4601/17/14/5084",
 "Integrating Microalgae into Sustainable Architecture for CO2 Capture and Urban Efficiency. Buildings, 2024, 14(12), 4045. https://www.mdpi.com/2075-5309/14/12/4045",
 "High spatial resolution assessment of air quality in urban centres using lichen carbon, nitrogen and sulfur contents. Environ. Sci. Pollut. Res., 2023. https://doi.org/10.1007/s11356-023-26652-8",
 "Low-Cost Monitoring of Airborne Heavy Metals Using Lichen Bioindicators. Atmosphere, 2025, 16(5), 576. https://www.mdpi.com/2073-4433/16/5/576",
 "Effective reduction of roadside air pollution with botanical biofiltration. Environmental Pollution, 2021. https://pubmed.ncbi.nlm.nih.gov/33684812/",
 "World Health Organization. Ambient (outdoor) air pollution. Fact sheet, 2024. https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health",
]
for i, r in enumerate(refs, 1):
    BODY.append(para(run("%d. %s" % (i, r), size=20), align="both", spacing_after=80, indent_first=0))

# ============================================================================
# PACKAGE DOCX
# ============================================================================
def build_docx(path):
    sect = ('<w:sectPr><w:pgSz w:w="%d" w:h="15840"/>'
            '<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" '
            'w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>'
            % (PAGE_W_DXA, MARGIN_DXA, MARGIN_DXA, MARGIN_DXA, MARGIN_DXA))
    doc = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
      '<w:body>' + "".join(BODY) + sect + '</w:body></w:document>')

    content_types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
      '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
      '<Default Extension="xml" ContentType="application/xml"/>'
      '<Default Extension="png" ContentType="image/png"/>'
      '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
      '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
      '</Types>')

    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
      '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
      '</Relationships>')

    doc_rels_items = ['<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
    for rid, target in RELS_IMG:
        doc_rels_items.append('<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="%s"/>' % (rid, target))
    doc_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
      + "".join(doc_rels_items) + '</Relationships>')

    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
      '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
      '<w:docDefaults><w:rPrDefault><w:rPr>'
      '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
      '<w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="en-US"/></w:rPr></w:rPrDefault></w:docDefaults>'
      '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
      '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
      '<w:sz w:val="24"/><w:szCs w:val="24"/></w:rPr></w:style>'
      '</w:styles>')

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("word/document.xml", doc)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        for fname, data in MEDIA:
            z.writestr("word/media/%s" % fname, data)

OUT = os.path.join(OUT_DIR, "Biologik_qoplamalar_havo_ifloslanishi_maqola.docx")
build_docx(OUT)
print("DOCX yaratildi:", OUT, "hajmi:", os.path.getsize(OUT), "bayt")
