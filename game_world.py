world = [[] for _ in range(4)]



def add_object(o, depth = 0):
  world[depth].append(o)

def add_objects(ol, depth = 0):
  world[depth].append += ol

def update():
  for layer in world:
    for o in layer:
      o.update()

def render():
  for layer in world:
    for o in layer:
      o.draw()