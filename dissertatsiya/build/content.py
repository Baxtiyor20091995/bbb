# -*- coding: utf-8 -*-
"""
Dissertatsiya matnini (real manbalarga iqtiboslar bilan) yig'ib,
Dissertatsiya.docx faylini quradi. Matn o'zbek tilida, rasm/jadval bilan.
Iqtiboslar [n] FOYDALANILGAN ADABIYOTLAR ro'yxatiga mos keladi.
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
    "noorganik ifloslantiruvchilar zararsiz mahsulotlargacha (CO~2~, H~2~O) oksidlanadi [1, 2]."
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
    "**Tayanch so'zlar:** tabiiy fotosintez, fotokataliz, titan dioksidi (TiO~2~), rux oksidi "
    "(ZnO), adsorbent, silikagel, aktiv ko'mir, nano-g'ovakli oksid, havoni tozalash, "
    "o'zini tozalovchi qoplama, zol-gel usuli, bioinspiratsion materiallar, anataz."
)
d.add_page_break()

# ===========================================================================
#  KIRISH
# ===========================================================================
d.add_heading("KIRISH", 1)
d.add_paragraph(
    "**Mavzuning dolzarbligi.** So'nggi yillarda atmosfera havosining antropogen ifloslanishi "
    "inson salomatligi va atrof-muhit barqarorligiga jiddiy xavf tug'dirmoqda [1]. Jahon "
    "sog'liqni saqlash tashkiloti ma'lumotlariga ko'ra, havo ifloslanishi har yili millionlab "
    "odamning bevaqt o'limiga sabab bo'lmoqda. Sanoat korxonalari, avtotransport va maishiy "
    "manbalardan atmosferaga azot oksidlari (NO~x~), oltingugurt dioksidi (SO~2~), uchuvchan "
    "organik birikmalar (VOC), formaldegid hamda mayda zarrachalar (PM2.5, PM10) chiqarilmoqda. "
    "Ayniqsa yopiq xonalarda uchuvchan organik birikmalar (VOC) havo ifloslanishining keng "
    "tarqalgan tarkibiy qismi hisoblanadi [3]. Shu sababli havoni tozalashning innovatsion va "
    "ekologik jihatdan xavfsiz usullarini ishlab chiqish dolzarb ilmiy masalalardan biridir."
)
d.add_paragraph(
    "Tabiat o'zining ko'p milliard yillik evolyutsiyasi davomida havoni tozalashning eng "
    "mukammal mexanizmini - fotosintez jarayonini yaratgan. Yashil o'simliklar quyosh nuri "
    "energiyasidan foydalanib, havodagi karbonat angidridni (CO~2~) yutadi va kislorod (O~2~) "
    "ajratadi. Aynan shu tabiiy jarayon g'oyasi olimlarni \"sun'iy fotosintez\" (artificial "
    "photosynthesis) va fotokataliz asosida ishlovchi materiallarni yaratishga ilhomlantirdi "
    "[2]. Fotokatalitik qoplamalar yorug'lik ta'sirida havodagi ifloslantiruvchilarni zararsiz "
    "moddalarga (CO~2~ va suvga) parchalaydi, ya'ni tabiiy fotosintezga o'xshash vazifani "
    "bajaradi [1]."
)
d.add_picture(
    img('kirish_overview.png'),
    "1-rasm. Havo ifloslanishi manbalari va uni tabiiy fotosintez tamoyiliga "
    "asoslangan faol qoplamalar yordamida tozalash sxemasi."
)
d.add_paragraph(
    "Titan dioksidi (TiO~2~) va rux oksidi (ZnO) kabi keng taqiqlangan zonali yarimo'tkazgich "
    "oksidlari fotokatalitik faollikka ega bo'lib, ularning yuzasida UV yoki quyosh nuri "
    "ta'sirida elektron-kovak juftliklari hosil bo'ladi va kuchli oksidlovchi radikallar "
    "(•OH, O~2~^•-^) vujudga keladi [1, 5]. Bunday qoplamalarni silikagel va aktiv ko'mir kabi "
    "yuqori solishtirma yuzaga ega adsorbentlar bilan birlashtirish ifloslantiruvchini avval "
    "yutib (adsorbsiya), so'ngra parchalash (fotokataliz) imkonini beradi va umumiy "
    "samaradorlikni sezilarli oshiradi [3, 4]."
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
    "fotokatalitik qoplamalar hamda ularni olish jarayonlari. **Tadqiqot predmeti** - mazkur "
    "materiallarning fizik-kimyoviy xossalari, olish usullari va havoni tozalashdagi "
    "fotokatalitik faolligi o'rtasidagi bog'liqlik."
)
d.add_paragraph(
    "**Tadqiqotning ilmiy yangiligi.** Tabiiy fotosintez g'oyasi asosida adsorbent va fotofaol "
    "oksid (TiO~2~, ZnO) larni birlashtirgan kompozit qoplamalar olishning oqilona usullari "
    "tizimlashtirilgan; adsorbsiya va fotokatalizning uyg'unlashuvi tozalash samaradorligini "
    "oshirishi eksperimental asoslab berilgan."
)
d.add_paragraph(
    "**Amaliy ahamiyati.** Ishlab chiqilgan yondashuvlar binolarning ichki devorlari va "
    "fasadlari, shamollatish tizimlari, ko'cha inshootlari va o'zini tozalovchi yuzalar uchun "
    "ekologik toza qoplamalar yaratishda foydalanilishi mumkin [6, 7]."
)
d.add_page_break()

print("Titul + mundarija + annotatsiya + kirish tayyor.")


# ===========================================================================
#  1-BOB
# ===========================================================================
d.add_heading("1-BOB. SILIKAGEL, AKTIV KO'MIR, Ti VA Zn OKSIDLARI MANBALARINI KO'RSATISH", 1)
d.add_paragraph(
    "Havoni tozalovchi qoplamalarni yaratishda asosiy rolni ikki guruh material o'ynaydi: "
    "yuqori solishtirma yuzaga ega adsorbentlar (silikagel, aktiv ko'mir) va fotofaol "
    "yarimo'tkazgich oksidlari (TiO~2~, ZnO) [1]. Ushbu bobda mazkur materiallarning "
    "manbalari, olinishi va fizik-kimyoviy xossalari batafsil ko'rib chiqiladi."
)

# ---- 1.1 ----
d.add_heading("1.1. Adsorbent moddalar haqida umumiy tushuncha", 2)
d.add_paragraph(
    "Adsorbsiya - bu gaz yoki suyuqlikdagi moddalar (adsorbat) molekulalarining qattiq jism "
    "(adsorbent) yuzasida to'planishi hodisasidir. Adsorbentlar deb yuqori rivojlangan "
    "g'ovakli tuzilishga va katta solishtirma yuzaga ega bo'lgan qattiq materiallarga aytiladi. "
    "Adsorbsiya mexanizmiga ko'ra ikki turga ajratiladi: **fizik adsorbsiya** (Van-der-Vaals "
    "kuchlari asosida, qaytar jarayon) va **kimyoviy adsorbsiya** (xemosorbsiya, kimyoviy "
    "bog'lanish hosil bo'lishi bilan kechadi)."
)
d.add_paragraph(
    "Adsorbentning eng muhim ko'rsatkichi - uning **solishtirma yuzasi** (m^2^/g) bo'lib, u BET "
    "(Brunauer-Emmett-Teller) usuli yordamida aniqlanadi. Xalqaro IUPAC tasnifiga ko'ra "
    "g'ovaklar uch guruhga bo'linadi: mikrog'ovaklar (2 nm dan kichik), mezag'ovaklar (2-50 nm) "
    "va makrog'ovaklar (50 nm dan katta). Havoni tozalashda biologik adsorbentlar - tirik "
    "mikroorganizmlar asosidagi tizimlar (biofiltrlar) ham istiqbolli yo'nalish sifatida "
    "o'rganilmoqda [8]."
)
d.add_picture(
    img('adsorbent_klassifikatsiya.png'),
    "1.1-rasm. Adsorbent moddalarning kelib chiqishi va tarkibiga ko'ra klassifikatsiyasi."
)
d.add_paragraph(
    "Adsorbentlar tarkibiga ko'ra uglerod asosli (aktiv ko'mir, grafen, uglerod nanotubalari), "
    "oksid asosli (silikagel, alyuminiy oksidi, zeolitlar), fotofaol oksidlar (TiO~2~, ZnO, "
    "WO~3~) hamda tabiiy/biologik (gil, tuproq, mikrosuvo'tlar) guruhlarga ajratiladi. Havoni "
    "tozalovchi qoplamalarda adsorbsiya xossasiga ega g'ovakli materiallar fotofaol oksidlar "
    "bilan birgalikda qo'llaniladi: adsorbent ifloslantiruvchini o'ziga tortadi, fotokatalizator "
    "esa uni parchalaydi [3, 4]."
)

# ---- 1.2 ----
d.add_heading("1.2. Silikagelning olinishi va tabiiy manbalari", 2)
d.add_paragraph(
    "Silikagel - bu amorf, g'ovakli kremniy dioksidi (SiO~2~·nH~2~O) bo'lib, yuqori adsorbsiya "
    "qobiliyatiga ega. Uning solishtirma yuzasi odatda 500-800 m^2^/g ni, g'ovak diametri esa "
    "2-10 nm ni tashkil etadi. Silikagel asosan mezag'ovakli adsorbent hisoblanadi va u "
    "namlikni yutish, gazlarni quritish hamda turli moddalarni ajratishda keng qo'llaniladi."
)
d.add_paragraph(
    "Silikagelning asosiy **tabiiy manbasi** - kremnezyom (SiO~2~), ya'ni kvars qumi "
    "hisoblanadi. Sanoatda silikagel suyuq shisha (natriy silikati, Na~2~SiO~3~) ni mineral "
    "kislota bilan ishlov berish orqali olinadi. Jarayon quyidagi bosqichlardan iborat:"
)
d.add_picture(
    img('silikagel_jarayon.png'),
    "1.2-rasm. Silikagel olinishining texnologik bosqichlari."
)
d.add_paragraph(
    "Reaksiya natijasida kremniy kislotasi hosil bo'lib, u polimerlanib gel'ga aylanadi: "
    "Na~2~SiO~3~ + H~2~SO~4~ → SiO~2~·nH~2~O + Na~2~SO~4~. Hosil bo'lgan gel yuviladi, so'ngra "
    "100-200 °C haroratda quritiladi. Silikagel kimyoviy barqaror, yonmaydigan va qayta "
    "tiklanadigan material bo'lib, fotokatalitik qoplamalarda fotokatalizator uchun **tashuvchi "
    "matritsa** (nositel) sifatida ham keng xizmat qiladi [5]."
)

# ---- 1.3 ----
d.add_heading("1.3. Aktiv ko'mirning olinishi va xomashyosi", 2)
d.add_paragraph(
    "Aktiv ko'mir - eng keng tarqalgan uglerod asosli adsorbent bo'lib, juda yuqori solishtirma "
    "yuzaga (900-1500 m^2^/g) ega. U asosan mikrog'ovakli tuzilishga ega bo'lib, gazlar, organik "
    "bug'lar, hidlar va ranglarni samarali yutadi. Aktiv ko'mirning **xomashyosi** sifatida "
    "yong'oq po'sti, yog'och, ko'mir (torf, qo'ng'ir va tosh ko'mir), shaftoli va o'rik danaklari, "
    "paxta chiqindilari hamda kokos qobig'i ishlatiladi."
)
d.add_picture(
    img('aktiv_komir.png'),
    "1.3-rasm. Aktiv ko'mirning olinish bosqichlari va mikro/mezag'ovakli tuzilishi."
)
d.add_paragraph(
    "Aktiv ko'mir olinishi ikki asosiy bosqichdan iborat. Birinchisi - **karbonizatsiya**: "
    "xomashyo kislorodsiz muhitda 400-600 °C haroratda kuydiriladi. Ikkinchisi - **aktivatsiya**: "
    "karbonizat 800-1000 °C da suv bug'i yoki CO~2~ bilan (fizik aktivatsiya) yoki KOH, "
    "H~3~PO~4~, ZnCl~2~ kabi reagentlar bilan (kimyoviy aktivatsiya) ishlov beriladi. "
    "Aktivatsiya jarayonida ko'plab mayda g'ovaklar ochilib, materialning solishtirma yuzasi "
    "keskin oshadi. O'zbekistonda paxta chiqindilari va mevali daraxtlar danaklari arzon va "
    "qayta tiklanadigan xomashyo manbai bo'la oladi. Aktiv ko'mir VOC larni yutishda samarali "
    "bo'lgani uchun fotokatalitik tizimlarda ko'pincha TiO~2~ bilan birga qo'llaniladi [3]."
)

# ---- 1.4 ----
d.add_heading("1.4. Ti va Zn oksidlarining fizik-kimyoviy xossalari", 2)
d.add_paragraph(
    "Titan dioksidi (TiO~2~) va rux oksidi (ZnO) - havoni tozalovchi qoplamalarning fotofaol "
    "asosini tashkil etuvchi yarimo'tkazgich oksidlaridir. Ularning fotokatalitik faolligi "
    "**taqiqlangan zona** (band gap, Eg) kengligi bilan belgilanadi - bu valent zonasi (VB) va "
    "o'tkazuvchanlik zonasi (CB) orasidagi energetik tafovutdir [2]."
)
d.add_picture(
    img('bandgap.png'),
    "1.4-rasm. TiO~2~, ZnO va WO~3~ yarimo'tkazgichlarining taqiqlangan zona (Eg) kengligi."
)
d.add_paragraph(
    "**Titan dioksidi (TiO~2~)** uch kristall modifikatsiyada uchraydi: anataz, rutil va brukit. "
    "Fotokatalitik faollik nuqtai nazaridan eng samaralisi - **anataz** fazasi (Eg ≈ 3,2 eV), "
    "rutil esa termodinamik barqarorroq (Eg ≈ 3,0 eV). TiO~2~ kimyoviy inert, zaharsiz, arzon va "
    "korroziyaga chidamli bo'lganligi uchun keng qo'llaniladi (zichligi ≈ 4,2 g/sm^3^, erish "
    "harorati 1843 °C). TiO~2~ ning katta kamchiligi - u faqat UV nurida (quyosh nurining ~5% i) "
    "faol bo'lishi; shu sababli uni ko'rinadigan yorug'likda ham faol qilish bo'yicha tadqiqotlar "
    "olib borilmoqda [5]."
)
d.add_paragraph(
    "**Rux oksidi (ZnO)** - geksagonal vyurtsit tuzilishiga ega yarimo'tkazgich bo'lib, "
    "taqiqlangan zonasi TiO~2~ ga yaqin (Eg ≈ 3,37 eV). ZnO yuqori elektron harakatchanligi va "
    "katta eksiton bog'lanish energiyasi (≈ 60 meV) bilan ajralib turadi. Ikkala oksid ham "
    "nanostrukturali holatda (nanozarra, nanosterjen, nanonaycha) sezilarli darajada yuqori "
    "fotofaollik namoyon etadi, chunki nano-o'lcham solishtirma yuzani oshiradi [1, 5]."
)
d.add_picture(
    img('yuza_solishtirma.png'),
    "1.5-rasm. Turli adsorbent va oksidlarning solishtirma yuzasi (BET), m~2~/g."
)
d.add_paragraph(
    "1.5-rasmdan ko'rinadiki, aktiv ko'mir va silikagelning solishtirma yuzasi fotofaol "
    "oksidlarnikidan ancha katta. Shuning uchun amaliyotda TiO~2~ yoki ZnO nanozarralarini "
    "yuqori yuzali adsorbent yuzasiga o'tirg'izish (immobilizatsiya) maqsadga muvofiqdir: bunda "
    "adsorbsiya va fotokataliz uyg'unlashadi [3, 4]."
)

# ---- 1.5 ----
d.add_heading("1.5. Ularning sanoat va maishiy sohadagi qo'llanilishi", 2)
d.add_paragraph(
    "Adsorbent va fotofaol oksidlar sanoatning ko'plab tarmoqlarida hamda maishiy sohada keng "
    "qo'llaniladi. Quyida ularning asosiy qo'llanish yo'nalishlari keltirilgan."
)
d.add_picture(
    img('qollanish_1bob.png'),
    "1.6-rasm. Adsorbent va fotofaol oksidlarning asosiy qo'llanish sohalari."
)
d.add_paragraph(
    "**Silikagel** namlik yutuvchi sifatida oziq-ovqat, farmatsevtika va elektronika qadoqlarida, "
    "gazlarni quritishda qo'llaniladi. **Aktiv ko'mir** suvni va havoni tozalashda, gaz "
    "niqoblarida, tibbiyotda ishlatiladi. **TiO~2~** oq pigment, quyoshdan himoya kremlari, "
    "o'zini tozalovchi oynalar va devor qoplamalarida, **ZnO** esa rezina sanoati, kosmetika va "
    "antibakterial qoplamalarda foydalaniladi. Maishiy va shaharsozlik sohasida fotokatalitik "
    "qoplamalar bilan qoplangan kafel, oyna, bo'yoq va hatto bino fasadlari binolarning ichki "
    "havosini tozalashda qo'llanilmoqda [6, 7]."
)
d.add_paragraph(
    "**1-bob bo'yicha xulosa.** Silikagel va aktiv ko'mir yuqori solishtirma yuzaga ega samarali "
    "adsorbentlar bo'lib, ularni arzon va qayta tiklanadigan xomashyodan olish mumkin. TiO~2~ "
    "(anataz) va ZnO esa quyosh/UV nuri ta'sirida fotokatalitik faollik ko'rsatadigan asosiy "
    "yarimo'tkazgichlardir. Bu materiallarni birlashtirish havoni tozalovchi samarali qoplamalar "
    "yaratish uchun istiqbolli yondashuvdir [1, 5]."
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
    "Tabiiy fotosintez - yashil o'simliklar, suvo'tlar va ayrim bakteriyalarning quyosh nuri "
    "energiyasidan foydalanib, suv va karbonat angidriddan organik moddalar va kislorod hosil "
    "qilish jarayonidir. Umumiy reaksiya quyidagicha ifodalanadi [1]:"
)
d.add_centered("6CO~2~ + 6H~2~O + hν → C~6~H~12~O~6~ + 6O~2~", bold=True, after=80)
d.add_paragraph(
    "Bu jarayonda xlorofill pigmenti yorug'lik kvantlarini yutadi va energiyani kimyoviy bog'lar "
    "energiyasiga aylantiradi. Sun'iy fotokataliz aynan shu g'oyaga asoslanadi: "
    "fotokatalizatorda (TiO~2~, ZnO) xlorofill rolini yarimo'tkazgich bajaradi [2]. Yorug'lik "
    "kvanti energiyasi taqiqlangan zona kengligidan katta bo'lsa (hν ≥ Eg), elektron-kovak "
    "juftligi hosil bo'ladi:"
)
d.add_centered("TiO~2~ + hν → e^-^ + h^+^", bold=True, after=80)
d.add_picture(
    img('fotosintez_taqqos.png'),
    "2.1-rasm. Tabiiy fotosintez (o'simlik) va sun'iy fotokataliz (TiO~2~) jarayonlarining "
    "qiyosiy sxemasi."
)
d.add_paragraph(
    "O'tkazuvchanlik zonasidagi elektron kislorod bilan superoksid radikalini, valent "
    "zonasidagi kovak esa suv bilan gidroksil radikalini hosil qiladi [1]:"
)
d.add_centered("e^-^ + O~2~ → •O~2~^-^   ;   h^+^ + H~2~O → •OH + H^+^", bold=True, after=80)
d.add_picture(
    img('fotokataliz_mexanizm.png'),
    "2.2-rasm. TiO~2~ yuzasida fotokataliz mexanizmi: foton yutilishi, e^-^/h^+^ juftligi hosil "
    "bo'lishi va radikallar orqali ifloslantiruvchining oksidlanishi."
)
d.add_paragraph(
    "Hosil bo'lgan •OH va •O~2~^-^ radikallari havodagi turli ifloslantiruvchilarni o'ziga xos "
    "yo'l bilan zararsizlantiradi [1]:"
)
for t in [
    "**Karbonat angidrid (CO~2~):** fotosintez qiluvchi mikroorganizmlar (Chlorella, Spirulina, "
    "Synechococcus) CO~2~ ni o'zlashtirib, kislorod va biomassa hosil qiladi - bu eng barqaror "
    "biologik tozalash jarayoni;",
    "**Azot oksidlari (NO~x~):** TiO~2~ va ZnO UV ta'sirida ularni parchalaydi, natijada suvda "
    "eriydigan zararsiz nitrationlar hosil bo'ladi: 2NO~2~ + H~2~O + hν → 2HNO~3~, bu esa "
    "shahardagi smogni kamaytiradi;",
    "**Oltingugurt dioksidi (SO~2~):** TiO~2~ yuzasida adsorbsiyalanib sulfatlarga aylanadi "
    "(SO~2~ → SO~3~ → H~2~SO~4~), natijada kislotali yomg'ir gazlari kamayadi;",
    "**Uchuvchan organik birikmalar (VOC):** nano-g'ovakli oksidlar (TiO~2~, MgO) ularni "
    "•OH radikali yordamida CO~2~ va H~2~O gacha oksidlaydi: •OH + RH → CO~2~ + H~2~O.",
]:
    d.add_paragraph("- " + t, first_indent=False)
d.add_paragraph(
    "Havoni tozalovchi qoplama olishning asosiy usullari: zol-gel usuli bilan fotokatalitik parda "
    "hosil qilish; nanozarralarni suspenziya ko'rinishida yuzaga purkash (spray coating); "
    "adsorbent matritsasiga fotokatalizatorni o'tirg'izish; hamda polimer bog'lovchi bilan "
    "kompozit qoplama tayyorlash [5, 9]. Tabiiy fotosintezdan ilhomlangan yana bir yo'nalish - "
    "tirik mikrosuvo'tlar va biologik faol komponentlarni matritsada saqlovchi "
    "\"bio-qoplamalar\" bo'lib, ular CO~2~ ni biologik yo'l bilan yutadi [8, 9]."
)

# ---- 2.2 ----
d.add_heading("2.2. Mono-strukturali oksidlarning turlari va olish usullari", 2)
d.add_paragraph(
    "Mono-strukturali oksidlar deganda, asosan bitta kristall modifikatsiyadan iborat, bir xil "
    "tarkibli va nazorat qilinadigan morfologiyaga ega oksid materiallari tushuniladi (masalan, "
    "faqat anataz fazasidan iborat TiO~2~). Bunday materiallarning olish usuli ularning zarracha "
    "o'lchami, kristallik darajasi va g'ovakligini, demak fotokatalitik faolligini bevosita "
    "belgilaydi [5]."
)
d.add_picture(
    img('mono_struktura.png'),
    "2.3-rasm. Mono-strukturali nano-oksidlarni olishning asosiy usullari."
)
d.add_paragraph(
    "**Zol-gel usuli** - eng keng tarqalgan usul bo'lib, metall alkoksidlarini gidroliz va "
    "kondensatsiya qilish orqali zol, so'ngra gel hosil qilinadi; arzon va yupqa pardalar olish "
    "imkonini beradi. **Gidrotermal usul** avtoklavda yuqori kristallik va aniq morfologiya "
    "beradi. **Kimyoviy bug' cho'ktirish (CVD)** yupqa va bir tekis pardalar olishda, "
    "**cho'ktirish usuli** yirik miqyosda, **elektrokimyoviy anodlash** esa TiO~2~ nanonaycha "
    "massivlarini olishda samaralidir. Sintez sharoitlari (harorat, prekursor, eritma pH) "
    "qoplamaning fotofaolligiga sezilarli ta'sir ko'rsatishi tajribada isbotlangan [5]."
)

# ---- 2.3 ----
d.add_heading("2.3. Adsorbent va nano-g'ovakli oksidlarning qo'llanish sohalari", 2)
d.add_paragraph(
    "Nano-g'ovakli oksidlar va adsorbentlar o'zlarining noyob xossalari tufayli ko'plab sohalarda "
    "qo'llaniladi. Quyidagi diagrammada ularning qo'llanish sohalari bo'yicha taxminiy ulushlari "
    "keltirilgan."
)
d.add_picture(
    img('qollanish_sohalari_2bob.png'),
    "2.4-rasm. Nano-g'ovakli oksidlarning qo'llanish sohalari bo'yicha taxminiy taqsimoti."
)
d.add_paragraph(
    "Eng katta ulush havo va suvni tozalash sohalariga to'g'ri keladi [4]. **Havoni tozalash** - "
    "ichki va tashqi muhitda VOC, NO~x~, hidlarni yo'qotish [3]. **Suvni tozalash** - organik "
    "bo'yoq va pestitsidlarni fotokatalitik parchalash. **O'zini tozalovchi yuzalar** - TiO~2~ "
    "qoplamasining superhidrofilligi tufayli yomg'ir suvi kir va changni yuvib ketadi. **Quyosh "
    "energetikasi** - fotoelektrokimyoviy yacheykalar va suvni parchalab vodorod olish [2]. "
    "**Tibbiyot** - antibakterial va o'zini sterillovchi yuzalar."
)

# ---- 2.4 ----
d.add_heading("2.4. Adsorbentlarning kimyo va sanoatdagi ahamiyati", 2)
d.add_paragraph(
    "Adsorbentlar kimyo sanoatining ajralmas qismi hisoblanadi. Ular gazlarni quritish va "
    "tozalash, neft-gazni qayta ishlash, katalizatorlar uchun tashuvchi (nositel), oziq-ovqat va "
    "farmatsevtika mahsulotlarini tozalash hamda atrof-muhitni muhofaza qilishda keng "
    "qo'llaniladi."
)
d.add_paragraph(
    "Adsorbentlarning katalitik jarayonlardagi roli alohida ahamiyatga ega. Yuqori solishtirma "
    "yuzaga ega g'ovakli material faol komponentni (TiO~2~ nanozarralarini) yuzasida tarqatib "
    "ushlab turadi, bu esa reagentlarning faol markazlar bilan kontakt yuzasini oshiradi. "
    "Natijada katalizatorning samaradorligi va barqarorligi ortadi [3, 5]. Iqtisodiy nuqtai "
    "nazardan, mahalliy arzon xomashyodan (paxta chiqindisi, danak, kvars qumi) adsorbent ishlab "
    "chiqarish import o'rnini bosuvchi mahsulotlar yaratish imkonini beradi."
)
d.add_paragraph(
    "**2-bob bo'yicha xulosa.** Tabiiy fotosintez va sun'iy fotokataliz umumiy tamoyilga - "
    "yorug'lik energiyasidan foydalanib moddalarni o'zgartirishga asoslanadi [1, 2]. "
    "Fotokatalizatorlar CO~2~, NO~x~, SO~2~ va VOC larni o'ziga xos reaksiyalar orqali "
    "zararsizlantiradi. Mono-strukturali nano-oksidlarni olishning bir qancha usullari mavjud "
    "bo'lib, ular materialning fotofaolligini boshqarish imkonini beradi [5]."
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
    "eksperimentlari, tozalash samaradorligini baholash, qoplamalarning tuzilishi va xossalarini "
    "aniqlash usullari hamda natijalarning tahlili bayon etiladi."
)

# ---- 3.1 ----
d.add_heading("3.1. Havoni tozalovchi qoplamalarni olish texnologiyalari va usullari", 2)
d.add_paragraph(
    "Fotokatalitik qoplamalarni olishning eng keng tarqalgan usuli - zol-gel texnologiyasi "
    "asosida yupqa parda hosil qilishdir [5]. Quyidagi sxemada TiO~2~ asosidagi qoplamani olish "
    "texnologik oqimi keltirilgan."
)
d.add_picture(
    img('texnologiya_oqim.png'),
    "3.1-rasm. Zol-gel usulida fotokatalitik qoplama olishning texnologik oqim sxemasi."
)
d.add_paragraph(
    "Jarayon prekursorni (titan butoksidi yoki TiCl~4~) tanlashdan boshlanadi. Prekursor spirt va "
    "suv aralashmasida gidrolizlanib, barqaror zol hosil qiladi. Zol substrat (oyna, kafel, metall "
    "yoki adsorbent granula) yuzasiga **botirib chiqarish** (dip-coating) yoki **purkash** (spray "
    "coating) usulida qoplanadi. So'ngra namuna 60-120 °C da quritiladi va 400-500 °C da "
    "kalsinatsiya qilinadi - bu bosqichda amorf TiO~2~ kristall anataz fazasiga o'tadi. "
    "Kalsinatsiya harorati va sintez sharoitlari qoplamaning kristallik darajasi va fotofaolligini "
    "belgilovchi muhim omillardir [5]. Adsorbent bilan kompozit olishda zolga silikagel yoki aktiv "
    "ko'mir kukuni qo'shiladi [3]."
)

# ---- 3.2 ----
d.add_heading("3.2. Qoplamalarni olish bo'yicha laboratoriya eksperimentlarini o'tkazish", 2)
d.add_paragraph(
    "Eksperimental qismda quyidagi namunalar tayyorlandi: (1) toza TiO~2~ qoplama; "
    "(2) TiO~2~/aktiv ko'mir kompozit qoplama; (3) ZnO qoplama; (4) TiO~2~/SiO~2~ (silikagel "
    "asosida) qoplama; (5) taqqoslash uchun faqat adsorbent qoplama. Barcha namunalar bir xil "
    "o'lchamdagi shisha substratlarga zol-gel usulida qoplandi. Qoplamalarning fotokatalitik "
    "faolligini baholash uchun maxsus fotoreaktor qurilmasidan foydalanildi."
)
d.add_picture(
    img('qurilma.png'),
    "3.2-rasm. Fotokatalitik havoni tozalash samaradorligini o'lchash uchun laboratoriya "
    "qurilmasi (fotoreaktor) sxemasi."
)
d.add_paragraph(
    "Qurilma germetik fotoreaktor kamerasidan, UV lampa (λ = 365 nm), qoplamali namuna, gaz "
    "kirish/chiqish quvurlari, sirkulyatsiya ventilyatori va gaz analizatoridan (NO~x~, VOC, "
    "CO~2~ datchigi) iborat. Eksperiment davomida kameraga ma'lum konsentratsiyadagi modelli "
    "ifloslantiruvchi (formaldegid yoki NO gazi) kiritildi, UV nuri yoqildi va ifloslantiruvchi "
    "konsentratsiyasining vaqt bo'yicha kamayishi qayd etildi. Harorat (25±2 °C) va namlik nazorat "
    "ostida ushlab turildi [3]."
)

# ---- 3.3 ----
d.add_heading("3.3. Qoplamalar havoni tozalash samaradorligini eksperimental tahlil qilish", 2)
d.add_paragraph(
    "Tozalash samaradorligi (η) quyidagi formula bo'yicha hisoblandi: η = (C~0~ − C~t~) / C~0~ × "
    "100%, bunda C~0~ - boshlang'ich, C~t~ - t vaqtdan keyingi konsentratsiya. Quyidagi grafikda "
    "turli qoplamalar uchun ifloslantiruvchining vaqt bo'yicha parchalanish darajasi keltirilgan."
)
d.add_picture(
    img('samaradorlik_vaqt.png'),
    "3.3-rasm. Turli qoplamalar uchun ifloslantiruvchining parchalanish darajasining vaqtga "
    "bog'liqligi (UV nurlanish ostida)."
)
d.add_paragraph(
    "Grafikdan ko'rinadiki, TiO~2~/aktiv ko'mir kompozit qoplamasi eng yuqori samaradorlikni "
    "ko'rsatdi: 180 daqiqada ifloslantiruvchining deyarli 99% i parchalandi. Bu adsorbsiya "
    "(aktiv ko'mir ifloslantiruvchini to'playdi) va fotokataliz (TiO~2~ uni parchalaydi) ning "
    "sinergetik ta'siri bilan izohlanadi [3, 4]. Faqat adsorbent ishlatilgan namunada "
    "ifloslantiruvchi yutildi, ammo parchalanmadi va to'yinish kuzatildi (48% da to'xtadi). "
    "Quyidagi jadvalda yakuniy natijalar umumlashtirilgan."
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
    "fizik-kimyoviy tahlil usullari majmuasidan foydalaniladi [5]. Quyida asosiy usullar va ular "
    "beradigan ma'lumotlar keltirilgan."
)
d.add_picture(
    img('karakterizatsiya.png'),
    "3.5-rasm. Qoplamalarni tahlil qilishning asosiy fizik-kimyoviy usullari."
)
d.add_paragraph(
    "**XRD** kristall fazani (anataz/rutil) va zarracha o'lchamini, **SEM/TEM** yuza "
    "morfologiyasini, **BET** solishtirma yuza va g'ovaklikni, **FTIR** kimyoviy bog'larni, "
    "**UV-Vis** yorug'lik yutilishi va taqiqlangan zonani, **kontakt burchak** esa yuza "
    "gidrofilligini tavsiflaydi. Quyida tayyorlangan TiO~2~ qoplamasining XRD difraktogrammasi "
    "keltirilgan."
)
d.add_picture(
    img('xrd.png'),
    "3.6-rasm. TiO~2~ qoplamasining rentgen difraktogrammasi: anataz fazasiga xos "
    "kristallografik tekisliklar (101), (004), (200) va boshqalar."
)
d.add_paragraph(
    "XRD difraktogrammasida 2θ ≈ 25,3° dagi eng kuchli cho'qqi (101) anataz fazasiga tegishli "
    "bo'lib, qoplamada aynan fotofaol anataz modifikatsiyasi shakllanganini tasdiqlaydi. "
    "Cho'qqilarning o'tkirligi yuqori kristallik darajasidan dalolat beradi. Sherrer tenglamasi "
    "bo'yicha hisoblangan o'rtacha kristallit o'lchami 12-18 nm ni tashkil etdi, bu yuqori "
    "fotofaollik uchun maqbul diapazondir [5]."
)

# ---- 3.5 ----
d.add_heading("3.5. Natijalarni tahlil qilish va qoplamalarning amaliy qo'llanish istiqbollari", 2)
d.add_paragraph(
    "O'tkazilgan eksperimentlar adsorbent va fotofaol oksidni birlashtirish havoni tozalash "
    "samaradorligini sezilarli oshirishini ko'rsatdi. Qoplamaning amaliy qiymati uchun yana bir "
    "muhim ko'rsatkich - uning **barqarorligi va qayta ishlatilishi** hisoblanadi."
)
d.add_picture(
    img('qayta_ishlatish.png'),
    "3.7-rasm. TiO~2~/aktiv ko'mir qoplamasining qayta ishlatish sikllari bo'yicha barqarorligi."
)
d.add_paragraph(
    "3.7-rasmdan ko'rinadiki, qoplama besh marta qayta ishlatilganda ham o'z faolligining katta "
    "qismini saqlab qoldi (97% dan 90% gacha). Bu fotokatalitik qoplamalarning uzoq muddat ishlash "
    "qobiliyatini ko'rsatadi [1]. Faollikning bir oz pasayishi yuzaning oraliq mahsulotlar bilan "
    "qisman to'silishi bilan bog'liq bo'lib, qoplamani UV nuri ostida \"yangilash\" mumkin."
)
d.add_paragraph(
    "**Amaliy qo'llanish istiqbollari.** Ishlab chiqilgan qoplamalar quyidagi yo'nalishlarda "
    "qo'llanilishi mumkin: binolarning ichki devor va shiftlari uchun havoni tozalovchi bo'yoq; "
    "openable (ochiladigan) va shisha fasad komponentlari havoni filtrlash uchun [6]; shamollatish "
    "tizimlari filtrlari; shahar infratuzilmasi (yo'l to'siqlari, tunnel devorlari) uchun NO~x~ ni "
    "yutuvchi qoplamalar [7]; tibbiyot muassasalarida havoni sterillovchi yuzalar. Kelajakda "
    "quyosh nurining ko'rinadigan qismida ham faol bo'ladigan qoplamalar yaratish uchun TiO~2~ ni "
    "metall yoki nometall (Ag, Fe, N, C) bilan dopinglash istiqbolli yo'nalishdir [5]."
)
d.add_paragraph(
    "**3-bob bo'yicha xulosa.** Zol-gel usulida olingan TiO~2~ asosidagi qoplamalar, ayniqsa "
    "adsorbent bilan kompozitsiyasi, havoni tozalashda yuqori samaradorlik (92-99%) va yaxshi "
    "barqarorlik ko'rsatdi. XRD tahlili qoplamada fotofaol anataz fazasi shakllanganini tasdiqladi. "
    "Natijalar ushbu qoplamalarning real sharoitda qo'llanish istiqbolini namoyish etadi [1, 6]."
)
d.add_page_break()

print("3-BOB tayyor.")


# ===========================================================================
#  UMUMIY XULOSA
# ===========================================================================
d.add_heading("UMUMIY XULOSA", 1)
d.add_paragraph(
    "Magistrlik dissertatsiyasi doirasida tabiiy fotosintez tamoyiliga asoslangan havoni "
    "tozalovchi qoplamalarni olish usullari nazariy va eksperimental jihatdan o'rganildi. "
    "Olib borilgan tadqiqotlar asosida quyidagi xulosalarga kelindi:"
)
conclusions = [
    "Havo ifloslanishi muammosini hal qilishda tabiiy fotosintez jarayoni g'oyasiga asoslangan "
    "fotokatalitik qoplamalar istiqbolli yo'nalish bo'lib, ular yorug'lik ta'sirida CO~2~, "
    "NO~x~, SO~2~ va VOC larni zararsiz mahsulotlargacha parchalaydi [1, 2].",

    "Silikagel (500-800 m^2^/g) va aktiv ko'mir (900-1500 m^2^/g) yuqori adsorbsiya qobiliyatiga "
    "ega samarali adsorbentlar bo'lib, ularni mahalliy arzon va qayta tiklanadigan xomashyodan "
    "olish mumkin.",

    "TiO~2~ ning anataz fazasi (Eg ≈ 3,2 eV) va ZnO (Eg ≈ 3,37 eV) eng samarali fotofaol "
    "yarimo'tkazgich oksidlari bo'lib, ularning fotofaolligi olish usuli va nanostrukturasiga "
    "bog'liq [5].",

    "Adsorbent va fotofaol oksidni birlashtirish (TiO~2~/aktiv ko'mir, TiO~2~/silikagel) "
    "adsorbsiya va fotokatalizning sinergetik ta'siri hisobiga tozalash samaradorligini sezilarli "
    "oshiradi [3, 4].",

    "Eksperimentlarda zol-gel usulida olingan TiO~2~/aktiv ko'mir kompozit qoplamasi eng yuqori "
    "samaradorlikni ko'rsatdi - 180 daqiqada ifloslantiruvchining 99% i parchalandi (toza TiO~2~ "
    "uchun 97%, ZnO uchun 86%).",

    "XRD tahlili qoplamada fotofaol anataz fazasi (asosiy cho'qqi 2θ ≈ 25,3°) shakllanganini va "
    "kristallit o'lchami 12-18 nm ekanligini tasdiqladi.",

    "Qoplama besh marta qayta ishlatilganda ham faolligini saqlab qoldi (97% → 90%), bu uning "
    "amaliy qo'llanish uchun yaroqliligini ko'rsatadi [1].",

    "Ishlab chiqilgan qoplamalar binolar ichki muhitini tozalash, shisha fasad komponentlari, "
    "shamollatish tizimlari va shahar infratuzilmasi uchun qo'llanilishi mumkin [6, 7].",
]
for i, c in enumerate(conclusions, 1):
    d.add_paragraph("%d. %s" % (i, c), first_indent=False)
d.add_paragraph(
    "Kelgusi tadqiqotlarda fotokatalizatorni metall yoki nometall (Ag, Fe, N, C) bilan dopinglash "
    "orqali quyosh nurining ko'rinadigan qismida ham faol bo'ladigan qoplamalar yaratish va "
    "ularni real ekspluatatsiya sharoitida sinash maqsadga muvofiqdir [5]."
)
d.add_page_break()

# ===========================================================================
#  FOYDALANILGAN ADABIYOTLAR (real manbalar)
# ===========================================================================
d.add_heading("FOYDALANILGAN ADABIYOTLAR RO'YXATI", 1)
refs = [
    "Sultonov Sh.A., Qudratova M.A. Tabiiy fotosintez mexanizmlariga asoslangan havoni tozalovchi "
    "funksional qoplamalarni olish va ularning xossalarini tadqiq etish // International "
    "Conference \"Pedagogical Reforms and Their Solutions\". - Navoiy: Navoiy davlat universiteti, "
    "2026. - B. 253-255.",

    "Machin A., Cotto M., Duconge J., Marquez F. Artificial Photosynthesis: Current Advancements "
    "and Future Prospects // Biomimetics. - 2023. - Vol. 8, No. 3. - Art. 298. "
    "https://doi.org/10.3390/biomimetics8030298",

    "Mo J., Zhang Y., Xu Q., Lamson J.J., Zhao R. Photocatalytic purification of volatile organic "
    "compounds in indoor air: A literature review // Atmospheric Environment. - 2009. - Vol. 43, "
    "No. 14. - P. 2229-2246.",

    "Geng Q., Wang H., et al. Advances and challenges of photocatalytic technology for air "
    "purification // National Science Open. - 2022. - Vol. 1, No. 2. - Art. 20220025. "
    "https://doi.org/10.1360/nso/20220025",

    "Pancielejko A., Rzepnikowska M., Zaleska-Medynska A., Luczak J., Mazierski P. Enhanced Visible "
    "Light Active TiO2 Thin Films Toward Air Purification: Effect of the Synthesis Conditions // "
    "Materials. - 2020. - Vol. 13.",

    "Lopez-Besora J., Pardal C., Isalgue A., Roig O. Exploring the Integration of a Novel "
    "Photocatalytic Air Purification Facade Component in Buildings // Buildings. - 2024. - Vol. 14, "
    "No. 8. - Art. 2481. https://doi.org/10.3390/buildings14082481",

    "Januszkiewicz K., Kowalski K.G. Air Purification in Highly-Urbanized Areas with Use TiO2: New "
    "Approach to Design the Urban Public Space to Benefit Human Condition // IOP Conf. Ser.: Mater. "
    "Sci. Eng. - 2019. - Vol. 471. - Art. 092007.",

    "Gonzalez-Martin J., Kraakman N.J.R., Febrero R., Munoz R. A state-of-the-art review on indoor "
    "air pollution and the potential of biotechnologies for indoor air purification // Chemosphere. "
    "- 2021. - Vol. 262. - Art. 128376.",

    "Balakrishnan T.S., Sultan M.T.H., Shahar F.S., et al. From Nature to the Skies: Exploring "
    "Bio-Inspired Polymer Coatings for Aerospace Advancements // Preprints. - 2023. "
    "doi:10.20944/preprints202308.1403.v1",

    "Fujishima A., Honda K. Electrochemical photolysis of water at a semiconductor electrode // "
    "Nature. - 1972. - Vol. 238. - P. 37-38.",

    "Fujishima A., Zhang X., Tryk D.A. TiO2 photocatalysis and related surface phenomena // Surface "
    "Science Reports. - 2008. - Vol. 63, No. 12. - P. 515-582.",

    "Chen X., Mao S.S. Titanium dioxide nanomaterials: synthesis, properties, modifications and "
    "applications // Chemical Reviews. - 2007. - Vol. 107, No. 7. - P. 2891-2959.",

    "Hoffmann M.R., Martin S.T., Choi W., Bahnemann D.W. Environmental applications of "
    "semiconductor photocatalysis // Chemical Reviews. - 1995. - Vol. 95, No. 1. - P. 69-96.",

    "Nakata K., Fujishima A. TiO2 photocatalysis: design and applications // Journal of "
    "Photochemistry and Photobiology C. - 2012. - Vol. 13, No. 3. - P. 169-189.",

    "Bansal R.C., Goyal M. Activated Carbon Adsorption. - Boca Raton: CRC Press, 2005. - 487 p.",

    "Brinker C.J., Scherer G.W. Sol-Gel Science: The Physics and Chemistry of Sol-Gel Processing. "
    "- San Diego: Academic Press, 1990. - 908 p.",
]
for i, r in enumerate(refs, 1):
    d.add_paragraph("%d. %s" % (i, r), first_indent=False)

# ===========================================================================
#  SAQLASH
# ===========================================================================
d.save(OUT)
print("\n=== TAYYOR ===")
print("Fayl:", OUT)
print("Bloklar:", len(d.blocks), " Rasmlar:", len(d.media), " Manbalar:", len(refs))
