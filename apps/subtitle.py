# core/subtitle.py
from core.template import *
from core.events import event_bus
from core.window import Window

class Subtitle(Window):
    def __init__(self):
        super().__init__("subtitle", pygame.Rect(320, 880, 1280, 200))

        self.font = pygame.font.Font("assets/fonts/LXGWNeoXiHei.ttf", 120)
        self.showing = "请显示歌词"
    
    def render_subtitle(self):
        foreground = self.font.render(self.showing, True, (255, 255, 255))
        f_rect = foreground.get_rect()
        f_rect.center = (self.rect.w//2, self.rect.h//2)
        self.surface.blit(foreground, f_rect)
    
    def draw(self, screen:pygame.Surface):
        # 子类重写方法
        self.surface.fill((0, 0, 0, 0))
        pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
        self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        # 子类重写方法
        pass

    def on_mouse_down(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"subtitle.on_mouse_down: {pos}")
        pass

    def on_mouse_up(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"subtitle.on_mouse_up: {pos}")
        pass

    def on_key_down(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"subtitle.on_key_down: {event}")
        pass

    def on_key_up(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"subtitle.on_key_up: {event}")
        pass
            