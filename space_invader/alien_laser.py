import pygame as pg
from pygame.sprite import Sprite, Group
from timer import Timer
from random import randint

class Alien_lasers:
    def __init__(self, game):
        self.game = game
        self.lasers = Group()
        self.ship_lasers = game.ship_lasers.lasers
        self.settings = game.settings
        self.screen = game.screen
        self.sound = game.sound
        self.ship = game.ship
        self.last_enemy_shot = pg.time.get_ticks()
        self.cooldown = 1000
        self.barriers = game.barriers.barriers
    def reset(self):
        self.lasers.empty()
    def shoot(self, alien):
        time_now = pg.time.get_ticks()
        if time_now - self.last_enemy_shot > self.cooldown and len(self.lasers) < 1:
            self.lasers.add(Alien_Laser(game=self, alien=alien))
            self.last_enemy_shot = pg.time.get_ticks()
        if pg.sprite.spritecollide(self.ship, self.lasers, True):
            self.ship.die()
        for laser in self.lasers:
            if pg.sprite.spritecollide(laser, self.ship_lasers, True):
                self.lasers.remove(laser)
            if pg.sprite.spritecollide(laser, self.barriers, True):
                self.lasers.remove(laser)
    def update(self):
        self.lasers.update()
        for laser in self.lasers.copy():
            if laser.rect.top >= self.settings.screen_height: self.lasers.remove(laser)
    def draw(self):
        for laser in self.lasers.sprites(): laser.draw()

class Alien_Laser(Sprite):
    """A class to manage lasers fired from the aliens"""
    def __init__(self, game, alien):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.image = pg.image.load(f'images/blue/shoot/shoot0.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = alien.rect.centerx
        self.rect.top = alien.rect.bottom
        if alien.type == 'blue':
            self.image_animation = [pg.image.load(f'images/blue/shoot/shoot{n}.png').convert_alpha() for n in range(4)]
        elif alien.type == 'green':
            self.image_animation = [pg.image.load(f'images/green/shoot/shoot{n}.png').convert_alpha() for n in range(4)]
        else:
            self.image_animation = [pg.image.load(f'images/pink/shoot/shoot{n}.png').convert_alpha() for n in range(4)]
        self.y = float(self.rect.y)
        self.speed_factor = self.settings.laser_speed_factor

        self.timer = Timer(image_list=self.image_animation, delay=50)
        self.sound.shoot_laser()
    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y
        self.draw()
    def draw(self):
        image = self.timer.image()
        rect = self.image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
