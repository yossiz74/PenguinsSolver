from Penguins.board import Board, EntityType
from game import Game
import pygame
from Penguins.constants import WIDTH, HEIGHT, ROWS, COLS, BLACK, SQUARE_SIZE
from copy import deepcopy
from button import Button, BUTTON_WIDTH, BUTTON_HEIGHT

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Penguins')


def mainloop(game: Game):
    run = True
    pygame.init()
    clock = pygame.time.Clock()
    board = game.board
    # create the buttons
    button_top = ROWS * SQUARE_SIZE + SQUARE_SIZE / 2 - BUTTON_HEIGHT / 2
    solve_button = Button(
        left=WIDTH / 4 - BUTTON_WIDTH / 2,
        top=button_top,
        text='Solve'
    )
    next_button = Button(
        left=3*WIDTH / 4 - BUTTON_WIDTH / 2,
        top=button_top,
        text='Next',
        visible=False
    )
    solution = None
    current_move_index = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if solve_button.mouse_inside_button():
                    board = deepcopy(game.board)
                    solution = game.solve()
                    if solution:
                        next_button.visible = True
                        solve_button.visible = False
                        print("Solution:")
                        for move in solution:
                            print(move)
                    else:
                        print("No solution found :(")
                        run = False
                if next_button.mouse_inside_button():
                    move = solution[current_move_index]
                    board.apply_move(move.entity_type, move.direction)
                    current_move_index += 1
                    next_button.visible = current_move_index < len(solution)
        board.draw_board(WIN)
        pygame.draw.rect(WIN, BLACK, (0, ROWS * SQUARE_SIZE, WIDTH, SQUARE_SIZE))
        solve_button.draw(WIN)
        next_button.draw(WIN)
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
