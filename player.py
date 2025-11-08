from pico2d import *
from event_set import *
from game_world import get_camera
from state_machine import StateMachine

PLAYER_DOCK_FRAMES = (
    (0, 0, 40, 40),      # 프레임 0
    (40, 0, 40, 40),     # 프레임 1
    (80, 0, 40, 40),     # 프레임 2
    (120, 0, 40, 40),    # 프레임 3
    (160, 0, 40, 40),    # 프레임 4
    (200, 0, 40, 40),    # 프레임 5
    (0, 40, 40, 40),     # 프레임 6
    (40, 40, 40, 40),    # 프레임 7
    (80, 40, 40, 40),    # 프레임 8
    (120, 40, 40, 40),   # 프레임 9
    (160, 40, 40, 40),   # 프레임 10
    (200, 40, 40, 40),   # 프레임 11
    (0, 80, 40, 40),     # 프레임 12
)

PLAYER_IDLE_FRAMES = (
    (0, 0, 40, 40),      # 프레임 0
    (40, 0, 40, 40),     # 프레임 1
    (80, 0, 40, 40),     # 프레임 2
    (120, 0, 40, 40),    # 프레임 3
    (160, 0, 40, 40),    # 프레임 4
    (200, 0, 40, 40),    # 프레임 5
    (0, 40, 40, 40),     # 프레임 6
    (40, 40, 40, 40),    # 프레임 7
    (80, 40, 40, 40),    # 프레임 8
    (120, 40, 40, 40),   # 프레임 9
    (160, 40, 40, 40),   # 프레임 10
    (200, 40, 40, 40),   # 프레임 11
    (0, 80, 40, 40),     # 프레임 12
    (40, 80, 40, 40),    # 프레임 13
    (80, 80, 40, 40),    # 프레임 14
    (120, 80, 40, 40)    # 프레임 15
)

PLAYER_MOVE_FRAMES = (
    (0, 0, 40, 40),      # 프레임 0
    (40, 0, 40, 40),     # 프레임 1
    (80, 0, 40, 40)     # 프레임 2
)

class Dock:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if e[0] == 'START':
            self.player.is_docked = True
            self.player.frame = 12

    def exit(self, e):
        return True

    def do(self):
        pass

    def draw(self):
        camera = get_camera()
        x, y, w, h = PLAYER_DOCK_FRAMES[self.player.frame]
        view_x, view_y = camera.world_to_view(self.player.x, self.player.y)
        draw_w, draw_h = camera.get_draw_size(w, h)
        self.player.image_dock.clip_draw(x, self.player.image_dock.h - 40 - y, w, h, view_x, view_y, draw_w, draw_h);

class Idle:
    def __init__(self, player):
        self.player = player
        self.frame_delta = 1

    def enter(self, e):
        if self.player.is_docked:  # Dock 상태에서 온 경우
            self.frame_delta = -1 # 도킹 애니메이션 역재생
        else:
            self.frame_delta = 1
            self.player.frame = 0

    def exit(self, e):
        if self.player.is_docked:
            return False # 도킹 애니메이션이 끝나지 않았으면 상태 전환 불가
        return True

    def do(self):
        if self.player.move_x != 0 or self.player.move_y != 0:
            self.player.stateMachine.handle_state_event(('!EMPTY', None))
            print('Player start moving')

        if self.player.is_docked and self.player.frame <= 0: # 도킹 애니메이션이 끝났을 때
            self.player.is_docked = False
            self.frame_delta = 1
            print('Player undocked')

        self.player.frame = (self.player.frame + self.frame_delta) % len(PLAYER_IDLE_FRAMES)

    def draw(self):
        camera = get_camera()
        if self.player.is_docked:
            image = self.player.image_dock
            x, y, w, h = PLAYER_DOCK_FRAMES[self.player.frame]
        else:
            image = self.player.image_idle
            x, y, w, h = PLAYER_IDLE_FRAMES[self.player.frame]

        view_x, view_y = camera.world_to_view(self.player.x, self.player.y)
        draw_w, draw_h = camera.get_draw_size(w, h)

        image.clip_draw(x, image.h - 40 - y, w, h, view_x, view_y, draw_w, draw_h)

class Move:
    key_push_count = int()
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0

    def exit(self, e):
        return True

    def do(self):
        if self.player.move_x == 0 and self.player.move_y == 0:
            self.player.stateMachine.handle_state_event(('EMPTY', None))

        self.player.x += self.player.move_x * 4
        self.player.y += self.player.move_y * 4

        self.player.frame = (self.player.frame + 1) % len(PLAYER_MOVE_FRAMES)

    def draw(self):
        camera = get_camera()
        x, y, w, h = PLAYER_MOVE_FRAMES[self.player.frame]
        view_x, view_y = camera.world_to_view(self.player.x, self.player.y)
        draw_w, draw_h = camera.get_draw_size(w, h)
        if self.player.move_x != 0:
            self.player.image_move_right.clip_composite_draw(x, self.player.image_move_right.h - 40 - y, w, h, 0,
            'h' if self.player.face_dir < 0 else 'x', view_x, view_y, draw_w, draw_h)
        elif self.player.move_y > 0:
            self.player.image_move_up.clip_draw(x, self.player.image_move_up.h - 40 - y, w, h, view_x, view_y, draw_w, draw_h)
        elif self.player.move_y < 0:
            self.player.image_move_down.clip_draw(x, self.player.image_move_down.h - 40 - y, w, h, view_x, view_y, draw_w, draw_h)

class Player:
    def __init__(self, robo_spider):
        self.image_dock = load_image('Assets/Sprites/Player/Attaching_Player_Docking.png')
        self.image_idle = load_image('Assets/Sprites/Player/Hero_Idle.png')
        self.image_move_right = load_image('Assets/Sprites/Player/Hero_Right_Moving.png')
        self.image_move_up = load_image('Assets/Sprites/Player/Hero_Up_Moving.png')
        self.image_move_down = load_image('Assets/Sprites/Player/Hero_Down_Moving.png')

        self.robo_spider = robo_spider
        self.is_docked = True   # 스파이더에 도킹 여부
        self.x = robo_spider.x - 16
        self.y = robo_spider.y + 16
        self.frame = 0
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
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        # IDLE과 MOVE 상태 변환을 위해 Player가 직접 키 입력을 처리
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_d:
                self.move_x += 1
                self.face_dir += 1
            elif event.key == SDLK_a:
                self.move_x -= 1
                self.face_dir -= 1
            elif event.key == SDLK_w:
                self.move_y += 1
            elif event.key == SDLK_s:
                self.move_y -= 1

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_d:
                self.move_x -= 1
                self.face_dir -= 1
            elif event.key == SDLK_a:
                self.move_x += 1
                self.face_dir += 1
            elif event.key == SDLK_w:
                self.move_y -= 1
            elif event.key == SDLK_s:
                self.move_y += 1

        print(f'Player handle_event: move_x={self.move_x}, move_y={self.move_y}, face_dir={self.face_dir}')

        self.stateMachine.handle_state_event(('INPUT', event))