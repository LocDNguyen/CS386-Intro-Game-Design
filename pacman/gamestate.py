from enum import Enum

class GameState(Enum):
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    HIGHSCORE = 2
    INSTRUCTION = 3
