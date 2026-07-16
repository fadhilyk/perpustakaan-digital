import ttkbootstrap as ttk

class LaporanFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.facade = facade
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # Header Aplikasi
        frame_header = ttk.Frame(self)
        frame_header.pack(fill="x", padx=20, pady=10)
        ttk.Label(frame_header, text="Laporan & Statistik", font=("Helvetica", 20, "bold")).pack(side="left")
        
        # Tombol Segarkan dan Kembali
        frame_header_btn = ttk.Frame(frame_header)
        frame_header_btn.pack(side="right")
        ttk.Button(frame_header_btn, text="Segarkan Data", bootstyle="info", command=self._load_data).pack(side="left", padx=5)
        ttk.Button(frame_header_btn, text="Kembali ke Dashboard", bootstyle="secondary outline", command=self._go_dashboard).pack(side="left", padx=5)

        # Tab Menu Notebook menggunakan ttkbootstrap
        self.notebook = ttk.Notebook(self, bootstyle="info")
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        # Tab 1: Daftar Buku
        self.tab_buku = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_buku, text="Laporan Daftar Buku")
        self._build_tab_buku()

        # Tab 2: Riwayat Transaksi
        self.tab_transaksi = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_transaksi, text="Laporan Riwayat Transaksi")
        self._build_tab_transaksi()

        # Tab 3: Anggota Teraktif
        self.tab_anggota = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.tab_anggota, text="Statistik Anggota Teraktif")
        self._build_tab_anggota()

    def _build_tree(self, parent, columns, widths, headings):
        """Helper internal untuk merender komponen Treeview lebih cepat secara seragam"""
        tree = ttk.Treeview(parent, columns=columns, show="headings", bootstyle="info")
        for col, heading, width in zip(columns, headings, widths):
            tree.heading(col, text=heading)
            # Penyelarasan: Jika tipe data umumnya integer (ID, Tahun, Stok), taruh di center
            anchor_pos = "center" if col in ["id", "tahun", "stok", "id_pinjam", "id_anggota", "pinjaman_aktif", "total_riwayat"] else "w"
            tree.column(col, width=width, anchor=anchor_pos)
            
        # Gulir vertikal
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        
        tree.pack(fill="both", expand=True)
        return tree

    def _build_tab_buku(self):
        cols = ("id", "judul", "penulis", "kategori", "tahun", "stok", "status")
        headings = ("ID", "Judul", "Penulis", "Kategori", "Tahun Terbit", "Stok", "Status")
        widths = (50, 250, 150, 150, 90, 60, 100)
        self.tree_buku = self._build_tree(self.tab_buku, cols, widths, headings)

    def _build_tab_transaksi(self):
        cols = ("id", "anggota", "buku", "petugas", "tgl_pinjam", "tgl_kembali", "status", "denda")
        headings = ("ID Pinjam", "Anggota", "Buku", "Petugas", "Tgl Pinjam", "Tgl Kembali", "Status", "Denda")
        widths = (80, 150, 200, 150, 100, 100, 100, 100)
        self.tree_transaksi = self._build_tree(self.tab_transaksi, cols, widths, headings)
        # Khusus denda, agar rata kanan (seperti uang)
        self.tree_transaksi.column("denda", anchor="e")

    def _build_tab_anggota(self):
        cols = ("id", "nama", "telepon", "total_riwayat", "pinjaman_aktif")
        headings = ("ID Anggota", "Nama Lengkap", "No. Telepon", "Total Riwayat Pinjaman", "Sedang Dipinjam (Belum Kembali)")
        widths = (80, 200, 150, 200, 250)
        self.tree_anggota = self._build_tree(self.tab_anggota, cols, widths, headings)

    def _load_data(self):
        """Memanggil kelas Laporan pada Facade yang sudah mengekspor data dalam bentuk Dictionary Siap Saji"""
        # 1. Isi Laporan Daftar Buku
        for item in self.tree_buku.get_children():
            self.tree_buku.delete(item)
        data_buku = self.facade.laporan.cetak_daftar_buku()
        for row in data_buku:
            self.tree_buku.insert("", "end", values=(
                row["ID"], row["Judul"], row["Penulis"], row["Kategori"], row["Tahun"], row["Stok"], row["Status"]
            ))
            
        # 2. Isi Laporan Data Riwayat Transaksi (Termasuk histori denda)
        for item in self.tree_transaksi.get_children():
            self.tree_transaksi.delete(item)
        data_trx = self.facade.laporan.cetak_riwayat_transaksi()
        for row in data_trx:
            self.tree_transaksi.insert("", "end", values=(
                row["ID Pinjam"], row["Anggota"], row["Buku"], row["Petugas"], 
                row["Tgl Pinjam"], row["Tgl Kembali"], row["Status"], f"Rp {int(row['Denda'])}"
            ))

        # 3. Isi Laporan Data Anggota Paling Aktif (Klasemen)
        for item in self.tree_anggota.get_children():
            self.tree_anggota.delete(item)
        data_anggota = self.facade.laporan.cetak_anggota_teraktif()
        for row in data_anggota:
            self.tree_anggota.insert("", "end", values=(
                row["ID Anggota"], row["Nama"], row["No. Telepon"], 
                row["Total Riwayat Pinjaman"], row["Pinjaman Aktif"]
            ))

    def _go_dashboard(self):
        from perpus_app.views.dashboard_frame import DashboardFrame
        self.master.show_frame(DashboardFrame)
