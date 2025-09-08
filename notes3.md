***Pokemon Count***
Count of Pokémon by Rarity: Total 649
- Common      : 119 : 18.34
- Uncommon    : 203 : 31.28
- Rare        : 146 : 22.50
- Ultrarare   : 52  : 8.01
- Epic        : 72  : 11.09
- Legendary   : 57  : 8.78

***RARITY_MODIFIERS***
- "common": 1.0,
- "uncommon": 0.8,
- "rare": 0.6,
- "ultrarare": 0.4,
- "epic": 0.25,
- "legendary": 0.1

***Ball Modifiers***
- "poke_ball": 1.0,
- "great_ball": 1.5,
- "ultra_ball": 2.0,
- "master_ball": 100.0

***Rarity Spawn Weight***
- "common": 100,
- "uncommon": 50,
- "rare": 25,
- "ultrarare": 10,
- "epic": 5,
- "legendary": 1

weights = [RARITY_SPAWN_WEIGHTS[p['rarity']] for p in pokemon_pool]
    
wild_pokemon = random.choices(pokemon_pool, weights=weights, k=1)[0]

base_catch_chance = 0.5 # 50% base chance
rarity_mod = RARITY_MODIFIERS.get(rarity, 0.1)
ball_mod = BALL_MODIFIERS.get(ball_type, 1.0)
catch_chance = base_catch_chance * rarity_mod * ball_mod

pokemon_pool = [p for p in all_pokemon]
weights = [RARITY_SPAWN_WEIGHTS[p['rarity']] for p in pokemon_pool]
random_pokemon = random.choices(pokemon_pool, weights=weights, k=1)[0]

