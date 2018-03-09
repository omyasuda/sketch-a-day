"""
sketch 67 180308 - Alexandre B A Villares
https://abav.lugaralgum.com/sketch-a-day
"""

def setup():
    size(400, 400)
    colorMode(HSB)
    strokeWeight(5)
    noFill()
    
def draw():
    background(0)
    N = map(mouseX, 0, width, QUARTER_PI/2, HALF_PI)
    D = map(mouseY, 0, height, 1, 5)
    poly_shape(width/2, height/2, N, D)
            
            
def poly_shape(x, y, angle, D):
        stroke((frameCount/10 * D) % 256, 255, 255, 100)
        with pushMatrix():
            translate(x, y)
            radius = 5 + D * 20 
            ps = createShape()
            ps.beginShape()
            a = 0
            while a < TWO_PI:
                sx = cos(a) * radius
                sy = sin(a) * radius
                ps.vertex(sx, sy)
                a += angle
            ps.endShape(CLOSE)
            shape(ps, 0, 0);
            if D > 1:
               for i in range(ps.getVertexCount()):
                   pv = ps.getVertex(i) # PVector
                   poly_shape(pv.x, pv.y, angle, D-1)
