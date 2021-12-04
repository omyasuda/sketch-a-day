# Alexandre B A Villares - https://abav.lugaralgum.com/
# To run this you will need Processing 3.5.4 + Python mode, instructions at: 
# https://abav.lugaralgum.com/como-instalar-o-processing-modo-python/index-EN.html

"""
628 triangle pairs (with no points in common), on a 3x3 grid
"""

from itertools import product, combinations, permutations

space, border = 20, 20

def setup():
    global tri_combos, W, H, position, num
    size(490 * 2 + 40, 140 * 2 + 40) # 49 x 14 
    strokeJoin(ROUND)
    grid = product(range(-1, 2), repeat=2)  # 3X3
    # all triple point combinations on a grid
    points = list(combinations(grid, 3))
    # filter out colinear triples
    triangles = []
    for p in points:
        area = (p[1][0] * (p[2][1] - p[0][1]) +
                p[2][0] * (p[0][1] - p[1][1]) +
                p[0][0] * (p[1][1] - p[2][1]))
        if area != 0:
            triangles.append(p)
    println("Number of possible triangles: {}".format(len(triangles)))
    all_combos = list(combinations(triangles, 2))
    tri_combos = [(ta, tb) for ta, tb in all_combos
                  if len(set(ta) | set(tb)) == 6]
    
    println("Number of triangle combinations: {}".format(len(tri_combos)))
    ## Ucomment the following lines to shuffle!
    # from random import shuffle
    # shuffle(tri_combos)
    W = (width - border * 2) // space
    H = (height - border * 2) // space
    println("Cols: {} Rows: {} Visible grid: {}".format(W, H, W * H))

    background(240)
    i = 0
    for y in range(H):
        for x in range(W):
            if i < len(tri_combos):
                pushMatrix()
                translate(border / 2 + space + space * x,
                          border / 2 + space + space * y)
                draw_combo(i)
                popMatrix()
                i += 1

def draw_combo(n):
    noFill()
    siz = space / 3
    for i, sl in enumerate(tri_combos[n]):
        colors = (color(0, 128, 0), color(0, 50, 128))
        stroke(colors[i])
        (x0, y0), (x1, y1), (x2, y2) = sl[0], sl[1], sl[2]
        triangle(x0 * siz, y0 * siz,
                 x1 * siz, y1 * siz,
                 x2 * siz, y2 * siz)
