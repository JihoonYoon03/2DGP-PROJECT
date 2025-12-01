from pico2d import *
from physics_data import *
from state_machine import StateMachine

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
        self.res_data.image.clip_composite_draw(0, 0, self.res_data.image.w, self.res_data.image.h,
                                                 0, '', self.res_data.x, self.res_data.y,
                                                self.res_data.w, self.res_data.h)
        self.res_data.font.draw(self.res_data.x - self.res_data.w * 0.32, self.res_data.y + self.res_data.h * 0.35, 'Resources', (255, 200, 0))
        list_y = self.res_data.list_y
        list_x = self.res_data.list_x
        count = 0
        for res, savings in self.res_data.res_amount.items():
            if savings == 0 and res != 0:
                continue
            self.res_data.res_image[res].clip_composite_draw(0, 0, self.res_data.res_image[res].w,
                                                              self.res_data.res_image[res].h,
                                                              0, '', list_x, list_y,
                                                             self.res_data.res_image[res].w * self.res_data.ratio,
                                                             self.res_data.res_image[res].h * self.res_data.ratio)
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
        self.ratio = (WIN_WIDTH / WIN_HEIGHT) / (1920 / 1080) * 1.5
        self.font = load_font('Assets/Fonts/ARIAL.ttf', int(11 * self.ratio))
        self.w = self.image.w * self.ratio
        self.h = self.image.h * self.ratio
        self.x = WIN_WIDTH - self.w // 2 - 10
        self.y = WIN_HEIGHT - self.h // 2 - 10
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
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass