from pico2d import *
from physics_data import *
from game_world import get_camera
from abc import ABCMeta
import game_framework
import game_world
import math
import random


class Projectile(metaclass=ABCMeta):
    image = dict()
    def __init__(self, x, y, rad, vx, vy, velocity, weapon_type, dmg):
        if len(Projectile.image) == 0:
            Projectile.image.setdefault(weapon_type, load_image('Assets/Sprites/Bullets/Bullet_MachineGun.png'))
        self.type = weapon_type
        self.inactive = False
        self.x = x
        self.y = y
        self.rad = rad
        self.vx = vx
        self.vy = vy
        self.velocity = velocity
        self.layer = 2

        self.dmg = dmg

        self.w = Projectile.image[self.type].w
        self.h = Projectile.image[self.type].h
        self.collision_range = (max(self.w, self.h) - 4) / 2

    def update(self):
        if self.inactive:
            return
        self.x += self.vx * self.velocity * game_framework.frame_time
        self.y += self.vy * self.velocity * game_framework.frame_time
        # 일정 범위 밖으로 나가면 비활성화
        if abs(self.x) > PIXEL_PER_METER * 200 + self.w or abs(self.y) > PIXEL_PER_METER * 200 + self.h:
            self.inactive = True
            print('Projectile deactivated due to out of bounds.')

    def draw(self):
        if self.inactive:
            return
        camera = get_camera()
        view_x, view_y = camera.world_to_view(self.x, self.y)
        draw_w, draw_h = camera.get_draw_size(self.w, self.h)
        if not camera.draw_clipping(view_x, view_y, draw_w, draw_h):
            Projectile.image[self.type].clip_composite_draw(0, 0, self.w, self.h,
                                                           self.rad, 'h',
                                                           view_x, view_y, draw_w, draw_h)

    def get_bb(self):
        pass

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass

class MachineGunProjectile(Projectile):
    def __init__(self, x, y, rad):
        r = rad + random.uniform(-MACHINE_GUN_SPREAD_RAD, MACHINE_GUN_SPREAD_RAD)
        vx = math.cos(r)
        vy = math.sin(r)

        normalizing = math.sqrt(vx * vx + vy * vy)
        vx /= normalizing
        vy /= normalizing

        velocity = MACHINE_GUN_BULLET_SPEED_MPS * PIXEL_PER_METER

        super().__init__(x, y, r, vx, vy, velocity, 'MachineGun', MACHINE_GUN_BULLET_DAMAGE)

        game_world.add_collision_pair_range('Machine_gun_bullet:enemy', self, None)

    def handle_collision(self, group, other):
        if group == 'Machine_gun_bullet:enemy':
            game_world.remove_collision_object(self)
            self.inactive = True


    def reactivate(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad + random.uniform(-MACHINE_GUN_SPREAD_RAD, MACHINE_GUN_SPREAD_RAD)
        self.vx = math.cos(self.rad)
        self.vy = math.sin(self.rad)
        normalizing = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        self.vx /= normalizing
        self.vy /= normalizing
        game_world.add_collision_pair_range('Machine_gun_bullet:enemy', self, None)
        self.inactive = False

class SpitterShot(Projectile):
    def __init__(self, x, y, rad):
        vx = math.cos(rad)
        vy = math.sin(rad)

        normalizing = math.sqrt(vx * vx + vy * vy)
        vx /= normalizing
        vy /= normalizing

        velocity = MACHINE_GUN_BULLET_SPEED_MPS * PIXEL_PER_METER

        super().__init__(x, y, rad, vx, vy, velocity, 'MachineGun', MACHINE_GUN_BULLET_DAMAGE)

        game_world.add_collision_pair_range('Spitter_shot:spider', self, None)

    def handle_collision(self, group, other):
        if group == 'Spitter_shot:spider':
            game_world.remove_collision_object(self)
            self.inactive = True


    def reactivate(self, x, y, rad):
        self.x = x
        self.y = y
        self.rad = rad + random.uniform(-MACHINE_GUN_SPREAD_RAD, MACHINE_GUN_SPREAD_RAD)
        self.vx = math.cos(self.rad)
        self.vy = math.sin(self.rad)
        normalizing = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        self.vx /= normalizing
        self.vy /= normalizing
        game_world.add_collision_pair_range('Spitter_shot:enemy', self, None)
        self.inactive = False