# core/subtitle.py
from itertools import combinations
from core.template import *
from core.shasav import Monzo, Harmononym, Val, Tuning
from core.paper import Interval
from core.image import UI
from core.events import event_bus
from core.window import Window
from core.am import am

class CaftR(Window):
    def __init__(self):
        super().__init__("caftr", pygame.Rect(1800, 0, 120, 1080))

        self.font = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 20)
        self.showing = "Chords"
        self.beat = 0
        self.isb = 8  # interval_showing_beat
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
        for n in range(len(song.chords)):
            c0 = song.chords[n]
            c1 = song.chords[n+1] if n<len(song.chords)-1 else {"start":114514, "shasaf":"Ah", "tag":"None", "first":0}
            if c0["start"] <= self.beat < c1["start"]:
                h0 = Harmononym(c0["shasaf"])
                p = UI["0D_96"]
                bass_y = 848 - -min([self.val@h for h in h0.monzos])
                for h in h0.monzos:
                    r = p.get_rect()
                    r.x = 0
                    r.centery = bass_y - (self.val@h)
                    self.surface.blit(p, r)
                for comma in combinations(h0.monzos, 2):
                    ht0, ht1 = self.val@comma[0], self.val@comma[1]
                    comma_96 = abs(ht0-ht1)
                    if comma_96 in self.tuning.vec:
                        p = UI[f"{self.tuning.vec.index(comma_96)+1}D_96"]
                        r = p.get_rect()
                        r.x = 0
                        r.centery = bass_y - (ht0+ht1)//2
                        self.surface.blit(p, r)
                r = UI["bass_96"].get_rect()
                r.x = 0
                r.centery = bass_y - (self.val@h0.monzos[0])
                self.surface.blit(UI["bass_96"], r)
                

                if n == len(song.chords)-1:
                    self.isb = 8
                else:
                    self.isb = c1["start"] - c0["start"]
                if n == 0 or c0["first"]:
                    self.blit(Interval(h0.monzos[0], (63, 985), alpha=(c0["start"]+self.isb-self.beat)/self.isb, first=True))
                elif c0["shasaf"].startswith("Ah"):
                    self.blit(Interval(Monzo("Ah"), (63, 985), alpha=(c0["start"]+self.isb-self.beat)/self.isb, ah=True))
                else:
                    cB = song.chords[n-1]
                    hB = Harmononym(cB["shasaf"])
                    self.blit(Interval(h0.monzos[0] - hB.monzos[0], (63, 985), alpha=(c0["start"]+self.isb-self.beat)/self.isb))
                break

        self.surface.blit(UI["bar_caftaphata"], (0, 900))


        # self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        self.beat = song.get_beat()

am.register("caftr", CaftR)  