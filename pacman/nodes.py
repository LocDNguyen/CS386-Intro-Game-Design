import pygame
from vector import Vector
from constants import *
import numpy


class Node(object):
    def __init__(self, x, y):
        self.position = Vector(x,y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL:None, STOP:None, PORTAL2:None}
        self.access = {UP:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       DOWN:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       LEFT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT],
                       RIGHT:[PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    def denyAccess(self, direction, character):
        if character.name in self.access[direction]:
            self.access[direction].remove(character.name)

    def allowAccess(self, direction, character):
        if character.name not in self.access[direction]:
            self.access[direction].append(character.name)

    def render(self, screen):
        for i in self.neighbors.keys():
            if self.neighbors[i] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[i].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4)
                pygame.draw.circle(screen, RED, self.position.asInt(), 12)

class NodeGroup(object):
    def __init__(self, level):
        self.level = level
        self.nodesLUT = {}
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        self.homekey = None
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)

    def readMazeFile(self, textfile):
        return numpy.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col+xoffset, row+yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y):
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectHorizontally(self, data, xoffset=0, yoffset=0):
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols:
                    key = None

    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col+xoffset, row+yoffset)
                    else:
                        otherkey = self.constructKey(col+xoffset, row+yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel):
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None

    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def getStartTempNode(self):
        nodes = list(self.nodesLUT.values())
        return nodes[46]

    def createHomeNodes(self, xoffset, yoffset):
        homedata = numpy.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])

        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey

    def connectHomeNodes(self, homekey, otherkey, direction):
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key]
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey]

    def setPortalPair(self, pair1, pair2):
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def setPortalPair2(self, pair1, pair2):
        key1 = pair1
        key2 = pair2
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL2] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL2] = self.nodesLUT[key1]

    def denyAccess(self, col, row, direction, character):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, character)

    def allowAccess(self, col, row, direction, character):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.allowAccess(direction, character)

    def denyAccessList(self, col, row, direction, characters):
        for character in characters:
            self.denyAccess(col, row, direction, character)

    def allowAccessList(self, col, row, direction, characters):
        for character in characters:
            self.allowAccess(col, row, direction, character)

    def denyHomeAccess(self, character):
        self.nodesLUT[self.homekey].denyAccess(DOWN, character)

    def allowHomeAccess(self, character):
        self.nodesLUT[self.homekey].allowAccess(DOWN, character)

    def denyHomeAccessList(self, characters):
        for character in characters:
            self.denyHomeAccess(character)

    def allowHomeAccessList(self, characters):
        for character in characters:
            self.allowHomeAccess(character)

    def render(self, screen):
        for node in self.nodesLUT.values():
            node.render(screen)
