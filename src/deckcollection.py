from enum import Enum


class House(Enum):
    BROBNAR = "Brobnar"
    DIS = "Dis"
    LOGOS = "Logos"
    MARS = "Mars"
    SANCTUM = "Sanctum"
    SHADOWS = "Shadows"
    UNTAMED = "Untamed"


def create_mappings(from_a, to_a):
    perm_to = create_permutations(to_a)
    mappings = []
    for p in perm_to:
        house_map = {}
        for i in range(len(from_a)):
            house_map[from_a[i]] = p[i]

        mappings.append(house_map)

    return mappings


def create_permutations(a):
    if len(a) <= 1:
        return [a]

    permutations = []
    for i in range(len(a)):
        sub_permutations = create_permutations(a[0:i] + a[i + 1:])
        permutations += list(map(lambda x: x + [a[i]], sub_permutations))

    return permutations


def merge_mappings(perm_map_list):
    if len(perm_map_list) == 1:
        return perm_map_list[0]

    ret_maps = []
    for merged_map in merge_mappings(perm_map_list[1:]):
        for morph in perm_map_list[0]:
            ret_maps.append({**morph, **merged_map})

    return ret_maps


# Hashable, do not change houses
class Deck:
    def __init__(self, house_set):
        if len(house_set) == 3:
            # TODO mark houses as private so they don't accidentally get set?
            self.houses = frozenset(house_set)
        else:
            raise ValueError("Deck must contain 3 houses")

    def __eq__(self, other):
        return self.houses == other.houses

    def __iter__(self):
        return iter(self.houses)

    def __hash__(self):
        return hash((self.houses, type(self)))

    def __str__(self):
        return "[" + ", ".join(map(lambda x: x.value, self.houses)) + "]"

    def apply_morphism(self, morph):
        after_map_houses = set()
        for house in self:
            after_map_houses.add(morph[house])

        return Deck(after_map_houses)


# Hashable, do not change decks
class DeckCollection:
    def __add__(self, deck):
        if deck in self.decks:
            return self

        return DeckCollection(list(self.decks) + [deck])

    def __eq__(self, other):
        try:
            for deck in other.decks:
                if deck not in self.decks:
                    return False

            return True

        except AttributeError:
            return False

    def __hash__(self):
        return hash((self.decks, type(self)))

    def __iter__(self):
        return iter(self.decks)

    def __init__(self, deck_list):
        self.decks = frozenset(deck_list)
        self._depth_map = None

    def __invert__(self):
        inverted_decks = [d for d in DeckCollection.full_collection() if d not in self.decks]
        return DeckCollection(inverted_decks)

    def __str__(self):
        return "[" + ", ".join(map(lambda x: str(x), self.decks)) + "]"

    @property
    def depth_map(self):
        if self._depth_map is None:
            self._depth_map = self._calculate_depth_map()

        return self._depth_map

    def _calculate_depth_map(self):
        house_map = {}
        for house in House:
            house_map[house] = 0
        for deck in self.decks:
            for house in deck:
                house_map[house] += 1

        depth_map = {}
        for house in house_map:
            depth = house_map[house]
            try:
                depth_map[depth].append(house)
            except KeyError:
                depth_map[depth] = [house]

        return depth_map

    def apply_morphism(self, morph):
        after_map_decks = set()
        for deck in self.decks:
            after_map_decks.add(deck.apply_morphism(morph))

        return DeckCollection(after_map_decks)

    def create_mappings_depth(self, to_depth):
        mappings_for_depth = []
        for depth in self.depth_map:
            mappings_for_depth.append(create_mappings(self.depth_map[depth], to_depth[depth]))

        return merge_mappings(mappings_for_depth)

    _all_decks = None

    def equiv(self, other):
        # this is where the hard work is
        try:
            if len(self.decks) != len(other.decks):
                return False
        except AttributeError:
            return False

        for depth in self.depth_map:
            if ((depth not in other.depth_map) or
                    len(self.depth_map[depth]) != len(other.depth_map[depth])):
                return False

        mappings = self.create_mappings_depth(other.depth_map)
        for morph in mappings:
            if self.apply_morphism(morph) != other:
                continue

            return True

        return False

    @staticmethod
    def full_collection():
        if DeckCollection._all_decks is not None:
            return DeckCollection._all_decks

        DeckCollection._all_decks = DeckCollection._generate_all_decks()
        return DeckCollection._all_decks

    @staticmethod
    def _generate_all_decks():
        return [Deck({x, y, z}) for x in House for y in House for z in House if x.value < y.value < z.value]
