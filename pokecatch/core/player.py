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
                "xp_from_catching": 0
            }
        }
        save_data(PLAYER_DATA_FILE, player_data)
        return player_data
        
    data = load_data(PLAYER_DATA_FILE)
    if "xp" not in data:
        data["xp"] = 0
    # Ensure existing players get a stats field without losing their save
    if "stats" not in data:
        data["stats"] = {
            "total_hunts": 0,
            "successful_catches": 0,
            "failed_catches": 0,
            "first_time_catches": 0,
            "xp_from_hunting": 0,
            "xp_from_catching": 0
        }
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
    # --- ANSI COLOR CODES ---
    class C:
        HEADING = '\033[1;37m'  # Bold White
        YELLOW  = '\033[93m'    # Bright Yellow
        GREEN   = '\033[92m'    # Bright Green
        RED     = '\033[91m'    # Bright Red
        CYAN    = '\033[96m'    # Bright Cyan
        PURPLE  = '\033[95m'    # Bright Purple
        GRAY    = '\033[90m'    # Dark Gray
        RESET   = '\033[0m'     # Reset all formatting
    player_data = load_player_data()
    player_dex = load_data(PLAYER_DEX)
    s = player_data.get("stats", {})
    import getpass
    username = getpass.getuser().upper()
    # TRAINER
    xp = player_data.get("xp", 0)
    level = get_player_level(xp)
    next_level_xp = int(100 * (level ** 1.5))
    prev_level_xp = int(100 * ((level-1) ** 1.5)) if level > 1 else 0
    
    xp_in_level = xp - prev_level_xp
    xp_needed_for_level = next_level_xp - prev_level_xp
    currency = player_data.get("currency", 0)
    xp_pct = (xp_in_level / xp_needed_for_level * 100) if xp_needed_for_level > 0 else 0
    # COLLECTION & GENERATIONS & RARITY
    species_data = {}
    total_pokemon = len(player_dex)
    rarity_counts = {"common": 0, "uncommon": 0, "rare": 0, "ultrarare": 0, "epic": 0, "legendary": 0, "mythical": 0}
    gen_counts = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
    for p in player_dex:
        pid = p['id']
        rarity = p.get('rarity', 'common').lower()
        if rarity in rarity_counts:
            rarity_counts[rarity] += 1
        
        if pid not in species_data:
            species_data[pid] = p
            gen = get_generation(pid)
            if gen in gen_counts:
                gen_counts[gen] += 1
    unique_pokemon = len(species_data)
    total_species_in_game = 1025
    col_prog_pct = (unique_pokemon / total_species_in_game) * 100
    # HUNTING
    total_hunts = s.get("total_hunts", 0)
    success = s.get("successful_catches", 0)
    failed = s.get("failed_catches", 0)
    catch_rate = (success / total_hunts * 100) if total_hunts > 0 else 0.0
    # BALLS
    balls = player_data.get("balls", {})
    ball_icons = {"poke_ball": "●", "great_ball": "◐", "ultra_ball": "◉", "master_ball": "✦"}
    rarity_icons = {"common": "●", "uncommon": "◆", "rare": "★", "epic": "◆", "legendary": "✦"}
    
    # Helper to colorize rarity strings based on tier
    def color_rarity(tier):
        if tier in ["legendary", "mythical", "epic"]: return C.PURPLE
        if tier in ["rare", "ultrarare"]: return C.CYAN
        if tier == "uncommon": return C.GREEN
        return C.GRAY
    
    # ------------------ PRINTING DASHBOARD ------------------
    print(f"\n{C.HEADING}╭{'─'*56}╮{C.RESET}")
    print(f"{C.HEADING}│{'◈ TRAINER PROFILE ◈':^56}│{C.RESET}")
    print(f"{C.HEADING}╰{'─'*56}╯{C.RESET}\n")
    print(f"  {C.HEADING}{username}{C.RESET}  ·  {C.YELLOW}₽ {currency:,}{C.RESET}")
    print(f"  Level {C.HEADING}{level}{C.RESET}  ·  {C.YELLOW}{xp_pct:.0f}%{C.RESET}  ({C.GRAY}{xp:,} / {next_level_xp:,} XP{C.RESET})\n")
    print(f"  {C.HEADING}◈ COLLECTION{C.RESET}")
    print(f"    Total Caught: {C.CYAN}{total_pokemon:<12}{C.RESET} Unique Species: {C.CYAN}{unique_pokemon}{C.RESET}")
    print(f"    Pokédex:      {C.CYAN}{col_prog_pct:.1f}%{C.RESET} {C.GRAY}({unique_pokemon} / 1025){C.RESET}\n")
    print(f"  {C.HEADING}◈ HUNTING & ACTIVITY{C.RESET}")
    print(f"    Total Hunts:  {C.HEADING}{total_hunts:<12}{C.RESET} Catch Rate:     {C.HEADING}{catch_rate:.1f}%{C.RESET}")
    print(f"    Successful:   {C.GREEN}{success:<12}{C.RESET} Failed:         {C.RED}{failed}{C.RESET}")
    print(f"    First Catch:  {C.CYAN}{s.get('first_time_catches', 0):<12}{C.RESET} Duplicates:     {C.GRAY}{success - s.get('first_time_catches', 0)}{C.RESET}\n")
    print(f"  {C.HEADING}◈ BALL BAG{C.RESET}")
    if not any(balls.values()):
        print(f"    {C.GRAY}(Empty){C.RESET}\n")
    else:
        for b in ["poke_ball", "great_ball", "ultra_ball", "master_ball"]:
            if balls.get(b, 0) > 0:
                name = b.replace('_', ' ').title()
                icon = ball_icons.get(b, "●")
                print(f"    {icon} {name:<14} × {C.HEADING}{balls[b]}{C.RESET}")
        print()
    print(f"  {C.HEADING}◈ RARITY BREAKDOWN{C.RESET}")
    r_keys = ["common", "uncommon", "rare", "epic", "legendary"]
    half = (len(r_keys) + 1) // 2
    for i in range(half):
        k1 = r_keys[i]
        c1 = color_rarity(k1)
        str1 = f"{c1}{rarity_icons.get(k1, '●')} {k1.capitalize()}: {rarity_counts.get(k1, 0)}{C.RESET}"
        
        if i + half < len(r_keys):
            k2 = r_keys[i + half]
            c2 = color_rarity(k2)
            str2 = f"{c2}{rarity_icons.get(k2, '●')} {k2.capitalize()}: {rarity_counts.get(k2, 0)}{C.RESET}"
        else:
            str2 = ""
            
        # We have to account for hidden ANSI characters when formatting columns, 
        # so we just add a manual spacer instead of using standard ljust
        spacer = " " * (25 - len(f"● {k1.capitalize()}: {rarity_counts.get(k1, 0)}"))
        print(f"    {str1}{spacer}{str2}")
    print()
    print(f"  {C.HEADING}◈ GENERATION DISCOVERY{C.RESET}")
    roman_gens = {1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V', 6: 'VI', 7: 'VII', 8: 'VIII', 9: 'IX'}
    gen_keys = [k for k, v in gen_counts.items() if v > 0]
    if not gen_keys:
        print(f"    {C.GRAY}No Pokémon caught yet.{C.RESET}\n")
    else:
        for g in gen_keys:
            print(f"    Gen {roman_gens[g]:<4} {C.CYAN}{gen_counts[g]}{C.RESET}")
        print()
    print(f"  {C.HEADING}◈ RECENT ACHIEVEMENTS{C.RESET}")
    achievements = []
    if unique_pokemon >= 10: achievements.append(f"{C.YELLOW}✦ 10 Pokémon Collected{C.RESET}")
    elif unique_pokemon > 0: achievements.append(f"{C.YELLOW}✦ Caught your first Pokémon{C.RESET}")
    
    if rarity_counts.get("rare", 0) > 0: achievements.append(f"{C.PURPLE}✦ Caught your first Rare Pokémon{C.RESET}")
    if rarity_counts.get("legendary", 0) > 0: achievements.append(f"{C.PURPLE}✦ Caught a Legendary Pokémon!{C.RESET}")
    if gen_counts.get(9, 0) > 0: achievements.append(f"{C.CYAN}✦ Discovered Generation IX{C.RESET}")
    if level > 1: achievements.append(f"{C.GREEN}✦ Reached Trainer Level {level}{C.RESET}")
    
    if not achievements:
        print(f"    {C.GRAY}(Start catching Pokémon to earn achievements!){C.RESET}")
    else:
        for a in achievements[:3]:
            print(f"    {a}")
    print()