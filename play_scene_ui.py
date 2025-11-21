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



class UIResourceData:
    def __init__(self):
        self.image = load_image('Assets/Sprites/UI/Window_GameInfo_ResourcesBackground.png')
        self.font = load_font('Assets/Fonts/Fifaks10Dev1.ttf', 20)
        self.x = WIN_WIDTH - self.image.w // 2
        self.y = WIN_HEIGHT - self.image.h // 2
        self.w = self.image.w * WIN_WIDTH / 1920
        self.h = self.image.h * WIN_HEIGHT / 1080

        self.res_amount = [0, 0, 0, 0, 0, 0, 0, 0]  # 자원 개수 저장 리스트

        self.IDLE = ResData(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        pass

    def set_resource_amount(self, index, amount):
        pass