import os.path
from time import sleep
from keyboard import read_key
from GameManager import GameManager

def main(game: GameManager) -> None:
    game.update()
    game.show()
    while True:
        key = read_key()
        player = game.entity["player"]
        if key == "w" and game.maze[player.y-1][player.x] == "road" and game.screen[player.y-1][player.x] == "null":
            player.y -= 1
        elif key == "a" and game.maze[player.y][player.x-1] == "road" and game.screen[player.y][player.x-1] == "null":
            player.x -= 1
        elif key == "s" and game.maze[player.y+1][player.x] == "road" and game.screen[player.y+1][player.x] == "null":
            player.y += 1
        elif key == "d" and game.maze[player.y][player.x+1] == "road" and game.screen[player.y][player.x+1] == "null":
            player.x += 1
        elif key == "esc":
            return
        game.update()
        game.show()
        sleep(game.fps)

if __name__ == "__main__":
    root = os.path.abspath(".")
    if root.endswith("\\source"):
        root = root[:-7]
    game = GameManager(os.path.join(root, "data", f"config.json5"))
    game.create_maze(game.maze_w, game.maze_h)
    game.summon_entity(game.maze_w * game.maze_h)
    main(game)