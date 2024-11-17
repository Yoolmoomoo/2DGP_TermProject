world = [[] for _ in range(4)]

################################# ADD & DEL OBJECT #################################

def add_object(o, depth = 0):
  world[depth].append(o)

def add_objects(ol, depth = 0):
  world[depth].append += ol

def remove_object(o):
  for layer in world:
    if o in layer:
      layer.remove(o) # list.remove : Remove in "GAME WORLD"
      #remove_collision_object(o) # Remove in "COLLISION SYSTEM"
      del o
      return
  raise ValueError('Cannot delete non existing object')

################################# UPDATE & RENDER #################################
def update():
  for layer in world:
    for o in layer:
      o.update()

def render():
  for layer in world:
    for o in layer:
      o.draw()