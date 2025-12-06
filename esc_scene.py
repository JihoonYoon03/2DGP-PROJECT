from pico2d import *
from physics_data import WIN_WIDTH, WIN_HEIGHT, WIN_W_RATIO, WIN_H_RATIO
import common
import game_framework
import play_scene
import event_set
import title_scene

class EscapeWindow:
    def __init__(self):
        self.image = load_image('Assets/Sprites/UI/Message_Background.png')
        self.font_size = int(28 * WIN_W_RATIO)
        self.font = load_font('Assets/Fonts/NeoDunggeunmoPro-Regular.ttf', self.font_size)
        self.x = WIN_WIDTH / 2
        self.y = WIN_HEIGHT / 2
        self.w = self.image.w * WIN_W_RATIO * 16.0 / 6
        self.h = self.image.h * WIN_H_RATIO * 9.0 / 6
        self.menu_bar = [MenuBar(self.x - self.w * 0.25, self.y - self.image.h * 0.5 * WIN_H_RATIO, '예'),
                         MenuBar(self.x + self.w * 0.25, self.y - self.image.h * 0.5 * WIN_H_RATIO, '아니오')]

    def update(self):
        self.menu_bar[0].update()
        self.menu_bar[1].update()

    def draw(self):
        str_esc = f'메인 화면으로 나가기'
        self.image.draw(self.x, self.y, self.w, self.h)
        self.font.draw(self.x - len(str_esc) * self.font_size * 0.44, self.y + self.image.h * 0.1, str_esc, (240, 220, 0))
        self.menu_bar[0].draw()
        self.menu_bar[1].draw()


class MenuBar:
    sound = None
    def __init__(self, x, y, string):
        if MenuBar.sound is None:
            MenuBar.sound = load_wav('Assets/Audios/UI/UI_Button_Click.wav')
            MenuBar.sound.set_volume(64)
        self.image_unselect = load_image('Assets/Sprites/UI/button_unselect.png')
        self.image_select = load_image('Assets/Sprites/UI/button_select.png')
        self.font_size = int(28 * WIN_W_RATIO)
        self.font = load_font('Assets/Fonts/NeoDunggeunmoPro-Regular.ttf', self.font_size)
        self.x = x
        self.y = y
        self.string = string
        self.w = self.image_unselect.w * 2.0
        self.h = self.image_unselect.h * 1.5
        self.mouse_hovering = False

    def update(self):
        if (self.x - self.w / 2 * WIN_W_RATIO <= common.mouse_x <= self.x + self.w / 2 * WIN_W_RATIO and
            self.y - self.h / 2 * WIN_H_RATIO <= common.mouse_y <= self.y + self.h / 2 * WIN_H_RATIO):
            self.mouse_hovering = True
        else:
            self.mouse_hovering = False

    def draw(self):
        if self.mouse_hovering:
            self.image_select.draw(self.x, self.y, self.w * WIN_W_RATIO, self.h * WIN_H_RATIO)
            self.font.draw(self.x - len(self.string) * self.font_size * 0.46, self.y, self.string, (0, 0, 0))
        else:
            self.image_unselect.draw(self.x, self.y, self.w * WIN_W_RATIO, self.h * WIN_H_RATIO)
            self.font.draw(self.x - len(self.string) * self.font_size * 0.46, self.y, self.string, (255, 255, 255))


def init():
    global esc
    esc = EscapeWindow()

def handle_events():
    global esc
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
        elif event.type == SDL_KEYUP and event.key == SDLK_a and event_set.flag_a:
            event_set.flag_a = False
            common.player.face_dir += 1
        elif event.type == SDL_KEYUP and event.key == SDLK_d and event_set.flag_d:
            event_set.flag_d = False
            common.player.face_dir += 1
        elif event.type == SDL_MOUSEBUTTONUP:
            if esc.menu_bar[0].mouse_hovering:  # 나가기
                MenuBar.sound.play()
                game_framework.pop_scene()
                game_framework.change_scene(title_scene)
            elif esc.menu_bar[1].mouse_hovering: # 취소
                MenuBar.sound.play()
                game_framework.pop_scene()


def update():
    global esc
    esc.update()

def draw():
    global esc
    clear_canvas()
    play_scene.draw_no_clear()
    esc.draw()
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