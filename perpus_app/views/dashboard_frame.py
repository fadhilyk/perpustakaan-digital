import ttkbootstrap as ttk
from datetime import datetime
from perpus_app.views.kategori_frame import KategoriFrame
from perpus_app.views.anggota_frame import AnggotaFrame
from perpus_app.views.peminjaman_frame import PeminjamanFrame
from perpus_app.views.laporan_frame import LaporanFrame
from perpus_app.config import StatusPeminjaman
from perpus_app.utils.icon_manager import IconManager
from perpus_app.utils.ui_helpers import add_card_hover_effect

class DashboardFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.facade = facade
        self._clock_job = None  # Menyimpan referensi job after() agar bisa dibatalkan
        self._build_ui()
        # Responsif: saat ukuran jendela berubah, posisi konten ikut menyesuaikan
        self.bind("<Configure>", self._on_resize)

    def _get_stats(self):
        """Menghitung statistik ringkas dari seluruh service."""
        total_judul   = len(self.facade.buku_service.get_all())
        total_anggota = len(self.facade.anggota_service.get_all())
        try:
            all_pinjam    = self.facade.peminjaman_service.get_all()
            dipinjam      = sum(1 for p in all_pinjam if p.get_status() == StatusPeminjaman.DIPINJAM)
        except Exception:
            dipinjam = 0
            
        # Tersedia adalah total seluruh STOK fisik yang ada saat ini
        tersedia = sum(b.stok for b in self.facade.buku_service.get_all())
        
        return total_judul, total_anggota, dipinjam, tersedia

    def _get_sapaan(self):
        """Mengembalikan sapaan dan simbol sesuai waktu saat ini."""
        jam = datetime.now().hour
        if 5 <= jam < 11:
            return "Selamat Pagi", "\u2600️"   # ☀️
        elif 11 <= jam < 15:
            return "Selamat Siang", "\U0001f31e"  # 🌞
        elif 15 <= jam < 18:
            return "Selamat Sore", "\U0001f324"   # 🌤
        else:
            return "Selamat Malam", "\U0001f319"  # 🌙

    def _build_ui(self):
        petugas      = getattr(self.facade, 'petugas_aktif', None)
        nama_petugas = petugas.nama if petugas else "Petugas"

        # ── Kontainer utama ─────────────────────────────────────────────────
        # Menggunakan place(relx, rely) agar selalu berada di tengah layar
        self.container = ttk.Frame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # ── Header ──────────────────────────────────────────────────────────
        sapaan, simbol = self._get_sapaan()

        # Judul dengan efek typewriter — dimulai kosong, warna biru info
        self.lbl_title = ttk.Label(
            self.container,
            text="",
            font=("Helvetica", 26, "bold"),
            bootstyle="info"
        )
        self.lbl_title.pack(pady=(0, 2))

        # Tagline italic — muncul setelah animasi typewriter selesai
        self.lbl_tagline = ttk.Label(
            self.container,
            text="",
            font=("Helvetica", 10, "italic")
        )
        self.lbl_tagline.pack(pady=(0, 6))

        # Mulai animasi typewriter
        self._judul_full  = "Dashboard Perpustakaan"
        self._judul_idx   = 0
        self._blink_count = 0
        self.after(300, self._typewriter)  # Delay kecil sebelum mulai mengetik

        ttk.Label(
            self.container,
            text=f"{simbol}  {sapaan}, {nama_petugas}",
            font=("Helvetica", 13)
        ).pack(pady=(0, 6))

        # Label jam real-time
        self.lbl_jam = ttk.Label(
            self.container,
            text="",
            font=("Courier", 11, "bold"),
            bootstyle="info"
        )
        self.lbl_jam.pack(pady=(0, 14))
        self._update_clock()  # Mulai tick jam

        # ── Separator atas ──────────────────────────────────────────────────
        ttk.Separator(self.container, orient="horizontal").pack(fill="x", pady=(0, 18))

        # ── Kartu Statistik ─────────────────────────────────────────────────
        total_judul, total_anggota, dipinjam, tersedia = self._get_stats()

        stats = [
            ("▣  Total Judul",   str(total_judul),   "primary"),
            ("◉  Total Anggota", str(total_anggota), "success"),
            ("↻  Dipinjam",      str(dipinjam),      "warning"),
            ("◆  Tersedia",      str(tersedia),      "info"),
        ]

        frame_stats = ttk.Frame(self.container)
        frame_stats.pack(pady=(0, 18))

        for i, (label, value, style) in enumerate(stats):
            card = ttk.Frame(frame_stats, padding=(20, 12), relief="groove", borderwidth=2)
            card.grid(row=0, column=i, padx=8)
            lbl_val = ttk.Label(
                card,
                text=value,
                font=("Helvetica", 26, "bold"),
                bootstyle=style
            )
            lbl_val.pack()
            lbl_desc = ttk.Label(
                card,
                text=label,
                font=("Helvetica", 9)
            )
            lbl_desc.pack()
            
            # Tambahkan efek hover
            add_card_hover_effect(card, [lbl_val, lbl_desc], style)

        # ── Separator bawah ─────────────────────────────────────────────────
        ttk.Separator(self.container, orient="horizontal").pack(fill="x", pady=(0, 18))

        # ── Tombol Menu ─────────────────────────────────────────────────────
        frame_btn = ttk.Frame(self.container)
        frame_btn.pack(pady=(0, 10))

        btn_style = "primary"
        btn_width = 24

        # Pre-load icons
        self.icon_dashboard = IconManager.get_icon("dashboard", size=(16, 16))
        self.icon_books = IconManager.get_icon("books", size=(16, 16))
        self.icon_users = IconManager.get_icon("users", size=(16, 16))
        self.icon_tags = IconManager.get_icon("tags", size=(16, 16))
        self.icon_logout = IconManager.get_icon("logout", size=(16, 16))

        # Baris 1
        ttk.Button(
            frame_btn, text=" Kelola Kategori", image=self.icon_tags, compound="left",
            bootstyle=btn_style, width=btn_width,
            command=lambda: self.master.show_frame(KategoriFrame)
        ).grid(row=0, column=0, padx=10, pady=8)
        ttk.Button(
            frame_btn, text=" Kelola Buku", image=self.icon_books, compound="left",
            bootstyle=btn_style, width=btn_width,
            command=self._go_buku
        ).grid(row=0, column=1, padx=10, pady=8)

        # Baris 2
        ttk.Button(
            frame_btn, text=" Kelola Anggota", image=self.icon_users, compound="left",
            bootstyle=btn_style, width=btn_width,
            command=lambda: self.master.show_frame(AnggotaFrame)
        ).grid(row=1, column=0, padx=10, pady=8)
        ttk.Button(
            frame_btn, text=" Transaksi Peminjaman", image=self.icon_dashboard, compound="left",
            bootstyle=btn_style, width=btn_width,
            command=lambda: self.master.show_frame(PeminjamanFrame)
        ).grid(row=1, column=1, padx=10, pady=8)

        # Baris 3: lebar penuh
        ttk.Button(
            frame_btn, text=" Laporan & Statistik", image=self.icon_dashboard, compound="left",
            bootstyle="info", width=btn_width,
            command=lambda: self.master.show_frame(LaporanFrame)
        ).grid(row=2, column=0, columnspan=2, padx=10, pady=8)

        # ── Logout ───────────────────────────────────────────────────────────
        ttk.Button(
            self.container, text=" Logout", image=self.icon_logout, compound="left",
            bootstyle="danger outline",
            command=self._logout
        ).pack(pady=(18, 0))

    def _typewriter(self):
        """Menampilkan judul huruf per huruf layaknya sedang diketik."""
        if not self.winfo_exists():
            return
        if self._judul_idx <= len(self._judul_full):
            teks_sekarang = self._judul_full[:self._judul_idx]
            # Tampilkan kursor | saat mengetik
            self.lbl_title.config(text=teks_sekarang + "|") 
            self._judul_idx += 1
            self.after(65, self._typewriter)
        else:
            # Selesai mengetik — mulai kedipkan kursor
            self._blink_count = 0
            self._blink_cursor()

    def _blink_cursor(self):
        """Mengkedipkan kursor | sebanyak 3x setelah typewriter selesai."""
        if not self.winfo_exists():
            return
        if self._blink_count < 6:
            if self._blink_count % 2 == 0:
                self.lbl_title.config(text=self._judul_full)
            else:
                self.lbl_title.config(text=self._judul_full + "|")
            self._blink_count += 1
            self.after(300, self._blink_cursor)
        else:
            # Kursor hilang, tampilkan judul bersih + munculkan tagline
            self.lbl_title.config(text=self._judul_full)
            self.lbl_tagline.config(
                text="Kelola koleksi buku dengan mudah & efisien"
            )

    def _update_clock(self):
        """Memperbarui label jam setiap 1 detik."""
        if not self.winfo_exists():
            return  # Hentikan jika frame sudah dihancurkan
        sekarang = datetime.now()
        hari_map = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
        bulan_map = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
                     "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        hari     = hari_map[sekarang.weekday()]
        bulan    = bulan_map[sekarang.month]
        tgl      = sekarang.strftime("%d")
        tahun    = sekarang.year
        jam_str  = sekarang.strftime("%H:%M:%S")
        self.lbl_jam.config(
            text=f"{hari}, {tgl} {bulan} {tahun}   \u2502   {jam_str}"
        )
        self._clock_job = self.after(1000, self._update_clock)

    def _on_resize(self, event):
        """Memindahkan kontainer ke tengah layar setiap kali ukuran frame berubah."""
        self.container.place(relx=0.5, rely=0.5, anchor="center")

    def _logout(self):
        self.facade.petugas_aktif = None
        from perpus_app.views.login_frame import LoginFrame
        self.master.show_frame(LoginFrame)

    def _go_buku(self):
        kategori_list = self.facade.kategori_service.get_all()
        if not kategori_list:
            from ttkbootstrap.dialogs import Messagebox
            Messagebox.show_warning(
                "Data kategori masih kosong! Anda wajib mendaftarkan kategori terlebih dahulu sebelum bisa menambahkan buku.",
                "Akses Ditolak - Kategori Kosong"
            )
            return
        from perpus_app.views.buku_frame import BukuFrame
        self.master.show_frame(BukuFrame)
