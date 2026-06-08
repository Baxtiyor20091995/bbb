# -*- coding: utf-8 -*-
"""BOB II - Design and development of the automated monitoring system."""

BOB2 = [
    ("h1", "II BOB. AVTOMATLASHTIRILGAN AKADEMIK MONITORING TIZIMINI "
           "LOYIHALASH VA ISHLAB CHIQISH"),

    # =================== 2.1 ===================
    ("h2", "2.1. Avtomatlashtirilgan akademik monitoring tizimiga qo'yiladigan "
           "talablar"),
    ("body", "Har qanday axborot tizimini ishlab chiqish uning oldiga "
             "qo'yiladigan talablarni aniq belgilashdan boshlanadi. Talablar "
             "tizimning nima qilishi (funksional talablar) va u qanday "
             "sifatlarga ega bo'lishi (nofunksional talablar) kerakligini "
             "tavsiflaydi. Birinchi bobda aniqlangan muammolar va akademik "
             "monitoringning tamoyillari ushbu talablarni shakllantirishda "
             "asos bo'ldi. Talablarni to'g'ri belgilash loyihaning "
             "muvaffaqiyatini ta'minlovchi eng muhim bosqichlardan biri "
             "hisoblanadi, chunki keyingi barcha bosqichlar - arxitekturani "
             "loyihalash, dasturlash va sinovdan o'tkazish - aynan shu "
             "talablarga tayanadi."),
    ("h3", "Tizim foydalanuvchilari va ularning rollari."),
    ("body", "Talablarni aniqlashdan oldin tizimning foydalanuvchilari "
             "(aktorlari) va ularning vazifalarini belgilash zarur. "
             "Foydalanuvchilar rollari tizimda kirish huquqlarini va "
             "funksiyalardan foydalanish doirasini belgilaydi."),
    ("table", [
        ["Rol", "Asosiy vazifalari"],
        ["Administrator",
         "Tizimni sozlash, foydalanuvchilarni va kirish huquqlarini "
         "boshqarish, ma'lumotnomalarni yuritish."],
        ["Rahbariyat (rektorat)",
         "Umumlashtirilgan ko'rsatkichlarni kuzatish, strategik "
         "hisobotlarni olish, muassasa kesimida tahlil."],
        ["Dekanat/kafedra",
         "Fakultet va guruhlar bo'yicha o'zlashtirishni kuzatish, "
         "muammoli holatlarni aniqlash."],
        ["Professor-o'qituvchi",
         "O'z fanlari bo'yicha talabalar natijalarini ko'rish, baho "
         "kiritish, tahlil olish."],
        ["Tyutor/kurator",
         "Biriktirilgan guruh talabalarining akademik xavfini kuzatish."],
        ["Talaba",
         "Shaxsiy o'zlashtirish ko'rsatkichlari, reyting va qarzdorliklarni "
         "ko'rish."],
    ]),
    ("caption", "2.1-jadval. Tizim foydalanuvchilari va ularning rollari"),
    ("h3", "Funksional talablar."),
    ("body", "Funksional talablar tizim bajarishi lozim bo'lgan aniq "
             "harakatlar va xizmatlarni belgilaydi. Ishlab chiqilayotgan "
             "tizim uchun quyidagi funksional talablar shakllantirildi:"),
    ("num", "ma'lumotlarni turli manbalardan (kontingent, reyting, davomat, "
            "masofaviy ta'lim platformasi) avtomatik yig'ish va "
            "integratsiyalash;"),
    ("num", "talabalar, guruhlar, fanlar va yo'nalishlar bo'yicha akademik "
            "ko'rsatkichlarni hisoblash va saqlash;"),
    ("num", "o'zlashtirish dinamikasini va tendensiyalarini real vaqt "
            "rejimida kuzatish;"),
    ("num", "akademik xavf ostidagi talabalarni belgilangan mezonlar asosida "
            "avtomatik aniqlash va ogohlantirish (erta ogohlantirish "
            "tizimi);"),
    ("num", "interaktiv boshqaruv panellari (dashboard) orqali "
            "ko'rsatkichlarni vizuallashtirish;"),
    ("num", "turli kesimlarda (talaba, guruh, fakultet, davr) hisobotlar "
            "shakllantirish va ularni eksport qilish;"),
    ("num", "foydalanuvchilar va ularning kirish huquqlarini rollar asosida "
            "boshqarish;"),
    ("num", "tizimdagi harakatlarni qayd etish (audit jurnali)."),
    ("h3", "Nofunksional talablar."),
    ("body", "Nofunksional talablar tizimning sifat xususiyatlarini "
             "belgilaydi. Ular tizimning ishonchli, xavfsiz va qulay "
             "bo'lishini ta'minlaydi."),
    ("table", [
        ["Talab", "Tavsifi"],
        ["Unumdorlik",
         "Asosiy so'rovlarga javob berish vaqti 2-3 soniyadan oshmasligi, "
         "bir vaqtda ko'p foydalanuvchini qo'llab-quvvatlash."],
        ["Kengaytiriluvchanlik",
         "Foydalanuvchilar va ma'lumotlar hajmi oshganda tizim barqaror "
         "ishlashi, yangi modullar qo'shish imkoni."],
        ["Xavfsizlik",
         "Autentifikatsiya, rollar asosida avtorizatsiya, ma'lumotlarni "
         "shifrlash va shaxsiy ma'lumotlar himoyasi."],
        ["Ishonchlilik",
         "Tizimning uzluksiz ishlashi, ma'lumotlarning zaxira nusxasini "
         "yaratish va tiklash mexanizmi."],
        ["Qulaylik (UX)",
         "Sodda va intuitiv interfeys, turli qurilmalarga moslashuvchanlik "
         "(responsive)."],
        ["Integratsiyalanuvchanlik",
         "Tashqi tizimlar bilan API orqali ma'lumot almashish imkoni."],
    ]),
    ("caption", "2.2-jadval. Tizimga qo'yiladigan nofunksional talablar"),
    ("body", "Shakllantirilgan funksional va nofunksional talablar tizimni "
             "loyihalash uchun yagona asos bo'lib xizmat qiladi. Keyingi "
             "bo'limda ushbu talablarni qondiradigan tizim arxitekturasi va "
             "ma'lumotlar bazasi modeli ishlab chiqiladi."),
    ("h3", "Loyiha cheklovlari va dastlabki shartlar."),
    ("body", "Talablar bilan bir qatorda, loyihaning cheklovlari va dastlabki "
             "shartlarini ham aniqlash zarur. Cheklovlar - bu tizimni ishlab "
             "chiqishda hisobga olinishi shart bo'lgan chegaralar. Ular "
             "texnik (mavjud infratuzilma, integratsiya qilinadigan "
             "tizimlarning imkoniyatlari), tashkiliy (ajratilgan resurslar, "
             "muddatlar) va huquqiy (shaxsiy ma'lumotlarni himoya qilish "
             "talablari) bo'lishi mumkin. Masalan, tizim mavjud talabalar "
             "kontingenti tizimi bilan integratsiyalashishi shart, demak u "
             "ushbu tizim taqdim etadigan ma'lumot formatlariga moslashishi "
             "kerak."),
    ("body", "Dastlabki shartlar - bu loyiha boshlanishida to'g'ri deb qabul "
             "qilinadigan taxminlar. Masalan, manba tizimlar zarur "
             "ma'lumotlarni taqdim eta oladi, foydalanuvchilar minimal "
             "kompyuter savodxonligiga ega va muassasada zarur tarmoq "
             "infratuzilmasi mavjud. Ushbu shartlarni aniq qayd etish "
             "loyihaning keyingi bosqichlarida yuzaga kelishi mumkin bo'lgan "
             "noaniqliklarni kamaytiradi."),
    ("h3", "Talablarni muhimlik bo'yicha tartiblash."),
    ("body", "Barcha talablarni bir vaqtning o'zida amalga oshirish ko'pincha "
             "imkonsiz bo'lgani uchun, ularni muhimlik darajasiga ko'ra "
             "tartiblash zarur. Buning uchun MoSCoW usulidan foydalanish "
             "mumkin, unga ko'ra talablar to'rt toifaga bo'linadi: majburiy "
             "(Must have), zarur (Should have), maqsadga muvofiq (Could have) "
             "va kelajak uchun (Won't have this time). Bu yondashuv "
             "loyihaning birinchi bosqichida eng muhim funksiyalarga "
             "e'tibor qaratish va tizimni bosqichma-bosqich rivojlantirish "
             "imkonini beradi."),
    ("table", [
        ["Muhimlik", "Talab misoli"],
        ["Majburiy", "Ma'lumotlarni yig'ish, ko'rsatkichlarni hisoblash, "
                     "asosiy panel."],
        ["Zarur", "Xavfni baholash va ogohlantirish, hisobotlar."],
        ["Maqsadga muvofiq", "Mobil moslashuv, qo'shimcha eksport "
                             "formatlari."],
        ["Kelajak uchun", "Sun'iy intellektga asoslangan bashorat, tavsiya "
                          "tizimi."],
    ]),
    ("caption", "2.7-jadval. Talablarni MoSCoW usuli bo'yicha tartiblash"),
    ("h3", "Asosiy foydalanish stsenariylari (use case)."),
    ("body", "Funksional talablarni yanada aniqlashtirish uchun tizimning "
             "asosiy foydalanish stsenariylarini ko'rib chiqamiz. "
             "Foydalanish stsenariysi - bu foydalanuvchi va tizim "
             "o'rtasidagi muayyan maqsadga erishishga qaratilgan o'zaro "
             "aloqalar ketma-ketligi. Quyida bir necha asosiy stsenariy "
             "tavsiflangan."),
    ("body", "\"Talaba o'zlashtirishini kuzatish\" stsenariysi. | "
             "professor-o'qituvchi yoki tyutor tizimga kiradi, kerakli "
             "guruh yoki talabani tanlaydi va uning o'zlashtirish "
             "ko'rsatkichlari, reyting dinamikasi hamda davomatini ko'radi. "
             "Tizim ma'lumotlarni grafik va jadval ko'rinishida taqdim etadi, "
             "salbiy tendensiyalarni ajratib ko'rsatadi."),
    ("body", "\"Xavf ostidagi talabalarni aniqlash\" stsenariysi. | dekanat "
             "xodimi xavf monitoringi panelini ochadi, tizim yuqori xavf "
             "zonasidagi talabalar ro'yxatini avtomatik shakllantiradi va "
             "har biri uchun xavf sabablarini ko'rsatadi. Xodim shu asosda "
             "profilaktik chora-tadbirlar rejasini tuzadi."),
    ("body", "\"Hisobot shakllantirish\" stsenariysi. | rahbariyat "
             "vakili kerakli davr va kesimni tanlaydi, tizim "
             "umumlashtirilgan hisobotni avtomatik tayyorlaydi va uni "
             "kerakli formatda eksport qilish imkonini beradi. Bu stsenariy "
             "an'anaviy qo'lda hisobot tayyorlashga ketadigan ko'p kunlik "
             "mehnatni bir necha daqiqaga qisqartiradi."),
    ("body", "Ushbu stsenariylar tizimning foydalanuvchilarga qanday qiymat "
             "yaratishini aniq ko'rsatadi va loyihalash jarayonida "
             "interfeyslar hamda funksiyalarni shakllantirish uchun asos "
             "bo'ladi. Har bir stsenariy uchun asosiy va muqobil oqimlar, "
             "shuningdek istisno holatlari ham aniqlanadi, bu tizimning "
             "barcha vaziyatlarda to'g'ri ishlashini ta'minlaydi."),

    # =================== 2.2 ===================
    ("h2", "2.2. Tizim arxitekturasi va ma'lumotlar bazasini loyihalash"),
    ("body", "Tizim arxitekturasi - bu uning asosiy komponentlari, ularning "
             "vazifalari va o'zaro aloqalarini belgilovchi yuqori darajadagi "
             "tuzilma. To'g'ri tanlangan arxitektura tizimning "
             "kengaytiriluvchanligi, ishonchliligi va qo'llab-quvvatlash "
             "qulayligini ta'minlaydi. Ishlab chiqilayotgan tizim uchun "
             "ko'p qatlamli (multi-tier) arxitektura tanlandi, u esa "
             "modulli (servisga yo'naltirilgan) yondashuv bilan "
             "to'ldirildi."),
    ("h3", "Arxitektura qatlamlari."),
    ("body", "Tizim arxitekturasi to'rtta asosiy qatlamdan iborat:"),
    ("body", "1. Taqdimot qatlami (Presentation Layer). | foydalanuvchi bilan "
             "o'zaro aloqani ta'minlovchi veb-interfeys. Bu qatlam boshqaruv "
             "panellari, jadvallar, grafiklar va formalarni ko'rsatadi. U "
             "brauzerda ishlaydi va server bilan API orqali ma'lumot "
             "almashadi."),
    ("body", "2. Amaliy mantiq qatlami (Application/Business Logic Layer). | "
             "tizimning markaziy qatlami bo'lib, u barcha hisob-kitoblar, "
             "ko'rsatkichlarni shakllantirish, xavfni baholash algoritmlari "
             "va biznes qoidalarini amalga oshiradi. Bu qatlam mustaqil "
             "servislar (modullar) ko'rinishida tashkil etiladi."),
    ("body", "3. Ma'lumotlarga kirish qatlami (Data Access Layer). | "
             "ma'lumotlar bazasi bilan o'zaro aloqani ta'minlaydi, "
             "so'rovlarni bajaradi va amaliy mantiq qatlamini ma'lumotlar "
             "saqlash tafsilotlaridan ajratadi."),
    ("body", "4. Ma'lumotlar qatlami (Data Layer). | ma'lumotlar bazasi va "
             "tashqi manbalar bilan integratsiya komponentlarini o'z ichiga "
             "oladi. Bu yerda ma'lumotlar saqlanadi va tashqi tizimlardan "
             "yig'iladi."),
    ("caption", "2.1-rasm. Avtomatlashtirilgan akademik monitoring tizimining "
                "ko'p qatlamli arxitekturasi (shartli sxema)"),
    ("body", "Ushbu qatlamli yondashuvning asosiy afzalligi - mas'uliyatlarni "
             "ajratish (separation of concerns) tamoyiliga rioya etilishidir. "
             "Har bir qatlam o'z vazifasini mustaqil bajaradi, bu esa "
             "tizimni ishlab chiqish, sinovdan o'tkazish va "
             "qo'llab-quvvatlashni osonlashtiradi. Masalan, interfeysni "
             "o'zgartirish amaliy mantiqqa ta'sir qilmaydi, ma'lumotlar "
             "bazasini almashtirish esa faqat ma'lumotlarga kirish qatlamini "
             "o'zgartirishni talab qiladi."),
    ("body", "Tizimning markaziy elementi sifatida integratsiya shinasi "
             "(integration bus) loyihalanadi. U turli manba tizimlardan "
             "ma'lumotlarni yig'ib, ularni yagona formatga keltiradi va "
             "markaziy ma'lumotlar omboriga joylaydi. Bu \"axborot orollari\" "
             "muammosini hal qiladi va birinchi bobda aniqlangan "
             "ma'lumotlarning tarqoqligi muammosini bartaraf etadi."),
    ("h3", "Ma'lumotlar bazasini loyihalash."),
    ("body", "Ma'lumotlar bazasi (MB) - tizimning poydevori bo'lib, u barcha "
             "akademik ma'lumotlarni tartibli saqlaydi. MB ni loyihalash "
             "konseptual, mantiqiy va fizik bosqichlardan iborat. Konseptual "
             "bosqichda mavzu sohasining asosiy mohiyatlari (entitylari) va "
             "ular o'rtasidagi bog'lanishlar aniqlanadi. Quyida tizimning "
             "asosiy mohiyatlari keltirilgan."),
    ("table", [
        ["Mohiyat (jadval)", "Asosiy maydonlar"],
        ["Talaba", "ID, F.I.Sh., guruh_ID, yo'nalish, o'qish_holati."],
        ["Guruh", "ID, nomi, kurs, yo'nalish_ID, ta'lim_shakli."],
        ["Fan", "ID, nomi, kredit, semestr, kafedra_ID."],
        ["O'qituvchi", "ID, F.I.Sh., kafedra_ID, lavozimi."],
        ["Baholash", "ID, talaba_ID, fan_ID, nazorat_turi, ball, sana."],
        ["Davomat", "ID, talaba_ID, fan_ID, sana, holat."],
        ["Ko'rsatkich", "ID, obyekt_turi, obyekt_ID, ko'rsatkich, qiymat, "
                        "davr."],
    ]),
    ("caption", "2.3-jadval. Ma'lumotlar bazasining asosiy mohiyatlari"),
    ("body", "Mohiyatlar o'rtasidagi bog'lanishlar quyidagicha belgilanadi: "
             "bir guruhga ko'p talaba tegishli (bir-ko'p munosabati); bir "
             "talaba ko'p fan bo'yicha bahoga ega (ko'p-ko'p munosabati, u "
             "baholash jadvali orqali amalga oshiriladi); bir o'qituvchi ko'p "
             "fanni o'qitishi mumkin. Ushbu bog'lanishlar \"mohiyat-bog'lanish\" "
             "(ER) diagrammasi orqali ko'rgazmali ifodalanadi."),
    ("caption", "2.2-rasm. Ma'lumotlar bazasining \"mohiyat-bog'lanish\" "
                "(ER) diagrammasi (shartli sxema)"),
    ("body", "Mantiqiy loyihalash bosqichida mohiyatlar relatsion modelning "
             "jadvallariga aylantiriladi, har bir jadval uchun birlamchi "
             "(primary key) va tashqi (foreign key) kalitlar belgilanadi, "
             "ma'lumotlar yaxlitligini ta'minlash uchun normalizatsiya "
             "amalga oshiriladi. Normalizatsiya ma'lumotlarning takrorlanishi "
             "(redundantligi) va anomaliyalarini bartaraf etadi. "
             "Ko'rsatkichlar kabi tez-tez murojaat qilinadigan ma'lumotlar "
             "uchun esa ayrim hollarda denormalizatsiya va indekslashdan "
             "foydalanib, so'rovlar unumdorligi oshiriladi."),
    ("body", "Katta hajmdagi tahliliy so'rovlarni samarali bajarish uchun "
             "tizimda operativ ma'lumotlar bazasi (OLTP) va tahliliy "
             "ma'lumotlar ombori (OLAP/Data Warehouse) ajratiladi. Operativ "
             "baza kundalik tranzaksiyalarni, ombor esa tarixiy ma'lumotlar "
             "va tahliliy hisob-kitoblarni saqlaydi. Bu yondashuv tizimning "
             "unumdorligi bo'yicha nofunksional talabni qondiradi."),
    ("h3", "Tizimning asosiy komponentlari."),
    ("body", "Yuqorida tavsiflangan qatlamlar doirasida tizimning aniq "
             "komponentlari ajratiladi. Har bir komponent muayyan vazifani "
             "bajaradi va boshqa komponentlar bilan belgilangan interfeyslar "
             "orqali aloqa qiladi. Quyidagi jadvalda tizimning asosiy "
             "komponentlari va ularning vazifalari keltirilgan."),
    ("table", [
        ["Komponent", "Vazifasi"],
        ["Veb-mijoz", "Foydalanuvchi interfeysi, ma'lumotlarni "
                      "vizuallashtirish."],
        ["API-shlyuz", "Mijoz so'rovlarini qabul qilish va tegishli "
                       "servisga yo'naltirish."],
        ["Amaliy servislar", "Biznes mantiq, ko'rsatkichlar va xavfni "
                             "hisoblash."],
        ["Integratsiya servisi", "Manba tizimlardan ma'lumot yig'ish (ETL)."],
        ["Ma'lumotlar bazasi", "Tuzilmali ma'lumotlarni saqlash."],
        ["Kesh ombori", "Tez-tez foydalaniladigan ma'lumotlarni saqlash."],
        ["Ogohlantirish servisi", "Xabarnomalar yuborish (e-pochta, tizim "
                                  "ichida)."],
    ]),
    ("caption", "2.4-jadval. Tizimning asosiy komponentlari"),
    ("body", "Komponentlarni bunday ajratish tizimni tushunishni, "
             "rivojlantirishni va sinovdan o'tkazishni osonlashtiradi. Har "
             "bir komponent mustaqil ravishda masshtablanishi mumkin: "
             "masalan, foydalanuvchilar soni oshganda faqat amaliy servislar "
             "nusxalari ko'paytiriladi, ma'lumotlar bazasi esa o'zgarishsiz "
             "qoladi. Bu moslashuvchanlik bulutli muhitda ayniqsa qimmatli."),
    ("h3", "Arxitektura uslubini tanlash: monolit va mikroservis."),
    ("body", "Tizim arxitekturasini loyihalashda muhim qarorlardan biri - "
             "monolit va mikroservis yondashuvlari o'rtasidagi tanlovdir. "
             "Monolit arxitekturada butun ilova yagona, ajralmas birlik "
             "sifatida ishlab chiqiladi va joylashtiriladi. Bu yondashuv "
             "boshlang'ich bosqichda soddaroq, ammo tizim kattalashgan sari "
             "uni rivojlantirish va masshtablash qiyinlashadi. Mikroservis "
             "arxitekturada esa tizim mustaqil joylashtiriladigan kichik "
             "servislarga bo'linadi, ularning har biri o'z vazifasini "
             "bajaradi va o'z ma'lumotlar omboriga ega bo'lishi mumkin."),
    ("body", "Akademik monitoring tizimi uchun gibrid yondashuv maqsadga "
             "muvofiq deb topildi: tizim mantiqiy ravishda mustaqil "
             "modullarga (servislarga) ajratiladi, lekin ularning ko'pchiligi "
             "umumiy ma'lumotlar omboridan foydalanadi. Bu yondashuv "
             "mikroservislarning kengaytiriluvchanlik afzalliklarini saqlab "
             "qolgan holda, to'liq taqsimlangan tizimning murakkabligidan "
             "qochish imkonini beradi. Tizim o'sib borishi bilan ayrim "
             "modullarni to'liq mustaqil servislarga ajratish mumkin."),
    ("h3", "Normalizatsiya va ma'lumotlar yaxlitligi."),
    ("body", "Ma'lumotlar bazasini mantiqiy loyihalashda normalizatsiya "
             "muhim o'rin tutadi. Normalizatsiya - bu jadvallarni shunday "
             "tashkil etishki, ma'lumotlar takrorlanmasin va yangilanish "
             "anomaliyalari yuzaga kelmasin. Masalan, agar talabaning guruhi "
             "haqidagi ma'lumot har bir baho yozuvida takrorlansa, guruh "
             "nomi o'zgarganda uni ko'p joyda yangilashga to'g'ri keladi va "
             "xatolik ehtimoli oshadi. Normalizatsiyada guruh ma'lumotlari "
             "alohida jadvalga ajratiladi va baho yozuvi unga faqat havola "
             "(kalit) orqali bog'lanadi."),
    ("body", "Ma'lumotlar yaxlitligini ta'minlash uchun cheklovlardan "
             "(constraints) foydalaniladi: birlamchi kalit har bir yozuvning "
             "yagonaligini, tashqi kalit esa jadvallar o'rtasidagi "
             "bog'lanishning to'g'riligini kafolatlaydi. Masalan, baho yozuvi "
             "faqat mavjud talaba va mavjud fanga bog'lanishi mumkin. Bundan "
             "tashqari, qiymat cheklovlari (masalan, ball 0 dan 100 gacha "
             "bo'lishi) ma'lumotlarning mantiqiy to'g'riligini ta'minlaydi. "
             "Ushbu mexanizmlar birgalikda ma'lumotlar bazasining "
             "ishonchliligini kafolatlaydi."),
    ("h3", "Tahliliy ombor va yulduz sxemasi."),
    ("body", "Operativ baza kundalik ishlar uchun normalizatsiya qilingan "
             "bo'lsa, tahliliy ombor (data warehouse) tahlil qulayligi uchun "
             "boshqacha tarzda tashkil etiladi. Tahliliy omborda ko'pincha "
             "\"yulduz sxemasi\" (star schema) qo'llaniladi: markazda "
             "o'lchanadigan faktlar jadvali (masalan, baholash faktlari), "
             "uning atrofida esa o'lchamlar jadvallari (talaba, fan, vaqt, "
             "guruh) joylashadi. Bu tuzilma katta hajmdagi ma'lumotlar "
             "bo'yicha turli kesimlarda tez tahliliy so'rovlar bajarish "
             "imkonini beradi."),
    ("body", "Masalan, yulduz sxemasi yordamida \"ma'lum bir yo'nalishda "
             "so'nggi uch semestrda o'rtacha ball qanday o'zgargan?\" yoki "
             "\"qaysi fanlar bo'yicha o'zlashtirish eng past?\" kabi "
             "savollarga tezda javob olish mumkin. Operativ bazadan tahliliy "
             "omborga ma'lumotlar ETL jarayoni orqali muntazam ko'chiriladi. "
             "Bunday ajratish operativ tizimning unumdorligiga ta'sir "
             "qilmagan holda murakkab tahlillarni o'tkazish imkonini beradi."),
    ("h3", "Ma'lumotlarni saqlash strategiyasi."),
    ("body", "Akademik monitoring tizimida turli xil ma'lumotlar saqlanadi: "
             "tuzilmali (talabalar, baholar, fanlar), yarim tuzilmali "
             "(jurnal yozuvlari, sozlamalar) va katta hajmli tahliliy "
             "ma'lumotlar. Har bir tur uchun mos saqlash texnologiyasini "
             "tanlash muhim. Tuzilmali ma'lumotlar relatsion bazada, tez "
             "o'zgaruvchi va keshlanadigan ma'lumotlar xotirada ishlovchi "
             "omborlarda, katta hajmli tahliliy ma'lumotlar esa ustunli "
             "(columnar) omborlarda saqlanishi mumkin. Bunday \"har bir "
             "vazifaga mos vosita\" (polyglot persistence) yondashuvi "
             "tizimning umumiy unumdorligini oshiradi."),
    ("body", "Ma'lumotlar xavfsizligi va yaxlitligini ta'minlash uchun "
             "muntazam zaxira nusxalash (backup), tranzaksiyalarni boshqarish "
             "va ma'lumotlarni tiklash mexanizmlari ko'zda tutiladi. Tarixiy "
             "ma'lumotlarni uzoq muddat saqlash siyosati ham belgilanadi, bu "
             "uzoq davrlardagi tendensiyalarni tahlil qilish imkonini beradi. "
             "Shuningdek, ma'lumotlarni arxivlash mexanizmi operativ bazaning "
             "hajmini boshqarib turishga yordam beradi."),
    ("h3", "Tizimni masshtablash va ishonchlilikni ta'minlash."),
    ("body", "Tizim foydalanuvchilar va ma'lumotlar hajmi oshgan sari "
             "barqaror ishlashda davom etishi kerak. Buning uchun ikki turdagi "
             "masshtablashdan foydalaniladi: vertikal (serverning quvvatini "
             "oshirish) va gorizontal (qo'shimcha serverlar qo'shish). "
             "Gorizontal masshtablash zamonaviy tizimlarda afzal "
             "hisoblanadi, chunki u deyarli cheksiz o'sish imkonini beradi. "
             "Buning uchun amaliy servislar holatsiz (stateless) tarzda "
             "loyihalanadi, bu ularning bir nechta nusxasini parallel "
             "ishlatishga imkon beradi. Yuklamani taqsimlash (load balancing) "
             "kelgan so'rovlarni server nusxalari o'rtasida teng taqsimlaydi."),
    ("body", "Ishonchlilikni ta'minlash uchun tizimda zaxiralash "
             "(redundancy) tamoyili qo'llaniladi: muhim komponentlar bir "
             "nechta nusxada ishlaydi, shunda bittasi ishdan chiqsa, "
             "boshqasi uning vazifasini davom ettiradi. Ma'lumotlar bazasi "
             "uchun replikatsiya (nusxalash) qo'llaniladi, bu ham "
             "ishonchlilikni, ham o'qish so'rovlarining unumdorligini "
             "oshiradi. Tizim holatini doimiy kuzatish (monitoring) va "
             "muammolar haqida avtomatik ogohlantirish mexanizmlari ham "
             "ishonchlilikni ta'minlashning muhim qismidir. Bu mexanizmlar "
             "nofunksional talablardagi yuqori darajadagi ishlash "
             "ko'rsatkichlariga (availability) erishishni kafolatlaydi."),

    # =================== 2.3 ===================
    ("h2", "2.3. Tizimning funksional modullari va ularning ishlash "
           "mexanizmi"),
    ("body", "Modulli arxitektura tamoyiliga muvofiq, tizim funksiyalari "
             "mustaqil, lekin o'zaro bog'langan modullarga taqsimlanadi. Har "
             "bir modul aniq belgilangan vazifani bajaradi, bu esa tizimni "
             "ishlab chiqish va kengaytirishni osonlashtiradi. Quyida "
             "tizimning asosiy funksional modullari va ularning ishlash "
             "mexanizmi batafsil ko'rib chiqiladi."),
    ("h3", "Ma'lumotlarni yig'ish va integratsiyalash moduli."),
    ("body", "Bu modul tizimning \"kirish darvozasi\" hisoblanadi. U turli "
             "manba tizimlardan (kontingent, reyting, davomat, masofaviy "
             "ta'lim) ma'lumotlarni yig'adi. Yig'ish ikki usulda amalga "
             "oshiriladi: rejalashtirilgan vaqtda avtomatik (masalan, har "
             "kecha) yoki real vaqtda voqealar asosida. Yig'ilgan ma'lumotlar "
             "ETL (Extract-Transform-Load) jarayonidan o'tadi: olinadi, "
             "tozalanadi va yagona formatga keltiriladi, so'ngra markaziy "
             "omborga yuklanadi. Modul ma'lumotlardagi xatoliklarni aniqlash "
             "va to'g'rilash mexanizmiga ega."),
    ("h3", "Ko'rsatkichlarni hisoblash va tahlil moduli."),
    ("body", "Ushbu modul tizimning \"miyasi\" vazifasini bajaradi. U "
             "yig'ilgan dastlabki ma'lumotlar asosida akademik "
             "ko'rsatkichlarni (o'rtacha ball, o'zlashtirish foizi, reyting "
             "dinamikasi, davomat koeffitsienti va boshqalar) hisoblaydi. "
             "Bundan tashqari, modul statistik tahlil o'tkazadi: "
             "tendensiyalarni aniqlaydi, davrlar va guruhlarni qiyoslaydi, "
             "korrelyatsiyalarni hisoblaydi. Hisoblangan natijalar keyingi "
             "tez foydalanish uchun ko'rsatkichlar jadvalida saqlanadi."),
    ("h3", "Akademik xavfni baholash va erta ogohlantirish moduli."),
    ("body", "Bu modul tizimning eng muhim innovatsion qismi hisoblanadi, "
             "chunki u monitoringni reaktiv yondashuvdan proaktiv yondashuvga "
             "o'tkazadi. Modul har bir talaba bo'yicha akademik xavf "
             "darajasini bir necha ko'rsatkich asosida baholaydi. Xavfni "
             "baholashda quyidagi omillar inobatga olinadi: o'rtacha ballning "
             "pasayish tendensiyasi, akademik qarzdorliklar soni, darslarni "
             "qoldirish darajasi va topshiriqlarni bajarmaslik. Har bir "
             "omilga vazn (koeffitsient) beriladi va umumiy xavf indeksi "
             "hisoblanadi."),
    ("body", "Umumiy xavf indeksi quyidagi umumlashtirilgan ko'rinishda "
             "ifodalanadi: R = w1*f1 + w2*f2 + ... + wn*fn, bunda fi - i-omil "
             "qiymati (normallashtirilgan), wi - uning vazni. Hisoblangan "
             "indeks qiymatiga ko'ra talaba uch toifaga ajratiladi: past "
             "xavf (\"yashil\"), o'rta xavf (\"sariq\") va yuqori xavf "
             "(\"qizil\") zonalari. Quyidagi jadvalda xavf darajalari va "
             "ularga mos chora-tadbirlar keltirilgan."),
    ("table", [
        ["Xavf zonasi", "Holat", "Tavsiya etiladigan chora"],
        ["Yashil", "Xavf past, ko'rsatkichlar barqaror",
         "Standart kuzatuv."],
        ["Sariq", "O'rta xavf, salbiy tendensiya kuzatilmoqda",
         "Tyutor bilan suhbat, qo'shimcha kuzatuv."],
        ["Qizil", "Yuqori xavf, qarzdorlik yoki keskin pasayish",
         "Tezkor aralashuv, individual reja."],
    ]),
    ("caption", "2.4-jadval. Akademik xavf zonalari va chora-tadbirlar"),
    ("body", "Talaba yuqori xavf zonasiga o'tganda, tizim avtomatik ravishda "
             "tegishli mas'ul shaxslarga (tyutor, dekanat) ogohlantirish "
             "(notifikatsiya) yuboradi. Bu erta ogohlantirish mexanizmi "
             "muammoni u jiddiylashguncha aniqlash va profilaktik chora "
             "ko'rish imkonini beradi - bu birinchi bobda qayd etilgan "
             "an'anaviy monitoringning asosiy kamchiligini bartaraf etadi."),
    ("h3", "Vizuallashtirish va boshqaruv paneli moduli."),
    ("body", "Bu modul tahlil natijalarini foydalanuvchiga tushunarli va "
             "ko'rgazmali shaklda taqdim etadi. U interaktiv boshqaruv "
             "panellari (dashboard) ni shakllantiradi: ko'rsatkichlar "
             "grafiklar, diagrammalar, indikatorlar va issiqlik xaritalari "
             "(heatmap) ko'rinishida aks ettiriladi. Foydalanuvchi "
             "ma'lumotlarni turli kesimlarda filtrlash va batafsil ko'rish "
             "(drill-down) imkoniyatiga ega. Har bir foydalanuvchi roliga "
             "mos boshqaruv paneli ko'rsatiladi: rahbariyat umumiy "
             "ko'rsatkichlarni, o'qituvchi esa o'z fanlari bo'yicha "
             "ma'lumotlarni ko'radi."),
    ("h3", "Hisobot moduli."),
    ("body", "Hisobot moduli belgilangan shablonlar asosida turli xil "
             "hisobotlarni avtomatik shakllantiradi (talaba bo'yicha, guruh "
             "bo'yicha, davr bo'yicha va h.k.). Hisobotlar PDF, Excel kabi "
             "formatlarda eksport qilinadi. Modul rejalashtirilgan "
             "hisobotlarni avtomatik tayyorlash va tegishli shaxslarga "
             "yuborish imkoniyatiga ham ega."),
    ("body", "Hisobotlar ikki turga bo'linadi: standart (oldindan "
             "belgilangan shablonli) va moslashtiriladigan (foydalanuvchi "
             "o'zi parametrlarni tanlaydigan). Standart hisobotlar muntazam "
             "hisobot beruvchi jarayonlarni avtomatlashtiradi, "
             "moslashtiriladigan hisobotlar esa o'ziga xos tahliliy "
             "ehtiyojlarni qondiradi. Modul, shuningdek, hisobotlarni "
             "muayyan vaqtda (masalan, har oy boshida) avtomatik tayyorlash "
             "va belgilangan shaxslarga yuborish jadvali (scheduler) bilan "
             "jihozlanadi. Bu rahbariyatni qo'shimcha harakatsiz, doimiy "
             "ravishda dolzarb ma'lumotlar bilan ta'minlaydi."),
    ("h3", "Ma'lumotnomalarni boshqarish moduli."),
    ("body", "Tizimning to'g'ri ishlashi uchun ko'plab ma'lumotnomalar "
             "(spravochniklar) - fakultetlar, yo'nalishlar, fanlar, o'quv "
             "rejalari, baholash mezonlari ro'yxati - yuritilishi kerak. "
             "Ma'lumotnomalarni boshqarish moduli ushbu asosiy ma'lumotlarni "
             "kiritish, tahrirlash va dolzarb holatda saqlash imkonini "
             "beradi. Ma'lumotnomalarning to'g'riligi butun tizimning "
             "ishonchliligiga ta'sir qiladi, chunki barcha hisob-kitoblar va "
             "tahlillar ularga tayanadi."),
    ("body", "Modul ma'lumotnomalardagi o'zgarishlarni tarixini (versiyalarini) "
             "saqlaydi, bu o'tmishdagi ma'lumotlarni to'g'ri talqin qilish "
             "uchun zarur. Masalan, agar o'quv reja o'zgargan bo'lsa, eski "
             "semestr ma'lumotlari o'sha davrdagi reja asosida, yangi "
             "ma'lumotlar esa yangilangan reja asosida hisoblanishi kerak. "
             "Ma'lumotnomalarni markazlashtirilgan boshqarish tizimning "
             "barcha modullari yagona, izchil ma'lumotlar bilan ishlashini "
             "kafolatlaydi."),
    ("h3", "Ogohlantirish va xabarnoma moduli."),
    ("body", "Ogohlantirish moduli tizimning proaktiv tabiatini ta'minlovchi "
             "muhim komponentdir. U boshqa modullardan kelgan voqealar "
             "asosida tegishli foydalanuvchilarga o'z vaqtida xabarnoma "
             "yuboradi. Xabarnomalar bir necha kanal orqali yetkaziladi: "
             "tizim ichidagi bildirishnomalar, elektron pochta va, zarurat "
             "bo'lsa, qisqa matnli xabarlar. Modul xabarnomalarning "
             "ahamiyatlilik darajasini ajratadi: oddiy axborot xabarlari va "
             "shoshilinch ogohlantirishlar turlicha taqdim etiladi."),
    ("body", "Modulning ishlash mantig'i quyidagicha: xavfni baholash moduli "
             "talabani qizil zonaga o'tkazganda, ogohlantirish moduli "
             "talabaning tyutori va dekanatига avtomatik xabar yuboradi. "
             "Xabarda talabaning kim ekanligi, xavf sababi va tavsiya "
             "etiladigan harakat ko'rsatiladi. Bu mas'ul shaxslarga "
             "vaziyatni tushunish va tezkor chora ko'rish imkonini beradi. "
             "Foydalanuvchilar xabarnomalarni qaysi hodisalar bo'yicha va "
             "qaysi kanal orqali olishni o'zlari sozlay olishadi, bu ortiqcha "
             "xabarlardan (notification fatigue) saqlanishga yordam beradi."),
    ("h3", "Boshqaruv panelining tashkil etilishi."),
    ("body", "Boshqaruv paneli (dashboard) tizimning eng ko'rinadigan va "
             "tez-tez ishlatiladigan qismidir. Uning samaradorligi "
             "ma'lumotlarning to'g'ri tashkil etilishi va vizuallashtirilishiga "
             "bog'liq. Panel tepasida eng muhim umumlashtirilgan "
             "ko'rsatkichlar (KPI kartalari) joylashtiriladi: umumiy "
             "o'zlashtirish, o'rtacha ball, xavf ostidagi talabalar soni. "
             "Quyiroqda batafsil grafiklar - o'zlashtirish dinamikasi, "
             "guruhlar bo'yicha taqqoslash, davomat tendensiyasi - "
             "joylashtiriladi."),
    ("body", "Vizuallashtirishda ma'lumot turiga mos grafik tanlanadi: "
             "vaqt bo'yicha o'zgarish uchun chiziqli grafik, qismlarni "
             "taqqoslash uchun ustunli diagramma, ulushlarni ko'rsatish uchun "
             "doiraviy diagramma, ko'p o'lchovli ma'lumot uchun issiqlik "
             "xaritasi qo'llaniladi. Rang kodlash izchil bo'lishi muhim: "
             "yashil - yaxshi holat, sariq - ogohlantirish, qizil - muammo. "
             "Foydalanuvchi har qanday ko'rsatkichni bosib, uning "
             "tafsilotlariga o'tishi (drill-down) mumkin, masalan, fakultet "
             "ko'rsatkichidan guruhlar, undan esa alohida talabalar "
             "darajasiga tushishi mumkin."),
    ("body", "Boshqaruv paneli har bir foydalanuvchi roliga moslashtiriladi "
             "(personalizatsiya). Rektor umummuassasa ko'rsatkichlarini, "
             "dekan o'z fakulteti ma'lumotlarini, o'qituvchi esa o'z fanlari "
             "bo'yicha natijalarni ko'radi. Bu har bir foydalanuvchiga aynan "
             "o'ziga kerakli ma'lumotni taqdim etadi va ortiqcha "
             "ma'lumotlardan chalg'imaslikni ta'minlaydi. Panel interaktiv "
             "filtrlar (davr, fakultet, yo'nalish, ta'lim shakli bo'yicha) "
             "bilan jihozlanadi, bu foydalanuvchiga ma'lumotlarni turli "
             "kesimlarda mustaqil tahlil qilish erkinligini beradi."),
    ("h3", "Foydalanuvchilarni va xavfsizlikni boshqarish moduli."),
    ("body", "Bu modul autentifikatsiya (foydalanuvchini tanish) va "
             "avtorizatsiya (kirish huquqlarini tekshirish) ni ta'minlaydi. "
             "U rollar asosida kirishni boshqarish (RBAC) modelidan "
             "foydalanadi: har bir foydalanuvchiga rol biriktiriladi, rol esa "
             "muayyan funksiyalar va ma'lumotlarga kirish huquqini belgilaydi. "
             "Modul, shuningdek, tizimdagi barcha muhim harakatlarni audit "
             "jurnalida qayd etadi, bu xavfsizlik va shaffoflikni "
             "ta'minlaydi."),
    ("body", "Modullar o'zaro dasturiy interfeyslar (API) orqali aloqa "
             "qiladi. Masalan, vizuallashtirish moduli ko'rsatkichlarni "
             "tahlil modulidan, xavf moduli esa hisoblangan ko'rsatkichlardan "
             "foydalanadi. Bunday modulli tuzilma har bir komponentni "
             "mustaqil rivojlantirish va, zarurat tug'ilsa, almashtirish "
             "imkonini beradi."),
    ("h3", "Akademik xavfni baholash algoritmi: batafsil bayon."),
    ("body", "Xavfni baholash moduli ishini aniq tushunish uchun uning "
             "algoritmini bosqichma-bosqich ko'rib chiqamiz. Algoritm "
             "quyidagi ketma-ketlikda ishlaydi: dastlab har bir talaba uchun "
             "tanlangan omillar (o'rtacha ball, davomat, qarzdorliklar, "
             "topshiriqlar bajarilishi) ning joriy qiymatlari yig'iladi. "
             "So'ngra har bir omil [0, 1] oralig'iga normallashtiriladi, "
             "bu turli o'lchov birliklaridagi ko'rsatkichlarni "
             "solishtirilishi mumkin holga keltiradi. Keyin har bir "
             "normallashtirilgan omil o'ziga tegishli vaznga ko'paytiriladi "
             "va ularning yig'indisi sifatida umumiy xavf indeksi "
             "hisoblanadi."),
    ("body", "Omillarning vaznlari ekspert baholash usuli yordamida yoki "
             "tarixiy ma'lumotlar tahlili asosida belgilanadi. Masalan, agar "
             "tahlil natijasida akademik qarzdorlik o'qishni tashlab "
             "ketishning eng kuchli belgisi ekanligi aniqlansa, bu omilga "
             "yuqoriroq vazn beriladi. Vaznlarni tarixiy ma'lumotlardan "
             "avtomatik o'rganish uchun kelajakda mashinaviy o'qitish "
             "usullari (masalan, logistik regressiya yoki qaror daraxtlari) "
             "qo'llanilishi mumkin, bu xavf bashoratining aniqligini "
             "oshiradi."),
    ("body", "Hisoblangan xavf indeksi belgilangan chegaraviy qiymatlar "
             "bilan solishtiriladi va talaba tegishli zonaga (yashil, sariq "
             "yoki qizil) joylashtiriladi. Chegaraviy qiymatlar ham "
             "moslashtiriladigan bo'lib, ular muassasa siyosati va tarixiy "
             "ma'lumotlar asosida sozlanadi. Talabaning zonasi o'zgarganda, "
             "ayniqsa u qizil zonaga o'tganda, tizim avtomatik ravishda "
             "tegishli mas'ul shaxslarga ogohlantirish yuboradi va voqeani "
             "jurnalda qayd etadi."),
    ("h3", "Ma'lumotlar oqimi va modullarning o'zaro ta'siri."),
    ("body", "Tizimdagi ma'lumotlar oqimini quyidagicha tasvirlash mumkin. "
             "Avval ma'lumot yig'ish moduli manba tizimlardan dastlabki "
             "ma'lumotlarni oladi va ularni markaziy omborga joylaydi. So'ngra "
             "ko'rsatkichlarni hisoblash moduli bu ma'lumotlar asosida "
             "akademik ko'rsatkichlarni hisoblaydi. Hisoblangan ko'rsatkichlar "
             "xavfni baholash moduli tomonidan tahlil qilinadi va xavf "
             "indekslari shakllantiriladi. Nihoyat, vizuallashtirish va "
             "hisobot modullari bu natijalarni foydalanuvchiga taqdim etadi. "
             "Bu oqim rejalashtirilgan vaqtda yoki yangi ma'lumot kelganda "
             "avtomatik takrorlanadi."),
    ("body", "Modullarning o'zaro ta'siri voqealarga asoslangan "
             "(event-driven) yondashuv orqali ham tashkil etilishi mumkin. "
             "Bunda biror voqea (masalan, yangi bahoning kiritilishi) tegishli "
             "modullarni faollashtiradi: ko'rsatkichlar qayta hisoblanadi, "
             "xavf indeksi yangilanadi va zarur bo'lsa ogohlantirish "
             "yuboriladi. Bu yondashuv tizimning real vaqt rejimida ishlashini "
             "va ma'lumotlarning doimo dolzarb bo'lishini ta'minlaydi."),

    ("h3", "Tizim ishlashining yaxlit misoli."),
    ("body", "Modullarning birgalikda qanday ishlashini yaxlit misol orqali "
             "ko'rsatamiz. Faraz qilaylik, ma'lum bir talaba ketma-ket "
             "ikkita oraliq nazoratdan past ball oldi va so'nggi ikki haftada "
             "darslarga muntazam qatnashmadi. Bu ma'lumotlar reyting va "
             "davomat tizimlarida qayd etiladi. Tunги rejalashtirilgan "
             "yig'ish vaqtida ma'lumot yig'ish moduli ushbu yangi yozuvlarni "
             "markaziy omborga yuklaydi."),
    ("body", "So'ngra ko'rsatkichlarni hisoblash moduli talabaning yangilangan "
             "o'rtacha ballini va davomat koeffitsientini qayta hisoblaydi va "
             "ularning salbiy tendensiyasini qayd etadi. Xavfni baholash "
             "moduli yangilangan ko'rsatkichlar asosida talabaning xavf "
             "indeksini qayta hisoblaydi; indeks chegaraviy qiymatdan oshib, "
             "talaba sariq zonadan qizil zonaga o'tadi. Shu zahoti "
             "ogohlantirish moduli talabaning tyutoriga va dekanatига "
             "xabarnoma yuboradi."),
    ("body", "Tyutor tizimga kirib, talabaning batafsil profilini ko'radi: "
             "xavf sababi (past ballar va davomat), ko'rsatkichlar "
             "dinamikasi va tavsiya etilgan harakat. Tyutor talaba bilan "
             "suhbat o'tkazadi va individual yordam rejasini tuzadi. Keyingi "
             "haftalarda tizim talabaning ko'rsatkichlarini kuzatishda davom "
             "etadi; agar holat yaxshilansa, talaba avtomatik ravishda sariq "
             "yoki yashil zonaga qaytadi. Ushbu misol tizimning qanday qilib "
             "muammoni erta aniqlash va profilaktik aralashuvni ta'minlashini "
             "yaqqol ko'rsatadi - bu birinchi bobda aniqlangan an'anaviy "
             "monitoringning eng jiddiy kamchiligini bartaraf etadi."),
    ("h3", "Modullarni loyihalashda qo'llanilgan dasturiy shablonlar."),
    ("body", "Modullarni sifatli va kengaytiriladigan qilib loyihalash uchun "
             "sinovdan o'tgan dasturiy shablonlardan (design patterns) "
             "foydalaniladi. Masalan, ma'lumotlarga kirish qatlamida "
             "\"Repository\" shabloni qo'llaniladi, u biznes mantiqni "
             "ma'lumotlar saqlash tafsilotlaridan ajratadi. Turli manba "
             "tizimlardan ma'lumot olishda \"Adapter\" shabloni ishlatiladi, "
             "u har bir manbaning o'ziga xos interfeysini tizimning umumiy "
             "interfeysiga moslashtiradi. Bu yangi manba qo'shishni "
             "osonlashtiradi."),
    ("body", "Xavfni baholash algoritmini moslashuvchan qilish uchun "
             "\"Strategy\" shabloni qo'llaniladi: turli baholash usullari "
             "(oddiy vaznli yig'indi yoki mashinaviy o'qitishga asoslangan "
             "model) bir-birini almashtira oladigan tarzda loyihalanadi. "
             "Ogohlantirish modulida esa \"Observer\" shabloni ishlatiladi: "
             "manfaatdor modullar muayyan voqealarga obuna bo'ladi va voqea "
             "yuz berganda avtomatik xabardor qilinadi. Bunday shablonlardan "
             "foydalanish tizim kodining sifatini, qayta ishlatiluvchanligini "
             "va qo'llab-quvvatlash qulayligini sezilarli oshiradi hamda "
             "uning uzoq muddatli rivojlanishini ta'minlaydi."),

    # =================== 2.4 ===================
    ("h2", "2.4. Tizimni dasturiy amalga oshirish texnologiyalari"),
    ("body", "Tizimni amalda yaratish uchun zamonaviy va sinovdan o'tgan "
             "texnologiyalar majmuasini tanlash muhim ahamiyatga ega. "
             "Texnologiyalarni tanlashda quyidagi mezonlar inobatga olindi: "
             "ishlab chiqish samaradorligi, unumdorlik, kengaytiriluvchanlik, "
             "xavfsizlik, hamjamiyat tomonidan qo'llab-quvvatlanishi va "
             "ochiq kodli yechimlarning mavjudligi. Quyida tizimning har bir "
             "qatlami uchun tanlangan texnologiyalar asoslanadi."),
    ("h3", "Frontend (mijoz qismi) texnologiyalari."),
    ("body", "Foydalanuvchi interfeysi veb-ilova ko'rinishida ishlab "
             "chiqiladi. Buning uchun zamonaviy JavaScript ekotizimidagi "
             "komponentga asoslangan freymverklar (masalan, React yoki Vue) "
             "qo'llaniladi. Ular interaktiv va tez ishlaydigan interfeyslar "
             "yaratish imkonini beradi. Ma'lumotlarni vizuallashtirish uchun "
             "ixtisoslashgan grafik kutubxonalardan (masalan, Chart.js yoki "
             "D3.js) foydalaniladi. Interfeysning turli qurilmalarga "
             "moslashuvi (responsive dizayn) ham ta'minlanadi."),
    ("h3", "Backend (server qismi) texnologiyalari."),
    ("body", "Amaliy mantiq qatlami server tomonida amalga oshiriladi. "
             "Buning uchun keng tarqalgan va kuchli ekotizimga ega bo'lgan "
             "dasturlash tillaridan biri - Python (Django yoki FastAPI "
             "freymverki bilan), Java (Spring freymverki bilan) yoki Node.js "
             "tanlanishi mumkin. Ma'lumotlar tahlili va xavfni baholash "
             "algoritmlarini amalga oshirish qulayligi nuqtai nazaridan "
             "Python alohida ustunlikka ega, chunki uning ma'lumotlar "
             "tahlili kutubxonalari (Pandas, NumPy, scikit-learn) boy va "
             "yaxshi rivojlangan."),
    ("body", "Server qismi RESTful API yoki GraphQL interfeysi orqali mijoz "
             "qismi bilan ma'lumot almashadi. Bu frontend va backendni "
             "to'liq ajratish (decoupling) imkonini beradi va tizimga "
             "kelajakda mobil ilova kabi yangi mijozlarni qo'shishni "
             "osonlashtiradi."),
    ("body", "API ni loyihalashda izchillik va hujjatlashtirilganlik muhim. "
             "REST yondashuvida har bir resurs (talaba, fan, ko'rsatkich) "
             "uchun standart amallar (yaratish, o'qish, yangilash, o'chirish) "
             "yagona uslubda tashkil etiladi. API ning avtomatik hujjati "
             "(masalan, OpenAPI/Swagger spetsifikatsiyasi) ishlab "
             "chiquvchilar uchun integratsiyani osonlashtiradi. API "
             "versiyalanishi esa tizimni rivojlantirar ekan, mavjud "
             "integratsiyalarning buzilmasligini ta'minlaydi. Bu yondashuvlar "
             "tizimning kengaytiriluvchanligi va boshqa tizimlar bilan "
             "integratsiyalanuvchanligi bo'yicha nofunksional talablarni "
             "qondiradi."),
    ("h3", "Ma'lumotlar bazasini boshqarish tizimi (MBBT)."),
    ("body", "Tuzilmali akademik ma'lumotlarni saqlash uchun relatsion MBBT "
             "(masalan, PostgreSQL yoki MySQL) tanlanadi. PostgreSQL o'zining "
             "ishonchliligi, murakkab so'rovlarni qo'llab-quvvatlashi va "
             "ochiq kodliligi bilan ajralib turadi. Tahliliy yuklamani "
             "operativ bazadan ajratish uchun alohida ma'lumotlar ombori "
             "qo'llanilishi mumkin. Tez-tez murojaat qilinadigan "
             "ko'rsatkichlarni keshlash (caching) uchun esa Redis kabi "
             "xotirada ishlovchi ma'lumotlar ombori ishlatiladi, bu "
             "unumdorlikni sezilarli oshiradi."),
    ("h3", "Infratuzilma va joylashtirish texnologiyalari."),
    ("body", "Tizimning modullarini mustaqil joylashtirish va boshqarish "
             "uchun konteynerlashtirish texnologiyasi (Docker) qo'llaniladi. "
             "Har bir modul alohida konteynerda ishlaydi, bu ularni izolyatsiya "
             "qilish va masshtablashni osonlashtiradi. Ko'p sonli "
             "konteynerlarni boshqarish (orkestratsiya) uchun Kubernetes kabi "
             "vositalardan foydalanish mumkin. Tizim mahalliy serverda yoki "
             "bulutli platformada joylashtirilishi mumkin."),
    ("body", "Dasturiy ta'minotni ishlab chiqish jarayonida versiyalarni "
             "boshqarish tizimi (Git), uzluksiz integratsiya va yetkazib "
             "berish (CI/CD) amaliyotlari hamda avtomatik sinov (testing) "
             "qo'llaniladi. Bu kod sifatini va ishlab chiqish jarayonining "
             "barqarorligini ta'minlaydi. Quyidagi jadvalda tizimning "
             "texnologik majmuasi (technology stack) umumlashtirilgan."),
    ("table", [
        ["Qatlam/Vazifa", "Tanlangan texnologiyalar"],
        ["Frontend", "React/Vue, Chart.js/D3.js, HTML5, CSS3"],
        ["Backend", "Python (Django/FastAPI) yoki Java (Spring)"],
        ["Ma'lumotlar bazasi", "PostgreSQL, ombor uchun OLAP yechimi"],
        ["Keshlash", "Redis"],
        ["Integratsiya", "REST API / GraphQL, ETL vositalari"],
        ["Infratuzilma", "Docker, Kubernetes, CI/CD, Git"],
    ]),
    ("caption", "2.5-jadval. Tizimning texnologik majmuasi (technology stack)"),
    ("body", "Tanlangan texnologiyalar majmuasi 2.1-bo'limda shakllantirilgan "
             "funksional va nofunksional talablarni to'liq qondiradi. U "
             "tizimning yuqori unumdorligi, kengaytiriluvchanligi, "
             "xavfsizligi va qo'llab-quvvatlash qulayligini ta'minlaydi. "
             "Barcha tanlangan texnologiyalar ochiq kodli yoki keng tarqalgan "
             "bo'lib, bu loyihaning iqtisodiy samaradorligini oshiradi va "
             "muayyan ta'minotchiga bog'lanib qolish (vendor lock-in) "
             "xavfini kamaytiradi."),
    ("h3", "Backend freymverklarini qiyosiy tahlili."),
    ("body", "Server qismi uchun freymverk tanlashda bir necha variant qiyosiy "
             "tahlil qilindi. Python ekotizimidagi Django to'liq "
             "funksiyali (batteries included) freymverk bo'lib, u tez ishlab "
             "chiqish va boy imkoniyatlar taqdim etadi. FastAPI esa zamonaviy, "
             "yuqori unumli va API yaratishga ixtisoslashgan freymverk. Java "
             "ekotizimidagi Spring korporativ darajadagi ishonchlilik va "
             "kengaytiriluvchanlik bilan ajralib turadi. Node.js esa yagona "
             "til (JavaScript) bilan ham frontend, ham backend yaratish "
             "imkonini beradi."),
    ("table", [
        ["Mezon", "Django", "FastAPI", "Spring"],
        ["Til", "Python", "Python", "Java"],
        ["Ishlab chiqish tezligi", "Yuqori", "Yuqori", "O'rta"],
        ["Unumdorlik", "O'rta", "Yuqori", "Yuqori"],
        ["Tahlil kutubxonalari", "Boy", "Boy", "O'rta"],
        ["Korxona uchun moslik", "Yaxshi", "Yaxshi", "A'lo"],
    ]),
    ("caption", "2.8-jadval. Backend freymverklarining qiyosiy tahlili"),
    ("body", "Tahlil natijasida ushbu loyiha uchun Python ekotizimi (Django "
             "yoki FastAPI) afzal deb topildi, chunki tizimning markaziy "
             "qismi - ma'lumotlarni tahlil qilish va xavfni baholash - "
             "Python ning boy ma'lumotlar tahlili kutubxonalaridan keng "
             "foydalanishni taqozo etadi. Bu yagona texnologik ekotizimda "
             "ham biznes mantiqni, ham tahliliy funksiyalarni amalga oshirish "
             "imkonini beradi va ishlab chiqishni soddalashtiradi."),
    ("body", "Ma'lumotlarni tahlil qilish va xavfni baholash algoritmlarini "
             "amalga oshirishda Python ning Pandas (ma'lumotlar bilan "
             "ishlash), NumPy (sonli hisoblashlar) va scikit-learn "
             "(mashinaviy o'qitish) kutubxonalaridan foydalaniladi. Bu "
             "kutubxonalar katta hajmdagi ma'lumotlarni samarali qayta "
             "ishlash va murakkab tahliliy hisob-kitoblarni amalga oshirish "
             "imkonini beradi. Kelajakda tizimni bashoratli tahlil bilan "
             "kengaytirishda aynan shu kutubxonalar asos bo'ladi, bu Python "
             "tanlovini yanada asoslantiradi."),
    ("h3", "Ishlab chiqish jarayoni va DevOps amaliyotlari."),
    ("body", "Tizimni ishlab chiqishda zamonaviy dasturiy injiniring "
             "amaliyotlariga rioya qilish kod sifati va loyiha "
             "boshqaruvining muhim shartidir. Versiyalarni boshqarish uchun "
             "Git tizimi qo'llaniladi, bu kod o'zgarishlarini kuzatish va "
             "jamoaviy ishlashni ta'minlaydi. Ishlab chiqish jarayoni "
             "iterativ va bosqichli (Agile) yondashuvga asoslanadi: tizim "
             "kichik, ishlaydigan qismlar (sprintlar) bo'yicha "
             "rivojlantiriladi va har bir qismdan keyin natija baholanadi."),
    ("body", "Uzluksiz integratsiya va yetkazib berish (CI/CD) amaliyoti "
             "kodga kiritilgan har bir o'zgartirishni avtomatik sinovdan "
             "o'tkazish va joylashtirishni ta'minlaydi. Bu xatoliklarni erta "
             "aniqlash va yangi funksiyalarni tez yetkazib berish imkonini "
             "beradi. Konteynerlashtirish (Docker) esa tizimning turli "
             "muhitlarda (ishlab chiqish, sinov, ishlab chiqarish) bir xil "
             "ishlashini kafolatlaydi. Ushbu amaliyotlar majmui tizimni "
             "ishonchli rivojlantirish va qo'llab-quvvatlash uchun mustahkam "
             "asos yaratadi."),
    ("h3", "Xavfsizlikni ta'minlash texnologiyalari."),
    ("body", "Tizim shaxsiy ma'lumotlar bilan ishlagani sababli xavfsizlik "
             "alohida e'tibor talab qiladi. Autentifikatsiya uchun zamonaviy "
             "standartlar - JWT (JSON Web Token) yoki OAuth 2.0 protokoli "
             "qo'llaniladi. Foydalanuvchi paroli ochiq holda emas, balki "
             "kriptografik xesh ko'rinishida saqlanadi. Ma'lumotlar tarmoq "
             "orqali uzatilishida HTTPS protokoli (TLS shifrlash) ishlatiladi. "
             "Ma'lumotlar bazasiga kirish cheklangan va parametrlangan "
             "so'rovlar orqali SQL-in'ektsiya hujumlaridan himoyalanadi."),
    ("body", "Rollar asosida kirishni boshqarish (RBAC) modeli har bir "
             "foydalanuvchi faqat o'z vazifasi uchun zarur ma'lumotlarga "
             "kirishini ta'minlaydi. Bundan tashqari, barcha muhim "
             "harakatlar audit jurnalida qayd etiladi, bu xavfsizlik "
             "hodisalarini tekshirish imkonini beradi. Tizim muntazam "
             "xavfsizlik tekshiruvidan (audit) o'tkazib turilishi tavsiya "
             "etiladi."),
    ("h3", "Tizimni sinovdan o'tkazish va sifatni ta'minlash."),
    ("body", "Sifatli dasturiy ta'minot yaratishning ajralmas qismi - uni "
             "har tomonlama sinovdan o'tkazishdir. Tizim uchun bir necha "
             "darajadagi sinovlar ko'zda tutiladi: birlik sinovlari (unit "
             "tests) alohida funksiyalar to'g'ri ishlashini, integratsion "
             "sinovlar modullarning o'zaro to'g'ri ishlashini, tizim "
             "sinovlari esa butun tizimning talablarga muvofiqligini "
             "tekshiradi. Foydalanuvchi tomonidan qabul qilish sinovi "
             "(UAT) tizimning real foydalanuvchi ehtiyojlarini "
             "qondirishini baholaydi."),
    ("body", "Avtomatlashtirilgan sinovlar CI/CD jarayoniga integratsiya "
             "qilinadi: kodga har bir o'zgartirish kiritilganda sinovlar "
             "avtomatik ishga tushadi va xatoliklar erta aniqlanadi. Bu "
             "yondashuv kod sifatini doimiy yuqori darajada saqlash va yangi "
             "o'zgartirishlar mavjud funksiyalarni buzmasligini ta'minlash "
             "imkonini beradi. Unumdorlikni baholash uchun esa yuklama "
             "sinovlari (load testing) o'tkaziladi, bu tizim ko'p "
             "foydalanuvchi sharoitida barqaror ishlashini tasdiqlaydi."),
    ("h3", "Kutilayotgan amaliy va iqtisodiy samaradorlik."),
    ("body", "Ishlab chiqilgan tizimni joriy etish bir qator amaliy va "
             "iqtisodiy samaralar beradi. Amaliy jihatdan: hisobot tayyorlash "
             "vaqti sezilarli qisqaradi, ma'lumotlar aniqligi oshadi, xavf "
             "ostidagi talabalar o'z vaqtida aniqlanadi va profilaktik chora "
             "ko'rish imkoni paydo bo'ladi. Bu, o'z navbatida, o'qishni "
             "tashlab ketish hollarini kamaytirishga va ta'lim sifatini "
             "oshirishga olib keladi."),
    ("body", "Iqtisodiy jihatdan: qog'ozbozlik va qo'lda mehnat kamayadi, "
             "xodimlarning vaqti tejaladi va u yuqoriroq qiymatli vazifalarga "
             "yo'naltiriladi. Ochiq kodli texnologiyalardan foydalanish "
             "litsenziya xarajatlarini kamaytiradi. Talabalarni saqlab "
             "qolish (retention) darajasining oshishi esa muassasaning "
             "moliyaviy barqarorligiga ijobiy ta'sir ko'rsatadi. Quyidagi "
             "jadvalda tizimni joriy etishning kutilayotgan samaralari "
             "umumlashtirilgan."),
    ("table", [
        ["Yo'nalish", "Kutilayotgan samara"],
        ["Vaqt", "Hisobot va tahlil tayyorlash vaqtining qisqarishi"],
        ["Sifat", "Ma'lumotlar aniqligi va qaror sifatining oshishi"],
        ["Profilaktika", "Xavf ostidagi talabalarni erta aniqlash"],
        ["Resurs", "Qog'oz va qo'lda mehnat xarajatlarining kamayishi"],
        ["Strategik", "Dalillarga asoslangan boshqaruvga o'tish"],
    ]),
    ("caption", "2.6-jadval. Tizimni joriy etishning kutilayotgan samaralari"),
    ("h3", "Tizimni bosqichma-bosqich joriy etish rejasi."),
    ("body", "Murakkab axborot tizimini joriy etish bir martalik hodisa "
             "emas, balki rejalashtirilgan, bosqichli jarayon bo'lishi kerak. "
             "Birinchi bosqichda tizim cheklangan miqyosda - bitta fakultet "
             "yoki yo'nalish doirasida pilot tartibida joriy etiladi. Bu "
             "bosqichda tizimning real sharoitdagi ishlashi sinovdan "
             "o'tkaziladi, kamchiliklar aniqlanadi va foydalanuvchilardan "
             "qaytar aloqa to'planadi. Pilot bosqich xavflarni kamaytiradi va "
             "keng ko'lamli joriy etishdan oldin tizimni takomillashtirish "
             "imkonini beradi."),
    ("body", "Ikkinchi bosqichda, pilot natijalari ijobiy bo'lsa, tizim "
             "barcha fakultetlarga bosqichma-bosqich kengaytiriladi. Bu "
             "bosqichda mavjud axborot tizimlari bilan to'liq integratsiya "
             "amalga oshiriladi va foydalanuvchilar ommaviy o'qitiladi. "
             "Uchinchi bosqichda tizim to'liq ishga tushiriladi va uning "
             "ishlashi muntazam kuzatib boriladi. Keyingi bosqichlarda esa "
             "tizim yangi imkoniyatlar - sun'iy intellektga asoslangan "
             "bashorat, mobil ilova, tavsiya tizimi - bilan kengaytiriladi. "
             "Bunday bosqichli yondashuv tizimning muvaffaqiyatli "
             "o'zlashtirilishini va investitsiyalarning oqlanishini "
             "ta'minlaydi."),
    ("body", "Tizimni joriy etishda texnik jihatlar bilan bir qatorda "
             "tashkiliy va inson omiliga ham e'tibor qaratish zarur. Yangi "
             "tizimga o'tish xodimlarning ish uslubini o'zgartiradi, bu esa "
             "ba'zan qarshilikka sabab bo'lishi mumkin. Shu sababli "
             "foydalanuvchilarni o'qitish, ularga tizimning afzalliklarini "
             "tushuntirish va o'zgarishlarni boshqarish (change management) "
             "tizimni muvaffaqiyatli joriy etishning muhim shartlari "
             "hisoblanadi. Texnik jihatdan mukammal tizim ham foydalanuvchilar "
             "uni qabul qilmasa, kutilgan samarani bermaydi."),
    ("h3", "Tizimni baholash mezonlari va sinov natijalari."),
    ("body", "Ishlab chiqilgan tizimning samaradorligini obyektiv baholash "
             "uchun aniq mezonlar belgilanadi. Texnik mezonlar tizimning "
             "ishlash ko'rsatkichlarini (so'rovga javob berish vaqti, bir "
             "vaqtdagi foydalanuvchilar soni, ishlash barqarorligi) o'lchaydi. "
             "Funksional mezonlar tizimning belgilangan vazifalarni to'g'ri "
             "bajarishini tekshiradi. Foydalanuvchiga yo'naltirilgan mezonlar "
             "esa interfeysning qulayligi va foydalanuvchilar "
             "qoniqishini baholaydi."),
    ("body", "Pilot sinov bosqichida quyidagi natijalarga erishish kutiladi: "
             "hisobot tayyorlash vaqtining sezilarli qisqarishi, "
             "ma'lumotlardagi xatoliklar sonining kamayishi, xavf ostidagi "
             "talabalarni erta aniqlash darajasining oshishi va "
             "foydalanuvchilarning ijobiy baholari. Sinov natijalari tizimni "
             "yanada takomillashtirish uchun qaytar aloqa sifatida xizmat "
             "qiladi. Olingan natijalar tizimning qo'yilgan maqsadlarga "
             "javob berishini tasdiqlaydi va uni keng ko'lamda joriy etish "
             "uchun asos bo'ladi."),
    ("body", "Tizim samaradorligini baholashda an'anaviy usul bilan "
             "solishtirish muhim ahamiyatga ega. Sinov davomida bir qism "
             "jarayonlar an'anaviy, boshqalari esa yangi tizim orqali "
             "bajarilib, natijalar qiyoslanadi. Bu qiyosiy tahlil tizimning "
             "aniq afzalliklarini miqdoriy ko'rsatkichlar bilan asoslash "
             "imkonini beradi va uning amaliy qiymatini isbotlaydi."),

    # =================== Conclusions ===================
    ("h2", "II bob bo'yicha xulosalar"),
    ("body", "Dissertatsiyaning ikkinchi bobida avtomatlashtirilgan akademik "
             "monitoring tizimini loyihalash va ishlab chiqish masalalari "
             "ko'rib chiqildi va quyidagi xulosalarga kelindi:"),
    ("num", "Tizimga qo'yiladigan funksional (ma'lumotlarni yig'ish va "
            "integratsiyalash, ko'rsatkichlarni hisoblash, xavfni baholash, "
            "vizuallashtirish, hisobot va boshqaruv) hamda nofunksional "
            "(unumdorlik, kengaytiriluvchanlik, xavfsizlik, ishonchlilik, "
            "qulaylik) talablar tizimi shakllantirildi va foydalanuvchilar "
            "rollari aniqlandi."),
    ("num", "Tizim uchun ko'p qatlamli va modulli arxitektura ishlab "
            "chiqildi. Qatlamlarga (taqdimot, amaliy mantiq, ma'lumotlarga "
            "kirish va ma'lumotlar) ajratish mas'uliyatlarni ajratish "
            "tamoyilini ta'minlaydi, integratsiya shinasi esa ma'lumotlar "
            "tarqoqligi muammosini hal qiladi."),
    ("num", "Ma'lumotlar bazasining konseptual va mantiqiy modeli "
            "loyihalandi: asosiy mohiyatlar, ular o'rtasidagi bog'lanishlar "
            "aniqlandi, normalizatsiya va unumdorlikni oshirish usullari "
            "(indekslash, keshlash, OLTP/OLAP ajratish) asoslandi."),
    ("num", "Tizimning funksional modullari (ma'lumot yig'ish, tahlil, xavfni "
            "baholash, vizuallashtirish, hisobot va xavfsizlik) hamda "
            "ularning o'zaro ishlash mexanizmi ishlab chiqildi. Xavfni "
            "baholash va erta ogohlantirish moduli monitoringni proaktiv "
            "yondashuvga o'tkazib, an'anaviy tizimning asosiy kamchiligini "
            "bartaraf etadi."),
    ("num", "Tizimni dasturiy amalga oshirish uchun zamonaviy texnologik "
            "majmua (frontend, backend, ma'lumotlar bazasi, infratuzilma) "
            "asoslab tanlandi. Tanlangan ochiq kodli texnologiyalar qo'yilgan "
            "talablarni qondiradi va loyihaning iqtisodiy samaradorligini "
            "ta'minlaydi."),
]

UMUMIY_XULOSA = [
    ("h1", "UMUMIY XULOSA VA TAVSIYALAR"),
    ("body", "Magistrlik dissertatsiyasida oliy ta'limda avtomatlashtirilgan "
             "akademik monitoring tizimini ishlab chiqish va tahlil qilish "
             "masalasi kompleks o'rganildi. Olib borilgan tadqiqot natijasida "
             "quyidagi umumiy xulosalarga kelindi:"),
    ("num", "Akademik monitoring oliy ta'limda ta'lim sifatini boshqarishning "
            "strategik vositasi bo'lib, uning samaradorligi ma'lumotlarni "
            "yig'ish, qayta ishlash va taqdim etishning tezligi hamda "
            "aniqligiga bevosita bog'liq. An'anaviy qo'lda bajariladigan "
            "monitoring zamonaviy talablarga to'liq javob bermaydi."),
    ("num", "An'anaviy monitoringning asosiy muammolari - ma'lumotlarning "
            "tarqoqligi, kechikishi, xatoliklar va profilaktik imkoniyatning "
            "yo'qligi - aynan avtomatlashtirish orqali samarali hal etiladi."),
    ("num", "Taklif etilgan ko'p qatlamli va modulli arxitektura, ma'lumotlar "
            "bazasi modeli hamda funksional modullar majmui tizimning "
            "kengaytiriluvchanligi, ishonchliligi va integratsiyaga "
            "moslashuvchanligini ta'minlaydi."),
    ("num", "Akademik xavfni baholash va erta ogohlantirish moduli "
            "monitoringni reaktiv yondashuvdan proaktiv yondashuvga o'tkazib, "
            "xavf ostidagi talabalarni oldindan aniqlash va profilaktik chora "
            "ko'rish imkonini beradi. Bu tizimning asosiy ilmiy va amaliy "
            "yangiligi hisoblanadi."),
    ("num", "Tanlangan zamonaviy va ochiq kodli texnologik majmua tizimni "
            "amalda joriy etish uchun texnik va iqtisodiy jihatdan asoslangan "
            "yechim hisoblanadi."),
    ("body", "Amaliy tavsiyalar sifatida quyidagilarni taklif etish mumkin: "
             "tizimni dastlab pilot tartibida bitta fakultet miqyosida joriy "
             "etish va natijalarni baholash; mavjud axborot tizimlari bilan "
             "integratsiyani bosqichma-bosqich amalga oshirish; "
             "foydalanuvchilarni o'qitish bo'yicha qo'llanmalar tayyorlash; "
             "kelajakda tizimni mashinaviy o'qitishga asoslangan bashorat "
             "modullari bilan kengaytirish."),
    ("body", "Tadqiqotning istiqbolli yo'nalishlari sifatida xavfni baholash "
             "algoritmlarini sun'iy intellekt usullari bilan takomillashtirish, "
             "talabalar uchun shaxsiy tavsiyalar (recommendation) tizimini "
             "qo'shish hamda monitoring natijalarini ta'lim dasturlarini "
             "takomillashtirishda qo'llash masalalarini ko'rsatish mumkin."),
    ("body", "Umuman olganda, dissertatsiyada qo'yilgan maqsad to'liq amalga "
             "oshirildi va belgilangan vazifalar bajarildi. Olib borilgan "
             "tadqiqot avtomatlashtirilgan akademik monitoring tizimini "
             "ishlab chiqishning nazariy va amaliy asoslarini yaratdi. "
             "Taklif etilgan yechimlar oliy ta'lim muassasalarida ta'lim "
             "sifatini boshqarishni zamonaviy, dalillarga asoslangan "
             "darajaga ko'tarishga xizmat qiladi. Ishning natijalari "
             "amaliyotga joriy etilishi ta'lim jarayonining samaradorligini "
             "oshirishga sezilarli hissa qo'shadi."),
]
