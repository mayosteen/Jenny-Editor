# main.py
# coding:utf-8


# region 初始化

import sys, os
from itertools import combinations

import pygame
from pygame.locals import * # type: ignore

from core.config import *
import core.file
import apps.record


pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

x_pos = (screen_width - WIDTH) // 2
y_pos = (screen_height - HEIGHT) // 2
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x_pos},{y_pos}'
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=0)
pygame.display.set_caption("Jenny Player")

# endregion


# 声音类
from core.song import Song

# region Transform类

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Scaler:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self.resize_update()

    def resize_update(self):
        global SPRITES
        for key,value in ORIGINAL_SPRITES.items():
            origin_width, origin_height = value.get_size()
            sprite_width = origin_width * self.x // DEFAULT_SCALE
            sprite_height = origin_height * self.y // DEFAULT_SCALE
            SPRITES[key] = pygame.transform.smoothscale(value, (sprite_width, sprite_height))
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self.resize_update()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self.resize_update()

# endregion

# region 渲染类

class GameSprite:
    def __init__(self, window:pygame.Surface, image_index, position):
        self.window = window

        self.image_index = image_index
        self.x, self.y = position
        
    def draw(self, region:Vec2):
        image = SPRITES[self.image_index]
        rect = image.get_rect()
        rect.x = (self.x + region.x - cam.x) * scale.x + WIDTH/2
        rect.centery = - (self.y + region.y - cam.y) * scale.y + HEIGHT/2
        self.window.blit(image, rect)

class PlayHead:
    def __init__(self, window:pygame.Surface, image=pygame.image.load("./assets/sprites/playhead.png")):
        self.window = window
        self.image = pygame.transform.scale(image, (10, HEIGHT))
        
    def draw(self):
        rect = self.image.get_rect()
        rect.right = WIDTH//2
        self.window.blit(self.image, rect)

class Column:
    def __init__(self, screen, index, chord):
        self.screen = screen
        self.index = index
        _beat = chord["beat"]
        tag = chord["tag"]
        tonic = tonic_calculate(_beat)
        self.region = Vec2(80 * index, tonic)
        self.lines = chord_map[tag]
        self.sprites = []

        for i in range(-20, 20):
            self.sprites.append(GameSprite(self.screen, "g2", (0, INTERVALS[2]*i)))
            self.sprites.append(GameSprite(self.screen, "g3", (0, INTERVALS[2]*i+INTERVALS[3])))

        for line in self.lines:
            self.sprites.append(GameSprite(self.screen, 0, (0, line)))

        for bar in combinations(self.lines, 2):
            interval = abs(bar[0]-bar[1])
            y = (bar[0]+bar[1]) / 2
            if interval in INTERVALS:
                dimen_index = INTERVALS.index(interval)

                self.sprites.append(GameSprite(self.screen, dimen_index, (0, y)))

    def draw(self):
        for sprite in self.sprites:
            sprite.draw(self.region)

    def draw_mask(self):
        mask = pygame.Surface(
            (80 * scale.x, (max(self.lines) - min(self.lines) + 40) * scale.y),
            SRCALPHA
            )
        mask.fill((255, 255, 255, 34))
        self.screen.blit(mask, (
            (self.region.x - cam.x) * scale.x + WIDTH/2,
            -(self.region.y + max(self.lines) + 20 - cam.y) * scale.y + HEIGHT/2
        ))

# endregion

# region 文本类

class Text:
    def __init__(self, window, custom_font):
        self.window = window
        self.font = custom_font

    def render(self, text:str, position=(0, 0), l_distance=25):
        for l_index, line in enumerate(text.split("\n")):
            text = self.font.render(line, True, (232, 199, 77))
            self.window.blit(text, (position[0], position[1] + l_index * l_distance))

# endregion


# region 计算函数

def tonic_calculate(target_beat):
    _tonic = chords["tonic"]
    for event in chords["events"]:
        if event["beat"] > target_beat:
            return _tonic
        elif event["type"] == 1:
            _tonic = event["value"]
    return _tonic

# 歌曲首末默认速度
SPEED = 2

def lerp(arr, x, f_weight=lambda t:t):
    if x <= arr[0]:
        return x / SPEED
    elif x >= arr[-1]:
        return len(arr)-1 + (x-arr[-1])/SPEED
    
    for i in range(len(arr)-1):
        a = arr[i]
        b = arr[i+1]
        if a <= x <= b:
            t = (x-a) / (b-a)
            return i + f_weight(t)
    
    return 0

# endregion

# region 事件函数

def quit():
    global state
    state = States.QUIT
    pygame.quit()
    sys.exit()

# endregion

# region 事件

def update():
    global state, cam, scale, beat
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                quit()

            if event.key == K_F1:
                apps.record.start(screen)
            elif event.key == K_F2:
                apps.record.stop(f".\\{index.get('song') or index.get('ogg')}", "./output.mp4")

            elif event.key == K_d:
                cam.x += 80
            elif event.key == K_a:
                cam.x -= 80
            elif event.key == K_w:
                cam.y += 72
            elif event.key == K_s:
                cam.y -= 72
                
            elif event.key == K_h:
                scale.x += 0.5
            elif event.key == K_f:
                scale.x -= 0.5
            elif event.key == K_t:
                scale.y += 0.5
            elif event.key == K_g:
                scale.y -= 0.5

            elif event.key == K_SPACE:
                song.play_or_pause()

# endregion

# region 时控和逻辑

clock = pygame.time.Clock()

"""
chord = 
{
    "chords":[
        {"beat": 0, "tag":"C"},
        {"beat": 2, "tag":"Em"},
        {"beat": 4, "tag":"Am"},
        {"beat": 6, "tag":"C7"}
}
"""

last_column_index = -1
column_index = -1
s = -1
last_beat = -1
beat = -1

key_72edo = {}

def getKey(column):
    tonic = tonic_calculate(chords["chords"][column]["beat"])
    return list(map(lambda x:x+tonic, chord_map[chords["chords"][column]["tag"]]))

def stopKey(keys):
    key_72edo[keys[0]-72].stop()
    for key in keys:
        key_72edo[key].stop()

def playKey(keys):
    key_72edo[keys[0]-72].play()
    for key in keys:
        key_72edo[key].play()

def loadKey(keys):
    key_72edo[keys[0]-72] = pygame.mixer.Sound(f"H:\\下载\\Jenny Editor\\Assets\\Audios\\{500+(keys[0]%72)-72}.wav")
    for key in keys:
        if not(key in key_72edo):
            key_72edo[key] = pygame.mixer.Sound(f"H:\\下载\\Jenny Editor\\Assets\\Audios\\{500+key}.wav")

def onChangeColumn(column):
    if column == 0:
        loadKey(getKey(column))
    if column > 0 and column < len(chords["chords"])+1:
        stopKey(getKey(column-1))
    if column < len(chords["chords"]):
        playKey(getKey(column))
    if column < len(chords["chords"])-1:
        loadKey(getKey(column+1))


def onChangeBeat(beat):
    # print(f"beat:{beat}")
    pass

def audio():
    global s, beat, last_column_index, last_beat
    if apps.record.frame > 0:
        s = apps.record.frame / FPS
    else:
        s = song.s
    beat = (s - chords["offset"]) / 60 * chords["bpm"]
    
    beat_array = [c["beat"] for c in chords["chords"]]
    column_index = lerp(beat_array, beat)
    cam.x = column_index * 80

    if column_index >= last_column_index + 1:
        last_column_index += 1
        onChangeColumn(last_column_index)

    if beat >= last_beat + 1:
        last_beat += 1
        onChangeBeat(last_beat)


# endregion

# region 文件



chord_map = core.file.open_json(".\\chord_map.json")

if len(sys.argv) > 1:
    project = core.file.Project(sys.argv[1])
index, song_path, chords = core.file.read()
song = Song(song_path)

# endregion

# region 显示

COLORS = {
    "bg":(81, 78, 97)
}

ORIGINAL_SPRITES = {
    0:pygame.image.load("./assets/sprites/0.png"),
    1:pygame.image.load("./assets/sprites/1.png"),
    2:pygame.image.load("./assets/sprites/2.png"),
    3:pygame.image.load("./assets/sprites/3.png"),
    4:pygame.image.load("./assets/sprites/4.png"),
    5:pygame.image.load("./assets/sprites/5.png"),
    "g1":pygame.image.load("./assets/sprites/g1.png"),
    "g2":pygame.image.load("./assets/sprites/g2.png"),
    "g3":pygame.image.load("./assets/sprites/g3.png"),
    "g4":pygame.image.load("./assets/sprites/g4.png"),
    "g5":pygame.image.load("./assets/sprites/g5.png"),
}

SPRITES = ORIGINAL_SPRITES.copy()

cam = Vec2(0.0, 0.0)

DEFAULT_SCALE = 20.0
scale = Scaler(SCALE, SCALE)

columns = []

def sprite_update():
    global columns
    columns = []

    for column_index, _chord in enumerate(chords["chords"]):
        columns.append(Column(screen, column_index, _chord))

sprite_update()

playhead = PlayHead(screen)

font = pygame.font.Font("./assets/fonts/xwxxh.ttf", 20)
debug = Text(screen, font)

def draw():
    screen.fill(COLORS["bg"])
    if 0 <= last_column_index < len(columns):
        columns[int(last_column_index)].draw_mask()
    for column in columns:
        column.draw()

    playhead.draw()

    # UI 绘制
    # debug.render(f"""当前音乐播放秒数：{song.s:.02f}
    #     当前音乐播放拍数：{beat:.02f}
    #     当前音乐播放列数：{column_index:.02f}""")
    
    pygame.display.flip()

def record():
    apps.record.update()

# endregion


if __name__ == "__main__":
    while state != States.QUIT:
        update()
        audio()
        draw()
        record()