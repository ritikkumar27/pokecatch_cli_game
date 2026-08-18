import os
from pathlib import Path

# --- File Paths ---
PKG_DIR = Path(__file__).parent

# Static assets (these are now bundled inside the game package)
DATA_DIR = PKG_DIR / "data"
SPRITES_DIR = PKG_DIR / "sprites/pokemons"
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
    "Common": 150,
    "Uncommon": 300,
    "Rare": 800,
    "UltraRare": 1500,
    "Epic": 3000,
    "Legendary": 10000,
    "Mythical": 25000
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
    "poke_ball" : 50,
    "great_ball": 150,
    "ultra_ball": 300,
    "net_ball": 250,
    "dive_ball": 250,
    "fast_ball": 250,
    "dusk_ball": 250,
    "nest_ball": 250,
    "repeat_ball": 250,
    "quick_ball": 400,
    "master_ball": 50000
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
    "poke_ball":   {"price": 50,   "category": "balls", "unlock_level": 1},
    "great_ball":  {"price": 150,   "category": "balls", "unlock_level": 3},
    "ultra_ball":  {"price": 250,  "category": "balls", "unlock_level": 8},
    "net_ball":    {"price": 250,  "category": "balls", "unlock_level": 5},
    "dive_ball":   {"price": 250,  "category": "balls", "unlock_level": 5},
    "fast_ball":   {"price": 250,  "category": "balls", "unlock_level": 5},
    "dusk_ball":   {"price": 250,  "category": "balls", "unlock_level": 5},
    "nest_ball":   {"price": 250,  "category": "balls", "unlock_level": 10},
    "repeat_ball": {"price": 250,  "category": "balls", "unlock_level": 10},
    "quick_ball":  {"price": 400,  "category": "balls", "unlock_level": 15},
    "master_ball": {"price": 50000,"category": "special", "unlock_level": 25}
}