import random

from pico2d import *
from physics_data import WIN_WIDTH, WIN_HEIGHT

from background import Background
from robo_spider import RoboSpider
from player import Player
from tile import Ground
from mine import Mine
from camera import Camera
from UI_play_scene import UIResourceData, UISpiderStatus
import UI_Upgrade_scene
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

    mines = [Mine(1, 5, x = 1920 / 2, y = TILE_SIZE_PIXEL * 20 * (i // 2) * 2 * (-1) ** i + random.randint(0, int(TILE_SIZE_PIXEL * 6))) for i in range(1, 4)]
    game_world.add_objects(mines, 5)

    ground = Ground()
    game_world.add_object(ground, 2)

    ground.add_mines(mines)

    common.spider = RoboSpider()
    game_world.add_object(common.spider, 1)

    common.player = Player()
    game_world.add_object(common.player, 2)

    # enemy_test0 = InfantryTier0(common.spider.x + 72, common.spider.y - 400, common.spider)
    # enemy_test1 = SpitterTier0(common.spider.x - 600, common.spider.y - 100, common.spider)
    # game_world.add_object(enemy_test0, 2)
    # game_world.add_object(enemy_test1, 2)

    common.spider.mine_list = ground.get_mine_list()
    common.cam.apply_camera_settings()  # 기본 상태(스파이더 추적) 적용

    common.wave_manager = WaveManager()

    common.UI_ResourceData = UIResourceData()
    game_world.add_object(common.UI_ResourceData, 10)

    common.UI_SpiderStatus = UISpiderStatus()
    game_world.add_object(common.UI_SpiderStatus, 10)

    common.obj_pool = ObjectPool()


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
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

    common.UI_ResourceData = None
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