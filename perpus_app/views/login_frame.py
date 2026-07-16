import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from perpus_app.exceptions.app_exceptions import AppError

class LoginFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.facade = facade
        self.master = master
        self._build_ui()

    def _build_ui(self):
        container = ttk.Frame(self)
        container.pack(expand=True)

        ttk.Label(container, text="Login Petugas", font=("Helvetica", 22, "bold")).pack(pady=(0, 30))

        frame_form = ttk.Frame(container)
        frame_form.pack(fill="x", pady=10)

        ttk.Label(frame_form, text="Username").pack(anchor="w")
        self.ent_username = ttk.Entry(frame_form, width=40)
        self.ent_username.pack(fill="x", pady=(0, 15))

        ttk.Label(frame_form, text="Password").pack(anchor="w")
        self.ent_password = ttk.Entry(frame_form, width=40, show="*")
        self.ent_password.pack(fill="x")

        # Label Error Inline (default text kosong)
        self.lbl_error = ttk.Label(container, text="", bootstyle="danger")
        self.lbl_error.pack(pady=10)

        btn_login = ttk.Button(container, text="Masuk", bootstyle="success", command=self._on_login)
        btn_login.pack(fill="x", pady=(5, 15))
        
        btn_register = ttk.Button(container, text="Daftar Petugas Baru", bootstyle="link", command=self._go_register)
        btn_register.pack()

    def _on_login(self):
        self.lbl_error.config(text="")
        username = self.ent_username.get().strip()
        password = self.ent_password.get()
        
        try:
            petugas = self.facade.petugas_service.login(username, password)
            # Simpan sesi (session) petugas aktif di facade agar bisa diakses modul lain
            self.facade.petugas_aktif = petugas
            
            # Berpindah ke menu utama
            from perpus_app.views.dashboard_frame import DashboardFrame
            self.master.show_frame(DashboardFrame)
            
        except AppError as e:
            self.lbl_error.config(text=str(e))
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Login Petugas: {e}")
            self.lbl_error.config(text="Terjadi kesalahan internal sistem.")

    def _go_register(self):
        from perpus_app.views.register_petugas_frame import RegisterPetugasFrame
        self.master.show_frame(RegisterPetugasFrame)
