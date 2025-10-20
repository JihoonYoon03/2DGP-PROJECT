from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_w

from state_machine import StateMachine

SizeOffset = 0.4

def w_pressed(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def w_released(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def s_pressed(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def s_released(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

class SpIdle:
    def __init__(self, spider):
        self.spider = spider
        self.size = spider.size

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self, camera):
        self.spider.image.clip_draw(self.spider.frame * 178 % (11 * 178), self.spider.height - 440 - (self.spider.frame // 11 * 444), 178, 440,
                                    self.spider.x - camera.x, self.spider.y - camera.y, 178 * self.size, 440 * self.size)

class SpUp:
    def __init__(self, spider):
        self.spider = spider
        self.size = spider.size
        self.w = spider.image.w
        self.h = spider.image.h

    def enter(self, e):
        pass

    def exit(self, e):
        # 추가 구현 필요사항: 애니메이션이 끝나기 전엔 IDLE 상태로 넘어가면 안됨.
        pass

    def do(self):
        self.spider.frame = (self.spider.frame + 1) % 16
        self.spider.y += 5 * self.size

    def draw(self, camera):
        self.spider.image.clip_draw(self.spider.frame * 178 % (11 * 178), self.spider.height - 440 - (self.spider.frame // 11 * 444), 178, 440,
                                    self.spider.x - camera.x, self.spider.y - camera.y, 178 * self.size, 440 * self.size)

class SpDown:
    def __init__(self, spider):
        self.spider = spider
        self.size = spider.size
        self.w = spider.image.w
        self.h = spider.image.h

    def enter(self, e):
        pass

    def exit(self, e):
        # 추가 구현 필요사항: 애니메이션이 끝나기 전엔 IDLE 상태로 넘어가면 안됨.
        pass

    def do(self):
        self.spider.frame = self.spider.frame - 1 if self.spider.frame > 0 else 15
        self.spider.y -= 5 * self.size

    def draw(self, camera):
        self.spider.image.clip_draw(self.spider.frame * 178 % (11 * 178), self.spider.height - 440 - (self.spider.frame // 11 * 444), 178, 440,
                                    self.spider.x - camera.x, self.spider.y - camera.y, 178 * self.size, 440 * self.size)

class RoboSpider:
    def __init__(self):
        global SizeOffset
        self.size = SizeOffset
        self.x = 400
        self.y = 300
        self.frame = 0
        self.image = load_image('Assets/Sprites/Spider/Spider_Moving.png')
        self.width = self.image.w
        self.height = self.image.h

        self.IDLE = SpIdle(self)
        self.UP = SpUp(self)
        self.DOWN = SpDown(self)
        self.stateMachine = StateMachine(
            self.IDLE,
        {
            self.IDLE : { w_pressed : self.UP, s_pressed : self.DOWN },
            self.UP : { w_released : self.IDLE, s_pressed : self.DOWN },
            self.DOWN : { s_released : self.IDLE, w_pressed : self.UP }
        })

    def update(self):
        self.stateMachine.update()

    def draw(self, camera):
        self.stateMachine.draw(camera)

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))