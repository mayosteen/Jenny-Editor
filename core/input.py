# core/input.py
import pygame
from core.events import event_bus
from pygame.locals import *

class InputManager:
    def __init__(self, wm):
        self.wm = wm

    def process(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                return False

            elif e.type == MOUSEBUTTONDOWN:
                event_bus.emit("mouse_down", {
                    "button": e.button,
                    "pos": e.pos
                })

            elif e.type == MOUSEBUTTONUP:
                event_bus.emit("mouse_up", {
                    "button": e.button,
                    "pos": e.pos
                })

            elif e.type == MOUSEMOTION:
                event_bus.emit("mouse_move", {
                    "pos": e.pos
                })

            elif e.type == KEYDOWN:
                event_bus.emit("key_down", {
                    "key": e.key,
                    "unicode": e.unicode
                })

        return True