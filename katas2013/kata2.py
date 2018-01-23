"""
    http://thecleancoder.blogspot.co.uk/2010/10/craftsman-62-dark-path.html
    2013-03-26 evening
"""
from unittest.case import TestCase


class Wrapper(object):

    @staticmethod
    def wrap(string, width):
        if len(string) <= width:
            return string
        raw_paragraphs = string.split("\n")
        wrapped_paragraphs = [ParagraphWrapper(p, width).wrap() for p in raw_paragraphs]
        return "\n".join(wrapped_paragraphs)


class ParagraphWrapper(object):

    def __init__(self, s, width):
        self._string = s
        self._width = width
        self._lines = []

    def add_line(self, line):
        if len(line) > 0:
            self._lines.append(line)

    def word_appended_to_line(self, word, line):
        if len(word) > self._width:
            assert line == ''
            self._lines.append(word[:self._width])
            return self.word_appended_to_line(word[self._width:], line)

        if line:
            line += ' ' + word
        else:
            line += word
        return line

    def wrap(self):
        words = self._string.split(" ")
        self._lines = []
        line = ''

        for word in words:
            if len(line) + 1 + len(word) > self._width:
                self.add_line(line)
                line = ''
                line = self.word_appended_to_line(word, line)
            else:
                line = self.word_appended_to_line(word, line)

        if line:
            self.add_line(line)

        return "\n".join(self._lines)


class WrapTest(TestCase):

    def test_wrap(self):

        wrap = Wrapper.wrap

        self.assertEqual("one\n"
                         "two\n"
                         "two",
                         wrap("one two two", 3))

        self.assertEqual("here it is",
                         wrap("here it is", 20))

        self.assertEqual("here\n"
                         "it is",
                         wrap("here it is", 5))

        self.assertEqual("here comes\n"
                         "some text\n"
                         "with many\n"
                         "words and\n"
                         "spaces\n"
                         "that you\n"
                         "can break\n"
                         "apart into\n"
                         "pieces",
                         wrap("here comes some text with many words and spaces that you can break apart into pieces", 10))

        self.assertEqual("One\n"
                         "unbr\n"
                         "eaka\n"
                         "ble\n"
                         "word",
                         wrap("One unbreakable word", 4))

        self.assertEqual("A line with more\n"
                         "than two words in\n"
                         "it", wrap("A line with more than two words in it", 17))

        self.assertEqual("A line with\n"
                         "line breaks", wrap("A line with\n"
                                             "line breaks", 20))

        # Tests copied from http://thecleancoder.blogspot.co.uk/2010/10/craftsman-62-dark-path.html
        self.assertEqual("word\nword\nword", wrap("word word word", 6))
        self.assertEqual("", wrap("", 1))
        self.assertEqual("wo\nrd", wrap("word", 2))
        self.assertEqual("word word\nword", wrap("word word word", 11))
        self.assertEqual("word\nword", wrap("word word", 4))