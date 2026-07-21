from core.config import *
from core.window import Window
from core.button import Button
from assets.uiconfig import *


class Blackboard(Window):
    def __init__(self, *args):
        super().__init__("Blackboard", *args)
        self.pressed = False
        self.state = "pen"
        self.mouse = (0, 0)
        self.color = (255, 255, 255)
        self.buttons = [
            Button(buttons["btn_close"], (12, self.rect.h-52)),
            Button(buttons["btn_eraser"], (64, self.rect.h-52)),
            Button(colors["white"], (116, self.rect.h-52)),
            Button(colors["red"], (168, self.rect.h-52)),
            Button(colors["blue"], (220, self.rect.h-52)),
        ]
    
    def draw_button(self, btn:Button):
        self.blit(btn.image, btn.rect)

    
    def _draw_content(self):
        self.fill((15, 38, 30))
        for button in self.buttons:
            self.draw_button(button)
    
    def onclick(self, pos):
        self.mouse = pos
        self.pressed = True
        for i, button in enumerate(self.buttons):
            if button.collide(pos):
                if i == 0:
                    self.close()
                elif i == 1:
                    self.state = "eraser"
                else:
                    self.state = "pen"
                    if i == 2:
                        self.color = (255, 255, 255)
                    if i == 3:
                        self.color = (255, 16, 0)
                    if i == 4:
                        self.color = (88, 188, 255)
                        
    def onmove(self, pos):
        if self.pressed:
            if self.state == "pen":
                pygame.draw.line(self, self.color, self.mouse, pos, 3)
            elif self.state == "eraser":
                pygame.draw.line(self, (15, 38, 30), self.mouse, pos, 150)
        self.mouse = pos

    def onrelease(self, pos):
        self.mouse = pos
        self.pressed = False
        for button in self.buttons:
            self.draw_button(button)

blackboard = Blackboard()
