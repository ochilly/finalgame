"""Items and Inventory for 'holding'/tracking Items"""

from collections import defaultdict


class Item(object):

    """Base class for all Items."""

    def __init__(self, name, description, value=0):
        """
        :param str name: Item name seen by a player.
        :param str description: 'Flavor' text seen by a player.
        :param int value: The value in currency.

        """
        self.name = str(name)
        self.description = str(description)
        self.value = int(value)
        self._pane_width = 26
        self._pane_divider = ''.join(['+', '-' * self._pane_width, '+'])

    @property
    def pane_width(self):
        return self._pane_width

    @pane_width.setter
    def pane_width(self, width):
        if width >= 0:
            self._pane_width = width
            self._pane_divider = ''.join(['+', '-' * width, '+'])
        else:
            pass

    @property
    def pane_divider(self):
        return self._pane_divider

    @pane_divider.setter
    def pane_divider(self, text):
        return

    def __repr__(self):
        return '{}(\"{}\", \"{}\", {})'.format(
            self.__class__.__name__,
            self.name,
            self.description,
            self.value
            )

    def __str__(self):
        return '\n\n{}\n| {:^{}} |\n{}\n| {:{}} |\n| Value:{:>{}} |\n{}'.format(
            self.pane_divider,
            self.name,
            self.pane_width - 2,
            self.pane_divider,
            ''.join(['\"', self.description, '\"']),
            self.pane_width - 2,
            self.value,
            self.pane_width - 8,
            self.pane_divider
            )

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, Item):
            return hash(self) == hash(other)
        else:
            return False


class Inventory(object):

    """
    Manages Items as a defaultdict(list, Class: object).
    Defaults to 5 slots total space
    Optionally, pass in items during construction

    """

    def __init__(self, slots=5, *initial_items):
        # TODO: what if user tries Inventory(Item1,Item2)???
        self.capacity = self.free = slots
        self.used = 0
        self._currency = 0
        self._contents = defaultdict(list)
        for item in initial_items:
            self.store(item)

    def __repr__(self):
        return '{}({}, {}, {})'.format(
            self.__class__.__name__,
            self.capacity,
            repr(Gold(self._currency)),
            ''.join([repr(item) + ', ' for item in self.contents()]
                    ).rstrip(', ')
            )

    def __str__(self):
        return ''.join([str(item) for item in self.contents()])

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, Inventory):
            return hash(self) == hash(other)
        else:
            return False

    def __len__(self):
        return self.used

    def contents(self, *types):
        """Return Items of specific type/s or a complete list."""
        if types:
            return [item
                    for item_type in types
                    for item in self._contents[item_type.capitalize()]
                    ]
        else:
            return [item
                    for items in self._contents.values()
                    for item in items
                    ]

    def is_full(self):
        """Return True if Inventory is full."""
        return self.used >= self.capacity

    def expand(self, amount_to_expand=1):
        """Increase total space an Inventory can hold.
        :param amount_to_expand int: default 1

        """
        self.capacity += amount_to_expand
        self.free += amount_to_expand

    def shrink(self, amount_to_shrink=1):
        """Reduce total space an Inventory can hold."""
        # TODO: what if they now have too many items?
        self.capacity -= amount_to_shrink
        self.free -= amount_to_shrink

    def store(self, *items):
        """Accept any amount of Items to Inventory."""
        # TODO: Better error handling for full inventory
        for item in items:
            item_type = item.__class__.__name__
            if item_type == 'Gold':
                self._currency += item.value
            elif not self.is_full():
                self._contents[item_type].append(item)
                self.used += 1
                self.free -= 1
            else:
                print(f"Inventory full. {item.name} not stored.")

    def drop(self, *items):
        """Remove any amount of Items from inventory."""
        for item in items:
            item_type = item.__class__.__name__
            if item in self.contents(item_type):
                self._contents[item_type].remove(item)
                self.used -= 1
                self.free += 1


class Weapon(Item):

    def __init__(self, name, description, value=0, damage=0):
        self.damage = int(damage)
        super().__init__(name, description, value)

    def __repr__(self):
        return ''.join([super().__repr__().rstrip(')'), f", {self.damage})"])

    def __str__(self):
        return "{}\n| Damage:{:>{}} |\n{}".format(
                    super().__str__(),
                    self.damage,
                    self.pane_width - 9,
                    self.pane_divider
                )

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, Weapon):
            return hash(self) == hash(other)
        else:
            return False


class Gold(Item):

    _name = "Gold Coins"

    @property
    def name(self):
        return type(self)._name

    def __init__(self, amount_of_coins=1):
        self.description = "Valuable coins, worn from handing."
        self.value = amount_of_coins

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value})'

    def __str__(self):
        return '\n {} {}\n{}\n"{}"\n'.format(
            self.value,
            self.name,
            '=' * (len(self.name) + len(str(self.value)) + 3),
            self.description,
        )


class Key(Item):

    def __init__(self, name, description='Opens a lock'):
        super().__init__(name, description)

    def __str__(self):
        return super().__str__()

    def __repr__(self):
        return '{}(\"{}\", \"{}\")'.format(
            self.__class__.__name__,
            self.name,
            self.description
            )


if __name__ == '__main__':
    def main():
        weapon1 = Weapon("Ass BlasTer 9000", "super shiny thang", 12_000, 100)
        gold_key = Key("Gold Key", "A Lustrous Key to somewhere")
        silver_key = Key("Silver Key", "A Shiny Key")
        gold1 = Gold()
        gold2 = Gold(23)

        backpack1 = Inventory(10)

        print("### TESTING Inventory.store() and drop()\n")
        print(f"slots filled: {backpack1.used}")
        print(f"adding 2 Gold items to backpack1 using *args")
        backpack1.store(gold1, gold2)
        print(f"slots filled: {backpack1.used}")
        print(f"adding 5 items to backpack1.")
        backpack1.store(Item("test_of_item", "this is a test", "9_000_000"))
        backpack1.store(weapon1)
        backpack1.store(Weapon("weapon2347s", "broken dagger"))
        backpack1.store(gold_key)
        backpack1.store(silver_key)
        print(f"slots filled: {backpack1.used}")

        print(f"dropping Item: {gold_key.name}.")
        backpack1.drop(gold_key)
        print(f"slots filled: {backpack1.used}")

        print("\n\n### TESTING __str__ OVERRIDE:")
        print(backpack1)

        print("\n### TESTING Item repr() and hash() OVERRIDES:\n")
        print(f"weapon1:\t__repr__ = {repr(weapon1)} __hash__ = {hash(weapon1)}")
        weapon2 = eval(repr(weapon1))
        print(f"weapon2:\t__repr__ = {weapon2.__repr__()} __hash__ = {weapon2.__hash__()}")
        print("\nweapon1 == weapon2:", weapon1 == weapon2)

        print("\n\n### TESTING Inventory repr() and hash() OVERRIDES:\n")
        print(repr(backpack1))
        backpack2 = eval(repr(backpack1))
        print(f"backpack1:\t__hash__ = {hash(backpack1)}")
        print(f"backpack2:\t__hash__ = {hash(backpack2)}")
        print("\nbackpack1 == backpack2:", backpack1 == backpack2)

        print(f"\n{backpack2.contents}")
        print(f"\n{backpack2.contents('WEApOn')}")
        print(f"\n{backpack2.contents('item', 'kEY')}")

        print(f"{backpack2._currency}")

        print(weapon1)
        weapon1.pane_width = 10
        print(weapon1)
        weapon1.pane_width = 42
        print(weapon1)

    main()
