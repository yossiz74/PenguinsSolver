from dataclasses import dataclass
from Penguins.board import Board
from Penguins.entity import Entity, EntityClass
from Penguins.direction import Direction
import copy


@dataclass
class Move:
    direction: Direction
    entity: Entity
    original_location = None

    def __repr__(self):
        return f"Move {self.entity.name} {self.direction.name}"


class Game:
    def __init__(self, board: Board):
        self.board = board
        self.seen_configuration = []
        self.search_tree_level = 0

    def is_won(self) -> bool:
        penguins = self.board.get_all_entities_of_class(EntityClass.PENGUIN)
        return len(penguins) == 0

    def entity_move_is_legal(self, entity: Entity, direction) -> bool:
        entity_location = self.board.get_entity_location(entity)
        if entity_location is None:
            return False
        if direction == Direction.LEFT:
            x = entity_location.col - 1
            y = entity_location.row
            while self.board.location_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return x < entity_location.col - 1  # false if there is an immediate blocking neighbour, true if the blocker is farther
                x -= 1
            return False
        if direction == Direction.RIGHT:
            x = entity_location.col + 1
            y = entity_location.row
            while self.board.location_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return x > entity_location.col + 1
                x += 1
            return False
        if direction == Direction.UP:
            x = entity_location.col
            y = entity_location.row + 1
            while self.board.location_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return y > entity_location.row + 1
                y += 1
            return False
        if direction == Direction.DOWN:
            x = entity_location.col
            y = entity_location.row - 1
            while self.board.location_is_inside_the_board(x, y):
                if self.board.there_is_a_blocker_entity_in(x, y):
                    return y < entity_location.row - 1
                y -= 1
            return False

    def get_all_possible_moves(self) -> list[Move]:
        possible_moves = []
        for e in self.board.entities:
            if e.entity_class != EntityClass.WATER:
                entity_possible_moves = self.get_possible_moves_of(e)
                possible_moves.extend(entity_possible_moves)
        return possible_moves

    def get_possible_moves_of(self, entity: Entity) -> list[Move]:
        possible_moves = []
        for d in Direction:
            if self.entity_move_is_legal(entity, d):
                possible_moves.append(Move(entity=entity, direction=d))
        return possible_moves

    def solve(self):
        possible_moves = self.get_all_possible_moves()
        # print(f"[{self.search_tree_level}] {possible_moves}")
        for m in possible_moves:
            self.perform_move(m)
            if any([self.board == x for x in self.seen_configuration]):
                # already examined this board setup, so no point of further examinations of this move
                # print("Already seen this board")
                self.revert_move(m)
                continue
            # print(board_before_move)
            # print(f"[{self.search_tree_level}] applied {m}")
            # print(self.board)
            self.seen_configuration.append(copy.deepcopy(self.board))
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
                    self.revert_move(m)
                    # print(f"[{self.search_tree_level}] Backtracking {m}")
        return []

    def perform_move(self, move: Move):
        move.original_location = self.board.apply_move(move.entity, move.direction)

    def revert_move(self, move):
        move.entity.move(col=move.original_location.col, row=move.original_location.row)
        if move.entity not in self.board.entities:  # dived penguin
            self.board.entities.append(move.entity)
