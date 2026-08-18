import pygame, subprocess

frame = 0
screen = pygame.Surface((1920, 1080))

def start(canvas):
    global screen, frame
    screen = canvas
    frame = 1

def update():
    global frame
    if frame:
        pygame.image.save(screen, f"recordings/{frame:06d}.png")
        frame += 1

def stop():
    global frame
    frame = 0
    subprocess.Popen("python apps/merge.py")