# core/subtitle.py
from core.template import *
from core.window import Window
from core.curves import io_circle
from core.config import V_WIDTH, V_HEIGHT
from core.events import event_bus
from core.am import am

class Animation(Window):
    def __init__(self):
        super().__init__("animation", pygame.Rect(0, 0, V_WIDTH, V_HEIGHT))

        self.font = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 20)
        self.beat = 0
        self.speed = 80
        self.x = 0
        self.y = 0
        self.windows = [
            am.get("chords")(),
            am.get("subtitle")(),
            am.get("caftr")(),
            ]
    
    def draw(self, screen:pygame.Surface):
        # 子类重写方法
        # self.surface.fill((139, 28, 27))
        self.surface.fill((30, 72, 109))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        # pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
        for id, sprite in song.sprites.items():
            if self.beat <= sprite.anim[0]["start"]:
                sprite.pos = sprite.anim[0]["position"]
            else:
                for p in range(len(sprite.anim)-1):
                    a0 = sprite.anim[p]
                    a1 = sprite.anim[p+1]
                    if a0["start"] <= self.beat <= a1["start"]:
                        p0 = a0["position"]
                        p1 = a1["position"]
                        sprite.pos = io_circle(p0, p1, (self.beat-a0["start"])/(a1["start"]-a0["start"]))
                            
            self.blit(sprite)

        for window in self.windows:
            window.draw(self.surface)
        # self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        event_bus.emit("record_update")
        self.beat = song.get_beat()
        for window in self.windows:
            window.update()

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
        print(f"animation.on_key_up: {event}")
        pass

am.register("animation", Animation)