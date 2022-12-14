
import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import GhostGroup
from fruit import Fruit
from pause import Pause
from text import TextGroup
from sprites import LifeSprites, MazeSprites
from portal import Portal
from gamestate import GameState


class Game(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.lives = 3
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.show = 1
        self.show2 = 1

    def restartGame(self):
        self.lives = 3
        self.pause.paused = True
        self.fruit = None
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.startGame()

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.nodes.denyHomeAccessList(self.ghosts)
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def nextLevel(self):
        self.showCharacters()
        self.pause.paused = True
        self.startGame()

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, 0)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def update(self):
        self.mazesprites = MazeSprites("maze_level1.txt", "maze_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup("maze_level1.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        homekey = self.nodes.createHomeNodes(11.5, 14)
        self.nodes.connectHomeNodes(homekey, (12, 14), LEFT)
        self.nodes.connectHomeNodes(homekey, (15, 14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(14, 26), LEFT)
        self.portal = Portal(self.pacman.node, "orange", STOP, self.pacman)
        self.portal2 = Portal(self.pacman.node, "blue", STOP, self.pacman)
        self.pellets = PelletGroup("pellets_level1.txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14))
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14))
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts)
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)
        while True:
            dt = self.clock.tick(30) / 1000.0
            self.textgroup.update(dt)
            self.pellets.update(dt)
            self.portal.update(dt)
            self.portal2.update(dt)
            if not self.pause.paused:
                self.ghosts.update(dt)
                if self.fruit is not None:
                    self.fruit.update(dt)
                self.checkGhostEvents()
                self.checkPelletEvents()
                self.checkFruitEvents()

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
                if afterPauseMethod == GameState.TITLE:
                    return GameState.TITLE
                afterPauseMethod()
            self.checkEvents()
            self.render()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            if self.score%2000 == 0:
                self.lives += 1
                self.lifesprites.addImage()
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFright()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideCharacters()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showCharacters()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            self.hideCharacters()

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FRIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    self.textgroup.addText(str(ghost.points), TEAL, ghost.position.x, ghost.position.y, 15, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showCharacters)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -= 1
                        self.lifesprites.removeImage()
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=GameState.TITLE)
                        else:
                            self.show = 1
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def showCharacters(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideCharacters(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(13, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), PINK, self.fruit.position.x, self.fruit.position.y, 15, time=1)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.show = 0
            if self.portal.direction == STOP:
                self.portal = Portal(self.pacman.node, "orange", self.pacman.direction, self.pacman)
                self.portal.render(self.screen)
        if self.show == 0:
            self.portal.place(self.portal.node)
            self.portal.render(self.screen)

        if keys[pygame.K_e]:
            self.show2 = 0
            if self.portal2.direction == STOP:
                self.portal2 = Portal(self.pacman.node, "blue", self.pacman.direction, self.pacman)
        if self.show2 == 0:
            self.portal2.place(self.portal2.node)
            self.portal2.render(self.screen)

        if self.show == 0 and self.show2 == 0 and self.portal.direction == STOP and self.portal2.direction == STOP:
            self.nodes.setPortalPair2((self.portal.position.x, self.portal.position.y), (self.portal2.position.x, self.portal2.position.y))

        if self.fruit is not None:
            self.fruit.render(self.screen)

        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        pygame.display.update()

# def main():
#     game = GameController()
#     game.startGame()
#     while True:
#         game.update()
#
# if __name__ == "__main__":
#     main()
