# core/window.py
import pygame
from core.sprite import WindowSprite
from core.ui import UI

PANEL_H = 40
BTN = 40


class Window:
    def __init__(self, title, rect):
        self.title = title
        self.rect = pygame.Rect(rect)
        self.sprite = WindowSprite(self)
        self.alive = True  # ✅ 新增：存活状态

        # 底部悬浮面板
        self.panel_rect = pygame.Rect(
            BTN * 3,
            self.rect.height - PANEL_H,
            self.rect.width - BTN * 4,
            PANEL_H
        )

        # 按钮
        self.close_rect = pygame.Rect(0,     self.rect.height - PANEL_H, BTN, BTN)
        self.max_rect   = pygame.Rect(BTN,   self.rect.height - PANEL_H, BTN, BTN)
        self.min_rect   = pygame.Rect(BTN*2, self.rect.height - PANEL_H, BTN, BTN)

        # resize
        self.resize_rect = pygame.Rect(
            self.rect.width - BTN,
            self.rect.height - PANEL_H,
            BTN,
            BTN
        )

        self._dragging = False
        self._resizing = False
        self._drag_offset = (0, 0)
        self._orig_rect = self.rect.copy()

    # ---------- 生命周期 ----------
    def update(self):
        pass

    def close(self):
        """✅ 仅标记死亡，不 kill"""
        self.alive = False

    def is_alive(self):
        """✅ 统一存活判断"""
        return self.alive and self.sprite.alive()

    # ---------- 渲染 ----------
    def _draw_content(self):
        self.sprite.image.fill((30, 30, 35))

        self.sprite.image.blit(UI["close"], self.close_rect.topleft)
        self.sprite.image.blit(UI["max"],   self.max_rect.topleft)
        self.sprite.image.blit(UI["min"],   self.min_rect.topleft)
        self.sprite.image.blit(UI["resize"], self.resize_rect.topleft)

        font = pygame.font.Font("assets/fonts/GothamPro.ttf", 24)
        txt = font.render(self.title, True, (220, 220, 220))
        txt_rect = txt.get_rect()
        txt_rect.x = self.panel_rect.x + 12
        txt_rect.centery = self.panel_rect.centery
        self.sprite.image.blit(txt, txt_rect)

    # ---------- 坐标 ----------
    def hit_test(self, pos):
        return (
            pos[0] - self.rect.x,
            pos[1] - self.rect.y
        )

    # ---------- 输入（✅ 不销毁） ----------
    def on_mouse_down(self, local_pos):
        lx, ly = local_pos

        if self.close_rect.collidepoint(lx, ly):
            self.close()  # ✅ 只标记
            return True

        if self.max_rect.collidepoint(lx, ly):
            return True

        if self.min_rect.collidepoint(lx, ly):
            return True

        if self.resize_rect.collidepoint(lx, ly):
            self._resizing = True
            self._orig_rect = self.rect.copy()
            self._drag_offset = (lx, ly)
            return True

        if self.panel_rect.collidepoint(lx, ly):
            self._dragging = True
            self._drag_offset = (lx, ly)
            return True

        return False

    def on_mouse_up(self, local_pos):
        self._dragging = False
        self._resizing = False

    def on_mouse_move(self, local_pos):
        lx, ly = local_pos

        if self._dragging:
            mx, my = pygame.mouse.get_pos()
            self.rect.x = mx - self._drag_offset[0]
            self.rect.y = my - self._drag_offset[1]

        if self._resizing:
            dx = lx - self._drag_offset[0]
            dy = ly - self._drag_offset[1]

            new_w = max(200, self._orig_rect.width + dx)
            new_h = max(120, self._orig_rect.height + dy)

            self.rect.size = (new_w, new_h)

            self.sprite.image = pygame.Surface((new_w, new_h), pygame.SRCALPHA)
            self.sprite.rect.size = (new_w, new_h)

            self.panel_rect.y = new_h - PANEL_H
            self.panel_rect.width = new_w - BTN * 4

            self.close_rect.topleft = (0, new_h - PANEL_H)
            self.max_rect.topleft   = (BTN, new_h - PANEL_H)
            self.min_rect.topleft   = (BTN*2, new_h - PANEL_H)
            self.resize_rect.topleft = (new_w - BTN, new_h - PANEL_H)