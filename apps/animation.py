# core/subtitle.py
from itertools import combinations
from core.template import *
from core.shasav import Monzo, Harmononym, Val
from core.image import UI
from core.events import event_bus
from core.window import Window

class Animation(Window):
    def __init__(self):
        super().__init__("subtitle", pygame.Rect(0, 0, 1920, 1080))

        self.font = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 20)
        self.showing = "Chords"
        self.beat = 0
        self.speed = 80
        self.x = 0
        self.y = 0
    
    def render_subtitle(self):
        foreground = self.font.render(self.showing, True, (255, 255, 255))
        f_rect = foreground.get_rect()
        f_rect.center = (self.rect.w//2, self.rect.h//2)
        self.surface.blit(foreground, f_rect)
    
    def draw(self, screen:pygame.Surface):
        # 子类重写方法
        self.surface.fill((139, 28, 27))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        # pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
        bar = pygame.Surface((self.rect.w, 2), flags=SRCALPHA)
        bar.fill((224, 133, 152, 77))
        for sprite in song.sprites:
            s = pygame.image.load(f'project/{sprite["image"]}')
            r = s.get_rect()
            if self.beat <= sprite["animation"][0]["start"]:
                p = sprite["position"]
                r.center = (
                    self.rect.w//2+( p[0] ),
                    self.rect.h//2-( p[1] ))
            else:
                for p in range(len(sprite["animation"])-1):
                    a0 = sprite["animation"][p]
                    a1 = sprite["animation"][p+1]
                    if a0["start"] <= self.beat <= a1["start"]:
                        p0 = a0["position"]
                        p1 = a1["position"]
                        offset = (self.beat-a0["start"])/(a1["start"]-a0["start"])
                        r.center = (
                            self.rect.w//2+( p0[0]*(1-offset) + p1[0]*offset ),
                            self.rect.h//2-( p0[1]*(1-offset) + p1[1]*offset ))
                            
            self.surface.blit(s, r)



        # self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        self.beat = song.get_beat()

    def on_mouse_down(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"animation.on_mouse_down: {pos}")
        pass

    def on_mouse_up(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"animation.on_mouse_up: {pos}")
        pass

    def on_key_down(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"animation.on_key_down: {event}")
        if event.unicode == "z":
            song.play()
        if event.unicode == "x":
            song.pause()
        if event.unicode == "c":
            song.resume()

    def on_key_up(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"animation.on_key_up: {event}")
        pass
            