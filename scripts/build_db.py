import csv
import json
import os

CSV_DIR = "/home/duckworth_cachy/doublechest/Projects/pokecatch_2/pokeapi/data/v2/csv"
OUTPUT_FILE = "/home/duckworth_cachy/doublechest/Projects/pokecatch_2/pokecatch_cli_game/data/pokemon_data.json"

def read_csv(filename):
    with open(os.path.join(CSV_DIR, filename), 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def build_db():
    print("Reading CSV files...")
    pokemon_raw = read_csv("pokemon.csv")
    species_raw = read_csv("pokemon_species.csv")
    pokemon_stats = read_csv("pokemon_stats.csv")
    stats = read_csv("stats.csv")
    pokemon_types = read_csv("pokemon_types.csv")
    types = read_csv("types.csv")
    pokemon_abilities = read_csv("pokemon_abilities.csv")
    abilities = read_csv("abilities.csv")

    # Mappings
    stat_map = {row['id']: row['identifier'] for row in stats}
    type_map = {row['id']: row['identifier'] for row in types}
    ability_map = {row['id']: row['identifier'] for row in abilities}
    
    species_map = {row['id']: row for row in species_raw}
    
    # Initialize DB
    db = {}
    for row in pokemon_raw:
        pid = row['id']
        db[pid] = {
            "name": row['identifier'].replace('-', ' ').title(),
            "types": [],
            "abilities": [],
            "stats": {},
            "rarity": "Common"
        }
        
    # Stats
    for row in pokemon_stats:
        pid = row['pokemon_id']
        if pid in db:
            stat_name = stat_map.get(row['stat_id'])
            if stat_name == 'hp': name = 'HP'
            elif stat_name == 'attack': name = 'Atk'
            elif stat_name == 'defense': name = 'Def'
            elif stat_name == 'special-attack': name = 'SpA'
            elif stat_name == 'special-defense': name = 'SpD'
            elif stat_name == 'speed': name = 'Spe'
            else: continue
            db[pid]['stats'][name] = int(row['base_stat'])
            
    # Types
    pokemon_types_sorted = sorted(pokemon_types, key=lambda x: int(x['slot']))
    for row in pokemon_types_sorted:
        pid = row['pokemon_id']
        if pid in db:
            db[pid]['types'].append(type_map.get(row['type_id']).capitalize())
            
    # Abilities
    for row in pokemon_abilities:
        pid = row['pokemon_id']
        if pid in db:
            ability_name = ability_map.get(row['ability_id']).replace('-', ' ').title()
            # Avoid duplicates if they exist
            if ability_name not in db[pid]['abilities']:
                db[pid]['abilities'].append(ability_name)
            
    # Calculate Totals and Rarity
    # We only want default forms to keep the game clean, unless you want all variations
    # Let's filter to only `is_default` = 1
    final_db = {}
    
    for row in pokemon_raw:
        pid = row['id']
        if row['is_default'] != '1':
            continue
            
        data = db.get(pid)
        if not data: continue
        
        species_id = row['species_id']
        species = species_map.get(species_id)
        if not species: continue
            
        stats_dict = data['stats']
        if len(stats_dict) < 6:
            continue
            
        total = sum(stats_dict.values())
        stats_dict['Total'] = total
        
        # Rarity calculation
        is_mythical = int(species['is_mythical']) if species['is_mythical'] else 0
        is_legendary = int(species['is_legendary']) if species['is_legendary'] else 0
        capture_rate = int(species['capture_rate']) if species['capture_rate'] else 255
        
        if is_mythical: rarity = "Mythical"
        elif is_legendary: rarity = "Legendary"
        elif total >= 600: rarity = "Epic"
        elif total >= 500 or capture_rate <= 45: rarity = "UltraRare"
        elif total >= 400 or capture_rate <= 90: rarity = "Rare"
        elif total >= 300 or capture_rate <= 190: rarity = "Uncommon"
        else: rarity = "Common"
        
        data['rarity'] = rarity
        final_db[pid] = data

    # Create directory if not exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(final_db, f, indent=2)
        
    print(f"Successfully generated data for {len(final_db)} standard Pokemon.")
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    build_db()
