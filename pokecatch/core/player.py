from pokecatch.config import PLAYER_DATA_FILE, PLAYER_DEX
from pokecatch.utils import load_data, save_data, display_sprite_pokedex


def get_generation(pokemon_id):
    if pokemon_id <= 151: return 1
    elif pokemon_id <= 251: return 2
    elif pokemon_id <= 386: return 3
    elif pokemon_id <= 493: return 4
    elif pokemon_id <= 649: return 5
    elif pokemon_id <= 721: return 6
    elif pokemon_id <= 809: return 7
    elif pokemon_id <= 905: return 8
    else: return 9


def load_player_data():
    if not PLAYER_DATA_FILE.exists():
        player_data = {
            "currency": 0,
            "xp": 0,
            "balls": {
                "poke_ball": 50,
                "great_ball": 0,
                "ultra_ball": 0,
                "master_ball": 0
            },

            "last_hunt_time": 0,
            "stats": {
                "total_hunts": 0,
                "successful_catches": 0,
                "failed_catches": 0,
                "first_time_catches": 0,
                "xp_from_hunting": 0,
                "xp_from_catching":0
            }
        }

        save_data(PLAYER_DATA_FILE, player_data)
        return player_data

    data = load_data(PLAYER_DATA_FILE)
    if "xp" not in data:
        data["xp"] = 0

    if "stats" not in data:
        data["stats"] = {

            "total_hunts": 0,
            "successful_catches": 0,
            "failed_catches": 0,
            "first_time_catches": 0,
            "xp_from_hunting": 0,
            "xp_from_catching":0

        }

    #----backfill script for lifetime stats

    if "lifetime_rarity" not in data["stats"]:
        data["stats"]["lifetime_rarity"] = {"common": 0, "uncommon": 0, "rare": 0, "ultrarare": 0, "epic": 0, "legendary": 0, "mythical": 0}
        data["stats"]["lifetime_gens"] = {str(i): 0 for i in range(1, 10)}
        data["stats"]["lifetime_unique_pids"] = []
        data["stats"]["total_lifetime_caught"] = 0

        # scanning current pokedex to establish baseline

        player_dex = load_data(PLAYER_DEX)
        for p in player_dex:
            pid = p['id']
            rarity = p.get('rarity', 'common').lower()
            if rarity in data["stats"]["lifetime_rarity"]:
                data["stats"]["lifetime_rarity"][rarity] += 1
            
            gen = get_generation(pid)
            data["stats"]["lifetime_gens"][str(gen)] += 1
            data["stats"]["total_lifetime_caught"] += 1
            
            if pid not in data["stats"]["lifetime_unique_pids"]:
                data["stats"]["lifetime_unique_pids"].append(pid)

    save_data(PLAYER_DATA_FILE, data)
    return data

def save_player_data(player_data):
    save_data(PLAYER_DATA_FILE, player_data)

def get_player_level(xp):
    """Calculates player level based on total XP using the formula: XP = 100 * (Level ^ 1.5)"""
    level = 1
    while xp >= int(100 * (level ** 1.5)):
        level += 1
    return level

def add_xp(amount):
    """Adds XP to the player and notifies them if they leveled up!"""
    player_data = load_player_data()
    old_level = get_player_level(player_data.get("xp", 0))
    
    player_data["xp"] = player_data.get("xp", 0) + amount
    save_player_data(player_data)
    
    new_level = get_player_level(player_data["xp"])
    if new_level > old_level:
        print(f"\n🎉 LEVEL UP! You are now Level {new_level}! 🎉")
        print("Check the store for new unlocked items and better discounts.\n")

def inventory():
    player_data = load_player_data()
    currency = player_data.get("currency", 0)
    xp = player_data.get("xp", 0)
    level = get_player_level(xp)
    next_level_xp = int(100 * (level ** 1.5))
    balls = player_data.get("balls", {})
    print("--- 🎒 Your Inventory ---")
    print(f"Level: {level} (XP: {xp} / {next_level_xp})")
    print(f"Poké Coins: ${currency}")
    print("\n--- Poké Balls ---")
    for ball, count in balls.items():
        if count > 0: # Only show balls you actually own
            print(f"- {ball.replace('_', ' ').capitalize():<12}: {count}")
    print("------------------------")




#-------POKEDEX------------------------------
def pokedex(args):
    player_dex = load_data(PLAYER_DEX)
    if not player_dex:
        print("You haven't caught any Pokémon yet. Go 'hunt' for some!")
        return
    # 1. Group by unique species
    species_data = {}
    total_caught = len(player_dex)
    for p in player_dex:
        pid = p['id']
        if pid not in species_data:
            species_data[pid] = {
                'pokemon': p,
                'count': 0
            }
        species_data[pid]['count'] += 1
    unique_species = len(species_data)
    def get_generation(pokemon_id):
        if pokemon_id <= 151: return 1
        elif pokemon_id <= 251: return 2
        elif pokemon_id <= 386: return 3
        elif pokemon_id <= 493: return 4
        elif pokemon_id <= 649: return 5
        elif pokemon_id <= 721: return 6
        elif pokemon_id <= 809: return 7
        elif pokemon_id <= 905: return 8
        else: return 9
    # 2. Detailed View for a Single Pokémon
    if args.pokemon_name:
        target_name = args.pokemon_name.lower()
        target_entry = None
        for pid, data in species_data.items():
            if data['pokemon']['name'].lower() == target_name:
                target_entry = data
                break
        
        if not target_entry:
            print(f"You haven't caught a {args.pokemon_name.capitalize()} yet!")
            return
        p = target_entry['pokemon']
        count = target_entry['count']
        
        print(f"╭{'─'*36}╮")
        print(f"│ {f'#{p['id']:03d} {p['name'].upper()}':^34} │")
        print(f"╰{'─'*36}╯\n")
        
        display_sprite_pokedex(p['id'])
        
        print(f"\nOwned: ×{count}\n")
        
        types_str = "/".join([t.capitalize() for t in p.get('types', [])])
        abilities_str = ", ".join([a.replace('-', ' ').title() for a in p.get('abilities', [])])
        
        print(f"Type:      {types_str}")
        print(f"Ability:   {abilities_str}\n")
        
        stats = p.get('stats', {})
        print(f"HP:        {stats.get('HP', '?')}")
        print(f"Attack:    {stats.get('Atk', '?')}")
        print(f"Defense:   {stats.get('Def', '?')}")
        print(f"Sp. Atk:   {stats.get('SpA', '?')}")
        print(f"Sp. Def:   {stats.get('SpD', '?')}")
        print(f"Speed:     {stats.get('Spe', '?')}\n")
        
        print(f"Base Stat Total: {stats.get('Total', '?')}")
        print(f"Rarity: {p.get('rarity', 'Unknown')}")
        print(f"Generation: {get_generation(p['id'])}")
        return
    # 3. List View Filters
    filtered_species = list(species_data.values())
    
    if args.gen:
        filtered_species = [s for s in filtered_species if get_generation(s['pokemon']['id']) == args.gen]
    if args.type:
        target_type = args.type.lower()
        filtered_species = [s for s in filtered_species if target_type in [t.lower() for t in s['pokemon'].get('types', [])]]
    if args.rarity:
        target_rarity = args.rarity.lower()
        filtered_species = [s for s in filtered_species if s['pokemon'].get('rarity', '').lower() == target_rarity]
    # 4. Sorting
    if args.sort == "id":
        filtered_species.sort(key=lambda s: s['pokemon']['id'])
    elif args.sort == "rarity":
        rarity_order = {"common": 1, "uncommon": 2, "rare": 3, "ultrarare": 4, "epic": 5, "legendary": 6, "mythical": 7}
        filtered_species.sort(key=lambda s: rarity_order.get(s['pokemon'].get('rarity', '').lower(), 0), reverse=True)
    elif args.sort == "owned":
        filtered_species.sort(key=lambda s: s['count'], reverse=True)
    elif args.sort == "bst":
        filtered_species.sort(key=lambda s: s['pokemon'].get('stats', {}).get('Total', 0), reverse=True)
    # 5. Pagination
    items_per_page = 20
    total_filtered = len(filtered_species)
    total_pages = max(1, (total_filtered + items_per_page - 1) // items_per_page)
    
    page = max(1, min(args.page, total_pages))
    start_idx = (page - 1) * items_per_page
    end_idx = min(start_idx + items_per_page, total_filtered)
    
    page_items = filtered_species[start_idx:end_idx]
    # 6. Print Header
    print(f"╭{'─'*85}╮")
    title = "YOUR POKÉDEX"
    stats_str = f"{unique_species} / 1025 species  ·  {total_caught} caught"
    print(f"│ {title:^83} │")
    print(f"│ {stats_str:^83} │")
    print(f"╰{'─'*85}╯\n")
    if not page_items:
        print("No Pokémon match your current filters.")
        return
    print(f"Showing {start_idx + 1}–{end_idx} of {total_filtered} species (Page {page}/{total_pages})\n")
    print(f" {'#':<4}   {'Pokémon':<15} {'Owned':<7} {'Type':<18} {'Rarity':<12} {'BST'}")
    print(f" {'─'*84}")
    
    for s in page_items:
        p = s['pokemon']
        count_str = f"×{s['count']}"
        types_str = " / ".join([t.capitalize() for t in p.get('types', [])])
        rarity = p.get('rarity', 'Unknown')
        bst = p.get('stats', {}).get('Total', '?')
        
        print(f" {p['id']:03d}    {p['name'].capitalize():<15} {count_str:<7} {types_str:<18} {rarity:<12} {bst}")
    if page < total_pages:
        print(f"\nUse 'pokecatch pokedex --page {page + 1}' to see more.")


def stats():
    try:
        from rich.console import Console
        from rich.rule import Rule
        from rich.table import Table
    except ImportError:
        print("Please run: pip install rich")
        return

    console = Console()
    
    player_data = load_player_data()
    player_dex = load_data(PLAYER_DEX)
    s = player_data.get("stats", {})

    import getpass
    username = getpass.getuser().upper()

    # --- DATA CALCULATIONS ---
    xp = player_data.get("xp", 0)
    level = get_player_level(xp)
    next_level_xp = int(100 * (level ** 1.5))
    prev_level_xp = int(100 * ((level-1) ** 1.5)) if level > 1 else 0
    xp_in_level = xp - prev_level_xp
    xp_needed_for_level = next_level_xp - prev_level_xp
    currency = player_data.get("currency", 0)
    store_discount = min(level * 0.005, 0.15) * 100

    unique_pokemon = len(s.get("lifetime_unique_pids", []))
    total_pokemon = s.get("total_lifetime_caught", 0)
    rarity_counts = s.get("lifetime_rarity", {"common": 0, "uncommon": 0, "rare": 0, "ultrarare": 0, "epic": 0, "legendary": 0, "mythical": 0})
    gen_counts = s.get("lifetime_gens", {str(i): 0 for i in range(1, 10)})

    total_hunts = s.get("total_hunts", 0)
    success = s.get("successful_catches", 0)
    failed = s.get("failed_catches", 0)
    catch_rate = (success / total_hunts * 100) if total_hunts > 0 else 0.0
    balls = player_data.get("balls", {})

    from pokecatch.config import BALL_PRICES
    all_balls = list(BALL_PRICES.keys())

    # --- PRINT VERTICAL DASHBOARD ---
    console.print()
    console.print(Rule("[bold white]◈ TRAINER PROFILE ◈", style="cyan"))
    console.print()

    console.print(f"  [bold cyan]{username}[/bold cyan]  ·  [bold yellow]₽ {currency:,}[/bold yellow]")
    xp_pct = (xp_in_level / xp_needed_for_level * 100) if xp_needed_for_level > 0 else 0
    console.print(f"  [white]Level {level}[/white]  [bold cyan]{xp_pct:.0f}%[/bold cyan]  [grey74]({xp:,} / {next_level_xp:,} XP)[/grey74]")
    console.print(f"  [grey74]Store Discount: {store_discount:.1f}%[/grey74]")
    console.print()

    # COLLECTION
    console.print(Rule("[bold green]◈ COLLECTION", style="green", align="left"))
    console.print(f"  [white]Total Caught:[/white]   {total_pokemon:<10} [white]Unique Species:[/white] {unique_pokemon}")
    col_pct = (unique_pokemon / 1025) * 100
    console.print(f"  [white]Pokédex:[/white]        [bold green]{col_pct:.1f}%[/bold green] [grey74]({unique_pokemon} / 1025)[/grey74]")
    console.print()

    # HUNTING
    console.print(Rule("[bold cyan]◈ HUNTING RECORD", style="cyan", align="left"))
    console.print(f"  [white]Total Hunts:[/white]  {total_hunts:<10} [white]Catch Rate:[/white] [bold cyan]{catch_rate:.1f}%[/bold cyan]")
    console.print(f"  [white]Successful:[/white]   [green]{success:<10}[/green] [white]Failed:[/white]     [red]{failed}[/red]")
    console.print(f"  [white]First Catch:[/white]  [cyan]{s.get('first_time_catches', 0):<10}[/cyan] [white]Duplicates:[/white] [grey74]{success - s.get('first_time_catches', 0)}[/grey74]")
    console.print(f"  [grey74]Hunt XP: {s.get('xp_from_hunting', 0):,}  |  Catch XP: {s.get('xp_from_catching', 0):,}[/grey74]")
    console.print()

    # RARITY
    console.print(Rule("[bold magenta]◈ RARITY", style="magenta", align="left"))
    rarity_table = Table.grid(padding=(0, 4))
    rarity_table.add_column()
    rarity_table.add_column()
    r_items = [
        ("[white]● Common", rarity_counts['common']),
        ("[green]◆ Uncommon", rarity_counts['uncommon']),
        ("[blue]★ Rare", rarity_counts['rare']),
        ("[cyan]✦ UltraRare", rarity_counts['ultrarare']),
        ("[red]▲ Epic", rarity_counts['epic']),
        ("[yellow]🌟 Legendary", rarity_counts['legendary']),
        ("[purple]💠 Mythical", rarity_counts['mythical'])
    ]
    for i in range(0, len(r_items), 2):
        col1 = f"  {r_items[i][0]}: {r_items[i][1]}"
        col2 = f"  {r_items[i+1][0]}: {r_items[i+1][1]}" if i+1 < len(r_items) else ""
        rarity_table.add_row(col1, col2)
    console.print(rarity_table)
    console.print()

    # BALLS
    console.print(Rule("[bold yellow]◈ BALL BAG", style="yellow", align="left"))
    balls_table = Table.grid(padding=(0, 4))
    balls_table.add_column()
    balls_table.add_column()
    b_items = []
    
    # Iterate dynamically over all available ball types
    for b in all_balls:
        if balls.get(b, 0) > 0:
            name = b.replace('_', ' ').title()
            b_items.append((name, balls[b]))
            
    if not b_items:
        console.print("  [grey74]Empty")
    else:
        for i in range(0, len(b_items), 2):
            col1 = f"  ● {b_items[i][0]}: [yellow]× {b_items[i][1]}[/yellow]"
            col2 = f"  ● {b_items[i+1][0]}: [yellow]× {b_items[i+1][1]}[/yellow]" if i+1 < len(b_items) else ""
            balls_table.add_row(col1, col2)
        console.print(balls_table)
    console.print()

    # GENERATIONS
    # GENERATIONS
    console.print(Rule("[bold blue]◈ GENERATION DISCOVERY", style="blue", align="left"))
    roman = {1:'I', 2:'II', 3:'III', 4:'IV', 5:'V', 6:'VI', 7:'VII', 8:'VIII', 9:'IX'}
    caught_gens = [g for g in gen_counts if gen_counts[g] > 0]
    if not caught_gens:
        console.print("  [grey74]No Pokémon caught yet.")
    else:
        for g in caught_gens:
            console.print(f"  Gen {roman[int(g)]:<4} [cyan]{gen_counts[g]}[/cyan]")
    console.print()

    # ACHIEVEMENTS
    console.print(Rule("[bold yellow]◈ ACHIEVEMENTS", style="yellow", align="left"))
    achievements = []
    if unique_pokemon >= 10: achievements.append("[yellow]⭐ 10 Pokémon Collected[/yellow]")
    elif unique_pokemon > 0: achievements.append("[yellow]⭐ Caught your first Pokémon[/yellow]")
    if rarity_counts.get("rare", 0) > 0: achievements.append("[blue]💎 Caught your first Rare[/blue]")
    if rarity_counts.get("legendary", 0) > 0: achievements.append("[yellow]🌟 Caught a Legendary![/yellow]")
    if gen_counts.get(9, 0) > 0: achievements.append("[red]🔴 Discovered Gen IX[/red]")
    if level > 1: achievements.append(f"[green]🔰 Reached Level {level}[/green]")
    
    if not achievements:
        console.print("  [grey74]Start catching Pokémon to earn achievements!")
    else:
        for a in achievements[:3]:
            console.print(f"  {a}")
    console.print()
