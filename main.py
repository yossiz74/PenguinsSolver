from board import Board, EntityType
from game import Game


def main():
    board = Board(5, 5)
    board.place_entity(EntityType.PENGUIN1, 0, 0)
    board.place_entity(EntityType.PENGUIN2, 0, 2)
    board.place_entity(EntityType.WATER, 2, 2)
    board.place_entity(EntityType.BEAR1, 0, 1)
    board.place_entity(EntityType.BEAR2, 0, 3)
    board.place_entity(EntityType.BEAR3, 0, 4)
    board.place_entity(EntityType.BEAR4, 2, 0)
    board.place_entity(EntityType.BEAR5, 3, 3)
    print(board)
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
