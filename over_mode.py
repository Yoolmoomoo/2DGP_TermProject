import game_framework
from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MouseButtonEvent, SDLK_r
import play_mode, title_mode

def init():
  open_canvas(512, 768)
  global image, click_sound
  image = load_image('./res/map/title.png')
  click_sound = load_wav('./res/sound/click.wav')
  click_sound.set_volume(80)
  # opening_sound = load_music('./res/sound/opening.mp3')
  title_mode.opening_sound.set_volume(32)
  title_mode.opening_sound.play()


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
    elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_r):
      click_sound.play()
      delay(0.5)
      close_canvas()
      game_framework.change_mode(play_mode)

def draw():
  clear_canvas()
  image.draw(256, 384)
  update_canvas()

def update():
  pass

def pause():
  pass

def resume():
  pass