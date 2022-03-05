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
    buttons = create_buttons()
    solution = None
    current_move_index = 0
    waiting_for_click_on_board = True
    col, row = -1, -1
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            some_entity_was_selected = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons['Solve'].mouse_inside_button():
                    waiting_for_click_on_board = False
                    board = deepcopy(game.board)
                    print(board)
                    solution = game.solve()
                    if solution:
                        buttons['Next'].visible = True
                        buttons['Solve'].visible = False
                        print("Solution:")
                        for move in solution:
                            print(move)
                    else:
                        print("No solution found :(")
                        run = False
                if buttons['Next'].mouse_inside_button():
                    move = solution[current_move_index]
                    board.apply_move(move.entity_type, move.direction)
                    current_move_index += 1
                    buttons['Next'].visible = current_move_index < len(solution)
                if waiting_for_click_on_board:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col, row = calc_location(mouse_x, mouse_y)
                    if not board.get_entities_in_location(col=col, row=row):
                        buttons['Water'].set_position(mouse_x + 1, mouse_y)
                        buttons['Water'].visible = True
                        buttons['Penguin'].set_position(mouse_x + 1, mouse_y + BUTTON_HEIGHT)
                        buttons['Penguin'].visible = True
                        buttons['Bear'].set_position(mouse_x + 1, mouse_y + BUTTON_HEIGHT * 2)
                        buttons['Bear'].visible = True
                        waiting_for_click_on_board = False
                if buttons['Water'].mouse_inside_button():
                    board.add_new_entity(EntityType.WATER1, col, row)
                    some_entity_was_selected = True
                if buttons['Penguin'].mouse_inside_button():
                    board.add_new_entity(EntityType.PENGUIN1, col, row)
                    some_entity_was_selected = True
                if buttons['Bear'].mouse_inside_button():
                    board.add_new_entity(EntityType.BEAR1, col, row)
                    some_entity_was_selected = True
                if some_entity_was_selected:
                    buttons['Water'].visible = False
                    buttons['Penguin'].visible = False
                    buttons['Bear'].visible = False
                    waiting_for_click_on_board = True
        board.draw(WIN)
        pygame.draw.rect(WIN, BLACK, (0, ROWS * SQUARE_SIZE, WIDTH, SQUARE_SIZE * 2))
        for b in buttons.values():
            b.draw(WIN)
        pygame.display.update()
    pygame.quit()


def calc_location(mouse_x, mouse_y):
    col = mouse_x // SQUARE_SIZE
    row = ROWS - 1 - mouse_y // SQUARE_SIZE
    return col, row


def create_buttons():
    button_top = ROWS * SQUARE_SIZE + SQUARE_SIZE / 2 - BUTTON_HEIGHT / 2
    buttons = dict()
    buttons['Solve'] = Button(
        left=WIDTH / 4 - BUTTON_WIDTH / 2,
        top=button_top,
        text='Solve'
    )
    buttons['Next'] = Button(
        left=3 * WIDTH / 4 - BUTTON_WIDTH / 2,
        top=button_top,
        text='Next',
        visible=False
    )
    buttons['Water'] = Button(
        left=3 * WIDTH / 4 - BUTTON_WIDTH / 2,
        top=button_top - 50,
        text='Water',
        visible=False
    )
    buttons['Penguin'] = Button(
        left=3 * WIDTH / 4 - BUTTON_WIDTH / 2,
        top=button_top,
        text='Penguin',
        visible=False
    )
    buttons['Bear'] = Button(
        left=3 * WIDTH / 4 - BUTTON_WIDTH / 2,
        top=button_top + 50,
        text='Bear',
        visible=False
    )
    return buttons


def create_board(sample_board=False):
    board = Board(rows=ROWS, columns=COLS)
    if sample_board:
        board.add_new_entity(EntityType.PENGUIN1, 4, 4)
        board.add_new_entity(EntityType.WATER1, 2, 2)
        board.add_new_entity(EntityType.BEAR1, 0, 3)
        board.add_new_entity(EntityType.BEAR2, 1, 1)
        board.add_new_entity(EntityType.BEAR3, 2, 4)
        board.add_new_entity(EntityType.BEAR4, 3, 4)
        board.add_new_entity(EntityType.BEAR5, 4, 0)
        board.add_new_entity(EntityType.BEAR6, 4, 3)
    return board


def main():
    board = create_board()
    game = Game(board)
    mainloop(game)


if __name__ == '__main__':
    main()
