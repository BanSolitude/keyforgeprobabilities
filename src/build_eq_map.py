from src.deckcollection import DeckCollection, Deck, House, NUM_DECKS
import json

TOTAL = 'total'


def find_equiv_in(decks, collections):
    for deck_collection in collections:
        if decks.equiv(deck_collection):
            return deck_collection

    return None


def main():
    equiv_map = {1: {TOTAL: NUM_DECKS, DeckCollection([Deck([House.BROBNAR, House.DIS, House.LOGOS])]): 35}}

    for prev in range(1, int(NUM_DECKS / 2) + 1):
        print(prev)
        cur = prev + 1
        equiv_map[cur] = {TOTAL: equiv_map[prev][TOTAL] * (NUM_DECKS - prev)}

        for collection in [c for c in equiv_map[prev] if c != TOTAL]:
            count = equiv_map[prev][collection]
            for deck in ~collection:
                temp = collection + deck

                # TODO Make first canonically?
                try:
                    equiv_map[cur][find_equiv_in(temp, equiv_map[cur])] += count
                except KeyError:
                    equiv_map[cur][temp] = count

    for key in equiv_map:
        for deck in equiv_map[key]:
            print(f"{deck}:{equiv_map[key][deck]}")

    with open('EqMap.json', 'w+') as map_file:
        json.dump(equiv_map, map_file)


if __name__ == '__main__':
    main()
