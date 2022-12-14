#!/usr/bin/env python3

import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from pause import Pause
from text import TextGroup
from sprites import MazeSprites
import pygame.freetype
from pacman_game import Game

from ui import UIPlain, UIElement
from highscore import get_highscore, set_highscore, write_highscore
from pygame.sprite import Sprite, RenderUpdates
from gamestate import GameState

blinky = pygame.image.load('blinky.png')
blinky = pygame.transform.scale(blinky, (40, 40))
pinky = pygame.image.load('pinky.png')
pinky = pygame.transform.scale(pinky, (40, 40))
inky = pygame.image.load('inky.png')
inky = pygame.transform.scale(inky, (40, 40))
clyde = pygame.image.load('clyde.png')
clyde = pygame.transform.scale(clyde, (40, 40))
pacman = pygame.image.load('pacman.png')
pacman = pygame.transform.scale(pacman, (64, 70))

highscore_file = 'highscores.txt'

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.pause = Pause(True)
        self.score = 0
        self.textgroup = TextGroup()
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.timeloop = 0
        self.timerloop = 14
        self.timer = 0
        self.time = 1
        self.time2 = 2
        self.time3 = 3
        self.time4 = 4
        self.time5 = 5
        self.time6 = 6
        self.time7 = 7
        self.time8 = 8
        self.time9 = 9
        self.time10 = 10
        self.time11 = 11
        self.time12 = 12


    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, 0)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def startGame(self):
        game_state = None
        self.pause.setPause(playerPaused=True)
        self.mazesprites = MazeSprites("maze.txt", "maze_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("maze.txt")
        self.pacman = Pacman(self.nodes.getNodeFromTiles(29, 26), LEFT)
        self.pellets = PelletGroup("pellets.txt")
        self.ghosts = GhostGroup(self.pacman.node, self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(31, 26))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(33, 26))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(35, 26))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(37, 26))
        while True:
            dt = self.clock.tick(30) / 1000.0
            self.timeloop += dt
            if self.timeloop >= self.timerloop:
                main()
            self.textgroup.hideText()
            self.textgroup.update(dt)
            self.pellets.update(dt)
            if not self.pause.paused:
                self.ghosts.update(dt)
                self.checkGhostEvents()
                self.checkPelletEvents()

            if self.pacman.alive:
                if not self.pause.paused:
                    self.pacman.update(dt)
            else:
                self.pacman.update(dt)

            if self.flashBG:
                self.flashTimer += dt
                if self.flashTimer >= self.flashTime:
                    self.flashTimer = 0
                    if self.background == self.background_norm:
                        self.background = self.background_flash
                    else:
                        self.background = self.background_norm

            afterPauseMethod = self.pause.update(dt)
            if afterPauseMethod is not None:
                afterPauseMethod()
            game_state = self.render(dt)
            if game_state == GameState.QUIT:
                return GameState.QUIT
            if game_state == GameState.HIGHSCORE:
                return GameState.HIGHSCORE
            if game_state == GameState.NEWGAME:
                return GameState.NEWGAME
            if game_state == GameState.INSTRUCTION:
                return GameState.INSTRUCTION

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFright()
                self.pacman.direction = RIGHT
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideCharacters()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FRIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.textgroup.addText(str(ghost.points), TEAL, ghost.position.x, ghost.position.y, 15, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showCharacters)
                    self.ghosts.remove(ghost)

    def showCharacters(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideCharacters(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def title(self, dt):
        font = pygame.font.SysFont('freesansbold.ttf', 37)
        blinkyname = font.render("-Shadow", True, RED)
        blinkyname2 = font.render("\"Blinky\"", True, RED)
        pinkyname = font.render("-Speedy", True, PINK)
        pinkyname2 = font.render("\"Pinky\"", True, PINK)
        inkyname = font.render("-Bashful", True, TEAL)
        inkyname2 = font.render("\"Inky\"", True, TEAL)
        clydename = font.render("-Pokey", True, ORANGE)
        clydename2 = font.render("\"Clyde\"", True, ORANGE)
        self.timer += dt
        if self.timer >= self.time:
            self.screen.blit(blinky, (100, 130))
        if self.timer >= self.time2:
            self.screen.blit(blinkyname, (140, 138))
        if self.timer >= self.time3:
            self.screen.blit(blinkyname2, (260, 138))

        if self.timer >= self.time4:
            self.screen.blit(pinky, (100, 175))
        if self.timer >= self.time5:
            self.screen.blit(pinkyname, (140, 183))
        if self.timer >= self.time6:
            self.screen.blit(pinkyname2, (260, 183))

        if self.timer >= self.time7:
            self.screen.blit(inky, (100, 220))
        if self.timer >= self.time8:
            self.screen.blit(inkyname, (140, 228))
        if self.timer >= self.time9:
            self.screen.blit(inkyname2, (260, 228))

        if self.timer >= self.time10:
            self.screen.blit(clyde, (100, 265))
        if self.timer >= self.time11:
            self.screen.blit(clydename, (140, 273))
        if self.timer >= self.time12:
            self.screen.blit(clydename2, (260, 273))

    def render(self, dt):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(pacman, (143, 45))
        self.title(dt)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)
        self.textgroup.showText(TENPOINTTXT)
        self.textgroup.showText(FIFTYPOINTTXT)
        self.textgroup.showText(PACMANTXT)

        start_btn = UIElement(center_position=(120, 370), font_size=24, text_rgb=WHITE, text="PLAY GAME", action=GameState.NEWGAME)
        score_btn = UIElement(center_position=(340, 370), font_size=24, text_rgb=WHITE, text="HIGH SCORES", action=GameState.HIGHSCORE)
        instruction_btn = UIElement(center_position=(235, 550), font_size=24, text_rgb=WHITE, text="Instructions", action=GameState.INSTRUCTION)
        buttons = RenderUpdates(start_btn, score_btn, instruction_btn)

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

        buttons.draw(self.screen)

        pygame.display.update()

    def highscore(self, file_name):
        scores = get_highscore(file_name)
        title =  UIPlain(center_position = (225, 50), font_size = 25, text_rgb = WHITE, text = "Highscores")
        first =  UIPlain(center_position = (225, 150), font_size = 30, text_rgb = WHITE, text = '1st: ' + scores.get('high')[0])
        second =  UIPlain(center_position = (225, 200), font_size = 30, text_rgb = WHITE, text = '2nd: ' + scores.get('mid')[0])
        third =  UIPlain(center_position = (225, 250), font_size = 30, text_rgb = WHITE, text = '3rd: ' + scores.get('low')[0])
        fourth = UIPlain(center_position = (225, 300), font_size = 30, text_rgb = WHITE, text = '4th: ' + scores.get('lowest')[0])
        menu_btn = UIElement(center_position=(90, 550), font_size=25, text_rgb= WHITE, text="Main Menu", action=GameState.TITLE)
        buttons = RenderUpdates(menu_btn, title, first, second, third, fourth)
        while True:
            self.screen.blit(self.background, (0, 0))
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
            buttons.draw(self.screen)
            pygame.display.flip()

    def instruction(self):
        first =  UIPlain(center_position = (225, 150), font_size = 30, text_rgb = WHITE, text = 'Arrow keys = Movement')
        second =  UIPlain(center_position = (225, 200), font_size = 30, text_rgb = WHITE, text = 'Q Key = Orange Portal')
        third =  UIPlain(center_position = (225, 250), font_size = 30, text_rgb = WHITE, text = 'E Key = Blue Portal')
        menu_btn = UIElement(center_position=(90, 550), font_size=25, text_rgb= WHITE, text="Main Menu", action=GameState.TITLE)
        buttons = RenderUpdates(menu_btn, first, second, third)
        while True:
            self.screen.blit(self.background, (0, 0))
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
            buttons.draw(self.screen)
            pygame.display.flip()


def main():
    game_state = GameState.TITLE
    g = GameController()
    tg = Game()

    while True:
        if game_state == GameState.TITLE:
            game_state = g.startGame()

        if game_state == GameState.NEWGAME:
            game_state = tg.update()

        if game_state == GameState.HIGHSCORE:
            game_state = g.highscore(highscore_file)

        if game_state == GameState.INSTRUCTION:
            game_state = g.instruction()

        if game_state == GameState.QUIT:
            pygame.quit()
            return

if __name__ == "__main__":
    main()
