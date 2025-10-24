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
        if self.camera.lock_spider:
            self.camera.x = self.camera.spider.x
            self.camera.y = self.camera.spider.y

class camUp():
    def __init__(self, camera):
        self.camera = camera

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.camera.lock_spider:
            self.camera.x = self.camera.spider.x
            self.camera.y = self.camera.spider.y
        else:
            self.camera.y += self.camera.speed

class camDown():
    def __init__(self, camera):
        self.camera = camera

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.camera.lock_spider:
            self.camera.x = self.camera.spider.x
            self.camera.y = self.camera.spider.y
        else:
            self.camera.y -= self.camera.speed

class Camera:
    def __init__(self, x_width, y_height, spider):
        self.x = x_width // 2
        self.y = y_height // 2
        self.center_x = x_width // 2
        self.center_y = y_height // 2
        self.zoom = 1.0
        self.lock_spider = True
        self.spider = spider
        self.speed = spider.speed

        self.IDLE = camStop(self)
        self.UP = camUp(self)
        self.DOWN = camDown(self)
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