import pygame.draw
from enum import Enum, auto
from Penguins.constants import SQUARE_SIZE, BLACK, WHITE, BLUE, GREY, ROWS


class EntityType(Enum):
    PENGUIN1 = auto()
    PENGUIN2 = auto()
    BEAR1 = auto()
    BEAR2 = auto()
    BEAR3 = auto()
    BEAR4 = auto()
    BEAR5 = auto()
    BEAR6 = auto()
    WATER1 = auto()
    WATER2 = auto()


class EntityClass(Enum):
    PENGUIN = auto()
    BEAR = auto()
    WATER = auto()


def get_entity_class(e: EntityType) -> EntityClass:
    if e in [EntityType.PENGUIN1, EntityType.PENGUIN2]:
        return EntityClass.PENGUIN
    if e in [EntityType.BEAR1, EntityType.BEAR2, EntityType.BEAR3, EntityType.BEAR4, EntityType.BEAR5, EntityType.BEAR6]:
        return EntityClass.BEAR
    if e in [EntityType.WATER1, EntityType.WATER2]:
        return EntityClass.WATER
    raise ValueError(f"Unknown entity type {e}")


class Entity:
    PADDING = 10
    OUTLINE = 2

    def __init__(self, row: int, col: int, entity_type: EntityType):
        self.row = row
        self.col = col
        self.entity_type = entity_type
        self.x = 0
        self.y = 0
        self.calc_pos()

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

    def _get_color_by_entity_class(self):
        ec = get_entity_class(self.entity_type)
        if ec == EntityClass.WATER:
            return BLUE
        if ec == EntityClass.BEAR:
            return WHITE
        if ec == EntityClass.PENGUIN:
            return BLACK
        raise ValueError(f"Unknown entity class {ec}")

    def __repr__(self):
        return self.entity_type.name
