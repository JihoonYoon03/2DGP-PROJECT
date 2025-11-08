from mine_data import data_set
from tile import TileSet

class Mine:
    def __init__(self, mine_id, x = 1920 / 2, y = 1080 / 2):
        mine_data = data_set[mine_id]
        # 광산 데이터 구조
        # 타일 타입, 타일 배치, 광물 배치, 광산 크기
        self.entrance_x = x + 20 + 40
        self.entrance_y = y
        self.tile_set = TileSet(mine_data['image'], mine_data['tiles'], self.entrance_x, self.entrance_y)

    def update(self):
        pass

    def draw(self):
        self.tile_set.draw()

    def handle_event(self, event):
        pass