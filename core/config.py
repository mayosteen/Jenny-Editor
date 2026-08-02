import sys, os
from enum import Enum
from screeninfo import get_monitors
import pygame
from pygame.locals import *  # type:ignore
pygame.init()


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

os.environ['SDL_VIDEO_WINDOW_POS'] = '0, 0'
pygame.display.set_caption("Jenny Editor")

class Screen:
    def __init__(self, w, h):
        self.surface = pygame.display.set_mode((w, h), flags=NOFRAME)
    
    def fill(self, color):
        self.surface.fill(color)
    
    def draw(self, window):
        if window._dirty:
            print(f"{__name__}.{self.__class__.__name__}.redraw:{window.title}")
            window.redraw()
            window._dirty = False
        if window.dragging:
            self.surface.blit(window.surface, window.drag_rect)
        else:
            self.surface.blit(window.surface, window.rect)

screen = Screen(WIDTH, HEIGHT)

from pygame.image import load
UI = {
    "base"     : load("./assets/UI/base.png"),

    # 任务
    "mayos"    : load("./assets/UI/mayos.png"),
    "highlight": load("./assets/UI/highlight.png"),
    "default"  : load("./assets/UI/default.png"),

    # 窗口
    "window"   : load("./assets/UI/window.png"),  # 取消最大化
    "close"    : load("./assets/UI/close.png"),
    "max"      : load("./assets/UI/max.png"),
    "full"     : load("./assets/UI/full.png"),
    "min"      : load("./assets/UI/min.png"),
    "drag"     : load("./assets/UI/drag.png"),

    # 命令行
    "terminal" : load("./assets/UI/terminal.png"),

    # 桌面
    "desktop"  : load("./assets/UI/desktop.png"),

    # 浏览器
    "explorer" : load("./assets/UI/explorer.png"),

    # 黑板
    "board"    : load("./assets/UI/board.png"),
    "pen"      : load("./assets/UI/pen.png"),
    "eraser"   : load("./assets/UI/eraser.png"),
    "white"    : load("./assets/UI/white.png"),
    "red"      : load("./assets/UI/red.png"),
    "blue"     : load("./assets/UI/blue.png"),
    "magenta"  : load("./assets/UI/magenta.png"),
    "size1"    : load("./assets/UI/size1.png"),
    "size2"    : load("./assets/UI/size2.png"),
    "size3"    : load("./assets/UI/size3.png"),
    "size4"    : load("./assets/UI/size4.png"),

    # 音乐
    "control"  : load("./assets/UI/control.png"),
    "play"     : load("./assets/UI/play.png"),
    "pause"    : load("./assets/UI/pause.png"),
    "rewind"   : load("./assets/UI/rewind.png"),
    "forward"  : load("./assets/UI/forward.png"),
}

COLORS = {
    "blackboard" : (15, 38, 30),
    "white"  : (248, 248, 240),
    "red"    : (255, 130, 130),
    "blue"   : (140, 190, 255),
    "magenta": (255, 180, 210),

    "control_bg" : (81, 78, 97),
}

# 任务
applauncher = {
    "terminal": "apps.terminal.Terminal",
    "desktop" : "apps.explorer.Desktop",
    "explorer": "apps.explorer.Explorer",
    "control" : "apps.control.Control",
}