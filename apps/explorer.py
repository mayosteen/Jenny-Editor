from core.config import *
from core.window import Window
from assets.uiconfig import icons


class Desktop(Window):
    def __init__(self):
        super().__init__("Desktop")
        self.bg = pygame.image.load("./assets/sprites/bg.png")
    
    def _draw_content(self):
        self.blit(self.bg, (0, 0))


class Taskbar(Window):
    def __init__(self, tasks, h):
        super().__init__("Desktop", 0, HEIGHT-h, WIDTH, h)
        self.tasks = tasks
    
    def _draw_content(self):
        self.fill((81, 78, 97))
        self.blit(icons["t_mayos"], (0, 0))
        for i, task in enumerate(self.tasks):
            self.blit(icons["t_"+task.title.lower()], ((i+1)*40, 0))
    
    def onclick(self, pos):
        if 0 <= pos[0] < 40:
            pygame.quit()
            sys.exit()


class Explorer(Window):
    def __init__(self, *args):
        super().__init__("Explorer", *args)
        self.mouse = (0, 0)
    
    def _draw_content(self):
        self.fill((128, 128, 128))
        self.draw_rect((255, 255, 255), (1, 1, self.rect.w-2, self.rect.h-2))
        self.draw_rect((128, 128, 128), self.mouse + (40, 40))
    
    def onclick(self, pos):
        self.mouse = pos
        self.mark_dirty()