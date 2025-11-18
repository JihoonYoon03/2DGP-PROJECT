from pico2d import *
import event_set
from event_set import mouse_motion, mouse_coordinate
from game_world import get_camera
from state_machine import StateMachine
from physics_data import *
import math
import game_framework
import game_world

class Idle:
    def __init__(self, hoover):
        self.hoover = hoover
        self.is_flip = ''

    def enter(self, e):
        if mouse_motion(e):
            mouse_x, mouse_y = mouse_coordinate(e)
            camera = get_camera()
            view_x, view_y = camera.world_to_view(self.hoover.player.x, self.hoover.player.y)
            dx = mouse_x - view_x
            dy = mouse_y - view_y
            self.hoover.angle = math.atan2(dy, dx)
            if abs(self.hoover.angle) > math.pi / 2:
                self.hoover.angle += math.pi
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
                                                   self.hoover.angle, self.is_flip,
                                                  view_x, view_y, draw_w, draw_h)
        self.hoover.image_front.clip_composite_draw(0, 0, self.hoover.image_front.w, self.hoover.image_front.h,
                                                    self.hoover.angle, self.is_flip,
                                                  view_x, view_y, draw_w, draw_h)


class Hoover:
    def __init__(self, player):
        self.image_back = load_image('Assets/Sprites/Hoover/ResourceHoover_lvl1_Back.png')
        self.image_front = load_image('Assets/Sprites/Hoover/ResourceHoover_lvl1_Front.png')

        self.player = player
        self.angle = 0
        self.shooting = False
        self.laser_range = TILE_SIZE_PIXEL * 2

        self.IDLE = Idle(self)

        self.stateMachine = StateMachine(self.IDLE,
                                         {
                                             self.IDLE: { mouse_motion : self.IDLE }
                                          })

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))

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


class HooverLaser:
    def __init__(self, hoover):
        self.image_ray = load_image('Assets/Sprites/Bullets/DrillingRay')
        self.image_ray_spark = load_image('Assets/Sprites/VFX/DrillingFlash.png')
        self.hoover = hoover

        self.frame = 0

        self.IDLE = ReadyToShoot(self)
        self.SHOOT = Shooting(self)

        self.stateMachine = StateMachine(self.IDLE,
                                         {
                                             self.IDLE: { lambda e: self.hoover.shooting : self.SHOOT },
                                             self.SHOOT: { lambda e: not self.hoover.shooting : self.IDLE }
                                          })
    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        self.stateMachine.handle_state_event(('INPUT', event))

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        pass