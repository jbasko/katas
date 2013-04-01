"""
    2013-04-01 Potter Kata
    http://craftsmanship.sv.cmu.edu/katas/potter-kata

    The last test is failing as the logic to calculate the cheapest option is not implemented.

    >>> price([1, 0, 0, 0, 0])
    8.0
    >>> price([2, 0, 0, 0, 0])
    16.0
    >>> price([1, 1, 0, 0, 0])
    15.2
    >>> price([1, 1, 1, 1, 1])
    30.0
    >>> price([1, 1, 1, 1, 2])
    38.0
    >>> price([1, 1, 2, 1, 2])
    45.2
    >>> price([2, 2, 2, 1, 1])
    51.2

"""

def price(books):

    sets = []
    for i in range(len(books)):
        x = books[i]
        for s in sets:
            if x == 0:
                break
            if i not in s:
                s.add(i)
                x -= 1
        for j in range(x, 0, -1):
            sets.append({i})

    factor = [0, 1, 0.95, 0.9, 0.8, 0.75]
    total = 0.0
    for s in sets:
        total += factor[len(s)] * len(s) * 8.0

    return total

factor = [0, 1, 0.95, 0.9, 0.8, 0.75]
"""
1+1 = 2
1+2 = 3
1+3 = 4
1+4 = 5
1+5 = 6
2+2 = 4
2+3 = 5
2+4 = 6
2+5 = 7
3+3 = 6
3+4 = 7
3+5 = 8
4+4 = 8
4+5 = 9
"""

best = {}
for i in range(11):
    best[i] = {}

for i in range(1, len(factor)):
    best[i][str(i)] = factor[i]
    for j in range(i, len(factor)):
        k = i + j
        x = (factor[i] * i + factor[j] * j) / (i + j)
        best[k]['{},{}'.format(i, j)] = x

from pprint import pprint
pprint(best)