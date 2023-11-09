import pyglet


class GameMenu(pyglet.window.Window):
    label = None

    def __init__(self):
        # PyGlet Window
        super().__init__(800, 600)
        self.mainMenu()


    def mainMenu(self):
        self.label = pyglet.text.Label('Hello, world',
                                       font_name='Times New Roman',
                                       font_size=36,
                                       x=self.width // 2, y=self.height // 2,
                                       anchor_x='center', anchor_y='center')

    def on_draw(self):
        self.clear()
        self.label.draw()
