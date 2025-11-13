from pico2d import *

import game_world
from state_machine import StateMachine
import event_set
from event_set import signal_empty, signal_not_empty, r_pressed, signal_time_out
from game_world import get_camera
from player import Player
import game_framework
from physics_data import *

# 스프라이트 프레임 정보 (x, y, w, h)
# 1행 1열부터 시작 (좌상단 기준)
# 178 * 444

SPIDER_WIDTH_SMALL = 178
SPIDER_HEIGHT_SMALL = 444

SPIDER_MOVE_FRAMES = [
    # 1행 (11개)
    (0, 0), (178, 0), (356, 0), (534, 0), (712, 0), (890, 0), (1068, 0), (1246, 0), (1424, 0), (1602, 0), (1780, 0),
    # 2행 (5개)
    (0, 444), (178, 444), (356, 444), (534, 444), (712, 444)
]

SPIDER_DOCK_FRAMES = (
    # 1행 (y=1608, h=440)
    (0, 1608, 178, 440), (178, 1608, 178, 440), (356, 1608, 178, 440), (534, 1608, 178, 440), (712, 1608, 178, 440),
    (890, 1608, 178, 440), (1068, 1608, 178, 440), (1246, 1608, 178, 440), (1424, 1608, 178, 440), (1602, 1608, 178, 440), (1780, 1608, 178, 440),
    # 2행 (y=1164, h=440)
    (0, 1164, 178, 440), (178, 1164, 178, 440), (356, 1164, 178, 440), (534, 1164, 178, 440), (712, 1164, 178, 440),
    (890, 1164, 178, 440), (1068, 1164, 178, 440), (1246, 1164, 178, 440), (1424, 1164, 178, 440), (1602, 1164, 178, 440), (1780, 1164, 178, 440),
    # 3행 (y=720, h=440)
    (0, 720, 178, 440), (178, 720, 178, 440), (356, 720, 178, 440), (534, 720, 178, 440), (712, 720, 178, 440),
    (890, 720, 178, 440), (1068, 720, 178, 440), (1246, 720, 178, 440), (1424, 720, 178, 440), (1602, 720, 178, 440), (1780, 720, 178, 440),
    # 4행 (y=276, h=440)
    (0, 276, 178, 440), (178, 276, 178, 440)
)

SPIDER_UNDOCK_FRAMES = (
    # 1행 (y=584, h=440)
    (0, 584, 178, 440), (178, 584, 178, 440), (356, 584, 178, 440), (534, 584, 178, 440), (712, 584, 178, 440),
    (890, 584, 178, 440), (1068, 584, 178, 440), (1246, 584, 178, 440), (1424, 584, 178, 440), (1602, 584, 178, 440), (1780, 584, 178, 440),
    # 2행 (y=140, h=440) - 7개만 사용
    (0, 140, 178, 440), (178, 140, 178, 440), (356, 140, 178, 440), (534, 140, 178, 440), (712, 140, 178, 440),
    (890, 140, 178, 440), (1068, 140, 178, 440)
)

SPIDER_INNER_DOCKER_FRAMES = (
    (0, 0), (40, 0), (80, 0),
    (0, 40), (40, 40), (80, 40)
)

class SpIdle:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp):
        self.sp = sp
        if SpIdle.frames_per_action is None:
            SpIdle.frames_per_action = len(SPIDER_MOVE_FRAMES)
        if SpIdle.action_per_time is None:
            SpIdle.action_per_time = get_spider_action_per_time(SpIdle.frames_per_action)

    def enter(self, e):
        if not self.sp.is_moving:
            self.sp.frame = 0

    def exit(self, e):
        return True

    def do(self):
        if self.sp.move_dir != 0:
            self.sp.stateMachine.handle_state_event(('!EMPTY', None))
            return

        if self.sp.is_moving:
            self.sp.frame = self.sp.frame + SpIdle.frames_per_action * SpIdle.action_per_time * game_framework.frame_time * self.sp.last_move_dir
            self.sp.y += self.sp.speed * SPIDER_RUN_SPEED_PPS * game_framework.frame_time * self.sp.last_move_dir
            if self.sp.frame <= 0 or self.sp.frame >= 16: # 이동 모션이 끝났을 때
                self.sp.is_moving = False
                self.sp.frame = 0
                self.sp.move_dir = 0
                self.sp.last_move_dir = 0
                return

    def draw(self):
        camera = get_camera()
        x, y = SPIDER_MOVE_FRAMES[int(self.sp.frame)]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL)
        self.sp.image_move.clip_draw(x, self.sp.image_move.h - SPIDER_HEIGHT_SMALL - y,
                                     SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL, view_x, view_y, draw_w, draw_h)

class SpMove:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp):
        self.sp = sp
        if SpMove.frames_per_action is None:
            SpMove.frames_per_action = len(SPIDER_MOVE_FRAMES)
        if SpMove.action_per_time is None:
            SpMove.action_per_time = get_spider_action_per_time(SpMove.frames_per_action)

    def enter(self, e):
        self.sp.is_moving = True

    def exit(self, e):
        return True

    def do(self):
        if self.sp.move_dir == 0:
            self.sp.stateMachine.handle_state_event(('EMPTY', None))
            return
        self.sp.frame = ((self.sp.frame
                         + SpMove.frames_per_action * SpMove.action_per_time * game_framework.frame_time * self.sp.move_dir)
                         % len(SPIDER_MOVE_FRAMES))
        self.sp.y += self.sp.speed * SPIDER_RUN_SPEED_PPS * game_framework.frame_time * self.sp.move_dir

    def draw(self):
        camera = get_camera()
        x, y = SPIDER_MOVE_FRAMES[int(self.sp.frame)]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL)
        self.sp.image_move.clip_draw(x, self.sp.image_move.h - SPIDER_HEIGHT_SMALL - y,
                                     SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL, view_x, view_y, draw_w, draw_h)

class SpDock:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp):
        self.sp = sp
        if SpDock.frames_per_action is None:
            SpDock.frames_per_action = len(SPIDER_DOCK_FRAMES)
        if SpDock.action_per_time is None:
            SpDock.action_per_time = get_spider_action_per_time(SpDock.frames_per_action)

    def enter(self, e):
        self.sp.is_moving = False
        self.sp.move_dir = 0
        self.sp.last_move_dir = 0
        self.sp.frame = 0
        event_set.reset_all_flags()

    def exit(self, e):
        if self.sp.frame < 34 or not self.sp.player.is_docked: return False # 도킹 모션이 끝나지 않았을 때는 상태 전환 불가
        return True

    def do(self):
        self.sp.frame = self.sp.frame + SpDock.frames_per_action * SpDock.action_per_time * game_framework.frame_time
        if self.sp.frame >= 34:
            self.sp.frame = 34
            camera = get_camera()
            camera.zoom = 2.0
            self.sp.is_docking = True

    def draw(self):
        camera = get_camera()
        x, y, w, h = SPIDER_DOCK_FRAMES[int(self.sp.frame)]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(178, 440)
        self.sp.image_dock.clip_draw(x, y, w, h, view_x, view_y, draw_w, draw_h)

class SpUndock:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp):
        self.sp = sp
        if SpUndock.frames_per_action is None:
            SpUndock.frames_per_action = len(SPIDER_UNDOCK_FRAMES)
        if SpUndock.action_per_time is None:
            SpUndock.action_per_time = get_spider_action_per_time(SpUndock.frames_per_action)

    def enter(self, e):
        camera = get_camera()
        camera.zoom = camera.screen_width / 1920 * 2
        self.sp.is_docking = False
        self.sp.move_dir = 0
        self.sp.last_move_dir = 0
        self.sp.frame = 0
        event_set.reset_all_flags()

    def exit(self, e):
        return True

    def do(self):
        if self.sp.frame < 17:
            self.sp.frame = self.sp.frame + SpUndock.frames_per_action * SpUndock.action_per_time * game_framework.frame_time
        else:
            self.sp.stateMachine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        camera = get_camera()
        x, y, w, h = SPIDER_UNDOCK_FRAMES[int(self.sp.frame)]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(178, 440)
        self.sp.image_undock.clip_draw(x, y, w, h, view_x, view_y, draw_w, draw_h)

class RoboSpider:
    def __init__(self, x = 960, y = 540):
        self.image_move = load_image('Assets/Sprites/Spider/Spider_Moving.png')
        self.image_dock = load_image('Assets/Sprites/Spider/Spider_Docking.png')
        self.image_undock = load_image('Assets/Sprites/Spider/Spider_Undocking.png')

        # 스파이더 중앙과 스프라이트 중앙 매칭 필요
        self.x = x - 178 // 2
        self.y = y
        self.speed = 1
        self.is_moving = False
        self.is_docking = False
        self.move_dir = 0
        self.last_move_dir = 0
        self.frame = 0

        self.w = 178
        self.h = 440

        self.inner = RoboSpiderIn(self)
        self.player = Player(self)
        game_world.add_collision_pair('player:tile', self.player, None)

        self.IDLE = SpIdle(self)
        self.UP = SpMove(self)
        self.DOCK = SpDock(self)
        self.UNDOCK = SpUndock(self)
        self.stateMachine = StateMachine(
            self.IDLE,
        {
            self.IDLE : { signal_not_empty : self.UP, r_pressed : self.DOCK },
            self.UP : { signal_empty : self.IDLE, r_pressed : self.DOCK },
            self.DOCK : { r_pressed : self.UNDOCK },
            self.UNDOCK : { signal_time_out : self.IDLE },
        })

    def update(self):
        self.stateMachine.update()
        self.inner.update()
        if self.is_docking:
            self.player.update()

    def draw(self):
        self.stateMachine.draw()
        if self.is_docking:
            self.inner.draw()
            self.player.draw()

    def handle_event(self, event):
        if not self.is_docking:
            prev_moving = self.move_dir != 0

            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_w:
                    event_set.flag_w = True
                    self.move_dir += 1
                    self.last_move_dir = 1
                elif event.key == SDLK_s:
                    event_set.flag_s = True
                    self.move_dir -= 1
                    self.last_move_dir = -1

            # 도킹 상태에서 키 홀딩 후, 도킹 해제 뒤 키업 처리 방지 필요
            elif event.type == SDL_KEYUP:
                if event.key == SDLK_w and event_set.flag_w:
                    event_set.flag_w = False
                    self.move_dir -= 1
                elif event.key == SDLK_s and event_set.flag_s:
                    event_set.flag_s = False
                    self.move_dir += 1

            now_moving = self.move_dir != 0

            # 정지 -> 이동
            if not prev_moving and now_moving:
                self.stateMachine.handle_state_event(('!EMPTY', None))

            # 이동 -> 정지
            elif prev_moving and not now_moving:
                self.stateMachine.handle_state_event(('EMPTY', None))

        self.stateMachine.handle_state_event(('INPUT', event))
        if self.is_docking:
            self.player.handle_event(event)

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass

class SpInIdle:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp_in):
        self.sp_in = sp_in
        if SpInIdle.frames_per_action is None:
            SpInIdle.frames_per_action = len(SPIDER_INNER_DOCKER_FRAMES)
        if SpInIdle.action_per_time is None:
            SpInIdle.action_per_time = get_player_action_per_time(SpInIdle.frames_per_action)

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        if self.sp_in.robo_spider.is_docking:
            self.sp_in.docker_frame = ((self.sp_in.docker_frame
                                       + SpInIdle.frames_per_action * SpInIdle.action_per_time * game_framework.frame_time)
                                       % SpInIdle.frames_per_action)
        else:
            self.sp_in.docker_x = self.sp_in.robo_spider.x - 16
            self.sp_in.docker_y = self.sp_in.robo_spider.y + 16

    def draw(self):
        camera = get_camera()
        # 배경 그리기
        view_x, view_y = camera.world_to_view(self.sp_in.robo_spider.x, self.sp_in.robo_spider.y - 2) # 2는 이미지 크기 보정용
        draw_w, draw_h = camera.get_draw_size(self.sp_in.image_background.w, self.sp_in.image_background.h)
        self.sp_in.image_background.clip_draw(0, 0, self.sp_in.image_background.w, self.sp_in.image_background.h,
                                              view_x, view_y, draw_w, draw_h)
        # 방 내부 그리기
        draw_w, draw_h = camera.get_draw_size(self.sp_in.image_room.w, self.sp_in.image_room.h)
        self.sp_in.image_room.clip_draw(0, 0, self.sp_in.image_room.w, self.sp_in.image_room.h,
                                        view_x, view_y, draw_w, draw_h)

        # 프레임 그리기
        draw_w, draw_h = camera.get_draw_size(self.sp_in.image_frame.w, self.sp_in.image_frame.h)
        self.sp_in.image_frame.clip_draw(0, 0, self.sp_in.image_frame.w, self.sp_in.image_frame.h,
                                         view_x, view_y, draw_w, draw_h)

        # 도킹 모듈 그리기
        x, y = SPIDER_INNER_DOCKER_FRAMES[int(self.sp_in.docker_frame)]
        docker_view_x, docker_view_y = camera.world_to_view(self.sp_in.docker_x, self.sp_in.docker_y)
        draw_w, draw_h = camera.get_draw_size(40, 40)
        self.sp_in.image_docker.clip_draw(x, self.sp_in.image_docker.h - 40 - y,
                                          40, 40, docker_view_x, docker_view_y, draw_w, draw_h)

# 스파이더 내부
class RoboSpiderIn:
    def __init__(self, robo_spider):
        self.image_room = load_image('Assets/Sprites/Spider/Spider_Inner_Back.png')
        self.image_frame = load_image('Assets/Sprites/Spider/Spider_Inner_Frame.png')
        self.image_background = load_image('Assets/Sprites/Spider/Spider_Inner_Opened.png')
        self.image_docker = load_image('Assets/Sprites/Spider/Spider_DockingModule.png')

        self.robo_spider = robo_spider

        self.docker_x = robo_spider.x - 16
        self.docker_y = robo_spider.y + 16
        self.docker_frame = 0

        self.IDLE = SpInIdle(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))