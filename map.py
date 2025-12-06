from pico2d import *
from tile import Tile_01, Tile_02
from portal import Portal
import game_world
import common

class Map_Start:
    def __init__(self):
        self.image = load_image('background_00.png')
        self.ground_tiles = [Tile_01(60 + i, 30) for i in range(0, 1280, 120)]
        self.tiles = [
            Tile_02(400, 250, patrol_route=[(350, 300), (580, 300)]),
            Tile_02(400 + 128, 250, patrol_route=[(350, 300), (580, 300)]),

            Tile_02(300, 150, patrol_route=[(250, 200), (350, 200)]),

            Tile_02(500, 160, patrol_route=[(450, 210), (680, 210)]),
            Tile_02(500 + 128, 160, patrol_route=[(450, 210), (680, 210)])
        ]
        #스테이지 00은 처음 튜토리얼 스테이지로서 monster_num이 필요없지만 다른 맵과의 통일성을 위해 0 이라는 값을 넣어놓음.
        self.monster_num = 0

        self.portal = Portal(1100, 120)

        self.w = self.image.w
        self.h = self.image.h
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

    def update(self):
        self.window_left = clamp(0, int(common.player.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(common.player.y) - self.ch // 2, self.h - self.ch - 1)
        self.portal.update()

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left,
            self.window_bottom,
            self.cw,
            self.ch,
            0,
            0
        )
        for tile in self.ground_tiles:
            tile.draw()
        for tile in self.tiles:
            tile.draw()

        self.portal.draw()

    def handle_collision(self, group, other):
        pass

class Map_01:
    def __init__(self):
        self.image = load_image('background_01.png')
        self.ground_tiles = [Tile_01(60+i, 30) for i in range(0, 1280, 120)]

        # 순찰 경로를 지정한 타일들
        # patrol_route가 None이면 순찰 경로 변경 안함, 값이 있으면 해당 경로로 변경
        self.tiles = [
            # 연속된 타일은 하나에만 patrol_route 지정 (왼쪽~오른쪽 범위)
            Tile_02(400, 250, patrol_route=[(350, 300), (580, 300)]),
            Tile_02(400 + 128, 250, patrol_route=[(350, 300), (580, 300)]),

            Tile_02(300, 150, patrol_route=[(250, 200), (350, 200)]),

            Tile_02(900, 150, patrol_route=[(850, 200), (1200, 200)]),
            Tile_02(1028, 150, patrol_route=[(850, 200), (1200, 200)]),
            Tile_02(1156, 150, patrol_route=[(850, 200), (1200, 200)]),

            Tile_02(690, 350, patrol_route=[(640, 400), (870, 400)]),
            Tile_02(690+128, 350, patrol_route=[(640, 400), (870, 400)]),
        ]
        self.monster_num = 6
        self.portal = None

        self.w = self.image.w
        self.h = self.image.h
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

    def update(self):
        self.window_left = clamp(0, int(common.player.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(common.player.y) - self.ch // 2, self.h - self.ch - 1)

        if self.monster_num == 0 and self.portal is None:
            self.portal = Portal(1100, 220)
        if self.portal:
            self.portal.update()

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left,
            self.window_bottom,
            self.cw,
            self.ch,
            0,
            0
        )
        for tile in self.ground_tiles:
            tile.draw()

        for tile in self.tiles:
            tile.draw()

        if self.portal is not None:
            self.portal.draw()
            game_world.add_collision_pair('portal:player', self.portal, None)

    def handle_collision(self, group, other):
        pass


class Map_02:
    def __init__(self):
        self.image = load_image('background_02.png')
        self.ground_tiles = [Tile_01(60 + i, 30) for i in range(0, 1280, 120)]
        self.tiles = [Tile_02(x, y) for x, y in
                      [(150, 150), (278, 150), (370, 240), (870, 240), (550, 300), (678, 300), (950, 150), (1078, 150),
                       (200, 400), (328, 400), (900, 400), (1028, 400)]]
        self.monster_num = 8
        self.portal = None

        self.w = self.image.w
        self.h = self.image.h
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

    def update(self):
        self.window_left = clamp(0, int(common.player.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(common.player.y) - self.ch // 2, self.h - self.ch - 1)

        if self.monster_num == 0 and self.portal is None:
            self.portal = Portal(1100, 220)
        if self.portal:
            self.portal.update()

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left,
            self.window_bottom,
            self.cw,
            self.ch,
            0,
            0
        )
        for tile in self.ground_tiles:
            tile.draw()
        for tile in self.tiles:
            tile.draw()
        if self.portal is not None:
            self.portal.draw()
            game_world.add_collision_pair('portal:player', self.portal, None)

    def handle_collision(self, group, other):
        pass


class Map_boss:
    def __init__(self):
        self.image = load_image('background_boss.png')
        self.ground_tiles = [Tile_01(60 + i, 30) for i in range(0, 1280, 120)]
        self.tiles = [Tile_02(x, y) for x, y in
                      [(576, 450), (704, 450),
                       (350, 350), (478, 350),
                       (802, 350), (930, 350),
                       (200, 250), (328, 250),
                       (952, 250), (1080, 250),
                       (350, 150), (930, 150)]]
        self.monster_num = 0
        self.portal = None

        self.w = self.image.w
        self.h = self.image.h
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()


    def update(self):
        self.window_left = clamp(0, int(common.player.x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(common.player.y) - self.ch // 2, self.h - self.ch - 1)

    def draw(self):
        self.image.clip_draw_to_origin(
            self.window_left,
            self.window_bottom,
            self.cw,
            self.ch,
            0,
            0
        )

        for tile in self.ground_tiles:
            tile.draw()
        for tile in self.tiles:
            tile.draw()

    def handle_collision(self, group, other):
        pass
