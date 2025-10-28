running = None
stack = None


def change_scene(scene):
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
    stack.append(scene)
    scene.init()


def push_scene(scene):
    global stack
    if (len(stack) > 0):
        stack[-1].pause()
    stack.append(scene)
    scene.init()


def pop_scene():
    global stack
    if (len(stack) > 0):
        stack[-1].finish()
        stack.pop()

    if (len(stack) > 0):
        stack[-1].resume()


def quit():
    global running
    running = False


def run(start_scene):
    global running, stack
    running = True
    stack = [start_scene]
    start_scene.init()

    while running:
        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
