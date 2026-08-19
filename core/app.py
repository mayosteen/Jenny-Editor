from core.template import *
from core.events import event_bus
from core.wm import WM
from core.config import *

class MayOS:
    def __init__(self):
        pygame.init()
        os.environ["SDL_VIDEO_WINDOW_POS"] = "%d, %d" % (0, 0)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        self.running = True
        self.wm = WM()
        event_bus.subscribe("request_open", self.open)
        event_bus.emit("request_open", "terminal")
        event_bus.emit("request_open", "chords")
        event_bus.emit("request_open", "subtitle")
        event_bus.emit("request_open", "animation")
            
    
    def open(self, app:str):
        app = app.lower()
        if   app == "terminal":
            from apps.terminal import Terminal
            self.wm.open(Terminal())
        elif app == "subtitle":
            from apps.subtitle import Subtitle
            self.wm.open(Subtitle())
        elif app == "chords":
            from apps.chords import Chords
            self.wm.open(Chords())
        elif app == "animation":
            from apps.animation import Animation
            self.wm.open(Animation())


    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif e.type == MOUSEBUTTONDOWN:
                    for window in reversed(self.wm.windows):
                        if window.rect.collidepoint(e.pos):
                            self.wm.active(window)
                            window.on_mouse_down((e.pos[0]-window.rect.x, e.pos[1]-window.rect.y))
                            break
                elif e.type == MOUSEBUTTONUP:
                    for window in reversed(self.wm.windows):
                        if window.rect.collidepoint(e.pos):
                            window.on_mouse_up((e.pos[0]-window.rect.x, e.pos[1]-window.rect.y))
                            break
                elif e.type == KEYDOWN:
                    if e.unicode == "/":
                        self.wm.active("terminal")
                    self.wm.windows[-1].on_key_down(e)
                elif e.type == KEYUP:
                    self.wm.windows[-1].on_key_up(e)

            self.screen.fill((0, 0, 0))
            self.wm.draw(self.screen)
            self.wm.update()
            pygame.display.flip()
            # self.clock.tick(60)
