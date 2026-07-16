import pytest
from perpus_app.models.anggota import Anggota
from perpus_app.models.petugas import Petugas
from perpus_app.models.buku import Buku
from perpus_app.models.peminjaman import Peminjaman
from perpus_app.exceptions.app_exceptions import ValidasiError, StokTidakCukupError
from perpus_app.config import DENDA_PER_HARI, StatusPeminjaman, StatusBuku

def test_pengguna_validation():
    # Inisialisasi Anggota akan memanggil setter dari superclass (Pengguna) yang memiliki validasi
    anggota = Anggota(1, "Budi", "08123456789", "budi@email.com", "Jl. Merdeka")
    
    assert anggota.nama == "Budi"
    assert anggota.email == "budi@email.com"
    
    # Test exception bila nilai di-set tidak valid (nama kosong)
    with pytest.raises(ValidasiError):
        anggota.set_nama("")
        
    # Test exception bila email format salah
    with pytest.raises(ValidasiError):
        anggota.set_email("budi-no-email")
        
    # Test exception bila no telp mengandung huruf
    with pytest.raises(ValidasiError):
        anggota.set_no_telepon("08123abc")

def test_buku_ketersediaan_dan_stok():
    # id_buku, judul, penulis, penerbit, tahun, stok, id_kategori
    buku = Buku(1, "Pemrograman Python", "Guido van Rossum", "Tech Books", 2020, 2, 1)
    
    # Cek ketersediaan dan status property di awal
    assert buku.cek_ketersediaan() is True
    assert buku.status == StatusBuku.TERSEDIA
    
    # Kurangi stok 1
    buku.kurangi_stok(1)
    assert buku.stok == 1
    assert buku.status == StatusBuku.TERSEDIA
    
    # Kurangi stok 1 (jadi 0)
    buku.kurangi_stok(1)
    assert buku.stok == 0
    assert buku.cek_ketersediaan() is False
    assert buku.status == StatusBuku.HABIS
    
    # Cek exception jika stok dikurangi padahal 0
    with pytest.raises(StokTidakCukupError):
        buku.kurangi_stok(1)
        
    # Tambah stok dan pastikan ketersediaan aktif kembali
    buku.tambah_stok(5)
    assert buku.stok == 5
    assert buku.status == StatusBuku.TERSEDIA

def test_peminjaman_hitung_denda():
    # id_pinjam, id_anggota, id_buku, id_petugas, tgl_pinjam, tgl_jatuh_tempo
    pinjam = Peminjaman(1, 1, 1, 1, "2026-07-01", "2026-07-08")
    
    # Kasus tepat waktu / sebelum jatuh tempo -> denda = 0.0
    assert pinjam.hitung_denda("2026-07-07") == 0.0
    assert pinjam.hitung_denda("2026-07-08") == 0.0
    
    # Kasus terlambat 2 hari ("2026-07-10" dikurangi "2026-07-08")
    expected_denda = 2 * DENDA_PER_HARI
    assert pinjam.hitung_denda("2026-07-10") == expected_denda
    
    # Tes integrasi dengan kembalikan_buku()
    pinjam.kembalikan_buku("2026-07-10")
    assert pinjam.status == StatusPeminjaman.DIKEMBALIKAN
    assert pinjam.denda == expected_denda
    assert pinjam.tgl_kembali == "2026-07-10"

def test_polymorphism_tampilkan_info():
    # Pembuatan objek yang sama-sama merupakan turunan Pengguna
    anggota = Anggota(1, "Budi", "08123456789", "budi@email.com", "Jl. A")
    petugas = Petugas(2, "Siti", "08129999999", "siti@email.com", "Pustakawan", "siti123", "hash")
    
    # Bukti polimorfisme, menaruh objek dalam 1 list (mixed) dan memanggil metode abstract
    pengguna_list = [anggota, petugas]
    
    hasil = []
    for p in pengguna_list:
        hasil.append(p.tampilkan_info())
        
    assert len(hasil) == 2
    # Memeriksa output override dari Anggota
    assert "Anggota: Budi, Alamat: Jl. A, Pinjaman Aktif: 0" in hasil[0]
    # Memeriksa output override dari Petugas
    assert "Petugas: Siti (Jabatan: Pustakawan)" in hasil[1]
