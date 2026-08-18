import pygame, subprocess, sys
from core.events import event_bus

class Recorder:
    def __init__(self):

        self.frame = 0
        self.is_recording = False
        self.surface = pygame.Surface((1920, 1080))

        event_bus.subscribe("record_start", self.start)
        event_bus.subscribe("record_update", self.update)
        event_bus.subscribe("record_stop", self.stop)

    def start(self, surface:pygame.Surface):
        self.surface = surface
        self.is_recording = True
        self.frame = 0

    def update(self, _):
        if self.is_recording:
            pygame.image.save(self.surface, f"cache/frame_{self.frame:06d}.png")
            self.frame += 1

    def stop(self, music):
        self.is_recording = False
        self.frame = 0
        proc = subprocess.Popen(
            [sys.executable, 'core/merge.py', f'project/{music}']
        )

recorder = Recorder()