from pico2d import *
import game_framework

class Item:
    def __init__(self,x =400, y = 300):
        self.Mp_potion_image = load_image('Mp_potion.png')
        self.Hp_potion_image = load_image('Hp_potion.png')
        self.x, self.y = x, y

    def update(self):
        if hasattr(self, 'candidate_grounds') and self.candidate_grounds:
            self.ground = max(self.candidate_grounds)
            self.candidate_grounds = []
        else:
            self.ground = 90

        if self.y > self.ground:
            self.velocity_y = -800 * game_framework.frame_time
            self.y += self.velocity_y
            if self.y < self.ground:
                self.y = self.ground
        else:
            self.y = self.ground


    def draw(self):
        self.Hp_potion_image.draw(self.x, self.y, 50, 50)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 20, self.x + 25, self.y + 20


    def handle_collision(self, group, other):
        pass