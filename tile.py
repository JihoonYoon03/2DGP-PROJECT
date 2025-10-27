from pico2d import *

# 블럭 39x39, 스프라이트 패딩 19
TILE_SIZE = 39
TILE_PADDING = 20
TILE_STRIDE = TILE_SIZE + TILE_PADDING

BEDROCK_TILES = (

)

class Tile:
    image = None
    def __init__(self, x = 400, y = 300):
        self.x = x
        self.y = y
        self.image = load_image('Assets/Sprites/Tile/Tex_Bedrock.png')
        self.w = 39
        self.h = 39

    def update(self):
        pass

    def draw(self, camera):
        tile_x, tile_y, tile_w, tile_h = BEDROCK_TILES[2]  # 8행 1열 타일
        self.image.clip_draw(tile_x, tile_y, tile_w, tile_h,
                             self.x - camera.x + camera.center_x,
                             self.y - camera.y + camera.center_y)

    def handle_event(self, event):
        pass

def get_tile_clip(index):
    if 0 <= index < len(BEDROCK_TILES):
        return BEDROCK_TILES[index]
    return None