from pico2d import *
import game_framework
import random
import game_world
import common

class Sword_range:
    def __init__(self,x =400, y = 300, face_dir=1):
        self.x, self.y = x, y
        self.face_dir = face_dir
        pass

    def update(self):
        pass

    def draw(self):
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        # if self.face_dir == 1:
        #     draw_rectangle(sx_ - 17, sy_ - 22, sx_ + 50, sy_ + 25, 0, 255, 0)
        # else:
        #     draw_rectangle(sx_ - 50, sy_ - 22, sx_ + 17, sy_ + 25, 0, 255, 0)

    def get_bb(self):
        if self.face_dir == 1:
            return self.x - 17, self.y - 22, self.x + 50, self.y + 25
        else:
            return self.x - 50, self.y - 22, self.x + 17, self.y + 25

    def handle_collision(self, group, other):
        if group == 'monster:sword':
            game_world.remove_object(self)
            common.player.sword_range = None  # player에서 중복 삭제 방지
