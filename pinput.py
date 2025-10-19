from pico2d import *

key_state = {}
button_state = {}
time = 0


def process_input(events):
    global time
    time += 1
    for event in events:
        if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
            key_state[event.key] = (event.type, time)
        elif event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP:
            button_state[event.button] = (event.type, time)

def key_pressed(key):
    """현재 키가 눌려있는지 확인"""
    if key not in key_state:
        return False
    return key_state[key][0] == SDL_KEYDOWN

def get_keydown(key):
    if key not in key_state:
        return False
    return key_state[key][0] == SDL_KEYDOWN and key_state[key][1] == time

def get_keyup(key):
    if key not in key_state:
        return False
    return key_state[key][0] == SDL_KEYUP and key_state[key][1] == time

def get_buttondown(button):
    if button not in button_state:
        return False
    return button_state[button][0] == SDL_MOUSEBUTTONDOWN and button_state[button][1] == time

def get_buttonup(button):
    if button not in button_state:
        return False
    return button_state[button][0] == SDL_MOUSEBUTTONUP and button_state[button][1] == time
