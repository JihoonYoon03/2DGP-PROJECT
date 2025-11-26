from pico2d import *

from physics_data import *
from behavior_tree import *
from game_world import get_camera
import game_framework
import math
import common
from abc import abstractmethod, ABCMeta

class EnemyBase(metaclass=ABCMeta):
    def __init__(self, x, y, spider, name, frame_data, w, h, frame, frame_count, frame_per_time, draw_angle, flip, state, speed, hp):
        self.x = x
        self.y = y
        self.spider = spider
        self.name = name

        self.image ={   'Walk' : load_image('Assets/Sprites/Zyrex/' + name + 'WalkTileset.png'),
                        'Attack' : load_image('Assets/Sprites/Zyrex/' + name + 'AttackTileset.png'),
                        'Death' : load_image('Assets/Sprites/Zyrex/' + name + 'DeathTileset.png')
                    }
        self.frame_data = frame_data
        self.w = w
        self.h = h
        self.frame = frame
        self.frame_count = frame_count
        self.frame_per_time = frame_per_time

        self.draw_angle = draw_angle
        self.flip = flip

        self.state = state

        self.tx = 0
        self.ty = 0
        self.speed = speed # m/s
        self.hp = hp

        self.build_behavior_tree()

    def update(self):
        self.frame = (self.frame + self.frame_per_time[self.state] * game_framework.frame_time) % self.frame_count[self.state]
        self.bt.run()

    def draw(self):
        camera = get_camera()
        clip_x, clip_y = self.frame_data[self.state][int(self.frame)]
        view_x, view_y = camera.world_to_view(self.x, self.y)
        draw_w, draw_h = camera.get_draw_size(self.w[self.state], self.h[self.state])
        if not camera.draw_clipping(view_x, view_y, draw_w, draw_h):
            self.image[self.state].clip_composite_draw(clip_x, self.image[self.state].h - self.h[self.state] - clip_y,
                                                       self.w[self.state], self.h[self.state],
                                                       self.draw_angle, self.flip,
                                                       view_x, view_y,
                                                       draw_w, draw_h)

    def handle_event(self, event):
        pass

    def get_bb(self):
        pass

    def handle_collision(self, other, group):
        pass

    @abstractmethod
    def build_behavior_tree(self):
        pass

class InfantryTier0(EnemyBase):
    def __init__(self, x, y, spider):
        super().__init__(
            x, y, spider,'Infantry',

    {'Walk' :(
                (0, 0), (40, 0), (80, 0),
                (0, 40), (40, 40), (80, 40),
                (0, 80), (40, 80), (80, 80)
                ),
                'Attack' :(),
                'Death' :()
                },

        {'Walk': 40, 'Attack' : 60, 'Death' : 40},
        {'Walk': 40, 'Attack' : 46, 'Death' : 50},

            0,
            {'Walk' : 8, 'Attack' : 8, 'Death': 8},
            {'Walk' : 8, 'Attack' : 8, 'Death': 8},
            0,
            '',

            'Walk',
            2,
            0
        )
        # self.draw_angle = math.pi / 2

    def target_in_range(self):
        pass

    def attack_target(self):
        pass

    def set_target_location(self):
        self.tx = self.spider.x
        self.ty = self.spider.y

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty):
        # 여기를 채우시오.
        distance = self.speed * PIXEL_PER_METER * game_framework.frame_time
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def move_to_target(self, r=0.5):
        self.state = 'Walk' # 디버그 출력
        self.move_little_to(self.tx, self.ty) # 목적지로 조금 이동
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('Target in range', self.target_in_range)
        a1 = Action('Attack Target', self.attack_target)
        attack_target = Sequence('Attack Target', c1, a1)

        a2 = Action('Set Target Location', self.set_target_location)
        a3 = Action('Move to Target', self.move_to_target)
        chase_target = Sequence('Chase Target', a2, a3)

        # root = Selector('Attack or Chase', attack_target, chase_target)
        root = chase_target
        self.bt = BehaviorTree(root)