from pico2d import *

import game_world

import game_framework
from player import Player
from monster_01 import Monster_1
from monster_02 import Monster_2
from monster_03 import Monster_3

from life import Life

from map import Map_01
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

    lives = [Life(35 + x * 60, 690) for x in range(5)]
    for life in lives:
        game_world.add_object(life, 2)

    player = Player()
    game_world.add_object(player, 1)

    monster_1 = [Monster_1(400 + x, 300) for x in range(0, 60, 20)]
    for monster in monster_1:
         game_world.add_object(monster, 1)
    game_world.add_collision_pair('monster_1:player', None, player)
    for monster in monster_1:
        game_world.add_collision_pair('monster_1:player', monster, None)

    #몬스터1, 원거리공격 충돌
    for monster in monster_1:
        game_world.add_collision_pair('monster_1:fire', monster, None)


    # monster_2 = Monster_2()
    # game_world.add_object(monster_2, 1)
    game_world.add_collision_pair('monster_2:player', None, player)

    # monster_3 = Monster_3()
    # game_world.add_object(monster_3, 1)
    game_world.add_collision_pair('monster_3:player', None, player)



    map_01 = Map_01()
    game_world.add_object(map_01, 0)
    game_world.add_collision_pair('map_01_tile:player', None, player)
    for tile in map_01.tiles:
        game_world.add_collision_pair('map_01_tile:player', tile, None)









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
