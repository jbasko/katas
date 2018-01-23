"""
You write a class called Wrapper, that has a single static function named wrap that takes two arguments,
a string, and a column number.
The function returns the string, but with line breaks inserted at just the right places to make sure that
no line is longer than the column number.
You try to break lines at word boundaries.

2018-01-23

First implementation: 19mins
Fix to match the old idea about breaking: 2mins
"""
import pytest


def wrap(text, columns):

    def get_lines():
        wrapped = None

        for line in text.splitlines():
            wrapped = []
            for word in line.split(' '):
                queue = [word]
                while queue:
                    token = queue.pop(0)
                    if len(token) > columns:
                        if wrapped:
                            yield ' '.join(wrapped)
                            wrapped = []
                        yield token[:columns]
                        queue.append(token[columns:])
                        continue
                    else:
                        len_wrapped = len(' '.join(wrapped))
                        if len_wrapped + len(token) <= columns:
                            wrapped.append(token)
                            continue
                        else:
                            yield ' '.join(wrapped)
                            wrapped = [token]
        if wrapped:
            yield ' '.join(wrapped)

    return '\n'.join(get_lines())


@pytest.mark.parametrize('text,columns,expected', [
    ['a', 1, 'a'],
    ['a a', 1, 'a\na'],
    ['a a a', 1, 'a\na\na'],
    ['aa aa aa', 2, 'aa\naa\naa'],
    ['a a', 3, 'a a'],
    ['a a', 4, 'a a'],
    ['a a', 4, 'a a'],
    ['a a a a', 3, 'a a\na a'],
    ['aaaa aaaa', 3, 'aaa\na\naaa\na'],
])
def test_all(text, columns, expected):
    assert expected == wrap(text, columns)
