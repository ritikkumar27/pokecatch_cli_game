# PokéCatch CLI

A Pokémon-catching game that lives entirely in your terminal. You hunt for wild Pokémon, decide which of the 11 Poké Ball types is worth using on each one, manage an inventory, level up, and slowly fill out a Pokédex — with actual sprites rendered inline if your terminal supports it.

I built this mostly to see how far I could push a terminal UI before it stopped feeling like a toy, and to play around with `rich` for the dashboards.

> **Note:** Images are rendered with `term-image`. It'll work in most terminals, but for the images to actually look good, use something like Kitty or WezTerm — they support the newer image protocols. In a plain terminal you'll still get everything, just no sprites.

---

## What's in it

- **All 1025 Pokémon**, across all 9 generations, in the hunting pool.
- **Rarity tiers** — 7 of them, from Common up to Mythical, each with its own spawn weight and sell value.
- **Leveling** — XP from hunting and catching, which unlocks store discounts and better gear as you go.
- **11 Poké Balls**, each with a different situational bonus — some care about typing, some about stats, one even checks the real-world time of day.
- **A store that actually rotates** — stock changes daily, and you fund purchases by selling off duplicates.
- **Dashboards for stats, Pokédex, and the store**, built with `rich` so it's not just a wall of text.

---

## Installation

1. Clone it:
   ```bash
   git clone https://github.com/ritikkumar27/pokecatch_cli_game.git
   cd pokecatch_cli_game
   ```

2. Install dependencies (needs Python 3):
   ```bash
   pip install -r requirements.txt
   ```
   This pulls in `rich`, `Pillow`, and `term-image`.

3. Install the CLI globally:
   ```bash
   ./install.sh
   ```

4. Play:
   ```bash
   pokecatch hunt
   ```

---

## Commands

| Command | Alias | What it does |
|---|---|---|
| `pokecatch hunt` | | Search for a wild Pokémon. |
| `pokecatch catch <ball>` | | Try to catch whatever you just found. |
| `pokecatch stats` | `s` | Trainer profile — XP, level, stats. |
| `pokecatch pokedex` | `dex` | Your caught Pokémon, filterable/sortable. |
| `pokecatch inventory` | `inv` | Your Poké Balls and Poké Dollars. |
| `pokecatch store` | | Open the store. |
| `pokecatch store buy <item> <qty>` | | Buy something. |
| `pokecatch store sell <name>` | | Sell one specific Pokémon. |
| `pokecatch store sell-dupes` | | Sells every duplicate at once, keeps one of each species — mostly here because doing this manually got tedious fast. |
| `pokecatch store sellall <rarity>` | | Sell everything of a given rarity. |

You can also filter/sort the Pokédex directly:
- `pokecatch dex pikachu` — details on one Pokémon
- `pokecatch dex --gen 3 --type water` — Gen 3 water types you own
- `pokecatch dex --sort rarity` — sorted by rarity

---

## How the mechanics work

### Encounter odds

Every hunt rolls a rarity tier first, then picks a random Pokémon from that pool.

| Rarity | Spawn chance | Sell value |
|---|---|---|
| Common | 50.0% | ₽30 |
| Uncommon | 28.0% | ₽75 |
| Rare | 12.0% | ₽300 |
| UltraRare | 6.0% | ₽500 |
| Epic | 2.5% | ₽1,000 |
| Legendary | 1.0% | ₽3,500 |
| Mythical | 0.5% | ₽7,500 |

### XP and leveling

- Hunting: +5 XP, just for trying.
- Catching: varies by rarity — 10 XP for a Common, up to 1000 XP for a Mythical.
- First-time catch of a species: double XP, as an incentive to actually go for new stuff instead of farming Commons.

Leveling up raises your base catch rate and eventually gets you up to a 15% discount at the store.

### Catching

The formula is straightforward:

`Base rate × Ball multiplier × Level bonus`

Base rates by rarity: Common 50%, Uncommon 40%, Rare 30%, UltraRare 20%, Epic 10%, Legendary 5%, Mythical 2%.

Balls (type the full name or the alias — `great_ball` or `gb`, either works):

| Ball | Alias | Effect | Unlocks at |
|---|---|---|---|
| Poké Ball | `pb` | 1.0x, baseline. | Lv 1 |
| Great Ball | `gb` | 1.5x. | Lv 3 |
| Ultra Ball | `ub` | 2.0x. | Lv 8 |
| Net Ball | `net` | 3.0x on Water or Bug types. | Lv 5 |
| Dive Ball | `dive` | 3.5x on Water types. | Lv 5 |
| Fast Ball | `fast` | 2.0x if Speed ≥ 80, 3.0x if Speed ≥ 120. | Lv 5 |
| Dusk Ball | `dusk` | 3.5x if it's night (6 PM–6 AM) when you catch. | Lv 5 |
| Nest Ball | `nest` | 2.0x if BST ≤ 400, 3.0x if BST ≤ 300 — good against low-stat mons. | Lv 10 |
| Repeat Ball | `repeat` | 3.0x if you already own that species. | Lv 10 |
| Quick Ball | `quick` | Flat 2.5x, no conditions. | Lv 15 |
| Master Ball | `mb` | Guaranteed catch. | Lv 25 |

The idea was to make ball choice actually matter instead of just "use the best one you have" — a Dusk Ball at night or a Repeat Ball on something you're farming for dupes can outperform an Ultra Ball if you're paying attention.

---
