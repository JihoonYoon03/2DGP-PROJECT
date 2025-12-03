import math


PIXEL_PER_METER = 20.0  # 20 pixel / 1m

GRAVITY = 9.81 * PIXEL_PER_METER

SPIDER_RUN_SPEED_KMPH = 18.0 # Km / Hour
SPIDER_RUN_SPEED_PPS = (SPIDER_RUN_SPEED_KMPH * 1000.0 / 3600.0) * PIXEL_PER_METER

SPIDER_BASE_FRAMES = 16
SPIDER_BASE_ACTION_PER_TIME = SPIDER_RUN_SPEED_KMPH / SPIDER_BASE_FRAMES

SPIDER_BASE_HP = 1000.0 # 기본 체력바 크기
SPIDER_MAX_HP = 1000.0
SPIDER_BASE_SHIELD = 500.0  # 기본 실드바 크기
SPIDER_MAX_SHIELD = 500.0

SPIDER_TURRET_ROTATE_SPEED = 75.0  # 도 단위 / 초

MACHINE_GUN_BULLET_SPEED_MPS = 20.0
MACHINE_GUN_BULLET_DAMAGE = 12.0
MACHINE_GUN_FIRE_RATE = 0.25  # 초 단위
MACHINE_GUN_SPREAD_RAD = 5.0 * math.pi / 180  # 라디안 단위

WAVE_BASE_TIME = 30.0  # 초 단위
WAVE_MAX_TIME = 30.0

PLAYER_RUN_SPEED_KMPH = 14.0  # Km / Hour
PLAYER_RUN_SPEED_PPS = (PLAYER_RUN_SPEED_KMPH * 1000.0 / 3600.0) * PIXEL_PER_METER

PLAYER_BASE_FRAMES = 13
PLAYER_BASE_ACTION_PER_TIME = PLAYER_RUN_SPEED_KMPH / PLAYER_BASE_FRAMES

HOOVER_VACUUM_POWER = 12000
HOOVER_VACUUM_DAMPING = 1.005
HOOVER_CAPACITY = 20
HOOVER_LASER_BASE_FRAMES = 5
HOOVER_LASER_BASE_ACTION_PER_TIME = 2.0
HOOVER_LASER_DAMAGE_PER_TIME = 100

SPITTER_ATTACK_RANGE = 30  # 공격 사거리, m
SPITTER_ATTACK_COUNT = 3    # 공격 횟수

TILE_SIZE_PIXEL = 40
TILE_W_H = 60
TILE_HP_MIN = 100

MAX_ORE_FALLING_SPEED = GRAVITY
ORE_RESTITUTION = 0.1 # 광석 튕김(반발) 계수
ORE_MASS = 0.5  # 광석 질량
ORE_FRICTION = 0.99  # 광석 마찰 계수

WIN_WIDTH = 1200
WIN_HEIGHT = 800

def get_spider_action_per_time(frame_count):
    return (SPIDER_BASE_FRAMES / frame_count) * SPIDER_BASE_ACTION_PER_TIME

def get_player_action_per_time(frame_count):
    return (PLAYER_BASE_FRAMES / frame_count) * PLAYER_BASE_ACTION_PER_TIME

def get_hoover_laser_action_per_time(frame_count):
    return (HOOVER_LASER_BASE_FRAMES / frame_count) * HOOVER_LASER_BASE_ACTION_PER_TIME

class Collider_bb:
    def __init__(self, owner, offset_x, offset_y, width, height):
        self.owner = owner
        self.x = owner.x + offset_x
        self.y = owner.y + offset_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.w = width
        self.h = height

    def get_bb(self):
        x, y = self.owner.x + self.offset_x, self.owner.y + self.offset_y
        return (self.x - self.w // 2,
                self.y - self.h // 2,
                self.x + self.w // 2,
                self.y + self.h // 2)

    def update(self):
        self.x = self.owner.x + self.offset_x
        self.y = self.owner.y + self.offset_y

    def handle_collision(self, group, other):
        self.owner.handle_collision(group, other)

class Collider_range:
    def __init__(self, owner, offset_x, offset_y, radius):
        self.owner = owner
        self.x = owner.x + offset_x
        self.y = owner.y + offset_y
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.collision_range = radius

    def get_position(self):
        return self.x, self.y

    def update(self):
        self.x = self.owner.x + self.offset_x
        self.y = self.owner.y + self.offset_y

    def handle_collision(self, group, other):
        self.owner.handle_collision(group, other)
