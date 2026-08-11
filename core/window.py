# core/window.py
from core.template import *
from core.events import event_bus

# 窗口基类
class Window:
    def __init__(self, title:str, rect:pygame.Rect):
        self.title = title
        self.surface = pygame.Surface(rect.size)
        self.rect = rect
    
    def draw(self, screen:pygame.Surface):
        # 子类重写方法
        self.surface.fill((103, 103, 131))
        pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
        screen.blit(self.surface, self.rect)
    
    def update(self):
        # 子类重写方法
        pass

    def on_mouse_down(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"window.on_mouse_down: {pos}")
        pass

    def on_mouse_up(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"window.on_mouse_up: {pos}")
        pass

    def on_key_down(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"window.on_key_down: {event}")
        pass

    def on_key_up(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"window.on_key_up: {event}")
        pass
            
