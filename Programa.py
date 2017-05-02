import pyglet
from random import randint

class Window(pyglet.window.Window):

    def __init__ (self):
        super(Window, self).__init__(1200,600,caption="RPG",resizable=True)
        self.char = Humano("Citizen.png", 400, 300)
        self.snout = Troll("Troll.png", 100, 100)

        pyglet.clock.schedule_interval(self.update, 0.000000001)

    def update(self, dt):
        self.clear()
        self.char.draw()
        self.snout.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.char.addy = 2
        elif symbol == pyglet.window.key.DOWN:
            self.char.addy = -2
        elif symbol == pyglet.window.key.LEFT:
             self.char.addx = -2
        elif symbol == pyglet.window.key.RIGHT:
            self.char.addx = 2


    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.char.addy = 0
        elif symbol == pyglet.window.key.DOWN:
            self.char.addy = 0
        elif symbol == pyglet.window.key.LEFT:
            self.char.addx = 0
        elif symbol == pyglet.window.key.RIGHT:
            self.char.addx = 0

class Humano():

    def __init__(self, nome, x, y):
        self.x = x
        self.y = y
        self.addx = 0
        self.addy = 0
        self.image = pyglet.resource.image(nome)

    def draw(self):
        self.x += self.addx
        self.y += self.addy
        self.image.blit(self.x,self.y)

class Troll():

    def __init__(self,nome, x, y):
        self.x = x
        self.y = y
        self.addx = 0
        self.addy = 0
        self.image = pyglet.resource.image(nome)

    def draw(self):
        self.x += self.addx
        self.y += self.addy
        self.image.blit(self.x,self.y)
        
def main():
    window = Window()
    pyglet.app.run()

if __name__ == "__main__":
    main()