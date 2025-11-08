from pico2d import *
from event_set import *
from game_world import get_camera
from state_machine import StateMachine

class Docked:
    def __init__(self, sp):
        self.sp = sp

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        pass

    def draw(self):
        camera = get_camera()
        pass

class Idle:
    def __init__(self, sp):
        self.sp = sp

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        pass

    def draw(self):
        camera = get_camera()
        pass

class Move:
    def __init__(self, sp):
        self.sp = sp

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        pass

    def draw(self):
        camera = get_camera()
        pass

class Player:
    def __init__(self, robo_spider):
        self.image_idle = load_image('Assets/Sprites/Player/Hero_Idle.png')
        self.image_move_right = load_image('Assets/Sprites/Player/Hero_Right_Moving.png')
        self.image_move_up = load_image('Assets/Sprites/Player/Hero_Up_Moving.png')
        self.image_move_down = load_image('Assets/Sprites/Player/Hero_Down_Moving.png')

        self.is_docked = True   # 스파이더에 도킹 여부
        self.x = robo_spider.x
        self.y = robo_spider.y
        self.face_dir = 0 # 1: right, -1: left, 2: up, -2: down
        self.move_x = 0
        self.move_y = 0

        self.DOCKED = Docked(self)
        self.IDLE = Idle(self)
        self.MOVE = Move(self)

        self.stateMachine = StateMachine(
            self.DOCKED,
            {
                self.DOCKED: { e_pressed : self.IDLE },
                self.IDLE: { w_pressed : self.MOVE, a_pressed : self.MOVE, s_pressed : self.MOVE, d_pressed : self.MOVE },
                self.MOVE: { w_released : self.MOVE, a_released : self.MOVE, s_released : self.MOVE, d_released : self.MOVE,
                             no_key_pressed : self.IDLE }
            })

        self.robo_spider = robo_spider

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass