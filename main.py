from board import Board, EntityType
from game import Game


def main():
    board = Board(5, 5)
    board.add_new_entity(EntityType.PENGUIN1, 4, 4)
    board.add_new_entity(EntityType.WATER1, 2, 2)
    board.add_new_entity(EntityType.BEAR1, 0, 3)
    board.add_new_entity(EntityType.BEAR2, 1, 1)
    board.add_new_entity(EntityType.BEAR3, 2, 4)
    board.add_new_entity(EntityType.BEAR4, 3, 4)
    board.add_new_entity(EntityType.BEAR5, 4, 0)
    board.add_new_entity(EntityType.BEAR6, 4, 3)
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
