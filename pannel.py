from pico2d import load_image
import common

class Pannel:
    def __init__(self):
        if common.player.life <= 0:
            self.image = load_image('lose.png')
        else:
            self.image = load_image('win.png')

    def draw(self):
        self.image.draw(300, 300, 400, 300)

    def update(self):
        pass