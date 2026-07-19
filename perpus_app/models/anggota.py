from typing import TYPE_CHECKING
from perpus_app.models.pengguna import Pengguna
from perpus_app.utils.validators import validasi_teks
from perpus_app.exceptions.app_exceptions import ValidasiError

# Menggunakan TYPE_CHECKING untuk menghindari circular import
if TYPE_CHECKING:
    from perpus_app.models.buku import Buku
    from perpus_app.models.peminjaman import Peminjaman
    from perpus_app.config import StatusPeminjaman

# INHERITANCE
class Anggota(Pengguna):
    def __init__(self, id_pengguna: int, nama: str, no_telepon: str, email: str, alamat: str):
        # Bukti Inheritance: Memanggil __init__ dari kelas induk
        super().__init__(id_pengguna, nama, no_telepon, email)
        
        self._alamat = ""
        self.set_alamat(alamat)
        self._list_peminjaman: list['Peminjaman'] = []

    @property
    def alamat(self) -> str:
        return self._alamat

    def get_alamat(self) -> str:
        return self._alamat

    def set_alamat(self, alamat: str) -> None:
        valid, pesan = validasi_teks(alamat, "Alamat")
        if not valid:
            raise ValidasiError(pesan)
        self._alamat = str(alamat).strip()

    @property
    def list_peminjaman(self) -> list['Peminjaman']:
        return self._list_peminjaman
        
    def set_list_peminjaman(self, peminjaman_list: list['Peminjaman']) -> None:
        self._list_peminjaman = peminjaman_list

    def pinjam_buku(self, buku: 'Buku') -> None:
        """
        Sesuai SDD, mendelegasikan ke PeminjamanService.
        Anggota tidak menulis file sendiri agar tidak melanggar layering.
        """
        pass

    def get_aktif(self) -> list['Peminjaman']:
        # Filter peminjaman yang berstatus "Dipinjam"
        from perpus_app.config import StatusPeminjaman
        return [p for p in self._list_peminjaman if getattr(p, 'status', p.get_status()) == StatusPeminjaman.DIPINJAM]

    def get_riwayat(self) -> list['Peminjaman']:
        return self._list_peminjaman

    # POLIMORFISME
    def tampilkan_info(self) -> str:
        return f"Anggota: {self.nama}, Alamat: {self._alamat}, Aktif Peminjaman: {len(self._list_peminjaman)}"
