# core/subtitle.py
from itertools import combinations
from core.template import *
from core.shasav import Monzo, Harmononym, Val
from core.image import UI
from core.events import event_bus
from core.window import Window
from core.curves import io_circle

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
        for id, sprite in song.sprites.items():
            if self.beat <= sprite.anim[0]["start"]:
                pass
            else:
                for p in range(len(sprite.anim)-1):
                    a0 = sprite.anim[p]
                    a1 = sprite.anim[p+1]
                    if a0["start"] <= self.beat <= a1["start"]:
                        p0 = a0["position"]
                        p1 = a1["position"]
                        sprite.pos = io_circle(p0, p1, (self.beat-a0["start"])/(a1["start"]-a0["start"]))
                            
            self.blit(sprite)



        # self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        event_bus.emit("record_update")
        beat = song.get_beat()
        # print(beat - self.beat)
        self.beat = beat

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
        if event.unicode == "a":
            event_bus.emit("record_start", self.surface)
        if event.unicode == "s":
            event_bus.emit("record_stop", song.music)

    def on_key_up(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"animation.on_key_up: {event}")
        pass
            