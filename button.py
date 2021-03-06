import pygame

from Penguins.constants import WHITE

BUTTON_WIDTH = 140
BUTTON_HEIGHT = 40
BUTTON_LIGHT_SHADE = (170, 170, 170)
BUTTON_DARK_SHADE = (100, 100, 100)


class Button:
    def __init__(self, left, top, text, visible=True):
        self.left = left
        self.top = top
        self.text = text
        self.visible = visible

    def set_position(self, left, top):
        self.left = left
        self.top = top

    def draw(self, win: pygame.Surface):
        if not self.visible:
            return
        small_font = pygame.font.SysFont('Arial', 35)
        text_render = small_font.render(self.text, True, WHITE)
        # if mouse is hovered on a button it changes to lighter shade
        if self.mouse_inside_button():
            pygame.draw.rect(win, BUTTON_LIGHT_SHADE, [self.left, self.top, BUTTON_WIDTH, BUTTON_HEIGHT])
        else:
            pygame.draw.rect(win, BUTTON_DARK_SHADE, [self.left, self.top, BUTTON_WIDTH, BUTTON_HEIGHT])
        # superimposing the text onto our button
        win.blit(text_render, (self.left + 36, self.top))

    def mouse_inside_button(self) -> bool:
        if not self.visible:
            return False
        mouse = pygame.mouse.get_pos()
        return self.left <= mouse[0] <= self.left + BUTTON_WIDTH and self.top <= mouse[1] <= self.top + BUTTON_HEIGHT
