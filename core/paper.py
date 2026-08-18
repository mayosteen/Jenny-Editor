import pygame
from core.config import V_WIDTH, V_HEIGHT

pygame.font.init()

def trans(p) -> tuple[int, int]:
    return (
        V_WIDTH//2+p[0],
        V_HEIGHT//2-p[1]
    )

class Paper:
    def __init__(self, surface:pygame.Surface, pos:tuple[int, int], animation):
        self.surface = surface.copy()
        self.rect = self.surface.get_rect()
        self._pos = pos
        self.rect.center = trans(self._pos)
        self.anim = animation

    @property
    def pos(self): return self._pos
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self.rect.center = trans(self._pos)

class Sprite(Paper):
    def __init__(self, img_path:str, pos:tuple[int, int], animation):
        super().__init__(pygame.image.load("project" + img_path), pos, animation)


class Rectangle(Paper):
    def __init__(self, size, color, pos, animation):
        self._size = size
        self._color = color
        self.surface = pygame.Surface(self._size, flags=pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self._pos = pos
        self.rect.center = trans(self._pos)
        self.anim = animation
        self.render()

    def render(self):
        self.surface.fill((self.color))

    @property
    def size(self): return self._color
    @size.setter
    def size(self, size):
        self._size = size
        self.surface = pygame.Surface(self._size, flags=pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.render()

    @property
    def color(self): return self._color
    @color.setter
    def color(self, color):
        self._color = color
        self.render()


class Text(Paper):
    def __init__(self, text:str, fontpath:str, size:int, color, pos:tuple[int, int], animation):
        self._text = text
        self.font = pygame.font.Font("assets/fonts/" + fontpath, size)
        self._aa = True
        self._color = color
        self._pos = pos
        self.anim = animation
        self.render()

    def render(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        self.rect.center = self._pos
        
    @property
    def text(self): return self._text
    @text.setter
    def text(self, text):
        self._text = text
        self.render()

    # @property
    # def pos(self): return self._pos
    # @pos.setter
    # def pos(self, pos):
    #     self._pos = pos
    #     self.rect.center = self._pos

    @property
    def color(self): return self._color
    @color.setter
    def color(self, color):
        self._color = color
        self.render()

def load_paper(pinfos):
    papers = {}
    for pinfo in pinfos:
        if pinfo["type"] == "text":
            paper = Text(
                text=pinfo["content"],
                fontpath=pinfo.get("fontpath", "HarmonyOSSansSCRegular.ttf"),
                size=pinfo["size"],
                color=pinfo["color"],
                pos=pinfo["position"],
                animation=pinfo["animation"],
            )
        elif pinfo["type"] == "sprite":
            paper = Sprite(
                img_path=pinfo["image"],
                pos=pinfo["position"],
                animation=pinfo["animation"],
            )
        elif pinfo["type"] in ["rect", "rectangle"]:
            paper = Rectangle(
                size=pinfo["size"],
                color=pinfo["color"],
                pos=pinfo["position"],
                animation=pinfo["animation"],
            )
        else:
            paper = Paper(pygame.Surface((100, 100)), (0, 0), [])
        papers[pinfo["id"]] = paper
    return papers
