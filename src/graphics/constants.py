import os
import pygame

game_folder = os.path.dirname(__file__)
resources_folder = game_folder + '/../../resources'
img_folder = os.path.join(resources_folder, 'sprites')
fonts_folder = os.path.join(resources_folder, 'fonts')
logo_img = pygame.image.load(os.path.join(img_folder, 'MIPT.png'))
background_img = pygame.image.load(os.path.join(img_folder, 'background.jpg'))


# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 200)
RED = (200, 100, 100)
GREEN = (100, 200, 100)
SCREEN_COLOR = WHITE
BUTTON_COLOR = BLUE
FONT_COLOR = BLACK

UPGRADES_LIST = [["Заботать LaTex", "Сходить на лабы", "Посмотреть матан", "Написать прогу", "Сдать коллок", "Закрыть англ",
             "Закрыть физру", "Покушать в КСП", "Закрыть зачеты", "Сдать сессию"],
            [10, 100, 1000, 10000, 50000, 100000, 200000, 500000, 1000000, 100000000],
            [1, 10, 100, 1000, 10000, 50000, 100000, 200000, 500000, 1000000]]
