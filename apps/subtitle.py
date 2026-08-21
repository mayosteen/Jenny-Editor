# core/subtitle.py
from core.template import *
from core.events import event_bus
from core.window import Window

class Subtitle(Window):
    def __init__(self):
        # super().__init__("subtitle", pygame.Rect(1280, 1080, 1280, 360))
        super().__init__("chords", pygame.Rect(0, 840, 1800, 240))

        self.font = pygame.font.Font("assets/fonts/HarmonyOSSansSCRegular.ttf", 120)
        self.showing = "歌词"
    
    def render_subtitle(self):
        foreground = self.font.render(self.showing, True, (255, 255, 255))
        f_rect = foreground.get_rect()
        f_rect.center = (self.rect.w//2, self.rect.h//2)
        self.surface.blit(foreground, f_rect)
    
    def draw(self, screen:pygame.Surface):
        # 子类重写方法
        self.surface.fill((0, 0, 0, 0))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, 0, self.rect.w, 1))
        # pygame.draw.rect(self.surface, (180, 179, 193), (self.rect.w-1, 0, 1, self.rect.h))
        # pygame.draw.rect(self.surface, (180, 179, 193), (0, self.rect.h-1, self.rect.w, 1))
        self.render_subtitle()
        screen.blit(self.surface, self.rect)
    
    def update(self):
        beat = song.get_beat()
        if beat < song.chords[0]["start"]:
            self.showing = "歌词"
        for subtext in song.subtitles:
            if beat >= subtext["start"]:
                self.showing = subtext["text"]
            else:
                break

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
        print(f"subtitle.on_key_up: {event}")
        pass
            