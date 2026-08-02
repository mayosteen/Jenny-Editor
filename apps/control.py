import json, zipfile

from core.config import *

from core.window import Window, Button


class Project:
    def __init__(self, project_file_name:str):
        if project_file_name.lower() == "default":
            pass
        elif project_file_name.lower().endswith((".jenny", ".jen", ".jny", ".zip")):
            with zipfile.ZipFile(project_file_name, "r") as z:
                z.extractall("./project")
        with open("./project/index.json", "r", encoding="utf-8") as f:
            self.index = json.load(f)


project = Project("default")


class Control(Window):
    def __init__(self, *args):
        super().__init__("Control", args)
        self.buttons += [
            Button(self, "btn_forward", "c", (12,  12)),
            Button(self, "btn_play",    "c", (64,  12)),
            Button(self, "btn_rewind",  "c", (116, 12)),
        ]
    

    def _draw_content(self):
        self.fill((128, 128, 128))
        self.draw_rect(COLORS["control_bg"], (1, 1, self.rect.w-2, self.rect.h-2))
        for b in self.buttons:
            self.draw_btn(b)
    

    def get_surface(self, screen):
        screen.draw(self)


    def onclick(self, pos):
        for b in self.buttons:
            if b.collide(pos):
                print(f"{__name__}.{self.__class__.__name__}.onclick:{b.tag}")
                if b.tag == "btn_close":
                    self.close()
                if b.tag == "btn_max":
                    self.state = "max"
                if b.tag == "btn_min":
                    self.state = "min"
                if b.tag == "btn_drag":
                    self.dragging = True
                    self.drag_offset = (
                        pos[0] - self.rect.x,
                        pos[1] - self.rect.y
                    )
                return b.tag


    def onmove(self, pos):
        # 子类重写这里
        print(f"{__name__}.{self.__class__.__name__}.onmove:{pos}")
        if self.dragging:
            self.drag_rect.x = pos[0] - self.drag_offset[0]
            self.drag_rect.y = pos[1] - self.drag_offset[1]


    def onrelease(self, pos):
        # 子类重写这里
        print(f"{__name__}.{self.__class__.__name__}.onrelease:{pos}")
        if self.dragging:
            self.dragging = False
            self.rect.x = pos[0] - self.drag_offset[0]
            self.rect.y = pos[1] - self.drag_offset[1]