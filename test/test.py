import unittest
from src import clicker


def back_to_default():
    clicker.DOLLAR_SCORE = 0
    clicker.RUB_SCORE = 0
    clicker.BOOSTER = 1
    clicker.AUTO_CLICKS = 0


class SimpleUpgradeTest(unittest.TestCase):
    upgrade_cpc = clicker.UpgradeCPC((200, 200), "text", 100, 100, (100, 100))

    def test_click(self):
        self.upgrade_cpc.click()
        self.assertEqual(clicker.DOLLAR_SCORE, 0)
        self.assertEqual(clicker.BOOSTER, 1)
        clicker.DOLLAR_SCORE = 100
        clicker.BOOSTER = 0
        self.upgrade_cpc.click()
        self.assertEqual(clicker.DOLLAR_SCORE, 0)
        self.assertEqual(clicker.BOOSTER, 100)
        back_to_default()

    upgrade_cps = clicker.UpgradeCPS((200, 200), "text", 200, 200, (100, 100))

    def test_auto_click(self):
        self.upgrade_cps.click()
        self.assertEqual(clicker.RUB_SCORE, 0)
        self.assertEqual(clicker.AUTO_CLICKS, 0)
        clicker.RUB_SCORE = 200
        self.upgrade_cps.click()
        self.assertEqual(clicker.RUB_SCORE, 0)
        self.assertEqual(clicker.AUTO_CLICKS, 200)
        back_to_default()

    upgrade_button3 = clicker.UpgradeCPS((200, 200), "text", 200, 200, (100, 100))
    upgrade_button4 = clicker.UpgradeCPC((200, 200), "text", 200, 200, (100, 100))

    def test_check_if_available(self):
        self.assertFalse(self.upgrade_button3.check_if_available())
        self.assertFalse(self.upgrade_button4.check_if_available())
        clicker.RUB_SCORE = 200
        self.assertFalse(self.upgrade_button4.check_if_available())
        self.assertTrue(self.upgrade_button3.check_if_available())
        clicker.DOLLAR_SCORE = 200
        clicker.RUB_SCORE = 0
        self.assertFalse(self.upgrade_button3.check_if_available())
        self.assertTrue(self.upgrade_button4.check_if_available())
        back_to_default()


class SimpleClickerTest(unittest.TestCase):
    game = clicker.Game()


if __name__ == '__main__':
    unittest.main()