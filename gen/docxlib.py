# -*- coding: utf-8 -*-
"""
Генератор файлов .docx без сторонних библиотек.
Поддержка: заголовки, абзацы, формулы (по центру, курсив), подписи к рисункам,
встраивание изображений PNG, таблицы, маркированные списки.
"""
import os
import zipfile
import struct
from xml.sax.saxutils import escape

EMU_PER_CM = 360000


def png_size(path):
    with open(path, "rb") as f:
        head = f.read(26)
    # IHDR: ширина и высота — байты 16..24
    w, h = struct.unpack(">II", head[16:24])
    return w, h


class DocxBuilder:
    def __init__(self):
        self.blocks = []          # список XML-параграфов
        self.images = []          # [(rId, arcname, srcpath)]
        self._img_counter = 0

    # ---- базовые run/paragraph helpers -------------------------------
    def _runs(self, text):
        """Поддержка простой разметки: *жирный* и _курсив_ не используем,
        текст подаётся уже разбитым. Здесь просто экранируем."""
        return (f'<w:r><w:rPr>{{RPR}}</w:rPr>'
                f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r>')

    def heading0(self, text):
        self.blocks.append(
            '<w:p><w:pPr><w:spacing w:before="280" w:after="120"/>'
            '<w:keepNext/>'
            '<w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="30"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')

    def heading1(self, text):
        self.blocks.append(
            '<w:p><w:pPr><w:spacing w:before="200" w:after="80"/>'
            '<w:keepNext/>'
            '<w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="28"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')

    def heading2(self, text):
        self.blocks.append(
            '<w:p><w:pPr><w:spacing w:before="140" w:after="60"/>'
            '<w:keepNext/>'
            '<w:rPr><w:b/><w:i/><w:sz w:val="26"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:i/><w:sz w:val="26"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')

    def para(self, text):
        # обоснование по ширине, красная строка, межстрочный 1.5
        self.blocks.append(
            '<w:p><w:pPr><w:ind w:firstLine="709"/>'
            '<w:jc w:val="both"/>'
            '<w:spacing w:line="360" w:lineRule="auto" w:after="60"/>'
            '<w:rPr><w:sz w:val="28"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:sz w:val="28"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')

    def formula(self, text):
        self.blocks.append(
            '<w:p><w:pPr><w:jc w:val="center"/>'
            '<w:spacing w:before="60" w:after="60"/>'
            '<w:rPr><w:i/><w:sz w:val="28"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:sz w:val="28"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')

    def caption(self, text):
        self.blocks.append(
            '<w:p><w:pPr><w:jc w:val="center"/>'
            '<w:spacing w:before="40" w:after="160"/>'
            '<w:rPr><w:sz w:val="24"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:sz w:val="24"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')

    def bullet(self, text):
        self.blocks.append(
            '<w:p><w:pPr><w:ind w:left="709" w:hanging="284"/>'
            '<w:jc w:val="both"/>'
            '<w:spacing w:line="360" w:lineRule="auto" w:after="40"/>'
            '<w:rPr><w:sz w:val="28"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:sz w:val="28"/></w:rPr>'
            f'<w:t xml:space="preserve">\u2013 {escape(text)}</w:t></w:r></w:p>')

    def image(self, path, width_cm=14.0):
        self._img_counter += 1
        n = self._img_counter
        rid = f"rIdImg{n}"
        arc = f"media/image{n}.png"
        self.images.append((rid, arc, path))
        w_px, h_px = png_size(path)
        cx = int(width_cm * EMU_PER_CM)
        cy = int(cx * h_px / w_px)
        self.blocks.append(
            '<w:p><w:pPr><w:jc w:val="center"/>'
            '<w:spacing w:before="120" w:after="20"/>'
            '<w:keepNext/></w:pPr>'
            '<w:r><w:drawing>'
            '<wp:inline distT="0" distB="0" distL="0" distR="0">'
            f'<wp:extent cx="{cx}" cy="{cy}"/>'
            '<wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:docPr id="{n}" name="Picture{n}"/>'
            '<wp:cNvGraphicFramePr>'
            '<a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>'
            '</wp:cNvGraphicFramePr>'
            '<a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:nvPicPr>'
            f'<pic:cNvPr id="{n}" name="image{n}.png"/>'
            '<pic:cNvPicPr/></pic:nvPicPr>'
            '<pic:blipFill>'
            f'<a:blip r:embed="{rid}"/>'
            '<a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            '<pic:spPr>'
            '<a:xfrm><a:off x="0" y="0"/>'
            f'<a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            '</pic:spPr></pic:pic>'
            '</a:graphicData></a:graphic>'
            '</wp:inline></w:drawing></w:r></w:p>')

    def table(self, headers, rows, widths=None):
        ncol = len(headers)
        total = 9300
        if widths is None:
            widths = [total // ncol] * ncol
        grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in widths)

        def cell(text, header=False, w=2000):
            rpr = '<w:b/>' if header else ''
            shade = '<w:shd w:val="clear" w:color="auto" w:fill="DCE2EC"/>' if header else ''
            jc = 'center' if header else 'left'
            return (
                '<w:tc><w:tcPr>'
                f'<w:tcW w:w="{w}" w:type="dxa"/>'
                f'{shade}'
                '<w:vAlign w:val="center"/></w:tcPr>'
                f'<w:p><w:pPr><w:jc w:val="{jc}"/>'
                '<w:spacing w:before="20" w:after="20" w:line="240" w:lineRule="auto"/>'
                f'<w:rPr>{rpr}<w:sz w:val="24"/></w:rPr></w:pPr>'
                f'<w:r><w:rPr>{rpr}<w:sz w:val="24"/></w:rPr>'
                f'<w:t xml:space="preserve">{escape(str(text))}</w:t></w:r></w:p></w:tc>')

        trs = []
        hcells = "".join(cell(h, True, widths[i]) for i, h in enumerate(headers))
        trs.append(f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{hcells}</w:tr>')
        for row in rows:
            rcells = "".join(cell(c, False, widths[i]) for i, c in enumerate(row))
            trs.append(f'<w:tr>{rcells}</w:tr>')

        borders = (
            '<w:tblBorders>'
            '<w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            '<w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            '<w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            '<w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            '<w:insideH w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            '<w:insideV w:val="single" w:sz="6" w:space="0" w:color="000000"/>'
            '</w:tblBorders>')
        self.blocks.append(
            '<w:tbl><w:tblPr>'
            '<w:tblW w:w="9300" w:type="dxa"/>'
            '<w:jc w:val="center"/>'
            f'{borders}'
            '<w:tblLook w:val="04A0"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>'
            f'{"".join(trs)}</w:tbl>'
            '<w:p><w:pPr><w:spacing w:after="60"/></w:pPr></w:p>')

    def pagebreak(self):
        self.blocks.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    # ---- сборка файла -------------------------------------------------
    def save(self, out_path):
        body = "".join(self.blocks)
        document_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document '
            'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<w:body>'
            f'{body}'
            '<w:sectPr>'
            '<w:pgSz w:w="11906" w:h="16838"/>'
            '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" '
            'w:header="708" w:footer="708" w:gutter="0"/>'
            '<w:pgNumType w:start="1"/>'
            '</w:sectPr></w:body></w:document>')

        styles_xml = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
            '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="ru-RU"/>'
            '</w:rPr></w:rPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
            '<w:name w:val="Normal"/><w:qFormat/></w:style></w:styles>')

        content_types = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Default Extension="png" ContentType="image/png"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '</Types>')

        rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '</Relationships>')

        img_rels = "".join(
            f'<Relationship Id="{rid}" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" '
            f'Target="{arc}"/>' for rid, arc, _ in self.images)
        doc_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            f'{img_rels}</Relationships>')

        with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", content_types)
            z.writestr("_rels/.rels", rels)
            z.writestr("word/document.xml", document_xml)
            z.writestr("word/styles.xml", styles_xml)
            z.writestr("word/_rels/document.xml.rels", doc_rels)
            for rid, arc, src in self.images:
                z.write(src, "word/" + arc)
