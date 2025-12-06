from pico2d import *

import UI_play_scene
import common
import event_set
import game_framework
import play_scene
from physics_data import *

name, comment = '', ''

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
        self.font_size_title = int(24 * WIN_W_RATIO)
        self.font_size_name = int(16 * WIN_W_RATIO * 2.2)
        self.font_size_comment = int(12 * WIN_W_RATIO * 2.2)
        self.image_anim = load_image('Assets/Sprites/UI/Open_Window_Talent_Animation.png')
        self.image_const = load_image('Assets/Sprites/UI/Window_Talent_Frame.png')
        self.image_back = load_image('Assets/Sprites/UI/Window_Talent_Background.png')
        self.font_discription = load_font('Assets/Fonts/NeoDunggeunmoPro-Regular.ttf', self.font_size_name)
        self.font = load_font('Assets/Fonts/NeoDunggeunmoPro-Regular.ttf', self.font_size_title)

        self.sound_open = load_wav('Assets/Audios/UI/UI OPEN.wav')
        self.sound_open.set_volume(64)
        self.sound_show = load_wav('Assets/Audios/UI/UI SHOW.wav')
        self.sound_show.set_volume(64)


        self.frame = 0
        self.frame_dir = 1
        self.frame_len = 11
        self.frame_speed = 20  # frames per second
        self.w = 1104
        self.h = 620
        self.w_ratio = WIN_WIDTH / self.w
        self.h_ratio = WIN_HEIGHT / self.h
        self.show = False

        frame_width = self.w * 0.8 * self.w_ratio
        frame_left = WIN_WIDTH // 2 - frame_width // 2 * 1.05
        frame_height = self.h * 0.8 * self.h_ratio
        frame_top = WIN_HEIGHT // 2 + frame_height // 2 * 1.1
        y = frame_top - frame_height * 0.2
        self.upgrade_menu = [
            UpgradeType(
                int(frame_left + frame_width * 1 / 6), y, frame_width * 0.25, '머신건',
                layout_keys={
                    0: ['베어링 향상 (1)', '베어링 향상 (2)', '베어링 향상 (3)'],
                    1: ['머신건 벨트 (1)', '머신건 벨트 (2)', '머신건 벨트 (3)'],
                    2: ['확장탄 (1)', '확장탄 (2)', '확장탄 (3)'],
                }
            ),
            UpgradeType(
                int(frame_left + frame_width * 3 / 6), y, frame_width * 0.25, '엑소슈트',
                layout_keys={
                    0: ['플라즈마 커터 (1)', '플라즈마 커터 (2)', '플라즈마 커터 (3)'],
                    1: ['리펄서 (1)', '리펄서 (2)', '리펄서 (3)'],
                }
            ),
            UpgradeType(
                int(frame_left + frame_width * 5 / 6), y, frame_width * 0.25, '로보스파이더',
                layout_keys={
                    1: ['수리'],
                    2: ['효과적인 수리 (1)', '효과적인 수리 (2)', '효과적인 수리 (3)'],
                }
            ),
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
            if not self.show:
                self.sound_show.play()
                self.show = True
        elif self.frame < 0:
            self.frame = 0
            self.show = False
            game_framework.pop_scene()

    def draw(self):
        if self.frame < self.frame_len:
            x, y = self.sprite_coord[int(self.frame)]
            self.image_anim.clip_draw(x, self.image_anim.h - self.h - y, self.w, self.h,
                                      WIN_WIDTH // 2, WIN_HEIGHT // 2,
                                      self.w * self.w_ratio, self.h * self.h_ratio)
        else:
            global name, comment
            self.image_back.draw(WIN_WIDTH // 2, WIN_HEIGHT // 2, self.w * self.w_ratio, self.h * self.h_ratio)
            self.font.draw(WIN_WIDTH // 2 - len('업그레이드') * self.font_size_title, WIN_HEIGHT // 2 + self.h // 2 * 0.9, '업그레이드', (255, 200, 0))
            for upgrade in self.upgrade_menu:
                upgrade.draw()
            self.image_const.draw(WIN_WIDTH // 2, WIN_HEIGHT // 2, self.w * self.w_ratio, self.h * self.h_ratio)

            self.font_discription.draw(WIN_WIDTH * 0.42, WIN_HEIGHT * 0.12, name, (255, 200, 0))
            self.font_discription.draw(WIN_WIDTH * 0.42, WIN_HEIGHT * 0.08, comment, (255, 255, 0))

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

    def __init__(self, x, y, back_w, image_path, layout_keys=None):
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
        self.row = len(max(layout_keys.values(), key=lambda lst: len(lst), default=0)) + 1
        self.layout_keys = layout_keys or {}
        self.icon_clip_x = UpgradeType.sprite_coord[image_path][0]
        self.icon_clip_y = UpgradeType.sprite_coord[image_path][1]
        self.offset = 1.5
        self.branch_back_w = back_w
        self.branch_back_h = 44

        # 버튼 배치 (layout_keys 우선 사용)
        self.upgrade_icon_list = []
        if self.layout_keys:
            for col, keys in self.layout_keys.items():
                for r, key in enumerate(keys):
                    if key in upgrade_info:
                        button_x = self.x - self.branch_back_w // 2 + 66 * WIN_W_RATIO + (self.branch_back_w // 3 * col)
                        button_y = self.branch_y - 120 * WIN_H_RATIO - 80 * r
                        self.upgrade_icon_list.append(UpgradeButton(button_x, button_y, key))

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
        row = self.row * 80 // 44
        for i in range(row):
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
    image_cost = None
    image_selector = None
    font = None
    font_size_cost = int(10 * WIN_W_RATIO * 2.2)
    sound_select = None
    sound_bought = None
    sound_cannot = None
    def __init__(self, x, y, upgrade_name, parent=None):
        if UpgradeButton.image_icon is None:
            UpgradeButton.image_icon = load_image('Assets/Sprites/UI/TalentIcons.png')
        if UpgradeButton.image_selling is None:
            UpgradeButton.image_selling = load_image('Assets/Sprites/UI/Window_Talent_TierPlate_Background.png')
        if UpgradeButton.image_bought is None:
            UpgradeButton.image_bought = load_image('Assets/Sprites/UI/Window_Talent_TierPlate_Bought.png')
        if UpgradeButton.font is None:
            UpgradeButton.font = load_font('Assets/Fonts/ARIAL.ttf', self.font_size_cost)
        if UpgradeButton.image_cost is None:
            UpgradeButton.image_cost = (
                load_image('Assets/Sprites/UI/CommonResource_Icon.png'),
                load_image('Assets/Sprites/UI/RareRes1_Icon.png'),
                load_image('Assets/Sprites/UI/RareRes2_Icon.png'),
                load_image('Assets/Sprites/UI/RareRes3_Icon.png'),
                load_image('Assets/Sprites/UI/RareRes4_Icon.png'),
                load_image('Assets/Sprites/UI/RareRes5_Icon.png'),
                load_image('Assets/Sprites/UI/RareRes6_Icon.png'),
                load_image('Assets/Sprites/UI/RareRes7_Icon.png'),
                load_image('Assets/Sprites/UI/RareRes8_Icon.png'),
            )
        if UpgradeButton.image_selector is None:
            UpgradeButton.image_selector = load_image('Assets/Sprites/UI/Window_Talent_TierPlate_Selected.png')
        if UpgradeButton.sound_select is None:
            UpgradeButton.sound_select = load_wav('Assets/Audios/UI/UI_Button_Click.wav')
            UpgradeButton.sound_select.set_volume(64)
        if UpgradeButton.sound_bought is None:
            UpgradeButton.sound_bought = load_wav('Assets/Audios/UI/buy 2.wav')
            UpgradeButton.sound_bought.set_volume(64)
        if UpgradeButton.sound_cannot is None:
            UpgradeButton.sound_cannot = load_wav('Assets/Audios/UI/UI_Button_Click_Unavailible.wav')
            UpgradeButton.sound_cannot.set_volume(64)

        self.x = x
        self.y = y
        self.upgrade_name = upgrade_name
        self.icon_x = upgrade_info[upgrade_name]['coord'][0]
        self.icon_y = upgrade_info[upgrade_name]['coord'][1]
        self.icon_w = 30
        self.icon_h = 30
        self.parent = parent
        self.offset = 1.5
        self.offset_cost = 2.2
        self.selected = False
        self.name = upgrade_name
        self.comment = upgrade_info[upgrade_name]['comment']
        self.button = MenuBar(self.x, self.y)

    def draw(self):
        if upgrade_complete[self.upgrade_name]:
            clip_draw_frame(self.image_bought,
                            0, 0, self.image_bought.w, self.image_bought.h,
                            self.x, self.y,
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
                        self.x , self.y + self.icon_h * 0.42,
                        self.icon_w * WIN_W_RATIO * self.offset,
                        self.icon_h * WIN_H_RATIO * self.offset
                        )

        if upgrade_complete[self.upgrade_name]:
            return

        i = 0
        red = (255, 100, 100)
        orange = (255, 200, 0)
        for res_type, cost in upgrade_info[self.upgrade_name]['cost'].items():
            clip_draw_frame(self.image_cost[res_type],
                        0, 0,
                        self.image_cost[res_type].w, self.image_cost[res_type].h,
                        self.x - self.icon_w * WIN_W_RATIO + self.icon_w * i, self.y - self.icon_h * WIN_H_RATIO * 0.8,
                        self.image_cost[res_type].w * WIN_W_RATIO * self.offset_cost,
                        self.image_cost[res_type].h * WIN_H_RATIO * self.offset_cost
                        )
            if common.UI_ResourceData.res_amount[res_type] < cost:
                color = red
            else:
                color = orange
            self.font.draw(self.x - self.icon_w * WIN_W_RATIO + self.icon_w * i, self.y - self.icon_h * WIN_H_RATIO * 0.8, f' {cost}', color)
            i += 1
        if self.selected:
            clip_draw_frame(self.image_selector,
                            0, 0, self.image_selector.w, self.image_selector.h,
                            self.x, self.y,
                            self.image_selector.w * WIN_W_RATIO * self.offset,
                            self.image_selector.h * WIN_H_RATIO * self.offset)
            self.button.draw()


    def handle_click(self):
        # 마우스 좌표 체크 후 선택 상태로 변경
        if upgrade_complete[self.upgrade_name]:
            return
        if (self.x - self.image_selling.w / 2 * WIN_W_RATIO <= common.mouse_x <= self.x + self.image_selling.w / 2 * WIN_W_RATIO and
            self.y - self.image_selling.h / 2 * WIN_H_RATIO <= common.mouse_y <= self.y + self.image_selling.h / 2 * WIN_H_RATIO):

            if self.selected:
                # 자원 체크
                for res_type, cost in upgrade_info[self.upgrade_name]['cost'].items():
                    if common.UI_ResourceData.res_amount[res_type] < cost:
                        UpgradeButton.sound_cannot.play()
                        return

                upgrade_amount, upgrade_type = upgrade_info[self.upgrade_name]['value']
                if self.upgrade_name == '수리' and common.spider.health == SPIDER_MAX_HP:
                    UpgradeButton.sound_cannot.play()
                    return

                # 자원 차감
                for res_type, cost in upgrade_info[self.upgrade_name]['cost'].items():
                    common.UI_ResourceData.res_amount[res_type] -= cost

                # 업그레이드 적용
                self.apply_upgrade(upgrade_amount)
                if self.upgrade_name == '수리':
                    UpgradeButton.sound_bought.play()
                    return
                upgrade_complete[self.upgrade_name] = True
                UpgradeButton.sound_bought.play()

            else:
                global name, comment
                name = self.name
                comment = self.comment
                self.selected = True
                UpgradeButton.sound_select.play()
        else:
            self.selected = False

    def apply_upgrade(self, upgrade_amount):
        if self.upgrade_name == '수리':
            common.spider.health += upgrade_amount
            if common.spider.health > SPIDER_MAX_HP:
                common.spider.health = SPIDER_MAX_HP
            return

        apply_upgrade_stats(upgrade_info[self.upgrade_name]['value'])


class MenuBar:
    def __init__(self, x, y):
        self.image_select = load_image('Assets/Sprites/UI/button_select.png')
        self.font_size = int(20 * WIN_W_RATIO)
        self.font = load_font('Assets/Fonts/NeoDunggeunmoPro-Regular.ttf', self.font_size)
        self.x = x
        self.y = y
        self.w = self.image_select.w
        self.h = self.image_select.h
        self.mouse_hovering = False

    def update(self):
        pass

    def draw(self):
        self.image_select.draw(self.x, self.y, self.w * WIN_W_RATIO, self.h * WIN_H_RATIO)
        self.font.draw(self.x - len('구매') * self.font_size / 2, self.y, '구매', (0, 0, 0))

def init():
    global frame
    frame = UIFrame()
    frame.sound_open.play()

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
            frame.sound_open.play()
            frame.exit()
        elif event.type == SDL_MOUSEBUTTONUP:
            for upgrade in frame.upgrade_menu:
                for button in upgrade.upgrade_icon_list:
                    button.handle_click()


def update():
    global frame
    frame.update()
    common.UI_SpiderStatus.update()

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


upgrade_info = {
    "베어링 향상 (1)": {'coord': (0, 0),   'cost': {0: 4},         'value': (0.3, 'UPGRADE_TURRET_ROTATE_SPEED'), 'comment' : '총기 회전 속도 +30%'},
    "베어링 향상 (2)": {'coord': (32, 0),  'cost': {0: 8},         'value': (0.2, 'UPGRADE_TURRET_ROTATE_SPEED'), 'comment' : '총기 회전 속도 +20%'},
    "베어링 향상 (3)": {'coord': (64, 0),  'cost': {0: 25, 2: 2},  'value': (0.2, 'UPGRADE_TURRET_ROTATE_SPEED'), 'comment' : '총기 회전 속도 +20%'},

    "머신건 벨트 (1)": {'coord': (96, 0),  'cost': {0: 6},         'value': (-0.25, 'UPGRADE_GUN_FIRE_RATE'), 'comment' : '머신건 발사 속도 +25%'},
    "머신건 벨트 (2)": {'coord': (128, 0), 'cost': {0: 14},        'value': (-0.15, 'UPGRADE_GUN_FIRE_RATE'), 'comment' : '머신건 발사 속도 +15%'},
    "머신건 벨트 (3)": {'coord': (160, 0), 'cost': {0: 18, 2: 2},  'value': (-0.1, 'UPGRADE_GUN_FIRE_RATE'), 'comment' : '머신건 발사 속도 +10%'},

    "확장탄 (1)":     {'coord': (192, 0), 'cost': {0: 8, 1: 2},   'value': (0.35, 'UPGRADE_GUN_BULLET_DAMAGE_PERCENT'), 'comment' : '총탄당 피해 +35%'},
    "확장탄 (2)":     {'coord': (224, 0), 'cost': {0: 12, 1: 6},  'value': (30, 'UPGRADE_GUN_BULLET_DAMAGE'), 'comment' : '총탄당 피해 +30'},
    "확장탄 (3)":     {'coord': (256, 0), 'cost': {0: 40, 2: 4},  'value': (0.25, 'UPGRADE_GUN_BULLET_DAMAGE_PERCENT'), 'comment' : '총탄당 피해 +25%'},

    # "확장 구경 (1)":  {'coord': (288, 0), 'cost': {0: 4},                     'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',
    # "확장 구경 (2)":  {'coord': (320, 0), 'cost': {0: 4, 1: 8},               'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',
    # "확장 구경 (3)":  {'coord': (352, 0), 'cost': {0: 4, 1: 8, 2: 12},        'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',

    # "철갑탄 (1)":     {'coord': (384, 0), 'cost': {0: 4},                     'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',
    # "철갑탄 (2)":     {'coord': (416, 0), 'cost': {0: 4, 1: 8},               'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',

    "컴펜세이터 (1)": {'coord': (448, 0), 'cost': {0: 4},         'value': (-0.4, 'UPGRADE_GUN_SPREAD'), 'comment' : '총탄 분산 -40%'},
    "컴펜세이터 (2)": {'coord': (480, 0), 'cost': {0: 4, 1: 8},   'value': (-0.45, 'UPGRADE_GUN_SPREAD'), 'comment' : '총탄 분산 -45%'},

    "리펄서 (1)":     {'coord': (64, 160),'cost': {0: 8},        'value': (0.2, 'UPGRADE_MINE_RUN_SPEED'), 'comment' : '엑소슈트 속도 +20%'},
    "리펄서 (2)":     {'coord': (96, 160),'cost': {0: 12},       'value': (0.25, 'UPGRADE_MINE_RUN_SPEED'), 'comment' : '엑소슈트 속도 +25%'},
    "리펄서 (3)":     {'coord': (128,160),'cost': {0: 20, 2: 6}, 'value': (0.3, 'UPGRADE_MINE_RUN_SPEED'), 'comment' : '엑소슈트 속도 +30%'},

    # "플라즈마 안정성 (1)": {'coord': (160,160),'cost': {0: 4},                 'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',
    # "플라즈마 안정성 (2)": {'coord': (192,160),'cost': {0: 4, 1: 8},           'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',

    "플라즈마 커터 (1)": {'coord': (224,160),'cost': {0: 6},       'value': (25, 'UPGRADE_LASER_DAMAGE'), 'comment' : '시추 효율 +25'},
    "플라즈마 커터 (2)": {'coord': (256,160),'cost': {0: 16, 1: 4},'value': (0.15, 'UPGRADE_LASER_DAMAGE_PERCENT'), 'comment' : '시추 효율 +25%'},
    "플라즈마 커터 (3)": {'coord': (288,160),'cost': {0: 25, 2: 4},'value': (25, 'UPGRADE_LASER_DAMAGE'), 'comment' : '시추 효율 +25'},
    # "플라즈마 커터 (4)": {'coord': (320,160),'cost': {0: 4, 1: 8, 2: 12, 3: 16}, 'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',
    # "플라즈마 커터 (5)": {'coord': (352,160),'cost': {0: 4, 1: 8, 2: 12, 3: 16, 4: 20}, 'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',
    # "플라즈마 커터 (6)": {'coord': (384,160),'cost': {0: 4, 1: 8, 2: 12, 3: 16, 4: 20, 5: 24}, 'value': (0.3, UPGRADE_TURRET_ROTATE_SPEED)}, 'comment' : '총기 회전 속도 +30%',

    "수리":            {'coord': (640,160),'cost': {2: 3},        'value': (SPIDER_MAX_HP * 0.15 * UPGRADE_REPAIR_EFFICIENCY, None), 'comment' : "체력 15% 회복. 무제한 사용이 가능합니다"},

    "효과적인 수리 (1)": {'coord': (0, 192), 'cost': {0: 20, 1: 5},       'value': (0.05, 'UPGRADE_REPAIR_EFFICIENCY'), 'comment' : "모든 유형의 수리 효율 +5%. 영구 적용됩니다"},
    "효과적인 수리 (2)": {'coord': (32,192), 'cost': {0: 20, 1: 10},      'value': (0.05, 'UPGRADE_REPAIR_EFFICIENCY'), 'comment' : "모든 유형의 수리 효율 +5%. 영구 적용됩니다"},
    "효과적인 수리 (3)": {'coord': (64,192), 'cost': {0: 20, 2: 8},       'value': (0.05, 'UPGRADE_REPAIR_EFFICIENCY'), 'comment' : "모든 유형의 수리 효율 +5%. 영구 적용됩니다"},
}

upgrade_complete = { key : False for key in upgrade_info.keys() }