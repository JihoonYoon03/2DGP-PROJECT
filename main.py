from pico2d import *


open_canvas(800, 600)

class RoboSpider:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.image = load_image('Assets/Sprites/Spider/Spider_Moving.png')
        self.width = self.image.w
        self.height = self.image.h

    def update(self):
        self.frame = (self.frame + 1) % 16

    def draw(self):
        self.image.clip_draw(self.frame * 178 % (11 * 178), self.height - 440 - (self.frame // 11 * 444), 178, 440, self.x, self.y)
        print(f'{self.frame // 10}')


def reset_world():
    global world

    world = []
    spider = RoboSpider()
    world.append(spider)

def handle_events():
    pass


def update_world():
    global world
    for thing in world:
        thing.update()


def render_world():
    global world

    for thing in world:
        thing.draw()

reset_world()

while True:
    clear_canvas()

    # logic
    handle_events()
    update_world()

    # render
    render_world()
    update_canvas()
    delay(0.05)

close_canvas()