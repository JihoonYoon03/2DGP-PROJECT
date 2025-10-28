from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_w, SDLK_s

from state_machine import StateMachine

SizeOffset = 1.0

def w_pressed(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def w_released(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def s_pressed(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def s_released(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

class SpIdle:
    def __init__(self, sp):
        self.sp = sp
        self.size = sp.size
        self.h = sp.image.h

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.sp.is_moving:
            self.sp.frame = self.sp.frame + self.sp.move_dir
            if self.sp.frame <= 0 or self.sp.frame >= 16:
                self.sp.is_moving = False
                self.sp.frame = 0
                self.sp.move_dir = 0
                return
            self.sp.y += self.sp.speed * self.sp.move_dir

    def draw(self, camera):
        self.sp.image.clip_draw(self.sp.frame * 178 % (11 * 178), self.h - 440 - (self.sp.frame // 11 * 444), 178, 440,
                                    self.sp.x - camera.x + camera.center_x, self.sp.y - camera.y + camera.center_y, 178 * self.size, 440 * self.size)

class SpUp:
    def __init__(self, sp):
        self.sp = sp
        self.size = sp.size
        self.h = sp.image.h

    def enter(self, e):
        self.sp.is_moving = True
        self.sp.move_dir = 1

    def exit(self, e):
        pass

    def do(self):
        self.sp.frame = (self.sp.frame + 1) % 16
        self.sp.y += self.sp.speed * self.sp.move_dir

    def draw(self, camera):
        self.sp.image.clip_draw(self.sp.frame * 178 % (11 * 178), self.h - 440 - (self.sp.frame // 11 * 444), 178, 440,
                                    self.sp.x - camera.x + camera.center_x, self.sp.y - camera.y + camera.center_y, 178 * self.size, 440 * self.size)

class SpDown:
    def __init__(self, sp):
        self.sp = sp
        self.size = sp.size
        self.h = sp.image.h

    def enter(self, e):
        self.sp.is_moving = True
        self.sp.move_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.sp.frame = self.sp.frame - 1 if self.sp.frame > 0 else 15
        self.sp.y += self.sp.speed * self.sp.move_dir

    def draw(self, camera):
        self.sp.image.clip_draw(self.sp.frame * 178 % (11 * 178), self.h - 440 - (self.sp.frame // 11 * 444), 178, 440,
                                    self.sp.x - camera.x + camera.center_x, self.sp.y - camera.y + camera.center_y, 178 * self.size, 440 * self.size)

class RoboSpider:
    def __init__(self, x = 800, y = 300):
        global SizeOffset
        self.size = SizeOffset
        self.x = x
        self.y = y
        self.speed = 5 * self.size
        self.is_moving = False
        self.move_dir = 0
        self.frame = 0
        self.image = load_image('Assets/Sprites/Spider/Spider_Moving.png')
        self.w = 178 * self.size
        self.h = 440 * self.size
        self.x -= 178 * self.size // 2

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