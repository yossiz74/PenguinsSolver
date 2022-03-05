import pygame.draw
from enum import Enum, auto
from Penguins.constants import SQUARE_SIZE, BLACK, WHITE, BLUE, GREY, ROWS


class EntityClass(Enum):
    PENGUIN = auto()
    BEAR = auto()
    WATER = auto()


class Entity:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row: int, col: int, entity_class: EntityClass, name: str):
        self.row = row
        self.col = col
        self.entity_class = entity_class
        self.name = name
        self.x = 0
        self.y = 0
        self.calc_pos()

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * (ROWS - 1 - self.row) + SQUARE_SIZE // 2

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def draw(self, win):
        color = self._get_color_by_entity_class()
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, color, (self.x, self.y), radius)

    def _get_color_by_entity_class(self) -> tuple[int, int, int]:
        if self.entity_class == EntityClass.WATER:
            return BLUE
        if self.entity_class == EntityClass.BEAR:
            return WHITE
        if self.entity_class == EntityClass.PENGUIN:
            return BLACK

    def __repr__(self):
        return self.name
