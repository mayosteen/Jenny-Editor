from core.config import *
from assets.uiconfig import *
from core.window import Window, Button

from apps.control import Control


class Desktop(Window):
    def __init__(self):
        super().__init__("Desktop", (0, 0, WIDTH, HEIGHT-40))
        self.bg = pygame.image.load("./assets/sprites/bg.png")
        self.buttons = [
            Button(self, "btn_explorer", "z", (12,  12)),
            Button(self, "btn_control",  "z", (64,  12)),
        ]
    
    def _draw_content(self):
        self.blit(self.bg, (0, 0))
        for b in self.buttons:
            self.draw_btn(b)
    
    def onclick(self, pos):
        for b in self.buttons:
            if b.collide(pos):
                print(f"{__name__}.{self.__class__.__name__}.onclick:{b.tag}")
                if b.tag == "btn_explorer":
                    t.new(Explorer(0, 0, 1280, 720))
                    print("new")
                elif b.tag == "btn_control":
                    t.new(Control(0, 0, 1280, 720))
                return b.tag


class Explorer(Window):
    def __init__(self, *args):
        super().__init__("Explorer", *args)
        self.mouse = (0, 0)
    
    def _draw_content(self):
        self.fill((128, 128, 128))
        self.draw_rect((255, 255, 255), (1, 1, self.rect.w-2, self.rect.h-2))
        self.draw_rect((128, 128, 128), self.mouse + (40, 40))
        for b in self.buttons:
            self.draw_btn(b)