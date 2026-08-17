import os
import sys
import time
import random

from pokecatch.config import (
    HUNT_COOLDOWN_SECONDS, DATA_FILE, WILD_POKEMON_STATE, PLAYER_DEX,
    RARITY_SPAWN_WEIGHTS, BASE_CATCH_RATES, XP_REWARDS
)

from pokecatch.utils import load_data, save_data, display_sprite
from pokecatch.core.player import load_player_data, save_player_data, get_player_level, add_xp

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
    
    # 1. Roll for Rarity
    rarity_tiers = list(RARITY_SPAWN_WEIGHTS.keys())
    rarity_weights = list(RARITY_SPAWN_WEIGHTS.values())
    chosen_rarity = random.choices(rarity_tiers, weights=rarity_weights, k=1)[0]
    
    # 2. Extract Pokémon of that rarity from new Dictionary format
    pokemon_pool_of_rarity = []
    for pid, p in all_pokemon.items():
        if p.get('rarity') == chosen_rarity:
            p['id'] = int(pid) # Ensure it has the ID so the sprite can be drawn
            pokemon_pool_of_rarity.append(p)
            
    if not pokemon_pool_of_rarity:
        print(f"Error: No Pokémon found for rarity {chosen_rarity}!")
        return
        
    wild_pokemon = random.choice(pokemon_pool_of_rarity)
    
    print(f"A wild {wild_pokemon['name'].capitalize()} appeared!")
    print(f"Rarity: {wild_pokemon['rarity'].capitalize()}")
    display_sprite(wild_pokemon['id'])

    # Extract and format stats for the UI
    types_str = "/".join([t.capitalize() for t in wild_pokemon.get('types', [])])
    abilities_str = ", ".join([a.replace('-', ' ').title() for a in wild_pokemon.get('abilities', [])])
    hp = wild_pokemon.get('stats', {}).get('HP', '?')
    total_stats = wild_pokemon.get('stats', {}).get('Total', '?')

    print(f"⚔️  Type: {types_str}  |  🧬 Ability: {abilities_str}")
    print(f"❤️  HP: {hp}  |  📊 Total Stats: {total_stats}")    

    
    player_data["last_hunt_time"] = time.time()
    player_data["stats"]["total_hunts"] += 1
    player_data["stats"]["xp_from_hunting"] += XP_REWARDS["hunt"]
    save_player_data(player_data)
    save_data(WILD_POKEMON_STATE, wild_pokemon)
    
    # Grant XP for exploring!
    add_xp(XP_REWARDS["hunt"])


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
    
    # --- DYNAMIC CATCH LOGIC ---
    base_chance = BASE_CATCH_RATES.get(rarity, 0.1)
    multiplier = 1.0
    
    types = [t.lower() for t in wild_pokemon.get('types', [])]
    speed = wild_pokemon.get('stats', {}).get('Spe', 50)
    total_stats = wild_pokemon.get('stats', {}).get('Total', 300)
    
    player_dex = load_data(PLAYER_DEX)
    is_new = not any(p['name'] == pokemon_name for p in player_dex)
    # Ball Multipliers
    if ball_type == "master_ball":
        multiplier = 100.0  # High enough to guarantee 1.0 (100%) when capped later
    elif ball_type == "ultra_ball":
        multiplier = 2.0
    elif ball_type == "great_ball":
        multiplier = 1.5
    elif ball_type == "net_ball":
        if "water" in types or "bug" in types: multiplier = 3.0
    elif ball_type == "dive_ball":
        if "water" in types: multiplier = 3.5
    elif ball_type == "fast_ball":
        if speed >= 120: multiplier = 3.0
        elif speed >= 80: multiplier = 2.0
    elif ball_type == "dusk_ball":
        current_hour = time.localtime().tm_hour
        if current_hour >= 18 or current_hour < 6: multiplier = 3.5
    elif ball_type == "nest_ball":
        if total_stats <= 300: multiplier = 3.0
        elif total_stats <= 400: multiplier = 2.0
    elif ball_type == "repeat_ball":
        if not is_new: multiplier = 3.0
    elif ball_type == "quick_ball":
        multiplier = 2.5 # Nerfed from 4.0x for balance
    
    # Apply Level Bonus
    level = get_player_level(player_data.get("xp", 0))
    level_bonus = min(level * 0.01, 0.25)
    
    catch_chance = base_chance * multiplier * (1 + level_bonus)
    catch_chance = min(catch_chance, 1.0) # Cap at 100%
    # ---------------------------
    
    if random.random() < catch_chance:
        print(f"Gotcha! {pokemon_name.capitalize()} was caught!")
        player_dex.append(wild_pokemon)
        save_data(PLAYER_DEX, player_dex)
        
        # Track Catch Stats
        player_data["stats"]["successful_catches"] += 1
        if is_new:
            player_data["stats"]["first_time_catches"] += 1
        
        # Grant XP
        xp_gained = XP_REWARDS.get(f"catch_{rarity}", 10)
        if is_new:
            print("New Pokédex entry! XP Doubled!")
            xp_gained *= 2
            
        player_data["stats"]["xp_from_catching"] += xp_gained
        save_player_data(player_data)
            
        print(f"You earned {xp_gained} XP!")
        add_xp(xp_gained)
    else:
        print(f"Oh no! {pokemon_name.capitalize()} broke free!")
        player_data["stats"]["failed_catches"] += 1
        save_player_data(player_data)
        
    os.remove(WILD_POKEMON_STATE)