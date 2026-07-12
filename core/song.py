import pygame
from core.config import *

class Song:
    def __init__(self, file:str):
        self.load(file)
        self.last_pause = 0

    def load(self, file:str):
        pygame.mixer.music.load(file)
    
    def onEditing(self):
        pass

    def onPlaying(self):
        pass

    @property
    def ms(self):
        return self.last_pause + pygame.mixer.music.get_pos()

    @property
    def s(self):
        return self.ms / 1000

    def play(self):
        pygame.mixer.music.play(0)
        pygame.mixer.music.set_pos(self.last_pause / 1000)
        pygame.mixer.music.set_volume(0.1)

    def pause(self):
        pygame.mixer.music.pause()

    def stop(self):
        global state

        if state:
            self.last_pause = 0
            state = States.EDIT
            pygame.mixer.music.pause()


    def play_or_pause(self):
        global state

        if state == States.EDIT:
            self.play()
            state = States.PLAY

        elif state == States.PAUSE:
            self.last_pause = self.ms
            self.play()
            state = States.PLAY

        elif state == States.PLAY:
            self.pause()
            state = States.PAUSE