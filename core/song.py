# song.py
import time
import pygame
import json
from core.shasav import Monzo, Harmononym, Val, Tuning

pygame.mixer.pre_init(frequency=48000, size=-16, channels=2, buffer=2048)
pygame.mixer.init()

class Song:
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.name = data["name"]
        self.music = data["music"]
        self.bpm = data["bpm"]
        self.offset = data.get("offset", 0.0)
        self.tonic = data.get("tonic", 0)
        self.val = Val(int(data["tuning"]))
        self.tuning = Tuning(int(data["tuning"]))

        self.chords = data["chords"]      # [{start(beat), shasav}]
        self.subtitles = data.get("subtitles", [])  # [{start(beat), text}]
        self.sprites = data.get("sprites", [])  # [{start(beat), text}]
        
        self.playing = False
        self.paused = False

        self._start = 0.0
        self._elapsed = 0.0  # 已播放秒数（不含 offset）

        self.load(f"project/{self.music}")

    # ---------- 控制 ----------
    def load(self, path):
        pygame.mixer.music.load(path)

    def play(self):
        pygame.mixer.music.play()
        self._start = time.perf_counter()
        self.playing = True
        self.paused = False

    def pause(self):
        if not self.playing or self.paused:
            return
        self._elapsed += time.perf_counter() - self._start
        pygame.mixer.music.pause()
        self.paused = True

    def resume(self):
        if not self.paused:
            return
        self._start = time.perf_counter()
        pygame.mixer.music.unpause()
        self.paused = False

    def stop(self):
        pygame.mixer.music.stop()
        self.playing = self.paused = False
        self._elapsed = 0.0

    # ---------- 时间 ----------
    def get_play_time(self) -> float:
        """音频已播放秒数（不含 offset）"""
        if not self.playing:
            return 0.0
        return pygame.mixer.music.get_pos() / 1000

    def get_beat(self):
        """当前拍（从 0 起算）"""
        # seconds = max(self.get_play_time() - self.offset, 0.0)
        seconds = self.get_play_time() - self.offset
        return seconds / (60.0 / self.bpm)


song = Song("project/index.json")