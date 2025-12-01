from pico2d import *
from physics_data import *
from game_world import get_camera
from abc import ABCMeta
import game_framework


class Projectile(metaclass=ABCMeta):
    image = { 'MachineGun' : load_image('Assets/Sprites/Bullets/Bullet_MachineGun.png')
              }
    def __init__(self, x, y, degree, vx, vy, velocity, weapon_type):
        self.type = weapon_type
        self.inactive = True
        self.x = x
        self.y = y
        self.degree = degree
        self.vx = vx
        self.vy = vy
        self.velocity = velocity

        self.w = Projectile.image[self.type].w
        self.h = Projectile.image[self.type].h
        self.collision_range = (max(self.w, self.h) - 4) / 2

    def update(self):
        self.x += self.vx * self.velocity * game_framework.frame_time
        self.y += self.vy * self.velocity * game_framework.frame_time
        # 일정 범위 밖으로 나가면 비활성화
        if abs(self.x) > PIXEL_PER_METER * 1000 + self.w or abs(self.y) > PIXEL_PER_METER * 1000 + self.h:
            self.inactive = True

    def draw(self):
        camera = get_camera()
        view_x, view_y = camera.world_to_view(self.x, self.y)
        draw_w, draw_h = camera.get_draw_size(self.w, self.h)
        if not camera.draw_clipping(view_x, view_y, draw_w, draw_h):
            Projectile.image[self.type].clip_composite_draw(0, 0, self.w, self.h,
                                                           math.radians(self.degree), '',
                                                           view_x, view_y, draw_w, draw_h)

    def get_bb(self):
        pass

    def get_position(self):
        return self.x, self.y

    def get_collision_range(self):
        return self.collision_range

class MachineGunProjectile(Projectile):
    def __init__(self, x, y, degree):
        vx = math.cos(math.radians(degree))
        vy = math.sin(math.radians(degree))

        normalizing = math.sqrt(vx * vx + vy * vy)
        vx /= normalizing
        vy /= normalizing

        velocity = MACHINE_GUN_BULLET_SPEED_MPS * PIXEL_PER_METER

        super().__init__(x, y, degree, vx, vy, velocity, 'MachineGun')

    def handle_collision(self, group, other):
        if group == 'MachineGun:enemy':
            self.inactive = True