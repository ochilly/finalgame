"""Items and Inventory for 'holding'/tracking Items"""
from collections import defaultdict


class Item(object):

    """Base Class for all items"""

    def __init__(self, name, description, value=0):
        self.name = name
        self.description = description
        self.value = int(value)

    def __repr__(self):
        return '{}(\"{}\", \"{}\", {})'.format(
            self.__class__.__name__,
            self.name,
            self.description,
            self.value
        )

    def __str__(self):
        return '\n {}\n{}\n"{}"\nValue:\t{}\n'.format(
            self.name,
            '=' * (len(self.name) + 2),
            self.description,
            self.value
        )

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        else:
            return False


class Inventory(object):

    """manages Items as a defaultdict"""

    def __init__(self, space_total=5, *initial_items):
        # TODO: what if user tries Inventory(Item1,Item2)???
        self._contents = defaultdict(list)
        self.space_used = 0
        self.space_total = space_total
        self.space_free = self.space_total - self.space_used
        for item in initial_items:
            self.store(item)

    def __repr__(self):
        return '{}({}, {})'.format(
            self.__class__.__name__,
            self.space_total,
            ''.join([repr(item) + ', ' for item in self.contents()]).rstrip(', ')
        )

    def __str__(self):
        return ''.join([str(item) for item in self.contents()])

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return hash(self) == hash(other)
        else:
            return False

    def __len__(self):
        return self.space_used

    def contents(self):
        """returns all items as a single list"""
        # inv_contents = []
        # for item_list in iter(self._contents.values()):
        #     for item in item_list:
        #         inv_contents.append(item)
        # return inv_contents
        return [item
                for item_list in iter(self._contents.values())
                for item in item_list]      # noice!

    def is_full(self):
        return self.space_used >= self.space_total

    def expand(self, amount_to_expand=1):
        """icreases the total space an Inventory can hold"""
        self.space_total += amount_to_expand
        self.space_free += amount_to_expand

    def shrink(self, amount_to_shrink=1):
        """reduces the total space an Inventory can hold"""
        # TODO: what if they now have too many items?
        self.space_total -= amount_to_shrink
        self.space_free -= amount_to_shrink

    def store(self, *items):
        """accepts Item objects to Inventory"""
        # TODO: Better error handling for full inventory
        for item in items:
            if not self.is_full():
                self._contents[type(item)].append(item)
                self.space_used += 1
                self.space_free -= 1
            else:
                print(f"Inventory full. {item.name} not stored.")

    def drop(self, *items):
        """remove object from inventory"""
        for item in items:
            if item in self._contents[type(item)]:
                self._contents[type(item)].remove(item)
                self.space_used -= 1
                self.space_free += 1


class Weapon(Item):

    def __init__(self, name, description, value=0, damage=0):
        self.damage = int(damage)
        super().__init__(name, description, value)

    def __repr__(self):
        return ''.join([super().__repr__().rstrip(')'), f", {self.damage})"])

    def __str__(self):
        return ''.join([super().__str__(), f"Damage:\t{self.damage}\n"])


class Gold(Item):
    # TODO: have all Gold items consolidate, that belongs in Inventory Class?

    def __init__(self, amount_of_coins=1):
        self.name = "Gold Coins"
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


if __name__ == '__main__':
    def main():
        weapon1 = Weapon("weapon01", "super shiny thang", 12_000, 100)
        gold_key = Item(name="Gold Key", description="A Lustrous Key to somewhere", value=0)
        silver_key = Item("Silver Key", "A Shiny Key", 0)
        gold1 = Gold()
        gold2 = Gold(23)

        backpack = Inventory(10)

        print("### TESTING Inventory.store() and drop()\n")
        print(f"slots filled: {backpack.space_used}")
        print(f"adding 2 items to backpack using *args")
        backpack.store(gold1, gold2)
        print(f"slots filled: {backpack.space_used}")
        print(f"adding 5 items to backpack.")
        backpack.store(Item("test_of_item", "this is a test", "9_000_000"))
        backpack.store(weapon1)
        backpack.store(Weapon("weapon2347s", "broken dagger"))
        backpack.store(gold_key)
        backpack.store(silver_key)
        print(f"slots filled: {backpack.space_used}")

        print(f"dropping Item: {gold_key.name}.")
        backpack.drop(gold_key)
        print(f"slots filled: {backpack.space_used}")

        print("\n\n### TESTING __str__ OVERRIDE:")
        print(backpack)

        print("\n### TESTING Item repr() and hash() OVERRIDES:\n")
        print(f"weapon1:\t__repr__ = {repr(weapon1)} __hash__ = {hash(weapon1)}")
        weapon_repr = eval(repr(weapon1))
        print(f"weapon_repr:\t__repr__ = {weapon_repr.__repr__()} __hash__ = {weapon_repr.__hash__()}")
        print("\nweapon1 == weapon_repr:", weapon1 == weapon_repr)

        print("\n\n### TESTING Inventory repr() and hash() OVERRIDES:\n")
        print(repr(backpack))
        backpack_repr = eval(repr(backpack))
        print(f"backpack:\t__hash__ = {hash(backpack)}")
        print(f"backpack_repr:\t__hash__ = {hash(backpack_repr)}")
        print("\nbackpack == backpack_repr:", backpack == backpack_repr)

    main()
