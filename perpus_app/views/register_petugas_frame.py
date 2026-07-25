import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.toast import ToastNotification
from perpus_app.exceptions.app_exceptions import AppError

class RegisterPetugasFrame(ttk.Frame):
    def __init__(self, master, facade, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.facade = facade
        self.master = master
        self._show_password = False
        self._show_konfirm  = False
        self._build_ui()

    def _build_ui(self):
        outer = ttk.Frame(self)
        outer.place(relx=0.5, rely=0.5, anchor="center")

        card = ttk.Frame(outer, padding=(40, 25), relief="groove", borderwidth=2)
        card.pack()

        ttk.Label(
            card, text="◈",
            font=("Helvetica", 36, "bold"),
            bootstyle="info"
        ).pack()
        ttk.Label(
            card, text="Perpustakaan Digital",
            font=("Helvetica", 10),
        ).pack(pady=(0, 2))
        ttk.Separator(card, orient="horizontal").pack(fill="x", pady=(10, 14))
        ttk.Label(
            card, text="Registrasi Petugas",
            font=("Helvetica", 16, "bold")
        ).pack(pady=(0, 16))

        frame_form = ttk.Frame(card)
        frame_form.pack(fill="x")

        def lbl(row, text):
            ttk.Label(frame_form, text=text).grid(
                row=row, column=0, sticky="w", pady=4, padx=(0, 12)
            )

        lbl(0, "Nama")
        self.ent_nama = ttk.Entry(frame_form, width=36)
        self.ent_nama.grid(row=0, column=1, pady=4, sticky="ew")

        lbl(1, "No. Telepon")
        self.ent_notelp = ttk.Entry(frame_form, width=36)
        self.ent_notelp.grid(row=1, column=1, pady=4, sticky="ew")

        lbl(2, "Email")
        self.ent_email = ttk.Entry(frame_form, width=36)
        self.ent_email.grid(row=2, column=1, pady=4, sticky="ew")

        lbl(3, "Jabatan")
        self.ent_jabatan = ttk.Entry(frame_form, width=36)
        self.ent_jabatan.insert(0, "Administrator")
        self.ent_jabatan.configure(state="readonly")
        self.ent_jabatan.grid(row=3, column=1, pady=4, sticky="ew")

        lbl(4, "Username")
        self.ent_username = ttk.Entry(frame_form, width=36)
        self.ent_username.grid(row=4, column=1, pady=4, sticky="ew")

        lbl(5, "Password")
        frame_pwd = ttk.Frame(frame_form)
        frame_pwd.grid(row=5, column=1, pady=4, sticky="ew")
        self.ent_password = ttk.Entry(frame_pwd, show="*")
        self.ent_password.pack(side="left", expand=True, fill="x")
        self.btn_toggle_pwd = ttk.Button(
            frame_pwd, text="◉", width=3,
            bootstyle="secondary outline",
            command=self._toggle_password
        )
        self.btn_toggle_pwd.pack(side="right", padx=(6, 0))

        lbl(6, "Konfirmasi")
        frame_konfirm = ttk.Frame(frame_form)
        frame_konfirm.grid(row=6, column=1, pady=4, sticky="ew")
        self.ent_konfirm = ttk.Entry(frame_konfirm, show="*")
        self.ent_konfirm.pack(side="left", expand=True, fill="x")
        self.btn_toggle_konfirm = ttk.Button(
            frame_konfirm, text="◉", width=3,
            bootstyle="secondary outline",
            command=self._toggle_konfirm
        )
        self.btn_toggle_konfirm.pack(side="right", padx=(6, 0))

        hint_text = "  ◆ Min. 8 karakter  ◆ Huruf kapital (A-Z)  ◆ Angka (0-9)  ◆ Simbol (@, _, !, #, ...)"
        ttk.Label(
            frame_form,
            text=hint_text,
            font=("Helvetica", 8, "italic"),
            bootstyle="secondary"
        ).grid(row=7, column=0, columnspan=2, sticky="w", pady=(2, 4))

        self.lbl_error = ttk.Label(card, text="", bootstyle="danger", font=("Helvetica", 9))
        self.lbl_error.pack(pady=(10, 0))

        ttk.Button(
            card, text="Daftar",
            bootstyle="primary",
            command=self._on_submit
        ).pack(fill="x", pady=(10, 6))

        ttk.Button(
            card, text="Kembali ke Halaman Login",
            bootstyle="link",
            command=self._go_login
        ).pack()

    def _toggle_password(self):
        self._show_password = not self._show_password
        if self._show_password:
            self.ent_password.config(show="")
            self.btn_toggle_pwd.config(text="◎")
        else:
            self.ent_password.config(show="*")
            self.btn_toggle_pwd.config(text="◉")

    def _toggle_konfirm(self):
        self._show_konfirm = not self._show_konfirm
        if self._show_konfirm:
            self.ent_konfirm.config(show="")
            self.btn_toggle_konfirm.config(text="◎")
        else:
            self.ent_konfirm.config(show="*")
            self.btn_toggle_konfirm.config(text="◉")

    def _on_submit(self):
        self.lbl_error.config(text="")

        nama     = self.ent_nama.get().strip()
        notelp   = self.ent_notelp.get().strip()
        email    = self.ent_email.get().strip()
        jabatan  = self.ent_jabatan.get().strip()
        username = self.ent_username.get().strip()
        password = self.ent_password.get()
        konfirm  = self.ent_konfirm.get()

        try:
            self.facade.petugas_service.registrasi(
                nama, notelp, email, jabatan, username, password, konfirm
            )
            ToastNotification(title="Sukses", message="Registrasi berhasil! Silakan login dengan akun yang dibuat.", duration=3000, bootstyle="success").show_toast()
            self._go_login()
        except AppError as e:
            self.lbl_error.config(text=str(e))
        except Exception as e:
            print(f"[System Log] Error tidak terduga pada Registrasi Petugas: {e}")
            self.lbl_error.config(text="Terjadi kesalahan internal sistem.")

    def _go_login(self):
        from perpus_app.views.login_frame import LoginFrame
        self.master.show_frame(LoginFrame)
