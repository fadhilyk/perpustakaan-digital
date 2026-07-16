from typing import Any

def generate_id(items: list[Any], id_property: str) -> int:
    """
    Generate auto-increment ID berdasarkan sekumpulan item yang sudah ada.
    Dapat menerima list of dictionary (data JSON mentah) atau list of object (data model).
    
    Args:
        items: List item yang ada.
        id_property: Nama atribut atau key yang menyimpan ID (misal: 'id_buku', 'id_pengguna').
        
    Returns:
        int: ID baru yang dihasilkan.
    """
    if not items:
        return 1
        
    ids = []
    for item in items:
        if isinstance(item, dict):
            if id_property in item:
                try:
                    ids.append(int(item[id_property]))
                except (ValueError, TypeError):
                    pass
        elif hasattr(item, id_property):
            try:
                ids.append(int(getattr(item, id_property)))
            except (ValueError, TypeError):
                pass
            
    if not ids:
        return 1
        
    return max(ids) + 1
