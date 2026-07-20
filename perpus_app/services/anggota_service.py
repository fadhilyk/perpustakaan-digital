from typing import Optional
from perpus_app.repositories.anggota_repository import AnggotaRepository
from perpus_app.models.anggota import Anggota
from perpus_app.exceptions.app_exceptions import DataTidakDitemukanError, ValidasiError
from perpus_app.utils.id_generator import generate_id

class AnggotaService:
    def __init__(self, repository: AnggotaRepository):
        self._repository = repository
        self.daftar_anggota: list[Anggota] = []
        self._load_data()

    def _load_data(self) -> None:
        data_dicts = self._repository.load()
        for row in data_dicts:
            anggota = Anggota(
                id_pengguna=row.get('id_pengguna'),
                nama=row.get('nama', ''),
                no_telepon=row.get('no_telepon', ''),
                email=row.get('email', ''),
                alamat=row.get('alamat', '')
            )
            self.daftar_anggota.append(anggota)

    def _save_data(self) -> None:
        data_dicts = [
            {
                "id_pengguna": a.id_pengguna,
                "nama": a.nama,
                "no_telepon": a.no_telepon,
                "email": a.email,
                "alamat": a.alamat
            }
            for a in self.daftar_anggota
        ]
        self._repository.save(data_dicts)

    def get_all(self) -> list[Anggota]:
        return self.daftar_anggota

    def get_by_id(self, id_anggota: int) -> Anggota:
        for a in self.daftar_anggota:
            if a.id_pengguna == id_anggota:
                return a
        # FAULT HANDLING
        raise DataTidakDitemukanError(f"Anggota dengan ID {id_anggota} tidak ditemukan.")

    def tambah(self, nama: str, no_telepon: str, email: str, alamat: str) -> Anggota:
        new_id = generate_id(self.daftar_anggota, "id_pengguna")
        anggota = Anggota(new_id, nama, no_telepon, email, alamat)
        self.daftar_anggota.append(anggota)
        self._save_data()
        return anggota

    def update(self, id_anggota: int, nama: str, no_telepon: str, email: str, alamat: str) -> Anggota:
        anggota = self.get_by_id(id_anggota)
        anggota.set_nama(nama)
        anggota.set_no_telepon(no_telepon)
        anggota.set_email(email)
        anggota.set_alamat(alamat)
        self._save_data()
        return anggota

    def hapus(self, id_anggota: int) -> None:
        anggota = self.get_by_id(id_anggota)
        
        # Opsi integritas: Kita bisa memblokir jika anggota memiliki pinjaman aktif, 
        # namun untuk saat ini difokuskan pada CRUD dasar
        if len(anggota.get_aktif()) > 0:
            # FAULT HANDLING
            raise ValidasiError(f"Anggota {anggota.nama} masih memiliki {len(anggota.get_aktif())} pinjaman aktif. Tidak bisa dihapus.")
            
        self.daftar_anggota.remove(anggota)
        self._save_data()
