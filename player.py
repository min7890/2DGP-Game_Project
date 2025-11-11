from pico2d import *
import math
from pinput import space_down, right_down, right_up, left_down, left_up
import time
import game_framework

from state_machine import StateMachine

# 플레이어 클래스
class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.velocity_x = 0

    def exit(self, e):
        pass

    def do(self):
        pass

    def draw(self):
        scale = 3

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.player.dir < 0 else '',
            self.player.x, self.player.y,
            sw * scale, sh * scale
        )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = self.player.y + 6 * scale
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.player.dir < 0 else '',
            self.player.x, head_y,
            sw * scale, sh * scale
        )

        # 왼쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_y = self.player.y - 4 * scale
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.player.dir < 0 else '',
            self.player.x - 1 * scale, leg_y,
            sw * scale, sh * scale
        )

        # 오른쪽 다리 그리기
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_y = self.player.y - 4 * scale
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.player.dir < 0 else '',
            self.player.x + 1 * scale, leg_y,
            sw * scale, sh * scale
        )

        # 왼쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_y = self.player.y - 1 * scale
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.player.dir < 0 else '',
            self.player.x - 3 * scale, arm_y,
            sw * scale, sh * scale
        )

        # 오른쪽 팔 그리기
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_y = self.player.y - 1 * scale
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.player.dir < 0 else '',
            self.player.x + 3 * scale, arm_y,
            sw * scale, sh * scale
        )


class Walk:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if right_down(e):
            self.player.dir = self.player.face_dir = 1
            self.player.velocity_x = 200  # 오른쪽으로 이동
        elif left_down(e):
            self.player.dir = self.player.face_dir = -1
            self.player.velocity_x = -200  # 왼쪽으로 이동

    def exit(self, e):
        self.player.velocity_x = 0  # 멈춤

    def do(self):
        self.player.x += self.player.velocity_x * game_framework.frame_time
        # 화면 범위 제한
        if self.player.x < 50:
            self.player.x = 50
        if self.player.x > 750:
            self.player.x = 750

    def draw(self):
        scale = 3
        walk_time = self.player.time * 10 if abs(self.player.velocity_x) > 0 else 0

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.player.sprite_body
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, ' ' if self.player.dir < 0 else 'h',
            self.player.x, self.player.y,
            sw * scale, sh * scale
        )

        # 머리 그리기
        sx, sy, sw, sh = self.player.sprite_head
        head_y = self.player.y + 6 * scale
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, ' ' if self.player.dir < 0 else 'h',
            self.player.x, head_y,
            sw * scale, sh * scale
        )

        # 왼쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_l
        leg_offset_l = math.sin(walk_time) * 4 if abs(self.player.velocity_x) > 0 else 0
        leg_y = self.player.y - 4 * scale + leg_offset_l
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, ' ' if self.player.dir < 0 else 'h',
            self.player.x - 1 * scale, leg_y,
            sw * scale, sh * scale
        )

        # 오른쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_leg_r
        leg_offset_r = -math.sin(walk_time) * 4 if abs(self.player.velocity_x) > 0 else 0
        leg_y = self.player.y - 4 * scale + leg_offset_r
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, ' ' if self.player.dir < 0 else 'h',
            self.player.x + 1 * scale, leg_y,
            sw * scale, sh * scale
        )

        # 왼쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_l
        arm_offset_l = math.sin(walk_time + math.pi) * 3 if abs(self.player.velocity_x) > 0 else 0
        arm_y = self.player.y - 1 * scale + arm_offset_l
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, ' ' if self.player.dir < 0 else 'h',
            self.player.x - 3 * scale, arm_y,
            sw * scale, sh * scale
        )

        # 오른쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.player.sprite_arm_r
        arm_offset_r = -math.sin(walk_time + math.pi) * 3 if abs(self.player.velocity_x) > 0 else 0
        arm_y = self.player.y - 1 * scale + arm_offset_r
        self.player.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, ' ' if self.player.dir < 0 else 'h',
            self.player.x + 3 * scale, arm_y,
            sw * scale, sh * scale
        )


class Player:
    def __init__(self):
        self.x, self.y = 400, 300
        self.velocity_x = 0  # 좌우 속도
        self.dir = 0  # 1: 오른쪽, -1: 왼쪽
        self.face_dir = 1  # 1: 오른쪽, -1: 왼쪽
        self.image = load_image('avatar_body0000.png')
        self.time = 0

        self.IDLE = Idle(self)
        self.WALK = Walk(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE: {right_down: self.WALK, left_down: self.WALK},
                self.WALK: {right_up: self.IDLE, left_up: self.IDLE}
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
