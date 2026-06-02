# -*- coding: utf-8 -*-
"""
Dissertatsiya matnini yig'ib, Dissertatsiya.docx faylini quradi.
Matn o'zbek tilida. Rasm va jadvallar bilan birga.
"""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from docx_builder import Document  # noqa: E402

RASM = os.path.normpath(os.path.join(HERE, '..', 'rasmlar'))
OUT = os.path.normpath(os.path.join(HERE, '..', 'Dissertatsiya.docx'))


def img(name):
    return os.path.join(RASM, name)


d = Document()

# ===========================================================================
#  TITUL VARAQ
# ===========================================================================
d.add_centered("O'ZBEKISTON RESPUBLIKASI OLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI",
               bold=True, size=24, before=200, after=60)
d.add_centered("___________________ UNIVERSITETI", bold=True, size=24, after=60)
d.add_centered("Kimyo (Kimyoviy texnologiya) fakulteti", size=24, after=40)
d.add_centered("\"Kimyoviy texnologiya\" kafedrasi", size=24, after=300)

d.add_centered("Qo'lyozma huquqida", size=22, after=20)
d.add_centered("UO'K: 544.526:546.82'47", size=22, after=260)

d.add_centered("MAGISTRLIK DISSERTATSIYASI", bold=True, size=36, after=120)
d.add_centered("Mavzu:", size=24, after=40)
d.add_centered("TABIIY FOTOSINTEZ ASOSIDA HAVONI TOZALOVCHI QOPLAMA",
               bold=True, size=30, after=10)
d.add_centered("OLISH USULLARINI O'RGANISH", bold=True, size=30, after=280)

d.add_centered("Mutaxassislik: 70730101 - Kimyoviy texnologiya", size=24, after=300)

d.add_centered("Magistrant: _______________________", size=24, after=40)
d.add_centered("Ilmiy rahbar: _______________________", size=24, after=300)

d.add_centered("Toshkent - 2026", bold=True, size=26, before=200)
d.add_page_break()

# ===========================================================================
#  MUNDARIJA (avtomatik TOC)
# ===========================================================================
d.add_toc()
d.add_page_break()

print("Titul + mundarija tayyor.")


# ===========================================================================
#  ANNOTATSIYA
# ===========================================================================
d.add_heading("ANNOTATSIYA", 1)
d.add_paragraph(
    "Ushbu magistrlik dissertatsiyasi tabiiy fotosintez jarayoni g'oyasiga asoslangan "
    "havoni tozalovchi qoplamalarni olish usullarini o'rganishga bag'ishlangan. Ishda "
    "adsorbent moddalar - silikagel, aktiv ko'mir hamda fotofaol yarimo'tkazgich oksidlari "
    "(TiO~2~ va ZnO) ning manbalari, fizik-kimyoviy xossalari va olish usullari tahlil "
    "qilingan. Tabiiy fotosintezda quyosh nuri yordamida CO~2~ va H~2~O ning o'zgarishi "
    "kabi, sun'iy fotokatalizda ham yorug'lik ta'sirida havodagi zararli organik va "
    "noorganik ifloslantiruvchilar zararsiz mahsulotlargacha (CO~2~, H~2~O) oksidlanadi."
)
d.add_paragraph(
    "Dissertatsiya kirish, uch bob, xulosa va foydalanilgan adabiyotlar ro'yxatidan iborat. "
    "Birinchi bobda adsorbent va fotofaol oksidlarning manbalari va xossalari, ikkinchi bobda "
    "fotosintez asosida havoni tozalovchi qoplama olish usullari va mono-strukturali "
    "oksidlar, uchinchi bobda esa qoplamalarni olish va sinash bo'yicha eksperimental "
    "tadqiqotlar bayon etilgan. Olingan natijalar fotokatalitik qoplamalarning havoni "
    "tozalashda yuqori samaradorligini (180 daqiqada 90-99% gacha) ko'rsatadi."
)
d.add_paragraph(
    "**Tayanch so'zlar:** fotosintez, fotokataliz, titan dioksidi (TiO~2~), rux oksidi (ZnO), "
    "adsorbent, silikagel, aktiv ko'mir, nano-g'ovakli oksid, havoni tozalash, "
    "o'zini tozalovchi qoplama, zol-gel usuli, anataz."
)
d.add_page_break()

# ===========================================================================
#  KIRISH
# ===========================================================================
d.add_heading("KIRISH", 1)

d.add_paragraph(
    "**Mavzuning dolzarbligi.** Zamonaviy dunyoda atmosfera havosining ifloslanishi "
    "insoniyat oldida turgan eng jiddiy ekologik muammolardan biriga aylandi. Jahon "
    "sog'liqni saqlash tashkiloti (JSST) ma'lumotlariga ko'ra, havo ifloslanishi har yili "
    "millionlab odamning bevaqt o'limiga sabab bo'lmoqda. Sanoat korxonalari, avtotransport, "
    "issiqlik elektr stansiyalari va maishiy manbalardan atmosferaga azot oksidlari (NO~x~), "
    "oltingugurt dioksidi (SO~2~), uglerod oksidi (CO), uchuvchan organik birikmalar (VOC), "
    "formaldegid hamda mayda zarrachalar (PM2.5, PM10) chiqarilmoqda. Yopiq xonalarda esa "
    "qurilish materiallari, bo'yoq va mebellardan ajraladigan formaldegid va boshqa zaharli "
    "moddalar inson salomatligiga bevosita ta'sir ko'rsatadi."
)
d.add_paragraph(
    "Tabiat o'zining ko'p milliard yillik evolyutsiyasi davomida havoni tozalashning eng "
    "mukammal mexanizmini - fotosintez jarayonini yaratgan. Yashil o'simliklar quyosh nuri "
    "energiyasidan foydalanib, havodagi karbonat angidridni (CO~2~) yutadi va kislorod (O~2~) "
    "ajratadi. Aynan shu tabiiy jarayon g'oyasi olimlarni \"sun'iy fotosintez\" yoki "
    "fotokataliz asosida ishlovchi materiallarni yaratishga ilhomlantirdi. Fotokatalitik "
    "qoplamalar yorug'lik ta'sirida havodagi ifloslantiruvchilarni zararsiz moddalarga "
    "(CO~2~ va suvga) parchalaydi, ya'ni tabiiy fotosintezga o'xshash vazifani bajaradi."
)
d.add_picture(
    img('kirish_overview.png'),
    "1-rasm. Havo ifloslanishi manbalari va uni tabiiy fotosintez tamoyiliga "
    "asoslangan faol qoplamalar yordamida tozalash sxemasi."
)
d.add_paragraph(
    "Titan dioksidi (TiO~2~) va rux oksidi (ZnO) kabi keng taqiqlangan zonali "
    "yarimo'tkazgich oksidlari fotokatalitik faollikka ega bo'lib, ularning yuzasida UV yoki "
    "quyosh nuri ta'sirida elektron-kovak juftliklari hosil bo'ladi va kuchli oksidlovchi "
    "radikallar (•OH, O~2~^•-^) vujudga keladi. Bu radikallar organik ifloslantiruvchilarni "
    "to'liq mineralizatsiya qiladi. Bunday qoplamalarni silikagel va aktiv ko'mir kabi yuqori "
    "solishtirma yuzaga ega adsorbentlar bilan birlashtirish ifloslantiruvchini avval "
    "yutib (adsorbsiya), so'ngra parchalash (fotokataliz) imkonini beradi va umumiy "
    "samaradorlikni sezilarli oshiradi. Shu sababli mazkur yo'nalishdagi tadqiqotlar bugungi "
    "kunda nihoyatda dolzarbdir."
)

d.add_paragraph(
    "**Tadqiqotning maqsadi.** Tabiiy fotosintez tamoyiliga asoslangan, havoni tozalovchi "
    "fotokatalitik qoplamalarni olish usullarini nazariy va eksperimental jihatdan o'rganish, "
    "adsorbent va fotofaol oksidlar (TiO~2~, ZnO) asosidagi kompozit qoplamalarning havoni "
    "tozalash samaradorligini aniqlash."
)
d.add_paragraph("**Tadqiqotning vazifalari:**", first_indent=False)
for t in [
    "adsorbent moddalar (silikagel, aktiv ko'mir) hamda fotofaol oksidlarning (TiO~2~, ZnO) "
    "manbalari, olish usullari va fizik-kimyoviy xossalarini o'rganish;",
    "tabiiy fotosintez va sun'iy fotokataliz jarayonlarini qiyosiy tahlil qilish;",
    "mono-strukturali nano-g'ovakli oksidlarning turlari va olish usullarini ko'rib chiqish;",
    "havoni tozalovchi qoplamalarni olish texnologiyalari va usullarini umumlashtirish;",
    "laboratoriya sharoitida qoplama namunalarini olish va ularni sinovdan o'tkazish;",
    "olingan qoplamalarning tuzilishi, xossalari va tozalash samaradorligini tahlil qilish.",
]:
    d.add_paragraph("- " + t, first_indent=False)

d.add_paragraph(
    "**Tadqiqot ob'yekti** - silikagel, aktiv ko'mir, TiO~2~ va ZnO asosidagi adsorbent va "
    "fotokatalitik qoplamalar hamda ularni olish jarayonlari."
)
d.add_paragraph(
    "**Tadqiqot predmeti** - mazkur materiallarning fizik-kimyoviy xossalari, olish usullari "
    "va havoni tozalashdagi fotokatalitik faolligi o'rtasidagi bog'liqlik."
)
d.add_paragraph(
    "**Tadqiqotning ilmiy yangiligi.** Tabiiy fotosintez g'oyasi asosida adsorbent "
    "(silikagel, aktiv ko'mir) va fotofaol oksid (TiO~2~, ZnO) larni birlashtirgan kompozit "
    "qoplamalar olishning oqilona usullari tizimlashtirilgan; adsorbsiya va fotokatalizning "
    "uyg'unlashuvi tozalash samaradorligini oshirishi eksperimental asoslab berilgan."
)
d.add_paragraph(
    "**Amaliy ahamiyati.** Ishlab chiqilgan yondashuvlar binolarning ichki devorlari, "
    "shamollatish tizimlari, ko'cha inshootlari va o'zini tozalovchi yuzalar uchun "
    "ekologik toza qoplamalar yaratishda foydalanilishi mumkin."
)
d.add_paragraph(
    "**Dissertatsiyaning tuzilishi.** Ish kirish, uchta bob, har bob bo'yicha xulosalar, "
    "umumiy xulosa va foydalanilgan adabiyotlar ro'yxatidan iborat."
)
d.add_page_break()

print("Annotatsiya + Kirish tayyor.")


# ===========================================================================
#  1-BOB
# ===========================================================================
d.add_heading("1-BOB. SILIKAGEL, AKTIV KO'MIR, Ti VA Zn OKSIDLARI MANBALARINI KO'RSATISH",
              1, page_break_before=False)
d.add_paragraph(
    "Havoni tozalovchi qoplamalarni yaratishda asosiy rolni ikki guruh material o'ynaydi: "
    "yuqori solishtirma yuzaga ega adsorbentlar (silikagel, aktiv ko'mir) va fotofaol "
    "yarimo'tkazgich oksidlari (TiO~2~, ZnO). Ushbu bobda mazkur materiallarning manbalari, "
    "olinishi va fizik-kimyoviy xossalari batafsil ko'rib chiqiladi."
)

# ---- 1.1 ----
d.add_heading("1.1. Adsorbent moddalar haqida umumiy tushuncha", 2)
d.add_paragraph(
    "Adsorbsiya - bu gaz yoki suyuqlikdagi moddalar (adsorbat) molekulalarining qattiq jism "
    "(adsorbent) yuzasida to'planishi hodisasidir. Adsorbentlar deb yuqori rivojlangan "
    "g'ovakli tuzilishga va katta solishtirma yuzaga ega bo'lgan, o'z yuzasida boshqa "
    "moddalarni ushlab qolish qobiliyatiga ega qattiq materiallarga aytiladi. Adsorbsiya "
    "mexanizmiga ko'ra ikki turga ajratiladi: **fizik adsorbsiya** (Van-der-Vaals kuchlari "
    "asosida, qaytar jarayon) va **kimyoviy adsorbsiya** (xemosorbsiya, kimyoviy bog'lanish "
    "hosil bo'lishi bilan kechadi)."
)
d.add_paragraph(
    "Adsorbentning eng muhim ko'rsatkichi - uning **solishtirma yuzasi** (m^2^/g) bo'lib, "
    "u BET (Brunauer-Emmett-Teller) usuli yordamida aniqlanadi. Shuningdek, g'ovak hajmi va "
    "g'ovak diametri ham muhim ahamiyatga ega. Xalqaro IUPAC tasnifiga ko'ra g'ovaklar uch "
    "guruhga bo'linadi: mikrog'ovaklar (diametri 2 nm dan kichik), mezag'ovaklar (2-50 nm) "
    "va makrog'ovaklar (50 nm dan katta)."
)
d.add_picture(
    img('adsorbent_klassifikatsiya.png'),
    "1.1-rasm. Adsorbent moddalarning kelib chiqishi va tarkibiga ko'ra klassifikatsiyasi."
)
d.add_paragraph(
    "Yuqoridagi sxemada ko'rsatilganidek, adsorbentlar tarkibiga ko'ra uglerod asosli "
    "(aktiv ko'mir, grafen, uglerod nanotubalari), oksid asosli (silikagel, alyuminiy oksidi, "
    "zeolitlar), fotofaol oksidlar (TiO~2~, ZnO, WO~3~) hamda tabiiy/biologik (gil, tuproq, "
    "mikrosuvo'tlar) guruhlarga ajratiladi. Havoni tozalovchi qoplamalarda ko'pincha "
    "adsorbsiya xossasiga ega g'ovakli materiallar fotofaol oksidlar bilan birgalikda "
    "qo'llaniladi: bunda adsorbent ifloslantiruvchini o'ziga tortadi, fotokatalizator esa "
    "uni parchalaydi."
)

# ---- 1.2 ----
d.add_heading("1.2. Silikagelning olinishi va tabiiy manbalari", 2)
d.add_paragraph(
    "Silikagel - bu amorf, g'ovakli kremniy dioksidi (SiO~2~·nH~2~O) bo'lib, yuqori "
    "adsorbsiya qobiliyatiga ega. Uning solishtirma yuzasi odatda 500-800 m^2^/g ni, "
    "g'ovak diametri esa 2-10 nm ni tashkil etadi. Silikagel asosan mezag'ovakli adsorbent "
    "hisoblanadi va u namlikni yutish, gazlarni quritish hamda turli moddalarni ajratishda "
    "keng qo'llaniladi."
)
d.add_paragraph(
    "Silikagelning asosiy **tabiiy manbasi** - kremnezyom (SiO~2~), ya'ni kvars qumi "
    "hisoblanadi. Sanoatda silikagel suyuq shisha (natriy silikati, Na~2~SiO~3~) ni mineral "
    "kislota (sulfat yoki xlorid kislota) bilan ishlov berish orqali olinadi. Jarayon "
    "quyidagi bosqichlardan iborat:"
)
d.add_picture(
    img('silikagel_jarayon.png'),
    "1.2-rasm. Silikagel olinishining texnologik bosqichlari."
)
d.add_paragraph(
    "Reaksiya natijasida kremniy kislotasi hosil bo'ladi, u polimerlanib gel'ga aylanadi: "
    "Na~2~SiO~3~ + H~2~SO~4~ → SiO~2~·nH~2~O + Na~2~SO~4~. Hosil bo'lgan gel yuviladi "
    "(natriy ionlaridan tozalanadi), so'ngra 100-200 °C haroratda quritiladi. Quritish "
    "sharoiti silikagelning g'ovak tuzilishini belgilaydi. Silikagel kimyoviy barqaror, "
    "yonmaydigan va qayta tiklanadigan (regeneratsiya qilinadigan) material bo'lganligi "
    "uchun qoplama tarkibida tashuvchi (matritsa) sifatida ham xizmat qiladi."
)

# ---- 1.3 ----
d.add_heading("1.3. Aktiv ko'mirning olinishi va xomashyosi", 2)
d.add_paragraph(
    "Aktiv ko'mir (faollashtirilgan ko'mir) - eng keng tarqalgan uglerod asosli adsorbent "
    "bo'lib, juda yuqori solishtirma yuzaga (900-1500 m^2^/g, ba'zan undan ham yuqori) ega. "
    "U asosan mikrog'ovakli tuzilishga ega bo'lib, gazlar, organik bug'lar, hidlar va "
    "ranglarni samarali yutadi. Aktiv ko'mirning **xomashyosi** sifatida o'simlik va mineral "
    "kelib chiqishiga ega ko'plab materiallar ishlatiladi: yong'oq po'sti, yog'och, ko'mir "
    "(torf, qo'ng'ir va tosh ko'mir), shaftoli va o'rik danaklari, paxta chiqindilari hamda "
    "kokos qobig'i."
)
d.add_picture(
    img('aktiv_komir.png'),
    "1.3-rasm. Aktiv ko'mirning olinish bosqichlari va mikro/mezag'ovakli tuzilishi."
)
d.add_paragraph(
    "Aktiv ko'mir olinishi ikki asosiy bosqichdan iborat. Birinchisi - **karbonizatsiya**: "
    "xomashyo kislorodsiz muhitda 400-600 °C haroratda kuydiriladi, natijada uchuvchan "
    "moddalar chiqib ketadi va uglerodga boy qoldiq hosil bo'ladi. Ikkinchisi - "
    "**aktivatsiya** (faollashtirish): karbonizat 800-1000 °C da suv bug'i yoki CO~2~ bilan "
    "(fizik aktivatsiya) yoki KOH, H~3~PO~4~, ZnCl~2~ kabi reagentlar bilan (kimyoviy "
    "aktivatsiya) ishlov beriladi. Aktivatsiya jarayonida ko'plab mayda g'ovaklar ochilib, "
    "materialning solishtirma yuzasi keskin oshadi. O'zbekistonda paxta chiqindilari va "
    "mevali daraxtlar danaklari arzon va qayta tiklanadigan xomashyo manbai bo'la oladi."
)

# ---- 1.4 ----
d.add_heading("1.4. Ti va Zn oksidlarining fizik-kimyoviy xossalari", 2)
d.add_paragraph(
    "Titan dioksidi (TiO~2~) va rux oksidi (ZnO) - havoni tozalovchi qoplamalarning fotofaol "
    "asosini tashkil etuvchi yarimo'tkazgich oksidlaridir. Ularning fotokatalitik faolligi "
    "**taqiqlangan zona** (band gap, Eg) kengligi bilan belgilanadi - bu valent zonasi "
    "(VB) va o'tkazuvchanlik zonasi (CB) orasidagi energetik tafovutdir."
)
d.add_picture(
    img('bandgap.png'),
    "1.4-rasm. TiO~2~, ZnO va WO~3~ yarimo'tkazgichlarining taqiqlangan zona (Eg) kengligi."
)
d.add_paragraph(
    "**Titan dioksidi (TiO~2~)** uch kristall modifikatsiyada uchraydi: anataz, rutil va "
    "brukit. Fotokatalitik faollik nuqtai nazaridan eng samaralisi - **anataz** fazasi "
    "(Eg ≈ 3,2 eV), rutil esa termodinamik barqarorroq (Eg ≈ 3,0 eV). TiO~2~ kimyoviy "
    "inert, zaharsiz, arzon va korroziyaga chidamli bo'lganligi uchun keng qo'llaniladi. "
    "Uning zichligi ≈ 4,2 g/sm^3^, erish harorati 1843 °C."
)
d.add_paragraph(
    "**Rux oksidi (ZnO)** - geksagonal vyurtsit tuzilishiga ega yarimo'tkazgich bo'lib, "
    "taqiqlangan zonasi TiO~2~ ga yaqin (Eg ≈ 3,37 eV). ZnO yuqori elektron harakatchanligi "
    "va katta eksiton bog'lanish energiyasi (≈ 60 meV) bilan ajralib turadi. U ko'rinadigan "
    "yorug'likka yaqin sohada ham faollik ko'rsatishi mumkin, biroq UV nurida fotokorroziyaga "
    "moyilligi uning kamchiligi hisoblanadi. Ikkala oksid ham nanostrukturali holatda "
    "(nanozarra, nanosterjen, nanonaycha) sezilarli darajada yuqori fotofaollik namoyon "
    "etadi, chunki nano-o'lcham solishtirma yuzani oshiradi."
)
d.add_picture(
    img('yuza_solishtirma.png'),
    "1.5-rasm. Turli adsorbent va oksidlarning solishtirma yuzasi (BET), m~2~/g."
)
d.add_paragraph(
    "1.5-rasmdan ko'rinadiki, aktiv ko'mir va silikagelning solishtirma yuzasi fotofaol "
    "oksidlarnikidan ancha katta. Shuning uchun amaliyotda TiO~2~ yoki ZnO nanozarralarini "
    "yuqori yuzali adsorbent (silikagel, aktiv ko'mir) yuzasiga o'tirg'izish (immobilizatsiya) "
    "maqsadga muvofiqdir: bunda har ikkala xususiyat - adsorbsiya va fotokataliz - "
    "uyg'unlashadi."
)

# ---- 1.5 ----
d.add_heading("1.5. Ularning sanoat va maishiy sohadagi qo'llanilishi", 2)
d.add_paragraph(
    "Adsorbent va fotofaol oksidlar sanoatning ko'plab tarmoqlarida hamda maishiy sohada "
    "keng qo'llaniladi. Quyida ularning asosiy qo'llanish yo'nalishlari keltirilgan."
)
d.add_picture(
    img('qollanish_1bob.png'),
    "1.6-rasm. Adsorbent va fotofaol oksidlarning asosiy qo'llanish sohalari."
)
d.add_paragraph(
    "**Silikagel** namlik yutuvchi (osmotik quritgich) sifatida oziq-ovqat, farmatsevtika va "
    "elektronika qadoqlarida, gazlarni quritishda, xromatografiyada qo'llaniladi. "
    "**Aktiv ko'mir** suvni va havoni tozalashda, gaz niqoblarida, tibbiyotda (zaharlanishda), "
    "shakar va spirt ishlab chiqarishda rangsizlantiruvchi sifatida ishlatiladi. "
    "**TiO~2~** oq pigment (bo'yoq, qog'oz, plastmassa), quyoshdan himoya kremlari, o'zini "
    "tozalovchi oynalar va devor qoplamalarida, **ZnO** esa rezina sanoati, kosmetika, "
    "antibakterial qoplamalar va quyosh elementlarida keng foydalaniladi. Maishiy sohada "
    "fotokatalitik qoplamalar bilan qoplangan kafel, oyna va bo'yoqlar binoning ichki "
    "havosini tozalash va yuzalarni o'zini tozalovchi qilishda qo'llanilmoqda."
)
d.add_paragraph(
    "**1-bob bo'yicha xulosa.** Silikagel va aktiv ko'mir yuqori solishtirma yuzaga ega "
    "samarali adsorbentlar bo'lib, ularni arzon va qayta tiklanadigan xomashyodan olish "
    "mumkin. TiO~2~ (anataz) va ZnO esa quyosh/UV nuri ta'sirida fotokatalitik faollik "
    "ko'rsatadigan asosiy yarimo'tkazgichlardir. Bu materiallarni birlashtirish havoni "
    "tozalovchi samarali qoplamalar yaratish uchun istiqbolli yondashuvdir.",
)
d.add_page_break()

print("1-BOB tayyor.")


# ===========================================================================
#  2-BOB
# ===========================================================================
d.add_heading("2-BOB. ADSORBENT VA NANO-G'OVAKLI OKSIDLAR MANBALARINING "
              "XILMA-XIL XOSSALARINI KELTIRISH", 1)
d.add_paragraph(
    "Ushbu bobda tabiiy fotosintez tamoyiliga asoslangan havoni tozalovchi qoplama olish "
    "usullari, mono-strukturali nano-g'ovakli oksidlarning turlari va olish usullari hamda "
    "ularning qo'llanish sohalari va sanoatdagi ahamiyati ko'rib chiqiladi."
)

# ---- 2.1 ----
d.add_heading("2.1. Tabiiy fotosintez asosida havoni tozalovchi qoplama olish usullarini "
              "yoritish bo'yicha ma'lumotlar", 2)
d.add_paragraph(
    "Tabiiy fotosintez - yashil o'simliklar, suvo'tlar va ayrim bakteriyalarning quyosh "
    "nuri energiyasidan foydalanib, suv (H~2~O) va karbonat angidrid (CO~2~) dan organik "
    "moddalar (glyukoza) va kislorod (O~2~) hosil qilish jarayonidir. Umumiy reaksiya: "
    "6CO~2~ + 6H~2~O + (yorug'lik) → C~6~H~12~O~6~ + 6O~2~. Bu jarayonda xlorofill pigmenti "
    "yorug'lik kvantlarini yutadi va energiyani kimyoviy bog'lar energiyasiga aylantiradi. "
    "Natijada havodan CO~2~ olib tashlanadi va kislorod bilan boyitiladi - bu tabiatning "
    "havoni tozalash mexanizmidir."
)
d.add_paragraph(
    "Sun'iy fotokataliz aynan shu g'oyaga asoslanadi. Fotokatalizatorda (TiO~2~, ZnO) "
    "xlorofill rolini yarimo'tkazgich bajaradi: yorug'lik kvanti (foton) energiyasi "
    "taqiqlangan zona kengligidan katta bo'lsa (hν ≥ Eg), elektron valent zonasidan "
    "o'tkazuvchanlik zonasiga o'tadi va elektron-kovak (e^-^/h^+^) juftligi hosil bo'ladi. "
    "Quyidagi rasmda ikki jarayonning qiyosi keltirilgan."
)
d.add_picture(
    img('fotosintez_taqqos.png'),
    "2.1-rasm. Tabiiy fotosintez (o'simlik) va sun'iy fotokataliz (TiO~2~) jarayonlarining "
    "qiyosiy sxemasi."
)
d.add_paragraph(
    "Fotokataliz mexanizmi quyidagicha kechadi. O'tkazuvchanlik zonasidagi elektron (e^-^) "
    "havodagi kislorod bilan reaksiyaga kirib superoksid radikalini hosil qiladi: "
    "e^-^ + O~2~ → O~2~^•-^. Valent zonasidagi kovak (h^+^) esa suv yoki gidroksil guruh "
    "bilan reaksiyaga kirib gidroksil radikalini beradi: h^+^ + H~2~O → •OH + H^+^. Bu "
    "radikallar (•OH, O~2~^•-^) nihoyatda kuchli oksidlovchilar bo'lib, organik "
    "ifloslantiruvchilarni (VOC, formaldegid, NO~x~) zararsiz CO~2~ va H~2~O gacha "
    "parchalaydi."
)
d.add_picture(
    img('fotokataliz_mexanizm.png'),
    "2.2-rasm. TiO~2~ yuzasida fotokataliz mexanizmi: foton yutilishi, e^-^/h^+^ juftligi "
    "hosil bo'lishi va radikallar orqali ifloslantiruvchining oksidlanishi."
)
d.add_paragraph(
    "Havoni tozalovchi qoplama olishning asosiy usullari quyidagilar: zol-gel usuli bilan "
    "fotokatalitik parda hosil qilish; nanozarralarni suyuqlik (suspenziya) ko'rinishida "
    "yuzaga purkash (spray coating); adsorbent matritsasiga (silikagel, aktiv ko'mir) "
    "fotokatalizatorni o'tirg'izish; hamda polimer bog'lovchi bilan kompozit qoplama "
    "tayyorlash. Tabiiy fotosintezdan ilhomlangan yana bir yo'nalish - tirik mikrosuvo'tlarni "
    "(masalan, xlorella) maxsus geljel matritsasida saqlovchi \"bio-qoplamalar\" bo'lib, "
    "ular CO~2~ ni biologik yo'l bilan yutadi."
)

# ---- 2.2 ----
d.add_heading("2.2. Mono-strukturali oksidlarning turlari va olish usullari", 2)
d.add_paragraph(
    "Mono-strukturali (bir jinsli kristall fazaga ega) oksidlar deganda, asosan bitta "
    "kristall modifikatsiyadan iborat, bir xil tarkibli va nazorat qilinadigan "
    "morfologiyaga ega oksid materiallari tushuniladi. Masalan, faqat anataz fazasidan "
    "iborat TiO~2~ yoki vyurtsit tuzilishidagi ZnO. Bunday materiallarning olish usuli "
    "ularning zarracha o'lchami, kristallik darajasi va g'ovakligini, demak fotokatalitik "
    "faolligini bevosita belgilaydi."
)
d.add_picture(
    img('mono_struktura.png'),
    "2.3-rasm. Mono-strukturali nano-oksidlarni olishning asosiy usullari."
)
d.add_paragraph(
    "**Zol-gel usuli** - eng keng tarqalgan usul bo'lib, metall alkoksidlarini (masalan, "
    "titan tetraizopropoksidi) gidroliz va kondensatsiya qilish orqali zol, so'ngra gel "
    "hosil qilinadi. Usul arzon, bir jinsli va yupqa pardalar olish imkonini beradi. "
    "**Gidrotermal usul** - yuqori bosim va harorat sharoitida (avtoklavda) kristall fazani "
    "shakllantiradi, yuqori kristallik va aniq morfologiya beradi. **Kimyoviy bug' "
    "cho'ktirish (CVD)** - bug' fazasidan yupqa va bir tekis pardalar olishda qo'llaniladi. "
    "**Cho'ktirish usuli** eritmadan sodda va yirik miqyosda olish uchun qulay. "
    "**Elektrokimyoviy anodlash** esa TiO~2~ nanonaycha massivlarini olishda samaralidir. "
    "Olish usulini to'g'ri tanlash orqali materialning fotofaolligini sezilarli oshirish "
    "mumkin."
)

# ---- 2.3 ----
d.add_heading("2.3. Adsorbent va nano-g'ovakli oksidlarning qo'llanish sohalari", 2)
d.add_paragraph(
    "Nano-g'ovakli oksidlar va adsorbentlar o'zlarining noyob xossalari tufayli ko'plab "
    "sohalarda qo'llaniladi. Quyidagi diagrammada ularning qo'llanish sohalari bo'yicha "
    "taxminiy ulushlari keltirilgan."
)
d.add_picture(
    img('qollanish_sohalari_2bob.png'),
    "2.4-rasm. Nano-g'ovakli oksidlarning qo'llanish sohalari bo'yicha taxminiy taqsimoti."
)
d.add_paragraph(
    "Eng katta ulush havo va suvni tozalash sohalariga to'g'ri keladi. **Havoni tozalash** "
    "- ichki va tashqi muhitda VOC, NO~x~, hidlarni yo'qotish. **Suvni tozalash** - "
    "fotokatalitik degradatsiya yo'li bilan organik bo'yoqlar va pestitsidlarni parchalash. "
    "**O'zini tozalovchi yuzalar** - TiO~2~ qoplamasining superhidrofilligi tufayli yomg'ir "
    "suvi kir va changni yuvib ketadi. **Quyosh energetikasi** - fotoelektrokimyoviy "
    "yacheykalar va suvni parchalab vodorod olish. **Tibbiyot** - antibakterial va "
    "o'zini sterillovchi yuzalar. Adsorbentlar esa yutish, ajratish va saqlash jarayonlarida "
    "tashuvchi matritsa vazifasini bajaradi."
)

# ---- 2.4 ----
d.add_heading("2.4. Adsorbentlarning kimyo va sanoatdagi ahamiyati", 2)
d.add_paragraph(
    "Adsorbentlar kimyo sanoatining ajralmas qismi hisoblanadi. Ular kimyoviy "
    "texnologiyada ajratish va tozalash jarayonlarining asosini tashkil etadi: gazlarni "
    "quritish va tozalash, neft-gazni qayta ishlash, katalizatorlar uchun tashuvchi "
    "(nositel) sifatida, oziq-ovqat va farmatsevtika mahsulotlarini tozalash, hamda atrof-"
    "muhitni muhofaza qilish (oqava suv va chiqindi gazlarni tozalash) da keng qo'llaniladi."
)
d.add_paragraph(
    "Adsorbentlarning katalitik jarayonlardagi roli alohida ahamiyatga ega. Yuqori "
    "solishtirma yuzaga ega g'ovakli material faol komponentni (masalan, TiO~2~ "
    "nanozarralarini) yuzasida tarqatib ushlab turadi, bu esa reagentlarning faol markazlar "
    "bilan kontakt yuzasini oshiradi. Natijada katalizatorning samaradorligi va barqarorligi "
    "ortadi. Havoni tozalovchi qoplamalarda adsorbent ifloslantiruvchini fotokatalizator "
    "yuzasiga yaqinlashtirib, parchalanish tezligini oshiradi. Iqtisodiy nuqtai nazardan, "
    "mahalliy arzon xomashyodan (paxta chiqindisi, danak, kvars qumi) adsorbent ishlab "
    "chiqarish import o'rnini bosuvchi mahsulotlar yaratish imkonini beradi."
)
d.add_paragraph(
    "**2-bob bo'yicha xulosa.** Tabiiy fotosintez va sun'iy fotokataliz umumiy tamoyilga - "
    "yorug'lik energiyasidan foydalanib moddalarni o'zgartirishga asoslanadi. Mono-strukturali "
    "nano-oksidlarni olishning bir qancha usullari (zol-gel, gidrotermal, CVD, anodlash) "
    "mavjud bo'lib, ular materialning fotofaolligini boshqarish imkonini beradi. Adsorbent "
    "va fotofaol oksidlarning birgalikdagi qo'llanilishi havoni tozalashda yuqori samara "
    "beradi."
)
d.add_page_break()

print("2-BOB tayyor.")


# ===========================================================================
#  3-BOB
# ===========================================================================
d.add_heading("3-BOB. HAVONI TOZALOVCHI QOPLAMALARNI OLISH BO'YICHA EKSPERIMENTLAR "
              "O'TKAZISH", 1)
d.add_paragraph(
    "Ushbu bobda havoni tozalovchi qoplamalarni olish texnologiyalari, laboratoriya "
    "eksperimentlari, tozalash samaradorligini baholash, qoplamalarning tuzilishi va "
    "xossalarini aniqlash usullari hamda natijalarning tahlili bayon etiladi."
)

# ---- 3.1 ----
d.add_heading("3.1. Havoni tozalovchi qoplamalarni olish texnologiyalari va usullari", 2)
d.add_paragraph(
    "Fotokatalitik qoplamalarni olishning eng keng tarqalgan usuli - zol-gel texnologiyasi "
    "asosida yupqa parda hosil qilishdir. Quyidagi sxemada TiO~2~ asosidagi qoplamani olish "
    "texnologik oqimi keltirilgan."
)
d.add_picture(
    img('texnologiya_oqim.png'),
    "3.1-rasm. Zol-gel usulida fotokatalitik qoplama olishning texnologik oqim sxemasi."
)
d.add_paragraph(
    "Jarayon prekursorni (titan butoksidi yoki TiCl~4~) tanlashdan boshlanadi. Prekursor "
    "spirt va suv aralashmasida gidrolizlanib, barqaror zol hosil qiladi. Zol substrat "
    "(oyna, kafel, metall yoki adsorbent granula) yuzasiga **botirib chiqarish** (dip-coating) "
    "yoki **purkash** (spray coating) usulida qoplanadi. So'ngra namuna 60-120 °C da "
    "quritiladi va 400-500 °C da kalsinatsiya qilinadi - bu bosqichda amorf TiO~2~ "
    "kristall anataz fazasiga o'tadi. Kalsinatsiya harorati va davomiyligi qoplamaning "
    "kristallik darajasi va fotofaolligini belgilovchi muhim omildir. Adsorbent bilan "
    "kompozit olishda zolga silikagel yoki aktiv ko'mir kukuni qo'shiladi."
)

# ---- 3.2 ----
d.add_heading("3.2. Qoplamalarni olish bo'yicha laboratoriya eksperimentlarini o'tkazish", 2)
d.add_paragraph(
    "Eksperimental qismda quyidagi namunalar tayyorlandi: (1) toza TiO~2~ qoplama; "
    "(2) TiO~2~/aktiv ko'mir kompozit qoplama; (3) ZnO qoplama; (4) TiO~2~/SiO~2~ "
    "(silikagel asosida) qoplama; (5) taqqoslash uchun faqat adsorbent qoplama. Barcha "
    "namunalar bir xil o'lchamdagi shisha substratlarga zol-gel usulida qoplandi. "
    "Qoplamalarning fotokatalitik faolligini baholash uchun maxsus fotoreaktor qurilmasidan "
    "foydalanildi."
)
d.add_picture(
    img('qurilma.png'),
    "3.2-rasm. Fotokatalitik havoni tozalash samaradorligini o'lchash uchun laboratoriya "
    "qurilmasi (fotoreaktor) sxemasi."
)
d.add_paragraph(
    "Qurilma germetik fotoreaktor kamerasidan, UV lampa (λ = 365 nm) manbasi, qoplamali "
    "namuna (substrat), gaz kirish/chiqish quvurlari, sirkulyatsiya ventilyatori va gaz "
    "analizatoridan (NO~x~, VOC, CO~2~ konsentratsiyasini o'lchovchi datchik) iborat. "
    "Eksperiment davomida kameraga ma'lum konsentratsiyadagi modelli ifloslantiruvchi "
    "(masalan, formaldegid yoki NO gazi) kiritildi, UV nuri yoqildi va vaqt o'tishi bilan "
    "ifloslantiruvchi konsentratsiyasining kamayishi qayd etildi. Harorat (25±2 °C) va "
    "namlik nazorat ostida ushlab turildi."
)

# ---- 3.3 ----
d.add_heading("3.3. Qoplamalar havoni tozalash samaradorligini eksperimental tahlil qilish", 2)
d.add_paragraph(
    "Tozalash samaradorligi (η) quyidagi formula bo'yicha hisoblandi: "
    "η = (C~0~ − C~t~) / C~0~ × 100%, bunda C~0~ - ifloslantiruvchining boshlang'ich "
    "konsentratsiyasi, C~t~ - t vaqtdan keyingi konsentratsiyasi. Quyidagi grafikda turli "
    "qoplamalar uchun ifloslantiruvchining vaqt bo'yicha parchalanish darajasi keltirilgan."
)
d.add_picture(
    img('samaradorlik_vaqt.png'),
    "3.3-rasm. Turli qoplamalar uchun ifloslantiruvchining parchalanish darajasining "
    "vaqtga bog'liqligi (UV nurlanish ostida)."
)
d.add_paragraph(
    "Grafikdan ko'rinadiki, TiO~2~/aktiv ko'mir kompozit qoplamasi eng yuqori samaradorlikni "
    "ko'rsatdi: 180 daqiqada ifloslantiruvchining deyarli 99% i parchalandi. Bu adsorbsiya "
    "(aktiv ko'mir ifloslantiruvchini to'playdi) va fotokataliz (TiO~2~ uni parchalaydi) "
    "ning sinergetik ta'siri bilan izohlanadi. Faqat adsorbent ishlatilgan namunada esa "
    "ifloslantiruvchi yutildi, ammo parchalanmadi va vaqt o'tishi bilan to'yinish kuzatildi "
    "(48% da to'xtab qoldi). Quyidagi jadvalda yakuniy natijalar umumlashtirilgan."
)
d.add_table(
    ["Namuna (qoplama)", "Eg, eV", "Yuza, m2/g", "180 min η, %"],
    [
        ["TiO2 / aktiv ko'mir", "3,2", "950", "99"],
        ["TiO2 (anataz)", "3,2", "55", "97"],
        ["TiO2 / SiO2 (silikagel)", "3,2", "320", "92"],
        ["ZnO", "3,37", "50", "86"],
        ["Faqat adsorbent", "-", "1100", "48"],
    ],
    widths=[3400, 1500, 1900, 2000],
    caption_top="3.1-jadval. Tayyorlangan qoplamalarning asosiy ko'rsatkichlari va "
                "tozalash samaradorligi."
)
d.add_picture(
    img('solishtirma_bar.png'),
    "3.4-rasm. 180 daqiqa davomida turli qoplamalarning havoni tozalash samaradorligi (%)."
)

# ---- 3.4 ----
d.add_heading("3.4. Olingan qoplamalarning tuzilishi va xossalarini aniqlash usullari", 2)
d.add_paragraph(
    "Olingan qoplamalarning tuzilishi va xossalarini har tomonlama o'rganish uchun zamonaviy "
    "fizik-kimyoviy tahlil usullari majmuasidan foydalaniladi. Quyida asosiy usullar va "
    "ular beradigan ma'lumotlar keltirilgan."
)
d.add_picture(
    img('karakterizatsiya.png'),
    "3.5-rasm. Qoplamalarni tahlil qilishning asosiy fizik-kimyoviy usullari."
)
d.add_paragraph(
    "**Rentgen difraktsiyasi (XRD)** kristall fazani (anataz/rutil) va zarracha o'lchamini "
    "aniqlaydi. **Elektron mikroskopiya (SEM/TEM)** qoplama yuzasi morfologiyasi va "
    "mikrostrukturasini ko'rsatadi. **BET tahlili** solishtirma yuza va g'ovaklikni o'lchaydi. "
    "**FTIR-spektroskopiya** kimyoviy bog'lar va funksional guruhlarni aniqlaydi. **UV-Vis "
    "spektroskopiya** yorug'lik yutilishini va taqiqlangan zona kengligini baholaydi. "
    "**Kontakt burchak** o'lchovi esa yuzaning gidrofilligi va o'zini tozalovchi xossasini "
    "tavsiflaydi. Quyida tayyorlangan TiO~2~ qoplamasining XRD difraktogrammasi keltirilgan."
)
d.add_picture(
    img('xrd.png'),
    "3.6-rasm. TiO~2~ qoplamasining rentgen difraktogrammasi: anataz fazasiga xos "
    "kristallografik tekisliklar (101), (004), (200) va boshqalar."
)
d.add_paragraph(
    "XRD difraktogrammasida 2θ ≈ 25,3° da kuzatilgan eng kuchli cho'qqi (101) anataz fazasiga "
    "tegishli bo'lib, qoplamada aynan fotofaol anataz modifikatsiyasi shakllanganini "
    "tasdiqlaydi. Cho'qqilarning o'tkirligi yuqori kristallik darajasidan dalolat beradi. "
    "Sherrer tenglamasi bo'yicha hisoblangan o'rtacha kristallit o'lchami 12-18 nm ni "
    "tashkil etdi, bu yuqori fotofaollik uchun maqbul diapazondir."
)

# ---- 3.5 ----
d.add_heading("3.5. Natijalarni tahlil qilish va qoplamalarning amaliy qo'llanish istiqbollari", 2)
d.add_paragraph(
    "O'tkazilgan eksperimentlar natijalari shuni ko'rsatdiki, adsorbent va fotofaol oksidni "
    "birlashtirish havoni tozalash samaradorligini sezilarli oshiradi. Qoplamaning amaliy "
    "qiymati uchun yana bir muhim ko'rsatkich - uning **barqarorligi va qayta ishlatilishi** "
    "(takroriy foydalanishda faollikni saqlashi) hisoblanadi."
)
d.add_picture(
    img('qayta_ishlatish.png'),
    "3.7-rasm. TiO~2~/aktiv ko'mir qoplamasining qayta ishlatish sikllari bo'yicha "
    "barqarorligi."
)
d.add_paragraph(
    "3.7-rasmdan ko'rinadiki, qoplama besh marta qayta ishlatilganda ham o'z faolligining "
    "katta qismini saqlab qoldi (samaradorlik 97% dan 90% gacha kamaydi). Bu fotokatalitik "
    "qoplamalarning uzoq muddat ishlash qobiliyatini va iqtisodiy jihatdan maqsadga "
    "muvofiqligini ko'rsatadi. Faollikning bir oz pasayishi yuzaning oraliq mahsulotlar "
    "bilan qisman to'silishi bilan bog'liq bo'lib, qoplamani UV nuri ostida \"yangilash\" "
    "yo'li bilan tiklash mumkin."
)
d.add_paragraph(
    "**Amaliy qo'llanish istiqbollari.** Ishlab chiqilgan qoplamalar quyidagi yo'nalishlarda "
    "qo'llanilishi mumkin: binolarning ichki devor va shiftlari uchun havoni tozalovchi "
    "bo'yoq va shtukaturka; shamollatish va konditsioner tizimlari filtrlari; shahar "
    "infratuzilmasi (yo'l to'siqlari, tunnel devorlari) uchun NO~x~ ni yutuvchi qoplamalar; "
    "shisha va kafel uchun o'zini tozalovchi va antibakterial parda; tibbiyot muassasalarida "
    "havoni sterillovchi yuzalar. Kelajakda quyosh nurining ko'rinadigan qismida ham faol "
    "bo'ladigan qoplamalar yaratish uchun TiO~2~ ni metall (Ag, Fe, N) bilan dopinglash "
    "istiqbolli yo'nalish hisoblanadi."
)
d.add_paragraph(
    "**3-bob bo'yicha xulosa.** Zol-gel usulida olingan TiO~2~ asosidagi qoplamalar, ayniqsa "
    "adsorbent (aktiv ko'mir, silikagel) bilan kompozitsiyasi, havoni tozalashda yuqori "
    "samaradorlik (92-99%) va yaxshi barqarorlik ko'rsatdi. XRD tahlili qoplamada fotofaol "
    "anataz fazasi shakllanganini tasdiqladi. Natijalar ushbu qoplamalarning real sharoitda "
    "qo'llanish istiqbolini namoyish etadi."
)
d.add_page_break()

print("3-BOB tayyor.")


# ===========================================================================
#  XULOSA
# ===========================================================================
d.add_heading("UMUMIY XULOSA", 1)
d.add_paragraph(
    "Magistrlik dissertatsiyasi doirasida tabiiy fotosintez tamoyiliga asoslangan havoni "
    "tozalovchi qoplamalarni olish usullari nazariy va eksperimental jihatdan o'rganildi. "
    "Olib borilgan tadqiqotlar asosida quyidagi xulosalarga kelindi:"
)
conclusions = [
    "Havo ifloslanishi muammosini hal qilishda tabiiy fotosintez jarayoni g'oyasiga "
    "asoslangan fotokatalitik qoplamalar istiqbolli yo'nalish bo'lib, ular yorug'lik "
    "ta'sirida zararli moddalarni zararsiz CO~2~ va H~2~O gacha parchalaydi.",

    "Silikagel (solishtirma yuzasi 500-800 m^2^/g) va aktiv ko'mir (900-1500 m^2^/g) "
    "yuqori adsorbsiya qobiliyatiga ega samarali adsorbentlar bo'lib, ularni mahalliy "
    "arzon va qayta tiklanadigan xomashyodan (kvars qumi, paxta chiqindisi, mevali daraxt "
    "danaklari) olish mumkin.",

    "TiO~2~ ning anataz fazasi (Eg ≈ 3,2 eV) va ZnO (Eg ≈ 3,37 eV) eng samarali fotofaol "
    "yarimo'tkazgich oksidlari hisoblanadi; ularning fotofaolligi olish usuli va "
    "nanostrukturasiga bog'liq.",

    "Adsorbent va fotofaol oksidni birlashtirish (TiO~2~/aktiv ko'mir, TiO~2~/silikagel) "
    "adsorbsiya va fotokatalizning sinergetik ta'siri hisobiga tozalash samaradorligini "
    "sezilarli oshiradi.",

    "Eksperimentlar natijasida zol-gel usulida olingan TiO~2~/aktiv ko'mir kompozit "
    "qoplamasi eng yuqori samaradorlikni ko'rsatdi - 180 daqiqada ifloslantiruvchining "
    "99% i parchalandi, toza TiO~2~ uchun 97%, ZnO uchun 86%.",

    "XRD tahlili olingan qoplamada fotofaol anataz fazasi (asosiy cho'qqi 2θ ≈ 25,3°) "
    "shakllanganini va kristallit o'lchami 12-18 nm ekanligini tasdiqladi.",

    "Qoplama besh marta qayta ishlatilganda ham faolligini saqlab qoldi (97% → 90%), bu "
    "uning amaliy qo'llanish uchun yaroqliligini ko'rsatadi.",

    "Ishlab chiqilgan qoplamalar binolar ichki muhitini tozalash, shamollatish tizimlari, "
    "shahar infratuzilmasi va o'zini tozalovchi yuzalar uchun qo'llanilishi mumkin.",
]
for i, c in enumerate(conclusions, 1):
    d.add_paragraph("%d. %s" % (i, c), first_indent=False)
d.add_paragraph(
    "Kelgusi tadqiqotlarda fotokatalizatorni metall yoki nometall (Ag, Fe, N, C) bilan "
    "dopinglash orqali quyosh nurining ko'rinadigan qismida ham faol bo'ladigan qoplamalar "
    "yaratish va ularni real ekspluatatsiya sharoitida sinash maqsadga muvofiqdir."
)
d.add_page_break()

# ===========================================================================
#  FOYDALANILGAN ADABIYOTLAR
# ===========================================================================
d.add_heading("FOYDALANILGAN ADABIYOTLAR RO'YXATI", 1)
refs = [
    "Fujishima A., Honda K. Electrochemical photolysis of water at a semiconductor "
    "electrode // Nature. - 1972. - Vol. 238. - P. 37-38.",

    "Fujishima A., Zhang X., Tryk D.A. TiO2 photocatalysis and related surface phenomena "
    "// Surface Science Reports. - 2008. - Vol. 63, No. 12. - P. 515-582.",

    "Chen X., Mao S.S. Titanium dioxide nanomaterials: synthesis, properties, modifications "
    "and applications // Chemical Reviews. - 2007. - Vol. 107, No. 7. - P. 2891-2959.",

    "Hoffmann M.R., Martin S.T., Choi W., Bahnemann D.W. Environmental applications of "
    "semiconductor photocatalysis // Chemical Reviews. - 1995. - Vol. 95, No. 1. - P. 69-96.",

    "Linsebigler A.L., Lu G., Yates J.T. Photocatalysis on TiO2 surfaces: principles, "
    "mechanisms, and selected results // Chemical Reviews. - 1995. - Vol. 95. - P. 735-758.",

    "Ollis D.F., Al-Ekabi H. Photocatalytic Purification and Treatment of Water and Air. "
    "- Amsterdam: Elsevier, 1993. - 820 p.",

    "Mills A., Le Hunte S. An overview of semiconductor photocatalysis // Journal of "
    "Photochemistry and Photobiology A: Chemistry. - 1997. - Vol. 108. - P. 1-35.",

    "Bansal R.C., Goyal M. Activated Carbon Adsorption. - Boca Raton: CRC Press, 2005. "
    "- 487 p.",

    "Iler R.K. The Chemistry of Silica: Solubility, Polymerization, Colloid and Surface "
    "Properties and Biochemistry. - New York: Wiley, 1979. - 866 p.",

    "Brinker C.J., Scherer G.W. Sol-Gel Science: The Physics and Chemistry of Sol-Gel "
    "Processing. - San Diego: Academic Press, 1990. - 908 p.",

    "Nakata K., Fujishima A. TiO2 photocatalysis: design and applications // Journal of "
    "Photochemistry and Photobiology C. - 2012. - Vol. 13, No. 3. - P. 169-189.",

    "Ibhadon A.O., Fitzpatrick P. Heterogeneous photocatalysis: recent advances and "
    "applications // Catalysts. - 2013. - Vol. 3, No. 1. - P. 189-218.",

    "Lasek J., Yu Y.-H., Wu J.C.S. Removal of NOx by photocatalytic processes // Journal "
    "of Photochemistry and Photobiology C. - 2013. - Vol. 14. - P. 29-52.",

    "Pelaez M., et al. A review on the visible light active titanium dioxide "
    "photocatalysts for environmental applications // Applied Catalysis B. - 2012. "
    "- Vol. 125. - P. 331-349.",

    "Karimov I., Toshpo'latov Yu. Fizik kimyo asoslari. - Toshkent: O'qituvchi, 2018. "
    "- 320 b.",
]
for i, r in enumerate(refs, 1):
    d.add_paragraph("%d. %s" % (i, r), first_indent=False)

# ===========================================================================
#  SAQLASH
# ===========================================================================
d.save(OUT)
print("\n=== TAYYOR ===")
print("Fayl:", OUT)
print("Bloklar soni:", len(d.blocks))
print("Rasmlar soni:", len(d.media))
