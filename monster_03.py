from pico2d import *
import math
import time
import game_framework
import game_world
from state_machine import StateMachine

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import common
import random

PIXEL_PER_METER = (10.0 / 0.2)
FLY_SPEED_KMPH = 10.0 # 10km/h
FLY_SPEED_MPM = (FLY_SPEED_KMPH * 1000.0 / 60.0)
FLY_SPEED_MPS = (FLY_SPEED_MPM / 60.0)
FLY_SPEED_PPS = (FLY_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_SECOND = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_SECOND
FRAMES_PER_ACTION = 5
FRAME_PER_SECOND = FRAMES_PER_ACTION * ACTION_PER_TIME


class Monster_3:
    def __init__(self):
        self.image = load_image('monster.png')
        self.x, self.y = 400, 300
        self.frame = 0
        self.dir = self.face_dir = 1
        self.tx, self.ty = 400, 300

        self.life = 4
        self.is_atk = False

        self.build_behavior_tree()

    def update(self):
        self.frame = (self.frame + FRAME_PER_SECOND * game_framework.frame_time) % 5
        # self.x += self.dir * FLY_SPEED_PPS * game_framework.frame_time
        # if (self.x >= 1230):
        #     self.dir = self.face_dir = -1
        # elif (self.x <= 50):
        #     self.dir = self.face_dir = 1

        self.bt.run()

    def draw(self):
        if self.is_atk:
            if self.dir > 0:
                self.image.clip_draw(int(self.frame) * 130, 10, 130, 100, self.x, self.y, 130 / 2, 100 / 2)
            else:
                self.image.clip_composite_draw(int(self.frame) * 130, 10, 130, 100, 3.141592, 'v', self.x, self.y, 130 / 2, 100 / 2)
        else:
            if self.dir > 0:
                self.image.clip_draw(int(self.frame) * 130, 120, 130, 100, self.x, self.y, 130 / 2, 100 / 2)
            else:
                self.image.clip_composite_draw(int(self.frame) * 130, 120, 130, 100, 3.141592, 'v', self.x, self.y, 130 / 2, 100 / 2)

        draw_rectangle(*self.get_bb())
        draw_circle(self.x, self.y, int(2 * PIXEL_PER_METER), 255, 255, 0)

    def get_bb(self):
        return self.x - 20, self.y - 30, self.x + 20, self.y + 30

    def handle_collision(self, group, other):
        if group == 'monster_3:fire':
            self.life -= 1
            if self.life <= 0:
                game_world.remove_object(self)
                common.map.monster_num -= 1
        elif group == 'monster_3:player':
            self.is_atk = True

        if group == 'map_00_monster_3:player':
            self.is_atk = True
        pass
    # def handle_detection_collision(self, group, other):
    #     pass

    def set_target_location(self, x=None, y=None):
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        return distance2 < (r * PIXEL_PER_METER) ** 2


    def move_little_to(self, tx, ty):
        #각도 구하기
        self.dir = math.atan2(ty - self.y, tx - self.x)
        #거리 구하기
        distance = FLY_SPEED_PPS * game_framework.frame_time
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
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_player(self, r=0.5):
        self.state = 'Walk'
        self.move_little_to(common.player.x, common.player.y)
        #소년에 근접했으면 성공 리턴
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