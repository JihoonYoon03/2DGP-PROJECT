from pico2d import *

from robo_spider import RoboSpider

open_canvas(800, 600)



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