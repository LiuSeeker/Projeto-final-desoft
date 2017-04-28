import pyglet

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


class Window(pyglet.window.Window):

    def __init__ (self):
        super(Window, self).__init__(800,600,caption="RPG")
        self.char = Humano("Ciizen.png", 400, 300)

        pyglet.clock.schedule_interval(self.update, 0.001)

    def update(self, dt):
        self.clear()
        self.char.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.char.addy = 5
        elif symbol == pyglet.window.key.DOWN:
            self.char.addy = -5
        elif symbol == pyglet.window.key.LEFT:
             mself.char.addx = -5
        elif symbol == pyglet.window.key.RIGHT:
            self.char.addx = 5
        print(self.char.addy, self.char.addx)

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP:
            self.char.addy = 0
        elif symbol == pyglet.window.key.DOWN:
            self.char.addy = 0
        elif symbol == pyglet.window.key.LEFT:
            self.char.addx = 0
        elif symbol == pyglet.window.key.RIGHT:
            self.char.addx = 0
        
def main():
    window = Window()
    pyglet.app.run()

if __name__ == "__main__":
    main()

