from collections import Counter
from dataclasses import dataclass

import pygame

from Penguins.constants import SQUARE_SIZE, BLACK, LIGHT_BLUE
from direction import Direction
from Penguins.entity import Entity, EntityType, EntityClass, get_entity_class


@dataclass
class Location:
    col: int
    row: int

    def __repr__(self):
        return f'Location(col={self.col}, row={self.row})'

    def __eq__(self, other):
        return (self.col == other.col) and (self.row == other.row)


class Board:
    def __init__(self, columns: int, rows: int):
        self.columns = columns
        self.rows = rows
        self.entities: list[Entity] = []

    def __eq__(self, other):
        answer = (self.columns == other.columns and self.rows == other.rows)
        for col in range(self.columns):
            for row in range(self.rows):
                my_entities = [get_entity_class(e) for e in self.get_entities_in_location(col, row)]
                other_entities = [get_entity_class(e) for e in other.get_entities_in_location(col, row)]
                if Counter(my_entities) != Counter(other_entities):
                    return False
        return answer

    def __repr__(self):
        s = ""
        for row in range(self.rows, 0, -1):
            for col in range(self.columns):
                s += "|"
                entities = self.get_entities_in_location(col, row - 1)
                if entities:
                    for e in entities:
                        s += e.name[0] + e.name[-1]
                else:
                    s += "  "
                s += "|"
            s += "\n"
        return s

    def add_new_entity(self, entity_type: EntityType, col: int, row: int):
        if entity_type != EntityType.NONE and entity_type in [e.entity_type for e in self.entities]:
            raise KeyError(f"Trying to add an already existing entity {entity_type}")
        self.entities.append(Entity(row=row, col=col, entity_type=entity_type))

    def move_entity(self, entity_type: EntityType, col: int, row: int):
        e = self.get_entity_of_type(entity_type)
        if not e:
            raise KeyError(f"Trying to move a non-existing entity {entity_type}")
        e.move(row=row, col=col)
        # if a penguin reaches the water, it dives into it
        if get_entity_class(entity_type) == EntityClass.PENGUIN:
            if any([get_entity_class(e) == EntityClass.WATER for e in self.get_entities_in_location(col, row)]):
                self.entities.remove(self.get_entity_of_type(entity_type))

    def get_entity_of_type(self, entity_type) -> Entity:
        for e in self.entities:
            if e.entity_type == entity_type:
                return e

    def get_entity_location(self, entity_type: EntityType) -> Location:
        e = self.get_entity_of_type(entity_type)
        if e is not None:
            return Location(row=e.row, col=e.col)

    def location_is_inside_the_board(self, col, row) -> bool:
        return (self.columns > col >= 0) and (self.rows > row >= 0)

    def there_is_a_blocker_entity_in(self, col, row) -> bool:
        entities = self.get_entities_in_location(col, row)
        return any([get_entity_class(e) in [EntityClass.PENGUIN, EntityClass.BEAR] for e in entities])

    def get_entities_in_location(self, col, row) -> list[EntityType]:
        answer = []
        for e in self.entities:
            if e.col == col and e.row == row:
                answer.append(e.entity_type)
        return answer

    def apply_move(self, entity_type, direction):
        if direction == Direction.RIGHT:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.col + 1, p.row):
                p.col += 1
                if not self.location_is_inside_the_board(p.col, p.row):
                    raise ValueError(f"{entity_type} went overboard")
            self.move_entity(entity_type, p.col, p.row)
        if direction == Direction.LEFT:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.col - 1, p.row):
                p.col -= 1
                if not self.location_is_inside_the_board(p.col, p.row):
                    raise ValueError(f"{entity_type} went overboard")
            self.move_entity(entity_type, p.col, p.row)
        if direction == Direction.UP:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.col, p.row + 1):
                p.row += 1
                if not self.location_is_inside_the_board(p.col, p.row):
                    raise ValueError(f"{entity_type} went overboard")
            self.move_entity(entity_type, p.col, p.row)
        if direction == Direction.DOWN:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.col, p.row - 1):
                p.row -= 1
                if not self.location_is_inside_the_board(p.col, p.row):
                    raise ValueError(f"{entity_type} went overboard")
            self.move_entity(entity_type, p.col, p.row)

    def draw(self, win):
        pygame.draw.rect(win, LIGHT_BLUE, (0, 0, self.columns * SQUARE_SIZE, self.rows * SQUARE_SIZE))
        for row in range(self.rows):
            for col in range(self.columns):
                pygame.draw.rect(win, BLACK, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
        for e in self.entities:
            e.draw(win)
