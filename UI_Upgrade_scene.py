from pico2d import *

import common
import event_set
import game_framework
import play_scene
import math
from physics_data import *


def clip_draw_frame(image, clip_x, clip_y, clip_w, clip_h, draw_x, draw_y, draw_w, draw_h):
    frame_w = WIN_WIDTH * 1104 / WIN_WIDTH
    frame_h = WIN_HEIGHT * 620 / WIN_HEIGHT
    left = draw_x - draw_w // 2
    right = draw_x + draw_w // 2
    top = draw_y + draw_h // 2
    bottom = draw_y - draw_h // 2
    if left < (WIN_WIDTH - frame_w) // 2:
        draw_w -= (frame_w // 2 - draw_x + left)
        clip_x += (frame_w // 2 - draw_x + left) * (clip_w / draw_w)
        left = (WIN_WIDTH - frame_w) // 2
    elif right < (WIN_WIDTH - frame_w) // 2:
        draw_w -= (right - (WIN_WIDTH + frame_w) // 2)
        clip_w -= (right - (WIN_WIDTH + frame_w) // 2) * (clip_w / draw_w)
        right = (WIN_WIDTH + frame_w) // 2
    if bottom < (WIN_HEIGHT - frame_h) // 2:
        draw_h -= (frame_h // 2 - draw_y + bottom)
        clip_y += (frame_h // 2 - draw_y + bottom) * (clip_h / draw_h)
        bottom = (WIN_HEIGHT - frame_h) // 2
    elif top < (WIN_HEIGHT - frame_h) // 2:
        draw_h -= (top - (WIN_HEIGHT + frame_h) // 2)
        clip_h -= (top - (WIN_HEIGHT + frame_h) // 2) * (clip_h / draw_h)
        top = (WIN_HEIGHT + frame_h) // 2
    if draw_w > 0 and draw_h > 0:
        image.clip_draw(int(clip_x), int(clip_y), int(clip_w), int(clip_h),
                        (left + right) // 2, (top + bottom) // 2,
                        draw_w, draw_h)

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

        frame_width = self.w * 0.8 * self.w_ratio
        frame_left = WIN_WIDTH // 2 - frame_width // 2 * 1.05
        frame_height = self.h * 0.8 * self.h_ratio
        frame_top = WIN_HEIGHT // 2 + frame_height // 2 * 1.1
        y = frame_top - frame_height * 0.2
        self.upgrade_menu = [
            UpgradeType(int(frame_left + frame_width * 1 / 6), y, frame_width * 0.25, '머신건'),
            UpgradeType(int(frame_left + frame_width * 3 / 6), y, frame_width * 0.25, '엑소슈트'),
            UpgradeType(int(frame_left + frame_width * 5 / 6), y, frame_width * 0.25, '로보스파이더'),
        ]

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
            for upgrade in self.upgrade_menu:
                upgrade.draw()
            self.image_const.draw(WIN_WIDTH // 2, WIN_HEIGHT // 2, self.w * self.w_ratio, self.h * self.h_ratio)

    def exit(self):
        self.frame_dir = -1


class UpgradeType:
    image_icon = None
    image_header = None
    image_branch = None
    image_branch_back = None

    font = None
    font_size = int(24 * WIN_W_RATIO)

    sprite_coord = {
        '머신건': (0, 0),
        '엑소슈트': (0, 64),
        '로보스파이더': (64, 64)
    }

    icon_w = 64
    icon_h = 64
    header_offset_y = int(-icon_h * 0.64 * WIN_H_RATIO)
    branch_y = 0
    branch_back_w = 0
    branch_back_h = 0

    frame_w = 0
    frame_h = 0

    def __init__(self, x, y, back_w, image_path, row=12):
        if UpgradeType.font is None:
            UpgradeType.font = load_font('Assets/Fonts/NeoDunggeunmoPro-Regular.ttf', self.font_size)
        if UpgradeType.image_icon is None:
            UpgradeType.image_icon = load_image('Assets/Sprites/UI/BranchIcons.png')
        if UpgradeType.image_header is None:
            UpgradeType.image_header = load_image('Assets/Sprites/UI/Window_Talent_Branch_Header_Background.png')
        if UpgradeType.image_branch is None:
            UpgradeType.image_branch = (
                load_image('Assets/Sprites/UI/Window_Talent_TierPlate_Path_Triple.png'),
                load_image('Assets/Sprites/UI/Window_Talent_TierPlate_Path_DownLeft.png'),
                load_image('Assets/Sprites/UI/Window_Talent_TierPlate_Path_DownRight.png')
            )
        if UpgradeType.image_branch_back is None:
            UpgradeType.image_branch_back = load_image('Assets/Sprites/UI/Window_Talent_Branch_Background.png')
        self.branch_y = y - (self.icon_h + self.image_branch[0].h) * WIN_H_RATIO

        self.image_path = image_path
        self.x = x
        self.y = y
        self.button_row = row
        self.icon_clip_x = UpgradeType.sprite_coord[image_path][0]
        self.icon_clip_y = UpgradeType.sprite_coord[image_path][1]
        self.offset = 1.5
        self.branch_back_w = back_w
        self.branch_back_h = 44

    def draw(self):# branch_back 길이 설정 (중앙 파트 반복 개수)
        part_h = 12
        part_w = self.image_branch_back.w
        img_h = self.image_branch_back.h
        start_y = self.branch_y - (self.image_branch[0].h // 2 + self.branch_back_h) * WIN_H_RATIO

        # 앞 파트
        clip_draw_frame(
            self.image_branch_back,
            0, img_h - part_h, part_w, part_h,
            self.x, start_y,
            self.branch_back_w, self.branch_back_h,
        )

        # 중앙 파트 반복 출력 (y값 감소)
        i = 0
        for i in range(self.button_row):
            clip_draw_frame(
                self.image_branch_back,
                0, img_h - part_h - 44, part_w, part_h,
                self.x, start_y - part_h - 44 * (i + 1) * WIN_H_RATIO,
                self.branch_back_w, 44
            )
        # 뒤 파트
        clip_draw_frame(
            self.image_branch_back,
            0, 0, part_w, part_h,
            self.x, start_y - part_h - 44 * (i + 2) * WIN_H_RATIO,
            self.branch_back_w, self.branch_back_h
        )
        clip_draw_frame(
            self.image_branch[0],
            0, 0, self.image_branch[0].w, self.image_branch[0].h,
            self.x, self.branch_y,
            self.image_branch[0].w * WIN_W_RATIO * self.offset,
            self.image_branch[0].h * WIN_H_RATIO * self.offset
        )

        # image_header를 image_icon 하단에 출력
        clip_draw_frame(
            self.image_header,
            0, 0, self.image_header.w, self.image_header.h,
            self.x, self.y + UpgradeType.header_offset_y,
            self.image_header.w * WIN_W_RATIO * self.offset, self.image_header.h * WIN_H_RATIO * self.offset
        )
        clip_draw_frame(
            self.image_icon,
            self.icon_clip_x, self.image_icon.h - self.icon_h - self.icon_clip_y,
            self.icon_w, self.icon_h,
            self.x, self.y,
            self.icon_w * WIN_W_RATIO * self.offset, self.icon_h * WIN_H_RATIO * self.offset
        )

        self.font.draw(self.x - len(self.image_path) * self.font_size / 2,
                       self.y - self.icon_h // 2 - self.font_size,
                       self.image_path, (255, 200, 0))


class UpgradeButton:
    image_icon = None
    def __init__(self):
        if UpgradeButton.image_icon is None:
            UpgradeButton.image_icon = load_image('Assets/Sprites/UI/TalentIcons.png')

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