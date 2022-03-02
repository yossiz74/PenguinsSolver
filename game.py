from board import Board
from enum import Enum, auto


class Move(Enum):
    LEFT = auto()
    UP = auto()
    RIGHT = auto()
    DOWN = auto()


class Game:
    def __init__(self, board: Board):
        self.board = board

    def is_won(self) -> bool:
        penguin_location = self.board.get_penguin_location()
        water_location = self.board.get_water_location()
        return penguin_location == water_location

    def penguin_move_is_legal(self, move) -> bool:
        penguin_location = self.board.get_penguin_location()
        if move == move.LEFT:
            x = penguin_location.x - 1
            y = penguin_location.y
            while self.board.point_is_inside_the_board(x, y):
                if self.board.there_is_a_bear_in(x, y):
                    return True
                x -= 1
            return False
        if move == move.RIGHT:
            pass
        if move == move.UP:
            pass
        if move == move.DOWN:
            pass
