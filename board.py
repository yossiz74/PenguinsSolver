from collections import Counter
from enum import Enum, auto
# from dataclasses import dataclass

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


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.entities = dict()  # map entity type to its location

    def __eq__(self, other):
        answer = (self.width == other.width and self.height == other.height)
        for x in range(self.width):
            for y in range(self.height):
                my_entities = [get_entity_class(e) for e in self.get_entities_in_location(x, y)]
                other_entities = [get_entity_class(e) for e in other.get_entities_in_location(x, y)]
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
                        s += e.name[0] + e.name[-1]
                else:
                    s += "  "
                s += "|"
            s += "\n"
        return s

    def add_new_entity(self, entity_type: EntityType, x: int, y: int):
        if entity_type in self.entities.keys():
            raise KeyError(f"Trying to add an already existing entity {entity_type}")
        self.entities[entity_type] = Point(x, y)

    def move_entity(self, entity_type: EntityType, x: int, y: int):
        if entity_type not in self.entities.keys():
            raise KeyError(f"Trying to move a non-existing entity {entity_type}")
        self.entities[entity_type] = Point(x, y)
        # if a penguin reaches the water, it dives into it
        if get_entity_class(entity_type) == EntityClass.PENGUIN:
            if any([get_entity_class(e) == EntityClass.WATER for e in self.get_entities_in_location(x, y)]):
                self.entities.pop(entity_type)

    def get_entity_location(self, entity_type: EntityType) -> Point:
        for et in self.entities.keys():
            if et == entity_type:
                return self.entities[et]

    def point_is_inside_the_board(self, x, y) -> bool:
        return (self.width > x >= 0) and (self.height > y >= 0)

    def there_is_a_blocker_entity_in(self, x, y) -> bool:
        entities = self.get_entities_in_location(x, y)
        return any([get_entity_class(e) in [EntityClass.PENGUIN, EntityClass.BEAR] for e in entities])

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
            self.move_entity(entity_type, p.x, p.y)
        if direction == Direction.LEFT:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.x - 1, p.y):
                p.x -= 1
                if not self.point_is_inside_the_board(p.x, p.y):
                    raise ValueError(f"{entity_type} went overboard")
            self.move_entity(entity_type, p.x, p.y)
        if direction == Direction.UP:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.x, p.y + 1):
                p.y += 1
                if not self.point_is_inside_the_board(p.x, p.y):
                    raise ValueError(f"{entity_type} went overboard")
            self.move_entity(entity_type, p.x, p.y)
        if direction == Direction.DOWN:
            p = self.get_entity_location(entity_type)
            while not self.there_is_a_blocker_entity_in(p.x, p.y - 1):
                p.y -= 1
                if not self.point_is_inside_the_board(p.x, p.y):
                    raise ValueError(f"{entity_type} went overboard")
            self.move_entity(entity_type, p.x, p.y)
