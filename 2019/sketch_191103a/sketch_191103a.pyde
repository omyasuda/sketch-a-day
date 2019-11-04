# Baseado no L-System apresentado pela Tatasz na
# Noite de Processing
# baseado no PentigreeLSystem do exemplo do Processing

iterations = 5
# axiom = "F"
axiom = "F-F-F-F-F"
sentence = axiom
stroke_len = 100
rules = (
         ("F", "F-F++F+F-F-F")
         # ("F", "F+F-F"),
         # ("F", "[+G-F]-G+F"),
         # ("G", "GHG"),
         # ("H", "H-FH")
         ,)
a = 72

def setup():
    size(700, 700)
    strokeWeight(1)
    generate(iterations)
    
def draw():
    global a
    background(220, 220, 200)    
    translate(width / 8, height / 8)
    global a    
    angle = radians(a)
    plot(angle)
    # if a <= 180:
    #     saveFrame("sketch###.png")
    #     print a
    #     a += 2.5
        

def generate(n):
    global stroke_len, sentence
    for c in range(n):
        stroke_len *= 0.5
        nextSentence = ""
        for c in sentence:
            found = False
            for c_a, c_b in rules:
                if c == c_a:
                    found = True
                    nextSentence += c_b
                    break
            if not found:
                nextSentence += c
        sentence = nextSentence

def plot(angle):
    for c in sentence:
        if c == "F":
            # stroke(255, 0, 0)
            line(0, 0, 0, -stroke_len)
            translate(0, -stroke_len)
         # ellipse(0, 0, 10, 10)
        elif c == "G":
            stroke(0, 0, 200)
            line(0, 0, 0, -stroke_len)
            translate(0, -stroke_len)
        elif c == "H":
            stroke(0, 200, 0)
            line(0, 0, 0, -stroke_len)
            translate(0, -stroke_len)
        elif c == "+":
            rotate(angle)
        elif c == "-":
            rotate(-angle)
        elif c == "[":
            pushMatrix()
        elif c == "]":
            popMatrix()
  
def keyPressed():
    global a
    if keyCode == LEFT:
        a -= 5
    if keyCode == RIGHT:
        a += 5        
    if key == 's':
        saveFrame("####.png")
                      
                                          
def settings():
    """ print markdown to add at the sketch-a-day page"""
    from os import path
    global SKETCH_NAME, OUTPUT
    SKETCH_NAME = path.basename(sketchPath())
    OUTPUT = ".png"
    println(
        """
![{0}]({2}/{0}/{0}{1})

[{0}](https://github.com/villares/sketch-a-day/tree/master/{2}/{0}) [[Py.Processing](https://villares.github.io/como-instalar-o-processing-modo-python/index-EN)]
""".format(SKETCH_NAME, OUTPUT, year())
    )
