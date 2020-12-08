"""
2020-12-08 evening
Write a function named wrap that takes two arguments: a string, and a column number.
The function returns the string, but with line breaks inserted at just the right places to make sure that
no line is longer than the column number.
You try to break lines at word boundaries.

This is more correct than the 2018 version despite being uglier.
Works even with line-breaks in the original text.
Doesn't preserve redundant whitespace.
"""

import pytest


def wrap(text: str, columns: int) -> str:
    line = []
    line_len = 0

    def get_word_lines(word: str):
        nonlocal line_len
        word_len = len(word)
        new_line_len = word_len if line_len == 0 else line_len + 1 + word_len

        if new_line_len <= columns:
            # The word fits on this line, let's just add
            line.append(word)
            if new_line_len == columns or new_line_len == columns - 1:
                yield line
                line[:] = []
                line_len = 0
            else:
                line_len = new_line_len

        elif word_len <= columns:
            # The word would fit on a separate line, but not when added to this line, don't break!
            yield line
            line[:] = []
            line_len = 0
            yield from get_word_lines(word)

        else:
            # Let's break up the word
            part_len = columns if line_len == 0 else columns - (line_len + 1)
            line.append(word[:part_len])
            yield line
            line[:] = []
            line_len = 0
            yield from get_word_lines(word[part_len:])

    def get_paragraph_lines(words):
        nonlocal line_len

        for word in words:
            yield from get_word_lines(word)

        if line:
            yield line
            line[:] = []
            line_len = 0

    def get_all_lines():
        for paragraph in text.splitlines():
            yield from get_paragraph_lines(paragraph.split())

    return "\n".join(" ".join(ln) for ln in get_all_lines())


@pytest.mark.parametrize('text,columns,expected', [
    ['a', 1, 'a'],
    ['ab', 1, 'a\nb'],
    ['aab', 2, 'aa\nb'],
    ['aabb', 2, 'aa\nbb'],
    ['aabbc', 2, 'aa\nbb\nc'],
    ['a b', 1, 'a\nb'],
    ['a b c', 1, 'a\nb\nc'],
    ['aa bb cc', 2, 'aa\nbb\ncc'],
    ['a a', 3, 'a a'],
    ['a a', 4, 'a a'],
    ['a\na', 3, 'a\na'],  # Line-break!
    ['a\na', 4, 'a\na'],  # Line-break!
    ['a a b b', 3, 'a a\nb b'],
    ['a a b b', 4, 'a a\nb b'],
    ['aaab bccc', 3, 'aaa\nb b\nccc'],
    ['aaaab bb ccccd', 4, 'aaaa\nb bb\ncccc\nd'],
    ['aaab ccc ddd eeef', 3, 'aaa\nb\nccc\nddd\neee\nf'],
    ['aa\nb ccc ddd eeef', 3, 'aa\nb\nccc\nddd\neee\nf'],  # Line-break!
])
def test_all(text, columns, expected):
    assert expected == wrap(text, columns)
