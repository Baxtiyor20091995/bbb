# -*- coding: utf-8 -*-
"""
Генератор файла .docx (Word) без сторонних библиотек.
Создаёт «Содержание» дипломной работы на русском языке.
"""
import zipfile
from xml.sax.saxutils import escape

OUT = "Содержание_дипломной_работы.docx"

# ----------------------------------------------------------------------
# Контент содержания.
# Уровни: 0 = заголовок главы (жирный), 1 = подраздел, 2 = под-подраздел
# Спец-тип "title" = заголовок по центру, "plain" = обычный жирный пункт
# ----------------------------------------------------------------------
CONTENT = [
    ("title", "СОДЕРЖАНИЕ"),
    ("plain", "ВВЕДЕНИЕ"),

    ("h0", "1. ТЕХНОЛОГИЧЕСКАЯ ЧАСТЬ"),
    ("h1", "1.1. Общая характеристика гидрометаллургического завода ГМЗ-7"),
    ("h1", "1.2. Назначение и место мельницы МШЦ в технологической схеме измельчения"),
    ("h1", "1.3. Устройство и принцип работы шаровой мельницы с центральной разгрузкой (МШЦ)"),
    ("h1", "1.4. Технологический процесс мокрого измельчения руды"),
    ("h1", "1.5. Основные технологические параметры процесса измельчения"),
    ("h2", "1.5.1. Производительность мельницы"),
    ("h2", "1.5.2. Степень измельчения и крупность готового продукта"),
    ("h2", "1.5.3. Соотношение «руда — вода — шары»"),
    ("h1", "1.6. Анализ существующей системы управления мельницей МШЦ"),
    ("h1", "1.7. Обоснование необходимости автоматизации технологического процесса"),

    ("h0", "2. РАСЧЁТНАЯ ЧАСТЬ"),
    ("h1", "2.1. Исходные данные для расчёта"),
    ("h1", "2.2. Технологический расчёт мельницы МШЦ"),
    ("h2", "2.2.1. Расчёт производительности мельницы"),
    ("h2", "2.2.2. Расчёт частоты вращения барабана"),
    ("h2", "2.2.3. Расчёт шаровой загрузки"),
    ("h1", "2.3. Расчёт мощности привода мельницы"),
    ("h1", "2.4. Выбор и расчёт электродвигателя"),
    ("h1", "2.5. Материальный баланс процесса измельчения"),
    ("h1", "2.6. Расчёт и выбор измерительных преобразователей (датчиков)"),
    ("h2", "2.6.1. Датчики уровня и расхода"),
    ("h2", "2.6.2. Датчики плотности пульпы"),
    ("h2", "2.6.3. Датчики температуры и давления"),
    ("h1", "2.7. Расчёт регулирующих органов и исполнительных механизмов"),
    ("h1", "2.8. Расчёт параметров настройки регулятора (ПИД-регулирование)"),

    ("h0", "3. РАЗРАБОТКА СХЕМ АВТОМАТИЗАЦИИ"),
    ("h1", "3.1. Анализ объекта управления как объекта автоматизации"),
    ("h1", "3.2. Разработка функциональной схемы автоматизации мельницы МШЦ"),
    ("h1", "3.3. Выбор структуры автоматизированной системы управления (АСУ ТП)"),
    ("h1", "3.4. Выбор технических средств автоматизации"),
    ("h2", "3.4.1. Выбор программируемого логического контроллера (ПЛК)"),
    ("h2", "3.4.2. Выбор первичных и вторичных приборов"),
    ("h2", "3.4.3. Выбор средств визуализации (SCADA-система)"),
    ("h1", "3.5. Разработка структурной и принципиальной электрической схем"),
    ("h1", "3.6. Разработка алгоритма управления процессом измельчения"),
    ("h1", "3.7. Разработка программного обеспечения для ПЛК"),
    ("h1", "3.8. Разработка человеко-машинного интерфейса (АРМ оператора)"),
    ("h1", "3.9. Контуры регулирования и защиты (блокировки, сигнализация)"),

    ("h0", "4. БЕЗОПАСНОСТЬ ЖИЗНЕДЕЯТЕЛЬНОСТИ"),
    ("h1", "4.1. Анализ опасных и вредных производственных факторов"),
    ("h1", "4.2. Техника безопасности при эксплуатации мельницы МШЦ"),
    ("h1", "4.3. Электробезопасность при обслуживании средств автоматизации"),
    ("h1", "4.4. Производственная санитария и гигиена труда"),
    ("h2", "4.4.1. Микроклимат, шум и вибрация"),
    ("h2", "4.4.2. Освещение рабочих мест"),
    ("h2", "4.4.3. Защита от пыли и вредных веществ"),
    ("h1", "4.5. Пожарная безопасность"),
    ("h1", "4.6. Экологическая безопасность и охрана окружающей среды"),
    ("h1", "4.7. Расчёт защитного заземления"),

    ("h0", "5. ЭКОНОМИЧЕСКАЯ ЧАСТЬ"),
    ("h1", "5.1. Технико-экономическое обоснование внедрения системы автоматизации"),
    ("h1", "5.2. Расчёт капитальных затрат на внедрение АСУ ТП"),
    ("h1", "5.3. Расчёт эксплуатационных расходов"),
    ("h1", "5.4. Расчёт экономии от внедрения автоматизации"),
    ("h2", "5.4.1. Снижение энергозатрат"),
    ("h2", "5.4.2. Повышение производительности"),
    ("h2", "5.4.3. Сокращение потерь и брака"),
    ("h1", "5.5. Расчёт срока окупаемости и экономического эффекта"),
    ("h1", "5.6. Технико-экономические показатели проекта"),

    ("plain", "ЗАКЛЮЧЕНИЕ"),
    ("plain", "СПИСОК ИСПОЛЬЗОВАННОЙ ЛИТЕРАТУРЫ"),
    ("plain", "ПРИЛОЖЕНИЯ"),
]


def make_paragraph(kind, text):
    t = escape(text)
    # Параметры по типу строки
    if kind == "title":
        # По центру, жирный, 16pt, отступ снизу
        return (
            '<w:p><w:pPr><w:jc w:val="center"/>'
            '<w:spacing w:before="120" w:after="240"/>'
            '<w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="32"/><w:szCs w:val="32"/></w:rPr>'
            f'<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
        )
    if kind in ("h0", "plain"):
        # Жирный, 14pt, без отступа слева
        before = "200" if kind == "h0" else "100"
        return (
            f'<w:p><w:pPr><w:spacing w:before="{before}" w:after="60"/>'
            '<w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:b/><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
            f'<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
        )
    if kind == "h1":
        # Обычный, 14pt, отступ слева 360 twips
        return (
            '<w:p><w:pPr><w:ind w:left="360"/><w:spacing w:after="40"/>'
            '<w:rPr><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:pPr>'
            f'<w:r><w:rPr><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
            f'<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
        )
    # h2 — отступ слева 720 twips
    return (
        '<w:p><w:pPr><w:ind w:left="720"/><w:spacing w:after="40"/>'
        '<w:rPr><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr></w:pPr>'
        f'<w:r><w:rPr><w:sz w:val="28"/><w:szCs w:val="28"/></w:rPr>'
        f'<w:t xml:space="preserve">{t}</w:t></w:r></w:p>'
    )


body = "".join(make_paragraph(k, v) for k, v in CONTENT)

document_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:body>'
    f'{body}'
    '<w:sectPr>'
    '<w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" w:header="708" w:footer="708" w:gutter="0"/>'
    '</w:sectPr>'
    '</w:body></w:document>'
)

# Стили по умолчанию: Times New Roman 14pt
styles_xml = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
    '<w:docDefaults><w:rPrDefault><w:rPr>'
    '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>'
    '<w:sz w:val="28"/><w:szCs w:val="28"/><w:lang w:val="ru-RU"/>'
    '</w:rPr></w:rPrDefault></w:docDefaults>'
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
    '<w:name w:val="Normal"/><w:qFormat/></w:style>'
    '</w:styles>'
)

content_types = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
    '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
    '<Default Extension="xml" ContentType="application/xml"/>'
    '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
    '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
    '</Types>'
)

rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
    '</Relationships>'
)

doc_rels = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
    '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    '</Relationships>'
)

with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", content_types)
    z.writestr("_rels/.rels", rels)
    z.writestr("word/document.xml", document_xml)
    z.writestr("word/styles.xml", styles_xml)
    z.writestr("word/_rels/document.xml.rels", doc_rels)

print("Файл создан:", OUT)
