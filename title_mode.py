import game_framework
from pico2d import load_image, get_events, update_canvas, clear_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MouseButtonEvent
import play_mode

def init():
  pass

def finish():
  global image
  del image

