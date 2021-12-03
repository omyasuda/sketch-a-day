def setup():
    size(550, 550)
    noCursor()
    strokeWeight(5)
    # frameRate(2)

def draw():
    background(240)
    tri_a = (500, 200), (250, 500),  (100, 100)
    r = 100
    f = frameCount
    tri_b = [(mouseX + r * cos(radians(a)), mouseY + r * sin(radians(a)))
            for a in (0 + f, 120 + f, 240 + f)]
    if tri_over_tri(tri_b, tri_a):
        fill(0, 200, 0)
    else:
        fill(0, 0, 200)
    (xa, ya), (xb, yb), (xc, yc) = tri_a
    noStroke()
    triangle(xa, ya, xb, yb, xc, yc)
    stroke(0)
    noFill()
    (xa, ya), (xb, yb), (xc, yc) = tri_b
    triangle(xa, ya, xb, yb, xc, yc)

def tri_over_tri(tri_a, tri_b):
    for x, y in tri_b:
        if point_in_triangle(x, y, tri_a):
            return True
    for x, y in tri_a:
        if point_in_triangle(x, y, tri_b):
            return True
    return False

def point_in_triangle(x, y, tri):
    (ax, ay), (bx, by), (cx, cy) = tri
    ab = (x - bx) * (ay - by) - (ax - bx) * (y - by)
    bc = (x - cx) * (by - cy) - (bx - cx) * (y - cy)
    ca = (x - ax) * (cy - ay) - (cx - ax) * (y - ay)
    return (ab < 0) == (bc < 0) == (ca < 0)

def triangle_area(a, b, c):
    return abs(a[0] * (b[1] - c[1]) +
               b[0] * (c[1] - a[1]) +
               c[0] * (a[1] - b[1]))
