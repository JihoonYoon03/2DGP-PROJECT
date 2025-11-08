import sdl2
from camera import Camera

def time_out(e):
    return e[0] == 'TIME_OUT'

def e_pressed(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYDOWN and e[1].key == sdl2.SDLK_e

def e_released(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYUP and e[1].key == sdl2.SDLK_e

def w_pressed(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYDOWN and e[1].key == sdl2.SDLK_w

def w_released(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYUP and e[1].key == sdl2.SDLK_w

def a_pressed(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYDOWN and e[1].key == sdl2.SDLK_a

def a_released(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYUP and e[1].key == sdl2.SDLK_a

def s_pressed(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYDOWN and e[1].key == sdl2.SDLK_s

def s_released(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYUP and e[1].key == sdl2.SDLK_s

def d_pressed(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYDOWN and e[1].key == sdl2.SDLK_d

def d_released(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYUP and e[1].key == sdl2.SDLK_d

def r_pressed(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYDOWN and e[1].key == sdl2.SDLK_r

def no_key_pressed(e):
    return e[0] == 'INPUT' and e[1].type == sdl2.SDL_KEYDOWN and \
        e[1].key not in (sdl2.SDLK_w, sdl2.SDLK_a, sdl2.SDLK_s, sdl2.SDLK_d)