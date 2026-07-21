# window.py
import pygame
from pygame.locals import * # type: ignore

from core.config import WIDTH, HEIGHT
from assets.uiconfig import *

class Window(pygame.Surface):
    def __init__(self, title, *args):
        self.title = title
        if len(args) == 0:  # ()
            super().__init__((WIDTH, HEIGHT), flags=SRCALPHA)
            self.rect = self.get_rect()
            self.rect.topleft = (0, 0)
        elif len(args) == 2:  # (w, h)
            super().__init__(args, flags=SRCALPHA)
            self.rect = self.get_rect()
            self.rect.center = (WIDTH//2, HEIGHT//2)
        elif len(args) == 4:  # (x, y, w, h)
            super().__init__(args[2:], flags=SRCALPHA)
            self.rect = self.get_rect()
            self.rect.topleft = args[0:2]
        else:
            raise ValueError(f"传入Window的参数应为0/2/4个，但是用户却填了{len(args)}个，分别是{args}")
            
        self.is_alive = True
        self._dirty = True

        self.title = title

    def update(self):
        """每帧调用，用于刷新逻辑"""
        if self._dirty:
            self.redraw()
            self._dirty = False

    def redraw(self):
        """强制重绘"""
        self.fill((0, 0, 0))
        self._draw_content()

    def _draw_content(self):
        """子类重写这里"""
        pass

    def get_surface(self, screen):
        screen.draw(self)

    def collide(self, pos):
        return self.rect.collidepoint(pos)

    def mousedown(self, pos):
        self.onclick((pos[0]-self.rect.x, pos[1]-self.rect.y))

    def onclick(self, pos):
        """子类重写这里"""
        pass

    def mousemotion(self, pos):
        self.onmove((pos[0]-self.rect.x, pos[1]-self.rect.y))

    def onmove(self, pos):
        """子类重写这里"""
        pass

    def mouseup(self, pos):
        self.onrelease((pos[0]-self.rect.x, pos[1]-self.rect.y))

    def onrelease(self, pos):
        """子类重写这里"""
        pass

    def mark_dirty(self):
        self._dirty = True

    def draw_rect(self, color, rect):
        pygame.draw.rect(self, color, rect)

    def close(self):
        self.is_alive = False
        del self

def resize(sur, w, h):
    return pygame.transform.scale(sur, (w, h))
