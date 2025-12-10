from functools import wraps

from pico2d import *
import math
from pinput import space_down, right_down, right_up, left_down, left_up, is_right_pressed, is_left_pressed, \
    is_lshift_pressed, is_d_pressed, a_down, is_a_pressed, s_down
import time
import game_framework
import game_world
from fire import Fire

from state_machine import StateMachine
from sword import Sword_range
import common

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

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
DASH_SPEED_KMPH = 70.0  # Km / Hour  성인은 평균적으로 한시간에 약 4~5킬로미터 정도 걷는다고함.
DASH_SPEED_MPM = (DASH_SPEED_KMPH * 1000.0 / 60.0)
DASH_SPEED_MPS = (DASH_SPEED_MPM / 60.0)
DASH_SPEED_PPS = (DASH_SPEED_MPS * PIXEL_PER_METER)

on_land = lambda e: e[0] == 'LAND'
not_walking = lambda e: e[0] == 'NOT_WALKING'
enter_idle_press_key = lambda e: e[0] == 'ENTER_IDLE_PRESS_KEY'
enter_run = lambda e: e[0] == 'ENTER_RUN'
enter_walk = lambda e: e[0] == 'ENTER_WALK'
enter_dash = lambda e: e[0] == 'ENTER_DASH'
time_out = lambda e: e[0] == 'TIMEOUT'

# 플레이어 클래스
class Idle:
    def __init__(self, player):
        self.player = player
        self.swing_time = 0
        self.swing_duration = 0.2  # 칼 휘두르기 모션 시간(초)
    def enter(self, e):
        self.player.velocity_x = 0
        self.player.jump = 2
        self.swing_time = 0

        # s_down 이벤트에서 enter가 호출되면 swing 시작
        if s_down(e):
            if not self.player.swing:
                self.player.swing_sword()
                self.swing_time = 0

    def exit(self, e):
        if a_down(e):
            self.player.fire_ball()

    def do(self):
        # swing 진행 중 타이머 업데이트
        if self.player.swing:
            self.swing_time += game_framework.frame_time
            if self.swing_time >= self.swing_duration:
                self.player.swing = False
                self.swing_time = 0


        # 좌우 이동 체크
        if is_left_pressed() and is_right_pressed():
            pass
        else:
            if is_left_pressed() and not is_right_pressed():
                self.player.face_dir = -1
                self.player.state_machine.handle_state_event(('ENTER_IDLE_PRESS_KEY', None))
            if is_right_pressed() and not is_left_pressed():
                self.player.face_dir = 1
                self.player.state_machine.handle_state_event(('ENTER_IDLE_PRESS_KEY', None))


        # 현재 위치가 ground보다 높으면 떨어뜨림
        if self.player.y > self.player.ground:
            self.player.velocity_y = -800 * game_framework.frame_time
            self.player.y += self.player.velocity_y
            if self.player.y < self.player.ground:
                self.player.y = self.player.ground
        else:
            self.player.y = self.player.ground

    def draw(self):
        # print(self.player.x, self.player.y, self.player.ground)
        scale = 3
        weapon_scale = 3.5

        sx_ = self.player.x - common.map.window_left
        sy_ = self.player.y - common.map.window_bottom

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, sy_,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, sy_,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = sy_ + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, head_y,
                sw * scale, sh * scale
            )

        # 왼쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_y = sy_ - 4 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_y = sy_ - 4 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 왼쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_y = sy_ - 1 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_y = sy_ - 1 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 칼 그리기
        if not self.player.swing:
            sx, sy, sw, sh = 89, 139, 17, 7
            arm_y = sy_ - 4 * weapon_scale
            if self.player.face_dir == -1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    0, '',
                    sx_ - 6 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
            elif self.player.face_dir == 1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    3.141592, '',
                    sx_ + 6 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
        else:
            angle = -math.pi / 2 + math.pi * (self.swing_time / self.swing_duration)

            sx, sy, sw, sh = 89, 139, 17, 7
            arm_y = sy_ - (4 + int(angle * 4)) * weapon_scale
            if self.player.face_dir == -1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    angle, '',
                    sx_ - 4 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
            elif self.player.face_dir == 1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    3.141592 - angle, '',
                    sx_ + 4 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )


class Walk:
    def __init__(self, player):
        self.player = player
        self.swing_time = 0
        self.swing_duration = 0.2  # 칼 휘두르기 모션 시간(초)

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
        elif left_up(e):
            if is_right_pressed():
                self.player.dir = self.player.face_dir = 1
            else:
                self.player.face_dir = -1
                self.player.state_machine.handle_state_event(('NOT_WALKING', None))
        elif right_up(e):
            if is_left_pressed():
                self.player.dir = self.player.face_dir = -1
            else:
                self.player.face_dir = 1
                self.player.state_machine.handle_state_event(('NOT_WALKING', None))

        # s_down 이벤트에서 enter가 호출되면 swing 시작
        if s_down(e):
            if not self.player.swing:
                self.player.swing_sword()
                self.swing_time = 0

    def exit(self, e):
        self.player.velocity_x = 0  # 멈춤
        if a_down(e):
            self.player.fire_ball()


    def do(self):
        # swing 진행 중 타이머 업데이트


        if self.player.swing:
            self.swing_time += game_framework.frame_time
            if self.swing_time >= self.swing_duration:
                self.player.swing = False
                self.swing_time = 0

        if is_lshift_pressed():
            self.player.state_machine.handle_state_event(('ENTER_RUN', None))
        if is_d_pressed() and self.player.can_dash:
            self.player.can_dash = False
            self.player.state_machine.handle_state_event(('ENTER_DASH', None))

        self.player.x += self.player.dir * WALK_SPEED_PPS * game_framework.frame_time


        # 화면 범위 제한
        # if self.player.x < 50:
        #     self.player.x = 50
        # if self.player.x > 1230:
        #     self.player.x = 1230

        # 현재 위치가 ground보다 높으면 떨어뜨림
        if self.player.y > self.player.ground:
            self.player.velocity_y = -800 * game_framework.frame_time
            self.player.y += self.player.velocity_y
            if self.player.y < self.player.ground:
                self.player.y = self.player.ground
        else:
            self.player.y = self.player.ground

    def draw(self):
        scale = 3
        weapon_scale = 3.5
        walk_time = self.player.time * 2 * math.pi

        sx_ = self.player.x - common.map.window_left
        sy_ = self.player.y - common.map.window_bottom

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, sy_,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, sy_,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = sy_ + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, head_y,
                sw * scale, sh * scale
            )

        # 왼쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_offset_l = math.sin(walk_time) * 4
        leg_y = sy_ - 4 * scale + leg_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_offset_r = -math.sin(walk_time) * 4
        leg_y = sy_ - 4 * scale + leg_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 왼쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_offset_l = math.sin(walk_time + math.pi) * 3
        arm_y = sy_ - 1 * scale + arm_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_offset_r = -math.sin(walk_time + math.pi) * 3
        arm_y = sy_ - 1 * scale + arm_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 칼 그리기 (걷기 애니메이션)
        if not self.player.swing:
            sx, sy, sw, sh = 89, 139, 17, 7
            arm_offset_l = math.sin(walk_time + math.pi) * 3
            arm_y = sy_ - 1 * weapon_scale + arm_offset_l
            if self.player.face_dir == -1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    0, '',
                    sx_ - 6 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
            elif self.player.face_dir == 1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    3.141592, '',
                    sx_ + 6 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
        else:
            # 칼 휘두르기 모션
            angle = -math.pi / 2 + math.pi * (self.swing_time / self.swing_duration)
            sx, sy, sw, sh = 89, 139, 17, 7
            arm_y = sy_ - (4 + int(angle * 4)) * weapon_scale
            if self.player.face_dir == -1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    angle, '',
                    sx_ - 4 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
            elif self.player.face_dir == 1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    3.141592 - angle, '',
                    sx_ + 4 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )


class Run:
    def __init__(self, player):
        self.player = player
        self.swing_time = 0
        self.swing_duration = 0.2  # 칼 휘두르기 모션 시간(초)

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

        if s_down(e):
            if not self.player.swing:
                self.player.swing_sword()
                self.swing_time = 0


    def exit(self, e):
        self.player.velocity_x = 0  # 멈춤
        if a_down(e):
            self.player.fire_ball()

    def do(self):
        if is_d_pressed() and self.player.can_dash:
            self.player.can_dash = False
            self.player.state_machine.handle_state_event(('ENTER_DASH', None))
        if not is_lshift_pressed():
            self.player.state_machine.handle_state_event(('ENTER_WALK', None))

        self.player.x += self.player.dir * RUN_SPEED_PPS * game_framework.frame_time

        # 플랫폼 체크 및 중력 적용
        # self.check_platform()

        if self.player.swing:
            self.swing_time += game_framework.frame_time
            if self.swing_time >= self.swing_duration:
                self.player.swing = False
                self.swing_time = 0

        # 화면 범위 제한
        if self.player.x < 50:
            self.player.x = 50
        if self.player.x > 1230:
            self.player.x = 1230


        # 현재 위치가 ground보다 높으면 떨어뜨림
        if self.player.y > self.player.ground:
            self.player.velocity_y = -800 * game_framework.frame_time
            self.player.y += self.player.velocity_y
            if self.player.y < self.player.ground:
                self.player.y = self.player.ground
        else:
            self.player.y = self.player.ground

    def draw(self):
        # print(self.player.dir)
        scale = 3
        weapon_scale = 3.5
        walk_time = self.player.time * 4 * math.pi

        sx_ = self.player.x - common.map.window_left
        sy_ = self.player.y - common.map.window_bottom

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, sy_,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, sy_,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = sy_ + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, head_y,
                sw * scale, sh * scale
            )

        # 왼쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_offset_l = math.sin(walk_time) * 4
        leg_y = sy_ - 4 * scale + leg_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_offset_r = -math.sin(walk_time) * 4
        leg_y = sy_ - 4 * scale + leg_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 왼쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_offset_l = math.sin(walk_time + math.pi) * 3
        arm_y = sy_ - 1 * scale + arm_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_offset_r = -math.sin(walk_time + math.pi) * 3
        arm_y = sy_ - 1 * scale + arm_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 칼 그리기 (걷기 애니메이션)
        if not self.player.swing:
            sx, sy, sw, sh = 89, 139, 17, 7
            arm_offset_l = math.sin(walk_time + math.pi) * 3
            arm_y = sy_ - 1 * weapon_scale + arm_offset_l
            if self.player.face_dir == -1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    0, '',
                    sx_ - 6 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
            elif self.player.face_dir == 1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    3.141592, '',
                    sx_ + 6 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
        else:
            # 칼 휘두르기 모션
            angle = -math.pi / 2 + math.pi * (self.swing_time / self.swing_duration)
            sx, sy, sw, sh = 89, 139, 17, 7
            arm_y = sy_ - (4 + int(angle * 4)) * weapon_scale
            if self.player.face_dir == -1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    angle, '',
                    sx_ - 4 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
            elif self.player.face_dir == 1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    3.141592 - angle, '',
                    sx_ + 4 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )


class Jump:
    def __init__(self, player):
        self.player = player
        self.player.jump = 2
        self.player.ground = 90


    def enter(self, e):
        self.player.jump -= 1
        if not a_down(e) and not right_down(e) and not left_down(e) and self.player.jump >= 0:
            self.player.velocity_y = 300  # 점프 초기 속도 (위쪽)
            self.player.gravity = -800    # 중력 (아래쪽)
        if right_down(e):
            self.player.face_dir = self.player.dir =  1
        elif left_down(e):
            self.player.face_dir = self.player.dir =  -1

    def exit(self, e):
        if a_down(e):
            self.player.fire_ball()

        self.player.velocity_y = 0    # 점프 종료 시 수직 속도 초기화

    def do(self):
        # 중력 적용
        self.player.velocity_y += self.player.gravity * game_framework.frame_time
        # 수직 이동
        self.player.y += self.player.velocity_y * game_framework.frame_time


        # 지면에 착지 확인
        if self.player.y <= self.player.ground:
            self.player.y = self.player.ground
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
        scale = 3
        weapon_scale = 3.5

        sx_ = self.player.x - common.map.window_left
        sy_ = self.player.y - common.map.window_bottom

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, sy_,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, sy_,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = sy_ + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, head_y,
                sw * scale, sh * scale
            )

        # 점프 시 다리는 위로 접힌 모습
        # 왼쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_y = sy_ - 2 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_y = sy_ - 2 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 점프 시 팔은 위로 뻗은 모습
        # 왼쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_y = sy_ + 1 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_y = sy_ + 1 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 칼 그리기
        sx, sy, sw, sh = 89, 139, 17, 7
        arm_y = sy_ + 1 * weapon_scale
        if self.player.face_dir == -1:
            self.player.weapon_image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 6 * weapon_scale, arm_y,
                sw * weapon_scale, sh * weapon_scale
            )
        elif self.player.face_dir == 1:
            self.player.weapon_image.clip_composite_draw(
                sx, sy, sw, sh,
                3.141592, '',
                sx_ + 6 * weapon_scale, arm_y,
                sw * weapon_scale, sh * weapon_scale
            )


class Dash:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dash_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        self.player.x += self.player.dir * DASH_SPEED_PPS * game_framework.frame_time

        # 화면 범위 제한
        if self.player.x < 50:
            self.player.x = 50
        if self.player.x > 1230:
            self.player.x = 1230

        if get_time() - self.player.dash_time > 0.2:
            self.player.state_machine.handle_state_event(('ENTER_WALK', None))

        # 현재 위치가 ground보다 높으면 떨어뜨림
        if self.player.y > self.player.ground:
            self.player.velocity_y = -800 * game_framework.frame_time
            self.player.y += self.player.velocity_y
            if self.player.y < self.player.ground:
                self.player.y = self.player.ground
        else:
            self.player.y = self.player.ground

    def draw(self):
        scale = 3
        weapon_scale = 3.5
        walk_time = self.player.time * 2 * math.pi

        sx_ = self.player.x - common.map.window_left
        sy_ = self.player.y - common.map.window_bottom

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, sy_,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, sy_,
                sw * scale, sh * scale
            )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = sy_ + 6 * scale
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_, head_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_, head_y,
                sw * scale, sh * scale
            )

        # 왼쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_offset_l = math.sin(walk_time) * 4
        leg_y = sy_ - 4 * scale + leg_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 오른쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_offset_r = -math.sin(walk_time) * 4
        leg_y = sy_ - 4 * scale + leg_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 1 * scale, leg_y,
                sw * scale, sh * scale
            )

        # 왼쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_offset_l = math.sin(walk_time + math.pi) * 3
        arm_y = sy_ - 1 * scale + arm_offset_l
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ - 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 오른쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_offset_r = -math.sin(walk_time + math.pi) * 3
        arm_y = sy_ - 1 * scale + arm_offset_r
        if self.player.face_dir == -1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, '',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )
        elif self.player.face_dir == 1:
            self.player.image.clip_composite_draw(
                sx, sy, sw, sh,
                0, 'h',
                sx_ + 3 * scale, arm_y,
                sw * scale, sh * scale
            )

        # 칼 그리기 (걷기 애니메이션)
        if not self.player.swing:
            sx, sy, sw, sh = 89, 139, 17, 7
            arm_offset_l = math.sin(walk_time + math.pi) * 3
            arm_y = sy_ - 1 * weapon_scale + arm_offset_l
            if self.player.face_dir == -1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    0, '',
                    sx_ - 6 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
            elif self.player.face_dir == 1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    3.141592, '',
                    sx_ + 6 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
        else:
            # 칼 휘두르기 모션
            angle = -math.pi / 2 + math.pi * (self.swing_time / self.swing_duration)
            sx, sy, sw, sh = 89, 139, 17, 7
            arm_y = sy_ - (4 + int(angle * 4)) * weapon_scale
            if self.player.face_dir == -1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    angle, '',
                    sx_ - 4 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )
            elif self.player.face_dir == 1:
                self.player.weapon_image.clip_composite_draw(
                    sx, sy, sw, sh,
                    3.141592 - angle, '',
                    sx_ + 4 * weapon_scale, arm_y,
                    sw * weapon_scale, sh * weapon_scale
                )


class Player:
    fire_sound = None

    def __init__(self):
        if not Player.fire_sound:
            Player.fire_sound = load_wav('sound/flame.ogg')
            Player.fire_sound.set_volume(32)

        self.x, self.y = 100, 90
        self.velocity_x = 0  # 좌우 속도
        self.velocity_y = 0  # 수직 속도
        self.gravity = 0     # 중력
        self.dir = 0  # 1: 오른쪽, -1: 왼쪽
        self.face_dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.image = load_image('avatar_body0000.png')
        self.weapon_image = load_image('weapons01.png')
        self.Mp_image = load_image('player_MP.png')
        self.time = 0
        self.jump = 2

        self.life = 5
        self.Mp = 3
        self.islife_down = False
        self.life_notdown_timer = 0

        self.ground = 90

        self.swing = False
        self.sword_range = None

        self.isInPortal = False

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.JUMP = Jump(self)
        self.RUN = Run(self)
        self.DASH = Dash(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {s_down: self.IDLE, a_down: self.IDLE, right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK, enter_idle_press_key: self.WALK, space_down: self.JUMP},
                self.WALK: {s_down: self.WALK, right_down: self.WALK, left_down: self.WALK, right_up: self.WALK, left_up: self.WALK, not_walking: self.IDLE, space_down: self.JUMP, enter_run: self.RUN, enter_dash: self.DASH, a_down: self.WALK},
                self.JUMP: {on_land: self.IDLE, a_down: self.JUMP, space_down: self.JUMP, right_down: self.JUMP, left_down: self.JUMP},
                self.RUN: {s_down: self.RUN, right_down: self.RUN, left_down: self.RUN, right_up: self.IDLE, left_up: self.IDLE, not_walking: self.IDLE, space_down: self.JUMP, enter_walk: self.WALK, enter_dash: self.DASH, a_down: self.RUN},
                self.DASH: {enter_walk: self.WALK},
            }
        )

        # 스프라이트 정보 (x, y, w, h)
        self.sprite_head = (0, 20, 16, 12)
        self.sprite_body = (0, 10, 10, 10)
        self.sprite_arm_l = (22, 14, 2, 4)
        self.sprite_arm_r = (26, 14, 2, 4)
        self.sprite_leg_l = (3, 0, 2, 4)
        self.sprite_leg_r = (9, 0, 2, 4)

        #Mp 자동회복
        self.last_Mp_recover_time = get_time()
        #dash용 시간측정
        self.last_dash_time = get_time()
        self.can_dash = True

    def update(self):
        self.isInPortal = False
        self.time += game_framework.frame_time
        self.state_machine.update()

        self.x = clamp(0.0, self.x, common.map.w - 1)
        self.y = clamp(0.0, self.y, common.map.h - 1)

        # print(self.x, common.map.w)

        if get_time() - self.last_Mp_recover_time > 15.0:
            if self.Mp < 3:
                self.Mp += 1
            self.last_Mp_recover_time = get_time()

        if get_time() - self.last_dash_time > 5.0:
            self.can_dash = True
            self.last_dash_time = get_time()



        if get_time() - self.life_notdown_timer > 2.0:
            self.islife_down = False

        if hasattr(self, 'candidate_grounds') and self.candidate_grounds:
            self.ground = max(self.candidate_grounds)
            self.candidate_grounds = []
        else:
            self.ground = 90

        if not self.swing and self.sword_range:
            game_world.remove_object(self.sword_range)
            self.sword_range = None
            pass

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        sx_ = self.x - common.map.window_left
        sy_ = self.y - common.map.window_bottom
        self.Mp_image.clip_draw(340, 31* (3 - self.Mp), 120, 31, sx_, sy_ + 35, 200 /4 , 40 / 4)
        # draw_rectangle(sx_ - 17, sy_ - 22, sx_ + 17, sy_ + 25)

    def fire_ball(self):
        if self.Mp > 0:
            Player.fire_sound.play()
            self.Mp -= 1
            fire = Fire(self.x+self.face_dir*30, self.y+15, self.face_dir * 8)
            game_world.add_object(fire, 1)
            game_world.add_collision_pair('monster_1:fire', None, fire)
            game_world.add_collision_pair('monster_2:fire', None, fire)
            game_world.add_collision_pair('monster_3:fire', None, fire)

    def swing_sword(self):
        self.swing = True
        self.sword_range = Sword_range(self.x, self.y, self.face_dir)
        game_world.add_object(self.sword_range, 1)
        game_world.add_collision_pair('monster:sword', None, self.sword_range)

    def get_player_x(self):
        return self.x


    # def get_detection_bb(self):
    #     return self.x - 17, self.y - 22, self.x + 17, self.y + 25

    def get_bb(self):
        return self.x - 17, self.y - 22, self.x + 17, self.y + 25

    def handle_collision(self, group, other):
        left, bottom, right, top = other.get_bb()
        if group == 'tile:player':
            if self.y > top and left <= self.x <= right:
                if not hasattr(self, 'candidate_grounds'):
                    self.candidate_grounds = []
                self.candidate_grounds.append(top + 18)
        if group in ('monster_1:player', 'monster_2:player', 'monster_3:player', 'monster_boss:player'):
            if self.life > 0 and not self.islife_down:
                if self.x <=  other.x:
                    self.x -= 20
                elif self.x > other.x:
                    self.x += 20
                self.life -= 1
                self.islife_down = True
                self.life_notdown_timer = get_time()

            print('몬스터와 충돌함')
            print(self.life)

        if group  == 'monster_boss_left:player':
            if self.life > 0 and not self.islife_down and common.monster_boss_left_hand.life > 0:
                if self.x <= other.x:
                    self.x -= 20
                elif self.x > other.x:
                    self.x += 20
                self.life -= 1
                self.islife_down = True
                self.life_notdown_timer = get_time()

            print('몬스터와 충돌함')
            print(self.life)

        if group  == 'monster_boss_right:player':
            if self.life > 0 and not self.islife_down and common.monster_boss_right_hand.life > 0:
                if self.x <= other.x:
                    self.x -= 20
                elif self.x > other.x:
                    self.x += 20
                self.life -= 1
                self.islife_down = True
                self.life_notdown_timer = get_time()

            print('몬스터와 충돌함')
            print(self.life)


        if group == 'portal:player':
            self.isInPortal = True
            print('포탈과 충돌함')

        if group == 'item:player':
            print('아이템과 충돌함')
            if other.Mp_or_Hp == 0:
                if self.Mp < 3:
                    self.Mp = min(3, self.Mp + 2)

            elif other.Mp_or_Hp == 1:
                if self.life < 5:
                    self.life += 1

        if group == 'boss_fire:player':
            if self.life > 0 and not self.islife_down:
                self.life -= 1
                self.islife_down = True
                self.life_notdown_timer = get_time()



    # def handle_detection_collision(self, group, other):
    #     if group == 'detection_monster_1:player':
    #         print('몬스터 감지 범위와 충돌함')
