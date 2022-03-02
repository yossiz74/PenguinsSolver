import unittest
from board import Board
from game import Game


class TestClass(unittest.TestCase):
    def test_GameIsWonWhenPenguinInWater(self):
        board = Board(height=1, width=1)
        board.place_penguin(0, 0)
        board.place_water(0, 0)
        game = Game(board)
        self.assertTrue(game.is_won())
