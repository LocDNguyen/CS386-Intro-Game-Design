import pygame
from constants import *
import numpy as np
from animation import Animator

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritesheet3.png").convert()
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * 28.5)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * 32)
        self.sheet = pygame.transform.scale(self.sheet, (width, height))

        self.sheet2 = pygame.image.load("spritesheet2.png").convert()
        transcolor = self.sheet2.get_at((0,0))
        self.sheet2.set_colorkey(transcolor)
        width = int(self.sheet2.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet2.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet2 = pygame.transform.scale(self.sheet2, (width, height))

    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

    def getImage2(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet2.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet2.subsurface(self.sheet2.get_clip())

class PacmanSprites(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.character = character
        self.character.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((8,0), (0, 0), (0, 2), (0, 0)))
        self.animations[RIGHT] = Animator(((10,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10,2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8,2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)

    def update(self, dt):
        if self.character.alive == True:
            if self.character.direction == LEFT:
                self.character.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (0, 0)
            elif self.character.direction == RIGHT:
                self.character.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (2, 0)
            elif self.character.direction == DOWN:
                self.character.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (4, 0)
            elif self.character.direction == UP:
                self.character.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (6, 0)
            elif self.character.direction == STOP:
                self.character.image = self.getImage(*self.stopimage)
        else:
            self.character.image = self.getImage(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage2(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class PortalSprites(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.rshot = pygame.image.load('portal_shot_1.png')
        self.rshot = pygame.transform.scale(self.rshot, (32, 32))
        self.lshot = pygame.transform.rotate(self.rshot, 180)
        self.ushot = pygame.transform.rotate(self.rshot, 90)
        self.dshot = pygame.transform.rotate(self.rshot, 270)
        self.stop1 = pygame.image.load('portal_entrance_1_1.png')
        self.stop1 = pygame.transform.scale(self.stop1, (32, 32))
        self.stop2 = pygame.image.load('portal_entrance_1_2.png')
        self.stop2 = pygame.transform.scale(self.stop2, (32, 32))
        self.stop3 = pygame.image.load('portal_entrance_1_3.png')
        self.stop3 = pygame.transform.scale(self.stop3, (32, 32))
        self.stop4 = self.stop3
        self.stop4 = pygame.transform.rotate(self.stop4, 90)
        self.character = character
        self.character.image = self.stop1
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (5, 0)

    def defineAnimations(self):
        self.animations[LEFT] = Animator((self.lshot, self.lshot))
        self.animations[RIGHT] = Animator((self.rshot, self.rshot))
        self.animations[UP] = Animator((self.ushot, self.ushot))
        self.animations[DOWN] = Animator((self.dshot, self.dshot))
        self.animations[STOP] = Animator((self.stop1, self.stop2, self.stop3), loop=False)
        self.animations[STOP2] = Animator((self.stop1, self.stop2, self.stop4), loop=False)

    def update(self, dt):
        if self.character.direction == LEFT:
            self.character.image = self.animations[LEFT].update(dt)
        if self.character.direction == RIGHT:
            self.character.image = self.animations[RIGHT].update(dt)
        if self.character.direction == DOWN:
            self.character.image = self.animations[DOWN].update(dt)
        if self.character.direction == UP:
            self.character.image = self.animations[UP].update(dt)
        if self.character.direction == STOP and self.character.direction2 == LEFT or self.character.direction == STOP and self.character.direction2 == RIGHT:
            self.character.image = self.animations[STOP].update(dt)
        if self.character.direction == STOP and self.character.direction2 == UP or self.character.direction == STOP and self.character.direction2 == DOWN:
            self.character.image = self.animations[STOP2].update(dt)

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage2(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class PortalSprites2(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.rshot = pygame.image.load('portal_shot_2.png')
        self.rshot = pygame.transform.scale(self.rshot, (32, 32))
        self.lshot = pygame.transform.rotate(self.rshot, 180)
        self.ushot = pygame.transform.rotate(self.rshot, 90)
        self.dshot = pygame.transform.rotate(self.rshot, 270)
        self.stop1 = pygame.image.load('portal_entrance_2_1.png')
        self.stop1 = pygame.transform.scale(self.stop1, (32, 32))
        self.stop2 = pygame.image.load('portal_entrance_2_2.png')
        self.stop2 = pygame.transform.scale(self.stop2, (32, 32))
        self.stop3 = pygame.image.load('portal_entrance_2_3.png')
        self.stop3 = pygame.transform.scale(self.stop3, (32, 32))
        self.stop4 = self.stop3
        self.stop4 = pygame.transform.rotate(self.stop4, 90)
        self.character = character
        self.character.image = self.stop1
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (5, 0)

    def defineAnimations(self):
        self.animations[LEFT] = Animator((self.lshot, self.lshot))
        self.animations[RIGHT] = Animator((self.rshot, self.rshot))
        self.animations[UP] = Animator((self.ushot, self.ushot))
        self.animations[DOWN] = Animator((self.dshot, self.dshot))
        self.animations[STOP] = Animator((self.stop1, self.stop2, self.stop3), loop=False)
        self.animations[STOP2] = Animator((self.stop1, self.stop2, self.stop4), loop=False)

    def update(self, dt):
        if self.character.direction == LEFT:
            self.character.image = self.animations[LEFT].update(dt)
        if self.character.direction == RIGHT:
            self.character.image = self.animations[RIGHT].update(dt)
        if self.character.direction == DOWN:
            self.character.image = self.animations[DOWN].update(dt)
        if self.character.direction == UP:
            self.character.image = self.animations[UP].update(dt)
        if self.character.direction == STOP and self.character.direction2 == LEFT or self.character.direction == STOP and self.character.direction2 == RIGHT:
            self.character.image = self.animations[STOP].update(dt)
        if self.character.direction == STOP and self.character.direction2 == UP or self.character.direction == STOP and self.character.direction2 == DOWN:
            self.character.image = self.animations[STOP2].update(dt)

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()

    def getStartImage(self):
        return self.getImage(8, 0)

    def getImage(self, x, y):
        return Spritesheet.getImage2(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class GhostSprites(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        self.character = character
        self.character.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()

    def defineAnimations(self):
        self.animations[FRIGHT] = Animator(((14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (18.1, 8), (18.1, 8), (19.9, 8), (19.9, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (18.1, 8), (18.1, 8), (19.9, 8), (19.9, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (18.1, 8), (18.1, 8), (19.9, 8), (19.9, 8),
        (14.5, 8), (14.5, 8), (16.3, 8), (16.3, 8), (18.1, 8), (18.1, 8), (19.9, 8), (19.9, 8)))

        self.animations[BLEFT] = Animator(((3.85, 8), (3.85, 8), (5.6, 8), (5.6, 8)))
        self.animations[BRIGHT] = Animator(((.2, 8), (.2, 8), (2.1, 8), (2.1, 8)))
        self.animations[BUP] = Animator(((7.40, 8), (7.40, 8), (9.15, 8), (9.15, 8)))
        self.animations[BDOWN] = Animator(((10.95, 8), (10.95, 8), (12.7, 8), (12.7, 8)))

        self.animations[PLEFT] = Animator(((3.85, 10), (3.85, 10), (5.6, 10), (5.6, 10)))
        self.animations[PRIGHT] = Animator(((.2, 10), (.2, 10), (2.1, 10), (2.1, 10)))
        self.animations[PUP] = Animator(((7.40, 10), (7.40, 10), (9.15, 10), (9.15, 10)))
        self.animations[PDOWN] = Animator(((10.95, 10), (10.95, 10), (12.7, 10), (12.7, 10)))

        self.animations[ILEFT] = Animator(((3.85, 12), (3.85, 12), (5.6, 12), (5.6, 12)))
        self.animations[IRIGHT] = Animator(((.2, 12), (.2, 12), (2.1, 12), (2.1, 12)))
        self.animations[IUP] = Animator(((7.40, 12), (7.40, 12), (9.15, 12), (9.15, 12)))
        self.animations[IDOWN] = Animator(((10.95, 12), (10.95, 12), (12.7, 12), (12.7, 12)))

        self.animations[CLEFT] = Animator(((3.85, 14), (3.85, 14), (5.6, 14), (5.6, 14)))
        self.animations[CRIGHT] = Animator(((.2, 14), (.2, 14), (2.1, 14), (2.1, 14)))
        self.animations[CUP] = Animator(((7.40, 14), (7.40, 14), (9.15, 14), (9.15, 14)))
        self.animations[CDOWN] = Animator(((10.95, 14), (10.95, 14), (12.7, 14), (12.7, 14)))

    def update(self, dt):
        if self.character.mode.current in [SCATTER, CHASE]:
            if self.character.name == 4:
                if self.character.direction == LEFT:
                    self.character.image = self.getImage(*self.animations[BLEFT].update(dt))
                elif self.character.direction == RIGHT:
                    self.character.image = self.getImage(*self.animations[BRIGHT].update(dt))
                elif self.character.direction == DOWN:
                    self.character.image = self.getImage(*self.animations[BDOWN].update(dt))
                elif self.character.direction == UP:
                    self.character.image = self.getImage(*self.animations[BUP].update(dt))
            if self.character.name == 5:
                if self.character.direction == LEFT:
                    self.character.image = self.getImage(*self.animations[PLEFT].update(dt))
                elif self.character.direction == RIGHT:
                    self.character.image = self.getImage(*self.animations[PRIGHT].update(dt))
                elif self.character.direction == DOWN:
                    self.character.image = self.getImage(*self.animations[PDOWN].update(dt))
                elif self.character.direction == UP:
                    self.character.image = self.getImage(*self.animations[PUP].update(dt))
            if self.character.name == 6:
                if self.character.direction == LEFT:
                    self.character.image = self.getImage(*self.animations[ILEFT].update(dt))
                elif self.character.direction == RIGHT:
                    self.character.image = self.getImage(*self.animations[IRIGHT].update(dt))
                elif self.character.direction == DOWN:
                    self.character.image = self.getImage(*self.animations[IDOWN].update(dt))
                elif self.character.direction == UP:
                    self.character.image = self.getImage(*self.animations[IUP].update(dt))
            if self.character.name == 7:
                if self.character.direction == LEFT:
                    self.character.image = self.getImage(*self.animations[CLEFT].update(dt))
                elif self.character.direction == RIGHT:
                    self.character.image = self.getImage(*self.animations[CRIGHT].update(dt))
                elif self.character.direction == DOWN:
                    self.character.image = self.getImage(*self.animations[CDOWN].update(dt))
                elif self.character.direction == UP:
                    self.character.image = self.getImage(*self.animations[CUP].update(dt))
        elif self.character.mode.current == FRIGHT:
            self.character.image = self.getImage(*self.animations[FRIGHT].update(dt))
        elif self.character.mode.current == SPAWN:
            if self.character.direction == LEFT:
                self.character.image = self.getImage2(8, 8)
            elif self.character.direction == RIGHT:
                self.character.image = self.getImage2(8, 10)
            elif self.character.direction == DOWN:
                self.character.image = self.getImage2(8, 6)
            elif self.character.direction == UP:
               self.character.image = self.getImage2(8, 4)

    def getStartImage(self):
        if self.character.name == 4:
            return self.getImage(3.85, 8)
        if self.character.name == 5:
            return self.getImage(10.95, 10)
        if self.character.name == 6:
            return self.getImage(7.4, 12)
        if self.character.name == 7:
            return self.getImage(7.4, 14)

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()
        self.character.image = self.getStartImage()
        self.character.mode.current = CHASE

    def resetFright(self):
        self.animations[FRIGHT].reset()

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    def getImage2(self, x, y):
        return Spritesheet.getImage2(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class FruitSprites(Spritesheet):
    def __init__(self, character):
        Spritesheet.__init__(self)
        self.character = character
        self.character.image = self.getStartImage()

    def getStartImage(self):
        return self.getImage2(16, 8)

    def getNumImage(self):
        return self.getImage(.2, 16)

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    def getImage2(self, x, y):
        return Spritesheet.getImage2(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class LifeSprites(Spritesheet):
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) > 0:
            self.images.pop(0)

    def addImage(self):
        self.images.append(self.getImage(0,0))

    def resetLives(self, numlives):
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))

    def getImage(self, x, y):
        return Spritesheet.getImage2(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class MazeSprites(Spritesheet):
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y):
        return Spritesheet.getImage2(self, x, y, TILEWIDTH, TILEHEIGHT)

    def readMazeFile(self, mazefile):
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y):
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background

    def rotate(self, sprite, value):
        return pygame.transform.rotate(sprite, value*90)
