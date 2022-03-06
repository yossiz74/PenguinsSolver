import unittest

from Penguins.board import Board
from Penguins.entity import EntityClass
from Penguins.direction import Direction
from Penguins.game import Game


class EndToEndTests(unittest.TestCase):
    def test_GetWinningMoveIfThereIsJustOneOption(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 0, 0)
        board.add_new_entity(EntityClass.WATER, 1, 0)
        game = Game(board)
        solution = game.solve()
        self.assertEqual(1, len(solution))
        self.assertEqual(Direction.LEFT, solution[0].direction)
        self.assertEqual(p1, solution[0].entity)

    def test_GetWinningMoveIfThereAreTwoOption(self):
        board = Board(columns=3, rows=3)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.WATER, 1, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 0, 2)
        game = Game(board)
        solution = game.solve()
        self.assertEqual(1, len(solution))
        self.assertEqual(Direction.RIGHT, solution[0].direction)
        self.assertEqual(p1, solution[0].entity)

    def test_FindSolutionWhenTwoMovesAreNeeded(self):
        board = Board(columns=3, rows=3)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 1)
        board.add_new_entity(EntityClass.WATER, 1, 1)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 2)
        game = Game(board)
        solution = game.solve()
        # There are two symmetric solutions here, either move B1 up or B2 down, and then move P1 right
        self.assertEqual(2, len(solution))
        assert solution[0].direction in [Direction.UP, Direction.DOWN]
        self.assertEqual(EntityClass.BEAR, solution[0].entity.entity_class)
        self.assertEqual(Direction.RIGHT, solution[1].direction)
        self.assertEqual(p1, solution[1].entity)

    def test_FindSolutionWhenManyMovesAreNeeded(self):
        board = Board(5, 5)
        board.add_new_entity(EntityClass.PENGUIN, 0, 2)
        board.add_new_entity(EntityClass.WATER, 2, 2)
        board.add_new_entity(EntityClass.BEAR, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 1, 2)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 3, 1)
        board.add_new_entity(EntityClass.BEAR, 3, 3)
        game = Game(board)
        game.solve()
        self.assertTrue(game.is_won())

    def test_FindSolutionWithMultiplePenguins(self):
        # takes long time to run
        board = Board(5, 5)
        board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.PENGUIN, 0, 2)
        board.add_new_entity(EntityClass.WATER, 2, 2)
        board.add_new_entity(EntityClass.BEAR, 0, 1)
        board.add_new_entity(EntityClass.BEAR, 0, 3)
        board.add_new_entity(EntityClass.BEAR, 0, 4)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 3, 3)
        game = Game(board)
        game.solve()
        self.assertTrue(game.is_won())

    def test_FindSolutionWithMultipleWaters(self):
        board = Board(5, 5)
        board.add_new_entity(EntityClass.WATER, 2, 1)
        board.add_new_entity(EntityClass.WATER, 3, 1)
        board.add_new_entity(EntityClass.PENGUIN, 1, 0)
        board.add_new_entity(EntityClass.BEAR, 0, 3)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 4)
        board.add_new_entity(EntityClass.BEAR, 3, 0)
        board.add_new_entity(EntityClass.BEAR, 4, 3)
        game = Game(board)
        game.solve()
        self.assertTrue(game.is_won())
