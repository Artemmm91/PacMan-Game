import pygame

from setting_files.colors import WHITE
from setting_files.settings import part, last_level, food_radius


class Food:
    def __init__(self, field):  # функция инициализации
        self.level = 0
        self.size = field.n
        self.Array = [[0 for i in range(self.size[0])] for j in range(self.size[1])]
        self.used = 0
        self.number_food = (self.size[0] - 1) * (self.size[1] - 1) - self.used
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if field.Array[i][j] == 0:
                    self.Array[i][j] = 0
                else:
                    self.Array[i][j] = -1
                    self.used += 1
        self.new_level()

    def is_food(self):  # функция проверки есть ли еда на поле
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.Array[i][j] == 1:
                    return True
        return False

    def new_level(self):  # функция создания нового левела
        if self.level < last_level:
            self.level += 1
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if self.Array[i][j] == 0:
                        self.Array[i][j] = 1

    def check_last_level(self):
        if self.level <= last_level:
            return True
        else:
            return False

    def show(self, surface):  # функция показа зерен
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.Array[i][j] == 1:
                    center_x = part * i + part // 2
                    center_y = part * j + part // 2
                    pygame.draw.circle(surface, WHITE, (center_y, center_x), food_radius)
