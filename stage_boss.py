from pico2d import *

import game_world

import game_framework
from player import Player
from monster_01 import Monster_1
from monster_02 import Monster_2
from monster_03 import Monster_3
from monster_boss import Monster_boss, Monster_boss_left_hand, Monster_boss_right_hand

from life import Life

from map import Map_boss
import pinput
import stage_00
import stage_01

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
            game_framework.change_mode(stage_00)
        else:
            pinput.update_key_state(event)  # 키 상태 업데이트
            common.player.handle_event(event)

def init():
    global player
    global map
    common.map = Map_boss()
    game_world.add_object(common.map, 0)

    # 플레이어를 먼저 생성
    common.player = Player()
    if common.player is not None:
        common.player.life = stage_01.prev_stage_life()
    game_world.add_object(common.player, 1)

    # 플레이어-타일 충돌 페어 등록 (플레이어 생성 후)
    game_world.add_collision_pair('tile:player', None, common.player)

    for tile in common.map.tiles:
        game_world.add_collision_pair('tile:player', tile, None)
        game_world.add_collision_pair('tile:monster_2', tile, None)
        game_world.add_collision_pair('tile:item', tile, None)

    game_world.add_collision_pair('portal:player', None, common.player)

    game_world.add_collision_pair('monster_boss:player', None, common.player)

    game_world.add_collision_pair('monster_3:player', None, common.player)

    game_world.add_collision_pair('item:player', None, common.player)

    game_world.add_collision_pair('boss_fire:player', None, common.player)

    common.monster_boss = Monster_boss(650, 400)
    game_world.add_object(common.monster_boss, 1)
    game_world.add_collision_pair('monster:sword', common.monster_boss, None)

    monster_boss_left_hand = Monster_boss_left_hand()
    game_world.add_object(monster_boss_left_hand, 2)

    monster_boss_left_hand = Monster_boss_right_hand()
    game_world.add_object(monster_boss_left_hand, 2)

    # monster_1 = [Monster_1(x, 120) for x in (400, 1050)]
    #
    # for monster in monster_1:
    #     game_world.add_object(monster, 1)
    # game_world.add_collision_pair('monster_1:player', None, common.player)
    # for monster in monster_1:
    #     # 플레이어 충돌
    #     game_world.add_collision_pair('monster_1:player', monster, None)
    #     # 몬스터1, 원거리공격 충돌
    #     game_world.add_collision_pair('monster_1:fire', monster, None)
    #     # 몬스터1, 타일 충돌
    #     game_world.add_collision_pair('tile:monster_1', None, monster)
    #     # 몬스터, 검 충돌
    #     game_world.add_collision_pair('monster:sword', monster, None)


    # # monster_1 = [Monster_2(x, y) for x, y in [(400, 285), (600, 88), (900, 185)]]
    # monster_2 = [Monster_2(x, y) for x, y in [(230, 430), (550, 330), (1000, 430), (818, 380)]]
    # for monster in monster_2:
    #     game_world.add_object(monster, 1)
    #
    #     game_world.add_collision_pair('monster_2:player', monster, None)
    #     game_world.add_collision_pair('monster_2:fire', monster, None)
    #     game_world.add_collision_pair('tile:monster_2', None, monster)
    #     game_world.add_collision_pair('monster:sword', monster, None)
    #
    # game_world.add_collision_pair('monster_2:player', None, common.player)
    # game_world.add_collision_pair('monster_3:player', None, common.player)
    #
    # monster_3 = [Monster_3(200, 400), Monster_3(800, 150)]
    # for monster in monster_3:
    #     game_world.add_object(monster, 1)
    #     # 플레이어 충돌
    #     game_world.add_collision_pair('monster_3:player', monster, None)
    #     # 몬스터3, 원거리공격 충돌
    #     game_world.add_collision_pair('monster_3:fire', monster, None)
    #     game_world.add_collision_pair('monster:sword', monster, None)
    # game_world.add_collision_pair('monster_3:player', None, common.player)












def update():
    game_world.update()
    game_world.handle_collisions()
    # game_world.handle_detection_collisions()

    current_life_objects = [obj for obj in game_world.world[2] if isinstance(obj, Life)]
    if len(current_life_objects) != common.player.life:
        # 기존 Life 객체 모두 제거
        for obj in current_life_objects:
            game_world.remove_object(obj)
        # 새 Life 객체 생성
        lives = [Life(35 + x * 60, 690) for x in range(common.player.life)]
        for life in lives:
            game_world.add_object(life, 2)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    game_world.clear()

def pause(): pass
def resume(): pass

def get_map():
    return map
