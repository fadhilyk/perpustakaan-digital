import os
from typing import Any
from perpus_app.repositories.base_repository import BaseRepository
from perpus_app.config import DATA_DIR

class PetugasRepository(BaseRepository):
    def __init__(self):
        super().__init__(os.path.join(DATA_DIR, "petugas.json"))

    def load(self) -> list[dict[str, Any]]:
        return super().load()
        
    def save(self, data: list[dict[str, Any]]) -> None:
        super().save(data)
