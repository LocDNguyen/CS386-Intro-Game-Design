import pygame as pg
from pygame.sprite import Sprite, Group
from laser import Lasers
from timer import Timer
from random import randint, choice


class The_one(Sprite):
    alien_images = [pg.transform.rotozoom(pg.image.load(f'images/red/red_alien{n}.png'), 0, 2) for n in range(2)]
    alien_explosion0_images = [pg.transform.rotozoom(pg.image.load(f'images/red/explode0/explode{n}.png'), 0, 2) for n in range(18)]
    alien_explosion100_images = [pg.transform.rotozoom(pg.image.load(f'images/red/explode100/explode{n}.png'), 0, 2) for n in range(18)]
    alien_explosion300_images = [pg.transform.rotozoom(pg.image.load(f'images/red/explode300/explode{n}.png'), 0, 2) for n in range(18)]

    def __init__(self, game, x, speed, sound, score):
        super().__init__()
        self.game = game
        self.screen = game.screen
        self.settings = game.settings
        self.sb = game.scoreboard
        self.sound = game.sound
        self.image = pg.image.load(f'images/red/red_alien0.png')
        self.rect = self.image.get_rect(topleft = (x,8))
        self.speed = speed
        self.score = score

        self.dying = self.dead = False

        if self.score == '100':
            self.timer_normal = Timer(image_list=self.alien_images, delay=800)
            self.timer_explosion = Timer(image_list=self.alien_explosion100_images, delay=90, is_loop=False)
            self.timer = self.timer_normal
        elif self.score == '300':
            self.timer_normal = Timer(image_list=self.alien_images, delay=800)
            self.timer_explosion = Timer(image_list=self.alien_explosion300_images, delay=90, is_loop=False)
            self.timer = self.timer_normal
        else:
            self.timer_normal = Timer(image_list=self.alien_images, delay=800)
            self.timer_explosion = Timer(image_list=self.alien_explosion0_images, delay=90, is_loop=False)
            self.timer = self.timer_normal
        print(self.score)
        self.sound.big_alien_move()
    def check_edge(self):
        return self.rect.left >= self.settings.screen_width + 200 or self.rect.right < -150
    def hit(self):
        if not self.dying:
            self.dying = True
            self.timer = self.timer_explosion
            self.sound.big_alien_stop()
            if self.score == '100':
                self.sb.score += 100
                self.sb.prep_score()
            elif self.score == '300':
                self.sb.score += 300
                self.sb.prep_score()
    def update(self):
        settings = self.settings
        if self.timer == self.timer_explosion and self.timer.is_expired():
            self.kill()
        self.rect.x += self.speed
        self.draw()
    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.left, rect.top = self.rect.left, self.rect.top
        self.screen.blit(image, rect)

class One():
    def __init__(self, game):
        self.game = game
        self.sound = game.sound
        self.alien = Group()
        self.ship_lasers = game.ship_lasers.lasers
        self.screen = game.screen
        self.settings = game.settings
        self.extra_spawn_time = randint(40,80)
        self.extra_alien_timer()
    def reset(self):
        self.alien.empty()
        self.sound.big_alien_stop()
        self.extra_alien_timer()
    def create_big_alien(self, side):
        self.speed = self.settings.big_alien_speed_factor
        if side == 'right':
            x = self.settings.screen_width + 1
            self.speed *= -1
        else:
            x = -150
        if len(self.alien) < 1:
            alien = The_one(game=self.game, x=x, speed=self.speed, sound=self.sound, score=choice(['0', '100', '300']))
            self.alien.add(alien)
    def check_alien_edge(self):
        for alien in self.alien.sprites():
            if alien.check_edge():
                self.alien.remove(alien)
    def check_collision(self):
        collisions = pg.sprite.groupcollide(self.alien, self.ship_lasers, False, True)
        if collisions:
            for alien in collisions:
                alien.hit()
    def update(self):
        self.check_alien_edge()
        self.extra_alien_timer()
        self.check_collision()
        for alien in self.alien.sprites():
            if alien.dead:
                alien.remove()
            alien.update()
    def draw(self):
        for alien in self.alien.sprites():
            alien.draw()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.create_big_alien(choice(['right','left']))
            self.extra_spawn_time = randint(400,800)
