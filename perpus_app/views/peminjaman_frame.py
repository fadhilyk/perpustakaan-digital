import ttkbootstrap as ttk
from perpus_app.config import StatusPeminjaman
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
from perpus_app.exceptions.app_exceptions import AppError
from perpus_app.utils.ui_helpers import setup_empty_state, toggle_empty_state

class PeminjamanFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.facade = facade
        
        # Pengambilan State Utama untuk Combo Box Peminjaman (buku wajib yang ber-stok > 0)
        self.list_anggota = self.facade.anggota_service.get_all()
        self.list_buku = [b for b in self.facade.buku_service.get_all() if b.stok > 0]
        
        self.selected_id_pinjam = None
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # 1. Header Area
        frame_header = ttk.Frame(self)
        frame_header.pack(fill="x", padx=20, pady=10)
        ttk.Label(frame_header, text="Sistem Transaksi Peminjaman", font=("Helvetica", 20, "bold")).pack(side="left")
        ttk.Button(frame_header, text="⬅ Kembali ke Dashboard", bootstyle="danger", command=self._go_dashboard).pack(side="right")

        frame_content = ttk.Frame(self)
        frame_content.pack(fill="both", expand=True, padx=20, pady=10)

        # 2. PANEL KIRI: FORM PERINTAH TRANSAKSI PINJAM & KEMBALI
        frame_form = ttk.Labelframe(frame_content, text="Panel Peminjaman Baru", padding=15)
        frame_form.pack(side="left", fill="y", padx=(0, 15))
        
        ttk.Label(frame_form, text="Anggota Peminjam").pack(anchor="w", pady=(5, 2))
        cb_anggota_values = [f"{a.id_pengguna} - {a.nama}" for a in self.list_anggota]
        self.cb_anggota = ttk.Combobox(frame_form, values=cb_anggota_values, state="readonly", width=35)
        self.cb_anggota.pack(fill="x", pady=(0, 15))
        
        # Hanya muat daftar buku yang stoknya di atas nol (tersedia di rak fisik)
        ttk.Label(frame_form, text="Buku Tersedia (Stok > 0)").pack(anchor="w", pady=(5, 2))
        cb_buku_values = [f"{b.id_buku} - {b.judul} (Stok: {b.stok})" for b in self.list_buku]
        self.cb_buku = ttk.Combobox(frame_form, values=cb_buku_values, state="readonly", width=35)
        self.cb_buku.pack(fill="x", pady=(0, 25))

        ttk.Button(frame_form, text="Eksekusi Peminjaman", bootstyle="success", command=self._on_pinjam).pack(fill="x", pady=5)
        ttk.Button(frame_form, text="Sinkronisasi / Muat Ulang Stok", bootstyle="outline-info", command=self._refresh_combos).pack(fill="x", pady=5)
        
        # Papan kendali untuk mengembalikan (hanya aktif jika yang diklik di tabel statusnya Aktif)
        ttk.Label(frame_form, text="Aksi Baris Tabel:").pack(anchor="w", pady=(40, 2))
        self.btn_kembali = ttk.Button(frame_form, text="Tandai Sudah Dikembalikan", bootstyle="warning", state="disabled", command=self._on_kembali)
        self.btn_kembali.pack(fill="x", pady=5)

        # 3. PANEL KANAN: TABEL DAFTAR SEMUA TRANSAKSI
        frame_kanan = ttk.Frame(frame_content)
        frame_kanan.pack(side="right", fill="both", expand=True)

        columns = ("id", "anggota", "buku", "tgl_pinjam", "jatuh_tempo", "status", "denda")
        self.tree = ttk.Treeview(frame_kanan, columns=columns, show="headings", bootstyle="info")
        self.tree.heading("id", text="Trx ID")
        self.tree.heading("anggota", text="Anggota")
        self.tree.heading("buku", text="Buku")
        self.tree.heading("tgl_pinjam", text="Tgl Pinjam")
        self.tree.heading("jatuh_tempo", text="Tenggat (Tempo)")
        self.tree.heading("status", text="Status")
        self.tree.heading("denda", text="Denda (Rp)")
        
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("anggota", width=180)
        self.tree.column("buku", width=220)
        self.tree.column("tgl_pinjam", width=100, anchor="center")
        self.tree.column("jatuh_tempo", width=110, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("denda", width=100, anchor="e")

        self.scrollbar = ttk.Scrollbar(frame_kanan, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.empty_state_frame = setup_empty_state(frame_kanan, "Belum ada riwayat peminjaman.")
        
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _render_tabel(self, data_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for p in data_list:
            # Karena composition root sudah merekonstruksi relasi pointer
            # Kita bisa memanggil properti internal dari objek '_anggota' dan '_buku'
            nama_anggota = getattr(p, '_anggota', None).nama if getattr(p, '_anggota', None) else f"ID {p.id_anggota}"
            judul_buku = getattr(p, '_buku', None).judul if getattr(p, '_buku', None) else f"ID {p.id_buku}"
            
            self.tree.insert("", "end", values=(
                p.id_pinjam, nama_anggota, judul_buku, p.tgl_pinjam, p.tgl_jatuh_tempo, p.status, int(p.denda)
            ))

    def _refresh_combos(self):
        self.list_anggota = self.facade.anggota_service.get_all()
        # Seleksi array in-line yang membuang buku tanpa stok dari dropdown (Stabilitas Bisnis)
        self.list_buku = [b for b in self.facade.buku_service.get_all() if b.stok > 0]
        
        cb_anggota_values = [f"{a.id_pengguna} - {a.nama}" for a in self.list_anggota]
        self.cb_anggota.config(values=cb_anggota_values)
        self.cb_anggota.set("")
        
        cb_buku_values = [f"{b.id_buku} - {b.judul} (Stok: {b.stok})" for b in self.list_buku]
        self.cb_buku.config(values=cb_buku_values)
        self.cb_buku.set("")

    def _load_data(self):
        pinjam_list = self.facade.peminjaman_service.get_all()
        
        toggle_empty_state(self.tree, getattr(self, 'scrollbar', None), getattr(self, 'empty_state_frame', None), len(pinjam_list) == 0)
        
        self._render_tabel(pinjam_list)
        self.btn_kembali.config(state="disabled")
        self.selected_id_pinjam = None

    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            val = item["values"]
            self.selected_id_pinjam = int(val[0])
            status = val[5]
            
            # State manager untuk tombol Pengembalian
            if status == StatusPeminjaman.DIPINJAM:
                self.btn_kembali.config(state="normal")
            else:
                self.btn_kembali.config(state="disabled")

    def _on_pinjam(self):
        val_anggota = self.cb_anggota.get()
        val_buku = self.cb_buku.get()
        
        if not val_anggota or not val_buku:
            Messagebox.show_warning("Tolong pilih satu 'Anggota' dan satu 'Buku' untuk dipinjamkan.", "Terkunci")
            return
            
        id_anggota = int(val_anggota.split(" - ")[0])
        id_buku = int(val_buku.split(" - ")[0])
        
        # Mengecek identitas diri sendiri dari Session (Siapa petugas yang sedang bertugas log in?)
        petugas = getattr(self.facade, "petugas_aktif", None)
        if not petugas:
            Messagebox.show_error("Autentikasi tidak terdeteksi atau kadaluwarsa. Log in ulang untuk melakukan transaksi.", "Sesi Hilang")
            return
            
        id_petugas = petugas.id_pengguna
        
        # EXCEPTION HANDLING
        try:
            self.facade.peminjaman_service.pinjam_buku(id_anggota, id_buku, id_petugas)
            self._load_data()
            self._refresh_combos()  # Segera kurangi stok di tampilan ComboBox!
            ToastNotification(title="Transaksi Berhasil", message="Sukses meminjamkan buku! Stok sudah otomatis dikurangi.", duration=3000, bootstyle="success").show_toast()
        except AppError as e:
            Messagebox.show_error(str(e), "Penolakan Transaksi")
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Pinjam Buku: {e}")
            Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _on_kembali(self):
        if not self.selected_id_pinjam:
            return
            
        konfirm = Messagebox.yesno(f"Setujui pengembalian untuk ID Transaksi {self.selected_id_pinjam}?\n(Denda otomatis dihitung).", "Konfirmasi Laporan Kembali")
        if konfirm == "Yes":
            # EXCEPTION HANDLING
            try:
                self.facade.peminjaman_service.kembalikan_buku(self.selected_id_pinjam)
                self._load_data()
                self._refresh_combos()  # Kembalikan stok buku ke ComboBox
                ToastNotification(title="Pengembalian Selesai", message="Buku resmi dikembalikan, kuota stok diperbarui dan denda dikalkulasi final.", duration=3000, bootstyle="success").show_toast()
            except AppError as e:
                Messagebox.show_error(str(e), "Kegagalan Sistem")
            except Exception as e:
                print(f"[System Log] Error tidak terduga pada Kembalikan Buku: {e}")
                Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _go_dashboard(self):
        from perpus_app.views.dashboard_frame import DashboardFrame
        self.master.show_frame(DashboardFrame)
