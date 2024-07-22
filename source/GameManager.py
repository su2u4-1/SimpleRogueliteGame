from random import randrange
import json5


def CreateMaze(w: int, h: int) -> list[list[int]]:
    """
    0       1       2       4       8
    ╔═════╗ ╔═════╗ ╔═╝.╚═╗ ╔═════╗ ╔═════╗
    ║.....║ ║.....╚ ║.....║ ╝.....║ ║.....║
    ║.....║ ║...... ║.....║ ......║ ║.....║
    ║.....║ ║.....╔ ║.....║ ╗.....║ ║.....║
    ╚═════╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚═╗.╔═╝
    """
    DX, DY = [1, 0, -1, 0], [0, 1, 0, -1]
    maze = [[0 for _ in range(w)] for _ in range(h)]
    f = [[True for _ in range(w)] for _ in range(h)]
    a = [(0, 0, 0, 1), (0, 0, 1, 0)]
    f[0][0] = False
    while True:
        for i in f:
            if True in i:
                break
        else:
            break
        t = a.pop(randrange(0, len(a)))
        if f[t[0] + t[2]][t[1] + t[3]]:
            f[t[0] + t[2]][t[1] + t[3]] = False
            s = 0
            if t[2] == 1:
                s += 1
                maze[t[0]][t[1]] += 4
            elif t[2] == -1:
                s += 4
                maze[t[0]][t[1]] += 1
            if t[3] == 1:
                s += 8
                maze[t[0]][t[1]] += 2
            elif t[3] == -1:
                s += 2
                maze[t[0]][t[1]] += 8
            maze[t[0] + t[2]][t[1] + t[3]] += s
            for i in range(4):
                a.append((t[0] + t[2] + DX[i]))
    return maze


class GameManager:
    def __init__(self, config_file_path: str) -> None:
        with open(config_file_path, "r") as f:
            config: dict[str, int | dict[str, str]] = json5.load(f)
        self.w: int = config["w"]
        self.h: int = config["h"]
        self.symbol: dict[str, str] = config["symbol"]
        self.screen = [["null" for _ in range(self.w)] for _ in range(self.h)]
        maze = CreateMaze(10, 5)
