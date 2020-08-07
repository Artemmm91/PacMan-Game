from sys import exit

import pygame

from game import Game
from objects.menu import Menu

if __name__ == "__main__":
    pygame.init()
    m = Menu()
    m.main_loop()
    pygame.display.quit()
    pygame.display.init()
    g = Game()
    if m.is_game:
        g.main_loop()
    exit()
