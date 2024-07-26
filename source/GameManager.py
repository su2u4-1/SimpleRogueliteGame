from os import system
from random import randrange
import json5
from Entity import Entity

DX, DY = [1, 0, -1, 0], [0, 1, 0, -1]


class GameManager:
    def __init__(self, config_file_path: str) -> None:
        with open(config_file_path, "r") as f:
            config: dict[str, int | dict[str, str]] = json5.load(f)
        self.w = config["w"]
        self.h = config["h"]
        self.fps = config["fps"]
        self.symbol: dict[str, str] = config["symbol"]
        self.maze_w = (self.w + 5) // 12
        self.maze_h = (self.h + 1) // 6
        self.screen = [["null" for _ in range(self.w)] for _ in range(self.h)]
        self.maze = [["null" for _ in range(self.w)] for _ in range(self.h)]
        self.entity: dict[str, Entity] = {}

    def create_maze(self, w: int, h: int) -> None:
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
            tx = t[0] + t[2]
            ty = t[1] + t[3]
            if f[tx][ty]:
                f[tx][ty] = False
                if t[3] == 1:
                    maze[tx][ty] += 4
                    maze[t[0]][t[1]] += 1
                elif t[2] == -1:
                    maze[tx][ty] += 8
                    maze[t[0]][t[1]] += 2
                if t[3] == -1:
                    maze[tx][ty] += 1
                    maze[t[0]][t[1]] += 4
                elif t[2] == 1:
                    maze[tx][ty] += 2
                    maze[t[0]][t[1]] += 8
                for i in range(4):
                    if 0 <= tx + DX[i] < h and 0 <= ty + DY[i] < w and f[tx + DX[i]][ty + DY[i]]:
                        a.append((tx, ty, DX[i], DY[i]))

        for i in range(len(maze)):
            for j in range(len(maze[i])):
                self.maze[i * 6][j * 12] = "wall_tl"
                self.maze[i * 6 + 4][j * 12] = "wall_dl"
                self.maze[i * 6][j * 12 + 6] = "wall_tr"
                self.maze[i * 6 + 4][j * 12 + 6] = "wall_dr"
                self.maze[i * 6][j * 12 + 1] = "wall_ho"
                self.maze[i * 6][j * 12 + 5] = "wall_ho"
                self.maze[i * 6 + 4][j * 12 + 1] = "wall_ho"
                self.maze[i * 6 + 4][j * 12 + 5] = "wall_ho"
                for x in range(1, 4):
                    for y in range(1, 6):
                        self.maze[i * 6 + x][j * 12 + y] = "road"
                if maze[i][j] >= 8:
                    maze[i][j] -= 8
                    self.maze[i * 6 + 4][j * 12 + 2] = "wall_tr"
                    self.maze[i * 6 + 4][j * 12 + 3] = "road"
                    self.maze[i * 6 + 4][j * 12 + 4] = "wall_tl"
                    self.maze[i * 6 + 5][j * 12 + 2] = "wall_st"
                    self.maze[i * 6 + 5][j * 12 + 3] = "road"
                    self.maze[i * 6 + 5][j * 12 + 4] = "wall_st"
                else:
                    self.maze[i * 6 + 4][j * 12 + 2] = "wall_ho"
                    self.maze[i * 6 + 4][j * 12 + 3] = "wall_ho"
                    self.maze[i * 6 + 4][j * 12 + 4] = "wall_ho"
                if maze[i][j] >= 4:
                    maze[i][j] -= 4
                    self.maze[i * 6 + 1][j * 12] = "wall_dr"
                    self.maze[i * 6 + 2][j * 12] = "road"
                    self.maze[i * 6 + 3][j * 12] = "wall_tr"
                else:
                    self.maze[i * 6 + 1][j * 12] = "wall_st"
                    self.maze[i * 6 + 2][j * 12] = "wall_st"
                    self.maze[i * 6 + 3][j * 12] = "wall_st"
                if maze[i][j] >= 2:
                    maze[i][j] -= 2
                    self.maze[i * 6][j * 12 + 2] = "wall_dr"
                    self.maze[i * 6][j * 12 + 3] = "road"
                    self.maze[i * 6][j * 12 + 4] = "wall_dl"
                else:
                    self.maze[i * 6][j * 12 + 2] = "wall_ho"
                    self.maze[i * 6][j * 12 + 3] = "wall_ho"
                    self.maze[i * 6][j * 12 + 4] = "wall_ho"
                if maze[i][j] >= 1:
                    maze[i][j] -= 1
                    self.maze[i * 6 + 1][j * 12 + 6] = "wall_dl"
                    self.maze[i * 6 + 2][j * 12 + 6] = "road"
                    self.maze[i * 6 + 3][j * 12 + 6] = "wall_tl"
                    for x in range(7, 12):
                        self.maze[i * 6 + 1][j * 12 + x] = "wall_ho"
                        self.maze[i * 6 + 2][j * 12 + x] = "road"
                        self.maze[i * 6 + 3][j * 12 + x] = "wall_ho"
                else:
                    self.maze[i * 6 + 1][j * 12 + 6] = "wall_st"
                    self.maze[i * 6 + 2][j * 12 + 6] = "wall_st"
                    self.maze[i * 6 + 3][j * 12 + 6] = "wall_st"

    def show(self) -> None:
        self.update()
        system("cls")
        for i in range(self.h):
            for j in range(self.w):
                if self.screen[i][j] == "null":
                    print(self.symbol[self.maze[i][j]], end="")
                else:
                    print(self.symbol[self.screen[i][j]], end="")
            print()

    def summon_entity(self, enemy_number: int):
        self.entity["player"] = Entity("player", 3, 2)
        for i in range(enemy_number):
            while True:
                tx, ty = randrange(0, self.maze_w), randrange(0, self.maze_h)
                if tx > 0 or ty > 0:
                    x, y = randrange(tx * 12 + 1, tx * 12 + 6), randrange(ty * 6 + 1, ty * 6 + 4)
                    if self.maze[y][x] == "road" and self.screen[y][x] == "null":
                        break
            size = randrange(0, 3)
            if size == 0:
                self.entity[f"enemy_{i}"] = Entity("enemy_s", x, y, (tx, ty))
            elif size == 1:
                self.entity[f"enemy_{i}"] = Entity("enemy_m", x, y, (tx, ty))
            elif size == 2:
                self.entity[f"enemy_{i}"] = Entity("enemy_l", x, y, (tx, ty))

    def update(self) -> None:
        self.screen = [["null" for _ in range(self.w)] for _ in range(self.h)]
        for i in self.entity.values():
            tx, mx = divmod(i.x, 12)
            ty, my = divmod(i.y, 6)
            if mx < 6 and my < 4:
                i.room = (tx, ty)
            else:
                i.room = (-1, -1)
            self.screen[i.y][i.x] = i.id
