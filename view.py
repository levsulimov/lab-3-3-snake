import tkinter as tk

import config as cfg
from models import SnakeGame


class App:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Змейка • Сулимов Л. И. • ПИ25-2")
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=cfg.WIDTH,
                                height=cfg.HEIGHT, bg=cfg.BG,
                                highlightthickness=0)
        self.canvas.pack()
        self.game = SnakeGame()
        self.best = 0
        self.root.bind("<KeyPress>", self.on_key)
        self.root.bind("<FocusOut>", self.on_focus_out)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.focus_set()
        self.tick()

    def run(self):
        self.root.mainloop()

    def on_focus_out(self, event):
        if self.game.state == "running":
            self.game.toggle_pause()
            self.draw()

    def on_click(self, event):
        if (self.game.state in ("menu", "over", "won")
                and 100 <= event.x <= cfg.WIDTH - 100
                and 240 <= event.y <= 430):
            self.game.reset()
            self.draw()

    def on_key(self, event):
        key = event.keysym.lower()
        directions = {"up": (0, -1), "w": (0, -1),
                      "down": (0, 1), "s": (0, 1),
                      "left": (-1, 0), "a": (-1, 0),
                      "right": (1, 0), "d": (1, 0)}
        if key in directions:
            self.game.turn(directions[key])
        elif key == "space":
            self.game.toggle_pause()
        elif key == "r" or (key == "return" and self.game.state
                            in ("menu", "over", "won")):
            self.game.reset()
        elif key == "escape":
            self.root.destroy()
            return
        self.draw()

    def tick(self):
        self.game.step()
        self.best = max(self.best, self.game.score)
        self.draw()
        delay = max(cfg.MIN_DELAY,
                    cfg.START_DELAY - self.game.score * cfg.SPEED_STEP)
        self.root.after(delay, self.tick)

    def text(self, x, y, value, size=12, color=cfg.TEXT, anchor="center"):
        self.canvas.create_text(x, y, text=value, fill=color,
                                font=("Segoe UI", size), anchor=anchor)

    def draw(self):
        c = self.canvas
        c.delete("all")
        c.create_rectangle(0, 0, cfg.WIDTH, cfg.HUD,
                           fill=cfg.PANEL, outline="")
        self.text(24, 25, "ЛАБОРАТОРНАЯ 3.3  /  ПИ25-2", 10,
                  cfg.MUTED, "w")
        self.text(24, 58, "ЗМЕЙКА", 25, cfg.GREEN, "w")
        self.text(cfg.WIDTH - 155, 28, "СЧЁТ / РЕКОРД СЕАНСА", 10,
                  cfg.MUTED)
        self.text(cfg.WIDTH - 155, 60,
                  f"{self.game.score:02d}   /   {self.best:02d}", 23)
        for x in range(cfg.COLS + 1):
            c.create_line(x * cfg.CELL, cfg.HUD, x * cfg.CELL,
                          cfg.HUD + cfg.ROWS * cfg.CELL, fill=cfg.GRID)
        for y in range(cfg.ROWS + 1):
            py = cfg.HUD + y * cfg.CELL
            c.create_line(0, py, cfg.WIDTH, py, fill=cfg.GRID)
        if self.game.food:
            x, y = self.game.food
            px, py = x * cfg.CELL, cfg.HUD + y * cfg.CELL
            c.create_oval(px + 5, py + 5, px + cfg.CELL - 5,
                          py + cfg.CELL - 5, fill=cfg.FOOD, outline="")
        for index, (x, y) in enumerate(self.game.body):
            px, py = x * cfg.CELL, cfg.HUD + y * cfg.CELL
            color = cfg.GREEN if index == 0 else "#38af89"
            c.create_rectangle(px + 2, py + 2, px + cfg.CELL - 2,
                               py + cfg.CELL - 2, fill=color, outline="")
            if index == 0:
                dx, dy = self.game.direction
                for side in (-1, 1):
                    ex = px + cfg.CELL / 2 + dx * 5 - dy * side * 5
                    ey = py + cfg.CELL / 2 + dy * 5 + dx * side * 5
                    c.create_oval(ex - 2, ey - 2, ex + 2, ey + 2,
                                  fill=cfg.BG, outline="")
        self.text(cfg.WIDTH / 2, cfg.HEIGHT - 23,
                  "↑ ↓ ← → / WASD — движение    Пробел — пауза    R — заново",
                  11, cfg.MUTED)
        titles = {"menu": "ЗМЕЙКА", "paused": "ПАУЗА",
                  "over": "ИГРА ОКОНЧЕНА", "won": "ПОЛЕ ЗАПОЛНЕНО!"}
        if self.game.state in titles:
            c.create_rectangle(100, 240, cfg.WIDTH - 100, 430,
                               fill=cfg.PANEL, outline=cfg.GREEN, width=2)
            self.text(cfg.WIDTH / 2, 285, titles[self.game.state], 26,
                      cfg.GREEN)
            subtitle = ("Пробел — продолжить" if self.game.state == "paused"
                        else "Enter или щелчок здесь — начать")
            self.text(cfg.WIDTH / 2, 335, subtitle, 14)
            self.text(cfg.WIDTH / 2, 385,
                      "Сулимов Лев Игоревич  •  ПИ25-2", 11, cfg.MUTED)
