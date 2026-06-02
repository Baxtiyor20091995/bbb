# -*- coding: utf-8 -*-
"""
Pure-Python DOCX (Microsoft Word) paketlovchi.
Faqat standart kutubxonalar: zipfile, struct, re, os.
Imkoniyatlar: sarlavhalar (Heading 1/2), tana matni (justify, 1.5 interval,
abzas, Times New Roman 14pt), rasmlar (inline, avto-masshtab), jadvallar,
titul varaq, avtomatik mundarija (TOC field), sahifa raqamlari (footer).
Inline markup: **qalin**, ~pastki indeks~, ^yuqori indeks^.
"""
import os
import re
import struct
import zipfile

EMU_PER_PX = 9525           # 96 DPI
CONTENT_WIDTH_EMU = 5800000  # taxminan 15.2 sm (A4, hoshiyalar bilan)


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def png_size(path):
    with open(path, 'rb') as f:
        head = f.read(24)
    if head[:8] != b'\x89PNG\r\n\x1a\n':
        raise ValueError('PNG emas: ' + path)
    w, h = struct.unpack('>II', head[16:24])
    return w, h


def runs_from_markup(text, base_size=None):
    """Inline markupni run XML ro'yxatiga aylantiradi.
    **qalin** segment ichida ham ~pastki~ / ^yuqori^ indeks ishlaydi."""
    out = []
    for part in re.split(r'(\*\*.*?\*\*)', text):
        if part == '':
            continue
        if part.startswith('**') and part.endswith('**') and len(part) >= 4:
            out.append(_sub_sup_runs(part[2:-2], bold=True, base_size=base_size))
        else:
            out.append(_sub_sup_runs(part, bold=False, base_size=base_size))
    return ''.join(out)


def _sub_sup_runs(text, bold=False, base_size=None):
    tokens = re.findall(r'(~[^~]*~|\^[^\^]*\^|[^~^]+)', text)
    out = []
    for tk in tokens:
        sub = sup = False
        t = tk
        if tk.startswith('~') and tk.endswith('~') and len(tk) >= 2:
            sub = True
            t = tk[1:-1]
        elif tk.startswith('^') and tk.endswith('^') and len(tk) >= 2:
            sup = True
            t = tk[1:-1]
        if t == '':
            continue
        rpr = []
        if bold:
            rpr.append('<w:b/>')
        if sub:
            rpr.append('<w:vertAlign w:val="subscript"/>')
        if sup:
            rpr.append('<w:vertAlign w:val="superscript"/>')
        if base_size:
            rpr.append('<w:sz w:val="%d"/>' % base_size)
            rpr.append('<w:szCs w:val="%d"/>' % base_size)
        rprx = '<w:rPr>%s</w:rPr>' % ''.join(rpr) if rpr else ''
        out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
                   % (rprx, esc(t)))
    return ''.join(out)


class Document:
    def __init__(self):
        self.blocks = []          # body XML bo'laklari
        self.media = []           # (rid, arcname, srcpath)
        self._rid = 10            # rId hisoblagich (footer/style uchun joy qoldiramiz)
        self._docpr = 100         # drawing docPr id

    def _next_rid(self):
        self._rid += 1
        return 'rId%d' % self._rid

    # ---------------- abzaslar / sarlavhalar ----------------
    def add_heading(self, text, level=1, page_break_before=False):
        style = 'Heading%d' % level
        ppr = ['<w:pStyle w:val="%s"/>' % style]
        if page_break_before:
            ppr.append('<w:pageBreakBefore/>')
        self.blocks.append(
            '<w:p><w:pPr>%s</w:pPr>%s</w:p>'
            % (''.join(ppr), runs_from_markup(text))
        )

    def add_paragraph(self, text, style='Body', jc=None, first_indent=True):
        ppr = ['<w:pStyle w:val="%s"/>' % style]
        if jc:
            ppr.append('<w:jc w:val="%s"/>' % jc)
        if not first_indent:
            ppr.append('<w:ind w:firstLine="0"/>')
        self.blocks.append(
            '<w:p><w:pPr>%s</w:pPr>%s</w:p>'
            % (''.join(ppr), runs_from_markup(text))
        )

    def add_centered(self, text, bold=False, size=None, color=None, before=0, after=0):
        space_before = before
        space_after = after
        rpr = []
        if bold:
            rpr.append('<w:b/>')
        if size:
            rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size))
        if color:
            rpr.append('<w:color w:val="%s"/>' % color)
        rprx = '<w:rPr>%s</w:rPr>' % ''.join(rpr) if rpr else ''
        self.blocks.append(
            '<w:p><w:pPr><w:jc w:val="center"/>'
            '<w:spacing w:before="%d" w:after="%d"/>'
            '<w:ind w:firstLine="0"/></w:pPr>'
            '<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r></w:p>'
            % (space_before, space_after, rprx, esc(text))
        )

    def add_spacer(self, count=1):
        for _ in range(count):
            self.blocks.append('<w:p><w:pPr><w:ind w:firstLine="0"/></w:pPr></w:p>')

    def add_page_break(self):
        self.blocks.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # ---------------- rasm + izoh ----------------
    def add_picture(self, path, caption=None, max_width_emu=CONTENT_WIDTH_EMU):
        w_px, h_px = png_size(path)
        cx = w_px * EMU_PER_PX
        cy = h_px * EMU_PER_PX
        if cx > max_width_emu:
            scale = max_width_emu / cx
            cx = int(cx * scale)
            cy = int(cy * scale)
        rid = self._next_rid()
        idx = len(self.media) + 1
        arc = 'media/image%d.png' % idx
        self.media.append((rid, arc, path))
        self._docpr += 1
        dp = self._docpr
        drawing = (
            '<w:p><w:pPr><w:keepNext/><w:jc w:val="center"/>'
            '<w:spacing w:before="120" w:after="60"/>'
            '<w:ind w:firstLine="0"/></w:pPr>'
            '<w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0">'
            '<wp:extent cx="%d" cy="%d"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            '<wp:docPr id="%d" name="Rasm%d"/>'
            '<wp:cNvGraphicFramePr>'
            '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
            '</wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:nvPicPr><pic:cNvPr id="%d" name="image%d.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill><a:blip r:embed="%s"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
            '</pic:pic></a:graphicData></a:graphic>'
            '</wp:inline></w:drawing></w:r></w:p>'
            % (cx, cy, dp, dp, dp, idx, rid, cx, cy)
        )
        self.blocks.append(drawing)
        if caption:
            self.blocks.append(
                '<w:p><w:pPr><w:pStyle w:val="Caption"/></w:pPr>%s</w:p>'
                % runs_from_markup(caption)
            )

    # ---------------- jadval ----------------
    def add_table(self, headers, rows, widths=None, caption_top=None):
        if caption_top:
            self.blocks.append(
                '<w:p><w:pPr><w:pStyle w:val="Caption"/></w:pPr>%s</w:p>'
                % runs_from_markup(caption_top)
            )
        ncol = len(headers)
        if not widths:
            widths = [int(9000 / ncol)] * ncol
        grid = ''.join('<w:gridCol w:w="%d"/>' % w for w in widths)

        def cell(text, w, header=False, jc='left'):
            rpr = '<w:b/>' if header else ''
            shd = '<w:shd w:val="clear" w:color="auto" w:fill="2962A8"/>' if header else ''
            col = '<w:color w:val="FFFFFF"/>' if header else ''
            return (
                '<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s'
                '<w:vAlign w:val="center"/></w:tcPr>'
                '<w:p><w:pPr><w:jc w:val="%s"/><w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'
                '<w:ind w:firstLine="0"/></w:pPr>'
                '<w:r><w:rPr>%s%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r></w:p></w:tc>'
                % (w, shd, jc, rpr, col, esc(str(text)))
            )

        trs = []
        trs.append('<w:tr><w:trPr><w:tblHeader/></w:trPr>'
                   + ''.join(cell(h, widths[i], True, 'center') for i, h in enumerate(headers))
                   + '</w:tr>')
        for row in rows:
            cells = ''.join(
                cell(c, widths[i], False, 'center' if i > 0 else 'left')
                for i, c in enumerate(row)
            )
            trs.append('<w:tr>%s</w:tr>' % cells)

        borders = (
            '<w:tblBorders>'
            '<w:top w:val="single" w:sz="6" w:space="0" w:color="6E7A8C"/>'
            '<w:left w:val="single" w:sz="6" w:space="0" w:color="6E7A8C"/>'
            '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="6E7A8C"/>'
            '<w:right w:val="single" w:sz="6" w:space="0" w:color="6E7A8C"/>'
            '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="9AA6B5"/>'
            '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="9AA6B5"/>'
            '</w:tblBorders>'
        )
        self.blocks.append(
            '<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>'
            '<w:jc w:val="center"/>%s'
            '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" '
            'w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'
            '</w:tblPr><w:tblGrid>%s</w:tblGrid>%s</w:tbl>'
            % (borders, grid, ''.join(trs))
        )
        # jadvaldan keyin kichik bo'shliq
        self.blocks.append('<w:p><w:pPr><w:spacing w:after="60"/><w:ind w:firstLine="0"/></w:pPr></w:p>')

    # ---------------- mundarija (TOC field) ----------------
    def add_toc(self):
        self.blocks.append(
            '<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr>'
            '<w:r><w:t>MUNDARIJA</w:t></w:r></w:p>'
        )
        self.blocks.append(
            '<w:p><w:pPr><w:ind w:firstLine="0"/></w:pPr>'
            '<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
            '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-3" \\h \\z \\u </w:instrText></w:r>'
            '<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
            '<w:r><w:rPr><w:i/><w:color w:val="808080"/></w:rPr>'
            '<w:t xml:space="preserve">[Mundarijani yangilash uchun: butun hujjatni belgilang (Ctrl+A) va F9 tugmasini bosing.]</w:t></w:r>'
            '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
        )

    # ---------------- titul varaq ----------------
    def add_title_page(self, lines):
        """lines: [(text, {opts})...] markaziy joylashgan."""
        for text, opt in lines:
            self.add_centered(
                text,
                bold=opt.get('bold', False),
                size=opt.get('size'),
                color=opt.get('color'),
                before=opt.get('before', 0),
                after=opt.get('after', 80),
            )
        self.add_page_break()

    # ---------------- saqlash ----------------
    def save(self, path):
        footer_rid = 'rIdFooter1'
        footer_first_rid = 'rIdFooter2'
        body = ''.join(self.blocks)
        sect = (
            '<w:sectPr>'
            '<w:footerReference w:type="default" r:id="%s"/>'
            '<w:footerReference w:type="first" r:id="%s"/>'
            '<w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" '
            'w:header="708" w:footer="708" w:gutter="0"/>'
            '<w:titlePg/>'
            '<w:docGrid w:linePitch="360"/>'
            '</w:sectPr>'
            % (footer_rid, footer_first_rid)
        )
        document_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:document '
            'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<w:body>%s%s</w:body></w:document>' % (body, sect)
        )

        # document.xml.rels
        rels = [
            '<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>',
            '<Relationship Id="rIdSettings" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>',
            '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>' % footer_rid,
            '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer2.xml"/>' % footer_first_rid,
        ]
        for rid, arc, _src in self.media:
            rels.append(
                '<Relationship Id="%s" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="%s"/>'
                % (rid, arc)
            )
        document_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>'
            % ''.join(rels)
        )

        # content types
        ctypes = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
            '<Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
            '<Override PartName="/word/footer2.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
            '</Types>'
        )

        root_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>'
        )

        settings_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:updateFields w:val="true"/>'
            '<w:defaultTabStop w:val="708"/>'
            '</w:settings>'
        )

        footer_default = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<w:p><w:pPr><w:jc w:val="center"/><w:ind w:firstLine="0"/>'
            '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr></w:pPr>'
            '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>'
            '<w:fldChar w:fldCharType="begin"/></w:r>'
            '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>'
            '<w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
            '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>'
            '<w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>'
        )
        footer_first = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:p><w:pPr><w:jc w:val="center"/><w:ind w:firstLine="0"/></w:pPr></w:p></w:ftr>'
        )

        styles_xml = self._styles_xml()

        with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('[Content_Types].xml', ctypes)
            z.writestr('_rels/.rels', root_rels)
            z.writestr('word/document.xml', document_xml)
            z.writestr('word/_rels/document.xml.rels', document_rels)
            z.writestr('word/styles.xml', styles_xml)
            z.writestr('word/settings.xml', settings_xml)
            z.writestr('word/footer1.xml', footer_default)
            z.writestr('word/footer2.xml', footer_first)
            for _rid, arc, src in self.media:
                z.write(src, 'word/' + arc)

    # ---------------- styles.xml ----------------
    def _styles_xml(self):
        font = 'Times New Roman'
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s"/>'
            '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="en-US"/>'
            '</w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="360" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
            '</w:docDefaults>'
            # Normal
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
            '<w:name w:val="Normal"/><w:qFormat/></w:style>'
            # Body
            '<w:style w:type="paragraph" w:styleId="Body">'
            '<w:name w:val="Body Text"/><w:basedOn w:val="Normal"/>'
            '<w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/>'
            '<w:ind w:firstLine="709"/><w:jc w:val="both"/></w:pPr>'
            '<w:rPr><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
            # Heading 1
            '<w:style w:type="paragraph" w:styleId="Heading1">'
            '<w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Body"/>'
            '<w:qFormat/>'
            '<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="160" w:line="360" w:lineRule="auto"/>'
            '<w:jc w:val="center"/><w:outlineLvl w:val="0"/></w:pPr>'
            '<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/><w:color w:val="1F3B5B"/></w:rPr></w:style>'
            # Heading 2
            '<w:style w:type="paragraph" w:styleId="Heading2">'
            '<w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Body"/>'
            '<w:qFormat/>'
            '<w:pPr><w:keepNext/><w:spacing w:before="200" w:after="120" w:line="360" w:lineRule="auto"/>'
            '<w:jc w:val="left"/><w:outlineLvl w:val="1"/></w:pPr>'
            '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/><w:color w:val="2962A8"/></w:rPr></w:style>'
            # Heading 3
            '<w:style w:type="paragraph" w:styleId="Heading3">'
            '<w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Body"/>'
            '<w:qFormat/>'
            '<w:pPr><w:keepNext/><w:spacing w:before="160" w:after="100" w:line="360" w:lineRule="auto"/>'
            '<w:jc w:val="left"/><w:outlineLvl w:val="2"/></w:pPr>'
            '<w:rPr><w:b/><w:i/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:style>'
            # Caption
            '<w:style w:type="paragraph" w:styleId="Caption">'
            '<w:name w:val="caption"/><w:basedOn w:val="Normal"/><w:qFormat/>'
            '<w:pPr><w:spacing w:before="40" w:after="200" w:line="240" w:lineRule="auto"/>'
            '<w:jc w:val="center"/><w:ind w:firstLine="0"/></w:pPr>'
            '<w:rPr><w:i/><w:sz w:val="24"/><w:szCs w:val="24"/><w:color w:val="404040"/></w:rPr></w:style>'
            # TOC stillari
            '<w:style w:type="paragraph" w:styleId="TOC1"><w:name w:val="toc 1"/><w:basedOn w:val="Normal"/>'
            '<w:pPr><w:spacing w:before="120" w:after="60" w:line="276" w:lineRule="auto"/>'
            '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9355"/></w:tabs><w:ind w:firstLine="0"/></w:pPr>'
            '<w:rPr><w:b/></w:rPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="TOC2"><w:name w:val="toc 2"/><w:basedOn w:val="Normal"/>'
            '<w:pPr><w:spacing w:after="40" w:line="276" w:lineRule="auto"/>'
            '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9355"/></w:tabs><w:ind w:left="284" w:firstLine="0"/></w:pPr></w:style>'
            '<w:style w:type="paragraph" w:styleId="TOC3"><w:name w:val="toc 3"/><w:basedOn w:val="Normal"/>'
            '<w:pPr><w:spacing w:after="40" w:line="276" w:lineRule="auto"/>'
            '<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="9355"/></w:tabs><w:ind w:left="567" w:firstLine="0"/></w:pPr></w:style>'
            # Hyperlink (TOC ichidagi)
            '<w:style w:type="character" w:styleId="Hyperlink"><w:name w:val="Hyperlink"/>'
            '<w:rPr><w:color w:val="0563C1"/></w:rPr></w:style>'
            '</w:styles>'
            % (font, font, font)
        )
