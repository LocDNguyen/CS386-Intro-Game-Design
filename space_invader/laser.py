import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer
from random import randint

class Lasers:
    def __init__(self, game):
        self.game = game
        self.lasers = Group()
        self.settings = game.settings
        self.screen = game.screen
        self.sound = game.sound
        self.barriers = game.barriers.barriers
    def reset(self):
        self.lasers.empty()
    def shoot(self, ship):
        self.lasers.add(Laser(settings=self.settings, screen=self.screen, ship=ship, sound=self.sound))
        for laser in self.lasers:
            if pg.sprite.spritecollide(laser, self.barriers, True):
                self.lasers.remove(laser)
    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.bottom <= 0: self.lasers.remove(laser)
    def draw(self):
        for laser in self.lasers.sprites(): laser.draw()

class Laser(Sprite):
    """A class to manage lasers fired from the ship"""

    def __init__(self, settings, screen, ship, sound):
        super().__init__()
        self.screen = screen
        self.image = pg.image.load(f'images/ship/shoot/shoot0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.bottom = ship.rect.top
        self.y = float(self.rect.y)
        self.image_animation = [pg.image.load(f'images/ship/shoot/shoot{n}.png').convert_alpha() for n in range(4)]
        self.speed_factor = settings.laser_speed_factor

        self.timer = Timer(image_list=self.image_animation)
        sound.shoot_laser()
    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y
        self.draw()
    def draw(self):
        image = self.timer.image()
        rect = self.image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
