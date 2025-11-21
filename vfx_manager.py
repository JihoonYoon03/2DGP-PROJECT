from pico2d import *
import game_world
import game_framework
from state_machine import StateMachine
from event_set import *
from abc import abstractmethod, ABCMeta


class VFXManager:
    def __init__(self):
        self.vfx_list = []
        self.vfx_pool = {}  # VFX 풀링용 딕셔너리

    def get_vfx_from_pool(self, vfx_class, *args):
        # setdefault로 풀에 해당 VFX 클래스가 있는지 판단
        pool = self.vfx_pool.setdefault(vfx_class, [])
        for vfx in pool:
            # 있으면 재활용
            if vfx.finished:
                vfx.reactivate(*args)
            return vfx
        else:
            # 없으면 새로 생성
            vfx = vfx_class(*args)
            pool.append(vfx)
            self.__add_vfx(vfx)
            game_world.add_object(vfx, vfx.layer)
        return vfx

    # private
    def __add_vfx(self, vfx, layer = 1):
        if vfx not in self.vfx_list:
            self.vfx_list.append(vfx)
            game_world.add_object(vfx, layer)

    # def delete_vfx(self, vfx):
    #     if vfx in self.vfx_list:
    #         self.vfx_list.remove(vfx)
    #         game_world.remove_object(vfx)

vfx_manager = VFXManager()

class VFXRunning:
    def __init__(self, vfx):
        self.vfx = vfx

    def enter(self, e):
        if signal_wake_up(e):
            self.vfx.current_frame = 0
            self.vfx.finished = False
        if self.vfx.summoner is not None:
            self.vfx.x, self.vfx.y = self.vfx.get_location()

    def exit(self, e):
        if self.vfx.additional_condition(e):
            return True
        else:
            return False

    def do(self):
        # VFX 소환자를 지정했을 경우, 위치 동기화. get_location은 VFX 별 구현
        if self.vfx.summoner is not None:
            self.vfx.x, self.vfx.y = self.vfx.get_location()

        self.vfx.current_frame += self.vfx.frame_per_time * game_framework.frame_time
        if self.vfx.current_frame >= self.vfx.frame_count:
            if self.vfx.loop:
                self.vfx.current_frame %= self.vfx.frame_count
            else:
                self.vfx.finished = True
                self.vfx.stateMachine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        cam = game_world.get_camera()

        frame = int(self.vfx.current_frame)

        clip_x, clip_y = self.vfx.image_clipper[frame]

        view_x, view_y = cam.world_to_view(self.vfx.x, self.vfx.y)
        draw_w, draw_h = cam.get_draw_size(self.vfx.frame_w, self.vfx.frame_h)

        self.vfx.image.clip_composite_draw(clip_x, self.vfx.image.h - self.vfx.frame_h - clip_y, self.vfx.frame_w, self.vfx.frame_h,
                                            0, '', view_x, view_y, draw_w, draw_h)

class VFXSleep:
    def __init__(self, vfx):
        self.vfx = vfx

    def enter(self, e):
        pass

    def exit(self, e):
        if self.vfx.additional_condition(e):
            return True
        else:
            return False

    def do(self):
        if not self.vfx.finished:
            self.vfx.stateMachine.handle_state_event(('WAKE_UP', None))

    def draw(self):
        pass


# VFX 부모 클래스
class VFX(metaclass=ABCMeta):
    def __init__(self):
        self.image = None
        self.image_clipper = None  # 이미지 클리핑 데이터 튜플
        self.x = 0
        self.y = 0
        self.frame_w = 0
        self.frame_h = 0
        self.layer = 1

        self.summoner = None

        self.frame_count = 0
        self.frame_per_time = 0 # 프레임 속도
        self.current_frame = 0

        self.elapsed_time = 0.0
        self.finished = False
        self.loop = False

        self.stateMachine = None

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        event_tuple = ('INPUT', event)
        self.stateMachine.handle_state_event(event_tuple)

    def reactivate(self, x, y):
        self.x = x
        self.y = y
        self.finished = False

    # VFX별 구현 필수
    @abstractmethod
    def get_location(self):
        pass

    @abstractmethod
    def additional_condition(self, e):
        pass

class VFXHooverLaserHit(VFX):
    # 시작 좌표 (x, y), 객체 레퍼런스
    def __init__(self, x, y, summoner = None, layer = 1):
        super().__init__()
        self.image = load_image('Assets/Sprites/VFX/DrillingFlash.png')
        self.image_clipper = (
        (0, 0), (64, 0), (0, 64)
        )

        self.x = x
        self.y = y
        self.frame_w = 64
        self.frame_h = 64
        self.layer = layer

        self.summoner = summoner

        self.frame_count = 3
        time_per_action = 0.3
        self.frame_per_time = time_per_action / self.frame_count # 프레임 속도

        self.loop = True

        self.IDLE = VFXRunning(self)
        self.SLEEP = VFXSleep(self)
        self.stateMachine = StateMachine(self.IDLE,
                                         {
                                             self.IDLE : { mouse_left_released : self.SLEEP },
                                             self.SLEEP : { mouse_left_pressed : self.IDLE}
                                         })

    def get_location(self):
        x = self.summoner.x + self.summoner.radius_display * math.cos(self.summoner.angle)
        y = self.summoner.y + self.summoner.radius_display * math.sin(self.summoner.angle)
        return x, y

    def additional_condition(self, e):
        if mouse_left_pressed(e):
            if self.summoner.shooting:
                return True
            else:
                return False
        return True