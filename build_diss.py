# -*- coding: utf-8 -*-
"""Assemble all parts and build the dissertation .docx."""
from diss_engine import build
from content_kirish import TITLE_PAGE, MUNDARIJA, KIRISH
from content_bob1 import BOB1
from content_bob2 import BOB2, UMUMIY_XULOSA

REFERENCES = [
    ("h1", "FOYDALANILGAN ADABIYOTLAR RO'YXATI"),
    ("num", "O'zbekiston Respublikasining \"Ta'lim to'g'risida\"gi Qonuni. - "
            "Toshkent, 2020."),
    ("num", "O'zbekiston Respublikasi Prezidentining \"O'zbekiston "
            "Respublikasi oliy ta'lim tizimini 2030-yilgacha rivojlantirish "
            "konsepsiyasini tasdiqlash to'g'risida\"gi Farmoni. - Toshkent, "
            "2019."),
    ("num", "O'zbekiston Respublikasi \"Raqamli O'zbekiston - 2030\" "
            "strategiyasi. - Toshkent, 2020."),
    ("num", "Sommerville I. Software Engineering. - 10th ed. - Pearson, "
            "2015."),
    ("num", "Pressman R., Maxim B. Software Engineering: A Practitioner's "
            "Approach. - 8th ed. - McGraw-Hill, 2014."),
    ("num", "Date C.J. An Introduction to Database Systems. - 8th ed. - "
            "Addison-Wesley, 2003."),
    ("num", "Elmasri R., Navathe S. Fundamentals of Database Systems. - "
            "7th ed. - Pearson, 2016."),
    ("num", "Romero C., Ventura S. Educational Data Mining and Learning "
            "Analytics: An updated survey // WIREs Data Mining and Knowledge "
            "Discovery. - 2020."),
    ("num", "Siemens G. Learning Analytics: The Emergence of a Discipline // "
            "American Behavioral Scientist. - 2013."),
    ("num", "Baker R., Inventado P. Educational Data Mining and Learning "
            "Analytics. - Springer, 2014."),
    ("num", "Fowler M. Patterns of Enterprise Application Architecture. - "
            "Addison-Wesley, 2002."),
    ("num", "Newman S. Building Microservices. - 2nd ed. - O'Reilly Media, "
            "2021."),
    ("num", "Kimball R., Ross M. The Data Warehouse Toolkit. - 3rd ed. - "
            "Wiley, 2013."),
    ("num", "Few S. Information Dashboard Design. - 2nd ed. - Analytics "
            "Press, 2013."),
    ("num", "Han J., Kamber M., Pei J. Data Mining: Concepts and Techniques. "
            "- 3rd ed. - Morgan Kaufmann, 2011."),
    ("num", "Tan P., Steinbach M., Kumar V. Introduction to Data Mining. - "
            "2nd ed. - Pearson, 2018."),
    ("num", "Richardson L., Ruby S. RESTful Web APIs. - O'Reilly Media, "
            "2013."),
    ("num", "Burns B. Designing Distributed Systems. - O'Reilly Media, "
            "2018."),
    ("num", "McKinney W. Python for Data Analysis. - 2nd ed. - O'Reilly "
            "Media, 2017."),
    ("num", "Geron A. Hands-On Machine Learning with Scikit-Learn, Keras, "
            "and TensorFlow. - 2nd ed. - O'Reilly Media, 2019."),
]

CONTENT = []
CONTENT += TITLE_PAGE
CONTENT += MUNDARIJA
CONTENT += KIRISH
CONTENT += BOB1
CONTENT += BOB2
CONTENT += UMUMIY_XULOSA
CONTENT += REFERENCES

OUT = "Dissertatsiya_Akademik_monitoring.docx"
build(CONTENT, OUT)

# crude stats
words = 0
for kind, payload in CONTENT:
    if isinstance(payload, str):
        words += len(payload.split())
    else:
        for row in payload:
            for cell in row:
                words += len(cell.split())
print("Built:", OUT)
print("Blocks:", len(CONTENT))
print("Approx words:", words)
print("Approx pages (~300 w/page):", round(words / 300, 1))
