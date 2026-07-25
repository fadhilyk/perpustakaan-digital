import os
from PIL import Image, ImageTk

class IconManager:

    _icons = {}
    
    @classmethod
    def get_icon(cls, name, size=(24, 24)):

        key = f"{name}_{size[0]}x{size[1]}"
        if key in cls._icons:
            return cls._icons[key]
            
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons', f"{name}.png")
        
        if not os.path.exists(icon_path):
            print(f"[Warning] Icon not found: {icon_path}")
            return None
            
        try:
            img = Image.open(icon_path)
            if img.size != size:
                img = img.resize(size, Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(img)
            cls._icons[key] = photo
            return photo
        except Exception as e:
            print(f"[Error] Failed to load icon {name}: {e}")
            return None
