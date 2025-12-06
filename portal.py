from pico2d import *
import game_framework
import common

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
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.image.clip_composite_draw(0, 0, 512, 512, self.rotation, '', sx_, sy_, 100, 100)
        self.image.clip_composite_draw(0, 512, 512, 512, self.rotation, '', sx_, sy_, 100, 100)
        self.image.clip_composite_draw(512, 0, 512, 512, self.rotation, '', sx_, sy_, 100, 100)
        self.image.clip_composite_draw(512, 512, 512, 512, self.rotation, '', sx_, sy_, 100, 100)

        draw_rectangle(sx_ - 50, sy_ - 50, sx_ + 50, sy_ + 50)

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def handle_collision(self, group, other):
        pass


    # def handle_detection_collision(self, group, other):
    #     pass