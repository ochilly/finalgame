"""
A simple text adventure designed as a learning experience for new programmers.
"""
__author__ = 'Phillip Johnson'
import world
from player import Player
from items import Weapon


def play():
    world.load_tiles()
    start_items = Weapon("Rock", "A fist-sized stone.", 0, 5)
    player = Player(start_items)
    room = world.tile_exists(player.location_x, player.location_y)
    print(room.intro_text())
    while player.is_alive() and not player.victory:
        room = world.tile_exists(player.location_x, player.location_y)
        room.modify_player(player)
        # Check again since the room could have changed the player's state
        if player.is_alive() and not player.victory:
            print("\nYou must choose!\n")
            available_actions = room.available_actions()
            for action in available_actions:
                print(action)
            valid_choice = False
            action_input = input('Action: ')
            for action in available_actions:
                if action_input == action.hotkey:
                    valid_choice = True
                    player.do_action(action, **action.kwargs)
                    break
            if not valid_choice:
                print(f"\n{action_input} is not a valid action! Try Again.")


if __name__ == "__main__":
    play()
