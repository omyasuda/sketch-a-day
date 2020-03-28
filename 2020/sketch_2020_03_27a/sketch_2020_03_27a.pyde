# Other L-System

iterations = 7
stroke_len = 2600
angle_deg = 45
axiom = 'L'
sentence = axiom
rules = {
    # 'L': '+RF-LFL-FR+',
    # 'R': '-LF+RFR+FL-',
    'L': '+RF[-RFR]-FR+',
    'R': '-LF[+LFL]+FL-',
}

def setup():
    size(700, 700)
    global xo, yo
    xo, yo = width / 2, height / 2 - 20
    strokeWeight(0.2)
    noFill()
    generate(iterations)

def draw():
    background(0)
    translate(xo, yo)
    plot(radians(angle_deg))

def generate(n):
    global stroke_len, sentence
    for _ in range(n):
        stroke_len *= 0.5
        next_sentence = ''
        for c in sentence:
            next_sentence += rules.get(c, c)
        sentence = next_sentence

def plot(angle):
    for c in sentence:
        if c == 'F':
            stroke(255)
            line(0, 0, 0, -stroke_len)
            translate(0, -stroke_len)
        elif c == '+':
            rotate(angle)
        elif c == '-':
            rotate(-angle)
        elif c == '[':
            pushMatrix()
        elif c == ']':
            popMatrix()

def keyPressed():
    global angle_deg, xo, yo, stroke_len
    if key == '-':
        angle_deg -= 5
        print(angle_deg)
    if str(key) in "=+":
        angle_deg += 5
        print(angle_deg)
    if key == 's':
        saveFrame('####.png')
    if key == 'a':
        stroke_len *= 2
    if key == 'z':
        stroke_len /= 2
    if keyCode == LEFT:
        xo -= 50
    if keyCode == RIGHT:
        xo += 50
    if keyCode == UP:
        yo -= 50
    if keyCode == DOWN:
        yo += 50
