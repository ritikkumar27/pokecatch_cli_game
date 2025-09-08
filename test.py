# def display_sprite_terminal():


#     all_pokemon = load_data(DATA_FILE)
#     if not all_pokemon:
#         print("Error: pokemon_data.json is empty or not found!")
#         return
#     # Weighted random choice based on rarity
#     pokemon_pool = [p for p in all_pokemon]
#     weights = [RARITY_SPAWN_WEIGHTS[p['rarity']] for p in pokemon_pool]
#     random_pokemon = random.choices(pokemon_pool, weights=weights, k=1)[0]



#     """Displays the pokemon sprite in the Kitty terminal."""
#     sprite_path = os.path.join(SPRITES_DIR, f"{random_pokemon['name']}.png")
#     if not os.path.exists(sprite_path):
#         print(f"Sprite for {random_pokemon['name']} not found!")
#         return
    
#     #using shlex.quote() to handle filenames with spaces or special characters
#     safe_sprite_path = shlex.quote(sprite_path)
#     #the full command as a single string
#     command = (f"convert {safe_sprite_path} -filter Hermite -resize 150% -trim png:- | kitty +kitten  icat --stdin=yes --align left")
#     try:
#         #use shell = True to interepret the pipe
#         subprocess.run(command, shell=True, check=True)
#         #***old line*** subprocess.run(["kitty", "+icat", "--align", "left","--scale-up", sprite_path], check=True)
        
#     except FileNotFoundError:
#         print("This game requires the Kitty terminal to display images.")
#     except Exception as e:
#         print(f"Error displaying image: {e}")