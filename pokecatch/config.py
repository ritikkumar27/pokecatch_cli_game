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



# --- File Paths ---
# ROOT_DIR points to the directory containing the 'data' and 'sprites' folders.
# Since config.py is inside the 'pokecatch' folder, the root is one level up (.parent)
# ROOT_DIR = Path(__file__).parent.parent
# DATA_DIR = ROOT_DIR / "data"
# SPRITES_DIR = ROOT_DIR / "sprites"
# DATA_FILE = DATA_DIR / 'pokemon_data.json'
# PLAYER_DEX = DATA_DIR / 'pokedex.json'
# WILD_POKEMON_STATE = DATA_DIR / 'wild_pokemon.json'
# PLAYER_DATA_FILE = DATA_DIR / 'player.json'


# --- Game Constants ---
HUNT_COOLDOWN_SECONDS = 0
RARITY_SELL_PRICES = {
    "common": 50,
    "uncommon": 100,
    "rare": 500,
    "ultrarare": 800,
    "epic": 1500,
    "legendary": 5000
}
RARITY_MODIFIERS = {
    "common": 1.0,
    "uncommon": 0.8,
    "rare": 0.6,
    "ultrarare": 0.4,
    "epic": 0.25,
    "legendary": 0.1
}
RARITY_SPAWN_WEIGHTS = {
    "common": 60,
    "uncommon": 25,
    "rare": 13,
    "ultrarare": 7,
    "epic": 3,
    "legendary": 0.7
}
BALL_PRICES = {
    "poke_ball" : 20,
    "great_ball": 200,
    "ultra_ball": 800,
    "master_ball": 100000
}
BALL_MODIFIERS = {
    "poke_ball": 1.0,
    "great_ball": 1.5,
    "ultra_ball": 2.0,
    "master_ball": 100.0
}
BALL_ALIASES = {
    "pb": "poke_ball",
    "gb": "great_ball",
    "ub": "ultra_ball",
    "mb": "master_ball"
}
CATCH_RATES = {
    "common":    {"poke_ball": 0.50, "great_ball": 0.90, "ultra_ball": 1.00, "master_ball": 1.0},
    "uncommon":  {"poke_ball": 0.40, "great_ball": 0.75, "ultra_ball": 1.00, "master_ball": 1.0},
    "rare":      {"poke_ball": 0.30, "great_ball": 0.60, "ultra_ball": 0.80, "master_ball": 1.0},
    "ultrarare": {"poke_ball": 0.20, "great_ball": 0.30, "ultra_ball": 0.75, "master_ball": 1.0},
    "epic":      {"poke_ball": 0.15, "great_ball": 0.20, "ultra_ball": 0.51, "master_ball": 1.0},
    "legendary": {"poke_ball": 0.05, "great_ball": 0.15, "ultra_ball": 0.25, "master_ball": 0.61}
}