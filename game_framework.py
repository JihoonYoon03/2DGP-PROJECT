import time

running = None
stack = None

frame_time = 0.0

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
    global frame_time

    running = True
    stack = [start_scene]
    start_scene.init()

    frame_time = 0.0
    start_time = time.time()
    while running:

        stack[-1].handle_events()
        stack[-1].update()
        stack[-1].draw()

        frame_time = time.time() - start_time
        start_time += frame_time
        frame_rate = 1.0 / frame_time

    while (len(stack) > 0):
        stack[-1].finish()
        stack.pop()
