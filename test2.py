
import time
import sys

def endless_dots(duration=5, interval=0.5):
    start = time.time()
    dots = ""
    while time.time() - start < duration:
        dots += "."
        sys.stdout.write(f"\rFighting{dots}")
        sys.stdout.flush()
        time.sleep(interval)
    print()  # move to next line after finishing

# Example: run for 5 seconds, adding a dot every 0.5s
endless_dots(5, 0.5)
print("ritik")

# import time
# import sys

# def animated_dots(duration=2, interval=0.5):
#     elapsed = 0
#     while elapsed < duration:
#         for dots in ['.', '..', '...']:
#             sys.stdout.write(f'\rFighting{dots}')  # extra spaces to overwrite
#             sys.stdout.flush()
#             time.sleep(interval)
#             elapsed += interval
#             if elapsed >= duration:
#                 break
#     sys.stdout.write('\r' + ' ' * 20 + '\r')  # clear line completely

# animated_dots(5, 0.5)
# time.sleep(2)
# print("ritik")



# import time
# import sys
# import random

# # catch_chance = base_catch_chance * rarity_mod * ball_mod

# # Animation function
# def animated_dots(duration=2, interval=0.5):
#     elapsed = 0
#     while elapsed < duration:
#         for dots in ['.', '..', '...']:
#             sys.stdout.write(f'\rFighting{dots}')
#             sys.stdout.flush()
#             time.sleep(interval)
#             elapsed += interval
#             if elapsed >= duration:
#                 break
#     print('\r', end='')  # Clear line after animation

# # Example usage
# animated_dots(2, 0.5)  # 2 seconds, 0.5 sec per dot
# time.sleep(2)
# sys.stdout.flush()
# print("ritik")

# # if random.random() < catch_chance:
# #     print(f"Gotcha! {pokemon_name.capitalize()} was caught!")
# #     player_dex = load_data(PLAYER_DEX)
# #     player_dex.append(wild_pokemon)
# #     save_data(PLAYER_DEX, player_dex)
# # else:
#     # print(f"Oh no! {pokemon_name.capitalize()} broke free!")
