import unittest
from board import Board, EntityType
from game import Game
from direction import Direction


class UnitTests(unittest.TestCase):
    def test_GameIsWonWhenPenguinInWater(self):
        board = Board(width=1, height=1)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.WATER, 0, 0)
        game = Game(board)
        self.assertTrue(game.is_won())

    def test_GameIsNotWonWhenPenguinNotInWater(self):
        board = Board(width=2, height=1)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.WATER, 1, 0)
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
        board = Board(width=3, height=2)
        board.place_entity(EntityType.BEAR1, 0, 0)
        self.assertTrue(board.there_is_a_blocker_entity_in(0, 0))
        self.assertFalse(board.there_is_a_blocker_entity_in(0, 1))
        self.assertFalse(board.there_is_a_blocker_entity_in(1, 0))

    def test_PenguinMoveIsIllegalIfThereIsNoBearInTheWay(self):
        board = Board(width=3, height=1)
        board.place_entity(EntityType.PENGUIN, 2, 0)
        game = Game(board)
        self.assertEqual(False, game.entity_move_is_legal(EntityType.PENGUIN, Direction.LEFT))  # assertFalse also asserts not returning value at all

    def test_BearMoveIsIllegalIfThereIsAPenguinNeighbour(self):
        board = Board(width=3, height=1)
        board.place_entity(EntityType.PENGUIN, 1, 0)
        board.place_entity(EntityType.BEAR1, 0, 0)
        board.place_entity(EntityType.BEAR2, 2, 0)
        game = Game(board)
        self.assertEqual(False, game.entity_move_is_legal(EntityType.BEAR1, Direction.RIGHT))

    def test_PenguinMoveIsLegalIfThereIsABearInTheWay(self):
        board = Board(width=5, height=5)
        board.place_entity(EntityType.PENGUIN, 2, 2)
        board.place_entity(EntityType.BEAR1, 2, 0)
        board.place_entity(EntityType.BEAR2, 0, 2)
        board.place_entity(EntityType.BEAR3, 2, 4)
        board.place_entity(EntityType.BEAR4, 4, 2)
        game = Game(board)
        self.assertTrue(game.entity_move_is_legal(EntityType.PENGUIN, Direction.LEFT))
        self.assertTrue(game.entity_move_is_legal(EntityType.PENGUIN, Direction.RIGHT))
        self.assertTrue(game.entity_move_is_legal(EntityType.PENGUIN, Direction.UP))
        self.assertTrue(game.entity_move_is_legal(EntityType.PENGUIN, Direction.DOWN))

    def test_GetPossibleMovesForEntityIsEmptyIfNoneAvailable(self):
        board = Board(width=2, height=2)
        board.place_entity(EntityType.PENGUIN, 1, 0)
        board.place_entity(EntityType.BEAR1, 0, 1)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.PENGUIN)
        self.assertEqual(0, len(possible_moves))

    def test_GetPossibleMovesForEntityIsEmptyIfNeighbourIsBlocker(self):
        board = Board(width=3, height=1)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.BEAR1, 1, 0)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.PENGUIN)
        self.assertEqual(0, len(possible_moves))

    def test_GetPossibleMovesForEntityReturnsOneIfOnlyOneAvailable(self):
        board = Board(width=3, height=1)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.BEAR1, 2, 0)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.PENGUIN)
        self.assertEqual(1, len(possible_moves))
        self.assertEqual(Direction.RIGHT, possible_moves[0].direction)

    def test_GetPossibleMovesForPenguinReturnsAllIfMultipleAvailable(self):
        board = Board(width=3, height=3)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.BEAR1, 2, 0)
        board.place_entity(EntityType.BEAR2, 0, 2)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.PENGUIN)
        self.assertEqual(2, len(possible_moves))
        self.assertTrue(Direction.RIGHT in [m.direction for m in possible_moves])
        self.assertTrue(Direction.UP in [m.direction for m in possible_moves])

    def test_GetPossibleMovesForBearReturnsAllIfMultipleAvailable(self):
        board = Board(width=3, height=3)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.BEAR1, 2, 0)
        board.place_entity(EntityType.BEAR2, 0, 2)
        board.place_entity(EntityType.BEAR3, 2, 2)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.BEAR3)
        self.assertEqual(2, len(possible_moves))
        self.assertTrue(Direction.LEFT in [m.direction for m in possible_moves])
        self.assertTrue(Direction.DOWN in [m.direction for m in possible_moves])

    def test_MoveEntitySingleStep(self):
        board = Board(width=3, height=1)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.BEAR1, 2, 0)
        board.apply_move(EntityType.PENGUIN, Direction.RIGHT)
        loc = board.get_entity_location(EntityType.PENGUIN)
        self.assertEqual(1, loc.x)
        self.assertEqual(0, loc.y)

    def test_MoveEntityMultipleSteps(self):
        board = Board(width=4, height=1)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.BEAR1, 3, 0)
        board.apply_move(EntityType.PENGUIN, Direction.RIGHT)
        loc = board.get_entity_location(EntityType.PENGUIN)
        self.assertEqual(2, loc.x)
        self.assertEqual(0, loc.y)


class IntegrationTests(unittest.TestCase):
    def test_PossibleMovesListIsEmptyIfThereAreNoPossibleMoves(self):
        board = Board(width=2, height=2)
        board.place_entity(EntityType.PENGUIN, 1, 0)
        board.place_entity(EntityType.BEAR1, 0, 1)
        game = Game(board)
        possible_moves = game.get_all_possible_moves()
        self.assertEqual(0, len(possible_moves))

    def test_ReturnBothPossibleMovesIfThereIsAGapBetweenPenguinAndBear(self):
        board = Board(width=3, height=1)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.BEAR1, 2, 0)
        game = Game(board)
        possible_moves = game.get_all_possible_moves()
        self.assertEqual(2, len(possible_moves))
        expected_moves = 0
        for m in possible_moves:
            if m.entity_type == EntityType.PENGUIN:
                self.assertEqual(m.direction, Direction.RIGHT)
                expected_moves += 1
            if m.entity_type == EntityType.BEAR1:
                self.assertEqual(m.direction, Direction.LEFT)
                expected_moves += 1
        self.assertEqual(2, expected_moves)


class EndToEndTests(unittest.TestCase):
    def test_GetWinningMoveIfThereIsJustOneOption(self):
        board = Board(width=3, height=1)
        board.place_entity(EntityType.PENGUIN, 2, 0)
        board.place_entity(EntityType.BEAR1, 0, 0)
        board.place_entity(EntityType.WATER, 1, 0)
        game = Game(board)
        solution = game.solve()
        self.assertEqual(1, len(solution))
        self.assertEqual(Direction.LEFT, solution[0].direction)
        self.assertEqual(EntityType.PENGUIN, solution[0].entity_type)

    def test_GetWinningMoveIfThereAreTwoOption(self):
        board = Board(width=3, height=3)
        board.place_entity(EntityType.PENGUIN, 0, 0)
        board.place_entity(EntityType.WATER, 1, 0)
        board.place_entity(EntityType.BEAR1, 2, 0)
        board.place_entity(EntityType.BEAR2, 0, 2)
        game = Game(board)
        solution = game.solve()
        self.assertEqual(1, len(solution))
        self.assertEqual(Direction.RIGHT, solution[0].direction)
        self.assertEqual(EntityType.PENGUIN, solution[0].entity_type)

    def test_FindSolutionWhenTwoMovesAreNeeded(self):
        board = Board(width=3, height=3)
        board.place_entity(EntityType.PENGUIN, 0, 1)
        board.place_entity(EntityType.WATER, 1, 1)
        board.place_entity(EntityType.BEAR1, 2, 0)
        board.place_entity(EntityType.BEAR2, 2, 2)
        game = Game(board)
        solution = game.solve()
        self.assertEqual(2, len(solution))
        assert solution[0].direction in [Direction.UP, Direction.DOWN]
        assert solution[0].entity_type in [EntityType.BEAR1, EntityType.BEAR2]
        self.assertEqual(Direction.RIGHT, solution[1].direction)
        self.assertEqual(EntityType.PENGUIN, solution[1].entity_type)

    def test_FindSolutionWhenManyMovesAreNeeded(self):
        board = Board(5, 5)
        board.place_entity(EntityType.PENGUIN, 0, 2)
        board.place_entity(EntityType.WATER, 2, 2)
        board.place_entity(EntityType.BEAR1, 0, 0)
        board.place_entity(EntityType.BEAR2, 1, 2)
        board.place_entity(EntityType.BEAR3, 2, 0)
        board.place_entity(EntityType.BEAR4, 3, 1)
        board.place_entity(EntityType.BEAR5, 3, 3)
        game = Game(board)
        solution = game.solve()
        self.assertTrue(game.is_won())
