"""
Length of longest contiguous monotonous string

2018-01-23, 10mins including tests
"""
import pytest


def longest_length(input_str):
    max_length = 0
    increasing = []
    decreasing = []

    for c in input_str:
        if increasing and c > increasing[-1]:
            increasing.append(c)
        else:
            max_length = max(max_length, len(increasing))
            increasing = [c]

        if decreasing and c < decreasing[-1]:
            decreasing.append(c)
        else:
            max_length = max(max_length, len(decreasing))
            decreasing = [c]

    return max(max_length, len(increasing), len(decreasing))


@pytest.mark.parametrize('input_str,length', [
    ['', 0],
    ['a', 1],
    ['aa', 1],
    ['ab', 2],
    ['ba', 2],
    ['abb', 2],
    ['aab', 2],
    ['baa', 2],
    ['bba', 2],
    ['abba', 2],
    ['baab', 2],
    ['ababc', 3],
    ['abcab', 3],
    ['aababcabcdabc', 4],
])
def test_all(input_str, length):
    assert longest_length(input_str) == length
