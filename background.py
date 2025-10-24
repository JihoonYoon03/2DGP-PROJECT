from pico2d import *
from state_machine import StateMachine

class Idle:
    def __init__(self, background):
        self.background = background

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.background.camera is not None:
            if self.background.y - self.background.camera.y > 300:
                self.background.y = self.background.y - 600
            elif self.background.y - self.background.camera.y < -300:
                self.background.y = self.background.y + 600

    def draw(self, camera):
        # 중앙
        self.background.image.clip_draw(0, 0, self.background.image.w, self.background.image.h,
                                        self.background.x - camera.x, self.background.y - camera.y, 800, 600)

        # 상단
        self.background.image.clip_draw(0, 0, self.background.image.w, self.background.image.h,
                                        self.background.x - camera.x, self.background.y + 600 - camera.y, 800, 600)

        # 하단
        self.background.image.clip_draw(0, 0, self.background.image.w, self.background.image.h,
                                        self.background.x - camera.x, self.background.y - 600 - camera.y, 800, 600)

class Background:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.camera = None
        self.image = load_image('Assets/Sprites/Background/NightBackground.png')

        self.IDLE = Idle(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self, camera):
        self.camera = camera
        self.stateMachine.draw(camera)

    def handle_event(self, event):
        pass