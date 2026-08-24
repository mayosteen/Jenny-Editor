# core/grid.py
from itertools import combinations
from core.template import *
from core.shasav import Monzo, Harmononym, Val
from core.image import UI
from core.color import COLOR
from core.window import Window
from core.events import event_bus
from core.am import am

class Grid(Window):
    def __init__(self):
        # super().__init__("chords", pygame.Rect(0, 1080, 1280, 360))
        super().__init__("grid", pygame.Rect(960, 0, 960, 840))

        self.font = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 20)
        self.beat = 0
        self.size = 64
        self.x = 0
        self.y = 0

    def grid_rect(self, m:Monzo):
        x = m.vec[1] if len(m.vec) >= 2 else 0  # 2D
        y = m.vec[2] if len(m.vec) >= 3 else 0  # 3D
        r = pygame.Rect((0, 0, self.size, self.size))
        r.center = (self.rect.w//2 + x*self.size, self.rect.h//2 - y*self.size)
        return r

    def draw_bass(self, b:Monzo, w:Monzo):
        if b == w:
            self.surface.blit(UI["grid_bass"], self.grid_rect(b))
        else:
            self.surface.blit(UI["grid_bass_white"], self.grid_rect(b))

    def draw_block(self, color, m):
        return pygame.draw.rect(self.surface, color, self.grid_rect(m))
    
    def draw(self, screen:pygame.Surface):
        # 子类重写方法
        # self.surface.fill((103, 102, 129))
        self.surface.fill(COLOR["bg"])
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        # pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
            
        for n in range(len(song.chords)):
            c0 = song.chords[n]
            c1 = song.chords[n+1] if n<len(song.chords)-1 else {"start":114514, "shasaf":"Ah", "tag":"None", "first":0}
            if c0["start"] <= self.beat < c1["start"]:
                h0 = Harmononym(c0["shasaf"])
                w = b = h0.monzos[0]
                for m in h0.monzos:
                    dif = m-w
                    if len(dif.vec) == 2 and dif.vec[1] < 0:
                        w = m
                for m in h0.monzos:
                    dim = \
                        "white" if m==w else \
                        "3D" if len((m-w).vec) >= 3 else \
                        "2D"
                    self.draw_block(COLOR[dim], m)
                self.draw_bass(b, w)
                break

        # 竖线
        bar = pygame.Surface((2, self.rect.h), flags=SRCALPHA)
        bar.fill(COLOR["gridline"])
        for i in range(-12, 12):
            self.surface.blit(bar, (self.rect.w//2 -self.size//2 +i*self.size -1, 0))

        # 横线
        bar = pygame.Surface((self.rect.w, 2), flags=SRCALPHA)
        bar.fill(COLOR["gridline"])
        for i in range(-10, 10):
            self.surface.blit(bar, (0, self.rect.h//2 -self.size//2 -i*self.size -1))

        # self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        self.beat = song.get_beat()

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

am.register("grid", Grid)