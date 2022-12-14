#!/usr/bin/env python3

import pygame as pg
import pygame.freetype
from settings import Settings
import game_functions as gf
from pygame.sprite import Sprite, RenderUpdates
from gamestate import GameState

from laser import Lasers
from alien import Aliens
from big_alien import One
from alien_laser import Alien_lasers
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from barrier import Barriers
from ui import UIPlain, UIElement
from highscore import get_highscore, set_highscore, write_highscore
import sys

pg.init()

screen = pg.display.set_mode((Settings().screen_width, Settings().screen_height))

mainscreen = pygame.image.load('images/mainscreen2.png')
mainscreen = pygame.transform.scale(mainscreen, (Settings().screen_width, Settings().screen_height))

blue_alien = pygame.image.load('images/blue/blue_alien0.png')
blue_alien = pygame.transform.scale(blue_alien, (64, 64))
pink_alien = pygame.image.load('images/pink/pink_alien0.png')
pink_alien = pygame.transform.scale(pink_alien, (64, 55))
green_alien = pygame.image.load('images/green/green_alien0.png')
red_alien = pygame.image.load('images/red/red_alien0.png')
red_alien = pygame.transform.scale(red_alien, (100, 50))

highscore_file = 'highscores.txt'


def game_loop(screen, buttons):
    while True:
        screen.blit(mainscreen, (0,0))
        screen.blit(blue_alien, (500, 340))
        screen.blit(green_alien, (500, 400))
        screen.blit(pink_alien, (500, 450))
        screen.blit(red_alien, (481, 520))

        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.QUIT:
                return GameState.QUIT

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action

        buttons.draw(screen)
        pygame.display.flip()

def title_screen(screen):
    title =  UIPlain(center_position = (600, 160), font_size = 160, text_rgb = Settings().WHITE, text = "SPACE")
    title_2 =  UIPlain(center_position = (600, 260), font_size = 90, text_rgb = Settings().GREEN, text = "INVADERS")
    score1 =  UIPlain(center_position = (650, 360), font_size = 30, text_rgb = Settings().WHITE, text = "= 10 PTS")
    score2 =  UIPlain(center_position = (650, 420), font_size = 30, text_rgb = Settings().WHITE, text = "= 20 PTS")
    score3 =  UIPlain(center_position = (650, 480), font_size = 30, text_rgb = Settings().WHITE, text = "= 40 PTS")
    score4 =  UIPlain(center_position = (650, 540), font_size = 30, text_rgb = Settings().WHITE, text = "= ???")
    start_btn = UIElement(center_position=(600, 650), font_size=30, text_rgb=Settings().GREEN, text="PLAY GAME", action=GameState.NEWGAME)
    score_btn = UIElement(center_position=(600, 720), font_size=30, text_rgb=Settings().WHITE, text="HIGH SCORES", action=GameState.HIGHSCORE)
    buttons = RenderUpdates(start_btn, score_btn, title, title_2, score1, score2, score3, score4)
    return game_loop(screen, buttons)

def highscore(file_name):
    scores = get_highscore(file_name)
    title =  UIPlain(center_position = (600, 200), font_size = 50, text_rgb = Settings().WHITE, text = "Highscores")
    first =  UIPlain(center_position = (660, 360), font_size = 30, text_rgb = Settings().WHITE, text = '1st: ' + scores.get('high')[0])
    second =  UIPlain(center_position = (660, 420), font_size = 30, text_rgb = Settings().WHITE, text = '2nd: ' + scores.get('mid')[0])
    third =  UIPlain(center_position = (660, 480), font_size = 30, text_rgb = Settings().WHITE, text = '3rd: ' + scores.get('low')[0])
    fourth = UIPlain(center_position = (660, 540), font_size = 30, text_rgb = Settings().WHITE, text = '4th: ' + scores.get('lowest')[0])
    menu_btn = UIElement(center_position=(130, 750), font_size=25, text_rgb=Settings().WHITE, text="Main Menu", action=GameState.TITLE)
    buttons = RenderUpdates(menu_btn, title, first, second, third, fourth)
    return game_loop(screen, buttons)

class Game:
    def __init__(self):
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self)

        self.barriers = Barriers(game=self)
        self.ship_lasers = Lasers(game=self)
        self.ship = Ship(game=self)
        self.alien_lasers = Alien_lasers(game=self)
        self.aliens = Aliens(game=self, alien_lasers=self.alien_lasers)
        self.big_alien = One(game=self)
        self.settings.initialize_speed_settings()

    def reset(self):
        print('Resetting game...')
        self.barriers.reset()
        self.ship.reset()
        self.aliens.reset()
        self.big_alien.reset()
        # self.scoreboard.reset()

    def game_over(self):
        print('All ships gone: game over!')
        set_highscore(highscore_file, self.scoreboard.score)
        self.sound.gameover()

    def play(self):
        self.sound.play_bg()
        clock = pg.time.Clock()
        fps = 60
        game_state = None
        while True:
            #screen.blit(mainscreen, (0,0))
            self.screen.fill(self.settings.bg_color)
            gf.check_events(settings=self.settings, ship=self.ship)
            game_state = self.ship.update()
            self.aliens.update()
            self.big_alien.update()
            self.barriers.update()
            self.scoreboard.update()
            pg.display.flip()
            clock.tick(fps)
            if game_state == GameState.TITLE:
                return GameState.TITLE


def main():
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            g = Game()
            game_state = g.play()

        if game_state == GameState.HIGHSCORE:
            game_state = highscore(highscore_file)

        if game_state == GameState.QUIT:
            pygame.quit()
            return


if __name__ == '__main__':
    main()
