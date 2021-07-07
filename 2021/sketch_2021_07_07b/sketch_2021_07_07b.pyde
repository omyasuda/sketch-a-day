from __future__ import print_function, division
import pickle

from graph import Graph
from grid import Grid, dim_grid

thread_running = False
viz_stat = False
selected_v = None
mode = 0
modes = ("move", "connect", "disconnect", "path", "swap")
found_path = []
NUM = 4 * 4

def setup():
    size(600, 600)
    textAlign(CENTER, CENTER)
    f = createFont("Source Code Pro Bold", 12)
    textFont(f)
    global graph, margin, w, h, cols, rows
    graph = Graph.empty_graph(range(NUM))
    margin = width / 40
    cols, rows = dim_grid(len(graph))
    w, h = (width - margin * 2) / cols, (height - margin * 2) / rows
    setup_grid(cols, rows)

def setup_grid(cols, rows):
    global grid
    # create grid postions for graph vertices
    grid = Grid(graph, cols, rows)
    print("Cyclic: " + str(graph.is_cyclic()))
    global gx, gy
    gx, gy = 0, 100


def draw():
    colorMode(RGB)
    background(128)

 
    for xa, ya, xb, yb, za, zb in grid.edge_coords():
        stroke(2)
        line(margin + w / 2 + xa * w,
             margin + h / 2 + ya * w,
             margin + w / 2 + xb * w,
             margin + h / 2 + yb * w,
             )
        strokeWeight(1)
        colorMode(HSB)
        fill(za * 8, 255, 255)
        circle(margin + w / 2 + xa * w,
               margin + h / 2 + ya * h, za * 5)

        fill(zb * 8, 255, 255)
        circle(margin + w / 2 + xb * w,
               margin + h / 2 + yb * h, zb * 5)        
                             
    if selected_v:
        i, j = grid[selected_v]
        stroke(255)
        strokeWeight(5)
        line(margin + w / 2 + i * w,
             margin + h / 2 + j * h, mouseX, mouseY)


    for v in grid.keys():
        x, y = grid[v]
        stroke(255)
        if v == selected_v:
            fill(0)
        elif mouse_near(v):
            fill(128)
        elif v in found_path:
            fill(0, 255, 0)
        else:
            noFill()
        strokeWeight(1)
        circle(margin + w / 2 + x * w,
               margin + h / 2 + y * h, 10)
        if viz_stat:
            colorMode(RGB)
            fill(255, 0, 0)
            text("{}:{}".format(v, graph.vertex_degree(v)).upper(),
                 margin + w / 2 + x * w, 
                 margin + h / 2 + y * h)

    fill(255)
    text(modes[mode], 40, 40)

def keyTyped():
    global gx, gy, viz_stat, grid, graph, mode
    if key  == ' ':
        mode = (mode + 1) % len(modes)
    elif key == 'r':
        setup_grid(cols, rows)
    elif key == 'v':
        viz_stat = not viz_stat
        print(grid.graph)
    elif key == 'p':
        saveFrame("####.png")
    elif key == 'd':
        with open("data/grid.data", "w") as f:
            pickle.dump((graph, grid), f)
            print("dump grid.data")
    elif key == 'l':
        with open("data/grid.data", "rb") as f2:
            graph, grid = pickle.load(f2)
            print("load grid.data")


def mouse_near(v):
    i, j = grid[v]
    return dist(margin + w / 2 + i * w,
                margin + h / 2 + j * h, mouseX, mouseY) < 20

def mousePressed():
    global selected_v
    for v in grid.keys():
        if mouse_near(v):
            selected_v = v
            return

def mouseDragged():
    if selected_v and mode == 0: # move
        dx = mouseX - pmouseX
        dy = mouseY - pmouseY
        i, j = grid[selected_v]
        i += dx / float(w)
        j += dy / float(h)
        grid[selected_v] = [i, j]
        print(grid[selected_v])
        

def mouseReleased():
    global selected_v
    if selected_v and mode == 1:  # connect
        for v in grid.keys():
            if mouse_near(v):
                grid.graph.add_edge((v, selected_v))
                
    if selected_v and mode == 2:  # disconnect
        for v in grid.keys():
            if mouse_near(v):
                grid.graph.remove_edge((v, selected_v))

    if selected_v and mode == 3:  # path
        for v in grid.keys():
            if mouse_near(v):
                path = grid.graph.find_shortest_path(v, selected_v)
                if path:
                    found_path[:] = path
                
                                                
    if selected_v and mode == 4:  # swap
        for v in grid.keys():
            if mouse_near(v):
                grid[selected_v], grid[v] = grid[v], grid[selected_v]

    
    
    
    
    selected_v = None
    
    
    
    
    
