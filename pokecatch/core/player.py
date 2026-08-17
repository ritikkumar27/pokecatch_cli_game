from pokecatch.config import PLAYER_DATA_FILE, PLAYER_DEX
from pokecatch.utils import load_data, save_data, display_sprite_pokedex

def load_player_data():
    if not PLAYER_DATA_FILE.exists():
        player_data = {
            "currency": 0,
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
    return load_data(PLAYER_DATA_FILE)

def save_player_data(player_data):
    save_data(PLAYER_DATA_FILE, player_data)

def inventory():
    player_data = load_player_data()
    currency = player_data.get("currency", 0)
    balls = player_data.get("balls", {})

    print("--- 🎒 Your Inventory ---")
    print(f"Poké Dollars: ${currency}")
    print("\n--- Poké Balls ---")
    for ball, count in balls.items():
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