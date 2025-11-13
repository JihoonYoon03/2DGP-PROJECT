from mine_data import data_set
from tile import TileSet

class Mine:
    def __init__(self, mine_id, x = 1920 / 2, y = 1080 / 2):
        mine_data = data_set[mine_id]
        # 광산 데이터 구조
        # 타일 타입, 타일 배치, 광물 배치, 광산 크기

        # 광산 입구 좌표
        self.entrance_x = x + 20 + 40
        self.entrance_y = y

        # 광산 입구 타일 인덱스
        self.entrance_tile_x = mine_data['tiles']['entrance'][0]
        self.entrance_tile_y = mine_data['tiles']['entrance'][1]

        # 입구 기준 상하 타일 개수
        self.mine_upper = abs(self.entrance_y - 1)
        self.mine_lower = mine_data['size'][1] - self.mine_upper - 1 # 입구 타일 포함 안함

        self.tile_set = TileSet(mine_data['image'], mine_data['size'], mine_data['tiles'], self.entrance_x, self.entrance_y)

    def update(self):
        pass

    def draw(self):
        self.tile_set.draw()

    def handle_event(self, event):
        pass