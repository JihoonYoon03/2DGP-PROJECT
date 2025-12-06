from math import degrees

from pico2d import *
from event_set import mouse_motion, mouse_coordinate, mouse_right_pressed, mouse_right_released, mouse_left_pressed, \
    mouse_left_released
from state_machine import StateMachine
from physics_data import *
from VFX import VFXHooverLaserHit
from game_world import get_camera
import common
import math
import game_framework
import game_world
import physics_data as pd

RAY_W_H = 28

class Idle:
    def __init__(self, hoover):
        self.hoover = hoover

    def enter(self, e):
        pass

    def exit(self, e):
        if not self.hoover.player.engage:
            return False
        return True

    def do(self):
        self.hoover.x = self.hoover.player.x
        self.hoover.y = self.hoover.player.y

    def draw(self):
        if self.hoover.player.is_docked:
            return

        camera = get_camera()
        draw_w, draw_h = camera.get_draw_size(self.hoover.image_back.w, self.hoover.image_back.h)
        view_x, view_y = camera.world_to_view(self.hoover.x, self.hoover.y)
        self.hoover.image_back.clip_composite_draw(0, 0, self.hoover.image_back.w, self.hoover.image_back.h,
                                                   self.hoover.draw_angle, self.hoover.is_flip,
                                                  view_x, view_y, draw_w, draw_h)
        self.hoover.image_front.clip_composite_draw(0, 0, self.hoover.image_front.w, self.hoover.image_front.h,
                                                    self.hoover.draw_angle, self.hoover.is_flip,
                                                  view_x, view_y, draw_w, draw_h)

class Vacuum:
    image_vacuum = None
    VACUUM_FRAMES = (
    (0, 0), (60, 0), (120, 0), (180, 0),
    (0, 60), (60, 60), (120, 60), (180, 60),
    (0, 120), (60, 120), (120, 120), (180, 120),
    (0, 180), (60, 180)
    )
    def __init__(self, hoover):
        if Vacuum.image_vacuum is None:
            Vacuum.image_vacuum = load_image('Assets/Sprites/Hoover/ResourceHoover_Sucking.png')
        self.hoover = hoover
        self.frame = 0
        self.w = self.h = 60
        self.frames_per_action = len(Vacuum.VACUUM_FRAMES)
        self.frame_per_time = 1 * self.frames_per_action

    def enter(self, e):
        self.hoover.Vacuuming = True
        pass

    def exit(self, e):
        self.hoover.Vacuuming = False
        return True

    def do(self):
        self.frame = (self.frame + self.frame_per_time * game_framework.frame_time) % self.frames_per_action
        self.hoover.x = self.hoover.player.x
        self.hoover.y = self.hoover.player.y

    def draw(self):
        if self.hoover.player.is_docked:
            return

        camera = get_camera()
        draw_w, draw_h = camera.get_draw_size(self.hoover.image_back.w, self.hoover.image_back.h)
        view_x, view_y = camera.world_to_view(self.hoover.x, self.hoover.y)
        self.hoover.image_back.clip_composite_draw(0, 0, self.hoover.image_back.w, self.hoover.image_back.h,
                                                   self.hoover.draw_angle, self.hoover.is_flip,
                                                  view_x, view_y, draw_w, draw_h)

        clip_x, clip_y = Vacuum.VACUUM_FRAMES[int(self.frame)]
        view_x2 = self.hoover.x + math.cos(self.hoover.angle) * (self.hoover.radius_min + self.w // 3)
        view_y2 = self.hoover.y + math.sin(self.hoover.angle) * (self.hoover.radius_min + self.w // 3)
        view_x2, view_y2 = camera.world_to_view(view_x2, view_y2)
        draw_w2, draw_h2 = camera.get_draw_size(self.w, self.h)
        Vacuum.image_vacuum.clip_composite_draw(clip_x, Vacuum.image_vacuum.h - self.h - clip_y, self.w, self.h,
                                                self.hoover.draw_angle, self.hoover.is_flip,
                                                view_x2, view_y2, draw_w2, draw_h2)

        self.hoover.image_front.clip_composite_draw(0, 0, self.hoover.image_front.w, self.hoover.image_front.h,
                                                    self.hoover.draw_angle, self.hoover.is_flip,
                                                  view_x, view_y, draw_w, draw_h)

        view_x, view_y = camera.world_to_view(self.hoover.player.x, self.hoover.player.y - 20)
        bar_w, bar_h = camera.get_draw_size(36, 8)
        self.hoover.image_bar_back.clip_draw(0, 0, self.hoover.image_bar_back.w, self.hoover.image_bar_back.h,
                                                       view_x, view_y, bar_w, bar_h)

        progress_w = self.hoover.caught_ores / HOOVER_CAPACITY * bar_w
        self.hoover.image_bar_progress.clip_draw(0, 0, self.hoover.image_bar_progress.w, self.hoover.image_bar_progress.h,
                                                       view_x - (bar_w - progress_w) / 2, view_y, progress_w, bar_h)

        self.hoover.image_bar_front.clip_draw(0, 0, self.hoover.image_bar_front.w, self.hoover.image_bar_front.h,
                                                       view_x, view_y, bar_w, bar_h)

class Drilling:
    def __init__(self, hoover):
        self.hoover = hoover
        self.frames_per_action = 5
        self.frame = 0
        self.action_per_time = get_hoover_laser_action_per_time(self.frames_per_action)

    def enter(self, e):
        self.hoover.shooting = True

    def exit(self, e):
        self.hoover.shooting = False
        return True

    def do(self):
        self.frame = ((self.frame + self.frames_per_action * self.action_per_time * game_framework.frame_time)
                            % self.frames_per_action)
        self.hoover.x = self.hoover.player.x
        self.hoover.y = self.hoover.player.y

    def draw(self):
        camera = get_camera()
        draw_w, draw_h = camera.get_draw_size(self.hoover.image_back.w, self.hoover.image_back.h)
        view_x, view_y = camera.world_to_view(self.hoover.x, self.hoover.y)
        self.hoover.image_back.clip_composite_draw(0, 0, self.hoover.image_back.w, self.hoover.image_back.h,
                                                   self.hoover.draw_angle, self.hoover.is_flip,
                                                  view_x, view_y, draw_w, draw_h)

        mid_w, mid_h = camera.get_draw_size(RAY_W_H // 2, RAY_W_H)
        end_w, end_h = camera.get_draw_size(RAY_W_H * (3 / 4), RAY_W_H)

        for dr in range(self.hoover.radius_min, self.hoover.radius_display, RAY_W_H // 2):
            x = dr * math.cos(self.hoover.angle)
            y = dr * math.sin(self.hoover.angle)

            view_x, view_y = camera.world_to_view(self.hoover.x + x, self.hoover.y + y)

            if dr == self.hoover.radius_min:
                # 첫 조각
                # 처음부터 3/4 지점까지 그리기
                clip_x = RAY_W_H * int(self.frame)
                clip_w = int(RAY_W_H * 3 / 4)
                self.hoover.image_ray.clip_composite_draw(clip_x, 0, clip_w, RAY_W_H,
                                                     self.hoover.draw_angle, self.hoover.is_flip,
                                                     view_x, view_y, end_w, end_h)

            elif (dr + RAY_W_H - RAY_W_H // 2) < self.hoover.radius_max:
                # 중간 조각
                # 1/4 지점부터 3/4 지점까지 그리기
                clip_x = RAY_W_H * int(self.frame) + RAY_W_H // 4
                clip_w = RAY_W_H // 2
                self.hoover.image_ray.clip_composite_draw(clip_x, 0, clip_w, RAY_W_H,
                                                     self.hoover.draw_angle, self.hoover.is_flip,
                                                     view_x, view_y, mid_w, mid_h)

            else:
                # 마지막 조각
                # 1/4 지점부터 끝까지 그리기
                clip_x = RAY_W_H * int(self.frame) + RAY_W_H // 4
                clip_w = int(RAY_W_H * 3 / 4)
                self.hoover.image_ray.clip_composite_draw(clip_x, 0, clip_w, RAY_W_H,
                                                     self.hoover.draw_angle, self.hoover.is_flip,
                                                     view_x, view_y, end_w, end_h)

        view_x, view_y = camera.world_to_view(self.hoover.x, self.hoover.y)
        self.hoover.image_front.clip_composite_draw(0, 0, self.hoover.image_front.w, self.hoover.image_front.h,
                                                    self.hoover.draw_angle, self.hoover.is_flip,
                                                  view_x, view_y, draw_w, draw_h)

class Hoover:
    def __init__(self, player):
        self.image_back = load_image('Assets/Sprites/Hoover/ResourceHoover_lvl1_Back.png')
        self.image_front = load_image('Assets/Sprites/Hoover/ResourceHoover_lvl1_Front.png')
        self.image_ray = load_image('Assets/Sprites/Bullets/DrillingRay.png')
        self.image_ray_spark = load_image('Assets/Sprites/VFX/DrillingFlash.png')
        self.image_bar_back = load_image('Assets/Sprites/UI/ResourceHoover_UI_Bar_Back.png')
        self.image_bar_front = load_image('Assets/Sprites/UI/ResourceHoover_UI_Bar_Front.png')
        self.image_bar_progress = load_image('Assets/Sprites/UI/ResourceHoover_UI_Bar_Progress.png')

        self.player = player
        self.x = player.x
        self.y = player.y
        self.angle = 0
        self.draw_angle = 0
        self.is_flip = ''

        self.laser_range = TILE_SIZE_PIXEL * 2
        self.radius_min = self.image_back.w // 2
        self.radius_max = self.radius_min + self.laser_range
        self.radius_vacuum = self.radius_min + self.laser_range
        self.degree_start = -50
        self.degree_end = 50
        self.range_inner_offset = (0, 0)
        self.caught_ores = 0
        self.res_amount = {
                0 : 0,
                1 : 0,
                2 : 0,
                3 : 0,
                4 : 0,
                5 : 0,
                6 : 0,
                7 : 0,
                8 : 0,
            }

        # 화면 표시용 레이저 사거리
        self.radius_display = self.radius_max
        self.damage = HOOVER_LASER_DAMAGE_PER_TIME * pd.UPGRADE_LASER_DAMAGE_PERCENT + pd.UPGRADE_LASER_DAMAGE
        self.penetration = 0
        self.Vacuuming = False
        self.shooting = False
        self.collide = False

        self.IDLE = Idle(self)
        self.VACUUM = Vacuum(self)
        self.DRILL = Drilling(self)

        self.stateMachine = StateMachine(self.IDLE,
                                         {
                                             self.IDLE: { mouse_motion : self.IDLE, mouse_right_pressed : self.VACUUM, mouse_left_pressed : self.DRILL },
                                             self.VACUUM: { mouse_motion : self.VACUUM, mouse_right_released : self.IDLE },
                                             self.DRILL : { mouse_motion : self.DRILL, mouse_left_released : self.IDLE, lambda e : not self.player.engage : self.IDLE }
                                          })

        self.collision_range = self.radius_vacuum
        game_world.add_collision_pair_ray_cast('hoover_laser:tile', self, None)
        game_world.add_collision_pair_radius_limited('ore:hoover_vacuum', None, self, self.radius_vacuum)

    def update(self):
        self.stateMachine.update()
        self.damage = HOOVER_LASER_DAMAGE_PER_TIME * pd.UPGRADE_LASER_DAMAGE_PERCENT + pd.UPGRADE_LASER_DAMAGE

    def draw(self):
        if common.player.is_docked or common.spider.stateMachine.cur_state == common.spider.DEATH and not common.player.engage:
            return
        self.stateMachine.draw()
        if common.debug_mode:
            view_x, view_y = common.cam.world_to_view(self.x, self.y)
            draw_circle(view_x, view_y, int(common.cam.value_to_view(self.radius_vacuum)), 100, 255, 0)

    def handle_event(self, event):
        if mouse_motion(('INPUT', event)):
            mouse_x, mouse_y = mouse_coordinate((None, event))
            camera = get_camera()
            view_x, view_y = camera.world_to_view(self.x, self.y)
            dx = mouse_x - view_x
            dy = mouse_y - view_y
            da = math.atan2(dy, dx) - self.angle
            self.angle += da
            self.degree_start += degrees(da)
            self.degree_end += degrees(da)
            self.draw_angle = self.angle
            if abs(self.draw_angle) > math.pi / 2:
                self.draw_angle += math.pi
                self.is_flip = 'h'
            else:
                self.is_flip = ''

        # 자원 수집 처리
        if not self.player.engage:
            if self.caught_ores > 0:
                common.spider.gather_resources(self.res_amount)
                self.caught_ores = 0
                for key in self.res_amount.keys():
                    self.res_amount[key] = 0

        self.stateMachine.handle_state_event(('INPUT', event))

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        if group == 'hoover_laser:tile':
            self.collide = True
            distance = math.sqrt((other.x - self.player.x) ** 2 + (other.y - self.player.y) ** 2)
            self.radius_display = int(distance) - TILE_SIZE_PIXEL // 2

            # 충돌 지점에 스파크 효과 추가
            spark_x = self.player.x + self.radius_display * math.cos(self.angle)
            spark_y = self.player.y + self.radius_display * math.sin(self.angle)
            common.obj_pool.get_object(VFXHooverLaserHit, spark_x, spark_y, self, 4, **{'unique_key': self})

        elif group == 'ore:hoover_vacuum':
            ore = other[0]
            distance = math.sqrt((ore.x - self.player.x) ** 2 + (ore.y - self.player.y) ** 2)
            overlap = self.radius_min + ore.collision_range - distance
            if overlap > 0 and self.Vacuuming and self.caught_ores < HOOVER_CAPACITY:
                self.res_amount[ore.res_type] += 1
                self.caught_ores += 1
                ore.caught_by_hoover(self)

    def handle_none_collision(self, group):
        if group == 'hoover_laser:tile':
            self.collide = False
            self.radius_display = self.radius_max