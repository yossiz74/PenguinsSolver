from collections import Counter
from enum import Enum, auto
from dataclasses import dataclass

from direction import Direction


class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y})'

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)


class EntityType(Enum):
    PENGUIN = auto()
    BEAR1 = auto()
    BEAR2 = auto()
    BEAR3 = auto()
    BEAR4 = auto()
    BEAR5 = auto()
    WATER = auto()


@dataclass
class Entity:
    entity_type: EntityType
    location: Point


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.entities = dict()  # map entity type to its location

    def __eq__(self, other):
        answer = (self.width == other.width and self.height == other.height)
        for x in range(self.width):
            for y in range(self.height):
                my_entities = self.get_entities_in_location(x, y)
                other_entities = other.get_entities_in_location(x, y)
                if Counter(my_entities) != Counter(other_entities):
                    return False
        return answer

    def __repr__(self):
        s = ""
        for y in range(self.height, 0, -1):
            for x in range(self.width):
                s += "|"
                entities = self.get_entities_in_location(x, y - 1)
                if entities:
                    for e in entities:
                        s += e.name[0]
                else:
                    s += "*"
                s += "|"
            s += "\n"
        return s

    def place_entity(self, entity_type: EntityType, x: int, y: int):
        self.entities[entity_type] = Point(x, y)

    def get_entity_location(self, entity_type: EntityType) -> Point:
        for et in self.entities.keys():
            if et == entity_type:
                return self.entities[et]

    def point_is_inside_the_board(self, x, y) -> bool:
        return (self.width > x >= 0) and (self.height > y >= 0)

    def there_is_a_blocker_entity_in(self, x, y) -> bool:
        entities = self.get_entities_in_location(x, y)
        return any([e != EntityType.WATER for e in entities])

    def get_entities_in_location(self, x, y) -> list[EntityType]:
        answer = []
        for et in self.entities.keys():
            entity_location = self.entities[et]
            if entity_location.x == x and entity_location.y == y:
                answer.append(et)
        return answer

    def apply_move(self, entity_type, direction):
        if direction == Direction.RIGHT:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.x + 1, p.y):
                p.x += 1
                if not self.point_is_inside_the_board(p.x, p.y):
                    raise ValueError(f"{entity_type} went overboard")
            self.place_entity(entity_type, p.x, p.y)
        if direction == Direction.LEFT:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.x - 1, p.y):
                p.x -= 1
                if not self.point_is_inside_the_board(p.x, p.y):
                    raise ValueError(f"{entity_type} went overboard")
            self.place_entity(entity_type, p.x, p.y)
        if direction == Direction.UP:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.x, p.y + 1):
                p.y += 1
                if not self.point_is_inside_the_board(p.x, p.y):
                    raise ValueError(f"{entity_type} went overboard")
            self.place_entity(entity_type, p.x, p.y)
        if direction == Direction.DOWN:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.x, p.y - 1):
                p.y -= 1
                if not self.point_is_inside_the_board(p.x, p.y):
                    raise ValueError(f"{entity_type} went overboard")
            self.place_entity(entity_type, p.x, p.y)
