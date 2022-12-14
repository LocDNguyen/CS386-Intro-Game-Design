import pygame
from character import Character
from constants import *
from sprites import FruitSprites

class Fruit(Character):
    def __init__(self, node):
        Character.__init__(self, node)
        self.name = FRUIT
        self.color = GREEN
        self.lifespan = 10
        self.timer = 0
        self.destroy = False
        self.points = 100
        self.sprites = FruitSprites(self)
        self.setBetweenNodes(RIGHT)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifespan:
            self.destroy = True
