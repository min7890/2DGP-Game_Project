from pico2d import *
import math
import time
import game_framework
import game_world
from state_machine import StateMachine

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import common
import random
from item import Item
from boss_fire import Fire

from monster_03 import Monster_3


PIXEL_PER_METER = (10.0 / 0.2)
FLY_SPEED_KMPH = 5.0 # 5km/h
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_SECOND = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_SECOND
FRAMES_PER_ACTION = 5
FRAME_PER_SECOND = FRAMES_PER_ACTION * ACTION_PER_TIME

def get_random_spawn_position():
    PIXEL_PER_METER_player = (10.0 / 0.3)  # 10 pixel 30 cm
    while True:
        x = random.randint(100, 1180)
        y = random.randint(150, 620)

        if (x - common.player.x) ** 2 + (y - common.player.y) ** 2 >= (2 * PIXEL_PER_METER_player) ** 2:
            return x, y

def spawn_monster_03(num = 0):
    monster_3 = [Monster_3(*get_random_spawn_position()) for _ in range(num)]
    for monster in monster_3:
        game_world.add_object(monster, 1)

        #몬스터2, 원거리공격 충돌
        game_world.add_collision_pair('monster_3:fire', monster, None)
        # 플레이어 충돌
        game_world.add_collision_pair('monster_3:player', monster, None)
        game_world.add_collision_pair('monster:sword', monster, None)


class Monster_boss:
    def __init__(self, x = 400, y =300):
        self.image = load_image('boss.png')
        self.font = load_font('ENCR10B.TTF', 30)
        self.x, self.y = x, y
        self.frame = 0
        self.dir = 0.0
        self.face_dir = 1

        self.state = 'Idle'

        self.fly_y = 1
        self.tx, self.ty = 400, 300

        self.life = 20
        self.is_atk = False
        self.det = False

        self.is_spowned = False

        self.last_fire_time = get_time()


    def update(self):
        self.det = False
        self.is_atk = False

        self.y += self.fly_y * FLY_SPEED_PPS * game_framework.frame_time
        if self.y > 400:
            self.fly_y = -1
        elif self.y < 300:
            self.fly_y = 1


        #10초마다 fire발사
        if get_time() - self.last_fire_time > 10.0:
            if self.life <= 10:
             self.fire_360()
             if common.map.monster_num < 5:
                 spawn_monster_03(1)
                 common.map.monster_num += 1
            self.last_fire_time = get_time()



        #보스몬스터 hp 5이하일때 몬스터3 소환 5마리, 위치이동
        if self.life <= 5 and not self.is_spowned:
            self.is_spowned = True
            spawn_monster_03(5)
            common.map.monster_num += 5
            self.x = 1050




    def draw(self):
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.image.clip_draw(0, 0, 230, 380, sx_, sy_)

        draw_rectangle(sx_ - 110, sy_ - 200, sx_ + 120, sy_ + 180)
        draw_circle(sx_, sy_, int(9 * PIXEL_PER_METER), 255, 255, 0)
        self.font.draw(450, 570, f'x{self.life}', (0, 0, 255))

    def get_bb(self):
        return self.x - 110, self.y - 200, self.x + 120, self.y + 180

    def fire_360(self):
        # 20도 간격으로 360도 발사 (18발)
        for angle in range(0, 360, 20):
            fire = Fire(self.x, self.y, angle, speed=10)
            game_world.add_object(fire, 1)
            game_world.add_collision_pair('boss_fire:player', fire, None)

    def handle_collision(self, group, other):
        if group == 'monster:sword':
            self.life -= 1
            if self.life <= 0:
                game_world.remove_object(self)
                common.map.monster_num -= 1


class Monster_boss_left_hand:
    def __init__(self):
        self.image = load_image('boss.png')
        self.hp_image = load_image('monster_hp.png')
        self.x, self.y = common.monster_boss.x - 100, common.monster_boss.y - 30

        self.dir = 0.0
        self.tx, self.ty = 400, 300

        self.life = 4
        self.is_atk = False
        self.det = False

        self.recover_time = get_time()

    def update(self):
        self.y = common.monster_boss.y - 30
        self.x = common.monster_boss.x - 100
        self.det = False
        self.is_atk = False

        if common.monster_boss.life <= 0:
            game_world.remove_object(self)

        if get_time() - self.recover_time > 30.0:
            if self.life < 4:
                self.life += 1
            self.recover_time = get_time()


    def draw(self):
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.hp_image.clip_draw(190, 31 * (4 - self.life), 150, 31, sx_, sy_ + 60, 200 / 4, 40 / 4)
        self.image.clip_draw(260, 15, 75, 70, sx_, sy_)

        draw_rectangle(sx_ - 40, sy_ - 40, sx_ + 40, sy_ + 25)
        draw_circle(sx_, sy_, int(2 * PIXEL_PER_METER), 255, 255, 0)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 25

    def handle_collision(self, group, other):
        if group == 'monster:sword':
            if self.life > 0:
                self.life -= 1

class Monster_boss_right_hand:
    def __init__(self):
        self.image = load_image('boss.png')
        self.hp_image = load_image('monster_hp.png')
        self.x, self.y = common.monster_boss.x + 100, common.monster_boss.y - 30

        self.dir = 0.0
        self.tx, self.ty = 400, 300

        self.life = 4
        self.is_atk = False
        self.det = False

        self.recover_time = get_time()

        if get_time() - self.recover_time > 30.0:
            if self.life < 4:
                self.life += 1
            self.recover_time = get_time()

    def update(self):
        self.y = common.monster_boss.y - 30
        self.x = common.monster_boss.x + 100
        self.det = False
        self.is_atk = False

        if common.monster_boss.life <= 0:
            game_world.remove_object(self)

    def draw(self):
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.hp_image.clip_draw(190, 31 * (4 - self.life), 150, 31, sx_, sy_ + 60, 200 / 4, 40 / 4)
        self.image.clip_draw(340, 15, 75, 70, sx_, sy_)

        draw_rectangle(sx_ - 40, sy_ - 40, sx_ + 30, sy_ + 25)
        draw_circle(sx_, sy_, int(2 * PIXEL_PER_METER), 255, 255, 0)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 30, self.y + 25

    def handle_collision(self, group, other):
        if group == 'monster:sword':
            if self.life > 0:
                self.life -= 1