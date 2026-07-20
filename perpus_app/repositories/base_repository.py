import json
import os
from abc import ABC, abstractmethod
from typing import Any
from perpus_app.exceptions.app_exceptions import PenyimpananError

class BaseRepository(ABC):
    def __init__(self, filepath: str):
        self._filepath = filepath

    @abstractmethod
    def load(self) -> list[dict[str, Any]]:
        if not os.path.exists(self._filepath):
            # Jika file tidak ada, asumsikan datanya kosong (mencegah crash)
            return []
            
        try:
            with open(self._filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    # Kita asumsikan semua penyimpanan berbasis JSON list of objects
                    raise PenyimpananError(f"Format JSON pada {self._filepath} harus berupa list (array).")
                return data
                
        except json.JSONDecodeError as e:
            raise PenyimpananError(f"File JSON corrupt atau rusak ({self._filepath}). Detail: {e}")
        except PermissionError:
            raise PenyimpananError(f"Tidak ada izin akses untuk membaca file: {self._filepath}.")
        except Exception as e:
            # Pengecualian lain jika FileNotFoundError lolos atau hal lainnya
            raise PenyimpananError(f"Gagal memuat data dari file {self._filepath}: {e}")

    @abstractmethod
    def save(self, data: list[dict[str, Any]]) -> None:
        try:
            os.makedirs(os.path.dirname(self._filepath), exist_ok=True)
            with open(self._filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
                
        except PermissionError:
            raise PenyimpananError(f"Tidak ada izin akses untuk menulis ke file: {self._filepath}.")
        except Exception as e:
            raise PenyimpananError(f"Gagal menyimpan data ke file {self._filepath}: {e}")
