from enum import Enum

WIDTH = 1920
HEIGHT = 1080

FPS = 60

SCALE = 2.0

RECENT_PROJECT_PATH = "Jenny-Editor"



INTERVALS = [ 0, 72, 42, 23, 58, 105, ]

class States(Enum):
    QUIT = "states.quit"
    PLAY = "states.play"
    PAUSE = "states.pause"
    EDIT = "states.edit"

state = States.EDIT

class EventTypes(Enum):
    TEMPO = 0
    TRANSPOSE = 1