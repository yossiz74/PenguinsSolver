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
        self.bear = Point(-1, -1)
        self.width = width
        self.height = height

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

    def place_bear(self, x: int, y: int):
        self.bear.x = x
        self.bear.y = y

    def point_is_inside_the_board(self, x, y) -> bool:
        return (self.width > x >= 0) and (self.height > y >= 0)

    def there_is_a_bear_in(self, x, y) -> bool:
        return (x == self.bear.x) and (y == self.bear.y)
