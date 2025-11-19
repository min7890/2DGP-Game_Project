from pico2d import *
from tile import Tile_01, Tile_02

class Map_01:
    def __init__(self):
        self.image = load_image('background_01.png')
        self.ground_tiles = [Tile_01(60+i, 30) for i in range(0, 1280, 120)]
        self.tiles = [Tile_02(x,y) for x, y in [(400, 250), (400 + 128, 250), (300, 150), (900, 150), (1028, 150), (1156, 150), (690, 350), (690+128, 350)]]

    def update(self):
        pass

    def draw(self):
        self.image.draw(1280 // 2, 720// 2, 1280, 720)
        for tile in self.ground_tiles:
            tile.draw()

        for tile in self.tiles:
            tile.draw()

    def handle_collision(self, group, other):
        pass

class Map_Start:
    def __init__(self):
        self.image = load_image('background_00.png')
        self.ground_tiles = [Tile_01(60 + i, 30) for i in range(0, 1280, 120)]
        self.tiles = [Tile_02(x, y) for x, y in
                      [(400, 250), (400 + 128, 250), (300, 150)]]
    def update(self):
        pass
    def draw(self):
        self.image.draw(1280 // 2, 720 // 2, 1280, 720)
        for tile in self.ground_tiles:
            tile.draw()
        for tile in self.tiles:
            tile.draw()
    def handle_collision(self, group, other):
        pass