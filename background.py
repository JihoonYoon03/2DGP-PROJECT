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
        pass

    def draw(self, camera = None):
        self.background.image.clip_draw(0, 0, self.background.image.w, self.background.image.h,
                                        self.background.x, self.background.y, 800, 600)

class Background:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.image = load_image('Assets/Sprites/Background/NightBackground.png')

        self.IDLE = Idle(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self, camera):
        self.stateMachine.draw(None)