from typing import Optional
from perpus_app.repositories.buku_repository import BukuRepository
from perpus_app.models.buku import Buku
from perpus_app.services.kategori_service import KategoriService
from perpus_app.exceptions.app_exceptions import DataTidakDitemukanError, ValidasiError
from perpus_app.utils.id_generator import generate_id

# CRUD
class BukuService:
    def __init__(self, repository: BukuRepository, kategori_service: KategoriService):
        self._repository = repository
        self._kategori_service = kategori_service
        self.daftar_buku: list[Buku] = []
        self._load_data()

    def _load_data(self) -> None:
        data_dicts = self._repository.load()
        for row in data_dicts:
            buku = Buku(
                id_buku=row.get('id_buku'),
                judul=row.get('judul', ''),
                penulis=row.get('penulis', ''),
                penerbit=row.get('penerbit', ''),
                tahun=row.get('tahun', 0),
                stok=row.get('stok', 0),
                id_kategori=row.get('id_kategori', 0)
            )
            self.daftar_buku.append(buku)

    def _save_data(self) -> None:
        data_dicts = [
            {
                "id_buku": b.id_buku,
                "judul": b.judul,
                "penulis": b.penulis,
                "penerbit": b.penerbit,
                "tahun": b.tahun,
                "stok": b.stok,
                "id_kategori": b.id_kategori
            }
            for b in self.daftar_buku
        ]
        self._repository.save(data_dicts)

    def get_all(self) -> list[Buku]:
        return self.daftar_buku

    def get_by_id(self, id_buku: int) -> Buku:
        for b in self.daftar_buku:
            if b.id_buku == id_buku:
                return b
        raise DataTidakDitemukanError(f"Buku dengan ID {id_buku} tidak ditemukan.")

    def tambah_buku(self, judul: str, penulis: str, penerbit: str, tahun: int, stok: int, id_kategori: int) -> Buku:
        # Validasi id_kategori sesuai instruksi
        try:
            kategori = self._kategori_service.get_by_id(id_kategori)
        except DataTidakDitemukanError:
            raise ValidasiError(f"Kategori dengan ID {id_kategori} tidak ditemukan atau tidak valid.")

        new_id = generate_id(self.daftar_buku, "id_buku")
        buku = Buku(new_id, judul, penulis, penerbit, tahun, stok, id_kategori)
        
        # Langsung sambungkan agregasi in-memory supaya konsisten
        buku._kategori = kategori
        kategori.tambah_buku(buku)
        
        self.daftar_buku.append(buku)
        self._save_data()
        return buku

    def update_buku(self, id_buku: int, judul: str, penulis: str, penerbit: str, tahun: int, stok: int, id_kategori: int) -> Buku:
        try:
            kategori = self._kategori_service.get_by_id(id_kategori)
        except DataTidakDitemukanError:
            raise ValidasiError(f"Kategori dengan ID {id_kategori} tidak ditemukan atau tidak valid.")
            
        buku = self.get_by_id(id_buku)
        
        # Update agregasi in-memory jika kategori berubah
        if buku.id_kategori != id_kategori and buku._kategori:
            buku._kategori.hapus_buku(id_buku)
            
        buku.set_judul(judul)
        buku.set_penulis(penulis)
        buku.set_penerbit(penerbit)
        buku.set_tahun(tahun)
        buku.set_stok(stok)
        buku.set_id_kategori(id_kategori)
        
        buku._kategori = kategori
        kategori.tambah_buku(buku)
        
        self._save_data()
        return buku

    def hapus_buku(self, id_buku: int) -> None:
        buku = self.get_by_id(id_buku)
        
        # Bersihkan referensi dari Kategori sebelum buku dihapus
        if buku._kategori:
            buku._kategori.hapus_buku(id_buku)
            
        self.daftar_buku.remove(buku)
        self._save_data()

    def cari_buku(self, keyword: str) -> list[Buku]:
        keyword = keyword.lower()
        hasil = []
        for b in self.daftar_buku:
            kategori_nama = b._kategori.nama_kategori.lower() if getattr(b, '_kategori', None) else ""
            if keyword in b.judul.lower() or keyword in b.penulis.lower() or keyword in kategori_nama:
                hasil.append(b)
        return hasil
