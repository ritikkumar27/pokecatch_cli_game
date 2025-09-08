# Pokecatch Game

Pokecatch is a command-line Pokémon catching game designed for the Kitty terminal. Hunt for wild Pokémon, catch them using different Poké Balls, and build your own Pokédex!

## Features

- **Hunt** for wild Pokémon with rarity-based spawn chances.
- **Catch** Pokémon using various Poké Balls, each with different catch rates.
- **View** your caught Pokémon in a Pokédex-style list.
- **Display** Pokémon sprites directly in the Kitty terminal.

## Requirements

- Python 3
- [Kitty terminal](https://sw.kovidgoyal.net/kitty/)
- ImageMagick (`convert` command)

## Installation

1. Clone this repository.
2. Ensure you have Kitty terminal and ImageMagick installed.
3. Make the `pokecatch` script executable:
   ```sh
   chmod +x pokecatch
   ```

## Usage

Run the game from your project directory:

```sh
./pokecatch hunt
./pokecatch catch poke_ball
./pokecatch my_pokemon
```

### Commands

- `hunt` : Search for a wild Pokémon.
- `catch <ball_type>` : Attempt to catch the current wild Pokémon. Ball types: `poke_ball`, `great_ball`, `ultra_ball`, `master_ball`.
- `my_pokemon` or `pokedex` : View your caught Pokémon.
- `terminal_pokemon` : Display a random Pokémon sprite in the terminal.

## Data Files

- Pokémon data: [`data/pokemon_data.json`](data/pokemon_data.json)
- Your Pokédex: [`data/pokedex.json`](data/pokedex.json)
- Sprites: [`sprites/`](sprites/)

## Notes

- Sprites are displayed using Kitty's image protocol.

