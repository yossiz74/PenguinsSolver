from board import Board


class Game:
    def __init__(self, board: Board):
        self.board = board

    def is_won(self) -> bool:
        penguin = self.board.get_penguin_location()
        water = self.board.get_water_location()
        return penguin == water
