"""
    2013-03-28 morning
    The Bowling Game - http://codingdojo.org/cgi-bin/wiki.pl?KataBowling

    FAILED!
    Next time should construct a list of each roll's contribution to the total score.
    Each roll contributes 1) the number of pins knocked down in the roll, 2) bonuses depending on the next
    two rolls.

    rolls:  0   0       9   /       5   /       X       X       9   -       X       X       X       X       X       X
    basic:  0   0       9   1       5   5       10      10      9   0       10      10      10      10      0       0
    bonus:  0   0       0   5       0   10      19      9       0   0       20      20      20      20
    total:      0           15          20      29      19          9       30      30      30      30

    TOTAL:  15 + 20 + 29 + 19 + 9 + 30*4 = 212

"""
from unittest.case import TestCase


def score(rolls):

    STRIKE = 'X'
    SPARE = '/'

    rolls = rolls.replace(' ', '')

    def is_complete(frame):
        return len(frame) == 2 or frame[0] in ['x', 'X']

    def score_frame(frame):
        if frame[0] in ['x', 'X']:
            return STRIKE
        elif len(frame) == 2 and frame[1] == '/':
            return SPARE
        else:
            score = 0
            for x in frame:
                if x != '-':
                    score += int(x)
            return score

    def true_score(score):
        if score in [STRIKE, SPARE]:
            return 10
        else:
            return score

    frames = []
    frame = []
    for i in range(0, len(rolls)):
        if not frame:
            frame = [rolls[i]]
        else:
            frame.append(rolls[i])
        if is_complete(frame):
            frames.append(frame)
            frame = []

    frame_scores = []
    total_score = 0

    first_score = score_frame(frames[0])
    total_score += true_score(first_score)
    frame_scores.append(first_score)

    for i in range(1, len(frames)):
        previous_score = frame_scores[-1]
        current_score = score_frame(frames[i])
        total_score += true_score(current_score)

        if i <= 10:
            if previous_score == STRIKE:
                total_score += true_score(current_score)
                if i >= 2 and score_frame(frame_scores[-2]) == STRIKE:
                    total_score += true_score(current_score)
            elif previous_score == SPARE:
                total_score += score_frame([[frames[i][0]]])

        frame_scores.append(current_score)

    return total_score


class BowlingGameTest(TestCase):

    def test_one_roll(self):
        self.assertEqual(0, score('00'))
        self.assertEqual(0, score('0-'))
        self.assertEqual(9, score('-9'))
        self.assertEqual(10, score('2/'))
        self.assertEqual(10, score('X'))

    def test_two_rolls(self):
        self.assertEqual(5, score('23'))

        self.assertEqual(9, score('-9'))

        self.assertEqual(10, score('2/'))

    def test_strikes(self):
        self.assertEqual(12, score('02X'))
        self.assertEqual(14, score('X2-'))

    def test_spares(self):
        self.assertEqual(12, score('2/1-'))
        self.assertEqual(14, score('2/12'))

    def test_my_big_example(self):
        self.assertEqual(212, score('00 9/ 5/ X X 9- X X X X X X'))

    def test_consecutive_strikes(self):
        self.assertEqual(30, score('XX'))
        self.assertEqual(60, score('XXX'))
        self.assertEqual(30, score('0-0-0-0-0-0-0-0-0-XXX'))

    def test_reference_examples(self):
        self.assertEqual(300, score('XXXXXXXXXXXX'))
        self.assertEqual(90, score('9-9-9-9-9-9-9-9-9-9-'))
        self.assertEqual(150, score('5/5/5/5/5/5/5/5/5/5/5'))