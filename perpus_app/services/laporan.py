from typing import List, Dict, Any
from perpus_app.services.buku_service import BukuService
from perpus_app.services.peminjaman_service import PeminjamanService
from perpus_app.services.anggota_service import AnggotaService

class Laporan:
    def __init__(self, buku_service: BukuService, peminjaman_service: PeminjamanService, anggota_service: AnggotaService):
        self._buku_service = buku_service
        self._peminjaman_service = peminjaman_service
        self._anggota_service = anggota_service

    def cetak_daftar_buku(self) -> List[Dict[str, Any]]:
        buku_list = self._buku_service.get_all()
        laporan = []
        for b in buku_list:
            kategori_nama = b._kategori.nama_kategori if getattr(b, '_kategori', None) else "Tanpa Kategori"
            laporan.append({
                "ID": b.id_buku,
                "Judul": b.judul,
                "Penulis": b.penulis,
                "Kategori": kategori_nama,
                "Tahun": b.tahun,
                "Stok": b.stok,
                "Status": b.status
            })
        return laporan

    def cetak_riwayat_transaksi(self) -> List[Dict[str, Any]]:
        pinjam_list = self._peminjaman_service.get_all()
        laporan = []
        for p in pinjam_list:
            nama_anggota = p._anggota.nama if getattr(p, '_anggota', None) else f"ID {p.id_anggota}"
            judul_buku = p._buku.judul if getattr(p, '_buku', None) else f"ID {p.id_buku}"
            nama_petugas = p._petugas.nama if getattr(p, '_petugas', None) else f"ID {p.id_petugas}"
            
            laporan.append({
                "ID Pinjam": p.id_pinjam,
                "Anggota": nama_anggota,
                "Buku": judul_buku,
                "Tgl Pinjam": p.tgl_pinjam,
                "Tgl Kembali": p.tgl_kembali or "-",
                "Status": p.status,
                "Denda": p.denda,
                "Petugas": nama_petugas
            })
        return laporan

    def cetak_anggota_teraktif(self) -> List[Dict[str, Any]]:
        anggota_list = self._anggota_service.get_all()
        
        # Sorting dengan lambda expression berdasarkan jumlah elemen pada riwayat peminjaman
        sorted_anggota = sorted(anggota_list, key=lambda a: len(a.get_riwayat()), reverse=True)
        
        laporan = []
        for a in sorted_anggota:
            laporan.append({
                "ID Anggota": a.id_pengguna,
                "Nama": a.nama,
                "No. Telepon": a.no_telepon,
                "Total Riwayat Pinjaman": len(a.get_riwayat()),
                "Pinjaman Aktif": len(a.get_aktif())
            })
        return laporan
