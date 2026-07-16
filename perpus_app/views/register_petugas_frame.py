import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from perpus_app.exceptions.app_exceptions import AppError

class RegisterPetugasFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.facade = facade
        self.master = master
        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self)
        container.pack(expand=True)

        ttk.Label(container, text="Registrasi Petugas", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        ttk.Label(container, text="Nama").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.ent_nama = ttk.Entry(container, width=40)
        self.ent_nama.grid(row=1, column=1, pady=5, padx=5)

        ttk.Label(container, text="No. Telepon").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.ent_notelp = ttk.Entry(container, width=40)
        self.ent_notelp.grid(row=2, column=1, pady=5, padx=5)

        ttk.Label(container, text="Email").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.ent_email = ttk.Entry(container, width=40)
        self.ent_email.grid(row=3, column=1, pady=5, padx=5)

        ttk.Label(container, text="Jabatan").grid(row=4, column=0, sticky="w", pady=5, padx=5)
        self.ent_jabatan = ttk.Entry(container, width=40)
        self.ent_jabatan.grid(row=4, column=1, pady=5, padx=5)

        ttk.Label(container, text="Username").grid(row=5, column=0, sticky="w", pady=5, padx=5)
        self.ent_username = ttk.Entry(container, width=40)
        self.ent_username.grid(row=5, column=1, pady=5, padx=5)

        ttk.Label(container, text="Password").grid(row=6, column=0, sticky="w", pady=5, padx=5)
        self.ent_password = ttk.Entry(container, width=40, show="*")
        self.ent_password.grid(row=6, column=1, pady=5, padx=5)

        ttk.Label(container, text="Konfirmasi").grid(row=7, column=0, sticky="w", pady=5, padx=5)
        self.ent_konfirm = ttk.Entry(container, width=40, show="*")
        self.ent_konfirm.grid(row=7, column=1, pady=5, padx=5)

        # Label Error Inline (default text kosong)
        self.lbl_error = ttk.Label(container, text="", bootstyle="danger")
        self.lbl_error.grid(row=8, column=0, columnspan=2, pady=10)

        btn_submit = ttk.Button(container, text="Daftar", bootstyle="primary", command=self._on_submit)
        btn_submit.grid(row=9, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        
        # Opsi ke layar login (bagi yang ingin mendaftarkan petugas berikutnya)
        btn_login = ttk.Button(container, text="Kembali ke Halaman Login", bootstyle="link", command=self._go_login)
        btn_login.grid(row=10, column=0, columnspan=2, pady=5)

    def _on_submit(self):
        # Reset pesan error
        self.lbl_error.config(text="")
        
        nama = self.ent_nama.get().strip()
        notelp = self.ent_notelp.get().strip()
        email = self.ent_email.get().strip()
        jabatan = self.ent_jabatan.get().strip()
        username = self.ent_username.get().strip()
        password = self.ent_password.get()
        konfirm = self.ent_konfirm.get()

        try:
            self.facade.petugas_service.registrasi(nama, notelp, email, jabatan, username, password, konfirm)
            Messagebox.show_info("Registrasi berhasil! Silakan login dengan akun yang dibuat.", "Sukses")
            self._go_login()
        except AppError as e:
            # Tampilkan pesan error secara inline
            self.lbl_error.config(text=str(e))
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Registrasi Petugas: {e}")
            self.lbl_error.config(text="Terjadi kesalahan internal sistem.")

    def _go_login(self):
        from perpus_app.views.login_frame import LoginFrame
        self.master.show_frame(LoginFrame)
