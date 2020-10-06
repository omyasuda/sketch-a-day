add_library('peasycam')
import villares.ubuntu_jogl_fix
from random import choice, sample

elements = []
pen = PVector()
origin = PVector()
border = 50

def setup():
    size(500, 500, P3D)
    frameRate(24)
    cam = PeasyCam(this, 400)

def generate(n=500):
    global elements
    # origin.set(width / 2, height / 2)
    pegs = (-20, -10, 0, 0, 10, 20)
    elements = [(choice('LCCRMY'),
                 (choice(pegs), choice(pegs)),
                 choice((1, 3)),)
                for _ in range(n)]

def draw():
    background(240, 240, 220)
    pen.set(origin)
    draw_e(elements)
    check_pen()


def draw_e(els):
    for i, e in enumerate(els):
        stroke(0)
        t, v, w = e
        strokeWeight(w)
        # if t == 'Y':
        if i % 2 == 0:
            rotateY(radians(1))
        # if i % 3 == 0:
        #     rotateX(radians(1))
        if t == 'L':
            line_e(v)
        if t == 'C':
            line_e(v, c=w)
        if t == 'M' and len(els) > 1:
            for _ in range(3):
                line_e(v)
                draw_e([els[i - 2]])
                # trans_e(-els[i - 1][1][0], -els[i - 1][1][1])
                # print(els[i - 3:i - 1])
        if t == 'R' and len(els) > 2:
            for _ in range(3):
                line_e(v)
                line_e((v[1] / 2, -v[0] / 2))
                draw_e([els[i - 1]])


def check_pen():
    # if (border * 1.5 < origin.x < width - border * 1.5
    #         and border * 1.5 < origin.y < height - border * 1.5):
    if pen.x >= width - border:
        origin.x -= 1
    elif pen.x < border:
        origin.x += 1
    elif pen.y >= height - border:
        origin.y -= 1
    elif pen.y < border:
        origin.y += 1
    else:
        generate()

def line_e(v, c=None):
    line(pen.x, pen.y, pen.x + v[0], pen.y + v[1])
    if c is not None:
        d = PVector(v[0], v[1]).mag()
        if c != 1:
            fill(0)
        else:
            noFill()
        circle(pen.x, pen.y, d / c ** 2)
    trans_e(v[0], v[1])

def trans_e(x, y):
    global pen
    pen += PVector(x, y)

def keyPressed():
    if key == ' ':
        generate()
