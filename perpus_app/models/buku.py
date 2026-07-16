from perpus_app.utils.validators import validasi_teks, validasi_tahun_terbit, validasi_stok
from perpus_app.exceptions.app_exceptions import ValidasiError, StokTidakCukupError
from perpus_app.config import StatusBuku

class Buku:
    def __init__(self, id_buku: int, judul: str, penulis: str, penerbit: str, tahun: int, stok: int, id_kategori: int):
        self._id_buku = id_buku
        self._id_kategori = id_kategori
        
        self._judul = ""
        self._penulis = ""
        self._penerbit = ""
        self._tahun = 0
        self._stok = 0
        
        # Setter dipanggil untuk melakukan validasi
        self.set_judul(judul)
        self.set_penulis(penulis)
        self.set_penerbit(penerbit)
        self.set_tahun(tahun)
        self.set_stok(stok)
        
        # Referensi balik objek KategoriBuku (dikelola oleh Service)
        self._kategori = None

    @property
    def id_buku(self) -> int:
        return self._id_buku

    @property
    def id_kategori(self) -> int:
        return self._id_kategori
        
    def set_id_kategori(self, id_kategori: int) -> None:
        self._id_kategori = id_kategori

    @property
    def judul(self) -> str:
        return self._judul

    def get_judul(self) -> str:
        return self._judul

    def set_judul(self, judul: str) -> None:
        valid, pesan = validasi_teks(judul, "Judul Buku")
        if not valid:
            raise ValidasiError(pesan)
        self._judul = str(judul).strip()

    @property
    def penulis(self) -> str:
        return self._penulis
        
    def get_penulis(self) -> str:
        return self._penulis

    def set_penulis(self, penulis: str) -> None:
        valid, pesan = validasi_teks(penulis, "Penulis")
        if not valid:
            raise ValidasiError(pesan)
        self._penulis = str(penulis).strip()

    @property
    def penerbit(self) -> str:
        return self._penerbit
        
    def get_penerbit(self) -> str:
        return self._penerbit

    def set_penerbit(self, penerbit: str) -> None:
        valid, pesan = validasi_teks(penerbit, "Penerbit")
        if not valid:
            raise ValidasiError(pesan)
        self._penerbit = str(penerbit).strip()

    @property
    def tahun(self) -> int:
        return self._tahun
        
    def get_tahun(self) -> int:
        return self._tahun

    def set_tahun(self, tahun: int | str) -> None:
        valid, pesan = validasi_tahun_terbit(tahun)
        if not valid:
            raise ValidasiError(pesan)
        self._tahun = int(tahun)

    @property
    def stok(self) -> int:
        return self._stok
        
    def get_stok(self) -> int:
        return self._stok

    def set_stok(self, stok: int | str) -> None:
        valid, pesan = validasi_stok(stok)
        if not valid:
            raise ValidasiError(pesan)
        self._stok = int(stok)

    @property
    def status(self) -> str:
        # Computed property: otomatis menyesuaikan berdasarkan sisa stok
        return StatusBuku.TERSEDIA if self._stok > 0 else StatusBuku.HABIS
        
    def get_status(self) -> str:
        return self.status

    def cek_ketersediaan(self) -> bool:
        return self._stok > 0

    def kurangi_stok(self, jumlah: int = 1) -> None:
        if self._stok - jumlah < 0:
            raise StokTidakCukupError(f"Stok buku '{self._judul}' tidak mencukupi. Sisa stok: {self._stok}.")
        self._stok -= jumlah

    def tambah_stok(self, jumlah: int = 1) -> None:
        if jumlah > 0:
            self._stok += jumlah
