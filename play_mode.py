from pico2d import *

import game_world

import game_framework
from player import Player
from monster_01 import Monster_1
import pinput

player = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            pinput.update_key_state(event)  # 키 상태 업데이트
            player.handle_event(event)

def init():
    global player

    player = Player()
    game_world.add_object(player, 1)

    monster_1 = Monster_1()
    game_world.add_object(monster_1, 1)






def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass
