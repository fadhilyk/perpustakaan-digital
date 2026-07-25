import os
from PIL import Image, ImageDraw

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'icons')

def create_icon(name, draw_func):
    if not os.path.exists(ICON_DIR):
        os.makedirs(ICON_DIR)
    
    path = os.path.join(ICON_DIR, f"{name}.png")
    if os.path.exists(path):
        return path
        
    img = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw_func(draw)
    
    img = img.resize((24, 24), Image.Resampling.LANCZOS)
    img.save(path)
    return path

def draw_dashboard(draw):
    color = (255, 255, 255, 255)
    draw.rounded_rectangle([8, 8, 28, 28], radius=4, fill=color)
    draw.rounded_rectangle([36, 8, 56, 28], radius=4, fill=color)
    draw.rounded_rectangle([8, 36, 28, 56], radius=4, fill=color)
    draw.rounded_rectangle([36, 36, 56, 56], radius=4, fill=color)

def draw_book(draw):
    color = (255, 255, 255, 255)
    draw.rounded_rectangle([12, 8, 52, 56], radius=4, fill=color)
    draw.line([24, 8, 24, 56], fill=(0,0,0,0), width=4)
    draw.line([32, 16, 44, 16], fill=(0,0,0,0), width=4)
    draw.line([32, 28, 44, 28], fill=(0,0,0,0), width=4)

def draw_users(draw):
    color = (255, 255, 255, 255)
    draw.ellipse([12, 10, 32, 30], fill=color)
    draw.ellipse([4, 34, 40, 60], fill=color)
    draw.ellipse([36, 16, 52, 32], fill=color)
    draw.ellipse([32, 36, 60, 60], fill=color)

def draw_tags(draw):
    color = (255, 255, 255, 255)
    draw.polygon([12, 32, 32, 12, 56, 12, 56, 36, 36, 56], fill=color)
    draw.ellipse([40, 20, 48, 28], fill=(0,0,0,0)) # Hole

def draw_logout(draw):
    color = (255, 255, 255, 255)
    draw.line([24, 12, 12, 12, 12, 52, 24, 52], fill=color, width=6)
    draw.line([24, 32, 52, 32], fill=color, width=6)
    draw.polygon([44, 20, 44, 44, 56, 32], fill=color)

def generate_all():
    create_icon("dashboard", draw_dashboard)
    create_icon("books", draw_book)
    create_icon("users", draw_users)
    create_icon("tags", draw_tags)
    create_icon("logout", draw_logout)

if __name__ == "__main__":
    generate_all()
    print("Icons generated successfully!")
