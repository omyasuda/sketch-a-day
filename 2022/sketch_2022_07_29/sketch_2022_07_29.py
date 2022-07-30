import random  # import sample, shuffle, seed
from villares.helpers import save_png_with_src

nodes = {}
unvisited_nodes = []
step = 6
NBS = (
    (-2, -2), (-2,  0),
    (-2,  2), ( 0, -2),
    ( 0,  2), ( 2, -2),
    ( 2,  0), ( 2,  2)
)
nbs = []
ox = oy = 0
def setup():
    global w, h
    size(800, 800)
    no_smooth()
    w, h = int(width / 2 / step - 5), int(height / 2 / step - 5)
    stroke_weight(2)
    start(266)

def start(rnd_seed):
    global s
    s = rnd_seed
    random.seed(rnd_seed)
    nbs[:] = NBS
    random.shuffle(nbs)
    nodes.clear()
    unvisited_nodes[:] = []
    x1, y1 = random.randint(-w, w), random.randint(-h, h)
    unvisited_nodes.extend((
        (x1, y1),
        (x1 + 1, y1 + 0),
    ))

def draw():
    background(200)
    translate(width / 2 + ox * step, height / 2 + oy * step)
    for n, v in nodes.items():
        xa, ya = n
        xb, yb, c, g = v
        if visible(xa, ya) and visible(xb, yb):
            stroke((240, 128, 64, 0)[c % 4])
            line(xa * step, ya * step, xb * step, yb * step)
    grow()

def key_pressed():
    if key == ' ':
        print(frame_count)
        start(frame_count)
    elif key == 's':
        save_png_with_src(f'seed{s}')

def visible(x, y):
    return (abs((x + ox) * step) < width / 2 - step * 5 and
            abs((y + oy) * step) < height / 2 - step * 5)
def grow():
    new_nodes = []
    while unvisited_nodes:
        x, y = unvisited_nodes.pop()
        _, _, c, g = nodes.get((x, y), (0, 0, len(unvisited_nodes), 0))
        if not visible(x, y):
            new_nodes.append((x, y))
            continue
        random.seed(g // 13 + c)
        xnbs = random.sample(nbs, random.randint(4, 6))
        for nx, ny in xnbs:
            xnx, yny = x + nx, y + ny
            if (xnx, yny) not in nodes:
                nodes[(xnx, yny)] = (x, y, c, g + 1)
                new_nodes.append((xnx, yny))
    unvisited_nodes[:] = new_nodes
