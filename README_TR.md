# zero-to-trade

[中文](README.md) · [English](README_EN.md) · [Español](README_ES.md) · [Português](README_PT.md) · [Français](README_FR.md) · [العربية](README_AR.md) · [Русский](README_RU.md) · [Deutsch](README_DE.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · **Türkçe** · [Bahasa Indonesia](README_ID.md)

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-306998)

**"Hangi ülkeyi seçeceğim ki?" sorusundan "para hesaba geçti" anına kadar yedi aşama. Üstüne sıkıcı kısımları sizin yerinize yapan on beş Python scripti ve doğrudan tarayıcınızda çalışan dört araçlı bir web sitesi. Hiçbir deneyim varsayılmıyor. Bütün mesele de bu.**

> 200 soğuk e-posta gönderdiniz ve sıfır yanıt aldınız. Sorun İngilizceniz değil. Sorun, işleri hangi sırayla yaptığınız.
>
> Bu depo, "ihracata başlamak" fikrini gerçekten üzerinde çalışabileceğiniz bir işe dönüştürür: bu öğleden sonra hangi siteyi açacağınız, içine ne yazacağınız ve hangi sonucun geçtiğiniz anlamına geldiği.

> Buradaki her şeyin altında yatan tek kural: **Ağır işi yapay zekâ yapar, kararları siz verirsiniz.**

Satın alınacak kurs yok. Ücretli paket yok. E-posta duvarı yok. MIT lisanslı, V20.

> PR'larınızı bekliyoruz; özellikle de bu deponun adını bile duymadığı bir pazara satış yapıyorsanız. Bkz. [CONTRIBUTING.md](CONTRIBUTING.md).

## 7 adımlık demo: gerçek bir listeyi seviyelendirin ve ilk mesajınızı 2 dakikada yazın

Önce dokümanları okumanıza gerek yok. Yedi adım; her biri tek satır, her biri kopyalayıp yapıştıracağınız tek komut — baştan sona yaklaşık 2 dakika. Aşağıdaki yedi komutun hepsi bu depoda gerçekten çalıştırıldı (2026-11-22, Python 3.x, yalnızca standart kütüphane). Örnek veriler kurgusaldır; şirket adları 【示例】 ("örnek") önekini taşır.

| Adım | Tek satırda | Komut (kopyala-yapıştır) |
|---|---|---|
| 1 Liste edinin | Örneği kendi dosyanıza kopyalayın; gerçek potansiyel müşterileriniz yalnızca bu kopyaya girer | `cp examples/leads_example.csv my_leads.csv` |
| 2 Seviyelendirin | 10 potansiyel müşteri T0–T3 arasında sıralanır; bugün 2'sini arayın | `python scripts/lead_score.py my_leads.csv` |
| 3 T0'ları inceleyin | Yazmadan önce T0'ın paravan şirket olmadığını kontrol edin; sağlamadığınız her bilgi "doğrulanacak" olarak döner | `python scripts/due_diligence.py --company "【示例】海湾轮胎贸易"` |
| 4 İlk mesajı yazın | T0 seviyesi için ilk temas taslağı; İngilizcesi gönderilir, Çincesi sizin kontrolünüz içindir | `python scripts/outreach_gen.py my_leads.csv --tier T0` |
| 5 Takibi planlayın | D0/D2/D5 ritmi: 6 günde 3 temas, üçüncü sessizlikten sonra durun | `python scripts/followup_plan.py --tier T0 --start 2026-11-22 --csv my_leads.csv` |
| 6 Yanıt gelince teklif verin | Maliyet + navlun + kâr marjı → FOB/CIF aralığı + üç basamaklı indirim merdiveni | `python scripts/quote_engine.py --cost 28 --freight 6 --margin 15` |
| 7 Sessizleşince hatırlatın | Tekliften 7 gün sonra yanıt yoksa gelişmeyi sorun — kararlı olun, çaresiz değil | `python scripts/nudge.py --day D7 --scenario quoted` |

4. adımdan sonra elinizde gerçekten gönderebileceğiniz bir ilk temas e-postası olur; 5. adımdan sonra önümüzdeki 6 gün boyunca her gün ne yapacağınızı bilirsiniz.

Python yok mu? Web sitesini açın: [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/) (ya da yerel kopyada [`index.html`](index.html) dosyasına çift tıklayın). Sitede tarayıcıda çalışan dört araç var — potansiyel müşteri puanlama, ilk temas, takip planı ve teklif — scriptlerle aynı kurallarla; arayüz de 12 dilde (sağ üstteki menü). Örnek listeyi yükleyin → puanlayıp T0'larınızı bulun → ilk temas mesajını oluşturup kopyalayın → `[ ]` yer tutucularını kendi adınız, şirketiniz ve WhatsApp numaranızla değiştirin → D0/D2/D5 takiplerini planlayın → yanıt gelince teklif verin. Hiçbir şey yüklenmez: listeniz tarayıcıdan asla çıkmaz. Sitedeki ilk temas metni İngilizce ve Çince referansıyla gelir; İspanyolca, Portekizce veya Arapça metin için `outreach_gen.py --lang es/pt/ar` kullanın.

---

## Bu depo gerçekte neyi çözüyor

Google'a "ihracata nasıl başlanır" yazın. Karşınıza bir kişinin başarı hikâyesi, iki yüz SEO yazısı, ücretli bir kursun bedava ön izlemesi ve hızlı para vaat eden bir YouTube küçük resmi çıkar. Hepsini okursunuz, bilgilendiğinizi hissedersiniz; ertesi sabah ise bir gümrük verisi sitesine bakıp ilk alana ne yazacağınızı bilemezsiniz.

Bu bilgi eksikliği değil. Bu, yanlış biçimde sunulmuş bilgi: parçalara bölünmüş, kazananın bakış açısından yazılmış ve tam da sizin bir şey yapacağınız noktada kesilmiş.

Çoğu eğitim bunu şöyle ele alır. *"Müşterileriniz hakkında arka plan araştırması yapmalısınız."* Sonra: *"Arka plan araştırması önemlidir."* Sonra hiçbir şey. Hangi alanlara, hangi sitelere bakacağınızı, kırmızı bayrağın neye benzediğini ya da ne zaman yeterince kontrol ettiğinizi hâlâ bilmezsiniz.

Bu depo tam tersini yapar: **bir görevi alır ve bir eyleme dönüşene kadar parçalamaya devam eder.**

| Eğitimlerin dediği | Bu deponun dediği |
|---|---|
| "Arka plan araştırması yapın" | L1 eleme, üç kontrol: site var mı, şirket ne kadar süredir kayıtlı, sosyal medya hesapları canlı mı. Birinden kalırsa o potansiyel müşteri ölüdür. |
| "Kalite nicelikten önemlidir" | 10 potansiyel müşteri T0/T1/T2/T3 olarak sıralanır; her seviyenin kendi sonraki adımı ve kendi zaman bütçesi vardır. |
| "Onları takip edin" | 1., 3., 5., 7. gün. Her seferinde farklı bir açı; 7. gün bir kararla biter: üstüne gitmek ya da bırakmak. |
| "Yapay zekâ ticareti değiştiriyor" | Yalnızca standart kütüphane kullanan on beş Python scripti (biri teklif motoru olan on dört iş scripti ve bir gizlilik koruyucu). `python scripts/lead_score.py examples/leads_example.csv` yazın, yaklaşık otuz saniyede tam seviyelendirme elinizde. |

Aynı bilgi. Farklı **ayrıntı düzeyi**. Bütün fark bu. Buradaki her iddia tek bir sorudan sağ çıkmak zorunda: Bu öğleden sonra neyi açacağım ve ne yazacağım?

Yani hayır, bu bir motivasyon metni değil. Bu bir kontrol listesi ve on beş script dosyası (on dört iş scripti + bir gizlilik koruyucu).

---

## Yedi aşama

Baştan sona tek bir zincir: bir ülke seçin, hesaptaki parayla bitirin. Her aşama için bir doküman ve her doküman gerçekten kullanabileceğiniz bir şeyle biter.

| Aşama | Ne yaparsınız | Çıktı |
|---|---|---|
| **01 Pazar seçin** | Dil, talep ve engel açısından puanlayın | 1 ilk pazar + onu savunacak 3 gerekçe |
| **02 Potansiyel müşteri bulun** | Dört yol: gümrük verileri, sosyal medya, arama, fuarlar | Günde ≥20 doğrulanmış potansiyel müşteri |
| **03 Alıcıyı inceleyin** | L1 eleme → L2 standart → L3 derinlemesine inceleme | A/B/C derecesi; dolandırıcılar elenmiş |
| **04 İletişime geçin** | Potansiyel müşterileri T0-T3 olarak seviyelendirin; ilk temasta üç kanal kullanın | Seviyelendirilmiş liste + D0/D2/D5 takip planı (6 günde 3 temas) |
| **05 Teknik detayları konuşun** | Önce küçük talepler. Fiyat her zaman en sonda | Teknik özellik / miktar / varış limanı |
| **06 Teklif verin ve pazarlık yapın** | Teklif disiplini: her indirim karşılığında bir şey kazandırır | Teklif formu + indirim merdiveni + konuşma kalıpları |
| **07 Siparişi teslim edin** | Sözleşme, üretim, muayene, belgeler, ödeme, navlun | Kapanmış teslimat döngüsü + tekrar satın alma planı |

Aşama dokümanları `docs/` klasöründedir; her aşamaya bir dosya ve hepsi aynı altı bölümlü yapıyı izler (bkz. [CONTRIBUTING.md](CONTRIBUTING.md)): **bu aşama ne işe yarar → adım adım nasıl yapılır → geçti/kaldı ölçütleri → klasik hatalar → kopyala-yapıştır şablonlar → bu aşama için yapay zekâ komutları.**

**Daha önce hiç yapmadınız mı?** [`docs/00-getting-started.md`](docs/00-getting-started.md) ne git ne de Python bildiğinizi varsayar ve yaklaşık 10 dakikada sizi harekete geçirir. Aceleniz mi var? [`docs/fast-path.md`](docs/fast-path.md) sıfırdan ilk yanıtınıza yedi gün sürer.

---

## 30 saniyede başlangıç

**Python kurmak istemiyor musunuz?** Web sitesini açın: [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/). Dört tarayıcı aracı — potansiyel müşteri puanlama, ilk temas, takip planı ve teklif — 12 arayüz dilinde. Bir CSV yapıştırın, T0-T3 seviyelendirmesini alın, ardından ilk temas metnini, takip tarihlerini ve teklifi. Kurulacak bir şey yok ve tarayıcınızdan hiçbir şey çıkmıyor.

On beş script dosyası: biri teklif motoru olan on dört iş scripti ve bir gizlilik koruyucu script (`check_private_data.py`, commit etmeden önce gerçek müşteri verisini tarar). Yalnızca standart kütüphane. Python 3.10+.

```bash
# 1. Tier your leads. CSV in, T0-T3 out, each tier with its next move.
python scripts/lead_score.py examples/leads_example.csv

# 2. Draft outreach copy for one tier, English and 中文 side by side.
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Build the follow-up plan. Three touches, real dates.
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv

# 4. Quote: cost + freight + margin -> FOB/CIF range + a 3-step concession ladder.
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

İlk komutun 10 örnek potansiyel müşteri üzerinde gerçekte ne yazdırdığı aşağıda. Script çıktısı Çincedir; 【示例】 yalnızca "örnek" anlamına gelen bir işarettir ve son sütun burada çevrilmiştir:

| Seviye | Şirket | Ülke | Puan | Sonraki adım |
|---|---|---|---|---|
| T0 | 【示例】海湾轮胎贸易 | Suudi Arabistan | 95 | ilk teması bugün gönderin, beklemeyin |
| T0 | 【示例】三角洲轮胎 | Suudi Arabistan | 88 | ilk teması bugün gönderin, beklemeyin |
| T1 | 【示例】阿曼蓝海 | Umman | 77 | bu hafta; metni bugün hazırlayın |
| T1 | 【示例】半岛汽车 | Suudi Arabistan | 71 | bu hafta; metni bugün hazırlayın |
| T1 | 【示例】尼罗河商贸 | Mısır | 67 | bu hafta; metni bugün hazırlayın |
| T1 | 【示例】迪拜轮毂行 | BAE | 65 | bu hafta; metni bugün hazırlayın |
| T1 | 【示例】利雅得汽配 | Suudi Arabistan | 60 | bu hafta; metni bugün hazırlayın |
| T2 | 【示例】尼日利亚先锋 | Nijerya | 46 | soğuk havuz, günde bir kez gözden geçirin |
| T3 | 【示例】黎凡特供配 | Lübnan | 20 | bilgi yetersiz, önce iletişim bilgisi + ihtiyaç bulun |
| T3 | 【示例】利雅得零件店 | Suudi Arabistan | 10 | bilgi yetersiz, önce iletişim bilgisi + ihtiyaç bulun |

Özet: **T0:2 / T1:5 / T2:1 / T3:2**. Bugün iletişime geçin: 【示例】海湾轮胎贸易, 【示例】三角洲轮胎. Bu hafta: 【示例】阿曼蓝海, 【示例】半岛汽车, 【示例】尼罗河商贸, 【示例】迪拜轮毂行, 【示例】利雅得汽配. Şimdilik dokunmayın: 【示例】黎凡特供配, 【示例】利雅得零件店.

CSV başlığı:

```
company,country,product,source,email,phone,years,contact,note
```

Yalnızca `company` zorunludur. Geri kalan her şey boş bırakılabilir; boş alanlar en düşük puanı alır. Puanı en çok etkileyen `source` alanıdır: `referral` / `trade_show` / `customs` / `linkedin` / `search`.

On beş scriptin hepsi `--help` kabul eder. `lead_score.py` ayrıca `--format json` seçeneğine ve `--country` / `--product` filtrelerine sahiptir; çıktıyı bir tabloya aktarmak isterseniz işinize yarar.

Scriptler yalnızca bir makinenin karar verebileceği şeylere karar verir: e-posta var mı, web sitesi var mı, T0 çıtasını geçiyor mu. Bir potansiyel müşterinin öğleden sonranızı hak edip etmediği ise dokümanlarda ve sizin aklınızda.

---

## Depo yapısı

```
zero-to-trade/
├── README.md              # Çince tam sürüm
├── README_EN.md           # İngilizce sürüm (tüm çevirilerin referansı)
├── README_ES.md / README_PT.md / README_FR.md / README_AR.md / README_RU.md
├── README_DE.md / README_JA.md / README_KO.md / README_TR.md / README_ID.md
│                          # İspanyolca, Portekizce, Fransızca, Arapça (RTL), Rusça, Almanca, Japonca, Korece, Türkçe (bu dosya), Endonezce
├── index.html             # Web sitesi: 4 tarayıcı aracı, 12 arayüz dili, sıfır bağımlılık (GitHub Pages)
├── MANIFESTO.md           # Anonim, ücretli kurs yok: markanın duruşu
├── GITHUB_LAUNCH.md       # Lansman + tanıtım kontrol listesi (Topics/About/PR/Show HN)
├── CONTRIBUTING.md        # Nasıl katkı verilir + doküman ve kod kuralları
├── CHANGELOG.md           # Değişiklik günlüğü: her seferinde ne değişti
├── ROADMAP.md             # Yol haritası: sürümler bundan sonra nereye gidiyor
├── LICENSE                # MIT
├── docs/                  # Her aşamaya bir dosya
│   ├── 00-getting-started.md
│   ├── fast-path.md       # Sıfırdan ilk yanıta 7 gün
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md # Gerçekçi bir ilk satış örneği, baştan sona
├── scripts/               # Çalıştırılabilir Python, yalnızca standart kütüphane
│   ├── lead_score.py      # Potansiyel müşterileri T0-T3 olarak seviyelendirir
│   ├── outreach_gen.py    # Seviyeye göre ilk temas metni (EN/ZH + İngilizce referanslı ES/PT/AR, V13)
│   ├── followup_plan.py   # D0/D2/D5 takip planı (6 günde 3 temas)
│   ├── quote_engine.py    # Teklif motoru: FOB/CIF aralığı + 3 basamaklı indirim merdiveni
│   ├── due_diligence.py   # V11 firma araştırma ajanı: L1/L2/L3 + A/B/C derecesi + kırmızı bayraklar
│   ├── tire_pack.py       # V12 lastik sektörü paketi: ebat + pazar → GCC maddeleri + gümrükleme belgeleri + pazar notları
│   ├── landed_cost.py     # Varış maliyeti, V14: FOB + navlun + sigorta → CIF; buna gümrük vergisi + varış masrafları → DDP
│   ├── trade_show.py      # Fuar, V15: fuarda toplanan katılımcılar → 24 saatlik takip planı (2 saatte teşekkür, 12 saatte teklif girişi, 24 saatte arama/WhatsApp takibi)
│   ├── nudge.py           # Hatırlatma kütüphanesi, V16: D3/D7/D14/D30 × teklif verildi/numune gönderildi/pazarlıkta → kısa WhatsApp sürümü + uzun e-posta sürümü (İngilizce + Çince)
│   ├── anchor_price.py    # Rakip çıpa fiyatlandırması, V18: gümrük verisinden rakip fiyat aralığı + kendi maliyetiniz → agresif/orta/temkinli CIF seviyeleri + 5 maddelik kontrol listesi
│   ├── fast_path.py     # V19 etkileşimli 7 günlük hızlı yol: --day N görevleri gösterir, --done N işaretler, --progress toplamları verir (docs/fast-path.md ile uyumlu)
│   ├── market_rules.py    # Pazar kuralları: hedef pazarlar, Türkiye/Brezilya engelleri, Meksika/ABD/AB hariç tutmaları
│   ├── daily_video_list.py  # Günlük 5 videoluk liste (3'ü sabah, 2'si öğleden sonra); ebat, pazar, satış argümanı ve çekim kontrolleriyle
│   ├── fulfillment_checklist.py  # Sipariş yerine getirme kontrol listesi: PI → avans → üretim → muayene → bakiye → rezervasyon → gümrük → B/L → belgeler → satış sonrası, avans/serbest bırakma/sevkiyatta sert para kontrolleri
│   └── check_private_data.py  # Gizlilik koruyucu: commit öncesi gerçek müşteri verisini tarar
├── examples/
│   ├── leads_example.csv  # Örnek veri, olduğu gibi çalıştırılabilir
│   ├── leads_example_lighting.csv  # Lastik dışı örnek: 8 LED aydınlatma potansiyel müşterisi
│   └── trade_show_example.csv  # Örnek fuar katılımcıları, her ilgi düzeyinden bir tane
├── tests/                 # Standart kütüphaneyle yazılmış 586 test
├── prompts/
│   └── AI_PROMPTS.md      # Aşamalara göre gruplanmış 40 kopyala-yapıştır komut (28 temel + 12 ileri düzey)
└── assets/                # Ekran görüntüleri, diyagramlar
```

---

## Neden scriptler, neden sadece bir yöntem dokümanı değil

"İş için yapay zekâ" depolarının çoğu aynı şeyi yapar: metodolojiyi alır, bir komuta yapıştırır, yayınlar. Bu depo tersten çalışır. **Önce disiplin, sonra araçlar.**

Nedeni şu: **Komut yazmakta iyi olmak, ticarette iyi olmakla aynı şey değildir.** Benim tahminim, sizin eksiğiniz kelimeler değil. Eksiğiniz, karar vermenin bir yolu. Bu yüzden:

- **Burada ürün, kuralların kendisidir.** T0'a bugün e-posta gider. T3 üç ay çekmecede bekler. Karşılığında hiçbir şey kazandırmayan bir indirim pazarlık değil, hediyedir. Bu kararları sizin yerinize hiçbir model veremez.
- **Hacim yapay zekâya gider.** 8 potansiyel müşteriyi tek seferde elemek, 50 şirket için üç seviyeli arka plan araştırması taslağı çıkarmak, yedi günlük takip varyasyonları üretmek. Saatlerce iş, içinde neredeyse hiç muhakeme yok.
- **Tekrarlanabilen her şey scripte dönüşür.** Seviyelendirme bir histen ibaretse standart değildir. Bu yüzden sıfır bağımlılıklı, 200 satırın altında bir script; iki kişi çalıştırdığında aynı sonuca varır.

Çizginin durduğu yer: **`if/else` ile çözülebiliyor mu? Scripte. Bir ödünleşim gerektiriyor mu? Dokümanlara. Bir insan yazmış gibi mi görünmesi gerekiyor? `prompts/` klasörüne.**

Pandas yok, OpenAI SDK yok; bilerek. Ortam kurulumu, yeni başlayanların bıraktığı yerdir. İhracatta yeni olan biri, müşteri bulmaya harcayacağından daha çok saati `pip install` ile kaybeder; bu da saat kaybetmek için çok aptalca bir yer.

---

## Yol haritası

> Tam yol haritası: [ROADMAP.md](ROADMAP.md); değişiklik geçmişi: [CHANGELOG.md](CHANGELOG.md).

| Sürüm | Durum | İçerik |
|---|---|---|
| **V13** | ✅ Yayında (2026-11-07) | Çok dilli ilk temas (`scripts/outreach_gen.py --lang es/pt/ar`: İspanyolca/Portekizce/Arapça metin + her taslağın ardından İngilizce orijinal; şablonlar İngilizce T0/T1/T2'yi bire bir yansıtır, scriptte tek bir satır içi sözlük) + `docs/04-outreach.md` yeni bölüm (kullanım + birebir yapıştırılmış 3 gerçek çıktı) + `tests/` 80 standart kütüphane testi + 40 komut değişmedi (28 temel + 12 ileri düzey) + 7 script dosyası |
| **V18** | ✅ Yayında (2026-11-07) | Rakip çıpa fiyatlandırması (`scripts/anchor_price.py`: gümrük verisinden rakip fiyat aralığı + kendi maliyetiniz → agresif/orta/temkinli CIF seviyeleri; her biri kâr payı, marj, FOB karşılığı, örtük kâr oranı ve ne zaman kullanılacağıyla; teklif vermeden önce 5 maddelik kontrol listesi — maliyet, navlun, döviz kuru, ödeme koşulları, geçerlilik — kontrol edilmeyen her madde işaretlenir; maliyet altı uyarısı “maliyetin altında, siparişi almayın, önce hacim karşılığı fiyat pazarlığı yapın”; eksik medyan (düşük + yüksek) / 2 olarak tahmin edilir ve tahmin olarak işaretlenir; `--format json` / `--audience client`) + `docs/anchor-price.md` (kullanım + çıpa rehberi + birebir yapıştırılmış 2 gerçek çıktı) + `docs/06-quote.md` içinde bir satır (teklif öncesi çıpa) + `tests/` 187 standart kütüphane testi + 40 komut değişmedi (28 temel + 12 ileri düzey) + 11 script dosyası |
| **V20** | ✅ Güncel (2026-11-14) | Yerel artımlı birleştirme + 10 sağlamlaştırma turu: birleşik CLI girişleri (sade dilde hatalar, uyumlu çıkış kodları) + güçlendirilmiş testler (tek mesaj modu, `--start-date` takma adı, çalışma kayıtları) + doküman rakamları uyumlu hale getirildi + lastik dışı örnek (8 LED aydınlatma potansiyel müşterisi) + demo sayfası V19 ile eşitlendi + hatalı CSV'ler için anlaşılır hatalar (eksik sütun / boş dosya / kapanmamış tırnak artık traceback vermiyor) + komut uyumu (P04-4 takip komutuna `--avoid-weekend` eklendi, P10-2 penceresi 48 saatte birleştirildi) + çalışma izleme eklendi (`logs/trace-YYYY-MM-DD.jsonl`, üç çekirdek scriptin her çalışması için bir satır) + kod temizliği (ortak yardımcılar tek yerde, net −151 satır; iki ölü yardımcı kaldırıldı) + `tests/` 586 standart kütüphane testi + 40 komut değişmedi (28 temel + 12 ileri düzey) + 15 script dosyası |
| **V19** | ✅ Yayında (2026-11-07) | Etkileşimli 7 günlük hızlı yol (`scripts/fast_path.py`: `--day N` günün görevlerini gösterir — görev adı + ne üretileceği + hangi script/dokümanın kullanılacağı; `--done N` bir günü zaman damgasıyla işaretler ve `--state` JSON dosyasına yazar, tekrarlanan işaretleme zaten işaretlendiğini söyler ve iki kez kaydedilmez; `--progress` tamamlanan / kalan / geciken toplamlarını verir (geciken = planlanan tarihi bugünden önce olup işaretlenmemiş gün, planlanan tarih = `--start` 1. gün + (N-1) gün; `--start` yoksa geciken sayısı yoktur ve bu açıkça belirtilir); `--list` 7 günün tamamını gösterir; görevler `docs/fast-path.md` ile satır satır uyumludur, ikinci bir liste uydurulmadı; `--help` gerçek örnekler içerir, hatalı gün veya tarih sade dilde hata verir) + `docs/fast-path-interactive.md` (kullanım + durum dosyası biçimi + gecikme kuralı + 7 günlük genel bakış + birebir yapıştırılmış 2 gerçek çıktı) + `docs/fast-path.md` başına bir satır (etkileşimli giriş) + `docs/00-getting-started.md` B5 adımında bir satır (kalan 8 script → 9) + `tests/` 226 standart kütüphane testi + 40 komut değişmedi (28 temel + 12 ileri düzey) + 12 script dosyası |
| **V17** | ✅ Yayında (2026-11-07) | Tam Portekizce ve Arapça README'ler (Brezilya Portekizcesiyle yeni `README_PT.md` ve RTL düzenli Arapça `README_AR.md`; ikisi de eksiksiz çevrildi ve README_EN.md ile uyumlu: aynı bölümler, tablolar, komutlar, script adları, dosya adları, sürüm ve rakamlar; tüm örnek şirketler/fiyatlar/iletişim bilgileri kurgusaldır, 【示例】 ile ve sample.example ayrılmış alan adıyla işaretlidir) + `tests/` 167 standart kütüphane testi + 40 komut değişmedi (28 temel + 12 ileri düzey) + 10 script dosyası |
| **V16** | ✅ Yayında (2026-11-07) | Hatırlatma kütüphanesi (`scripts/nudge.py`: D3/D7/D14/D30 × teklif verildi/numune gönderildi/pazarlıkta, toplam 12 taslak, kısa WhatsApp sürümü + uzun e-posta sürümü, önce İngilizce ve her taslağın ardından Çince çevirisi; ton merdiveni — D3 hafif hatırlatma, D7 gelişmeyi sorma, D14 yüz kurtaran üç seçenek (daha düşük fiyat / farklı özellik / daha uzun ödeme vadesi), D30 kapıyı açık bırakan son not; 0. gün teklifin/numunenin/fiyat görüşmesinin yapıldığı gündür, followup_plan'ın ilk temas ritminden farklı bir başlangıç noktası, bir yazışma yalnızca tek bir hattı izler; `--channel whatsapp/email/both` / `--format json` / `--out`) + `docs/nudge.md` (kullanım + followup_plan ile nasıl örtüştüğü + birebir yapıştırılmış 2 gerçek çıktı) + `docs/00-getting-started.md` içinde bir satır (script listesi 6 → 7) + `tests/` 152 standart kütüphane testi + 40 komut değişmedi (28 temel + 12 ileri düzey) + 10 script dosyası |
| **V15** | ✅ Yayında (2026-11-07) | Fuar takibi (`scripts/trade_show.py`: fuarda toplanan katılımcılar ilgi düzeyine göre sıralanarak 24 saatlik takip planına dönüşür — 2 saatte teşekkür + materyaller, 12 saatte teklif girişi, 24 saatte arama/WhatsApp takibi; tek tek `--add` + toplu `--csv`, `--format json` / `--out`; ilk temas taslağı outreach_gen T0/T1/T2 şablonunu izler) + `docs/trade-show.md` (kullanım + birebir yapıştırılmış 1 gerçek çıktı) + `examples/trade_show_example.csv` (her ilgi düzeyinden bir tane olmak üzere 3 örnek katılımcı) + `docs/00-getting-started.md` ve `docs/02-find-leads.md` içinde birer satır (fuardan sonra potansiyel müşterilerle ne yapılacağı) + `tests/` 127 standart kütüphane testi + 40 komut değişmedi (28 temel + 12 ileri düzey) + 9 script dosyası |
| **V14** | ✅ Yayında (2026-11-07) | Varış maliyeti hesabı (`scripts/landed_cost.py`: FOB + navlun + sigorta → CIF; buna gümrük vergisi + varış limanı masrafları → DDP; birim maliyet + toplamlar + satış fiyatı verildiğinde kâr payı; `--qty` / `--format json` / `--audience client`) + `docs/landed-cost.md` (kullanım + formül tablosu + birebir yapıştırılmış 2 gerçek çıktı) + `docs/00-getting-started.md` ve `docs/06-quote.md` içinde birer satır (önce quote_engine ile FOB/CIF teklifi verin, sonra landed_cost ile tam varış maliyetini hesaplayın) + `tests/` 97 standart kütüphane testi + 40 komut değişmedi (28 temel + 12 ileri düzey) + 8 script dosyası |
| **V12** | ✅ Yayında (2026-11-07) | Lastik sektörü paketi (`scripts/tire_pack.py`: ebat + pazar → GCC sertifika maddeleri + varış limanı gümrükleme belgeleri + pazar notları; 4 TBR ebadı × 8 pazar) + `docs/tire-pack.md` (kullanım + birebir yapıştırılmış 2 gerçek çıktı) + `docs/00-getting-started.md` script listesi güncellendi + `tests/` 68 standart kütüphane testi + 40 komut (28 temel + 12 ileri düzey) + 7 script dosyası |
| **V11** | ✅ Yayında (2026-11-07) | Firma araştırma ajanı (`scripts/due_diligence.py`: L1/L2/L3 + A/B/C derecesi + kırmızı bayrak kontrol listesi + müşteri görünümü + JSON çıktısı) + `docs/03-due-diligence.md` 13. bölüm (birebir yapıştırılmış gerçek çıktı) + P03-5 komutu + `tests/` 52 standart kütüphane testi + 40 komut (28 temel + 12 ileri düzey) + 6 script dosyası |
| **V10** | ✅ Yayında (2026-11-07) | 6 ileri düzey modül (08 bağımsız site / 09 sosyal medya matrisi / 10 fuarlar / 11 lojistik ve ödeme / 12 risk ve uyum / 13 kilit müşteriler) + 3 öğrenme yolu + sorun giderme ve katkıcı iş akışı + sağlamlaştırılmış teklif motoru (müşteri görünümü izolasyonu, sınır kontrolleri) + `tests/` 30 standart kütüphane testi + 39 komut (27 temel + 12 ileri düzey) + Python ile uyumlu tarayıcı demosu puanlaması |
| **v0.1.5** | Yayınlandı | Kurulum gerektirmeyen tarayıcı demosu (index.html) + v0.2 teklif motoru alfa sürümü (quote_engine.py) + marka manifestosu (MANIFESTO) + lansman/tanıtım kontrol listesi (GITHUB_LAUNCH) + Fast Path + satış örneği |
| **v0.1** | Yayınlandı | 7 aşama dokümanı, 4 standart kütüphane iş scripti, 27 komut, iki dilli README |
| **v0.2** | ✅ Yayında (alfa) | **Yapay zekâ teklif motoru**: `scripts/quote_engine.py` kullanımda — maliyetleri + pazarı + rakip çıpa fiyatını girin → FOB/CIF aralığı + üç basamaklı indirim merdiveni (her basamak karşılığında bir şey kazandırmalı); müşteri görünümü izolasyonu ve sınır kontrolleri sağlamlaştırıldı (bkz. `tests/test_quote_engine.py`) |
| **Sonraki sürüm** | Belirlenecek | Sonraki yön belirlenecek (etkileşimli 7 günlük hızlı yol V19'da yayına girdi) |
| **Uzun vade** | — | Sektör paketleri (lastik, yapı malzemeleri, makine, hırdavat); Fransızca/Rusça ilk temas metni (İspanyolca, Portekizce ve Arapça V13'te geldi); kimliksizleştirilmiş açık potansiyel müşteri veri setleri; otomatik rakip çıpa fiyatlandırması için teklif motorunun gümrük verilerine bağlanması |

V20 sonraki sürümü beklemiyor: 10 sağlamlaştırma turu şimdiden kullanıma hazır (hatalı CSV'ler traceback yerine sade dilde hata veriyor, her çalışma bir iz satırı yazıyor, ortak yardımcılar tek yerde). Sonraki sürümü beklemenize gerek yok — scriptler zaten depoda ve 586 testin hepsi yeşil.

---

## Katkı

Buradaki eksik dokümanlar değil. Eksik olan, **ülkeye özgü saha bilgisi.** Orta Doğu'ya ilk lastik siparişinin nasıl gittiğini biliyorum. Ekvador'da yapı malzemesi dağıtımının nasıl işlediğini ya da Nijerya gümrüğünün gerçekte hangi belgeleri istediğini hiç bilmiyorum. Bunu ancak orada satış yapanlar doldurabilir.

En kolayından başlayarak üç yol:

1. **Bir şeyi düzeltin.** Yazım hatası, eskimiş bir bilgi, lapa gibi okunan bir kural. Bir issue açın. Tek bir cümle bile sessizlikten iyidir. Şablon üç şey sorar: hangi satırda koptunuz, hangi rakamın kaynağı yok, hangi kural sizin sektörünüzde geçerli değil.
2. **Bir aşamayı çevirin.** İspanyolca, Arapça, Portekizce, Rusça, Fransızca, Vietnamca — gerçekten hangi dili konuşuyorsanız. Altı bölümlü yapıyı koruyun, dili değiştirin, terimleri [GLOSSARY.md](GLOSSARY.md) ile eşleştirin.
3. **Kendi ülkenizi veya sektörünüzü ekleyin.** Eksik olan parça bu. Yapılması gerektiğini düşündüğünüzü değil, yaptığınızı yazın. Alan adları, belge adları, kanalın nasıl kurulduğu, insanların nasıl ödediği ve neden ödemeyi reddettikleri.

Kod katkısı da olur, tek bir kesin kuralla: **Python 3.10+, yalnızca standart kütüphane.** Gerekçesi [CONTRIBUTING.md](CONTRIBUTING.md) içinde.

---

## Geliştiriciler için: kurcalanabilir ve hiç bağımlılığı yok

On dört iş scriptinin tamamı (`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine` / `due_diligence` / `tire_pack` / `landed_cost` / `trade_show` / `nudge` / `anchor_price` / `fast_path` / `market_rules` / `daily_video_list` / `fulfillment_checklist`, artı gizlilik koruyucu `check_private_data.py`) yalnızca standart kütüphane kullanır. `pip install` yok. Fork'layın, değiştirin, kendi işlerinize ekleyin:

- Ağırlıklar size yanlış mı geliyor? `lead_score.py` dosyasının başında dört sabit var (`CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W`). Toplam yine 100 ile sınırlı.
- Kendi gümrük verileriniz mi var? Başlığı eşleştirin (`company,country,product,source,email,phone,years,contact,note`) ve verin.
- Kendi aracınızın içinde mi kullanmak istiyorsunuz? Her script temiz şekilde import edilir. `score_lead()`, `render()`, `plan_followups()`, `build_quote()` sözlük ve liste döndüren saf fonksiyonlardır. Ağ yok, dosya yazma yok.
- CI her PR'da `py_compile` artı test paketini (Python 3.10–3.13) artı bir gizlilik kapısını çalıştırır; böylece hatalı bir düzenleme gizlice içeri sızamaz.

> Buradaki tercih: **zekice olandan çok doğrulanabilir olan.** Sözüme güvenmeyin: `python scripts/lead_score.py examples/leads_example.csv` komutunu çalıştırın ve çıkanı okuyun.

---

## Sizi yanlış bir yoldan kurtardıysa

Yıldız verin. Sağ üst köşede. Tüm istediğimiz bu. Altı ay sonra adını unuttuğunuzda ve gece 11'de takip planına ihtiyaç duyduğunuzda bu depoyu yeniden bulmanın yolu da bu.

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[Star History grafiğinin tamamını görüntüleyin](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Çeviriler

README 12 dilde mevcut; web sitesinin arayüzü de öyle. Referans metin İngilizcedir.

- [中文](README.md) (Çince, tam sürüm)
- [English](README_EN.md) (İngilizce, tam sürüm — referans metin)
- [Español](README_ES.md) (İspanyolca, başlangıç sürümü, gözden geçirecek kişiler aranıyor)
- [Português](README_PT.md) (Brezilya Portekizcesi, tam sürüm)
- [Français](README_FR.md) (Fransızca, tam sürüm)
- [العربية](README_AR.md) (Arapça, tam sürüm, RTL)
- [Русский](README_RU.md) (Rusça, tam sürüm)
- [Deutsch](README_DE.md) (Almanca, tam sürüm)
- [日本語](README_JA.md) (Japonca, tam sürüm)
- [한국어](README_KO.md) (Korece, tam sürüm)
- [Türkçe](README_TR.md) (Türkçe, tam sürüm — bu sayfa)
- [Bahasa Indonesia](README_ID.md) (Endonezce, tam sürüm)

`docs/` içindeki aşama dokümanları hâlâ yalnızca Çince. Akıcı konuştuğunuz dilde istediğiniz aşamayı çevirin; altı bölümlü yapıyı koruyun ve terimleri [GLOSSARY.md](GLOSSARY.md) ile uyumlu hale getirin. Bir README'yi gözden geçirebilecek anadil konuşucularını da memnuniyetle bekliyoruz. Bkz. [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Lisans

[MIT](LICENSE) © 2026 zero-to-trade contributors

Kullanın, değiştirin, onunla satış yapın. Atıf satırını koruyun. Tek bir uyarı: Bunların hiçbiri anlaşma yapacağınızı garanti etmez. Garanti ettiği şey, bir sonraki adımı bilmediğiniz için olduğunuz yerde saplanıp kalmayacağınızdır.

---

## Sorular ve katkılar

**Bir issue açın: https://github.com/6hn68/zero-to-trade/issues**

Burada yanlış bir şey mi var? Söyleyin; bu da bir katkı sayılır. Bu deponun adını bile duymadığı bir pazara mı satış yapıyorsunuz? İşte gerçekten görmek istediğim PR bu. Yöntemin tamamının hatalı olduğunu mu düşünüyorsunuz? Bir issue'da benimle tartışın; yanılıyorsam bunu yüksek sesle duymayı tercih ederim.

Yazar biyografisi yok; bilerek. **Sizi ikna eden, kimin yazdığı değil, içerik olmalı.** Bana ulaşmanız gerekirse: bir issue'da bakımcıyı @ ile etiketleyin ya da web sitesinin altındaki form üzerinden mesaj bırakın. Her iki yol da yazara ulaşır.
