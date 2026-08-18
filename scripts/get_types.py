import json
import os

def fetch_unique_types():
    # Adjust the path based on whether you moved 'data' inside 'pokecatch' or left it in the root
    filepath = "data/pokemon_data.json"
    if not os.path.exists(filepath):
        filepath = "/home/duckworth_cachy/doublechest/Projects/pokecatch_2/pokecatch_cli_game/data/pokemon_data.json"
        
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            pokemon_data = json.load(file)
            
        unique_types = set()
        
        # Loop through every pokemon in the JSON file
        for pokemon_id, info in pokemon_data.items():
            # Get the 'types' list, defaulting to an empty list if it doesn't exist
            for p_type in info.get("types", []):
                unique_types.add(p_type)
                
        # Sort the types alphabetically
        sorted_types = sorted(list(unique_types))
        
        print(f"Found {len(sorted_types)} unique Pokémon types:")
        for t in sorted_types:
            print(f"- {t}")
            
    except FileNotFoundError:
        print("Error: Could not find pokemon_data.json. Make sure you run this from the project root!")

if __name__ == "__main__":
    fetch_unique_types()