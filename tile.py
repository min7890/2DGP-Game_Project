from pico2d import *
import common

class Tile_01:
    def __init__(self, x = 400, y =300, patrol_route=None):
        self.tile_image_01 = load_image('tile_01.png')
        self.x, self.y = x, y
        # 순찰 경로: None이면 이 타일에서는 순찰 경로 변경 안함
        self.patrol_route = patrol_route

    def update(self):
        pass

    def draw(self):
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.tile_image_01.draw(sx_, sy_)
        draw_rectangle(sx_ - 65, sy_ - 40, sx_ + 65, sy_ + 40)

    def get_bb(self):
        return self.x - 65, self.y - 40, self.x + 65, self.y + 40

    def handle_collision(self, group, other):
        pass

class Tile_02:
    def __init__(self, x = 400, y =300, patrol_route=None):
        self.tile_image_02 = load_image('tile_02.png')
        self.x, self.y = x, y
        # 순찰 경로: None이면 이 타일에서는 순찰 경로 변경 안함
        self.patrol_route = patrol_route

    def update(self):
        pass

    def draw(self):
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.tile_image_02.draw(sx_, sy_)
        draw_rectangle(sx_ - 64, sy_ - 16, sx_ + 64, sy_ + 16)

    def get_bb(self):
        return self.x - 64, self.y - 16, self.x + 64, self.y + 16


    def handle_collision(self, group, other):
        pass