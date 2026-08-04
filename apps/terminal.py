# apps/terminal.py
import pygame
from core.window import Window
from core.events import event_bus

FONT_PATH = "assets/fonts/LXGWWenKaiMonoGBScreen.ttf"
FONT_SIZE = 16


class Terminal(Window):
    def __init__(self):
        super().__init__("terminal", (100, 80, 720, 420))
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)
        self.fg = (220, 220, 220)
        self.buffer = "> "

        event_bus.subscribe("key_down", self._on_key_down)

    def _on_key_down(self, data):
        k, u = data["key"], data["unicode"]
        if k == pygame.K_RETURN:
            self.buffer += "\n> "
        elif k == pygame.K_BACKSPACE and len(self.buffer) > 2:
            self.buffer = self.buffer[:-1]
        elif u:
            self.buffer += u

    def _draw_content(self):
        # 内容区全窗口
        self.sprite.image.fill((20, 20, 25))

        # 调用父类画底部面板 + 按钮
        super()._draw_content()

        # 终端文字
        x, y = 8, 8
        line_h = self.font.get_height()

        for line in self.buffer.split("\n"):
            self.sprite.image.blit(
                self.font.render(line, True, self.fg),
                (x, y)
            )
            y += line_h