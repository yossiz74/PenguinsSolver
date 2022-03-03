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

    def place_entity(self, entity_type: EntityType, x: int, y: int):
        self.entities[entity_type] = Point(x, y)

    def get_entity_location(self, entity_type: EntityType) -> Point:
        for et in self.entities.keys():
            if et == entity_type:
                return self.entities[et]

    def point_is_inside_the_board(self, x, y) -> bool:
        return (self.width > x >= 0) and (self.height > y >= 0)

    def there_is_a_blocker_entity_in(self, x, y) -> bool:
        e = self._get_entity_in(x, y)
        return e and e.entity_type != EntityType.WATER

    def _get_entity_in(self, x, y):
        for et in self.entities.keys():
            entity_location = self.entities[et]
            if entity_location.x == x and entity_location.y == y:
                return Entity(entity_type=et, location=entity_location)
        return None

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
