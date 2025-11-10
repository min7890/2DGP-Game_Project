from pico2d import *
import math
from pinput import key_pressed, process_input

# 게임 초기화
open_canvas(800, 600)

# 이미지 로드



# 플레이어 클래스
class Idle:
    pass


class Walk:
    pass


class Run:
    pass


class Jump:
    pass


class Player:
    def __init__(self):

        self.x, self.y = 400, 300
        self.velocity_x = 0  # 좌우 속도
        self.direction = 1  # 1: 오른쪽, -1: 왼쪽
        self.frame = 0  # 애니메이션 프레임

        self.image = load_image('avatar_body0000.png')

        self.time = 0

        self.IDLE = Idle(self)
        self.WALK = Walk(self)
        self.RUN = Run(self)
        self.JUMP = Jump(self)
        

        # 스프라이트 정보 (x, y, w, h)
        self.sprite_head = (0, 20, 16, 12)
        self.sprite_body = (0, 10, 10, 10)
        self.sprite_arm_l = (22, 14, 2, 4)
        self.sprite_arm_r = (26, 14, 2, 4)
        self.sprite_leg_l = (3, 0, 2, 4)
        self.sprite_leg_r = (9, 0, 2, 4)

    def update(self, delta_time):
        self.time += delta_time

        # 키 입력 처리
        self.velocity_x = 0
        if key_pressed(SDLK_a):
            self.velocity_x = -200
            self.direction = -1
        elif key_pressed(SDLK_d):
            self.velocity_x = 200
            self.direction = 1

        # 위치 업데이트
        self.x += self.velocity_x * delta_time

        # 화면 범위 제한
        if self.x < 50:
            self.x = 50
        if self.x > 750:
            self.x = 750

    def draw(self):
        # 스케일 (확대 배율)
        scale = 3

        # 걷기 애니메이션을 위한 시간 값
        walk_time = self.time * 10 if abs(self.velocity_x) > 0 else 0

        # 몸통 그리기 (중심)
        sx, sy, sw, sh = self.sprite_body
        self.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.direction < 0 else '',
            self.x, self.y,
            sw * scale, sh * scale
        )

        # 머리 그리기
        sx, sy, sw, sh = self.sprite_head
        head_y = self.y + 6 * scale
        self.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, ' ' if self.direction < 0 else 'h',
            self.x, head_y,
            sw * scale, sh * scale
        )

        # 왼쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.sprite_leg_l
        leg_offset_l = math.sin(walk_time) * 4 if abs(self.velocity_x) > 0 else 0
        leg_y = self.y - 4 * scale + leg_offset_l
        self.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.direction < 0 else '',
            self.x - 1 * scale, leg_y,
            sw * scale, sh * scale
        )

        # 오른쪽 다리 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.sprite_leg_r
        leg_offset_r = -math.sin(walk_time) * 4 if abs(self.velocity_x) > 0 else 0
        leg_y = self.y - 4 * scale + leg_offset_r
        self.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.direction < 0 else '',
            self.x + 1 * scale, leg_y,
            sw * scale, sh * scale
        )

        # 왼쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.sprite_arm_l
        arm_offset_l = math.sin(walk_time + math.pi) * 3 if abs(self.velocity_x) > 0 else 0
        arm_y = self.y - 1 * scale + arm_offset_l
        self.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.direction < 0 else '',
            self.x - 3 * scale, arm_y,
            sw * scale, sh * scale
        )

        # 오른쪽 팔 그리기 (걷기 애니메이션)
        sx, sy, sw, sh = self.sprite_arm_r
        arm_offset_r = -math.sin(walk_time + math.pi) * 3 if abs(self.velocity_x) > 0 else 0
        arm_y = self.y - 1 * scale + arm_offset_r
        self.image.clip_composite_draw(
            sx, sy, sw, sh,
            0, 'h' if self.direction < 0 else '',
            self.x + 3 * scale, arm_y,
            sw * scale, sh * scale
        )


# 플레이어 생성
player = Player()

# 게임 루프
running = True
last_time = get_time()

while running:
    clear_canvas()

    # 델타 타임 계산
    current_time = get_time()
    delta_time = current_time - last_time
    last_time = current_time

    # 이벤트 처리
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

    # 입력 처리 (업데이트 전에 호출해야 함)
    process_input(events)

    # 업데이트
    player.update(delta_time)

    # 그리기
    player.draw()

    # 간단한 텍스트 대신 배경만 표시

    update_canvas()

    delay(0.01)

close_canvas()