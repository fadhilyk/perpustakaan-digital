from perpus_app.repositories.kategori_repository import KategoriRepository
from perpus_app.repositories.buku_repository import BukuRepository
from perpus_app.repositories.anggota_repository import AnggotaRepository
from perpus_app.repositories.petugas_repository import PetugasRepository
from perpus_app.repositories.peminjaman_repository import PeminjamanRepository

from perpus_app.services.kategori_service import KategoriService
from perpus_app.services.buku_service import BukuService
from perpus_app.services.anggota_service import AnggotaService
from perpus_app.services.petugas_service import PetugasService
from perpus_app.services.peminjaman_service import PeminjamanService
from perpus_app.services.laporan import Laporan

class Perpustakaan:
    """
    Facade dan Composition Root.
    Mengelola dan menyatukan semua interaksi antar Service Layer.
    """
    def __init__(self):
        # 1. Instansiasi Repositories
        self.kategori_repo = KategoriRepository()
        self.buku_repo = BukuRepository()
        self.anggota_repo = AnggotaRepository()
        self.petugas_repo = PetugasRepository()
        self.peminjaman_repo = PeminjamanRepository()

        # 2. Instansiasi Services (Dependency Injection via Konstruktor)
        # Menunjukkan relasi Composition (1-1) sesuai SDD
        self.kategori_service = KategoriService(self.kategori_repo)
        self.buku_service = BukuService(self.buku_repo, self.kategori_service)
        self.anggota_service = AnggotaService(self.anggota_repo)
        self.petugas_service = PetugasService(self.petugas_repo)
        self.peminjaman_service = PeminjamanService(
            self.peminjaman_repo,
            self.buku_service,
            self.anggota_service,
            self.petugas_service
        )
        
        self.laporan = Laporan(self.buku_service, self.peminjaman_service, self.anggota_service)

        # 3. Merajut relasi in-memory setelah data-data tersebut diload dari JSON
        self._rekonstruksi_data()

    def _rekonstruksi_data(self) -> None:
        """
        Rekonstruksi semua relasi agregasi dan asosiasi di memori agar OOP utuh,
        mengubah referensi by ID menjadi referensi by Object Instance.
        """
        buku_list = self.buku_service.get_all()
        kategori_list = self.kategori_service.get_all()
        peminjaman_list = self.peminjaman_service.get_all()
        anggota_list = self.anggota_service.get_all()
        petugas_list = self.petugas_service.get_all()

        # 3a. Relasi Kategori <-> Buku (1-N Agregasi)
        for buku in buku_list:
            for kategori in kategori_list:
                if buku.id_kategori == kategori.id_kategori:
                    buku._kategori = kategori
                    kategori.tambah_buku(buku)
                    break

        # 3b. Relasi Peminjaman <-> (Buku, Anggota, Petugas) (1-N Asosiasi)
        for pinjam in peminjaman_list:
            for buku in buku_list:
                if pinjam.id_buku == buku.id_buku:
                    pinjam._buku = buku
                    break
                    
            for anggota in anggota_list:
                if pinjam.id_anggota == anggota.id_pengguna:
                    pinjam._anggota = anggota
                    break
                    
            for petugas in petugas_list:
                if pinjam.id_petugas == petugas.id_pengguna:
                    pinjam._petugas = petugas
                    break

        # 3c. Relasi Anggota <-> List Peminjaman (1-N Asosiasi/Agregasi di sisi anggota)
        for anggota in anggota_list:
            pinjaman_anggota = [p for p in peminjaman_list if p.id_anggota == anggota.id_pengguna]
            anggota.set_list_peminjaman(pinjaman_anggota)

    def daftar_anggota(self):
        """
        Mengembalikan daftar seluruh anggota yang sudah terintegrasi
        secara in-memory beserta list_peminjaman-nya.
        """
        return self.anggota_service.get_all()

    def tampilkan_laporan(self):
        """
        Mengembalikan instance Laporan yang bertugas membuat kompilasi data.
        """
        return self.laporan
