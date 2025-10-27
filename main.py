from pico2d import *

from background import Background
from robo_spider import RoboSpider
from camera import Camera
import game_world
from tile import Tile

tile = None

def reset_world():
    global spider
    global camera
    #global tile

    background = Background()
    game_world.add_object(background, 0)

    spider = RoboSpider()
    game_world.add_object(spider, 1)

    #tile = Tile()
    #game_world.add_object(tile, 2)

    camera = Camera(800, 600, spider)


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            game_world.handle_event(event)
            camera.handle_event(event)


def update_world():
    game_world.update()
    camera.update()


def render_world():
    global camera
    game_world.render(camera)

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