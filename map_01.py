from pico2d import *
from tile import Tile_01, Tile_02

class Map_01:
    def __init__(self):
        self.image = load_image('background_01.png')
        self.tiles_01 = [Tile_01(60+i, 30) for i in range(0, 1280, 120)]
        self.tile_positions = [(400, 250), (400 + 128, 250), (300, 150)]

    def update(self):
        pass

    def draw(self):
        self.image.draw(1280 // 2, 720// 2, 1280, 720)
        for tile in self.tiles_01:
            tile.draw()

        tile_02 = [Tile_02(x, y) for x, y in self.tile_positions]
        for tile in tile_02:
            tile.draw()


    def handle_collision(self, group, other):
        pass