import pygame as pg
from pygame.sprite import Sprite, Group

class Barrier(Sprite):
    def __init__(self, size, color, x, y, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.image = pg.Surface((size,size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))
    def update(self):
        self.draw()
    def draw(self):
        self.screen.blit(self.image, self.rect)


class Barriers():
    # shape = ['  xxxxxxx',
    #          ' xxxxxxxxx',
    #          'xxxxxxxxxxx',
    #          'xxxxxxxxxxx',
    #          'xxxxxxxxxxx',
    #          'xxx     xxx',
    #          'xx       xx']
    shape = ['  xxxxxxxxxxxxx',
             ' xxxxxxxxxxxxxxx',
             'xxxxxxxxxxxxxxxxx',
             'xxxxxxxxxxxxxxxxx',
             'xxxxxxxxxxxxxxxxx',
             'xxxxxxxxxxxxxxxxx',
             'xxxxxxxxxxxxxxxxx',
             'xxxxx       xxxxx',
             'xxxx         xxxx',
             'xxx           xxx']
    def __init__(self, game):
        self.shape = Barriers.shape
        self.game = game
        self.settings = game.settings
        self.piece = 12
        self.barriers = Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [num * (self.settings.screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(offset = self.obstacle_x_positions, x_start = self.settings.screen_width / 25, y_start = 600)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.piece + offset_x
                    y = y_start + row_index * self.piece
                    piece = Barrier(self.piece, (241,79,80), x, y, self.game)
                    self.barriers.add(piece)

    def create_multiple_obstacles(self, offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    def reset(self):
        self.barriers.empty()
        self.create_multiple_obstacles(offset = self.obstacle_x_positions, x_start = self.settings.screen_width / 25, y_start = 600)

    def update(self):
        for barrier in self.barriers.sprites():
            barrier.update()

    def draw(self):
        for barrier in self.barriers.sprites():
            barrier.draw()
