from pico2d import *
import math
import time
import game_framework
import game_world
from state_machine import StateMachine


class Monster_2:
    def __init__(self):
        self.image = load_image('monster.png')
        self.x, self.y = 400, 300
        self.frame = 0

    def update(self):
        pass
    def draw(self):
        pass

    def handle_collision(self, group, other):
        pass