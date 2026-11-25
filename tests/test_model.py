import random
import unittest

from models import SnakeGame


class SnakeTests(unittest.TestCase):

    def setUp(self):
        self.game = SnakeGame(6, 4, random.Random(7))
        self.game.reset()

    def test_food_never_on_body(self):
        for _ in range(50):
            self.game.place_food()
            self.assertNotIn(self.game.food, self.game.body)

    def test_eating_grows_and_scores(self):
        self.game.food = (4, 2)
        self.game.step()
        self.assertEqual(len(self.game.body), 4)
        self.assertEqual(self.game.score, 1)
        self.assertNotIn(self.game.food, self.game.body)

    def test_reverse_and_double_turn_are_rejected(self):
        self.game.turn((-1, 0))
        self.assertEqual(self.game.next_direction, (1, 0))
        self.game.turn((0, -1))
        self.game.turn((-1, 0))
        self.game.step()
        self.assertEqual(self.game.body[0], (3, 1))

    def test_wall_collision(self):
        self.game.food = (0, 0)
        for _ in range(3):
            self.game.step()
        self.assertEqual(self.game.state, "over")

    def test_body_collision(self):
        self.game.body = [(2, 2), (2, 1), (3, 1), (3, 2), (4, 2)]
        self.game.food = (0, 0)
        self.game.step()
        self.assertEqual(self.game.state, "over")

    def test_tail_cell_is_available(self):
        self.game.body = [(2, 2), (2, 1), (3, 1), (3, 2)]
        self.game.food = (0, 0)
        self.game.step()
        self.assertEqual(self.game.state, "running")
        self.assertEqual(self.game.body[0], (3, 2))

    def test_pause_freezes_model(self):
        before = self.game.body[:]
        self.game.toggle_pause()
        self.game.step()
        self.assertEqual(self.game.body, before)
        self.game.toggle_pause()
        self.assertEqual(self.game.state, "running")

    def test_full_board_wins(self):
        self.game.body = [(4, 3)] + [
            (x, y) for y in range(4) for x in range(6)
            if (x, y) not in ((4, 3), (5, 3))
        ]
        self.game.food = (5, 3)
        self.game.step()
        self.assertEqual(self.game.state, "won")
        self.assertIsNone(self.game.food)
        self.assertEqual(len(self.game.body), 24)

    def test_reset_clears_previous_game(self):
        self.game.score = 9
        self.game.state = "over"
        self.game.reset()
        self.assertEqual(self.game.score, 0)
        self.assertEqual(len(self.game.body), 3)
        self.assertEqual(self.game.state, "running")


if __name__ == "__main__":
    unittest.main()
