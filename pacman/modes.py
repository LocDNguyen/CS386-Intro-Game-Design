from constants import *

class MainMode(object):
    def __init__(self):
        self.timer = 0
        self.scatter()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

class ModeController(object):
    def __init__(self, character):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode()
        self.current = self.mainmode.mode
        self.character = character

    def setFrightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FRIGHT
        elif self.current is FRIGHT:
            self.timer = 0

    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FRIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.character.normalMode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if self.character.node == self.character.spawnNode:
                self.character.normalMode()
                self.current = self.mainmode.mode

    def setSpawnMode(self):
        if self.current is FRIGHT:
            self.current = SPAWN
