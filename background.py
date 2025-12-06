import random

import common
import game_framework
from pico2d import *
from state_machine import StateMachine
from game_world import get_camera
from physics_data import *

class Idle:
    bgm = []
    bgm_battle = None
    def __init__(self, bg):
        if not Idle.bgm:
            for i in range(0, 9):
                Idle.bgm.append(load_music('Assets/Audios/BGM/Game_Theme_' + f'{i + 1}' + '.wav'))
                Idle.bgm[i].set_volume(90)
        if Idle.bgm_battle is None:
            Idle.bgm_battle = load_music('Assets/Audios/BGM/Battle_Theme.wav')
            Idle.bgm_battle.set_volume(90)
        self.bgm_cur = -1
        self.bg = bg
        self.bgm_elapsed = 0

    def enter(self, e):
        self.bgm_cur = random.randint(0, 8)
        Idle.bgm[self.bgm_cur].play()

    def exit(self, e):
        return True

    def do(self):
        camera = get_camera()
        if self.bg.y - camera.world_y > self.bg.image.h / 2:
            self.bg.y = self.bg.y - self.bg.image.h
        elif self.bg.y - camera.world_y < self.bg.image.h / -2:
            self.bg.y = self.bg.y + self.bg.image.h

        if common.wave_manager and common.wave_manager.waveRunning:
            self.bgm_elapsed = 0.0
            return
        elif not common.wave_manager.waveRunning:
            self.bgm_elapsed += game_framework.frame_time
            if self.bgm_elapsed >= 120: # 2분마다 배경음악 변경
                self.play_new_bgm()

    def play_new_bgm(self):
        if self.bgm_cur != -1:
            self.bgm_elapsed = 0
            self.bgm_cur = random.randint(0, 8)
            Idle.bgm[self.bgm_cur].play()

    def draw(self):
        camera = get_camera()
        draw_w, draw_h = camera.get_draw_size(self.bg.image.w, self.bg.image.h)

        # 광산 디폴트 배경
        self.bg.image_tile.clip_draw(0, 452, TILE_W_H, TILE_W_H, WIN_WIDTH / 2, WIN_HEIGHT / 2, TILE_W_H * WIN_WIDTH, TILE_W_H * WIN_HEIGHT)

        # 중앙
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y + self.bg.image.h)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, draw_w, draw_h)

        # 상단
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, draw_w, draw_h)

        # 하단
        view_x, view_y = camera.world_to_view(self.bg.x, self.bg.y - self.bg.image.h)
        self.bg.image.clip_draw(0, 0, self.bg.image.w, self.bg.image.h, view_x, view_y, draw_w, draw_h)


class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.image = load_image('Assets/Sprites/Background/NightBackground.png')
        self.image_tile = load_image('Assets/Sprites/Tile/Tex_Bedrock.png') # (0, 452)만 사용

        self.IDLE = Idle(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

    def handle_event(self, event):
        pass