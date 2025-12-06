from pico2d import *

import game_world
import game_framework
import event_set
import common
import math
import UI_Upgrade_scene
import game_end_scene
from state_machine import StateMachine
from event_set import signal_empty, signal_not_empty, r_pressed, signal_time_out, signal_dead
from physics_data import *
import physics_data as pd
from projectile import *

# 스프라이트 프레임 정보 (x, y, w, h)
# 1행 1열부터 시작 (좌상단 기준)
# 178 * 444

SPIDER_WIDTH_SMALL = 178
SPIDER_HEIGHT_SMALL = 442

SPIDER_MOVE_FRAMES = [
    # 1행 (11개)
    (0, 0), (178, 0), (356, 0), (534, 0), (712, 0), (890, 0), (1068, 0), (1246, 0), (1424, 0), (1602, 0), (1780, 0),
    # 2행 (5개)
    (0, 442), (178, 442), (356, 442), (534, 442), (712, 442)
]

SPIDER_DOCK_FRAMES = (
    # 1행 (11개)
    (0, 0), (178, 0), (356, 0), (534, 0), (712, 0),
    (890, 0), (1068, 0), (1246, 0), (1424, 0), (1602, 0), (1780, 0),
    # 2행 (11개)
    (0, 444), (178, 444), (356, 444), (534, 444), (712, 444),
    (890, 444), (1068, 444), (1246, 444), (1424, 444), (1602, 444), (1780, 444),
    # 3행 (11개)
    (0, 888), (178, 888), (356, 888), (534, 888), (712, 888),
    (890, 888), (1068, 888), (1246, 888), (1424, 888), (1602, 888), (1780, 888),
    # 4행 (2개)
    (0, 1332), (178, 1332)
)

SPIDER_UNDOCK_FRAMES = (
    # 1행 (11개)
    (0, 0), (178, 0), (356, 0), (534, 0), (712, 0),
    (890, 0), (1068, 0), (1246, 0), (1424, 0), (1602, 0), (1780, 0),
    # 2행 (7개)
    (0, 444), (178, 444), (356, 444), (534, 444), (712, 444),
    (890, 444), (1068, 444)
)

SPIDER_INNER_DOCKER_FRAMES = (
    (0, 0), (40, 0), (80, 0),
    (0, 40), (40, 40), (80, 40)
)

SPIDER_EXPLODE_FRAMES = (
    (0, 0), (1000, 0), (2000, 0), (3000, 0), (4000, 0), (5000, 0), (6000, 0), (7000, 0),
    (0, 740), (1000, 740), (2000, 740), (3000, 740), (4000, 740), (5000, 740), (6000, 740), (7000, 740),
    (0, 1480), (1000, 1480), (2000, 1480), (3000, 1480), (4000, 1480), (5000, 1480), (6000, 1480), (7000, 1480),
    (0, 2220), (1000, 2220), (2000, 2220), (3000, 2220), (4000, 2220), (5000, 2220), (6000, 2220), (7000, 2220),
    (0, 2960), (1000, 2960), (2000, 2960), (3000, 2960), (4000, 2960), (5000, 2960)
)

class SpIdle:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp):
        self.sp = sp
        if SpIdle.frames_per_action is None:
            SpIdle.frames_per_action = len(SPIDER_MOVE_FRAMES)
        if SpIdle.action_per_time is None:
            SpIdle.action_per_time = get_spider_action_per_time(SpIdle.frames_per_action)

    def enter(self, e):
        if not self.sp.is_moving:
            self.sp.frame = 0

    def exit(self, e):
        if r_pressed(e):
            # 도킹 시도 시 근처 광산이 없으면 도킹 불가
            return self.sp.find_nearby_mine()
        return True

    def do(self):
        if self.sp.move_dir != 0:
            self.sp.stateMachine.handle_state_event(('!EMPTY', None))
            return

        if self.sp.is_moving:
            self.sp.frame = self.sp.frame + SpIdle.frames_per_action * SpIdle.action_per_time * game_framework.frame_time * self.sp.last_move_dir
            self.sp.y += self.sp.speed * SPIDER_RUN_SPEED_PPS * game_framework.frame_time * self.sp.last_move_dir
            if self.sp.frame <= 0 or self.sp.frame >= 16: # 이동 모션이 끝났을 때
                self.sp.is_moving = False
                self.sp.frame = 0
                self.sp.move_dir = 0
                self.sp.last_move_dir = 0
                return

    def draw(self):
        camera = get_camera()
        x, y = SPIDER_MOVE_FRAMES[int(self.sp.frame)]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y - 14) # 14는 이미지 크기 보정용
        draw_w, draw_h = camera.get_draw_size(SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL)
        self.sp.image_move.clip_draw(x, self.sp.image_move.h - SPIDER_HEIGHT_SMALL - y,
                                     SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL, view_x, view_y, draw_w, draw_h)

class SpMove:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp):
        self.sp = sp
        if SpMove.frames_per_action is None:
            SpMove.frames_per_action = len(SPIDER_MOVE_FRAMES)
        if SpMove.action_per_time is None:
            SpMove.action_per_time = get_spider_action_per_time(SpMove.frames_per_action)

    def enter(self, e):
        self.sp.is_moving = True

    def exit(self, e):
        if r_pressed(e):
            return self.sp.find_nearby_mine()
        return True

    def do(self):
        if self.sp.move_dir == 0:
            self.sp.stateMachine.handle_state_event(('EMPTY', None))
            return
        self.sp.frame = ((self.sp.frame
                         + SpMove.frames_per_action * SpMove.action_per_time * game_framework.frame_time * self.sp.move_dir)
                         % len(SPIDER_MOVE_FRAMES))
        self.sp.y += self.sp.speed * SPIDER_RUN_SPEED_PPS * game_framework.frame_time * self.sp.move_dir

    def draw(self):
        camera = get_camera()
        x, y = SPIDER_MOVE_FRAMES[int(self.sp.frame)]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y - 14)
        draw_w, draw_h = camera.get_draw_size(SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL)
        self.sp.image_move.clip_draw(x, self.sp.image_move.h - SPIDER_HEIGHT_SMALL - y,
                                     SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL, view_x, view_y, draw_w, draw_h)

class SpDock:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp):
        self.sp = sp
        self.dist_to_mine = 0
        self.aligning = False
        if SpDock.frames_per_action is None:
            SpDock.frames_per_action = len(SPIDER_DOCK_FRAMES)
        if SpDock.action_per_time is None:
            SpDock.action_per_time = get_spider_action_per_time(SpDock.frames_per_action)

    def enter(self, e):
        self.aligning = True
        self.dist_to_mine = self.sp.docked_mine.entrance_y - self.sp.y
        self.sp.move_dir = self.dist_to_mine / abs(self.dist_to_mine) if self.dist_to_mine != 0 else 0
        self.sp.last_move_dir = 0
        event_set.reset_all_flags()

    def exit(self, e):
        if self.sp.stateMachine.next_state == self.sp.DEATH:
            return True
        if self.sp.frame < 34 or not common.player.is_docked: return False # 도킹 모션이 끝나지 않았을 때는 상태 전환 불가
        return True

    def do(self):
        # 광산 바로 위까지 위치 조정
        if self.aligning:
            move_amount = self.sp.speed * SPIDER_RUN_SPEED_PPS * game_framework.frame_time * self.sp.move_dir

            # 광산 위치에 매우 근접
            if abs(self.sp.docked_mine.entrance_y - (self.sp.y + move_amount)) <= 8:
                self.sp.y = self.sp.docked_mine.entrance_y
                self.aligning = False
                self.sp.is_moving = False
                self.sp.move_dir = 0
                self.sp.last_move_dir = 0
                self.sp.frame = 0

            # 아닌 경우 계속 이동하여 위치 조정
            else:
                self.sp.y += move_amount
                self.sp.frame = ((self.sp.frame
                                 + SpMove.frames_per_action * SpMove.action_per_time * game_framework.frame_time * self.sp.move_dir)
                                 % len(SPIDER_MOVE_FRAMES))

        # 정확히 광산 위일 때 도킹
        else:
            if self.sp.frame < 34:
                self.sp.frame = self.sp.frame + SpDock.frames_per_action * SpDock.action_per_time * game_framework.frame_time
            elif not self.sp.is_docking:
                self.sp.frame = 34
                self.sp.docked_mine.reveal()
                self.sp.is_docking = True
                common.player.is_docked = True
                common.cam.apply_camera_settings()

    def draw(self):
        camera = get_camera()
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y - 14)
        draw_w, draw_h = camera.get_draw_size(SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL)
        if self.aligning:
            x, y = SPIDER_MOVE_FRAMES[int(self.sp.frame)]
            self.sp.image_move.clip_draw(x, self.sp.image_move.h - SPIDER_HEIGHT_SMALL - y,
                                         SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL, view_x, view_y, draw_w, draw_h)
        else:
            x, y = SPIDER_DOCK_FRAMES[int(self.sp.frame)]
            self.sp.image_dock.clip_draw(x, self.sp.image_dock.h - SPIDER_HEIGHT_SMALL - y,
                                         SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL, view_x, view_y, draw_w, draw_h)

class SpUndock:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp):
        self.sp = sp
        if SpUndock.frames_per_action is None:
            SpUndock.frames_per_action = len(SPIDER_UNDOCK_FRAMES)
        if SpUndock.action_per_time is None:
            SpUndock.action_per_time = get_spider_action_per_time(SpUndock.frames_per_action)

    def enter(self, e):
        self.sp.is_docking = False
        self.docked_mine = None
        self.sp.move_dir = 0
        self.sp.last_move_dir = 0
        self.sp.frame = 0
        event_set.reset_all_flags()

    def exit(self, e):
        if self.sp.stateMachine.next_state == self.sp.DEATH:
            return True
        common.cam.apply_camera_settings()
        return True

    def do(self):
        if self.sp.frame < 17:
            self.sp.frame = self.sp.frame + SpUndock.frames_per_action * SpUndock.action_per_time * game_framework.frame_time
        else:
            self.sp.stateMachine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        camera = get_camera()
        x, y = SPIDER_UNDOCK_FRAMES[int(self.sp.frame)]
        view_x, view_y = camera.world_to_view(self.sp.x, self.sp.y - 14)
        draw_w, draw_h = camera.get_draw_size(SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL)
        self.sp.image_undock.clip_draw(x, self.sp.image_undock.h - SPIDER_HEIGHT_SMALL - y,
                                       SPIDER_WIDTH_SMALL, SPIDER_HEIGHT_SMALL, view_x, view_y, draw_w, draw_h)

class SpExplode:
    frames_per_action = None
    action_per_time = None

    sound_explode = None
    def __init__(self, sp):
        if SpExplode.frames_per_action is None:
            SpExplode.frames_per_action = len(SPIDER_EXPLODE_FRAMES)
        if SpExplode.action_per_time is None:
            SpExplode.action_per_time = get_spider_action_per_time(SpExplode.frames_per_action) * 0.6
        if SpExplode.sound_explode is None:
            SpExplode.sound_explode = load_wav('Assets/Audios/Spider/Spider_Death.wav')
            SpExplode.sound_explode.set_volume(64)
        self.sp = sp
        self.w = SPIDER_EXPLODE_FRAMES[9][0]
        self.h = SPIDER_EXPLODE_FRAMES[9][1]

    def enter(self, e):
        SpExplode.sound_explode.play()
        self.sp.frame = 0

    def exit(self, e):
        return True

    def do(self):
        self.sp.frame += SpExplode.frames_per_action * SpExplode.action_per_time * game_framework.frame_time
        if self.sp.frame >= len(SPIDER_EXPLODE_FRAMES):
            self.sp.frame = len(SPIDER_EXPLODE_FRAMES) - 1
            game_framework.push_scene(game_end_scene)

    def draw(self):
        camera = get_camera()
        x, y = SPIDER_EXPLODE_FRAMES[int(self.sp.frame)]
        view_x, view_y = camera.world_to_view(self.sp.x - 194, self.sp.y - 14 - 112) # 14는 이미지 크기 보정용
        draw_w, draw_h = camera.get_draw_size(self.w, self.h)
        self.sp.image_explode.clip_draw(x, self.sp.image_explode.h - self.h - y,
                                     self.w, self.h, view_x, view_y, draw_w, draw_h)

class RoboSpider:
    def __init__(self, x = 1920 / 2, y = 1080 / 2):
        self.image_move = load_image('Assets/Sprites/Spider/Spider_Moving.png')
        self.image_dock = load_image('Assets/Sprites/Spider/Spider_Docking.png')
        self.image_undock = load_image('Assets/Sprites/Spider/Spider_Undocking.png')
        self.image_explode = load_image('Assets/Sprites/Spider/Spider_Death.png')

        self.sound_hit = load_wav('Assets/Audios/Enemy/enemy attack 1.wav')
        self.sound_hit.set_volume(32)

        self.sound_idle = load_wav('Assets/Audios/Spider/Spider_Idle.wav')
        self.sound_idle.set_volume(4)
        self.sound_move_start = load_wav('Assets/Audios/Spider/Spider_Moving_Start.wav')
        self.sound_move_start.set_volume(40)
        self.sound_move = load_wav('Assets/Audios/Spider/Spider_Idle.wav')
        self.sound_move.set_volume(40)
        self.sound_move_stomp = load_wav('Assets/Audios/Spider/Spider_Moving_Idle.wav')
        self.sound_move_stomp.set_volume(40)
        self.sound_move_stop = load_wav('Assets/Audios/Spider/Spider_Moving_Finish.wav')
        self.sound_move_stop.set_volume(40)

        self.x = x - 178 // 2
        self.y = y
        self.speed = 1
        self.health = SPIDER_MAX_HP
        self.shield = SPIDER_MAX_SHIELD
        self.is_moving = False
        self.is_docking = False
        self.move_dir = 0
        self.last_move_dir = 0
        self.frame = 0

        self.w = 178
        self.h = 440
        self.range_inner = self.w * 0.5 # 내부 반경
        self.range_inner_offset = (60, 0)
        game_world.add_collision_pair_radius_limited('player:spider_inner_dome', None, self, self.range_inner, True)

        self.turret = Turret(self)

        self.collision_range = self.w * 1.16  # 외부 충돌 반경
        self.collision_range_offset = (130, 4)
        self.collider_spider = Collider_range(self, self.collision_range_offset[0], self.collision_range_offset[1], self.collision_range)
        game_world.add_collision_pair_range('spider:enemy_melee', self.collider_spider, None)
        game_world.add_collision_pair_range('spider:SpitterShot', self.collider_spider, None)

         # 충돌 범위 제한
        self.degree_start = 90
        self.degree_end = 270
        self.collider_entrance_up = Collider_bb(self, 74, 60, 30, 70)
        self.collider_entrance_down = Collider_bb(self, 74, -60, 30, 70)
        self.barrier = Collider_bb(self, 0, 0, self.w * 1.05, 200)
        game_world.add_collision_pair_bb('player:spider_inner_bb', None, self.collider_entrance_up)
        game_world.add_collision_pair_bb('player:spider_inner_bb', None, self.collider_entrance_down)
        game_world.add_collision_pair_bb('spider_mine_barrier:ore', self.barrier, None)

        # 광산 레퍼런스 리스트와 현재 도킹된 광산 입구 위치
        self.mine_list = list()
        self.docked_mine = None

        # 스파이더 내부
        self.inner = RoboSpiderIn(self)
        game_world.add_object(self.inner, 2)

        self.IDLE = SpIdle(self)
        self.UP = SpMove(self)
        self.DOCK = SpDock(self)
        self.UNDOCK = SpUndock(self)
        self.DEATH = SpExplode(self)
        self.stateMachine = StateMachine(
            self.IDLE,
        {
            self.IDLE : { signal_not_empty : self.UP, r_pressed : self.DOCK, signal_dead : self.DEATH },
            self.UP : { signal_empty : self.IDLE, r_pressed : self.DOCK, signal_dead : self.DEATH },
            self.DOCK : { r_pressed : self.UNDOCK, signal_dead : self.DEATH },
            self.UNDOCK : { signal_time_out : self.IDLE, signal_dead : self.DEATH },
            self.DEATH : {}
        })

    def update(self):
        if all(mine.resEmpty for mine in self.mine_list) and len(common.ore_list) == 0 and not common.player.engage:
            game_framework.push_scene(game_end_scene)

        self.stateMachine.update()
        if self.stateMachine.cur_state == self.DEATH:
            return
        self.turret.update()
        self.collider_spider.update()
        self.collider_entrance_up.update()
        self.collider_entrance_down.update()
        self.barrier.update()
        if self.shield >= SPIDER_MAX_SHIELD:
            self.shield = SPIDER_MAX_SHIELD
        elif not common.wave_manager.waveRunning:
            self.shield += SPIDER_SHIELD_REGEN_PPS * game_framework.frame_time

    def draw(self):
        if self.stateMachine.cur_state != self.DEATH:
            self.turret.draw()
        self.stateMachine.draw()

        if common.debug_mode:
            view_x, view_y = common.cam.world_to_view(self.x + self.collision_range_offset[0], self.y + self.collision_range_offset[1])
            draw_circle(view_x, view_y, int(self.collision_range * common.cam.zoom), 255, 0, 0)

    def handle_event(self, event):
        if self.stateMachine.cur_state == self.DEATH:
            return

        event_tuple = ('INPUT', event)

        if event_set.f_pressed(event_tuple) and common.player.is_docked:
            game_framework.push_scene(UI_Upgrade_scene)

        if not self.is_docking and self.stateMachine.cur_state != self.DOCK:
            prev_moving = self.move_dir != 0

            if event_set.w_pressed(event_tuple):
                event_set.flag_w = True
                self.move_dir += 1
                self.last_move_dir = 1
            elif event_set.s_pressed(event_tuple):
                event_set.flag_s = True
                self.move_dir -= 1
                self.last_move_dir = -1

            elif event_set.w_released(event_tuple) and event_set.flag_w:
                event_set.flag_w = False
                self.move_dir -= 1
            elif event_set.s_released(event_tuple) and event_set.flag_s:
                event_set.flag_s = False
                self.move_dir += 1

            now_moving = self.move_dir != 0

            # 정지 -> 이동
            if not prev_moving and now_moving:
                self.stateMachine.handle_state_event(('!EMPTY', None))

            # 이동 -> 정지
            elif prev_moving and not now_moving:
                self.stateMachine.handle_state_event(('EMPTY', None))

        self.turret.handle_event(event)
        self.stateMachine.handle_state_event(('INPUT', event))

    def get_bb(self):
        half_w = self.w // 2
        half_h = self.h // 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        if group == 'spider:enemy_melee' or group == 'spider:SpitterShot':
            self.sound_hit.play()
            if self.shield > 0:
                self.shield -= other.owner.dmg  # 충돌 대상이 enemy의 collider_range 객체이므로 owner로 접근
                if self.shield < 0:
                    self.shield = 0
            else:
                self.health -= other.owner.dmg  # 충돌 대상이 enemy의 collider_range 객체이므로 owner로 접근
                print('RoboSpider HP:', self.health)
                if self.health < 0:
                    self.health = 0
                    self.stateMachine.handle_state_event(('DEAD', None))

    # 도킹 시 근처 광산을 찾는 함수
    def find_nearby_mine(self):
        # 도킹 시 광산 입구와의 최대 거리
        max_distance = TILE_SIZE_PIXEL * 5
        for mine in self.mine_list:
            if abs(mine.entrance_y - self.y) <= max_distance:  # 광산 입구 근처에 있을 때
                self.docked_mine = mine
                return True
        return False

    def gather_resources(self, amount):
        common.UI_ResourceData.add_resources(amount)
        self.inner.rh_frame = 1 # 자원 수집기 작동 애니메이션 재생

class SpInIdle:
    frames_per_action = None
    action_per_time = None

    def __init__(self, sp_in):
        self.sp_in = sp_in
        if SpInIdle.frames_per_action is None:
            SpInIdle.frames_per_action = len(SPIDER_INNER_DOCKER_FRAMES)
        if SpInIdle.action_per_time is None:
            SpInIdle.action_per_time = get_player_action_per_time(SpInIdle.frames_per_action)

    def enter(self, e):
        pass

    def exit(self, e):
        return True

    def do(self):
        if self.sp_in.sp.is_docking:
            self.sp_in.docker_frame = ((self.sp_in.docker_frame
                                       + SpInIdle.frames_per_action * SpInIdle.action_per_time * game_framework.frame_time)
                                       % SpInIdle.frames_per_action)
            self.sp_in.barrier_frame = ((self.sp_in.barrier_frame + self.sp_in.barrier_frames_per_time * game_framework.frame_time)
                                        % self.sp_in.barrier_frame_count)
            if 0 < self.sp_in.rh_frame:
                self.sp_in.rh_frame += self.sp_in.rh_per_time * game_framework.frame_time
                if self.sp_in.rh_frame > self.sp_in.rh_frame_count:
                    self.sp_in.rh_frame = 0

        self.sp_in.docker_x = self.sp_in.sp.x - 16
        self.sp_in.docker_y = self.sp_in.sp.y

    def draw(self):
        if common.spider.stateMachine.cur_state == common.spider.DEATH:
            return

        camera = get_camera()
        # 배경 그리기
        view_x, view_y = camera.world_to_view(self.sp_in.sp.x, self.sp_in.sp.y - 16) # 이미지 크기 보정용 -2 추가
        draw_w, draw_h = camera.get_draw_size(self.sp_in.image_background.w, self.sp_in.image_background.h)
        if not camera.draw_clipping(view_x, view_y, draw_w, draw_h):
            self.sp_in.image_background.clip_draw(0, 0, self.sp_in.image_background.w, self.sp_in.image_background.h,
                                                    view_x, view_y, draw_w, draw_h)
            # 방 내부 그리기
            draw_w, draw_h = camera.get_draw_size(self.sp_in.image_room.w, self.sp_in.image_room.h)
            self.sp_in.image_room.clip_draw(0, 0, self.sp_in.image_room.w, self.sp_in.image_room.h,
                                            view_x, view_y, draw_w, draw_h)

        # 도킹 게이트 그리기
        gate_view_x, gate_view_y = camera.world_to_view(self.sp_in.sp.x + self.sp_in.sp.w * 0.44, self.sp_in.sp.y)
        gate_draw_w, gate_draw_h = camera.get_draw_size(40, 84)
        if not camera.draw_clipping(gate_view_x, gate_view_y, gate_draw_w, gate_draw_h):
            frame = int(self.sp_in.barrier_frame)
            self.sp_in.image_barrier.clip_draw(frame * 40, self.sp_in.image_barrier.h - 84, 40, 84,
                                                gate_view_x, gate_view_y, gate_draw_w, gate_draw_h)

            # 자원 수집기 그리기
            rh_view_x, rh_view_y = camera.world_to_view(self.sp_in.sp.x + self.sp_in.sp.w * 0.28, self.sp_in.sp.y)
            rh_draw_w, rh_draw_h = camera.get_draw_size(44, 124)
            frame = int(self.sp_in.rh_frame)
            row = frame // 11 + 1
            self.sp_in.image_rh.clip_draw(frame % 11 * 44, self.sp_in.image_rh.h - row * 124, 44, 124,
                                            rh_view_x, rh_view_y, rh_draw_w, rh_draw_h)

        # 프레임 그리기
        draw_w, draw_h = camera.get_draw_size(self.sp_in.image_frame.w, self.sp_in.image_frame.h)
        if not camera.draw_clipping(view_x, view_y, draw_w, draw_h):
            self.sp_in.image_frame.clip_draw(0, 0, self.sp_in.image_frame.w, self.sp_in.image_frame.h,
                                            view_x, view_y, draw_w, draw_h)

            # 도킹 모듈 그리기
            x, y = SPIDER_INNER_DOCKER_FRAMES[int(self.sp_in.docker_frame)]
            docker_view_x, docker_view_y = camera.world_to_view(self.sp_in.docker_x, self.sp_in.docker_y)
            draw_w, draw_h = camera.get_draw_size(40, 40)
            self.sp_in.image_docker.clip_draw(x, self.sp_in.image_docker.h - 40 - y,
                                              40, 40, docker_view_x, docker_view_y, draw_w, draw_h)

# 스파이더 내부
class RoboSpiderIn:
    def __init__(self, robo_spider):
        self.image_room = load_image('Assets/Sprites/Spider/Spider_Inner_Back.png')
        self.image_frame = load_image('Assets/Sprites/Spider/Spider_Inner_Frame.png')
        self.image_background = load_image('Assets/Sprites/Spider/Spider_Inner_Opened.png')
        self.image_docker = load_image('Assets/Sprites/Spider/Spider_DockingModule.png')
        self.image_barrier = load_image('Assets/Sprites/Spider/EnergyGate_Idle.png')
        self.image_rh = load_image('Assets/Sprites/Spider/Spider_ResourceHandler_Working.png')

        self.sp = robo_spider

        self.docker_x = robo_spider.x - 16
        self.docker_y = robo_spider.y
        self.docker_frame = 0

        self.barrier_frame = 0
        self.barrier_frames_per_time = 8
        self.barrier_frame_count = 4

        # rh = resource handler
        self.rh_frame = 0
        self.rh_per_time = 8
        self.rh_frame_count = 16

        self.IDLE = SpInIdle(self)
        self.stateMachine = StateMachine(self.IDLE, {})

    def update(self):
        if self.sp.is_docking:
            self.stateMachine.update()

    def draw(self):
        if self.sp.is_docking:
            self.stateMachine.draw()

            if common.debug_mode:
                x1, y1, x2, y2 = self.sp.collider_entrance_up.get_bb()
                view_x1, view_y1 = common.cam.world_to_view(x1, y1)
                view_x2, view_y2 = common.cam.world_to_view(x2, y2)
                draw_rectangle(view_x1, view_y1, view_x2, view_y2)

                x1, y1, x2, y2 = self.sp.collider_entrance_down.get_bb()
                view_x1, view_y1 = common.cam.world_to_view(x1, y1)
                view_x2, view_y2 = common.cam.world_to_view(x2, y2)
                draw_rectangle(view_x1, view_y1, view_x2, view_y2)

                x1, y1, x2, y2 = self.sp.barrier.get_bb()
                view_x1, view_y1 = common.cam.world_to_view(x1, y1)
                view_x2, view_y2 = common.cam.world_to_view(x2, y2)
                draw_rectangle(view_x1, view_y1, view_x2, view_y2, 150, 200, 255)

                # 2, 3사분면 반원 그리기 (디버그용)
                view_x, view_y = common.cam.world_to_view(self.sp.x + self.sp.range_inner_offset[0], self.sp.y)
                draw_circle(view_x, view_y, int(common.cam.value_to_view(self.sp.range_inner)), 255, 0, 0)

    def handle_event(self, event):
        pass

class Turret:
    sound_shoot = None
    def __init__(self, spider):
        if Turret.sound_shoot is None:
            Turret.sound_shoot = load_wav('Assets/Audios/SFX/gunshot 2.wav')
            Turret.sound_shoot.set_volume(48)
        self.image = load_image('Assets/Sprites/Turret/Turret_MachineGun.png')
        self.spider = spider

        self.radius = self.spider.w * 0.8  # 터렛 회전 반경
        self.recoil_distance = 1  # 반동 거리
        self.angle = math.pi
        self.cur_angle = math.pi
        self.rot_speed = math.radians(SPIDER_TURRET_ROTATE_SPEED * pd.UPGRADE_TURRET_ROTATE_SPEED)  # 초당 회전 각도

        self.shooting = False
        self.last_fire_time = 0
        self.fire_rate = MACHINE_GUN_FIRE_RATE * UPGRADE_GUN_FIRE_RATE  # 총알 발사 간격 (초)

    def update(self):
        self.rot_speed = math.radians(SPIDER_TURRET_ROTATE_SPEED * pd.UPGRADE_TURRET_ROTATE_SPEED)
        self.fire_rate = MACHINE_GUN_FIRE_RATE * pd.UPGRADE_GUN_FIRE_RATE

        # 터렛 각도 보간
        da = self.angle - self.cur_angle
        if abs(da) < 0.01:
            self.cur_angle = self.angle
        else:
            if da > 0:
                self.cur_angle += min(self.rot_speed * game_framework.frame_time, da)
            else:
                self.cur_angle -= min(self.rot_speed * game_framework.frame_time, -da)

        self.last_fire_time = clamp(0, self.last_fire_time + game_framework.frame_time, self.fire_rate)

        if self.shooting:
            if self.last_fire_time >= self.fire_rate:
                self.last_fire_time %= self.fire_rate
                bullet_x = self.spider.x + 60 + (self.radius + self.image.w // 2) * math.cos(self.cur_angle)
                bullet_y = self.spider.y + (self.radius + self.image.w // 2) * math.sin(self.cur_angle)
                # 총알 발사. x, y, rad 인자 필요
                common.obj_pool.get_object(MachineGunProjectile, bullet_x, bullet_y, self.cur_angle, MACHINE_GUN_BULLET_DAMAGE * pd.UPGRADE_GUN_BULLET_DAMAGE_PERCENT + pd.UPGRADE_GUN_BULLET_DAMAGE)
                Turret.sound_shoot.play()

    def draw(self):
        camera = get_camera()
        turret_x = self.spider.x + 60 + (self.radius - self.recoil_distance / max(0.1, self.last_fire_time / self.fire_rate)) * math.cos(self.cur_angle)
        turret_y = self.spider.y + (self.radius - self.recoil_distance / max(0.1, self.last_fire_time / self.fire_rate)) * math.sin(self.cur_angle)
        turret_x, turret_y = camera.world_to_view(turret_x, turret_y)
        turret_w, turret_h = camera.get_draw_size(self.image.w, self.image.h)
        self.image.clip_composite_draw(0, 0, self.image.w, self.image.h,
                                            self.cur_angle, 'h',
                                              turret_x, turret_y, turret_w, turret_h)

    def handle_event(self, event):
        if event_set.mouse_motion(('INPUT', event)) and common.player.turret_control:
            mouse_x, mouse_y = event_set.mouse_coordinate((None, event))
            camera = get_camera()
            view_x, view_y = camera.world_to_view(self.spider.x + 60, self.spider.y)
            dx = mouse_x - view_x
            dy = mouse_y - view_y
            angle = math.atan2(dy, dx)
            if angle < 0:
                angle += 2 * math.pi
            da = angle - self.angle
            self.angle = clamp(math.pi / 2, self.angle + da, math.pi * 3 / 2)

        if event_set.mouse_left_pressed(('INPUT', event)) and common.player.turret_control:
            self.shooting = True

        if event_set.mouse_left_released(('INPUT', event)) or not common.player.turret_control:
            self.shooting = False


    def handle_collision(self, group, other):
        pass