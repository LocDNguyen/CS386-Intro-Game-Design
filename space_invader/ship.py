import pygame as pg
from pygame.sprite import Sprite
from laser import Lasers
from game_functions import clamp
from vector import Vector
from sys import exit
from gamestate import GameState
from timer import Timer


class Ship(Sprite):
    ship_image = [pg.image.load(f'images/ship/ship{n}.png') for n in range(1)]
    ship_explosion_images = [pg.image.load(f'images/ship/explosion{n}.png') for n in range(13)]

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sound = game.sound
        self.barriers = game.barriers.barriers
        self.ships_left = game.settings.ship_limit
        self.image = pg.image.load('images/ship/ship0.png')
        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
        self.posn = self.center_ship()
        self.vel = Vector()

        self.dying = self.dead = False

        self.timer_normal = Timer(image_list=self.ship_image, delay=500)
        self.timer_explosion = Timer(image_list=self.ship_explosion_images, is_loop=False)
        self.timer = self.timer_normal

        self.live_image = pg.image.load('images/ship/ship0.png')

        self.last_shot = pg.time.get_ticks()
        self.cooldown = 1000

        self.lasers = game.ship_lasers

        self.shooting = False
    def center_ship(self):
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        return Vector(self.rect.left, self.rect.top)
    def reset(self):
        self.vel = Vector()
        self.posn = self.center_ship()
        self.lasers.reset()
        self.dying = self.dead = False
        self.rect.left, self.rect.top = self.posn.x, self.posn.y
        self.timer_normal = Timer(image_list=self.ship_image, delay=500)
        self.timer_explosion = Timer(image_list=self.ship_explosion_images, is_loop=False)
        self.timer = self.timer_normal
    def die(self):
        if not self.dying:
            self.dying = True
            self.dead = True
            self.timer = self.timer_explosion
            self.ships_left -= 1
            print(f'Ship is dead! Only {self.ships_left} ships left')
    def update(self):
        self.speed = self.settings.ship_speed_factor
        if self.dead:
            self.speed *= 0
            if self.timer == self.timer_explosion and self.timer.is_expired() and self.ships_left > 0:
                self.reset()

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if (keys[pg.K_RIGHT] and self.rect.right < self.settings.screen_width):
            self.rect.x += self.speed
        if keys[pg.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if (keys[pg.K_DOWN] and self.rect.bottom < self.settings.screen_height):
            self.rect.y += self.speed

        time_now = pg.time.get_ticks()
        if keys[pg.K_SPACE] and time_now - self.last_shot > self.cooldown:
            self.lasers.shoot(ship=self)
            self.last_shot = pg.time.get_ticks()

        if self.ships_left <= 0:
            self.game.game_over()
            return GameState.TITLE

        if pg.sprite.spritecollide(self, self.barriers, False):
            self.die()

        self.lasers.update()
        self.draw()


    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)
        for live in range(self.ships_left - 1):
            x = 5 + (live * (self.live_image.get_size()[0] + 10))
            self.screen.blit(self.live_image, (x, 8))
