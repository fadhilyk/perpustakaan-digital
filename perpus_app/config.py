import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

LAMA_PINJAM_HARI = 7
DENDA_PER_HARI = 1000.0

class StatusBuku:
    TERSEDIA = "Tersedia"
    HABIS = "Habis"

class StatusPeminjaman:
    DIPINJAM = "Dipinjam"
    DIKEMBALIKAN = "Dikembalikan"
