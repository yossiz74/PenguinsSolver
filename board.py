from enum import Enum, auto
from dataclasses import dataclass


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
        self.entities = []

    def place_entity(self, entity_type: EntityType, x: int, y: int):
        entity = Entity(entity_type=entity_type, location=Point(x, y))
        self.entities.append(entity)

    def get_entity_location(self, entity_type: EntityType) -> Point:
        for entity in self.entities:
            if entity.entity_type == entity_type:
                return entity.location

    def point_is_inside_the_board(self, x, y) -> bool:
        return (self.width > x >= 0) and (self.height > y >= 0)

    def there_is_a_blocker_entity_in(self, x, y) -> bool:
        e = self._get_entity_in(x, y)
        return e and e.entity_type in [EntityType.PENGUIN, EntityType.BEAR1, EntityType.BEAR2, EntityType.BEAR3, EntityType.BEAR4]

    def _get_entity_in(self, x, y):
        for entity in self.entities:
            if entity.location.x == x and entity.location.y == y:
                return entity
        return None
