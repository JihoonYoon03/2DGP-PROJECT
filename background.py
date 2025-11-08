from pico2d import *
from state_machine import StateMachine
from game_world import get_camera

class Idle:
    def __init__(self, bg):
        self.bg = bg

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        camera = get_camera()
        if self.bg.y - camera.world_y > self.bg.image.h / 2:
            self.bg.y = self.bg.y - self.bg.image.h
        elif self.bg.y - camera.world_y < self.bg.image.h / -2:
            self.bg.y = self.bg.y + self.bg.image.h

    def draw(self):
        camera = get_camera()
        draw_w, draw_h = camera.get_draw_size(self.bg.image.w, self.bg.image.h)

        # 중앙
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y + self.bg.image.h)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, draw_w, draw_h)

        # 상단
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, draw_w, draw_h)

        # 하단
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y - self.bg.image.h)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, draw_w, draw_h)


class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = load_image('Assets/Sprites/Background/NightBackground.png')

        self.IDLE = Idle(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        pass