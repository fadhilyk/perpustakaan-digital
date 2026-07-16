# AGENTS.md - Panduan untuk Coding Agent
Proyek: Sistem Manajemen Perpustakaan Digital (`perpustakaan-digital/`)
Dokumen acuan wajib dibaca lebih dulu: `PRD.md`, `SDD.md`.

Dokumen ini adalah instruksi operasional untuk **agent coding** (mis. Claude Code / agent lain) yang akan menulis kode berdasarkan `PRD.md` dan `SDD.md`. Ikuti aturan ini secara ketat.

---

## 1. Prinsip Umum

1. **Jangan menebak requirement.** Jika sesuatu tidak jelas, rujuk `PRD.md`/`SDD.md` dulu. Jika tetap ambigu, buat asumsi paling masuk akal, tulis di komentar/README, lalu lanjutkan — jangan berhenti menunggu klarifikasi kecuali benar-benar blocking.
2. **Ikuti struktur folder di SDD.md Bagian 2 persis.** Jangan mengganti nama package (`perpus_app`), jangan pindahkan file ke lokasi lain tanpa alasan kuat.
3. **Konvensi penamaan wajib PEP 8**: `snake_case` untuk file/fungsi/variabel, `PascalCase` untuk kelas, `UPPER_SNAKE_CASE` untuk konstanta (`config.py`).
4. **Satu kelas domain inti = satu file** di `models/` (memudahkan pemetaan ke diagram UML asli saat dinilai dosen).
5. **GUI wajib `ttkbootstrap`** (fallback `tkinter` polos jika `ttkbootstrap` gagal di-import — bungkus dengan try/except import di `views/app.py`).
6. **Dilarang** menyisipkan logic bisnis di dalam file `views/*.py`. View hanya boleh: mengambil input, memanggil service, menampilkan hasil/errors. Semua perhitungan (denda, stok, validasi bisnis) ada di `services/` atau `models/`.
7. **Dilarang** GUI mengakses `repositories/` langsung. Selalu lewat `services/`.

## 2. Mode Kerja: Plan Mode → Build Mode

Agent bekerja dalam dua mode berurutan untuk setiap langkah di `WORKFLOW_PROMPTS.md`:

- **Plan Mode**: sebelum menulis kode, agent menuliskan rencana singkat (file apa yang akan dibuat/diubah, kelas/fungsi apa saja, relasi apa yang diimplementasikan, referensi ke bagian SDD.md yang relevan). Tidak menulis kode dulu di mode ini.
- **Build Mode**: setelah rencana disetujui (atau otomatis jika prompt bersifat sekuensial dan sudah jelas), agent menulis kode sesuai rencana, lalu menjalankan test yang relevan bila sudah ada.

Setiap prompt di `WORKFLOW_PROMPTS.md` sudah diberi label **[PLAN]** atau **[BUILD]** agar jelas mode mana yang harus dijalankan.

## 3. Urutan Pengerjaan (High-Level)

Ikuti 6 fase berikut secara berurutan (detail prompt per-langkah ada di `WORKFLOW_PROMPTS.md`):

| Fase | Nama | Isi |
|---|---|---|
| 0 | Setup & Fondasi | Struktur folder, `config.py`, exceptions, base repository, validators |
| 1 | Domain Models | `Pengguna`, `Anggota`, `Petugas`, `KategoriBuku`, `Buku`, `Peminjaman` |
| 2 | Repositories | Repository JSON per entitas |
| 3 | Services | `KategoriService`, `BukuService`, `AnggotaService`, `PetugasService`, `PeminjamanService`, `Perpustakaan`, `Laporan` |
| 4 | GUI Views | Registrasi, Login, Dashboard, Kategori, Buku, Anggota, Peminjaman, Laporan |
| 5 | Integrasi, Testing & Polishing | `main.py` routing, unit test, seed data, README |

> **PENTING (state saat ini):** Struktur folder pada `AGENTS.md` versi final sudah dikoreksi (package inti bernama `perpus_app/`, konvensi `snake_case` konsisten, file test sudah disiapkan). Jika ada implementasi sebelumnya yang memakai struktur lama, **jalankan ulang Step 0.1 dengan `AGENTS.md` versi ini** sebelum melanjutkan ke Step 0.2, agar seluruh fase berikutnya konsisten dengan struktur final.

## 4. Aturan Implementasi Khusus (Non-Negotiable)

### 4.1 Flow Registrasi Administrator
- `main.py` **wajib** mengecek `data/petugas.json` saat start.
- Jika kosong/tidak ada → tampilkan `RegisterPetugasFrame` (bukan `LoginFrame`).
- Setelah registrasi sukses → otomatis pindah ke `LoginFrame`.
- Jika sudah ada minimal 1 petugas → langsung `LoginFrame`.
- Password di-hash (`hashlib.sha256`), tidak pernah simpan plaintext.

### 4.2 Flow Kategori Sebelum Buku
- `BukuFrame` **wajib** memanggil `kategori_service.get_all()` setiap kali frame ditampilkan.
- Jika hasilnya kosong → tampilkan dialog peringatan dan arahkan ke `KategoriFrame`; jangan tampilkan form tambah buku.
- Combobox kategori pada form buku **hanya** diisi dari `KategoriService`, tidak boleh input teks bebas.
- `KategoriService.hapus(id_kategori)` wajib memeriksa apakah masih ada `Buku` dengan `id_kategori` tsb → jika ada, raise `KategoriMasihDipakaiError`, jangan hapus.

### 4.3 Empat Pilar OOP — Checklist Wajib Dipenuhi Kode
- [ ] `Pengguna` adalah `abc.ABC` dengan minimal 1 `@abstractmethod`.
- [ ] Semua atribut domain di-*private* (`_nama`) + `@property`/getter-setter dengan validasi di setter.
- [ ] `Anggota` dan `Petugas` inherit dari `Pengguna` dan memanggil `super().__init__()`.
- [ ] `tampilkan_info()` di-override berbeda pada `Anggota` dan `Petugas` (bukti polymorphism, bisa didemokan lewat loop `for p in daftar_pengguna: print(p.tampilkan_info())`).

### 4.4 Exception & Validasi
- Semua custom exception WAJIB didefinisikan di `exceptions/app_exceptions.py` sesuai SDD.md Bagian 6.1 — jangan membuat exception baru di file lain.
- Setiap tombol aksi di GUI wajib dibungkus try/except sesuai pola SDD.md Bagian 6.2.
- Semua validator ada di `utils/validators.py`, dipanggil dari GUI **dan** ulang di Service Layer.

## 5. Definition of Done (per Fase)

Sebuah fase dianggap selesai jika:
1. Semua file yang direncanakan sudah dibuat sesuai struktur folder SDD.md.
2. Tidak ada `import` yang melanggar arah layering (Bagian 1.7).
3. Unit test terkait fase tersebut (jika ada di `tests/`) **lulus** (`pytest`).
4. Tidak ada exception generik (`except Exception:`) tanpa re-raise/logging yang jelas di service layer.
5. Kode lolos baca-ulang manual terhadap checklist Bagian 4.3 (4 pilar OOP) jika fase menyentuh `models/`.

## 6. Larangan

- Jangan membuat versi CLI sebagai pengganti GUI.
- Jangan memakai database eksternal (SQLite/MySQL/Postgres) — persistensi wajib JSON sesuai PRD/SDD.
- Jangan menyimpan password plaintext.
- Jangan mengizinkan form Tambah Buku muncul tanpa kategori tersedia.
- Jangan membuat 1 file raksasa berisi semua kelas — ikuti pemisahan file di Bagian 2 SDD.md.

## 7. Referensi Silang

- Model & atribut lengkap → `SDD.md` §3
- Service & tanggung jawab → `SDD.md` §4
- Skema JSON per entitas → `SDD.md` §5
- Hierarki exception → `SDD.md` §6
- Aturan validasi per field → `SDD.md` §7
- Urutan langkah detail & prompt siap pakai → `WORKFLOW_PROMPTS.md`
