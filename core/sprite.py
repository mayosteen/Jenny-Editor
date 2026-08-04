import pygame
from pygame.sprite import Sprite

class WindowSprite(Sprite):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.image = pygame.Surface(window.rect.size, pygame.SRCALPHA)
        self.rect = window.rect.copy()

    def update(self):
        self.rect.topleft = self.window.rect.topleft
        self.window._draw_content()   # ← 关键：驱动内容绘制