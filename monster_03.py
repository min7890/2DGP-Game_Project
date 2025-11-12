from pico2d import *
import math
import time
import game_framework
import game_world
from state_machine import StateMachine

PIXEL_PER_METER = (10.0 / 0.2)
WALK_SPEED_KMPH = 15.0 # 15km/h
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

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

    def update(self):
        self.frame = (self.frame + FRAME_PER_SECOND * game_framework.frame_time) % 5
        self.x += self.dir * WALK_SPEED_PPS * game_framework.frame_time
        if (self.x >= 1230):
            self.dir = self.face_dir = -1
        elif (self.x <= 50):
            self.dir = self.face_dir = 1
        pass
    def draw(self):
        if self.face_dir == 1:
            # self.image.clip_draw(130, 120, 130, 100, 300, 400)
            self.image.clip_draw(int(self.frame) * 130, 120, 130, 100, self.x, self.y, 130 / 2, 100 / 2)

        else:
            self.image.clip_composite_draw(int(self.frame) * 130, 120, 130, 100, 3.141592, 'v', self.x, self.y, 130 / 2, 100 / 2)
        pass

    def handle_collision(self, group, other):
        pass