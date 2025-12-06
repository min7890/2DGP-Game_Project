from pico2d import *
import game_framework
import random
import game_world

class Item:
    def __init__(self,x =400, y = 300):
        self.Mp_potion_image = load_image('Mp_potion.png')
        self.Hp_potion_image = load_image('Hp_potion.png')
        self.x, self.y = x, y
        self.Mp_or_Hp = random.randint(0, 1) #0:Mp, 1:Hp

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
        if self.Mp_or_Hp == 0:
            self.Mp_potion_image.draw(self.x, self.y, 50, 50)
        else:
            self.Hp_potion_image.draw(self.x, self.y, 50, 50)

        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 25, self.y - 20, self.x + 25, self.y + 20


    def handle_collision(self, group, other):
        if group == 'item:player':
            game_world.remove_object(self)

        if group == 'tile:item':
            left, bottom, right, top = other.get_bb()

            if self.y > top and left <= self.x <= right:
                if not hasattr(self, 'candidate_grounds'):
                    self.candidate_grounds = []
                self.candidate_grounds.append(top + 18)

        pass