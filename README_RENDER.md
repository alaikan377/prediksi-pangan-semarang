# Public Deployment — Render

Paket ini adalah versi ringan untuk hosting publik dari **Sistem Prediksi Ketersediaan Stok Pangan Kota Semarang**.

## Mengapa versi ringan?

Eksperimen dan model final sudah selesai dijalankan sebelumnya. File `forecast_champion_2026_2028.csv` berisi hasil forecast final 36 bulan yang dihasilkan oleh champion model hasil refit 2019–2025.

Untuk deployment publik gratis, aplikasi **tidak memuat TensorFlow atau objek SARIMA saat runtime**. API membaca hasil forecast final tersebut dan menyajikannya ke dashboard. Hal ini menurunkan kebutuhan RAM secara drastis tanpa mengubah angka forecast yang ditampilkan.

## Cakupan

- Historis: Januari 2019 – Desember 2024
- Proyeksi resmi: Januari – Desember 2025
- Forecast final model: Januari 2026 – Desember 2028
- Horizon: 1–36 bulan
- Komoditas: 7

## Deploy ke Render

1. Buat repository GitHub baru.
2. Upload **isi folder ini** ke root repository (jangan upload folder pembungkus lain di atasnya).
3. Masuk ke Render.
4. Pilih **New > Blueprint** dan hubungkan repository tersebut.
5. Render akan membaca `render.yaml`.
6. Konfirmasi pembuatan web service pada plan **Free**.
7. Tunggu build dan deploy selesai.
8. Buka URL Render, lalu tambahkan `/dashboard`.

Jika menggunakan **New > Web Service** secara manual:

- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
- Health Check Path: `/health`

## Endpoint

- `/`
- `/health`
- `/dashboard`
- `/metadata`
- `/commodities`
- `/historical?commodity=Beras`
- `/forecast`
- `/forecast-all`
- `/predict-next`
- `/docs`

## Catatan

Free web service Render dapat spin down ketika tidak menerima traffic. Request pertama setelah idle dapat membutuhkan waktu lebih lama sampai service aktif kembali.
