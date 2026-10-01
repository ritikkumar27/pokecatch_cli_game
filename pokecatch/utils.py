import os
import json
from PIL import Image
from term_image.image import AutoImage
from pokecatch.config import SPRITES_DIR


def load_data(filepath):

    if not os.path.exists(filepath):
        return []
    
    with open(filepath, 'r') as f:
        return json.load(f)

def save_data(filepath, data):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    temp_path = filepath.with_suffix(filepath.suffix + ".tmp")
    with open(temp_path, 'w') as f:
        json.dump(data, f, indent=2)
        f.flush()
        os.fsync(f.fileno()) # Guarantee it is on the hard drive
    os.replace(temp_path, filepath) # Atomic instant replacement



def display_sprite(pokemon_name):

    sprite_path = SPRITES_DIR / f"{pokemon_name}.png"
    if not sprite_path.exists():
        print(f"Sprite for {pokemon_name} not found!")
        return

    try:
        img = Image.open(sprite_path).convert("RGBA")
        bbox = img.getchannel('A').getbbox()
        if bbox:
            img = img.crop(bbox)

        scale_factor = 1.0 #review #pokemon size #pokemonsize
        calculated_width = int((img.width * scale_factor) / 3)
        calculated_width = max(1, calculated_width)
        
        term_img = AutoImage(img, width=calculated_width)
        term_img.draw(h_align="<", pad_height=1)

    except Exception as e:
        print(f"Error displaying image: {e}")

def display_sprite_pokedex(pokemon_name):
    sprite_path = SPRITES_DIR / f"{pokemon_name}.png"
    if not sprite_path.exists():
        print(f"Sprite for {pokemon_name} not found!")
        return
    
    try:
        img = Image.open(sprite_path).convert("RGBA")
        bbox = img.getchannel('A').getbbox()
        if bbox:
            img = img.crop(bbox)
        
        scale_factor = 1.0 
        calculated_width = int((img.width * scale_factor) / 3)
        calculated_width = max(1, calculated_width)
        
        term_img = AutoImage(img, width=calculated_width)
        term_img.draw(h_align="<", pad_height=1)
        
    except Exception as e:
        print(f"Error displaying image: {e}")