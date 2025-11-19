from pico2d import *
import game_framework

class Portal:
    def __init__(self,x =400, y = 300):
        self.image = load_image('portal.png')
        self.x, self.y = x, y
        self.rotation = 0
        self.time_sum = 0.0

    def update(self):
        self.time_sum += game_framework.frame_time * -200
        self.rotation = (self.time_sum + 180) % 360 - 180


    def draw(self):
        self.image.clip_composite_draw(0, 0, 512, 512, self.rotation, '', self.x, self.y, 100, 100)
        self.image.clip_composite_draw(0, 512, 512, 512, self.rotation, '', self.x, self.y, 100, 100)
        self.image.clip_composite_draw(512, 0, 512, 512, self.rotation, '', self.x, self.y, 100, 100)
        self.image.clip_composite_draw(512, 512, 512, 512, self.rotation, '', self.x, self.y, 100, 100)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def handle_collision(self, group, other):
        pass