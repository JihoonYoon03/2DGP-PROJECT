from pico2d import *

import common
import event_set
import game_framework
import play_scene
from physics_data import *

class UIFrame:
    def __init__(self):
        self.image_anim = load_image('Assets/Sprites/UI/Open_Window_Talent_Animation.png')
        self.image_const = load_image('Assets/Sprites/UI/Window_Talent_Frame.png')
        self.image_back = load_image('Assets/Sprites/UI/Window_Talent_Background.png')
        self.frame = 0
        self.frame_dir = 1
        self.frame_len = 11
        self.frame_speed = 16  # frames per second
        self.w = 1104
        self.h = 620
        self.w_ratio = WIN_WIDTH / self.w
        self.h_ratio = WIN_HEIGHT / self.h

        self.sprite_coord =(
            (0, 0), (1104, 0), (2208, 0),
            (0, 620), (1104, 620), (2208, 620),
            (0, 1240), (1104, 1240), (2208, 1240),
            (0, 1860), (1104, 1860)
        )

    def update(self):
        self.frame += self.frame_speed * game_framework.frame_time * self.frame_dir
        if self.frame >= self.frame_len:
            self.frame = self.frame_len
        elif self.frame < 0:
            self.frame = 0
            game_framework.pop_scene()

    def draw(self):
        if self.frame < self.frame_len:
            x, y = self.sprite_coord[int(self.frame)]
            self.image_anim.clip_draw(x, self.image_anim.h - self.h - y, self.w, self.h,
                                      WIN_WIDTH // 2, WIN_HEIGHT // 2,
                                      self.w * self.w_ratio, self.h * self.h_ratio)
        else:
            self.image_back.draw(WIN_WIDTH // 2, WIN_HEIGHT // 2, self.w * self.w_ratio, self.h * self.h_ratio)
            self.image_const.draw(WIN_WIDTH // 2, WIN_HEIGHT // 2, self.w * self.w_ratio, self.h * self.h_ratio)

    def exit(self):
        self.frame_dir = -1


class UpgradeType:
    def __init__(self, x, y, w, h, image_path):
        pass

class UpgradeButton:
    def __init__(self):
        pass

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
    global frame
    frame = UIFrame()

def handle_events():
    global frame
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            common.mouse_x, common.mouse_y = event.x, WIN_HEIGHT - event.y
        elif event.type == SDL_KEYUP and event.key == SDLK_w and event_set.flag_w:
            event_set.flag_w = False
            common.spider.move_dir -= 1
        elif event.type == SDL_KEYUP and event.key == SDLK_s and event_set.flag_s:
            event_set.flag_s = False
            common.spider.move_dir += 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            frame.exit()


def update():
    global frame
    frame.update()

def draw():
    global frame
    clear_canvas()
    play_scene.draw_no_clear()
    frame.draw()
    common.UI_ResourceData.draw()
    common.UI_SpiderStatus.draw()
    common.cursor_image.draw(common.mouse_x, common.mouse_y, common.cursor_image.w * WIN_W_RATIO * 3.4, common.cursor_image.h * WIN_H_RATIO * 3.4)
    update_canvas()

def pause():
    pass

def resume():
    pass

def finish():
    pass