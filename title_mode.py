from pico2d import *
import game_framework
import stage_00

image = None
font = None

def init():
    global image, font
    image = load_image('title_image.png')
    font = load_font('ENCR10B.TTF', 30)

def finish():
    global image
    del image

def update():
    pass

def draw():
    clear_canvas()
    image.draw(300, 300, 600, 600)
    font.draw(100, 100, f'Press space to start', (255, 255, 0))
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(stage_00)
    pass

def pause():
    pass

def resume():
    pass