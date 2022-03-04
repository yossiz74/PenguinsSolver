from Penguins.board import Board, EntityType
from game import Game
import pygame
from Penguins.constants import WIDTH, HEIGHT, ROWS, COLS
from copy import deepcopy

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Penguins')


def mainloop(game: Game):
    run = True
    clock = pygame.time.Clock()
    board = game.board
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO if on solve button:
                board = deepcopy(game.board)
                solution = game.solve()
                if solution:
                    print("Solution:")
                    for move in solution:
                        print(move)
                else:
                    print("No solution found :(")
                    run = False
                # TODO if on next button: apply next move
                pass
        board.draw_board(WIN)
        pygame.display.update()
    pygame.quit()


def main():
    board = create_board()
    game = Game(board)
    mainloop(game)


def create_board():
    board = Board(rows=ROWS, columns=COLS)
    board.add_new_entity(EntityType.PENGUIN1, 4, 4)
    board.add_new_entity(EntityType.WATER1, 2, 2)
    board.add_new_entity(EntityType.BEAR1, 0, 3)
    board.add_new_entity(EntityType.BEAR2, 1, 1)
    board.add_new_entity(EntityType.BEAR3, 2, 4)
    board.add_new_entity(EntityType.BEAR4, 3, 4)
    board.add_new_entity(EntityType.BEAR5, 4, 0)
    board.add_new_entity(EntityType.BEAR6, 4, 3)
    print(board)
    return board


if __name__ == '__main__':
    main()
