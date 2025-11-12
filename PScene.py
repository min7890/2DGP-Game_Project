class Pscene:
    def __init__(self):
        self.elements = []

    def update(self):
        pass

    def draw(self):
        for element in self.elements:
            element.draw(None)
        pass

    def add_element(self, element):
        self.elements.append(element)
        pass

    def remove_element(self, element):
        if element in self.elements:
            self.elements.remove(element)
        pass


