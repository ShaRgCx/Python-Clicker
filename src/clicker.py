#!/bin/python3
import pygame
import os

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
SCREEN_COLOR = WHITE
BUTTON_COLOR = BLUE
FONT_COLOR = BLACK

FONT = pygame.font.Font(fonts_folder + '/Font.ttf', int(HEIGHT / 40))

SCORE = 0
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


class Upgrade(Button):
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
        text_surface = FONT.render(" " + str(self.text) + "    " + str(self.price) + "     " + str(self.count * self.cps), False, FONT_COLOR)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (self.rect.left + 10, self.rect.top + self.rect.height * 0.25)
        surface.blit(text_surface, text_rect)

    def click(self):
        global SCORE
        global BOOSTER
        if SCORE >= self.price:
            self.count += 1
            SCORE -= self.price
            BOOSTER += self.cps
            self.price *= 1.2
            self.price = int(self.price)

    def auto_clicker(self):
        global SCORE
        global AUTO_CLICKS
        if SCORE >= self.price:
            self.count += 1
            SCORE -= self.price
            AUTO_CLICKS += self.cps
            self.price *= 1.2
            self.price = int(self.price)

    def check_if_available(self):
        if self.price <= SCORE:
            self.color = BLUE
            return True
        else:
            self.color = RED
            return False

    def change_color(self, new_color):
        self.color = new_color


UPGRADES_LIST = [["Заботать LaTex", "Сходить на лабы", "Посмотреть матан", "Написать прогу", "Сдать коллок", "Закрыть англ",
             "Закрыть физру", "Покушать в КСП", "Закрыть зачеты", "Сдать сессию"],
            [10, 100, 1000, 10000, 50000, 100000, 200000, 50000000, 100000000, 10000000000],
            [1, 10, 100, 1000, 10000, 50000, 100000, 200000, 50000000, 100000000]]

UPGRADES = []
MAIN_MENU = []
SETTINGS = []


def initiate_buttons():
    global UPGRADES
    global MAIN_MENU
    global SETTINGS
    UPGRADES = []
    for i in range(10):
        UPGRADES.append(
            Upgrade((WIDTH / 4 + WIDTH / 2 * (i % 2), (int(i / 2) * HEIGHT / 6) + HEIGHT / 6), UPGRADES_LIST[0][i],
                    UPGRADES_LIST[1][i], UPGRADES_LIST[2][i], (WIDTH * 3 / 8, HEIGHT / 12)))

    MAIN_MENU = [Button((WIDTH / 2, 2 * HEIGHT / 3), "Settings", (WIDTH / 4, HEIGHT / 6)),
                 Button((WIDTH / 2, HEIGHT / 3), "Play!", (WIDTH / 4, HEIGHT / 6))]

    SETTINGS = [Button((WIDTH / 3, 2 * HEIGHT / 3), "FullScreen", (WIDTH / 4, HEIGHT / 6)),
                Button((2 * WIDTH / 3, HEIGHT / 3), "800 x 600", (WIDTH / 4, HEIGHT / 6)),
                Button((2 * WIDTH / 3, 2 * HEIGHT / 3), "1200 x 900", (WIDTH / 4, HEIGHT / 6)),
                Button((WIDTH / 3, HEIGHT / 3), "Back", (WIDTH / 4, HEIGHT / 6))]


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
        self.upgrades = UPGRADES
        self.menu_running = True
        self.menu_buttons = MAIN_MENU
        self.settings_running = True
        self.settings_buttons = SETTINGS
        self.prev_tick = 0

    def render_main(self):
        SCREEN.fill(SCREEN_COLOR)
        SCREEN.blit(self.background.image, self.background.rect)
        SCREEN.blit(self.logo.image, self.logo.rect)
        for i in self.upgrades:
            i.draw(SCREEN)
            i.check_if_available()
        global SCORE
        text1 = self.font.render("Current score " + str(SCORE), True, FONT_COLOR)
        text_upgr_1 = self.font.render("Price   Points per CLICK", True, FONT_COLOR)
        text_upgr_2 = self.font.render("Price   Points per SEC", True, FONT_COLOR)
        SCREEN.blit(text1, (5 * WIDTH / 8, 11 * HEIGHT / 12))
        SCREEN.blit(text_upgr_1, (WIDTH / 5, HEIGHT / 20))
        SCREEN.blit(text_upgr_2, (5 * WIDTH / 7, HEIGHT / 20))
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
        self.upgrades = UPGRADES
        self.settings_buttons = SETTINGS
        self.menu_buttons = MAIN_MENU
        self.logo = Logo((WIDTH / 10, 23 * HEIGHT / 24))
        self.background = Background((WIDTH / 2, HEIGHT / 2))
        self.font = pygame.font.Font(fonts_folder + '/Font.ttf', int(WIDTH / 40))
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
        global SCORE
        global AUTO_CLICKS
        if pygame.time.get_ticks() - self.prev_tick >= 1000:
            SCORE += AUTO_CLICKS
            self.prev_tick = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # space button is pressed
                    global BOOSTER
                    SCORE += BOOSTER
                elif event.key == pygame.K_ESCAPE:  # escape is pressed
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # right mouse click
                for number, upgr in enumerate(self.upgrades):
                    if upgr.rect.collidepoint(event.pos):
                        if number % 2 == 0:
                            upgr.click()
                        else:
                            upgr.auto_clicker()
                if self.upgrades[9].count >= 1:
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
