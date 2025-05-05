import os.path
from time import sleep
from keyboard import read_key
from GameManager import GameManager
from Entity import Entity


DX, DY = [1, 0, -1, 0], [0, 1, 0, -1]


def find_path(start: tuple[int, int], end: tuple[int, int], map: list[list[str]]) -> list[tuple[int, int]]:
    f = [[j != "road" for j in i] for i in map]
    a = [start]
    p = {start: (-1, -1)}
    f[start[1]][start[0]] = False
    f[end[1]][end[0]] = False
    while True:
        if len(a) == 0:
            if len(p) == 0:
                return []
            end = min(p.keys(), key=lambda x: (x[0] - end[0]) ** 2 + (x[1] - end[1]) ** 2)
            return find_path(start, end, map)
        i = a.pop(0)
        if i == end:
            break
        if f[i[1]][i[0]]:
            continue
        f[i[1]][i[0]] = True
        for d in range(4):
            x, y = i[0] + DX[d], i[1] + DY[d]
            if 0 <= x < len(map[0]) and 0 <= y < len(map) and not f[y][x]:
                p[(x, y)] = i
                a.append((x, y))
    path: list[tuple[int, int]] = []
    while i != (-1, -1):
        path.append(i)
        i = p[i]
    return path[:-1]


def move(v: Entity, player: Entity) -> None:
    game.update()
    m: list[list[str]] = []
    for i in range(6):
        t: list[str] = []
        for j in range(12):
            t1 = game.screen[player.room[1] * 6 + i][player.room[0] * 12 + j]
            if t1 == "null":
                t1 = game.maze[player.room[1] * 6 + i][player.room[0] * 12 + j]
            t.append(t1)
        m.append(t)
    path = find_path((v.x % 12, v.y % 6), (player.x % 12, player.y % 6), m)
    if len(path) == 0:
        return
    x, y = path[-1]
    x += v.room[0] * 12
    y += v.room[1] * 6
    if game.maze[y][x] == "road" and game.screen[y][x] == "null":
        v.x, v.y = x, y


def main(game: GameManager) -> None:
    game.show()
    cc = None
    cc_count = 0
    key = "null"
    while True:
        key = read_key()
        if key == cc:
            cc_count += 1
        else:
            cc = key
            cc_count = 0
        player = game.entity["player"]
        if key == "w" and game.maze[player.y - 1][player.x] == "road" and game.screen[player.y - 1][player.x] == "null":
            player.y -= 1
        elif key == "a" and game.maze[player.y][player.x - 1] == "road" and game.screen[player.y][player.x - 1] == "null":
            player.x -= 1
        elif key == "s" and game.maze[player.y + 1][player.x] == "road" and game.screen[player.y + 1][player.x] == "null":
            player.y += 1
        elif key == "d" and game.maze[player.y][player.x + 1] == "road" and game.screen[player.y][player.x + 1] == "null":
            player.x += 1
        elif key == "esc":
            return
        for i in game.entity.values():
            game.update()
            if i.id.startswith("enemy_") and i.room == player.room:
                move(i, player)
        game.show()
        if cc_count >= 5:
            sleep(game.speed / 2)
        else:
            sleep(game.speed)


if __name__ == "__main__":
    root = os.path.abspath(".")
    if root.endswith("\\source"):
        root = root[:-7]
    game = GameManager(os.path.join(root, "data", f"config.json"))
    game.create_maze(game.maze_w, game.maze_h)
    game.summon_entity(game.maze_w * game.maze_h)
    main(game)
