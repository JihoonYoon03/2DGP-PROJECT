from pico2d import *
from physics_data import *
import game_framework
import common
import title_scene
import play_scene


class GameEndWindow:
    def __init__(self):
        self.image = load_image('Assets/Sprites/UI/Message_Background.png')
        self.x = WIN_WIDTH / 2
        self.y = WIN_HEIGHT / 2
        self.menu_bar = MenuBar(self.x, self.y - self.image.h * 3 / 4 * WIN_H_RATIO)

    def update(self):
        self.menu_bar.update()

    def draw(self):
        self.image.draw(self.x, self.y, self.image.w * WIN_W_RATIO * 1.5, self.image.h * WIN_H_RATIO * 1.5)
        self.menu_bar.draw()

class MenuBar:
    def __init__(self, x, y):
        self.image_unselect = load_image('Assets/Sprites/UI/button_unselect.png')
        self.image_select = load_image('Assets/Sprites/UI/button_select.png')
        self.font_size = int(40 * WIN_W_RATIO)
        self.font = load_font('Assets/Fonts/NeoDunggeunmoPro-Regular.ttf', self.font_size)
        self.x = x
        self.y = y
        self.w = self.image_unselect.w * 3.5
        self.h = self.image_unselect.h * 3.5
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
            self.font.draw(self.x - len('메인 화면으로') * self.font_size / 2, self.y, '메인 화면으로', (0, 0, 0))
        else:
            self.image_unselect.draw(self.x, self.y, self.w * WIN_W_RATIO, self.h * WIN_H_RATIO)
            self.font.draw(self.x - len('메인 화면으로') * self.font_size / 2, self.y, '메인 화면으로', (255, 255, 255))

def init():
    global end
    end = GameEndWindow()

def handle_events():
    global end
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            # 나가기 창 띄우기
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            common.mouse_x, common.mouse_y = event.x, WIN_HEIGHT - event.y
        elif event.type == SDL_MOUSEBUTTONUP:
            if end.menu_bar.mouse_hovering:
                game_framework.pop_scene()
                game_framework.change_scene(title_scene)


def update():
    global end
    end.update()

def draw():
    global end
    clear_canvas()
    play_scene.draw_no_clear()
    end.draw()
    common.cursor_image.draw(common.mouse_x, common.mouse_y, common.cursor_image.w * WIN_W_RATIO * 3.4, common.cursor_image.h * WIN_H_RATIO * 3.4)
    update_canvas()

def pause():
    pass

def resume():
    pass

def finish():
    pass