from pico2d import *
from enum import IntFlag
from physics_data import *
import game_world
import game_framework
from game_world import get_camera
from physics_data import TILE_SIZE_PIXEL, TILE_W_H
from state_machine import StateMachine

# Tex_Bedrock.png 타일 좌표 (x, y)
# 타일 크기: 40x40, 패딩: 20칸, 좌측/상단 패딩: 10칸
# 이미지 상단이 0행
TILES = (
    # 0행
    (0, 452), (60, 452), (120, 452), (180, 452), (240, 452), (300, 452),
    # 1행
    (0, 392), (60, 392), (120, 392), (180, 392), (240, 392), (300, 392),
    # 2행
    (0, 332), (60, 332), (120, 332), (180, 332), (240, 332), (300, 332),
    # 3행
    (0, 272), (60, 272), (120, 272), (180, 272), (240, 272), (300, 272),
    # 4행
    (0, 212), (60, 212), (120, 212), (180, 212), (240, 212), (300, 212),
    # 5행
    (0, 152), (60, 152), (120, 152), (180, 152), (240, 152), (300, 152),
    # 6행
    (0, 92), (60, 92), (120, 92), (180, 92), (240, 92), (300, 92),
    # 7행
    (0, 32), (60, 32), (120, 32), (180, 32), (240, 32), (300, 32),
)

TILE_CRACKS = (
    (4, 213), (52, 213), (100, 213), (148, 213), (196, 213)
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
    1. 모든 면이 오픈되면 모든 모서리도 오픈 (자동 처리되므로 모서리 플래그 제거)
    2. 인접한 두 면이 오픈되면 사이 모서리도 오픈 (자동 처리되므로 모서리 플래그 제거)
       ex- 상단+우측 -> 우상단 모서리 오픈 (C_RU 제거)
    3. 모서리 플래그의 방향이 하나라도 면 플래그와 겹치면 해당 모서리 플래그 제거
       ex- F_R | C_RU -> C_RU는 F_R과 겹치므로 제거 -> F_R
    """
    faces = flags & 0b11110000
    corners = flags & 0b00001111

    # 모든 면이 오픈되면 모든 모서리도 오픈 (모서리 플래그 제거)
    if faces == 0b11110000:
        return faces  # 모서리 플래그 모두 제거

    # 인접한 두 면이 오픈되면 사이 모서리 플래그 제거
    # 상단+우측 -> 우상단 모서리 플래그 제거
    if (flags & TileFlag.F_U) and (flags & TileFlag.F_R):
        corners &= ~TileFlag.C_RU

    # 우측+하단 -> 우하단 모서리 플래그 제거
    if (flags & TileFlag.F_R) and (flags & TileFlag.F_D):
        corners &= ~TileFlag.C_RD

    # 하단+좌측 -> 좌하단 모서리 플래그 제거
    if (flags & TileFlag.F_D) and (flags & TileFlag.F_L):
        corners &= ~TileFlag.C_LD

    # 좌측+상단 -> 좌상단 모서리 플래그 제거
    if (flags & TileFlag.F_L) and (flags & TileFlag.F_U):
        corners &= ~TileFlag.C_LU

    # 모서리 플래그가 면 플래그와 방향이 하나라도 겹치면 제거
    # C_RU (우상단): F_R 또는 F_U와 겹침
    if (flags & TileFlag.F_R) or (flags & TileFlag.F_U):
        corners &= ~TileFlag.C_RU

    # C_RD (우하단): F_R 또는 F_D와 겹침
    if (flags & TileFlag.F_R) or (flags & TileFlag.F_D):
        corners &= ~TileFlag.C_RD

    # C_LD (좌하단): F_L 또는 F_D와 겹침
    if (flags & TileFlag.F_L) or (flags & TileFlag.F_D):
        corners &= ~TileFlag.C_LD

    # C_LU (좌상단): F_L 또는 F_U와 겹침
    if (flags & TileFlag.F_L) or (flags & TileFlag.F_U):
        corners &= ~TileFlag.C_LU

    return faces | corners


# 타일 인덱스 변환 함수
def tile_index_from_flags(flags: int) -> int:
    """비트 플래그를 타일 인덱스로 변환"""
    normalized = normalize_tile_flags(flags)
    return TILE_FLAG_MAP.get(normalized, 0)  # 매핑에 없으면 0번 타일

# 지표면 클래스
class Ground:
    image = None

    def __init__(self, x = 1920 / 2, y = 1080 / 2):
        self.x = x + 20
        self.y = y
        if Ground.image is None:
            Ground.image = load_image('Assets/Sprites/Tile/Tex_Bedrock.png')

        self.mines = list()

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
        draw_w, draw_h = camera.get_draw_size(TILE_W_H, TILE_W_H)

        for dy in range(-30, 31):
            world_y = self.y + dy * TILE_SIZE_PIXEL

            # 광산 입구 + 위아래 1칸 건너뛰기
            skip = False
            for mine in self.mines:
                if abs(world_y - mine.entrance_y) <= TILE_SIZE_PIXEL:
                    skip = True
                    break

            if skip:
                continue

            view_x, view_y = camera.world_to_view(self.x, self.y + dy * TILE_SIZE_PIXEL)

            self.image.clip_draw(tile_x, tile_y, TILE_W_H, TILE_W_H,
                                      view_x, view_y, draw_w, draw_h)

    def handle_event(self, event):
        pass

    # 광산 위치 정보 추가
    def add_mines(self, mine_list):
        for mine in mine_list:
            self.mines.append(mine)

    def get_mine_list(self):
        return self.mines


class TileSet:
    def __init__(self, image_path, mine_size, tile_info, begin_x, begin_y, layer):
        self.image = load_image(image_path)
        self.tiles = list()
        # 인접 타일 체크용 타일 위치 리스트
        self.tiles_location = dict()

        for row in range(mine_size[1]):
            for col in range(mine_size[0]):
                if tile_info['location'][row][col] is False: continue
                self.tiles.append(Tile(self, begin_x, begin_y, col, row, tile_info['flag'][row][col], tile_info['entrance'], tile_info['bedrock'][row][col]))
                # 타일 위치 기록
                self.tiles_location.setdefault((row, col), self.tiles[-1])

        # 타일 출력은 각 타일 객체가 처리
        game_world.add_objects(self.tiles, layer)
        self.camera = None

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass

    def tile_destroyed(self, tile):
        for d_row in range(tile.row - 1, tile.row + 2):
            # 범위 벗어남
            if d_row < 0 or d_row >= len(self.tiles_location):
                continue
            for d_col in range(tile.col - 1, tile.col + 2):
                # 범위 벗어남 or tile 본인 위치
                if d_col < 0 or d_col >= len(self.tiles_location) or (d_row == tile.row and d_col == tile.col):
                    continue
                if (d_row, d_col) in self.tiles_location:
                    self.tiles_location[(d_row, d_col)].nearby_destroyed(tile)
                    print('called nearby_destroyed for tile at ({}, {})'.format(d_row, d_col))

        self.tiles.remove(tile)
        self.tiles_location.pop((tile.y, tile.x), None)

class TileDefault:
    def __init__(self, tile):
        self.tile = tile
        self.crack_level = 0

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        if self.tile.hp < self.tile.max_hp:
            self.crack_level = int((1 - self.tile.hp / self.tile.max_hp) * (len(TILE_CRACKS) - 1))

    def draw(self):
        camera = get_camera()
        view_x, view_y = camera.world_to_view(self.tile.x, self.tile.y)
        draw_w, draw_h = camera.get_draw_size(TILE_W_H, TILE_W_H)

        if not self.tile.is_exposed:
            image_x, image_y = TILES[0]  # 비노출 타일
            Tile.image_bedrock.clip_draw(
                image_x, image_y, TILE_W_H, TILE_W_H,
                view_x, view_y, draw_w, draw_h
            )
            return

        if self.tile.is_bedrock:
            image = Tile.image_bedrock
        else:
            image = self.tile.tileset.image

        image.clip_draw(
            self.tile.image_x, self.tile.image_y, TILE_W_H, TILE_W_H,
            view_x, view_y, draw_w, draw_h
        )

        if self.tile.has_resource:
            res_clip_w = self.tile.res_image.w
            res_clip_h = self.tile.res_image.h
            res_draw_w, res_draw_h = camera.get_draw_size(res_clip_w, res_clip_h)

            self.tile.res_image.clip_composite_draw(
                0, 0, res_clip_w, res_clip_h,
                0, '', view_x, view_y, res_draw_w, res_draw_h
            )

        if self.tile.hp < self.tile.max_hp:
            crack_x, crack_y = TILE_CRACKS[self.crack_level]
            draw_w, draw_h = camera.get_draw_size(TILE_SIZE_PIXEL, TILE_SIZE_PIXEL)
            Tile.image_crack.clip_draw(
                crack_x, crack_y, TILE_SIZE_PIXEL, TILE_SIZE_PIXEL,
                view_x, view_y, draw_w, draw_h
            )

        if self.tile.is_exposed:
            x1, y1, x2, y2 = self.tile.get_bb()
            view_x1, view_y1 = camera.world_to_view(x1, y1)
            view_x2, view_y2 = camera.world_to_view(x2, y2)
            draw_rectangle(view_x1, view_y1, view_x2, view_y2)


class Tile:
    # tile_data: 타일 데이터 튜플
    image_bedrock = None
    image_crack = None
    image_resource = list()
    def __init__(self, tile_set, begin_x, begin_y, col, row, flags, entrance_index, is_bedrock):
        if Tile.image_bedrock is None:
            Tile.image_bedrock = load_image('Assets/Sprites/Tile/Tex_Bedrock.png')
        if Tile.image_crack is None:
            Tile.image_crack = load_image('Assets/Sprites/Tile/crack_cube_library (1).png')
        if len(Tile.image_resource) == 0:
            Tile.image_resource.append(load_image('Assets/Sprites/Tile/CommonResource_Tile.png'))
            Tile.image_resource.append(load_image('Assets/Sprites/Tile/RareRes1_Tile.png'))

        self.col = col
        self.row = row

        # 타일 월드 좌표
        self.x = col * TILE_SIZE_PIXEL + begin_x
        self.y = (entrance_index[1] - row) * TILE_SIZE_PIXEL + begin_y # 출입구 인덱스 중심 좌표 보정

        # 타일 플래그 및 인덱스화
        self.raw_flags = flags # 원본 비트 플래그 (이어진 면에 대한 모서리 플래그 제외 없음)
        self.TILES_index = tile_index_from_flags(normalize_tile_flags(flags))  # 인덱스화된 플래그

        # 노출 여부로 충돌 체크 및 렌더링 결정
        # flag == 0 이면 비노출이란 의미
        self.is_exposed = False if flags == 0 else True

        # 타일 이미지 클리핑 좌표
        self.image_x, self.image_y = TILES[self.TILES_index]

        self.tileset = tile_set
        self.is_bedrock = is_bedrock

        # 타일 체력
        self.max_hp = TILE_HP_MIN
        self.hp = TILE_HP_MIN
        self.crack_level = 0

        # 광물 보유 여부, 전체 광산 타일 생성 후 배정됨
        self.has_resource = False
        self.resource_type = None
        self.res_image = None

        if self.is_exposed:
            game_world.add_collision_pair_bb('player:tile', None, self)
            game_world.add_collision_pair_ray_cast('hoover_laser:tile', None, self)

        self.IDLE = TileDefault(self)

        self.stateMachine = StateMachine(
            self.IDLE,
            {}
        )

    def nearby_destroyed(self, destroyed_tile):
        dx = destroyed_tile.x - self.x
        dy = destroyed_tile.y - self.y

        flags = self.raw_flags
        # 방향 별 플래그 세팅
        if dx != 0 and dy != 0:
            if dx > 0 and dy > 0:
                flags |= TileFlag.C_RU
            elif dx > 0 > dy:
                flags |= TileFlag.C_RD
            elif dx < 0 and dy < 0:
                flags |= TileFlag.C_LD
            elif dx < 0 < dy:
                flags |= TileFlag.C_LU

        else:
            if dx > 0:
                flags |= TileFlag.F_R
            elif dx < 0:
                flags |= TileFlag.F_L
            elif dy > 0:
                flags |= TileFlag.F_U
            elif dy < 0:
                flags |= TileFlag.F_D

        self.update_flags(flags)

        if not self.is_exposed:
            self.is_exposed = True
            game_world.add_collision_pair_bb('player:tile', None, self)
            game_world.add_collision_pair_ray_cast('hoover_laser:tile', None, self)

    def update_flags(self, flags):
        self.raw_flags = flags
        self.TILES_index = tile_index_from_flags(normalize_tile_flags(flags))
        self.image_x, self.image_y = TILES[self.TILES_index]

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        pass

    def get_bb(self):
        return (self.x - TILE_SIZE_PIXEL // 2, self.y - TILE_SIZE_PIXEL // 2,
                self.x + TILE_SIZE_PIXEL // 2, self.y + TILE_SIZE_PIXEL // 2)

    def handle_collision(self, group, other):
        if group == 'hoover_laser:tile':
            if not self.is_bedrock:
                self.hp -= other.damage * game_framework.frame_time
                if self.hp <= 0:
                    game_world.remove_object(self)
                    self.tileset.tile_destroyed(self)

    def get_resource(self, res_type):
        self.has_resource = True
        self.resource_type = res_type
        self.res_image = Tile.image_resource[res_type]