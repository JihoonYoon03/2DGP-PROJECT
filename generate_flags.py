# location 데이터로부터 flag 데이터 자동 생성 스크립트
from tile import TileFlag

F_U, F_R, F_D, F_L = TileFlag.F_U, TileFlag.F_R, TileFlag.F_D, TileFlag.F_L
C_RU, C_RD, C_LD, C_LU = TileFlag.C_RU, TileFlag.C_RD, TileFlag.C_LD, TileFlag.C_LU

t = True
_ = False

# location 데이터 입력
location = (
    (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t),
    (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t),
    (t, _, _, _, _, _, _, _, _, _, _, _, _, _, t, t, t, t, _, _, _, t, t),
    (t, _, _, _, _, _, _, _, _, _, _, _, _, t, t, t, _, _, _, _, _, t, t),
    (t, _, _, _, _, _, t, t, t, _, _, _, _, t, _, _, _, _, _, _, _, t, t),
    (t, _, _, _, _, _, _, _, t, t, _, _, _, _, _, _, _, _, t, t, _, t, t),
    (t, _, _, _, _, _, _, _, _, t, t, _, _, t, _, _, _, _, t, t, _, t, t),
    (t, _, _, _, _, _, _, _, _, _, _, _, _, t, _, t, t, t, t, t, _, t, t),
    (t, _, _, t, t, t, t, _, _, _, _, _, _, t, _, _, _, _, _, _, _, t, t),
    (t, _, _, t, t, t, t, _, _, t, t, t, t, t, _, _, _, _, t, t, _, t, t),
    (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t, t),
    (_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t, t),
    (t, _, _, _, _, _, _, _, t, _, _, t, t, t, t, t, t, t, _, _, _, t, t),
    (t, _, _, t, t, _, _, _, t, _, _, _, t, _, _, _, _, _, _, _, _, t, t),
    (t, _, _, t, t, t, _, t, t, _, _, _, t, t, t, _, _, _, t, t, _, t, t),
    (t, _, _, _, _, _, _, t, _, _, _, _, _, _, t, _, _, _, t, t, _, t, t),
    (t, _, _, _, _, _, _, t, _, _, _, _, _, _, t, t, t, _, _, _, _, t, t),
    (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t, _, _, _, _, t, t),
    (t, _, _, t, t, t, t, t, _, _, _, _, _, _, _, _, _, _, _, _, _, t, t),
    (t, _, _, t, _, _, _, t, _, _, t, t, t, _, _, _, _, _, _, _, _, t, t),
    (t, _, _, _, _, _, _, _, _, t, t, t, t, _, _, _, _, _, _, _, _, t, t),
    (t, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, t, t),
    (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t),
    (t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t, t))

rows = len(location)
cols = len(location[0])

# 특정 위치가 열린 공간인지 확인하는 함수
def is_open(row, col):
    # 맵 범위 밖이면 닫힌 것으로 판단
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return False
    # location에서 t(벽)이면 닫힌 것으로 판단
    if location[row][col] == t:
        return False
    # _(빈 공간)이면 열린 것
    return True

flags = []

for row in range(rows):
    flag_row = []
    for col in range(cols):
        # 벽(t)에 대해서만 플래그 계산
        if location[row][col] == t:
            flag = 0

            # 상하좌우 4방향 체크
            # 위 (row-1)
            if is_open(row - 1, col):
                flag |= F_U

            # 오른쪽 (col+1)
            if is_open(row, col + 1):
                flag |= F_R

            # 아래 (row+1)
            if is_open(row + 1, col):
                flag |= F_D

            # 왼쪽 (col-1)
            if is_open(row, col - 1):
                flag |= F_L

            # 대각선 4방향 체크
            # 오른쪽 위 (row-1, col+1)
            if is_open(row - 1, col + 1):
                flag |= C_RU

            # 오른쪽 아래 (row+1, col+1)
            if is_open(row + 1, col + 1):
                flag |= C_RD

            # 왼쪽 아래 (row+1, col-1)
            if is_open(row + 1, col - 1):
                flag |= C_LD

            # 왼쪽 위 (row-1, col-1)
            if is_open(row - 1, col - 1):
                flag |= C_LU

            flag_row.append(flag)
        else:
            # 빈 공간(_)은 0
            flag_row.append(0)

    flags.append(flag_row)

# 플래그 값을 이름으로 변환하는 함수
def flag_to_name(flag):
    if flag == 0:
        return "0"

    parts = []
    if flag & F_U:
        parts.append("F_U")
    if flag & F_R:
        parts.append("F_R")
    if flag & F_D:
        parts.append("F_D")
    if flag & F_L:
        parts.append("F_L")
    if flag & C_RU:
        parts.append("C_RU")
    if flag & C_RD:
        parts.append("C_RD")
    if flag & C_LD:
        parts.append("C_LD")
    if flag & C_LU:
        parts.append("C_LU")

    return "|".join(parts)

# 결과 출력
print("                # 타일 개방여부 플래그")
print("                'flag': (")
for i, row in enumerate(flags):
    print(f"                    # {i}행")
    flag_names = [flag_to_name(f) for f in row]
    print(f"                    ({', '.join(flag_names)}),")
print("                )")

