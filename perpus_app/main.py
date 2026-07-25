import os
import json
from perpus_app.config import DATA_DIR
from perpus_app.services.perpustakaan import Perpustakaan
from perpus_app.views.app import PerpustakaanApp
from perpus_app.views.register_petugas_frame import RegisterPetugasFrame
from perpus_app.views.login_frame import LoginFrame

def main():
    perpus = Perpustakaan()
    
    start_frame = LoginFrame
    path_petugas = os.path.join(DATA_DIR, "petugas.json")
    
    if not os.path.exists(path_petugas):
        start_frame = RegisterPetugasFrame
    else:
        try:
            with open(path_petugas, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list) or len(data) == 0:
                    start_frame = RegisterPetugasFrame
        except Exception:
            start_frame = RegisterPetugasFrame
            
    app = PerpustakaanApp(facade=perpus, start_frame_class=start_frame)
    app.mainloop()

if __name__ == "__main__":
    main()
