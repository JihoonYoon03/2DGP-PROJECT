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
    for pairs in collision_pairs.values():
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

collision_pairs = {}

def add_collision_pair(group, a, b):
    if group not in collision_pairs: # 처음 추가되는 그룹이면
        collision_pairs[group] = [[], []] # 해당 그룹을 만든다
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def handle_collisions_bb():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide_bb(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)