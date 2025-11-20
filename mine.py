from mine_data import data_set
from tile import *
from pico2d import *
from game_world import get_camera
from physics_data import *

class Mine:
    image_entrance = None
    image_bedrock = None
    def __init__(self, mine_id, x = 1920 / 2, y = 1080 / 2):
        if Mine.image_entrance is None:
            Mine.image_entrance = load_image('Assets/Sprites/Tile/Enter_Biome.png')
        if Mine.image_bedrock is None:
            Mine.image_bedrock = load_image('Assets/Sprites/Tile/Tex_Bedrock.png')

        self.revealed = False

        mine_data = data_set[mine_id]
        # 광산 데이터 구조
        # 타일 타입, 타일 배치, 광물 배치, 광산 크기

        # 광산 입구 좌표
        self.entrance_x = x + 20
        self.entrance_y = y

        # 지표면 1칸 제외 광산 입구 위치
        self.begin_x = x + 20 + 40
        self.begin_y = y

        # 광산 입구 타일 인덱스
        self.entrance_tile_x = mine_data['tiles']['entrance'][0]
        self.entrance_tile_y = mine_data['tiles']['entrance'][1]

        # 입구 기준 상하 타일 개수
        self.mine_upper = abs(self.entrance_y - 1)
        self.mine_lower = mine_data['size'][1] - self.mine_upper - 1 # 입구 타일 포함 안함

        self.tile_set = TileSet(mine_data['image'], mine_data['size'], mine_data['tiles'], self.begin_x, self.begin_y)

        # 입구 위아래 타일
        self.entrance_tile_top = Tile(self.tile_set, self.begin_x, self.begin_y, -1,  self.entrance_tile_y - 1, F_L,
                                      mine_data['tiles']['entrance'], True)
        self.entrance_tile_bottom = Tile(self.tile_set, self.begin_x, self.begin_y, -1, self.entrance_tile_y + 1, F_L,
                                      mine_data['tiles']['entrance'], True)

        game_world.add_collision_pair_bb('player:tile', None, self.entrance_tile_top)
        game_world.add_collision_pair_bb('player:tile', None, self.entrance_tile_bottom)
    def update(self):
        pass

    def draw(self):
        camera = get_camera()

        if not self.revealed:
            # 입구 타일
            view_x, view_y = camera.world_to_view(self.entrance_x, self.entrance_y)
            draw_w, draw_h = camera.get_draw_size(TILE_SIZE_PIXEL, TILE_SIZE_PIXEL)
            Mine.image_entrance.clip_composite_draw(0, 0, TILE_SIZE_PIXEL, TILE_SIZE_PIXEL, 0, '', view_x, view_y, draw_w, draw_h)

        # 입구 위아래 기반암
        self.entrance_tile_top.draw()
        self.entrance_tile_bottom.draw()

    def handle_event(self, event):
        pass

    def reveal(self):
        self.revealed = True
        self.entrance_tile_top.update_flags(F_L | F_D)
        self.entrance_tile_bottom.update_flags(F_L | F_U)