# apps/desktop_icon.py
import pygame
from pygame.sprite import Sprite
from core.events import event_bus
from core.ui import UI

ICON_S = 40


class DesktopIcon(Sprite):
    def __init__(self, app_name, pos):
        super().__init__()
        self.app_name = app_name
        self.image = pygame.Surface((ICON_S, ICON_S), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self._pressed = False
        self._redraw()

    def _redraw(self):
        self.image.fill((0, 0, 0, 0))
        base = UI.get("base")
        icon = UI.get(self.app_name)
        if base:
            self.image.blit(base, (0, 0))
        if icon:
            self.image.blit(icon, (0, 0))

    def set_pressed(self, p):
        if self._pressed != p:
            self._pressed = p
            self._redraw()

    def on_click(self):
        event_bus.emit("request_open_window", self.app_name)