from tile import TileFlag

F_U, F_R, F_D, F_L = TileFlag.F_U, TileFlag.F_R, TileFlag.F_D, TileFlag.F_L
C_RU, C_RD, C_LD, C_LU = TileFlag.C_RU, TileFlag.C_RD, TileFlag.C_LD, TileFlag.C_LU
ALL_OPEN, ALL_CLOSED = TileFlag.ALL_OPEN, TileFlag.ALL_CLOSED

T = True;
F = False;

data_set = {1: {
        # 타일 이미지: 경로
        'image': 'Assets/Sprites/Tile/Block01Tileset.png',

        # 맵 타입: 타일 배치 및 플래그.
        'tiles':
            {'location': (
                (T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, F, T),
                (T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T, T)),

                'flag': (  # 첫 번째 행 (상단 벽)
                    (C_RD, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, F_D, C_LD),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (F_R, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L),
                    (C_RU, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, F_U, C_LU))
            }
    }
}
