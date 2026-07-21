# button.py
import pygame

class Button:
    def __init__(self, image:pygame.Surface, *args):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = args
    
    def collide(self, pos):
        return self.rect.collidepoint(pos)