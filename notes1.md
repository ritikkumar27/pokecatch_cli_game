command:
-------------------------------------------------------------------

NEW:


magick /home/duckworth/pokecatch_game/sprites/149.png -filter Box -define filter:blur=0.8 -resize 230% -trim png:- | kitty +kitten  icat --stdin=yes --align left





--------------------------------------------------------------------
//decided : but not working
"convert", sprite_path, "-filter", "Hermite", "-resize", "250%", "-trim", "png:-", "|", "kitty", "+kitten",  "icat", "--stdin=yes", "--align", "left"

convert /home/duckworth/Downloads/generation-5/pokemon/main-sprites/black-white/493.png -filter Hermite -resize 250% -trim png:- | kitty +kitten  icat --stdin=yes --align left

subprocess.run(["convert", sprite_path, "-filter", "Hermite", "-resize", "250%", "-trim", "png:-", "|", "kitty", "+kitten",  "icat", "--stdin=yes", "--align", "left"], check=True)





-----------------------------------------------------------------

//most convinient : crystal clear
 convert /home/duckworth/Downloads/generation-5/pokemon/main-sprites/black-white/6.png -sample 250% -trim png:- | kitty +kitten  icat --stdin=yes --align left

//most convinient : blurred clear


--------------------------------

***TESTING***

filter Hermite resize 250%:
convert /home/duckworth/Downloads/generation-5/pokemon/main-sprites/black-white/493.png -filter Hermite -resize 250% -trim png:- | kitty +kitten  icat --stdin=yes --align left

adaptive resize
convert /home/duckworth/Downloads/generation-5/pokemon/main-sprites/black-white/149.png -adaptive-resize 250% -trim png:- | kitty +kitten  icat --stdin=yes --align left

sample:
convert /home/duckworth/Downloads/generation-5/pokemon/main-sprites/black-white/493.png -sample 250% -trim png:- | kitty +kitten  icat --stdin=yes --align left

resize:
convert /home/duckworth/Downloads/generation-5/pokemon/main-sprites/black-white/493.png -resize 250% -trim png:- | kitty +kitten  icat --stdin=yes --align left













---------------------------------------------------------------------------------------------------------------
//discarded
convert /home/duckworth/pokecatch_game/sprites/bulbasaur.png -trim png:- | kitty +kitten icat --stdin=yes --scale-up

//blurred
convert /home/duckworth/pokecatch_game/sprites/bulbasaur.png -resize 900% -trim png:- | kitty +kitten  icat --stdin=yes --align left


//crystal clear
convert /home/duckworth/pokecatch_game/sprites/bulbasaur.png -sample 900% -trim png:- | kitty +kitten  icat --stdin=yes --align left



//blurry image : gen 5 pokemon database
convert /home/duckworth/Downloads/generation-5/pokemon/main-sprites/black-white/384.png -resize 500% -trim png:- | kitty +kitten  icat --stdin=yes --align left

//crystal clear image with gen 5 pokemon database
 convert /home/duckworth/Downloads/generation-5/pokemon/main-sprites/black-white/384.png -sample 500% -trim png:- | kitty +kitten  icat --stdin=yes --align left



Initialized empty Git repository in /home/duckworth/pokecatch_game/.git/



 
