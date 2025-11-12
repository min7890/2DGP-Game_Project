from pico2d import *

class Map_01:
    def __init__(self):
        self.image = load_image('background_01.png')
        self.tile_image_01 = load_image('tile_01.png')
        self.tile_image_02 = load_image('tile_02.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1280 // 2, 720// 2, 1280, 720)
        for i in range(0, 1280, 120):
            self.tile_image_01.draw(60 + i, 30)

        self.tile_image_02.draw(400, 250)
        self.tile_image_02.draw(400+128, 250)
        self.tile_image_02.draw(300, 150)



    def handle_collision(self, group, other):
        pass