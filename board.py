class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point(x={self.x}, y={self.y})'

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)


class Board:
    def __init__(self, width: int, height: int):
        self.penguin = Point(-1, -1)
        self.water = Point(-1, -1)

    def place_penguin(self, x: int, y: int):
        self.penguin.x = x
        self.penguin.y = y

    def place_water(self, x: int, y: int):
        self.water.x = x
        self.water.y = y

    def get_penguin_location(self) -> Point:
        return self.penguin

    def get_water_location(self) -> Point:
        return self.water
