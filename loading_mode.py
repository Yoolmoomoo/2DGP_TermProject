import game_framework
from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE, SDL_MouseButtonEvent
import play_mode, game_world

def init():
  global images, start_time
  images = [
    load_image('./res/ui/3.png'),  # 3
    load_image('./res/ui/2.png'),  # 2
    load_image('./res/ui/1.png'),  # 1
    load_image('./res/ui/fight.png')  # Fight
  ]
  start_time = get_time()
  delay(0.2)


def finish():
  global images
  for image in images:
    del image

def handle_events():
  events = get_events()
  for event in events:
    if event.type == SDL_QUIT:
      game_framework.quit()
    elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
      game_framework.quit()


def draw():
  clear_canvas()
  game_world.render()
  # 현재 시간을 기준으로 어떤 이미지를 그릴지 결정
  elapsed_time = get_time() - start_time
  image_index = int(elapsed_time // 1)  # 1초 간격으로 이미지 교체

  if image_index < len(images):  # 이미지 인덱스가 유효하면 그리기
    images[image_index].draw(500, 350, 300, 300)  # 화면 중앙에 이미지 그리기 (400, 300 좌표는 예시)
  update_canvas()

def update():
  global start_time
  if get_time() - start_time > 4.0:
    game_framework.pop_mode()


def pause():
  pass

def resume():
  pass