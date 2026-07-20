import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
from perpus_app.exceptions.app_exceptions import AppError
from perpus_app.utils.ui_helpers import setup_empty_state, toggle_empty_state

class BukuFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.facade = facade
        
        self.kategori_list = self.facade.kategori_service.get_all()

        self.selected_id = None
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # 1. Header
        frame_header = ttk.Frame(self)
        frame_header.pack(fill="x", padx=20, pady=10)
        ttk.Label(frame_header, text="Kelola Data Buku", font=("Helvetica", 20, "bold")).pack(side="left")
        ttk.Button(frame_header, text="⬅ Kembali ke Dashboard", bootstyle="danger", command=self._go_dashboard).pack(side="right")

        # 2. Main Content Split
        frame_content = ttk.Frame(self)
        frame_content.pack(fill="both", expand=True, padx=20, pady=10)

        # 2a. Kiri: Form Buku
        frame_form = ttk.Labelframe(frame_content, text="Form Detail Buku", padding=15)
        frame_form.pack(side="left", fill="y", padx=(0, 15))
        
        ttk.Label(frame_form, text="Judul Buku").pack(anchor="w", pady=(5, 2))
        self.ent_judul = ttk.Entry(frame_form, width=35)
        self.ent_judul.pack(fill="x", pady=(0, 5))
        
        ttk.Label(frame_form, text="Penulis").pack(anchor="w", pady=(5, 2))
        self.ent_penulis = ttk.Entry(frame_form, width=35)
        self.ent_penulis.pack(fill="x", pady=(0, 5))
        
        ttk.Label(frame_form, text="Penerbit").pack(anchor="w", pady=(5, 2))
        self.ent_penerbit = ttk.Entry(frame_form, width=35)
        self.ent_penerbit.pack(fill="x", pady=(0, 5))
        
        ttk.Label(frame_form, text="Tahun Terbit").pack(anchor="w", pady=(5, 2))
        self.ent_tahun = ttk.Entry(frame_form, width=35)
        self.ent_tahun.pack(fill="x", pady=(0, 5))
        
        ttk.Label(frame_form, text="Stok").pack(anchor="w", pady=(5, 2))
        self.ent_stok = ttk.Entry(frame_form, width=35)
        self.ent_stok.pack(fill="x", pady=(0, 5))
        
        # Combobox Kategori yang bersumber ketat dari list dinamis
        ttk.Label(frame_form, text="Kategori").pack(anchor="w", pady=(5, 2))
        cb_values = [f"{k.id_kategori} - {k.nama_kategori}" for k in self.kategori_list]
        self.cb_kategori = ttk.Combobox(frame_form, values=cb_values, state="readonly")
        self.cb_kategori.pack(fill="x", pady=(0, 15))

        # Action Buttons
        frame_action = ttk.Frame(frame_form)
        frame_action.pack(fill="x", pady=10)
        ttk.Button(frame_action, text="Tambah", bootstyle="success", command=self._on_tambah).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(frame_action, text="Update", bootstyle="warning", command=self._on_update).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(frame_action, text="Hapus", bootstyle="danger", command=self._on_hapus).pack(side="left", expand=True, fill="x", padx=2)
        
        ttk.Button(frame_form, text="Bersihkan Pilihan", bootstyle="outline-secondary", command=self._clear_form).pack(fill="x", pady=5)

        # 2b. Kanan: Search & Table
        frame_kanan = ttk.Frame(frame_content)
        frame_kanan.pack(side="right", fill="both", expand=True)

        frame_search = ttk.Frame(frame_kanan)
        frame_search.pack(fill="x", pady=(0, 10))
        ttk.Label(frame_search, text="Pencarian (Judul/Penulis/Kategori):").pack(side="left", padx=(0, 10))
        self.ent_search = ttk.Entry(frame_search, width=40)
        self.ent_search.pack(side="left", padx=(0, 5))
        ttk.Button(frame_search, text="Cari", bootstyle="info", command=self._on_search).pack(side="left", padx=2)
        ttk.Button(frame_search, text="Reset", bootstyle="secondary outline", command=self._load_data).pack(side="left", padx=2)

        columns = ("id", "judul", "penulis", "penerbit", "tahun", "stok", "kategori", "status")
        self.tree = ttk.Treeview(frame_kanan, columns=columns, show="headings", bootstyle="info")
        self.tree.heading("id", text="ID")
        self.tree.heading("judul", text="Judul")
        self.tree.heading("penulis", text="Penulis")
        self.tree.heading("penerbit", text="Penerbit")
        self.tree.heading("tahun", text="Tahun")
        self.tree.heading("stok", text="Stok")
        self.tree.heading("kategori", text="Kategori")
        self.tree.heading("status", text="Status")
        
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("judul", width=200)
        self.tree.column("penulis", width=120)
        self.tree.column("penerbit", width=120)
        self.tree.column("tahun", width=60, anchor="center")
        self.tree.column("stok", width=50, anchor="center")
        self.tree.column("kategori", width=120)
        self.tree.column("status", width=80, anchor="center")

        self.scrollbar = ttk.Scrollbar(frame_kanan, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        self.empty_state_frame = setup_empty_state(frame_kanan, "Belum ada Buku. Silakan tambah data baru.")
        
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _render_tabel(self, data_list):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        toggle_empty_state(self.tree, getattr(self, 'scrollbar', None), getattr(self, 'empty_state_frame', None), len(data_list) == 0)
            
        for b in data_list:
            kat_nama = b._kategori.nama_kategori if getattr(b, '_kategori', None) else "Tanpa Kategori"
            self.tree.insert("", "end", values=(
                b.id_buku, b.judul, b.penulis, b.penerbit, b.tahun, b.stok, kat_nama, b.status
            ))

    def _load_data(self):
        self.ent_search.delete(0, "end")
        buku_list = self.facade.buku_service.get_all()
        self._render_tabel(buku_list)

    def _on_search(self):
        keyword = self.ent_search.get().strip()
        if keyword:
            hasil = self.facade.buku_service.cari_buku(keyword)
            self._render_tabel(hasil)
        else:
            self._load_data()

    def _clear_form(self):
        self.selected_id = None
        self.ent_judul.delete(0, "end")
        self.ent_penulis.delete(0, "end")
        self.ent_penerbit.delete(0, "end")
        self.ent_tahun.delete(0, "end")
        self.ent_stok.delete(0, "end")
        self.cb_kategori.set('')

    def _on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            val = item["values"]
            self._clear_form()
            self.selected_id = int(val[0])
            
            # Kita mengambil data utuh dari service untuk mengisi form secara aman
            try:
                buku = self.facade.buku_service.get_by_id(self.selected_id)
                self.ent_judul.insert(0, buku.judul)
                self.ent_penulis.insert(0, buku.penulis)
                self.ent_penerbit.insert(0, buku.penerbit)
                self.ent_tahun.insert(0, str(buku.tahun))
                self.ent_stok.insert(0, str(buku.stok))
                
                # Meng-sinkronkan combobox kategori dengan data asli
                kategori_str = f"{buku.id_kategori} - {buku._kategori.nama_kategori}" if getattr(buku, '_kategori', None) else ""
                if kategori_str in self.cb_kategori['values']:
                    self.cb_kategori.set(kategori_str)
            except AppError:
                pass

    def _get_form_data(self):
        judul = self.ent_judul.get().strip()
        penulis = self.ent_penulis.get().strip()
        penerbit = self.ent_penerbit.get().strip()
        
        try:
            tahun = int(self.ent_tahun.get().strip())
        except ValueError:
            raise AppError("Input 'Tahun' harus berupa format angka bulat (misal: 2023).")
            
        try:
            stok = int(self.ent_stok.get().strip())
        except ValueError:
            raise AppError("Input 'Stok' harus berupa angka numerik.")
            
        kat_val = self.cb_kategori.get()
        if not kat_val:
            raise AppError("Silakan tentukan Kategori melalui pilihan dropdown Combobox.")
            
        # Ekstrak digit pertama dari pola "ID - Nama"
        id_kategori = int(kat_val.split(" - ")[0])
        return judul, penulis, penerbit, tahun, stok, id_kategori

    def _on_tambah(self):
        try:
            judul, penulis, penerbit, tahun, stok, id_kategori = self._get_form_data()
            self.facade.buku_service.tambah_buku(judul, penulis, penerbit, tahun, stok, id_kategori)
            self._clear_form()
            self._load_data()
            ToastNotification(title="Berhasil", message="Buku berhasil ditambahkan.", duration=3000, bootstyle="success").show_toast()
        except AppError as e:
            Messagebox.show_error(str(e), "Penolakan Validasi")
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Tambah/Update Buku: {e}")
            Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _on_update(self):
        if not self.selected_id:
            Messagebox.show_warning("Tentukan buku mana yang mau diupdate dengan mengekliknya di tabel.", "Pemilihan Wajib")
            return
            
        try:
            judul, penulis, penerbit, tahun, stok, id_kategori = self._get_form_data()
            self.facade.buku_service.update_buku(self.selected_id, judul, penulis, penerbit, tahun, stok, id_kategori)
            self._clear_form()
            self._load_data()
            ToastNotification(title="Berhasil", message="Buku berhasil diperbarui.", duration=3000, bootstyle="success").show_toast()
        except AppError as e:
            Messagebox.show_error(str(e), "Penolakan Validasi")
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Tambah/Update Buku: {e}")
            Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _on_hapus(self):
        if not self.selected_id:
            Messagebox.show_warning("Pilih buku dari tabel terlebih dahulu.", "Peringatan")
            return
            
        konfirm = Messagebox.yesno(f"Anda yakin akan menghapus data buku ID {self.selected_id}?", "Verifikasi Hapus")
        if konfirm == "Yes":
            try:
                self.facade.buku_service.hapus_buku(self.selected_id)
                self._clear_form()
                self._load_data()
                ToastNotification(title="Dihapus", message="Rekam jejak buku berhasil dihapus.", duration=3000, bootstyle="warning").show_toast()
            except AppError as e:
                Messagebox.show_error(str(e), "Gagal Menghapus")
            except Exception as e:
                print(f"[System Log] Error tidak terduga pada Hapus Buku: {e}")
                Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _go_dashboard(self):
        from perpus_app.views.dashboard_frame import DashboardFrame
        self.master.show_frame(DashboardFrame)
