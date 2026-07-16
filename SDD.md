# SDD - Sistem Manajemen Perpustakaan Digital
**Software Design Document**
Versi: 1.0 · Bahasa: Python 3.10+ · GUI: ttkbootstrap/tkinter · Persistensi: JSON

---

## 1. Gambaran Arsitektur

Arsitektur menggunakan pola **layered architecture** 4 lapis agar setiap pilar OOP dan setiap relasi dari diagram kelas dapat ditempatkan secara jelas dan dapat diuji terpisah dari GUI:

```
┌─────────────────────────────────────────────┐
│  GUI Layer (views/)                          │  ttkbootstrap frames & dialogs
├─────────────────────────────────────────────┤
│  Service Layer (services/)                   │  BukuService, PeminjamanService,
│                                               │  Perpustakaan (facade), Laporan
├─────────────────────────────────────────────┤
│  Domain / Model Layer (models/)              │  Pengguna, Anggota, Petugas,
│                                               │  Buku, KategoriBuku, Peminjaman
├─────────────────────────────────────────────┤
│  Persistence Layer (repositories/)           │  Repository per entitas -> JSON
└─────────────────────────────────────────────┘
```

GUI **tidak pernah** mengakses repository langsung; selalu lewat Service Layer. Ini menjaga *encapsulation* di level arsitektur, bukan hanya level kelas.

## 2. Struktur Folder (Final)

> Nama package dalam huruf kecil (`snake_case`), sesuai PEP 8. `perpus_app` adalah package inti; `perpustakaan-digital/` adalah root proyek (boleh berisi tanda hubung karena bukan nama modul yang di-import).

```
perpustakaan-digital/
├── perpus_app/
│   ├── __init__.py
│   ├── main.py                      # entry point, cek petugas.json -> route ke Registrasi/Login
│   ├── config.py                    # konstanta: lama pinjam default, denda/hari, path data
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pengguna.py              # class Pengguna (ABC)
│   │   ├── anggota.py               # class Anggota(Pengguna)
│   │   ├── petugas.py               # class Petugas(Pengguna)
│   │   ├── kategori_buku.py         # class KategoriBuku
│   │   ├── buku.py                  # class Buku
│   │   └── peminjaman.py            # class Peminjaman
│   ├── services/
│   │   ├── __init__.py
│   │   ├── buku_service.py          # class BukuService
│   │   ├── kategori_service.py      # class KategoriService (CRUD kategori, tidak ada di diagram
│   │   │                              awal tapi dibutuhkan utk CRUD kategori penuh)
│   │   ├── anggota_service.py       # class AnggotaService (CRUD anggota)
│   │   ├── petugas_service.py       # class PetugasService (registrasi & login)
│   │   ├── peminjaman_service.py    # class PeminjamanService
│   │   ├── perpustakaan.py          # class Perpustakaan (facade / composition root)
│   │   └── laporan.py               # class Laporan
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py       # generic JSON repository (abstract)
│   │   ├── buku_repository.py
│   │   ├── kategori_repository.py
│   │   ├── anggota_repository.py
│   │   ├── petugas_repository.py
│   │   └── peminjaman_repository.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   └── app_exceptions.py        # seluruh custom exception (Bagian 6)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py            # fungsi validasi input
│   │   └── id_generator.py          # generator id auto-increment
│   └── views/
│       ├── __init__.py
│       ├── app.py                   # root ttkbootstrap.Window + router antar frame
│       ├── login_frame.py
│       ├── register_petugas_frame.py
│       ├── dashboard_frame.py
│       ├── kategori_frame.py
│       ├── buku_frame.py
│       ├── anggota_frame.py
│       ├── peminjaman_frame.py
│       └── laporan_frame.py
├── data/
│   ├── buku.json
│   ├── kategori.json
│   ├── anggota.json
│   ├── petugas.json
│   └── peminjaman.json
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_buku_service.py
│   ├── test_peminjaman_service.py
│   └── test_validators.py
├── requirements.txt
├── README.md
├── PRD.md
├── SDD.md
├── AGENTS.md
└── WORKFLOW_PROMPTS.md
```

**Konvensi wajib:**
- Semua file dan fungsi: `snake_case`. Semua kelas: `PascalCase`.
- Satu kelas domain inti = satu file (memudahkan mapping ke diagram UML saat penilaian).
- Import antar layer hanya boleh mengarah "ke bawah" (`views` → `services` → `models`/`repositories`); tidak boleh sebaliknya.

## 3. Spesifikasi Kelas Domain (Models)

### 3.1 `Pengguna` (Abstract Base Class)
```python
from abc import ABC, abstractmethod

class Pengguna(ABC):
    def __init__(self, id_pengguna: int, nama: str, no_telepon: str, email: str):
        self._id_pengguna = id_pengguna
        self._nama = nama
        self._no_telepon = no_telepon
        self._email = email

    @property
    def id_pengguna(self) -> int: ...
    @property
    def nama(self) -> str: ...

    def get_nama(self) -> str: ...
    def set_nama(self, nama: str) -> None: ...   # validasi non-kosong di sini

    @abstractmethod
    def tampilkan_info(self) -> str:
        """Setiap turunan WAJIB override -> polymorphism."""
```

### 3.2 `Anggota(Pengguna)`
- Atribut tambahan: `_alamat: str`, `_list_peminjaman: list[Peminjaman]`.
- `pinjam_buku(buku: Buku) -> None` — mendelegasikan ke `PeminjamanService` (Anggota tidak menulis file sendiri, agar tidak melanggar layering).
- `get_aktif() -> list[Peminjaman]` — filter status `"Dipinjam"`.
- `get_riwayat() -> list[Peminjaman]` — seluruh riwayat.
- Override `tampilkan_info()` → menampilkan nama, alamat, jumlah pinjaman aktif.

### 3.3 `Petugas(Pengguna)`
- Atribut tambahan: `_jabatan: str`, `_username: str`, `_password_hash: str`.
- `proses_pinjam(peminjaman: Peminjaman) -> None`.
- `verifikasi(anggota: Anggota) -> bool`.
- Override `tampilkan_info()` → menampilkan nama & jabatan.
- Password **tidak pernah** disimpan plaintext; gunakan `hashlib.sha256` (cukup untuk tugas kuliah; disebutkan sebagai batasan keamanan di README).

### 3.4 `KategoriBuku`
- Atribut: `_id_kategori`, `_nama_kategori`, `_deskripsi`.
- `tambah_buku(buku)`, `hapus_buku(id_buku)`, `get_daftar_buku() -> list[Buku]` — merupakan sisi "banyak" dari agregasi dikelola lewat referensi id, bukan objek langsung, untuk menghindari *circular reference* saat serialisasi JSON (lihat Bagian 5).

### 3.5 `Buku`
- Atribut: `id_buku`, `judul`, `penulis`, `penerbit`, `tahun`, `stok`, `status`, `id_kategori` (FK).
- `kurangi_stok(jumlah=1)` → raise `StokTidakCukupError` bila hasil < 0.
- `tambah_stok(jumlah=1)`.
- `cek_ketersediaan() -> bool` → `stok > 0`.
- `status` diturunkan otomatis (property) dari `stok` ("Tersedia"/"Habis") — contoh *encapsulation* (computed property, bukan field yang bisa langsung diubah sembarangan).

### 3.6 `Peminjaman`
- Atribut: `id_pinjam`, `tgl_pinjam`, `tgl_jatuh_tempo`, `tgl_kembali`, `status`, `denda`, `id_anggota` (FK), `id_buku` (FK), `id_petugas` (FK).
- `hitung_denda() -> float` → `max(0, (tgl_kembali_aktual - tgl_jatuh_tempo).days) * DENDA_PER_HARI`.
- `kembalikan_buku()` → set `tgl_kembali`, status `"Dikembalikan"`, hitung denda.
- `get_status() -> str`.

## 4. Spesifikasi Kelas Service

| Kelas | Tanggung Jawab | Relasi Kunci |
|---|---|---|
| `BukuService` | CRUD `Buku`, pencarian, agregasi `List[Buku]` | 1—N dengan `Buku` |
| `KategoriService` | CRUD `KategoriBuku`, cegah hapus kategori yang masih dipakai `Buku` | 1—N dengan `KategoriBuku`→`Buku` |
| `AnggotaService` | CRUD `Anggota` | 1—N via `Perpustakaan` |
| `PetugasService` | Registrasi, login, hashing password | Membentuk objek `Petugas` |
| `PeminjamanService` | `pinjam_buku(id_anggota, id_buku, id_petugas)`, `kembalikan_buku(id_pinjam)`, agregasi `List[Peminjaman]` | 1—N dengan `Peminjaman`; 1—1 dengan `Laporan` |
| `Perpustakaan` | **Composition root / facade**: membentuk & menyimpan instance `BukuService`, `PeminjamanService`, `AnggotaService`; expose `daftar_anggota()`, `tampilkan_laporan()` | 1—1 dengan `BukuService` & `PeminjamanService`; 1—N dengan `Anggota` |
| `Laporan` | `cetak_daftar_buku()`, `cetak_riwayat_transaksi()`, `cetak_anggota_teraktif()` — menerima data lewat constructor/method dari service, tidak mengakses repository langsung | 1—1 dengan `PeminjamanService` |

`Perpustakaan` berperan sebagai **Composition Root**: satu-satunya tempat semua service di-*instantiate* dan disuntikkan (manual dependency injection) ke `views/app.py`. Ini membuat relasi 1–1 pada diagram (Perpustakaan↔BukuService, Perpustakaan↔PeminjamanService) eksplisit di kode, bukan sekadar impor global.

## 5. Strategi Persistensi JSON & Relasi

Karena JSON tidak mendukung referensi objek langsung, semua relasi antar entitas disimpan sebagai **ID (foreign key)**, mirip pola *DTO*:

```json
// data/buku.json
[
  {"id_buku": 1, "judul": "Laskar Pelangi", "penulis": "Andrea Hirata",
   "penerbit": "Bentang", "tahun": 2005, "stok": 3, "id_kategori": 2}
]
```

```json
// data/peminjaman.json
[
  {"id_pinjam": 1, "id_anggota": 4, "id_buku": 1, "id_petugas": 1,
   "tgl_pinjam": "2026-07-01", "tgl_jatuh_tempo": "2026-07-08",
   "tgl_kembali": null, "status": "Dipinjam", "denda": 0.0}
]
```

Saat aplikasi start, `Perpustakaan` memuat seluruh JSON lalu **merekonstruksi relasi objek in-memory** (mis. `Anggota.list_peminjaman` diisi ulang dari `peminjaman.json` yang cocok `id_anggota`). Setiap perubahan (create/update/delete) memicu `repository.save_all()` agar file JSON selalu sinkron dengan state in-memory (write-through, sederhana untuk skala tugas kuliah).

`base_repository.py` mendefinisikan kelas abstrak generik:
```python
class BaseRepository(ABC):
    @abstractmethod
    def load(self) -> list[dict]: ...
    @abstractmethod
    def save(self, data: list[dict]) -> None: ...
```
→ Contoh *abstraction* tambahan di lapisan persistence, sekaligus memudahkan mengganti backend (mis. ke SQLite) di masa depan tanpa mengubah service layer.

## 6. Exception Handling

### 6.1 Hierarki Custom Exception (`exceptions/app_exceptions.py`)
```python
class AppError(Exception):
    """Base untuk semua exception aplikasi."""

class ValidasiError(AppError):
    """Input tidak valid (form GUI)."""

class DataTidakDitemukanError(AppError):
    """ID entitas tidak ada (buku/anggota/kategori/peminjaman)."""

class StokTidakCukupError(AppError):
    """Stok buku habis saat proses pinjam."""

class KategoriMasihDipakaiError(AppError):
    """Kategori tidak boleh dihapus karena masih punya buku terkait."""

class AutentikasiError(AppError):
    """Username/password salah, atau username sudah terdaftar saat registrasi."""

class PenyimpananError(AppError):
    """Gagal baca/tulis file JSON (I/O, JSON corrupt, permission)."""
```

### 6.2 Prinsip Penanganan
- **Service layer**: melempar (`raise`) exception spesifik di atas — tidak pernah membiarkan `Exception` generik bocor ke GUI tanpa konteks.
- **GUI layer**: setiap aksi tombol dibungkus `try/except AppError as e: messagebox/toast; except Exception as e: log + pesan generik "Terjadi kesalahan tak terduga"`. Aplikasi **tidak boleh crash** akibat input pengguna.
- Operasi file (`base_repository`) membungkus `json.JSONDecodeError`, `FileNotFoundError`, `PermissionError` menjadi `PenyimpananError` agar GUI cukup menangani satu jenis exception untuk semua masalah penyimpanan.

## 7. Validasi Input (`utils/validators.py`)

| Field | Aturan |
|---|---|
| Nama / Judul / Penulis / Nama Kategori | Tidak boleh kosong, trim whitespace, panjang 2–100 karakter |
| Email | Regex format email standar |
| No. Telepon | Hanya digit, panjang 8–15 |
| Tahun terbit | Integer, 1400 ≤ tahun ≤ tahun sekarang |
| Stok | Integer ≥ 0 |
| Username | Alfanumerik, tanpa spasi, unik terhadap `petugas.json` |
| Password | Minimal 6 karakter, harus sama dengan konfirmasi password saat registrasi |
| Pilihan Kategori (form Buku) | Wajib dipilih dari daftar kategori yang ada (tidak boleh kosong / free text) |
| Pilihan Buku (form Peminjaman) | Wajib buku dengan `cek_ketersediaan() == True` |

Setiap fungsi validator mengembalikan `(bool, str)` → `(valid, pesan_error)`, dipanggil di GUI sebelum data diteruskan ke Service Layer; Service Layer **tetap** memvalidasi ulang (defense-in-depth) supaya logic bisnis tidak bergantung pada GUI.

## 8. Alur Routing GUI (`views/app.py`)

```
main.py
  └─ cek petugas.json
       ├─ kosong  -> RegisterPetugasFrame (registrasi admin pertama)
       └─ ada isi -> LoginFrame
LoginFrame (sukses) -> DashboardFrame
DashboardFrame -> KategoriFrame | BukuFrame | AnggotaFrame | PeminjamanFrame | LaporanFrame
BukuFrame.on_show():
    if kategori_service.get_all() kosong:
        tampilkan dialog warning -> redirect ke KategoriFrame
    else:
        tampilkan form tambah buku dengan combobox kategori terisi
```

## 9. Sequence Diagram (Teks) — Pinjam Buku

```
User(Petugas) -> PeminjamanFrame: klik "Pinjam Buku"
PeminjamanFrame -> PeminjamanService: pinjam_buku(id_anggota, id_buku, id_petugas)
PeminjamanService -> BukuService: get_by_id(id_buku)
BukuService --> PeminjamanService: Buku
PeminjamanService -> Buku: cek_ketersediaan()
alt stok habis
    PeminjamanService --> PeminjamanFrame: raise StokTidakCukupError
else stok tersedia
    PeminjamanService -> Buku: kurangi_stok(1)
    PeminjamanService -> Peminjaman: new Peminjaman(...)
    PeminjamanService -> PeminjamanRepository: save_all()
    PeminjamanService --> PeminjamanFrame: Peminjaman berhasil dibuat
end
```

## 10. Unit Test Minimum yang Wajib Ada

- `test_models.py`: property/getter-setter, `hitung_denda()`, `cek_ketersediaan()`, override `tampilkan_info()` pada `Anggota` vs `Petugas` (bukti polymorphism).
- `test_buku_service.py`: tambah/hapus/cari buku, `StokTidakCukupError`.
- `test_peminjaman_service.py`: alur pinjam→kembalikan, perhitungan denda telat.
- `test_validators.py`: semua aturan pada Bagian 7 (kasus valid & invalid).

## 11. Dependencies (`requirements.txt`)

```
ttkbootstrap>=1.10
pytest>=8.0
```

(`tkinter` sudah bawaan Python standard library.)
