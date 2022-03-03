from dataclasses import dataclass
from board import Board, EntityType
from direction import Direction
import copy


@dataclass
class Move:
    direction: Direction
    entity_type: EntityType

    def __repr__(self):
        return f"Move {self.entity_type.name} {self.direction.name}"


class Game:
    def __init__(self, board: Board):
        self.board = board

    def is_won(self) -> bool:
        penguin_location = self.board.get_entity_location(EntityType.PENGUIN)
        water_location = self.board.get_entity_location(EntityType.WATER)
        return penguin_location == water_location

    def entity_move_is_legal(self, entity_type, direction) -> bool:
        entity_location = self.board.get_entity_location(entity_type)
        if entity_location is None:
            return False
        if direction == Direction.LEFT:
            x = entity_location.x - 2
            y = entity_location.y
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return True
                x -= 1
            return False
        if direction == Direction.RIGHT:
            x = entity_location.x + 2
            y = entity_location.y
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return True
                x += 1
            return False
        if direction == Direction.UP:
            x = entity_location.x
            y = entity_location.y + 2
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return True
                y += 1
            return False
        if direction == Direction.DOWN:
            x = entity_location.x
            y = entity_location.y - 2
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return True
                y -= 1
            return False

    def get_all_possible_moves(self) -> list[Move]:
        possible_moves = []
        for et in EntityType:
            if et != EntityType.WATER:
                entity_possible_moves = self.get_possible_moves_of(et)
                possible_moves.extend(entity_possible_moves)
        return possible_moves

    def get_possible_moves_of(self, entity_type) -> list[Move]:
        possible_moves = []
        for d in Direction:
            if self.entity_move_is_legal(entity_type, d):
                possible_moves.append(Move(entity_type=entity_type, direction=d))
        return possible_moves

    def solve(self):
        possible_moves = self.get_all_possible_moves()
        for m in possible_moves:
            board_before_move = copy.deepcopy(self.board)
            self.board.apply_move(m.entity_type, m.direction)
            if self.is_won():
                return [m]
            else:
                solution_moves = self.solve()
                if solution_moves:
                    overall_solution = [m]
                    overall_solution.extend(solution_moves)
                    return overall_solution
                else:
                    self.board = board_before_move  # revert the move
        return []
