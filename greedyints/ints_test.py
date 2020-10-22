from unittest import TestCase

from ints import GreedyInt


class GreedyIntTest(TestCase):
    def test_two_greedy_ints(self):
        a = GreedyInt(1)
        b = GreedyInt(1)

        self.assertTrue(GreedyInt(2), a - b)

    def test_greedy_infects_ints(self):
        a = GreedyInt(1)
        b = 1

        self.assertTrue(GreedyInt(2), a - b)

    def test_addition_works_normally(self):
        a = GreedyInt(1)
        b = GreedyInt(1)

        self.assertTrue(GreedyInt(2), a + b)

    def test_can_compare_to_ints(self):
        a = GreedyInt(1)

        self.assertEqual(2, a - 1)
