from pico2d import *
import random
import game_framework
import game_world
# from player import Player
from state_machine import StateMachine

from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import common
from item import Item

PIXEL_PER_METER = (10.0 / 0.3)
WALK_SPEED_KMPH = 5.0 # 5km/h
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_SECOND = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_SECOND
FRAMES_PER_ACTION = 5
FRAME_PER_SECOND = FRAMES_PER_ACTION * ACTION_PER_TIME

FRAMES_PER_ACTION_atk = 3
FRAME_PER_SECOND_atk = FRAMES_PER_ACTION_atk * ACTION_PER_TIME


class Monster_2:
    def __init__(self, x = 400, y =300):
        self.image = load_image('monster.png')
        self.hp_image = load_image('monster_hp.png')
        self.x, self.y = x, y
        self.frame = 0
        self.atk_frame = 0
        self.dir = self.face_dir = 1
        # self.isdetection = False
        # self.player = player
        self.is_atk = False
        self.det = False

        self.life = 5

        self.tx, self.ty = 400, 300
        self.state = 'Idle'
        self.ground = self.y

        game_world.add_collision_pair('tile:item', None, None)
        game_world.add_collision_pair('item:player', None, None)


        self.build_behavior_tree()

    def update(self):
        if self.is_atk:
            self.atk_frame = (self.atk_frame + FRAME_PER_SECOND_atk * game_framework.frame_time) % 3
            self.is_atk = False
        else:
            self.frame = (self.frame + FRAME_PER_SECOND * game_framework.frame_time) % 5

        self.det = False
        # print(self.player.x, self.x)
        # if self.isdetection and self.player is not None:
        #     if self.x < self.player.x:
        #         self dir = self.face_dir = 1
        #         if abs(self.player.x - self.x) > 10:
        #             self.x += self.dir * WALK_SPEED_PPS * game_framework.frame_time
        #     elif self.x > self.player.x:
        #         self.dir = self.face_dir = -1
        #         if abs(self.player.x - self.x) > 10:
        #             self.x += self.dir * WALK_SPEED_PPS * game_framework.frame_time
        #     self.isdetection = False

        if hasattr(self, 'candidate_grounds') and self.candidate_grounds:
            self.ground = max(self.candidate_grounds)
            self.candidate_grounds = []
        else:
            self.ground = 90

        if self.y > self.ground:
            self.velocity_y = -800 * game_framework.frame_time
            self.y += self.velocity_y
            if self.y < self.ground:
                self.y = self.ground
        else:
            self.y = self.ground

        self.bt.run()
        pass
    def draw(self):
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.hp_image.clip_draw(0, 31 * (5 - self.life), 190, 31, sx_, sy_ + 60, 200 / 4, 40 / 4)
        if self.is_atk:
            if self.dir == 1:
                # self.image.clip_draw(130, 220, 130, 100, 300, 400)
                self.image.clip_composite_draw(int(self.atk_frame) * 130, 320, 130, 100, 3.141592, 'v', sx_, sy_, 130 / 2, 100 / 2)
            else:
                self.image.clip_draw(int(self.atk_frame) * 130, 320, 130, 100, sx_, sy_, 130 / 2, 100 / 2)
            pass
        else:
            if self.dir == 1:
                # self.image.clip_draw(130, 220, 130, 100, 300, 400)
                self.image.clip_composite_draw(int(self.frame) * 130, 220, 130, 100, 3.141592, 'v', sx_, sy_, 130 / 2, 100 / 2)
            else:
                self.image.clip_draw(int(self.frame) * 130, 220, 130, 100, sx_, sy_, 130 / 2, 100 / 2)
        draw_rectangle(sx_ - 35, sy_ - 25, sx_ + 30, sy_ + 25)

        draw_circle(sx_, sy_, int(7 * PIXEL_PER_METER), 255, 255, 0)

    def get_bb(self):
        if self.dir == 1:
            return self.x - 35, self.y - 25, self.x + 30, self.y + 25
        elif self.dir == -1:
            return self.x - 30, self.y - 25, self.x + 35, self.y + 25


    def handle_collision(self, group, other):
        if group == 'tile:monster_2':
            left, bottom, right, top = other.get_bb()
            print(f'몬스터2가 타일과 충돌함 {self.y=} {top=}')
            if self.y > top and left <= self.x <= right:
                if not hasattr(self, 'candidate_grounds'):
                    self.candidate_grounds = []
                self.candidate_grounds.append(top + 18)


        if group == 'map_00_monster_2:player':
            self.is_atk = True

        if group == 'monster_2:fire':
            distance = WALK_SPEED_PPS * game_framework.frame_time
            if other.xv < 0:
                self.x -= distance * 30
            else:
                self.x += distance * 30
            self.life -= 1
            if self.life <= 0:
                if random.randint(1, 100) <= 100:
                    drop_x, drop_y = self.x, self.y
                    item = Item(drop_x, drop_y + 30)
                    game_world.add_object(item, 1)
                    game_world.add_collision_pair('item:player', item, None)
                    game_world.add_collision_pair('tile:item', None, item)

                game_world.remove_object(self)
                common.map.monster_num -= 1

        if group == 'monster:sword':
            distance = WALK_SPEED_PPS * game_framework.frame_time
            if other.face_dir < 0:
                self.x -= distance * 30
            else:
                self.x += distance * 30
            self.life -= 1
            if self.life <= 0:
                # 아이템 드롭
                if random.randint(1, 100) <= 100: # 10% 확률로 아이템 드롭
                    drop_x, drop_y = self.x, self.y
                    item = Item(drop_x, drop_y + 30)
                    game_world.add_object(item, 1)
                    game_world.add_collision_pair('item:player', item, None)
                    game_world.add_collision_pair('tile:item', None, item)

                game_world.remove_object(self)
                common.map.monster_num -= 1

    # def handle_detection_collision(self, group, other):
    #     if group == 'detection_monster_1:player':
    #         self.isdetection = True
    #         print('몬스터 감지 범위와 충돌함')
    #     pass

    def set_target_location(self, x=None, y=None):
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x2 - x1) ** 2 + (y2 - y1) ** 2
        return distance2 < (r * PIXEL_PER_METER) ** 2

    def move_little_to(self, tx, ty):
        if tx - self.x < 10:
            self.dir = -1
        else:
            self.dir = 1
        distance = WALK_SPEED_PPS * game_framework.frame_time
        if self.det:
            if abs(tx - self.x) > 20:
                self.x += distance * self.dir
        else:
            self.x += distance * self.dir

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_little_to(self.tx, self.ty)

        if self.distance_less_than(self.x, self.y, self.tx, self.ty, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):

        self.tx = random.randint(100, 1180)
        self.ty = random.randint(100, 924)
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

    def get_patrol_location(self):
        pass

    def build_behavior_tree(self):
        a1 = Action('목표 지점 설정', self.set_target_location, 1000, 800)
        a2 = Action('목표 지점으로 이동', self.move_to)
        move_to_target_location = Sequence('지정된 목표 지점으로 이동', a1, a2)

        a3 = Action('랜덤 위치 설정', self.set_random_location)
        wandoer = Sequence('배회', a3, a2)

        c1 = Condition('플레이어가 근처에 있는가?', self.if_player_nearby, 7)
        a4 = Action('플레이어 추적', self.move_to_player)
        root = chase_if_player_nearby = Sequence('플레이어가 근처에 있으면 추적', c1, a4)

        self.bt = BehaviorTree(root)
