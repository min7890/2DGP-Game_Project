from pico2d import *
import math
from pinput import space_down, right_down, right_up, left_down, left_up, is_right_pressed, is_left_pressed, is_lshift_pressed
import time
import game_framework

from state_machine import StateMachine

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
WALK_SPEED_KMPH = 5.0  # Km / Hour  성인은 평균적으로 한시간에 약 4~5킬로미터 정도 걷는다고함.
WALK_SPEED_MPM = (WALK_SPEED_KMPH * 1000.0 / 60.0)
WALK_SPEED_MPS = (WALK_SPEED_MPM / 60.0)
WALK_SPEED_PPS = (WALK_SPEED_MPS * PIXEL_PER_METER)

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour  성인은 평균적으로 한시간에 약 4~5킬로미터 정도 걷는다고함.
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


on_land = lambda e: e[0] == 'LAND'
not_walking = lambda e: e[0] == 'NOT_WALKING'
enter_idle_press_key = lambda e: e[0] == 'ENTER_IDLE_PRESS_KEY'
enter_run = lambda e: e[0] == 'ENTER_RUN'
enter_walk = lambda e: e[0] == 'ENTER_WALK'


# 플레이어 클래스
class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.velocity_x = 0

    def exit(self, e):
        if is_left_pressed():
            self.player.dir = self.face_dir = -1
        elif is_right_pressed():
            self.player.dir = self.face_dir = 1
        pass

    def do(self):
        if is_left_pressed() and is_right_pressed():
            pass
        else:
            if is_left_pressed():
                self.player.state_machine.handle_state_event(('ENTER_IDLE_PRESS_KEY', None))

            if is_right_pressed():
                self.player.state_machine.handle_state_event(('ENTER_IDLE_PRESS_KEY', None))
        pass

    def draw(self):
        scale = 3

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x, self.player.y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x, self.player.y,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = self.player.y + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x, head_y,
                sw * scale, sh * scale
            )

        # 왼쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_y = self.player.y - 4 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_y = self.player.y - 4 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 왼쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_y = self.player.y - 1 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_y = self.player.y - 1 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x + 3 * scale, arm_y,
                sw * scale, sh * scale
            )


class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if right_down(e):
            if is_left_pressed():
                self.player.face_dir = 1
                self.player.state_machine.handle_state_event(('NOT_WALKING', None))
            else:
                self.player.dir = self.player.face_dir = 1
        elif left_down(e):
            if is_right_pressed():
                self.player.face_dir = -1
                self.player.state_machine.handle_state_event(('NOT_WALKING', None))
            else:
                self.player.dir = self.player.face_dir = -1



    def exit(self, e):
        self.player.velocity_x = 0  # 멈춤

    def do(self):
        if is_lshift_pressed():
            self.player.state_machine.handle_state_event(('ENTER_RUN', None))
        self.player.x += self.player.dir * WALK_SPEED_PPS * game_framework.frame_time
        # 화면 범위 제한
        if self.player.x < 50:
            self.player.x = 50
        if self.player.x > 1230:
            self.player.x = 1230

    def draw(self):
        # print(self.player.dir)
        scale = 3
        walk_time = self.player.time * 2 * math.pi

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x, self.player.y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x, self.player.y,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = self.player.y + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x, head_y,
                sw * scale, sh * scale
            )

        # 왼쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_offset_l = math.sin(walk_time) * 4
        leg_y = self.player.y - 4 * scale + leg_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_offset_r = -math.sin(walk_time) * 4
        leg_y = self.player.y - 4 * scale + leg_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 왼쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_offset_l = math.sin(walk_time + math.pi) * 3
        arm_y = self.player.y - 1 * scale + arm_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_offset_r = -math.sin(walk_time + math.pi) * 3
        arm_y = self.player.y - 1 * scale + arm_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x + 3 * scale, arm_y,
                sw * scale, sh * scale
            )

class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if right_down(e):
            if is_left_pressed():
                self.player.face_dir = 1
                self.player.state_machine.handle_state_event(('NOT_WALKING', None))
            else:
                self.player.dir = self.player.face_dir = 1
        elif left_down(e):
            if is_right_pressed():
                self.player.face_dir = -1
                self.player.state_machine.handle_state_event(('NOT_WALKING', None))
            else:
                self.player.dir = self.player.face_dir = -1


    def exit(self, e):
        self.player.velocity_x = 0  # 멈춤

    def do(self):
        if not is_lshift_pressed():
            self.player.state_machine.handle_state_event(('ENTER_WALK', None))
        self.player.x += self.player.dir * RUN_SPEED_PPS * game_framework.frame_time
        # 화면 범위 제한
        if self.player.x < 50:
            self.player.x = 50
        if self.player.x > 1230:
            self.player.x = 1230

    def draw(self):
        # print(self.player.dir)
        scale = 3
        walk_time = self.player.time * 4 * math.pi

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x, self.player.y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x, self.player.y,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = self.player.y + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x, head_y,
                sw * scale, sh * scale
            )

        # 왼쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_offset_l = math.sin(walk_time) * 4
        leg_y = self.player.y - 4 * scale + leg_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_offset_r = -math.sin(walk_time) * 4
        leg_y = self.player.y - 4 * scale + leg_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 왼쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_offset_l = math.sin(walk_time + math.pi) * 3
        arm_y = self.player.y - 1 * scale + arm_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_offset_r = -math.sin(walk_time + math.pi) * 3
        arm_y = self.player.y - 1 * scale + arm_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x + 3 * scale, arm_y,
                sw * scale, sh * scale
            )

class Jump:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.velocity_y = 300  # 점프 초기 속도 (위쪽)
        self.player.gravity = -800    # 중력 (아래쪽)

    def exit(self, e):
        self.player.velocity_y = 0    # 점프 종료 시 수직 속도 초기화

    def do(self):
        # 중력 적용
        self.player.velocity_y += self.player.gravity * game_framework.frame_time
        # 수직 이동
        self.player.y += self.player.velocity_y * game_framework.frame_time

        # 지면에 착지 확인 (y = 300이 지면)
        if self.player.y <= 300:
            self.player.y = 300
            self.player.velocity_y = 0
            self.player.state_machine.handle_state_event(('LAND', None))

        # 화면 범위 제한 (좌우 이동 가능)
        if self.player.dir != 0:
            self.player.x += self.player.dir * WALK_SPEED_PPS * game_framework.frame_time
            if self.player.x < 50:
                self.player.x = 50
            if self.player.x > 1230:
                self.player.x = 1230

    def draw(self):
        print('JUMP')
        scale = 3

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x, self.player.y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x, self.player.y,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = self.player.y + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x, head_y,
                sw * scale, sh * scale
            )

        # 점프 시 다리는 위로 접힌 모습
        # 왼쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_y = self.player.y - 2 * scale  # 평상시보다 2픽셀 위로
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_y = self.player.y - 2 * scale  # 평상시보다 2픽셀 위로
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 점프 시 팔은 위로 뻗은 모습
        # 왼쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_y = self.player.y + 1 * scale  # 평상시보다 2픽셀 위로
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_y = self.player.y + 1 * scale  # 평상시보다 2픽셀 위로
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                self.player.x + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                self.player.x + 3 * scale, arm_y,
                sw * scale, sh * scale
            )


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.velocity_x = 0  # 좌우 속도
        self.velocity_y = 0  # 수직 속도
        self.gravity = 0     # 중력
        self.dir = 0  # 1: 오른쪽, -1: 왼쪽
        self.face_dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.image = load_image('avatar_body0000.png')
        self.time = 0

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.JUMP = Jump(self)
        self.RUN = Run(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK, enter_idle_press_key: self.WALK, space_down: self.JUMP},
                self.WALK: {right_down: self.WALK, left_down: self.WALK, right_up: self.IDLE, left_up: self.IDLE, not_walking: self.IDLE, space_down: self.JUMP, enter_run: self.RUN},
                self.JUMP: {on_land: self.IDLE},
                self.RUN: {right_down: self.RUN, left_down: self.RUN, right_up: self.IDLE, left_up: self.IDLE, not_walking: self.IDLE, space_down: self.JUMP, enter_walk: self.WALK},
            }
        )

        # 스프라이트 정보 (x, y, w, h)
        self.sprite_head = (0, 20, 16, 12)
        self.sprite_body = (0, 10, 10, 10)
        self.sprite_arm_l = (22, 14, 2, 4)
        self.sprite_arm_r = (26, 14, 2, 4)
        self.sprite_leg_l = (3, 0, 2, 4)
        self.sprite_leg_r = (9, 0, 2, 4)

    def update(self):
        self.time += game_framework.frame_time
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y + 40

    def handle_collision(self, group, other):
        pass
