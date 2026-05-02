# Smart Review Alert

Smart Review Alert adalah aplikasi web analisis sentimen ulasan yang dirancang untuk membantu tim membaca sinyal pelanggan secara cepat, ringkas, dan dapat ditindaklanjuti. Aplikasi ini menggabungkan antarmuka dashboard berbasis Flask, model Machine Learning untuk klasifikasi sentimen, serta integrasi Telegram untuk mengirimkan hasil analisis secara real-time.

Proyek ini dikembangkan sebagai Proyek Utama Informatika, namun disusun dengan pendekatan yang mendekati standar produk: struktur kode lebih rapi, konfigurasi dipisahkan dari kode, aset statis siap untuk deployment, dan aplikasi dapat dijalankan lokal maupun di Vercel.

## Value Proposition

Dalam banyak layanan digital, ulasan pelanggan sering tersebar, terlambat dianalisis, atau hanya dibaca secara manual. Smart Review Alert menawarkan alur yang lebih cepat:

- Pengguna memasukkan ulasan pelanggan.
- Sistem memproses teks menggunakan model Machine Learning.
- Hasil sentimen ditampilkan langsung di dashboard.
- Notifikasi dapat dikirim ke Telegram untuk pemantauan cepat.

Dengan pola ini, aplikasi dapat menjadi fondasi awal untuk monitoring kepuasan pelanggan, early warning review negatif, dan dashboard insight layanan.

## Fitur Utama

- Dashboard analisis sentimen dengan tampilan responsif.
- Input ulasan hingga 2000 karakter.
- Pilihan model klasifikasi:
  - Support Vector Machine
  - Naive Bayes
- Hasil prediksi real-time.
- Status pengiriman Telegram pada hasil analisis.
- Login sederhana untuk prototipe.
- Konfigurasi berbasis environment variable.
- Siap deploy ke Vercel.

## Tech Stack

- Backend: Flask
- Machine Learning: scikit-learn, joblib
- Frontend: HTML, CSS, JavaScript
- Notification: Telegram Bot API
- Deployment Target: Vercel
- Runtime lokal: Python virtual environment

## Struktur Proyek

```text
.
├── app.py                  # Entry point utama Flask untuk Vercel
├── run_local.py            # Runner lokal
├── sentiment_model.py      # Loader model dan fungsi prediksi sentimen
├── telegram_bot.py         # Bot Telegram opsional untuk dijalankan terpisah
├── database.py             # Placeholder database untuk mode prototipe
├── requirements.txt        # Dependency Python
├── vercel.json             # Konfigurasi Vercel
├── .env.example            # Contoh environment variable
├── .python-version         # Versi Python untuk deployment
├── templates/              # Template HTML Flask
├── public/static/          # CSS dan JavaScript
└── model_ml/               # File model Machine Learning dan vectorizer
```

## Prasyarat

- Python 3.12 atau 3.13 untuk lokal.
- pip.
- Virtual environment.
- Akun Vercel jika ingin deploy.
- Bot Telegram jika ingin mengaktifkan notifikasi.

## Menjalankan Lokal

Jika memakai environment `myenv` yang sudah ada di proyek:

```powershell
& ".\myenv\Scripts\python.exe" ".\run_local.py"
```

Buka aplikasi di:

```text
http://127.0.0.1:5000
```

Jika ingin membuat virtual environment baru:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python run_local.py
```

## Environment Variable

Salin `.env.example` menjadi `.env` untuk konfigurasi lokal:

```powershell
copy .env.example .env
```

Daftar konfigurasi:

| Variable | Wajib | Keterangan |
| --- | --- | --- |
| `SECRET_KEY` | Ya | Secret key untuk session Flask. Gunakan nilai acak yang kuat saat production. |
| `LOGIN_PASSWORD` | Tidak | Jika diisi, aplikasi hanya menerima password ini. Jika kosong, cocok untuk mode prototipe. |
| `TELEGRAM_BOT_TOKEN` | Tidak | Token dari BotFather untuk mengirim notifikasi Telegram. |
| `TELEGRAM_CHAT_IDS` | Tidak | Satu atau beberapa chat ID, pisahkan dengan koma. |

Contoh:

```env
SECRET_KEY=isi-dengan-secret-yang-kuat
LOGIN_PASSWORD=admin123
TELEGRAM_BOT_TOKEN=123456:token-bot
TELEGRAM_CHAT_IDS=123456789,987654321
```

## Deploy ke Vercel

Proyek ini sudah disesuaikan agar dapat dideploy ke Vercel.

Langkah deploy:

1. Push repository ke GitHub.
2. Masuk ke Vercel dan pilih Import Project.
3. Pilih repository Smart Review Alert.
4. Tambahkan Environment Variables:
   - `SECRET_KEY`
   - `LOGIN_PASSWORD`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_IDS`
5. Jalankan deploy.

Vercel akan memakai `app.py` sebagai Flask application. Aset statis berada di `public/static`, sehingga dapat dilayani dengan pola deployment Vercel.

## Alur Aplikasi

1. Pengguna login ke dashboard.
2. Pengguna memasukkan teks ulasan.
3. Pengguna memilih model Machine Learning.
4. Flask menerima request `/predict`.
5. `sentiment_model.py` memuat vectorizer dan model dari `model_ml/`.
6. Sistem mengembalikan hasil `POSITIF` atau `NEGATIF`.
7. Jika Telegram dikonfigurasi, hasil dikirim ke chat yang terdaftar.

## Model Machine Learning

Aplikasi menggunakan file model yang sudah dilatih sebelumnya:

- `model_ml/SVM_model.pkl`
- `model_ml/naive_bayes_model.pkl`
- `model_ml/vectorizer.pkl`

`requirements.txt` mengunci `scikit-learn==1.6.1` agar kompatibel dengan model yang tersimpan.

## Catatan Keamanan

- Jangan menyimpan token Telegram langsung di kode.
- Jangan commit file `.env`.
- Gunakan `SECRET_KEY` yang kuat saat deploy.
- Untuk production yang lebih serius, login sederhana sebaiknya diganti dengan autentikasi database atau penyedia identitas.
- Review negatif atau data pelanggan sebaiknya diproses dengan memperhatikan privasi data.

## Roadmap Pengembangan

- Menambahkan autentikasi berbasis database.
- Menyimpan riwayat prediksi.
- Menambahkan visualisasi tren sentimen.
- Menambahkan upload dataset dan retraining model.
- Menambahkan dashboard admin.
- Menambahkan endpoint API publik dengan token.

## Status Proyek

Smart Review Alert saat ini berada pada tahap prototipe fungsional. Fokus utama proyek adalah membuktikan alur end-to-end dari input ulasan, prediksi sentimen, hingga notifikasi cepat. Struktur terbaru sudah dibuat lebih rapi agar mudah dikembangkan menjadi aplikasi yang lebih matang.

## Kredit

Dikembangkan sebagai bagian dari Proyek Utama Informatika di Universitas Teknologi Yogyakarta.
