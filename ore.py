from pico2d import *
from pygame.draw import circle

from physics_data import *
from state_machine import StateMachine
from game_world import get_camera
import game_framework
import game_world

class Idle:
    def __init__(self, ore):
        self.ore = ore

    def enter(self, event):
        pass

    def exit(self, event):
        return True

    def do(self):
        self.ore.vx += self.ore.ax * game_framework.frame_time
        self.ore.vy += self.ore.ay * game_framework.frame_time
        self.ore.vy -= GRAVITY * game_framework.frame_time
        if self.ore.vy > MAX_ORE_FALLING_SPEED:
            self.ore.vy = MAX_ORE_FALLING_SPEED
        self.ore.x += self.ore.vx * game_framework.frame_time
        self.ore.y += self.ore.vy * game_framework.frame_time

    def draw(self):
        camera = get_camera()
        view_x, view_y = camera.world_to_view(self.ore.x, self.ore.y)
        draw_w, draw_h = camera.get_draw_size(self.ore.w, self.ore.h)
        self.ore.image.clip_draw(0, 0, self.ore.w, self.ore.h,
                                                   view_x, view_y, draw_w, draw_h)

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
        self.ax = 0.0
        self.ay = 0.0
        self.vx = 0.0
        self.vy = -GRAVITY * 0.5  # 약간 떨어지면서 시작
        self.ore_type = ore_type

        self.image = Ore.image_ore[self.ore_type]
        self.w = Ore.image_ore[self.ore_type].w
        self.h = Ore.image_ore[self.ore_type].h

        self.IDLE = Idle(self)
        self.stateMachine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {}
            })

        self.collision_range = min(self.image.w, self.image.h) / 1.2
        game_world.add_collision_pair_bb('ore:tile', self, None)
        game_world.add_collision_pair_range('ore:ore', self, self)

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

        camera = get_camera()
        x1 = self.x - self.collision_range / 2
        y1 = self.y - self.collision_range / 2
        x2 = self.x + self.collision_range / 2
        y2 = self.y + self.collision_range / 2
        view_x1, view_y1 = camera.world_to_view(x1, y1)
        view_x2, view_y2 = camera.world_to_view(x2, y2)
        draw_rectangle(view_x1, view_y1, view_x2, view_y2)

    def handle_event(self, event):
        # self.stateMachine.handle_state_event(('INPUT', event))
        pass

    def get_bb(self):
        half_w = Ore.image_ore[self.ore_type].w // 2
        half_h = Ore.image_ore[self.ore_type].h // 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        if group == 'ore:tile':
            tile_left = other.x - TILE_SIZE_PIXEL // 2
            tile_right = other.x + TILE_SIZE_PIXEL // 2
            tile_top = other.y + TILE_SIZE_PIXEL // 2
            tile_bottom = other.y - TILE_SIZE_PIXEL // 2

            half_w = self.w // 2
            half_h = self.h // 2

            prev_x = self.x - self.vx * game_framework.frame_time
            prev_y = self.y - self.vy * game_framework.frame_time

            dx = self.x - prev_x
            dy = self.y - prev_y

            # 충돌 축 결정
            if abs(dy) > abs(dx):
                if self.vy < 0:  # 아래로 떨어지는 중
                    self.y = tile_top + half_h
                else:  # 위로 올라가는 중
                    self.y = tile_bottom - half_h
                self.vy = 0
                self.ay = 0
            else:
                if self.vx > 0:  # 오른쪽 이동 중
                    self.x = tile_left - half_w
                else:  # 왼쪽 이동 중
                    self.x = tile_right + half_w
                self.vx = 0
                self.ax = 0

        elif group == 'ore:ore':
            dx = self.x - other.x
            dy = self.y - other.y

            dist = math.hypot(dx, dy)
            min_dist = (self.collision_range + other.collision_range) // 2  # 충돌범위 합

            if dist == 0:
                # 완전히 겹친 경우 임의 방향으로 분리
                dx, dy = 1, 0
                dist = 1

            # 겹침 정도
            overlap = min_dist - dist
            if overlap > 0:
                # 겹친 만큼 반씩 밀어냄
                self.x += (dx / dist) * (overlap / 2)
                self.y += (dy / dist) * (overlap / 2)

                # 반대쪽 ore는 자기 핸들러에서 처리

                self.vx = 0
                self.vy = 0
                self.ax = 0
                self.ay = 0