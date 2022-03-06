from Penguins.board import Board
from Penguins.entity import EntityClass
from Penguins.game import Game, Move
import pygame
from Penguins.constants import WIDTH, HEIGHT, ROWS, COLS, BLACK, SQUARE_SIZE
from button import Button, BUTTON_WIDTH, BUTTON_HEIGHT

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Penguins')


def mouse_clicked_on_board(x: int, y: int) -> bool:
    return (0 <= x <= SQUARE_SIZE * COLS) and (0 <= y <= SQUARE_SIZE * ROWS)


def mouse_not_clicked_on_buttons(x: int, y: int, buttons: list[Button]) -> bool:
    return not any(b.mouse_inside_button() for b in buttons)


def mainloop(game: Game):
    run = True
    pygame.init()
    clock = pygame.time.Clock()
    board = game.board
    # create the buttons
    buttons = create_buttons()
    solution = None
    current_move_index = 0
    allow_click_on_board = True
    col, row = -1, -1
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            some_entity_was_selected = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if buttons['Solve'].mouse_inside_button():
                    allow_click_on_board = False
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_WAIT))
                    solution = game.solve()
                    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
                    buttons['Solve'].visible = False
                    if solution:
                        buttons['Next'].visible = True
                        print("Solution:")
                        for move in solution:
                            print(move)
                        # reverts the moves so we can present the original board
                        for move in reversed(solution):
                            game.revert_move(move)
                    else:
                        print("No solution found :(")
                        buttons['Done'].visible = True
                if buttons['Next'].mouse_inside_button():
                    move: Move = solution[current_move_index]
                    board.apply_move(move.entity, move.direction)
                    current_move_index += 1
                    if current_move_index >= len(solution):
                        buttons['Next'].visible = False
                        buttons['Done'].visible = True
                if allow_click_on_board and mouse_clicked_on_board(mouse_x, mouse_y) and mouse_not_clicked_on_buttons(mouse_x, mouse_y, list(buttons.values())):
                    col, row = calc_location(mouse_x, mouse_y)
                    # print(f"{x},{y} -> {col},{row}")
                    if not board.get_entities_in_location(col=col, row=row):
                        buttons['Water'].set_position(mouse_x + 1, mouse_y)
                        buttons['Water'].visible = True
                        buttons['Penguin'].set_position(mouse_x + 1, mouse_y + BUTTON_HEIGHT)
                        buttons['Penguin'].visible = True
                        buttons['Bear'].set_position(mouse_x + 1, mouse_y + BUTTON_HEIGHT * 2)
                        buttons['Bear'].visible = True
                if buttons['Water'].mouse_inside_button():
                    board.add_new_entity(EntityClass.WATER, col, row)
                    some_entity_was_selected = True
                if buttons['Penguin'].mouse_inside_button():
                    board.add_new_entity(EntityClass.PENGUIN, col, row)
                    some_entity_was_selected = True
                if buttons['Bear'].mouse_inside_button():
                    board.add_new_entity(EntityClass.BEAR, col, row)
                    some_entity_was_selected = True
                if some_entity_was_selected:
                    buttons['Water'].visible = False
                    buttons['Penguin'].visible = False
                    buttons['Bear'].visible = False
                if buttons['Done'].mouse_inside_button():
                    run = False
        board.draw(WIN)
        pygame.draw.rect(WIN, BLACK, (0, ROWS * SQUARE_SIZE, WIDTH, SQUARE_SIZE * 2))
        for b in buttons.values():
            b.draw(WIN)
        pygame.display.update()
    pygame.quit()


def calc_location(mouse_x, mouse_y):
    col = mouse_x // SQUARE_SIZE
    row = mouse_y // SQUARE_SIZE
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
    buttons['Done'] = Button(
        left=WIDTH / 4 - BUTTON_WIDTH / 2,
        top=button_top,
        text='Done',
        visible=False
    )
    return buttons


def create_board(sample_board=False):
    board = Board(rows=ROWS, columns=COLS)
    if sample_board:
        board.add_new_entity(EntityClass.PENGUIN, 4, 4)
        board.add_new_entity(EntityClass.WATER, 2, 2)
        board.add_new_entity(EntityClass.BEAR, 0, 3)
        board.add_new_entity(EntityClass.BEAR, 1, 1)
        board.add_new_entity(EntityClass.BEAR, 2, 4)
        board.add_new_entity(EntityClass.BEAR, 3, 4)
        board.add_new_entity(EntityClass.BEAR, 4, 0)
        board.add_new_entity(EntityClass.BEAR, 4, 3)
    return board


def main():
    board = create_board()
    game = Game(board)
    mainloop(game)


if __name__ == '__main__':
    main()
