from pico2d import *
import behavior_tree

class EnemyBase:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.name = ''
        self.image_walk = load_image('Assets/Sprites/Zyrex/' + self.name + 'WalkTileset.png')
        self.image_attack = load_image('Assets/Sprites/Zyrex/' + self.name + 'AttackTileset.png')
        self.image_death = load_image('Assets/Sprites/Zyrex/' + self.name + 'DeathTileset.png')
        self.frame = 0
        self.frame_count = [0, 0, 0] # 걷기, 공격, 죽기
        self.frame_per_time = [0, 0, 0]

        self.set_behavior_tree()

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

    def set_behavior_tree(self):
        pass