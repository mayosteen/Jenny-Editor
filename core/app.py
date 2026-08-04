# core/app.py
import pygame
from config import WIDTH, HEIGHT
from core.ui import load_ui
from core.wm import WindowManager
from core.taskbar import Taskbar
from core.input import InputManager
from apps.desktop import Desktop
from apps.terminal import Terminal

class MayOS:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MayOS")

        # ✅ 关键：display 初始化后再加载 UI
        load_ui()

        self.clock = pygame.time.Clock()
        self.wm = WindowManager()
        self.input = InputManager(self.wm)

        self.desktop = Desktop()
        self.taskbar = Taskbar(self.wm)

        self.wm.open(self.desktop)
        self.wm.open(Terminal())
        self.wm.add_system(self.taskbar)

    def run(self):
        while True:
            if not self.input.process():
                break

            self.wm.update()
            self.wm.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()