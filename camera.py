from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_w
from state_machine import StateMachine

def w_pressed(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w

def w_released(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w

def s_pressed(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s

def s_released(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s

class camStop():
    def __init__(self, camera):
        self.camera = camera

    def enter(self, e):
        pass

    def do(self):
        pass

class camUp():
    def __init__(self, camera, amount):
        self.camera = camera
        self.amount = amount

    def enter(self, e):
        pass

    def do(self):
        self.camera.y += self.amount

class camDown():
    def __init__(self, camera, amount):
        self.camera = camera
        self.amount = amount

    def enter(self, e):
        pass

    def do(self):
        self.camera.y -= self.amount

class Camera:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.zoom = 1.0

        self.IDLE = camStop(self)
        self.UP = camUp(self, 5)
        self.DOWN = camDown(self, 5)
        self.stateMachine = StateMachine(self.IDLE,
        {
            self.IDLE : { w_pressed : self.UP, s_pressed : self.DOWN },
            self.UP : { w_released : self.IDLE, s_pressed : self.DOWN },
            self.DOWN : { s_released : self.IDLE, w_pressed: self.UP }
        })