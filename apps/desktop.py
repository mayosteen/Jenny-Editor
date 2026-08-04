# apps/desktop.py
import pygame
from pygame.sprite import Group
from core.window import Window
from core.events import event_bus
from .desktop_icon import DesktopIcon
from config import WIDTH, HEIGHT

class Desktop(Window):
    def __init__(self):
        super().__init__("desktop", (0, 0, WIDTH, HEIGHT - 40))
        self.bg = pygame.Surface(self.rect.size)
        self.bg.fill((60, 120, 200))
        self.icons = Group()

        self.icons.add(DesktopIcon("terminal", (40, 40)))
        self.icons.add(DesktopIcon("explorer", (40, 120)))
        self.icons.add(DesktopIcon("control",  (40, 200)))

        event_bus.subscribe("mouse_down", self._on_down)
        event_bus.subscribe("mouse_up",   self._on_up)

    def _draw_content(self):
        self.sprite.image.fill((0, 0, 0, 0))
        self.sprite.image.blit(self.bg, (0, 0))
        self.icons.draw(self.sprite.image)

    def _on_down(self, data):
        if data["button"] != 1:
            return
        mx, my = data["pos"]
        lx, ly = mx - self.rect.x, my - self.rect.y
        for icon in self.icons:
            if icon.rect.collidepoint(lx, ly):
                icon.set_pressed(True)
                break

    def _on_up(self, data):
        if data["button"] != 1:
            return
        mx, my = data["pos"]
        lx, ly = mx - self.rect.x, my - self.rect.y
        for icon in self.icons:
            if icon.rect.collidepoint(lx, ly) and icon._pressed:
                icon.on_click()
            icon.set_pressed(False)