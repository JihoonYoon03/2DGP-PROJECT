from pico2d import *
import play_scene


open_canvas()
play_scene.reset_world()

while play_scene.running:
    clear_canvas()

    # logic
    play_scene.handle_events()
    play_scene.update_world()

    # render
    play_scene.render_world()
    update_canvas()
    delay(0.05)

close_canvas()