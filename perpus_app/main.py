import os
import json
from perpus_app.config import DATA_DIR
from perpus_app.services.perpustakaan import Perpustakaan
from perpus_app.views.app import PerpustakaanApp
from perpus_app.views.register_petugas_frame import RegisterPetugasFrame
from perpus_app.views.login_frame import LoginFrame

def main():
    # 1. Inisialisasi Composition Root (semua repository & services termuat in-memory)
    perpus = Perpustakaan()
    
    # 2. Periksa ketersediaan akun Petugas berdasarkan isi file data/petugas.json
    start_frame = LoginFrame
    path_petugas = os.path.join(DATA_DIR, "petugas.json")
    
    if not os.path.exists(path_petugas):
        start_frame = RegisterPetugasFrame
    else:
        # EXCEPTION HANDLING
        try:
            with open(path_petugas, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Jika file berupa list kosong, wajib dilempar ke menu Registrasi
                if not isinstance(data, list) or len(data) == 0:
                    start_frame = RegisterPetugasFrame
        except Exception:
            # Jika file rusak (JSONDecodeError), maka anggap belum ada
            start_frame = RegisterPetugasFrame
            
    # 3. Luncurkan Window GUI Utama
    app = PerpustakaanApp(facade=perpus, start_frame_class=start_frame)
    app.mainloop()

if __name__ == "__main__":
    main()
