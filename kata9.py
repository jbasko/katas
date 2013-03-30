"""
    2013-03-29 Tennis Score Calculator (One infinite set only)

    >>> sim = Sim()
    >>> sim.game(player=0)
    >>> sim.score()
    '0-0 15-0'
    >>> sim.game(player=1)
    >>> sim.score()
    '0-0 15-15'
    >>> sim.game(player=1)
    >>> sim.score()
    '0-0 15-30'
    >>> sim.game(player=1)
    >>> sim.score()
    '0-0 15-40'
    >>> sim.game(player=1)
    >>> sim.score()
    '0-1'
    >>> sim.game(player=1)
    >>> sim.game(player=1)
    >>> sim.game(player=1)
    >>> sim.score()
    '0-1 0-40'
    >>> sim.game(player=0)
    >>> sim.game(player=0)
    >>> sim.score()
    '0-1 30-40'
    >>> sim.game(player=0)
    >>> sim.score()
    '0-1 D'
    >>> sim.game(player=0)
    >>> sim.score()
    '0-1 A-40'
    >>> sim.game(player=1)
    >>> sim.score()
    '0-1 D'
    >>> sim.game(player=1)
    >>> sim.score()
    '0-1 40-A'
    >>> sim.game(player=1)
    >>> sim.score()
    '0-2'
"""


class GameScore(object):

        def __init__(self):
            self.points = [0, 0]
            self.advantage = None

        def __getitem__(self, item):
            return self.points[item]

        def __setitem__(self, key, value):
            self.points[key] = value

        def has_advantage(self, player):
            return self.advantage == player


class Sim(object):

    def __init__(self):
        self._games = []

    def game(self, player):
        self._games.append(player)

    def score(self):

        match_score = [0, 0]

        game_score = GameScore()

        def is_deuce():
            return game_score[0] == 40 and game_score[1] == 40 and game_score.advantage is None

        def win_game(player):
            match_score[player] += 1
            game_score[0] = 0
            game_score[1] = 0
            game_score.advantage = None

        def current_game_score():
            if is_deuce():
                return 'D'
            elif game_score.has_advantage(0):
                return 'A-40'
            elif game_score.has_advantage(1):
                return '40-A'
            else:
                return '{}-{}'.format(game_score[0], game_score[1])

        for g in self._games:
            if game_score[g] <= 15:
                game_score[g] += 15
            elif game_score[g] == 30:
                game_score[g] = 40
            elif is_deuce():
                game_score.advantage = g
            elif game_score.has_advantage(g):
                win_game(g)
            elif game_score.has_advantage(abs(g-1)):
                game_score.advantage = None
            else:
                # g has 40 points and wins
                win_game(g)

        match_score_str = '-'.join(str(p) for p in match_score)
        game_score_str = current_game_score()

        score_str = match_score_str
        if game_score_str != '0-0':
            score_str += ' ' + game_score_str
        return score_str