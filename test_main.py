import unittest
from board import Board, EntityType, Point
from game import Game
from direction import Direction


class UnitTests(unittest.TestCase):
    def test_GameIsWonWhenThereAreNoPenguinsLeft(self):
        board = Board(width=1, height=1)
        board.add_new_entity(EntityType.WATER, 0, 0)
        game = Game(board)
        self.assertTrue(game.is_won())

    def test_WhenAPenguinIsOnWaterItIsRemovedFromTheGame(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 2, 0)
        board.add_new_entity(EntityType.WATER, 0, 0)
        game = Game(board)
        board.move_entity(EntityType.PENGUIN1, 0, 0)
        self.assertIsNone(board.get_entity_location(EntityType.PENGUIN1))

    def test_GameIsNotWonWhenThereArePenguinsOnBoard(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN2, 1, 0)
        board.add_new_entity(EntityType.WATER, 2, 0)
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
        board.add_new_entity(EntityType.BEAR1, 0, 0)
        self.assertTrue(board.there_is_a_blocker_entity_in(0, 0))
        self.assertFalse(board.there_is_a_blocker_entity_in(0, 1))
        self.assertFalse(board.there_is_a_blocker_entity_in(1, 0))

    def test_PenguinMoveIsIllegalIfThereIsNoBearInTheWay(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 2, 0)
        game = Game(board)
        self.assertEqual(False, game.entity_move_is_legal(EntityType.PENGUIN1, Direction.LEFT))  # assertFalse also asserts not returning value at all

    def test_BearMoveIsIllegalIfThereIsAPenguinNeighbour(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 1, 0)
        board.add_new_entity(EntityType.BEAR1, 0, 0)
        board.add_new_entity(EntityType.BEAR2, 2, 0)
        game = Game(board)
        self.assertEqual(False, game.entity_move_is_legal(EntityType.BEAR1, Direction.RIGHT))

    def test_PenguinMoveIsLegalIfThereIsABearInTheWay(self):
        board = Board(width=5, height=5)
        board.add_new_entity(EntityType.PENGUIN1, 2, 2)
        board.add_new_entity(EntityType.BEAR1, 2, 0)
        board.add_new_entity(EntityType.BEAR2, 0, 2)
        board.add_new_entity(EntityType.BEAR3, 2, 4)
        board.add_new_entity(EntityType.BEAR4, 4, 2)
        game = Game(board)
        self.assertTrue(game.entity_move_is_legal(EntityType.PENGUIN1, Direction.LEFT))
        self.assertTrue(game.entity_move_is_legal(EntityType.PENGUIN1, Direction.RIGHT))
        self.assertTrue(game.entity_move_is_legal(EntityType.PENGUIN1, Direction.UP))
        self.assertTrue(game.entity_move_is_legal(EntityType.PENGUIN1, Direction.DOWN))

    def test_GetPossibleMovesForEntityIsEmptyIfNoneAvailable(self):
        board = Board(width=2, height=2)
        board.add_new_entity(EntityType.PENGUIN1, 1, 0)
        board.add_new_entity(EntityType.BEAR1, 0, 1)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.PENGUIN1)
        self.assertEqual(0, len(possible_moves))

    def test_GetPossibleMovesForEntityIsEmptyIfNeighbourIsBlocker(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.BEAR1, 1, 0)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.PENGUIN1)
        self.assertEqual(0, len(possible_moves))

    def test_GetPossibleMovesForEntityReturnsOneIfOnlyOneAvailable(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.BEAR1, 2, 0)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.PENGUIN1)
        self.assertEqual(1, len(possible_moves))
        self.assertEqual(Direction.RIGHT, possible_moves[0].direction)

    def test_GetPossibleMovesForPenguinReturnsAllIfMultipleAvailable(self):
        board = Board(width=3, height=3)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.BEAR1, 2, 0)
        board.add_new_entity(EntityType.BEAR2, 0, 2)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.PENGUIN1)
        self.assertEqual(2, len(possible_moves))
        self.assertTrue(Direction.RIGHT in [m.direction for m in possible_moves])
        self.assertTrue(Direction.UP in [m.direction for m in possible_moves])

    def test_GetPossibleMovesForBearReturnsAllIfMultipleAvailable(self):
        board = Board(width=3, height=3)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.BEAR1, 2, 0)
        board.add_new_entity(EntityType.BEAR2, 0, 2)
        board.add_new_entity(EntityType.BEAR3, 2, 2)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(EntityType.BEAR3)
        self.assertEqual(2, len(possible_moves))
        self.assertTrue(Direction.LEFT in [m.direction for m in possible_moves])
        self.assertTrue(Direction.DOWN in [m.direction for m in possible_moves])

    def test_MoveEntitySingleStep(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.BEAR1, 2, 0)
        board.apply_move(EntityType.PENGUIN1, Direction.RIGHT)
        loc = board.get_entity_location(EntityType.PENGUIN1)
        self.assertEqual(Point(1, 0), loc)

    def test_MoveEntityMultipleSteps(self):
        board = Board(width=4, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.BEAR1, 3, 0)
        board.apply_move(EntityType.PENGUIN1, Direction.RIGHT)
        loc = board.get_entity_location(EntityType.PENGUIN1)
        self.assertEqual(2, loc.x)
        self.assertEqual(0, loc.y)

    def test_BoardsAreEqualIfSameSizeAndEntitiesAreInSameLocations(self):
        board1 = Board(width=3, height=1)
        board2 = Board(width=3, height=1)
        self.assertEqual(board1, board2)
        board1.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board1.add_new_entity(EntityType.BEAR1, 2, 0)
        board2.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board2.add_new_entity(EntityType.BEAR1, 2, 0)
        self.assertEqual(board1, board2)

    def test_BoardsAreEqualIfSameSizeAndSameEntityClassesAreInSameLocations(self):
        board1 = Board(width=3, height=1)
        board2 = Board(width=3, height=1)
        self.assertEqual(board1, board2)
        board1.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board1.add_new_entity(EntityType.BEAR1, 2, 0)
        board2.add_new_entity(EntityType.PENGUIN2, 0, 0)
        board2.add_new_entity(EntityType.BEAR3, 2, 0)
        self.assertEqual(board1, board2)

    def test_BoardsAreNotEqualIfSomeLocationIsDifferent(self):
        board1 = Board(width=3, height=1)
        board2 = Board(width=3, height=1)
        self.assertEqual(board1, board2)
        board1.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board1.add_new_entity(EntityType.BEAR1, 2, 0)
        board2.add_new_entity(EntityType.PENGUIN2, 0, 0)
        board2.add_new_entity(EntityType.BEAR3, 1, 0)
        self.assertNotEqual(board1, board2)


class IntegrationTests(unittest.TestCase):
    def test_PossibleMovesListIsEmptyIfThereAreNoPossibleMoves(self):
        board = Board(width=2, height=2)
        board.add_new_entity(EntityType.PENGUIN1, 1, 0)
        board.add_new_entity(EntityType.BEAR1, 0, 1)
        game = Game(board)
        possible_moves = game.get_all_possible_moves()
        self.assertEqual(0, len(possible_moves))

    def test_ReturnBothPossibleMovesIfThereIsAGapBetweenPenguinAndBear(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.BEAR1, 2, 0)
        game = Game(board)
        possible_moves = game.get_all_possible_moves()
        self.assertEqual(2, len(possible_moves))
        expected_moves = 0
        for m in possible_moves:
            if m.entity_type == EntityType.PENGUIN1:
                self.assertEqual(m.direction, Direction.RIGHT)
                expected_moves += 1
            if m.entity_type == EntityType.BEAR1:
                self.assertEqual(m.direction, Direction.LEFT)
                expected_moves += 1
        self.assertEqual(2, expected_moves)


class EndToEndTests(unittest.TestCase):
    def test_GetWinningMoveIfThereIsJustOneOption(self):
        board = Board(width=3, height=1)
        board.add_new_entity(EntityType.PENGUIN1, 2, 0)
        board.add_new_entity(EntityType.BEAR1, 0, 0)
        board.add_new_entity(EntityType.WATER, 1, 0)
        game = Game(board)
        solution = game.solve()
        self.assertEqual(1, len(solution))
        self.assertEqual(Direction.LEFT, solution[0].direction)
        self.assertEqual(EntityType.PENGUIN1, solution[0].entity_type)

    def test_GetWinningMoveIfThereAreTwoOption(self):
        board = Board(width=3, height=3)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.WATER, 1, 0)
        board.add_new_entity(EntityType.BEAR1, 2, 0)
        board.add_new_entity(EntityType.BEAR2, 0, 2)
        game = Game(board)
        solution = game.solve()
        self.assertEqual(1, len(solution))
        self.assertEqual(Direction.RIGHT, solution[0].direction)
        self.assertEqual(EntityType.PENGUIN1, solution[0].entity_type)

    def test_FindSolutionWhenTwoMovesAreNeeded(self):
        board = Board(width=3, height=3)
        board.add_new_entity(EntityType.PENGUIN1, 0, 1)
        board.add_new_entity(EntityType.WATER, 1, 1)
        board.add_new_entity(EntityType.BEAR1, 2, 0)
        board.add_new_entity(EntityType.BEAR2, 2, 2)
        game = Game(board)
        solution = game.solve()
        self.assertEqual(2, len(solution))
        assert solution[0].direction in [Direction.UP, Direction.DOWN]
        assert solution[0].entity_type in [EntityType.BEAR1, EntityType.BEAR2]
        self.assertEqual(Direction.RIGHT, solution[1].direction)
        self.assertEqual(EntityType.PENGUIN1, solution[1].entity_type)

    def test_FindSolutionWhenManyMovesAreNeeded(self):
        board = Board(5, 5)
        board.add_new_entity(EntityType.PENGUIN1, 0, 2)
        board.add_new_entity(EntityType.WATER, 2, 2)
        board.add_new_entity(EntityType.BEAR1, 0, 0)
        board.add_new_entity(EntityType.BEAR2, 1, 2)
        board.add_new_entity(EntityType.BEAR3, 2, 0)
        board.add_new_entity(EntityType.BEAR4, 3, 1)
        board.add_new_entity(EntityType.BEAR5, 3, 3)
        game = Game(board)
        solution = game.solve()
        self.assertTrue(game.is_won())

    def test_FindSolutionWithMultiplePenguins(self):
        board = Board(5, 5)
        board.add_new_entity(EntityType.PENGUIN1, 0, 0)
        board.add_new_entity(EntityType.PENGUIN2, 0, 2)
        board.add_new_entity(EntityType.WATER, 2, 2)
        board.add_new_entity(EntityType.BEAR1, 0, 1)
        board.add_new_entity(EntityType.BEAR2, 0, 3)
        board.add_new_entity(EntityType.BEAR3, 0, 4)
        board.add_new_entity(EntityType.BEAR4, 2, 0)
        board.add_new_entity(EntityType.BEAR5, 3, 3)
        game = Game(board)
        solution = game.solve()
        self.assertTrue(game.is_won())

    @unittest.skip
    def test_FindSolutionWithMultipleWaters(self):
        board = Board(5, 5)
        # board.add_new_entity(EntityType.WATER1, 2, 1)
        # board.add_new_entity(EntityType.WATER2, 3, 1)
        board.add_new_entity(EntityType.PENGUIN1, 1, 0)
        board.add_new_entity(EntityType.BEAR1, 0, 3)
        board.add_new_entity(EntityType.BEAR2, 2, 0)
        board.add_new_entity(EntityType.BEAR3, 2, 4)
        board.add_new_entity(EntityType.BEAR4, 3, 0)
        board.add_new_entity(EntityType.BEAR5, 4, 3)
        game = Game(board)
        solution = game.solve()
        self.assertTrue(game.is_won())
