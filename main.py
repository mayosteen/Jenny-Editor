# main.py
# coding:utf-8


# region 初始化
from core.init import *
from apps.explorer import Desktop
from apps.explorer import Taskbar
from apps.explorer import Explorer
from apps.blackboard import Blackboard


def main():

    desktop = Desktop()
    taskbar = Taskbar([
        Blackboard(0, 0, WIDTH, HEIGHT),
        ], 40)
    syswindows = [desktop,taskbar]
    windows = taskbar.tasks
    active_window = windows[-1]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit()
            
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if taskbar.collide(mouse_pos):
                    taskbar.mousedown(mouse_pos)
                
                for window in reversed(windows):
                    if window.collide(mouse_pos):
                        active_window = window
                        active_window.mousedown(mouse_pos)
                        windows.remove(active_window)
                        windows.append(active_window)
                        break
            
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
                del taskbar.tasks[i]

        pygame.display.flip()


if __name__ == "__main__":
    main()
