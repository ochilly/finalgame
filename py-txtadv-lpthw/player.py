"""Player with relevant attributes and possible actions"""

import random
import items
import world


class Player(object):

    def __init__(self, *initial_items):
        self.health = 100
        self.victory = False
        self.location_x, self.location_y = world.starting_position
        self.inventory = items.Inventory(slots=5)
        if initial_items:
            for item in initial_items:
                self.inventory.store(item)

    def is_alive(self):
        return self.health > 0

    def print_inventory(self):
        print(self.inventory, '\n')

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_west(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        best_weapon = None
        max_dmg = 0
        for weapon in self.inventory.contents('Weapon'):
            if weapon.damage > max_dmg:
                max_dmg = weapon.damage
                best_weapon = weapon

        print("You use {} against {}!".format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print("You killed {}!".format(enemy.name))
        else:
            print("{} HP is {}.".format(enemy.name, enemy.hp))

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        r = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[r])


if __name__ == '__main__':
    def main():
        player = Player()
        player.inventory.store(items.Gold(3))
        print(player.inventory)

    main()
