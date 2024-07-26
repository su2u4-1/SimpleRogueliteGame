from typing import Any


class Entity:
    def __init__(self, id, x, y, attr: dict[str, Any] = {}):
        self.id = id
        self.x = x
        self.y = y
        self.attr = attr
