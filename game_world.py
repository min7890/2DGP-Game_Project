world = [[] for _ in range(4)]

def add_object(o, depth = 0):
    world[depth].append(o)


def add_objects(ol, depth = 0):
    world[depth] += ol


def update():
    for layer in world:
        for o in layer:
            o.update()


def render():
    for layer in world:
        for o in layer:
            o.draw()


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            return

    raise ValueError('Cannot delete non existing object')


def clear():
    global world, collision_pairs

    for layer in world:
        layer.clear()
    collision_pairs.clear()


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True # 충돌 발생

def detection_collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_detection_bb()
    left_b, bottom_b, right_b, top_b = b.get_detection_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True # 충돌 발생

collision_pairs = {}
detection_collision_pairs = {}

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def add_detection_collision_pair(group, a, b):
    if group not in detection_collision_pairs:
        detection_collision_pairs[group] = [ [], [] ]
    if a:
        detection_collision_pairs[group][0].append(a)
    if b:
        detection_collision_pairs[group][1].append(b)

def remove_collision_pair(group, a, b):
    if group not in collision_pairs:
        return
    if a and a in collision_pairs[group][0]:
            collision_pairs[group][0].remove(a)
    if b and b in collision_pairs[group][1]:
            collision_pairs[group][1].remove(b)

def remove_detection_collision_pair(group, a, b):
    if group not in detection_collision_pairs:
        return
    if a and a in detection_collision_pairs[group][0]:
            detection_collision_pairs[group][0].remove(a)
    if b and b in detection_collision_pairs[group][1]:
            detection_collision_pairs[group][1].remove(b)

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0][:]:
            for b in pairs[1][:]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)

def handle_detection_collisions():
    for group, pairs in detection_collision_pairs.items():
        for a in pairs[0][:]:
            for b in pairs[1][:]:
                if detection_collide(a, b):
                    a.handle_detection_collision(group, b)
                    b.handle_detection_collision(group, a)

