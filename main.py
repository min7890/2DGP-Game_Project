from pico2d import *
import pinput

open_canvas(1280, 720)

def event_update():
    running = True
    event_list = get_events()
    pinput.process_input(event_list)
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    return running

def render():
    clear_canvas()

    # player = load_image('avatar_body0000.png')

    # player.clip_draw(0, 10, 10, 10, 390, 300.1875, 100, 100)  # 몸
    # player.clip_draw(0, 20, 16, 12, 400, 300.375, 100, 100)  # 머리
    # player.clip_draw(10, 10, 10, 10, 100, 100, 100, 100) #등
    # player.clip_draw(14, 0, 2, 2, 100, 100, 100, 100) #왼쪽 눈
    # player.clip_draw(16, 0, 2, 2, 100, 100, 100, 100) #오른쪽 눈
    # player.clip_draw(22, 14, 2, 4, 100, 100, 100, 100) #왼팔
    # player.clip_draw(26, 14, 2, 4, 100, 100, 100, 100) #오른팔
    # player.clip_draw(3, 0, 2, 4, 100, 100, 100, 100) #왼다리
    # player.clip_draw(9, 0, 2, 4, 100, 100, 100, 100) #오른다리

    player = load_image('avatar02.png')
    player.clip_draw(0, 0, 245, 472, 100, 100, 100, 100)

    update_canvas()

running = True

while event_update():
    render()






close_canvas()