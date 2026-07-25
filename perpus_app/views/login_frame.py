import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from perpus_app.exceptions.app_exceptions import AppError

class LoginFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.facade = facade
        self.master = master
        self._show_password = False
        self._build_ui()

    def _build_ui(self):
        self.outer = ttk.Frame(self)
        self.outer.place(relx=0.5, rely=0.5, anchor="center")

        card = ttk.Frame(self.outer, padding=(40, 30), relief="groove", borderwidth=2)
        card.pack()

        ttk.Label(
            card, text="◈",
            font=("Helvetica", 40, "bold"),
            bootstyle="info"
        ).pack()
        ttk.Label(
            card, text="Perpustakaan Digital",
            font=("Helvetica", 10),
        ).pack(pady=(0, 2))
        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=(10, 16))
        ttk.Label(
            card, text="Login Petugas",
            font=("Helvetica", 18, "bold")
        ).pack(pady=(0, 20))

        frame_form = ttk.Frame(card)
        frame_form.pack(fill="x")

        ttk.Label(frame_form, text="Username").pack(anchor="w")
        self.ent_username = ttk.Entry(frame_form, width=38)
        self.ent_username.pack(fill="x", pady=(0, 14))

        ttk.Label(frame_form, text="Password").pack(anchor="w")
        frame_pwd = ttk.Frame(frame_form)
        frame_pwd.pack(fill="x", pady=(0, 6))

        self.ent_password = ttk.Entry(frame_pwd, width=32, show="*")
        self.ent_password.pack(side="left", fill="x", expand=True)

        self.btn_toggle = ttk.Button(
            frame_pwd, text="◉", width=3,
            bootstyle="secondary outline",
            command=self._toggle_password
        )
        self.btn_toggle.pack(side="left", padx=(6, 0))

        self.ent_username.bind("<Return>", lambda e: self._on_login())
        self.ent_password.bind("<Return>", lambda e: self._on_login())

        self.lbl_error = ttk.Label(card, text="", bootstyle="danger", font=("Helvetica", 9))
        self.lbl_error.pack(pady=(4, 0))

        ttk.Button(
            card, text="Masuk",
            bootstyle="success",
            command=self._on_login
        ).pack(fill="x", pady=(10, 8))

        ttk.Button(
            card, text="Daftar Petugas Baru",
            bootstyle="link",
            command=self._go_register
        ).pack()

    def _toggle_password(self):
        self._show_password = not self._show_password
        if self._show_password:
            self.ent_password.config(show="")
            self.btn_toggle.config(text="◎")  # Ikon "mata terbuka"
        else:
            self.ent_password.config(show="*")
            self.btn_toggle.config(text="◉")  # Ikon "mata tertutup"

    def _on_login(self):
        self.lbl_error.config(text="")
        username = self.ent_username.get().strip()
        password = self.ent_password.get()

        try:
            petugas = self.facade.petugas_service.login(username, password)
            self.facade.petugas_aktif = petugas
            from perpus_app.views.dashboard_frame import DashboardFrame
            self.master.show_frame(DashboardFrame)

        except AppError as e:
            self.lbl_error.config(text=str(e))
            self._shake()
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Login Petugas: {e}")
            self.lbl_error.config(text="Terjadi kesalahan internal sistem.")
            self._shake()

    def _shake(self):
        offsets = [0.02, -0.02, 0.016, -0.016, 0.01, -0.01, 0.005, -0.005, 0.0]
        self._shake_step(offsets, 0)

    def _shake_step(self, offsets, idx):
        if not self.winfo_exists():
            return
        if idx >= len(offsets):
            self.outer.place(relx=0.5, rely=0.5, anchor="center")
            return
        self.outer.place(relx=0.5 + offsets[idx], rely=0.5, anchor="center")
        self.after(45, lambda: self._shake_step(offsets, idx + 1))

    def _go_register(self):
        from perpus_app.views.register_petugas_frame import RegisterPetugasFrame
        self.master.show_frame(RegisterPetugasFrame)
