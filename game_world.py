world = [[] for _ in range(4)]

################################# ADD & DEL OBJECT #################################

def add_object(o, depth = 0):
  world[depth].append(o)

def add_objects(ol, depth = 0):
  world[depth] += ol

def remove_object(o):
  for layer in world:
    if o in layer:
      layer.remove(o) # list.remove : Remove in "GAME WORLD"
      remove_collision_object(o) # Remove in "COLLISION SYSTEM"
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

################################# COLLISION #################################
collision_pairs = {} # {key: [[], []]}

#group(str key) : "boy:ball", "boy:zombie" ...
def add_collision_pair(group, a, b):
  if group not in collision_pairs:
    collision_pairs[group] = [ [], [] ]
  if a:
    collision_pairs[group][0].append(a)
  if b:
    collision_pairs[group][1].append(b)

def remove_collision_object(o):
  for pairs in collision_pairs.values(): # dict에서 value만 추출
    if o in pairs[0]:
      pairs[0].remove(o)
    if o in pairs[1]:
      pairs[1].remove(o)

def collide(a, b):
  for bb in a.get_bb():
    la, ba, ra, ta = bb
  for bb in b.get_bb():
    lb, bb, rb, tb = bb

  if la > rb: return False
  if ra < lb: return False
  if la > rb: return False
  if la > rb: return False

  return True

def handle_collisions():
  for group, pairs in collision_pairs.items():
    for a in pairs[0]:
      for b in pairs[1]:
        if collide(a,b):
          a.handle_collision(group, b)
          b.handle_collision(group, a)
