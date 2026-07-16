import ttkbootstrap as ttk
from perpus_app.views.kategori_frame import KategoriFrame
from perpus_app.views.buku_frame import BukuFrame
from perpus_app.views.anggota_frame import AnggotaFrame
from perpus_app.views.peminjaman_frame import PeminjamanFrame
from perpus_app.views.laporan_frame import LaporanFrame

class DashboardFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.facade = facade
        self._build_ui()

    def _build_ui(self):
        petugas = getattr(self.facade, 'petugas_aktif', None)
        nama_petugas = petugas.nama if petugas else "Petugas"

        # Salam pembuka dan judul
        ttk.Label(self, text="Dashboard Perpustakaan", font=("Helvetica", 24, "bold")).pack(pady=(30, 5))
        ttk.Label(self, text=f"Selamat Datang, {nama_petugas}", font=("Helvetica", 14)).pack(pady=(0, 30))

        # Kontainer tombol agar berada di tengah
        frame_btn = ttk.Frame(self)
        frame_btn.pack(pady=10)

        btn_style = "primary"
        btn_width = 25

        # Baris 1: Kategori & Buku
        ttk.Button(frame_btn, text="Kelola Kategori", bootstyle=btn_style, width=btn_width, 
                   command=lambda: self.master.show_frame(KategoriFrame)).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(frame_btn, text="Kelola Buku", bootstyle=btn_style, width=btn_width, 
                   command=lambda: self.master.show_frame(BukuFrame)).grid(row=0, column=1, padx=10, pady=10)
                   
        # Baris 2: Anggota & Transaksi
        ttk.Button(frame_btn, text="Kelola Anggota", bootstyle=btn_style, width=btn_width, 
                   command=lambda: self.master.show_frame(AnggotaFrame)).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(frame_btn, text="Transaksi Peminjaman", bootstyle=btn_style, width=btn_width, 
                   command=lambda: self.master.show_frame(PeminjamanFrame)).grid(row=1, column=1, padx=10, pady=10)
                   
        # Baris 3: Laporan
        ttk.Button(frame_btn, text="Laporan & Statistik", bootstyle="info", width=btn_width, 
                   command=lambda: self.master.show_frame(LaporanFrame)).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Logout di bawah
        ttk.Button(self, text="Logout", bootstyle="danger outline", command=self._logout).pack(pady=40)

    def _logout(self):
        # Menghapus session petugas
        self.facade.petugas_aktif = None
        # Mengembalikan ke halaman Login
        from perpus_app.views.login_frame import LoginFrame
        self.master.show_frame(LoginFrame)
