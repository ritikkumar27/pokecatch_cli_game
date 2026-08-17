#!/usr/bin/env python3
import os
import json
import random
import subprocess
import argparse
import shlex 
import time 
import sys

from term_image.image import AutoImage
from PIL import Image

# --- HELPER FUNCTIONS ---

#display wild pokemon
def display_sprite(pokemon_name):
    
    sprite_path = os.path.join(SPRITES_DIR, f"{pokemon_name}.png")
    if not os.path.exists(sprite_path):
        print(f"Sprite for {pokemon_name} not found!")
        return
    
    try:
        img = Image.open(sprite_path).convert("RGBA")
        
        bbox = img.getchannel('A').getbbox()
        if bbox:
            img = img.crop(bbox)
        
        # -- SET YOUR PERCENTAGE HERE --
        # 3.0 means 300%, 1.5 means 150%, 0.5 means 50%, etc.
        scale_factor = 3.0
        
        # Convert the pixel width to terminal columns (divide by ~3 for aspect ratio)
        calculated_width = int((img.width * scale_factor) / 3)
        
        # Use our calculated percentage width
        term_img = AutoImage(img, width=calculated_width)
        term_img.draw(h_align="<", pad_height=1)
        
    except Exception as e:
        print(f"Error displaying image: {e}")

def display_sprite_pokedex(pokemon_name):
    sprite_path = os.path.join(SPRITES_DIR, f"{pokemon_name}.png")
    if not os.path.exists(sprite_path):
        print(f"Sprite for {pokemon_name} not found!")
        return
    
    try:
        img = Image.open(sprite_path).convert("RGBA")
        
        bbox = img.getchannel('A').getbbox()
        if bbox:
            img = img.crop(bbox)
        
        # 1.25 means 125%, matching your original Pokédex size
        scale_factor = 1.25 
        calculated_width = int((img.width * scale_factor) / 3)
        
        # We ensure width is at least 1, otherwise term-image might throw an error on tiny sprites
        calculated_width = max(1, calculated_width)
        
        term_img = AutoImage(img, width=calculated_width)
        term_img.draw(h_align="<", pad_height=1)
        
    except Exception as e:
        print(f"Error displaying image: {e}")
def load_data(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        return json.load(f)

def save_data(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

# --- GAME COMMANDS ---

def hunt():

    player_data = load_player_data()
    current_time = time.time() # Gets the current time in seconds
    last_hunt = player_data.get("last_hunt_time", 0)
    time_since_last_hunt = current_time - last_hunt

    if time_since_last_hunt < HUNT_COOLDOWN_SECONDS:
        time_left = int(HUNT_COOLDOWN_SECONDS - time_since_last_hunt)
        print(f"You are tired from your last hunt. Please wait {time_left} more seconds.")
        return # Stop the function here


    # os.system('clear')
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

    if not os.path.exists(WILD_POKEMON_STATE):
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

    #time pause for anticipation
    def endless_dots(duration=5, interval=0.5):
        start = time.time()
        dots = ""
        while time.time() - start < duration:
            dots += "."
            sys.stdout.write(f"\rFighting{dots}")
            sys.stdout.flush()
            time.sleep(interval)
        print()

    #run 5 seconds : add dot 0.5 seconds
    endless_dots(5, 0.5)
    
    catch_chance = CATCH_RATES.get(rarity, {}).get(ball_type, 0.0)
    
    if random.random() < catch_chance:
        print(f"Gotcha! {pokemon_name.capitalize()} was caught!")
        player_dex = load_data(PLAYER_DEX)
        player_dex.append(wild_pokemon)
        save_data(PLAYER_DEX, player_dex)
    else:
        print(f"Oh no! {pokemon_name.capitalize()} broke free!")

    os.remove(WILD_POKEMON_STATE)
#---------------------------------------------------------------------------------------------------------------------

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
    # --------------------------

    print("\nUse 'pokecatch store buy <item> <amount>' to buy.")
    print("Use 'pokecatch store sell <pokemon_name>' to sell.")
    print("----------------------")

def sell_all_by_rarity(rarity_to_sell):

    player_dex = load_data(PLAYER_DEX)
    player_data = load_data(PLAYER_DATA_FILE)

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

#--------------------------------------------------------------------------------------------------------------------------------



def my_pokemon():
    player_dex = load_data(PLAYER_DEX)
    if not player_dex:
        print("You haven't caught any Pokémon yet. Go 'hunt' for some!")
        return

    print("--- Your Pokémons ---")
    print()

    #sort by id
    sorted_dex = sorted(player_dex, key=lambda p: p['id'])
    for p in sorted_dex:


        #display pokedex pokemon in small size
        display_sprite_pokedex(p['id'])

        print(f"- #{p['id']:03d} {p['name'].capitalize()} (Rarity: {p['rarity']})")
        print()
    print("--------------------")

def load_player_data():
    
    if not os.path.exists(PLAYER_DATA_FILE):
        #starting data for a new player
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

#execution and argument passing

def main():
    parser = argparse.ArgumentParser(description="A Pokémon catching game for the Kitty terminal.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    #hunt command
    hunt_parser = subparsers.add_parser("hunt", help="Search for a wild Pokémon.")
    
    #catch command
    catch_parser = subparsers.add_parser("catch", help="Throw a Poké Ball to catch a Pokémon.")
    valid_ball_choices = list(BALL_MODIFIERS.keys()) + list(BALL_ALIASES.keys())
    catch_parser.add_argument("ball", choices=valid_ball_choices, help="The type of ball to use (e.g., poke_ball,pb,great_ball,gb,ultra_ball,ub).")

    #pokedex
    my_pokemon_parser = subparsers.add_parser("my_pokemon", help="See all the Pokémon you have caught.")
    my_pokemon_parser = subparsers.add_parser("pokedex", help="See all the Pokémon you have caught.")





    inventory_parser = subparsers.add_parser("inventory", help="Check your items and currency.")
    #store command
    store_parser = subparsers.add_parser("store", help="Visit the Poké Mart to buy and sell.")
    store_subparsers = store_parser.add_subparsers(dest="action", help="Store actions")

    #store buy command
    buy_parser = store_subparsers.add_parser("buy", help="Buy items from the store.")
    buy_parser.add_argument("item", choices=BALL_PRICES.keys(), help="The item to buy.")
    buy_parser.add_argument("amount", type=int, nargs='?', default=1, help="How many to buy (default: 1).")

    #store sell command
    sell_parser = store_subparsers.add_parser("sell", help="Sell a caught Pokémon.")
    sell_parser.add_argument("pokemon_name", help="The name of the Pokémon to sell.")

    sellall_parser = store_subparsers.add_parser("sellall", help="Sell all Pokémon of a specific rarity.")
    sellall_parser.add_argument("rarity", choices=RARITY_SELL_PRICES.keys(), help="The rarity of Pokémon to sell.")



    args = parser.parse_args()

    if args.command == "hunt":
        hunt()
    elif args.command == "catch":
        ball_input = args.ball
        ball_to_use = BALL_ALIASES.get(ball_input, ball_input)
        catch(ball_to_use)
    elif args.command == "my_pokemon":
        my_pokemon()
    elif args.command == "pokedex":
        my_pokemon()
    elif args.command == "inventory":
        inventory()
    elif args.command == "store":
        if args.action == "buy":
            buy_item(args.item, args.amount)
        elif args.action == "sell":
            sell_pokemon(args.pokemon_name)
        elif args.action == "sellall":
            sell_all_by_rarity(args.rarity)
        else:
            display_store()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()