import pygame
from core.config import *

# region 相机

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

cam = Vec2(0.0, 0.0)

# endregion

# region 缩放

class Scaler:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.resize_update()

    def resize_update(self):
        global SPRITES
        for key,value in ORIGINAL_SPRITES.items():
            origin_width, origin_height = value.get_size()
            sprite_width = origin_width * self.x // DEFAULT_SCALE
            sprite_height = origin_height * self.y // DEFAULT_SCALE
            SPRITES[key] = pygame.transform.smoothscale(value, (sprite_width, sprite_height))
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.resize_update()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.resize_update()

scale = Scaler(SCALE, SCALE)

# endregion