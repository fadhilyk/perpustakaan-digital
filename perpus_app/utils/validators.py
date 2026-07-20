# INPUT VALIDASI
import re
from datetime import datetime

# INPUT VALIDASI
def validasi_teks(teks: str, nama_field: str) -> tuple[bool, str]:
    if not teks or not str(teks).strip():
        return False, f"{nama_field} tidak boleh kosong."
    teks = str(teks).strip()
    if len(teks) < 2 or len(teks) > 100:
        return False, f"Panjang {nama_field} harus antara 2 dan 100 karakter."
    return True, ""

# INPUT VALIDASI
def validasi_email(email: str) -> tuple[bool, str]:
    if not email or not str(email).strip():
        return False, "Email tidak boleh kosong."
    email = str(email).strip()
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        return False, "Format email tidak valid."
    return True, ""

# INPUT VALIDASI
def validasi_no_telepon(no_telepon: str) -> tuple[bool, str]:
    if not no_telepon or not str(no_telepon).strip():
        return False, "No. Telepon tidak boleh kosong."
    no_telepon = str(no_telepon).strip()
    if not no_telepon.isdigit():
        return False, "No. Telepon hanya boleh berisi angka."
    if len(no_telepon) < 8 or len(no_telepon) > 15:
        return False, "Panjang No. Telepon harus antara 8 dan 15 digit."
    return True, ""

# INPUT VALIDASI
def validasi_tahun_terbit(tahun: int | str) -> tuple[bool, str]:
    if tahun is None or not str(tahun).strip():
        return False, "Tahun terbit tidak boleh kosong."
    # EXCEPTION HANDLING
    try:
        tahun_int = int(tahun)
    except ValueError:
        return False, "Tahun terbit harus berupa angka."
    
    tahun_sekarang = datetime.now().year
    if tahun_int < 1400 or tahun_int > tahun_sekarang:
        return False, f"Tahun terbit harus antara 1400 dan {tahun_sekarang}."
    return True, ""

# INPUT VALIDASI
def validasi_stok(stok: int | str) -> tuple[bool, str]:
    if stok is None or not str(stok).strip():
        return False, "Stok tidak boleh kosong."
    # EXCEPTION HANDLING
    try:
        stok_int = int(stok)
    except ValueError:
        return False, "Stok harus berupa angka."
    
    if stok_int < 0:
        return False, "Stok tidak boleh kurang dari 0."
    return True, ""

# INPUT VALIDASI
def validasi_username(username: str) -> tuple[bool, str]:
    if not username or not str(username).strip():
        return False, "Username tidak boleh kosong."
    username = str(username).strip()
    if " " in username:
        return False, "Username tidak boleh mengandung spasi."
    if not username.isalnum():
        return False, "Username hanya boleh berisi huruf dan angka."
    # Pengecekan unik akan dilakukan di tingkat Service
    return True, ""

# INPUT VALIDASI
def validasi_password(password: str, konfirmasi_password: str) -> tuple[bool, str]:
    if not password:
        return False, "Password tidak boleh kosong."
    if len(password) < 8:
        return False, "Password minimal 8 karakter."
    if not re.search(r"[A-Z]", password):
        return False, "Password harus mengandung minimal 1 huruf kapital (A-Z)."
    if not re.search(r"[0-9]", password):
        return False, "Password harus mengandung minimal 1 angka (0-9)."
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':,.<>?/\\|`~]", password):
        return False, "Password harus mengandung minimal 1 karakter simbol (contoh: @, _, !, #)."
    if password != konfirmasi_password:
        return False, "Password dan konfirmasi password tidak cocok."
    return True, ""

# INPUT VALIDASI
def validasi_pilihan(pilihan, nama_field: str) -> tuple[bool, str]:
    if not pilihan or str(pilihan).strip() == "":
         return False, f"{nama_field} wajib dipilih."
    return True, ""
