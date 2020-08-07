import pygame

from button import Button
from setting_files import settings
from setting_files.colors import YELLOW, BLACK, BUTTON_STYLE_Menu


class Menu:
    def __init__(self):
        self.screen_size = settings.start_screen
        self.screen = pygame.display.set_mode(self.screen_size)
        self.logo = pygame.image.load("images/logo.png")
        self.logo = pygame.transform.scale(self.logo, (600, 140))
        self.geom_logo = self.logo.get_rect()
        self.set_geom_logo()
        self.w_close = False
        self.is_game = True
        self.button_start = Button(
            (200, 300, 300, 100), YELLOW, self.button_action_start, text='Start', **BUTTON_STYLE_Menu
        )
        self.button_exit = Button(
            (200, 500, 300, 100), YELLOW, self.button_action_exit, text='Exit', **BUTTON_STYLE_Menu
        )

    def set_geom_logo(self):
        self.geom_logo.x = 50
        self.geom_logo.y = 60

    def button_action_start(self):
        self.w_close = True

    def button_action_exit(self):
        self.is_game = False
        self.w_close = True

    def main_loop(self):
        while not self.w_close:
            self.check_event()
            self.draw()

    def check_event(self):
        events = pygame.event.get()
        for event in events:
            self.button_start.check_event(event)  # обновляем кнопки
            self.button_exit.check_event(event)
            if event.type == pygame.QUIT:
                self.w_close = True
                self.is_game = False

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_logo()
        self.button_exit.update(self.screen)
        self.button_start.update(self.screen)
        pygame.display.flip()

    def draw_logo(self):
        self.screen.blit(self.logo, self.geom_logo)
