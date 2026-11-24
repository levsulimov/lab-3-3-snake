"""Проверки обработчиков интерфейса; необходим графический сеанс."""

from types import SimpleNamespace
import unittest

from main import prepare_tk
from view import App


class InterfaceTests(unittest.TestCase):
    """Проверить запуск, паузу и рисование реального Canvas."""

    @classmethod
    def setUpClass(cls):
        """Подготовить Tcl/Tk из установленного Python."""
        prepare_tk()

    def setUp(self):
        """Создать скрытое окно для каждого сценария."""
        self.app = App()
        self.app.root.withdraw()

    def tearDown(self):
        """Закрыть окно и его таймеры."""
        self.app.root.destroy()

    def test_start_pause_and_restart(self):
        """Enter запускает, пробел ставит паузу, R сбрасывает счёт."""
        self.app.on_key(SimpleNamespace(keysym="Return"))
        self.assertEqual(self.app.game.state, "running")
        self.app.on_key(SimpleNamespace(keysym="space"))
        self.assertEqual(self.app.game.state, "paused")
        self.app.game.score = 5
        self.app.on_key(SimpleNamespace(keysym="r"))
        self.assertEqual(self.app.game.score, 0)
        self.assertGreater(len(self.app.canvas.find_all()), 20)

    def test_losing_focus_pauses(self):
        """Потеря фокуса защищает от движения без управления."""
        self.app.game.reset()
        self.app.on_focus_out(None)
        self.assertEqual(self.app.game.state, "paused")

    def test_menu_click_bounds(self):
        """Щелчок вне панели не начинает игру."""
        self.app.on_click(SimpleNamespace(x=10, y=10))
        self.assertEqual(self.app.game.state, "menu")
        self.app.on_click(SimpleNamespace(x=200, y=300))
        self.assertEqual(self.app.game.state, "running")


if __name__ == "__main__":
    unittest.main()
