from typing import Optional
from perpus_app.repositories.kategori_repository import KategoriRepository
from perpus_app.models.kategori_buku import KategoriBuku
from perpus_app.exceptions.app_exceptions import DataTidakDitemukanError, KategoriMasihDipakaiError
from perpus_app.utils.id_generator import generate_id

class KategoriService:
    def __init__(self, repository: KategoriRepository):
        self._repository = repository
        self.daftar_kategori: list[KategoriBuku] = []
        self._load_data()

    def _load_data(self) -> None:
        data_dicts = self._repository.load()
        for row in data_dicts:
            kategori = KategoriBuku(
                id_kategori=row.get('id_kategori'),
                nama_kategori=row.get('nama_kategori', ''),
                deskripsi=row.get('deskripsi', '')
            )
            self.daftar_kategori.append(kategori)

    def _save_data(self) -> None:
        data_dicts = [
            {
                "id_kategori": k.id_kategori,
                "nama_kategori": k.nama_kategori,
                "deskripsi": k.deskripsi
            }
            for k in self.daftar_kategori
        ]
        self._repository.save(data_dicts)

    def get_all(self) -> list[KategoriBuku]:
        return self.daftar_kategori

    def get_by_id(self, id_kategori: int) -> KategoriBuku:
        for k in self.daftar_kategori:
            if k.id_kategori == id_kategori:
                return k
        # FAULT HANDLING
        raise DataTidakDitemukanError(f"Kategori dengan ID {id_kategori} tidak ditemukan.")

    def tambah(self, nama_kategori: str, deskripsi: str = "") -> KategoriBuku:
        new_id = generate_id(self.daftar_kategori, "id_kategori")
        kategori = KategoriBuku(new_id, nama_kategori, deskripsi)
        self.daftar_kategori.append(kategori)
        self._save_data()
        return kategori

    def update(self, id_kategori: int, nama_kategori: str, deskripsi: str = "") -> KategoriBuku:
        kategori = self.get_by_id(id_kategori)
        kategori.set_nama_kategori(nama_kategori)
        kategori.set_deskripsi(deskripsi)
        self._save_data()
        return kategori

    def hapus(self, id_kategori: int) -> None:
        kategori = self.get_by_id(id_kategori)
        
        # Mengecek apakah ada Buku dengan id_kategori tsb
        # Karena relasi agregasi di _rekonstruksi_data() sudah diisi, kita cukup baca list ini
        if len(kategori.get_daftar_buku()) > 0:
            # FAULT HANDLING
            raise KategoriMasihDipakaiError(
                f"Kategori '{kategori.nama_kategori}' tidak bisa dihapus karena masih dipakai oleh {len(kategori.get_daftar_buku())} buku."
            )
            
        self.daftar_kategori.remove(kategori)
        self._save_data()
