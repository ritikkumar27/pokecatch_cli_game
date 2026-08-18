from pokecatch.config import PLAYER_DEX, RARITY_SELL_PRICES, BALL_PRICES
from pokecatch.utils import load_data, save_data
from pokecatch.core.player import load_player_data, save_player_data

import datetime
from pokecatch.config import PLAYER_DEX, RARITY_SELL_PRICES, STORE_ITEMS, USER_SAVE_DIR
from pokecatch.utils import load_data, save_data
from pokecatch.core.player import load_player_data, save_player_data, get_player_level
SHOP_FILE = USER_SAVE_DIR / 'shop.json'



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
    from pokecatch.config import BALL_ALIASES, STORE_ITEMS
    if item_name.lower() in BALL_ALIASES:
        item_name = BALL_ALIASES[item_name.lower()]
    if item_name not in STORE_ITEMS:
        print(f"Sorry, '{item_name}' is not for sale.")
        return
        
    player_data = load_player_data()
    level = get_player_level(player_data.get("xp", 0))
    item_data = STORE_ITEMS[item_name]
    
    if level < item_data["unlock_level"]:
        print(f"You must be Level {item_data['unlock_level']} to buy this item.")
        return
        
    price = item_data["price"]
    total_cost = price * amount
    
    if player_data['currency'] < total_cost:
        print(f"You need ₽ {total_cost:,}, but you only have ₽ {player_data['currency']:,}.")
        return
        
    player_data['currency'] -= total_cost
    
    # Give the ball to the player
    if 'balls' not in player_data:
        player_data['balls'] = {}
    if item_name not in player_data['balls']:
        player_data['balls'][item_name] = 0
        
    player_data['balls'][item_name] += amount
    save_player_data(player_data)
    
    print(f"✅ You bought {amount} {item_name.replace('_', ' ').title()}(s) for ₽ {total_cost:,}.")
    print(f"Your new balance is ₽ {player_data['currency']:,}.")

def display_store():
    try:
        from rich.console import Console
    except ImportError:
        print("Please run: pip install rich")
        return
    console = Console()
    player_data = load_player_data()
    level = get_player_level(player_data.get("xp", 0))
    currency = player_data.get("currency", 0)
    balls = player_data.get("balls", {})
    
    # --- HEADER ---
    console.print()
    console.print("╭──────────────────────────────────────────────────────────────╮", style="cyan")
    console.print("│                         POKÉ MART                            │", style="bold cyan")
    console.print("╰──────────────────────────────────────────────────────────────╯", style="cyan")
    console.print(f"  [bold yellow]₽ {currency:,}[/bold yellow]")
    console.print()
    # Define Layout
    sections = [
        {"title": "BALLS", "keys": ["poke_ball", "great_ball", "ultra_ball"]},
        {"title": "SPECIAL BALLS", "keys": ["net_ball", "dive_ball", "fast_ball", "dusk_ball", "nest_ball", "repeat_ball", "quick_ball"]},
        {"title": "MASTER", "keys": ["master_ball"]}
    ]
    ball_descriptions = {
        "net_ball": "Bug / Water    3×",
        "dive_ball": "Water          3.5×",
        "fast_ball": "Speed ≥ 120    3×",
        "dusk_ball": "Night          3.5×",
        "nest_ball": "BST ≤ 300      3×",
        "repeat_ball": "Already Caught 3×",
        "quick_ball": "Flat Boost     2.5×"
    }
    from pokecatch.config import STORE_ITEMS
    
    for section in sections:
        console.print(f"[bold white]{section['title']}[/bold white]")
        console.print("──────────────────────────────────────────────────────────────", style="grey50")
        console.print()
        
        for key in section["keys"]:
            data = STORE_ITEMS[key]
            name = key.replace('_', ' ').title()
            price_str = f"₽{data['price']:,}"
            owned = balls.get(key, 0)
            
            if level >= data["unlock_level"]:
                console.print(f"  {name:<15} [yellow]{price_str:<9}[/yellow] [grey74]You own: {owned}[/grey74]")
                if key in ball_descriptions:
                    console.print(f"  [cyan]{ball_descriptions[key]}[/cyan]")
            else:
                console.print(f"  {name:<15} [red]Requires Level {data['unlock_level']}[/red]")
        console.print()
        
    console.print("──────────────────────────────────────────────────────────────", style="grey50")
    console.print("  [cyan]pokecatch store buy <item> <amount>[/cyan]")
    console.print("  [cyan]pokecatch store sell <pokemon>[/cyan] | [cyan]sellall <rarity>[/cyan] | [cyan]sell-dupes[/cyan]")
    console.print()
    
def sell_all_by_rarity(rarity_to_sell):
    player_dex = load_data(PLAYER_DEX)
    player_data = load_player_data()

    if not player_dex:
        print("Your Pokedex is empty! There is nothing to sell.")
        return

    # Safety Lock
    if rarity_to_sell.lower() in ["epic", "legendary", "mythical"]:
        try:
            from rich.prompt import Confirm
            confirm = Confirm.ask(f"[bold red]WARNING:[/bold red] Are you sure you want to sell ALL your {rarity_to_sell.capitalize()} Pokémon?")
            if not confirm:
                print("Sale cancelled.")
                return
        except ImportError:
            import builtins
            confirm = builtins.input(f"WARNING: Are you sure you want to sell ALL your {rarity_to_sell.capitalize()} Pokémon? [y/N]: ")
            if confirm.lower() not in ['y', 'yes']:
                print("Sale cancelled.")
                return

    pokemon_to_sell = []
    remaining_pokemon = []
    total_earnings = 0
    
    # We iterate case-insensitively over keys to get the correct rarity price
    price_per_pokemon = 50
    for r, p in RARITY_SELL_PRICES.items():
        if r.lower() == rarity_to_sell.lower():
            price_per_pokemon = p
            break

    for p in player_dex:
        if p.get('rarity', '').lower() == rarity_to_sell.lower():
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
    
    print(f"✅ Sold {len(pokemon_to_sell)} {rarity_to_sell.capitalize()} Pokémon for ₽ {total_earnings:,}.")
    print(f"Your new balance is ₽ {player_data['currency']:,}.")

def sell_dupes():
    player_dex = load_data(PLAYER_DEX)
    player_data = load_player_data()

    if not player_dex:
        print("Your Pokédex is empty! There is nothing to sell.")
        return

    # Count occurrences of each species
    species_counts = {}
    for p in player_dex:
        pid = p['id']
        if pid not in species_counts:
            species_counts[pid] = []
        species_counts[pid].append(p)
        
    pokemon_to_sell = []
    remaining_pokemon = []
    total_earnings = 0
    
    # Calculate price based on case-insensitive mapping
    price_map = {r.lower(): p for r, p in RARITY_SELL_PRICES.items()}
    
    for pid, instances in species_counts.items():
        # Keep the first one, sell the rest
        remaining_pokemon.append(instances[0])
        if len(instances) > 1:
            for duplicate in instances[1:]:
                pokemon_to_sell.append(duplicate)
                rarity = duplicate.get('rarity', 'common').lower()
                total_earnings += price_map.get(rarity, 50)
                
    if not pokemon_to_sell:
        print("You don't have any duplicate Pokémon to sell!")
        return
        
    try:
        from rich.prompt import Confirm
        confirm = Confirm.ask(f"Ready to sell [bold cyan]{len(pokemon_to_sell)}[/bold cyan] duplicate Pokémon for [bold yellow]₽ {total_earnings:,}[/bold yellow]?")
        if not confirm:
            print("Sale cancelled.")
            return
    except ImportError:
        import builtins
        confirm = builtins.input(f"Ready to sell {len(pokemon_to_sell)} duplicate Pokémon for ₽ {total_earnings:,}? [y/N]: ")
        if confirm.lower() not in ['y', 'yes']:
            print("Sale cancelled.")
            return
            
    player_data['currency'] += total_earnings
    save_data(PLAYER_DEX, remaining_pokemon)
    save_player_data(player_data)
    
    print(f"✅ Successfully sold {len(pokemon_to_sell)} duplicates for ₽ {total_earnings:,}!")
    print(f"Your new balance is ₽ {player_data['currency']:,}.")