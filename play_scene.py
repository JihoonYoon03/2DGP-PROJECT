from pico2d import *

from background import Background
from robo_spider import RoboSpider
from tile import Tile
from camera import Camera
import game_world
import game_framework

tile = None

def init():
    global spider
    global camera
    global tile

    background = Background()
    game_world.add_object(background, 0)

    spider = RoboSpider()
    game_world.add_object(spider, 1)

    tile = Tile()
    game_world.add_object(tile, 2)

    camera = Camera(800, 600)
    camera.cam_lock(spider)


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            game_world.handle_event(event)
            camera.handle_event(event)


def update():
    game_world.update()
    camera.update()
    delay(0.05)


def draw():
    global camera
    clear_canvas()
    game_world.render(camera)
    update_canvas()

def pause():
    pass

def resume():
    pass

def finish():
    game_world.clear()