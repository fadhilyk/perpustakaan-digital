import datetime
from typing import Optional
from perpus_app.repositories.peminjaman_repository import PeminjamanRepository
from perpus_app.models.peminjaman import Peminjaman
from perpus_app.services.buku_service import BukuService
from perpus_app.services.anggota_service import AnggotaService
from perpus_app.services.petugas_service import PetugasService
from perpus_app.exceptions.app_exceptions import DataTidakDitemukanError, ValidasiError
from perpus_app.utils.id_generator import generate_id
from perpus_app.config import LAMA_PINJAM_HARI, StatusPeminjaman

class PeminjamanService:
    def __init__(self, repository: PeminjamanRepository, 
                 buku_service: BukuService, 
                 anggota_service: AnggotaService, 
                 petugas_service: PetugasService):
        self._repository = repository
        self._buku_service = buku_service
        self._anggota_service = anggota_service
        self._petugas_service = petugas_service
        
        self.daftar_pinjam: list[Peminjaman] = []
        self._load_data()

    def _load_data(self) -> None:
        data_dicts = self._repository.load()
        for row in data_dicts:
            p = Peminjaman(
                id_pinjam=row.get('id_pinjam'),
                id_anggota=row.get('id_anggota', 0),
                id_buku=row.get('id_buku', 0),
                id_petugas=row.get('id_petugas', 0),
                tgl_pinjam=row.get('tgl_pinjam', ''),
                tgl_jatuh_tempo=row.get('tgl_jatuh_tempo', ''),
                tgl_kembali=row.get('tgl_kembali'),
                status=row.get('status', StatusPeminjaman.DIPINJAM),
                denda=row.get('denda', 0.0)
            )
            self.daftar_pinjam.append(p)

    def _save_data(self) -> None:
        data_dicts = [
            {
                "id_pinjam": p.id_pinjam,
                "id_anggota": p.id_anggota,
                "id_buku": p.id_buku,
                "id_petugas": p.id_petugas,
                "tgl_pinjam": p.tgl_pinjam,
                "tgl_jatuh_tempo": p.tgl_jatuh_tempo,
                "tgl_kembali": p.tgl_kembali,
                "status": p.status,
                "denda": p.denda
            }
            for p in self.daftar_pinjam
        ]
        self._repository.save(data_dicts)

    def get_all(self) -> list[Peminjaman]:
        return self.daftar_pinjam

    def get_by_id(self, id_pinjam: int) -> Peminjaman:
        for p in self.daftar_pinjam:
            if p.id_pinjam == id_pinjam:
                return p
        raise DataTidakDitemukanError(f"Transaksi Peminjaman dengan ID {id_pinjam} tidak ditemukan.")

    def pinjam_buku(self, id_anggota: int, id_buku: int, id_petugas: int) -> Peminjaman:
        # 1. Pastikan seluruh entitas valid & ada (bila tidak ada, mereka akan raise DataTidakDitemukanError)
        anggota = self._anggota_service.get_by_id(id_anggota)
        buku = self._buku_service.get_by_id(id_buku)
        petugas = self._petugas_service.get_by_id(id_petugas)

        # 2. Kurangi stok (akan me-raise StokTidakCukupError jika stok buku <= 0)
        buku.kurangi_stok(1)
        
        # Karena kita mengubah state (stok) buku, kita wajib menyimpannya ke buku.json
        # via akses _save_data() milik BukuService
        self._buku_service._save_data()

        # 3. Kalkulasi tanggal (hari ini + durasi konfigurasi)
        tgl_pinjam_dt = datetime.date.today()
        tgl_pinjam = tgl_pinjam_dt.strftime("%Y-%m-%d")
        tgl_jatuh_tempo_dt = tgl_pinjam_dt + datetime.timedelta(days=LAMA_PINJAM_HARI)
        tgl_jatuh_tempo = tgl_jatuh_tempo_dt.strftime("%Y-%m-%d")

        # 4. Buat record peminjaman baru
        new_id = generate_id(self.daftar_pinjam, "id_pinjam")
        pinjam = Peminjaman(
            id_pinjam=new_id, 
            id_anggota=id_anggota, 
            id_buku=id_buku, 
            id_petugas=id_petugas, 
            tgl_pinjam=tgl_pinjam, 
            tgl_jatuh_tempo=tgl_jatuh_tempo
        )

        # 5. Rajut referensi in-memory agar langsung mencerminkan perubahan
        pinjam._buku = buku
        pinjam._anggota = anggota
        pinjam._petugas = petugas
        
        # Tambahkan ke history list peminjaman pada Anggota
        anggota.list_peminjaman.append(pinjam)
        
        # 6. Simpan transaksi peminjaman
        self.daftar_pinjam.append(pinjam)
        self._save_data()
        
        return pinjam

    def kembalikan_buku(self, id_pinjam: int) -> Peminjaman:
        pinjam = self.get_by_id(id_pinjam)
        
        if pinjam.status == StatusPeminjaman.DIKEMBALIKAN:
            raise ValidasiError(f"Buku untuk transaksi ID {id_pinjam} sudah dikembalikan sebelumnya.")
            
        # 1. Update status peminjaman (juga memicu kalkulasi denda otomatis)
        pinjam.kembalikan_buku() 
        
        # 2. Kembalikan stok buku
        if pinjam._buku:
            pinjam._buku.tambah_stok(1)
            # Simpan perubahan state buku
            self._buku_service._save_data()
            
        # 3. Simpan perubahan peminjaman
        self._save_data()
        
        return pinjam
