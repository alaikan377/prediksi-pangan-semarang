# GitHub Pages Deployment

Versi statis dari Sistem Prediksi Ketersediaan Stok Pangan Kota Semarang.

## Isi
- `index.html` — halaman utama GitHub Pages
- `dashboard.html` — salinan dashboard
- `data.json` — data yang dibaca dashboard secara lokal
- `forecast_champion_2026_2028.csv` — forecast final
- `model_ready_pangan_semarang_2019_2025.csv` — sumber historis/proyeksi
- `deployment_metadata_2019_2025.json` — metadata model
- `.nojekyll` — menonaktifkan pemrosesan Jekyll

## Penting
Versi publik ini tidak menjalankan Python, TensorFlow, atau SARIMA di server.
Dashboard menampilkan hasil forecast final 2026–2028 yang sudah dihasilkan oleh
model deployment final. Ini cocok untuk GitHub Pages yang hanya mendukung
hosting statis.

## Aktifkan GitHub Pages
1. Upload/replace file-file paket ini ke root repository.
2. Repository -> Settings -> Pages.
3. Source: Deploy from a branch.
4. Branch: `main`.
5. Folder: `/(root)`.
6. Save.
