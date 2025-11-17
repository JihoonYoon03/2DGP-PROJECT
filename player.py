from pico2d import *
import event_set
from event_set import signal_empty, signal_not_empty, signal_in_range, e_pressed
from game_world import get_camera, collide_bb
from state_machine import StateMachine
from physics_data import *
import math
import game_framework
import game_world

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40

PLAYER_DOCK_FRAMES = (
    (0, 0), (40, 0), (80, 0), (120, 0), (160, 0), (200, 0),
    (0, 40), (40, 40), (80, 40), (120, 40), (160, 40), (200, 40),
    (0, 80),
)

PLAYER_IDLE_FRAMES = (
    (0, 0), (40, 0), (80, 0), (120, 0), (160, 0), (200, 0),
    (0, 40), (40, 40), (80, 40), (120, 40), (160, 40), (200, 40),
    (0, 80), (40, 80), (80, 80), (120, 80)
)

PLAYER_MOVE_FRAMES = (
    (0, 0), (40, 0), (80, 0)
)


class Dock:
    frames_per_action = None
    action_per_time = None
    def __init__(self, player):
        self.player = player
        if Dock.frames_per_action is None:
            Dock.frames_per_action = len(PLAYER_DOCK_FRAMES)
        if Dock.action_per_time is None:
            Dock.action_per_time = get_player_action_per_time(Dock.frames_per_action)

    def enter(self, e):
        if e[0] == 'START':
            self.player.is_docked = True
            self.player.frame = 12
        elif e[0] == 'IN_RANGE':
            self.player.is_docked = True
            self.player.x = self.player.robo_spider.inner.docker_x
            self.player.y = self.player.robo_spider.inner.docker_y
            self.player.frame = 0
            self.player.move_x = 0
            self.player.move_y = 0
            event_set.reset_all_flags()

    def exit(self, e):
        return True

    def do(self):
        if self.player.is_docked:
            self.player.x = self.player.robo_spider.inner.docker_x
            self.player.y = self.player.robo_spider.inner.docker_y
        if self.player.frame < Dock.frames_per_action - 1:
            self.player.frame = ((self.player.frame
                                  + Dock.frames_per_action * Dock.action_per_time * game_framework.frame_time)
                                 % Dock.frames_per_action)
        if self.player.frame >= Dock.frames_per_action:
            self.player.frame = Dock.frames_per_action - 1

    def draw(self):
        camera = get_camera()
        x, y = PLAYER_DOCK_FRAMES[int(self.player.frame)]
        view_x, view_y = camera.world_to_view(self.player.x, self.player.y)
        draw_w, draw_h = camera.get_draw_size(PLAYER_WIDTH, PLAYER_HEIGHT)
        self.player.image_dock.clip_draw(x, self.player.image_dock.h - PLAYER_HEIGHT - y, PLAYER_WIDTH, PLAYER_HEIGHT,
                                         view_x, view_y, draw_w, draw_h)


class Idle:
    frames_per_action = None
    action_per_time = None
    def __init__(self, player):
        self.player = player
        self.frame_delta = 1
        if Idle.frames_per_action is None:
            Idle.frames_per_action = len(PLAYER_IDLE_FRAMES)
        if Idle.action_per_time is None:
            Idle.action_per_time = get_player_action_per_time(Idle.frames_per_action)

    def enter(self, e):
        if self.player.is_docked:  # Dock 상태에서 온 경우
            self.frame_delta = -1  # 도킹 애니메이션 역재생
        else:
            self.frame_delta = 1
            self.player.frame = 0

    def exit(self, e):
        if self.player.is_docked:
            return False  # 도킹 애니메이션이 끝나지 않았으면 상태 전환 불가
        return True

    def do(self):
        if self.player.is_docked:
            self.player.frame = (self.player.frame
                                  + Idle.frames_per_action * Idle.action_per_time * game_framework.frame_time * self.frame_delta)
        else:
            self.player.frame = ((self.player.frame
                                + Idle.frames_per_action * Idle.action_per_time * game_framework.frame_time * self.frame_delta)
                                % Idle.frames_per_action)

        if self.player.is_docked and self.player.frame <= 0:  # 도킹 애니메이션이 끝났을 때
            self.player.is_docked = False
            self.frame_delta = 1


    def draw(self):
        camera = get_camera()
        if self.player.is_docked:
            image = self.player.image_dock
            x, y = PLAYER_DOCK_FRAMES[int(self.player.frame)]
        else:
            image = self.player.image_idle
            x, y = PLAYER_IDLE_FRAMES[int(self.player.frame)]

        view_x, view_y = camera.world_to_view(self.player.x, self.player.y)
        draw_w, draw_h = camera.get_draw_size(PLAYER_WIDTH, PLAYER_HEIGHT)

        image.clip_draw(x, image.h - PLAYER_HEIGHT - y, PLAYER_WIDTH, PLAYER_HEIGHT, view_x, view_y, draw_w, draw_h)


class Move:
    key_push_count = int()
    frames_per_action = None
    action_per_time = None

    def __init__(self, player):
        self.player = player
        if Move.frames_per_action is None:
            Move.frames_per_action = len(PLAYER_MOVE_FRAMES)
        if Move.action_per_time is None:
            Move.action_per_time = get_player_action_per_time(Move.frames_per_action)

    def enter(self, e):
        if e[0] == '!EMPTY':
            self.player.frame = 0

    def exit(self, e):
        return True

    def do(self):
        self.player.delta_x = self.player.move_x * PLAYER_RUN_SPEED_PPS * game_framework.frame_time
        self.player.delta_y = self.player.move_y * PLAYER_RUN_SPEED_PPS * game_framework.frame_time
        self.player.x += self.player.delta_x
        self.player.y += self.player.delta_y

        self.player.frame = ((self.player.frame
                              + Move.frames_per_action * Move.action_per_time * game_framework.frame_time)
                             % Move.frames_per_action)

        if self.player.x > self.player.robo_spider.x + 100:
            camera = get_camera()
            camera.cam_lock(self.player)
        else:
            camera = get_camera()
            camera.cam_lock(self.player.robo_spider)

    def draw(self):
        camera = get_camera()
        x, y = PLAYER_MOVE_FRAMES[int(self.player.frame)]
        view_x, view_y = camera.world_to_view(self.player.x, self.player.y)
        draw_w, draw_h = camera.get_draw_size(PLAYER_WIDTH, PLAYER_HEIGHT)

        # 좌우
        if self.player.move_x != 0:
            self.player.image_move_right.clip_composite_draw(x, self.player.image_move_right.h -
                                                             PLAYER_HEIGHT - y, PLAYER_WIDTH, PLAYER_HEIGHT,
                                                             0, 'h' if self.player.face_dir < 0 else 'x',
                                                             view_x, view_y, draw_w, draw_h)

        # 상하
        elif self.player.move_y > 0:
            self.player.image_move_up.clip_draw(x, self.player.image_move_up.h - PLAYER_HEIGHT - y,
                                                PLAYER_WIDTH, PLAYER_HEIGHT, view_x, view_y, draw_w, draw_h)
        elif self.player.move_y < 0:
            self.player.image_move_down.clip_draw(x, self.player.image_move_down.h - PLAYER_HEIGHT - y,
                                                  PLAYER_WIDTH, PLAYER_HEIGHT, view_x, view_y, draw_w, draw_h)


class Player:
    def __init__(self, robo_spider):
        self.image_dock = load_image('Assets/Sprites/Player/Attaching_Player_Docking.png')
        self.image_idle = load_image('Assets/Sprites/Player/Hero_Idle.png')
        self.image_move_right = load_image('Assets/Sprites/Player/Hero_Right_Moving.png')
        self.image_move_up = load_image('Assets/Sprites/Player/Hero_Up_Moving.png')
        self.image_move_down = load_image('Assets/Sprites/Player/Hero_Down_Moving.png')

        self.robo_spider = robo_spider
        self.is_docked = True  # 스파이더에 도킹 여부
        self.x = robo_spider.x - 16
        self.y = robo_spider.y + 16
        self.frame = 0
        self.face_dir = 0  # 1: right, -1: left, 2: up, -2: down
        self.move_x = 0
        self.move_y = 0
        self.delta_x = 0
        self.delta_y = 0

        self.DOCKED = Dock(self)
        self.IDLE = Idle(self)
        self.MOVE = Move(self)

        self.stateMachine = StateMachine(
            self.DOCKED,
            {
                self.DOCKED: {e_pressed: self.IDLE},
                self.IDLE: {signal_not_empty: self.MOVE, signal_in_range: self.DOCKED},
                self.MOVE: {signal_empty: self.IDLE, signal_in_range: self.DOCKED}
            })

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

        camera = get_camera()
        x1, y1, x2, y2 = self.get_bb()
        view_x1, view_y1 = camera.world_to_view(x1, y1)
        view_x2, view_y2 = camera.world_to_view(x2, y2)
        draw_rectangle(view_x1, view_y1, view_x2, view_y2)

    def handle_event(self, event):
        prev_moving = (self.move_x != 0 or self.move_y != 0)

        event_tuple = ('INPUT', event)

        # IDLE과 MOVE 상태 변환을 위해 Player가 직접 키 입력을 처리
        if event_set.e_pressed(event_tuple) and not self.is_docked:
            if math.sqrt(math.pow((self.x - self.robo_spider.inner.docker_x), 2) +
                         math.pow((self.y - self.robo_spider.inner.docker_y), 2)) < 30:
                self.stateMachine.handle_state_event(('IN_RANGE', None))
                return
        elif event_set.d_pressed(event_tuple):
            event_set.flag_d = True
            self.move_x += 1
            self.face_dir += 1
        elif event_set.a_pressed(event_tuple):
            event_set.flag_a = True
            self.move_x -= 1
            self.face_dir -= 1
        elif event_set.w_pressed(event_tuple):
            event_set.flag_w = True
            self.move_y += 1
        elif event_set.s_pressed(event_tuple):
            event_set.flag_s = True
            self.move_y -= 1

        elif event_set.d_released(event_tuple) and event_set.flag_d:
            event_set.flag_d = False
            self.move_x -= 1
            self.face_dir -= 1
        elif event_set.a_released(event_tuple) and event_set.flag_a:
            event_set.flag_a = False
            self.move_x += 1
            self.face_dir += 1
        elif event_set.w_released(event_tuple) and event_set.flag_w:
            event_set.flag_w = False
            self.move_y -= 1
        elif event_set.s_released(event_tuple) and event_set.flag_s:
            event_set.flag_s = False
            self.move_y += 1

        now_moving = (self.move_x != 0 or self.move_y != 0)

        # 정지 -> 이동
        if not prev_moving and now_moving and not self.is_docked:
            self.stateMachine.handle_state_event(('!EMPTY', None))

        # 이동 -> 정지
        elif prev_moving and not now_moving:
            self.stateMachine.handle_state_event(('EMPTY', None))

        # 만약 이동 -> 이동 (방향 전환 등)이면 IDLE 상태를 거치지 않게됨

        self.stateMachine.handle_state_event(('INPUT', event))

    def get_bb(self):
        return self.x - PLAYER_WIDTH // 3, self.y - PLAYER_HEIGHT // 2.5, \
               self.x + PLAYER_WIDTH // 3, self.y + PLAYER_HEIGHT // 2.5

    def handle_collision(self, group, other):
        if group == 'player:tile':
            # 충돌 취소 후, 다시 계산
            origin_x = self.x
            origin_y = self.y
            self.x -= self.delta_x
            self.y -= self.delta_y

            # x만 증가시킬 때 충돌 검사
            self.x = origin_x
            x_collide = collide_bb(self, other)

            # y만 증가시킬 때 충돌 검사
            self.x -= self.delta_x  # 복구
            self.y = origin_y
            y_collide = collide_bb(self, other)

            self.y -= self.delta_y

            if not x_collide:
                self.x += self.delta_x * 0.5
            if not y_collide:
                self.y += self.delta_y * 0.5