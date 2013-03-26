"""
    http://thecleancoder.blogspot.co.uk/2010/10/craftsman-62-dark-path.html
    2013-03-26 evening
"""
from unittest.case import TestCase


def append_line_to_lines(line, lines):
    if len(line) > 0:
            lines.append(line)


def word_appended_to_line(word, line, lines, width):
    if len(word) > width:
        assert line == ''
        lines.append(word[:width])
        return word_appended_to_line(word[width:], line, lines, width)

    if line:
        line += ' ' + word
    else:
        line += word
    return line


def wrap_paragraph(s, width):
    words = s.split(" ")
    lines = []
    line = ''

    for word in words:
        if len(line) + 1 + len(word) > width:
            append_line_to_lines(line, lines)
            line = ''
            line = word_appended_to_line(word, line, lines, width)
        else:
            line = word_appended_to_line(word, line, lines, width)

    if line:
        append_line_to_lines(line, lines)

    return "\n".join(lines)


def wrap(s, width):
    if len(s) <= width:
        return s

    raw_paragraphs = s.split("\n")
    wrapped_paragraphs = []
    for paragraph in raw_paragraphs:
        wrapped_paragraphs.append(wrap_paragraph(paragraph, width))
    return "\n".join(wrapped_paragraphs)


class WrapTest(TestCase):

    def test_wrap(self):
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