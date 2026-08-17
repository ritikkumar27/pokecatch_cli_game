from pokecatch.config import PLAYER_DEX, RARITY_SELL_PRICES, BALL_PRICES
from pokecatch.utils import load_data, save_data
from pokecatch.core.player import load_player_data, save_player_data

import datetime
from pokecatch.config import PLAYER_DEX, RARITY_SELL_PRICES, STORE_ITEMS, USER_SAVE_DIR
from pokecatch.utils import load_data, save_data
from pokecatch.core.player import load_player_data, save_player_data, get_player_level
SHOP_FILE = USER_SAVE_DIR / 'shop.json'

def get_store_state():
    today = str(datetime.date.today())
    if not SHOP_FILE.exists():
        state = {"last_refresh": today, "items": {}}
        for item, data in STORE_ITEMS.items():
            state["items"][item] = data.get("daily_stock", 10)
        save_data(SHOP_FILE, state)
        return state
        
    state = load_data(SHOP_FILE)
    if state.get("last_refresh") != today:
        # It's a new day! Refresh stock
        state["last_refresh"] = today
        state["items"] = {}
        for item, data in STORE_ITEMS.items():
            state["items"][item] = data.get("daily_stock", 10)
        save_data(SHOP_FILE, state)
    return state
def save_store_state(state):
    save_data(SHOP_FILE, state)

# --------------------------------------------------------------

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
    if item_name not in STORE_ITEMS:
        print(f"Sorry, '{item_name}' is not for sale.")
        return
    player_data = load_player_data()
    level = get_player_level(player_data.get("xp", 0))
    item_data = STORE_ITEMS[item_name]
    
    if level < item_data["unlock_level"]:
        print(f"You must be Level {item_data['unlock_level']} to buy this item.")
        return
        
    state = get_store_state()
    stock = state["items"].get(item_name, 0)
    
    if amount > stock:
        print(f"The store only has {stock} of those left today!")
        return
    discount = min(level * 0.005, 0.15)
    price = int(item_data["price"] * (1 - discount))
    total_cost = price * amount
    if player_data['currency'] < total_cost:
        print(f"You need ${total_cost}, but you only have ${player_data['currency']}.")
        return
        
    player_data['currency'] -= total_cost
    
    # Give the ball to the player (create key if they don't own any yet)
    if item_name not in player_data['balls']:
        player_data['balls'][item_name] = 0
        
    player_data['balls'][item_name] += amount
    save_player_data(player_data)
    
    # Remove from store stock
    state["items"][item_name] -= amount
    save_store_state(state)
    print(f"You bought {amount} {item_name.replace('_', ' ').title()}(s) for ${total_cost}.")
    print(f"Your new balance is ${player_data['currency']}.")

def display_store():
    player_data = load_player_data()
    level = get_player_level(player_data.get("xp", 0))
    discount = min(level * 0.005, 0.15)
    
    print("--- 🏪 Poké Mart ---")
    print(f"Welcome! You are Level {level} (Discount: {discount*100:.1f}%). You have ${player_data['currency']}.")
    
    print("\n--- Items for Sale (Purchase) ---")
    state = get_store_state()
    for item, data in STORE_ITEMS.items():
        if level >= data["unlock_level"]:
            base_price = data["price"]
            discounted_price = int(base_price * (1 - discount))
            stock = state["items"].get(item, 0)
            stock_str = str(stock) if stock > 0 else "SOLD OUT"
            print(f"- {item.replace('_', ' ').title():<12}: ${discounted_price} (Stock: {stock_str})")
        else:
            print(f"- [LOCKED] Unlocks at Level {data['unlock_level']}")
    
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