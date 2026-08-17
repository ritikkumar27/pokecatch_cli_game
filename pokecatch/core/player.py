from pokecatch.config import PLAYER_DATA_FILE, PLAYER_DEX
from pokecatch.utils import load_data, save_data, display_sprite_pokedex

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
            "last_hunt_time": 0 
        }
        save_data(PLAYER_DATA_FILE, player_data)
        return player_data
        
    data = load_data(PLAYER_DATA_FILE)
    # Ensure existing players get an xp field without losing their save
    if "xp" not in data:
        data["xp"] = 0
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
    print(f"╭{'─'*72}╮")
    title = "YOUR POKÉDEX"
    stats_str = f"{unique_species} / 1025 species  ·  {total_caught} caught"
    print(f"│ {title:^70} │")
    print(f"│ {stats_str:^70} │")
    print(f"╰{'─'*72}╯\n")
    if not page_items:
        print("No Pokémon match your current filters.")
        return
    print(f"Showing {start_idx + 1}–{end_idx} of {total_filtered} species (Page {page}/{total_pages})\n")
    print(f" {'#':<4}   {'Pokémon':<15} {'Owned':<8} {'Type':<20} {'BST'}")
    print(f" {'─'*71}")
    
    for s in page_items:
        p = s['pokemon']
        count_str = f"×{s['count']}"
        types_str = " / ".join([t.capitalize() for t in p.get('types', [])])
        bst = p.get('stats', {}).get('Total', '?')
        
        print(f" {p['id']:03d}    {p['name'].capitalize():<15} {count_str:<8} {types_str:<20} {bst}")
    if page < total_pages:
        print(f"\nUse 'pokecatch pokedex --page {page + 1}' to see more.")

