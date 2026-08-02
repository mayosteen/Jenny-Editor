# window.py
import pygame
from pygame.locals import * # type: ignore

from core.config import UI

class Button:
    def __init__(self, window, tag:str, key:str, pos:tuple):
        self.window = window
        self._tag = tag
        self.image = UI[tag]
        self.key = key.lower()
        self.pos = pos
        self.rect = self.image.get_rect()
        self.update()
    
    def collide(self, pos):
        return self.rect.collidepoint(pos)
    
    @property
    def tag(self):
        return self._tag
    
    @tag.setter
    def tag(self, new):
        self._tag = new
        self.image = UI[new]
    
    def update(self):
        """
        Button position:
        (q)   (e)

        (z)   (c)
        """
        if self.key in "qz":
            self.rect.left = self.pos[0]
        elif self.key in "ec":
            self.rect.right = self.window.rect.w - self.pos[0]
        if self.key in "qe":
            self.rect.top = self.pos[1]
        elif self.key in "zc":
            self.rect.bottom = self.window.rect.h - self.pos[1]
        else:
            raise KeyError(f'{__name__}.{self.__class__.__name__}.__init__:Invalid key:"{self.key}"')

class Window:
    def __init__(self, title, *rect):
        self.title = title
        self.rect = pygame.Rect(rect)
        self.surface = pygame.Surface(self.rect.size, flags=SRCALPHA)
        self.buttons = [
            Button(self, "close", "z", (12,  12)),
            Button(self, "max",   "z", (64,  12)),
            Button(self, "min",   "z", (116, 12)),
            Button(self, "drag",  "z", (168, 12)),
        ]
            
        self.state = "window"
        self.dragging = False
        self.drag_rect = pygame.Rect(rect)
        self.drag_offset = (0, 0)
        self._dirty = True

        self.title = title
        print(f"{__name__}.{self.__class__.__name__}.__init__:Added window {self.title}")

    # 渲染
    def fill(self, color): self.surface.fill(color)
    def blit(self, surface, rect): self.surface.blit(surface, rect)
    def draw_rect(self, color, rect): pygame.draw.rect(self.surface, color, rect)
    def draw_btn(self, button:Button): self.surface.blit(button.image, button.rect)
    def mark_dirty(self): self._dirty = True
    def redraw(self): self._draw_content()

    # 存储
    def save(self, path): pygame.image.save(self.surface, path)
    
    # 逻辑
    def collide(self, pos): return self.rect.collidepoint(pos)
    def close(self):
        self.state = "close"
        del self
    
    # 事件
    def mousedown(  self, pos): self.onclick(  (pos[0]-self.rect.x, pos[1]-self.rect.y))
    def mousemotion(self, pos): self.onmove(   (pos[0]-self.rect.x, pos[1]-self.rect.y))
    def mouseup(    self, pos): self.onrelease((pos[0]-self.rect.x, pos[1]-self.rect.y))
    def keydown(    self, key): self.onkeydown( key)
    def keyup(      self, key): self.onkeyup(   key)

    ############################## 子类重写函数 ##############################

    def _draw_content(self):
        # 子类重写这里
        pass

    def update(self):
        # 每帧调用，用于刷新逻辑
        pass

    def onclick(self, pos):
        for b in self.buttons:
            if b.collide(pos):
                print(f"{__name__}.{self.__class__.__name__}.onclick:{b.tag}")
                if b.tag == "close":
                    self.close()
                if b.tag == "max":
                    self.state = "max"
                if b.tag == "min":
                    self.state = "min"
                if b.tag == "drag":
                    self.dragging = True
                    self.drag_offset = (
                        pos[0] - self.rect.x,
                        pos[1] - self.rect.y
                    )
                return b.tag


    def onmove(self, pos):
        # 子类重写这里
        print(f"{__name__}.{self.__class__.__name__}.onmove:{pos}")
        if self.dragging:
            self.drag_rect.x = pos[0] - self.drag_offset[0]
            self.drag_rect.y = pos[1] - self.drag_offset[1]


    def onrelease(self, pos):
        # 子类重写这里
        print(f"{__name__}.{self.__class__.__name__}.onrelease:{pos}")
        if self.dragging:
            self.dragging = False
            self.rect.x = pos[0] - self.drag_offset[0]
            self.rect.y = pos[1] - self.drag_offset[1]
    

    def onkeydown(self, key):
        # 子类重写这里
        print(f"{__name__}.{self.__class__.__name__}.onkeydown:{key}")
    

    def onkeyup(self, key):
        # 子类重写这里
        print(f"{__name__}.{self.__class__.__name__}.onkeyup:{key}")


def resize(sur, w, h):
    return pygame.transform.scale(sur, (w, h))
