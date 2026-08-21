import pygame
from pygame.locals import *  # type:ignore
from core.config import V_WIDTH, V_HEIGHT
from core.shasav import Monzo
from core.color import COLOR

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
        self.rect.center = trans(self._pos)
        
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
    #     self.rect.center = trans(self._pos)

    @property
    def color(self): return self._color
    @color.setter
    def color(self, color):
        self._color = color
        self.render()


qoz = pygame.font.Font("assets/fonts/Qoz.ttf", 35)

class Interval(Paper):
    def __init__(self, monzo:Monzo, pos, alpha=1, first=False, ah=False):
        self.chars = []
        self.x = 0
        self.y = 0
        if first:
            self.add_words(",", COLOR["1D"])
        # print(monzo)
        for p,v in zip(range(1, 17), monzo.vec):
            if 2 <= p <= 6:
                c = COLOR[f"{p}D"]
                if v > 0:
                    self.add_words(str(p) + "+" * abs(v), c)
                if v < 0:
                    self.add_words(str(p) + "-" * abs(v), c)
        if len(self.chars) == 1 and first:
            self.chars = []
            self.x = 0
            self.add_words("!", COLOR["1D"])
        elif len(self.chars) == 0 and ah:
            self.add_words("<", COLOR["1D"])
        elif len(self.chars) == 0 and not ah:
            self.add_words("1", COLOR["1D"])
        self.surface = pygame.Surface((self.x, self.y), flags=SRCALPHA)
        for i in self.chars:
            self.surface.blit(i[0], i[1])

        self.surface.set_alpha(min(int(alpha * 256), 255))
        self.rect = self.surface.get_rect()
        self._pos = pos
        self.rect.center = self._pos  # 不用trans因为caftr没有用trans逆向
        # print(self.rect)

    def add_words(self, string, color):
        char = qoz.render(string, True, color)
        self.chars.append([char, (self.x, 0)])
        self.x += char.get_width()
        self.y = max(self.y, char.get_height())



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
