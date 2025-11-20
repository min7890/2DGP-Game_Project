from pico2d import *
from tile import Tile_01, Tile_02
from portal import Portal
import game_world

class Map_01:
    def __init__(self):
        self.image = load_image('background_01.png')
        self.ground_tiles = [Tile_01(60+i, 30) for i in range(0, 1280, 120)]
        self.tiles = [Tile_02(x,y) for x, y in [(400, 250), (400 + 128, 250), (300, 150), (900, 150), (1028, 150), (1156, 150), (690, 350), (690+128, 350)]]
        self.monster_num = 3
        self.portal = None

    def update(self):
        if self.monster_num == 0 and self.portal is None:
            self.portal = Portal(1100, 220)
        pass

    def draw(self):
        self.image.draw(1280 // 2, 720// 2, 1280, 720)
        for tile in self.ground_tiles:
            tile.draw()

        for tile in self.tiles:
            tile.draw()

        if self.portal is not None:
            self.portal.draw()
            game_world.add_collision_pair('portal:player', self.portal, None)

    def handle_collision(self, group, other):
        pass

class Map_Start:
    def __init__(self):
        self.image = load_image('background_00.png')
        self.ground_tiles = [Tile_01(60 + i, 30) for i in range(0, 1280, 120)]
        self.tiles = [Tile_02(x, y) for x, y in
                      [(400, 250), (400 + 128, 250), (300, 150)]]
        self.portal = Portal(1100, 120)
    def update(self):
        self.portal.update()
        pass
    def draw(self):
        self.image.draw(1280 // 2, 720 // 2, 1280, 720)
        for tile in self.ground_tiles:
            tile.draw()
        for tile in self.tiles:
            tile.draw()

        self.portal.draw()
    def handle_collision(self, group, other):
        pass

class Map_02:
    def __init__(self):
        self.image = load_image('background_02.png')
        self.ground_tiles = [Tile_01(60 + i, 30) for i in range(0, 1280, 120)]
        self.tiles = [Tile_02(x, y) for x, y in
                      [(400, 250), (400 + 128, 250), (300, 150), (900, 150), (1028, 150), (1156, 150), (690, 350),
                       (690 + 128, 350)]]
        self.monster_num = 3
        self.portal = None
    def update(self):
        if self.monster_num == 0 and self.portal is None:
            self.portal = Portal(1100, 220)
        pass
    def draw(self):
        self.image.draw(1280 // 2, 720 // 2, 1280, 720)
        for tile in self.ground_tiles:
            tile.draw()
        for tile in self.tiles:
            tile.draw()
        if self.portal is not None:
            self.portal.draw()
            game_world.add_collision_pair('portal:player', self.portal, None)
    def handle_collision(self, group, other):
        pass