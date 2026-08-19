# core/subtitle.py
from itertools import combinations
from core.template import *
from core.shasav import Monzo, Harmononym, Val, Tuning
from core.image import UI
from core.events import event_bus
from core.window import Window

class CaftR(Window):
    def __init__(self):
        super().__init__("caftr", pygame.Rect(1800, 0, 120, 1080))

        self.font = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 20)
        self.showing = "Chords"
        self.beat = 0
        self.val = Val(96)
        self.tuning = Tuning(96)
    
    def render_subtitle(self):
        foreground = self.font.render(self.showing, True, (255, 255, 255))
        f_rect = foreground.get_rect()
        f_rect.center = (self.rect.w//2, self.rect.h//2)
        self.surface.blit(foreground, f_rect)
    
    def draw(self, screen:pygame.Surface):
        # 子类重写方法
        self.surface.fill((0, 0, 0, 178))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        # pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
        for i in reversed(song.chords):
            if self.beat >= i["start"]:
                hs = Harmononym(i["shasaf"])
                p = UI["0D_96"]
                for h in hs.monzos:
                    r = p.get_rect()
                    r.x = 0
                    r.centery = 848 - (self.val@h)
                    self.surface.blit(p, r)
                for comma in combinations(hs.monzos, 2):
                    h0, h1 = self.val@comma[0], self.val@comma[1]
                    comma_96 = abs(h0-h1)
                    if comma_96 in self.tuning.vec:
                        p = UI[f"{self.tuning.vec.index(comma_96)+1}D_96"]
                        r = p.get_rect()
                        r.x = 0
                        r.centery = 848 - (h0+h1)//2
                        self.surface.blit(p, r)
                break


        # self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        self.beat = song.get_beat()
            