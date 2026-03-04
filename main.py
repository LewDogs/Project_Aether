# Import Classes
from player import Player
from world import World
from actions import GeneralActions

import utils

# Main part of the script
if __name__ == "__main__":
    # Initialise Player Object
    hero = Player()

    # Initialise World Object
    the_world = World()
    the_world.build_map(utils.load_map_file('map.csv'))
    
    # Initialise Actions Object
    actions = GeneralActions()

    # Start building your character
    hero.init_player(False)

    # Start the game. Play the intro sequence
    the_world.begin()

    # Begin the game loop
    play = True
    while(play):
        action = input("What would you like to do? ")
        if action == "quit":
            play = False
        elif action in actions.directions:
            actions.manage_directions(action)
        else:
            actions.manage_action(action)

