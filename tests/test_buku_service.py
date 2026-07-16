import pytest
from perpus_app.services.buku_service import BukuService
from perpus_app.services.kategori_service import KategoriService
from perpus_app.repositories.buku_repository import BukuRepository
from perpus_app.repositories.kategori_repository import KategoriRepository
from perpus_app.exceptions.app_exceptions import ValidasiError

@pytest.fixture
def setup_services(tmp_path, monkeypatch):
    # Mocking konstanta DATA_DIR agar tidak menimpa data asli aplikasi
    monkeypatch.setattr("perpus_app.repositories.buku_repository.DATA_DIR", str(tmp_path))
    monkeypatch.setattr("perpus_app.repositories.kategori_repository.DATA_DIR", str(tmp_path))

    k_repo = KategoriRepository()
    b_repo = BukuRepository()
    
    k_service = KategoriService(k_repo)
    b_service = BukuService(b_repo, k_service)
    
    return b_service, k_service

def test_tambah_buku_kategori_valid(setup_services):
    b_service, k_service = setup_services
    
    # Persiapan: Buat kategori valid
    kat = k_service.tambah("Pemrograman", "Buku IT")
    
    # Eksekusi: Tambah buku dengan id_kategori yang baru saja dibuat
    buku = b_service.tambah_buku("Belajar Python", "Guido", "TechPub", 2023, 5, kat.id_kategori)
    
    # Verifikasi
    assert buku.judul == "Belajar Python"
    assert buku.id_kategori == kat.id_kategori
    assert len(b_service.get_all()) == 1

def test_tambah_buku_kategori_invalid(setup_services):
    b_service, k_service = setup_services
    
    # Eksekusi: Tambah buku dengan id_kategori fiktif yang pasti tidak ada
    with pytest.raises(ValidasiError) as exc:
        b_service.tambah_buku("Buku Aneh", "Penulis X", "Penerbit Y", 2020, 5, 9999)
        
    # Verifikasi Exception dilempar dengan benar
    assert "tidak ditemukan" in str(exc.value)
