from pokecatch.config import PLAYER_DATA_FILE, PLAYER_DEX
from pokecatch.utils import load_data, save_data, display_sprite_pokedex

def load_player_data():
    if not PLAYER_DATA_FILE.exists():
        player_data = {
            "currency": 0,
            "xp": 0,
            "balls": {
                "poke_ball": 50,
                "great_ball": 0,
                "ultra_ball": 0,
                "master_ball": 0
            },
            "last_hunt_time": 0 
        }
        save_data(PLAYER_DATA_FILE, player_data)
        return player_data
        
    data = load_data(PLAYER_DATA_FILE)
    # Ensure existing players get an xp field without losing their save
    if "xp" not in data:
        data["xp"] = 0
        save_data(PLAYER_DATA_FILE, data)
    return data

def save_player_data(player_data):
    save_data(PLAYER_DATA_FILE, player_data)

def get_player_level(xp):
    """Calculates player level based on total XP using the formula: XP = 100 * (Level ^ 1.5)"""
    level = 1
    while xp >= int(100 * (level ** 1.5)):
        level += 1
    return level

def add_xp(amount):
    """Adds XP to the player and notifies them if they leveled up!"""
    player_data = load_player_data()
    old_level = get_player_level(player_data.get("xp", 0))
    
    player_data["xp"] = player_data.get("xp", 0) + amount
    save_player_data(player_data)
    
    new_level = get_player_level(player_data["xp"])
    if new_level > old_level:
        print(f"\n🎉 LEVEL UP! You are now Level {new_level}! 🎉")
        print("Check the store for new unlocked items and better discounts.\n")

def inventory():
    player_data = load_player_data()
    currency = player_data.get("currency", 0)
    xp = player_data.get("xp", 0)
    level = get_player_level(xp)
    next_level_xp = int(100 * (level ** 1.5))
    balls = player_data.get("balls", {})
    print("--- 🎒 Your Inventory ---")
    print(f"Level: {level} (XP: {xp} / {next_level_xp})")
    print(f"Poké Coins: ${currency}")
    print("\n--- Poké Balls ---")
    for ball, count in balls.items():
        if count > 0: # Only show balls you actually own
            print(f"- {ball.replace('_', ' ').capitalize():<12}: {count}")
    print("------------------------")

def my_pokemon():
    player_dex = load_data(PLAYER_DEX)
    if not player_dex:
        print("You haven't caught any Pokémon yet. Go 'hunt' for some!")
        return

    print("--- Your Pokémons ---\n")
    sorted_dex = sorted(player_dex, key=lambda p: p['id'])
    for p in sorted_dex:
        display_sprite_pokedex(p['id'])
        print(f"- #{p['id']:03d} {p['name'].capitalize()} (Rarity: {p['rarity']})\n")
    print("--------------------")