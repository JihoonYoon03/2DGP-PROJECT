from pico2d import *

from physics_data import *
from behavior_tree import *
from game_world import get_camera
import game_world
import game_framework
import math
import common
from abc import abstractmethod, ABCMeta

class EnemyBase(metaclass=ABCMeta):
    def __init__(self, x, y, spider, name, frame_data, w, h, frame, frame_count, frame_per_time, draw_angle, flip, state, speed, hp, dmg=0):
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
        self.collision_range = (max(w['Walk'], h['Walk']) - 4) / 2
        self.frame = frame
        self.frame_count = frame_count
        self.frame_per_time = frame_per_time

        self.draw_angle = draw_angle
        self.flip = flip

        self.last_state = state
        self.state = state

        self.tx = 0
        self.ty = 0
        self.speed = speed # m/s
        self.hp = hp
        self.dmg = dmg  # 근접 유닛 데미지(원거리는 총알 데미지로 처리)
        self.attack_collider = None
        self.attacked = False   # 현재 프레임 사이클에서 공격 수행했는지 여부

        self.build_behavior_tree()

    def update(self):
        self.frame = (self.frame + self.frame_per_time[self.state] * game_framework.frame_time) % self.frame_count[self.state]
        if self.last_state != self.state:
            self.frame = 0
            self.last_state = self.state
        if self.attack_collider is not None:
            self.attack_collider.update()

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
        draw_circle(view_x, view_y, int(self.collision_range * camera.zoom), 255, 0, 0)

        if self.attack_collider is not None:
            x, y = self.attack_collider.get_position()
            x, y = camera.world_to_view(x, y)
            r = int(self.attack_collider.collision_range * camera.zoom)
            draw_circle(x, y, r, 255, 0, 0)

    def handle_event(self, event):
        pass

    def get_bb(self):
        pass

    def handle_collision(self, group, other):
        if group == 'spider:enemy_melee':
            if self.attack_collider is not None:
                print('enemy attacking')
                game_world.remove_collision_object(self.attack_collider)
                self.attack_collider = None

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
                'Attack' :( # 60*44
                    (0, 3), (60, 3), (120, 3), (180, 3),
                    (0, 47), (60, 47), (120, 47), (180, 47)
                ),
                'Death' :()
                },

        {'Walk': 40, 'Attack' : 54, 'Death' : 40},
        {'Walk': 40, 'Attack' : 44, 'Death' : 50},

            0,
            {'Walk' : 8, 'Attack' : 8, 'Death': 8},
            {'Walk' : 8, 'Attack' : 8, 'Death': 8},
            math.pi / 2,
            '',

            'Walk',
            2,
            100,
            10
        )

    def target_in_range(self, target, r=0.5):
        if self.distance_less_than(self.x, target.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def attack_target(self):
        self.last_state = self.state
        self.state = 'Attack'  # 디버그 출력
        if int(self.frame) == 0:
            self.attacked = False

        if 4 < self.frame < 5 and not self.attacked: # 공격 프레임에서 데미지 적용
            self.attacked = True
            if self.attack_collider is None:
                self.attack_collider = Collider_range(self, 0, self.collision_range * (-1 if self.flip else 1) , self.collision_range // 2)
                game_world.add_collision_pair_range('spider:enemy_melee', None, self.attack_collider)

        return BehaviorTree.SUCCESS

    def set_target_location(self, target):
        if target is None:
            raise ValueError('목적지가 설정되어야 합니다.')
        self.tx = target.x
        self.ty = target.y
        if self.ty < self.y:
            self.flip = 'h'
        else:
            self.flip = ''
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 <= (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty):
        # 여기를 채우시오.
        distance = self.speed * PIXEL_PER_METER * game_framework.frame_time
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def move_to_target(self, r=0.5):
        if self.distance_less_than(self.x, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        self.last_state = self.state
        self.state = 'Walk' # 디버그 출력
        self.move_little_to(self.x, self.ty) # 목적지로 조금 이동
        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('Target in range', self.target_in_range, self.spider, (self.spider.collision_range - 30 + self.collision_range) / PIXEL_PER_METER)
        a1 = Action('Attack Target', self.attack_target)
        attack = Sequence('Attack', c1, a1)

        a2 = Action('Set Target Location', self.set_target_location, self.spider)
        a3 = Action('Move to Target', self.move_to_target, (self.spider.collision_range - 30 + self.collision_range) / PIXEL_PER_METER)
        chase_target = Sequence('Chase Target', a2, a3)

        root = Selector('Attack or Chase', attack, chase_target)
        self.bt = BehaviorTree(root)