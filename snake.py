import curses
import random
import time


def setup_screen() -> curses.window:
    screen = curses.initscr()
    curses.curs_set(0)
    screen.keypad(True)
    screen.nodelay(True)
    screen.timeout(100)
    curses.start_color()
    curses.use_default_colors()
    return screen


def place_food(height: int, width: int, snake: list[tuple[int, int]]) -> tuple[int, int]:
    while True:
        food = (random.randint(1, height - 2), random.randint(1, width - 2))
        if food not in snake:
            return food


def run_game(screen: curses.window) -> int:
    height, width = screen.getmaxyx()
    snake = [(height // 2, width // 2 + 1), (height // 2, width // 2)]
    direction = curses.KEY_RIGHT
    score = 0
    food = place_food(height, width, snake)

    while True:
        screen.clear()
        screen.border()
        screen.addstr(0, 2, f" Score: {score} ")
        screen.addch(food[0], food[1], "*")
        for segment in snake:
            screen.addch(segment[0], segment[1], "#")

        key = screen.getch()
        if key in (curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT):
            opposite = {
                curses.KEY_UP: curses.KEY_DOWN,
                curses.KEY_DOWN: curses.KEY_UP,
                curses.KEY_LEFT: curses.KEY_RIGHT,
                curses.KEY_RIGHT: curses.KEY_LEFT,
            }
            if key != opposite[direction]:
                direction = key
        elif key in (ord("q"), ord("Q")):
            break

        head_y, head_x = snake[0]
        if direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1

        new_head = (head_y, head_x)
        if new_head in snake or head_y in (0, height - 1) or head_x in (0, width - 1):
            break

        snake.insert(0, new_head)
        if new_head == food:
            score += 1
            food = place_food(height, width, snake)
        else:
            snake.pop()

        time.sleep(0.05)

    return score


def main() -> None:
    screen = setup_screen()
    try:
        score = run_game(screen)
    finally:
        curses.endwin()

    print(f"Game over! Final score: {score}")


if __name__ == "__main__":
    main()
