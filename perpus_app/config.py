import os
from pathlib import Path

# Path root aplikasi
BASE_DIR = Path(__file__).resolve().parent.parent

# Path folder data JSON
DATA_DIR = BASE_DIR / "data"

# Konstanta Aturan Peminjaman
LAMA_PINJAM_HARI = 7
DENDA_PER_HARI = 1000.0

# Enum / Konstanta Status Buku
class StatusBuku:
    TERSEDIA = "Tersedia"
    HABIS = "Habis"

# Enum / Konstanta Status Peminjaman
class StatusPeminjaman:
    DIPINJAM = "Dipinjam"
    DIKEMBALIKAN = "Dikembalikan"
