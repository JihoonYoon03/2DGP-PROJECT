from pico2d import *

import common
import game_framework
from physics_data import *
from state_machine import StateMachine

UI_BAR_RATIO = [2.0, 1.0, 1.0]  # 체력, 실드, 웨이브 바 비율

class ResData:
    def __init__(self, res_data):
        self.res_data = res_data

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        pass

    def draw(self):
        self.res_data.image.draw(self.res_data.x, self.res_data.y, self.res_data.w, self.res_data.h)
        self.res_data.font.draw(self.res_data.x - self.res_data.w * 0.36, self.res_data.y + self.res_data.h * 0.36, 'Resources', (255, 200, 0))
        list_y = self.res_data.list_y
        list_x = self.res_data.list_x
        count = 0
        for res, savings in self.res_data.res_amount.items():
            if savings == 0 and res != 0:
                continue
            self.res_data.res_image[res].draw(list_x, list_y,
                                              self.res_data.res_image[res].w * WIN_W_RATIO * 2.0,
                                              self.res_data.res_image[res].h * WIN_H_RATIO * 2.0)
            amount_text = f'{savings}'
            self.res_data.font.draw(list_x + 14, list_y, amount_text, (255, 200, 0))
            list_y -= self.res_data.dy
            count += 1
            if count == 5:
                list_x += self.res_data.dx
                list_y = self.res_data.list_y



class UIResourceData:
    def __init__(self):
        self.image = load_image('Assets/Sprites/UI/Window_GameInfo_ResourcesBackground.png')
        self.res_image = (
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
        self.font = load_font('Assets/Fonts/Fifaks10Dev1.ttf', int(24 * WIN_W_RATIO))
        self.w = self.image.w * WIN_W_RATIO * 1.8
        self.h = self.image.h * WIN_W_RATIO * 2.12
        self.x = WIN_WIDTH - self.w // 2 - 20 * WIN_W_RATIO
        self.y = WIN_HEIGHT - self.h // 2 - 62 * WIN_H_RATIO
        self.list_x = self.x - self.w * 0.3
        self.list_y = self.y + self.h * 0.2
        self.dx = self.w * 0.9 // 2
        self.dy = self.h * 0.9 // 9 + 6

        self.res_amount = {
            0 : 0,
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0,
            5 : 0,
            6 : 0,
            7 : 0,
            8 : 0
        }

        self.IDLE = ResData(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        pass

    def add_resources(self, res_input):
        for res, amount in res_input.items():
            if res in self.res_amount:
                self.res_amount[res] += amount


class UISpiderStatus():
    def __init__(self):
        self.image_back = load_image('Assets/Sprites/UI/Window_GameInfo_BarBackground.png')
        self.image_health = load_image('Assets/Sprites/UI/Window_GameInfo_Health_Bar.png')
        self.image_health_icon = load_image('Assets/Sprites/UI/Window_GameInfo_Health_Icon.png')
        self.image_shield = load_image('Assets/Sprites/UI/Window_GameInfo_Shield_Bar.png')
        self.image_shield_icon = load_image('Assets/Sprites/UI/Window_GameInfo_Shield_Icon.png')
        self.image_wave = load_image('Assets/Sprites/UI/Window_GameInfo_Daytime_Bar.png')
        self.image_wave_icon = load_image('Assets/Sprites/UI/Window_GameInfo_Daytime_Icon.png')
        # 바 최대 비율 계산
        self.base_bar_ratio = [SPIDER_MAX_HP / SPIDER_BASE_HP * UI_BAR_RATIO[0],
                            SPIDER_MAX_SHIELD / SPIDER_BASE_SHIELD * UI_BAR_RATIO[1],
                               WAVE_MAX_TIME / WAVE_BASE_TIME * UI_BAR_RATIO[2]]
        # 현재 바 비율
        self.cur_bar_ratio = [1.0, 1.0, 0.0]

        self.bar_width = int(WIN_WIDTH * 0.017)  # 바 너비
        self.bar_height = int(WIN_HEIGHT * 0.05)  # 바 높이
        self.offset = int(WIN_WIDTH * 0.006)  # 바 사이 간격

        self.x = int(WIN_WIDTH * 0.02)
        self.y = int(WIN_HEIGHT * 0.12)

    def update(self):
        # 안전장치
        if common.spider is None or common.wave_manager is None:
            return

        # 현재 바 비율 계산
        self.cur_bar_ratio[0] = common.spider.health / SPIDER_MAX_HP
        self.cur_bar_ratio[1] = common.spider.shield / SPIDER_MAX_SHIELD
        self.cur_bar_ratio[2] = common.wave_manager.wave_timer / WAVE_MAX_TIME

    def draw(self):
        for i in range(3):
            bar_x = self.x + i * (self.bar_width + self.offset)
            bar_y = self.y
            image_bar = None
            image_icon = None
            if i == 0:
                image_bar = self.image_health
                image_icon = self.image_health_icon
            elif i == 1:
                image_bar = self.image_shield
                image_icon = self.image_shield_icon
            elif i == 2:
                image_bar = self.image_wave
                image_icon = self.image_wave_icon

            self.image_back.draw_to_origin(bar_x, bar_y,
                                           self.bar_width,
                                           int(self.bar_height * self.base_bar_ratio[i]))
            if common.spider is None:
                continue

            # 상태 바
            image_bar.draw_to_origin(bar_x + (self.bar_width - int(self.bar_width - 4 * WIN_W_RATIO)) // 2,
                                     bar_y + (self.bar_height - int(self.bar_height - 4 * WIN_H_RATIO)) // 2,
                                     int(self.bar_width - 4 * WIN_W_RATIO),
                                     int(self.bar_height * self.base_bar_ratio[i] * self.cur_bar_ratio[i] - 4 * WIN_H_RATIO))

            # 아이콘
            image_icon.draw_to_origin(bar_x + int(self.bar_width - self.bar_width * 1.2) // 2,
                                      bar_y - int(self.bar_width * 1.2) + 5,
                                      int(self.bar_width * 1.2),
                                      int(self.bar_width * 1.2))

    def handle_event(self, event):
        pass