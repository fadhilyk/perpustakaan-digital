# PRD - Sistem Manajemen Perpustakaan Digital
**Product Requirements Document**
Mata Kuliah: Object-Oriented Programming (OOP)
Versi: 1.0
Bahasa Implementasi: Python 3.10+
Jenis Aplikasi: Desktop GUI (ttkbootstrap / tkinter)

---

## 1. Latar Belakang

Tugas ini meminta pembuatan **Sistem Manajemen Perpustakaan Digital** berbasis GUI (bukan CLI) menggunakan Python, dengan penyimpanan data pada file JSON (tanpa database eksternal). Aplikasi harus merepresentasikan diagram kelas (UML) yang telah dirancang, mengimplementasikan seluruh relasi antar kelas, mendukung operasi CRUD penuh, menerapkan keempat pilar OOP (Abstraction, Encapsulation, Inheritance, Polymorphism), serta memiliki exception handling dan validasi input yang layak.

## 2. Tujuan Produk

1. Membuktikan pemahaman OOP secara praktis melalui aplikasi nyata.
2. Menyediakan sistem yang dapat digunakan petugas perpustakaan untuk mengelola kategori buku, buku, anggota, dan transaksi peminjaman/pengembalian.
3. Menghasilkan laporan sederhana (daftar buku, riwayat transaksi, anggota teraktif).
4. Menjamin integritas alur data: **tidak ada buku tanpa kategori**, **tidak ada akses sistem tanpa akun petugas (administrator) yang terdaftar**.

## 3. Ruang Lingkup (Scope)

### Termasuk (In-Scope)
- Autentikasi sederhana: registrasi akun Petugas (administrator) pertama kali + login.
- CRUD Kategori Buku.
- CRUD Buku (harus memilih kategori yang sudah ada).
- CRUD Anggota.
- CRUD Petugas (opsional untuk multi-user administrasi).
- Transaksi Peminjaman: pinjam buku, kembalikan buku, hitung denda otomatis.
- Laporan: daftar buku, riwayat transaksi, anggota teraktif.
- Penyimpanan data persisten dalam file JSON.
- Validasi input dan exception handling di semua form.

### Tidak Termasuk (Out-of-Scope)
- Autentikasi berbasis cloud/online, enkripsi password tingkat lanjut (cukup hashing sederhana).
- Multi-cabang perpustakaan / multi-database.
- Notifikasi email/SMS.
- Deployment sebagai aplikasi web.

## 4. Aktor (User Roles)

| Aktor | Deskripsi | Turunan Kelas |
|---|---|---|
| **Administrator / Petugas** | Login ke sistem, mengelola kategori, buku, anggota, memproses peminjaman & pengembalian, melihat laporan | `Petugas(Pengguna)` |
| **Anggota** | Direpresentasikan sebagai data (tidak login), dicatat riwayat peminjamannya oleh Petugas | `Anggota(Pengguna)` |

> Catatan: Sesuai diagram kelas, `Pengguna` merupakan kelas dasar abstrak. `Anggota` dan `Petugas` sama-sama melakukan *inheritance* dari `Pengguna` (relasi *Extends* pada diagram).

## 5. Alur Pengguna Utama (Critical User Flows)

### 5.1 Alur Registrasi Administrator Pertama Kali (Wajib)
1. Saat aplikasi pertama kali dijalankan dan belum ada data Petugas tersimpan (`petugas.json` kosong/tidak ada), aplikasi **langsung menampilkan form "Registrasi Administrator"** (bukan form login).
2. User mengisi: nama, email, no. telepon, jabatan, username, password (+ konfirmasi password).
3. Sistem memvalidasi input (format email, panjang password minimal, kecocokan konfirmasi password, keunikan username).
4. Setelah berhasil, akun Petugas pertama disimpan, dan sistem otomatis menampilkan halaman Login.
5. Jika Petugas sudah pernah terdaftar, aplikasi langsung menampilkan halaman **Login**. Halaman login juga menyediakan tautan "Registrasi Petugas Baru" untuk menambah administrator lain (hanya bisa diakses setelah login sebagai Petugas yang sudah ada, demi keamanan dasar).

### 5.2 Alur Wajib: Kategori Sebelum Buku
1. Setelah login, menu **"Tambah Buku"** memeriksa apakah minimal 1 `KategoriBuku` sudah ada.
2. Jika **belum ada kategori sama sekali**, sistem:
   - Menonaktifkan/mengunci form tambah buku, ATAU
   - Menampilkan dialog peringatan: *"Belum ada kategori buku. Silakan tambahkan kategori terlebih dahulu."* dan mengarahkan user ke form **Tambah Kategori Buku**.
3. Form Tambah Buku wajib menampilkan dropdown/combobox kategori yang **hanya berisi kategori yang sudah dibuat** (tidak boleh input teks bebas untuk kategori pada form buku).
4. Setelah kategori dipilih, proses tambah buku berjalan normal (validasi judul, penulis, tahun, stok, dll).

### 5.3 Alur Peminjaman
1. Petugas memilih menu Peminjaman → Pinjam Buku.
2. Petugas memilih Anggota (dari daftar) dan Buku (hanya buku dengan status "Tersedia"/stok > 0).
3. Sistem memvalidasi ketersediaan stok (`cekKetersediaan()`), lalu membuat `Peminjaman` baru dengan `tgl_pinjam` = hari ini, `tgl_jatuh_tempo` = hari ini + N hari (default 7/14 hari, dikonfigurasi), status "Dipinjam".
4. Stok buku berkurang otomatis (`kurangiStok()`).

### 5.4 Alur Pengembalian
1. Petugas memilih Peminjaman aktif → Kembalikan Buku.
2. Sistem menghitung denda (`hitungDenda()`) jika `tanggal_kembali_aktual > tgl_jatuh_tempo`.
3. Status peminjaman diubah menjadi "Dikembalikan", stok buku bertambah (`tambahStok()`).

### 5.5 Alur Laporan
1. Petugas membuka menu Laporan.
2. Sistem menampilkan tiga jenis laporan: Daftar Buku, Riwayat Transaksi, Anggota Teraktif (berdasarkan jumlah peminjaman terbanyak).

## 6. Kebutuhan Fungsional (Functional Requirements)

| ID | Kebutuhan | Prioritas |
|---|---|---|
| FR-01 | Sistem dapat mendaftarkan akun Petugas (administrator) baru | Must |
| FR-02 | Sistem dapat login dengan username/password Petugas | Must |
| FR-03 | CRUD Kategori Buku (Create, Read, Update, Delete) | Must |
| FR-04 | CRUD Buku, wajib memilih kategori yang sudah ada, tidak bisa tambah buku jika kategori kosong | Must |
| FR-05 | CRUD Anggota | Must |
| FR-06 | Transaksi Pinjam Buku dengan validasi stok | Must |
| FR-07 | Transaksi Kembalikan Buku dengan perhitungan denda otomatis | Must |
| FR-08 | Laporan: Daftar Buku, Riwayat Transaksi, Anggota Teraktif | Must |
| FR-09 | Pencarian buku berdasarkan judul/penulis/kategori | Should |
| FR-10 | Validasi input pada seluruh form (tidak boleh kosong, tipe data sesuai, format email, dsb) | Must |
| FR-11 | Exception handling untuk seluruh operasi I/O (baca/tulis JSON) dan operasi bisnis (stok habis, id tidak ditemukan, dsb) | Must |
| FR-12 | Data tersimpan otomatis ke file JSON setiap ada perubahan | Must |
| FR-13 | Hapus Kategori yang masih memiliki buku terkait harus ditolak/di-warning (menjaga integritas relasi Agregasi) | Should |

## 7. Kebutuhan Non-Fungsional

- **Bahasa**: Python 3.10+.
- **GUI Framework**: `ttkbootstrap` (di atas `tkinter`) untuk tampilan modern; fallback ke `tkinter` murni jika library tidak tersedia.
- **Penyimpanan**: File JSON per entitas (`data/buku.json`, `data/anggota.json`, `data/kategori.json`, `data/peminjaman.json`, `data/petugas.json`).
- **Arsitektur**: Layered — GUI (Views) → Service Layer (BukuService, PeminjamanService, Perpustakaan) → Model/Domain (entities) → Persistence (JSON repository).
- **Maintainability**: Kode mengikuti PEP 8, penamaan `snake_case`, satu kelas per file.
- **Testability**: Setiap service memiliki unit test (`unittest`/`pytest`).
- **Portabilitas**: Berjalan di Windows/Linux/Mac tanpa instalasi database eksternal.

## 8. Pemetaan 4 Pilar OOP (Wajib Ada)

| Pilar | Implementasi |
|---|---|
| **Abstraction** | `Pengguna` sebagai *abstract base class* (`abc.ABC`) dengan method abstrak `tampilkan_info()`; `Laporan` mengekspos interface cetak tanpa membuka detail implementasi data internal |
| **Encapsulation** | Semua atribut domain bersifat *private* (`_atribut`) diakses lewat `@property` / getter-setter (`get_nama()`, `set_nama()`); validasi ada di setter |
| **Inheritance** | `Anggota(Pengguna)` dan `Petugas(Pengguna)` mewarisi atribut & method dasar dari `Pengguna` |
| **Polymorphism** | `tampilkan_info()` di-*override* berbeda pada `Anggota` (menampilkan alamat & jumlah pinjaman aktif) dan `Petugas` (menampilkan jabatan); `get_status()` pada `Peminjaman` dapat dipanggil polymorphically dari list campuran objek |

## 9. Pemetaan Relasi Diagram Kelas → Implementasi

| Relasi (Diagram) | Kardinalitas | Jenis | Implementasi Python |
|---|---|---|---|
| `Perpustakaan` — `BukuService` | 1—1 | Composition | `Perpustakaan.__init__` membuat instance `BukuService` |
| `Perpustakaan` — `PeminjamanService` | 1—1 | Composition | `Perpustakaan.__init__` membuat instance `PeminjamanService` |
| `PeminjamanService` — `Laporan` | 1—1 | Composition | `PeminjamanService` memiliki referensi ke `Laporan` |
| `Perpustakaan` — `Anggota` | 1—N | Aggregation | `Perpustakaan.daftar_anggota: list[Anggota]` |
| `BukuService` — `Buku` | 1—N | Aggregation | `BukuService.daftar_buku: list[Buku]` |
| `KategoriBuku` — `Buku` | 1—N | Aggregation | `KategoriBuku.daftar_buku` (referensi) + `Buku._kategori` (referensi balik) |
| `PeminjamanService` — `Peminjaman` | 1—N | Aggregation | `PeminjamanService.daftar_pinjam: list[Peminjaman]` |
| `Anggota` — `Peminjaman` | 1—N | Association | `Anggota.list_peminjaman: list[Peminjaman]` |
| `Buku` — `Peminjaman` | 1—N | Association | `Peminjaman._buku: Buku` (referensi) |
| `Petugas` — `Peminjaman` | 1—N | Association | `Peminjaman._petugas: Petugas` (referensi) |
| `Pengguna` — `Anggota` | Inheritance | Generalization | `class Anggota(Pengguna)` |
| `Pengguna` — `Petugas` | Inheritance | Generalization | `class Petugas(Pengguna)` |

## 10. Kriteria Penerimaan (Acceptance Criteria)

- [ ] Aplikasi dapat dijalankan (`python main.py`) dan menampilkan GUI, bukan CLI.
- [ ] Saat data Petugas kosong, form Registrasi Administrator tampil otomatis.
- [ ] Tidak bisa menambah buku sebelum ada minimal 1 kategori.
- [ ] Semua relasi pada tabel Bagian 9 dapat ditelusuri di kode (unit test membuktikan navigasi objek).
- [ ] CRUD Kategori, Buku, Anggota berjalan penuh (create/read/update/delete) dengan persist ke JSON.
- [ ] Transaksi pinjam/kembali mengubah stok buku secara konsisten.
- [ ] Exception (mis. stok habis, ID tidak ditemukan, file JSON korup) ditangkap dan ditampilkan sebagai pesan error yang ramah pengguna, tidak menyebabkan crash.
- [ ] Validasi input mencegah data kosong/format salah masuk ke sistem.
- [ ] Empat pilar OOP dapat ditunjukkan eksplisit di kode dan didemonstrasikan di laporan/tugas.

## 11. Deliverables

1. Source code aplikasi (`perpustakaan-digital/`).
2. `PRD.md` (dokumen ini), `SDD.md`, `AGENTS.md`, `WORKFLOW_PROMPTS.md`/`.pdf`.
3. File data JSON contoh (seed data).
4. Unit test dasar.
5. README singkat cara menjalankan aplikasi.
