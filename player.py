from pico2d import *
from event_set import *
from game_world import get_camera


class Player:
    def __init__(self, robo_spider):
        self.image_idle = load_image('Assets/Sprites/Player/Hero_Idle.png')
        self.image_move_right = load_image('Assets/Sprites/Player/Hero_Right_Moving.png')
        self.image_move_up = load_image('Assets/Sprites/Player/Hero_Up_Moving.png')
        self.image_move_down = load_image('Assets/Sprites/Player/Hero_Down_Moving.png')

        self.is_docked = True
        self.x = robo_spider.x
        self.y = robo_spider.y
        self.face_dir = 0 # 1: right, -1: left, 2: up, -2: down
        self.move_x = 0
        self.move_y = 0

        self.robo_spider = robo_spider

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass