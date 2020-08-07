import pygame

from button import Button
from objects.field import Field
from objects.food import Food
from objects.ghost import Ghost
from objects.pacman import PacMan
from setting_files.colors import BLACK, BUTTON_STYLE
from setting_files.settings import part, start, start_ghost1, start_ghost2, start_ghost3, start_ghost4


def read_map(file):
    pole = open(file, "r")
    data = []
    count = 1
    for line in pole:
        if count != 1:
            row = [int(i) for i in line.split()]
            data.append(row)
        count += 1
    pole.close()
    return data


def read_size(file):
    pole = open(file, "r")
    size = pole.readline().split(" ")
    size = [int(size[0]), int(size[1])]
    pole.close()
    return size


class Game:
    file_records = 'text_files/records.txt'
    file_map = 'text_files/map.txt'
    name = 'Artem '
    bg_name = 'images/images.jpg'

    def __init__(self):
        # state
        self.w_close = False
        self.w_pause = False

        # objects
        self.size = read_size(self.file_map)
        self.after_wait = 0
        self.field_map = read_map(self.file_map)
        self.field_size = (self.size[0] * part, self.size[1] * part)
        self.screen_size = (self.field_size[0], self.field_size[1] + 70)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.my_font = pygame.font.Font("images/111.ttf", 30)
        self.pacman_life = pygame.image.load("images/pacman.png")
        self.pacman_life = pygame.transform.scale(self.pacman_life, (50, 50))
        self.geom_life = self.pacman_life.get_rect()
        self.bg = pygame.image.load(self.bg_name)
        self.bg = pygame.transform.scale(self.bg, self.screen_size)
        self.bg_geom = self.bg.get_rect()

        self.button_pause = Button(
            (10, self.field_size[1] + 10, 100, 50), BLACK, self.button_action_pause, text='Pause', **BUTTON_STYLE
        )
        self.button_exit = Button(
            (120, self.field_size[1] + 10, 100, 50), BLACK, self.button_action_exit, text='Exit', **BUTTON_STYLE
        )

        self.field = Field(self.field_map, self.size)
        self.food = Food(self.field)
        self.hero = PacMan(start, self.size)
        self.ghost1 = Ghost(start_ghost1, 1)
        self.ghost2 = Ghost(start_ghost2, 2)
        self.ghost3 = Ghost(start_ghost3, 3)
        self.ghost4 = Ghost(start_ghost4, 4)

        self.level = 1
        self.life = 3
        self.score = 0

    def main_loop(self):
        while not self.w_close:
            self.process_events()
            self.game_logic()
            self.draw()
            self.after_game()
            pygame.time.wait(20)
        self.write_score()

    def after_game(self):
        if self.after_wait != 0:
            pygame.time.wait(500)

    def write_score(self):
        file_score = open(self.file_records, 'a')
        score_line = self.name + str(self.score) + '\n'
        file_score.write(score_line)
        file_score.close()

    def button_action_pause(self):
        if self.w_pause:
            self.w_pause = False
        else:
            self.w_pause = True

    def button_action_exit(self):
        self.w_close = True

    def process_events(self):
        events = pygame.event.get()
        for event in events:
            self.button_pause.check_event(event)  # обновляем кнопки
            self.button_exit.check_event(event)
            if event.type == pygame.QUIT:
                self.w_close = True
            if event.type == pygame.KEYDOWN and not self.w_pause:
                self.hero.change_direct(event.key)

    def game_logic(self):
        if not self.w_pause:
            self.hero.shift(self.field, self.food, self.ghost1, self.ghost2, self.ghost3, self.ghost4)
            self.ghost1.shift(self.field, self.hero, self.ghost2, self.ghost3, self.ghost4)
            self.ghost2.shift(self.field, self.hero, self.ghost1, self.ghost3, self.ghost4)
            self.ghost3.shift(self.field, self.hero, self.ghost1, self.ghost2, self.ghost4)
            self.ghost4.shift(self.field, self.hero, self.ghost2, self.ghost3, self.ghost1)
            self.score = self.hero.score

        if self.food.check_last_level():
            if not self.food.is_food():
                self.food.new_level()
                self.level += 1
                self.food.level += 1
        else:
            self.w_close = True

        if self.life > self.hero.death:
            self.life = self.hero.death
        if self.life == 0:
            self.after_wait = 1
            self.w_close = True

    def draw(self):
        self.screen.fill(BLACK)
        # self.screen.blit(self.bg, self.bg_geom)
        self.button_exit.update(self.screen)
        self.button_pause.update(self.screen)
        self.draw_elements()
        self.field.show(self.screen, self.size)
        self.food.show(self.screen)
        self.hero.draw(self.screen)
        self.draw_life()
        self.screen.blit(self.ghost1.ghost, self.ghost1.geometry)
        self.screen.blit(self.ghost2.ghost, self.ghost2.geometry)
        self.screen.blit(self.ghost3.ghost, self.ghost3.geometry)
        self.screen.blit(self.ghost4.ghost, self.ghost4.geometry)
        pygame.display.flip()

    def draw_elements(self):
        pygame.draw.rect(self.screen, BLACK, (230, self.field_size[1] + 10, 50, 50))  # выводим на экран данный уровень
        text_pole1 = self.my_font.render(str(self.level), True, (255, 255, 255))
        self.screen.blit(text_pole1, (250, self.field_size[1] + 24))
        pygame.draw.rect(self.screen, BLACK, (290, self.field_size[1] + 10, 70, 50))  # выводим на экран очки
        text_pole2 = self.my_font.render(str(self.score), True, (255, 255, 255))
        self.screen.blit(text_pole2, (300, self.field_size[1] + 24))

    def draw_life(self):
        if self.life == 1:
            self.geom_life.x = 400
            self.geom_life.y = self.field_size[1] + 10
            self.screen.blit(self.pacman_life, self.geom_life)
        if self.life == 2:
            self.geom_life.x = 400
            self.geom_life.y = self.field_size[1] + 10
            self.screen.blit(self.pacman_life, self.geom_life)
            self.geom_life.x = 460
            self.geom_life.y = self.field_size[1] + 10
            self.screen.blit(self.pacman_life, self.geom_life)
        if self.life == 3:
            self.geom_life.x = 400
            self.geom_life.y = self.field_size[1] + 10
            self.screen.blit(self.pacman_life, self.geom_life)
            self.geom_life.x = 460
            self.geom_life.y = self.field_size[1] + 10
            self.screen.blit(self.pacman_life, self.geom_life)
            self.geom_life.x = 520
            self.geom_life.y = self.field_size[1] + 10
            self.screen.blit(self.pacman_life, self.geom_life)
