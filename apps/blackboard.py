from core.config import *
from assets.uiconfig import *

from core.window import Window
from core.button import Button

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
        self.page = 0
        self.last_page = 0
    
    def _draw_content(self):
        self.fill((15, 38, 30))
    
    def rewind(self):
        if self.page > 0:
            if self.page >= self.last_page:
                pygame.image.save(self, f"./screenshots/page_{self.page:03d}.png")
            self.page -= 1
            self.blit(pygame.image.load(f"./screenshots/page_{self.page:03d}.png"), (0, 0))
    
    def forward(self):
        if self.page >= self.last_page:
            pygame.image.save(self, f"./screenshots/page_{self.page:03d}.png")
            self.fill((15, 38, 30))
            self.blit(pygame.image.load(f"./screenshots/page_{self.page:03d}.png"), (-self.rect.w//3, -self.rect.h//4))
            self.page += 1
            self.last_page += 1
        else:
            self.page += 1
            self.blit(pygame.image.load(f"./screenshots/page_{self.page:03d}.png"), (0, 0))


class Buttonbar(Window):
    def __init__(self, buttons, *args):
        super().__init__("Buttonbar", *args)
        self.buttons = buttons
    
    def draw_button(self, btn:Button):
        self.blit(btn.image, btn.rect)

    def _draw_content(self):
        self.fill((15, 38, 30))
        for button in self.buttons:
            self.draw_button(button)

class Blackboard(Window):
    def __init__(self, *args):
        super().__init__("Blackboard", *args)
        self.boardbody = Boardbody(*args)
        self.pressed = False
        self.state = "pen"
        self.pensize = 3
        self.mouse_pos = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.step = 20
        self.mouse = (0, 0)
        self.color = COLORS["btn_white"]
        self.button_tags = [
            "btn_close",
            "btn_pen",
            "btn_eraser",
            "btn_pen_1",
            "btn_pen_2",
            "btn_pen_3",
            "btn_pen_4",
            "btn_white",
            "btn_red",
            "btn_blue",
            "btn_magenta",

        ]
        self.buttons = [Button("btn_rewind", (self.rect.w-104, 12)), Button("btn_forward", (self.rect.w-52, 12))]
        x = 12
        for button_tag in self.button_tags:
            self.buttons.append(Button(button_tag, (x, 12)))
            x += 52
        self.buttonbar = Buttonbar(self.buttons, 0, self.rect.h-64, self.rect.w, 64)
    
    def _draw_content(self):
        pass
    
    def get_surface(self, screen):
        screen.draw(self.boardbody)
        screen.draw(self.buttonbar)

    def onclick(self, pos):
        self.mouse = pos
        self.pressed = True
        for b in self.buttons:
            print(b.tag)
            if b.collide((pos[0], pos[1]-self.rect.h+64)):
                if b.tag == 0:
                    self.close()
                elif b.tag == "btn_pen":
                    self.state = "pen"
                elif b.tag == "btn_pen_1":
                    self.pensize = 1
                elif b.tag == "btn_pen_2":
                    self.pensize = 2
                elif b.tag == "btn_pen_3":
                    self.pensize = 5
                elif b.tag == "btn_pen_4":
                    self.pensize = 10
                elif b.tag == "btn_eraser":
                    self.state = "eraser"
                elif b.tag == "btn_rewind":
                    self.boardbody.rewind()
                elif b.tag == "btn_forward":
                    self.boardbody.forward()
                else:
                    color = COLORS.get(b.tag)
                    if color is not None:
                        self.state = "pen"
                        self.color = color
                        
    def onmove(self, pos):
        self.mouse_pos.pop(0)
        self.mouse_pos.append(pos)
        if self.pressed:
            if self.state == "pen":
                # pygame.draw.line(self, self.color, self.mouse, pos, 3)
                for t in range(self.step):
                    if self.pensize == 1:
                        pygame.draw.aaline(self.boardbody, self.color, 
                                        catmull_rom(self.mouse_pos, t/self.step), 
                                        catmull_rom(self.mouse_pos, (t+1)/self.step), 
                                        1)
                    else:
                        pygame.draw.line(self.boardbody, self.color, 
                                        catmull_rom(self.mouse_pos, t/self.step), 
                                        catmull_rom(self.mouse_pos, (t+1)/self.step), 
                                        self.pensize)
                        if self.pensize > 5:
                            pygame.draw.circle(self.boardbody, self.color, catmull_rom(self.mouse_pos, t/self.step), self.pensize//2)
            elif self.state == "eraser":
                # pygame.draw.line(self, (15, 38, 30), self.mouse, pos, 150)
                for t in range(self.step):
                    pygame.draw.circle(self.boardbody, (15, 38, 30), catmull_rom(self.mouse_pos, t/self.step), 100)
        self.mouse = pos

    def onrelease(self, pos):
        self.mouse = pos
        self.pressed = False

blackboard = Blackboard()
