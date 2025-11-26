from pico2d import *
from physics_data import *
from behavior_tree import *
from game_world import get_camera
import game_framework
import math
from abc import abstractmethod, ABCMeta

class EnemyBase(metaclass=ABCMeta):
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.name = name

        self.image ={   'Walk' : load_image('Assets/Sprites/Zyrex/' + name + 'WalkTileset.png'),
                        'Attack' : load_image('Assets/Sprites/Zyrex/' + name + 'AttackTileset.png'),
                        'Death' : load_image('Assets/Sprites/Zyrex/' + name + 'DeathTileset.png')
                    }
        self.frame_data ={ 'Walk' : (),
                           'Attack' : (),
                            'Death': ()
                        }
        self.w = {'Walk' : 0, 'Attack' : 0, 'Death': 0}
        self.h = {'Walk' : 0, 'Attack' : 0, 'Death': 0}
        self.frame = 0
        self.frame_count = {'Walk' : 0, 'Attack' : 0, 'Death': 0} # 걷기, 공격, 죽기
        self.frame_per_time = {'Walk' : 0, 'Attack' : 0, 'Death': 0}
        self.draw_angle = 0
        self.flip = ''
        self.state = 'Walk'

        self.tx = 0
        self.ty = 0
        self.speed = 0
        self.hp = 0

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
    def __init__(self, x, y):
        super().__init__('Infantry')
        self.x = x
        self.y = y

        self.frame_data['Walk'] += (
            (0, 0), (40, 0), (80, 0),
            (0, 40), (40, 40), (80, 40),
            (0, 80), (40, 80), (80, 80)
        )
        self.w['Walk'] = 40
        self.w['Attack'] = 60
        self.w['Death'] = 40

        self.h['Walk'] = 40
        self.h['Attack'] = 46
        self.h['Death'] = 50

        self.frame = 0

        for key in self.frame_count.keys():
            self.frame_count[key] = 8
            self.frame_per_time[key] = 8

        # self.draw_angle = math.pi / 2
        self.flip = ''

        self.speed = PIXEL_PER_METER

    def target_in_range(self):
        pass

    def attack_target(self):
        pass

    def set_target_location(self):
        pass

    def move_to_target(self):
        pass

    def build_behavior_tree(self):
        c1 = Condition('Target in range', self.target_in_range)
        a1 = Action('Attack Target', self.attack_target)
        attack_target = Sequence('Attack Target', c1, a1)

        a2 = Action('Set Target Location', self.set_target_location)
        a3 = Action('Move to Target', self.move_to_target)
        chase_target = Sequence('Chase Target', a1, a2)

        root = Selector('Attack or Chase', attack_target, chase_target)
        self.bt = BehaviorTree(root)