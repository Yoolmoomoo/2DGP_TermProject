from pico2d import *
import game_framework
import random
from Map import map
from Luffy import luffy

def handle_events():
  events = get_events()
  for event in events:
    if event.type == SDL_QUIT:
      game_framework.quit()
    elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
      game_framework.quit()
    else:
      luffy.handle_event(event)
