import unittest
import random
from engine import Game, SHAPES


class Rules(unittest.TestCase):
    def test_first_bag(self):
        g = Game(rng=random.Random(7))
        pieces = []
        for _ in range(7):
            pieces.append(g.kind)
            g.spawn()
        self.assertEqual(set(pieces), set(SHAPES))

    def test_four_lines_and_challenge_win(self):
        g = Game(True)
        g.lines = 21
        g.board[-4:] = [[None]+['X']*9 for _ in range(4)]
        g.shape, g.x, g.y = ('#',)*4, 0, 16
        g.lock()
        self.assertEqual((g.lines, g.score, g.state), (25, 3600, 'course clear'))
        self.assertFalse(any(any(row) for row in g.board))

    def test_landing_and_top_out(self):
        g = Game()
        g.drop()
        self.assertEqual(sum(bool(c) for row in g.board for c in row), 4)
        g.board[:4] = [['X']*10 for _ in range(4)]
        g.spawn()
        self.assertEqual(g.state, 'game over')
