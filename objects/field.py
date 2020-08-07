import pygame

from setting_files.colors import rand_color, BLACK
from setting_files.settings import part


def draw_side(i, j, side, surface):
    if side == 0:
        pygame.draw.rect(surface, rand_color, (j * part, i * part, part // 2, part))
    if side == 1:
        pygame.draw.rect(surface, rand_color, (j * part, i * part + part // 2, part, part // 2))
    if side == 2:
        pygame.draw.rect(surface, rand_color, (j * part + part // 2, i * part, part // 2, part))
    if side == 3:
        pygame.draw.rect(surface, rand_color, (j * part, i * part, part, part // 2))


class Field:
    def __init__(self, field, size):  # инициализация
        self.height = size[0]
        self.width = size[1]
        self.form = 3
        self.n = [size[0], size[1]]
        self.Array = field

    def check_block(self, pair):  # по координатам блока определяет есть ли блок там
        if self.height > pair[0] >= 0 and self.width > pair[1] >= 0:
            if self.Array[pair[1]][pair[0]] != 1:
                return True
            else:
                return False
        else:
            return False

    def check_coord(self, x, y):  # по координате определяет есть ли блок там
        i = x // part
        j = y // part
        return self.check_block([i, j])

    def draw_new_side(self, i, j, side, surface):
        if side == 0:
            pygame.draw.rect(surface, BLACK, (j * part, i * part + self.form, part // 2, part - 2 * self.form))
        if side == 1:
            pygame.draw.rect(surface, BLACK,
                             (j * part + self.form, i * part + part // 2, part - 2 * self.form, part // 2))
        if side == 2:
            pygame.draw.rect(surface, BLACK,
                             (j * part + part // 2, i * part + self.form, part // 2, part - 2 * self.form))
        if side == 3:
            pygame.draw.rect(surface, BLACK, (j * part + self.form, i * part, part - 2 * self.form, part // 2))

    def draw_block(self, i, j, surface, size):
        pygame.draw.circle(surface, rand_color, (j * part + part // 2, i * part + part // 2), part // 2)
        if j != (size[1] - 1) and self.Array[i][j + 1] == 1:
            draw_side(i, j, 2, surface)
        if j != 0 and self.Array[i][j - 1] == 1:
            draw_side(i, j, 0, surface)
        if i != 0 and self.Array[i - 1][j] == 1:
            draw_side(i, j, 3, surface)
        if i != (size[0] - 1) and self.Array[i + 1][j] == 1:
            draw_side(i, j, 1, surface)
        if j != (size[1] - 1) and self.Array[i][j + 1] == 1:
            self.draw_new_side(i, j, 2, surface)
        if j != 0 and self.Array[i][j - 1] == 1:
            self.draw_new_side(i, j, 0, surface)
        if i != 0 and self.Array[i - 1][j] == 1:
            self.draw_new_side(i, j, 3, surface)
        if i != (size[0] - 1) and self.Array[i + 1][j] == 1:
            self.draw_new_side(i, j, 1, surface)
        pygame.draw.circle(surface, BLACK, (j * part + part // 2, i * part + part // 2), part // 2 - self.form)
        pygame.draw.circle(surface, rand_color,
                           (j * part + part // 2, i * part + part // 2), part // 2 - 2 * self.form, self.form)

    def show(self, surface, size):  # функция показа поля с блоками
        for i in range(self.n[0]):
            for j in range(self.n[1]):
                if self.Array[i][j] == 1:
                    self.draw_block(i, j, surface, size)
