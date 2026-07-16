import hashlib
from typing import Optional
from perpus_app.repositories.petugas_repository import PetugasRepository
from perpus_app.models.petugas import Petugas
from perpus_app.exceptions.app_exceptions import AutentikasiError, DataTidakDitemukanError, ValidasiError
from perpus_app.utils.validators import validasi_password
from perpus_app.utils.id_generator import generate_id

class PetugasService:
    def __init__(self, repository: PetugasRepository):
        self._repository = repository
        self.daftar_petugas: list[Petugas] = []
        self._load_data()

    def _load_data(self) -> None:
        data_dicts = self._repository.load()
        for row in data_dicts:
            petugas = Petugas(
                id_pengguna=row.get('id_pengguna'),
                nama=row.get('nama', ''),
                no_telepon=row.get('no_telepon', ''),
                email=row.get('email', ''),
                jabatan=row.get('jabatan', ''),
                username=row.get('username', ''),
                password_hash=row.get('password_hash', '')
            )
            self.daftar_petugas.append(petugas)

    def _save_data(self) -> None:
        data_dicts = [
            {
                "id_pengguna": p.id_pengguna,
                "nama": p.nama,
                "no_telepon": p.no_telepon,
                "email": p.email,
                "jabatan": p.jabatan,
                "username": p.username,
                "password_hash": p.password_hash
            }
            for p in self.daftar_petugas
        ]
        self._repository.save(data_dicts)

    def get_all(self) -> list[Petugas]:
        return self.daftar_petugas

    def get_by_id(self, id_pengguna: int) -> Petugas:
        for p in self.daftar_petugas:
            if p.id_pengguna == id_pengguna:
                return p
        raise DataTidakDitemukanError(f"Petugas dengan ID {id_pengguna} tidak ditemukan.")

    def _hash_password(self, password: str) -> str:
        """Helper internal untuk mengubah password plaintext menjadi hash SHA-256."""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def _cek_username_unik(self, username: str) -> bool:
        """Memeriksa keunikan username untuk mencegah pendaftaran ganda."""
        for p in self.daftar_petugas:
            if p.username == username:
                return False
        return True

    def registrasi(self, nama: str, no_telepon: str, email: str, jabatan: str, 
                   username: str, password: str, konfirmasi_password: str) -> Petugas:
        # Validasi kesesuaian dan panjang minimal password
        valid, pesan = validasi_password(password, konfirmasi_password)
        if not valid:
            raise ValidasiError(pesan)
            
        # Pengecekan username unik agar tidak terjadi tabrakan identitas
        if not self._cek_username_unik(username):
            raise AutentikasiError(f"Username '{username}' sudah terdaftar!")
            
        new_id = generate_id(self.daftar_petugas, "id_pengguna")
        password_hash = self._hash_password(password)
        
        petugas = Petugas(new_id, nama, no_telepon, email, jabatan, username, password_hash)
        self.daftar_petugas.append(petugas)
        self._save_data()
        return petugas

    def login(self, username: str, password: str) -> Petugas:
        """Melakukan otentikasi berdasarkan kecocokan hash password."""
        password_hash = self._hash_password(password)
        for p in self.daftar_petugas:
            if p.username == username and p.password_hash == password_hash:
                return p
                
        # Sengaja pesannya digeneralisir agar hacker tidak bisa brute-force 
        # menebak username saja atau password saja.
        raise AutentikasiError("Username atau password salah!")
