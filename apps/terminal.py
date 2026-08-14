# core/terminal.py
import time
from core.template import *
from core.events import event_bus
from core.window import Window

class Terminal(Window):
    def __init__(self):
        super().__init__("terminal", pygame.Rect(0, 0, 2560, 1440))

        self.font = pygame.font.Font("assets/fonts/svgafix.fon", 12)
        self.path = r"M:\MayOS\>"
        self.commands = [""]
        event_bus.subscribe("print", self.print)

    
    def draw(self, screen):
        self.surface.fill((0, 0, 0))
        for i in range(len(self.commands)):
            # 检测是否为系统提示
            command = self.commands[i]
            if command != "" and command[0] == "ÿ":
                text_surface = self.font.render(self.commands[i][1:], True, (255, 255, 255))
            else:
                text_surface = self.font.render(self.path + self.commands[i], True, (255, 255, 255))
            self.surface.blit(text_surface, (0, i * 16))
        if time.time()-int(time.time())<=0.5:
            pygame.draw.rect(self.surface, (255, 255, 255), (
                (len(self.commands[-1])+len(self.path))*8, 
                (len(self.commands)-1)*16,
                8, 16))
        screen.blit(self.surface, self.rect)
    
    def update(self):
        pass

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
            if command[0] == "/":
                self.run(command)
            self.enter()
        elif event.key == K_BACKSPACE:
            print("terminal.on_key_down: ←")
            if len(self.commands[-1]) > 0:
                self.commands[-1] = self.commands[-1][:-1]
        elif event.unicode and event.unicode.isprintable():
            print(f"terminal.on_key_down: {event.unicode}")
            if self.commands[-1] != "" and event.unicode == "/":
                self.enter()
            self.commands[-1] += event.unicode

    def on_key_up(self, event:pygame.event.Event):
        if event.key in (K_RETURN, K_KP_ENTER):
            print("terminal.on_key_up: \\n")
        elif event.key == K_BACKSPACE:
            print("terminal.on_key_up: ←")
        elif event.unicode and event.unicode.isprintable():
            print(f"terminal.on_key_up: {event.unicode}")

    def enter(self):
        print(f"terminal.enter:_")
        self.commands.append("")

    def print(self, command:str):
        if command != "":
            self.commands.append("ÿ" + command)
        else:
            raise IndexError("you have just printed 棍母")
        # self.enter()

    def run(self, command:str):
        params = command.split()
        if len(params) == 1:
            state = params[0]
            if state in ["/ai", "/ymq", "/ym7", "/zenia"]:
                self.print("Zenia AI is unavailable.")
            else:
                self.print("Invalid command.")
                self.print("state")
        elif len(params) >= 2:
            state, app, *args = params
            if state == "/open":
                event_bus.emit("request_open", app)
            elif state == "/close":
                event_bus.emit("request_close", app)
            elif state == "/list":
                if app == "window":
                    event_bus.emit("request_window_list")
            else:
                self.print("Invalid command.")
            