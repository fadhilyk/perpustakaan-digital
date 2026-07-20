# FAULT HANDLING
class AppError(Exception):
    pass

class ValidasiError(AppError):
    pass

class DataTidakDitemukanError(AppError):
    pass

class StokTidakCukupError(AppError):
    pass

class KategoriMasihDipakaiError(AppError):
    pass

class AutentikasiError(AppError):
    pass

class PenyimpananError(AppError):
    pass
