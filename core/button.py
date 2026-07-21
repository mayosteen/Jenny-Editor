# button.py
import pygame
from assets.uiconfig import *

class Button:
    def __init__(self, tag, *args):
        self._tag = tag
        self.image = UI[tag]
        self.rect = self.image.get_rect()
        self.rect.topleft = args
    
    def collide(self, pos):
        return self.rect.collidepoint(pos)
    
    @property
    def tag(self):
        return self._tag
    
    @tag.setter
    def tag(self, new):
        self._tag = new
        self.image = UI[new]