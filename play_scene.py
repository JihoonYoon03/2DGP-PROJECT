from pico2d import *

from background import Background
from robo_spider import RoboSpider
from tile import Ground
from mine import Mine
from camera import Camera
import game_world
import game_framework

def init():
    global spider
    global ground
    global mines

    background = Background()
    game_world.add_object(background, 0)

    spider = RoboSpider()
    game_world.add_object(spider, 1)

    ground = Ground()
    game_world.add_object(ground, 2)

    cam = Camera(800, 600)
    cam.cam_lock(spider)
    game_world.set_camera(cam)

    mines = Mine(1)
    game_world.add_object(mines, 2)


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            game_world.handle_event(event)


def update():
    game_world.update()
    delay(0.05)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

def finish():
    game_world.clear()