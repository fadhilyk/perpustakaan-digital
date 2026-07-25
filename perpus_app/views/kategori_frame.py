import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
from perpus_app.exceptions.app_exceptions import AppError
from perpus_app.utils.ui_helpers import setup_empty_state, toggle_empty_state

class KategoriFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.facade = facade
        
        self.selected_id = None
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        frame_header = ttk.Frame(self)
        frame_header.pack(fill="x", padx=20, pady=10)
        ttk.Label(frame_header, text="Kelola Kategori Buku", font=("Helvetica", 20, "bold")).pack(side="left")
        ttk.Button(frame_header, text="⬅ Kembali ke Dashboard", bootstyle="danger", command=self._go_dashboard).pack(side="right")

        frame_content = ttk.Frame(self)
        frame_content.pack(fill="both", expand=True, padx=20, pady=10)

        frame_form = ttk.Labelframe(frame_content, text="Form Kategori", padding=15)
        frame_form.pack(side="left", fill="y", padx=(0, 15))

        ttk.Label(frame_form, text="Nama Kategori").pack(anchor="w", pady=(5, 2))
        self.ent_nama = ttk.Entry(frame_form, width=30)
        self.ent_nama.pack(fill="x", pady=(0, 10))

        ttk.Label(frame_form, text="Deskripsi").pack(anchor="w", pady=(5, 2))
        self.ent_deskripsi = ttk.Entry(frame_form, width=30)
        self.ent_deskripsi.pack(fill="x", pady=(0, 10))

        frame_action = ttk.Frame(frame_form)
        frame_action.pack(fill="x", pady=15)
        
        ttk.Button(frame_action, text="Tambah", bootstyle="success", command=self._on_tambah).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(frame_action, text="Update", bootstyle="warning", command=self._on_update).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(frame_action, text="Hapus", bootstyle="danger", command=self._on_hapus).pack(side="left", expand=True, fill="x", padx=2)
        
        ttk.Button(frame_form, text="Bersihkan Pilihan", bootstyle="outline-secondary", command=self._clear_form).pack(fill="x")

        frame_table = ttk.Frame(frame_content)
        frame_table.pack(side="right", fill="both", expand=True)
        
        columns = ("id", "nama", "deskripsi")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", bootstyle="info")
        self.tree.heading("id", text="ID")
        self.tree.heading("nama", text="Nama Kategori")
        self.tree.heading("deskripsi", text="Deskripsi")
        
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("nama", width=180)
        self.tree.column("deskripsi", width=350)
        
        self.scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.empty_state_frame = setup_empty_state(frame_table, "Belum ada Kategori. Silakan tambah data baru.")
        
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        kategori_list = self.facade.kategori_service.get_all()
        
        toggle_empty_state(self.tree, self.scrollbar, self.empty_state_frame, len(kategori_list) == 0)
        
        for k in kategori_list:
            self.tree.insert("", "end", values=(k.id_kategori, k.nama_kategori, k.deskripsi))

    def _clear_form(self):
        self.selected_id = None
        self.ent_nama.delete(0, "end")
        self.ent_deskripsi.delete(0, "end")

    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            val = item["values"]
            self._clear_form()
            self.selected_id = int(val[0])
            self.ent_nama.insert(0, val[1])
            self.ent_deskripsi.insert(0, str(val[2]) if val[2] else "")

    def _on_tambah(self):
        nama = self.ent_nama.get().strip()
        desk = self.ent_deskripsi.get().strip()
        try:
            self.facade.kategori_service.tambah(nama, desk)
            self._clear_form()
            self._load_data()
            ToastNotification(title="Berhasil", message="Kategori berhasil ditambahkan.", duration=3000, bootstyle="success").show_toast()
        except AppError as e:
            Messagebox.show_error(str(e), "Gagal Validasi")
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Kategori Tambah/Update: {e}")
            Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _on_update(self):
        if not self.selected_id:
            Messagebox.show_warning("Mohon pilih kategori yang ingin di-update dari tabel terlebih dahulu.", "Pilih Data")
            return
            
        nama = self.ent_nama.get().strip()
        desk = self.ent_deskripsi.get().strip()
        try:
            self.facade.kategori_service.update(self.selected_id, nama, desk)
            self._clear_form()
            self._load_data()
            ToastNotification(title="Berhasil", message="Kategori berhasil diperbarui.", duration=3000, bootstyle="success").show_toast()
        except AppError as e:
            Messagebox.show_error(str(e), "Gagal Validasi")

    def _on_hapus(self):
        if not self.selected_id:
            Messagebox.show_warning("Mohon pilih kategori yang ingin dihapus dari tabel terlebih dahulu.", "Pilih Data")
            return
            
        konfirm = Messagebox.yesno(f"Yakin ingin menghapus kategori dengan ID {self.selected_id}?", "Konfirmasi Penghapusan")
        if konfirm == "Yes":
            try:
                self.facade.kategori_service.hapus(self.selected_id)
                self._clear_form()
                self._load_data()
                ToastNotification(title="Dihapus", message="Kategori telah berhasil dihapus dari peredaran.", duration=3000, bootstyle="warning").show_toast()
            except AppError as e:
                Messagebox.show_error(str(e), "Tidak Dapat Dihapus")
            except Exception as e:
                print(f"[System Log] Error tidak terduga pada Hapus Kategori: {e}")
                Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _go_dashboard(self):
        from perpus_app.views.dashboard_frame import DashboardFrame
        self.master.show_frame(DashboardFrame)
