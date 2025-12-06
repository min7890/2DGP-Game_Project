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

def spawn_monster_03():
    monster_3 = [Monster_3(*get_random_spawn_position()) for _ in range(5)]
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
        self.x, self.y = x, y
        self.frame = 0
        self.dir = 0.0
        self.face_dir = 1

        self.fly_y = 1
        self.tx, self.ty = 400, 300

        self.life = 20
        self.is_atk = False
        self.det = False

        self.is_spowned = False

        self.last_fire_time = get_time()

        self.build_behavior_tree()

    def update(self):
        self.y += self.fly_y * FLY_SPEED_PPS * game_framework.frame_time
        if self.y > 400:
            self.fly_y = -1
        elif self.y < 300:
            self.fly_y = 1
        self.det = False
        self.is_atk = False


        #10초마다 fire발사
        if get_time() - self.last_fire_time > 10.0:
            if self.life <= 10:
             self.fire_360()
            self.last_fire_time = get_time()

        #보스몬스터 hp 5이하일때 몬스터3 소환 5마리
        if self.life <= 5 and not self.is_spowned:
            self.is_spowned = True
            spawn_monster_03()

        # self.bt.run()

    def draw(self):
        self.image.clip_draw(0, 0, 230, 380, self.x, self.y)

        draw_rectangle(*self.get_bb())
        draw_circle(self.x, self.y, int(2 * PIXEL_PER_METER), 255, 255, 0)

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



        pass


    def set_target_location(self, x=None, y=None):
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        return distance2 < (r * PIXEL_PER_METER) ** 2


    def move_little_to(self, tx, ty):
        #각도 구하기
        self.dir = math.atan2(ty - self.y, tx - self.x)

        if tx - self.x < 10:
            self.face_dir = -1
        else:
            self.face_dir = 1
        #거리 구하기
        distance = FLY_SPEED_PPS * game_framework.frame_time
        if self.det:
            if abs(tx - self.x) > 20:
                self.x += distance * math.cos(self.dir)
            self.y += distance * math.sin(self.dir)
        else:
            self.x += distance * math.cos(self.dir)
            self.y += distance * math.sin(self.dir)

    def move_to(self, r=0.5):
        self.state = 'Fly'
        self.move_little_to(self.tx, self.ty)
        # 목표 지점에 거의 도착했으면 성공 리턴
        if self.distance_less_than(self.x, self.y, self.tx, self.ty, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx = random.randint(100, 1180)
        self.ty = random.randint(100, 620)
        return BehaviorTree.SUCCESS

    def if_player_nearby(self, distance):
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, distance):
            self.det = True
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_player(self, r=0.5):
        self.state = 'Walk'
        self.move_little_to(common.player.x, common.player.y)
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):

        a1 = Action('목표 지점으로 이동', self.move_to)

        a2 = Action('랜덤 위치 설정', self.set_random_location)
        wander = Sequence('배회', a2, a1)

        c1 = Condition('플레이어가 근처에 있는가?', self.if_player_nearby, 2)
        a3 = Action('플레이어 추적', self.move_to_player)
        chase_if_player_nearby = Sequence('소년이 근처에 있으면 추적', c1, a3)

        root = chase_or_wander = Selector('소년이 가까이 있으면추적하고, 아니면 배회', chase_if_player_nearby, wander)

        self.bt = BehaviorTree(root)

class Monster_boss_left_hand:
    def __init__(self):
        self.image = load_image('boss.png')
        self.x, self.y = common.monster_boss.x - 100, common.monster_boss.y - 30

        self.dir = 0.0
        self.tx, self.ty = 400, 300

        self.life = 4
        self.is_atk = False
        self.det = False

    def update(self):
        self.y = common.monster_boss.y - 30
        self.det = False
        self.is_atk = False

    def draw(self):
        self.image.clip_draw(260, 15, 75, 70, self.x, self.y)

        draw_rectangle(*self.get_bb())
        draw_circle(self.x, self.y, int(2 * PIXEL_PER_METER), 255, 255, 0)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 40, self.y + 25

    def handle_collision(self, group, other):
        pass

class Monster_boss_right_hand:
    def __init__(self):
        self.image = load_image('boss.png')
        self.x, self.y = common.monster_boss.x + 100, common.monster_boss.y - 30

        self.dir = 0.0
        self.tx, self.ty = 400, 300

        self.life = 4
        self.is_atk = False
        self.det = False

    def update(self):
        self.y = common.monster_boss.y - 30
        self.det = False
        self.is_atk = False

    def draw(self):
        self.image.clip_draw(340, 15, 75, 70, self.x, self.y)

        draw_rectangle(*self.get_bb())
        draw_circle(self.x, self.y, int(2 * PIXEL_PER_METER), 255, 255, 0)

    def get_bb(self):
        return self.x - 40, self.y - 40, self.x + 30, self.y + 25

    def handle_collision(self, group, other):
        pass