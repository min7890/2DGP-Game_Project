from pico2d import *
import math
import time
import game_framework
import game_world
from state_machine import StateMachine
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import common
import random

PIXEL_PER_METER = (10.0 / 0.3) # 10pixel = 10cm = 0.1m
WALK_SPEED_KMPH = 10.0 # 10km/h
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_SECOND = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_SECOND
FRAMES_PER_ACTION = 3
FRAME_PER_SECOND = FRAMES_PER_ACTION * ACTION_PER_TIME

class Monster_1:
    def __init__(self, x = 400, y =300):
        self.image = load_image('monster.png')
        self.atk_image = load_image('monster_01_atk.png')
        self.is_atk = False
        self.x, self.y = x, y
        self.frame = 0
        self.dir = self.face_dir = 1

        self.det = False

        self.ground = self.y

        self.life = 3

        self.tx, self.ty = 400, 300
        self.state = 'Idle'

        self.build_behavior_tree()

        # 현재 밟고 있는 타일 추적 (순찰 경로 변경용)
        self.current_patrol_tile = None

        self.loc_no = 0
        self.patrol_locations = [(350, 300), (580, 300)]

    def update(self):
        if self.is_atk:
            self.frame = (self.frame + FRAME_PER_SECOND * game_framework.frame_time) % 6
            if common.player.x <= self.x:
                self.dir = self.face_dir = -1
            else:
                self.dir = self.face_dir = 1
            self.is_atk = False
            self.det = False
        else:
            self.frame = (self.frame + FRAME_PER_SECOND * game_framework.frame_time) % 3
            # if self.loc_no == 0:
            #     self.dir = self.face_dir = 1
            # else:
            #     self.dir = self.face_dir = -1

            # self.x += self.dir * WALK_SPEED_PPS * game_framework.frame_time
            # if (self.x >= 570):
            #     self.dir = self.face_dir = -1
            # elif (self.x <= 370):
            #     self.dir = self.face_dir = 1

        if hasattr(self, 'candidate_grounds') and self.candidate_grounds:
            self.ground = max(self.candidate_grounds)
            self.candidate_grounds = []
        else:
            self.ground = 90 + 20

        if self.y > self.ground:
            self.velocity_y = -800 * game_framework.frame_time
            self.y += self.velocity_y
            if self.y < self.ground:
                self.y = self.ground
        else:
            self.y = self.ground

        # print(self.is_atk)
        print(f'몬스터의 ground: {self.ground=}')

        if self.ground == 90 + 20:
            root = self.chase_or_wander
        else:
            root = self.chase_or_patrol

        self.bt = BehaviorTree(root)

        self.bt.run()

        pass
    def draw(self):
        #atk
        if self.is_atk:
            if self.face_dir == 1:
                # self.image.clip_draw(120, 420, 110, 190, 300, 400)
                self.atk_image.clip_composite_draw(int(self.frame) * 95, 0, 95, 190, 3.141592, 'v', self.x, self.y, 110 / 2, 190 / 2)
            else:
                self.atk_image.clip_draw(int(self.frame) * 95, 0, 95, 190, self.x, self.y, 110 / 2, 190 / 2)
            pass
        #walk
        else:
            print('walk')
            if self.face_dir == 1:
                # self.image.clip_draw(120, 420, 110, 190, 300, 400)
                self.image.clip_composite_draw(int(self.frame) * 120, 420, 110, 190, 3.141592, 'v', self.x, self.y, 110 / 2, 190 / 2)
            else:
                self.image.clip_draw(int(self.frame) * 120, 420, 110, 190, self.x, self.y, 110 / 2, 190 / 2)

        draw_rectangle(*self.get_bb())
        draw_circle(self.x, self.y, int(5 * PIXEL_PER_METER), 255, 255, 0)


    def get_bb(self):
        return self.x - 25, self.y - 40, self.x + 25, self.y + 45

    def handle_collision(self, group, other):
        if group == 'monster_1:fire':
            self.life -= 1
            if self.life <= 0:
                game_world.remove_object(self)
                common.map.monster_num -= 1

        elif group == 'monster_1:player':
            self.is_atk = True

        if group == 'map_00_monster_1:player':
            self.is_atk = True

        if group in ('map_01_tile:monster_1', 'map_00_tile:monster_1'):
            left, bottom, right, top = other.get_bb()
            print(f'몬스터_01가 타일과 충돌함 {self.patrol_locations=} {self.ground=}')
            print(f'{self.x=}, {self.y=}')
            if self.y > top and left <= self.x <= right:
                if not hasattr(self, 'candidate_grounds'):
                    self.candidate_grounds = []
                self.candidate_grounds.append(top + 38)

                # 타일에 순찰 경로가 정의되어 있고, 현재 타일과 다르면 순찰 경로 업데이트
                if hasattr(other, 'patrol_route') and other.patrol_route is not None:
                    if self.current_patrol_tile != other:
                        self.current_patrol_tile = other
                        self.patrol_locations = other.patrol_route
                        self.loc_no = 0


    # def handle_detection_collision(self, group, other):
    #     pass

    def set_target_location(self, x=None, y=None):
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        return distance2 < (r * PIXEL_PER_METER) ** 2

    def move_little_to(self, tx, ty):
        if tx - self.x < 10:
            self.dir = self.face_dir = -1
        else:
            self.dir = self.face_dir = 1
        distance = WALK_SPEED_PPS * game_framework.frame_time
        if self.det:
            if abs(tx - self.x) > 20:
                self.x += distance * self.dir
        else:
            self.x += distance * self.dir

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_little_to(self.tx, self.ty)

        # 순찰은 x좌표만 비교
        if abs(self.x - self.tx) < r * PIXEL_PER_METER:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx = random.randint(100, 1180)
        self.ty = 90 + 20
        return BehaviorTree.SUCCESS

    def if_player_nearby(self, distance):
        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, distance):
            self.det = True
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_player(self, r = 0.5):

        self.state = 'Walk'
        self.move_little_to(common.player.x, common.player.y)

        if self.distance_less_than(common.player.x, common.player.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def get_patrol_location(self):
        self.tx, self.ty = self.patrol_locations[self.loc_no]
        self.loc_no = (self.loc_no + 1) % len(self.patrol_locations)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        a1 = Action('목표 지점으로 이동', self.move_to)

        c1 = Condition('플레이어가 근처에 있는가?', self.if_player_nearby, 5)
        a2 = Action('플레이어 추적', self.move_to_player)
        chase_if_player_nearby = Sequence('플레이어가 근처에 있으면 추적', c1, a2)

        a3 = Action('다음 순찰 위치를 가져오기', self.get_patrol_location)
        patrol = Sequence('순찰', a3, a1)

        a4 = Action('랜덤 위치 설정', self.set_random_location)
        wander = Sequence('배회', a4, a1)

        chase_or_wander = Selector('플레이어가 가까이 있으면추적하고, 아니면 배회', chase_if_player_nearby, wander)
        chase_or_patrol = Selector('플레이어가 가까이 있으면 추적하고, 아니면 순찰', chase_if_player_nearby, patrol)

        self.chase_or_wander = chase_or_wander
        self.chase_or_patrol = chase_or_patrol

        if self.ground == 90 + 20:
            root = chase_or_wander
        else:
            root = chase_or_patrol


        self.bt = BehaviorTree(root)
