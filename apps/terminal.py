from core.window import Window


class Terminal(Window):
    def __init__(self, *rect):
        super().__init__("terminal", *rect)
        self.command = ""
    
    def _draw_content(self):
        self.fill((0, 0, 0))
    
    def onkeydown(self, key):
        print(f"{__name__}.{self.__class__.__name__}.onkeydown:{key}")
        self.command += chr(key)