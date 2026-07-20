from typing import TYPE_CHECKING
from perpus_app.models.pengguna import Pengguna
from perpus_app.utils.validators import validasi_teks, validasi_username
from perpus_app.exceptions.app_exceptions import ValidasiError

if TYPE_CHECKING:
    from perpus_app.models.anggota import Anggota as KelasAnggota
    from perpus_app.models.peminjaman import Peminjaman

# INHERITANCE
class Petugas(Pengguna):
    def __init__(self, id_pengguna: int, nama: str, no_telepon: str, email: str, jabatan: str, username: str, password_hash: str):
        # Bukti Inheritance: Memanggil __init__ dari kelas induk
        super().__init__(id_pengguna, nama, no_telepon, email)
        
        self._jabatan = ""
        self._username = ""
        self._password_hash = password_hash
        
        self.set_jabatan(jabatan)
        self.set_username(username)

    @property
    def jabatan(self) -> str:
        return self._jabatan

    def get_jabatan(self) -> str:
        return self._jabatan

    def set_jabatan(self, jabatan: str) -> None:
        valid, pesan = validasi_teks(jabatan, "Jabatan")
        if not valid:
            raise ValidasiError(pesan)
        self._jabatan = str(jabatan).strip()

    @property
    def username(self) -> str:
        return self._username

    def get_username(self) -> str:
        return self._username

    def set_username(self, username: str) -> None:
        valid, pesan = validasi_username(username)
        if not valid:
            raise ValidasiError(pesan)
        self._username = str(username).strip()
        
    @property
    def password_hash(self) -> str:
        return self._password_hash
        
    def set_password_hash(self, password_hash: str) -> None:
        self._password_hash = password_hash

    def proses_pinjam(self, peminjaman: 'Peminjaman') -> None:
        pass

    def verifikasi(self, anggota: 'KelasAnggota') -> bool:
        return True

    # POLIMORFISME
    def tampilkan_info(self) -> str:
        # Bukti Polymorphism: Implementasi metode yang dioverride berbeda dari Anggota
        return f"Petugas: {self.nama} (Jabatan: {self._jabatan})"
