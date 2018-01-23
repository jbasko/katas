"""
    2013-04-04 Overlapping rectangles
    http://learn.hackerearth.com/question/327/test-cases-for-overlap-of-rectangles/
"""
from unittest.case import TestCase


class Rect(object):

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


def is_overlap(a, b):
    x_overlap = False
    y_overlap = False

    a_x = sorted([a.x1, a.x2])
    b_x = sorted([b.x1, b.x2])
    x = sorted([a_x, b_x])
    if x[0][1] > x[1][0]:
        x_overlap = True

    a_y = sorted([a.y1, a.y2])
    b_y = sorted([b.y1, b.y2])
    y = sorted([a_y, b_y])
    if y[0][1] > y[1][0]:
        y_overlap = True

    return x_overlap and y_overlap


class OverlappingRectanglesTest(TestCase):

    def test_no_overlap_on_any_dimension(self):
        a = Rect(0, 0, 10, 10)
        b = Rect(20, 20, 30, 30)
        self.assertFalse(is_overlap(a, b))

    def test_a_encloses_b_completely(self):
        a = Rect(0, 0, 100, 100)
        b = Rect(20, 20, 80, 80)
        self.assertTrue(is_overlap(a, b))

    def test_a_and_b_start_on_same_x_and_overlap(self):
        a = Rect(0, 0, 100, 100)
        b = Rect(0, 0, 100, 80)
        self.assertTrue(is_overlap(a, b))

    def test_a_and_b_start_on_same_x_and_do_not_overlap(self):
        a = Rect(0, 0, 100, 100)
        b = Rect(0, 0, -100, 100)
        self.assertFalse(is_overlap(a, b))

    def test_a_and_b_overlap_on_x_not_on_y(self):
        a = Rect(0, 10, 100, 100)
        b = Rect(10, -10, 90, -100)
        self.assertFalse(is_overlap(a, b))

    def test_a_and_b_overlap_on_x_enclosed_on_y(self):
        a = Rect(0, 0, 100, 100)
        b = Rect(-10, 20, 50, 80)
        self.assertTrue(is_overlap(a, b))

    def test_a_and_b_overlap_on_x_y_partially(self):
        a = Rect(0, 0, 100, 100)
        b = Rect(50, 50, 200, 200)
        self.assertTrue(is_overlap(a, b))