import pygame

from setting_files.settings import food_radius, pacman_radius, ghost_radius, part, score_point, pacman_speed, start


def dist_square(b, a):  # квадрат расстояния между точками
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def food_check(pacman):  # функция определения съедания пакманом зерна
    x_left = pacman.geometry.x
    y_up = pacman.geometry.y
    x_right = pacman.geometry.x + pacman.geometry.width
    y_bottom = pacman.geometry.y + pacman.geometry.height
    x_center = pacman.geometry.x + pacman.geometry.width // 2
    y_center = pacman.geometry.y + pacman.geometry.height // 2
    first_quarter = (x_right // part, y_up // part)  # квадрат где находится верхний правый угол пакмана
    second_quarter = (x_right // part, y_bottom // part)  # квадрат где находится нижний правый угол пакмана
    third_quarter = (x_left // part, y_bottom // part)  # квадрат где находится левый нижний угол пакмана
    fourth_quarter = (x_left // part, y_up // part)  # квадрат где находится левый верхний угол пакмана
    if dist_square((x_center, y_center), center(first_quarter)) <= (food_radius + pacman_radius - 2) ** 2:
        return first_quarter
    if dist_square((x_center, y_center), center(second_quarter)) <= (food_radius + pacman_radius - 2) ** 2:
        return second_quarter
    if dist_square((x_center, y_center), center(third_quarter)) <= (food_radius + pacman_radius - 2) ** 2:
        return third_quarter
    if dist_square((x_center, y_center), center(fourth_quarter)) <= (food_radius + pacman_radius - 2) ** 2:
        return fourth_quarter
    return 0


def center(cell):  # функция центра клетки
    return [cell[0] * part + part // 2, cell[1] * part + part // 2]


def collision(ghost, pacman):
    pacman_center = ((pacman.geometry.x + pacman_radius // 2), (pacman.geometry.y + pacman_radius // 2))
    if ghost.geometry.x <= pacman_center[0] <= ghost.geometry.x + 2 * ghost_radius and \
            ghost.geometry.y <= pacman_center[1] <= ghost.geometry.y + 2 * ghost_radius:
        return False
    else:
        return True


def all_collision(pacman, g1, g2, g3, g4):
    if collision(g1, pacman) and collision(g2, pacman) and collision(g3, pacman) and collision(g4, pacman):
        return False
    else:
        return True


class PacMan:
    def __init__(self, start_position, size):  # инициализация пакмана
        self.now_hero = pygame.image.load('images/pacman0.png')
        self.now_hero = pygame.transform.scale(self.now_hero, (pacman_radius * 2, pacman_radius * 2))
        self.hero = pygame.image.load('images/pacman0.png')
        self.hero = pygame.transform.scale(self.hero, (pacman_radius * 2, pacman_radius * 2))
        self.hero_1 = pygame.image.load('images/pacman1.png')
        self.hero_1 = pygame.transform.scale(self.hero_1, (pacman_radius * 2, pacman_radius * 2))
        self.hero_2 = pygame.image.load('images/pacman2.png')
        self.hero_2 = pygame.transform.scale(self.hero_2, (pacman_radius * 2, pacman_radius * 2))
        self.start_image = self.hero
        self.start_image_1 = self.hero_1
        self.start_image_2 = self.hero_2
        self.geometry = self.hero.get_rect()
        self.speed_y = pacman_speed
        self.speed_x = pacman_speed
        self.score = 0
        self.hyper_phase = 5
        self.event_block = 0
        self.event_food = [0, [0, 0]]
        self.event_ghost = 0
        self.phase = 0
        self.death = 3
        self.speed = [pacman_speed, 0]  # скорость пакмана
        self.direction = 0  # направление морды
        self.start_position = start_position
        self.geometry.x = start_position[0] * part
        self.geometry.y = start_position[1] * part
        self.size = (size[0] * part, size[1] * part)

    def shift(self, field, food, g1, g2, g3, g4):  # движение пакмана
        self.geometry.x += self.speed[0]
        self.geometry.y += self.speed[1]
        self.check_position(field, g1, g2, g3, g4)
        if self.event_block == 1:
            self.geometry.x -= self.speed[0]
            self.geometry.y -= self.speed[1]
        if self.event_food[0] == 1:
            if food.Array[self.event_food[1][1]][self.event_food[1][0]] == 1:
                self.score += score_point
            if food.Array[self.event_food[1][1]][self.event_food[1][0]] != -1:
                food.Array[self.event_food[1][1]][self.event_food[1][0]] = 0
        if self.event_ghost == 1:
            self.death -= 1
            self.geometry.x = start[0] * part
            self.geometry.y = start[1] * part

    def change_direct(self, key):  # функция изменения направления
        key = chr(key)
        if key == 'w':
            self.speed = [0, -1 * self.speed_y]
            self.direction = 1
        if key == 's':
            self.speed = [0, self.speed_y]
            self.direction = 3
        if key == 'a':
            self.speed = [-1 * self.speed_x, 0]
            self.direction = 2
        if key == 'd':
            self.speed = [self.speed_x, 0]
            self.direction = 0
        self.hero = pygame.transform.rotate(self.start_image, 90 * self.direction)
        self.hero_1 = pygame.transform.rotate(self.start_image_1, 90 * self.direction)
        self.hero_2 = pygame.transform.rotate(self.start_image_2, 90 * self.direction)

    def check_position(self, field, g1, g2, g3, g4):  # функция определяющая по позиции пакмана
        # его пересечение с остальными объектами
        x_left = self.geometry.x
        y_up = self.geometry.y
        self.event_block = 0
        self.event_food = [0, [0, 0]]
        self.event_ghost = 0
        x_right = self.geometry.x + self.geometry.width
        y_bottom = self.geometry.y + self.geometry.height
        if x_left < 0 or x_right > self.size[0] or y_up < 0 or y_bottom > self.size[1]:
            self.event_block = 1
        if not(field.check_coord(x_right, y_up) and field.check_coord(x_right, y_bottom)
               and field.check_coord(x_left, y_bottom) and field.check_coord(x_left, y_up)):
            self.event_block = 1
        food_eat = food_check(self)
        if food_eat != 0:
            self.event_food = [1, food_eat]
        if all_collision(self, g1, g2, g3, g4):
            self.event_ghost = 1
        if self.geometry.left < part:
            self.geometry.x = self.size[0] - part - self.geometry.width - 5
        if self.geometry.right > self.size[0] - part:
            self.geometry.x = part + 5

    def draw(self, screen):
        if self.phase <= self.hyper_phase:
            self.phase += 1
            self.now_hero = self.hero_1
        else:
            if self.phase <= 2 * self.hyper_phase:
                self.phase += 1
                self.now_hero = self.hero_2
            else:
                self.now_hero = self.hero
                self.phase += 1
                if self.phase == 3 * self.hyper_phase:
                    self.phase = 0
        screen.blit(self.now_hero, self.geometry)
