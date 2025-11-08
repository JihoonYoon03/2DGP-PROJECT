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

def remove_object(obj):
    for layer in world:
        if obj in layer:
            layer.remove(obj)
            return

    raise Exception("object not found in any layer")

def clear():
    for layer in world:
        layer.clear()