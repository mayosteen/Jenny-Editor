import sys, os
import pygame
from pygame.locals import * # type: ignore
pygame.init()
from core.config import *

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