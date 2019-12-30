# Russian Roulette game made in python. The rules are simple: Each player has to press enter to pull the trigger
# and the player that hits the chambers that contains the bullet, losses!


# After the game is over the user has the option to restart the game.

import random
import pyjokes

def russian_roulette():
    fatal_bullet = random.randint(0, 5)

    if fatal_bullet == 0:
        print('(X)', end='')
    else:
        print('(O)', end='')

    for x in range(5):
        if fatal_bullet == x+1:
            print(' X', end='')
        else:
            print(' O', end='')

    if fatal_bullet == 0:
        print(' Bang your dead!!!')

russian_roulette()

print(pyjokes.get_joke())
