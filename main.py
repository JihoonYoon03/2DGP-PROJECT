from pico2d import *
import game_framework
import play_scene as start_scene
from physics_data import WIN_WIDTH, WIN_HEIGHT


open_canvas(WIN_WIDTH, WIN_HEIGHT)
game_framework.run(start_scene)
close_canvas()