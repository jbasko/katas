"""
    2013-04-02 Greed Kata
    http://nimblepros.com/media/36619/greed%20kata.pdf
"""
from Queue import Queue
from unittest.case import TestCase


class Bonus(object):

    def __init__(self, score=0, rolls=None):
        self.score = score
        self.rolls = rolls or []


bonuses = [
    Bonus(100, [1]),
    Bonus(50, [5]),
    Bonus(1000, [1, 1, 1]),
    Bonus(200, [2, 2, 2]),
    Bonus(300, [3, 3, 3]),
    Bonus(400, [4, 4, 4]),
    Bonus(500, [5, 5, 5]),
    Bonus(600, [6, 6, 6]),
]


class Leaf(object):

    def __init__(self, score=0, rolls=None):
        self.score = score
        self.rolls = rolls or []

    def get_bonus_leaf(self, bonus):
        rolls = list(self.rolls)
        for i in range(len(bonus.rolls)):
            try:
                k = rolls.index(bonus.rolls[i])
                del rolls[k]
            except ValueError:
                return None
        return Leaf(score=self.score + bonus.score, rolls=rolls)


def score(rolls):

    root = Leaf(rolls=rolls)

    fringe = Queue()
    fringe.put(root)
    best_leaf = None

    while fringe.qsize() > 0:
        current = fringe.get()
        if best_leaf is None or best_leaf.score < current.score:
            best_leaf = current
        for b in bonuses:
            leaf = current.get_bonus_leaf(b)
            if leaf:
                fringe.put(leaf)

    return best_leaf.score if best_leaf else 0


class GreedTest(TestCase):

    def test_score(self):
        self.assertEqual(1150, score([1, 1, 1, 5, 1]))
        self.assertEqual(0, score([2, 3, 4, 6, 2]))
        self.assertEqual(350, score([3, 4, 5, 3, 3]))
        self.assertEqual(250, score([1, 5, 1, 2, 4]))
        self.assertEqual(600, score([5, 5, 5, 5, 5]))