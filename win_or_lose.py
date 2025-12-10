from pico2d import *
import game_framework
import title_mode
from pannel import Pannel
import game_world


def init():
    global pannel
    pannel = Pannel()
    game_world.add_object(pannel, 2)

def finish():
    global pannel
    game_world.remove_object(pannel)
    del pannel

def update():
    game_world.update() #아이템 모드에서는 플레이모드가 유지되어야 하므로
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.pop_mode()
            elif event.key == SDLK_SPACE:
                game_framework.pop_mode()
                game_framework.change_mode(title_mode)




    pass

def pause():
    pass

def resume():
    pass