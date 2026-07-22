from core.config import *
from assets.uiconfig import *

from core.window import Window, Buttonbar, Button

def quadratic_bezier(t, p):
    """
    二次贝塞尔曲线
    p0: 前前点
    p1: 前一点
    p2: 当前点
    """
    p0 = p[0]
    p1 = p[1]
    p2 = p[2]
    x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
    y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
    return int(x), int(y)

def catmull_rom(p, t, tension=0.5):
    p0 = p[0]
    p1 = p[1]
    p2 = p[2]
    p3 = p[3]
    t2 = t * t
    t3 = t2 * t

    m1 = ((p2[0] - p0[0]) * tension,
          (p2[1] - p0[1]) * tension)
    m2 = ((p3[0] - p1[0]) * tension,
          (p3[1] - p1[1]) * tension)

    h00 =  2*t3 - 3*t2 + 1
    h10 =    t3 - 2*t2 + t
    h01 = -2*t3 + 3*t2
    h11 =    t3 - t2

    x = h00*p1[0] + h10*m1[0] + h01*p2[0] + h11*m2[0]
    y = h00*p1[1] + h10*m1[1] + h01*p2[1] + h11*m2[1]

    return int(x), int(y)

class Boardbody(Window):
    def __init__(self, *args):
        super().__init__("Boardbody", *args)
        self.state = "pen"
        self.color = COLORS["btn_white"]
        self.pensize = 3
        self.page = 0
        self.last_page = 0
    
    def _draw_content(self):
        self.fill(COLORS["blackboard"])

    def draw_line(self, pos1, pos2):
        if self.state == "pen":
            if self.pensize <= 1:
                pygame.draw.aaline(self.surface, self.color, pos1, pos2, 1)
            else:
                pygame.draw.line(self.surface, self.color, pos1, pos2, self.pensize)
            if self.pensize > 5:
                pygame.draw.circle(self.surface, self.color, pos1, self.pensize//2)
        elif self.state == "eraser":
            pygame.draw.circle(self.surface, COLORS["blackboard"], pos1, 100)

    def load_page(self, *pos):
        self.blit(pygame.image.load(f"./screenshots/page_{self.page:03d}.png"), pos)
    def save_page(self):
        self.save(f"./screenshots/page_{self.page:03d}.png")

    def skip_to(self):
        pass
    
    def rewind(self):
        self.save_page()
        if self.page >= 1:
            self.page -= 1
            self.load_page(0, 0)
            self.page += 1
            self.load_page(self.rect.w//3, self.rect.h//4)
            self.page -= 1
    
    def forward(self):
        self.save_page()
        if self.page == self.last_page:
            self.last_page += 1
            self._draw_content()
        else:
            self.page += 1
            self.load_page(0, 0)
            self.page -= 1
        self.load_page(-self.rect.w//3, -self.rect.h//4)
        self.page += 1



class Control(Window):
    def __init__(self, *args):
        super().__init__("Control", *args)
        self.state = state
        self.button_tags = [
            "btn_close",
            "btn_play",
            "btn_pause",
        ]

        self.buttons = [Button("btn_rewind", (self.rect.w-104, 12)), Button("btn_forward", (self.rect.w-52, 12))]
        x = 12
        for button_tag in self.button_tags:
            self.buttons.append(Button(button_tag, (x, 12)))
            x += 52
        self.buttonbar = Buttonbar(self.buttons, 0, self.rect.h-64, self.rect.w, 64)
    
    def _draw_content(self):
        self.fill(COLORS["control_bg"])
    
    def get_surface(self, screen):
        screen.draw(self)
        screen.draw(self.buttonbar)

    def onclick(self, pos):
        pass
                        
    def onmove(self, pos):
        pass

    def onrelease(self, pos):
        pass