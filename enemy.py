from pico2d import *

from physics_data import *
from behavior_tree import *
from game_world import get_camera
import game_world
import game_framework
import math
import random
import common
from projectile import *
from abc import abstractmethod, ABCMeta

class EnemyBase(metaclass=ABCMeta):
    sound_hit = None
    sound_death = None
    def __init__(self, x, y, spider, name, frame_data, w, h, frame, frame_count, frame_per_time, draw_angle, flip, state, speed, hp, dmg, range):
        if EnemyBase.sound_hit is None:
            EnemyBase.sound_hit = load_wav('Assets/Audios/Enemy/enemy damage 1.wav')
            EnemyBase.sound_hit.set_volume(64)
        if EnemyBase.sound_death is None:
            EnemyBase.sound_death = load_wav('Assets/Audios/Enemy/enemy death 1.wav')
            EnemyBase.sound_death.set_volume(64)
        self.x = x
        self.y = y
        self.spider = spider.collider_spider
        self.name = name

        self.image ={   'Walk' : load_image('Assets/Sprites/Zyrex/' + name + 'WalkTileset.png'),
                        'Attack' : load_image('Assets/Sprites/Zyrex/' + name + 'AttackTileset.png'),
                        'Death' : load_image('Assets/Sprites/Zyrex/' + name + 'DeathTileset.png')
                    }
        self.frame_data = frame_data
        self.w = w
        self.h = h
        self.collision_range = (max(w['Walk'], h['Walk']) - 4) / 2
        self.frame = frame
        self.frame_count = frame_count
        self.frame_per_time = frame_per_time

        self.draw_angle = draw_angle
        self.flip = flip

        self.last_state = state
        self.state = state

        self.tx = 0
        self.ty = 0
        self.speed = speed # m/s
        self.hp = hp
        self.dmg = dmg  # 근접 유닛 데미지(원거리는 총알 데미지로 처리)
        self.attack_range = range if range > 0 else self.collision_range # 공격 사거리 (근접은 콜라이더 범위로 처리, 0)
        self.attack_collider = None
        self.attacked = False   # 현재 프레임 사이클에서 공격 수행했는지 여부

        self.build_behavior_tree()

        game_world.add_collision_pair_range('Machine_gun_bullet:enemy', None, self)

    def check_state(self):
        if self.last_state != self.state:
            self.frame = 0
        self.last_state = self.state

    def update(self):
        if self.state != 'Death':
            self.bt.run()
            self.check_state()
        self.frame += self.frame_per_time[self.state] * game_framework.frame_time
        if self.frame >= self.frame_count[self.state]:
            if self.state == 'Death':
                self.frame = 0
                game_world.remove_object(self)
            else:
                self.frame %= self.frame_count[self.state]
        if self.attack_collider is not None:
            self.attack_collider.update()


    def draw(self):
        camera = get_camera()
        clip_x, clip_y = self.frame_data[self.state][int(self.frame)]
        view_x, view_y = camera.world_to_view(self.x, self.y)
        draw_w, draw_h = camera.get_draw_size(self.w[self.state], self.h[self.state])
        if not camera.draw_clipping(view_x, view_y, draw_w, draw_h):
            self.image[self.state].clip_composite_draw(clip_x, self.image[self.state].h - self.h[self.state] - clip_y,
                                                       self.w[self.state], self.h[self.state],
                                                       self.draw_angle, self.flip,
                                                       view_x, view_y,
                                                       draw_w, draw_h)

        if common.debug_mode:
            draw_circle(view_x, view_y, int(self.collision_range * camera.zoom), 255, 0, 0)
            draw_circle(view_x, view_y, int(self.attack_range * camera.zoom), 255, 255, 0)
            view_x, view_y = camera.world_to_view(self.tx, self.ty)
            draw_circle(view_x, view_y, int(10 * camera.zoom), 255, 0, 255)

            if self.attack_collider is not None:
                x, y = self.attack_collider.get_position()
                x, y = camera.world_to_view(x, y)
                r = int(self.attack_collider.collision_range * camera.zoom)
                draw_circle(x, y, r, 255, 0, 0)

    def handle_event(self, event):
        pass

    # 총알에서 호출
    def getDamage(self, dmg):
        EnemyBase.sound_hit.play()
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            # 사망 모션
            game_world.remove_collision_object(self)
            self.frame = 0
            self.state = 'Death'
            EnemyBase.sound_death.play()

    def handle_collision(self, group, other):
        if group == 'spider:enemy_melee':
            if self.attack_collider is not None:
                game_world.remove_collision_object(self.attack_collider)
                self.attack_collider = None
        elif group == 'Machine_gun_bullet:enemy':
            pass

    def get_bb(self):
        pass

    @abstractmethod
    def build_behavior_tree(self):
        pass

class InfantryTier0(EnemyBase):
    def __init__(self, x, y, spider):
        super().__init__(
            x, y, spider,'Infantry',

    {'Walk' :(
                (0, 0), (40, 0), (80, 0),
                (0, 40), (40, 40), (80, 40),
                (0, 80), (40, 80), (80, 80)
                ),
                'Attack' :(
                    (0, 3), (60, 3), (120, 3), (180, 3),
                    (0, 47), (60, 47), (120, 47), (180, 47)
                ),
                'Death' :(
                    (0, 14), (52, 14), (104, 14), (156, 14),
                    (0, 68), (52, 68), (104, 68), (156, 68)
                )
                },

        {'Walk': 40, 'Attack' : 54, 'Death' : 52},
        {'Walk': 40, 'Attack' : 44, 'Death' : 44},

            0,
            {'Walk' : 8, 'Attack' : 8, 'Death': 8},
            {'Walk' : 8, 'Attack' : 8, 'Death': 8},
            math.pi / 2,
            '',

            'Walk',
            INFANTRY_RUN_SPEED_MPS,
            INFANTRY_HP,
            INFANTRY_ATTACK_DAMAGE,
            0
        )

    def target_in_range(self, target, r=0.5):
        if self.distance_less_than(self.x, target.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def attack_target(self):
        self.state = 'Attack'
        if int(self.frame) == 0:
            self.attacked = False

        if 4 < self.frame < 5 and not self.attacked: # 공격 프레임에서 데미지 적용
            self.attacked = True
            if self.attack_collider is None:
                self.attack_collider = Collider_range(self, 0, self.collision_range * (-1 if self.flip else 1), self.collision_range // 2)
                game_world.add_collision_pair_range('spider:enemy_melee', None, self.attack_collider)

        return BehaviorTree.SUCCESS

    def set_target_location(self, target):
        if target is None:
            raise ValueError('목적지가 설정되어야 합니다.')
        if self.attack_collider:
            game_world.remove_collision_object(self.attack_collider)
            self.attack_collider = None
        self.state = 'Walk'
        self.tx = target.x
        self.ty = target.y
        if self.ty < self.y:
            self.flip = 'h'
        else:
            self.flip = ''
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 <= (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty):
        # 여기를 채우시오.
        distance = self.speed * PIXEL_PER_METER * game_framework.frame_time
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)

    def move_to_target(self, r=0.5):
        if self.distance_less_than(self.x, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        self.move_little_to(self.x, self.ty) # 목적지로 조금 이동
        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        c1 = Condition('Target in range', self.target_in_range, self.spider, (self.spider.collision_range + self.attack_range - 20) / PIXEL_PER_METER)
        a1 = Action('Attack Target', self.attack_target)
        attack = Sequence('Attack', c1, a1)

        a2 = Action('Set Target Location', self.set_target_location, self.spider)
        a3 = Action('Move to Target', self.move_to_target, (self.spider.collision_range + self.attack_range - 20) / PIXEL_PER_METER)
        chase_target = Sequence('Chase Target', a2, a3)

        root = Selector('Attack or Chase', attack, chase_target)
        self.bt = BehaviorTree(root)



class SpitterTier0(EnemyBase):
    def __init__(self, x, y, spider):
        super().__init__(
            x, y, spider,'Spitter',

    {'Walk' :(
                (0, 0), (44, 0),
                (0, 34), (44, 34),
                (0, 68), (44, 68),
                (0, 102),
                ),
                'Attack': (
                    (0, 0), (44, 0), (88, 0), (132, 0), (176, 0),
                    (0, 43), (44, 43), (88, 43), (132, 43), (176, 43),
                    (0, 86), (44, 86), (88, 86)
                ),
                'Death' :(
                    (0, 0), (44, 0), (88, 0), (132, 0), (176, 0),
                    (0, 43), (44, 43), (88, 43), (132, 43), (176, 43),
                    (0, 86), (44, 86), (88, 86))
                },

        {'Walk': 44, 'Attack' : 44, 'Death' : 44},
        {'Walk': 34, 'Attack' : 43, 'Death' : 43},

            0,
            {'Walk' : 7, 'Attack' : 13, 'Death': 8},
            {'Walk' : 7, 'Attack' : 7, 'Death': 7},
            0,
            '',



            'Walk',
            SPITTER_RUN_SPEED_MPS,
            SPITTER_HP,
            0,
            SPITTER_ATTACK_RANGE * PIXEL_PER_METER
        )
        # tx, ty 오프셋
        self.offset_x = 0
        self.offset_y = 0
        # 이전 스파이더 좌표 기억
        self.last_target_x = 0
        self.last_target_y = 0
        self.movNext = False
        self.attack_count = SPITTER_ATTACK_COUNT


    def target_in_range(self, target, r=0.5):
        if self.distance_less_than(target.x, target.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def reached_target_location(self):
        if self.distance_less_than(self.x, self.y, self.tx, self.ty, 0.01):
            self.movNext = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def shoot_bullet(self, target):
        self.state = 'Attack'
        if int(self.frame) == 0:
            self.attacked = False

        if 10 < self.frame < 11 and not self.attacked: # 공격 프레임에서 데미지 적용
            self.attacked = True
            rad = math.atan2(target.y - self.y, target.x - self.x)
            if rad < 0:
                rad += math.pi * 2
            common.obj_pool.get_object(SpitterShot, self.x, self.y, rad + math.radians(random.uniform(-10, 10)), SPITTER_ATTACK_DAMAGE)
            self.attack_count -= 1

        return BehaviorTree.SUCCESS

    def set_target_location(self, target):
        if target is None:
            raise ValueError('목적지가 설정되어야 합니다.')
        self.state = 'Walk'
        angle = random.uniform(math.radians(160), math.radians(200))
        radius = random.uniform(self.attack_range * 0.8 + self.spider.collision_range, self.attack_range + self.spider.collision_range)
        self.offset_x = math.cos(angle) * radius
        self.offset_y = math.sin(angle) * radius
        self.tx = target.x + self.offset_x
        self.ty = target.y + self.offset_y
        self.last_target_x = target.x
        self.last_target_y = target.y
        self.movNext = True
        self.attack_count = SPITTER_ATTACK_COUNT
        return BehaviorTree.SUCCESS

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 <= (PIXEL_PER_METER * r) ** 2

    def move_little_to(self, tx, ty):
        # 여기를 채우시오.
        distance = self.speed * PIXEL_PER_METER * game_framework.frame_time
        dir = math.atan2(ty - self.y, tx - self.x)
        self.x += distance * math.cos(dir)
        self.y += distance * math.sin(dir)

    def move_to_target(self, r=0.5):
        # 스파이더가 움직였으면 타깃 위치도 그만큼 이동
        dx = self.spider.x - self.last_target_x
        dy = self.spider.y - self.last_target_y
        self.tx += dx
        self.ty += dy
        self.last_target_x = self.spider.x
        self.last_target_y = self.spider.y

        if self.distance_less_than(self.x, self.y, self.tx, self.ty, 0.01):
            self.movNext = True
            return BehaviorTree.SUCCESS
        self.move_little_to(self.tx, self.ty) # 목적지로 조금 이동
        return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        # 공격 시퀀스
        # 1. 목표지점 도달 / 2. 타겟이 사거리 내에 있음 / 3. 공격 횟수 남음 / 4. 공격
        c1 = Condition('Target location reached', self.reached_target_location)
        c2 = Condition('Target in range', self.target_in_range, self.spider, (self.spider.collision_range + self.attack_range) / PIXEL_PER_METER)
        c3 = Condition('Attack count left', lambda: BehaviorTree.SUCCESS if self.attack_count > 0 else BehaviorTree.FAIL)
        a1 = Action('Shoot projectile', self.shoot_bullet, self.spider)
        attack = Sequence('Attack', c1, c2, c3, a1)

        c4 = Condition('Target location not set', lambda: BehaviorTree.FAIL  if self.movNext else BehaviorTree.SUCCESS)
        a2 = Action('Set Target Location', self.set_target_location, self.spider)
        set_target_location = Sequence('Set Target', c4, a2)

        a3 = Action('Move to Target', self.move_to_target, (self.spider.collision_range + self.attack_range) / PIXEL_PER_METER)
        chase = Selector('Chase', set_target_location, a3)

        root = Selector('Attack or Chase', attack, chase)
        self.bt = BehaviorTree(root)



class WaveManager:
    def __init__(self):
        self.bgm = load_music('Assets/Audios/BGM/Battle_Theme.wav')
        self.bgm.set_volume(90)
        self.alert = load_wav('Assets/Audios/SFX/Night_Start.wav')
        self.alert.set_volume(64)
        self.clear = load_wav('Assets/Audios/SFX/Night_End.wav')
        self.clear.set_volume(64)
        self.bgm_len = 64
        self.bgm_elapsed = 0.0
        self.current_wave = 0
        self.wave_timer = 0.0
        self.waves_raw = (
            # 기본 데이터
            {InfantryTier0: 6, SpitterTier0: 3},
            {InfantryTier0: 10, SpitterTier0: 8},
            {InfantryTier0: 12, SpitterTier0: 20},
        )
        self.waves = [
            # 실제 웨이브의 적 유닛별 남은 수
            { InfantryTier0 : 6, SpitterTier0 : 3 },
            { InfantryTier0 : 10, SpitterTier0 : 8 },
            {InfantryTier0: 12, SpitterTier0: 20},
        ]
        self.spawn_interval = (
            # 웨이브의 적 유닛별 스폰 간격 (초)
            { InfantryTier0 : 1.5, SpitterTier0 : 2.0 },
            { InfantryTier0 : 1.2, SpitterTier0 : 1.8 },
            {InfantryTier0: 1.2, SpitterTier0: 1.4}
        )
        self.last_spawn_time = {InfantryTier0: 0.0, SpitterTier0: 0.0}
        self.cur_enemies = []
        self.waveRunning = False

    def start_wave(self):
        if self.current_wave >= len(self.waves):
            self.current_wave = len(self.waves) - 1
        self.waveRunning = True
        self.bgm.play()
        self.alert.play(2)
        common.cam.apply_camera_settings()

    def update(self):
        if self.waveRunning:
            self.bgm_elapsed += game_framework.frame_time
            if self.bgm_elapsed >= self.bgm_len:
                self.bgm_elapsed = 0.0
                self.bgm.play()

            for enemy_type, amount in self.waves[self.current_wave].items():
                self.last_spawn_time[enemy_type] += game_framework.frame_time
                if amount > 0 and self.last_spawn_time[enemy_type] >= self.spawn_interval[self.current_wave][enemy_type]:
                    new_enemy = None

                    if enemy_type == InfantryTier0:
                        new_enemy = InfantryTier0(common.spider.x + 72, common.spider.y + (-1 if amount % 2 == 0 else 1) * 1080, common.spider)
                    elif enemy_type == SpitterTier0:
                        new_enemy = SpitterTier0(common.spider.x - 1920 - 100, common.spider.y, common.spider)

                    if new_enemy is not None:
                        self.last_spawn_time[enemy_type] -= self.spawn_interval[self.current_wave][enemy_type]
                        self.cur_enemies.append(new_enemy)
                        game_world.add_object(new_enemy, 3)
                    self.waves[self.current_wave][enemy_type] -= 1

            # 웨이브 클리어 조건: 모든 적 유닛이 스폰되고 모두 제거됨
            all_spawned = all(v == 0 for v in self.waves[self.current_wave].values())
            all_dead = all(enemy.hp == 0 for enemy in self.cur_enemies)
            if all_spawned and all_dead:
                self.waveRunning = False
                self.waves[self.current_wave] = self.waves_raw[self.current_wave].copy()
                self.current_wave += 1
                self.wave_timer = 0.0
                self.last_spawn_time = {InfantryTier0: 0.0, SpitterTier0: 0.0}
                self.cur_enemies = []
                common.cam.apply_camera_settings()
                common.background.IDLE.play_current_bgm()
                self.clear.play()
        else:
            self.wave_timer += game_framework.frame_time
            if self.wave_timer > WAVE_MAX_TIME:
                self.wave_timer = WAVE_MAX_TIME
                self.start_wave()