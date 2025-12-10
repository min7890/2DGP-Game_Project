from pico2d import *
import game_framework
import title_mode as start_mode
# import stage_boss as start_mode

#플레이어는 1 픽셀당 3cm
#w = 1280픽셀 * 3cm = 3840cm = 38.4m
#h = 720픽셀 * 3cm = 2160cm = 21.6m

# open_canvas(1280, 720)
open_canvas(600, 600)
game_framework.run(start_mode)
close_canvas()