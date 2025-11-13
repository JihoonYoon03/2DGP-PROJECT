from contextlib import nullcontext

from pico2d import *
from state_machine import StateMachine
from enum import IntFlag
import game_world
from game_world import get_camera

# Tex_Bedrock.png 타일 좌표 (x, y)
# 타일 크기: 40x40, 패딩: 20칸, 좌측/상단 패딩: 10칸
# 이미지 상단이 0행
TILES = (
    # 0행
    (10, 462), (70, 462), (130, 462), (190, 462), (250, 462), (310, 462),
    # 1행
    (10, 402), (70, 402), (130, 402), (190, 402), (250, 402), (310, 402),
    # 2행
    (10, 342), (70, 342), (130, 342), (190, 342), (250, 342), (310, 342),
    # 3행
    (10, 282), (70, 282), (130, 282), (190, 282), (250, 282), (310, 282),
    # 4행
    (10, 222), (70, 222), (130, 222), (190, 222), (250, 222), (310, 222),
    # 5행
    (10, 162), (70, 162), (130, 162), (190, 162), (250, 162), (310, 162),
    # 6행
    (10, 102), (70, 102), (130, 102), (190, 102), (250, 102), (310, 102),
    # 7행
    (10, 42), (70, 42), (130, 42), (190, 42), (250, 42), (310, 42),
)


# 타일 기준 8방향으로 열린/닫힌 상태를 비트 플래그로 표현
class TileFlag(IntFlag):
    # 면 (Face) - 상위 4비트
    F_U = 0b10000000  # 상단 (Up)
    F_R = 0b01000000  # 우측 (Right)
    F_D = 0b00100000  # 하단 (Down)
    F_L = 0b00010000  # 좌측 (Left)

    # 모서리 (Corner) - 하위 4비트
    C_RU = 0b00001000  # 우상단 (Right-Up)
    C_RD = 0b00000100  # 우하단 (Right-Down)
    C_LD = 0b00000010  # 좌하단 (Left-Down)
    C_LU = 0b00000001  # 좌상단 (Left-Up)

    ALL_OPEN = 0b11111111
    ALL_CLOSED = 0b00000000


F_U, F_R, F_D, F_L = TileFlag.F_U, TileFlag.F_R, TileFlag.F_D, TileFlag.F_L
C_RU, C_RD, C_LD, C_LU = TileFlag.C_RU, TileFlag.C_RD, TileFlag.C_LD, TileFlag.C_LU
ALL_OPEN, ALL_CLOSED = TileFlag.ALL_OPEN, TileFlag.ALL_CLOSED

# 비트 플래그 -> 타일 인덱스 직접 매핑
TILE_FLAG_MAP = {

    # 0행
    ALL_CLOSED: 0,  # 모든 모서리 닫힘
    F_U: 1,
    F_L: 2,
    ALL_OPEN: 3,
    C_LD | C_RD: 4,
    C_LU | C_RD: 5,

    # 1행
    F_U | F_L: 6,
    F_U | F_R: 7,
    F_D | F_L: 8,
    F_D | F_R: 9,
    C_LU | C_LD: 10,
    C_LD | C_RU: 11,

    # 2행
    F_L | F_D | F_R: 12,
    F_U | F_L | F_D: 13,
    F_U | F_L | F_R: 14,
    F_U | F_R | F_D: 15,
    C_LU | C_RU: 16,
    F_D: 17,

    # 3행
    C_RD: 18,
    C_LD: 19,
    C_LU: 20,
    C_RU: 21,
    C_RU | C_RD: 22,
    F_R: 23,

    # 4행
    F_L | F_R: 24,
    F_U | F_D: 25,
    C_LU | C_LD | C_RU | C_RD: 26,
    -1: 27,
    F_U | C_LD | C_RD: 28,
    F_R | C_RU | C_RD: 29,

    # 5행
    C_LU | C_LD | C_RU: 30,
    C_LU | C_RU | C_RD: 31,
    C_LD | C_RU | C_RD: 32,
    C_LU | C_LD | C_RD: 33,
    F_R | C_LU | C_LD: 34,
    F_D | C_LU | C_RU: 35,

    # 6행
    F_U | F_L | C_RD: 36,
    F_U | F_R | C_LD: 37,
    F_L | F_D | C_RU: 38,
    F_D | F_R | C_LU: 39,
    F_U | C_RD: 40,
    F_L | C_RD: 41,

    # 7행
    F_U | C_LD: 42,
    F_R | C_LD: 43,
    F_R | C_LU: 44,
    F_D | C_LU: 45,
    F_L | C_RU: 46,
    F_D | C_RU: 47
}


# 타일 플래그 정규화 함수. 플래그 조합을 입력으로 받으면 하나로 합쳐 int형 반환
def normalize_tile_flags(flags: int) -> int:
    """
    규칙:
    1. 모든 면이 오픈되면 모든 모서리도 오픈
    2. 인접한 두 면이 오픈되면 사이 모서리도 오픈
       ex- 상단+우측 -> 우상단 모서리 오픈
    """
    faces = flags & 0b11110000
    corners = flags & 0b00001111

    # 모든 면이 오픈되면 모든 모서리도 오픈
    if faces == 0b11110000:
        return flags | 0b00001111

    # 인접한 두 면이 오픈되면 사이 모서리 오픈
    # 상단+우측 -> 우상단
    if (flags & TileFlag.F_U) and (flags & TileFlag.F_R):
        corners &= ~TileFlag.C_RU

    # 우측+하단 -> 우하단
    if (flags & TileFlag.F_R) and (flags & TileFlag.F_D):
        corners &= ~TileFlag.C_RD

    # 하단+좌측 -> 좌하단
    if (flags & TileFlag.F_D) and (flags & TileFlag.F_L):
        corners &= ~TileFlag.C_LD

    # 좌측+상단 -> 좌상단
    if (flags & TileFlag.F_L) and (flags & TileFlag.F_U):
        corners &= ~TileFlag.C_LU

    return faces | corners


# 타일 인덱스 변환 함수
def tile_index_from_flags(flags: int) -> int:
    """비트 플래그를 타일 인덱스로 변환"""
    normalized = normalize_tile_flags(flags)
    return TILE_FLAG_MAP.get(normalized, 0)  # 매핑에 없으면 0번 타일

class Ground:
    image = None

    def __init__(self, x = 1920 / 2, y = 1080 / 2):
        self.x = x + 20
        self.y = y
        if Ground.image is None:
            Ground.image = load_image('Assets/Sprites/Tile/Tex_Bedrock.png')
        self.w = 40
        self.h = 40
        self.mine_location_y = list()
        self.mine_height = list()

        self.deep_x, self.deep_y = TILES[0]

        # self.IDLE = Idle(self)
        #
        # self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        camera = get_camera()
        if self.y - camera.world_y > 300:
            self.y = self.y - 300
        elif self.y - camera.world_y < -300:
            self.y = self.y + 300

    def draw(self):
        camera = get_camera()
        tile_x, tile_y = TILES[2]
        draw_w, draw_h = camera.get_draw_size(self.w, self.h)

        for dy in range(-30, 31):
            world_y = self.y + dy * self.h

            # 광산 입구 + 위아래 1칸 건너뛰기
            skip = False
            for mine_y in self.mine_location_y:
                if abs(world_y - mine_y) <= self.h:
                    skip = True
                    break

            if skip:
                continue

            view_x, view_y = camera.world_to_view(self.x, self.y + dy * self.h)

            self.image.clip_draw(tile_x, tile_y, self.w, self.h,
                                      view_x, view_y, draw_w, draw_h)

            # 땅 내부 그리기
            # view_x, view_y = camera.world_to_view(self.tile.x + self.tile.w * 10, self.tile.y + dy * self.tile.h)
            # self.tile.image.clip_draw(Idle.deep_x, Idle.deep_y, self.tile.w, self.tile.h,
            #                           round(view_x), round(view_y),
            #                           round(self.tile.w * 19 * camera.zoom), round(self.tile.h * camera.zoom))

    def handle_event(self, event):
        pass

    def add_mine_locations(self, mine_list):
        for mine in mine_list:
            self.mine_location_y.append(mine.entrance_y)
            self.mine_height.append((mine.mine_upper, mine.mine_lower)) # 상하 타일 개수

    def get_mine_locations(self):
        return self.mine_location_y


class TileSet:
    def __init__(self, image_path, mine_size, tile_info, begin_x, begin_y):
        self.image = load_image(image_path)
        self.tiles = list()
        for row in range(mine_size[1]):
            for col in range(mine_size[0]):
                if tile_info['location'][row][col] is False: continue
                self.tiles.append(Tile(self, begin_x, begin_y, col, row, tile_info['flag'][row][col], tile_info['entrance'], tile_info['bedrock'][row][col]))
        self.camera = None

    def update(self):
        pass

    def draw(self):
        for tile in self.tiles:
            tile.draw()

    def handle_event(self, event):
        pass

class Tile:
    # tile_data: 타일 데이터 튜플
    image_bedrock = None
    def __init__(self, tile_set, begin_x, begin_y, col, row, flags, entrance_index, is_bedrock):
        if Tile.image_bedrock is None:
            Tile.image_bedrock = load_image('Assets/Sprites/Tile/Tex_Bedrock.png')

        # 단일 타일 크기
        self.w = 40
        self.h = 40

        # 타일 월드 좌표
        self.x = col * self.w + begin_x
        self.y = (entrance_index[1] - row) * self.h + begin_y # 출입구 인덱스 기준 좌표 보정

        # 타일 플래그 및 인덱스화
        self.raw_flags = flags # 원본 비트 플래그 (이어진 면에 대한 모서리 플래그 제외 없음)
        self.TILES_index = tile_index_from_flags(normalize_tile_flags(flags))  # 인덱스화된 플래그

        # 타일 이미지 클리핑 좌표
        self.image_x, self.image_y = TILES[self.TILES_index]

        self.tileset = tile_set
        self.is_bedrock = is_bedrock

        game_world.add_collision_pair('player:tile', None, self)

    def update_flags(self, flags):
        self.raw_flags = flags
        self.TILES_index = tile_index_from_flags(normalize_tile_flags(flags))

    def draw(self):
        camera = get_camera()
        view_x, view_y = camera.world_to_view(self.x, self.y)
        draw_w, draw_h = camera.get_draw_size(self.w, self.h)

        if self.is_bedrock:
            Tile.image_bedrock.clip_draw(
                self.image_x, self.image_y, self.w, self.h,
                view_x, view_y, draw_w, draw_h
            )
        else:
            self.tileset.image.clip_draw(
                self.image_x, self.image_y, self.w, self.h,
                view_x, view_y, draw_w, draw_h
            )

        x1, y1, x2, y2 = self.get_bb()
        view_x1, view_y1 = camera.world_to_view(x1, y1)
        view_x2, view_y2 = camera.world_to_view(x2, y2)
        draw_rectangle(view_x1, view_y1, view_x2, view_y2)

    def get_bb(self):
        return self.x - self.w // 2, self.y - self.h // 2, self.x + self.w // 2, self.y + self.h // 2

    def handle_collision(self, group, other):
        pass