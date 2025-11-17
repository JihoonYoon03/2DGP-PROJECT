from pico2d import *
from physics_data import WIN_WIDTH, WIN_HEIGHT

from background import Background
from robo_spider import RoboSpider
from tile import Ground
from mine import Mine
from camera import Camera
import game_world
import game_framework

def init():
    background = Background()
    game_world.add_object(background, 0)

    cam = Camera(WIN_WIDTH, WIN_HEIGHT)
    game_world.set_camera(cam)

    mines = [Mine(1)]
    game_world.add_objects(mines, 1)

    ground = Ground()
    game_world.add_object(ground, 1)

    ground.add_mines(mines)

    spider = RoboSpider()
    game_world.add_object(spider, 2)

    spider.mine_list = ground.get_mine_list()
    cam.cam_lock(spider, WIN_WIDTH // 3)


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
    game_world.handle_collisions_bb()


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