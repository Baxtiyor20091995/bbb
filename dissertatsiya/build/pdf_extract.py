# -*- coding: utf-8 -*-
"""
Sof Python (faqat zlib, re) PDF matn ajratuvchi.
ToUnicode CMap (bfchar/bfrange) ni parse qilib, CID-shrift glyph
kodlarini Unicode'ga o'giradi. Tarmoqsiz/kutubxonasiz ishlaydi.
Skanerlangan (rasm) PDF'lardan matn chiqmaydi.
"""
import zlib
import re
import sys


def _iter_streams(raw):
    for m in re.finditer(rb'stream\r?\n', raw):
        start = m.end()
        end = raw.find(b'endstream', start)
        if end == -1:
            continue
        blob = raw[start:end].rstrip(b'\r\n')
        try:
            yield zlib.decompress(blob)
        except Exception:
            continue


def _hex_to_unicode(h):
    """<XXXX...> hexni UTF-16BE deb dekodlash."""
    h = re.sub(rb'\s', b'', h)
    if len(h) % 2:
        h += b'0'
    try:
        bts = bytes.fromhex(h.decode('ascii'))
        return bts.decode('utf-16-be', 'replace')
    except Exception:
        return ''


def build_cmap(raw):
    """Hujjatdagi barcha ToUnicode CMaplarni bitta global lug'atga yig'amiz.
    Kalit: butun son (kod). Qiymat: unicode satr. Kod uzunligi (bayt) ham."""
    cmap = {}
    code_len = 2
    for dec in _iter_streams(raw):
        if b'beginbfchar' not in dec and b'beginbfrange' not in dec:
            continue
        # bfchar
        for blk in re.findall(rb'beginbfchar(.*?)endbfchar', dec, re.DOTALL):
            for m in re.finditer(rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
                src, dst = m.group(1), m.group(2)
                code_len = max(code_len, len(src) // 2)
                cmap[int(src, 16)] = _hex_to_unicode(dst)
        # bfrange
        for blk in re.findall(rb'beginbfrange(.*?)endbfrange', dec, re.DOTALL):
            # forma 1: <lo> <hi> <dst>
            for m in re.finditer(
                    rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', blk):
                lo = int(m.group(1), 16)
                hi = int(m.group(2), 16)
                base = _hex_to_unicode(m.group(3))
                code_len = max(code_len, len(m.group(1)) // 2)
                if base and hi - lo < 65536:
                    b0 = ord(base[0])
                    for i in range(hi - lo + 1):
                        cmap[lo + i] = chr(b0 + i)
            # forma 2: <lo> <hi> [ <d1> <d2> ... ]
            for m in re.finditer(
                    rb'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*\[(.*?)\]', blk, re.DOTALL):
                lo = int(m.group(1), 16)
                dsts = re.findall(rb'<([0-9A-Fa-f]+)>', m.group(3))
                for i, d in enumerate(dsts):
                    cmap[lo + i] = _hex_to_unicode(d)
    return cmap, code_len


def _decode_hex_str(h, cmap, code_len):
    h = re.sub(rb'\s', b'', h).decode('ascii', 'ignore')
    if len(h) % 2:
        h += '0'
    step = code_len * 2
    out = []
    for i in range(0, len(h), step):
        chunk = h[i:i + step]
        if not chunk:
            continue
        code = int(chunk, 16)
        if code in cmap:
            out.append(cmap[code])
        elif len(chunk) == 4 and (code >> 8) in cmap and (code & 0xFF) in cmap:
            out.append(cmap[code >> 8] + cmap[code & 0xFF])
    return ''.join(out)


def _decode_literal_str(b, cmap):
    # literal (..) -> baytlar; cmap bo'lsa bayt-kod sifatida
    out = bytearray()
    i = 0
    n = len(b)
    while i < n:
        c = b[i]
        if c == 0x5C:
            i += 1
            if i >= n:
                break
            e = b[i]
            mp = {0x6E: 0x0A, 0x72: 0x0D, 0x74: 0x09, 0x62: 0x08,
                  0x66: 0x0C, 0x28: 0x28, 0x29: 0x29, 0x5C: 0x5C}
            if e in mp:
                out.append(mp[e]); i += 1
            elif 0x30 <= e <= 0x37:
                m = re.match(rb'[0-7]{1,3}', bytes(b[i:i + 3]))
                out.append(int(m.group(0), 8) & 0xFF); i += len(m.group(0))
            else:
                out.append(e); i += 1
        else:
            out.append(c); i += 1
    if cmap and all(byt in cmap for byt in out if byt > 32):
        return ''.join(cmap.get(byt, chr(byt)) for byt in out)
    return out.decode('latin-1', 'replace')


def extract_text(path):
    with open(path, 'rb') as f:
        raw = f.read()
    cmap, code_len = build_cmap(raw)
    show = re.compile(rb'<([0-9A-Fa-f\s]+)>\s*Tj|\(((?:[^()\\]|\\.)*)\)\s*Tj'
                      rb'|\[(.*?)\]\s*TJ', re.DOTALL)
    hx = re.compile(rb'<([0-9A-Fa-f\s]+)>')
    lit = re.compile(rb'\(((?:[^()\\]|\\.)*)\)')
    num = re.compile(rb'(-?\d+(?:\.\d+)?)')
    def render_block(block):
        line = []
        for m in show.finditer(block):
            if m.group(1) is not None:        # <hex> Tj
                line.append(_decode_hex_str(m.group(1), cmap, code_len))
            elif m.group(2) is not None:      # (lit) Tj
                line.append(_decode_literal_str(m.group(2), cmap))
            elif m.group(3) is not None:      # [..] TJ
                arr = m.group(3)
                pos = 0
                buf = []
                for tok in re.finditer(rb'<([0-9A-Fa-f\s]+)>|\(((?:[^()\\]|\\.)*)\)', arr):
                    gap = arr[pos:tok.start()]
                    nums = num.findall(gap)
                    if nums:
                        try:
                            if abs(float(nums[-1])) > 100:
                                buf.append(' ')
                        except ValueError:
                            pass
                    if tok.group(1) is not None:
                        buf.append(_decode_hex_str(tok.group(1), cmap, code_len))
                    else:
                        buf.append(_decode_literal_str(tok.group(2), cmap))
                    pos = tok.end()
                line.append(''.join(buf))
        return ''.join(line)

    out_lines = []
    for dec in _iter_streams(raw):
        if b'Tj' not in dec and b'TJ' not in dec:
            continue
        blocks = re.findall(rb'BT(.*?)ET', dec, re.DOTALL)
        if not blocks:
            blocks = [dec]
        rendered = [render_block(b) for b in blocks]
        rendered = [r for r in rendered if r.strip()]
        # alohida matn bloklari orasiga bo'sh joy
        txt = ' '.join(rendered)
        if txt.strip():
            out_lines.append(txt)
    text = '\n'.join(out_lines)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text.strip()


if __name__ == '__main__':
    path = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
    t = extract_text(path)
    print("LEN:", len(t))
    print("----- PREVIEW -----")
    print(t[:limit])
