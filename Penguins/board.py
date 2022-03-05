from collections import Counter
from dataclasses import dataclass

import pygame

from Penguins.constants import SQUARE_SIZE, BLACK, LIGHT_BLUE
from direction import Direction
from Penguins.entity import Entity, EntityClass


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
        self.next_index_to_use_for_entity = dict()
        for ec in EntityClass:
            self.next_index_to_use_for_entity[ec] = 1

    def __eq__(self, other):
        """ Boards are equal if they are of same size, and have the same entities in the same locations """
        answer = (self.columns == other.columns and self.rows == other.rows)
        for col in range(self.columns):
            for row in range(self.rows):
                if Counter(self.get_entities_in_location(col, row)) != Counter(other.get_entities_in_location(col, row)):
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

    def add_new_entity(self, entity_class: EntityClass, col: int, row: int) -> Entity:
        index = self.next_index_to_use_for_entity[entity_class]
        self.next_index_to_use_for_entity[entity_class] += 1
        name = entity_class.name + str(index)
        entity = Entity(row=row, col=col, entity_class=entity_class, name=name)
        self.entities.append(entity)
        return entity

    def move_entity(self, entity: Entity, col: int, row: int):
        entity.move(row=row, col=col)
        # if a penguin reaches the water, it dives into it
        if entity.entity_class == EntityClass.PENGUIN:
            if any([x.entity_class == EntityClass.WATER for x in self.get_entities_in_location(col, row)]):
                self.entities.remove(entity)

    def get_entity_location(self, entity: Entity) -> Location:
        if entity in self.entities:
            return Location(row=entity.row, col=entity.col)

    def location_is_inside_the_board(self, col, row) -> bool:
        return (self.columns > col >= 0) and (self.rows > row >= 0)

    def there_is_a_blocker_entity_in(self, col, row) -> bool:
        entities = self.get_entities_in_location(col, row)
        return any([e.entity_class in [EntityClass.PENGUIN, EntityClass.BEAR] for e in entities])

    def get_entities_in_location(self, col, row) -> list[Entity]:
        answer = []
        for e in self.entities:
            if e.col == col and e.row == row:
                answer.append(e)
        return answer

    def apply_move(self, entity: Entity, direction: Direction) -> Location:
        col, row = entity.col, entity.row
        orig_loc = Location(col=col, row=row)
        if direction == Direction.RIGHT:
            while not self.there_is_a_blocker_entity_in(col + 1, row):
                col += 1
        if direction == Direction.LEFT:
            while not self.there_is_a_blocker_entity_in(col - 1, row):
                col -= 1
        if direction == Direction.UP:
            while not self.there_is_a_blocker_entity_in(col, row + 1):
                row += 1
        if direction == Direction.DOWN:
            while not self.there_is_a_blocker_entity_in(col, row - 1):
                row -= 1
        self.move_entity(entity, col, row)
        return orig_loc

    def draw(self, win):
        pygame.draw.rect(win, LIGHT_BLUE, (0, 0, self.columns * SQUARE_SIZE, self.rows * SQUARE_SIZE))
        for row in range(self.rows):
            for col in range(self.columns):
                pygame.draw.rect(win, BLACK, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
        for e in self.entities:
            e.draw(win)

    def get_all_entities_of_class(self, entity_class: EntityClass):
        return [e for e in self.entities if e.entity_class == entity_class]
