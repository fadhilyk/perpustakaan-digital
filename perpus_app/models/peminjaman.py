import datetime
from typing import TYPE_CHECKING, Optional
from perpus_app.config import DENDA_PER_HARI, StatusPeminjaman

if TYPE_CHECKING:
    from perpus_app.models.buku import Buku
    from perpus_app.models.anggota import Anggota
    from perpus_app.models.petugas import Petugas

class Peminjaman:
    def __init__(self, id_pinjam: int, id_anggota: int, id_buku: int, id_petugas: int, 
                 tgl_pinjam: str, tgl_jatuh_tempo: str, tgl_kembali: Optional[str] = None, 
                 status: str = StatusPeminjaman.DIPINJAM, denda: float = 0.0):
        # FK / ID references
        self._id_pinjam = id_pinjam
        self._id_anggota = id_anggota
        self._id_buku = id_buku
        self._id_petugas = id_petugas
        
        # State attributes
        self._tgl_pinjam = tgl_pinjam
        self._tgl_jatuh_tempo = tgl_jatuh_tempo
        self._tgl_kembali = tgl_kembali
        self._status = status
        self._denda = float(denda)
        
        # In-memory Object References (Dikelola oleh layer Service)
        self._buku: Optional['Buku'] = None
        self._anggota: Optional['Anggota'] = None
        self._petugas: Optional['Petugas'] = None

    @property
    def id_pinjam(self) -> int:
        return self._id_pinjam
        
    @property
    def id_anggota(self) -> int:
        return self._id_anggota
        
    @property
    def id_buku(self) -> int:
        return self._id_buku
        
    @property
    def id_petugas(self) -> int:
        return self._id_petugas

    @property
    def tgl_pinjam(self) -> str:
        return self._tgl_pinjam
        
    @property
    def tgl_jatuh_tempo(self) -> str:
        return self._tgl_jatuh_tempo
        
    @property
    def tgl_kembali(self) -> Optional[str]:
        return self._tgl_kembali

    @property
    def denda(self) -> float:
        return self._denda

    def get_status(self) -> str:
        return self._status

    @property
    def status(self) -> str:
        return self._status

    def hitung_denda(self, tgl_kembali_aktual: str) -> float:
        """
        Menghitung denda berdasarkan selisih tgl_kembali_aktual dengan tgl_jatuh_tempo.
        Jika belum jatuh tempo atau tepat waktu, denda = 0.0.
        Format tanggal diharapkan: 'YYYY-MM-DD'
        """
        fmt = "%Y-%m-%d"
        try:
            kembali = datetime.datetime.strptime(tgl_kembali_aktual, fmt).date()
            jatuh_tempo = datetime.datetime.strptime(self._tgl_jatuh_tempo, fmt).date()
            selisih_hari = (kembali - jatuh_tempo).days
            return float(max(0, selisih_hari) * DENDA_PER_HARI)
        except ValueError:
            # Jika format tidak sesuai, asumsikan denda 0 agar aplikasi tidak crash,
            # tetapi secara ideal format akan selalu konsisten YYYY-MM-DD
            return 0.0

    def kembalikan_buku(self, tgl_kembali_aktual: str = None) -> None:
        """
        Mengubah status menjadi dikembalikan, menyetel tanggal kembali,
        dan menghitung kalkulasi denda keterlambatan secara otomatis.
        """
        if not tgl_kembali_aktual:
            tgl_kembali_aktual = datetime.date.today().strftime("%Y-%m-%d")
            
        self._tgl_kembali = tgl_kembali_aktual
        self._status = StatusPeminjaman.DIKEMBALIKAN
        self._denda = self.hitung_denda(tgl_kembali_aktual)
