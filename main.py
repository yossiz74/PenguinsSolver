from board import Board, EntityType
from game import Game


def main():
    board = Board(3, 3)
    board.place_entity(EntityType.PENGUIN, 0, 1)
    board.place_entity(EntityType.WATER, 1, 1)
    board.place_entity(EntityType.BEAR1, 2, 0)
    board.place_entity(EntityType.BEAR2, 2, 2)
    game = Game(board)
    solution = game.solve()
    if solution:
        print("Solution:")
        for move in solution:
            print(move)
    else:
        print("No solution found :(")


if __name__ == '__main__':
    main()
