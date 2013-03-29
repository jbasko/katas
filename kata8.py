"""
    2013-03-28 evening
    Prime Factors Kata http://craftsmanship.sv.cmu.edu/exercises/prime-factors-kata

    >>> generate(1)
    []
    >>> generate(2)
    [2]
    >>> generate(3)
    [3]
    >>> generate(4)
    [2, 2]
    >>> generate(6)
    [2, 3]
    >>> generate(30)
    [2, 3, 5]
"""


def generate(m):
    factors = []
    i = 2
    while i <= m:
        while m % i == 0:
            factors.append(i)
            m = m / i
        i += 1
    return factors

