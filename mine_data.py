from tile import TileFlag

F_U, F_R, F_D, F_L = TileFlag.F_U, TileFlag.F_R, TileFlag.F_D, TileFlag.F_L
C_RU, C_RD, C_LD, C_LU = TileFlag.C_RU, TileFlag.C_RD, TileFlag.C_LD, TileFlag.C_LU
ALL_OPEN, ALL_CLOSED = TileFlag.ALL_OPEN, TileFlag.ALL_CLOSED

t = True
_ = False

data_set = {1: {
    # 타일 이미지: 경로
    'image': 'Assets/Sprites/Tile/Block01Tileset.png',

    # 맵 크기: 가로, 세로 타일 개수
    'size': (23, 24),

    # 맵 타입: 타일 배치 및 플래그.
    'tiles':
        {
            'entrance': (0, 11),  # 출입구 타일 좌표 (타일 인덱스)
            # 타일 배치
            'location': (
                (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t),
                (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t),
                (t, t, _, _, _, _, _, _, _, _, _, _, _, t, t, t, t, t, _, _, _, t, t),
                (t, t, _, _, _, _, t, t, t, t, _, _, _, t, t, t, _, _, _, _, _, t, t),
                (t, t, t, t, t, _, t, t, t, t, _, _, _, t, t, t, _, _, _, _, _, t, t),
                (t, t, t, t, t, _, _, t, t, t, t, t, t, t, _, _, _, _, t, t, _, t, t),
                (t, t, t, t, t, _, _, _, _, t, t, t, t, t, t, t, t, t, t, t, _, t, t),
                (t, t, _, t, t, t, t, _, _, _, _, _, t, t, t, t, t, t, t, t, _, t, t),
                (t, t, _, t, t, t, t, _, _, t, t, t, t, t, _, _, _, t, t, t, _, t, t),
                (t, t, _, t, t, t, t, _, _, t, t, t, t, t, _, _, _, t, t, t, _, t, t),
                (t, t, _, _, t, t, t, _, _, t, t, t, t, t, _, _, _, _, _, _, _, t, t),
                (_, _, _, _, _, _, _, _, _, _, t, t, t, _, _, _, _, _, _, _, _, t, t),
                (t, t, _, t, t, _, _, _, t, _, t, t, t, t, t, t, t, t, _, _, _, t, t),
                (t, t, _, t, t, t, _, t, t, _, t, t, t, t, t, _, _, _, _, _, _, t, t),
                (t, t, t, t, t, t, _, t, t, _, t, t, t, t, t, _, _, _, t, t, _, t, t),
                (t, t, t, t, t, t, _, t, t, _, _, _, _, t, t, _, _, _, t, t, _, t, t),
                (t, t, _, t, t, t, _, t, _, _, _, _, _, t, t, t, t, _, _, _, _, t, t),
                (t, t, _, t, t, t, _, _, _, _, _, _, _, t, t, t, t, _, _, _, _, t, t),
                (t, t, _, t, t, t, t, t, _, _, _, _, _, _, _, _, _, _, _, _, _, t, t),
                (t, t, _, t, t, t, t, t, _, _, t, t, t, _, _, _, _, _, _, _, _, t, t),
                (t, t, _, _, _, _, _, _, _, t, t, t, t, _, _, _, _, _, _, _, _, t, t),
                (t, t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t, t),
                (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t),
                (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t)),

            # 기반암 여부
            'bedrock': (
                (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t),
                (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t)),

            # 타일 개방여부 플래그
            'flag': (
                # 0행
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                # 1행
                (0, C_RD, F_D | C_RD, F_D | C_RD | C_LD, F_D | C_RD | C_LD, F_D | C_RD | C_LD, F_D | C_RD | C_LD,
                 F_D | C_RD | C_LD, F_D | C_RD | C_LD, F_D | C_RD | C_LD, F_D | C_RD | C_LD, F_D | C_RD | C_LD,
                 F_D | C_LD, C_LD, 0, 0, 0, C_RD, F_D | C_RD, F_D | C_RD | C_LD, F_D | C_LD, C_LD, 0),
                # 2행
                (0, F_R | C_RD, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L | C_LD, 0, C_RD, F_D | C_RD,
                 F_R | F_D | C_RD | C_LD, 0, 0, 0, F_L | C_LD, 0),
                # 3행
                (0, F_R | C_RU, 0, 0, 0, 0, F_U | F_L | C_RU | C_LD | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU,
                 F_U | F_R | C_RU | C_RD | C_LU, 0, 0, 0, F_L | C_LD | C_LU, 0, F_R | C_RD, 0, 0, 0, 0, 0,
                 F_L | C_LD | C_LU, 0),
                # 4행
                (0, C_RU, F_U | C_RU, F_U | C_RU | C_LU, F_U | F_R | C_RU | C_RD | C_LU, 0, F_D | F_L | C_LD | C_LU,
                 C_LD, 0, F_R | C_RU, 0, 0, 0, F_L | C_RD | C_LU, F_D | C_RD, F_R | F_D | C_RU | C_RD | C_LD, 0, 0, 0,
                 0, 0, F_L | C_LD | C_LU, 0),
                # 5행
                (0, 0, 0, 0, F_R | C_RU | C_RD, 0, 0, F_D | F_L | C_RD | C_LD, F_D | C_LD, C_RU | C_LD, F_U | C_RU,
                 F_U | C_RU | C_LU, F_U | C_LU, F_R | C_LU, 0, 0, 0, 0, F_U | F_L | C_RU | C_LU,
                 F_U | F_R | C_RU | C_RD | C_LU, 0, F_L | C_LD | C_LU, 0),
                # 6행
                (0, C_RD, F_D, C_LD, F_R | C_RU, 0, 0, 0, 0, F_D | F_L | C_RD | C_LD, F_D | C_RD | C_LD, F_D | C_LD,
                 C_LD, C_RU, F_U | C_RU, F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_LU, C_LU, F_R | C_RU | C_RD, 0,
                 F_L | C_LD | C_LU, 0),
                # 7행
                (0, F_R | C_RD, 0, F_L | C_LD, C_RU, F_U | C_RU, F_U | F_R | C_RU | C_RD | C_LU, 0, 0, 0, 0, 0, F_L,
                 C_RD, F_D | C_RD, F_D | C_RD | C_LD, F_D | C_LD, C_LD, 0, F_R | C_RU | C_RD, 0, F_L | C_LD | C_LU, 0),
                # 8행
                (0, F_R | C_RU | C_RD, 0, F_L | C_LD | C_LU, 0, 0, F_R | C_RU | C_RD, 0, 0,
                 F_U | F_L | C_RU | C_LD | C_LU, F_U | C_RU | C_LU, F_U | C_LU, C_LU, F_R | C_RD, 0, 0, 0, F_L | C_LD,
                 0, F_R | C_RU | C_RD, 0, F_L | C_LD | C_LU, 0),
                # 9행
                (0, F_R | C_RU | C_RD, 0, F_D | F_L | C_LD | C_LU, C_LD, 0, F_R | C_RU | C_RD, 0, 0, F_L | C_LD | C_LU,
                 0, 0, 0, F_R | C_RU | C_RD, 0, 0, 0, F_D | F_L | C_RD | C_LD | C_LU, F_D | C_RD | C_LD,
                 F_R | F_D | C_RU | C_RD | C_LD, 0, F_L | C_LD | C_LU, 0),
                # 10행
                (F_D | C_RD, F_R | F_D | C_RU | C_RD | C_LD, 0, 0, F_D | F_L | C_RD | C_LD, F_D | C_RD | C_LD,
                 F_R | F_D | C_RU | C_RD | C_LD, 0, 0, F_D | F_L | C_LD | C_LU, C_LD, 0, C_RD, F_R | F_D | C_RU | C_RD,
                 0, 0, 0, 0, 0, 0, 0, F_L | C_LD | C_LU, 0),
                # 11행
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L | C_LD, 0, F_R, 0, 0, 0, 0, 0, 0, 0, 0, F_L | C_LD | C_LU, 0),
                # 12행
                (F_U | C_RU, F_U | F_R | C_RU | C_RD | C_LU, 0, F_U | F_L | C_RU | C_LD | C_LU, F_U | F_R | C_RU | C_LU,
                 0, 0, 0, F_U | F_R | F_L | C_RU | C_RD | C_LU, 0, F_L | C_LD | C_LU, 0, C_RU, F_U | C_RU,
                 F_U | C_RU | C_RD | C_LU, F_U | F_D | C_RU | C_RD | C_LU, F_U | F_D | C_RU | C_RD | C_LD | C_LU,
                 F_U | F_R | F_D | C_RU | C_RD | C_LD | C_LU, 0, 0, 0, F_L | C_LD | C_LU, 0),
                # 13행
                (0, F_R | C_RU, 0, F_L | C_LU, C_RU, F_U | F_R | C_RU | C_RD, 0, F_U | F_L | C_LD | C_LU,
                 F_R | C_RU | C_RD | C_LU, 0, F_L | C_LD | C_LU, 0, 0, 0, F_R | C_RD, 0, 0, 0, 0, 0, 0,
                 F_L | C_LD | C_LU, 0),
                # 14행
                (0, C_RU, F_U, C_LU, 0, F_R | C_RU | C_RD, 0, F_L | C_LD | C_LU, F_R | C_RU | C_RD, 0,
                 F_D | F_L | C_RD | C_LD | C_LU, F_D | C_RD | C_LD, F_D | C_LD, C_LD, F_R | C_RU | C_RD, 0, 0, 0,
                 F_U | F_L | C_RU | C_LD | C_LU, F_U | F_R | C_RU | C_RD | C_LU, 0, F_L | C_LD | C_LU, 0),
                # 15행
                (0, C_RD, F_D, C_LD, 0, F_R | C_RU | C_RD, 0, F_L | C_RD | C_LD | C_LU, F_R | F_D | C_RU | C_RD, 0, 0,
                 0, 0, F_L | C_LD, F_R | C_RU, 0, 0, 0, F_D | F_L | C_RD | C_LD | C_LU, F_R | F_D | C_RU | C_RD | C_LD,
                 0, F_L | C_LD | C_LU, 0),
                # 16행
                (0, F_R | C_RD, 0, F_L | C_LD, 0, F_R | C_RU | C_RD, 0, F_R | F_D | F_L | C_RD | C_LD | C_LU, 0, 0, 0,
                 0, 0, F_L | C_LD | C_LU, C_RU, F_U | C_RU, F_U | F_R | C_RU | C_RD | C_LU, 0, 0, 0, 0,
                 F_L | C_LD | C_LU, 0),
                # 17행
                (0, F_R | C_RU | C_RD, 0, F_L | C_LD | C_LU, 0, F_R | C_RU, 0, 0, 0, 0, 0, 0, 0,
                 F_D | F_L | C_RD | C_LD | C_LU, F_D | C_RD | C_LD, F_D | C_RD | C_LD, F_R | F_D | C_RU | C_RD | C_LD,
                 0, 0, 0, 0, F_L | C_LD | C_LU, 0),
                # 18행
                (0, F_R | C_RU | C_RD, 0, F_L | C_LD | C_LU, 0, C_RU, F_U | C_RU, F_U | F_R | C_RU | C_RD | C_LU, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L | C_LD | C_LU, 0),
                # 19행
                (0, F_R | C_RU | C_RD, 0, F_D | F_L | C_RD | C_LD | C_LU, F_D | C_RD | C_LD, F_D | C_RD | C_LD,
                 F_D | C_RD | C_LD, F_R | F_D | C_RU | C_RD | C_LD, 0, 0, F_U | F_L | C_RU | C_LU, F_U | C_RU | C_LU,
                 F_U | F_R | C_RU | C_RD | C_LU, 0, 0, 0, 0, 0, 0, 0, 0, F_L | C_LD | C_LU, 0),
                # 20행
                (0, F_R | C_RU | C_RD, 0, 0, 0, 0, 0, 0, 0, F_U | F_D | F_L | C_RD | C_LD | C_LU,
                 F_D | C_RD | C_LD | C_LU, F_D | C_RD | C_LD, F_R | F_D | C_RU | C_RD | C_LD, 0, 0, 0, 0, 0, 0, 0, 0,
                 F_L | C_LD | C_LU, 0),
                # 21행
                (0, F_R | C_RU, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, F_L | C_LU, 0),
                # 22행
                (0, C_RU, F_U | C_RU, F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU,
                 F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU,
                 F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU,
                 F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_RU | C_LU, F_U | C_LU, C_LU, 0),
                # 23행
                (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            )
        },

    # 광물 종류별 분포율 (총 타일 개수의 %)
    'minerals': {
        0: 93,
        1: 7,
    }
}
}
