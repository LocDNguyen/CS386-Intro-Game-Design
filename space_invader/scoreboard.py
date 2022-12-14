import pygame as pg
from highscore import get_highscore

class Scoreboard:
    def __init__(self, game):
        self.score = 0
        self.level = 1
        self.high_score = 0

        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 35)

        self.score_image = None
        self.score_rect = None
        self.prep_score()

    def prep_score(self):
        score_str = str(self.score)
        self.score_image = self.font.render("Score: " + score_str, True, self.text_color)

        level_str = str(self.level)
        self.level_image = self.font.render("Level: " + level_str, True, self.text_color)

        scores = get_highscore('highscores.txt')
        highscore_str = str(scores.get('high')[0])
        self.highscore_image = self.font.render("High score: " + highscore_str, True, self.text_color)

    def reset(self):
        self.score = 0
        self.level = 0
        self.update()

    def update(self):
        self.draw()

    def draw(self):
        self.screen.blit(self.score_image, (1060, 10))
        self.screen.blit(self.level_image, (1064, 40))
        self.screen.blit(self.highscore_image, (self.screen_rect.centerx - 90, 10))
