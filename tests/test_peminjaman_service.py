import pytest
import datetime
from perpus_app.services.perpustakaan import Perpustakaan
from perpus_app.exceptions.app_exceptions import StokTidakCukupError

@pytest.fixture
def perpustakaan_test(tmp_path, monkeypatch):
    # Mengarahkan semua Repositori untuk membaca/menulis ke direktori temp (sandbox)
    monkeypatch.setattr("perpus_app.repositories.kategori_repository.DATA_DIR", str(tmp_path))
    monkeypatch.setattr("perpus_app.repositories.buku_repository.DATA_DIR", str(tmp_path))
    monkeypatch.setattr("perpus_app.repositories.anggota_repository.DATA_DIR", str(tmp_path))
    monkeypatch.setattr("perpus_app.repositories.petugas_repository.DATA_DIR", str(tmp_path))
    monkeypatch.setattr("perpus_app.repositories.peminjaman_repository.DATA_DIR", str(tmp_path))
    
    # Inisiasi Composition Root (merangkai seluruh layanan)
    perpus = Perpustakaan()
    
    # Persiapan Skenario Dasar: Kategori, Buku (stok=1), Anggota, Petugas
    kat = perpus.kategori_service.tambah("Fiksi", "Novel")
    buku = perpus.buku_service.tambah_buku("Laskar Pelangi", "Andrea Hirata", "Bentang", 2005, 1, kat.id_kategori)
    anggota = perpus.anggota_service.tambah("Budi", "0812345678", "budi@x.com", "Jakarta")
    petugas = perpus.petugas_service.registrasi("Admin", "0811234567", "admin@x.com", "Kepala", "admin", "password123", "password123")
    
    return perpus, buku, anggota, petugas

def test_pinjam_buku_sampai_stok_habis(perpustakaan_test):
    perpus, buku, anggota, petugas = perpustakaan_test
    
    # Pinjaman Pertama: Berhasil (stok sisa 1 -> 0)
    pinjam1 = perpus.peminjaman_service.pinjam_buku(anggota.id_pengguna, buku.id_buku, petugas.id_pengguna)
    assert pinjam1 is not None
    assert buku.stok == 0
    assert buku.status == "Habis"
    
    # Anggota lain mencoba pinjam buku yang sama ketika stok 0
    anggota2 = perpus.anggota_service.tambah("Andi", "0813456789", "andi@x.com", "Bandung")
    
    with pytest.raises(StokTidakCukupError) as exc:
        perpus.peminjaman_service.pinjam_buku(anggota2.id_pengguna, buku.id_buku, petugas.id_pengguna)
        
    assert "tidak mencukupi" in str(exc.value)

def test_alur_pinjam_dan_kembalikan_dengan_denda(perpustakaan_test, monkeypatch):
    perpus, buku, anggota, petugas = perpustakaan_test
    
    # 1. Proses Peminjaman
    pinjam = perpus.peminjaman_service.pinjam_buku(anggota.id_pengguna, buku.id_buku, petugas.id_pengguna)
    
    # Pastikan in-memory referensi ter-update
    assert pinjam in anggota.list_peminjaman
    assert buku.stok == 0
    
    # 2. Simulasi Waktu Melaju: Kita set hari ini menjadi 2 hari setelah jatuh tempo
    tgl_jatuh_tempo = datetime.datetime.strptime(pinjam.tgl_jatuh_tempo, "%Y-%m-%d").date()
    tgl_kembali_simulasi = tgl_jatuh_tempo + datetime.timedelta(days=2)
    
    # Monkeypatch modul datetime.date pada peminjaman.py untuk memalsukan today()
    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return tgl_kembali_simulasi
            
    monkeypatch.setattr("perpus_app.models.peminjaman.datetime.date", MockDate)
    
    # 3. Proses Pengembalian
    perpus.peminjaman_service.kembalikan_buku(pinjam.id_pinjam)
    
    # 4. Verifikasi State Setelah Kembali
    assert pinjam.status == "Dikembalikan"
    assert pinjam.denda > 0  # Pastikan terkena denda keterlambatan 2 hari
    assert buku.stok == 1  # Stok buku harus naik kembali menjadi 1
