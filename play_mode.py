from pico2d import *
import game_framework

import game_world
import over_mode, title_mode, loading_mode
from map import Map, Ground
from luffy import Luffy
from naruto import Naruto

def pause():
  pass
def resume():
  pass

def init():
  open_canvas(1000, 700) # 1000 700
  global luffy, naruto, play_mode_end, end_time, map, load_flag, start_time, ai_time, win_flag

  load_flag = False
  win_flag = -1
  play_mode_end = False
  end_time = 0

  map = Map()
  game_world.add_object(map,0)

  grounds = [Ground(x*70) for x in range(15)]
  game_world.add_objects(grounds, 1)

  naruto = Naruto()
  game_world.add_object(naruto, 2)

  luffy = Luffy()
  game_world.add_object(luffy, 2)

  ##### 충돌 페어 등록 #####
  game_world.add_collision_pair('luffy:map', luffy, map)
  game_world.add_collision_pair('luffy:naruto', luffy, naruto)

  start_time = get_time()
  ai_time = get_time()

def handle_events():
  events = get_events()
  for event in events:
    if event.type == SDL_QUIT:
      game_framework.quit()
    elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
      game_framework.quit()
    else:
      luffy.handle_event(event)


def update():
  global play_mode_end, end_time, win_flag
  game_world.update()
  game_world.handle_collisions() ##### 충돌 감지 #####

  if play_mode_end == True and get_time()-end_time > 5.0:
    game_framework.change_mode(over_mode)
    pass

  if naruto.hp <= 0 and luffy.state_flag != 'Win':
    luffy.state_machine.add_event(('WIN', 0))
    end_time = get_time()
    play_mode_end = True
    if win_flag == -1:
      win_flag = 1


def draw():
  global load_flag, start_time
  clear_canvas()
  game_world.render()
  # if load_flag == False:
  #   game_framework.push_mode(loading_mode)
  #   load_flag = True

  update_canvas()

def finish():
  global luffy, naruto, map, grounds
  game_world.remove_object(map)
  game_world.remove_object(luffy)
  game_world.remove_object(naruto)
  close_canvas()
  # game_world.update()

