# window.py
import pygame
from pygame.locals import * # type: ignore

from core.config import WIDTH, HEIGHT
from assets.uiconfig import *

from core.button import Button

class Window:
    def __init__(self, title, *args):
        self.title = title
        if len(args) == 0:  # ()
            self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        elif len(args) == 2:  # (w, h)
            self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, args[0], args[1])
            self.rect.center = WIDTH//2, HEIGHT//2
        elif len(args) == 4:  # (x, y, w, h)
            self.rect = pygame.Rect(*args)
        else:
            raise ValueError(f"传入Window的参数应为0/2/4个，但是用户却填了{len(args)}个，分别是{args}")
        self.surface = pygame.Surface(self.rect.size, flags=SRCALPHA)
            
        self.is_alive = True
        self._dirty = True

        self.title = title

    def blit(self, surface, rect):
        self.surface.blit(surface, rect)
    
    def fill(self, color):
        self.surface.fill(color)

    def save(self, path):
        pygame.image.save(self.surface, path)

    def update(self):
        """每帧调用，用于刷新逻辑"""
        if self._dirty:
            self.redraw()
            self._dirty = False

    # 绘制
    def redraw(self):
        """强制重绘"""
        self._draw_content()

    def _draw_content(self):
        """子类重写这里"""
        pass

    def get_surface(self, screen):
        screen.draw(self)

    def mark_dirty(self):
        self._dirty = True

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.surface, color, rect)

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

    def close(self):
        self.is_alive = False
        del self

def resize(sur, w, h):
    return pygame.transform.scale(sur, (w, h))

class Buttonbar(Window):
    def __init__(self, buttons, *args):
        super().__init__("Buttonbar", *args)
        self.buttons = buttons
    
    def draw_button(self, btn:Button):
        self.blit(btn.image, btn.rect)

    def _draw_content(self):
        for button in self.buttons:
            self.draw_button(button)
