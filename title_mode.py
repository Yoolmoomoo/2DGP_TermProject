import game_framework
from pico2d import load_image, get_events, update_canvas, clear_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MouseButtonEvent
import play_mode

def init():
  pass

def finish():
  global image
  del image

def handle_events():
  events = get_events()
  for event in events:
    if event.type == SDL_QUIT:
      game_framework.quit()
    elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
      game_framework.quit()
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
      game_framework.change_mode(play_mode)

def draw():
  clear_canvas()
  image.draw(400,300)
  update_canvas()

def update():
  pass

def pause():
  pass

def resume():
  pass