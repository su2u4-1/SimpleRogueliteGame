import os.path
from time import sleep
from keyboard import read_key
from GameManager import GameManager
from Entity import Entity


def find_path(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    pass


def move(v: Entity, player: Entity) -> None:
    path = find_path((v.x, v.y), (player.x, player.y))


def main(game: GameManager) -> None:
    game.update_screen()
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
        tx, mx = divmod(player.x, 12)
        ty, my = divmod(player.y, 6)
        if mx < 6 and my < 4:
            player.attr["room"] = (tx, ty)
        for i in game.entity.values():
            if i.attr["room"] == player.attr["room"]:
                move(i, player)
        game.update_screen()
        game.show()
        if cc_count >= 5:
            sleep(game.fps / 2)
        else:
            sleep(game.fps)


if __name__ == "__main__":
    root = os.path.abspath(".")
    if root.endswith("\\source"):
        root = root[:-7]
    game = GameManager(os.path.join(root, "data", f"config.json5"))
    game.create_maze(game.maze_w, game.maze_h)
    game.summon_entity(game.maze_w * game.maze_h)
    main(game)
