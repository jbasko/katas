"""
    2013-03-31 Making Change
    http://craftsmanship.sv.cmu.edu/katas/making-change

    >>> exchange = Exchange(denominations=[1, 2, 5, 10, 20, 50, 100, 200])
    >>> exchange.change(1)
    {'1': 1}
    >>> exchange.change(2)
    {'2': 1}
    >>> exchange.change(5)
    {'5': 1}
    >>> change = exchange.change(6)
    >>> change['5'], change['1']
    (1, 1)
    >>> change = exchange.change(9)
    >>> change['5'], change['2']
    (1, 2)
    >>> exchange.change(10)
    {'10': 1}
    >>> change = exchange.change(98)
    >>> change['50'], change['20'], change['5'], change['2'], change['1']
    (1, 2, 1, 1, 1)
    >>> exchange.change(0)
    {}
"""
import collections


class Exchange(object):
    def __init__(self, denominations):
        self._denominations = sorted(denominations)
        self._denominations.reverse()

    def change(self, value):
        coins = collections.defaultdict(int)
        for d in self._denominations:
            while value >= d:
                coins[str(d)] += 1
                value -= d
        return dict(coins)

