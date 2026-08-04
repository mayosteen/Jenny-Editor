# core/taskbar.py
import pygame
from pygame.sprite import Sprite
from core.events import event_bus
from core.ui import UI
from config import WIDTH, HEIGHT

TASKBAR_H = 40
ICON_S = 40


class Taskbar(Sprite):
    def __init__(self, wm):
        super().__init__()
        self.wm = wm
        self.image = pygame.Surface((WIDTH, TASKBAR_H), pygame.SRCALPHA)
        self.rect = self.image.get_rect(bottomleft=(0, HEIGHT))

        self._highlight = -1
        event_bus.subscribe("window_opened",  lambda _: self._redraw())
        event_bus.subscribe("window_closed",  lambda _: self._redraw())
        event_bus.subscribe("window_focused", self._on_focus)

        self._redraw()

    def _on_focus(self, win):
        try:
            self._highlight = self.wm.windows.index(win)
        except ValueError:
            self._highlight = -1
        self._redraw()

    def _redraw(self):
        self.image.fill((26, 42, 53))
        self.image.blit(UI["mayos"], (0, 0))

        for i, win in enumerate(self.wm.windows):
            key = win.title.lower()
            icon = UI.get(key)
            if not icon:
                continue

            x = (i + 1) * ICON_S
            self.image.blit(icon, (x, 0))
            if i == self._highlight:
                self.image.blit(UI["highlight"], (x, 0))

    def update(self):
        pass