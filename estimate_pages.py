# -*- coding: utf-8 -*-
"""Approximate rendered page count for the dissertation content."""
import math
from content_kirish import TITLE_PAGE, MUNDARIJA, KIRISH
from content_bob1 import BOB1
from content_bob2 import BOB2, UMUMIY_XULOSA
from build_diss import REFERENCES

CONTENT = (TITLE_PAGE + MUNDARIJA + KIRISH + BOB1 + BOB2 + UMUMIY_XULOSA
           + REFERENCES)

# Layout assumptions (points). A4 usable height ~ 700pt after margins+footer.
PAGE_PT = 690.0
CHARS_PER_LINE = 82          # ~14pt TNR across ~16.5cm
LINE_PT_BODY = 21.0          # 14pt * 1.5 line spacing
AFTER_PT = 6.0               # paragraph spacing after (120 twips)

def text_of(payload):
    if isinstance(payload, str):
        return payload
    return " ".join(c for row in payload for c in row)

used = 0.0
pages = 1
def add(pt):
    global used, pages
    used += pt
    while used > PAGE_PT:
        used -= PAGE_PT
        pages += 1

for kind, payload in CONTENT:
    if kind in ("h1", "h1np"):
        # chapter title starts new page
        if kind == "h1":
            pages += 1
            used = 0.0
        add(LINE_PT_BODY * 2 + 18)
    elif kind in ("h2",):
        add(LINE_PT_BODY + 14)
    elif kind in ("h3",):
        add(LINE_PT_BODY + 10)
    elif kind in ("body", "plain", "num", "bullet"):
        n = max(1, math.ceil(len(text_of(payload)) / CHARS_PER_LINE))
        add(n * LINE_PT_BODY + AFTER_PT)
    elif kind == "center":
        add(LINE_PT_BODY + AFTER_PT)
    elif kind == "caption":
        add(LINE_PT_BODY + 8)
    elif kind == "table":
        rows = len(payload)
        add(rows * 20 + 12)   # ~20pt per row at 12pt + spacing
    elif kind == "pb":
        pages += 1
        used = 0.0

print("Estimated rendered pages:", pages)
print("Total blocks:", len(CONTENT))
