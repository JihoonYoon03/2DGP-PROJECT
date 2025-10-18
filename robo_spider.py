from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

from state_machine import StateMachine

class Idle:
    def __init__(self, spider):
        self.spider = spider

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        self.spider.image.clip_draw(self.spider.frame * 178 % (11 * 178), self.spider.height - 440 - (self.spider.frame // 11 * 444), 178, 440, self.spider.x, self.spider.y)

class RoboSpider:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.image = load_image('Assets/Sprites/Spider/Spider_Moving.png')
        self.width = self.image.w
        self.height = self.image.h

        self.IDLE = Idle(self)
        self.stateMachine = StateMachine(
            self.IDLE,
        {
            self.IDLE : {}
        })

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()