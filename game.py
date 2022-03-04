from dataclasses import dataclass
from board import Board, EntityType, EntityClass, get_entity_class
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
        self.seen_boards = []
        self.search_tree_level = 0

    def is_won(self) -> bool:
        p1_location = self.board.get_entity_location(EntityType.PENGUIN1)
        p2_location = self.board.get_entity_location(EntityType.PENGUIN2)
        return p1_location is None and p2_location is None

    def entity_move_is_legal(self, entity_type, direction) -> bool:
        entity_location = self.board.get_entity_location(entity_type)
        if entity_location is None:
            return False
        if direction == Direction.LEFT:
            x = entity_location.x - 1
            y = entity_location.y
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return x < entity_location.x - 1  # false if there is an immediate blocking neighbour, true if the blocker is farther
                x -= 1
            return False
        if direction == Direction.RIGHT:
            x = entity_location.x + 1
            y = entity_location.y
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return x > entity_location.x + 1
                x += 1
            return False
        if direction == Direction.UP:
            x = entity_location.x
            y = entity_location.y + 1
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return y > entity_location.y + 1
                y += 1
            return False
        if direction == Direction.DOWN:
            x = entity_location.x
            y = entity_location.y - 1
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return y < entity_location.y - 1
                y -= 1
            return False

    def get_all_possible_moves(self) -> list[Move]:
        possible_moves = []
        for et in EntityType:
            if get_entity_class(et) != EntityClass.WATER:
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
        # print(f"[{self.search_tree_level}] {possible_moves}")
        for m in possible_moves:
            board_before_move = copy.deepcopy(self.board)
            self.board.apply_move(m.entity_type, m.direction)
            if any([self.board == x for x in self.seen_boards]):
                # already examined this board setup, so no point of further examinations of this move
                # print("Already seen this board")
                self.board = board_before_move  # revert the move
                continue
            # print(board_before_move)
            # print(f"[{self.search_tree_level}] applied {m}")
            # print(self.board)
            self.seen_boards.append(copy.deepcopy(self.board))
            if self.is_won():
                return [m]
            else:
                self.search_tree_level += 1
                solution_moves = self.solve()
                self.search_tree_level -= 1
                if solution_moves:
                    overall_solution = [m]
                    overall_solution.extend(solution_moves)
                    return overall_solution
                else:
                    self.board = board_before_move  # revert the move
                    # print(f"[{self.search_tree_level}] Backtracking {m}")
        return []
