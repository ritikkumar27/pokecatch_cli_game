from pokecatch.config import PLAYER_DEX, RARITY_SELL_PRICES, BALL_PRICES
from pokecatch.utils import load_data, save_data
from pokecatch.core.player import load_player_data, save_player_data

def sell_pokemon(pokemon_name):
    player_dex = load_data(PLAYER_DEX)
    player_data = load_player_data()

    pokemon_to_sell = None
    for p in player_dex:
        if p['name'].lower() == pokemon_name.lower():
            pokemon_to_sell = p
            break
    
    if pokemon_to_sell:
        rarity = pokemon_to_sell['rarity']
        price = RARITY_SELL_PRICES.get(rarity, 50)
        
        player_dex.remove(pokemon_to_sell)
        player_data['currency'] += price
        
        save_data(PLAYER_DEX, player_dex)
        save_player_data(player_data)
        
        print(f"You sold {pokemon_name.capitalize()} for ${price}.")
        print(f"Your new balance is ${player_data['currency']}.")
    else:
        print(f"You don't have a Pokémon named {pokemon_name.capitalize()} to sell.")

def buy_item(item_name, amount):
    if item_name not in BALL_PRICES:
        print(f"Sorry, '{item_name}' is not for sale.")
        return

    player_data = load_player_data()
    price = BALL_PRICES[item_name]
    total_cost = price * amount

    if player_data['currency'] < total_cost:
        print(f"You don't have enough money! You need ${total_cost}, but you only have ${player_data['currency']}.")
        return
        
    player_data['currency'] -= total_cost
    player_data['balls'][item_name] += amount
    save_player_data(player_data)

    print(f"You bought {amount} {item_name.replace('_', ' ')}(s) for ${total_cost}.")
    print(f"Your new balance is ${player_data['currency']}.")

def display_store():
    player_data = load_player_data()
    print("--- 🏪 Poké Mart ---")
    print(f"Welcome! You have ${player_data['currency']}.")
    
    print("\n--- Items for Sale (Purchase) ---")
    for item, price in BALL_PRICES.items():
        print(f"- {item.replace('_', ' ').capitalize():<12}: ${price}")
    
    print("\n--- Pokémon Sell Prices ---")
    for rarity, price in RARITY_SELL_PRICES.items():
        print(f"- {rarity.capitalize():<12}: ${price}")

    print("\nUse 'pokecatch store buy <item> <amount>' to buy.")
    print("Use 'pokecatch store sell <pokemon_name>' to sell.")
    print("----------------------")

def sell_all_by_rarity(rarity_to_sell):
    player_dex = load_data(PLAYER_DEX)
    player_data = load_player_data()

    if not player_dex:
        print("Your Pokedex is empty! There is nothing to sell.")
        return

    pokemon_to_sell = []
    remaining_pokemon = []
    total_earnings = 0
    price_per_pokemon = RARITY_SELL_PRICES.get(rarity_to_sell, 0)

    for p in player_dex:
        if p['rarity'].lower() == rarity_to_sell.lower():
            pokemon_to_sell.append(p)
            total_earnings += price_per_pokemon
        else:
            remaining_pokemon.append(p)
            
    if not pokemon_to_sell:
        print(f"You have no {rarity_to_sell.capitalize()} Pokémon to sell.")
        return
        
    player_data['currency'] += total_earnings
    save_data(PLAYER_DEX, remaining_pokemon)
    save_player_data(player_data)
    
    print(f"✅ Sold {len(pokemon_to_sell)} {rarity_to_sell.capitalize()} Pokémon for ${total_earnings}.")
    print(f"Your new balance is ${player_data['currency']}.")