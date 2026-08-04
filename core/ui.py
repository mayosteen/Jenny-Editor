# core/ui.py
import pygame

UI = {}
_LOADED = False

def load_ui():
    global _LOADED, UI
    if _LOADED:
        return

    def load(name):
        img = pygame.image.load(f"assets/UI/{name}.png")
        return img.convert_alpha()

    names = (
        "base",
        "close",
        "max",
        "min",
        "resize",
        "mayos",
        "terminal",
        "explorer",
        "control",
        "highlight",
    )

    for n in names:
        UI[n] = load(n)

    _LOADED = True
