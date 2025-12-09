from pico2d import load_image

class Life:
    def __init__(self, x = 400, y = 300):
        self.image = load_image('life.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)

    def update(self):
        pass

class Boss_Life:
    def __init__(self, x = 400, y = 300):
        self.image = load_image('boss_life.png')
        self.x, self.y = x, y

    def draw(self):
        self.image.draw(self.x, self.y, 100, 100)

    def update(self):
        pass
