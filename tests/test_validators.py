import pytest
from datetime import datetime
from perpus_app.utils.validators import (
    validasi_teks, validasi_email, validasi_no_telepon,
    validasi_tahun_terbit, validasi_stok, validasi_username,
    validasi_password, validasi_pilihan
)

def test_validasi_teks():
    assert validasi_teks("Belajar Python", "Judul")[0] is True
    
    valid, pesan = validasi_teks("", "Judul")
    assert valid is False
    assert "tidak boleh kosong" in pesan
    
    valid, pesan = validasi_teks("A", "Judul")
    assert valid is False
    assert "antara 2 dan 100" in pesan
    
    valid, pesan = validasi_teks("A" * 101, "Judul")
    assert valid is False
    assert "antara 2 dan 100" in pesan

def test_validasi_email():
    assert validasi_email("test@email.com")[0] is True
    assert validasi_email("budi.santoso@company.co.id")[0] is True
    
    valid, pesan = validasi_email("test.email")
    assert valid is False
    assert "tidak valid" in pesan
    
    assert validasi_email("")[0] is False

def test_validasi_no_telepon():
    assert validasi_no_telepon("0812345678")[0] is True
    assert validasi_no_telepon("6281987654321")[0] is True
    
    valid, pesan = validasi_no_telepon("081")
    assert valid is False
    assert "antara 8 dan 15 digit" in pesan
    
    valid, pesan = validasi_no_telepon("abcdefgh")
    assert valid is False
    assert "hanya boleh berisi angka" in pesan

def test_validasi_tahun_terbit():
    assert validasi_tahun_terbit(2020)[0] is True
    assert validasi_tahun_terbit("2015")[0] is True
    
    valid, pesan = validasi_tahun_terbit(1399)
    assert valid is False
    assert "antara 1400" in pesan
    
    tahun_depan = datetime.now().year + 1
    valid, pesan = validasi_tahun_terbit(tahun_depan)
    assert valid is False
    assert "antara 1400" in pesan
    
    assert validasi_tahun_terbit("bukan_tahun")[0] is False

def test_validasi_stok():
    assert validasi_stok(10)[0] is True
    assert validasi_stok("5")[0] is True
    assert validasi_stok(0)[0] is True
    
    valid, pesan = validasi_stok(-1)
    assert valid is False
    assert "kurang dari 0" in pesan
    
    assert validasi_stok("nol")[0] is False

def test_validasi_username():
    assert validasi_username("admin123")[0] is True
    
    valid, pesan = validasi_username("admin 123")
    assert valid is False
    assert "spasi" in pesan
    
    valid, pesan = validasi_username("admin@123")
    assert valid is False
    assert "huruf dan angka" in pesan

def test_validasi_password():
    assert validasi_password("pass123", "pass123")[0] is True
    
    valid, pesan = validasi_password("pass", "pass")
    assert valid is False
    assert "minimal 6 karakter" in pesan
    
    valid, pesan = validasi_password("pass123", "pass456")
    assert valid is False
    assert "tidak cocok" in pesan

def test_validasi_pilihan():
    assert validasi_pilihan("1 - Fiksi", "Kategori")[0] is True
    assert validasi_pilihan(1, "Opsi")[0] is True
    
    valid, pesan = validasi_pilihan("", "Kategori")
    assert valid is False
    assert "wajib dipilih" in pesan
    assert validasi_pilihan(None, "Kategori")[0] is False
