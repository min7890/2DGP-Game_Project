from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (1.0 / 0.02)

class Fire:
    image = None

    def __init__(self, x, y, throwin_speed = 10):
        if Fire.image == None:
            Fire.image = load_image('BulletAtlas.png')
        self.x, self.y = x, y
        self.xv = throwin_speed

    def draw(self):
        self.image.clip_draw(210, 125, 125, 110, self.x, self.y, 50, 50)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.x += self.xv * game_framework.frame_time * PIXEL_PER_METER

    def get_bb(self):
        return self.x - 30, self.y - 15, self.x + 20, self.y + 12

    def handle_collision(self, group, other):
        if group == 'monster_1:fire':
            current_stage = game_framework.stack[-1]
            game_world.remove_object(self)
            if hasattr(current_stage, 'get_map') and current_stage.get_map().monster_num > 0:
                current_stage.get_map().monster_num -= 1
                print(current_stage.get_map().monster_num)
        pass
    # def handle_detection_collision(self, group, other):
    #     pass