from pico2d import *

key_state = {}
button_state = {}


def process_input(events):
    for event in events:
        if event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
            key_state[event.key] = (event.type)
        elif event.type == SDL_MOUSEBUTTONDOWN or event.type == SDL_MOUSEBUTTONUP:
            button_state[event.button] = (event.type)
    pass

def get_keydown(key):
    if key not in key_state:
        return False
    return key_state[key][0] == SDL_KEYDOWN

def get_keyup(key):
    if key not in key_state:
        return False
    return key_state[key][0] == SDL_KEYUP

def get_buttondown(button):
    if button not in button_state:
        return False
    return button_state[key][0] == SDL_MOUSEBUTTONDOWN

def get_buttonup(button):
    if button not in button_state:
        return False
    return button_state[key][0] == SDL_MOUSEBUTTONUP
