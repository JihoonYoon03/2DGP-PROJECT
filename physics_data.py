from game_world import get_camera

PIXEL_PER_METER = 20.0  # 20 pixel / 1m

SPIDER_RUN_SPEED_KMPH = 20.0 # Km / Hour
SPIDER_RUN_SPEED_PPS = (SPIDER_RUN_SPEED_KMPH * 1000.0 / 3600.0) * PIXEL_PER_METER

SPIDER_BASE_FRAMES = 16
SPIDER_BASE_ACTION_PER_TIME = 1.0

PLAYER_RUN_SPEED_KMPH = 12.0  # Km / Hour
PLAYER_RUN_SPEED_PPS = (PLAYER_RUN_SPEED_KMPH * 1000.0 / 3600.0) * PIXEL_PER_METER

PLAYER_BASE_FRAMES = 13
PLAYER_BASE_ACTION_PER_TIME = 1.0

HOOVER_LASER_BASE_FRAMES = 5
HOOVER_LASER_BASE_ACTION_PER_TIME = 2.0
HOOVER_LASER_DAMAGE_PER_TIME = 80

TILE_SIZE_PIXEL = 40
TILE_W_H = 60
TILE_HP_MIN = 100

WIN_WIDTH = 1280
WIN_HEIGHT = 720

def get_spider_action_per_time(frame_count):
    return (SPIDER_BASE_FRAMES / frame_count) * SPIDER_BASE_ACTION_PER_TIME

def get_player_action_per_time(frame_count):
    return (PLAYER_BASE_FRAMES / frame_count) * PLAYER_BASE_ACTION_PER_TIME

def get_hoover_laser_action_per_time(frame_count):
    return (HOOVER_LASER_BASE_FRAMES / frame_count) * HOOVER_LASER_BASE_ACTION_PER_TIME

class Collider_bb:
    def __init__(self, owner, offset_x, offset_y, width, height):
        self.owner = owner
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.width = width
        self.height = height

    def get_bb(self):
        x, y = self.owner.x, self.owner.y
        return (x + self.offset_x - self.width // 2,
                y + self.offset_y - self.height // 2,
                x + self.offset_x + self.width // 2,
                y + self.offset_y + self.height // 2)

    def handle_collision(self, group, other):
        self.owner.handle_collision(group, other)
