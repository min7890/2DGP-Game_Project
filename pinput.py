from pico2d import *
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_LSHIFT, SDLK_d

# 현재 눌려있는 키 상태 추적
pressed_keys = {
    SDLK_RIGHT: False,
    SDLK_LEFT: False,
    SDLK_SPACE: False,
    SDLK_LSHIFT: False,
    SDLK_d: False
}

def update_key_state(event):
    """이벤트를 받아서 키 상태를 업데이트"""
    if event.type == SDL_KEYDOWN:
        if event.key in pressed_keys:
            pressed_keys[event.key] = True
    elif event.type == SDL_KEYUP:
        if event.key in pressed_keys:
            pressed_keys[event.key] = False

def is_key_pressed(key):
    """특정 키가 현재 눌려있는지 확인"""
    return pressed_keys.get(key, False)

def is_right_pressed():
    """오른쪽 키가 눌려있는지 확인"""
    return pressed_keys[SDLK_RIGHT]

def is_left_pressed():
    """왼쪽 키가 눌려있는지 확인"""
    return pressed_keys[SDLK_LEFT]

def is_space_pressed():
    """스페이스 키가 눌려있는지 확인"""
    return pressed_keys[SDLK_SPACE]

def space_down(e): # e is space down ?
    print('sape down event detected')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def right_down(e):
    print('right down event detected')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    print('right up event detected')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    print('left down event detected')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    print('left up event detected')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def lshift_down(e):
    print('left shift down event detected')
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

def is_lshift_pressed():
    """왼쪽 쉬프트 키가 눌려있는지 확인"""
    return pressed_keys[SDLK_LSHIFT]

def is_d_pressed():
    """D 키가 눌려있는지 확인"""
    return pressed_keys[SDLK_d]

