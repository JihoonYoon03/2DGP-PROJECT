import math

world = [[]]

camera = None

def set_camera(cam):
    global camera
    camera = cam

def get_camera():
    return camera

def add_object(obj, layer = 0):
    if layer >= len(world):
        # 레이어 부족할 시 추가
        for _ in range(layer - len(world) + 1):
            world.append([])
    world[layer].append(obj)

def add_objects(objs, layer = 0):
    if layer >= len(world):
        # 레이어 부족할 시 추가
        for _ in range(layer - len(world) + 1):
            world.append([])
    world[layer] += objs

def update():
    global camera
    if camera:
        camera.update()
    for layer in world:
        for obj in layer:
            obj.update()

def render():
    for layer in world:
        for obj in layer:
            obj.draw()

def handle_event(event):
    global camera
    if camera:
        camera.handle_event(event)
    for layer in world:
        for obj in layer:
            obj.handle_event(event)

def remove_collision_object(o):
    for pairs in collision_pairs_bb.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def remove_object(obj):
    for layer in world:
        if obj in layer:
            layer.remove(obj)
            remove_collision_object(obj)
            return

    raise Exception("object not found in any layer")

def clear():
    for layer in world:
        layer.clear()

def collide_bb(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True

# degree_start, degree_end : 충돌 체크 범위 각도
# rotation : 충돌 체크 범위 회전각
# 범위 외부로 나가는 충돌 체크
def collide_outer_radius(a, b, degree_start, degree_end, radius, offset):
    # 중심점(부채꼴 기준점) 정의
    cx = b.x + offset[0]
    cy = b.y + offset[1]

    # 각도/거리 계산
    start = math.radians(degree_start % 360)
    end = math.radians(degree_end % 360)

    angle = math.atan2(a.y - cy, a.x - cx)
    if angle < 0:
        angle += 2 * math.pi

    dx = a.x - cx
    dy = a.y - cy
    dist = math.sqrt(dx * dx + dy * dy)

    # 각도 범위 체크
    if start <= end:
        if not (start <= angle <= end):
            return False
    else:
        if not (angle >= start or angle <= end):
            return False

    return dist >= radius

collision_pairs_bb = {}
collision_pairs_outer_radius = {}

def add_collision_pair_bb(group, a, b):
    if group not in collision_pairs_bb: # 처음 추가되는 그룹이면
        collision_pairs_bb[group] = [[], []] # 해당 그룹을 만든다
    if a:
        collision_pairs_bb[group][0].append(a)
    if b:
        collision_pairs_bb[group][1].append(b)


def add_collision_pair_outer_radius(group, a, b, degree_start=0, degree_end=0, radius=0, offset=(0,0)):
    if group not in collision_pairs_outer_radius:
        collision_pairs_outer_radius[group] = [[], [], degree_start, degree_end, radius, offset]
    if a:
        collision_pairs_outer_radius[group][0].append(a)
    if b:
        collision_pairs_outer_radius[group][1].append(b)
    # 그룹당 하나의 설정값만 사용
    collision_pairs_outer_radius[group][2] = degree_start
    collision_pairs_outer_radius[group][3] = degree_end
    collision_pairs_outer_radius[group][4] = radius
    collision_pairs_outer_radius[group][5] = offset

def handle_collisions():
    handle_collisions_bb()
    handle_collisions_outer_radius()

def handle_collisions_bb():
    for group, pairs in collision_pairs_bb.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide_bb(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)


def handle_collisions_outer_radius():
    for group, data in collision_pairs_outer_radius.items():
        a_list = data[0]
        b_list = data[1]
        degree_start = data[2]
        degree_end = data[3]
        radius = data[4]
        offset = data[5]

        for a in a_list:
            for b in b_list:
                if collide_outer_radius(a, b, degree_start, degree_end, radius, offset):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)