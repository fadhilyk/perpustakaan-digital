from typing import TYPE_CHECKING
from perpus_app.utils.validators import validasi_teks
from perpus_app.exceptions.app_exceptions import ValidasiError

if TYPE_CHECKING:
    from perpus_app.models.buku import Buku

class KategoriBuku:
    def __init__(self, id_kategori: int, nama_kategori: str, deskripsi: str = ""):
        self._id_kategori = id_kategori
        self._nama_kategori = ""
        self._deskripsi = ""
        
        self.set_nama_kategori(nama_kategori)
        self.set_deskripsi(deskripsi)
        
        self._daftar_buku: list['Buku'] = []

    @property
    def id_kategori(self) -> int:
        return self._id_kategori

    @property
    def nama_kategori(self) -> str:
        return self._nama_kategori

    def get_nama_kategori(self) -> str:
        return self._nama_kategori

    def set_nama_kategori(self, nama_kategori: str) -> None:
        valid, pesan = validasi_teks(nama_kategori, "Nama Kategori")
        if not valid:
            raise ValidasiError(pesan)
        self._nama_kategori = str(nama_kategori).strip()

    @property
    def deskripsi(self) -> str:
        return self._deskripsi

    def get_deskripsi(self) -> str:
        return self._deskripsi

    def set_deskripsi(self, deskripsi: str) -> None:
        self._deskripsi = str(deskripsi).strip() if deskripsi else ""

    def tambah_buku(self, buku: 'Buku') -> None:
        if buku not in self._daftar_buku:
            self._daftar_buku.append(buku)

    def hapus_buku(self, id_buku: int) -> None:
        self._daftar_buku = [buku for buku in self._daftar_buku if getattr(buku, 'id_buku', getattr(buku, '_id_buku', -1)) != id_buku]

    def get_daftar_buku(self) -> list['Buku']:
        return self._daftar_buku
