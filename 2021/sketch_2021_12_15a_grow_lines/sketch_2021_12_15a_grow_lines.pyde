from random import choice

def setup():
    size(600, 600)
    generate_lines()

def generate_lines():
    global glines
    def rw(): 
        return choice(range(50, width, 100)) #10, 40, 70,.... 790. 
    def ro(): 
        return choice((-5, 0, 5))
    glines = []
    while len(glines) < 10:
        x, y = rw(), rw()
        gl = GrowingLine((x, y), (x + ro(), y + ro()))
        for other_gl in glines:
            if gl.simple_intersect(other_gl):
                break
        else:
            glines.append(gl)    

def draw():
    background(255)
    for gl in reversed(glines):
        for other_gl in glines:
            gl.check_collision(other_gl)
        gl.draw()
        gl.check_screen_limit()
        gl.grow()

def keyPressed():
    if key == ' ':
        generate_lines()


class GrowingLine():

    def __init__(self, a, b, generation=5):
        self.a = PVector(*a)
        self.b = PVector(*b)
        self.grow_a = True
        self.grow_b = True
        self.v = PVector(*self.a) - PVector(*self.b)
        self.v.normalize()
        self.generation = generation
        
    def tamanho(self):
        return PVector.dist(self.a, self.b)

    def draw(self):
        strokeWeight(1 + self.generation / 10.0)
        line(self.a.x, self.a.y, self.b.x, self.b.y)

    def grow(self):
        if self.grow_a:
            self.a += self.v #/ 2.0
        if self.grow_b:
            self.b -= self.v #/ 2.0
            
        if random(100) < 1:
            self.new_line(0.3, invert=choice((True, False)))

    def new_line(self, t, invert=False):
        if self.generation >= 0:
            p = self.ponto_na_linha(1 - t if invert else t)
            p2 = self.ponto_fora(p, invert)
            self.generation -= 1
            gl = GrowingLine(p, p2, self.generation)
            glines.append(gl)
            

    def check_collision(self, other):
        if self is not other:
            if self.grow_a and other.contains_point(self.a.x,
                                                    self.a.y,
                                                    tolerance=0.01):
                self.grow_a = False
            if self.grow_b and other.contains_point(self.b.x,
                                                    self.b.y,
                                                    tolerance=0.01):
                self.grow_b = False
                

    def check_screen_limit(self):
        if self.grow_a and not point_in_screen(self.a):
            self.grow_a = False
        if self.grow_b and not point_in_screen(self.b):
            self.grow_b = False
            
    def contains_point(self, x, y, tolerance=0.1):
        return point_over_line(x, y,
                               self.a.x, self.a.y,
                               self.b.x, self.b.y,
                               tolerance)
        
    def simple_intersect(self, other): #Interseção
        a1, b1 = self.a, self.b
        a2, b2 = other.a, other.b
        return ccw(a1, b1, a2) != ccw(a1, b1, b2) and ccw(a2, b2, a1) != ccw(a2, b2, b1)
    
    def ponto_na_linha(self, t): #Ponto na superfício da linha
        return PVector.lerp(self.a, self.b, t)  
    
    def angulo(self):
        ax, ay = self.a.x, self.a.y
        bx, by = self.b.x, self.b.y
        return atan2(by-ay, bx-ax) 
    
    def ponto_fora(self, p, invert=False):
        d = 10 
        if invert:
            a = self.angulo() - PI
        else: 
            a = self.angulo()
        x = p.x + d * cos(a + HALF_PI)
        y = p.y + d * sin(a + HALF_PI)
        return PVector(x, y)        
                
def ccw(a, b, c):
    """Returns True if the points are arranged counter-clockwise in the plane"""
    return (b[0] - a[0]) * (c[1] - a[1]) > (b[1] - a[1]) * (c[0] - a[0])


def point_over_line(px, py, lax, lay, lbx, lby,
                    tolerance=0.1):
    """
    Check if point is over line using the sum of
    the distances from the point to the line ends
    (the result has to be near equal for True).
    """
    ab = dist(lax, lay, lbx, lby)
    pa = dist(lax, lay, px, py)
    pb = dist(px, py, lbx, lby)
    return (pa + pb) <= ab + tolerance

def point_in_screen(*args):
    if len(args) == 1:
        x, y = args[0][0], args[0][1]
    else:
        x, y = args[0], args[1]
    return 0 <= screenX(x, y) <= width and 0 <= screenY(x, y) <= height
