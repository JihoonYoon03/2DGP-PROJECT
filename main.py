from pico2d import *

from background import Background
from robo_spider import RoboSpider

def reset_world():
    global world
    global spider

    world = []

    background = Background()
    world.append(background)

    spider = RoboSpider()
    world.append(spider)

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            spider.handle_event(event)


def update_world():
    global world
    for thing in world:
        thing.update()


def render_world():
    global world

    for thing in world:
        thing.draw()

running = True


open_canvas()
reset_world()

while running:
    clear_canvas()

    # logic
    handle_events()
    update_world()

    # render
    render_world()
    update_canvas()
    delay(0.05)

close_canvas()