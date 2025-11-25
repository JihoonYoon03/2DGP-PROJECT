from pico2d import *
from pygame.draw import circle

from physics_data import *
from state_machine import StateMachine
from game_world import get_camera
import game_framework
import game_world


class Idle:
    def __init__(self, ore):
        self.ore = ore

    def enter(self, event):
        pass

    def exit(self, event):
        return True

    def do(self):
        dt = game_framework.frame_time

        # 가속도 -> 속도
        self.ore.vx += self.ore.ax * dt
        self.ore.vy += self.ore.ay * dt

        # 중력 적용
        self.ore.vy -= GRAVITY * dt

        # 낙하 속도 제한
        if self.ore.vy < -MAX_ORE_FALLING_SPEED:
            self.ore.vy = -MAX_ORE_FALLING_SPEED

        # 속도 -> 위치
        self.ore.x += self.ore.vx * dt
        self.ore.y += self.ore.vy * dt

        # 힘/토크 초기화 (다음 프레임을 위해)
        self.ore.ax = 0
        self.ore.ay = 0

        self.ore.vx *= self.ore.friction
        self.ore.vy *= self.ore.friction

    def draw(self):
        camera = get_camera()
        view_x, view_y = camera.world_to_view(self.ore.x, self.ore.y)
        draw_w, draw_h = camera.get_draw_size(self.ore.w, self.ore.h)
        if not camera.draw_clipping(view_x, view_y, draw_w, draw_h):
            self.ore.image.clip_composite_draw(0, 0, self.ore.w, self.ore.h,
                                               0, '',
                                               view_x, view_y, draw_w, draw_h)


class Ore:
    image_ore = list()

    def __init__(self, x, y, res_type):
        if len(Ore.image_ore) == 0:
            Ore.image_ore.append(load_image('Assets/Sprites/Item/CommonResource_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes1_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes2_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes3_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes4_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes5_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes6_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes7_Item.png'))
            Ore.image_ore.append(load_image('Assets/Sprites/Item/RareRes8_Item.png'))

        # 위치
        self.x = x
        self.y = y

        # 이미지 설정
        self.res_type = res_type
        self.image = Ore.image_ore[self.res_type]
        self.w = Ore.image_ore[self.res_type].w
        self.h = Ore.image_ore[self.res_type].h

        # 충돌 범위
        self.collision_range = min(self.image.w, self.image.h) * 0.4
        self.radius = self.collision_range  # 원형 근사 반지름

        # 물리 속성
        self.mass = ORE_MASS
        self.restitution = ORE_RESTITUTION
        self.friction = ORE_FRICTION  # 마찰 계수

        # 선형 운동
        self.vx = 1.0
        self.vy = -GRAVITY * 0.5
        self.ax = 0.0
        self.ay = 0.0

        # 상태 머신
        self.IDLE = Idle(self)
        self.stateMachine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {}
            })

        # 충돌 등록
        game_world.add_collision_pair_bb('ore:tile', self, None)
        game_world.add_collision_pair_range('ore:ore', self, self)
        game_world.add_collision_pair_radius_limited('ore:hoover_vacuum', self, None, None)
        game_world.add_collision_pair_bb('spider_mine_barrier:ore', None, self)

    def update(self):
        self.stateMachine.update()

    def draw(self):
        self.stateMachine.draw()

        camera = get_camera()
        view_x, view_y = camera.world_to_view(self.x, self.y)
        draw_circle(view_x, view_y, int(self.collision_range * camera.zoom), 255)

    def handle_event(self, event):
        pass

    def get_bb(self):
        half_w = self.w // 2
        half_h = self.h // 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        if group == 'ore:tile':
            self.ground_friction(other)

        elif group == 'ore:ore':
            dx = other.x - self.x
            dy = other.y - self.y
            dist = math.hypot(dx, dy)
            if dist < self.collision_range + other.collision_range:
                self.resolve_collision(self, other, dx, dy, dist)

        elif group == 'ore:hoover_vacuum':
            if other[0].Vacuuming:
                self.apply_attraction(other[0].x, other[0].y, HOOVER_VACUUM_POWER)

        elif group == 'spider_mine_barrier:ore':
            self.stopped_by_barrier(other)


    def caught_by_hoover(self, hoover):
        game_world.remove_object(self)

    def stopped_by_barrier(self, barrier):
        self.x = barrier.x + barrier.w // 2 + self.w // 2 + 1
        self.vx = 0
        self.vy = 0

    def ground_friction(self, ground):
        """타일과의 충돌 처리 및 마찰 적용"""
        half_w = self.w // 2
        half_h = self.h // 2

        # 중심 간 벡터
        dx = self.x - ground.x
        dy = self.y - ground.y

        # 침투 깊이 계산
        x_overlap = (TILE_SIZE_PIXEL // 2 + half_w) - abs(dx)
        y_overlap = (TILE_SIZE_PIXEL // 2 + half_h) - abs(dy)

        # 최소 침투 축이 충돌 법선
        if x_overlap < y_overlap:
            # X축 충돌 (좌우 벽)
            normal = (1 if dx > 0 else -1, 0)
            penetration = x_overlap
        else:
            # Y축 충돌 (위아래)
            normal = (0, 1 if dy > 0 else -1)
            penetration = y_overlap

        # 위치 보정
        self.x += normal[0] * penetration
        self.y += normal[1] * penetration

        # 법선 방향 속도 성분
        vel_normal = self.vx * normal[0] + self.vy * normal[1]

        # 법선 방향으로 접근 중이면 반발
        if vel_normal < 0:
            # 법선 방향 속도 제거
            self.vx -= normal[0] * vel_normal * (1 + self.restitution)
            self.vy -= normal[1] * vel_normal * (1 + self.restitution)

        # 접선 방향 (마찰 적용)
        tangent = (-normal[1], normal[0])

        # 접촉점에서의 접선 방향 속도
        # = 중심의 접선 속도 + 회전에 의한 속도
        contact_vel_tangent = (self.vx * tangent[0] + self.vy * tangent[1])

        # 속도가 매우 작으면 완전 정지
        velocity_threshold = 5.0  # 픽셀/초
        if abs(contact_vel_tangent) < velocity_threshold:
            self.vx -= tangent[0] * contact_vel_tangent
            self.vy -= tangent[1] * contact_vel_tangent

    def resolve_collision(self, body1, body2, dx, dy, dist):
        """광석끼리의 충돌 처리"""
        if dist == 0:
            return

        # 법선 벡터 (정규화)
        nx = dx / dist
        ny = dy / dist

        # 침투 깊이
        overlap = body1.collision_range + body2.collision_range - dist

        if overlap <= 0:
            return

        # 위치 보정 (질량 비율로 분배)
        total_mass = body1.mass + body2.mass
        ratio1 = body2.mass / total_mass
        ratio2 = body1.mass / total_mass

        body1.x -= nx * overlap * ratio1
        body1.y -= ny * overlap * ratio1
        body2.x += nx * overlap * ratio2
        body2.y += ny * overlap * ratio2

        # 상대 속도
        rv_x = body2.vx - body1.vx
        rv_y = body2.vy - body1.vy

        # 법선 방향 상대 속도
        vel_along_normal = rv_x * nx + rv_y * ny

        # 이미 멀어지고 있으면 무시
        if vel_along_normal > 0:
            return

        # 반발 계수
        e = (body1.restitution + body2.restitution) * 0.5

        # 임펄스 크기
        j = -(1 + e) * vel_along_normal
        j /= (1 / body1.mass + 1 / body2.mass)

        # 임펄스 적용
        impulse_x = j * nx
        impulse_y = j * ny

        body1.vx -= impulse_x / body1.mass
        body1.vy -= impulse_y / body1.mass
        body2.vx += impulse_x / body2.mass
        body2.vy += impulse_y / body2.mass

    def apply_force(self, fx, fy):
        """외부 힘 적용 (인력 등)"""
        self.ax += fx / self.mass
        self.ay += fy / self.mass

    def apply_attraction(self, target_x, target_y, strength=50000):
        """특정 지점으로 끌어당기는 힘"""
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)

        if dist > 0:
            # 거리 제곱에 반비례
            force_magnitude = strength / (dist ** HOOVER_VACUUM_DAMPING) % (HOOVER_VACUUM_POWER / 4)  # 최대 힘 제한
            # 정규화된 방향 * 힘
            fx = (dx / dist) * force_magnitude
            fy = (dy / dist) * force_magnitude
            self.apply_force(fx, fy)