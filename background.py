from pico2d import *
from state_machine import StateMachine

class Background:
    def __init__(self):
        self.x = 400
        self.y = 300
        self.image = load_image('Assets/Sprites/Spider/Spider_Moving.png')

        self.IDLE = None  # Placeholder for the IDLE state
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()