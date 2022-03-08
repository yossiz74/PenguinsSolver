import unittest
from Penguins.board import Board, Location
from Penguins.entity import EntityClass
from Penguins.game import Game, Move
from Penguins.direction import Direction


class BoardTests(unittest.TestCase):
    def test_GetAllEntitiesReturnsEmptyListIfNoneExist(self):
        board = Board(columns=1, rows=1)
        result = board.get_all_entities_of_class(EntityClass.PENGUIN)
        self.assertListEqual([], result)

    def test_GetAllEntitiesByClassReturnsAllOfThatClass(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        p2 = board.add_new_entity(EntityClass.PENGUIN, 2, 0)
        board.add_new_entity(EntityClass.WATER, 1, 0)
        result = board.get_all_entities_of_class(EntityClass.PENGUIN)
        self.assertListEqual([p1, p2], result)

    def test_WhenAPenguinIsOnWaterItIsRemovedFromTheGame(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 2, 0)
        board.add_new_entity(EntityClass.WATER, 0, 0)
        board.move_entity(p1, 0, 0)
        self.assertIsNone(board.get_entity_location(p1))

    def test_BoardsAreEqualIfSameSizeAndEntitiesAreInSameLocations(self):
        board1 = Board(columns=3, rows=1)
        board2 = Board(columns=3, rows=1)
        self.assertEqual(board1, board2)
        board1.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board1.add_new_entity(EntityClass.BEAR, 2, 0)
        board2.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board2.add_new_entity(EntityClass.BEAR, 2, 0)
        self.assertEqual(board1, board2)

    def test_BoardsAreEqualIfSameSizeAndSameEntityClassesAreInSameLocations(self):
        board1 = Board(columns=3, rows=1)
        board2 = Board(columns=3, rows=1)
        self.assertEqual(board1, board2)
        board1.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board1.add_new_entity(EntityClass.BEAR, 2, 0)
        board2.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board2.add_new_entity(EntityClass.BEAR, 2, 0)
        self.assertEqual(board1, board2)

    def test_BoardsAreNotEqualIfSomeLocationIsDifferent(self):
        board1 = Board(columns=3, rows=1)
        board2 = Board(columns=3, rows=1)
        self.assertEqual(board1, board2)
        board1.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board1.add_new_entity(EntityClass.BEAR, 2, 0)
        board2.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board2.add_new_entity(EntityClass.BEAR, 1, 0)
        self.assertNotEqual(board1, board2)

    def test_PointIsInsideTheBoard(self):
        board = Board(columns=2, rows=3)
        self.assertTrue(board.location_is_inside_the_board(0, 0))
        self.assertTrue(board.location_is_inside_the_board(0, 1))
        self.assertTrue(board.location_is_inside_the_board(0, 2))
        self.assertTrue(board.location_is_inside_the_board(1, 0))
        self.assertTrue(board.location_is_inside_the_board(1, 1))
        self.assertTrue(board.location_is_inside_the_board(1, 2))
        self.assertFalse(board.location_is_inside_the_board(-1, 0))
        self.assertFalse(board.location_is_inside_the_board(2, 0))
        self.assertFalse(board.location_is_inside_the_board(0, -1))
        self.assertFalse(board.location_is_inside_the_board(0, 3))

    def test_ThereIsABlockerEntity(self):
        board = Board(columns=3, rows=2)
        board.add_new_entity(EntityClass.BEAR, 0, 0)
        self.assertTrue(board.there_is_a_blocker_entity_in(0, 0))
        self.assertFalse(board.there_is_a_blocker_entity_in(0, 1))
        self.assertFalse(board.there_is_a_blocker_entity_in(1, 0))

    def test_MoveEntitySingleStep(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.apply_move(p1, Direction.RIGHT)
        loc = board.get_entity_location(p1)
        self.assertEqual(Location(1, 0), loc)

    def test_MoveEntityMultipleSteps(self):
        board = Board(columns=4, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 3, 0)
        board.apply_move(p1, Direction.RIGHT)
        loc = board.get_entity_location(p1)
        self.assertEqual(2, loc.col)
        self.assertEqual(0, loc.row)

    def test_RevertMoveEntityMultipleSteps(self):
        board = Board(columns=4, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 3, 0)
        orig_loc = board.apply_move(p1, Direction.RIGHT)
        p1.move(col=orig_loc.col, row=orig_loc.row)
        loc = board.get_entity_location(p1)
        self.assertEqual(0, loc.col)
        self.assertEqual(0, loc.row)


class GameTests(unittest.TestCase):
    def test_GameIsWonWhenThereAreNoPenguinsLeft(self):
        board = Board(columns=1, rows=1)
        board.add_new_entity(EntityClass.WATER, 0, 0)
        game = Game(board)
        self.assertTrue(game.is_won())

    def test_GameIsNotWonWhenThereArePenguinsOnBoard(self):
        board = Board(columns=3, rows=1)
        board.add_new_entity(EntityClass.PENGUIN, 1, 0)
        board.add_new_entity(EntityClass.WATER, 2, 0)
        game = Game(board)
        self.assertFalse(game.is_won())

    def test_PenguinMoveIsIllegalIfThereIsNoBearInTheWay(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 2, 0)
        game = Game(board)
        self.assertEqual(False, game.entity_move_is_legal(p1, Direction.LEFT))  # assertFalse also asserts not returning value at all

    def test_BearMoveIsIllegalIfThereIsAPenguinNeighbour(self):
        board = Board(columns=3, rows=1)
        board.add_new_entity(EntityClass.PENGUIN, 1, 0)
        b1 = board.add_new_entity(EntityClass.BEAR, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        game = Game(board)
        self.assertEqual(False, game.entity_move_is_legal(b1, Direction.RIGHT))

    def test_PenguinMoveIsLegalIfThereIsABearInTheWay(self):
        board = Board(columns=5, rows=5)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 2, 2)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 0, 2)
        board.add_new_entity(EntityClass.BEAR, 2, 4)
        board.add_new_entity(EntityClass.BEAR, 4, 2)
        game = Game(board)
        self.assertTrue(game.entity_move_is_legal(p1, Direction.LEFT))
        self.assertTrue(game.entity_move_is_legal(p1, Direction.RIGHT))
        self.assertTrue(game.entity_move_is_legal(p1, Direction.UP))
        self.assertTrue(game.entity_move_is_legal(p1, Direction.DOWN))

    def test_GetPossibleMovesForEntityIsEmptyIfNoneAvailable(self):
        board = Board(columns=2, rows=2)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 1, 0)
        board.add_new_entity(EntityClass.BEAR, 0, 1)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(p1)
        self.assertEqual(0, len(possible_moves))

    def test_GetPossibleMovesForEntityIsEmptyIfNeighbourIsBlocker(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 1, 0)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(p1)
        self.assertEqual(0, len(possible_moves))

    def test_GetPossibleMovesForEntityReturnsOneIfOnlyOneAvailable(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(p1)
        self.assertEqual(1, len(possible_moves))
        self.assertEqual(Direction.RIGHT, possible_moves[0].direction)

    def test_GetPossibleMovesForPenguinReturnsAllIfMultipleAvailable(self):
        board = Board(columns=3, rows=3)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 0, 2)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(p1)
        self.assertEqual(2, len(possible_moves))
        self.assertTrue(Direction.RIGHT in [m.direction for m in possible_moves])
        self.assertTrue(Direction.DOWN in [m.direction for m in possible_moves])

    def test_GetPossibleMovesForBearReturnsAllIfMultipleAvailable(self):
        board = Board(columns=3, rows=3)
        board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.BEAR, 0, 2)
        b1 = board.add_new_entity(EntityClass.BEAR, 2, 2)
        game = Game(board)
        possible_moves = game.get_possible_moves_of(b1)
        self.assertEqual(2, len(possible_moves))
        self.assertTrue(Direction.LEFT in [m.direction for m in possible_moves])
        self.assertTrue(Direction.UP in [m.direction for m in possible_moves])

    def test_PossibleMovesListIsEmptyIfThereAreNoPossibleMoves(self):
        board = Board(columns=2, rows=2)
        board.add_new_entity(EntityClass.PENGUIN, 1, 0)
        board.add_new_entity(EntityClass.BEAR, 0, 1)
        game = Game(board)
        possible_moves = game.get_all_possible_moves()
        self.assertEqual(0, len(possible_moves))

    def test_ReturnBothPossibleMovesIfThereIsAGapBetweenPenguinAndBear(self):
        board = Board(columns=3, rows=1)
        board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        game = Game(board)
        possible_moves = game.get_all_possible_moves()
        self.assertEqual(2, len(possible_moves))
        expected_moves = 0
        for m in possible_moves:
            if m.entity.entity_class == EntityClass.PENGUIN:
                self.assertEqual(m.direction, Direction.RIGHT)
                expected_moves += 1
            if m.entity.entity_class == EntityClass.BEAR:
                self.assertEqual(m.direction, Direction.LEFT)
                expected_moves += 1
        self.assertEqual(2, expected_moves)

    def test_Move(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        game = Game(board)
        move = Move(direction=Direction.RIGHT, entity=p1)
        game.perform_move(move)
        self.assertEqual(0, p1.row)
        self.assertEqual(1, p1.col)

    def test_RevertMove(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        game = Game(board)
        move = Move(direction=Direction.RIGHT, entity=p1)
        game.perform_move(move)
        game.revert_move(move)
        self.assertEqual(0, p1.row)
        self.assertEqual(0, p1.col)

    def test_RevertMoveOfDivingPenguin(self):
        board = Board(columns=3, rows=1)
        p1 = board.add_new_entity(EntityClass.PENGUIN, 0, 0)
        board.add_new_entity(EntityClass.BEAR, 2, 0)
        board.add_new_entity(EntityClass.WATER, 1, 0)
        game = Game(board)
        move = Move(direction=Direction.RIGHT, entity=p1)
        game.perform_move(move)
        self.assertNotIn(p1, game.board.entities)
        game.revert_move(move)
        self.assertIn(p1, game.board.entities)
