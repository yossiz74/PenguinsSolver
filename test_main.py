import unittest
from board import Board
from game import Game, Move


class UnitTests(unittest.TestCase):
    def test_GameIsWonWhenPenguinInWater(self):
        board = Board(width=1, height=1)
        board.place_penguin(0, 0)
        board.place_water(0, 0)
        game = Game(board)
        self.assertTrue(game.is_won())

    def test_GameIsNotWonWhenPenguinNotInWater(self):
        board = Board(width=2, height=1)
        board.place_penguin(0, 0)
        board.place_water(1, 0)
        game = Game(board)
        self.assertFalse(game.is_won())

    def test_PointIsInsideTheBoard(self):
        board = Board(width=2, height=3)
        self.assertTrue(board.point_is_inside_the_board(0, 0))
        self.assertTrue(board.point_is_inside_the_board(0, 1))
        self.assertTrue(board.point_is_inside_the_board(0, 2))
        self.assertTrue(board.point_is_inside_the_board(1, 0))
        self.assertTrue(board.point_is_inside_the_board(1, 1))
        self.assertTrue(board.point_is_inside_the_board(1, 2))
        self.assertFalse(board.point_is_inside_the_board(-1, 0))
        self.assertFalse(board.point_is_inside_the_board(2, 0))
        self.assertFalse(board.point_is_inside_the_board(0, -1))
        self.assertFalse(board.point_is_inside_the_board(0, 3))

    def test_ThereIsABear(self):
        board = Board(width=3, height=1)
        board.place_bear(0, 0)
        self.assertTrue(board.there_is_a_bear_in(0, 0))
        self.assertFalse(board.there_is_a_bear_in(0, 1))
        self.assertFalse(board.there_is_a_bear_in(1, 0))


class IntegrationTests(unittest.TestCase):
    def test_PenguinMoveIsIllegalIfThereIsNoBearInTheWay(self):
        board = Board(width=3, height=1)
        board.place_penguin(2, 0)
        game = Game(board)
        self.assertEqual(False, game.penguin_move_is_legal(Move.LEFT))  # assertFalse also asserts not returning value at all

    def test_PenguinMoveIsLegalIfThereIsABearInTheWay(self):
        board = Board(width=3, height=1)
        board.place_penguin(2, 0)
        board.place_bear(0, 0)
        game = Game(board)
        self.assertTrue(game.penguin_move_is_legal(Move.LEFT))
