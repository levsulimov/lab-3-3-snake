import random

from config import COLS, ROWS


class SnakeGame:

    def __init__(self, cols=COLS, rows=ROWS, rng=None):
        if cols < 6 or rows < 4:
            raise ValueError("Минимальное поле: 6 × 4")
        self.cols = cols
        self.rows = rows
        self.rng = rng if rng is not None else random.Random()
        self.reset()
        self.state = "menu"

    def reset(self):
        x, y = self.cols // 2, self.rows // 2
        self.body = [(x, y), (x - 1, y), (x - 2, y)]
        self.direction = (1, 0)
        self.next_direction = self.direction
        self.turn_queued = False
        self.score = 0
        self.state = "running"
        self.place_food()

    def place_food(self):
        occupied = set(self.body)
        free = [(x, y) for y in range(self.rows)
                for x in range(self.cols) if (x, y) not in occupied]
        self.food = self.rng.choice(free) if free else None
        if not free:
            self.state = "won"

    def turn(self, direction):
        if self.state != "running" or self.turn_queued:
            return
        if direction not in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            return
        reverse = (-self.direction[0], -self.direction[1])
        if direction != reverse and direction != self.direction:
            self.next_direction = direction
            self.turn_queued = True

    def toggle_pause(self):
        if self.state in ("running", "paused"):
            self.state = "paused" if self.state == "running" else "running"

    def step(self):
        if self.state != "running":
            return
        self.direction = self.next_direction
        self.turn_queued = False
        x, y = self.body[0]
        dx, dy = self.direction
        head = (x + dx, y + dy)
        growing = head == self.food
        obstacle = self.body if growing else self.body[:-1]
        if not (0 <= head[0] < self.cols and 0 <= head[1] < self.rows):
            self.state = "over"
            return
        if head in obstacle:
            self.state = "over"
            return
        self.body.insert(0, head)
        if growing:
            self.score += 1
            self.place_food()
        else:
            self.body.pop()
