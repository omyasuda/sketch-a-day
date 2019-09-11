from __future__ import division


def setup():
    size(600, 600)
    blendMode(MULTIPLY)
    rectMode(CENTER)
    noStroke()
    noLoop()
    global ox, oy
    ox, oy = 0 , 0

        
def draw():
    colorMode(RGB)
    background(240, 240, 220)
    rec_grid(width / 2, height / 2, 2, 580)
    
def rec_grid(x, y, n, tw):

    pushMatrix()
    translate(x, y)
    cw = tw / n
    margin = (cw - tw) / 2

    for i in range(n):
        nx = cw * i + margin
        for j in range(n):
            ny = cw * j + margin
            if cw > 8 and random(10) < 8.5:
                rec_grid(nx, ny, 2, cw)
            elif cw < 8:
                colorMode(HSB)
                c = map(cw, 5, width / 4, 0, 250)
                fill(c, 200, 255)
                noStroke()
                # circle(nx, ny, cw - 2)                
                global ox, oy
                stroke(dist(ox, oy, nx, ny)/ 5., 255, 255)
                line(ox, oy, nx, ny)
                ox += x
                oy += y  

 
                                
    popMatrix()

    
    
def keyPressed():
    saveFrame("####.png")
    redraw()
    global ox, oy
    ox, oy = 0 , 0
    
    
    
