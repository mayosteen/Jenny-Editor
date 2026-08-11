# core/terminal.py
from core.template import *
from core.events import event_bus
from core.window import Window

class Terminal(Window):
    def __init__(self):
        super().__init__("terminal", pygame.Rect(0, 0, 1920, 1080))

        self.font = pygame.font.Font("assets/fonts/SIMSUN.TTF", 16)
        self.commands = [""]
        event_bus.subscribe("pygame.event", self.handle_event)

    
    def draw(self, screen):
        self.surface.fill((0, 0, 0))
        for i in range(len(self.commands)):
            text_surface = self.font.render("> " + self.commands[i], False, (255, 255, 255))
            self.surface.blit(text_surface, (10, 30 + i * 20))
        screen.blit(self.surface, self.rect)
    
    def update(self):
        pass

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.on_mouse_down(event)
        elif event.type == MOUSEBUTTONUP:
            self.on_mouse_up(event)
        elif event.type == KEYDOWN:
            self.on_key_down(event)
        elif event.type == KEYUP:
            self.on_key_up(event)

    def on_mouse_down(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"terminal.on_mouse_down: {pos}")
        pass

    def on_mouse_up(self, pos:tuple[int, int]):
        # 子类重写方法
        print(f"terminal.on_mouse_up: {pos}")
        pass

    def on_key_down(self, event:pygame.event.Event):
        if event.key in (K_RETURN, K_KP_ENTER):
            print("terminal.on_key_down: \\n")
            command = self.commands[-1].rstrip("\n\r")
            print(command)
            if command:
                self.run(command)
            self.commands.append("")
        elif event.key == K_BACKSPACE:
            print("terminal.on_key_down: ←")
            if len(self.commands[-1]) != 0:
                self.commands[-1] = self.commands[-1][:-1]
        elif event.unicode and event.unicode.isprintable():
            print(f"terminal.on_key_down: {event.unicode}")
            self.commands[-1] += event.unicode

    def on_key_up(self, event:pygame.event.Event):
        # 子类重写方法
        print(f"terminal.on_key_up: {event}")
        pass

    def run(self, command:str):
        print(command.split())
        state, app, *args = command.split()
        if state == "/open":
            event_bus.emit("request_open", app)
        elif state == "/close":
            event_bus.emit("request_close", app)
        elif state == "/list":
            if app == "window":
                event_bus.emit("request_window_list")
            