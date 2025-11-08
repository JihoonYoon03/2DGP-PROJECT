from pico2d import *
from event_set import *
from game_world import get_camera
from state_machine import StateMachine

class Dock:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        self.player.is_docked = False
        return True

    def do(self):
        pass

    def draw(self):
        camera = get_camera()
        pass

class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        if self.player.move_x != 0 or self.player.move_y != 0:
            self.player.stateMachine.handle_state_event((signal_not_empty, None))

    def draw(self):
        camera = get_camera()

class Move:
    key_push_count = int()
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        # 키 입력 개수 확인용
        Move.key_push_count += 1
        pass

    def exit(self, e):
        return True

    def do(self):
        if self.player.move_x == 0 and self.player.move_y == 0:
            self.player.stateMachine.handle_state_event((signal_empty, None))

    def draw(self):
        camera = get_camera()

class Player:
    def __init__(self, robo_spider):
        self.image_dock = load_image('Assets/Sprites/Player/Attaching_Player_Docking.png')
        self.image_idle = load_image('Assets/Sprites/Player/Hero_Idle.png')
        self.image_move_right = load_image('Assets/Sprites/Player/Hero_Right_Moving.png')
        self.image_move_up = load_image('Assets/Sprites/Player/Hero_Up_Moving.png')
        self.image_move_down = load_image('Assets/Sprites/Player/Hero_Down_Moving.png')

        self.robo_spider = robo_spider
        self.is_docked = True   # 스파이더에 도킹 여부
        self.x = robo_spider.x
        self.y = robo_spider.y
        self.face_dir = 0 # 1: right, -1: left, 2: up, -2: down
        self.move_x = 0
        self.move_y = 0

        self.DOCKED = Dock(self)
        self.IDLE = Idle(self)
        self.MOVE = Move(self)

        self.stateMachine = StateMachine(
            self.DOCKED,
            {
                self.DOCKED: { e_pressed : self.IDLE },
                self.IDLE: { signal_not_empty : self.MOVE },
                self.MOVE: { signal_empty : self.IDLE },
            })


    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        # IDLE과 MOVE 상태 변환을 위해 Player가 직접 키 입력을 처리
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                self.move_x += 1
                self.face_dir += 1
            elif event.key == SDLK_LEFT:
                self.move_x -= 1
                self.face_dir -= 1
            elif event.key == SDLK_UP:
                self.move_y += 1
            elif event.key == SDLK_DOWN:
                self.move_y -= 1

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                self.move_x -= 1
                self.face_dir -= 1
            elif event.key == SDLK_LEFT:
                self.move_x += 1
                self.face_dir += 1
            elif event.key == SDLK_UP:
                self.move_y -= 1
            elif event.key == SDLK_DOWN:
                self.move_y += 1

        self.stateMachine.handle_state_event(('INPUT', event))