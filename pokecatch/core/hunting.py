import os
import sys
import time
import random

from pokecatch.config import (
    HUNT_COOLDOWN_SECONDS, DATA_FILE, WILD_POKEMON_STATE, PLAYER_DEX,
    RARITY_SPAWN_WEIGHTS, BASE_CATCH_RATES
)

from pokecatch.utils import load_data, save_data, display_sprite
from pokecatch.core.player import load_player_data, save_player_data

def hunt():
    player_data = load_player_data()
    current_time = time.time()
    last_hunt = player_data.get("last_hunt_time", 0)
    time_since_last_hunt = current_time - last_hunt
    if time_since_last_hunt < HUNT_COOLDOWN_SECONDS:
        time_left = int(HUNT_COOLDOWN_SECONDS - time_since_last_hunt)
        print(f"You are tired from your last hunt. Please wait {time_left} more seconds.")
        return 
    all_pokemon = load_data(DATA_FILE)
    if not all_pokemon:
        print("Error: pokemon_data.json is empty or not found!")
        return
    
    rarity_tiers = list(RARITY_SPAWN_WEIGHTS.keys())
    rarity_weights = list(RARITY_SPAWN_WEIGHTS.values())
    chosen_rarity = random.choices(rarity_tiers, weights=rarity_weights, k=1)[0]
    pokemon_pool_of_rarity = [p for p in all_pokemon if p['rarity'] == chosen_rarity]
    wild_pokemon = random.choice(pokemon_pool_of_rarity)
    
    print(f"A wild {wild_pokemon['name'].capitalize()} appeared!")
    print(f"Rarity: {wild_pokemon['rarity'].capitalize()}")
    display_sprite(wild_pokemon['id'])
    player_data["last_hunt_time"] = time.time()
    save_player_data(player_data)
    save_data(WILD_POKEMON_STATE, wild_pokemon)


def catch(ball_type):
    if not WILD_POKEMON_STATE.exists():
        print("You haven't found a Pokémon to catch! Use 'pokecatch hunt' first.")
        return
    player_data = load_player_data()
    
    if player_data["balls"].get(ball_type, 0) <= 0:
        print(f"You don't have any {ball_type.replace('_', ' ')}s!")
        return
    
    player_data["balls"][ball_type] -= 1
    save_player_data(player_data)
    wild_pokemon = load_data(WILD_POKEMON_STATE)
    pokemon_name = wild_pokemon['name']
    rarity = wild_pokemon['rarity']
    print(f"You threw a {ball_type.replace('_', ' ')} at {pokemon_name.capitalize()}...")
    print(f"You have {player_data['balls'][ball_type]} left.")
    def endless_dots(duration=5, interval=0.5):
        start = time.time()
        dots = ""
        while time.time() - start < duration:
            dots += "."
            sys.stdout.write(f"\rFighting{dots}")
            sys.stdout.flush()
            time.sleep(interval)
        print()
    endless_dots(5, 0.5)
    
    # catch_chance = BASE_CATCH_RATES.get(rarity, {}).get(ball_type, 0.0)

    # --- DYNAMIC CATCH LOGIC ---
    base_chance = BASE_CATCH_RATES.get(rarity, 0.1)
    multiplier = 1.0
    
    # Extract Pokémon stats/types to evaluate conditional balls
    types = [t.lower() for t in wild_pokemon.get('types', [])]
    speed = wild_pokemon.get('stats', {}).get('Spe', 50)
    # Ball Modifiers
    if ball_type == "master_ball":
        multiplier = 255.0  # Guaranteed catch
    elif ball_type == "ultra_ball":
        multiplier = 2.0
    elif ball_type == "great_ball":
        multiplier = 1.5
    elif ball_type == "net_ball":
        if "water" in types or "bug" in types:
            multiplier = 3.0
    elif ball_type == "dive_ball":
        if "water" in types:
            multiplier = 3.5
    elif ball_type == "fast_ball":
        if speed > 100:
            multiplier = 3.0
    elif ball_type == "dusk_ball":
        current_hour = time.localtime().tm_hour
        # Night time between 18:00 (6 PM) and 06:00 (6 AM)
        if current_hour >= 18 or current_hour < 6:
            multiplier = 3.5
    elif ball_type == "nest_ball":
        if rarity in ["Common", "Uncommon"]:
            multiplier = 3.0
    elif ball_type == "repeat_ball":
        # Check if already caught
        player_dex = load_data(PLAYER_DEX)
        if any(p['name'] == pokemon_name for p in player_dex):
            multiplier = 3.0
    elif ball_type == "quick_ball":
        # Since CLI combat is one-turn, Quick Ball is effectively always a 4.0x!
        multiplier = 4.0
    
    catch_chance = base_chance * multiplier
    # ---------------------------
    
    if random.random() < catch_chance:
        print(f"Gotcha! {pokemon_name.capitalize()} was caught!")
        player_dex = load_data(PLAYER_DEX)
        player_dex.append(wild_pokemon)
        save_data(PLAYER_DEX, player_dex)
    else:
        print(f"Oh no! {pokemon_name.capitalize()} broke free!")
    os.remove(WILD_POKEMON_STATE)
