from pico2d import *


# Tex_Bedrock.png 타일 좌표 (x, y)
# 타일 크기: 40x40, 패딩: 20칸, 좌측/상단 패딩: 10칸
# 이미지 상단이 1행
TILES = (
    # 1행
    (10, 462), (70, 462), (130, 462), (190, 462), (250, 462), (310, 462),
    # 2행
    (10, 402), (70, 402), (130, 402), (190, 402), (250, 402), (310, 402),
    # 3행
    (10, 342), (70, 342), (130, 342), (190, 342), (250, 342), (310, 342),
    # 4행
    (10, 282), (70, 282), (130, 282), (190, 282), (250, 282), (310, 282),
    # 5행
    (10, 222), (70, 222), (130, 222), (190, 222), (250, 222), (310, 222),
    # 6행
    (10, 162), (70, 162), (130, 162), (190, 162), (250, 162), (310, 162),
    # 7행
    (10, 102), (70, 102), (130, 102), (190, 102), (250, 102), (310, 102),
    # 8행
    (10, 42), (70, 42), (130, 42), (190, 42), (250, 42), (310, 42),
)

class Tile:
    image = None
    def __init__(self, x = 400, y = 300):
        self.x = x
        self.y = y
        self.image = load_image('Assets/Sprites/Tile/Tex_Bedrock.png')
        self.w = 40
        self.h = 40

    def update(self):
        pass

    def draw(self, camera):
        tile_x, tile_y = TILES[2]  # 0행 2열 타일 (0-based)
        self.image.clip_draw(tile_x, tile_y, self.w, self.h,
                             self.x - camera.x + camera.center_x,
                             self.y - camera.y + camera.center_y)

    def handle_event(self, event):
        pass