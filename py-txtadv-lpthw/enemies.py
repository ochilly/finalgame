"""Defines the enemies in the game"""


class Enemy:
    """A base class for all enemies"""
    def __init__(self, name, health, damage):
        """Creates a new enemy

        :param name: the name of the enemy
        :param health: the hit points of the enemy
        :param damage: the damage the enemy does with each attack
        """
        self.name = name
        self.health = health
        self.damage = damage

    def is_alive(self):
        return self.health > 0


class GiantSpider(Enemy):
    def __init__(self):
        super().__init__(name="Giant Spider", health=10, damage=2)


class Ogre(Enemy):
    def __init__(self):
        super().__init__(name="Ogre", health=30, damage=15)
