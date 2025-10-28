from pico2d import *
from state_machine import StateMachine

class Idle:
    def __init__(self, bg):
        self.bg = bg

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.bg.camera is not None:
            if self.bg.y - self.bg.camera.world_y > 300:
                self.bg.y = self.bg.y - 600
            elif self.bg.y - self.bg.camera.world_y < -300:
                self.bg.y = self.bg.y + 600

    def draw(self, camera):
        # 중앙
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h,
                                        self.bg.x - camera.world_x + camera.view_x, self.bg.y + self.bg.image.h - camera.world_y + camera.view_y)

        # 상단
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h,
                                        self.bg.x - camera.world_x + camera.view_x, self.bg.y - camera.world_y + camera.view_y)

        # 하단
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h,
                                        self.bg.x - camera.world_x + camera.view_x, self.bg.y - self.bg.image.h  - camera.world_y + camera.view_y)

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