from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_w, SDLK_s
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

    def exit(self, e):
        pass

    def do(self):
        pass

class camUp():
    def __init__(self, camera, amount):
        self.camera = camera
        self.amount = amount

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.camera.y += self.amount

class camDown():
    def __init__(self, camera, amount):
        self.camera = camera
        self.amount = amount

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.camera.y -= self.amount

class Camera:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.zoom = 1.0

        self.IDLE = camStop(self)
        self.UP = camUp(self, speed)
        self.DOWN = camDown(self, speed)
        self.stateMachine = StateMachine(self.IDLE,
        {
            self.IDLE : { w_pressed : self.UP, s_pressed : self.DOWN },
            self.UP : { w_released : self.IDLE, s_pressed : self.DOWN },
            self.DOWN : { s_released : self.IDLE, w_pressed: self.UP }
        })

    def update(self):
        self.stateMachine.update()

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))