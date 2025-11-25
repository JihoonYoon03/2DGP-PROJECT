from pico2d import *
from physics_data import *
from behavior_tree import *
import math
from abc import abstractmethod, ABCMeta

class EnemyBase(metaclass=ABCMeta):
    def __init__(self, name):
        self.x = 0
        self.y = 0
        self.name = name

        self.image_walk = load_image('Assets/Sprites/Zyrex/' + name + 'WalkTileset.png')
        self.image_attack = load_image('Assets/Sprites/Zyrex/' + name + 'AttackTileset.png')
        self.image_death = load_image('Assets/Sprites/Zyrex/' + name + 'DeathTileset.png')
        self.w = [0, 0, 0]
        self.h = [0, 0, 0]
        self.frame = 0
        self.frame_count = [0, 0, 0] # 걷기, 공격, 죽기
        self.frame_per_time = [0, 0, 0]
        self.draw_angle = 0
        self.flip = ''
        self.state = 'Walk'

        self.tx = 0
        self.ty = 0
        self.speed = 0
        self.hp = 0

        self.build_behavior_tree()

    def update(self):
        self.bt.run()

    def draw(self):
        pass

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
        self.w = [41, 60, 40]
        self.h = [41, 46, 50]

        self.frame = 0
        self.frame_count = [8, 8, 8] # 걷기, 공격, 죽기
        self.frame_per_time = [4, 4, 4]
        self.draw_angle = math.pi / 2
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