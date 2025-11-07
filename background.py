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
            if self.bg.y - self.bg.camera.world_y > self.bg.image.h / 2:
                self.bg.y = self.bg.y - self.bg.image.h
            elif self.bg.y - self.bg.camera.world_y < self.bg.image.h / -2:
                self.bg.y = self.bg.y + self.bg.image.h

    def draw(self, camera):
        # 중앙
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y + self.bg.image.h)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, self.bg.image.w * camera.zoom, self.bg.image.h * camera.zoom)

        # 상단
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, self.bg.image.w * camera.zoom, self.bg.image.h * camera.zoom)

        # 하단
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y - self.bg.image.h)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, self.bg.image.w * camera.zoom, self.bg.image.h * camera.zoom)

class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
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