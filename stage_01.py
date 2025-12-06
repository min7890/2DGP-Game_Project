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
import stage_02
import stage_00

import common

def handle_events():
    event_list = get_events()
    for event in event_list:
        if common.player.life == 0:
            game_framework.change_mode(stage_00)

        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_f and common.player.isInPortal:
            game_framework.change_mode(stage_02)
        else:
            pinput.update_key_state(event)  # 키 상태 업데이트
            common.player.handle_event(event)

def init():
    global player

    common.player = Player()
    game_world.add_object(common.player, 1)

    game_world.add_collision_pair('item:player', None, common.player)

    # lives = [Life(35 + x * 60, 690) for x in range(player.life)]
    # for life in lives:
    #     game_world.add_object(life, 2)

    monster_1 = [Monster_1(400 + x, 300) for x in range(0, 60, 20)]
    monster_1 += [Monster_1(900 + x, 200) for x in (30, 300)]
    # monster_1 = [Monster_1(300, 200)]
    for monster in monster_1:
         game_world.add_object(monster, 1)
    game_world.add_collision_pair('monster_1:player', None, common.player)
    for monster in monster_1:
        #플레이어 충돌
        game_world.add_collision_pair('monster_1:player', monster, None)
        # 몬스터1, 원거리공격 충돌
        game_world.add_collision_pair('monster_1:fire', monster, None)
        # 몬스터1, 타일 충돌
        game_world.add_collision_pair('tile:monster_1', None, monster)
        # 몬스터, 검 충돌
        game_world.add_collision_pair('monster:sword', monster, None)


    # monster_2 = Monster_2()
    # game_world.add_object(monster_2, 1)
    game_world.add_collision_pair('monster_2:player', None, common.player)


    monster_3 = Monster_3()
    game_world.add_object(monster_3, 1)
    game_world.add_collision_pair('monster_3:player', None, common.player)
    # 플레이어 충돌
    game_world.add_collision_pair('monster_3:player', monster_3, None)
    # 몬스터3, 원거리공격 충돌
    game_world.add_collision_pair('monster_3:fire', monster_3, None)
    game_world.add_collision_pair('monster:sword', monster_3, None)


    global map
    common.map = Map_01()
    game_world.add_object(common.map, 0)
    game_world.add_collision_pair('tile:player', None, common.player)
    for tile in common.map.tiles:
        game_world.add_collision_pair('tile:player', tile, None)

        game_world.add_collision_pair('tile:item', tile, None)

    game_world.add_collision_pair('portal:player', None, common.player)

    for monster in monster_1:
        game_world.add_collision_pair('tile:monster_1', None, monster)
    for tile in common.map.tiles:
        game_world.add_collision_pair('tile:monster_1', tile, None)









def update():
    game_world.update()
    game_world.handle_collisions()

    current_life_objects = [obj for obj in game_world.world[2] if isinstance(obj, Life)]
    if len(current_life_objects) != common.player.life:
        # 기존 Life 객체 모두 제거
        for obj in current_life_objects:
            game_world.remove_object(obj)
        # 새 Life 객체 생성
        lives = [Life(35 + x * 60, 570) for x in range(common.player.life)]
        for life in lives:
            game_world.add_object(life, 2)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def prev_stage_life():
    if common.player is None:
        return 5
    else:
        return common.player.life

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

def get_map():
    return common.map
