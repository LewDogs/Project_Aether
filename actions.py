# import random
import utils
from world import World
from player import Player

world = World()
hero = Player()

class GeneralActions:
    def __init__(self):
        self.directions = ["n","s","e","w"]
    
    def manage_directions(self, action):
        # Check if it is a valid exit in this room
        print(world.loc_exits())
        if hasattr(world.loc_exits(), action):
            # If exit exists, move the hero to that location
            hero.current_location = getattr(utils.get_current_room_attr('exits', world), action)
            utils.next_prompt(world.loc_name())
            utils.next_prompt(world.loc_desc())
            if not hero.current_location in hero.visited:
                hero.visited.add(hero.current_location)
        else:
            print("Exit doesn't exist")
    
    def manage_action(self, action):
        match action:
            case "map":
                world.reveal_map()
            case "exits":
                exits = utils.get_current_room_attr('exits', world)
                print(list(vars(exits).keys()))
            case "items":
                print(world.loc_items())
            case action.startswith("take"):
                print("You want to " + action)
            case _: 
                print("I don't know what you mean...")

