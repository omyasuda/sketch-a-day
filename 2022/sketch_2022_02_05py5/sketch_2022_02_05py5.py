import py5   
import pymunk
from random import randint, sample, choice

space = pymunk.Space() # create a new space for your simulation
space.gravity = (0, 400)
BOX_NUMBER = 30

def setup():
    global initial_shape_count
    py5.size(500, 600)
    py5.color_mode(py5.HSB)
    pymunk.Poly.draw = draw_box  # this is called "monkeypatching"
    pymunk.Circle.draw = draw_ball
    pymunk.Segment.draw = draw_seg
    mw, mh = py5.width, py5.height
    segments = [
        ((0, 0), (0, mh)), 
        ((mw, 0), (mw, mh)),
        ((0, mh), (mw, mh)),
    ] 
    for point_a, point_b in segments:
        s = pymunk.Segment(space.static_body, point_a, point_b, 5)
        s.elasticity = 1
        space.add(s)
    for point_a, point_b in (((x, mh), (x, mh * 0.75)) for x in range(25, mw, 25)):
        s = pymunk.Segment(space.static_body, point_a, point_b, 1)
        s.elasticity = 1
        space.add(s)
    initial_shape_count = len(space.shapes)
    populate_boxes()

def draw():
    py5.background(150)
    py5.no_stroke()
    for obj in space.shapes:
        obj.draw()
    space.step(1/py5.get_frame_rate()) # advance simulation step
    if py5.is_key_pressed and py5.key_code == py5.SHIFT:
        add_balls()
    if py5.is_mouse_pressed and py5.mouse_button == py5.RIGHT:
        add_balls()
    for obj in reversed(space.shapes):
        if obj.body.position.y > py5.height + 10:
            space.remove(obj)
    print(len(space.shapes))

def populate_boxes():
    while len(space.shapes) < initial_shape_count + BOX_NUMBER:
        x, y = randint(0, py5.width), randint(100, py5.height * 0.70)
        if all(map(lambda obj:  obj.point_query((x, y)).distance > 40,
                   space.shapes)):
            create_box(x, y)
   
def add_balls():
    create_ball(py5.mouse_x + randint(0, 1), py5.mouse_y)
   
def create_box(x, y):
    body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    body.position = x, y
    w, h = choice((10, 20, 30, 40)), choice((10, 20, 30, 40)) 
    space.add(body, pymunk.Poly.create_box(body, (w, h)))
    body.angle += py5.radians(randint(-5, 5) * 10)
 
def draw_box(obj):
    py5.push_matrix()
    py5.translate(obj.body.position.x, obj.body.position.y)
    py5.rotate(obj.body.angle)
    pts = obj.get_vertices()
    py5.begin_shape()
    py5.fill((pts[0][0] * pts[0][1]) % 255, 200, 200)
    for x, y in pts:
        py5.vertex(x, y)
    py5.end_shape(py5.CLOSE)
    py5.pop_matrix()

def create_ball(x, y):
    body = pymunk.Body(mass=5, moment=10)
    body.position = x, y
    ball = pymunk.Circle(body, radius=5)
    ball.elasticity = 0.2
    space.add(body, ball)
   

def draw_ball(obj):
    py5.fill(0) #(obj.radius * 10, 255, 255)
    py5.circle(obj.body.position.x, obj.body.position.y, obj.radius * 2)  

def draw_seg(obj): 
    py5.push()
    py5.stroke(255)    
    py5.stroke_weight(obj.radius*2)
    py5.line(obj.a.x, obj.a.y, obj.b.x, obj.b.y)  
    py5.pop()
    
def mouse_dragged():
    for obj in space.shapes:
    #   if is_box(obj):    
         info = obj.point_query((py5.mouse_x, py5.mouse_y))
         if info.distance < 2:
             v = pymunk.Vec2d(py5.mouse_x - py5.pmouse_x,
                              py5.mouse_y - py5.pmouse_y)
             obj.body.position += v

def mouse_wheel(e):
    for obj in space.shapes:
        if is_box(obj):
             info = obj.point_query((py5.mouse_x, py5.mouse_y))
             if info.distance < 2:
                 obj.body.angle += py5.radians(e.getCount())
       
def key_pressed():
    if py5.key == ' ':
        for obj in reversed(space.shapes):
            if is_ball(obj) or is_box(obj):
                space.remove(obj)
        populate_boxes()

def is_ball(obj): return isinstance(obj, pymunk.shapes.Circle)
def is_box(obj): return isinstance(obj, pymunk.shapes.Poly)     

py5.run_sketch()
