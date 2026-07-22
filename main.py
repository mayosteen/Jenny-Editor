# main.py
# coding:utf-8


# region 初始化
from core.init import *
from apps.explorer import Desktop
from apps.explorer import Taskbar
from apps.explorer import Explorer
from apps.blackboard import Blackboard
# from apps.control import Control


def main():

    desktop = Desktop()
    taskbar = Taskbar([
        Blackboard(0, 0, WIDTH, HEIGHT),
    ], 40)
    windows = taskbar.tasks
    syswindows = [desktop,taskbar]
    active_window = windows[-1]
    touched = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
            
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                touched = False
                
                for window in reversed(windows):
                    if window.collide(mouse_pos):
                        active_window = window
                        active_window.mousedown(mouse_pos)
                        windows.remove(active_window)
                        windows.append(active_window)
                        touched = True
                        break
                if taskbar.collide(mouse_pos) and (not touched):
                    taskbar.mousedown(mouse_pos)
            
            elif event.type == MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                active_window.mousemotion(mouse_pos)
            
            elif event.type == MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                active_window.mouseup(mouse_pos)
        
        screen.fill((20, 20, 20))
        for window in syswindows:
            window._draw_content()
            screen.draw(window)
        for window in windows:
            window.update()
            window.get_surface(screen)
        for i, window in enumerate(windows):
            if not window.is_alive:
                print(window.title)
                del taskbar.tasks[i]

        pygame.display.flip()


if __name__ == "__main__":
    main()
