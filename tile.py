from pico2d import *
from state_machine import StateMachine

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

class Idle:
    def __init__(self, tile):
        self.tile = tile

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        if self.tile.camera is not None:
            if self.tile.y - self.tile.camera.world_y > 300:
                self.tile.y = self.tile.y - 300
            elif self.tile.y - self.tile.camera.world_y < -300:
                self.tile.y = self.tile.y + 300

    def draw(self, camera):
        tile_x, tile_y = TILES[2]  # 0행 2열 타일 (0-based)
        for dy in range(-15, 16):   # 위아래 600 픽셀 커버
            view_x, view_y = camera.world_to_view(self.tile.x, self.tile.y + dy * self.tile.h)
            self.tile.image.clip_draw(tile_x, tile_y, self.tile.w, self.tile.h, view_x, view_y, self.tile.w * camera.zoom, self.tile.h * camera.zoom)


class Tile:
    image = None
    def __init__(self, x = 960, y = 540):
        self.x = x + 20
        self.y = y
        if Tile.image is None:
            Tile.image = load_image('Assets/Sprites/Tile/Tex_Bedrock.png')
        self.w = 40
        self.h = 40
        self.camera = None

        self.IDLE = Idle(self)

        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self, camera):
        self.camera = camera
        self.stateMachine.draw(camera)

    def handle_event(self, event):
        pass