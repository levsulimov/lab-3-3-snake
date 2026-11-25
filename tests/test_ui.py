from types import SimpleNamespace
import unittest

from main import prepare_tk
from view import App


class InterfaceTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        prepare_tk()

    def setUp(self):
        self.app = App()
        self.app.root.withdraw()

    def tearDown(self):
        self.app.root.destroy()

    def test_start_pause_and_restart(self):
        self.app.on_key(SimpleNamespace(keysym="Return"))
        self.assertEqual(self.app.game.state, "running")
        self.app.on_key(SimpleNamespace(keysym="space"))
        self.assertEqual(self.app.game.state, "paused")
        self.app.game.score = 5
        self.app.on_key(SimpleNamespace(keysym="r"))
        self.assertEqual(self.app.game.score, 0)
        self.assertGreater(len(self.app.canvas.find_all()), 20)

    def test_losing_focus_pauses(self):
        self.app.game.reset()
        self.app.on_focus_out(None)
        self.assertEqual(self.app.game.state, "paused")

    def test_menu_click_bounds(self):
        self.app.on_click(SimpleNamespace(x=10, y=10))
        self.assertEqual(self.app.game.state, "menu")
        self.app.on_click(SimpleNamespace(x=200, y=300))
        self.assertEqual(self.app.game.state, "running")


if __name__ == "__main__":
    unittest.main()
