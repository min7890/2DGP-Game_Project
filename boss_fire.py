from pico2d import *
import game_world
import game_framework
import math
import common

PIXEL_PER_METER = (1.0 / 0.02)

class Fire:
    image = None

    def __init__(self, x, y, angle, speed=10):
        if Fire.image == None:
            Fire.image = load_image('BulletAtlas.png')
        self.x, self.y = x, y
        self.xv = speed * math.cos(math.radians(angle))
        self.yv = speed * math.sin(math.radians(angle))

    def draw(self):
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.image.clip_draw(210, 125, 125, 110, sx_, sy_, 50, 50)
        draw_rectangle(sx_ - 30, sy_ - 15, sx_ + 20, sy_ + 12)

    def update(self):
        self.x += self.xv * game_framework.frame_time * PIXEL_PER_METER
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

    def get_bb(self):
        return self.x - 30, self.y - 15, self.x + 20, self.y + 12

    def handle_collision(self, group, other):
        if group == 'boss_fire:player':
            if self in game_world.world[1]:
                game_world.remove_object(self)
