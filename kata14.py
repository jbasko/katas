"""
    2013-04-01
    1) Frequency of characters in string
    2) Permutations of a given string

    >>> f = frequencies('code')
    >>> f['c'], f['o'], f['d'], f['e'], f['z']
    (1, 1, 1, 1, 0)

    >>> permutations('a')
    ['a']
    >>> permutations('ab')
    ['ab', 'ba']
    >>> permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
"""

from collections import Counter


def frequencies(s):
    return Counter(s)


def _perms(chars):
    assert isinstance(chars, set), type(chars)
    if len(chars) == 1:
        return [chars.pop()]
    p = []
    for c in chars:
        tails = _perms(chars.difference({c}))
        for tail in tails:
            p.append(c + tail)
    return p

def permutations(s):
    chars = set(s)
    return sorted(_perms(chars))