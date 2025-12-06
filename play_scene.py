import random

from pico2d import *

import event_set
from physics_data import WIN_WIDTH, WIN_HEIGHT

from background import Background
from robo_spider import RoboSpider
from player import Player
from tile import Ground
from mine import Mine
from camera import Camera
from UI_play_scene import UIResourceData, UISpiderStatus, UIKey
import upgrade_scene
import esc_scene
from object_pool import ObjectPool
from enemy import *
import common
import game_world
import game_framework
import physics_data

def init():
    clear()
    hide_cursor()
    common.cursor_image = load_image('Assets/Sprites/UI/Cursor_Target.png')
    common.background = Background()
    game_world.add_object(common.background, 0)

    common.cam = Camera(WIN_WIDTH, WIN_HEIGHT)

    ground = Ground()
    game_world.add_object(ground, 1)


    mines = [Mine(4, 1920 / 2, TILE_SIZE_PIXEL * 20 * (i // 2) * 2 * (-1) ** i + random.randint(0, int(TILE_SIZE_PIXEL * i * 2))) for i in range(1, 4)]
    game_world.add_objects(mines, 1)
    ground.add_mines(mines)

    common.spider = RoboSpider()
    game_world.add_object(common.spider, 1)

    common.player = Player()
    game_world.add_object(common.player, 2)

    common.spider.mine_list = ground.get_mine_list()
    common.cam.apply_camera_settings()  # 기본 상태(스파이더 추적) 적용

    common.wave_manager = WaveManager()

    common.UI_ResourceData = UIResourceData()
    game_world.add_object(common.UI_ResourceData, 10)

    common.UI_SpiderStatus = UISpiderStatus()
    game_world.add_object(common.UI_SpiderStatus, 10)

    common.UI_Key = UIKey()
    game_world.add_object(common.UI_Key, 10)

    common.obj_pool = ObjectPool()


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            event_set.reset_all_flags()
            common.spider.move_dir = 0
            common.player.move_x = 0
            common.player.move_y = 0
            common.player.stateMachine.handle_state_event(('EMPTY', None))
            game_framework.push_scene(esc_scene)
        elif event.type == SDL_MOUSEMOTION:
            common.mouse_x, common.mouse_y = event.x, WIN_HEIGHT - event.y

        game_world.handle_event(event)


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    common.cursor_image.draw(common.mouse_x, common.mouse_y, common.cursor_image.w * WIN_W_RATIO * 3.4, common.cursor_image.h * WIN_H_RATIO * 3.4)
    update_canvas()

def draw_no_clear():
    game_world.render()

def pause():
    pass

def resume():
    pass

def finish():
    game_world.clear()

def clear():
    common.cam = None
    common.spider = None
    common.player = None

    common.UI_SpiderStatus = None

    common.obj_pool = None
    common.wave_manager = None

    common.cursor_image = None
    common.mouse_x, common.mouse_y = 0, 0
    common.ore_list = []

    common.run_time = 0
    common.debug_mode = False
    physics_data.clear()
    game_world.clear()