import unittest
from src.deckcollection import *


class DeckCollectionTests(unittest.TestCase):
    def test_checkEquivDecksEquiv_returnsTrue(self):
        self.assertTrue(DeckCollection([Deck({House.BROBNAR, House.DIS, House.LOGOS})]).equiv
                        (DeckCollection([Deck({House.UNTAMED, House.MARS, House.SHADOWS})])))

    def test_fromRunningScriptEquiv_returnsTrue(self):
        collections = (DeckCollection([Deck([House.LOGOS, House.SHADOWS, House.BROBNAR]),
                                       Deck([House.UNTAMED, House.SANCTUM, House.MARS]),
                                       Deck([House.LOGOS, House.DIS, House.BROBNAR])]),
                       DeckCollection([Deck([House.DIS, House.SHADOWS, House.BROBNAR]),
                                       Deck([House.UNTAMED, House.SANCTUM, House.MARS]),
                                       Deck([House.LOGOS, House.DIS, House.BROBNAR])]))
        self.assertTrue(collections[0].equiv(collections[1]))

    def test_checkDiffDecksEqual_returnsFalse(self):
        self.assertNotEqual(DeckCollection([
            Deck({House.BROBNAR, House.DIS, House.LOGOS}),
            Deck({House.BROBNAR, House.DIS, House.MARS})]
        ),
            DeckCollection([
                Deck({House.UNTAMED, House.DIS, House.LOGOS}),
                Deck({House.UNTAMED, House.SHADOWS, House.MARS})]
            ))


if __name__ == '__main__':
    unittest.main()
