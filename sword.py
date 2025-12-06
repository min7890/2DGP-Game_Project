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
        draw_rectangle(*self.get_bb(), 0, 255, 0)
        pass

    def get_bb(self):
        if self.face_dir == 1:
            return self.x + 17, self.y - 22, self.x + 50, self.y + 25
        else:
            return self.x - 50, self.y - 22, self.x - 17, self.y + 25

    def handle_collision(self, group, other):
        pass