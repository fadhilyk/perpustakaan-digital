import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from perpus_app.exceptions.app_exceptions import AppError

class AnggotaFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.facade = facade
        
        self.selected_id = None
        self._build_ui()
        self._load_data()

    def _build_ui(self):
        # Header
        frame_header = ttk.Frame(self)
        frame_header.pack(fill="x", padx=20, pady=10)
        ttk.Label(frame_header, text="Kelola Data Anggota", font=("Helvetica", 20, "bold")).pack(side="left")
        ttk.Button(frame_header, text="Kembali ke Dashboard", bootstyle="secondary outline", command=self._go_dashboard).pack(side="right")

        # Konten Terbelah (Kiri Form, Kanan Tabel)
        frame_content = ttk.Frame(self)
        frame_content.pack(fill="both", expand=True, padx=20, pady=10)

        # KIRI: FORM
        frame_form = ttk.Labelframe(frame_content, text="Form Data Diri Anggota", padding=15)
        frame_form.pack(side="left", fill="y", padx=(0, 15))
        
        ttk.Label(frame_form, text="Nama Lengkap").pack(anchor="w", pady=(5, 2))
        self.ent_nama = ttk.Entry(frame_form, width=35)
        self.ent_nama.pack(fill="x", pady=(0, 5))
        
        ttk.Label(frame_form, text="No. Telepon").pack(anchor="w", pady=(5, 2))
        self.ent_notelp = ttk.Entry(frame_form, width=35)
        self.ent_notelp.pack(fill="x", pady=(0, 5))
        
        ttk.Label(frame_form, text="Email").pack(anchor="w", pady=(5, 2))
        self.ent_email = ttk.Entry(frame_form, width=35)
        self.ent_email.pack(fill="x", pady=(0, 5))
        
        ttk.Label(frame_form, text="Alamat Domisili").pack(anchor="w", pady=(5, 2))
        self.ent_alamat = ttk.Entry(frame_form, width=35)
        self.ent_alamat.pack(fill="x", pady=(0, 15))

        # Action Buttons
        frame_action = ttk.Frame(frame_form)
        frame_action.pack(fill="x", pady=10)
        ttk.Button(frame_action, text="Tambah", bootstyle="success", command=self._on_tambah).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(frame_action, text="Update", bootstyle="warning", command=self._on_update).pack(side="left", expand=True, fill="x", padx=2)
        ttk.Button(frame_action, text="Hapus", bootstyle="danger", command=self._on_hapus).pack(side="left", expand=True, fill="x", padx=2)
        
        ttk.Button(frame_form, text="Bersihkan Pilihan", bootstyle="outline-secondary", command=self._clear_form).pack(fill="x", pady=5)

        # KANAN: TABEL DATA ANGGOTA
        frame_kanan = ttk.Frame(frame_content)
        frame_kanan.pack(side="right", fill="both", expand=True)

        columns = ("id", "nama", "notelp", "email", "alamat")
        self.tree = ttk.Treeview(frame_kanan, columns=columns, show="headings", bootstyle="info")
        self.tree.heading("id", text="ID")
        self.tree.heading("nama", text="Nama Anggota")
        self.tree.heading("notelp", text="No. Telepon")
        self.tree.heading("email", text="Email")
        self.tree.heading("alamat", text="Alamat")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("nama", width=200)
        self.tree.column("notelp", width=120)
        self.tree.column("email", width=200)
        self.tree.column("alamat", width=250)

        scrollbar = ttk.Scrollbar(frame_kanan, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

    def _render_tabel(self, data_list):
        """Merender baris tabel, mem-bypass properti private secara aman menggunakan getter (getattr)."""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for a in data_list:
            # Karena di model _no_telepon dan _email adalah protected, getattr kita fungsikan untuk jaga-jaga
            no_telp = getattr(a, '_no_telepon', '')
            email = getattr(a, '_email', '')
            self.tree.insert("", "end", values=(
                a.id_pengguna, a.nama, no_telp, email, a.alamat
            ))

    def _load_data(self):
        """Memuat seluruh koleksi data Anggota via Service."""
        anggota_list = self.facade.anggota_service.get_all()
        self._render_tabel(anggota_list)

    def _clear_form(self):
        self.selected_id = None
        self.ent_nama.delete(0, "end")
        self.ent_notelp.delete(0, "end")
        self.ent_email.delete(0, "end")
        self.ent_alamat.delete(0, "end")

    def _on_select(self, event):
        """Remote pengisian Data ke Form ketika ada yang terpilih di tabel."""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            val = item["values"]
            self._clear_form()
            self.selected_id = int(val[0])
            self.ent_nama.insert(0, str(val[1]))
            self.ent_notelp.insert(0, str(val[2]))
            self.ent_email.insert(0, str(val[3]))
            # Handle kondisi "None" menjadi string kosong
            alamat_val = str(val[4]) if str(val[4]) != "None" else ""
            self.ent_alamat.insert(0, alamat_val)

    def _get_form_data(self):
        nama = self.ent_nama.get().strip()
        notelp = self.ent_notelp.get().strip()
        email = self.ent_email.get().strip()
        alamat = self.ent_alamat.get().strip()
        return nama, notelp, email, alamat

    def _on_tambah(self):
        try:
            nama, notelp, email, alamat = self._get_form_data()
            self.facade.anggota_service.tambah(nama, notelp, email, alamat)
            self._clear_form()
            self._load_data()
            Messagebox.show_info("Berhasil mendaftarkan anggota baru.", "Sukses")
        except AppError as e:
            Messagebox.show_error(str(e), "Pelanggaran Validasi")
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Tambah/Update Anggota: {e}")
            Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _on_update(self):
        if not self.selected_id:
            Messagebox.show_warning("Mohon pilih baris data di tabel yang mau Anda perbarui.", "Peringatan Pemilihan")
            return
        try:
            nama, notelp, email, alamat = self._get_form_data()
            self.facade.anggota_service.update(self.selected_id, nama, notelp, email, alamat)
            self._clear_form()
            self._load_data()
            Messagebox.show_info(f"Data anggota ID {self.selected_id} sukses diperbarui.", "Berhasil Diubah")
        except AppError as e:
            Messagebox.show_error(str(e), "Pelanggaran Validasi")
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Tambah/Update Anggota: {e}")
            Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _on_hapus(self):
        if not self.selected_id:
            Messagebox.show_warning("Pilih anggota yang akan Anda lenyapkan dari tabel terlebih dahulu.", "Peringatan Hapus")
            return
            
        konfirm = Messagebox.show_question(f"Anda sangat yakin untuk menghapus Anggota ID {self.selected_id} selamanya?", "Konfirmasi Eksekusi")
        if konfirm == "Yes":
            try:
                self.facade.anggota_service.hapus(self.selected_id)
                self._clear_form()
                self._load_data()
                Messagebox.show_info("Anggota berhasil terhapus sempurna.", "Penghapusan Sukses")
            except AppError as e:
                Messagebox.show_error(str(e), "Penolakan Integritas Bisnis")
            except Exception as e:
                print(f"[System Log] Error tidak terduga pada Hapus Anggota: {e}")
                Messagebox.show_error("Terjadi kesalahan internal sistem.", "Error Sistem")

    def _go_dashboard(self):
        from perpus_app.views.dashboard_frame import DashboardFrame
        self.master.show_frame(DashboardFrame)
