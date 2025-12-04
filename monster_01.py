from pico2d import *
import math
import time
import game_framework
import game_world
from state_machine import StateMachine
import common

PIXEL_PER_METER = (10.0 / 0.2) # 10pixel = 10cm = 0.1m
WALK_SPEED_KMPH = 10.0 # 10km/h
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_SECOND = 0.7
ACTION_PER_TIME = 1.0 / TIME_PER_SECOND
FRAMES_PER_ACTION = 3
FRAME_PER_SECOND = FRAMES_PER_ACTION * ACTION_PER_TIME

TIME_PER_SECOND_atk = 1.0
ACTION_PER_TIME_atk = 1.0 / TIME_PER_SECOND_atk
FRAMES_PER_ACTION_atk = 6
FRAME_PER_SECOND_atk = FRAMES_PER_ACTION_atk * ACTION_PER_TIME_atk

class Monster_1:
    def __init__(self, x = 400, y =300):
        self.image = load_image('monster.png')
        self.atk_image = load_image('monster_01_atk.png')
        self.is_atk = False
        self.x, self.y = x, y
        self.frame = 0
        self.dir = self.face_dir = 1

    def update(self):
        if self.is_atk:
            self.frame = (self.frame + FRAME_PER_SECOND_atk * game_framework.frame_time) % 6
            if common.player.x <= self.x:
                self.dir = self.face_dir = -1
            else:
                self.dir = self.face_dir = 1
            self.is_atk = False
        else:
            self.frame = (self.frame + FRAME_PER_SECOND * game_framework.frame_time) % 3
            self.x += self.dir * WALK_SPEED_PPS * game_framework.frame_time
            if (self.x >= 570):
                self.dir = self.face_dir = -1
            elif (self.x <= 370):
                self.dir = self.face_dir = 1

        # print(self.is_atk)

        pass
    def draw(self):
        #atk
        if self.is_atk:
            print('atk')
            if self.face_dir == 1:
                # self.image.clip_draw(120, 420, 110, 190, 300, 400)
                self.atk_image.clip_composite_draw(int(self.frame) * 95, 0, 95, 190, 3.141592, 'v', 400, 300, 110 / 2, 190 / 2)
            else:
                self.atk_image.clip_draw(int(self.frame) * 95, 0, 95, 190, 400, 300, 110 / 2, 190 / 2)
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
        pass

    def get_bb(self):
        return self.x - 25, self.y - 40, self.x + 25, self.y + 45

    def handle_collision(self, group, other):
        if group == 'monster_1:fire':
            game_world.remove_object(self)
        elif group == 'monster_1:player':
            self.is_atk = True
            pass

    # def handle_detection_collision(self, group, other):
    #     pass


