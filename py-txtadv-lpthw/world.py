"""loads in and checks world/map tiles"""

import os


_world = {}
starting_position = (0, 0)


def tile_exists(x, y):
        """Returns the tile at the given coordinates or None if there is no tile.

        :param x: the x-coordinate in the worldspace
        :param y: the y-coordinate in the worldspace
        :return: the tile at the given coordinates or None if there is no tile
        """
        return _world.get((x, y))


def load_tiles():
    """Parses a file that describes the world space into the _world object"""
    script_path = os.path.dirname(os.path.realpath(__file__))
    # a similar alternative: import sys, script_path = sys.path[0]
    with open(f'{script_path}/../resources/map.txt', 'r') as map_file:
        rows = map_file.readlines()
    x_max = len(rows[0].split('\t'))
    for y in range(len(rows)):
        cols = rows[y].split('\t')
        for x in range(x_max):
            tile_name = cols[x].replace('\n', '')
            if tile_name == 'StartingRoom':
                global starting_position
                starting_position = (x, y)
            _world[(x, y)] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)
