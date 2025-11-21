from pico2d import *
from physics_data import *
from state_machine import StateMachine

class Idle:
    def __init__(self, ore):
        self.ore = ore

    def enter(self, event):
        pass

    def exit(self, event):
        return True

    def do(self):
        pass

    def draw(self):
        self.ore.draw()

class Ore:
    image_ore = list()
    def __init__(self, x, y, ore_type):
        if len(Ore.image_ore) == 0:
            Ore.image_ore.append(load_image('Assets/Sprites/Item/CommonResource_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes1_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes2_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes3_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes4_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes5_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes6_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes7_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes8_Item.png'))

        # ore 드롭 위치
        self.x = x
        self.y = y

        self.dir_vector = (0, 0)
        self.acceleration = 0.0
        self.velocity = 0.0
        self.ore_type = ore_type

        self.IDLE = Idle(self)
        self.stateMachine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {}
            })

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        # self.stateMachine.handle_state_event(('INPUT', event))
        pass

    def get_bb(self):
        half_w = Ore.image_ore[self.ore_type].w // 2
        half_h = Ore.image_ore[self.ore_type].h // 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        pass