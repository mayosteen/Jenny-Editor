import sys, os
import pygame
from pygame.locals import * # type: ignore
from core.config import applauncher, UI, WIDTH, HEIGHT
from core.window import Window, Button

class TaskManager:
    def __init__(self):
        self.ask = []
        self.askshow = []
    
    def new(self, window_name:str, *rect):
        window = applauncher[window_name](*rect)
        self.ask.append(window)
        self.askshow.append(window)
        print(f"{__name__}.{self.__class__.__name__}.new:{window.title}")
    
    def activate(self, window:Window):
        if not(window.title in ["desktop", "command"]):
            self.ask.remove(window)
            self.ask.append(window)
        print(f"{__name__}.{self.__class__.__name__}.activate:{window.title}")
    
    def close(self, window:Window):
        self.ask.remove(window)
        self.askshow.remove(window)
        print(f"{__name__}.{self.__class__.__name__}.close:{window.title}")
        if window.title == "command":
            pygame.quit()
            sys.exit()
    
    def update(self):
        for i, window in enumerate(self.ask):
            if window.state in ("close", "closed"):
                self.close(self.ask[i])

class Taskbar(Window):
    def __init__(self, t:TaskManager, h):
        super().__init__("taskbar", (0, HEIGHT-h, WIDTH, h))
        self.t = t
    
    def _draw_content(self):
        self.fill((26, 42, 53))
        self.blit(UI["mayos"], (0, 0))
        for i, window in enumerate(self.t.askshow):
            self.blit(UI[window.title.lower()], ((i+1)*40, 0))
            if window == self.t.ask[-1]:
                self.blit(UI["highlight"], ((i+1)*40, 0))
    
    def onclick(self, pos):
        if 0 <= pos[0] < 40:
            print(f"{__name__}.{self.__class__.__name__}.onclick:MayOS Logo")
            pygame.quit()
            sys.exit()
        else:
            window_index = pos[0]//40-1
            if window_index < len(self.t.ask):
                active_window = self.t.askshow[window_index]
                print(f"{__name__}.{self.__class__.__name__}.onclick:{active_window.title}")
                print(len(self.t.ask), len(self.t.askshow))
                self.t.activate(active_window)