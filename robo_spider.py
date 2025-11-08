from pico2d import *
from state_machine import StateMachine
from event_set import *
from game_world import get_camera
from player import Player

# self.sp.frame * 178 % (11 * 178), self.h - 440 - (self.sp.frame // 11 * 444), 178, 440,


# Spider_Moving 스프라이트 프레임 정보 (x, y, w, h)
# 1행 1열부터 시작 (좌상단 기준)

SPIDER_MOVE_FRAMES = (
    # 1행 (프레임 0-10)
    (0, 584, 178, 440),
    (178, 584, 178, 440),
    (356, 584, 178, 440),
    (534, 584, 178, 440),
    (712, 584, 178, 440),
    (890, 584, 178, 440),
    (1068, 584, 178, 440),
    (1246, 584, 178, 440),
    (1424, 584, 178, 440),
    (1602, 584, 178, 440),
    (1780, 584, 178, 440),

    # 2행 (프레임 11-15)
    (0, 140, 178, 440),
    (178, 140, 178, 440),
    (356, 140, 178, 440),
    (534, 140, 178, 440),
    (712, 140, 178, 440),
)

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

class SpIdle:
    def __init__(self, sp):
        self.sp = sp

    def enter(self, e):
        if not self.sp.is_moving:
            self.sp.frame = 0

    def exit(self, e):
        return True

    def do(self):
        if self.sp.is_moving:
            self.sp.frame = self.sp.frame + self.sp.move_dir
            if self.sp.frame <= 0 or self.sp.frame >= 16: # 이동 모션이 끝났을 때
                self.sp.is_moving = False
                self.sp.frame = 0
                self.sp.move_dir = 0
                return
            self.sp.y += self.sp.speed * self.sp.move_dir

    def draw(self):
        camera = get_camera()
        x, y, w, h = SPIDER_MOVE_FRAMES[self.sp.frame]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(178, 440)
        self.sp.image_move.clip_draw(x, y, w, h, view_x, view_y, draw_w, draw_h)

class SpUp:
    def __init__(self, sp):
        self.sp = sp

    def enter(self, e):
        self.sp.is_moving = True
        self.sp.move_dir = 1

    def exit(self, e):
        return True

    def do(self):
        self.sp.frame = (self.sp.frame + 1) % 16
        self.sp.y += self.sp.speed * self.sp.move_dir

    def draw(self):
        camera = get_camera()
        x, y, w, h = SPIDER_MOVE_FRAMES[self.sp.frame]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(178, 440)
        self.sp.image_move.clip_draw(x, y, w, h, view_x, view_y, draw_w, draw_h)

class SpDown:
    def __init__(self, sp):
        self.sp = sp

    def enter(self, e):
        self.sp.is_moving = True
        self.sp.move_dir = -1

    def exit(self, e):
        return True

    def do(self):
        self.sp.frame = self.sp.frame - 1 if self.sp.frame > 0 else 15
        self.sp.y += self.sp.speed * self.sp.move_dir

    def draw(self):
        camera = get_camera()
        x, y, w, h = SPIDER_MOVE_FRAMES[self.sp.frame]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(178, 440)
        self.sp.image_move.clip_draw(x, y, w, h, view_x, view_y, draw_w, draw_h)

class SpDock:
    def __init__(self, sp):
        self.sp = sp

    def enter(self, e):
        self.sp.is_moving = False
        self.sp.move_dir = 0
        self.sp.frame = 0

    def exit(self, e):
        if self.sp.frame < 34: return False # 도킹 모션이 끝나지 않았을 때는 상태 전환 불가
        return True

    def do(self):
        if self.sp.frame < 34:
            self.sp.frame = self.sp.frame + 1
        else:
            camera = get_camera()
            camera.zoom = 2.0
            self.sp.is_docking = True

    def draw(self):
        camera = get_camera()
        x, y, w, h = SPIDER_DOCK_FRAMES[self.sp.frame]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(178, 440)
        self.sp.image_dock.clip_draw(x, y, w, h, view_x, view_y, draw_w, draw_h)

class SpUndock:
    def __init__(self, sp):
        self.sp = sp

    def enter(self, e):
        camera = get_camera()
        camera.zoom = camera.screen_width / 1920 * 2
        self.sp.frame = 0
        self.sp.is_docking = False

    def exit(self, e):
        return True

    def do(self):
        if self.sp.frame < 17:
            self.sp.frame = self.sp.frame + 1
        else:
            self.sp.stateMachine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        camera = get_camera()
        x, y, w, h = SPIDER_UNDOCK_FRAMES[self.sp.frame]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y)
        draw_w, draw_h = camera.get_draw_size(178, 440)
        self.sp.image_undock.clip_draw(x, y, w, h, view_x, view_y, draw_w, draw_h)

class RoboSpider:
    def __init__(self, x = 960, y = 540):
        self.image_move = load_image('Assets/Sprites/Spider/Spider_Moving.png')
        self.image_dock = load_image('Assets/Sprites/Spider/Spider_Docking.png')
        self.image_undock = load_image('Assets/Sprites/Spider/Spider_Undocking.png')

        self.inner = RoboSpiderIn(self)
        self.x = x
        self.y = y
        self.speed = 5
        self.is_moving = False
        self.is_docking = False
        self.move_dir = 0
        self.frame = 0
        self.w = 178
        self.h = 440
        self.x -= 178 // 2

        self.player = Player(self)

        self.IDLE = SpIdle(self)
        self.UP = SpUp(self)
        self.DOWN = SpDown(self)
        self.DOCK = SpDock(self)
        self.UNDOCK = SpUndock(self)
        self.stateMachine = StateMachine(
            self.IDLE,
        {
            self.IDLE : { w_pressed : self.UP, s_pressed : self.DOWN, r_pressed : self.DOCK },
            self.UP : { w_released : self.IDLE, s_pressed : self.DOWN, r_pressed : self.DOCK },
            self.DOWN : { s_released : self.IDLE, w_pressed : self.UP, r_pressed : self.DOCK },
            self.DOCK : { r_pressed : self.UNDOCK },
            self.UNDOCK : { signal_time_out : self.IDLE },
        })

    def update(self):
        self.stateMachine.update()
        if self.is_docking:
            self.player.update()
            self.inner.update()

    def draw(self):
        self.stateMachine.draw()
        if self.is_docking:
            self.inner.draw()
            self.player.draw()

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))
        if self.is_docking:
            self.player.handle_event(event)

class SpInIdle:
    def __init__(self, sp_in):
        self.sp_in = sp_in

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        pass

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

# 스파이더 내부
class RoboSpiderIn:
    def __init__(self, robo_spider):
        self.image_room = load_image('Assets/Sprites/Spider/Spider_Inner_Back.png')
        self.image_frame = load_image('Assets/Sprites/Spider/Spider_Inner_Frame.png')
        self.image_background = load_image('Assets/Sprites/Spider/Spider_Inner_Opened.png')
        self.robo_spider = robo_spider
        self.IDLE = SpInIdle(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))