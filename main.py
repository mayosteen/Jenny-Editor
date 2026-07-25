# main.py
# coding:utf-8


# region 初始化
from core.init import *
from core.tasks import TaskManager, Taskbar
from apps.explorer import Desktop
from apps.explorer import Explorer
from apps.control import Control


def main():
    global t
    t.new(Desktop())
    t.new(Explorer(0, 0, WIDTH//2, HEIGHT//2))
    t.new(Explorer(40, 40, WIDTH//2, HEIGHT//2))
    t.new(Explorer(80, 80, WIDTH//2, HEIGHT//2))

    taskbar = Taskbar(t, 40)
    active_window = t.ask[-1]
    touched = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                # quit
                if t.ask[-1].title == "Desktop":
                    pygame.quit()
                    sys.exit()
                else:
                    t.close(t.ask[-1])
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # quit
                    if t.ask[-1].title == "Desktop":
                        pygame.quit()
                        sys.exit()
                    else:
                        t.close(t.ask[-1])
            
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                touched = False
                
                for window in reversed(t.ask):
                    if window.collide(mouse_pos):
                        active_window = window
                        t.activate(active_window)
                        active_window.mousedown(mouse_pos)
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
        
        t.update()
        
        screen.fill((20, 20, 20))
        taskbar._draw_content()
        screen.draw(taskbar)
        for window in t.ask:
            window.update()
            screen.draw(window)

        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
