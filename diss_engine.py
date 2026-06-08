# -*- coding: utf-8 -*-
"""Dissertation .docx builder (stdlib only).

CONTENT is a list of (kind, payload) tuples consumed by build().
Kinds:
  "h1"      -> chapter title (centered, bold, 16pt, page break before)
  "h2"      -> section heading (bold, 14pt)
  "h3"      -> sub-heading (bold italic, 14pt)
  "body"    -> justified paragraph, first-line indent
  "plain"   -> justified paragraph, no indent
  "center"  -> centered bold paragraph
  "bullet"  -> bulleted list item
  "num"     -> numbered list item
  "caption" -> centered italic small (figure/table caption)
  "table"   -> payload is a list of rows (list of cells); first row = header
  "pb"      -> page break (payload ignored)
"""
import zipfile
from xml.sax.saxutils import escape


def _run(text, bold=False, italic=False, sz=None):
    rpr = ""
    inner = ""
    if bold:
        inner += "<w:b/>"
    if italic:
        inner += "<w:i/>"
    if sz:
        inner += '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)
    if inner:
        rpr = "<w:rPr>%s</w:rPr>" % inner
    return ('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>'
            % (rpr, escape(text)))


def _p(content, *, jc=None, indent=None, spacing_after=120, spacing_before=0,
       num_id=None, page_break=False, line=360):
    ppr = "<w:pPr>"
    ppr += '<w:spacing w:before="%d" w:after="%d" w:line="%d" w:lineRule="auto"/>' % (
        spacing_before, spacing_after, line)
    if jc:
        ppr += '<w:jc w:val="%s"/>' % jc
    if indent:
        ppr += '<w:ind w:firstLine="%d"/>' % indent
    if num_id:
        ppr += ('<w:numPr><w:ilvl w:val="0"/><w:numId w:val="%d"/></w:numPr>'
                % num_id)
    ppr += "</w:pPr>"
    pb = ('<w:r><w:br w:type="page"/></w:r>') if page_break else ""
    return "<w:p>%s%s%s</w:p>" % (ppr, pb, content)


def _split_lead(text):
    # bold lead-in before the first " | "
    if " | " in text:
        lead, rest = text.split(" | ", 1)
        return _run(lead + " ", bold=True) + _run(rest)
    return _run(text)


def _table(rows):
    # rows: list of list of strings; first row is header (bold, shaded)
    cols = max(len(r) for r in rows)
    grid = "".join('<w:gridCol w:w="%d"/>' % int(9300 / cols)
                   for _ in range(cols))
    out = ['<w:tbl>'
           '<w:tblPr><w:tblStyle w:val="TableGrid"/>'
           '<w:tblW w:w="0" w:type="auto"/>'
           '<w:tblBorders>'
           '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
           '</w:tblBorders></w:tblPr>'
           '<w:tblGrid>%s</w:tblGrid>' % grid]
    for i, row in enumerate(rows):
        out.append("<w:tr>")
        for cell in row:
            shade = ('<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/>'
                     if i == 0 else "")
            para = _p(_run(cell, bold=(i == 0), sz=24),
                      spacing_after=20, line=240)
            out.append('<w:tc><w:tcPr><w:tcW w:w="%d" w:type="dxa"/>%s'
                       '</w:tcPr>%s</w:tc>'
                       % (int(9300 / cols), shade, para))
        out.append("</w:tr>")
    out.append("</w:tbl>")
    # add an empty paragraph after table for spacing
    out.append(_p(_run(""), spacing_after=120))
    return "".join(out)


def render(content):
    parts = []
    for kind, payload in content:
        if kind == "h1":
            parts.append(_p(_run(payload, bold=True, sz=32),
                            jc="center", spacing_before=240,
                            spacing_after=240, page_break=True))
        elif kind == "h1np":  # h1 without page break (first one)
            parts.append(_p(_run(payload, bold=True, sz=32),
                            jc="center", spacing_before=120,
                            spacing_after=240))
        elif kind == "h2":
            parts.append(_p(_run(payload, bold=True, sz=28),
                            jc="left", spacing_before=200, spacing_after=120))
        elif kind == "h3":
            parts.append(_p(_run(payload, bold=True, italic=True, sz=28),
                            jc="left", spacing_before=160, spacing_after=100))
        elif kind == "body":
            parts.append(_p(_split_lead(payload), jc="both", indent=567))
        elif kind == "plain":
            parts.append(_p(_split_lead(payload), jc="both"))
        elif kind == "center":
            parts.append(_p(_run(payload, bold=True), jc="center"))
        elif kind == "bullet":
            parts.append(_p(_run(payload), jc="both", num_id=1))
        elif kind == "num":
            parts.append(_p(_run(payload), jc="both", num_id=2))
        elif kind == "caption":
            parts.append(_p(_run(payload, italic=True, sz=24), jc="center",
                            spacing_after=160))
        elif kind == "table":
            parts.append(_table(payload))
        elif kind == "pb":
            parts.append(_p(_run(""), page_break=True, spacing_after=0))
        else:
            raise ValueError("unknown kind: %s" % kind)
    return "".join(parts)


def build(content, out_path, title="Magistrlik dissertatsiyasi"):
    body_xml = render(content)
    document = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/'
        'wordprocessingml/2006/main">'
        '<w:body>%s'
        '<w:sectPr>'
        '<w:pgSz w:w="11906" w:h="16838"/>'
        '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" '
        'w:header="720" w:footer="566" w:gutter="0"/>'
        '<w:pgNumType w:start="1"/>'
        '</w:sectPr></w:body></w:document>' % body_xml
    )

    content_types = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
        'content-types">'
        '<Default Extension="rels" ContentType="application/'
        'vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Override PartName="/word/document.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
        '<Override PartName="/word/styles.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
        '<Override PartName="/word/numbering.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.wordprocessingml.numbering+xml"/>'
        '<Override PartName="/word/footer1.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>'
        '</Types>'
    )
    rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
        'relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/officeDocument" '
        'Target="word/document.xml"/>'
        '</Relationships>'
    )
    doc_rels = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/'
        'relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/styles" Target="styles.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/numbering" Target="numbering.xml"/>'
        '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
        '</Relationships>'
    )
    # add footer reference into sectPr
    document = document.replace(
        '<w:pgNumType w:start="1"/>',
        '<w:footerReference w:type="default" r:id="rId3"/>'
        '<w:pgNumType w:start="1"/>')
    document = document.replace(
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">',
        'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships">', 1)

    footer = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/'
        '2006/main">'
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        '</w:p></w:ftr>'
    )

    styles = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:styles xmlns:w="http://schemas.openxmlformats.org/'
        'wordprocessingml/2006/main">'
        '<w:docDefaults><w:rPrDefault><w:rPr>'
        '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" '
        'w:cs="Times New Roman"/><w:sz w:val="28"/><w:szCs w:val="28"/>'
        '</w:rPr></w:rPrDefault>'
        '<w:pPrDefault><w:pPr><w:spacing w:line="360" w:lineRule="auto"/>'
        '</w:pPr></w:pPrDefault></w:docDefaults>'
        '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
        '<w:name w:val="Normal"/></w:style>'
        '<w:style w:type="table" w:styleId="TableGrid">'
        '<w:name w:val="Table Grid"/><w:tblPr></w:tblPr></w:style>'
        '</w:styles>'
    )
    numbering = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
        '<w:numbering xmlns:w="http://schemas.openxmlformats.org/'
        'wordprocessingml/2006/main">'
        '<w:abstractNum w:abstractNumId="0"><w:lvl w:ilvl="0">'
        '<w:start w:val="1"/><w:numFmt w:val="bullet"/>'
        '<w:lvlText w:val="\u2013"/><w:lvlJc w:val="left"/>'
        '<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl>'
        '</w:abstractNum>'
        '<w:abstractNum w:abstractNumId="1"><w:lvl w:ilvl="0">'
        '<w:start w:val="1"/><w:numFmt w:val="decimal"/>'
        '<w:lvlText w:val="%1)"/><w:lvlJc w:val="left"/>'
        '<w:pPr><w:ind w:left="720" w:hanging="360"/></w:pPr></w:lvl>'
        '</w:abstractNum>'
        '<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>'
        '<w:num w:numId="2"><w:abstractNumId w:val="1"/></w:num>'
        '</w:numbering>'
    )

    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", document)
        z.writestr("word/_rels/document.xml.rels", doc_rels)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/numbering.xml", numbering)
        z.writestr("word/footer1.xml", footer)
    return out_path
