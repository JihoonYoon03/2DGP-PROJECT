from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

from state_machine import StateMachine

class RoboSpider:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.frame = 0
        self.image = load_image('Assets/Sprites/Spider/Spider_Moving.png')
        self.width = self.image.w
        self.height = self.image.h

        self.stateMachine = StateMachine()

    def update(self):
        self.stateMachine.update()
        #self.frame = (self.frame + 1) % 16

    def draw(self):
        self.stateMachine.draw()
        #self.image.clip_draw(self.frame * 178 % (11 * 178), self.height - 440 - (self.frame // 11 * 444), 178, 440, self.x, self.y)