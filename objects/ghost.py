import pygame

from setting_files.settings import part, level_hard, ghost_radius


def search_div(a, b):  # функция находящий делитель числа a который больше делителя числа b
    for i in range(a - b + 1):
        if a % (i + b) == 0:
            return i + b
    return a


def ghost_block(cell, bl, ghost):  # функция которая определяет свободная ли клетка от привидения
    # или от того куда хочет пойти приведения
    if bl == cell or ghost.direction == cell:
        return False
    else:
        return True


def ghost_free(cell, g1, g2, g3):  # узнает есть ли в клетке эти 3 приведения
    bl1 = g1.geometry.x // part, g1.geometry.y // part
    bl2 = g2.geometry.x // part, g2.geometry.y // part
    bl3 = g3.geometry.x // part, g3.geometry.y // part
    if ghost_block(cell, bl1, g1) and ghost_block(cell, bl2, g2) and ghost_block(cell, bl3, g3):
        return True
    else:
        return False


def choose(cell_1, cell_2, aim, field):
        dist_1 = (cell_1[0] - aim[0])**2 + (cell_1[1] - aim[1]) ** 2
        dist_2 = (cell_2[0] - aim[0]) ** 2 + (cell_2[1] - aim[1]) ** 2
        if not field.check_block(cell_1):
            return 2
        if not field.check_block(cell_2):
            return 1
        if dist_1 > dist_2:
            return 2
        else:
            return 1


def choose_3(cell_1, cell_2, cell_3, aim, field):
    dist_1 = (cell_1[0] - aim[0]) ** 2 + (cell_1[1] - aim[1]) ** 2
    dist_2 = (cell_2[0] - aim[0]) ** 2 + (cell_2[1] - aim[1]) ** 2
    dist_3 = (cell_3[0] - aim[0]) ** 2 + (cell_3[1] - aim[1]) ** 2
    if not field.check_block(cell_1):
        return choose(cell_2, cell_3, aim, field) + 1
    if not field.check_block(cell_2):
        a = choose(cell_1, cell_3, aim, field)
        if a == 1:
            return 1
        else:
            return 3
    if not field.check_block(cell_3):
        return choose(cell_1, cell_2, aim, field)
    if dist_1 > dist_2:
        return choose(cell_2, cell_3, aim, field) + 1
    else:
        a = choose(cell_1, cell_3, aim, field)
        if a == 1:
            return 1
        else:
            return 3


class Ghost:
    def __init__(self, start_ghost, type_im):  # инициализация
        type_im = str(type_im)  # тип картинки
        self.type_ghost = type_im
        image_string = 'images/ghost' + type_im + '.png'  # имя по типу картинки
        self.ghost = pygame.image.load(image_string)  # картинка привидения
        self.ghost = pygame.transform.scale(self.ghost, (ghost_radius * 2, ghost_radius * 2))
        self.geometry = self.ghost.get_rect()  # его геометрия
        self.geometry.x = start_ghost[0] * part
        self.geometry.y = start_ghost[1] * part
        self.speed = [level_hard, level_hard]  # скорость зависящая от уровня сложности
        self.block_position = start_ghost  # позиция привидения в клетке
        self.direction = [-1, -1]  # куда хочет пойти привидение
        if part % self.speed[0] != 0:  # делаем скорость которая бы делила размер клетки
            self.speed[0] = search_div(part, self.speed[0])
        if part % self.speed[1] != 0:
            self.speed[1] = search_div(part, self.speed[1])

    def centr(self):  # определяет центр приведения
        return self.geometry.x + self.geometry.width // 2, self.geometry.y + self.geometry.height // 2

    def block_aim(self, field, pacman, g1, g2, g3):
        pacman_position = pacman[0], pacman[1]
        pacman_block = pacman_position[0] // part, pacman_position[1] // part
        if self.direction == [-1, -1]:
            if pacman_block[0] > self.block_position[0]:
                if field.check_block((self.block_position[0] + 1, self.block_position[1])) \
                        and ghost_free((self.block_position[0] + 1, self.block_position[1]), g1, g2, g3):
                    self.direction = [self.block_position[0] + 1, self.block_position[1]]
                else:
                    if pacman_block[1] > self.block_position[1]:
                        if field.check_block((self.block_position[0], self.block_position[1] + 1)) \
                                and ghost_free((self.block_position[0], self.block_position[1] + 1), g1, g2, g3):
                            self.direction = [self.block_position[0], self.block_position[1] + 1]
                        else:
                            if choose([self.block_position[0], self.block_position[1] - 1],
                                      [self.block_position[0] - 1, self.block_position[1]], pacman_block, field) == 1:
                                self.direction = [self.block_position[0], self.block_position[1] - 1]
                            else:
                                self.direction = [self.block_position[0] - 1, self.block_position[1]]
                    if pacman_block[1] < self.block_position[1]:
                        if field.check_block((self.block_position[0], self.block_position[1] - 1)) \
                                and ghost_free((self.block_position[0], self.block_position[1] - 1), g1, g2, g3):
                            self.direction = [self.block_position[0], self.block_position[1] - 1]
                        else:
                            if choose([self.block_position[0], self.block_position[1] + 1],
                                      [self.block_position[0] - 1, self.block_position[1]], pacman_block, field) == 1:
                                self.direction = [self.block_position[0], self.block_position[1] + 1]
                            else:
                                self.direction = [self.block_position[0] - 1, self.block_position[1]]
                    if pacman_block[1] == self.block_position[1]:
                        if field.check_block((self.block_position[0] + 1, self.block_position[1])) \
                                and ghost_free((self.block_position[0] + 1, self.block_position[1]), g1, g2, g3):
                            self.direction = [self.block_position[0] + 1, self.block_position[1]]
                        else:
                            r = choose_3([self.block_position[0], self.block_position[1] + 1],
                                         [self.block_position[0] - 1, self.block_position[1]],
                                         [self.block_position[0] + 1, self.block_position[1]], pacman_block, field)
                            if r == 1:
                                self.direction = [self.block_position[0], self.block_position[1] + 1]
                            else:
                                if r == 2:
                                    self.direction = [self.block_position[0] - 1, self.block_position[1]]
                                else:
                                    self.direction = [self.block_position[0] + 1, self.block_position[1]]
            if pacman_block[0] < self.block_position[0]:
                if field.check_block((self.block_position[0] - 1, self.block_position[1])) \
                        and ghost_free((self.block_position[0] - 1, self.block_position[1]), g1, g2, g3):
                    self.direction = [self.block_position[0] - 1, self.block_position[1]]
                else:
                    if pacman_block[1] > self.block_position[1]:
                        if field.check_block((self.block_position[0], self.block_position[1] + 1)) \
                                and ghost_free((self.block_position[0], self.block_position[1] + 1), g1, g2, g3):
                            self.direction = [self.block_position[0], self.block_position[1] + 1]
                        else:
                            if choose([self.block_position[0], self.block_position[1] - 1],
                                      [self.block_position[0] + 1, self.block_position[1]], pacman_block, field) == 1:
                                self.direction = [self.block_position[0], self.block_position[1] - 1]
                            else:
                                self.direction = [self.block_position[0] + 1, self.block_position[1]]
                    if pacman_block[1] < self.block_position[1]:
                        if field.check_block((self.block_position[0], self.block_position[1] - 1)) \
                                and ghost_free((self.block_position[0], self.block_position[1] - 1), g1, g2, g3):
                            self.direction = [self.block_position[0], self.block_position[1] - 1]
                        else:
                            if choose([self.block_position[0], self.block_position[1] + 1],
                                      [self.block_position[0] + 1, self.block_position[1]], pacman_block, field) == 1:
                                self.direction = [self.block_position[0], self.block_position[1] + 1]
                            else:
                                self.direction = [self.block_position[0] + 1, self.block_position[1]]
                    if pacman_block[1] == self.block_position[1]:
                        if field.check_block((self.block_position[0] - 1, self.block_position[1])) \
                                and ghost_free((self.block_position[0] - 1, self.block_position[1]), g1, g2, g3):
                            self.direction = [self.block_position[0] - 1, self.block_position[1]]
                        else:
                            r = choose_3([self.block_position[0], self.block_position[1] + 1],
                                         [self.block_position[0], self.block_position[1] - 1],
                                         [self.block_position[0] + 1, self.block_position[1]], pacman_block, field)
                            if r == 1:
                                self.direction = [self.block_position[0], self.block_position[1] + 1]
                            else:
                                if r == 2:
                                    self.direction = [self.block_position[0], self.block_position[1] - 1]
                                else:
                                    self.direction = [self.block_position[0] + 1, self.block_position[1]]
            if pacman_block[0] == self.block_position[0]:
                if pacman_block[1] > self.block_position[1]:
                    if field.check_block((self.block_position[0], self.block_position[1] + 1)) \
                            and ghost_free((self.block_position[0], self.block_position[1] + 1), g1, g2, g3):
                        self.direction = [self.block_position[0], self.block_position[1] + 1]
                else:
                    r = choose_3([self.block_position[0], self.block_position[1] - 1],
                                 [self.block_position[0] - 1, self.block_position[1]],
                                 [self.block_position[0] + 1, self.block_position[1]], pacman_block, field)
                    if r == 1:
                        self.direction = [self.block_position[0], self.block_position[1] - 1]
                    else:
                        if r == 2:
                            self.direction = [self.block_position[0] - 1, self.block_position[1]]
                        else:
                            self.direction = [self.block_position[0] + 1, self.block_position[1]]
                if pacman_block[1] < self.block_position[1]:
                    if field.check_block((self.block_position[0], self.block_position[1] - 1)) \
                            and ghost_free((self.block_position[0], self.block_position[1] - 1), g1, g2, g3):
                        self.direction = [self.block_position[0], self.block_position[1] - 1]
                    else:
                        r = choose_3([self.block_position[0], self.block_position[1] + 1],
                                     [self.block_position[0] - 1, self.block_position[1]],
                                     [self.block_position[0] + 1, self.block_position[1]], pacman_block, field)
                        if r == 1:
                            self.direction = [self.block_position[0], self.block_position[1] + 1]
                        else:
                            if r == 2:
                                self.direction = [self.block_position[0] - 1, self.block_position[1]]
                            else:
                                self.direction = [self.block_position[0] + 1, self.block_position[1]]
        if self.direction != [-1, -1]:
            differ = (self.direction[0] - self.block_position[0], self.direction[1] - self.block_position[1])
            direct_coord = self.direction[0] * part, self.direction[1] * part
            if differ[1] == 0:
                if self.geometry.x != direct_coord[0]:
                    self.geometry.x += differ[0] * self.speed[0]
                else:
                    self.block_position = self.direction
                    self.direction = [-1, -1]
            if differ[0] == 0:
                if self.geometry.y != direct_coord[1]:
                    self.geometry.y += differ[1] * self.speed[1]
                else:
                    self.block_position = self.direction
                    self.direction = [-1, -1]

    def shift(self, field, pacman, ghost_blinky, ghost_2, ghost_3):  # если само приведение не блинки то пофиг кого
        # первым писать, но если привидение блинки то его надо писать первым
        aim = pacman.geometry.x, pacman.geometry.y
        if self.type_ghost == 2:
            if pacman.direction == 0:
                aim = pacman.geometry.x + 4 * part, pacman.geometry.y
            if pacman.direction == 3:
                aim = pacman.geometry.x, pacman.geometry.y + 4 * part
            if pacman.direction == 2:
                aim = pacman.geometry.x - 4 * part, pacman.geometry.y
            if pacman.direction == 1:
                aim = pacman.geometry.x, pacman.geometry.y - 4 * part
        if self.type_ghost == 3:
            if ghost_blinky.direction != [-1, -1]:
                mid_aim = 0, 0
                if pacman.direction == 0:
                    mid_aim = pacman.geometry.x + 2 * part, pacman.geometry.y
                if pacman.direction == 3:
                    mid_aim = pacman.geometry.x, pacman.geometry.y - 2 * part
                if pacman.direction == 2:
                    mid_aim = pacman.geometry.x - 2 * part, pacman.geometry.y
                if pacman.direction == 1:
                    mid_aim = pacman.geometry.x, pacman.geometry.y + 2 * part
                blinky_aim = ghost_blinky.direction[0] * part, ghost_blinky.direction[1] * part
                aim = blinky_aim[0] + 2 * mid_aim[0], blinky_aim[1] + 2 * mid_aim[1]
        if self.type_ghost == 4:
            dist = abs(self.geometry.x - pacman.geometry.x) + abs(self.geometry.y - pacman.geometry.y)
            if dist <= 9:
                aim = pacman.geometry.x + part, pacman.geometry.y - 2 * part
        self.block_aim(field, aim, ghost_blinky, ghost_2, ghost_3)
