import unittest
from src import clicker

def back_to_default():
    clicker.SCORE = 0
    clicker.BOOSTER = 1
    clicker.AUTO_CLICKS = 0

class SimpleUpgradeTest(unittest.TestCase):
    upgrade_button1 = clicker.Upgrade((200, 200), "text", 100, 100, (100, 100))

    def test_click(self):
        self.upgrade_button1.click()
        self.assertEqual(clicker.SCORE, 0)
        self.assertEqual(clicker.BOOSTER, 1)
        clicker.SCORE = 100
        clicker.BOOSTER = 0
        self.upgrade_button1.click()
        self.assertEqual(clicker.SCORE, 0)
        self.assertEqual(clicker.BOOSTER, 100)
        back_to_default()

    upgrade_button2 = clicker.Upgrade((200, 200), "text", 200, 200, (100, 100))

    def test_auto_click(self):
        self.upgrade_button2.auto_clicker()
        self.assertEqual(clicker.SCORE, 0)
        self.assertEqual(clicker.AUTO_CLICKS, 0)
        clicker.SCORE = 200
        self.upgrade_button2.auto_clicker()
        self.assertEqual(clicker.SCORE, 0)
        self.assertEqual(clicker.AUTO_CLICKS, 200)
        back_to_default()

    upgrade_button3 = clicker.Upgrade((200, 200), "text", 200, 200, (100, 100))

    def test_check_if_available(self):
        self.assertFalse(self.upgrade_button3.check_if_available())
        clicker.SCORE = 200
        self.assertTrue(self.upgrade_button3.check_if_available())
        back_to_default()


class SimpleClickerTest(unittest.TestCase):
    game = clicker.Game()


if __name__ == '__main__':
    unittest.main()