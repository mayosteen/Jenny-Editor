from core.events import event_bus

class WM:
    def __init__(self):
        self.windows = []
        event_bus.subscribe("request_close", self.close)
        event_bus.subscribe("request_window_list", self.window_list)

    def open(self, window):
        print(f"wm.open: {window.title}")
        self.windows.append(window)

    def active(self, window):
        if window in self.windows:
            self.windows.remove(window)
            self.windows.append(window)

    def close(self, window):
        if window in self.windows:
            self.windows.remove(window)
        elif isinstance(window, str) and window.lower() != "terminal":
            for w in self.windows[:]:
                if w.title.lower() == window.lower():
                    self.windows.remove(w)
    
    def window_list(self, _):
        titles = [window.title for window in self.windows]
        print(" ".join(titles))
    
    def draw(self, screen):
        for window in self.windows:
            window.draw(screen)
    
    def update(self):
        for window in self.windows:
            window.update()