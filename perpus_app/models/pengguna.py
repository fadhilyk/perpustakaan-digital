from abc import ABC, abstractmethod
from perpus_app.utils.validators import validasi_teks, validasi_email, validasi_no_telepon
from perpus_app.exceptions.app_exceptions import ValidasiError

class Pengguna(ABC):
    def __init__(self, id_pengguna: int, nama: str, no_telepon: str, email: str):
        self._id_pengguna = id_pengguna
        self._nama = ""
        self._no_telepon = ""
        self._email = ""
        
        self.set_nama(nama)
        self.set_no_telepon(no_telepon)
        self.set_email(email)

    @property
    def id_pengguna(self) -> int:
        return self._id_pengguna

    @property
    def nama(self) -> str:
        return self._nama
        
    @property
    def no_telepon(self) -> str:
        return self._no_telepon
        
    @property
    def email(self) -> str:
        return self._email

    def get_nama(self) -> str:
        return self._nama

    def set_nama(self, nama: str) -> None:
        valid, pesan = validasi_teks(nama, "Nama Pengguna")
        if not valid:
            raise ValidasiError(pesan)
        self._nama = str(nama).strip()
        
    def get_no_telepon(self) -> str:
        return self._no_telepon
        
    def set_no_telepon(self, no_telepon: str) -> None:
        valid, pesan = validasi_no_telepon(no_telepon)
        if not valid:
            raise ValidasiError(pesan)
        self._no_telepon = str(no_telepon).strip()
        
    def get_email(self) -> str:
        return self._email
        
    def set_email(self, email: str) -> None:
        valid, pesan = validasi_email(email)
        if not valid:
            raise ValidasiError(pesan)
        self._email = str(email).strip()

    @abstractmethod
    def tampilkan_info(self) -> str:
        pass
