import json
from collections import Counter

try:
    # This assumes the 'data' folder is in the same directory as the script.
    with open('data/pokemon_data.json', 'r') as f:
        pokemon_data = json.load(f)

    # Extract the rarity of each Pokémon into a list
    rarities = [pokemon['rarity'] for pokemon in pokemon_data]

    # Use collections.Counter to count the occurrences of each rarity
    rarity_counts = Counter(rarities)

    print("Count of Pokémon by Rarity:")
    
    # Define a logical order for display
    sorted_rarities = ["common", "uncommon", "rare", "ultrarare", "epic", "legendary"]
    
    for rarity in sorted_rarities:
        # Check if the rarity exists in our counts before printing
        if rarity in rarity_counts:
            count = rarity_counts[rarity]
            # Use formatting for clean alignment
            print(f"- {rarity.capitalize():<12}: {count}")

except FileNotFoundError:
    print("Error: 'data/pokemon_data.json' not found.")
    print("Please make sure you are running this script from your 'pokecatch_game' directory.")
except Exception as e:
    print(f"An error occurred: {e}")