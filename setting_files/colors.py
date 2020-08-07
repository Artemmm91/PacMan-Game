from random import randint
import pygame
pygame.font.init()
pixel_font = 'images/111.ttf'
RED = (255, 0, 0)  # цвета кнопки
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 143, 219)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 0)
YELLOW = (255, 225, 53)
rand_color = (randint(0, 255), randint(0, 255), randint(0, 255))
BUTTON_STYLE = {  # стиль кнопки
    "font": pygame.font.Font(pixel_font, 18),
    "hover_color": BLACK,
    "clicked_color": BLACK,
    "clicked_font_color": BLACK,
    "hover_font_color": RED
}
BUTTON_STYLE_Menu = {  # стиль кнопки
    "font": pygame.font.Font(pixel_font, 18),
    "hover_color": ORANGE,
    "clicked_color": ORANGE,
    "clicked_font_color": BLACK,
    "hover_font_color": BLUE,
    "font_color": LIGHT_BLUE
}
