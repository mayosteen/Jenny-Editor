import os, sys
from enum import Enum
from screeninfo import get_monitors
import pygame

# 窗口
FULLSCREEN = False
if FULLSCREEN:
    monitor = get_monitors()[0]
    WIDTH = monitor.width
    HEIGHT = monitor.height
else:
    WIDTH = 1920
    HEIGHT = 1080

FPS = 60

GRID = 40

# 文件
RECENT_PROJECT_PATH = "Jenny-Editor/recent"

# 状态
class States(Enum):
    QUIT = 0
    PLAY = 1
    PAUSE = 2
    EDIT = 3

state = States.EDIT

class EventTypes(Enum):
    TEMPO = 0
    TRANSPOSE = 1


# 声音
INTERVALS = [ 0, 72, 42, 23, 58, 105, ]


# 造型
SPRITES = {
    0:pygame.image.load("./assets/sprites/72edo/0.png"),
    1:pygame.image.load("./assets/sprites/72edo/1.png"),
    2:pygame.image.load("./assets/sprites/72edo/2.png"),
    3:pygame.image.load("./assets/sprites/72edo/3.png"),
    4:pygame.image.load("./assets/sprites/72edo/4.png"),
    5:pygame.image.load("./assets/sprites/72edo/5.png"),
    "g1":pygame.image.load("./assets/sprites/g1.png"),
    "g2":pygame.image.load("./assets/sprites/g2.png"),
    "g3":pygame.image.load("./assets/sprites/g3.png"),
    "g4":pygame.image.load("./assets/sprites/g4.png"),
    "g5":pygame.image.load("./assets/sprites/g5.png"),
}

FONT = pygame.font.Font("./assets/fonts/xwxxh.ttf", 12)