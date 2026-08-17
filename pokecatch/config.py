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
    "Common": 50,
    "Uncommon": 100,
    "Rare": 500,
    "UltraRare": 800,
    "Epic": 1500,
    "Legendary": 5000,
    "Mythical": 10000
}

RARITY_SPAWN_WEIGHTS = {
    "Common": 40,
    "Uncommon": 30,
    "Rare": 15,
    "UltraRare": 10,
    "Epic": 3,
    "Legendary": 1.5,
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
    "pb": "poke_ball",
    "gb": "great_ball",
    "ub": "ultra_ball",
    "net": "net_ball",
    "dive": "dive_ball",
    "fast": "fast_ball",
    "dusk": "dusk_ball",
    "nest": "nest_ball",
    "repeat": "repeat_ball",
    "quick": "quick_ball",
    "mb": "master_ball"
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