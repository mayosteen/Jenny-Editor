import sys, os
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

from core.tasks import TaskManager
t = TaskManager()