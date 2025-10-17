from pico2d import *

open_canvas(1280, 720)

running = True

while running:
    clear_canvas()








    update_canvas()



    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

close_canvas()