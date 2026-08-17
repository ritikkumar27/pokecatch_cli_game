import os
from pathlib import Path

# --- File Paths ---
PKG_DIR = Path(__file__).parent

# Static assets (these are now bundled inside the game package)
DATA_DIR = PKG_DIR / "data"
SPRITES_DIR = PKG_DIR / "sprites"
DATA_FILE = DATA_DIR / 'pokemon_data.json'
WILD_POKEMON_STATE = DATA_DIR / 'wild_pokemon.json'


# User save data (Save to the user's home directory so progress isn't lost on updates!)
USER_SAVE_DIR = Path.home() / ".pokecatch"
USER_SAVE_DIR.mkdir(exist_ok=True)  # Automatically creates ~/.pokecatch if it doesn't exist
PLAYER_DEX = USER_SAVE_DIR / 'pokedex.json'
PLAYER_DATA_FILE = USER_SAVE_DIR / 'player.json'

# --- Game Constants ---
HUNT_COOLDOWN_SECONDS = 0



RARITY_SELL_PRICES = {
    "Common": 30,
    "Uncommon": 75,
    "Rare": 300,
    "UltraRare": 500,
    "Epic": 1000,
    "Legendary": 3500,
    "Mythical": 7500
}

RARITY_SPAWN_WEIGHTS = {
    "Common": 50.0,
    "Uncommon": 28.0,
    "Rare": 12.0,
    "UltraRare": 6.0,
    "Epic": 2.5,
    "Legendary": 1.0,
    "Mythical": 0.5
}

BALL_PRICES = {
    "poke_ball" : 200,
    "great_ball": 600,
    "ultra_ball": 1200,
    "net_ball": 1000,
    "dive_ball": 1000,
    "fast_ball": 1000,
    "dusk_ball": 1000,
    "nest_ball": 1000,
    "repeat_ball": 1000,
    "quick_ball": 1500,
    "master_ball": 100000
}

BALL_ALIASES = {
    "pb": "poke_ball", "gb": "great_ball", "ub": "ultra_ball", 
    "net": "net_ball", "dive": "dive_ball", "fast": "fast_ball", 
    "dusk": "dusk_ball", "nest": "nest_ball", "repeat": "repeat_ball", 
    "quick": "quick_ball", "mb": "master_ball"
}

BASE_CATCH_RATES = {
    "Common": 0.50,
    "Uncommon": 0.40,
    "Rare": 0.30,
    "UltraRare": 0.20,
    "Epic": 0.10,
    "Legendary": 0.05,
    "Mythical": 0.02
}

# XP granted for activities
XP_REWARDS = {
    "hunt": 5,
    "catch_Common": 10,
    "catch_Uncommon": 20,
    "catch_Rare": 50,
    "catch_UltraRare": 100,
    "catch_Epic": 200,
    "catch_Legendary": 500,
    "catch_Mythical": 1000,
}


# The new Dynamic Store System!
STORE_ITEMS = {
    "poke_ball":   {"price": 200,   "category": "balls", "unlock_level": 1,  "daily_stock": 50},
    "great_ball":  {"price": 600,   "category": "balls", "unlock_level": 3,  "daily_stock": 30},
    "ultra_ball":  {"price": 1200,  "category": "balls", "unlock_level": 8,  "daily_stock": 20},
    "net_ball":    {"price": 1000,  "category": "balls", "unlock_level": 5,  "daily_stock": 15},
    "dive_ball":   {"price": 1000,  "category": "balls", "unlock_level": 5,  "daily_stock": 15},
    "fast_ball":   {"price": 1000,  "category": "balls", "unlock_level": 5,  "daily_stock": 15},
    "dusk_ball":   {"price": 1000,  "category": "balls", "unlock_level": 5,  "daily_stock": 15},
    "nest_ball":   {"price": 1000,  "category": "balls", "unlock_level": 10, "daily_stock": 15},
    "repeat_ball": {"price": 1000,  "category": "balls", "unlock_level": 10, "daily_stock": 15},
    "quick_ball":  {"price": 1500,  "category": "balls", "unlock_level": 15, "daily_stock": 10},
    "master_ball": {"price": 100000,"category": "special", "unlock_level": 25, "daily_stock": 1}
}