from pico2d import *

class Tile_01:
    def __init__(self, x = 400, y =300, patrol_route=None):
        self.tile_image_01 = load_image('tile_01.png')
        self.x, self.y = x, y
        # 순찰 경로: None이면 이 타일에서는 순찰 경로 변경 안함
        self.patrol_route = patrol_route

    def update(self):
        pass

    def draw(self):
        self.tile_image_01.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

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
        self.tile_image_02.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 64, self.y - 16, self.x + 64, self.y + 16


    def handle_collision(self, group, other):
        pass