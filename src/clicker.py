#!/bin/python3
import pygame
import os
from src import dollar

pygame.init()
pygame.mixer.init()

game_folder = os.path.dirname(__file__)
resources_folder = game_folder + '/../resources'
img_folder = os.path.join(resources_folder, 'sprites')
fonts_folder = os.path.join(resources_folder, 'fonts')
logo_img = pygame.image.load(os.path.join(img_folder, 'MIPT.png'))
background_img = pygame.image.load(os.path.join(img_folder, 'background.jpg'))

WIDTH = 800  # game window width
HEIGHT = 600  # game window height
FPS = 30  # частота кадров в секунду
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

#colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 100, 200)
RED = (200, 100, 100)
GREEN = (100, 200, 100)
SCREEN_COLOR = WHITE
BUTTON_COLOR = BLUE
FONT_COLOR = BLACK

FONT = pygame.font.Font(fonts_folder + '/Font.ttf', int(HEIGHT / 45))

DOLLAR_SCORE = 0
RUB_SCORE = 0
BOOSTER = 1
AUTO_CLICKS = 0


class Logo(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(logo_img, (int(WIDTH / 5), int(HEIGHT / 12)))
        self.image.set_colorkey(SCREEN_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = position


class Background(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(background_img, (int(WIDTH), int(HEIGHT)))
        self.image.set_colorkey(SCREEN_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = position


class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, size):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.image = pygame.Surface(size)
        self.image.fill(BUTTON_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.font = pygame.font.Font(fonts_folder + '/Font.ttf', int(HEIGHT / 20))

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect, 0)
        pygame.draw.rect(surface, WHITE, self.rect, 2)
        text_surface = self.font.render(self.text, False, FONT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.rect.left + 10, self.rect.top + self.rect.height * 0.25)
        surface.blit(text_surface, text_rect)


class CurrencyButton(Button):
    def __init__(self, pos, text, size):
        super().__init__(pos, text, size)
        self.rect = Button(pos, text, size).rect
        self.count = 0
        self.text = text
        self.color = GREEN
        self.border_color = BLACK
        self.exchange_rate = int(dollar.get_currency_price())
        self.last_time = pygame.time.get_ticks()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        if pygame.time.get_ticks() - self.last_time >= 100000:
            self.update_exchange_rate()
            self.last_time = pygame.time.get_ticks()
        text_surface = FONT.render("Обменять по курсу: $1 = " + str(self.exchange_rate) + "RUB", False, FONT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.rect.left + 10, self.rect.top + self.rect.height * 0.25)
        surface.blit(text_surface, text_rect)

    def click(self):
        global RUB_SCORE
        global DOLLAR_SCORE
        if DOLLAR_SCORE > 0:
            RUB_SCORE += DOLLAR_SCORE * self.exchange_rate
            DOLLAR_SCORE = 0

    def update_exchange_rate(self):
        self.exchange_rate = int(dollar.get_currency_price())


class UpgradeCPS(Button):
    def __init__(self, pos, text, price, cps, size):
        super().__init__(pos, text, size)
        self.rect = Button(pos, text, size).rect
        self.count = 0
        self.text = text
        self.price = price
        self.cps = cps
        self.color = RED
        self.border_color = BLACK

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        text_surface = FONT.render(" " + str(self.text) + " " + str(self.price) + "RUB  +" + str(self.cps), False, FONT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.rect.left + 10, self.rect.top + self.rect.height * 0.25)
        surface.blit(text_surface, text_rect)

    def click(self):
        global RUB_SCORE
        global AUTO_CLICKS
        if RUB_SCORE >= self.price:
            self.count += 1
            RUB_SCORE -= self.price
            AUTO_CLICKS += self.cps
            self.price *= 1.2
            self.price = int(self.price)

    def check_if_available(self):
        if self.price <= RUB_SCORE:
            self.color = BLUE
            return True
        else:
            self.color = RED
            return False


class UpgradeCPC(Button):
    def __init__(self, pos, text, price, cps, size):
        super().__init__(pos, text, size)
        self.rect = Button(pos, text, size).rect
        self.count = 0
        self.text = text
        self.price = price
        self.cps = cps
        self.color = RED
        self.border_color = BLACK

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, self.border_color, self.rect, 2)
        text_surface = FONT.render(" " + str(self.text) + "  $" + str(self.price) + "  +" + str(self.cps), False, FONT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.rect.left + 10, self.rect.top + self.rect.height * 0.25)
        surface.blit(text_surface, text_rect)

    def click(self):
        global DOLLAR_SCORE
        global BOOSTER
        if DOLLAR_SCORE >= self.price:
            self.count += 1
            DOLLAR_SCORE -= self.price
            BOOSTER += self.cps
            self.price *= 1.2
            self.price = int(self.price)

    def check_if_available(self):
        if self.price <= DOLLAR_SCORE:
            self.color = BLUE
            return True
        else:
            self.color = RED
            return False


UPGRADES_LIST = [["Заботать LaTex", "Сходить на лабы", "Посмотреть матан", "Написать прогу", "Сдать коллок", "Закрыть англ",
             "Закрыть физру", "Покушать в КСП", "Закрыть зачеты", "Сдать сессию"],
            [10, 100, 1000, 10000, 50000, 100000, 200000, 500000, 1000000, 100000000],
            [1, 10, 100, 1000, 10000, 50000, 100000, 200000, 500000, 1000000]]

UPGRADES_CPS = []
UPGRADES_CPC = []
MAIN_MENU = []
SETTINGS = []
CURRENCY = []


def initiate_buttons():
    global UPGRADES_CPC
    global UPGRADES_CPS
    global MAIN_MENU
    global SETTINGS
    global CURRENCY
    UPGRADES_CPS = []
    UPGRADES_CPC = []
    for i in range(10):
        if i % 2 == 0:
            UPGRADES_CPC.append(
                UpgradeCPC((WIDTH / 4 + WIDTH / 2 * (i % 2), (int(i / 2) * HEIGHT / 6) + HEIGHT / 6),
                           UPGRADES_LIST[0][i],
                           UPGRADES_LIST[1][i], UPGRADES_LIST[2][i], (WIDTH * 3 / 8, HEIGHT / 12)))
        else:
            UPGRADES_CPS.append(
                UpgradeCPS((WIDTH / 4 + WIDTH / 2 * (i % 2), (int(i / 2) * HEIGHT / 6) + HEIGHT / 6),
                           UPGRADES_LIST[0][i],
                           UPGRADES_LIST[1][i], UPGRADES_LIST[2][i], (WIDTH * 3 / 8, HEIGHT / 12)))

    MAIN_MENU = [Button((WIDTH / 2, 2 * HEIGHT / 3), "Settings", (WIDTH / 4, HEIGHT / 6)),
                 Button((WIDTH / 2, HEIGHT / 3), "Play!", (WIDTH / 4, HEIGHT / 6))]

    SETTINGS = [Button((WIDTH / 3, 2 * HEIGHT / 3), "FullScreen", (WIDTH / 4, HEIGHT / 6)),
                Button((2 * WIDTH / 3, HEIGHT / 3), "800 x 600", (WIDTH / 4, HEIGHT / 6)),
                Button((2 * WIDTH / 3, 2 * HEIGHT / 3), "1200 x 900", (WIDTH / 4, HEIGHT / 6)),
                Button((WIDTH / 3, HEIGHT / 3), "Back", (WIDTH / 4, HEIGHT / 6))]

    CURRENCY = [CurrencyButton((31 * WIDTH / 60, HEIGHT / 16), "", (WIDTH * 3 / 8, HEIGHT / 12))]


initiate_buttons()


class Game:
    def __init__(self):
        pygame.display.set_caption("MIPT clicker")
        self.clock = pygame.time.Clock()
        self.running = True
        self.logo = Logo((WIDTH / 10, 23 * HEIGHT / 24))
        self.background = Background((WIDTH / 2, HEIGHT / 2))
        self.font = pygame.font.Font(fonts_folder + '/Font.ttf', 20)
        self.font2 = pygame.font.Font(fonts_folder + '/Font.ttf', 40)
        self.upgradesCPC = UPGRADES_CPC
        self.upgradesCPS = UPGRADES_CPS
        self.menu_running = True
        self.menu_buttons = MAIN_MENU
        self.currency_button = CURRENCY
        self.settings_running = True
        self.settings_buttons = SETTINGS
        self.prev_tick = 0

    def render_main(self):
        SCREEN.fill(SCREEN_COLOR)
        SCREEN.blit(self.background.image, self.background.rect)
        SCREEN.blit(self.logo.image, self.logo.rect)
        for i in self.upgradesCPC:
            i.draw(SCREEN)
            i.check_if_available()
        for i in self.upgradesCPS:
            i.draw(SCREEN)
            i.check_if_available()
        self.currency_button[0].draw(SCREEN)
        global DOLLAR_SCORE
        global RUB_SCORE
        text_score_dollar = self.font.render("$" + str(DOLLAR_SCORE), True, FONT_COLOR)
        text_score_rub = self.font.render("Your wallet:  " + str(RUB_SCORE) + "RUB", True, FONT_COLOR)
        text_upgr_1 = self.font.render("$ per CLICK: " + str(BOOSTER), True, FONT_COLOR)
        text_upgr_2 = self.font.render("$ per SEC: " + str(AUTO_CLICKS), True, FONT_COLOR)
        SCREEN.blit(text_score_dollar, (3 * WIDTH / 4, 11 * HEIGHT / 12))
        SCREEN.blit(text_score_rub, (WIDTH / 4, 11 * HEIGHT / 12))
        SCREEN.blit(text_upgr_1, (WIDTH / 20, HEIGHT / 20))
        SCREEN.blit(text_upgr_2, (10 * WIDTH / 14, HEIGHT / 20))
        pygame.display.flip()

    def render_menu(self):
        SCREEN.fill(BLACK)
        for i in self.menu_buttons:
            i.draw(SCREEN)
        pygame.display.flip()

    def render_settings(self):
        SCREEN.fill(BLACK)
        for i in self.settings_buttons:
            i.draw(SCREEN)
        pygame.display.flip()

    def render_win(self):
        SCREEN.fill(BLACK)
        text_win = self.font2.render("СЕССИЯ СДАНА!!!", True, WHITE)
        SCREEN.blit(text_win, (WIDTH / 2, HEIGHT / 2))
        pygame.display.flip()
        pygame.time.delay(200)
        SCREEN.fill(WHITE)
        text_win = self.font2.render("СЕССИЯ СДАНА!!!", True, BLACK)
        SCREEN.blit(text_win, (WIDTH / 5, HEIGHT / 5))
        pygame.display.flip()
        pygame.time.delay(200)

    def check_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in self.menu_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.text == "Play!":
                            self.menu_running = False
                        elif button.text == "Settings":
                            self.settings_running = True
                            while self.settings_running:
                                self.render_settings()
                                self.check_settings_event()

    def change_screen_size(self):
        global FONT
        initiate_buttons()
        FONT = pygame.font.Font(fonts_folder + '/Font.ttf', int(HEIGHT / 40))
        self.upgradesCPS = UPGRADES_CPS
        self.upgradesCPC = UPGRADES_CPC
        self.settings_buttons = SETTINGS
        self.menu_buttons = MAIN_MENU
        self.logo = Logo((WIDTH / 10, 23 * HEIGHT / 24))
        self.background = Background((WIDTH / 2, HEIGHT / 2))
        self.currency_button = CURRENCY
        self.font = pygame.font.Font(fonts_folder + '/Font.ttf', int(WIDTH / 45))
        self.font2 = pygame.font.Font(fonts_folder + '/Font.ttf', int(WIDTH / 20))

    def check_settings_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                global WIDTH
                global HEIGHT
                global SCREEN
                for button in self.settings_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.text == "FullScreen":
                            WIDTH = 1920
                            HEIGHT = 1080
                        elif button.text == "800 x 600":
                            WIDTH = 800
                            HEIGHT = 600
                        elif button.text == "1200 x 900":
                            WIDTH = 1200
                            HEIGHT = 900
                        elif button.text == "Back":
                            self.settings_running = False
                        self.change_screen_size()
                        SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    def check_events(self):
        global RUB_SCORE
        global DOLLAR_SCORE
        global AUTO_CLICKS
        if pygame.time.get_ticks() - self.prev_tick >= 1000:
            DOLLAR_SCORE += AUTO_CLICKS
            self.prev_tick = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # space button is pressed
                    global BOOSTER
                    DOLLAR_SCORE += BOOSTER
                elif event.key == pygame.K_ESCAPE:  # escape is pressed
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # right mouse click
                for upgr in self.upgradesCPS:
                    if upgr.rect.collidepoint(event.pos):
                        upgr.click()
                for upgr in self.upgradesCPC:
                    if upgr.rect.collidepoint(event.pos):
                        upgr.click()
                if self.currency_button[0].rect.collidepoint(event.pos):
                    self.currency_button[0].click()
                if self.upgradesCPS[4].count == 1:
                    self.game_end()

    def game_end(self):
        while self.running:
            self.render_win()
            self.check_events()

    def game_loop(self):
        while self.menu_running:
            self.render_menu()
            self.check_menu_events()

        while self.running:
            self.clock.tick(FPS)
            self.check_events()
            self.render_main()


def run():
    game = Game()
    game.game_loop()


run()
