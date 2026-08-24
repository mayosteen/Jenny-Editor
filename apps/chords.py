# core/subtitle.py
from itertools import combinations
from core.template import *
from core.shasav import Monzo, Harmononym, Val
from core.image import UI
from core.color import COLOR
from core.window import Window
from core.events import event_bus
from core.am import am

class Chords(Window):
    def __init__(self):
        # super().__init__("chords", pygame.Rect(0, 1080, 1280, 360))
        super().__init__("chords", pygame.Rect(0, 0, 960, 840))

        self.font_small = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 20)
        self.font = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 30)
        self.font_big = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 50)
        self.beat = 0
        self.speed = 80
        self.x = 0
        self.y = 0
    
    def draw(self, screen:pygame.Surface):
        # 子类重写方法
        # self.surface.fill((103, 102, 129))
        self.surface.fill(COLOR["bg_chords"])
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        # pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
        for n in range(len(song.chords)):
            c0 = song.chords[n]
            c1 = song.chords[n+1] if n<len(song.chords)-1 else {"start":114514, "shasaf":"Ah", "tag":"None", "first":0}
            if c0["start"] <= self.beat < c1["start"]:
                h0 = Harmononym(c0["shasaf"])
                heights = [song.val@m for m in h0.monzos]
                m1 = max(heights)
                m2 = min(heights)
                pygame.draw.rect(self.surface, COLOR["playing_chord"], (
                    #self.rect.w // 2 + (c0["start"] * self.speed - self.x),
                    (c0["start"] * self.speed - self.x),
                    self.rect.h // 2 - (m1*2) -41,
                    (c1["start"]-c0["start"])*40*2,
                    (m1-m2)*2 +82,
                ))
                break

        bar = pygame.Surface((self.rect.w, 2), flags=SRCALPHA)
        bar.fill(COLOR["2D"] + (85,))
        for i in range(-10, 11):
            if i == 0:
                bar1 = pygame.Surface((self.rect.w, 20), flags=SRCALPHA)
                bar1.fill(COLOR["white"] + (20,))
                self.surface.blit(bar1, (0, self.rect.h // 2 - i*song.tuning.vec[1]*2 -10))
            self.surface.blit(bar, (0, self.rect.h // 2 - i*song.tuning.vec[1]*2 -1))
            tag = self.font_small.render({-2:"b7",-1:"4",0:"1",1:"5",2:"2",3:"6",4:"3",5:"7",}.get(i, ""), True, COLOR["white"])
            tagr = tag.get_rect()
            tagr.x = 10
            tagr.centery = self.rect.h // 2 - i*song.tuning.vec[1]*2 -1
            self.surface.blit(tag, tagr)

        bar.fill(COLOR["3D"] + (51,))
        for i in range(-10, 11):
            self.surface.blit(bar, (0, self.rect.h // 2 - i*song.tuning.vec[1]*2 -song.tuning.vec[2]*2 -1))
            tag = self.font_small.render({-3:"5",-2:"2",-1:"6",0:"3",1:"7",2:"#4",3:"#1",}.get(i, ""), True, COLOR["white"])
            tagr = tag.get_rect()
            tagr.x = 10
            tagr.centery = self.rect.h // 2 - i*song.tuning.vec[1]*2 -song.tuning.vec[2]*2 -1
            self.surface.blit(tag, tagr)

        for i in song.chords:
            hs = Harmononym(i["shasaf"])
            p = UI["0D"]
            tag = self.font.render(i["tag"], True, COLOR["white"])
            tagr = tag.get_rect()
            # tagr.center = (self.rect.w // 2 + (i["start"] * self.speed - self.x) + 80, self.rect.h - 20)
            tagr.center = ((i["start"] * self.speed - self.x) + 80, self.rect.h - 20)
            self.surface.blit(tag, tagr)
            bp = UI["bass"]
            br = bp.get_rect()
            # br.x = self.rect.w // 2 + (i["start"] * self.speed - self.x)
            br.x = (i["start"] * self.speed - self.x)
            br.centery = self.rect.h // 2 - ((song.val@hs.monzos[0])*2)
            self.surface.blit(bp, br)
            for h in hs.monzos:
                r = p.get_rect()
                # r.x = self.rect.w // 2 + (i["start"] * self.speed - self.x)
                r.x = (i["start"] * self.speed - self.x)
                r.centery = self.rect.h // 2 - ((song.val@h)*2)
                self.surface.blit(p, r)
            for comma in combinations(hs.monzos, 2):
                h0, h1 = song.val@comma[0], song.val@comma[1]
                comma_72 = abs(h0-h1)
                if comma_72 in song.tuning.vec:
                    p = UI[f"{song.tuning.vec.index(comma_72)+1}D"]
                    r = p.get_rect()
                    # r.x = self.rect.w // 2 + (i["start"] * self.speed - self.x)
                    r.x = (i["start"] * self.speed - self.x)
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
            song.forward(-1.0)
        if event.unicode == "c":
            if song.playing:
                if song.paused:
                    song.resume()
                else:
                    song.pause()
            else:
                song.play()
        if event.unicode == "v":
            song.forward(5.0)
        if event.unicode == "a":
            event_bus.emit("record_start", self.surface)
        if event.unicode == "s":
            event_bus.emit("record_stop", song.music)

    def on_key_up(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"chords.on_key_up: {event}")
        pass

am.register("chords", Chords)