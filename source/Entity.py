from typing import Any


class Entity:
    def __init__(self, id: str, x: int, y: int, room: tuple[int, int] = (-1, -1), attr: dict[str, Any] = {}):
        self.id = id
        self.x = x
        self.y = y
        self.room = room
        self.attr = attr
