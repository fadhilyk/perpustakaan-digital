# Sistem Manajemen Perpustakaan Digital

Aplikasi berbasis GUI (*Graphical User Interface*) yang dibangun secara murni menggunakan bahasa Python dan balutan tema modern `ttkbootstrap`. Aplikasi ini didesain untuk mempermudah dan mendigitalisasi pengelolaan data operasional perpustakaan sehari-hari.

Aplikasi ini secara disiplin mengadopsi prinsip arsitektur perangkat lunak 4-lapis (*Layered Architecture*) yang memisahkan logika antarmuka (GUI Views), layanan bisnis (Services), model domain abstrak (Models), dan mekanisme penyimpanan (Repositories). Konsep ini menjamin kode yang solid, mudah dites (*testable*), dan menganut kuat pilar *Object-Oriented Programming* (OOP).

## 🌟 Ringkasan Fitur

- **Manajemen Autentikasi Petugas**: Sistem pendaftaran dan *login* aman dengan fitur pelindung *password* menggunakan *hash* SHA-256.
- **Kelola Master Data (CRUD)**:
  - **Kategori Buku**: Menambah, mengubah, dan menghapus kategori. Dilengkapi validasi keamanan: kategori tidak bisa dihapus secara sembrono jika masih ada buku fisik yang menggunakan label tersebut (*Integritas Relasi*).
  - **Katalog Buku**: Pendataan koleksi buku beserta penyesuaian jumlah stok aktual di rak.
  - **Data Anggota**: Pengelolaan anggota perpustakaan secara detail (Nama, Email, Telepon, Alamat domisili).
- **Sistem Transaksi Peminjaman**:
  - Validasi ketat ketersediaan stok buku (*real-time*). Anggota tak bisa meminjam jika stok = 0.
  - Mekanisme identifikasi otomatis Petugas yang sedang melayani transaksi (dari sesi *login* aktif).
  - Sistem pengembalian buku disertai kalkulasi denda keterlambatan secara otomatis.
- **Laporan & Statistik Otomatis**: Dasbor khusus berisi data tabular interaktif yang memuat daftar seluruh koleksi buku, riwayat transaksi lengkap, serta "klasemen" statistik anggota paling aktif di perpustakaan.

## 🛠️ Prasyarat & Instalasi

Pastikan komputer/laptop Anda telah terpasang perangkat **Python versi 3.10** (atau lebih baru).

1. **Kloning atau Buka Repositori**:
   Buka terminal/CMD dan arahkan direktori (*cd*) menuju *folder* `perpustakaan_digital` ini.

2. **Instalasi Modul Pendukung**:
   Aplikasi ini sangat minim kebergantungan eksternal. Kami hanya memanfaatkan pustaka `ttkbootstrap` untuk mempercantik UI, serta `pytest` untuk lingkungan pengujian. Pasang dengan komando:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Cara Menjalankan Aplikasi

Jalankan aplikasi secara komprehensif (agar konfigurasi jalur modul atau *routing* terbaca jelas) menggunakan perintah berikut dari dalam folder utama proyek:

```bash
python -m perpus_app.main
```
> **Catatan Alur Pintar**: Jika ini adalah momen pertama kali Anda menjalankan aplikasi di mana file `petugas.json` masih hampa tak bernyawa, sistem dengan cerdas akan otomatis memandu Anda ke layar **Registrasi Petugas Perdana**. Setelah akun tersebut rampung, silakan masuk melalui jendela **Login** ke depannya.

## 🧪 Menjalankan Pengujian Sistem (Unit Tests)

Integritas aplikasi ini dikawal oleh *unit testing* yang kokoh. Untuk menjalankan dan memvalidasi keabsahan fungsi, ketik:

```bash
python -m pytest tests/
```

## ⚠️ Catatan Pembatasan (*Limitations*)

Sistem dirancang sedemikian rupa untuk menonjolkan penerapan logika desain (PBO/OOP) yang baik sesuai kriteria penilaian. Namun, sistem punya batasan sebagai berikut:
- **Penyimpanan Lokal (File JSON Bersahaja)**: Program ini pantang menggunakan *Database Management System* (seperti SQL/Postgres) melainkan menyimpan rekaman di dalam *flat-file* format `.json` (di dalam folder `data/`). Format ini ideal untuk penugasan *standalone app*, namun tidak dianjurkan untuk penggunaan *Multi-User* skala masif karena ketiadaan fitur *locking* saat transaksi konjugasi.
- **Keamanan *Hashing* Dasar**: Sandi (*password*) staf disimpan aman lewat enkripsi satu arah *SHA-256*. Meski lebih mulia dari teks mentah (*plaintext*), standar keamanan modern *enterprise* umumnya menambahkan bumbu *Salt* algoritma khusus (seperti Bcrypt) demi menjegal manuver serangan *Rainbow Table*.
- **Relasi *In-Memory* (_Facade Reconstruction_)**: Setiap aplikasi dinyalakan, gerbang antarmuka `Perpustakaan()` akan menyedot miliaran bit JSON ke dalam memori aplikasi sebagai wujud nyata Objek Kelas (Contoh: `peminjaman._anggota` menjadi *instance* utuh, tak sebatas angka ID). Hal ini membuktikan kentalnya paradigma Polimorfisme & Asosiasi PBO, namun rakus RAM bila baris data membeludak dalam skala jutaan.
