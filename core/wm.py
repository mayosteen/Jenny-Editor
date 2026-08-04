# core/wm.py
import pygame
from pygame.sprite import LayeredUpdates
from core.events import event_bus


class WindowManager:
    def __init__(self):
        self.group = LayeredUpdates()
        self.windows = []
        self.system_sprites = []
        self.focused = None

        # ✅ 输入事件（唯一入口）
        event_bus.subscribe("mouse_down", self._on_down)
        event_bus.subscribe("mouse_up",   self._on_up)
        event_bus.subscribe("mouse_move", self._on_move)

        # ✅ 应用请求打开窗口（关键修复）
        event_bus.subscribe("request_open_window", self._on_request_open)

    # ---------- 窗口管理 ----------
    def open(self, window):
        self.windows.append(window)
        self.group.add(window.sprite, layer=len(self.windows))
        self.focused = window
        event_bus.emit("window_opened", window)

    def close(self, window):
        window.close()

    # ---------- 系统 Sprite ----------
    def add_system(self, sprite):
        self.system_sprites.append(sprite)
        self.group.add(sprite, layer=9999)

    # ---------- 输入分发 ----------
    def _on_down(self, data):
        mx, my = data["pos"]

        # 系统 Sprite 优先（Taskbar）
        for spr in self.system_sprites:
            if hasattr(spr, "on_mouse_down") and spr.rect.collidepoint(mx, my):
                spr.on_mouse_down(data)
                return

        # 窗口（从顶到底）
        for w in reversed(self.windows):
            if not w.is_alive():
                continue

            lx, ly = w.hit_test((mx, my))
            if w.on_mouse_down((lx, ly)):
                self.focused = w
                if w.sprite.alive():
                    self.group.move_to_front(w.sprite)
                return

    def _on_up(self, data):
        mx, my = data["pos"]

        for spr in self.system_sprites:
            if hasattr(spr, "on_mouse_up"):
                spr.on_mouse_up(data)

        for w in self.windows:
            if not w.is_alive():
                continue
            w.on_mouse_up(w.hit_test((mx, my)))

    def _on_move(self, data):
        if self.focused and self.focused.is_alive():
            mx, my = data["pos"]
            self.focused.on_mouse_move(self.focused.hit_test((mx, my)))

    # ---------- 应用请求 ----------
    def _on_request_open(self, name):
        from apps.terminal import Terminal
        # from apps.explorer import Explorer
        # from apps.control import Control

        if name == "terminal":
            self.open(Terminal())
        # elif name == "explorer":
        #     self.open(Explorer())
        # elif name == "control":
        #     self.open(Control())

    # ---------- 统一回收 ----------
    def update(self):
        self.group.update()

        dead_windows = [w for w in self.windows if not w.is_alive()]
        for w in dead_windows:
            w.sprite.kill()
            self.windows.remove(w)

        if self.focused and not self.focused.is_alive():
            self.focused = self.windows[-1] if self.windows else None

    def draw(self, surface):
        self.group.draw(surface)