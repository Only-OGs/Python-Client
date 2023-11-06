import pyglet
from pyglet.window import key
import socketio

# PyGlet Window
window = pyglet.window.Window(800, 600)

# Label
label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')
# Erstelle SocketIO Client
sio = socketio.Client()

@window.event
def on_draw():
    window.clear()
    label.draw()
# Event-Handler für Antworten vom Server
@sio.event
def response(data):
    print(f"Server response: {data}")

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        sio.emit('message', "A pressed")
        label.text = "A pressed"

if __name__ == '__main__':
    sio.connect('http://localhost:8080')
    pyglet.app.run()



