# Alexandre B A Villares - https://abav.lugaralgum.com/
# To run this you will need Processing 3.5.4 + Python mode, instructions at: 
# https://abav.lugaralgum.com/como-instalar-o-processing-modo-python/index-EN.html

"""
triangle pairs on 6 hexagon vertices with no more than 1 point in common: 100
"""

from itertools import product, combinations, permutations
from villares.line_geometry import poly_edges, simple_intersect

space, border = 50, 50
colors = (
    color(0, 200, 0),
    color(0, 0, 200, 128),
    color(200, 0,0, 128),
    )

def setup():
    global coords
    size(100 + 16 * 50, 100 + 12* 50)
    strokeJoin(ROUND)
    points = list(range(6))
    triangles = list(combinations(points, 3))
    coords = hex_points(0, 0, 1)
    tri_combos = set(map(TriCombo, combinations(triangles, 3)))
    tri_combos = sorted(tri_combos,
                        key=lambda c: sum(map(tri_area, c)),
                        reverse=True
                        )
    println("Number of triangle combinations: {}".format(len(tri_combos)))
    W = (width - border * 2) // space
    H = (height - border * 2) // space
    println("Cols: {} Rows: {} Visible grid: {}".format(W, H, W * H))
    background(200)
    for y in range(H):
        for x in range(W):
            if len(tri_combos):
                pushMatrix()
                translate(border / 2 + space + space * x,
                          border / 2 + space + space * y)
                tri_combos.pop().draw()
                popMatrix()

    saveFrame('combos.png')

def hex_points(x, y, tamanho):
    return [(x + tamanho * cos(PI / 180 * 60 * i),
             y + tamanho * sin(PI / 180 * 60 * i))
             for i in range(6)]
    
def tri_area(t):
    a, b, c = t
    ax, ay = coords[a]
    bx, by = coords[b]
    cx, cy = coords[c]
    return abs(bx * (cy - ay) +
              cx * (ay - by) +
              ax * (by - cy))
                
class TriCombo:
    def __init__(self, triangles):
        self.triangles = tuple(sorted(tuple(sorted(tri)) for tri in triangles))
    
    def __getitem__(self, i):
        return self.triangles[i]
    
    def __iter__(self):
        return iter(self.triangles)
    
    def draw(self):
        noStroke()
        siz = space / 2.5
        for tri, c in zip(self, colors):
            fill(c)
            p0, p1, p2 = tri
            (x0, y0), (x1, y1), (x2, y2) = coords[p0], coords[p1], coords[p2]
            triangle(x0 * siz, y0 * siz,
                    x1 * siz, y1 * siz,
                    x2 * siz, y2 * siz)
            
    def __eq__(self, other):
        return hash(self) == hash(other)
            
    def __hash__(self):
        r = self
        h = hash(self.triangles)        
        for _ in range(5):
            r = r.rotate()
            rh = hash(r.triangles)
            h = min(h, rh)
        return h
    
    def rotate(self):
        return TriCombo(((a + 1) % 6, (b + 1) % 6, (c + 1) % 6)
                        for a, b, c in self)
