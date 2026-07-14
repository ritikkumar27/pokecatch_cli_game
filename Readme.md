# PokéCatch CLI

A command-line Pokémon catching game for the Kitty terminal. Hunt for wild Pokémon, catch them using different Poké Balls, manage your inventory, and build your Pokédex with sprites rendered directly in your terminal!

 <!-- Replace with a real screenshot or GIF of your game! -->

## Features

- **Gotta Catch 'Em All:** Hunt for Pokémon with spawn chances weighted by rarity (Common, Uncommon, Rare, Ultra-Rare, Epic, and Legendary).
- **Strategic Catching:** Use four different types of Poké Balls (`Poke`, `Great`, `Ultra`, `Master`), each with unique catch rates depending on the Pokémon's rarity.
- **Your Personal Pokédex:** View all your caught Pokémon, complete with their sprites, sorted by Pokédex number.
- **Inventory Management:** Keep track of your Poké Balls and your earnings in Poké Coins.
- **Poké Mart Economy:** Visit the store to buy more Poké Balls or sell your caught Pokémon for Coins.
- **Bulk Selling:** Quickly earn money by selling all Pokémon of a specific rarity at once.

## Requirements

- Python 3
- Kitty terminal
- ImageMagick (the `magick` command must be available in your PATH)

## Installation

1.  **Clone the repository:**
    ```
    git clone https://github.com/ritikkumar27/pokecatch_cli_game.git
    ```

2.  **Navigate into the directory:**
    ```
    cd pokecatch_cli_game
    ```

3.  **Run the installation script:**
    This will create a symbolic link to make the `pokecatch` command available system-wide. You may be prompted for your administrator (`sudo`) password.
    ```
    ./install.sh
    ```

4.  **Start playing!**
    You can now run the game from any directory.
    ```
    pokecatch hunt
    ```

### Commands

The game is run using the `pokecatch` command followed by a subcommand.

| Command | Description |
|---|---|
| `pokecatch hunt` | Search for a wild Pokémon. |
| `pokecatch catch <ball_type>` | Attempt to catch the current wild Pokémon. |
| `pokecatch pokedex` | View your collection of caught Pokémon. (Alias: `my_pokemon`) |
| `pokecatch inventory` | Check your current Poké Balls and Poké Dollars. |
| `pokecatch store` | Visit the Poké Mart to see prices. |
| `pokecatch store buy <item> [amount]` | Buy Poké Balls. `amount` is optional and defaults to 1. |
| `pokecatch store sell <pokemon_name>` | Sell a specific Pokémon from your collection. |
| `pokecatch store sellall <rarity>` | Sell all Pokémon of a specific rarity. |

#### Ball Types
The `<ball_type>` argument for the `catch` command. It can be the full name or a shortcut:
- `poke_ball` (or `pb`)
- `great_ball` (or `gb`)
- `ultra_ball` (or `ub`)
- `master_ball` (or `mb`)

#### Rarity Types
The `<rarity>` argument for the `sellall` command can be:
`common`, `uncommon`, `rare`, `ultrarare`, `epic`, `legendary`.

### Catch Rates

| Rarity    | Poké Ball | Great Ball | Ultra Ball | Master Ball |
| :-------- | :-------- | :--------- | :--------- | :---------- |
| **Common** | 50%       | 90%        | 100%       | 100%        |
| **Uncommon** | 40%       | 75%        | 100%       | 100%        |
| **Rare** | 30%       | 60%        | 80%        | 100%        |
| **Ultrarare** | 20%       | 30%        | 75%        | 100%        |
| **Epic** | 15%       | 20%        | 51%        | 100%        |
| **Legendary** | 5%        | 20%        | 25%        | 61%         |

<!-- ## Game Data & Resetting Progress -->

Missed my today's commit, lmao

<!-- Your game progress is stored in the `data/` directory:
- `pokedex.json`: Contains all the Pokémon you have caught.
- `player.json`: Stores your inventory and currency.

To reset your game and start over, simply delete these two files. -->

