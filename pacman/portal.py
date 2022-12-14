import pygame
from pygame.locals import *
from vector import Vector
from constants import *
from character import Character
from sprites import PortalSprites, PortalSprites2

class Portal(Character):
    def __init__(self, node, color, direction=STOP, pacman=None):
        Character.__init__(self, node)
        self.name = PORTAL
        self.pacman = pacman
        self.direction = direction
        self.direction2 = self.direction
        self.color = GREEN
        self.alive = False
        if color == "orange":
            self.sprites = PortalSprites(self)
        else:
            self.sprites = PortalSprites2(self)
        self.num = 0

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False

    def place(self, node):
        self.alive = True
        if self.direction2 != STOP:
            self.setNextNode(self.direction2)

    def reset(self):
        Character.reset(self)
        self.direction = None
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction2]*200*dt
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(self.direction2)
            # if self.target is not self.node:
            #     self.direction2 = self.direction2
            # else:
            #     self.target = self.getNewTarget(self.direction2)
            if self.node.neighbors[self.direction2] == None:#if self.target is self.node:
                # print(self.target)
                # print(self.node)
                # print(self.num)
                self.direction = STOP
            self.setPosition()
