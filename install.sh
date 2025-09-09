#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="/usr/local/bin/pokecatch"

echo "This script will create a symbolic link from your script to ${DEST}."
echo "You may be asked for your administrator password."

sudo ln -sf "${SCRIPT_DIR}/pokecatch" "${DEST}"

echo ""
echo "✅ Installation complete!"
echo "You can now run the game by typing 'pokecatch hunt' in your terminal."