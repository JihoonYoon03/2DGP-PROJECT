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
    font_size = int(24 * WIN_W_RATIO)
    def __init__(self):
        self.image_anim = load_image('Assets/Sprites/UI/Open_Window_Talent_Animation.png')
        self.image_const = load_image('Assets/Sprites/UI/Window_Talent_Frame.png')
        self.image_back = load_image('Assets/Sprites/UI/Window_Talent_Background.png')
        self.font = load_font('Assets/Fonts/NeoDunggeunmoPro-Regular.ttf', self.font_size)
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
            self.font.draw(WIN_WIDTH // 2 - len('업그레이드') * self.font_size, WIN_HEIGHT // 2 + self.h // 2 * 0.9, '업그레이드', (255, 200, 0))
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

        self.upgrade_icon_list = [
            UpgradeButton(self.x, self.branch_y, '베어링 향상 (1)'),
        ]

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

        for button in self.upgrade_icon_list:
            button.draw()


class UpgradeButton:
    image_icon = None
    image_selling = None
    image_bought = None

    def __init__(self, x, y, upgrade_name, parent=None):
        if UpgradeButton.image_icon is None:
            UpgradeButton.image_icon = load_image('Assets/Sprites/UI/TalentIcons.png')
        if UpgradeButton.image_selling is None:
            UpgradeButton.image_selling = load_image('Assets/Sprites/UI/Window_Talent_TierPlate_Background.png')
        if UpgradeButton.image_bought is None:
            UpgradeButton.image_bought = load_image('Assets/Sprites/UI/Window_Talent_TierPlate_Bought.png')

        self.x = x
        self.y = y
        self.upgrade_name = upgrade_name
        self.icon_x = sprite_coord[upgrade_name][0]
        self.icon_y = sprite_coord[upgrade_name][1]
        self.icon_w = 30
        self.icon_h = 30
        self.parent = parent
        self.offset = 1.5

    def draw(self):
        if self.parent and upgrade_complete[self.parent] and upgrade_complete[self.upgrade_name]:
            clip_draw_frame(self.image_bought,
                            self.x, self.y,
                            0, 0, self.image_bought.w, self.image_bought.h,
                            self.image_bought.w * WIN_W_RATIO * self.offset,
                            self.image_bought.h * WIN_H_RATIO * self.offset)
        else:
            clip_draw_frame(self.image_selling,
                            0, 0, self.image_selling.w, self.image_selling.h,
                            self.x, self.y,
                            self.image_selling.w * WIN_W_RATIO * self.offset,
                            self.image_selling.h * WIN_H_RATIO * self.offset)
        clip_draw_frame(self.image_icon,
                        self.icon_x, self.image_icon.h - self.icon_h - self.icon_y,
                        self.icon_w, self.icon_h,
                        self.x + self.icon_w * WIN_W_RATIO * 0.1, self.y + self.icon_h * WIN_H_RATIO * 0.6,
                        self.icon_w * WIN_W_RATIO * self.offset,
                        self.icon_h * WIN_H_RATIO * self.offset
                        )



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


sprite_coord = {
    "베어링 향상 (1)": (1, 1),    "베어링 향상 (2)": (32, 1),   "베어링 향상 (3)": (63, 1),   "머신건 벨트 (1)": (94, 1),   "머신건 벨트 (2)": (125, 1),  "머신건 벨트 (3)": (156, 1),  "확장탄 (1)": (187, 1),  "확장탄 (2)": (218, 1),
    "확장탄 (3)": (249, 1),  "확장 구경 (1)": (280, 1),  "확장 구경 (2)": (311, 1),  "확장 구경 (3)": (342, 1),  "철갑탄 (1)": (373, 1),  "철갑탄 (2)": (404, 1),  "컴펜세이터 (1)": (435, 1),  "컴펜세이터 (2)": (466, 1),
    # "": (497, 1),  "": (528, 1),  "": (559, 1),  "": (590, 1),  "": (621, 1),  "": (652, 1),  "": (683, 1),  "": (714, 1),
    #
    # "": (1, 32),   "": (32, 32),  "": (63, 32),  "": (94, 32),  "": (125, 32), "": (156, 32), "": (187, 32), "": (218, 32),
    # "": (249, 32), "": (280, 32), "": (311, 32), "": (342, 32), "": (373, 32), "": (404, 32), "": (435, 32), "": (466, 32),
    # "": (497, 32), "": (528, 32), "": (559, 32), "": (590, 32), "": (621, 32), "": (652, 32), "": (683, 32), "": (714, 32),
    #
    # "": (1, 63),   "": (32, 63),  "": (63, 63),  "": (94, 63),  "": (125, 63), "": (156, 63), "": (187, 63), "": (218, 63),
    # "": (249, 63), "": (280, 63), "": (311, 63), "": (342, 63), "": (373, 63), "": (404, 63), "": (435, 63), "": (466, 63),
    # "": (497, 63), "": (528, 63), "": (559, 63), "": (590, 63), "": (621, 63), "": (652, 63), "": (683, 63), "": (714, 63),
    #
    # "": (1, 94),   "": (32, 94),  "": (63, 94),  "": (94, 94),  "": (125, 94), "": (156, 94), "": (187, 94), "": (218, 94),
    # "": (249, 94), "": (280, 94), "": (311, 94), "": (342, 94), "": (373, 94), "": (404, 94), "": (435, 94), "": (466, 94),
    # "": (497, 94), "": (528, 94), "": (559, 94), "": (590, 94), "": (621, 94), "": (652, 94), "": (683, 94), "": (714, 94),
    #
    # "": (1, 125),  "": (32, 125), "": (63, 125), "": (94, 125), "": (125, 125),"": (156, 125),"": (187, 125),"": (218, 125),
    # "": (249, 125),"": (280, 125),"": (311, 125),"": (342, 125),"": (373, 125),"": (404, 125),"": (435, 125),"": (466, 125),
    # "": (497, 125),"": (528, 125),"": (559, 125),"": (590, 125),"": (621, 125),"": (652, 125),"": (683, 125),"": (714, 125),

    '''"": (1, 156),  "": (32, 156),''' "리펄서 (1)": (63, 156), "리펄서 (2)": (94, 156), "리펄서 (3)": (125, 156), "플라즈마 안정성 (1)": (156, 156), "플라즈마 안정성 (2)": (187, 156), "플라즈마 커터 (1)": (218, 156),
    "플라즈마 커터 (2)": (249, 156), "플라즈마 커터 (3)": (280, 156),"플라즈마 커터 (4)": (311, 156),"플라즈마 커터 (5)": (342, 156),"플라즈마 커터 (6)": (373, 156),'''"": (404, 156),"": (435, 156),"": (466, 156),'''
    # "": (497, 156),"": (528, 156),"": (559, 156),"": (590, 156),"": (621, 156),
    "수리": (652, 156),
    # "": (683, 156),"": (714, 156),
                                                                                                                                       
    "효과적인 수리 (1)": (1, 187),  "효과적인 수리 (2)": (32, 187), "효과적인 수리 (3)": (63, 187),
    # "": (94, 187), "": (125, 187),"": (156, 187),"": (187, 187),"": (218, 187),
    # "": (249, 187),"": (280, 187),"": (311, 187),"": (342, 187),"": (373, 187),"": (404, 187),"": (435, 187),"": (466, 187),
    # "": (497, 187),"": (528, 187),"": (559, 187),"": (590, 187),"": (621, 187),"": (652, 187),"": (683, 187),"": (714, 187),
    #
    # "": (1, 218),  "": (32, 218), "": (63, 218), "": (94, 218), "": (125, 218),"": (156, 218),"": (187, 218),"": (218, 218),
    # "": (249, 218),"": (280, 218),"": (311, 218),"": (342, 218),"": (373, 218),"": (404, 218),"": (435, 218),"": (466, 218),
    # "": (497, 218),"": (528, 218),"": (559, 218),"": (590, 218),"": (621, 218),"": (652, 218),"": (683, 218),"": (714, 218),
    #
    # "": (1, 249),  "": (32, 249), "": (63, 249), "": (94, 249), "": (125, 249),"": (156, 249),"": (187, 249),"": (218, 249),
    # "": (249, 249),"": (280, 249),"": (311, 249),"": (342, 249),"": (373, 249),"": (404, 249),"": (435, 249),"": (466, 249),
    # "": (497, 249),"": (528, 249),"": (559, 249),"": (590, 249),"": (621, 249),"": (652, 249),"": (683, 249),"": (714, 249),
    #
    # "": (1, 280),  "": (32, 280), "": (63, 280), "": (94, 280), "": (125, 280),"": (156, 280),"": (187, 280),"": (218, 280),
    # "": (249, 280),"": (280, 280),"": (311, 280),"": (342, 280),"": (373, 280),"": (404, 280),"": (435, 280),"": (466, 280),
    # "": (497, 280),"": (528, 280),"": (559, 280),"": (590, 280),"": (621, 280),"": (652, 280),"": (683, 280),"": (714, 280),
    #
    # "": (1, 311),  "": (32, 311), "": (63, 311), "": (94, 311), "": (125, 311),"": (156, 311),"": (187, 311),"": (218, 311),
    # "": (249, 311),"": (280, 311),"": (311, 311),"": (342, 311),"": (373, 311),"": (404, 311),"": (435, 311),"": (466, 311),
    # "": (497, 311),"": (528, 311),"": (559, 311),"": (590, 311),"": (621, 311),"": (652, 311),"": (683, 311),"": (714, 311),
    #
    # "": (1, 342),  "": (32, 342), "": (63, 342), "": (94, 342), "": (125, 342),"": (156, 342),"": (187, 342),"": (218, 342),
    # "": (249, 342),"": (280, 342),"": (311, 342),"": (342, 342),"": (373, 342),"": (404, 342),"": (435, 342),"": (466, 342),
    # "": (497, 342),"": (528, 342),"": (559, 342),"": (590, 342),"": (621, 342),"": (652, 342),"": (683, 342),"": (714, 342),
}

upgrade_complete = { key : False for key in sprite_coord.keys() }