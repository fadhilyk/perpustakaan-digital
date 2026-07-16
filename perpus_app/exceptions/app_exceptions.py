class AppError(Exception):
    """Base untuk semua exception aplikasi."""
    pass

class ValidasiError(AppError):
    """Input tidak valid (form GUI)."""
    pass

class DataTidakDitemukanError(AppError):
    """ID entitas tidak ada (buku/anggota/kategori/peminjaman)."""
    pass

class StokTidakCukupError(AppError):
    """Stok buku habis saat proses pinjam."""
    pass

class KategoriMasihDipakaiError(AppError):
    """Kategori tidak boleh dihapus karena masih punya buku terkait."""
    pass

class AutentikasiError(AppError):
    """Username/password salah, atau username sudah terdaftar saat registrasi."""
    pass

class PenyimpananError(AppError):
    """Gagal baca/tulis file JSON (I/O, JSON corrupt, permission)."""
    pass
