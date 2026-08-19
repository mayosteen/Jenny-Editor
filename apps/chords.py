# core/subtitle.py
from itertools import combinations
from core.template import *
from core.shasav import Monzo, Harmononym, Val
from core.image import UI
from core.events import event_bus
from core.window import Window

class Chords(Window):
    def __init__(self):
        super().__init__("chords", pygame.Rect(0, 1080, 1280, 360))

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
        self.surface.fill((103, 102, 129))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        # pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
        bar = pygame.Surface((self.rect.w, 2), flags=SRCALPHA)
        bar.fill((224, 133, 152, 77))
        for i in range(-10, 11):
            self.surface.blit(bar, (0, self.rect.h // 2 - i*song.tuning.vec[1]*2 -1))
        for i in song.chords:
            hs = Harmononym(i["shasaf"])
            p = UI["0D"]
            for h in hs.monzos:
                r = p.get_rect()
                r.x = self.rect.w // 2 + (i["start"] * self.speed - self.x)
                r.centery = self.rect.h // 2 - ((song.val@h)*2)
                self.surface.blit(p, r)
            for comma in combinations(hs.monzos, 2):
                h0, h1 = song.val@comma[0], song.val@comma[1]
                comma_72 = abs(h0-h1)
                if comma_72 in song.tuning.vec:
                    p = UI[f"{song.tuning.vec.index(comma_72)+1}D"]
                    r = p.get_rect()
                    r.x = self.rect.w // 2 + (i["start"] * self.speed - self.x)
                    r.centery = self.rect.h // 2 - (h0+h1)  # /2*2 抵消
                    self.surface.blit(p, r)


        # self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        self.beat = song.get_beat()
        self.x = self.speed * self.beat

    def on_mouse_down(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"chords.on_mouse_down: {pos}")
        pass

    def on_mouse_up(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"chords.on_mouse_up: {pos}")
        pass

    def on_key_down(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"chords.on_key_down: {event}")
        if event.unicode == "z":
            song.play()
        if event.unicode == "x":
            song.pause()
        if event.unicode == "c":
            song.resume()

    def on_key_up(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"chords.on_key_up: {event}")
        pass
            