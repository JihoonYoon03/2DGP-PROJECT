from pico2d import *
import event_set
import vfx_manager
from event_set import mouse_motion, mouse_coordinate
from game_world import get_camera
from state_machine import StateMachine
from physics_data import *
from vfx_manager import vfx_manager, VFXHooverLaserHit
import math
import game_framework
import game_world

RAY_W_H = 28

class Idle:
    def __init__(self, hoover):
        self.hoover = hoover
        self.is_flip = ''
        self.draw_angle = 0

    def enter(self, e):
        if mouse_motion(e):
            mouse_x, mouse_y = mouse_coordinate(e)
            camera = get_camera()
            view_x, view_y = camera.world_to_view(self.hoover.player.x, self.hoover.player.y)
            dx = mouse_x - view_x
            dy = mouse_y - view_y
            self.hoover.angle = math.atan2(dy, dx)
            self.draw_angle = self.hoover.angle
            if abs(self.draw_angle) > math.pi / 2:
                self.draw_angle += math.pi
                self.is_flip = 'h'
            else:
                self.is_flip = ''

    def exit(self, e):
        return True

    def do(self):
        pass

    def draw(self):
        if self.hoover.player.is_docked:
            return

        camera = get_camera()
        draw_w, draw_h = camera.get_draw_size(self.hoover.image_back.w, self.hoover.image_back.h)
        view_x, view_y = camera.world_to_view(self.hoover.player.x, self.hoover.player.y)
        self.hoover.image_back.clip_composite_draw(0, 0, self.hoover.image_back.w, self.hoover.image_back.h,
                                                   self.draw_angle, self.is_flip,
                                                  view_x, view_y, draw_w, draw_h)
        self.hoover.laser.draw()
        self.hoover.image_front.clip_composite_draw(0, 0, self.hoover.image_front.w, self.hoover.image_front.h,
                                                    self.draw_angle, self.is_flip,
                                                  view_x, view_y, draw_w, draw_h)


class Hoover:
    def __init__(self, player):
        self.image_back = load_image('Assets/Sprites/Hoover/ResourceHoover_lvl1_Back.png')
        self.image_front = load_image('Assets/Sprites/Hoover/ResourceHoover_lvl1_Front.png')

        self.player = player
        self.angle = 0
        self.laser_range = TILE_SIZE_PIXEL * 2
        self.laser = HooverLaser(self)

        self.IDLE = Idle(self)

        self.stateMachine = StateMachine(self.IDLE,
                                         {
                                             self.IDLE: { mouse_motion : self.IDLE }
                                          })

    def update(self):
        self.stateMachine.update()
        self.laser.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))

        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            self.laser.shooting = True
        elif event.type == SDL_MOUSEBUTTONUP and event.button == SDL_BUTTON_LEFT:
            self.laser.shooting = False

        self.laser.handle_event(event)

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass


class ReadyToShoot:
    def __init__(self, laser):
        self.laser = laser

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        pass

    def draw(self):
        pass

class Shooting:
    frames_per_action = 5
    action_per_time = None

    def __init__(self, laser):
        self.laser = laser
        if Shooting.action_per_time is None:
            Shooting.action_per_time = get_hoover_laser_action_per_time(Shooting.frames_per_action)

    def enter(self, e):
        print("Shooting Laser")

    def exit(self, e):
        return True

    def do(self):
        self.laser.frame = ((self.laser.frame + Shooting.frames_per_action * Shooting.action_per_time * game_framework.frame_time)
                            % Shooting.frames_per_action)
        self.laser.x = self.laser.hoover.player.x
        self.laser.y = self.laser.hoover.player.y
        self.laser.angle = self.laser.hoover.angle

    def draw(self):
        camera = get_camera()
        mid_w, mid_h = camera.get_draw_size(RAY_W_H // 2, RAY_W_H)
        end_w, end_h = camera.get_draw_size(RAY_W_H * (3 / 4), RAY_W_H)

        for dr in range(self.laser.radius_min, self.laser.radius_display, RAY_W_H // 2):
            x = dr * math.cos(self.laser.angle)
            y = dr * math.sin(self.laser.angle)

            view_x, view_y = camera.world_to_view(self.laser.x + x, self.laser.y + y)

            if dr == self.laser.radius_min:
                # 첫 조각
                # 처음부터 3/4 지점까지 그리기
                clip_x = RAY_W_H * int(self.laser.frame)
                clip_w = int(RAY_W_H * 3 / 4)
                self.laser.image_ray.clip_composite_draw(clip_x, 0, clip_w, RAY_W_H,
                                                     self.laser.angle, '',
                                                     view_x, view_y, end_w, end_h)

            elif (dr + RAY_W_H - RAY_W_H // 2) < self.laser.radius_max:
                # 중간 조각
                # 1/4 지점부터 3/4 지점까지 그리기
                clip_x = RAY_W_H * int(self.laser.frame) + RAY_W_H // 4
                clip_w = RAY_W_H // 2
                self.laser.image_ray.clip_composite_draw(clip_x, 0, clip_w, RAY_W_H,
                                                     self.laser.angle, '',
                                                     view_x, view_y, mid_w, mid_h)

            else:
                # 마지막 조각
                # 1/4 지점부터 끝까지 그리기
                clip_x = RAY_W_H * int(self.laser.frame) + RAY_W_H // 4
                clip_w = int(RAY_W_H * 3 / 4)
                self.laser.image_ray.clip_composite_draw(clip_x, 0, clip_w, RAY_W_H,
                                                     self.laser.angle, '',
                                                     view_x, view_y, end_w, end_h)


class HooverLaser:
    def __init__(self, hoover):
        self.image_ray = load_image('Assets/Sprites/Bullets/DrillingRay.png')
        self.image_ray_spark = load_image('Assets/Sprites/VFX/DrillingFlash.png')
        self.hoover = hoover
        self.x = hoover.player.x
        self.y = hoover.player.y
        self.angle = hoover.angle

        self.frame = 0

        self.radius_min = self.hoover.image_back.w // 2 + 2
        # 충돌 처리용 레이저 사거리
        self.radius_max = self.radius_min + self.hoover.laser_range
        # 화면 표시용 레이저 사거리
        self.radius_display = self.radius_max
        self.shooting = False
        self.penetration = 0
        self.damage = HOOVER_LASER_DAMAGE_PER_TIME

        self.IDLE = ReadyToShoot(self)
        self.SHOOT = Shooting(self)

        self.stateMachine = StateMachine(self.IDLE,
                                         {
                                             self.IDLE: { lambda e: self.shooting and self.hoover.player.engage : self.SHOOT },
                                             self.SHOOT: { lambda e: not self.shooting or not self.hoover.player.engage : self.IDLE }
                                          })

        game_world.add_collision_pair_ray_cast('hoover_laser:tile', self, None)

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        if group == 'hoover_laser:tile':
            distance = math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)
            self.radius_display = int(distance) - TILE_SIZE_PIXEL // 2

            # 충돌 지점에 스파크 효과 추가
            spark_x = self.x + self.radius_display * math.cos(self.angle)
            spark_y = self.y + self.radius_display * math.sin(self.angle)
            vfx_manager.get_vfx_from_pool(VFXHooverLaserHit, spark_x, spark_y, self, 4)

    def handle_none_collision(self, group):
        if group == 'hoover_laser:tile':
            self.radius_display = self.radius_max