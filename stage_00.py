from pico2d import *

import game_world

import game_framework
from player import Player
from monster_01 import Monster_1
from monster_02 import Monster_2
from monster_03 import Monster_3

from fire import Fire

from map import Map_Start
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


    # monster_2 = Monster_2()
    # game_world.add_object(monster_2, 1)
    game_world.add_collision_pair('monster_2:player', None, player)

    # monster_3 = Monster_3()
    # game_world.add_object(monster_3, 1)
    game_world.add_collision_pair('monster_3:player', None, player)



    map = Map_Start()
    game_world.add_object(map, 0)
    game_world.add_collision_pair('map_01_tile:player', None, player)
    for tile in map.tiles:
        game_world.add_collision_pair('map_01_tile:player', tile, None)

def spawn_monster():
    monster_1 = Monster_1(400, 300)
    game_world.add_object(monster_1, 1)
    game_world.add_collision_pair('monster_1:player', None, player)
    game_world.add_collision_pair('monster_1:player', monster_1, None)
    #몬스터1, 원거리공격 충돌
    game_world.add_collision_pair('monster_1:fire', monster_1, None)







def update():
    game_world.update()
    game_world.handle_collisions()

    monsters = [obj for obj in game_world.world[1] if isinstance(obj, Monster_1)]
    if not monsters:
        # 몬스터가 사라진 상태
        spawn_monster()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass
