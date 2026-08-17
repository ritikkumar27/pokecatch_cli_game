import argparse

# Importing constants
from pokecatch.config import BALL_MODIFIERS, BALL_ALIASES, BALL_PRICES, RARITY_SELL_PRICES


# Importing game logic from the core modules!
from pokecatch.core.hunting import hunt, catch
from pokecatch.core.player import inventory, my_pokemon
from pokecatch.core.store import buy_item, sell_pokemon, sell_all_by_rarity, display_store

def main():
    parser = argparse.ArgumentParser(description="A Pokémon catching game for the terminal.")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # hunt command
    hunt_parser = subparsers.add_parser("hunt", help="Search for a wild Pokémon.")
    
    # catch command
    catch_parser = subparsers.add_parser("catch", help="Throw a Poké Ball to catch a Pokémon.")
    valid_ball_choices = list(BALL_MODIFIERS.keys()) + list(BALL_ALIASES.keys())
    catch_parser.add_argument("ball", choices=valid_ball_choices, help="The type of ball to use (e.g., poke_ball,pb,great_ball,gb).")
    # pokedex
    my_pokemon_parser = subparsers.add_parser("my_pokemon", help="See all the Pokémon you have caught.")
    pokedex_parser = subparsers.add_parser("pokedex", help="See all the Pokémon you have caught.")
    # inventory
    inventory_parser = subparsers.add_parser("inventory", help="Check your items and currency.")
    
    # store command
    store_parser = subparsers.add_parser("store", help="Visit the Poké Mart to buy and sell.")
    store_subparsers = store_parser.add_subparsers(dest="action", help="Store actions")
    # store buy
    buy_parser = store_subparsers.add_parser("buy", help="Buy items from the store.")
    buy_parser.add_argument("item", choices=BALL_PRICES.keys(), help="The item to buy.")
    buy_parser.add_argument("amount", type=int, nargs='?', default=1, help="How many to buy (default: 1).")
    # store sell
    sell_parser = store_subparsers.add_parser("sell", help="Sell a caught Pokémon.")
    sell_parser.add_argument("pokemon_name", help="The name of the Pokémon to sell.")
    sellall_parser = store_subparsers.add_parser("sellall", help="Sell all Pokémon of a specific rarity.")
    sellall_parser.add_argument("rarity", choices=RARITY_SELL_PRICES.keys(), help="The rarity of Pokémon to sell.")
    args = parser.parse_args()
    # Route the commands to the proper functions
    if args.command == "hunt":
        hunt()
    elif args.command == "catch":
        ball_to_use = BALL_ALIASES.get(args.ball, args.ball)
        catch(ball_to_use)
    elif args.command in ("my_pokemon", "pokedex"):
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
