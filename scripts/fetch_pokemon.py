import json
import urllib.request
import urllib.error
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

DATA_FILE = Path('data/pokemon_data.json')
MAX_ID = 898

# Weights for assigning rarity to non-legendary new pokemon
RARITY_CHOICES = ['common', 'uncommon', 'rare', 'epic', 'ultrarare']
RARITY_WEIGHTS = [119, 203, 146, 72, 52]

def fetch_json(url, retries=3):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** attempt)
            else:
                raise
        except Exception as e:
            time.sleep(2 ** attempt)
    raise Exception(f"Failed to fetch {url} after {retries} retries.")

def get_pokemon_data(poke_id):
    print(f"Fetching ID {poke_id}...")
    try:
        # Fetch base pokemon details
        base_data = fetch_json(f"https://pokeapi.co/api/v2/pokemon/{poke_id}")
        
        # Fetch species details
        species_data = fetch_json(f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}")
        
        # Parse Name
        name = base_data['name']
        
        # Parse Types
        types = [t['type']['name'] for t in base_data['types']]
        
        # Parse Abilities
        abilities = [a['ability']['name'] for a in base_data['abilities']]
        
        # Parse Stats
        stats_list = base_data['stats']
        base_stats = {
            'hp': next(s['base_stat'] for s in stats_list if s['stat']['name'] == 'hp'),
            'attack': next(s['base_stat'] for s in stats_list if s['stat']['name'] == 'attack'),
            'defense': next(s['base_stat'] for s in stats_list if s['stat']['name'] == 'defense'),
            'sp_atk': next(s['base_stat'] for s in stats_list if s['stat']['name'] == 'special-attack'),
            'sp_def': next(s['base_stat'] for s in stats_list if s['stat']['name'] == 'special-defense'),
            'speed': next(s['base_stat'] for s in stats_list if s['stat']['name'] == 'speed'),
        }
        base_stats['total'] = sum(base_stats.values())
        
        # Parse Species
        species_name = "Unknown"
        for genus in species_data.get('genera', []):
            if genus['language']['name'] == 'en':
                species_name = genus['genus']
                break
                
        is_legendary = species_data.get('is_legendary', False)
        is_mythical = species_data.get('is_mythical', False)
        
        return {
            'id': poke_id,
            'name': name,
            'types': types,
            'species': species_name,
            'abilities': abilities,
            'base_stats': base_stats,
            'is_legendary_or_mythical': is_legendary or is_mythical
        }
    except Exception as e:
        print(f"Error fetching ID {poke_id}: {e}")
        return None

def main():
    # Load existing data to preserve rarity
    existing_data = {}
    if DATA_FILE.exists():
        with open(DATA_FILE, 'r') as f:
            for p in json.load(f):
                existing_data[p['id']] = p

    results = []
    # Use ThreadPoolExecutor to speed up requests
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_id = {executor.submit(get_pokemon_data, poke_id): poke_id for poke_id in range(1, MAX_ID + 1)}
        for future in as_completed(future_to_id):
            data = future.result()
            if data:
                results.append(data)
                
    # Sort results by ID
    results.sort(key=lambda x: x['id'])
    
    # Merge existing rarity, assign new rarity
    final_data = []
    for p_data in results:
        poke_id = p_data['id']
        is_leg_myth = p_data.pop('is_legendary_or_mythical')
        
        if poke_id in existing_data and 'rarity' in existing_data[poke_id]:
            p_data['rarity'] = existing_data[poke_id]['rarity']
        else:
            if is_leg_myth:
                p_data['rarity'] = 'legendary'
            else:
                p_data['rarity'] = random.choices(RARITY_CHOICES, weights=RARITY_WEIGHTS, k=1)[0]
                
        final_data.append(p_data)

    # Save new data
    with open(DATA_FILE, 'w') as f:
        json.dump(final_data, f, indent=2)
        
    print(f"\nSuccessfully saved {len(final_data)} pokemon to {DATA_FILE}")

if __name__ == "__main__":
    main()
