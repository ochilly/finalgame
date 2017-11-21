"""Player with relevant attributes and possible actions"""

import items
import world


class Player(object):

    def __init__(self):
        self.inventory = items.Inventory(10, items.Gold(5))
        self.hit_points = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False

    def is_alive(self):
        return self.hit_points > 0

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        # TODO: some print statement

    def move_north(self):
        self.move(dx=0, dy=-1)

    def move_east(self):
        self.move(dx=1, dy=0)

    def move_south(self):
        self.move(dx=0, dy=1)

    def move_west(self):
        self.move(dx=-1, dy=0)


if __name__ == '__main__':
    def main():
        player = Player()
        player.inventory.store(items.Gold(3))
        print(player.inventory)

    main()
