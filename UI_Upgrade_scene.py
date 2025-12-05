from pico2d import *

import common
import event_set
import game_framework
from physics_data import *

mouse_x, mouse_y = 0, 0

class MainImage:
    def __init__(self):
        self.image = load_image('Assets/Sprites/Background/Loading_Background.png')
        self.image_hole = load_image('Assets/Sprites/Background/Loading_Center.png')
        self.hole_w = 76
        self.hole_h = 72
        self.frame = 0
        self.frame_len = 12
        self.frame_speed = 8  # frames per second

        self.sprite_coord =(
            (0, 0), (76, 0), (152, 0), (228, 0), (304, 0), (380, 0),
            (0, 72), (76, 72), (152, 72), (228, 72), (304, 72), (380, 72)
        )

    def update(self):
        self.frame = (self.frame + self.frame_speed * game_framework.frame_time) % self.frame_len

    def draw(self):
        x, y = self.sprite_coord[int(self.frame)]
        self.image.draw(WIN_WIDTH // 2, WIN_HEIGHT // 2, WIN_WIDTH, WIN_HEIGHT)
        self.image_hole.clip_draw(x, self.image_hole.h - self.hole_h - y, self.hole_w, self.hole_h,
                                  WIN_WIDTH * 0.653, WIN_HEIGHT * 0.668,
                                  self.hole_w * WIN_W_RATIO * 4, self.hole_h * WIN_H_RATIO * 4)

class Logo:
    def __init__(self):
        self.x = WIN_WIDTH // 2
        self.y = WIN_HEIGHT - WIN_HEIGHT // 8
        self.w = 340
        self.h = 190
        self.frame = 0
        self.frame_len = 18
        self.frame_speed = 10 # frames per second
        self.image = load_image('Assets/Sprites/UI/LOGO_Final animation.png')

        self.sprite_coord = (
            (0, 0), (340, 0), (680, 0), (1020, 0), (1360, 0), (1700, 0),
            (0, 190), (340, 190), (680, 190), (1020, 190), (1360, 190), (1700, 190),
            (0, 380), (340, 380), (680, 380), (1020, 380), (1360, 380), (1700, 380)
        )

    def update(self):
        self.frame += self.frame_speed * game_framework.frame_time
        if self.frame >= self.frame_len:
            self.frame = self.frame_len - 1

    def draw(self):
        x, y = self.sprite_coord[int(self.frame)]
        self.image.clip_draw(x, self.image.h - self.h - y, self.w, self.h, self.x, self.y, self.w * WIN_W_RATIO, self.h * WIN_H_RATIO)

class MenuBar:
    def __init__(self):
        self.image_unselect = load_image('Assets/Sprites/UI/button_unselect.png')
        self.image_select = load_image('Assets/Sprites/UI/button_select.png')
        self.font = load_font('Assets/Fonts/Fifaks10Dev1.ttf', int(40 * WIN_W_RATIO))
        self.x = WIN_WIDTH // 2
        self.y = WIN_HEIGHT // 8
        self.w = self.image_unselect.w * 3.5
        self.h = self.image_unselect.h * 3.5
        self.mouse_hovering = False

    def update(self):
        global mouse_x, mouse_y
        if (self.x - self.w / 2 * WIN_W_RATIO <= mouse_x <= self.x + self.w / 2 * WIN_W_RATIO and
            self.y - self.h / 2 * WIN_H_RATIO <= mouse_y <= self.y + self.h / 2 * WIN_H_RATIO):
            self.mouse_hovering = True
        else:
            self.mouse_hovering = False

    def draw(self):
        if self.mouse_hovering:
            self.image_select.draw(self.x, self.y, self.w * WIN_W_RATIO, self.h * WIN_H_RATIO)
            self.font.draw(self.x - 100 * WIN_W_RATIO, self.y - 4 * WIN_H_RATIO, 'GAME START', (0, 0, 0))
        else:
            self.image_unselect.draw(self.x, self.y, self.w * WIN_W_RATIO, self.h * WIN_H_RATIO)
            self.font.draw(self.x - 100 * WIN_W_RATIO, self.y - 4 * WIN_H_RATIO, 'GAME START', (255, 255, 255))

def init():
    global main_image, logo_image, menu_bar
    main_image = MainImage()
    logo_image = Logo()
    menu_bar = MenuBar()

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # 나가기 창 띄우기
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            common.mouse_x, common.mouse_y = event.x, WIN_HEIGHT - event.y
        elif event.type == SDL_KEYDOWN and event.key == SDLK_f:
            game_framework.pop_scene()
        elif event.type == SDL_KEYUP and event.key == SDLK_w:
            event_set.flag_w = False
            common.spider.move_dir -= 1
        elif event.type == SDL_KEYUP and event.key == SDLK_s:
            event_set.flag_s = False
            common.spider.move_dir += 1


def update():
    global logo_image, menu_bar, main_image
    main_image.update()
    logo_image.update()
    menu_bar.update()

def draw():
    global main_image, logo_image, menu_bar
    clear_canvas()
    main_image.draw()
    logo_image.draw()
    menu_bar.draw()
    common.cursor_image.draw(common.mouse_x, common.mouse_y, common.cursor_image.w * WIN_W_RATIO * 3.4, common.cursor_image.h * WIN_H_RATIO * 3.4)
    update_canvas()

def pause():
    pass

def resume():
    pass

def finish():
    pass