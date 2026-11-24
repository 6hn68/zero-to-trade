# zero-to-trade

[中文](README.md) · [English](README_EN.md) · [Español](README_ES.md) · [Português](README_PT.md) · [Français](README_FR.md) · [العربية](README_AR.md) · [Русский](README_RU.md) · [Deutsch](README_DE.md) · [日本語](README_JA.md) · [한국어](README_KO.md) · [Türkçe](README_TR.md) · **Bahasa Indonesia**

![CI](https://github.com/6hn68/zero-to-trade/actions/workflows/ci.yml/badge.svg) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.10%2B-306998)

**Tujuh tahap, dari "negara mana yang harus saya pilih" sampai "uangnya sudah masuk." Ditambah lima belas skrip Python yang mengerjakan bagian membosankan, dan sebuah situs web dengan empat alat yang langsung berjalan di browser Anda. Tanpa perlu pengalaman. Justru itu intinya.**

> Anda mengirim 200 email dingin dan tidak ada satu pun balasan. Masalahnya bukan bahasa Inggris Anda. Masalahnya urutan kerja Anda.
>
> Repo ini mengubah "mulai ekspor" menjadi sesuatu yang benar-benar bisa dikerjakan: situs mana yang dibuka sore ini, apa yang diketik di sana, dan hasil seperti apa yang berarti Anda lolos.

> Satu aturan yang mendasari semuanya di sini: **AI yang mengerjakan bagian berat, Anda yang mengambil keputusan.**

Tanpa kursus yang harus dibeli. Tanpa paket berbayar. Tanpa harus menyerahkan email. Berlisensi MIT, V20.

> PR sangat diterima, terutama dari Anda yang berjualan ke pasar yang belum pernah disentuh repo ini. Lihat [CONTRIBUTING.md](CONTRIBUTING.md).

## Demo 7 langkah: kelompokkan daftar nyata dan tulis penjangkauan pertama Anda dalam 2 menit

Tidak perlu membaca dokumentasi dulu. Tujuh langkah, masing-masing satu baris dan satu perintah yang tinggal disalin — sekitar 2 menit dari awal sampai akhir. Ketujuh perintah di bawah ini benar-benar dijalankan di repo ini (2026-11-22, Python 3.x, hanya pustaka standar). Data contohnya fiktif; nama perusahaan diberi awalan 【示例】 ("contoh").

| Langkah | Dalam satu baris | Perintah (salin-tempel) |
|---|---|---|
| 1 Siapkan daftar | Salin contoh ke file Anda sendiri; prospek asli Anda hanya masuk ke salinan ini | `cp examples/leads_example.csv my_leads.csv` |
| 2 Kelompokkan | 10 prospek diurutkan ke T0–T3; hubungi 2 di antaranya hari ini | `python scripts/lead_score.py my_leads.csv` |
| 3 Periksa T0 | Pastikan T0 bukan perusahaan cangkang sebelum Anda menulis; apa pun yang tidak Anda berikan kembali dengan tanda "perlu diverifikasi" | `python scripts/due_diligence.py --company "【示例】海湾轮胎贸易"` |
| 4 Tulis sentuhan pertama | Draf penjangkauan untuk tingkat T0, bahasa Inggris untuk dikirim, bahasa Mandarin untuk Anda periksa sendiri | `python scripts/outreach_gen.py my_leads.csv --tier T0` |
| 5 Rencanakan tindak lanjut | Ritme D0/D2/D5: 3 sentuhan dalam 6 hari, berhenti setelah diam yang ketiga | `python scripts/followup_plan.py --tier T0 --start 2026-11-22 --csv my_leads.csv` |
| 6 Beri penawaran saat mereka membalas | Biaya + ongkos kirim + margin → kisaran FOB/CIF + tangga konsesi tiga langkah | `python scripts/quote_engine.py --cost 28 --freight 6 --margin 15` |
| 7 Ingatkan saat mereka diam | 7 hari setelah penawaran tanpa balasan, tanyakan perkembangannya — tegas, bukan putus asa | `python scripts/nudge.py --day D7 --scenario quoted` |

Setelah langkah 4, Anda memegang email sentuhan pertama yang benar-benar bisa dikirim; setelah langkah 5, Anda tahu apa yang harus dilakukan setiap hari selama 6 hari ke depan.

Tidak punya Python? Buka situs webnya, [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/) (atau klik dua kali [`index.html`](index.html) di salinan lokal). Ada empat alat yang berjalan di browser — penilaian prospek, penjangkauan, rencana tindak lanjut, dan penawaran — dengan aturan yang sama seperti skripnya, dan antarmukanya tersedia dalam 12 bahasa (menu kanan atas). Muat daftar contoh → nilai dan temukan T0 Anda → buat pesan sentuhan pertama lalu salin → ganti placeholder `[ ]` dengan nama, perusahaan, dan WhatsApp Anda sendiri → rencanakan tindak lanjut D0/D2/D5 → beri penawaran saat mereka membalas. Tidak ada yang diunggah: daftar Anda tidak pernah keluar dari browser. Teks sentuhan pertama di situs web tersedia dalam bahasa Inggris dengan acuan bahasa Mandarin; untuk teks bahasa Spanyol, Portugis, atau Arab, gunakan `outreach_gen.py --lang es/pt/ar`.

---

## Apa yang sebenarnya diperbaiki

Cari di Google "bagaimana cara mulai ekspor." Yang Anda dapat: kisah sukses satu orang, dua ratus artikel SEO, cuplikan gratis dari kursus berbayar, dan thumbnail YouTube yang menjanjikan uang cepat. Anda membaca semuanya, merasa sudah paham, lalu keesokan paginya Anda menatap situs data bea cukai tanpa tahu apa yang harus diisi di kolom pertama.

Itu bukan kekurangan informasi. Itu informasi dalam bentuk yang salah: dipotong-potong, ditulis dari sudut pandang pemenang, dan berhenti tepat sebelum bagian di mana Anda harus melakukan sesuatu.

Begini cara kebanyakan tutorial membahasnya. *"Anda sebaiknya melakukan riset latar belakang pelanggan."* Lalu: *"Riset latar belakang itu penting."* Lalu tidak ada apa-apa. Anda tetap tidak tahu kolom mana, situs mana, seperti apa tanda bahaya itu, atau kapan pemeriksaan Anda sudah cukup.

Repo ini melakukan kebalikannya: **ambil satu tugas dan terus pecah sampai menjadi tindakan.**

| Kata tutorial | Kata repo ini |
|---|---|
| "Lakukan riset latar belakang" | Saringan L1, tiga cek: apakah situsnya ada, sudah berapa lama perusahaan terdaftar, apakah akun media sosialnya aktif. Gagal satu saja, prospek itu gugur. |
| "Kualitas lebih penting daripada kuantitas" | 10 prospek dikelompokkan ke T0/T1/T2/T3, setiap tingkat punya langkah berikutnya dan anggaran waktunya sendiri. |
| "Tindak lanjuti mereka" | Hari 1, 3, 5, 7. Sudut pandang berbeda setiap kali, dan hari ke-7 diakhiri dengan keputusan: lanjut atau lepas. |
| "AI sedang mengubah perdagangan" | Lima belas skrip Python yang hanya memakai pustaka standar (empat belas skrip bisnis, salah satunya mesin penawaran, ditambah satu penjaga privasi). Jalankan `python scripts/lead_score.py examples/leads_example.csv` dan Anda mendapat pengelompokan lengkap dalam sekitar tiga puluh detik. |

Informasinya sama. **Tingkat kerinciannya** yang berbeda. Hanya itu bedanya. Setiap klaim di sini harus lolos satu pertanyaan: apa yang saya buka sore ini, dan apa yang saya ketik?

Jadi bukan, ini bukan motivasi. Ini daftar periksa dan lima belas file skrip (empat belas skrip bisnis + satu penjaga privasi).

---

## Tujuh tahap

Satu rantai dari awal sampai akhir: dimulai dengan memilih negara, diakhiri dengan uang di rekening. Satu dokumen per tahap, dan setiap dokumen diakhiri dengan sesuatu yang benar-benar bisa Anda pakai.

| Tahap | Apa yang Anda lakukan | Hasil |
|---|---|---|
| **01 Pilih pasar** | Nilai berdasarkan bahasa, permintaan, dan hambatan | 1 pasar pertama + 3 alasan untuk mempertahankannya |
| **02 Cari prospek** | Empat jalur: data bea cukai, media sosial, pencarian, pameran dagang | ≥20 prospek terverifikasi per hari |
| **03 Periksa pembeli** | Saringan L1 → standar L2 → pendalaman L3 | Peringkat A/B/C; penipu tersaring |
| **04 Jalin kontak** | Kelompokkan prospek T0-T3; jalankan tiga saluran pada sentuhan pertama | Daftar bertingkat + rencana tindak lanjut D0/D2/D5 (3 sentuhan dalam 6 hari) |
| **05 Bahas spesifikasi** | Permintaan kecil dulu. Harga selalu paling akhir | Spesifikasi / kuantitas / pelabuhan tujuan |
| **06 Penawaran & negosiasi** | Disiplin penawaran: setiap konsesi harus dibayar dengan sesuatu | Lembar penawaran + tangga konsesi + naskah percakapan |
| **07 Kirim pesanan** | Kontrak, produksi, inspeksi, dokumen, pembayaran, pengapalan | Siklus pengiriman tuntas + rencana pembelian ulang |

Dokumen tahap ada di `docs/`, satu file per tahap, semuanya mengikuti struktur enam bagian yang sama (lihat [CONTRIBUTING.md](CONTRIBUTING.md)): **untuk apa tahap ini → cara mengerjakannya, langkah demi langkah → kriteria lolos/gagal → kesalahan klasik → templat siap salin → prompt AI untuk tahap ini.**

**Belum pernah melakukan ini?** [`docs/00-getting-started.md`](docs/00-getting-started.md) tidak mengandaikan Anda paham git atau Python, dan membuat Anda mulai bergerak dalam sekitar 10 menit. Sedang terburu-buru? [`docs/fast-path.md`](docs/fast-path.md) adalah tujuh hari dari nol sampai balasan pertama Anda.

---

## Mulai cepat 30 detik

**Tidak mau memasang Python?** Buka situs webnya: [6hn68.github.io/zero-to-trade](https://6hn68.github.io/zero-to-trade/). Empat alat browser — penilaian prospek, penjangkauan, rencana tindak lanjut, dan penawaran — dalam 12 bahasa antarmuka. Tempel CSV, dapatkan pengelompokan T0-T3, lalu sentuhan pertama, tanggal tindak lanjut, dan penawaran. Tidak ada yang perlu dipasang, dan tidak ada yang keluar dari browser Anda.

Lima belas file skrip: empat belas skrip bisnis, salah satunya mesin penawaran, ditambah skrip penjaga privasi (`check_private_data.py`, memindai data pelanggan asli sebelum Anda commit). Hanya pustaka standar. Python 3.10+.

```bash
# 1. Kelompokkan prospek Anda. CSV masuk, T0-T3 keluar, setiap tingkat dengan langkah berikutnya.
python scripts/lead_score.py examples/leads_example.csv

# 2. Buat draf teks penjangkauan untuk satu tingkat, bahasa Inggris dan 中文 berdampingan.
python scripts/outreach_gen.py examples/leads_example.csv --tier T0

# 3. Susun rencana tindak lanjut. Tiga sentuhan, tanggal nyata.
python scripts/followup_plan.py --tier T0 --start 2026-10-08 --csv examples/leads_example.csv

# 4. Penawaran: biaya + ongkos kirim + margin -> kisaran FOB/CIF + tangga konsesi 3 langkah.
python scripts/quote_engine.py --cost 28 --freight 6 --margin 15
```

Inilah yang benar-benar dicetak oleh perintah pertama, untuk 10 prospek contoh. Skripnya mengeluarkan hasil dalam bahasa Mandarin; 【示例】 hanyalah penanda yang berarti "contoh", dan kolom terakhir diterjemahkan di sini:

| Tingkat | Perusahaan | Negara | Skor | Tindakan berikutnya |
|---|---|---|---|---|
| T0 | 【示例】海湾轮胎贸易 | Arab Saudi | 95 | kirim sentuhan pertama hari ini, jangan menunggu |
| T0 | 【示例】三角洲轮胎 | Arab Saudi | 88 | kirim sentuhan pertama hari ini, jangan menunggu |
| T1 | 【示例】阿曼蓝海 | Oman | 77 | minggu ini; siapkan drafnya hari ini |
| T1 | 【示例】半岛汽车 | Arab Saudi | 71 | minggu ini; siapkan drafnya hari ini |
| T1 | 【示例】尼罗河商贸 | Mesir | 67 | minggu ini; siapkan drafnya hari ini |
| T1 | 【示例】迪拜轮毂行 | UEA | 65 | minggu ini; siapkan drafnya hari ini |
| T1 | 【示例】利雅得汽配 | Arab Saudi | 60 | minggu ini; siapkan drafnya hari ini |
| T2 | 【示例】尼日利亚先锋 | Nigeria | 46 | kelompok dingin, cek sekali sehari |
| T3 | 【示例】黎凡特供配 | Lebanon | 20 | info belum cukup, cari dulu kontak + kebutuhannya |
| T3 | 【示例】利雅得零件店 | Arab Saudi | 10 | info belum cukup, cari dulu kontak + kebutuhannya |

Ringkasan: **T0:2 / T1:5 / T2:1 / T3:2**. Hubungi hari ini: 【示例】海湾轮胎贸易, 【示例】三角洲轮胎. Minggu ini: 【示例】阿曼蓝海, 【示例】半岛汽车, 【示例】尼罗河商贸, 【示例】迪拜轮毂行, 【示例】利雅得汽配. Biarkan dulu: 【示例】黎凡特供配, 【示例】利雅得零件店.

Header CSV:

```
company,country,product,source,email,phone,years,contact,note
```

Hanya `company` yang wajib. Sisanya boleh kosong, dan kolom kosong mendapat skor terendah. `source` paling berpengaruh: `referral` / `trade_show` / `customs` / `linkedin` / `search`.

Kelima belas skrip menerima `--help`. `lead_score.py` juga punya `--format json` serta filter `--country` / `--product`, jika Anda ingin mengalirkannya ke spreadsheet.

Skrip hanya memutuskan apa yang bisa diputuskan mesin: ada email atau tidak, ada situs web atau tidak, apakah lolos batas T0. Apakah sebuah prospek layak menyita sore Anda, itu ada di dokumentasi, dan di kepala Anda.

---

## Struktur repositori

```
zero-to-trade/
├── README.md              # Versi lengkap bahasa Mandarin
├── README_EN.md           # Versi bahasa Inggris (acuan untuk setiap terjemahan)
├── README_ES.md / README_PT.md / README_FR.md / README_AR.md / README_RU.md
├── README_DE.md / README_JA.md / README_KO.md / README_TR.md / README_ID.md
│                          # Spanyol, Portugis, Prancis, Arab (RTL), Rusia, Jerman, Jepang, Korea, Turki, Indonesia
├── index.html             # Situs web: 4 alat browser, 12 bahasa antarmuka, tanpa dependensi (GitHub Pages)
├── MANIFESTO.md           # Anonim, tanpa kursus berbayar: sikap merek
├── GITHUB_LAUNCH.md       # Daftar periksa peluncuran + promosi (Topics/About/PR/Show HN)
├── CONTRIBUTING.md        # Cara berkontribusi + konvensi dokumen dan kode
├── CHANGELOG.md           # Catatan perubahan: apa yang berubah setiap kali
├── ROADMAP.md             # Peta jalan: arah versi berikutnya
├── LICENSE                # MIT
├── docs/                  # Satu file per tahap
│   ├── 00-getting-started.md
│   ├── fast-path.md       # 7 hari dari nol sampai balasan pertama
│   ├── 01-market-selection.md
│   ├── 02-find-leads.md
│   ├── 03-due-diligence.md
│   ├── 04-outreach.md
│   ├── 05-negotiation.md
│   ├── 06-quote.md
│   ├── 07-order-delivery.md
│   └── deal-walkthrough.md # Contoh lengkap transaksi pertama yang realistis
├── scripts/               # Python siap jalan, hanya pustaka standar
│   ├── lead_score.py      # Kelompokkan prospek T0-T3
│   ├── outreach_gen.py    # Teks penjangkauan per tingkat (EN/ZH + ES/PT/AR dengan acuan bahasa Inggris, V13)
│   ├── followup_plan.py   # Rencana tindak lanjut D0/D2/D5 (3 sentuhan dalam 6 hari)
│   ├── quote_engine.py    # Mesin penawaran: kisaran FOB/CIF + tangga konsesi 3 langkah
│   ├── due_diligence.py   # V11 agen pemeriksaan latar belakang: L1/L2/L3 + peringkat A/B/C + tanda bahaya
│   ├── tire_pack.py       # V12 paket industri ban: ukuran + pasar → poin GCC + dokumen kepabeanan + catatan pasar
│   ├── landed_cost.py     # Biaya sampai tujuan, V14: FOB + ongkos kirim + asuransi → CIF, ditambah bea masuk + biaya tujuan → DDP
│   ├── trade_show.py      # Pameran dagang, V15: peserta pameran yang dikumpulkan → rencana tindak lanjut 24 jam (terima kasih dalam 2 jam, petunjuk penawaran dalam 12 jam, telepon/WhatsApp dalam 24 jam)
│   ├── nudge.py           # Pustaka pengingat, V16: D3/D7/D14/D30 × sudah ditawar/sudah kirim sampel/sedang negosiasi → versi WhatsApp singkat + versi email lebih panjang (Inggris + Mandarin)
│   ├── anchor_price.py    # Harga patokan pesaing, V18: kisaran harga pesaing dari data bea cukai + biaya Anda → tingkat CIF agresif/tengah/konservatif + daftar periksa 5 butir
│   ├── fast_path.py     # V19 jalur cepat 7 hari interaktif: --day N menampilkan tugas, --done N mencentang, --progress menghitung total (selaras dengan docs/fast-path.md)
│   ├── market_rules.py    # Aturan pasar: pasar sasaran, hambatan Turki/Brasil, pengecualian Meksiko/AS/UE
│   ├── daily_video_list.py  # Daftar harian 5 video (3 pagi, 2 sore) dengan cek ukuran, pasar, keunggulan, dan pengambilan gambar
│   ├── fulfillment_checklist.py  # Daftar periksa pemenuhan pesanan: PI → uang muka → produksi → inspeksi → pelunasan → booking → bea cukai → B/L → dokumen → purnajual, pengaman uang ketat pada uang muka/pelepasan/pengiriman
│   └── check_private_data.py  # Penjaga privasi: memindai data pelanggan asli sebelum commit
├── examples/
│   ├── leads_example.csv  # Data contoh, bisa langsung dijalankan
│   ├── leads_example_lighting.csv  # Contoh non-ban: 8 prospek lampu LED
│   └── trade_show_example.csv  # Contoh peserta pameran, satu per tingkat minat
├── tests/                 # 586 tes pustaka standar
├── prompts/
│   └── AI_PROMPTS.md      # 40 prompt siap salin (28 inti + 12 lanjutan), dikelompokkan per tahap
└── assets/                # Tangkapan layar, diagram
```

---

## Mengapa skrip, bukan sekadar dokumen metode

Kebanyakan repo "AI untuk bisnis" melakukan hal yang sama: ambil metodologinya, tempel ke prompt, rilis. Repo ini berjalan terbalik. **Disiplin dulu, alat belakangan.**

Alasannya: **pandai membuat prompt tidak sama dengan pandai berdagang.** Taruhan saya, Anda tidak kekurangan kata-kata. Anda kekurangan cara untuk memutuskan. Jadi:

- **Aturan adalah produknya di sini.** T0 mendapat email hari ini. T3 disimpan di laci selama tiga bulan. Konsesi yang tidak dibayar dengan apa pun adalah hadiah, bukan negosiasi. Tidak ada model yang boleh mengambil keputusan itu untuk Anda.
- **Volume diserahkan ke AI.** Menyaring 8 prospek sekaligus, menyusun tiga level riset latar belakang untuk 50 perusahaan, membuat variasi tindak lanjut untuk tujuh hari. Kerja berjam-jam, nyaris tanpa pertimbangan di dalamnya.
- **Apa pun yang berulang dijadikan skrip.** Kalau pengelompokan hanya berdasarkan perasaan, itu bukan standar. Jadi ia menjadi skrip di bawah 200 baris tanpa dependensi, dan dua orang yang menjalankannya akan mendapat jawaban yang sama.

Di mana garisnya: **bisa ditulis sebagai `if/else`? Masuk skrip. Butuh pertimbangan untung-rugi? Masuk dokumentasi. Harus terdengar seperti ditulis manusia? Masuk `prompts/`.**

Tanpa pandas, tanpa OpenAI SDK, dan itu disengaja. Penyiapan lingkungan adalah titik di mana pemula menyerah. Orang yang baru di ekspor akan kehilangan lebih banyak jam untuk `pip install` daripada untuk mencari pelanggan, dan itu tempat yang konyol untuk kehilangan mereka.

---

## Peta jalan

> Peta jalan lengkap: [ROADMAP.md](ROADMAP.md); riwayat perubahan: [CHANGELOG.md](CHANGELOG.md).

| Versi | Status | Isi |
|---|---|---|
| **V13** | ✅ Rampung (2026-11-07) | Penjangkauan multibahasa (`scripts/outreach_gen.py --lang es/pt/ar`: teks Spanyol/Portugis/Arab + teks asli bahasa Inggris setelah setiap draf; templat mencerminkan T0/T1/T2 bahasa Inggris satu per satu, satu dict inline di dalam skrip) + bagian baru di `docs/04-outreach.md` (cara pakai + 3 keluaran nyata ditempel apa adanya) + `tests/` 80 tes pustaka standar + 40 prompt tidak berubah (28 inti + 12 lanjutan) + 7 file skrip |
| **V18** | ✅ Rampung (2026-11-07) | Harga patokan pesaing (`scripts/anchor_price.py`: kisaran harga pesaing dari data bea cukai + biaya Anda → tingkat CIF agresif/tengah/konservatif, masing-masing dengan ruang laba, margin, padanan FOB, markup tersirat, dan kapan dipakai; daftar periksa 5 butir — biaya, ongkos kirim, kurs, syarat pembayaran, masa berlaku — sebelum memberi penawaran, butir yang belum dicek ditandai; peringatan di bawah biaya “di bawah biaya, jangan ambil pesanan, negosiasikan volume untuk harga dulu”; nilai tengah yang hilang diperkirakan sebagai (rendah + tinggi) / 2 dan ditandai sebagai perkiraan; `--format json` / `--audience client`) + `docs/anchor-price.md` (cara pakai + panduan patokan + 2 keluaran nyata ditempel apa adanya) + satu baris di `docs/06-quote.md` (tetapkan patokan sebelum memberi penawaran) + `tests/` 187 tes pustaka standar + 40 prompt tidak berubah (28 inti + 12 lanjutan) + 11 file skrip |
| **V20** | ✅ Saat ini (2026-11-14) | Penggabungan inkremen lokal + 10 putaran penguatan: titik masuk CLI terpadu (pesan galat dalam bahasa sederhana, kode keluar diseragamkan) + tes lebih kuat (mode satu pesan, alias `--start-date`, log eksekusi) + angka dokumentasi diselaraskan + contoh non-ban (8 prospek lampu LED) + halaman demo disinkronkan dengan V19 + pesan galat ramah untuk CSV bermasalah (kolom hilang / file kosong / tanda kutip tak tertutup tidak lagi menampilkan traceback) + penyelarasan prompt (perintah tindak lanjut P04-4 mendapat `--avoid-weekend`, jendela P10-2 diseragamkan menjadi 48 jam) + pelacakan eksekusi diterapkan (`logs/trace-YYYY-MM-DD.jsonl`, satu baris per eksekusi tiga skrip inti) + perapian kode (helper bersama disimpan di satu tempat, bersih −151 baris; dua helper mati dihapus) + `tests/` 586 tes pustaka standar + 40 prompt tidak berubah (28 inti + 12 lanjutan) + 15 file skrip |
| **V19** | ✅ Rampung (2026-11-07) | Jalur cepat 7 hari interaktif (`scripts/fast_path.py`: `--day N` menampilkan tugas hari itu — nama tugas + apa yang dihasilkan + skrip/dokumen yang dipakai; `--done N` mencentang satu hari dengan stempel waktu, ditulis ke file JSON `--state`, centang ulang akan memberi tahu sudah dicentang dan tidak dicatat dua kali; `--progress` menghitung total selesai / tersisa / terlambat (terlambat = tanggal rencana lebih awal dari hari ini dan belum dicentang, tanggal rencana = hari ke-1 `--start` + (N-1) hari; tanpa `--start` tidak ada hitungan terlambat, dan itu dinyatakan dengan jelas); `--list` menampilkan ketujuh hari; tugas diselaraskan baris demi baris dengan `docs/fast-path.md`, tanpa daftar kedua yang dikarang; `--help` memuat contoh nyata, hari atau tanggal yang salah mendapat pesan galat dalam bahasa sederhana) + `docs/fast-path-interactive.md` (cara pakai + format file state + aturan terlambat + ikhtisar 7 hari + 2 keluaran nyata ditempel apa adanya) + satu baris di bagian atas `docs/fast-path.md` (pintu masuk interaktif) + satu baris di langkah B5 `docs/00-getting-started.md` (8 skrip tersisa → 9) + `tests/` 226 tes pustaka standar + 40 prompt tidak berubah (28 inti + 12 lanjutan) + 12 file skrip |
| **V17** | ✅ Rampung (2026-11-07) | README lengkap bahasa Portugis dan Arab (`README_PT.md` baru dalam bahasa Portugis Brasil dan `README_AR.md` dalam bahasa Arab dengan tata letak RTL, keduanya diterjemahkan penuh dan selaras dengan README_EN.md: bagian, tabel, perintah, nama skrip, nama file, versi, dan angka yang sama; semua perusahaan/harga/kontak contoh fiktif, ditandai 【示例】 dengan domain cadangan sample.example) + `tests/` 167 tes pustaka standar + 40 prompt tidak berubah (28 inti + 12 lanjutan) + 10 file skrip |
| **V16** | ✅ Rampung (2026-11-07) | Pustaka pengingat (`scripts/nudge.py`: D3/D7/D14/D30 × sudah ditawar/sudah kirim sampel/sedang negosiasi, total 12 draf, versi WhatsApp singkat + versi email lebih panjang, bahasa Inggris dulu dengan terjemahan Mandarin setelah setiap draf; tangga nada — D3 pengingat ringan, D7 tanyakan perkembangan, D14 tiga pilihan untuk menjaga muka (harga lebih rendah / spesifikasi lain / syarat pembayaran lebih panjang), D30 catatan terakhir yang tetap membuka pintu; Hari 0 adalah hari penawaran/sampel/pembahasan harga dikirim, patokan yang berbeda dari ritme sentuhan pertama followup_plan, satu utas hanya mengikuti satu jalur; `--channel whatsapp/email/both` / `--format json` / `--out`) + `docs/nudge.md` (cara pakai + keselarasannya dengan followup_plan + 2 keluaran nyata ditempel apa adanya) + satu baris di `docs/00-getting-started.md` (daftar skrip 6 → 7) + `tests/` 152 tes pustaka standar + 40 prompt tidak berubah (28 inti + 12 lanjutan) + 10 file skrip |
| **V15** | ✅ Rampung (2026-11-07) | Tindak lanjut pameran dagang (`scripts/trade_show.py`: peserta pameran yang dikumpulkan diurutkan berdasarkan minat menjadi rencana tindak lanjut 24 jam — terima kasih + materi dalam 2 jam, petunjuk penawaran dalam 12 jam, telepon/WhatsApp dalam 24 jam; `--add` satu per satu + `--csv` sekaligus, `--format json` / `--out`; draf sentuhan pertama mengikuti templat T0/T1/T2 outreach_gen) + `docs/trade-show.md` (cara pakai + 1 keluaran nyata ditempel apa adanya) + `examples/trade_show_example.csv` (3 contoh peserta pameran, satu per tingkat minat) + masing-masing satu baris di `docs/00-getting-started.md` dan `docs/02-find-leads.md` (apa yang dilakukan dengan prospek setelah pameran) + `tests/` 127 tes pustaka standar + 40 prompt tidak berubah (28 inti + 12 lanjutan) + 9 file skrip |
| **V14** | ✅ Rampung (2026-11-07) | Estimasi biaya sampai tujuan (`scripts/landed_cost.py`: FOB + ongkos kirim + asuransi → CIF, ditambah bea masuk + biaya pelabuhan tujuan → DDP; biaya per unit + total + ruang laba bila harga jual diberikan; `--qty` / `--format json` / `--audience client`) + `docs/landed-cost.md` (cara pakai + tabel rumus + 2 keluaran nyata ditempel apa adanya) + masing-masing satu baris di `docs/00-getting-started.md` dan `docs/06-quote.md` (beri penawaran FOB/CIF dengan quote_engine dulu, lalu hitung biaya sampai tujuan lengkap dengan landed_cost) + `tests/` 97 tes pustaka standar + 40 prompt tidak berubah (28 inti + 12 lanjutan) + 8 file skrip |
| **V12** | ✅ Rampung (2026-11-07) | Paket industri ban (`scripts/tire_pack.py`: ukuran + pasar → poin sertifikasi GCC + dokumen kepabeanan pelabuhan tujuan + catatan pasar; 4 ukuran TBR × 8 pasar) + `docs/tire-pack.md` (cara pakai + 2 keluaran nyata ditempel apa adanya) + daftar skrip di `docs/00-getting-started.md` diperbarui + `tests/` 68 tes pustaka standar + 40 prompt (28 inti + 12 lanjutan) + 7 file skrip |
| **V11** | ✅ Rampung (2026-11-07) | Agen pemeriksaan latar belakang (`scripts/due_diligence.py`: L1/L2/L3 + peringkat A/B/C + daftar periksa tanda bahaya + tampilan klien + keluaran JSON) + bagian 13 `docs/03-due-diligence.md` (keluaran nyata ditempel apa adanya) + prompt P03-5 + `tests/` 52 tes pustaka standar + 40 prompt (28 inti + 12 lanjutan) + 6 file skrip |
| **V10** | ✅ Rampung (2026-11-07) | 6 modul lanjutan (08 situs mandiri / 09 matriks media sosial / 10 pameran dagang / 11 logistik & pembayaran / 12 risiko & kepatuhan / 13 akun utama) + 3 jalur belajar + pemecahan masalah & alur kerja kontributor + mesin penawaran diperkuat (isolasi tampilan klien, cek batas) + `tests/` 30 tes pustaka standar + 39 prompt (27 inti + 12 lanjutan) + penilaian demo browser diselaraskan dengan Python |
| **v0.1.5** | Dirilis | Demo browser tanpa instalasi (index.html) + mesin penawaran alfa v0.2 (quote_engine.py) + manifesto merek (MANIFESTO) + daftar periksa peluncuran/promosi (GITHUB_LAUNCH) + Fast Path + contoh lengkap transaksi |
| **v0.1** | Dirilis | 7 dokumen tahap, 4 skrip bisnis pustaka standar, 27 prompt, README dwibahasa |
| **v0.2** | ✅ Rampung (alfa) | **Mesin penawaran AI**: `scripts/quote_engine.py` sudah aktif — masukkan biaya + pasar + harga patokan pesaing → kisaran FOB/CIF + tangga konsesi tiga langkah (setiap langkah harus dibayar dengan sesuatu); isolasi tampilan klien dan cek batas diperkuat (lihat `tests/test_quote_engine.py`) |
| **Versi berikutnya** | Belum diputuskan | Arah berikutnya belum diputuskan (jalur cepat 7 hari interaktif rampung di V19) |
| **Jangka panjang** | — | Paket industri (ban, bahan bangunan, mesin, perkakas); teks penjangkauan dalam bahasa Prancis/Rusia (Spanyol, Portugis, dan Arab rampung di V13); dataset prospek publik yang dianonimkan; menghubungkan mesin penawaran ke data bea cukai untuk harga patokan pesaing otomatis |

V20 tidak menunggu versi berikutnya: 10 putaran penguatan sudah bisa dipakai sekarang (CSV bermasalah mendapat pesan galat dalam bahasa sederhana alih-alih traceback, setiap eksekusi menulis satu baris jejak, helper bersama ada di satu tempat). Tidak perlu menunggu versi berikutnya — skripnya sudah ada di repo, dengan 586 tes yang semuanya hijau.

---

## Berkontribusi

Yang kurang di sini bukan dokumentasi. Yang kurang adalah **detail lapangan per negara.** Saya tahu bagaimana pesanan ban pertama ke Timur Tengah berjalan. Saya sama sekali tidak tahu bagaimana distribusi bahan bangunan di Ekuador, atau dokumen apa yang sebenarnya diminta bea cukai Nigeria. Hanya orang yang berjualan di sana yang bisa mengisinya.

Tiga cara untuk ikut, mulai dari yang paling ringan:

1. **Perbaiki sesuatu.** Salah ketik, fakta usang, aturan yang terbaca tidak jelas. Buka issue. Satu kalimat lebih baik daripada diam. Templatnya menanyakan tiga hal: baris mana yang membuat Anda bingung, angka mana yang tidak ada sumbernya, aturan mana yang tidak berlaku di industri Anda.
2. **Terjemahkan satu tahap.** Spanyol, Arab, Portugis, Rusia, Prancis, Vietnam — bahasa apa pun yang benar-benar Anda kuasai. Pertahankan struktur enam bagian, ganti bahasanya, cocokkan istilah dengan [GLOSSARY.md](GLOSSARY.md).
3. **Tambahkan negara atau industri Anda.** Inilah bagian yang hilang. Tulis apa yang sudah Anda kerjakan, bukan apa yang menurut Anda seharusnya dikerjakan. Nama kolom, nama dokumen, bagaimana saluran dibangun, bagaimana orang membayar, dan mengapa mereka menolak membayar.

Kode juga diterima, dengan satu aturan tegas: **Python 3.10+, hanya pustaka standar.** Alasannya ada di [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Untuk pengembang: mudah dioprek, dan tanpa dependensi

Keempat belas skrip bisnis (`lead_score` / `outreach_gen` / `followup_plan` / `quote_engine` / `due_diligence` / `tire_pack` / `landed_cost` / `trade_show` / `nudge` / `anchor_price` / `fast_path` / `market_rules` / `daily_video_list` / `fulfillment_checklist`, ditambah penjaga privasi `check_private_data.py`) hanya memakai pustaka standar. Tidak ada `pip install`. Fork, ubah, masukkan ke proyek Anda sendiri:

- Bobotnya terasa kurang pas? Ada empat konstanta di bagian atas `lead_score.py` (`CONTACT_W / SOURCE_W / SIGNAL_W / MATURITY_W`). Batasnya tetap 100.
- Punya data bea cukai sendiri? Samakan header-nya (`company,country,product,source,email,phone,years,contact,note`) lalu masukkan.
- Ingin memakainya di dalam alat Anda sendiri? Setiap skrip bisa diimpor dengan bersih. `score_lead()`, `render()`, `plan_followups()`, `build_quote()` adalah fungsi murni yang mengembalikan dict dan list. Tanpa jaringan, tanpa menulis file.
- CI menjalankan `py_compile` ditambah rangkaian tes (Python 3.10–3.13) ditambah gerbang privasi pada setiap PR, sehingga suntingan yang buruk tidak lolos diam-diam.

> Prinsipnya di sini: **bisa diverifikasi lebih penting daripada cerdik.** Jangan percaya begitu saja pada kata-kata saya: jalankan `python scripts/lead_score.py examples/leads_example.csv` dan baca hasilnya.

---

## Kalau ini menyelamatkan Anda dari satu langkah keliru

Beri bintang. Pojok kanan atas. Hanya itu permintaannya. Itu juga cara Anda menemukannya lagi enam bulan dari sekarang, saat Anda sudah lupa namanya dan butuh rencana tindak lanjut pukul 11 malam.

![Stars](https://img.shields.io/github/stars/6hn68/zero-to-trade?style=social) ![Last Commit](https://img.shields.io/github/last-commit/6hn68/zero-to-trade)

[Lihat grafik Star History lengkap](https://www.star-history.com/#6hn68/zero-to-trade&Date)

---

## Terjemahan

README tersedia dalam 12 bahasa, begitu pula antarmuka situs webnya. Bahasa Inggris adalah teks acuannya.

- [中文](README.md) (Mandarin, lengkap)
- [Español](README_ES.md) (Spanyol, versi awal, mencari peninjau)
- [Português](README_PT.md) (Portugis Brasil, lengkap)
- [Français](README_FR.md) (Prancis, lengkap)
- [العربية](README_AR.md) (Arab, lengkap, RTL)
- [Русский](README_RU.md) (Rusia, lengkap)
- [Deutsch](README_DE.md) (Jerman, lengkap)
- [日本語](README_JA.md) (Jepang, lengkap)
- [한국어](README_KO.md) (Korea, lengkap)
- [Türkçe](README_TR.md) (Turki, lengkap)
- [Bahasa Indonesia](README_ID.md) (versi lengkap bahasa Indonesia)

Dokumen tahap di `docs/` masih hanya tersedia dalam bahasa Mandarin. Terjemahkan tahap mana pun yang Anda kuasai; pertahankan struktur enam bagian dan selaraskan istilah dengan [GLOSSARY.md](GLOSSARY.md). Penutur asli yang bisa meninjau README juga sangat kami sambut. Lihat [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Lisensi

[MIT](LICENSE) © 2026 zero-to-trade contributors

Pakai, ubah, gunakan untuk berjualan. Pertahankan baris kreditnya. Satu catatan: tidak ada satu pun di sini yang menjamin Anda akan mendapat transaksi. Yang dijamin adalah Anda tidak akan macet hanya karena tidak tahu langkah berikutnya.

---

## Pertanyaan & kontribusi

**Buka issue: https://github.com/6hn68/zero-to-trade/issues**

Ada yang salah di sini? Katakan saja, itu sudah termasuk kontribusi. Berjualan ke pasar yang belum pernah disentuh repo ini? Itulah PR yang benar-benar saya tunggu. Menurut Anda seluruh metodenya keliru? Debat saya di issue, saya lebih suka salah secara terbuka.

Sengaja tanpa biodata penulis. **Yang seharusnya meyakinkan Anda adalah isinya, bukan siapa penulisnya.** Perlu menghubungi saya: @ maintainer di sebuah issue, atau tinggalkan pesan lewat formulir di bagian bawah situs web. Cara mana pun, pesan Anda akan sampai ke penulis.
